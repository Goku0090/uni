#!/usr/bin/env python
import os
import django

# Setup Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'auth_project.settings')
django.setup()

from accounts.models import StudentProfile
from django.contrib.auth import get_user_model

def create_test_profiles():
    User = get_user_model()

    # Create test users and profiles with Python skills
    users_data = [
        ('test_python1', 'python, javascript, react'),
        ('test_python2', 'python, django, machine learning'),
        ('test_python3', 'python, data science, ai'),
        ('test_web_dev', 'javascript, react, html, css'),
        ('test_designer', 'design, ui/ux, figma, photoshop'),
    ]

    print("Creating test profiles...")

    for username, interests in users_data:
        if not User.objects.filter(username=username).exists():
            user = User.objects.create_user(
                username=username,
                email=f'{username}@test.com',
                password='test123'
            )
            profile = StudentProfile.objects.create(
                user=user,
                full_name=username.replace('_', ' ').title(),
                interests=interests,
                college='Test University',
                location='Test City',
                profile_completed=True
            )
            print(f'[OK] Created profile: {profile.full_name} with interests: {profile.interests}')
        else:
            print(f'[SKIP] User {username} already exists')

    print("\n=== VERIFICATION ===")
    # Verify the profiles were created
    python_profiles = StudentProfile.objects.filter(interests__icontains='python')
    print(f"Profiles with 'python': {python_profiles.count()}")

    for profile in python_profiles:
        print(f"  - {profile.full_name}: {profile.interests}")

    print(f"\nTotal profiles now: {StudentProfile.objects.count()}")

if __name__ == '__main__':
    create_test_profiles()
