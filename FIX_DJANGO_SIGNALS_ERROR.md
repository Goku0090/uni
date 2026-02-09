# Fix Django Signals Error - ProjectTeamMember Reference

**Issue:** Django SystemCheckError on server startup  
**Status:** ✅ **FIXED**  
**Severity:** Critical (prevents server startup)

---

## The Error

```
django.core.management.base.SystemCheckError: System check identified some issues:

ERRORS:
accounts.signals_realtime: (signals.E001) The function 'team_member_added' was 
connected to the 'post_save' signal with a lazy reference to the sender 
'accounts.projectteammember', but app 'accounts' doesn't provide model 'projectteammember'.
```

**Translation:** The signals file is trying to reference a model `ProjectTeamMember` that doesn't actually exist in the accounts app.

---

## Root Cause

In `models.py`, `ProjectTeamMember` is defined as an **alias** (backward compatibility):

```python
# At bottom of models.py
ProjectTeam = ProjectMember
ProjectTeamMember = ProjectMember  # Just an alias, not a real model
```

But `signals_realtime.py` was trying to use it as if it were a real model:

```python
# BROKEN - Using the alias instead of real model
@receiver(post_save, sender='accounts.ProjectTeamMember')
from .models import Project, ProjectTeamMember, Comment, Like, Connection
post_save.connect(team_member_added, sender=ProjectTeamMember)
```

---

## The Fix

Changed all references from `ProjectTeamMember` to `ProjectMember`:

### Change 1: Decorator
```python
# BEFORE
@receiver(post_save, sender='accounts.ProjectTeamMember')

# AFTER
@receiver(post_save, sender='accounts.ProjectMember')
```

### Change 2: Import
```python
# BEFORE
from .models import Project, ProjectTeamMember, Comment, Like, Connection

# AFTER
from .models import Project, ProjectMember, Comment, Like, Connection
```

### Change 3: Signal Connection
```python
# BEFORE
post_save.connect(team_member_added, sender=ProjectTeamMember)

# AFTER
post_save.connect(team_member_added, sender=ProjectMember)
```

---

## Files Modified

| File | Change | Status |
|------|--------|--------|
| `accounts/signals_realtime.py` | Line 54: Decorator | ✅ Fixed |
| `accounts/signals_realtime.py` | Line 252: Import | ✅ Fixed |
| `accounts/signals_realtime.py` | Line 255: Connection | ✅ Fixed |

---

## What This Signal Does

The `team_member_added` signal triggers when a new team member is added to a project:

```
New ProjectMember created
    ↓
Signal fires
    ↓
Broadcast to WebSocket group
    ↓
All viewers see "New member joined" instantly
```

This is part of the real-time features for project collaboration.

---

## How to Test

### Before Fix
```bash
python manage.py runserver
# ERROR: SystemCheckError - Can't find ProjectTeamMember model
# Server won't start
```

### After Fix
```bash
python manage.py runserver
# ✅ System check passed
# ✅ Server starts successfully
# ✅ No warnings or errors

# OR with Daphne:
daphne -b 127.0.0.1 -p 8000 auth_project.asgi:application
# ✅ Listening on TCP address 127.0.0.1:8000
```

---

## Deployment

This fix is included in your codebase. To deploy:

```bash
git add accounts/signals_realtime.py
git commit -m "Fix signals error: use ProjectMember instead of alias ProjectTeamMember"
git push origin main
```

---

## Related

This was discovered while testing the overall application. It prevents:
- ✅ Server startup
- ✅ Real-time team member notifications
- ✅ WebSocket broadcasting for project updates

All fixed now! ✅

---

## Summary

| Aspect | Before | After |
|--------|--------|-------|
| **Server Start** | ❌ SystemCheckError | ✅ Works |
| **Model Reference** | Wrong (alias) | Correct (real model) |
| **Signal Handler** | Broken | Working |
| **Real-time Updates** | Not possible | Enabled ✅ |

---

**Status:** ✅ Fixed and ready to deploy
