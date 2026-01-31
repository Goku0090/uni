#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Login Issue Diagnostic Script
Checks all components needed for login to work
"""

import os
import sys
import django

# Setup Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'auth_project.settings')
django.setup()

from django.conf import settings
from django.contrib.auth.models import User
from accounts.models import StudentProfile, OTP

print("="*70)
print("LOGIN ISSUE DIAGNOSTIC")
print("="*70)
print()

# 1. Database Check
print("1. DATABASE CHECK")
print("-" * 70)
try:
    user_count = User.objects.count()
    profile_count = StudentProfile.objects.count()
    print("[OK] Database connected")
    print("   - Total users: {}".format(user_count))
    print("   - Total profiles: {}".format(profile_count))
    
    if user_count == 0:
        print("   [WARN] No users in database!")
        print("   ACTION: Register a user first")
    else:
        print("   Sample users:")
        for u in User.objects.all()[:3]:
            email = u.email if u.email else "NO EMAIL"
            profile = "[OK]" if hasattr(u, 'student_profile') else "[FAIL]"
            print("      - {} ({}) - Profile: {}".format(u.username, email, profile))
except Exception as e:
    print("[ERROR] Database error: {}".format(e))
    
print()

# 2. CSRF Configuration
print("2. CSRF CONFIGURATION")
print("-" * 70)
csrf_enabled = 'django.middleware.csrf.CsrfViewMiddleware' in settings.MIDDLEWARE
print("CSRF middleware: {}".format("[OK] ENABLED" if csrf_enabled else "[FAIL] DISABLED"))
if not csrf_enabled:
    print("   ACTION: Enable CSRF in settings.py middleware list")
print()

# 3. Authentication Configuration
print("3. AUTHENTICATION CONFIGURATION")
print("-" * 70)
backends = settings.AUTHENTICATION_BACKENDS
print("Authentication backends configured: {}".format(len(backends)))
for backend in backends:
    print("   - {}".format(backend))
print()

# 4. Email Configuration
print("4. EMAIL CONFIGURATION")
print("-" * 70)
email_backend = settings.EMAIL_BACKEND
print("Email backend: {}".format(email_backend))
print("Default from email: {}".format(settings.DEFAULT_FROM_EMAIL))

# Check required env vars
required_env_vars = ['BREVO_API_KEY', 'DEFAULT_FROM_EMAIL']
missing = []
for var in required_env_vars:
    value = os.getenv(var)
    if not value:
        missing.append(var)
        print("[FAIL] {}: NOT SET".format(var))
    else:
        masked = value[:5] + '***' if len(value) > 5 else '***'
        print("[OK] {}: {}".format(var, masked))

if missing:
    print("\n[WARN] MISSING EMAIL CONFIG: {}".format(', '.join(missing)))
    print("   ACTION: Set these in .env file")
else:
    print("\n[OK] Email configuration complete")

print()

# 5. Settings Check
print("5. DJANGO SETTINGS")
print("-" * 70)
print("DEBUG: {}".format(settings.DEBUG))
print("DATABASE ENGINE: {}".format(settings.DATABASES['default'].get('ENGINE', 'Unknown')))
print("INSTALLED_APPS: {} apps".format(len(settings.INSTALLED_APPS)))
if 'accounts' in settings.INSTALLED_APPS:
    print("   [OK] accounts app installed")
else:
    print("   [FAIL] accounts app NOT installed")
print()

# 6. Forms Check
print("6. LOGIN FORM CONFIGURATION")
print("-" * 70)
try:
    from accounts.forms import LoginForm
    print("[OK] LoginForm imported successfully")
    form = LoginForm()
    print("   Fields: {}".format(list(form.fields.keys())))
except Exception as e:
    print("[ERROR] LoginForm error: {}".format(e))
print()

# 7. Views Check
print("7. LOGIN VIEW CONFIGURATION")
print("-" * 70)
try:
    from accounts.views import login_view
    print("[OK] login_view imported successfully")
    
    # Check if login_view has email support
    import inspect
    source = inspect.getsource(login_view)
    if 'User.objects.get(email=' in source:
        print("[OK] Email authentication support detected")
    else:
        print("[WARN] No email authentication detected")
except Exception as e:
    print("[ERROR] login_view error: {}".format(e))
print()

# 8. URL Configuration
print("8. URL ROUTING")
print("-" * 70)
try:
    from django.urls import reverse
    login_url = reverse('login')
    print("[OK] Login URL: {}".format(login_url))
except Exception as e:
    print("[ERROR] URL routing error: {}".format(e))
print()

# 9. Session Configuration
print("9. SESSION CONFIGURATION")
print("-" * 70)
print("SESSION_ENGINE: {}".format(settings.SESSION_ENGINE))
print("SESSION_COOKIE_AGE: {} seconds".format(settings.SESSION_COOKIE_AGE))
print("SESSION_COOKIE_SECURE: {}".format(settings.SESSION_COOKIE_SECURE))
print()

# 10. Summary
print("=" * 70)
print("SUMMARY")
print("=" * 70)

issues = []

if user_count == 0:
    issues.append("[FAIL] No users registered - register a user first")
    
if not csrf_enabled:
    issues.append("[FAIL] CSRF middleware disabled - enable it in settings")
    
if missing:
    issues.append("[FAIL] Missing email config: {}".format(', '.join(missing)))

if not issues:
    print("[OK] All checks passed! Login should work.")
    print()
    print("Next steps:")
    print("1. Go to http://localhost:8000/login/")
    print("2. Enter username or email")
    print("3. Enter password")
    print("4. Should see 'OTP sent' message")
    print("5. Check email for OTP")
else:
    print("[WARN] ISSUES FOUND:")
    for issue in issues:
        print("   {}".format(issue))

print()
print("=" * 70)
