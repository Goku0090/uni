"""
Test script to verify user profile viewing works correctly
Run with: python manage.py shell < test_profile_view.py
"""

from django.contrib.auth.models import User
from accounts.models import StudentProfile, UserStats, Activity, Follow, Connection, Project
from django.db.models import Q
from django.utils import timezone

# Create test users if they don't exist
print("=" * 60)
print("Testing User Profile Viewing")
print("=" * 60)

# Check if users exist
user1, created1 = User.objects.get_or_create(
    username='testuser1',
    defaults={'email': 'test1@example.com', 'first_name': 'Test', 'last_name': 'User1'}
)
print(f"\n1. User 1 (testuser1): {'Created' if created1 else 'Already exists'}")
print(f"   ID: {user1.id}, Email: {user1.email}")

# Create StudentProfile for user1
profile1, created_prof1 = StudentProfile.objects.get_or_create(
    user=user1,
    defaults={
        'full_name': 'Test User One',
        'college': 'MIT',
        'location': 'Boston',
        'bio': 'Test bio for user 1',
        'profile_completed': True
    }
)
print(f"\n2. StudentProfile for User 1: {'Created' if created_prof1 else 'Already exists'}")
print(f"   Name: {profile1.full_name}, College: {profile1.college}")

# Check user stats
user_stats, created_stats = UserStats.objects.get_or_create(
    user=user1,
    defaults={
        'projects_created': 0,
        'connections_made': 0,
        'likes_received': 0,
        'followers_count': 0,
        'following_count': 0
    }
)
print(f"\n3. UserStats for User 1: {'Created' if created_stats else 'Already exists'}")
print(f"   Stats: {user_stats.projects_created} projects, {user_stats.connections_made} connections")

# Check projects
projects = Project.objects.filter(user=user1)
print(f"\n4. Projects for User 1: {projects.count()} projects found")
for p in projects[:3]:
    print(f"   - {p.title} (visibility: {p.visibility})")

# Check activities
activities = Activity.objects.filter(user=user1, is_public=True)
print(f"\n5. Public Activities for User 1: {activities.count()} activities")
for a in activities[:3]:
    print(f"   - {a.activity_type}: {a.title}")

# Check connections
connections = Connection.objects.filter(
    Q(sender=user1, status='accepted') | Q(receiver=user1, status='accepted')
)
print(f"\n6. Accepted Connections for User 1: {connections.count()}")

# Check followers
followers = Follow.objects.filter(following=user1)
print(f"\n7. Followers for User 1: {followers.count()}")

# Simulate profile viewing
print("\n" + "=" * 60)
print("Simulating Profile View Access")
print("=" * 60)

profile_user = user1
try:
    # Get user stats
    user_stats, created = UserStats.objects.get_or_create(user=profile_user, defaults={})
    if created or (timezone.now() - user_stats.last_updated).seconds > 300:
        user_stats.update_stats()
    print("\n✓ UserStats retrieved/updated successfully")

    # Get activities
    activities = Activity.objects.filter(
        user=profile_user,
        is_public=True
    ).select_related(
        'user', 'project', 'target_user', 'connection'
    ).order_by('-created_at')[:20]
    print(f"✓ Activities retrieved: {activities.count()} items")

    # Get projects
    projects = Project.objects.filter(
        user=profile_user,
        visibility__in=['public', 'shared']
    ).order_by('-created_at')[:6]
    print(f"✓ Projects retrieved: {projects.count()} items")

    # Get connections
    connections_count = Connection.objects.filter(
        Q(sender=profile_user, status='accepted') | Q(receiver=profile_user, status='accepted')
    ).count()
    print(f"✓ Connections count: {connections_count}")

    # Get student profile
    student_profile = profile_user.student_profile
    print(f"✓ StudentProfile retrieved: {student_profile.full_name}")

    print("\n" + "=" * 60)
    print("✓ ALL TESTS PASSED - Profile view should work!")
    print("=" * 60)

except StudentProfile.DoesNotExist:
    print("\n✗ ERROR: StudentProfile not found for user")
except Exception as e:
    print(f"\n✗ ERROR: {type(e).__name__}: {str(e)}")
    import traceback
    traceback.print_exc()
