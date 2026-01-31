#!/usr/bin/env python
import os
import django
import sys

# Setup Django
sys.path.append('.')
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'auth_project.settings')
django.setup()

from accounts.models import StudentProfile, User
from django.db.models import Q

print("=== Testing Find Collaborators Search ===")

# Test search for user
query = "Goku"
print(f"Testing search for existing user: '{query}'")
print(f"\nSearching for: '{query}'")

# Test the new logic from the view
# First try to find users with profiles matching the criteria
users_with_matching_profiles = User.objects.filter(
    Q(student_profile__full_name__icontains=query) |
    Q(student_profile__college__icontains=query) |
    Q(student_profile__location__icontains=query) |
    Q(student_profile__interests__icontains=query)
).select_related('student_profile')

# Then find users by their basic user fields (username, name, email)
users_by_basic_fields = User.objects.filter(
    Q(username__icontains=query) |
    Q(first_name__icontains=query) |
    Q(last_name__icontains=query) |
    Q(email__icontains=query)
)

# Combine and deduplicate
all_matching_users = list(users_with_matching_profiles) + list(users_by_basic_fields)
unique_users = []
seen_ids = set()
for user in all_matching_users:
    if user.id not in seen_ids:
        unique_users.append(user)
        seen_ids.add(user.id)

# Limit results and create search results
unique_users = unique_users[:20]

print(f"Total matching users: {len(unique_users)}")
for user in unique_users[:5]:  # Show first 5
    has_profile = hasattr(user, 'student_profile') and user.student_profile
    if has_profile:
        print(f"  - User with profile: {user.username} -> {user.student_profile.full_name}")
    else:
        print(f"  - User without profile: {user.username} -> {user.get_full_name() or 'No name'}")

# Test search for non-existing user
print(f"\nTesting search for non-existing user: 'nonexistent'")
query2 = "nonexistent"
users_with_matching_profiles2 = User.objects.filter(
    Q(student_profile__full_name__icontains=query2) |
    Q(student_profile__college__icontains=query2) |
    Q(student_profile__location__icontains=query2) |
    Q(student_profile__interests__icontains=query2)
).select_related('student_profile')

users_by_basic_fields2 = User.objects.filter(
    Q(username__icontains=query2) |
    Q(first_name__icontains=query2) |
    Q(last_name__icontains=query2) |
    Q(email__icontains=query2)
)

all_matching_users2 = list(users_with_matching_profiles2) + list(users_by_basic_fields2)
unique_users2 = []
seen_ids2 = set()
for user in all_matching_users2:
    if user.id not in seen_ids2:
        unique_users2.append(user)
        seen_ids2.add(user.id)

unique_users2 = unique_users2[:20]
print(f"Total matching users for 'nonexistent': {len(unique_users2)}")

# Test suggestions
print("\n=== Testing Suggestions ===")
all_users = User.objects.all()
users_with_profiles = StudentProfile.objects.select_related('user')

print(f"Total users: {all_users.count()}")
print(f"Users with profiles: {users_with_profiles.count()}")

# Test a few suggestions
suggestions = list(users_with_profiles[:3])
print(f"Sample suggestions: {len(suggestions)}")
for suggestion in suggestions:
    print(f"  - {suggestion.user.username}: {suggestion.full_name}")
