#!/usr/bin/env python
"""
Fix duplicate SocialApp entries for OAuth providers
"""
import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'auth_project.settings')
django.setup()

from allauth.socialaccount.models import SocialApp
from django.contrib.sites.models import Site

print("=" * 70)
print("CHECKING FOR DUPLICATE OAUTH APPS")
print("=" * 70)

# Check for duplicate Google apps
google_apps = SocialApp.objects.filter(provider='google')
print(f"\nTotal Google apps: {google_apps.count()}")
for app in google_apps:
    sites = list(app.sites.all())
    print(f"   ID: {app.id}")
    print(f"   Name: {app.name}")
    print(f"   Client ID: {app.client_id[:20]}...")
    print(f"   Sites: {[s.domain for s in sites]}")
    print()

# Check for duplicate GitHub apps
github_apps = SocialApp.objects.filter(provider='github')
print(f"Total GitHub apps: {github_apps.count()}")
for app in github_apps:
    sites = list(app.sites.all())
    print(f"   ID: {app.id}")
    print(f"   Name: {app.name}")
    print(f"   Client ID: {app.client_id[:20]}...")
    print(f"   Sites: {[s.domain for s in sites]}")
    print()

# Check all sites
sites = Site.objects.all()
print(f"Total Sites: {sites.count()}")
for site in sites:
    print(f"   ID: {site.id}, Domain: {site.domain}, Name: {site.name}")
    print()

print("\n" + "=" * 70)
print("CURRENT SITE IN DJANGO")
print("=" * 70)
from django.conf import settings
print(f"SITE_ID: {settings.SITE_ID}")
current_site = Site.objects.get(id=settings.SITE_ID)
print(f"Current Site: {current_site.domain} (ID: {current_site.id})")

print("\n" + "=" * 70)
print("FIX STRATEGY")
print("=" * 70)

if google_apps.count() > 1:
    print(f"\nFound {google_apps.count()} Google apps - DUPLICATE DETECTED")
    print("   Keeping the first one, deleting duplicates...")
    
    keep_id = google_apps.first().id
    delete_ids = google_apps.values_list('id', flat=True)[1:]
    
    for app_id in delete_ids:
        app = SocialApp.objects.get(id=app_id)
        print(f"   [DELETING] Google app ID: {app_id} ({app.name})")
        app.delete()
    
    print(f"   [KEPT] Google app ID: {keep_id}")
else:
    print("\n[OK] Google apps are OK (0 or 1)")

if github_apps.count() > 1:
    print(f"\nFound {github_apps.count()} GitHub apps - DUPLICATE DETECTED")
    print("   Keeping the first one, deleting duplicates...")
    
    keep_id = github_apps.first().id
    delete_ids = github_apps.values_list('id', flat=True)[1:]
    
    for app_id in delete_ids:
        app = SocialApp.objects.get(id=app_id)
        print(f"   [DELETING] GitHub app ID: {app_id} ({app.name})")
        app.delete()
    
    print(f"   [KEPT] GitHub app ID: {keep_id}")
else:
    print("\n[OK] GitHub apps are OK (0 or 1)")

print("\n" + "=" * 70)
print("VERIFICATION")
print("=" * 70)

google_apps_after = SocialApp.objects.filter(provider='google')
github_apps_after = SocialApp.objects.filter(provider='github')

print(f"\nGoogle apps after fix: {google_apps_after.count()}")
if google_apps_after.exists():
    app = google_apps_after.first()
    print(f"   [OK] {app.name} (ID: {app.id})")
    print(f"   Sites: {[s.domain for s in app.sites.all()]}")

print(f"\nGitHub apps after fix: {github_apps_after.count()}")
if github_apps_after.exists():
    app = github_apps_after.first()
    print(f"   [OK] {app.name} (ID: {app.id})")
    print(f"   Sites: {[s.domain for s in app.sites.all()]}")

print("\n" + "=" * 70)
print("DUPLICATE OAUTH APPS FIXED!")
print("=" * 70)
