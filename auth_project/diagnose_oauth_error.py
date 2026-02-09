#!/usr/bin/env python
"""
Diagnose the MultipleObjectsReturned error from allauth
"""
import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'auth_project.settings')
django.setup()

from allauth.socialaccount.models import SocialApp
from django.contrib.sites.models import Site
from django.conf import settings

print("=" * 70)
print("DIAGNOSING OAUTH MULTIPLEOBJECTSRETURNED ERROR")
print("=" * 70)

# The error happens in adapter.py when calling get_app()
# Let's simulate what it does

print(f"\nCurrent SITE_ID: {settings.SITE_ID}")
current_site = Site.objects.get(id=settings.SITE_ID)
print(f"Current Site: {current_site.domain}")

print("\n" + "=" * 70)
print("CHECKING SOCIALAPP SITES RELATIONSHIPS")
print("=" * 70)

all_apps = SocialApp.objects.all()
print(f"\nTotal SocialApps: {all_apps.count()}")

for app in all_apps:
    sites = app.sites.all()
    print(f"\nApp: {app.name} (ID: {app.id}, Provider: {app.provider})")
    print(f"  Client ID: {app.client_id}")
    print(f"  Sites: {list(sites.values_list('domain', flat=True))}")
    print(f"  Number of sites: {sites.count()}")

print("\n" + "=" * 70)
print("SIMULATING ALLAUTH GET_APP() LOGIC")
print("=" * 70)

# This is what adapter.get_app() does:
# 1. Gets the current site
# 2. Looks for apps where site matches

current_site_id = settings.SITE_ID
print(f"\nLooking for SocialApps linked to Site ID: {current_site_id}")

google_on_site = SocialApp.objects.filter(
    sites__id=current_site_id,
    provider='google'
)

print(f"Google apps on current site: {google_on_site.count()}")
for app in google_on_site:
    print(f"  - {app.name} (ID: {app.id})")

github_on_site = SocialApp.objects.filter(
    sites__id=current_site_id,
    provider='github'
)

print(f"GitHub apps on current site: {github_on_site.count()}")
for app in github_on_site:
    print(f"  - {app.name} (ID: {app.id})")

# Check if any app is associated with multiple sites
print("\n" + "=" * 70)
print("CHECKING FOR MULTI-SITE ASSOCIATIONS")
print("=" * 70)

for app in all_apps:
    site_count = app.sites.count()
    if site_count > 1:
        print(f"\nWARNING: {app.name} is linked to {site_count} sites:")
        for site in app.sites.all():
            print(f"  - {site.domain}")

print("\n" + "=" * 70)
print("SOLUTION")
print("=" * 70)

print("\nThe MultipleObjectsReturned error occurs when:")
print("1. A SocialApp is linked to multiple Sites, OR")
print("2. Multiple SocialApps exist for the same provider on one site")

print("\nTo fix:")
print("1. Ensure each SocialApp is linked to exactly ONE site")
print("2. Or ensure your site matches the OAuth app's site domain")

# Get the current site's domain
print(f"\nYour current Django site: {current_site.domain}")
print(f"Make sure this matches your OAuth provider's redirect URI")
print("\nExample OAuth redirect URIs:")
print(f"  - For localhost: http://localhost:8000/accounts/google/login/callback/")
print(f"  - For production: https://yourdomain.com/accounts/google/login/callback/")
