"""
Authentication Service for UniSinq
Handles user authentication related services like welcome emails.
"""

import logging
from django.conf import settings
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from django.utils import timezone

logger = logging.getLogger(__name__)


class AuthService:
    """
    Service class for handling authentication-related functionality
    """

    @staticmethod
    def send_welcome_back_email(email, username):
        """
        Send a welcome back email to returning users

        Args:
            email (str): User's email address
            username (str): User's username

        Returns:
            bool: True if email sent successfully, False otherwise
        """
        try:
            subject = f"Welcome back to UniSinq, {username}! 🚀"

            # Plain text version
            text_content = f"""
Hi {username}!

Welcome back to UniSinq! We're excited to see you again.

Continue your journey of innovation and collaboration with fellow students worldwide.

What's new:
• Connect with more students from different colleges
• Start or join exciting projects
• Build your portfolio and network
• Access enhanced messaging and notifications

Ready to dive back in? Visit: http://localhost:8000

Happy collaborating!
🚀 The UniSinq Team

---
This email was sent to {email}
If you didn't request this, please ignore this email.
"""

            # HTML version
            html_content = f"""
<!DOCTYPE html>
<html>
<head>
    <meta charset="utf-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Welcome Back to UniSinq</title>
    <style>
        body {{
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            line-height: 1.6;
            color: #333;
            max-width: 600px;
            margin: 0 auto;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            padding: 20px;
        }}
        .container {{
            background: white;
            border-radius: 15px;
            padding: 40px;
            box-shadow: 0 10px 30px rgba(0,0,0,0.1);
        }}
        .header {{
            text-align: center;
            margin-bottom: 30px;
        }}
        .logo {{
            font-size: 2.5em;
            font-weight: bold;
            background: linear-gradient(45deg, #667eea, #764ba2);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            margin-bottom: 10px;
        }}
        .welcome-text {{
            font-size: 1.2em;
            color: #666;
            margin: 20px 0;
        }}
        .features {{
            background: #f8f9fa;
            border-radius: 10px;
            padding: 25px;
            margin: 25px 0;
        }}
        .feature-item {{
            margin: 10px 0;
            padding-left: 20px;
            position: relative;
        }}
        .feature-item:before {{
            content: "•";
            color: #667eea;
            font-weight: bold;
            position: absolute;
            left: 0;
        }}
        .cta-button {{
            display: inline-block;
            background: linear-gradient(45deg, #667eea, #764ba2);
            color: white;
            padding: 15px 30px;
            text-decoration: none;
            border-radius: 25px;
            font-weight: bold;
            text-align: center;
            margin: 20px 0;
            box-shadow: 0 4px 15px rgba(102, 126, 234, 0.3);
        }}
        .cta-button:hover {{
            transform: translateY(-2px);
            box-shadow: 0 6px 20px rgba(102, 126, 234, 0.4);
        }}
        .footer {{
            margin-top: 30px;
            padding-top: 20px;
            border-top: 1px solid #eee;
            font-size: 0.9em;
            color: #666;
            text-align: center;
        }}
        .rocket {{
            font-size: 1.5em;
        }}
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <div class="logo">🚀 UniSinq</div>
            <h1>Welcome Back, {username}!</h1>
            <p class="welcome-text">We're thrilled to see you again!</p>
        </div>

        <p>Continue your journey of innovation and collaboration with fellow students worldwide. Your account is ready and waiting for you.</p>

        <div class="features">
            <h3 style="margin-top: 0; color: #333;">✨ What's New & Improved:</h3>
            <div class="feature-item">Connect with more students from different colleges</div>
            <div class="feature-item">Start or join exciting collaborative projects</div>
            <div class="feature-item">Build your portfolio and professional network</div>
            <div class="feature-item">Enhanced messaging and notification system</div>
            <div class="feature-item">Real-time collaboration tools</div>
        </div>

        <div style="text-align: center; margin: 30px 0;">
            <a href="http://localhost:8000" class="cta-button">
                🚀 Continue Your Journey
            </a>
        </div>

        <p>Ready to dive back into the world of student collaboration? Your dashboard is waiting!</p>

        <p>Happy collaborating,<br>
        <strong>The UniSinq Team</strong> <span class="rocket">🚀</span></p>

        <div class="footer">
            <p>
                This email was sent to {email}<br>
                If you didn't expect this email, please ignore it.<br>
                <small>Sent at {timezone.now().strftime('%Y-%m-%d %H:%M UTC')}</small>
            </p>
        </div>
    </div>
</body>
</html>
"""

            # Send the email
            msg = EmailMultiAlternatives(
                subject=subject,
                body=text_content,
                from_email=settings.DEFAULT_FROM_EMAIL,
                to=[email]
            )
            msg.attach_alternative(html_content, "text/html")

            # Send the email
            result = msg.send()

            if result == 1:
                logger.info(f"Welcome back email sent successfully to {email}")
                return True
            else:
                logger.warning(f"Welcome back email reported {result} sent (expected 1) for {email}")
                return False

        except Exception as e:
            logger.error(f"Failed to send welcome back email to {email}: {str(e)}")
            return False

    @staticmethod
    def send_welcome_email(email, username):
        """
        Send a welcome email to new users

        Args:
            email (str): User's email address
            username (str): User's username

        Returns:
            bool: True if email sent successfully, False otherwise
        """
        try:
            subject = f"Welcome to UniSync, {username}! 🎉"

            # Plain text version
            text_content = f"""
Welcome to UniSync, {username}!

Congratulations on joining the premier platform for student collaboration!

Here's what you can do:
• Complete your profile to connect with others
• Post projects or join existing ones
• Network with students from different colleges
• Build your portfolio and skills

Get started: http://localhost:8000/accounts/student-details/

Welcome to the community!
🚀 The UniSync Team

---
This email was sent to {email}
"""

            # HTML version
            html_content = f"""
<!DOCTYPE html>
<html>
<head>
    <meta charset="utf-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Welcome to UniSync</title>
    <style>
        body {{
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            line-height: 1.6;
            color: #333;
            max-width: 600px;
            margin: 0 auto;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            padding: 20px;
        }}
        .container {{
            background: white;
            border-radius: 15px;
            padding: 40px;
            box-shadow: 0 10px 30px rgba(0,0,0,0.1);
        }}
        .header {{
            text-align: center;
            margin-bottom: 30px;
        }}
        .logo {{
            font-size: 2.5em;
            font-weight: bold;
            background: linear-gradient(45deg, #667eea, #764ba2);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            margin-bottom: 10px;
        }}
        .welcome-text {{
            font-size: 1.2em;
            color: #666;
            margin: 20px 0;
        }}
        .features {{
            background: #f8f9fa;
            border-radius: 10px;
            padding: 25px;
            margin: 25px 0;
        }}
        .feature-item {{
            margin: 10px 0;
            padding-left: 20px;
            position: relative;
        }}
        .feature-item:before {{
            content: "•";
            color: #667eea;
            font-weight: bold;
            position: absolute;
            left: 0;
        }}
        .cta-button {{
            display: inline-block;
            background: linear-gradient(45deg, #667eea, #764ba2);
            color: white;
            padding: 15px 30px;
            text-decoration: none;
            border-radius: 25px;
            font-weight: bold;
            text-align: center;
            margin: 20px 0;
            box-shadow: 0 4px 15px rgba(102, 126, 234, 0.3);
        }}
        .cta-button:hover {{
            transform: translateY(-2px);
            box-shadow: 0 6px 20px rgba(102, 126, 234, 0.4);
        }}
        .footer {{
            margin-top: 30px;
            padding-top: 20px;
            border-top: 1px solid #eee;
            font-size: 0.9em;
            color: #666;
            text-align: center;
        }}
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <div class="logo">🚀 UniSync</div>
            <h1>Welcome to UniSync, {username}!</h1>
            <p class="welcome-text">Congratulations on joining the premier platform for student collaboration!</p>
        </div>

        <p>You're now part of a growing community of students who are building amazing projects together. Here's what you can do to get started:</p>

        <div class="features">
            <h3 style="margin-top: 0; color: #333;">🚀 Getting Started:</h3>
            <div class="feature-item">Complete your profile to connect with others</div>
            <div class="feature-item">Post your own projects or join existing ones</div>
            <div class="feature-item">Network with students from different colleges</div>
            <div class="feature-item">Build your portfolio and develop new skills</div>
        </div>

        <div style="text-align: center; margin: 30px 0;">
            <a href="http://localhost:8000/accounts/student-details/" class="cta-button">
                🎯 Complete Your Profile
            </a>
        </div>

        <p>Welcome to the community of innovators and collaborators!</p>

        <p>Best regards,<br>
        <strong>The UniSync Team</strong> 🚀</p>

        <div class="footer">
            <p>
                This email was sent to {email}<br>
                <small>Sent at {timezone.now().strftime('%Y-%m-%d %H:%M UTC')}</small>
            </p>
        </div>
    </div>
</body>
</html>
"""

            # Send the email
            msg = EmailMultiAlternatives(
                subject=subject,
                body=text_content,
                from_email=settings.DEFAULT_FROM_EMAIL,
                to=[email]
            )
            msg.attach_alternative(html_content, "text/html")

            result = msg.send()

            if result == 1:
                logger.info(f"Welcome email sent successfully to {email}")
                return True
            else:
                logger.warning(f"Welcome email reported {result} sent (expected 1) for {email}")
                return False

        except Exception as e:
            logger.error(f"Failed to send welcome email to {email}: {str(e)}")
            return False

    @staticmethod
    def send_password_reset_email(email, username, reset_link):
        """
        Send password reset email

        Args:
            email (str): User's email address
            username (str): User's username
            reset_link (str): Password reset link

        Returns:
            bool: True if email sent successfully, False otherwise
        """
        try:
            subject = f"Password Reset - UniSync"

            text_content = f"""
Hi {username},

You requested a password reset for your UniSync account.

Click this link to reset your password:
{reset_link}

This link will expire in 24 hours.

If you didn't request this, please ignore this email.

Best regards,
The UniSync Team
"""

            html_content = f"""
<!DOCTYPE html>
<html>
<head>
    <style>
        body {{ font-family: Arial, sans-serif; background: #f4f4f4; padding: 20px; }}
        .container {{ background: white; padding: 30px; border-radius: 10px; box-shadow: 0 0 10px rgba(0,0,0,0.1); }}
        .button {{ background: #007bff; color: white; padding: 10px 20px; text-decoration: none; border-radius: 5px; }}
    </style>
</head>
<body>
    <div class="container">
        <h2>Password Reset Request</h2>
        <p>Hi {username},</p>
        <p>You requested a password reset for your UniSync account.</p>
        <p><a href="{reset_link}" class="button">Reset Password</a></p>
        <p>This link will expire in 24 hours.</p>
        <p>If you didn't request this, please ignore this email.</p>
        <p>Best regards,<br>The UniSync Team</p>
    </div>
</body>
</html>
"""

            msg = EmailMultiAlternatives(
                subject=subject,
                body=text_content,
                from_email=settings.DEFAULT_FROM_EMAIL,
                to=[email]
            )
            msg.attach_alternative(html_content, "text/html")

            result = msg.send()

            if result == 1:
                logger.info(f"Password reset email sent successfully to {email}")
                return True
            else:
                logger.warning(f"Password reset email reported {result} sent for {email}")
                return False

        except Exception as e:
            logger.error(f"Failed to send password reset email to {email}: {str(e)}")
            return False
