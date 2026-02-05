#!/usr/bin/env python
"""
Fix script to create test StudentProfiles for testing Find Collaborators feature.
Run: python fix_no_collaborators.py
"""

import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'auth_project.settings')
django.setup()

from django.contrib.auth.models import User
from accounts.models import StudentProfile

# Test data - users with complete profiles
TEST_USERS = [
    {
        'username': 'alice',
        'email': 'alice@college.com',
        'password': 'testpass123',
        'first_name': 'Alice',
        'last_name': 'Johnson',
        'profile': {
            'full_name': 'Alice Johnson',
            'college': 'MIT',
            'location': 'Boston, MA',
            'bio': 'Passionate about web development and open source projects',
            'skills': ['Python', 'React', 'Django', 'PostgreSQL', 'JavaScript'],
            'interests': ['Web Development', 'Open Source', 'Startups'],
            'role_preference': 'Full Stack Developer'
        }
    },
    {
        'username': 'bob',
        'email': 'bob@college.com',
        'password': 'testpass123',
        'first_name': 'Bob',
        'last_name': 'Smith',
        'profile': {
            'full_name': 'Bob Smith',
            'college': 'Stanford',
            'location': 'San Francisco, CA',
            'bio': 'AI/ML enthusiast and data scientist exploring neural networks',
            'skills': ['Python', 'TensorFlow', 'PyTorch', 'Data Science', 'SQL'],
            'interests': ['AI', 'Machine Learning', 'Deep Learning', 'Research'],
            'role_preference': 'ML Engineer'
        }
    },
    {
        'username': 'carol',
        'email': 'carol@college.com',
        'password': 'testpass123',
        'first_name': 'Carol',
        'last_name': 'White',
        'profile': {
            'full_name': 'Carol White',
            'college': 'UC Berkeley',
            'location': 'San Francisco, CA',
            'bio': 'Full-stack developer with strong UI/UX design skills',
            'skills': ['JavaScript', 'React', 'Node.js', 'CSS', 'Figma', 'UI Design'],
            'interests': ['Web Design', 'UX/UI', 'Frontend Development', 'Animation'],
            'role_preference': 'Full Stack Developer'
        }
    },
    {
        'username': 'david',
        'email': 'david@college.com',
        'password': 'testpass123',
        'first_name': 'David',
        'last_name': 'Lee',
        'profile': {
            'full_name': 'David Lee',
            'college': 'IIT Delhi',
            'location': 'New Delhi, India',
            'bio': 'Mobile app developer and tech entrepreneur building innovative solutions',
            'skills': ['Flutter', 'Swift', 'Java', 'Firebase', 'Mobile Development'],
            'interests': ['Mobile Apps', 'Startups', 'IoT', 'DevOps'],
            'role_preference': 'Mobile Developer'
        }
    },
    {
        'username': 'emma',
        'email': 'emma@college.com',
        'password': 'testpass123',
        'first_name': 'Emma',
        'last_name': 'Davis',
        'profile': {
            'full_name': 'Emma Davis',
            'college': 'Harvard',
            'location': 'Boston, MA',
            'bio': 'Cloud infrastructure expert passionate about DevOps and scalability',
            'skills': ['AWS', 'Docker', 'Kubernetes', 'Python', 'Infrastructure as Code'],
            'interests': ['Cloud Computing', 'DevOps', 'System Design', 'Performance'],
            'role_preference': 'DevOps Engineer'
        }
    },
    {
        'username': 'frank',
        'email': 'frank@college.com',
        'password': 'testpass123',
        'first_name': 'Frank',
        'last_name': 'Brown',
        'profile': {
            'full_name': 'Frank Brown',
            'college': 'Carnegie Mellon',
            'location': 'Pittsburgh, PA',
            'bio': 'Cybersecurity specialist and ethical hacker protecting digital assets',
            'skills': ['Cybersecurity', 'Penetration Testing', 'C++', 'Network Security'],
            'interests': ['Security', 'Hacking', 'Privacy', 'Blockchain'],
            'role_preference': 'Security Engineer'
        }
    }
]

def main():
    print("=" * 70)
    print("Creating Test StudentProfiles for Find Collaborators Testing")
    print("=" * 70)
    
    created_count = 0
    already_exist_count = 0
    
    for user_data in TEST_USERS:
        username = user_data['username']
        email = user_data['email']
        password = user_data['password']
        profile_data = user_data['profile']
        
        # Create or get user
        user, user_created = User.objects.get_or_create(
            username=username,
            defaults={
                'email': email,
                'first_name': user_data['first_name'],
                'last_name': user_data['last_name'],
            }
        )
        
        if user_created:
            user.set_password(password)
            user.save()
        
        # Create or get profile
        profile, profile_created = StudentProfile.objects.get_or_create(
            user=user,
            defaults=profile_data
        )
        
        if profile_created:
            print(f"\n✅ Created new profile:")
            print(f"   Username: {username}")
            print(f"   Name: {profile.full_name}")
            print(f"   College: {profile.college}")
            print(f"   Skills: {', '.join(profile.skills)}")
            created_count += 1
        else:
            print(f"\nℹ️  Profile already exists: {username}")
            already_exist_count += 1
    
    # Print summary
    print("\n" + "=" * 70)
    print("SUMMARY")
    print("=" * 70)
    print(f"✅ New profiles created: {created_count}")
    print(f"ℹ️  Already existing: {already_exist_count}")
    print(f"📊 Total profiles in database: {StudentProfile.objects.count()}")
    
    # Print test credentials
    print("\n" + "=" * 70)
    print("TEST CREDENTIALS")
    print("=" * 70)
    print("Use any of these to login and test:\n")
    for user_data in TEST_USERS:
        print(f"  👤 Username: {user_data['username']}")
        print(f"     Password: {user_data['password']}")
        print(f"     College: {user_data['profile']['college']}\n")
    
    # Instructions
    print("=" * 70)
    print("NEXT STEPS")
    print("=" * 70)
    print("1. Start the server: python manage.py runserver")
    print("2. Visit: http://127.0.0.1:8000/accounts/login/")
    print("3. Login with any test user (e.g., alice/testpass123)")
    print("4. Go to: http://127.0.0.1:8000/find-collaborators/")
    print("5. You should see collaborator cards displayed!")
    print("=" * 70)

if __name__ == '__main__':
    try:
        main()
        print("\n✨ Done! Your test data is ready.")
    except Exception as e:
        print(f"\n❌ Error: {e}")
        import traceback
        traceback.print_exc()
