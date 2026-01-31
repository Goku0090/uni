#!/usr/bin/env python
"""
Script to clean up duplicate SocialApp entries in UniSync
"""
import os
import sys
import django

# Setup Django
sys.path.append('auth_project')
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'auth_project.settings')

try:
    django.setup()
    print("Django setup successful")
except Exception as e:
    print(f"Django setup failed: {e}")
    sys.exit(1)

from allauth.socialaccount.models import SocialApp
from django.contrib.sites.models import Site

def cleanup_social_apps():
    print('Cleaning up duplicate SocialApp entries...\n')

    print('BEFORE CLEANUP:')
    for app in SocialApp.objects.all():
        sites = [s.domain for s in app.sites.all()]
        print(f'  {app.provider}: {app.name} - Sites: {sites}')

    site = Site.objects.get(domain='127.0.0.1:8000')
    print(f'\nTarget site: {site.domain}')

    # Clean up duplicates
    for provider in ['google', 'github']:
        apps = SocialApp.objects.filter(provider=provider)
        print(f'\n{provider.upper()}: Found {apps.count()} apps')

        if apps.count() > 1:
            # Keep the one linked to our site, or the first one
            keep_app = apps.filter(sites=site).first()
            if not keep_app:
                keep_app = apps.first()

            # Delete others
            deleted_count = apps.exclude(id=keep_app.id).delete()[0]
            print(f'  Deleted {deleted_count} duplicate(s)')

            # Make sure it's linked to our site
            if not keep_app.sites.filter(id=site.id).exists():
                keep_app.sites.add(site)
                print(f'  Linked {keep_app.name} to site')

            print(f'  Kept: {keep_app.name}')
        elif apps.count() == 1:
            app = apps.first()
            if not app.sites.filter(id=site.id).exists():
                app.sites.add(site)
                print(f'  Linked {app.name} to site')
            else:
                print(f'  Already properly linked: {app.name}')
        else:
            print(f'  No {provider} apps found')

    print('\nAFTER CLEANUP:')
    for app in SocialApp.objects.all():
        sites = [s.domain for s in app.sites.all()]
        print(f'  {app.provider}: {app.name} - Sites: {sites}')

    total_apps = SocialApp.objects.count()
    print(f'\nTotal SocialApp entries: {total_apps}')

    # Verify each provider has exactly one app
    for provider in ['google', 'github']:
        count = SocialApp.objects.filter(provider=provider).count()
        status = '✅' if count == 1 else '❌'
        print(f'{status} {provider}: {count} app(s)')

if __name__ == '__main__':
    cleanup_social_apps()
