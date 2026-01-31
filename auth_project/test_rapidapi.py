#!/usr/bin/env python
"""
Test script for RapidAPI university integration
"""
import os
import sys
import django

# Setup Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'auth_project.settings')
django.setup()

from accounts.college_utils import CollegeManager

def test_rapidapi():
    """Test the RapidAPI integration"""
    print("Testing RapidAPI University Integration")
    print("=" * 50)

    # Test 1: Get colleges
    print("\nTest 1: Fetching universities from RapidAPI...")
    try:
        colleges = CollegeManager.get_colleges(use_cache=False)
        print(f"Found {len(colleges)} universities")
        if colleges:
            print("First 10 universities:")
            for i, college in enumerate(colleges[:10], 1):
                print(f"   {i}. {college}")
        else:
            print("No universities found")
    except Exception as e:
        print(f"Error fetching universities: {e}")

    # Test 2: Search colleges
    print("\nTest 2: Testing college search...")
    try:
        results = CollegeManager.search_colleges("harvard", max_results=5)
        print(f"Search for 'harvard': {len(results)} results")
        for result in results:
            print(f"   • {result}")
    except Exception as e:
        print(f"Error searching colleges: {e}")

    # Test 3: Validate college
    print("\nTest 3: Testing college validation...")
    try:
        is_valid = CollegeManager.validate_college("Harvard University")
        print(f"Harvard University validation: {'Valid' if is_valid else 'Invalid'}")
    except Exception as e:
        print(f"Error validating college: {e}")

    print("\nRapidAPI integration test completed!")

if __name__ == "__main__":
    test_rapidapi()
