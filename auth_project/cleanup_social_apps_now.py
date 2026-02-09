#!/usr/bin/env python
"""
AUTO-FIX: Remove all duplicate SocialApp entries
"""

import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'auth_project.settings')
django.setup()

from allauth.socialaccount.models import SocialApp

print("=" * 80)
print("REMOVING DUPLICATE SOCIAL APPS")
print("=" * 80)

providers = ['google', 'github']
total_deleted = 0

for provider in providers:
    apps = SocialApp.objects.filter(provider=provider)
    count = apps.count()
    
    if count > 1:
        print(f"\n⚠️ Found {count} {provider} apps")
        
        # Keep first, delete rest
        apps_to_delete = list(apps)[1:]
        
        for app in apps_to_delete:
            print(f"  🗑️  Deleting: ID={app.id}, Name={app.name}")
            app.delete()
            total_deleted += 1
        
        print(f"  ✅ Kept: ID={apps.first().id}, Name={apps.first().name}")
    
    elif count == 1:
        print(f"\n✅ {provider}: OK (1 app)")
    else:
        print(f"\n❌ {provider}: NOT CONFIGURED (0 apps)")

print("\n" + "=" * 80)
print(f"SUMMARY: Deleted {total_deleted} duplicate apps")
print("=" * 80)

# Show final state
print("\nFinal Social Apps:")
for app in SocialApp.objects.all():
    print(f"  ✅ {app.provider.upper()}: {app.name}")

print("\n✅ CLEANUP COMPLETE - Your login page should now work!")
print("=" * 80)
