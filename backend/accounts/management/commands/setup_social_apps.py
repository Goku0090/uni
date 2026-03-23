"""
Management command to set up social apps for OAuth login
"""
import os
from django.core.management.base import BaseCommand
from django.contrib.sites.models import Site
from allauth.socialaccount.models import SocialApp


class Command(BaseCommand):
    help = 'Set up social apps for OAuth login'

    def handle(self, *args, **options):
        # Get the current site
        site = Site.objects.get_or_create(id=1)[0]
        site.domain = os.getenv('RENDER_EXTERNAL_HOSTNAME', 'unisinq.onrender.com')
        site.name = 'UniSinq'
        site.save()
        self.stdout.write(f"Updated site: {site.domain}")

        # Get OAuth credentials from environment
        google_client_id = os.getenv('GOOGLE_CLIENT_ID', '').strip()
        google_client_secret = os.getenv('GOOGLE_CLIENT_SECRET', '').strip()
        github_client_id = os.getenv('GITHUB_CLIENT_ID', '').strip()
        github_client_secret = os.getenv('GITHUB_CLIENT_SECRET', '').strip()

        # Set up Google OAuth
        if google_client_id and google_client_secret:
            google_app, created = SocialApp.objects.get_or_create(
                provider='google',
                defaults={
                    'name': 'Google'
                }
            )
            google_app.client_id = google_client_id
            google_app.secret = google_client_secret
            google_app.save()
            google_app.sites.add(site)
            self.stdout.write(self.style.SUCCESS(f"Google OAuth app {'created' if created else 'updated'}"))
        else:
            self.stdout.write(self.style.WARNING("Google OAuth credentials not found in environment"))

        # Set up GitHub OAuth
        if github_client_id and github_client_secret:
            github_app, created = SocialApp.objects.get_or_create(
                provider='github',
                defaults={
                    'name': 'GitHub'
                }
            )
            github_app.client_id = github_client_id
            github_app.secret = github_client_secret
            github_app.save()
            github_app.sites.add(site)
            self.stdout.write(self.style.SUCCESS(f"GitHub OAuth app {'created' if created else 'updated'}"))
        else:
            self.stdout.write(self.style.WARNING("GitHub OAuth credentials not found in environment"))

        # List all social apps
        self.stdout.write("\nCurrent social apps:")
        for app in SocialApp.objects.all():
            self.stdout.write(f"  - {app.provider}: {app.name}")
