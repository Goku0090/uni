"""
Setup OAuth Social Apps for Django-allauth
This fixes the 500 error on /accounts/3rdparty/signup/
"""

import os
import django
from django.conf import settings

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'auth_project.settings')
django.setup()

from allauth.socialaccount.models import SocialApp
from django.contrib.sites.models import Site

def setup_oauth():
    """Create or update SocialApp entries for Google and GitHub"""
    
    # Get or create Site
    site = Site.objects.get_or_create(id=1, defaults={
        'domain': 'localhost:8000',
        'name': 'UniSync'
    })[0]
    
    print(f"Site: {site.domain}")
    
    # ==================== GOOGLE OAUTH ====================
    google_app, created = SocialApp.objects.get_or_create(
        provider='google',
        defaults={
            'name': 'Google',
            'client_id': os.getenv('GOOGLE_OAUTH_CLIENT_ID', 'your-google-client-id'),
            'secret': os.getenv('GOOGLE_OAUTH_SECRET_KEY', 'your-google-secret-key'),
        }
    )
    
    # Ensure site association
    if site not in google_app.sites.all():
        google_app.sites.add(site)
    
    status = "CREATED" if created else "UPDATED"
    print(f"[OK] Google OAuth {status}")
    print(f"  - Client ID: {google_app.client_id}")
    print(f"  - Sites: {list(google_app.sites.all().values_list('domain', flat=True))}")
    
    # ==================== GITHUB OAUTH ====================
    github_app, created = SocialApp.objects.get_or_create(
        provider='github',
        defaults={
            'name': 'GitHub',
            'client_id': os.getenv('GITHUB_OAUTH_CLIENT_ID', 'your-github-client-id'),
            'secret': os.getenv('GITHUB_OAUTH_SECRET_KEY', 'your-github-secret-key'),
        }
    )
    
    # Ensure site association
    if site not in github_app.sites.all():
        github_app.sites.add(site)
    
    status = "CREATED" if created else "UPDATED"
    print(f"[OK] GitHub OAuth {status}")
    print(f"  - Client ID: {github_app.client_id}")
    print(f"  - Sites: {list(github_app.sites.all().values_list('domain', flat=True))}")
    
    print("\n[SUCCESS] OAuth Setup Complete!")
    print("\nNOTE: Update .env with real credentials:")
    print("  GOOGLE_OAUTH_CLIENT_ID=xxx")
    print("  GOOGLE_OAUTH_SECRET_KEY=xxx")
    print("  GITHUB_OAUTH_CLIENT_ID=xxx")
    print("  GITHUB_OAUTH_SECRET_KEY=xxx")

if __name__ == '__main__':
    setup_oauth()
