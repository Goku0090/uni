# Fix: signals_realtime.py AttributeError - Complete Resolution

## Problem
```
AttributeError at /post-project/
'Project' object has no attribute 'owner'
Exception Location: e:\login\auth_project\accounts\signals_realtime.py, line 28
```

## Root Causes & Fixes Applied

### 1. **ProjectMember Model Field Name Mismatch** (Line 65)
**Issue:** Signal handler references `instance.member` which doesn't exist  
**Model Definition:** ProjectMember has `user` field (not `member`)

```python
# BEFORE (Wrong)
member = instance.member

# AFTER (Fixed)
member = instance.user
```

---

### 2. **Connection Model Field Name Mismatch** (Lines 176-181)
**Issue:** Signal handler references `instance.from_user` and `instance.to_user`  
**Model Definition:** Connection model uses `sender` and `receiver` fields

```python
# BEFORE (Wrong)
notify_user(
    user=instance.to_user,
    message=f'{instance.from_user.username} sent you a connection request',
    related_object_id=instance.from_user.id,
)

# AFTER (Fixed)
notify_user(
    user=instance.receiver,
    message=f'{instance.sender.username} sent you a connection request',
    related_object_id=instance.sender.id,
)
```

---

### 3. **Connection Query Field Mismatch** (Lines 193-196)
**Issue:** `broadcast_activity_feed()` queries Connection with non-existent fields  
**Model Definition:** Connection has `sender`, `receiver`, `status` (not `from_user`, `to_user`, `is_following`)

```python
# BEFORE (Wrong)
followers = Connection.objects.filter(
    to_user=actor,
    is_following=True
).values_list('from_user_id', flat=True)

# AFTER (Fixed)
followers = Connection.objects.filter(
    receiver=actor,
    status='accepted'
).values_list('sender_id', flat=True)
```

---

### 4. **Notification Model Field Name Mismatch** (Lines 224-228)
**Issue:** Signal handler uses `type` instead of `notification_type`  
**Model Definition:** Notification model uses `notification_type` field

```python
# BEFORE (Wrong)
notification = Notification.objects.create(
    user=user,
    type=notification_type,
    related_object_id=related_object_id,
    message=message,
)

# AFTER (Fixed)
notification = Notification.objects.create(
    user=user,
    notification_type=notification_type,
    title=title,
    message=message,
)
```

---

## Summary of Field Name Corrections

| Model | Wrong Field | Correct Field | Context |
|-------|------------|---------------|---------|
| ProjectMember | `instance.member` | `instance.user` | Signal handler line 65 |
| Connection | `instance.to_user` | `instance.receiver` | Notification recipient |
| Connection | `instance.from_user` | `instance.sender` | Notification sender |
| Connection (Query) | `to_user`, `is_following` | `receiver`, `status='accepted'` | Activity broadcast |
| Connection (Query) | `from_user_id` | `sender_id` | Activity broadcast |
| Notification | `type=` | `notification_type=` | Object creation |
| Notification | Missing | `title=title` | Object creation |

---

## Testing Checklist

- [ ] Create a new project via `/post-project/` without AttributeError
- [ ] Send connection request and verify receiver notification
- [ ] Accept connection and verify activity broadcast
- [ ] Post comment on project and verify broadcast
- [ ] Like project and verify owner notification
- [ ] Check `/admin/accounts/notification/` for created notifications
- [ ] Verify WebSocket broadcasts reach correct channel groups

---

## Files Modified
- `e:/login/auth_project/accounts/signals_realtime.py`

## Date Fixed
February 07, 2026

## Related Issues
- Project creation error during signal handler execution
- Connection notifications not sent
- Activity feed broadcast failures
