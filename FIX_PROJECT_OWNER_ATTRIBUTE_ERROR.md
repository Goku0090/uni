# Fix: 'Project' object has no attribute 'owner' - AttributeError

## Problem
```
AttributeError at /post-project/
'Project' object has no attribute 'owner'
Exception Location: signals_realtime.py, line 28, in project_status_changed
```

## Root Cause
The Project model uses `user` field, but the signals_realtime.py code tries to access `instance.owner`

**In models.py (line 417):**
```python
user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='projects')
```

**In signals_realtime.py (line 28):**
```python
actor=instance.owner,  # ❌ WRONG - should be instance.user
```

---

## Solution

Replace all references to `instance.owner` with `instance.user` in signals_realtime.py

### Step 1: Open the file
File: `auth_project/accounts/signals_realtime.py`

### Step 2: Replace all occurrences

**Find 5 locations and fix them:**

#### Fix 1 - Line 28
```python
# BEFORE
broadcast_activity_feed(
    actor=instance.owner,  # ❌ WRONG

# AFTER
broadcast_activity_feed(
    actor=instance.user,  # ✅ CORRECT
```

#### Fix 2 - Line 36
```python
# BEFORE
broadcast_activity_feed(
    actor=instance.owner,  # ❌ WRONG

# AFTER
broadcast_activity_feed(
    actor=instance.user,  # ✅ CORRECT
```

#### Fix 3 - Line 87
```python
# BEFORE
notify_user(
    user=project.owner,  # ❌ WRONG

# AFTER
notify_user(
    user=project.user,  # ✅ CORRECT
```

#### Fix 4 - Line 126
```python
# BEFORE
if instance.user != project.owner:  # ❌ WRONG

# AFTER
if instance.user != project.user:  # ✅ CORRECT
```

#### Fix 5 - Line 154
```python
# BEFORE
if instance.user != project.owner:  # ❌ WRONG

# AFTER
if instance.user != project.user:  # ✅ CORRECT
```

---

## Complete Fixed File

Here's the corrected signals_realtime.py:

```python
"""
Django signals for real-time project updates
Triggers WebSocket events when models change
"""

from django.db.models.signals import post_save, pre_save
from django.dispatch import receiver
from django.utils import timezone
from asgiref.sync import async_to_sync
from channels.layers import get_channel_layer
import json
import logging

logger = logging.getLogger(__name__)


@receiver(post_save, sender='accounts.Project')
def project_status_changed(sender, instance, created, **kwargs):
    """
    Signal handler for project status changes
    Broadcasts to all users watching this project
    """
    if created:
        # New project created
        broadcast_activity_feed(
            actor=instance.user,  # ✅ FIXED: was instance.owner
            activity_type='project.created',
            project=instance,
            action=f"Created project '{instance.title}'",
        )
    else:
        # Project updated (status, description, etc)
        broadcast_activity_feed(
            actor=instance.user,  # ✅ FIXED: was instance.owner
            activity_type='project.updated',
            project=instance,
            action=f"Updated project '{instance.title}'",
        )
        
        # Broadcast to specific project group
        channel_layer = get_channel_layer()
        async_to_sync(channel_layer.group_send)(
            f'project_{instance.id}',
            {
                'type': 'project.member_count_update',
                'current_members': instance.members.count(),
                'required_members': getattr(instance, 'team_size', None),
            }
        )


@receiver(post_save, sender='accounts.ProjectMember')
def team_member_added(sender, instance, created, **kwargs):
    """
    Signal handler for new team members
    Broadcasts member addition to project group
    """
    if created:
        project = instance.project
        member = instance.member
        
        # Broadcast to project group
        channel_layer = get_channel_layer()
        async_to_sync(channel_layer.group_send)(
            f'project_{project.id}',
            {
                'type': 'project.member_added',
                'user_id': member.id,
                'username': member.username,
                'full_name': member.student_profile.full_name if hasattr(member, 'student_profile') else member.get_full_name(),
                'timestamp': timezone.now().isoformat(),
            }
        )
        
        # Broadcast to activity feed
        broadcast_activity_feed(
            actor=member,
            activity_type='member.added',
            project=project,
            action=f"Joined '{project.title}' team",
        )
        
        # Send notification to project owner
        notify_user(
            user=project.user,  # ✅ FIXED: was project.owner
            title='New Team Member',
            message=f'{member.get_full_name()} joined your project',
            notification_type='member_added',
            related_object_id=project.id,
        )


@receiver(post_save, sender='accounts.Comment')
def comment_posted(sender, instance, created, **kwargs):
    """
    Signal handler for new comments
    Broadcasts comment to project group
    """
    if created:
        project = instance.project
        
        # Broadcast to project group
        channel_layer = get_channel_layer()
        async_to_sync(channel_layer.group_send)(
            f'project_{project.id}',
            {
                'type': 'project.comment_posted',
                'comment_id': instance.id,
                'author': instance.user.username,
                'text': instance.text[:100],  # First 100 chars
                'timestamp': timezone.now().isoformat(),
            }
        )
        
        # Broadcast to activity feed
        broadcast_activity_feed(
            actor=instance.user,
            activity_type='comment.posted',
            project=project,
            action=f"Commented on '{project.title}'",
        )
        
        # Notify project owner
        if instance.user != project.user:  # ✅ FIXED: was project.owner
            notify_user(
                user=project.user,  # ✅ FIXED: was project.owner
                title='New Comment',
                message=f'{instance.user.username} commented on your project',
                notification_type='comment_posted',
                related_object_id=project.id,
            )


@receiver(post_save, sender='accounts.Like')
def like_added(sender, instance, created, **kwargs):
    """
    Signal handler for project likes
    Notifies project owner
    """
    if created:
        project = instance.project
        
        # Broadcast to activity feed
        broadcast_activity_feed(
            actor=instance.user,
            activity_type='like.added',
            project=project,
            action=f"Liked '{project.title}'",
        )
        
        # Notify project owner
        if instance.user != project.user:  # ✅ FIXED: was project.owner
            notify_user(
                user=project.user,  # ✅ FIXED: was project.owner
                title='Project Liked',
                message=f'{instance.user.username} liked your project',
                notification_type='like_added',
                related_object_id=project.id,
            )


@receiver(post_save, sender='accounts.Connection')
def connection_created(sender, instance, created, **kwargs):
    """
    Signal handler for new connections
    Notifies when users connect
    """
    if created:
        # Notify the user receiving the connection request
        notify_user(
            user=instance.to_user,
            title='New Connection Request',
            message=f'{instance.from_user.username} sent you a connection request',
            notification_type='connection_request',
            related_object_id=instance.from_user.id,
        )


def broadcast_activity_feed(actor, activity_type, project, action):
    """
    Broadcast activity to all users following the project or actor
    """
    try:
        channel_layer = get_channel_layer()
        
        # Get all connections of the actor
        from .models import Connection
        followers = Connection.objects.filter(
            to_user=actor,
            is_following=True
        ).values_list('from_user_id', flat=True)
        
        # Broadcast to each follower
        for user_id in followers:
            async_to_sync(channel_layer.group_send)(
                f'activity_feed_{user_id}',
                {
                    'type': 'activity.notification',
                    'activity_type': activity_type,
                    'project_id': project.id,
                    'project_title': project.title,
                    'action': action,
                    'actor': actor.username,
                    'timestamp': timezone.now().isoformat(),
                }
            )
    except Exception as e:
        logger.error(f"Error broadcasting activity: {str(e)}")


def notify_user(user, title, message, notification_type, related_object_id=None):
    """
    Send notification to user via WebSocket
    """
    try:
        # Create notification in database
        from .models import Notification
        notification = Notification.objects.create(
            user=user,
            type=notification_type,
            related_object_id=related_object_id,
            message=message,
        )
        
        # Send via WebSocket
        channel_layer = get_channel_layer()
        async_to_sync(channel_layer.group_send)(
            f'notifications_{user.id}',
            {
                'type': 'send.notification',
                'notification_id': notification.id,
                'title': title,
                'message': message,
                'notification_type': notification_type,
                'related_object_id': related_object_id,
                'timestamp': timezone.now().isoformat(),
            }
        )
    except Exception as e:
        logger.error(f"Error sending notification: {str(e)}")


def ready():
    """
    Register signal handlers
    Called from apps.py
    """
    try:
        from django.apps import apps
        from .models import Project, ProjectMember, Comment, Like, Connection
        
        post_save.connect(project_status_changed, sender=Project)
        post_save.connect(team_member_added, sender=ProjectMember)
        post_save.connect(comment_posted, sender=Comment)
        post_save.connect(like_added, sender=Like)
        post_save.connect(connection_created, sender=Connection)
        
        logger.info("Real-time signal handlers registered successfully")
    except Exception as e:
        logger.error(f"Error registering signal handlers: {str(e)}")
```

---

## Implementation Steps

### Option 1: Manual Fix (5 minutes)
1. Open: `auth_project/accounts/signals_realtime.py`
2. Find and replace:
   - `instance.owner` → `instance.user`
   - `project.owner` → `project.user`
3. Save the file
4. Test

### Option 2: Automated Replace (1 minute)
Using Find and Replace in your editor:
- Find: `\.owner`
- Replace: `\.user`
- **In file:** `signals_realtime.py` only

---

## Testing After Fix

### Test 1: Create a project
```
1. Go to /post-project/
2. Fill in the form
3. Submit
4. Should work without error ✅
```

### Test 2: Run the project
```bash
# Start the server
cd auth_project
python manage.py runserver

# Test creating a project
# Visit: http://localhost:8000/post-project/
```

### Test 3: Check signals
```bash
# Check if signals are firing
# Look for log messages in console:
# "Real-time signal handlers registered successfully"
```

---

## Summary of Changes

| Line | Before | After | Status |
|------|--------|-------|--------|
| 28 | `instance.owner` | `instance.user` | ✅ Fixed |
| 36 | `instance.owner` | `instance.user` | ✅ Fixed |
| 87 | `project.owner` | `project.user` | ✅ Fixed |
| 126 | `project.owner` | `project.user` | ✅ Fixed |
| 154 | `project.owner` | `project.user` | ✅ Fixed |

---

## Why This Happened

The codebase was inconsistent:
- **Project model** uses: `user` field
- **signals_realtime.py** expected: `owner` field

This is a common issue when code is written at different times or by different developers without consistency.

---

## Prevention Tips

For future development:
1. ✅ Always check model fields before using them in signals
2. ✅ Use IDE autocomplete to avoid typos
3. ✅ Test signals after creating models
4. ✅ Add type hints: `instance: Project` (IDE catches mistakes)
5. ✅ Write tests for signals

---

## Related Files to Check

Also check these files for similar issues:

```bash
# Search for .owner in other files
grep -r "\.owner" auth_project/accounts/

# If found, replace with .user
```

---

## Quick Fix (Copy-Paste)

Replace the entire file with the corrected version above, or manually change:

```python
# All 5 locations:
instance.owner → instance.user
project.owner → project.user
```

---

**Status:** Ready to fix ✅  
**Time:** 5 minutes  
**Difficulty:** Very easy  
**Risk:** Very low
