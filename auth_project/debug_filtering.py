#!/usr/bin/env python
import os
import sys
import django

# Setup Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'auth_project.settings')
django.setup()

from accounts.models import StudentProfile, User
from django.db.models import Q

def debug_filtering():
    print("=== DEBUG FILTERING ===")

    # Get all profiles
    all_profiles = StudentProfile.objects.all()
    print(f"Total profiles: {all_profiles.count()}")

    for profile in all_profiles:
        print(f"  - {profile.user.username}: {profile.interests}")

    # Test Python filtering
    print("\n=== Testing Python Filter ===")
    skills_filter = ['python']

    base_profiles = StudentProfile.objects.exclude(user__id=1).select_related('user')

    print(f"Profiles before filtering: {base_profiles.count()}")

    # Apply skills filter
    if skills_filter:
        skills_query = Q()
        for skill in skills_filter:
            skills_query |= Q(interests__icontains=skill.lower())
        base_profiles = base_profiles.filter(skills_query)

    print(f"Profiles after Python filtering: {base_profiles.count()}")

    for profile in base_profiles:
        print(f"  - {profile.user.username}: {profile.interests}")

    # Test URL parameter simulation
    print("\n=== Testing URL Parameter Simulation ===")
    from django.test import RequestFactory
    from accounts.views import find_collaborators

    factory = RequestFactory()
    request = factory.get('/find-collaborators/?skills=python')
    request.user = User.objects.get(id=2)  # Assuming user exists

    try:
        response = find_collaborators(request)
        print("View executed successfully")
    except Exception as e:
        print(f"Error in view: {e}")

if __name__ == '__main__':
    debug_filtering()
