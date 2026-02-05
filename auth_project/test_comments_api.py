#!/usr/bin/env python
"""
Test script to verify comment API is working correctly
Run: python test_comments_api.py
"""

import os
import sys
import django

# Setup Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'auth_project.settings')
sys.path.insert(0, os.path.dirname(__file__))
django.setup()

from django.urls import resolve, reverse
from django.contrib.auth.models import User
from accounts.models import Project, Comment, StudentProfile
from django.test import Client
import json

print("=" * 80)
print("COMMENT API TEST SCRIPT")
print("=" * 80)

# Test 1: Check URL routing
print("\n[TEST 1] URL Routing Check")
print("-" * 80)

try:
    # Check if the route exists
    match = resolve('/api/projects/1/comments/')
    print(f"✅ GET /api/projects/1/comments/ → {match.func.__name__}")
except Exception as e:
    print(f"❌ GET /api/projects/1/comments/ → ERROR: {e}")

try:
    match = resolve('/api/projects/1/comments/add/')
    print(f"✅ POST /api/projects/1/comments/add/ → {match.func.__name__}")
except Exception as e:
    print(f"❌ POST /api/projects/1/comments/add/ → ERROR: {e}")

try:
    match = resolve('/api/comments/1/delete/')
    print(f"✅ DELETE /api/comments/1/delete/ → {match.func.__name__}")
except Exception as e:
    print(f"❌ DELETE /api/comments/1/delete/ → ERROR: {e}")

try:
    match = resolve('/api/comments/1/edit/')
    print(f"✅ PUT /api/comments/1/edit/ → {match.func.__name__}")
except Exception as e:
    print(f"❌ PUT /api/comments/1/edit/ → ERROR: {e}")

# Test 2: Database Check
print("\n[TEST 2] Database Check")
print("-" * 80)

user_count = User.objects.count()
project_count = Project.objects.count()
comment_count = Comment.objects.count()

print(f"Users in database: {user_count}")
print(f"Projects in database: {project_count}")
print(f"Comments in database: {comment_count}")

if user_count == 0:
    print("⚠️  No users in database. Create a test user first.")
if project_count == 0:
    print("⚠️  No projects in database. Create a test project first.")

# Test 3: Create test data
print("\n[TEST 3] Create Test Data")
print("-" * 80)

# Create test user if doesn't exist
user, created = User.objects.get_or_create(username='testuser', defaults={
    'email': 'test@example.com'
})
if created:
    user.set_password('testpass123')
    user.save()
    print(f"✅ Created test user: testuser")
else:
    print(f"✅ Test user already exists: testuser")

# Create StudentProfile if doesn't exist
profile, created = StudentProfile.objects.get_or_create(user=user, defaults={
    'full_name': 'Test User',
    'college': 'Test College'
})
if created:
    print(f"✅ Created StudentProfile for testuser")
else:
    print(f"✅ StudentProfile already exists for testuser")

# Create test project if doesn't exist
project, created = Project.objects.get_or_create(
    title='Test Project for Comments',
    defaults={
        'user': user,
        'description': 'A test project to test the comments API',
        'category': 'Testing',
        'visibility': 'public'
    }
)
if created:
    print(f"✅ Created test project: {project.id}")
else:
    print(f"✅ Test project already exists: {project.id}")

# Test 4: API Endpoint Test
print("\n[TEST 4] API Endpoint Test")
print("-" * 80)

client = Client()

# Test GET comments
print(f"\nGET /api/projects/{project.id}/comments/")
response = client.get(f'/api/projects/{project.id}/comments/')
if response.status_code == 200:
    data = response.json()
    print(f"✅ Status: {response.status_code}")
    print(f"   Success: {data.get('success')}")
    print(f"   Comment count: {data.get('count')}")
    print(f"   Comments: {data.get('comments', [])}")
elif response.status_code == 302:
    print(f"⚠️  Status: {response.status_code} (Redirected - probably need to login)")
elif response.status_code == 404:
    print(f"❌ Status: 404 - Endpoint not found!")
    print(f"   Check URL routing. Route might be: /accounts/api/projects/{project.id}/comments/")
else:
    print(f"❌ Status: {response.status_code}")
    print(f"   Response: {response.content.decode()}")

# Test 5: Authenticated API Test
print("\n[TEST 5] Authenticated API Test")
print("-" * 80)

# Login
logged_in = client.login(username='testuser', password='testpass123')
if logged_in:
    print(f"✅ Logged in as: testuser")
else:
    print(f"❌ Failed to login")

# Try GET again with authentication
print(f"\nGET /api/projects/{project.id}/comments/ (authenticated)")
response = client.get(f'/api/projects/{project.id}/comments/')
if response.status_code == 200:
    data = response.json()
    print(f"✅ Status: {response.status_code}")
    print(f"   Response: {json.dumps(data, indent=2)}")
else:
    print(f"❌ Status: {response.status_code}")
    print(f"   Response: {response.content.decode()}")

# Test 6: Create Comment
print("\n[TEST 6] Create Comment Test")
print("-" * 80)

# Get CSRF token
from django.middleware.csrf import get_token
csrf_token = get_token(client)

# Post a comment
print(f"\nPOST /api/projects/{project.id}/comments/add/")
response = client.post(
    f'/api/projects/{project.id}/comments/add/',
    data=json.dumps({'content': 'Test comment'}),
    content_type='application/json',
    HTTP_X_CSRFTOKEN=csrf_token
)

if response.status_code == 200:
    data = response.json()
    print(f"✅ Status: {response.status_code}")
    print(f"   Response: {json.dumps(data, indent=2)}")
    if data.get('success'):
        print(f"✅ Comment created successfully!")
        comment_id = data.get('comment', {}).get('id')
        print(f"   Comment ID: {comment_id}")
else:
    print(f"❌ Status: {response.status_code}")
    print(f"   Response: {response.content.decode()}")

# Test 7: Get Comments Again
print("\n[TEST 7] Verify Comment Was Saved")
print("-" * 80)

response = client.get(f'/api/projects/{project.id}/comments/')
if response.status_code == 200:
    data = response.json()
    count = data.get('count', 0)
    print(f"✅ Comment count: {count}")
    if count > 0:
        print(f"✅ Comments are being returned from API!")
        print(f"   First comment: {data.get('comments', [])[0]}")
    else:
        print(f"⚠️  No comments returned (might be okay if just created)")
else:
    print(f"❌ Status: {response.status_code}")

# Summary
print("\n" + "=" * 80)
print("SUMMARY")
print("=" * 80)

print(f"""
✅ If all tests above are GREEN, comments API is working correctly!

If you see errors:

1. "Endpoint not found" (404) 
   → The URL routing is wrong. Check accounts/urls.py line 125-128
   → Make sure it says: path('projects/<int:project_id>/comments/', ...)
   → NOT: path('api/projects/<int:project_id>/comments/', ...)

2. "Redirected" (302)
   → You need to be logged in to use the API

3. "Internal Server Error" (500)
   → Check Django logs: tail -f logs/django.log
   → Or check the error message above

4. "No comments returned"
   → Database might not have the project yet
   → Or comments aren't being created (check POST test above)

For more debugging, see: DEBUG_ERROR_LOADING_COMMENTS.md
""")
