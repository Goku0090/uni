#!/usr/bin/env python
"""
Debug script to check what conversations are being passed to the template
Run: python manage.py shell < debug_conversations.py
"""

import os
import django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'auth_project.settings')
django.setup()

from django.contrib.auth.models import User
from accounts.models import Message, MessageReadStatus, ChatRoom

# Get the first user (or change to a specific user)
user = User.objects.first()

if not user:
    print("No users found in database")
else:
    print(f"\n{'='*60}")
    print(f"Checking conversations for user: {user.username}")
    print(f"{'='*60}\n")
    
    # Check direct message conversations
    print("DIRECT CONVERSATIONS:")
    print("-" * 60)
    
    # Get all users who have messaged this user
    conversation_users = User.objects.filter(
        sent_messages__receiver=user
    ).distinct()
    
    print(f"Total users who messaged {user.username}: {conversation_users.count()}")
    
    for i, conv_user in enumerate(conversation_users, 1):
        last_message = Message.objects.filter(
            Q(sender=user, receiver=conv_user) |
            Q(sender=conv_user, receiver=user)
        ).order_by('-created_at').first()
        
        unread_count = Message.objects.filter(
            sender=conv_user,
            receiver=user
        ).exclude(
            id__in=MessageReadStatus.objects.filter(
                user=user
            ).values_list('message_id', flat=True)
        ).count()
        
        print(f"\n{i}. {conv_user.username}")
        print(f"   Last message: {last_message.content[:50] if last_message else 'None'}")
        print(f"   Unread: {unread_count}")
        print(f"   Type: direct")
    
    # Check group chat conversations
    print(f"\n\nGROUP CHAT CONVERSATIONS:")
    print("-" * 60)
    
    group_chat_rooms = ChatRoom.objects.filter(
        members__user=user,
        members__is_active=True,
        is_active=True,
        chat_type='group'
    ).distinct()
    
    print(f"Total group chats for {user.username}: {group_chat_rooms.count()}")
    
    for i, room in enumerate(group_chat_rooms, 1):
        last_message = room.messages.order_by('-created_at').first()
        unread_count = room.messages.exclude(
            id__in=MessageReadStatus.objects.filter(
                user=user
            ).values_list('message_id', flat=True)
        ).count()
        
        print(f"\n{i}. {room.name}")
        print(f"   Last message: {last_message.content[:50] if last_message else 'None'}")
        print(f"   Unread: {unread_count}")
        print(f"   Members: {room.members.count()}")
        print(f"   Type: group")
    
    print(f"\n{'='*60}")
    print(f"TOTAL CONVERSATIONS: {conversation_users.count() + group_chat_rooms.count()}")
    print(f"{'='*60}\n")

from django.db.models import Q
