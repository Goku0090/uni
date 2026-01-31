#!/usr/bin/env python
"""
Debug Profile Photo Storage
Run: python manage.py shell < debug_profile_photo.py
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

print("=" * 70)
print("PROFILE PHOTO DEBUG - DATABASE vs FILESYSTEM")
print("=" * 70)

print("\n📁 FILESYSTEM:")
print(f"MEDIA_ROOT: {settings.MEDIA_ROOT}")
print(f"Exists: {os.path.exists(settings.MEDIA_ROOT)}")

profile_photos_dir = os.path.join(settings.MEDIA_ROOT, 'profile_photos')
print(f"\nProfile photos directory: {profile_photos_dir}")
print(f"Exists: {os.path.exists(profile_photos_dir)}")

if os.path.exists(profile_photos_dir):
    files = os.listdir(profile_photos_dir)
    print(f"Files in directory: {len(files)}")
    for f in sorted(files):
        print(f"  - {f}")

print("\n" + "=" * 70)
print("📊 DATABASE:")
print("=" * 70)

# Check all profiles with photos
profiles_with_photos = StudentProfile.objects.exclude(profile_photo='').exclude(profile_photo__isnull=True)
print(f"\nProfiles with photos (DB): {profiles_with_photos.count()}")

for profile in profiles_with_photos:
    print(f"\n👤 {profile.user.username}:")
    print(f"   DB field value: {profile.profile_photo.name if profile.profile_photo else 'None'}")
    print(f"   DB field path: {profile.profile_photo.path if profile.profile_photo else 'None'}")
    print(f"   URL: {profile.profile_photo.url if profile.profile_photo else 'None'}")
    
    # Check if file exists
    if profile.profile_photo:
        file_path = profile.profile_photo.path
        exists = os.path.exists(file_path)
        print(f"   File exists on disk: {exists} {'✅' if exists else '❌'}")
        if exists:
            size = os.path.getsize(file_path)
            print(f"   File size: {size} bytes")
        else:
            print(f"   Expected path: {file_path}")
    print("   " + "-" * 60)

print("\n" + "=" * 70)
print("SUMMARY:")
print("=" * 70)

missing_files = []
for profile in profiles_with_photos:
    if profile.profile_photo:
        file_path = profile.profile_photo.path
        if not os.path.exists(file_path):
            missing_files.append({
                'user': profile.user.username,
                'filename': profile.profile_photo.name,
                'path': file_path
            })

if missing_files:
    print(f"\n⚠️  {len(missing_files)} MISSING FILES (DB says file exists, but it doesn't):")
    for item in missing_files:
        print(f"\n  User: {item['user']}")
        print(f"  DB filename: {item['filename']}")
        print(f"  Expected path: {item['path']}")
        print(f"  FIX: Delete the DB reference or upload the file again")
else:
    print(f"\n✅ All files in database exist on disk!")

print("\n" + "=" * 70)
