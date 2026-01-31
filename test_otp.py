#!/usr/bin/env python
import os
import sys
import django

# Setup Django environment
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'auth_project.settings')
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'auth_project'))

django.setup()

from accounts.models import OTP
from django.contrib.auth.models import User
from django.utils import timezone

def test_otp():
    print("=== Testing OTP Generation ===")

    try:
        # Check OTP table
        print(f"OTP table name: {OTP._meta.db_table}")
        print(f"Total OTPs in database: {OTP.objects.count()}")

        # Create test user if needed
        user, created = User.objects.get_or_create(
            username='testuser',
            defaults={'email': 'test@example.com'}
        )
        print(f"Test user created: {created}")

        # Generate OTP
        print("Generating OTP...")
        otp_obj = OTP.generate_otp('test@example.com', 'login')

        print("✅ OTP generated successfully!")
        print(f"OTP code: {otp_obj.otp_code}")
        print(f"OTP purpose: {otp_obj.purpose}")
        print(f"OTP email: {otp_obj.email}")
        print(f"OTP valid: {otp_obj.is_valid()}")
        print(f"OTP expires: {otp_obj.expires_at}")

        return True

    except Exception as e:
        print(f"❌ Error generating OTP: {str(e)}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == '__main__':
    success = test_otp()
    sys.exit(0 if success else 1)
