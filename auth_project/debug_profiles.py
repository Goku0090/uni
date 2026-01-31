#!/usr/bin/env python
import os
import django

# Setup Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'auth_project.settings')
django.setup()

from accounts.models import StudentProfile

def debug_profiles():
    print("=== DEBUGGING STUDENT PROFILES ===")

    # Get all profiles
    profiles = StudentProfile.objects.all()
    print(f"Total profiles: {profiles.count()}")

    print("\n=== First 5 profiles ===")
    for profile in profiles[:5]:
        print(f"Profile: {profile.full_name}")
        print(f"  Interests: {repr(profile.interests)}")
        print(f"  College: {profile.college}")
        print(f"  Location: {profile.location}")
        print()

    # Check for profiles with python
    print("=== Profiles with 'python' in interests ===")
    python_profiles = StudentProfile.objects.filter(interests__icontains='python')
    print(f"Profiles with python: {python_profiles.count()}")

    for profile in python_profiles:
        print(f"Python profile: {profile.full_name}")
        print(f"  Interests: {repr(profile.interests)}")
        print()

    # Check for profiles with 'Python' (capital P)
    print("=== Profiles with 'Python' in interests ===")
    python_capital_profiles = StudentProfile.objects.filter(interests__icontains='Python')
    print(f"Profiles with 'Python': {python_capital_profiles.count()}")

    for profile in python_capital_profiles:
        print(f"Python profile: {profile.full_name}")
        print(f"  Interests: {repr(profile.interests)}")
        print()

    # Check all unique interests
    print("=== All unique interests ===")
    all_interests = set()
    for profile in profiles:
        if profile.interests:
            interests = [interest.strip().lower() for interest in profile.interests.split(',')]
            all_interests.update(interests)

    print("Unique interests:", sorted(list(all_interests)))

if __name__ == '__main__':
    debug_profiles()
