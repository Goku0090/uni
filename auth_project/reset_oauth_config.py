#!/usr/bin/env python
"""
One-command OAuth configuration reset and validation
Handles the MultipleObjectsReturned error from allauth
"""
import os
import sys
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'auth_project.settings')
django.setup()

from allauth.socialaccount.models import SocialApp
from django.contrib.sites.models import Site
from django.conf import settings

def main():
    print("\n" + "=" * 70)
    print("OAUTH CONFIGURATION RESET & FIX")
    print("=" * 70)
    
    # Get current site
    try:
        site = Site.objects.get(id=settings.SITE_ID)
    except Site.DoesNotExist:
        print(f"\nERROR: Site ID {settings.SITE_ID} not found!")
        return False
    
    print(f"\nTarget Site: {site.domain} (ID: {site.id})")
    
    # Step 1: Remove all duplicate SocialApps
    print("\n" + "-" * 70)
    print("STEP 1: Removing Duplicate OAuth Apps")
    print("-" * 70)
    
    providers = ['google', 'github']
    for provider in providers:
        apps = SocialApp.objects.filter(provider=provider)
        count = apps.count()
        
        if count == 0:
            print(f"[SKIP] {provider.upper()}: No apps found")
        elif count == 1:
            app = apps.first()
            print(f"[OK] {provider.upper()}: 1 app exists (ID: {app.id})")
        else:
            print(f"[FIX] {provider.upper()}: Found {count} duplicates, keeping first...")
            keep_id = apps.first().id
            for app in apps.exclude(id=keep_id):
                print(f"       Deleting ID: {app.id}")
                app.delete()
            print(f"       Kept ID: {keep_id}")
    
    # Step 2: Ensure SocialApps are linked to correct site
    print("\n" + "-" * 70)
    print("STEP 2: Linking Apps to Correct Site")
    print("-" * 70)
    
    for provider in providers:
        try:
            app = SocialApp.objects.get(provider=provider)
            
            # Check if app is linked to site
            if not app.sites.filter(id=site.id).exists():
                print(f"[FIX] {provider.upper()}: Linking to site {site.domain}...")
                app.sites.clear()  # Remove from other sites
                app.sites.add(site)  # Add to current site
                print(f"       Linked to Site ID: {site.id}")
            else:
                print(f"[OK] {provider.upper()}: Already linked to {site.domain}")
        
        except SocialApp.DoesNotExist:
            print(f"[SKIP] {provider.upper()}: App not found (OK for production)")
        except Exception as e:
            print(f"[ERROR] {provider.upper()}: {str(e)}")
            return False
    
    # Step 3: Validate configuration
    print("\n" + "-" * 70)
    print("STEP 3: Validating Configuration")
    print("-" * 70)
    
    all_valid = True
    for provider in providers:
        apps = SocialApp.objects.filter(provider=provider)
        
        if apps.count() != 1:
            print(f"[WARN] {provider.upper()}: Expected 1 app, found {apps.count()}")
            all_valid = False
            continue
        
        app = apps.first()
        
        # Check if credentials are placeholder
        if app.client_id.startswith('your-') or app.client_id == '':
            print(f"[WARN] {provider.upper()}: Using placeholder credentials")
            print(f"       Update in Django Admin at /admin/socialaccount/socialapp/")
            continue
        
        # Check if linked to current site
        if not app.sites.filter(id=site.id).exists():
            print(f"[ERROR] {provider.upper()}: Not linked to current site!")
            all_valid = False
            continue
        
        print(f"[OK] {provider.upper()}: Valid configuration")
    
    # Step 4: Final check
    print("\n" + "-" * 70)
    print("STEP 4: OAuth Adapter Test")
    print("-" * 70)
    
    try:
        # This is what fails with MultipleObjectsReturned
        from allauth.socialaccount.adapter import DefaultSocialAccountAdapter
        adapter = DefaultSocialAccountAdapter(None)
        
        for provider in providers:
            try:
                app = adapter.get_app(None, provider)
                if app:
                    print(f"[OK] {provider.upper()}: Adapter can retrieve app")
            except SocialApp.DoesNotExist:
                print(f"[INFO] {provider.upper()}: App not configured (OK)")
            except Exception as e:
                print(f"[ERROR] {provider.upper()}: {type(e).__name__}: {str(e)}")
                all_valid = False
    except Exception as e:
        print(f"[ERROR] Adapter test failed: {str(e)}")
        all_valid = False
    
    # Final summary
    print("\n" + "=" * 70)
    if all_valid:
        print("SUCCESS: OAuth configuration is valid and ready to use!")
    else:
        print("WARNING: OAuth configuration has issues but duplicate apps removed")
    print("=" * 70)
    print("\nNext steps:")
    print("1. If you see 'placeholder credentials' warnings:")
    print("   - Go to http://localhost:8000/admin/socialaccount/socialapp/")
    print("   - Update Google and GitHub credentials")
    print("2. Test OAuth login at http://localhost:8000/accounts/login/")
    print("=" * 70 + "\n")
    
    return True

if __name__ == '__main__':
    try:
        success = main()
        sys.exit(0 if success else 1)
    except Exception as e:
        print(f"\nFATAL ERROR: {str(e)}")
        import traceback
        traceback.print_exc()
        sys.exit(1)
