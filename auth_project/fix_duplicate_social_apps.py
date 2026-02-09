#!/usr/bin/env python
"""
Fix: MultipleObjectsReturned error from django-allauth
Removes duplicate SocialApp entries in the database
"""

import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'auth_project.settings')
django.setup()

from allauth.socialaccount.models import SocialApp
from django.contrib.sites.models import Site

print("=" * 80)
print("CLEANING UP DUPLICATE SOCIAL APPS")
print("=" * 80)

# Get current site
try:
    current_site = Site.objects.get_current()
    print(f"\nCurrent Site: {current_site.name} (ID: {current_site.id})")
except:
    print("\n⚠️ Could not get current site")

# List all social apps
print("\n" + "=" * 80)
print("CURRENT SOCIAL APPS IN DATABASE")
print("=" * 80)

all_apps = SocialApp.objects.all()
print(f"\nTotal Social Apps: {all_apps.count()}")

provider_groups = {}
for app in all_apps:
    provider = app.provider
    if provider not in provider_groups:
        provider_groups[provider] = []
    provider_groups[provider].append(app)
    print(f"\n📱 ID: {app.id}")
    print(f"   Provider: {app.provider}")
    print(f"   Name: {app.name}")
    print(f"   Client ID: {app.client_id[:20]}..." if len(app.client_id) > 20 else f"   Client ID: {app.client_id}")
    print(f"   Sites: {list(app.sites.all())}")

# Find duplicates
print("\n" + "=" * 80)
print("DUPLICATE DETECTION")
print("=" * 80)

has_duplicates = False
for provider, apps in provider_groups.items():
    if len(apps) > 1:
        has_duplicates = True
        print(f"\n⚠️ DUPLICATE FOUND: {provider}")
        print(f"   Count: {len(apps)} apps")
        for i, app in enumerate(apps, 1):
            print(f"   {i}. ID: {app.id}, Name: {app.name}")

if not has_duplicates:
    print("\n✅ No duplicates found!")
else:
    print("\n" + "=" * 80)
    print("FIX OPTIONS")
    print("=" * 80)
    print("\nOption 1: AUTO-DELETE (Keep first, delete rest)")
    print("  Run: python manage.py shell")
    print("  Then paste the code below:\n")
    
    print("""
from allauth.socialaccount.models import SocialApp

# Delete duplicates (keep first app of each provider)
for provider, apps in {
    'google': SocialApp.objects.filter(provider='google'),
    'github': SocialApp.objects.filter(provider='github'),
}.items():
    if apps.count() > 1:
        to_delete = list(apps)[1:]
        for app in to_delete:
            print(f"Deleting duplicate {provider} app (ID: {app.id})")
            app.delete()
""")

print("\nOption 2: MANUAL-DELETE")
print("  python manage.py shell")
print("  from allauth.socialaccount.models import SocialApp")
print("  SocialApp.objects.get(id=X).delete()  # Replace X with app ID")

print("\n" + "=" * 80)
