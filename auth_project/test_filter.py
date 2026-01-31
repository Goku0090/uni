#!/usr/bin/env python
import os
import sys
import django

# Setup Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'auth_project.settings')
django.setup()

from accounts.models import StudentProfile, User
from django.db.models import Q

def test_filtering():
    print("=== Testing Python Filter ===")

    # Test filtering
    skills_filter = ['python']
    base_profiles = StudentProfile.objects.exclude(user__id=1).select_related('user')

    print(f'Profiles before filtering: {base_profiles.count()}')

    # Apply skills filter
    if skills_filter:
        skills_query = Q()
        for skill in skills_filter:
            skills_query |= Q(interests__icontains=skill.lower())
        base_profiles = base_profiles.filter(skills_query)

    print(f'Profiles after Python filtering: {base_profiles.count()}')

    for profile in base_profiles:
        print(f'  - {profile.user.username}: {profile.interests}')

if __name__ == '__main__':
    test_filtering()
