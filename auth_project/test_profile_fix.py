#!/usr/bin/env python
"""Test script to verify user profile API fix"""

import os
import sys
import django

# Fix encoding for Windows
if sys.platform == 'win32':
    import io
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

# Setup Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'auth_project.settings')
django.setup()

from accounts.models import Project, User
from django.db.models import Count

print("=" * 80)
print("Testing User Profile API - Project Fetching Fix")
print("=" * 80)

# Get first user
user = User.objects.first()
if not user:
    print("ERROR: No users found in database")
    exit(1)

print(f"\nOK - User: {user.username} (ID: {user.id})")

# Test the fixed query
try:
    projects = Project.objects.filter(user=user).values(
        'id', 'title', 'description', 'category', 'is_active',
        'created_at', 'updated_at'
    ).annotate(
        likes_count=Count('likes'),
        comments_count=Count('comments'),
        team_members_count=Count('members')
    ).order_by('-created_at')
    
    print(f"OK - Query executed successfully")
    print(f"OK - Projects found: {projects.count()}")
    
    for p in projects:
        print(f"\n  Project: {p['title']}")
        print(f"    - Category: {p['category']}")
        print(f"    - Likes: {p['likes_count']}")
        print(f"    - Comments: {p['comments_count']}")
        print(f"    - Team Members: {p['team_members_count']}")
    
    print("\n" + "=" * 80)
    print("SUCCESS - FIX SUCCESSFUL - API endpoint should work now!")
    print("=" * 80)
    
except Exception as e:
    print(f"\nERROR: {str(e)}")
    import traceback
    traceback.print_exc()
    exit(1)
