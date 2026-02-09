#!/usr/bin/env python
"""
Deep debugging of the MultipleObjectsReturned error
"""
import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'auth_project.settings')
django.setup()

from allauth.socialaccount.models import SocialApp
from django.contrib.sites.models import Site
from django.conf import settings
from django.db.models import Count

print("=" * 70)
print("DEEP DEBUG: MultipleObjectsReturned Error")
print("=" * 70)

# Get all apps and their site relationships
print("\n[1] Raw Database Query:")
print("-" * 70)

all_apps = SocialApp.objects.all()
print(f"Total SocialApps in database: {all_apps.count()}")

for app in all_apps:
    print(f"\nApp: {app.name} (ID: {app.id}, Provider: {app.provider})")
    print(f"  Client ID: {app.client_id}")
    sites = app.sites.all()
    print(f"  Linked to {sites.count()} site(s):")
    for site in sites:
        print(f"    - {site.domain} (ID: {site.id})")

# Check the actual query that's failing
print("\n[2] Simulating Allauth Query:")
print("-" * 70)

site = Site.objects.get(id=settings.SITE_ID)
print(f"Current Site: {site.domain} (ID: {site.id})")

# This is the actual allauth query that's failing
print("\nQuery: SocialApp.objects.filter(sites__id={}, provider='google')")
google_apps = SocialApp.objects.filter(sites__id=site.id, provider='google')
print(f"Result: {google_apps.count()} app(s)")
for app in google_apps:
    print(f"  - ID: {app.id}, Name: {app.name}")

print("\nQuery: SocialApp.objects.filter(sites__id={}, provider='github')")
github_apps = SocialApp.objects.filter(sites__id=site.id, provider='github')
print(f"Result: {github_apps.count()} app(s)")
for app in github_apps:
    print(f"  - ID: {app.id}, Name: {app.name}")

# Check through-table directly
print("\n[3] Checking M2M Through Table:")
print("-" * 70)

from django.db import connection
from django.apps import apps

SocialAppModel = apps.get_model('socialaccount', 'SocialApp')
through_model = SocialAppModel.sites.through

print(f"\nThrough table: {through_model._meta.db_table}")

# Direct query
with connection.cursor() as cursor:
    cursor.execute(f"SELECT * FROM {through_model._meta.db_table}")
    rows = cursor.fetchall()
    print(f"Rows in through table: {len(rows)}")
    for row in rows:
        print(f"  {row}")

# Check for duplicate M2M entries
print("\n[4] Checking for Duplicate M2M Entries:")
print("-" * 70)

through_instances = through_model.objects.all()
print(f"Total M2M entries: {through_instances.count()}")

# Group by app and site
from django.db.models import Count
duplicates = through_model.objects.values('socialapp_id', 'site_id').annotate(
    count=Count('*')
).filter(count__gt=1)

if duplicates.exists():
    print("DUPLICATES FOUND IN M2M TABLE:")
    for dup in duplicates:
        print(f"  App ID: {dup['socialapp_id']}, Site ID: {dup['site_id']}, Count: {dup['count']}")
        # Delete duplicates
        entries = through_model.objects.filter(
            socialapp_id=dup['socialapp_id'],
            site_id=dup['site_id']
        )
        print(f"    Deleting {entries.count() - 1} duplicate(s)...")
        entries[1:].delete()
else:
    print("No duplicate M2M entries found")

# Re-test
print("\n[5] Re-testing After Cleanup:")
print("-" * 70)

print("Query: SocialApp.objects.filter(sites__id={}, provider='google')")
google_apps = SocialApp.objects.filter(sites__id=site.id, provider='google')
print(f"Result: {google_apps.count()} app(s)")

print("Query: SocialApp.objects.filter(sites__id={}, provider='github')")
github_apps = SocialApp.objects.filter(sites__id=site.id, provider='github')
print(f"Result: {github_apps.count()} app(s)")

print("\n" + "=" * 70)
print("DONE")
print("=" * 70)
