"""
Test script to verify Connection System works
Run: python test_connections.py
"""

import os
import sys
import django

# Fix Windows encoding
sys.stdout.reconfigure(encoding='utf-8')

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'auth_project.settings')
django.setup()

from django.contrib.auth.models import User
from accounts.models import StudentProfile, Connection

print("=" * 60)
print("TESTING CONNECTION SYSTEM")
print("=" * 60)

# Test 1: Check if Connection model exists
try:
    connection_count = Connection.objects.count()
    print(f"\n✅ Test 1 PASSED: Connection model exists")
    print(f"   Current connections in database: {connection_count}")
except Exception as e:
    print(f"\n❌ Test 1 FAILED: {e}")

# Test 2: Check if we can create a connection
try:
    # Get or create test users
    user1, _ = User.objects.get_or_create(
        username='testuser1',
        defaults={'email': 'test1@example.com'}
    )
    user2, _ = User.objects.get_or_create(
        username='testuser2',
        defaults={'email': 'test2@example.com'}
    )
    
    # Create profiles if they don't exist
    StudentProfile.objects.get_or_create(
        user=user1,
        defaults={'full_name': 'Test User 1', 'college': 'Test College'}
    )
    StudentProfile.objects.get_or_create(
        user=user2,
        defaults={'full_name': 'Test User 2', 'college': 'Test College'}
    )
    
    # Try to create a connection
    connection, created = Connection.objects.get_or_create(
        sender=user1,
        receiver=user2,
        defaults={'status': 'pending'}
    )
    
    if created:
        print(f"\n✅ Test 2 PASSED: Created test connection")
    else:
        print(f"\n✅ Test 2 PASSED: Connection already exists")
    
    print(f"   Status: {connection.status}")
    print(f"   From: {connection.sender.username}")
    print(f"   To: {connection.receiver.username}")
    
except Exception as e:
    print(f"\n❌ Test 2 FAILED: {e}")

# Test 3: Check if we can query connections
try:
    sent_connections = Connection.objects.filter(sender=user1).count()
    received_connections = Connection.objects.filter(receiver=user2).count()
    pending = Connection.objects.filter(status='pending').count()
    accepted = Connection.objects.filter(status='accepted').count()
    
    print(f"\n✅ Test 3 PASSED: Can query connections")
    print(f"   Sent by {user1.username}: {sent_connections}")
    print(f"   Received by {user2.username}: {received_connections}")
    print(f"   Total pending: {pending}")
    print(f"   Total accepted: {accepted}")
    
except Exception as e:
    print(f"\n❌ Test 3 FAILED: {e}")

# Test 4: Check if views can be imported
try:
    from accounts.views import (
        send_connection_request,
        accept_connection,
        reject_connection,
        my_connections
    )
    print(f"\n✅ Test 4 PASSED: All connection views imported successfully")
except Exception as e:
    print(f"\n❌ Test 4 FAILED: {e}")

# Test 5: Check if templates exist
import os
from django.conf import settings

try:
    template_dir = os.path.join(settings.BASE_DIR, 'accounts', 'templates')
    templates_to_check = [
        'find_collaborators.html',
        'my_connections.html'
    ]
    
    all_exist = True
    for template in templates_to_check:
        path = os.path.join(template_dir, template)
        if not os.path.exists(path):
            print(f"   Missing: {template}")
            all_exist = False
    
    if all_exist:
        print(f"\n✅ Test 5 PASSED: All templates exist")
    else:
        print(f"\n⚠️  Test 5 WARNING: Some templates missing")
        
except Exception as e:
    print(f"\n❌ Test 5 FAILED: {e}")

print("\n" + "=" * 60)
print("TESTING COMPLETE")
print("=" * 60)
print("\n💡 To test in browser:")
print("   1. Run: python manage.py runserver")
print("   2. Create two user accounts")
print("   3. Go to Find Collaborators")
print("   4. Click 'Connect' on a user")
print("   5. Login to other account")
print("   6. Go to My Connections")
print("   7. Accept the connection request")
print("\n")
