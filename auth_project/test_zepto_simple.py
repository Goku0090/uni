#!/usr/bin/env python
"""
Simple ZeptoMail Test - Run this to verify ZeptoMail is working
Usage: python manage.py shell < test_zepto_simple.py
Or copy-paste commands one by one in Django shell
"""

import os
import sys
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'auth_project.settings')

import django
django.setup()

from django.conf import settings
from django.core.mail import send_mail
from accounts.services.auth_service import AuthService
from accounts.models import OTP

print("\n" + "="*70)
print("  🧪 ZEPTOMAIL QUICK TEST")
print("="*70 + "\n")

# Test 1: Check Backend Configuration
print("📋 TEST 1: Checking Configuration")
print("-" * 70)
print(f"✓ EMAIL_BACKEND: {settings.EMAIL_BACKEND}")
print(f"✓ DEFAULT_FROM_EMAIL: {settings.DEFAULT_FROM_EMAIL}")
print(f"✓ ZEPTO_MAIL_API_KEY: {'SET ✓' if settings.ZEPTO_MAIL_API_KEY else 'NOT SET ✗'}")
print(f"✓ ZEPTO_MAIL_TOKEN: {'SET ✓' if settings.ZEPTO_MAIL_TOKEN else 'NOT SET ✗'}")

if "ZeptoMailBackend" in settings.EMAIL_BACKEND:
    print("\n✅ RESULT: ZeptoMail backend is configured correctly!")
elif "console" in settings.EMAIL_BACKEND.lower():
    print("\n⚠️  RESULT: Using Console backend (check your console for OTP)")
elif "smtp" in settings.EMAIL_BACKEND.lower():
    print("\n⚠️  RESULT: Using Gmail SMTP backend")
else:
    print("\n❌ RESULT: Unknown email backend")

# Test 2: Try to import ZeptoMailBackend
print("\n📋 TEST 2: Checking ZeptoMailBackend Import")
print("-" * 70)
try:
    from accounts.zepto_mail_backend import ZeptoMailBackend
    print("✅ ZeptoMailBackend imported successfully")
except Exception as e:
    print(f"❌ Failed to import ZeptoMailBackend: {str(e)}")

# Test 3: Send Test Email
print("\n📋 TEST 3: Sending Test Email")
print("-" * 70)
test_email = input("Enter your email address to test: ").strip()

if test_email:
    try:
        result = send_mail(
            subject='🧪 ZeptoMail Test Email',
            message='This is a test email from UniSync ZeptoMail configuration.',
            from_email=settings.DEFAULT_FROM_EMAIL,
            recipient_list=[test_email],
            fail_silently=False,
        )
        
        if result:
            print(f"✅ Test email sent successfully!")
            print(f"   Check {test_email} for the email")
            print(f"   If using console backend, check Django console output")
        else:
            print("❌ Email send returned 0 (failed)")
    except Exception as e:
        print(f"❌ Error sending test email: {str(e)}")
        import traceback
        traceback.print_exc()
else:
    print("⏭️  Skipping test email")

# Test 4: Test OTP Generation and Sending
print("\n📋 TEST 4: Testing OTP Generation & Sending")
print("-" * 70)
otp_test_email = input("Enter email for OTP test (can be same): ").strip()

if otp_test_email:
    try:
        # Generate OTP
        otp = OTP.generate_otp(email=otp_test_email, purpose='testing')
        print(f"✓ OTP generated: {otp.otp_code}")
        print(f"  Email: {otp.email}")
        print(f"  Purpose: {otp.purpose}")
        print(f"  Valid: {otp.is_valid()}")
        
        # Send OTP email
        print(f"\nSending OTP email...")
        result = AuthService.send_otp_email(
            email=otp_test_email,
            otp_code=otp.otp_code,
            purpose='testing'
        )
        
        if result:
            print(f"✅ OTP email sent successfully!")
            print(f"   OTP Code (for testing): {otp.otp_code}")
            print(f"   Check {otp_test_email} inbox")
        else:
            print("❌ OTP email failed to send")
            
    except Exception as e:
        print(f"❌ Error with OTP: {str(e)}")
        import traceback
        traceback.print_exc()
else:
    print("⏭️  Skipping OTP test")

# Test 5: Check Recent Logs
print("\n📋 TEST 5: Checking Recent Logs")
print("-" * 70)
log_path = 'logs/django.log'
try:
    with open(log_path, 'r', encoding='utf-8', errors='ignore') as f:
        lines = f.readlines()
    
    email_lines = [l for l in lines if 'email' in l.lower() or 'zepto' in l.lower() or 'otp' in l.lower()]
    
    if email_lines:
        print("Recent email-related logs:")
        for line in email_lines[-10:]:  # Last 10 email-related lines
            print(f"  {line.strip()}")
    else:
        print("No email-related logs found")
except FileNotFoundError:
    print(f"⚠️  Log file not found at {log_path}")

# Final Summary
print("\n" + "="*70)
print("  📊 TEST SUMMARY")
print("="*70)
print("""
✅ If you see:
   • ZeptoMailBackend in EMAIL_BACKEND → Using ZeptoMail (Good!)
   • Test emails sent successfully → OTP emails will work!
   • OTP generated and sent → System ready!

⚠️ If you see:
   • Console backend → Edit .env with ZeptoMail credentials
   • "Connection refused" → Check ZeptoMail credentials
   • "Domain not verified" → Verify domain in ZeptoMail

🚀 NEXT STEPS:
   1. Check your email inbox for test messages
   2. If received → ZeptoMail is working! 🎉
   3. If not received → Check logs above for errors
""")
print("="*70 + "\n")
