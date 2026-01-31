#!/usr/bin/env python
"""
Email Testing Script for UniSync
Tests email configuration and sends test emails to verify setup.
"""

import os
import sys
import django

# Setup Django
sys.path.append(os.path.dirname(__file__))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'auth_project.settings')

try:
    django.setup()
    print("Django setup successful")
except Exception as e:
    print(f"Django setup failed: {e}")
    sys.exit(1)

from django.conf import settings
from django.core.mail import send_mail, EmailMultiAlternatives

def test_email_configuration():
    """Test email configuration and display current settings"""
    print("\n" + "="*50)
    print("EMAIL CONFIGURATION TEST")
    print("="*50)

    print(f"Email Backend: {settings.EMAIL_BACKEND}")
    print(f"Default From Email: {settings.DEFAULT_FROM_EMAIL}")

    # Check which backend is configured
    backends = {
        'accounts.zepto_mail_backend.ZeptoMailBackend': 'ZeptoMail',
        'django.core.mail.backends.smtp.EmailBackend': 'SMTP',
        'django.core.mail.backends.console.EmailBackend': 'Console'
    }

    backend_name = backends.get(settings.EMAIL_BACKEND, 'Unknown')
    print(f"Backend Type: {backend_name}")

    # Check specific configurations
    if 'zeptomail' in settings.EMAIL_BACKEND.lower():
        api_key = getattr(settings, 'ZEPTO_MAIL_API_KEY', None)
        mail_token = getattr(settings, 'ZEPTO_MAIL_TOKEN', None)
        print(f"ZeptoMail API Key: {'Configured' if api_key else 'Missing'}")
        print(f"ZeptoMail Mail Token: {'Configured' if mail_token else 'Missing'}")

    elif 'smtp' in settings.EMAIL_BACKEND.lower():
        host_user = getattr(settings, 'EMAIL_HOST_USER', None)
        host_password = getattr(settings, 'EMAIL_HOST_PASSWORD', None)
        host = getattr(settings, 'EMAIL_HOST', None)
        port = getattr(settings, 'EMAIL_PORT', None)
        print(f"SMTP Host: {host or 'Not set'}")
        print(f"SMTP Port: {port or 'Not set'}")
        print(f"SMTP Username: {'Configured' if host_user else 'Missing'}")
        print(f"SMTP Password: {'Configured' if host_password else 'Missing'}")

def send_test_email():
    """Send a test email to verify configuration"""
    print("\n" + "="*50)
    print("TESTING EMAIL DELIVERY")
    print("="*50)

    # Get recipient email from command line or use default
    recipient = sys.argv[1] if len(sys.argv) > 1 else 'test@example.com'

    if recipient == 'test@example.com':
        print("WARNING: Using default test email. Provide actual email as argument:")
        print(f"   python {sys.argv[0]} your-email@example.com")

    print(f"Sending test email to: {recipient}")

    try:
        # Send plain text email
        result = send_mail(
            'UniSync Email Test',
            f'This is a test email from UniSync.\n\nIf you receive this email, your email configuration is working correctly!\n\nBackend: {settings.EMAIL_BACKEND}\nTimestamp: {django.utils.timezone.now()}',
            settings.DEFAULT_FROM_EMAIL,
            [recipient],
            fail_silently=False
        )

        if result == 1:
            print("SUCCESS: Plain text email sent successfully!")
        else:
            print(f"WARNING: Email reported {result} sent (expected 1)")

    except Exception as e:
        print(f"ERROR: Plain text email failed: {e}")

    # Try HTML email if plain text worked
    try:
        html_content = f"""
        <html>
        <head>
            <style>
                body {{ font-family: Arial, sans-serif; background: #f4f4f4; padding: 20px; }}
                .container {{ background: white; padding: 30px; border-radius: 10px; box-shadow: 0 0 10px rgba(0,0,0,0.1); }}
                .header {{ background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); color: white; padding: 20px; border-radius: 8px; margin-bottom: 20px; }}
                .success {{ background: #d4edda; color: #155724; padding: 15px; border-radius: 5px; margin: 15px 0; }}
            </style>
        </head>
        <body>
            <div class="container">
                <div class="header">
                    <h1>UniSync Email Test</h1>
                    <p>HTML Email Configuration Test</p>
                </div>

                <div class="success">
                    <h3>Success!</h3>
                    <p>Your email configuration is working correctly!</p>
                </div>

                <p><strong>Configuration Details:</strong></p>
                <ul>
                    <li>Backend: {settings.EMAIL_BACKEND}</li>
                    <li>From: {settings.DEFAULT_FROM_EMAIL}</li>
                    <li>Timestamp: {django.utils.timezone.now()}</li>
                </ul>

                <p>If you're seeing this email, both plain text and HTML email delivery are working!</p>

                <hr>
                <p><small>This is an automated test email from UniSync. If you received this by mistake, please ignore.</small></p>
            </div>
        </body>
        </html>
        """

        msg = EmailMultiAlternatives(
            'UniSync HTML Email Test',
            'This is a test of HTML email functionality. If you see HTML formatting, your configuration is working!',
            settings.DEFAULT_FROM_EMAIL,
            [recipient]
        )
        msg.attach_alternative(html_content, "text/html")

        html_result = msg.send()

        if html_result == 1:
            print("SUCCESS: HTML email sent successfully!")
        else:
            print(f"WARNING: HTML email reported {html_result} sent (expected 1)")

    except Exception as e:
        print(f"ERROR: HTML email failed: {e}")

def main():
    """Main test function"""
    print("UniSync Email Testing Script")
    print("============================")

    test_email_configuration()
    send_test_email()

    print("\n" + "="*50)
    print("NEXT STEPS")
    print("="*50)

    if 'console' in settings.EMAIL_BACKEND:
        print("Console Backend Active:")
        print("   - Check your Django console/runserver output for email content")
        print("   - Emails are not actually sent, just printed to console")
        print("   - Perfect for development testing")

    elif 'zeptomail' in settings.EMAIL_BACKEND:
        print("ZeptoMail Backend Active:")
        print("   - If emails are not being received:")
        print("     1. Check ZeptoMail dashboard for delivery status")
        print("     2. Verify domain verification (unisync.app)")
        print("     3. Ensure API key and mail token are correct")
        print("     4. Check ZeptoMail account limits/credits")

    elif 'smtp' in settings.EMAIL_BACKEND:
        print("SMTP Backend Active:")
        print("   - If emails are not being received:")
        print("     1. Check spam/junk folder")
        print("     2. Verify SMTP credentials")
        print("     3. Check firewall/antivirus blocking port 587")
        print("     4. Try different SMTP provider")

    print("\nFor more help, see EMAIL_TROUBLESHOOTING.md")
    print("Visit Help Center: /accounts/help/")
    print("Contact Support: /accounts/contact/")

if __name__ == '__main__':
    main()
