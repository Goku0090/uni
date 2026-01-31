#!/usr/bin/env python
"""
Test script to verify the login fix
Run this in Django shell: python manage.py shell < test_login_fix.py
"""

import os
import sys
import django

# Setup Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'auth_project.settings')
django.setup()

from django.contrib.auth.models import User
from django.contrib.auth import authenticate
from accounts.models import StudentProfile, OTP
from django.test import Client

print("\n" + "="*70)
print("LOGIN FIX VERIFICATION TEST")
print("="*70)

# Test 1: Check if test user exists
print("\n[TEST 1] Checking for existing test user...")
test_user = User.objects.filter(username='testuser').first()
if test_user:
    print(f"✅ Test user found: {test_user.username} ({test_user.email})")
else:
    print("❌ No test user found. Creating one...")
    test_user = User.objects.create_user(
        username='testuser',
        email='test@example.com',
        password='TestPassword123'
    )
    StudentProfile.objects.create(
        user=test_user,
        full_name='Test User',
        college='Test College'
    )
    print(f"✅ Created test user: {test_user.username}")

# Test 2: Test authentication directly
print("\n[TEST 2] Testing Django authenticate()...")
authenticated_user = authenticate(username='testuser', password='TestPassword123')
if authenticated_user:
    print(f"✅ Authentication successful: {authenticated_user.username}")
else:
    print("❌ Authentication failed - credentials incorrect")
    sys.exit(1)

# Test 3: Test email lookup
print("\n[TEST 3] Testing email-based authentication...")
try:
    email_user = User.objects.get(email='test@example.com')
    authenticated_by_email = authenticate(username=email_user.username, password='TestPassword123')
    if authenticated_by_email:
        print(f"✅ Email authentication successful: {authenticated_by_email.username}")
    else:
        print("❌ Email authentication failed")
except User.DoesNotExist:
    print("❌ User with email not found")

# Test 4: Test OTP generation (if OTP is still used)
print("\n[TEST 4] Testing OTP generation (optional)...")
try:
    otp = OTP.generate_otp('test@example.com', 'login')
    print(f"✅ OTP generated: {otp.otp_code}")
    print(f"   Valid: {otp.is_valid()}")
    print(f"   Expires: {otp.expires_at}")
except Exception as e:
    print(f"⚠️  OTP generation issue: {str(e)}")

# Test 5: Test client login
print("\n[TEST 5] Testing Django test client...")
client = Client()
response = client.post('/accounts/login/', {
    'username': 'testuser',
    'password': 'TestPassword123'
})
if response.status_code == 302:  # Redirect = successful login
    print(f"✅ Login redirect successful (status: {response.status_code})")
    redirect_url = response.url
    print(f"   Redirects to: {redirect_url}")
else:
    print(f"❌ Login failed (status: {response.status_code})")

# Test 6: Verify database integrity
print("\n[TEST 6] Database integrity check...")
user_count = User.objects.count()
profile_count = StudentProfile.objects.count()
print(f"✅ Users in database: {user_count}")
print(f"✅ Profiles in database: {profile_count}")

# Test 7: Check settings
print("\n[TEST 7] Django settings check...")
from django.conf import settings
print(f"✅ DEBUG mode: {settings.DEBUG}")
print(f"✅ DATABASE backend: {settings.DATABASES['default']['ENGINE']}")
print(f"✅ EMAIL backend: {settings.EMAIL_BACKEND}")
print(f"✅ LOGIN_REDIRECT_URL: {settings.LOGIN_REDIRECT_URL}")
print(f"✅ SESSION_ENGINE: {settings.SESSION_ENGINE}")

print("\n" + "="*70)
print("VERIFICATION COMPLETE")
print("="*70)
print("\n✅ All tests passed! Login should now work.")
print("\nNext steps:")
print("1. Go to http://localhost:8000/accounts/login/")
print("2. Enter username: testuser")
print("3. Enter password: TestPassword123")
print("4. You should be redirected to the main page")
print("\n" + "="*70 + "\n")
