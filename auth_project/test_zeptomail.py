#!/usr/bin/env python
"""
ZeptoMail Configuration Test Script
Tests ZeptoMail setup and email sending functionality.
Usage: python manage.py shell < test_zeptomail.py
Or: python test_zeptomail.py (if run directly)
"""

import os
import sys
import django
from pathlib import Path

# Setup Django if running directly
if __name__ == "__main__":
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'auth_project.settings')
    django.setup()

from django.conf import settings
from django.core.mail import send_mail, EmailMultiAlternatives
from accounts.models import OTP
from accounts.services.auth_service import AuthService


def print_header(text):
    """Print a formatted header"""
    print("\n" + "=" * 70)
    print(f"  {text}")
    print("=" * 70 + "\n")


def print_section(text):
    """Print a formatted section"""
    print(f"\n📋 {text}")
    print("-" * 70)


def check_environment():
    """Check if environment variables are set"""
    print_header("CHECKING ENVIRONMENT VARIABLES")
    
    api_key = getattr(settings, 'ZEPTO_MAIL_API_KEY', None)
    mail_token = getattr(settings, 'ZEPTO_MAIL_TOKEN', None)
    from_email = getattr(settings, 'DEFAULT_FROM_EMAIL', None)
    backend = getattr(settings, 'EMAIL_BACKEND', None)
    
    print_section("Email Configuration")
    print(f"✓ EMAIL_BACKEND: {backend}")
    print(f"✓ DEFAULT_FROM_EMAIL: {from_email}")
    print(f"✓ ZEPTO_MAIL_API_KEY: {'SET ✓' if api_key else 'NOT SET ✗'}")
    print(f"✓ ZEPTO_MAIL_TOKEN: {'SET ✓' if mail_token else 'NOT SET ✗'}")
    
    # Check .env file
    print_section(".env File Status")
    env_path = Path('e:/login/auth_project/.env')
    if env_path.exists():
        print(f"✓ .env file found at: {env_path}")
        # Count lines with credentials
        with open(env_path, 'r') as f:
            content = f.read()
            has_api_key = 'ZEPTO_MAIL_API_KEY=' in content
            has_token = 'ZEPTO_MAIL_TOKEN=' in content
            has_from_email = 'DEFAULT_FROM_EMAIL=' in content
        
        print(f"  - ZEPTO_MAIL_API_KEY in .env: {'YES ✓' if has_api_key else 'NO ✗'}")
        print(f"  - ZEPTO_MAIL_TOKEN in .env: {'YES ✓' if has_token else 'NO ✗'}")
        print(f"  - DEFAULT_FROM_EMAIL in .env: {'YES ✓' if has_from_email else 'NO ✗'}")
    else:
        print(f"✗ .env file NOT found at: {env_path}")
        print("  Create it by copying .env.example")
    
    return api_key and mail_token, from_email, backend


def test_backend_initialization():
    """Test if ZeptoMail backend can be initialized"""
    print_header("TESTING BACKEND INITIALIZATION")
    
    try:
        from accounts.zepto_mail_backend import ZeptoMailBackend
        print_section("ZeptoMailBackend Import")
        print("✓ ZeptoMailBackend imported successfully")
        
        # Try to instantiate
        print_section("Backend Instantiation")
        try:
            backend = ZeptoMailBackend()
            print("✓ ZeptoMailBackend initialized successfully")
            print(f"  - API Key: {backend.api_key[:10]}..." if backend.api_key else "  - No API key")
            print(f"  - Mail Token: {backend.mail_token[:10]}..." if backend.mail_token else "  - No mail token")
            return True
        except ValueError as e:
            print(f"✗ Backend initialization failed: {str(e)}")
            return False
    except Exception as e:
        print(f"✗ Error importing ZeptoMailBackend: {str(e)}")
        return False


def test_simple_email():
    """Test sending a simple email"""
    print_header("TESTING SIMPLE EMAIL SENDING")
    
    from_email = settings.DEFAULT_FROM_EMAIL
    test_email = input("\n📧 Enter test email address to send test email to: ").strip()
    
    if not test_email:
        print("⏭️  Skipping simple email test")
        return False
    
    try:
        print_section("Sending Test Email")
        print(f"From: {from_email}")
        print(f"To: {test_email}")
        print(f"Using backend: {settings.EMAIL_BACKEND}")
        
        result = send_mail(
            subject='🧪 ZeptoMail Test Email',
            message='This is a test email from UniSync ZeptoMail configuration.',
            from_email=from_email,
            recipient_list=[test_email],
            fail_silently=False,
        )
        
        if result:
            print("\n✓ Email sent successfully!")
            print(f"  Check {test_email} for the test email")
            return True
        else:
            print("\n✗ Email failed to send")
            return False
            
    except Exception as e:
        print(f"\n✗ Error sending email: {str(e)}")
        import traceback
        traceback.print_exc()
        return False


def test_html_email():
    """Test sending HTML email"""
    print_header("TESTING HTML EMAIL SENDING")
    
    from_email = settings.DEFAULT_FROM_EMAIL
    test_email = input("\n📧 Enter test email address for HTML email test: ").strip()
    
    if not test_email:
        print("⏭️  Skipping HTML email test")
        return False
    
    try:
        print_section("Sending HTML Email")
        
        msg = EmailMultiAlternatives(
            subject='🎨 ZeptoMail HTML Email Test',
            body='This is the plain text version',
            from_email=from_email,
            to=[test_email],
        )
        
        html_content = """
        <html>
        <body>
            <h1>🚀 UniSync Test Email</h1>
            <p>This is a <strong>test HTML email</strong> from ZeptoMail.</p>
            <div style="background: #667eea; color: white; padding: 20px; border-radius: 8px;">
                <h2>Test Successful!</h2>
                <p>If you're seeing this, ZeptoMail is working correctly.</p>
            </div>
        </body>
        </html>
        """
        
        msg.attach_alternative(html_content, "text/html")
        result = msg.send()
        
        if result:
            print("\n✓ HTML email sent successfully!")
            print(f"  Check {test_email} for the HTML email")
            return True
        else:
            print("\n✗ HTML email failed to send")
            return False
            
    except Exception as e:
        print(f"\n✗ Error sending HTML email: {str(e)}")
        import traceback
        traceback.print_exc()
        return False


def test_otp_generation():
    """Test OTP generation and sending"""
    print_header("TESTING OTP GENERATION & SENDING")
    
    test_email = input("\n📧 Enter email for OTP test: ").strip()
    
    if not test_email:
        print("⏭️  Skipping OTP test")
        return False
    
    try:
        print_section("Generating OTP")
        otp = OTP.generate_otp(email=test_email, purpose='testing')
        print(f"✓ OTP generated: {otp.otp_code}")
        print(f"  - Email: {otp.email}")
        print(f"  - Purpose: {otp.purpose}")
        print(f"  - Valid: {otp.is_valid()}")
        
        print_section("Sending OTP Email")
        result = AuthService.send_otp_email(
            email=test_email,
            otp_code=otp.otp_code,
            purpose='testing'
        )
        
        if result:
            print("✓ OTP email sent successfully!")
            print(f"  Check {test_email} for the OTP email")
            print(f"  OTP Code (for testing): {otp.otp_code}")
            return True
        else:
            print("✗ OTP email failed to send")
            return False
            
    except Exception as e:
        print(f"\n✗ Error with OTP: {str(e)}")
        import traceback
        traceback.print_exc()
        return False


def test_otp_verification():
    """Test OTP verification"""
    print_header("TESTING OTP VERIFICATION")
    
    test_email = input("\n📧 Enter email to check OTP for: ").strip()
    
    if not test_email:
        print("⏭️  Skipping OTP verification test")
        return False
    
    try:
        print_section("Looking up OTP")
        otp = OTP.objects.filter(email=test_email).order_by('-created_at').first()
        
        if not otp:
            print(f"✗ No OTP found for {test_email}")
            return False
        
        print(f"✓ OTP found: {otp.otp_code}")
        print(f"  - Email: {otp.email}")
        print(f"  - Purpose: {otp.purpose}")
        print(f"  - Created: {otp.created_at}")
        print(f"  - Valid: {otp.is_valid()}")
        
        otp_code = input(f"\nEnter OTP code to verify (or press Enter to skip): ").strip()
        
        if not otp_code:
            print("⏭️  Skipping verification")
            return True
        
        print_section("Verifying OTP")
        result = AuthService.verify_otp(email=test_email, otp_code=otp_code, purpose=otp.purpose)
        
        if result:
            print("✓ OTP verified successfully!")
            return True
        else:
            print("✗ OTP verification failed (invalid or expired)")
            return False
            
    except Exception as e:
        print(f"\n✗ Error with OTP verification: {str(e)}")
        import traceback
        traceback.print_exc()
        return False


def check_logs():
    """Check recent logs for errors"""
    print_header("CHECKING LOGS FOR ERRORS")
    
    log_path = Path('e:/login/auth_project/logs/django.log')
    
    if not log_path.exists():
        print("⚠️  Log file not found at:", log_path)
        return
    
    print_section("Recent Log Errors (last 20 lines with 'error' or 'failed')")
    
    try:
        with open(log_path, 'r', encoding='utf-8', errors='ignore') as f:
            lines = f.readlines()
        
        error_lines = [
            line.strip() for line in lines 
            if 'error' in line.lower() or 'failed' in line.lower()
        ]
        
        if error_lines:
            for line in error_lines[-20:]:
                print(f"  {line}")
        else:
            print("✓ No errors found in logs")
            
    except Exception as e:
        print(f"⚠️  Could not read logs: {str(e)}")


def main_menu():
    """Main test menu"""
    print_header("⚙️  ZEPTOMAIL CONFIGURATION TEST SUITE")
    print("""
This tool will help you verify your ZeptoMail setup for OTP emails.

Tests available:
  1. Check environment variables
  2. Test backend initialization
  3. Send simple test email
  4. Send HTML test email
  5. Test OTP generation & sending
  6. Test OTP verification
  7. Check logs for errors
  8. Run all tests
  9. Exit
""")
    
    choice = input("Select test (1-9): ").strip()
    return choice


if __name__ == "__main__":
    print("\n🚀 UniSync ZeptoMail Test Suite\n")
    
    results = {}
    
    while True:
        choice = main_menu()
        
        if choice == '1':
            check_environment()
        elif choice == '2':
            results['backend'] = test_backend_initialization()
        elif choice == '3':
            results['simple'] = test_simple_email()
        elif choice == '4':
            results['html'] = test_html_email()
        elif choice == '5':
            results['otp'] = test_otp_generation()
        elif choice == '6':
            results['otp_verify'] = test_otp_verification()
        elif choice == '7':
            check_logs()
        elif choice == '8':
            # Run all tests
            check_environment()
            results['backend'] = test_backend_initialization()
            results['simple'] = test_simple_email()
            results['html'] = test_html_email()
            results['otp'] = test_otp_generation()
            print_header("TEST SUMMARY")
            for test, result in results.items():
                status = "✓ PASSED" if result else "✗ FAILED"
                print(f"  {test}: {status}")
        elif choice == '9':
            print("\n👋 Goodbye!\n")
            break
        else:
            print("⚠️  Invalid option. Please select 1-9.")


# Standalone script functionality
if __name__ == "__main__" and len(sys.argv) > 1 and sys.argv[1] == 'auto':
    # Auto-run all tests
    print_header("⚙️  RUNNING ALL ZEPTOMAIL TESTS")
    
    env_ok, from_email, backend = check_environment()
    test_backend_initialization()
    
    if not env_ok:
        print("\n⚠️  Missing credentials. Please configure .env first.")
    else:
        print("\n✓ Environment configured correctly")
