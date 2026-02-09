# ACTION PLAN: Fix OAuth MultipleObjectsReturned Error (5-10 minutes)

## Current Status
- OAuth error when clicking "Login with Google" / "Login with GitHub"
- Error: `django.core.exceptions.MultipleObjectsReturned`
- WebSocket code tested and ready

## Root Cause
Multiple SocialApp entries in database causing allauth adapter confusion

## Step-by-Step Fix

### Step 1: Run Diagnostic (1 minute)
```bash
cd e:\login\auth_project
python diagnose_oauth_error.py
```

**Expected output:**
```
Total Google apps: 1
Total GitHub apps: 1
```

**If shows > 1:** Continue to Step 2

### Step 2: Run Cleanup Script (1 minute)
```bash
python fix_duplicate_oauth.py
```

**What it does:**
- Detects duplicate SocialApp entries
- Keeps the first one
- Deletes all duplicates
- Verifies the fix

**Expected output:**
```
[OK] GOOGLE: 1 app exists
[OK] GITHUB: 1 app exists
```

### Step 3: Manual Fix (if needed)
```bash
python manage.py shell
```

```python
from allauth.socialaccount.models import SocialApp

# Count current apps
google = SocialApp.objects.filter(provider='google')
github = SocialApp.objects.filter(provider='github')

print(f"Google apps: {google.count()}")
print(f"GitHub apps: {github.count()}")

# If > 1, delete duplicates
if google.count() > 1:
    print(f"Deleting {google.count() - 1} duplicate Google apps...")
    google.exclude(id=google.first().id).delete()

if github.count() > 1:
    print(f"Deleting {github.count() - 1} duplicate GitHub apps...")
    github.exclude(id=github.first().id).delete()

# Verify
google_final = SocialApp.objects.filter(provider='google').count()
github_final = SocialApp.objects.filter(provider='github').count()

print(f"\nAfter cleanup:")
print(f"Google apps: {google_final}")  # Should be 1
print(f"GitHub apps: {github_final}")  # Should be 1

exit()
```

### Step 4: Update Credentials (2 minutes)
```
URL: http://localhost:8000/admin/socialaccount/socialapp/
```

For each OAuth app:

**Google:**
- Client id: `(from Google Cloud Console)`
- Client secret: `(from Google Cloud Console)`
- Sites: Add `localhost:8000`

**GitHub:**
- Client id: `(from GitHub OAuth app)`
- Client secret: `(from GitHub OAuth app)`
- Sites: Add `localhost:8000`

### Step 5: Clear Cache & Restart
```bash
# Clear Django cache
python manage.py shell
```

```python
from django.core.cache import cache
cache.clear()
print("Cache cleared")
exit()
```

### Step 6: Test OAuth Login
```
1. Browser: http://localhost:8000/accounts/login/
2. Click "Login with Google"
3. Should redirect to Google OAuth login page (NOT error)
4. Complete login flow
```

## Expected Result
- ✅ OAuth login works
- ✅ No MultipleObjectsReturned error
- ✅ User can login with Google/GitHub
- ✅ WebSocket can connect: `ws://localhost:8000/ws/project/2/`

## If Still Not Working

### Check 1: Django Logs
```bash
type e:\login\auth_project\logs\django.log | findstr "oauth"
type e:\login\auth_project\logs\django.log | findstr "error"
```

### Check 2: Verify Site Configuration
```bash
python manage.py shell
```

```python
from django.contrib.sites.models import Site
from django.conf import settings

site = Site.objects.get(id=settings.SITE_ID)
print(f"Current site: {site.domain} (ID: {site.id})")
print(f"Make sure this matches your localhost URL")

exit()
```

### Check 3: Database State
```bash
python diagnose_oauth_error.py
python deep_debug_oauth.py
```

### Check 4: Reset Everything
```bash
# NUCLEAR OPTION - Only if nothing else works
python manage.py shell
```

```python
from allauth.socialaccount.models import SocialApp
from django.contrib.sites.models import Site

# Backup current setup
print("Current apps:")
for app in SocialApp.objects.all():
    print(f"  {app.name}: {app.client_id}")

# Delete all
SocialApp.objects.all().delete()

# Get site
site = Site.objects.get(id=1)

# Create fresh
google = SocialApp.objects.create(
    provider='google',
    name='Google',
    client_id='your-google-client-id',
    secret='your-google-client-secret'
)
google.sites.add(site)

github = SocialApp.objects.create(
    provider='github',
    name='GitHub',
    client_id='your-github-client-id',
    secret='your-github-client-secret'
)
github.sites.add(site)

print("OAuth apps recreated")
exit()
```

Then update credentials in Django admin.

## Troubleshooting

| Symptom | Cause | Fix |
|---------|-------|-----|
| Still get MultipleObjectsReturned | Duplicates still exist | Run `fix_duplicate_oauth.py` again |
| OAuth link does nothing | No credentials | Update in Django admin |
| Redirects to error page | Wrong site domain | Check `SITE_ID` in settings |
| Cache still invalid | Django cache outdated | Run `cache.clear()` |
| WebSocket won't connect | Server not running | Start: `python manage.py runworker` |

## Files You'll Use

1. **diagnose_oauth_error.py** - Check what's wrong
2. **fix_duplicate_oauth.py** - Automatic fix
3. **reset_oauth_config.py** - Full reset
4. **FIX_OAUTH_ERROR_QUICK.md** - Quick reference
5. **SOLUTION_MULTIPLEOBJECTSRETURNED_AND_WEBSOCKET.md** - Complete guide

## Quick Summary

```
Problem:  MultipleObjectsReturned on OAuth login
Solution: Run fix_duplicate_oauth.py
Time:     5-10 minutes
Result:   OAuth login works, WebSocket ready
```

---

## Testing After Fix

### Terminal 1: Start Django
```bash
cd e:\login\auth_project
python manage.py runserver
```

### Terminal 2: Start WebSocket (if testing WebSocket)
```bash
cd e:\login\auth_project
python manage.py runworker project_update activity_feed notifications
```

### Browser Test
```javascript
// Test OAuth
// Click: http://localhost:8000/accounts/login/ -> "Login with Google"

// Test WebSocket
let socket = new WebSocket("ws://localhost:8000/ws/project/2/");
socket.onopen = () => console.log("✅ WebSocket Connected!");
socket.onerror = (e) => console.error("Error:", e);
```

---

**Ready to fix? Start with Step 1!**

Last Updated: 2026-02-08
