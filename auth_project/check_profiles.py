#!/usr/bin/env python
import os
import django
import sys

# Setup Django
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'auth_project.settings')
django.setup()

from django.contrib.auth.models import User
from accounts.models import StudentProfile

def check_users():
    print("=== User Statistics ===")
    total_users = User.objects.count()
    users_with_profiles = StudentProfile.objects.count()
    users_without_profiles = User.objects.exclude(student_profile__isnull=False).count()

    print(f"Total users: {total_users}")
    print(f"Users with profiles: {users_with_profiles}")
    print(f"Users without profiles: {users_without_profiles}")

    print("\n=== Sample Users ===")
    users = User.objects.all()[:5]
    for user in users:
        has_profile = hasattr(user, 'student_profile') and user.student_profile
        profile_status = "HAS PROFILE" if has_profile else "NO PROFILE"
        print(f"- {user.username}: {profile_status}")
        if has_profile:
            interests = user.student_profile.interests or "No interests"
            college = user.student_profile.college or "No college"
            print(f"  Interests: {interests[:50]}...")
            print(f"  College: {college}")

if __name__ == "__main__":
    check_users()
