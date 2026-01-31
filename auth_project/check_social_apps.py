#!/usr/bin/env python
"""Check for duplicate social apps in database."""

import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'auth_project.settings')
django.setup()

from allauth.socialaccount.models import SocialApp
from collections import Counter

print("=" * 70)
print("SOCIAL APPS IN DATABASE")
print("=" * 70)

apps = SocialApp.objects.all()

if not apps.exists():
    print("✅ No social apps configured (safe)")
else:
    for app in apps:
        print(f"\nID: {app.id}")
        print(f"Provider: {app.provider}")
        print(f"Name: {app.name}")
        print(f"Client ID: {app.client_id[:20]}..." if app.client_id else "Client ID: EMPTY")
        print(f"Sites: {list(app.sites.all())}")

print("\n" + "=" * 70)
print(f"TOTAL APPS: {apps.count()}")
print("=" * 70)

# Check for duplicates
providers = [app.provider for app in apps]
duplicates = [p for p, count in Counter(providers).items() if count > 1]

if duplicates:
    print(f"\n⚠️  DUPLICATES FOUND FOR: {duplicates}")
    print("\nTo fix, delete the duplicates:")
    for provider in duplicates:
        dupe_apps = SocialApp.objects.filter(provider=provider)
        print(f"\n  {provider} apps:")
        for app in dupe_apps:
            print(f"    ID {app.id}: {app.name}")
        print(f"  → Keep one, delete others by ID")
else:
    print("\n✅ No duplicates found")
