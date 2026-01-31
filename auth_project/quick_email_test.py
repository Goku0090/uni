#!/usr/bin/env python
"""
Quick Email Test - Simple one-liner to test email configuration
Usage: python quick_email_test.py
"""

import os
import sys
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'auth_project.settings')
sys.path.insert(0, os.path.dirname(__file__))

# Initialize Django
django.setup()

from django.conf import settings
from django.core.mail import EmailMultiAlternatives

print("\n" + "="*70)
print("QUICK EMAIL TEST")
print("="*70)

print(f"\n✓ EMAIL_BACKEND: {settings.EMAIL_BACKEND}")
print(f"✓ DEFAULT_FROM_EMAIL: {settings.DEFAULT_FROM_EMAIL}")

# Detect which backend is in use
if 'brevo' in settings.EMAIL_BACKEND.lower():
    if settings.BREVO_API_KEY:
        print(f"✓ BREVO_API_KEY: SET (first 10 chars: {settings.BREVO_API_KEY[:10]}...)")
    else:
        print("✗ BREVO_API_KEY: NOT SET")
elif 'zepto' in settings.EMAIL_BACKEND.lower():
    if settings.ZEPTO_MAIL_API_KEY and settings.ZEPTO_MAIL_TOKEN:
        print(f"✓ ZEPTO_MAIL_API_KEY: SET")
        print(f"✓ ZEPTO_MAIL_TOKEN: SET")
    else:
        print("✗ ZEPTO_MAIL credentials: MISSING")
elif 'gmail' in settings.EMAIL_HOST.lower() if hasattr(settings, 'EMAIL_HOST') else False:
    if settings.EMAIL_HOST_USER:
        print(f"✓ EMAIL_HOST_USER: {settings.EMAIL_HOST_USER}")
    else:
        print("✗ EMAIL_HOST_USER: NOT SET")
elif 'console' in settings.EMAIL_BACKEND.lower():
    print("⚠ WARNING: Using Console Backend - Emails print to console only!")
    print("  Configure email service in .env file")

print("\n--- Testing Email Send ---")
try:
    msg = EmailMultiAlternatives(
        subject="UniSync OTP Test",
        body="Your OTP test code: 123456",
        from_email=settings.DEFAULT_FROM_EMAIL,
        to=["test@example.com"]
    )
    msg.attach_alternative("<h1>Your OTP: 123456</h1>", "text/html")
    
    result = msg.send()
    
    if result > 0:
        print(f"✓ SUCCESS: Email send returned {result}")
        print("  Email backend is working correctly!")
    else:
        print(f"✗ FAILED: Email send returned {result}")
        print("  Check email backend configuration")
        
except Exception as e:
    print(f"✗ ERROR: {str(e)}")
    print("\nFix steps:")
    print("1. Create .env file in auth_project directory")
    print("2. Add email service credentials (see .env.template)")
    print("3. Restart Django server")
    print(f"\nDetails: {type(e).__name__}")

print("\n" + "="*70)
print("For detailed diagnostics, run: python test_email_diagnostic.py")
print("="*70 + "\n")
