# UniSync OAuth Error Fix Guide

## Problem Summary
When users click "Login with Google" or "Login with GitHub", they get a 500 error:
```
django.core.exceptions.MultipleObjectsReturned
```

## Root Cause
The Django Allauth OAuth adapter found **multiple SocialApp entries** (OAuth configurations) in the database, but it expected exactly one per provider.

## Solution (Choose One)

### ⚡ Quick Fix (Recommended - 2 minutes)
```bash
cd auth_project
python fix_duplicate_oauth.py
```

### Manual Fix (5 minutes)
```bash
python manage.py shell
```

```python
from allauth.socialaccount.models import SocialApp

# Delete all duplicates
google_apps = SocialApp.objects.filter(provider='google')
if google_apps.count() > 1:
    google_apps.exclude(id=google_apps.first().id).delete()

github_apps = SocialApp.objects.filter(provider='github')
if github_apps.count() > 1:
    github_apps.exclude(id=github_apps.first().id).delete()

# Verify
print(f"Google: {SocialApp.objects.filter(provider='google').count()}")
print(f"GitHub: {SocialApp.objects.filter(provider='github').count()}")

exit()
```

### Full Reset (10 minutes)
```bash
python reset_oauth_config.py
```

## After Fixing

1. **Update credentials** in Django admin:
   - URL: `http://localhost:8000/admin/socialaccount/socialapp/`
   - Add Google Client ID and Secret
   - Add GitHub Client ID and Secret

2. **Test OAuth login**:
   - Go to: `http://localhost:8000/accounts/login/`
   - Click "Login with Google"
   - Should work!

## Files Available

| File | Purpose | Runtime |
|------|---------|---------|
| `fix_duplicate_oauth.py` | Automatic duplicate removal | 1 min |
| `diagnose_oauth_error.py` | Diagnose what's wrong | 1 min |
| `reset_oauth_config.py` | Full reset with validation | 2 min |
| `deep_debug_oauth.py` | Deep database inspection | 1 min |
| `ACTION_PLAN_FIX_OAUTH_NOW.md` | Step-by-step guide | - |
| `FIX_OAUTH_ERROR_QUICK.md` | Quick reference | - |
| `SOLUTION_MULTIPLEOBJECTSRETURNED_AND_WEBSOCKET.md` | Full explanation | - |
| `FIX_OAUTH_MULTIPLEOBJECTSRETURNED_ERROR.md` | Detailed solutions | - |

## Testing Checklist

- [ ] Run `python fix_duplicate_oauth.py`
- [ ] Check output: Shows 1 Google, 1 GitHub app
- [ ] Go to Django admin `/admin/socialaccount/socialapp/`
- [ ] Verify each app has valid credentials
- [ ] Clear browser cookies: `Ctrl+Shift+Delete`
- [ ] Test OAuth: `http://localhost:8000/accounts/login/`
- [ ] Click "Login with Google"
- [ ] Should redirect to Google login (not error)

## Quick Verification

```bash
# Check what's in database
python diagnose_oauth_error.py

# Expected output should show:
# Google apps on current site: 1
# GitHub apps on current site: 1
```

## WebSocket Status
Your WebSocket code is correct:
```javascript
let socket = new WebSocket("ws://localhost:8000/ws/project/2/");
socket.onopen = () => console.log("✅ WORKING!");
```

To use it:
1. Start WebSocket server: `python manage.py runworker project_update activity_feed notifications`
2. Have Redis running
3. Connect from browser (see `SOLUTION_MULTIPLEOBJECTSRETURNED_AND_WEBSOCKET.md` for details)

## Need More Help?

- **Quick reference**: `FIX_OAUTH_ERROR_QUICK.md`
- **Step-by-step**: `ACTION_PLAN_FIX_OAUTH_NOW.md`
- **Detailed guide**: `SOLUTION_MULTIPLEOBJECTSRETURNED_AND_WEBSOCKET.md`
- **Complete explanation**: `FIX_OAUTH_MULTIPLEOBJECTSRETURNED_ERROR.md`

## Summary

```
Error: MultipleObjectsReturned on OAuth login
Cause: Duplicate SocialApp entries
Fix:   python fix_duplicate_oauth.py
Time:  2-5 minutes
```

---

**Status**: Ready to implement  
**Created**: 2026-02-08  
**Location**: `/auth_project/`
