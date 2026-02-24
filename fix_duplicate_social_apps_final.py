#!/usr/bin/env python
"""
Fix duplicate SocialApp entries in django-allauth
This script removes duplicate OAuth app configurations
"""

import os
import sys
import django

# Setup Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'auth_project.settings')
# Add backend directory to path
backend_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'backend')
sys.path.insert(0, backend_dir)

django.setup()

from django.contrib.sites.models import Site
from allauth.socialaccount.models import SocialApp

def cleanup_social_apps():
    """Remove duplicate SocialApp entries"""
    
    print("=" * 60)
    print("CLEANING UP DUPLICATE SOCIAL APPS")
    print("=" * 60)
    
    # Get current site
    try:
        site = Site.objects.get_current()
        print(f"\n✓ Current site: {site.domain} (ID: {site.id})")
    except Exception as e:
        print(f"✗ Error getting site: {e}")
        return
    
    # Providers to check
    providers = ['google', 'github']
    
    for provider in providers:
        print(f"\n{'─' * 60}")
        print(f"Processing provider: {provider.upper()}")
        print('─' * 60)
        
        apps = SocialApp.objects.filter(provider=provider)
        
        if not apps.exists():
            print(f"  ℹ No {provider} apps found")
            continue
        
        print(f"  Found {apps.count()} {provider} app(s):")
        
        for idx, app in enumerate(apps, 1):
            site_names = [s.domain for s in app.sites.all()]
            print(f"\n    [{idx}] {app.name}")
            print(f"        ID: {app.id}")
            print(f"        Provider: {app.provider}")
            print(f"        Client ID: {app.client_id[:20]}..." if app.client_id else "        Client ID: (none)")
            print(f"        Sites: {', '.join(site_names) if site_names else '(none)'}")
        
        # Keep the first one, delete others
        if apps.count() > 1:
            print(f"\n  ⚠ Found {apps.count()} duplicate(s)")
            keep_app = apps.first()
            delete_apps = apps.exclude(id=keep_app.id)
            
            print(f"\n  ✓ Keeping: {keep_app.name} (ID: {keep_app.id})")
            
            # Make sure the kept app is linked to current site
            if not keep_app.sites.filter(id=site.id).exists():
                print(f"    → Adding current site to {provider} app")
                keep_app.sites.add(site)
            
            # Delete duplicates
            for app in delete_apps:
                print(f"  ✗ Deleting duplicate: {app.name} (ID: {app.id})")
                app.delete()
            
            print(f"\n  ✓ Cleanup complete for {provider}")
        else:
            print(f"\n  ✓ Only one {provider} app found (no duplicates)")
    
    print("\n" + "=" * 60)
    print("✓ CLEANUP COMPLETE")
    print("=" * 60)
    
    # Summary
    print("\nFinal status:")
    for provider in providers:
        count = SocialApp.objects.filter(provider=provider).count()
        if count == 0:
            print(f"  • {provider.capitalize()}: NOT CONFIGURED (buttons will be disabled)")
        elif count == 1:
            print(f"  • {provider.capitalize()}: ✓ Configured (1 app)")
        else:
            print(f"  • {provider.capitalize()}: ✗ ERROR ({count} apps - still have duplicates!)")

if __name__ == '__main__':
    cleanup_social_apps()
