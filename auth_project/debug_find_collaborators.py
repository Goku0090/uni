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
from django.test import RequestFactory

# Simulate the find_collaborators view logic
def debug_find_collaborators():
    print("=== Debug Find Collaborators ===\n")

    # Create a mock request (assuming user ID 1 exists)
    try:
        test_user = User.objects.get(id=1)
        print(f"Testing with user: {test_user.username} (ID: {test_user.id})")
    except User.DoesNotExist:
        print("User with ID 1 doesn't exist, using first available user")
        test_user = User.objects.first()
        print(f"Testing with user: {test_user.username} (ID: {test_user.id})")

    # Simulate the view logic
    try:
        user_profile = test_user.student_profile
        user_interests = user_profile.interests.lower().split(",") if user_profile.interests else []
        print(f"User profile found: {user_profile.full_name}")
        print(f"User interests: {user_interests}")
    except StudentProfile.DoesNotExist:
        user_interests = []
        user_profile = None
        print("No user profile found")

    # Search functionality (empty query for suggestions)
    query = ""
    print(f"\nSearch query: '{query}'")

    if query:
        print("Would perform search...")
    else:
        print("No search query, showing suggestions")

    # Suggestions logic
    print("\n=== Suggestions Logic ===")

    # Get all users except current user
    all_users = User.objects.exclude(id=test_user.id)
    print(f"Total other users: {all_users.count()}")

    # Separate users with and without profiles
    users_with_profiles = StudentProfile.objects.exclude(user=test_user).select_related('user')
    users_without_profiles = all_users.exclude(student_profile__isnull=False)

    print(f"Users with profiles: {users_with_profiles.count()}")
    print(f"Users without profiles: {users_without_profiles.count()}")

    # Filter profiles based on interests
    collaborators = []
    if user_interests:
        print(f"Filtering by user interests: {user_interests}")
        query_filter = Q()
        for interest in user_interests:
            interest = interest.strip()
            if interest:
                query_filter |= Q(interests__icontains=interest)

        # Get matching profiles
        matching_profiles = users_with_profiles.filter(query_filter).distinct()
        print(f"Profiles matching interests: {matching_profiles.count()}")

        # Add match scores
        for profile in matching_profiles:
            profile_interests = profile.interests.lower().split(",") if profile.interests else []
            matching_interests = set(user_interests) & set([i.strip() for i in profile_interests])
            profile.match_score = int((len(matching_interests) / len(user_interests)) * 100) if user_interests else 0
            collaborators.append(profile)
            print(f"  - {profile.user.username}: {profile.full_name} (match: {profile.match_score}%)")

        # If we don't have enough suggestions, add some random profiles
        if len(collaborators) < 10:
            remaining_profiles = users_with_profiles.exclude(id__in=[p.id for p in collaborators])[:10-len(collaborators)]
            print(f"Adding {remaining_profiles.count()} random profiles")
            for profile in remaining_profiles:
                profile.match_score = 0  # No match score for random suggestions
                collaborators.append(profile)
    else:
        print("No user interests, showing random profiles")
        # No user interests, show random profiles
        collaborators = list(users_with_profiles[:10])

    # If still not enough, add users without profiles
    if len(collaborators) < 10:
        additional_needed = 10 - len(collaborators)
        print(f"Adding {additional_needed} users without profiles")
        for user in users_without_profiles[:additional_needed]:
            class PseudoProfile:
                def __init__(self, user):
                    self.user = user
                    self.full_name = user.get_full_name() or user.username
                    self.college = "Profile not completed"
                    self.location = ""
                    self.interests = ""
                    self.bio = "This user hasn't completed their profile yet."
                    self.profile_photo = None
                    self.match_score = 0

            collaborators.append(PseudoProfile(user))

    suggestions = collaborators[:10]  # Limit to 10 suggestions

    print(f"\nFinal suggestions count: {len(suggestions)}")
    for i, suggestion in enumerate(suggestions[:5]):  # Show first 5
        print(f"  {i+1}. {suggestion.user.username}: {suggestion.full_name} ({suggestion.college})")

    # Check what would be passed to template
    print("\n=== Template Context ===")
    print(f"query: '{query}'")
    print(f"search_results: [] (empty since no query)")
    print(f"suggestions length: {len(suggestions)}")
    print(f"user_interests: {user_interests}")

    return len(suggestions) > 0

if __name__ == "__main__":
    has_suggestions = debug_find_collaborators()
    print(f"\nResult: {'Suggestions will be shown' if has_suggestions else 'No suggestions will be shown'}")
