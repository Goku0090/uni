#!/usr/bin/env python
"""
Test script for the FieldError fix
Run: python manage.py shell < test_fielderror_fix.py
"""

import os
import django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'auth_project.settings')
django.setup()

from accounts.models import Message, MessageReadStatus, ChatRoom
from django.contrib.auth.models import User
from django.db.models import Q

print("\n" + "="*70)
print("Testing FieldError Fix - Django ORM 'ne' Lookup")
print("="*70 + "\n")

user = User.objects.first()

if not user:
    print("❌ No user found in database")
else:
    print(f"Testing for user: {user.username}")
    print("-"*70)
    
    # Test 1: Query without chat_room filter
    print("\n1. Testing basic exclude query...")
    try:
        result = MessageReadStatus.objects.filter(
            user=user
        ).exclude(
            message__sender=user
        ).count()
        print(f"   ✅ Query successful!")
        print(f"   Result: {result} unread messages from others")
    except Exception as e:
        print(f"   ❌ Query failed: {type(e).__name__}: {e}")
    
    # Test 2: Query with chat_room filter
    print("\n2. Testing with chat_room filter...")
    room = ChatRoom.objects.first()
    if room:
        try:
            result = MessageReadStatus.objects.filter(
                message__chat_room=room,
                user=user
            ).exclude(
                message__sender=user
            ).count()
            print(f"   ✅ Query successful!")
            print(f"   Chat room: {room.name}")
            print(f"   Result: {result} unread messages in this room")
        except Exception as e:
            print(f"   ❌ Query failed: {type(e).__name__}: {e}")
    else:
        print("   ⚠️  No chat rooms found to test")
    
    # Test 3: Verify old query would fail
    print("\n3. Verifying old query fails (as expected)...")
    try:
        # This should fail with FieldError
        result = MessageReadStatus.objects.filter(
            user=user,
            message__sender__ne=user  # Invalid lookup!
        ).count()
        print(f"   ⚠️  Old query unexpectedly succeeded (should have failed)")
    except Exception as e:
        if 'ne' in str(e) or 'FieldError' in type(e).__name__:
            print(f"   ✅ Old query correctly fails with: {type(e).__name__}")
            print(f"      Message: {str(e)[:80]}...")
        else:
            print(f"   ❌ Unexpected error: {e}")

print("\n" + "="*70)
print("Test Complete")
print("="*70 + "\n")
