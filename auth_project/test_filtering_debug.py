#!/usr/bin/env python
import os
import sys
import django
from django.test import RequestFactory
from django.contrib.auth.models import User

# Setup Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'auth_project.settings')
django.setup()

from accounts.views import find_collaborators

def test_filtering():
    print("=== Testing Filtering Debug ===")

    # Create a mock request
    factory = RequestFactory()

    # Create a test user if needed
    try:
        user = User.objects.get(username='testuser')
    except User.DoesNotExist:
        user = User.objects.create_user(username='testuser', email='test@example.com', password='testpass')

    # Test with skills filter
    request = factory.get('/accounts/find-collaborators/?skills=python')
    request.user = user

    try:
        response = find_collaborators(request)
        print(f"Response status: {response.status_code}")

        # Check context
        if hasattr(response, 'context_data'):
            context = response.context_data
        else:
            # For render() responses, context is not directly accessible
            print("Cannot access context directly from render() response")
            return

        print(f"Query: {context.get('query', 'None')}")
        print(f"Skills filter: {context.get('skills_filter', 'None')}")
        print(f"Active filters: {context.get('active_filters', 'None')}")
        print(f"Search results count: {len(context.get('search_results', []))}")

        # Print search results
        search_results = context.get('search_results', [])
        for i, profile in enumerate(search_results):
            print(f"  {i+1}. {profile.user.username}: {profile.interests}")

    except Exception as e:
        print(f"Error: {e}")
        import traceback
        traceback.print_exc()

if __name__ == '__main__':
    test_filtering()
