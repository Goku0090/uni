"""
Test script to verify projects now show in feed
Run with: python manage.py shell < test_feed_fix.py
"""

from django.contrib.auth.models import User
from accounts.models import Project, StudentProfile
from accounts.utils import ProjectVisibilityFilter
from django.utils import timezone

print("=" * 70)
print("Testing Project Feed Visibility After Fix")
print("=" * 70)

# Get or create test user
user, created = User.objects.get_or_create(
    username='feedtestuser',
    defaults={
        'email': 'feedtest@example.com',
        'first_name': 'Feed',
        'last_name': 'Tester'
    }
)
print(f"\n1. Test User: {user.username} (email: {user.email})")
print(f"   {'Created' if created else 'Already exists'}")

# Get or create profile
try:
    profile = user.student_profile
    print(f"\n2. StudentProfile exists: Yes")
    print(f"   Name: {profile.full_name}")
    print(f"   College: {profile.college}")
    print(f"   Skills: {profile.skills}")
    print(f"   Interests: {profile.interests}")
except StudentProfile.DoesNotExist:
    # Create a profile
    profile, _ = StudentProfile.objects.get_or_create(
        user=user,
        defaults={
            'full_name': 'Feed Tester',
            'college': 'MIT',
            'skills': ['Python', 'Django', 'React'],
            'interests': ['AI', 'Web Development', 'Data Science'],
            'profile_completed': True
        }
    )
    print(f"\n2. StudentProfile created")
    print(f"   Name: {profile.full_name}")
    print(f"   College: {profile.college}")
    print(f"   Skills: {profile.skills}")
    print(f"   Interests: {profile.interests}")

# Get all projects from database
all_projects = Project.objects.all().order_by('-created_at')
print(f"\n3. Total Projects in Database: {all_projects.count()}")

if all_projects.count() == 0:
    print("   ⚠️  WARNING: No projects found in database!")
    print("   Create some test projects first.")
else:
    # Show first 3 projects in database
    print("   Sample projects:")
    for i, p in enumerate(all_projects[:3], 1):
        print(f"     {i}. '{p.title}' by {p.user.username} (created: {p.created_at.strftime('%Y-%m-%d')})")

# Test the visibility filter
print(f"\n4. Testing ProjectVisibilityFilter.get_visible_projects()...")
try:
    visible_projects, match_details = ProjectVisibilityFilter.get_visible_projects(user)
    print(f"   ✅ Filter executed successfully")
    print(f"   Result: {len(visible_projects)} projects visible")
except Exception as e:
    print(f"   ❌ ERROR in filter: {type(e).__name__}: {str(e)}")
    import traceback
    traceback.print_exc()
    visible_projects = []
    match_details = {}

# Analyze results
if visible_projects:
    print(f"\n5. Project Visibility Analysis:")
    
    # Count by match score
    perfect = sum(1 for p in visible_projects if match_details[p.id]['score'] >= 80)
    good = sum(1 for p in visible_projects if 60 <= match_details[p.id]['score'] < 80)
    some = sum(1 for p in visible_projects if 20 < match_details[p.id]['score'] < 60)
    explore = sum(1 for p in visible_projects if match_details[p.id]['score'] == 0)
    own = sum(1 for p in visible_projects if match_details[p.id]['score'] == 100)
    
    print(f"   ✨ Perfect Match (80-100):    {perfect} projects")
    print(f"   👍 Good Match (60-79):        {good} projects")
    print(f"   👀 Some Match (21-59):        {some} projects")
    print(f"   🔍 Explore (0 match):         {explore} projects")
    print(f"   🏆 Your Projects (100):       {own} projects")

    # Show top 5 projects
    print(f"\n6. Top 5 Projects by Relevance:")
    for i, project in enumerate(visible_projects[:5], 1):
        match_info = match_details[project.id]
        score = match_info['score']
        reasons = match_info['reasons']
        
        # Emoji based on score
        if score == 100:
            emoji = "🏆"
        elif score >= 80:
            emoji = "⭐"
        elif score >= 60:
            emoji = "👍"
        elif score >= 20:
            emoji = "👀"
        else:
            emoji = "🔍"
        
        print(f"\n   {i}. {emoji} {project.title}")
        print(f"      Owner: {project.user.username}")
        print(f"      Score: {score}/100")
        print(f"      Reasons: {', '.join(reasons)}")
        print(f"      Created: {project.created_at.strftime('%Y-%m-%d %H:%M')}")

    # Final verdict
    print(f"\n" + "=" * 70)
    if len(visible_projects) == all_projects.count():
        print("✅ SUCCESS: All projects are now showing in the feed!")
        print("   The filter includes projects with all match scores.")
    elif len(visible_projects) > 0:
        print(f"⚠️  PARTIAL: {len(visible_projects)}/{all_projects.count()} projects visible")
        print("   Some projects might be filtered out. Check match scores.")
    else:
        print("❌ FAILED: No projects visible! Filter is still too restrictive.")
    print("=" * 70)

else:
    print(f"\n❌ ERROR: No projects returned from filter!")
    print("   This suggests the filter is broken or database is empty.")

# Check if filter correctly prioritizes user's own projects
user_projects = [p for p in visible_projects if p.user == user]
if user_projects:
    print(f"\n7. User's Own Projects: {len(user_projects)} found")
    for p in user_projects[:3]:
        print(f"   - {p.title}")
    # Check if they're at the top
    top_5_has_user_projects = any(p.user == user for p in visible_projects[:5])
    if top_5_has_user_projects:
        print(f"   ✅ User's projects are prioritized (in top 5)")
    else:
        print(f"   ⚠️  User's projects are not in top 5")

print(f"\n" + "=" * 70)
print("Test Complete!")
print("=" * 70)
