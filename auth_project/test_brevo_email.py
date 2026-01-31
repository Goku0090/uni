#!/usr/bin/env python
"""
Test Brevo Email Backend
Run: python manage.py shell < test_brevo_email.py
Or: python test_brevo_email.py
"""

import os
import sys
import django

# Setup Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'auth_project.settings')
django.setup()

from django.core.mail import send_mail, EmailMultiAlternatives
from django.conf import settings

print("=" * 60)
print("BREVO EMAIL BACKEND TEST")
print("=" * 60)

# Check configuration
print("\n📋 CONFIGURATION CHECK:")
print(f"EMAIL_BACKEND: {settings.EMAIL_BACKEND}")
print(f"BREVO_API_KEY: {'SET ✅' if settings.BREVO_API_KEY else 'NOT SET ❌'}")
print(f"DEFAULT_FROM_EMAIL: {settings.DEFAULT_FROM_EMAIL}")

if not settings.BREVO_API_KEY:
    print("\n❌ BREVO_API_KEY is not set in .env file")
    print("Please add: BREVO_API_KEY=your-api-key")
    sys.exit(1)

# Test 1: Simple email
print("\n" + "=" * 60)
print("TEST 1: Simple Text Email")
print("=" * 60)
try:
    result = send_mail(
        subject='UniSync - Brevo Test Email',
        message='This is a test email from UniSync to verify Brevo is working correctly.',
        from_email=settings.DEFAULT_FROM_EMAIL,
        recipient_list=['test@aabbbccc.online'],  # Change to your test email
        fail_silently=False,
    )
    print(f"✅ Email sent successfully!")
    print(f"   Result: {result}")
except Exception as e:
    print(f"❌ Error: {str(e)}")
    import traceback
    traceback.print_exc()

# Test 2: HTML email with alternative
print("\n" + "=" * 60)
print("TEST 2: HTML Email with Alternative")
print("=" * 60)
try:
    text_message = "This is a test email from UniSync."
    html_message = """
    <html>
    <body style="font-family: Arial, sans-serif;">
        <h2>🚀 UniSync Test Email</h2>
        <p>This is an HTML test email from UniSync.</p>
        <p><strong>Status:</strong> Brevo is working!</p>
    </body>
    </html>
    """
    
    msg = EmailMultiAlternatives(
        subject='UniSync - Brevo HTML Test',
        body=text_message,
        from_email=settings.DEFAULT_FROM_EMAIL,
        to=['test@aabbbccc.online']  # Change to your test email
    )
    msg.attach_alternative(html_message, "text/html")
    result = msg.send()
    
    print(f"✅ HTML email sent successfully!")
    print(f"   Result: {result}")
except Exception as e:
    print(f"❌ Error: {str(e)}")
    import traceback
    traceback.print_exc()

# Test 3: OTP Email (actual use case)
print("\n" + "=" * 60)
print("TEST 3: OTP Email (Real Use Case)")
print("=" * 60)
try:
    from accounts.models import OTP
    
    test_email = 'test@aabbbccc.online'  # Change to your test email
    otp = OTP.generate_otp(test_email, 'test')
    
    subject = f"🚀 UniSync - Your Test OTP Code"
    from_email = settings.DEFAULT_FROM_EMAIL
    to = [test_email]
    
    text_message = f"""
Hi there!

Your OTP for testing is: {otp.otp_code}

This OTP is valid for 5 minutes only.

If you didn't request this, please ignore this email.

Best regards,
🚀 UniSync Team
"""
    
    html_message = f"""
<!DOCTYPE html>
<html>
<head>
<style>
    body {{ font-family: Arial, sans-serif; background: #f4f4f4; padding: 20px; }}
    .container {{ background: white; padding: 30px; border-radius: 10px; box-shadow: 0 0 10px rgba(0,0,0,0.1); }}
    .otp-box {{ background: #007bff; color: white; padding: 20px; text-align: center; border-radius: 8px; margin: 20px 0; }}
    .otp-code {{ font-size: 32px; font-weight: bold; letter-spacing: 8px; }}
</style>
</head>
<body>
<div class="container">
    <h2>🔐 UniSync Verification</h2>
    <p>Hi there!</p>
    <p>Your OTP for <b>testing</b> is:</p>
    <div class="otp-box"><div class="otp-code">{otp.otp_code}</div></div>
    <p>This OTP is valid for <strong>5 minutes</strong>. Do not share it with anyone.</p>
    <p>Ignore if you did not request this.</p>
    <p>– 🚀 UniSync Team</p>
</div>
</body>
</html>
"""
    
    msg = EmailMultiAlternatives(subject, text_message, from_email, to)
    msg.attach_alternative(html_message, "text/html")
    result = msg.send()
    
    print(f"✅ OTP email sent successfully!")
    print(f"   OTP Code: {otp.otp_code}")
    print(f"   Recipient: {test_email}")
    print(f"   Result: {result}")
except Exception as e:
    print(f"❌ Error: {str(e)}")
    import traceback
    traceback.print_exc()

print("\n" + "=" * 60)
print("TEST COMPLETE")
print("=" * 60)
print("\n💡 Next Steps:")
print("1. Check your email inbox for test messages")
print("2. If emails arrive, Brevo is working! ✅")
print("3. If not, check:")
print("   - BREVO_API_KEY is correct in .env")
print("   - DEFAULT_FROM_EMAIL is verified in Brevo dashboard")
print("   - Check Brevo dashboard for delivery logs")
print("=" * 60)
