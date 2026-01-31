#!/usr/bin/env python
"""
Quick fix for broken profile photos
Run: python manage.py shell < fix_pongal_now.py
"""

import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'auth_project.settings')
django.setup()

from accounts.models import StudentProfile
from django.contrib.auth.models import User

print("=" * 60)
print("FIXING BROKEN PROFILE PHOTOS")
print("=" * 60)

# Find and clear all broken photo references
profiles_with_photos = StudentProfile.objects.exclude(profile_photo='').exclude(profile_photo__isnull=True)

fixed = 0
for profile in profiles_with_photos:
    if profile.profile_photo:
        file_path = profile.profile_photo.path
        if not os.path.exists(file_path):
            print(f"\n❌ Found broken: {profile.user.username}")
            print(f"   File: {profile.profile_photo.name}")
            print(f"   Path: {file_path}")
            
            # Clear it
            profile.profile_photo = None
            profile.save()
            print(f"   ✅ CLEARED")
            fixed += 1

print("\n" + "=" * 60)
if fixed > 0:
    print(f"✅ FIXED {fixed} broken photo reference(s)")
    print("\nNow you can:")
    print("1. Go to http://127.0.0.1:8000/student-profile/")
    print("2. Upload a new photo")
    print("3. Click Save")
    print("\nPhoto should now work! ✅")
else:
    print("✅ No broken photos found!")
print("=" * 60)
