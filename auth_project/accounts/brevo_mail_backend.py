"""
Brevo Email Backend for Django
Sends emails using Brevo transactional email service.
API: https://www.brevo.com/
"""

import json
import logging
from django.core.mail.backends.base import BaseEmailBackend
from django.core.mail.message import sanitize_address
from django.conf import settings
import requests

logger = logging.getLogger(__name__)


class BrevoMailBackend(BaseEmailBackend):
    """
    A Django email backend that uses Brevo API to send emails.
    
    Brevo is a professional transactional email service with:
    - High deliverability rates
    - Built-in tracking and analytics
    - Free tier (300 emails/day)
    - Excellent for OTP and notification emails
    
    Configuration:
        Set BREVO_API_KEY in settings or environment variables
    """

    def __init__(self, api_key=None, fail_silently=False, **kwargs):
        super().__init__(fail_silently=fail_silently, **kwargs)
        
        # Get API key from settings or initialization parameter
        self.api_key = api_key or getattr(settings, 'BREVO_API_KEY', None)
        
        # Brevo API endpoint for sending emails
        self.api_url = 'https://api.brevo.com/v3/smtp/email'
        
        # Validate configuration
        if not self.api_key:
            error_msg = (
                "BREVO_API_KEY setting is required for Brevo backend. "
                "Get your API key from https://www.brevo.com/"
            )
            logger.error(error_msg)
            raise ValueError(error_msg)
        
        # Set up headers for API requests
        self.headers = {
            'Accept': 'application/json',
            'Content-Type': 'application/json',
            'api-key': self.api_key
        }
        
        logger.info("Brevo backend initialized successfully")

    def send_messages(self, email_messages):
        """
        Send one or more EmailMessage objects using Brevo API.
        
        Args:
            email_messages: List of Django EmailMessage objects
            
        Returns:
            int: Number of successfully sent messages
        """
        if not email_messages:
            return 0
        
        sent_count = 0
        
        for message in email_messages:
            try:
                # Prepare payload in Brevo API format
                payload = self._prepare_payload(message)
                
                # Send via Brevo API
                response = requests.post(
                    self.api_url,
                    headers=self.headers,
                    json=payload,
                    timeout=30  # 30 second timeout
                )
                
                # Check response status
                if response.status_code == 201:
                    # 201 Created = Success
                    sent_count += 1
                    logger.info(f"Email sent successfully to {message.to} via Brevo")
                    
                elif response.status_code == 200:
                    # Some versions return 200
                    sent_count += 1
                    logger.info(f"Email sent successfully to {message.to} via Brevo")
                    
                else:
                    # Error response
                    logger.error(f"Brevo API error {response.status_code}: {response.text}")
                    if not self.fail_silently:
                        raise Exception(f"Brevo API error {response.status_code}: {response.text}")
                        
            except requests.exceptions.Timeout:
                logger.error(f"Brevo API timeout for email to {message.to}")
                if not self.fail_silently:
                    raise
                    
            except requests.exceptions.ConnectionError as e:
                logger.error(f"Brevo connection error: {str(e)}")
                if not self.fail_silently:
                    raise
                    
            except Exception as e:
                logger.error(f"Failed to send email to {message.to}: {str(e)}")
                if not self.fail_silently:
                    raise
        
        return sent_count

    def _prepare_payload(self, message):
        """
        Convert Django EmailMessage to Brevo API payload format.
        
        Args:
            message: Django EmailMessage object
            
        Returns:
            dict: Brevo API payload
            
        Brevo API Documentation:
        https://developers.brevo.com/reference/sendtransacemail
        """
        
        # Get sender email
        from_email = sanitize_address(message.from_email, message.encoding)
        
        # Get recipient emails
        to_recipients = [
            sanitize_address(addr, message.encoding) 
            for addr in message.to
        ]
        
        # Build basic payload
        payload = {
            "sender": {
                "name": "UniSinq",
                "email": from_email
            },
            "to": [
                {"email": email, "name": email.split('@')[0]}
                for email in to_recipients
            ],
            "subject": message.subject,
        }
        
        # Handle message content (HTML and Text)
        text_content = message.body
        html_content = None
        
        # Check for HTML alternative
        if hasattr(message, 'alternatives') and message.alternatives:
            for content, mime_type in message.alternatives:
                if mime_type == 'text/html':
                    html_content = content
                elif mime_type == 'text/plain':
                    text_content = content
        
        # Set content
        if html_content:
            payload["htmlContent"] = html_content
        if text_content:
            payload["textContent"] = text_content
        
        # Add CC recipients if present
        if message.cc:
            payload["cc"] = [
                {"email": sanitize_address(addr, message.encoding)}
                for addr in message.cc
            ]
        
        # Add BCC recipients if present
        if message.bcc:
            payload["bcc"] = [
                {"email": sanitize_address(addr, message.encoding)}
                for addr in message.bcc
            ]
        
        # Add reply-to address if specified
        if message.reply_to:
            payload["replyTo"] = {
                "email": sanitize_address(message.reply_to[0], message.encoding)
            }
        
        # Add headers if present
        if message.extra_headers:
            payload["headers"] = message.extra_headers
        
        # Enable click and open tracking
        payload["trackOpens"] = True
        payload["trackClicks"] = True
        
        return payload

    def open(self):
        """
        Open connection.
        Brevo uses REST API so no persistent connection is needed.
        
        Returns:
            bool: Always True
        """
        return True

    def close(self):
        """
        Close connection.
        Brevo uses REST API so no cleanup is needed.
        """
        pass
