#!/usr/bin/env python
"""
Diagnostic tool to check what's wrong with project detail view
Run: python manage.py shell < DIAGNOSE_ISSUE.py
"""

import os
import sys
import django
from django.conf import settings

# Setup Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'auth_project.settings')
django.setup()

from django.test import Client
from django.db import connection
from django.test.utils import CaptureQueriesContext
from accounts.models import Project, User

print("=" * 80)
print("DIAGNOSTIC CHECK FOR PROJECT DETAIL VIEW")
print("=" * 80)

# Check 1: Database Connection
print("\n1. DATABASE CONNECTION:")
try:
    from django.db import connections
    for alias in connections:
        try:
            connections[alias].ensure_connection()
            print(f"   ✓ {alias} connection OK")
        except Exception as e:
            print(f"   ✗ {alias} connection FAILED: {e}")
except Exception as e:
    print(f"   ✗ Error checking connections: {e}")

# Check 2: Project exists
print("\n2. PROJECT DATA:")
try:
    project_count = Project.objects.count()
    print(f"   ✓ Total projects: {project_count}")
    
    if project_count > 0:
        first_project = Project.objects.first()
        print(f"   ✓ First project ID: {first_project.id}")
        print(f"   ✓ Project owner: {first_project.user.username}")
    else:
        print("   ⚠ No projects found!")
except Exception as e:
    print(f"   ✗ Error: {e}")

# Check 3: User exists
print("\n3. USER DATA:")
try:
    user_count = User.objects.count()
    print(f"   ✓ Total users: {user_count}")
    
    if user_count > 0:
        first_user = User.objects.first()
        print(f"   ✓ First user: {first_user.username}")
except Exception as e:
    print(f"   ✗ Error: {e}")

# Check 4: View imports
print("\n4. VIEW IMPORTS:")
try:
    from accounts.views import project_detail
    print(f"   ✓ project_detail view imported successfully")
except Exception as e:
    print(f"   ✗ Failed to import project_detail: {e}")
    import traceback
    traceback.print_exc()

# Check 5: Test the view with query capture
print("\n5. VIEW EXECUTION TEST:")
try:
    if Project.objects.count() > 0:
        client = Client()
        project_id = Project.objects.first().id
        
        print(f"   Testing with project_id={project_id}")
        
        with CaptureQueriesContext(connection) as context:
            response = client.get(f'/accounts/project-detail/{project_id}/')
        
        print(f"   Response status: {response.status_code}")
        print(f"   Number of queries: {len(context)}")
        
        if response.status_code == 200:
            print(f"   ✓ View executed successfully")
        elif response.status_code == 404:
            print(f"   ⚠ View returned 404 - URL may be wrong")
        elif response.status_code == 500:
            print(f"   ✗ View returned 500 - Internal server error")
            print(f"   Check error logs for details")
        else:
            print(f"   ⚠ Unexpected status code: {response.status_code}")
        
        # Print first few queries
        print(f"\n   First 3 queries:")
        for i, query in enumerate(context[:3]):
            print(f"     Query {i+1}: {query['sql'][:100]}...")
    else:
        print("   ⚠ No projects to test with")
except Exception as e:
    print(f"   ✗ Error testing view: {e}")
    import traceback
    traceback.print_exc()

# Check 6: Template
print("\n6. TEMPLATE CHECK:")
try:
    from django.template.loader import get_template
    template = get_template('project_detail.html')
    print(f"   ✓ project_detail.html template found")
except Exception as e:
    print(f"   ✗ Template not found: {e}")

# Check 7: Model relationships
print("\n7. MODEL RELATIONSHIPS:")
try:
    from accounts.models import Project, Comment, ProjectTeam
    
    project = Project.objects.first()
    if project:
        print(f"   ✓ Project object accessible")
        print(f"     - Has user: {hasattr(project, 'user')}")
        print(f"     - Has comments: {hasattr(project, 'comments')}")
        print(f"     - Has team: {hasattr(project, 'team')}")
        print(f"     - Has tasks: {hasattr(project, 'tasks')}")
        print(f"     - Has milestones: {hasattr(project, 'milestones')}")
except Exception as e:
    print(f"   ✗ Error: {e}")

print("\n" + "=" * 80)
print("DIAGNOSTIC COMPLETE")
print("=" * 80)
