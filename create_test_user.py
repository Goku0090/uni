#!/usr/bin/env python
"""
Quick script to create a test user for UniSync
Run with: python create_test_user.py
"""

import os
import sys
import django

# Add the auth_project directory to Python path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'auth_project'))

# Configure Django settings
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'auth_project.settings')
django.setup()

from django.contrib.auth.models import User
from accounts.models import StudentProfile

def create_test_user():
    """Create a test user for development testing"""

    # Use a unique username based on timestamp
    import time
    username = f'testuser{int(time.time())}'

    # Create a fresh test user
    try:
        user = User.objects.create_user(
            username=username,
            email=f'{username}@example.com',
            password='testpass123',
            first_name='Test',
            last_name='User'
        )
        print(f'[SUCCESS] Created user: {user.username} / {user.email}')

        # Create profile
        profile = StudentProfile.objects.create(
            user=user,
            full_name='Test User',
            college='Test College',
            profile_completed=True
        )
        print(f'[SUCCESS] Created profile: {profile.full_name}')

        print('\n' + '='*50)
        print('TEST USER CREATED SUCCESSFULLY!')
        print('='*50)
        print(f'Username: {username}')
        print('Password: testpass123')
        print(f'Email: {user.email}')
        print()
        print('TEST URLS:')
        print('Main site: http://127.0.0.1:8000/')
        print('Login page: http://127.0.0.1:8000/accounts/login/')
        print('Register: http://127.0.0.1:8000/accounts/register/')
        print('About: http://127.0.0.1:8000/about/')
        print('='*50)

        return username

    except Exception as e:
        print(f'[ERROR] Error creating test user: {e}')
        return None

if __name__ == '__main__':
    create_test_user()
