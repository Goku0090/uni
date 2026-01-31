# Message Read Status - Fix Required

## Problem

The code tries to use `is_read` field on Message model, but the Message model uses a separate `MessageReadStatus` model to track read/unread status.

```
Error: FieldError: Cannot resolve keyword 'is_read' into field
```

## Root Cause

- **Message model:** Uses `MessageReadStatus` model for tracking (no `is_read` field)
- **Code:** Multiple views try to filter/update using `is_read=False`
- **Result:** Database error when accessing messages

## Affected Lines

| Line | Issue | Fix |
|------|-------|-----|
| 1848-1852 | `is_read=False` filter in message_view | ✅ FIXED |
| 889-893 | `is_read=False` update in chat_view | Needs fixing |
| 911-915 | `is_read=False` update in chat_view | Needs fixing |

## How to Fix

The Message model provides helper methods:

```python
# Check if message is read by a user
message.is_read_by(user)  # Returns: True/False

# Mark message as read by user
message.mark_as_read_by(user)  # Creates MessageReadStatus entry
```

### Fix for Line 889-893

**Before (BROKEN):**
```python
Message.objects.filter(
    sender=other_user,
    receiver=request.user,
    is_read=False
).update(is_read=True, read_at=timezone.now())
```

**After (FIXED):**
```python
received_messages = Message.objects.filter(
    sender=other_user,
    receiver=request.user
)
for message in received_messages:
    message.mark_as_read_by(request.user)
```

### Fix for Line 911-915

**Before (BROKEN):**
```python
Message.objects.filter(
    sender=other_user,
    receiver=request.user,
    is_read=False
).update(is_read=True)
```

**After (FIXED):**
```python
received_messages = Message.objects.filter(
    sender=other_user,
    receiver=request.user
)
for message in received_messages:
    if not message.is_read_by(request.user):
        message.mark_as_read_by(request.user)
```

## Database Models Reference

### Message Model (Line 149)
```python
class Message(models.Model):
    sender = ForeignKey(User)
    receiver = ForeignKey(User)
    content = TextField()
    # NO is_read field!
    # Uses MessageReadStatus instead
    
    def mark_as_read_by(self, user):
        """Mark message as read by a user"""
        MessageReadStatus.objects.get_or_create(
            message=self,
            user=user,
            defaults={'read_at': timezone.now()}
        )
    
    def is_read_by(self, user):
        """Check if read by user"""
        return MessageReadStatus.objects.filter(
            message=self, 
            user=user
        ).exists()
```

### MessageReadStatus Model (Line 264)
```python
class MessageReadStatus(models.Model):
    message = ForeignKey(Message)
    user = ForeignKey(User)
    read_at = DateTimeField()
    
    class Meta:
        unique_together = ['message', 'user']
```

## Complete Fix for views.py

You need to manually edit these lines in `accounts/views.py`:

### Location 1: Line 889-893
```python
# OLD:
Message.objects.filter(
    sender=other_user,
    receiver=request.user,
    is_read=False
).update(is_read=True, read_at=timezone.now())

# NEW:
received_messages = Message.objects.filter(
    sender=other_user,
    receiver=request.user
)
for message in received_messages:
    message.mark_as_read_by(request.user)
```

### Location 2: Line 911-915
```python
# OLD:
Message.objects.filter(
    sender=other_user,
    receiver=request.user,
    is_read=False
).update(is_read=True)

# NEW:
received_messages = Message.objects.filter(
    sender=other_user,
    receiver=request.user
)
for message in received_messages:
    message.mark_as_read_by(request.user)
```

## Testing After Fix

```python
# In Django shell
python manage.py shell

# Test marking message as read
from accounts.models import Message, MessageReadStatus, User
msg = Message.objects.first()
user = User.objects.first()

# Mark as read
msg.mark_as_read_by(user)

# Check if read
print(msg.is_read_by(user))  # Should print: True

exit()
```

## Why This Design?

Using a separate `MessageReadStatus` model is better because:

1. **Scalability:** Each message tracks read status per user
2. **Timestamps:** Records when each user read the message
3. **Group Chats:** Supports multiple users reading same message
4. **No data loss:** Old status preserved (not overwritten)

## Complete Notification Model (for reference)

The `Notification` model DOES have `is_read`:
```python
class Notification(models.Model):
    ...
    is_read = BooleanField(default=False)  # ✅ This is correct
```

So notifications can use `is_read=False` directly, but messages cannot.

## Summary

**The Issue:** Code uses `is_read` on Message model, but it doesn't exist

**The Solution:** Use the Message model's helper methods:
- `message.mark_as_read_by(user)` - Mark as read
- `message.is_read_by(user)` - Check if read

**Files to Edit:** `accounts/views.py` lines 889-893 and 911-915

**Time to Fix:** 2 minutes (2 manual edits)
