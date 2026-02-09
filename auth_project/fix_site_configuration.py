#!/usr/bin/env python
"""
Fix Django Site configuration for localhost development
"""

import os
import sys
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'auth_project.settings')
django.setup()

from django.contrib.sites.models import Site
from allauth.socialaccount.models import SocialApp

print("=" * 70)
print("FIXING DJANGO SITE CONFIGURATION")
print("=" * 70)

# Get or create localhost site
site, created = Site.objects.get_or_create(
    id=1,
    defaults={
        'domain': 'localhost:8000',
        'name': 'Local Development',
    }
)

if created:
    print(f"\nCreated new site: {site.domain}")
else:
    print(f"\nUpdating existing site...")
    print(f"  Before: {site.domain}")
    site.domain = 'localhost:8000'
    site.name = 'Local Development'
    site.save()
    print(f"  After: {site.domain}")

# Link all SocialApps to the localhost site
print("\n" + "=" * 70)
print("LINKING SOCIALAPPS TO LOCALHOST")
print("=" * 70)

all_apps = SocialApp.objects.all()
print(f"\nFound {all_apps.count()} SocialApp(s):")

for app in all_apps:
    print(f"\n  {app.provider.upper()}: {app.name}")
    
    # Add site if not already linked
    if not app.sites.filter(id=site.id).exists():
        app.sites.add(site)
        print(f"    -> Added to {site.domain}")
    else:
        print(f"    -> Already linked to {site.domain}")

print("\n" + "=" * 70)
print("VERIFICATION")
print("=" * 70)

print(f"\nCurrent site (SITE_ID=1):")
current_site = Site.objects.get(id=1)
print(f"  Domain: {current_site.domain}")
print(f"  Name: {current_site.name}")

print(f"\nSocialApps:")
for app in SocialApp.objects.all():
    sites = [s.domain for s in app.sites.all()]
    print(f"  {app.provider.upper()}: {app.name}")
    print(f"    Sites: {sites}")

print("\n" + "=" * 70)
print("COMPLETE!")
print("=" * 70)
print("\nYour site is now configured for localhost development.")
print("Restart Django: python manage.py runserver")
print("Then visit: http://localhost:8000/login/")
