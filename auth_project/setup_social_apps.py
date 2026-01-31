#!/usr/bin/env python
"""
Setup script to create Django Allauth SocialApp entries for Google and GitHub OAuth
"""
import os
import django
from pathlib import Path

# Setup Django
BASE_DIR = Path(__file__).resolve().parent
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'auth_project.settings')
django.setup()

from django.contrib.sites.models import Site
from allauth.socialaccount.models import SocialApp
from django.core.management import execute_from_command_line

def setup_social_apps():
    """Create social app entries for Google and GitHub"""
    print("Setting up UniSync Social Login Apps...")

    # Get or create site
    site, created = Site.objects.get_or_create(
        pk=1,
        defaults={'domain': '127.0.0.1:8000', 'name': 'UniSync Local'}
    )

    if created:
        print(f"Created site: {site.domain}")

    # Clean up duplicates first
    print("Cleaning up duplicate social apps...")

    # Remove duplicates for Google
    google_apps = SocialApp.objects.filter(provider='google')
    if google_apps.count() > 1:
        # Keep the first one, delete the rest
        keep_app = google_apps.first()
        google_apps.exclude(id=keep_app.id).delete()
        print(f"Removed {google_apps.count() - 1} duplicate Google apps")

    # Remove duplicates for GitHub
    github_apps = SocialApp.objects.filter(provider='github')
    if github_apps.count() > 1:
        # Keep the first one, delete the rest
        keep_app = github_apps.first()
        github_apps.exclude(id=keep_app.id).delete()
        print(f"Removed {github_apps.count() - 1} duplicate GitHub apps")

    # Google OAuth App
    google_app, google_created = SocialApp.objects.get_or_create(
        provider='google',
        defaults={
            'name': 'Google OAuth',
            'client_id': os.getenv('GOOGLE_CLIENT_ID', 'your-google-client-id-here'),
            'secret': os.getenv('GOOGLE_CLIENT_SECRET', 'your-google-client-secret-here'),
        }
    )

    if google_created:
        google_app.sites.add(site)
        google_app.save()
        print("Created Google OAuth app")
    else:
        # Ensure it's associated with the site
        if not google_app.sites.filter(id=site.id).exists():
            google_app.sites.add(site)
            google_app.save()
        print("Google OAuth app already exists")

    # GitHub OAuth App
    github_app, github_created = SocialApp.objects.get_or_create(
        provider='github',
        defaults={
            'name': 'GitHub OAuth',
            'client_id': os.getenv('GITHUB_CLIENT_ID', 'your-github-client-id-here'),
            'secret': os.getenv('GITHUB_CLIENT_SECRET', 'your-github-client-secret-here'),
        }
    )

    if github_created:
        github_app.sites.add(site)
        github_app.save()
        print("Created GitHub OAuth app")
    else:
        # Ensure it's associated with the site
        if not github_app.sites.filter(id=site.id).exists():
            github_app.sites.add(site)
            github_app.save()
        print("GitHub OAuth app already exists")

    print("\nSocial login setup complete!")
    print("Summary:")
    print(f"Site: {site.domain}")
    print("Google OAuth: Configured")
    print("GitHub OAuth: Configured")
    print("\nSocial login buttons should now be visible on the login page!")

if __name__ == '__main__':
    setup_social_apps()
