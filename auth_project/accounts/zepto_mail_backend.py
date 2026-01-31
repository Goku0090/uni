"""
ZeptoMail Email Backend for Django
Sends emails using ZeptoMail transactional email service.
"""

import json
import logging
from django.core.mail.backends.base import BaseEmailBackend
from django.core.mail.message import sanitize_address
from django.conf import settings
import requests

logger = logging.getLogger(__name__)


class ZeptoMailBackend(BaseEmailBackend):
    """
    A Django email backend that uses ZeptoMail API to send emails.
    """

    def __init__(self, api_key=None, mail_token=None, fail_silently=False, **kwargs):
        super().__init__(fail_silently=fail_silently, **kwargs)

        # Get credentials from settings or parameters
        self.api_key = api_key or getattr(settings, 'ZEPTO_MAIL_API_KEY', None)
        self.mail_token = mail_token or getattr(settings, 'ZEPTO_MAIL_TOKEN', None)

        # ZeptoMail API endpoint
        self.api_url = 'https://api.zeptomail.com/v1.1/email'

        # Validate configuration
        if not self.api_key:
            raise ValueError("ZEPTO_MAIL_API_KEY setting is required for ZeptoMail backend")

        if not self.mail_token:
            raise ValueError("ZEPTO_MAIL_TOKEN setting is required for ZeptoMail backend")

        # Set up headers for API requests
        self.headers = {
            'Accept': 'application/json',
            'Content-Type': 'application/json',
            'Authorization': f'Zoho-enczapikey {self.api_key}'
        }

        logger.info("ZeptoMail backend initialized successfully")

    def send_messages(self, email_messages):
        """
        Send one or more EmailMessage objects using ZeptoMail API.

        Args:
            email_messages: List of EmailMessage objects

        Returns:
            int: Number of successfully sent messages
        """
        if not email_messages:
            return 0

        sent_count = 0

        for message in email_messages:
            try:
                # Convert Django EmailMessage to ZeptoMail format
                zepto_payload = self._prepare_payload(message)

                # Send email via ZeptoMail API
                response = requests.post(
                    self.api_url,
                    headers=self.headers,
                    json=zepto_payload,
                    timeout=30  # 30 second timeout
                )

                # Check response
                if response.status_code == 200:
                    response_data = response.json()
                    if response_data.get('status') == 'success':
                        sent_count += 1
                        logger.info(f"Email sent successfully to {message.to}")
                    else:
                        logger.error(f"ZeptoMail API error: {response_data}")
                        if not self.fail_silently:
                            raise Exception(f"ZeptoMail API error: {response_data}")
                else:
                    logger.error(f"ZeptoMail HTTP error {response.status_code}: {response.text}")
                    if not self.fail_silently:
                        raise Exception(f"ZeptoMail HTTP error {response.status_code}: {response.text}")

            except Exception as e:
                logger.error(f"Failed to send email: {str(e)}")
                if not self.fail_silently:
                    raise

        return sent_count

    def _prepare_payload(self, message):
        """
        Convert Django EmailMessage to ZeptoMail API payload format.

        Args:
            message: Django EmailMessage object

        Returns:
            dict: ZeptoMail API payload
        """
        # Get recipient emails
        to_recipients = [sanitize_address(addr, message.encoding) for addr in message.to]

        # Prepare payload
        payload = {
            "from": {
                "address": sanitize_address(message.from_email, message.encoding)
            },
            "to": [
                {"email_address": {"address": email}} for email in to_recipients
            ],
            "subject": message.subject,
            "track_clicks": True,
            "track_opens": True
        }

        # Handle message body - support both plain text and HTML
        has_html = False
        text_body = message.body
        html_body = None

        # Check if message has HTML alternative
        if hasattr(message, 'alternatives') and message.alternatives:
            for alternative in message.alternatives:
                if alternative[1] == 'text/html':
                    html_body = alternative[0]
                    has_html = True
                    break
                elif alternative[1] == 'text/plain':
                    text_body = alternative[0]

        # Set body based on content type
        if message.content_subtype == 'html' or has_html:
            # HTML email
            if html_body:
                payload["htmlbody"] = html_body
            else:
                payload["htmlbody"] = message.body
            payload["textbody"] = text_body
        else:
            # Plain text email
            payload["textbody"] = message.body

        # Add CC if present
        if message.cc:
            payload["cc"] = [
                {"email_address": {"address": sanitize_address(addr, message.encoding)}}
                for addr in message.cc
            ]

        # Add BCC if present
        if message.bcc:
            payload["bcc"] = [
                {"email_address": {"address": sanitize_address(addr, message.encoding)}}
                for addr in message.bcc
            ]

        # Add reply-to if specified
        if message.reply_to:
            payload["reply_to"] = [
                {"address": sanitize_address(addr, message.encoding)} for addr in message.reply_to
            ]

        return payload

    def open(self):
        """
        Open connection. ZeptoMail uses REST API so no persistent connection needed.
        """
        return True

    def close(self):
        """
        Close connection. ZeptoMail uses REST API so no cleanup needed.
        """
        pass
