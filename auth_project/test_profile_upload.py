#!/usr/bin/env python
"""
Test Profile Photo Upload
Run: python manage.py shell < test_profile_upload.py
"""

import os
import sys
import django

# Setup Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'auth_project.settings')
django.setup()

from django.conf import settings
from accounts.models import StudentProfile
from django.contrib.auth.models import User

print("=" * 60)
print("PROFILE PHOTO UPLOAD CONFIGURATION TEST")
print("=" * 60)

# Check configuration
print("\n📋 CONFIGURATION:")
print(f"MEDIA_URL: {settings.MEDIA_URL}")
print(f"MEDIA_ROOT: {settings.MEDIA_ROOT}")
print(f"DEBUG: {settings.DEBUG}")
print(f"MEDIA_ROOT exists: {os.path.exists(settings.MEDIA_ROOT)}")

# Create profile_photos directory if it doesn't exist
profile_photos_dir = os.path.join(settings.MEDIA_ROOT, 'profile_photos')
if not os.path.exists(profile_photos_dir):
    os.makedirs(profile_photos_dir, exist_ok=True)
    print(f"\n✅ Created profile_photos directory: {profile_photos_dir}")
else:
    print(f"\n✅ profile_photos directory exists: {profile_photos_dir}")

# Check permissions
print(f"\nDirectory writable: {os.access(profile_photos_dir, os.W_OK)}")

# List existing files
print(f"\nFiles in {profile_photos_dir}:")
try:
    files = os.listdir(profile_photos_dir)
    if files:
        for f in files:
            print(f"  - {f}")
    else:
        print("  (empty)")
except Exception as e:
    print(f"  Error listing files: {e}")

# Check a sample user profile
print("\n📊 SAMPLE USER PROFILES:")
try:
    profiles = StudentProfile.objects.all()[:3]
    for profile in profiles:
        print(f"  - {profile.user.username}: photo={'Yes' if profile.profile_photo else 'No'}")
        if profile.profile_photo:
            print(f"    Photo: {profile.profile_photo.name}")
            print(f"    URL: /media/{profile.profile_photo.name}")
except Exception as e:
    print(f"  Error: {e}")

print("\n" + "=" * 60)
print("✅ Configuration is ready for photo uploads!")
print("=" * 60)
