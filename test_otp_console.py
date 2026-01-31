#!/usr/bin/env python
import os
import sys
import django

# Setup Django environment
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'auth_project.settings')
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'auth_project'))

django.setup()

from accounts.models import OTP
from django.core.mail import send_mail

def test_console_email():
    print("=== Testing Console Email Backend ===")

    # Test OTP generation
    print("Generating OTP...")
    otp = OTP.generate_otp('test@example.com', 'login')
    print(f"OTP Code: {otp.otp_code}")

    # Test email sending
    print("Sending email via console backend...")
    try:
        send_mail(
            'Test OTP - Console Backend',
            f'Your test OTP is: {otp.otp_code}\n\nThis should appear in the Django console!',
            'noreply@unisync.app',
            ['test@example.com'],
            fail_silently=False
        )
        print("Email sent successfully!")
    except Exception as e:
        print(f"Email sending failed: {e}")

    print("=== Test Complete ===")

if __name__ == '__main__':
    test_console_email()
