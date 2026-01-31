#!/usr/bin/env python
"""
Email Configuration Diagnostic Script
Tests email backend and OTP sending
"""

import os
import sys
import django

# Setup Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'auth_project.settings')
sys.path.insert(0, os.path.dirname(__file__))
django.setup()

from django.conf import settings
from django.core.mail import EmailMultiAlternatives
from accounts.models import OTP
import logging

logger = logging.getLogger('accounts')

print("\n" + "="*60)
print("EMAIL CONFIGURATION DIAGNOSTIC")
print("="*60)

# 1. Check EMAIL_BACKEND
print(f"\n1. EMAIL_BACKEND: {settings.EMAIL_BACKEND}")

# 2. Check API Keys
print(f"\n2. API KEYS CONFIGURED:")
print(f"   - BREVO_API_KEY: {'✓ SET' if settings.BREVO_API_KEY else '✗ NOT SET'}")
print(f"   - ZEPTO_MAIL_API_KEY: {'✓ SET' if settings.ZEPTO_MAIL_API_KEY else '✗ NOT SET'}")
print(f"   - ZEPTO_MAIL_TOKEN: {'✓ SET' if settings.ZEPTO_MAIL_TOKEN else '✗ NOT SET'}")
print(f"   - EMAIL_HOST_USER: {'✓ SET' if settings.EMAIL_HOST_USER else '✗ NOT SET'}")

# 3. Default FROM email
print(f"\n3. DEFAULT_FROM_EMAIL: {settings.DEFAULT_FROM_EMAIL}")

# 4. Test email sending
print(f"\n4. TESTING EMAIL SEND...")
test_email = "test@example.com"

try:
    # Create test OTP
    otp = OTP.generate_otp(test_email, 'test')
    print(f"   - OTP Generated: {otp.otp_code}")
    
    # Try to send email
    subject = "Test OTP Email"
    text = f"Your OTP is: {otp.otp_code}"
    html = f"<h1>Your OTP is: {otp.otp_code}</h1>"
    
    msg = EmailMultiAlternatives(
        subject=subject,
        body=text,
        from_email=settings.DEFAULT_FROM_EMAIL,
        to=[test_email]
    )
    msg.attach_alternative(html, "text/html")
    
    result = msg.send()
    print(f"   - Email Send Result: {result} (1=success, 0=fail)")
    
    if result > 0:
        print("   ✓ EMAIL SENT SUCCESSFULLY")
    else:
        print("   ✗ EMAIL FAILED TO SEND")
        
except Exception as e:
    print(f"   ✗ ERROR: {str(e)}")
    import traceback
    traceback.print_exc()

# 5. Check logs
print(f"\n5. CHECKING LOGS...")
log_file = os.path.join(settings.BASE_DIR, 'logs', 'django.log')
if os.path.exists(log_file):
    print(f"   Log file exists: {log_file}")
    with open(log_file, 'r') as f:
        lines = f.readlines()[-10:]
        print(f"   Last 10 log entries:")
        for line in lines:
            print(f"   {line.rstrip()}")
else:
    print(f"   ✗ Log file not found: {log_file}")

print("\n" + "="*60)
