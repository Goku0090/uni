#!/usr/bin/env python
import os
import sys
import django

# Setup Django environment
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'auth_project.settings')
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'auth_project'))

django.setup()

from accounts.models import OTP

def test_otp():
    print("=== Testing OTP Generation ===")

    try:
        # Check OTP table
        print("OTP table name:", OTP._meta.db_table)
        print("Total OTPs in database:", OTP.objects.count())

        # Generate OTP
        print("Generating OTP...")
        otp_obj = OTP.generate_otp('test@example.com', 'login')

        print("SUCCESS: OTP generated!")
        print("OTP code:", otp_obj.otp_code)
        print("OTP purpose:", otp_obj.purpose)
        print("OTP email:", otp_obj.email)
        print("OTP valid:", otp_obj.is_valid())
        print("OTP expires:", otp_obj.expires_at)

        return True

    except Exception as e:
        print("ERROR generating OTP:", str(e))
        import traceback
        traceback.print_exc()
        return False

if __name__ == '__main__':
    success = test_otp()
    print("Test result:", "PASSED" if success else "FAILED")
