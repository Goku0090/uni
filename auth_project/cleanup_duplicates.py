#!/usr/bin/env python
"""
Cleanup duplicate SocialApp entries
Run with: python manage.py shell < cleanup_duplicates.py
Or: python cleanup_duplicates.py (if run from same directory as manage.py)
"""

import os
import sys
import django

# Setup Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'auth_project.settings')
django.setup()

from allauth.socialaccount.models import SocialApp
from django.contrib.sites.models import Site

print("=" * 70)
print("CLEANING UP DUPLICATE SOCIAL APPS")
print("=" * 70)

# Get all social apps
all_apps = SocialApp.objects.all()
print(f"\nTotal SocialApp entries in database: {all_apps.count()}")

for app in all_apps:
    sites = [s.domain for s in app.sites.all()]
    print(f"\n  ID: {app.id}")
    print(f"  Name: {app.name}")
    print(f"  Provider: {app.provider}")
    print(f"  Client ID: {app.client_id[:30] if app.client_id else '(empty)'}...")
    print(f"  Sites: {sites}")

# Check for duplicates by provider
print("\n" + "=" * 70)
print("CHECKING FOR DUPLICATES BY PROVIDER")
print("=" * 70)

providers = {}
for app in all_apps:
    if app.provider not in providers:
        providers[app.provider] = []
    providers[app.provider].append(app)

for provider, apps in providers.items():
    print(f"\n{provider.upper()}: {len(apps)} app(s)")
    if len(apps) > 1:
        print(f"  ⚠️  DUPLICATE FOUND! Need to delete {len(apps) - 1} app(s)")

# Delete duplicates - keep only the first one of each provider
print("\n" + "=" * 70)
print("DELETING DUPLICATES")
print("=" * 70)

for provider, apps in providers.items():
    if len(apps) > 1:
        print(f"\n{provider.upper()}:")
        keep_app = apps[0]
        print(f"  ✓ KEEPING: ID={keep_app.id}, Name={keep_app.name}")
        
        for app in apps[1:]:
            print(f"  ✗ DELETING: ID={app.id}, Name={app.name}")
            app.delete()

# Verify cleanup
print("\n" + "=" * 70)
print("VERIFICATION")
print("=" * 70)

all_apps = SocialApp.objects.all()
print(f"\nTotal SocialApp entries after cleanup: {all_apps.count()}\n")

if all_apps.count() == 0:
    print("  (No SocialApp entries - OAuth will be disabled)")
else:
    for app in all_apps:
        sites = [s.domain for s in app.sites.all()]
        print(f"  ✓ {app.provider.upper()}: {app.name} (ID={app.id})")
        print(f"    Sites: {sites}")

print("\n✅ CLEANUP COMPLETE!")
print("=" * 70)
print("\nNext steps:")
print("1. Restart Django: python manage.py runserver")
print("2. Visit: http://localhost:8000/login/")
print("3. Should load without error now!")
