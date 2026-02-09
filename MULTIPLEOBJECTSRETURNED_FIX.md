# ✅ MultipleObjectsReturned Error - FIXED

## The Problem

```
django.core.exceptions.MultipleObjectsReturned
[ERROR] "GET /login/ HTTP/1.1" 500
```

When visiting `/login/`, django-allauth tries to get the OAuth provider (Google/GitHub) but finds **multiple SocialApp entries** for the same provider, causing the error.

---

## Root Cause

Duplicate `SocialApp` objects in the database:
- Multiple Google apps configured
- Or multiple GitHub apps configured
- Django-allauth can't decide which one to use → crashes

This happens when:
1. Social apps are manually created in admin
2. Setup scripts run multiple times
3. Test data not cleaned up

---

## Solution: Clean Up Database

Run these Django shell commands to remove duplicates:

### Option 1: Via Django Shell (Recommended)

```bash
cd e:/login/auth_project
python manage.py shell
```

Then paste these commands:

```python
from allauth.socialaccount.models import SocialApp
from django.contrib.sites.models import Site

# Get current site
site = Site.objects.get_current()
print(f"Current site: {site.domain}")

# Fix Google
google_apps = SocialApp.objects.filter(provider='google')
if google_apps.count() > 1:
    print(f"\nFound {google_apps.count()} Google apps - removing duplicates")
    keep = google_apps.first()
    print(f"Keeping: {keep.name} (ID: {keep.id})")
    for app in google_apps.exclude(id=keep.id):
        print(f"Deleting: {app.name} (ID: {app.id})")
        app.delete()
    if not keep.sites.filter(id=site.id).exists():
        keep.sites.add(site)
        print(f"Added site to {keep.name}")
elif google_apps.count() == 1:
    app = google_apps.first()
    if not app.sites.filter(id=site.id).exists():
        app.sites.add(site)
        print("Google app linked to current site")
    print("Google: ✓ OK")

# Fix GitHub
github_apps = SocialApp.objects.filter(provider='github')
if github_apps.count() > 1:
    print(f"\nFound {github_apps.count()} GitHub apps - removing duplicates")
    keep = github_apps.first()
    print(f"Keeping: {keep.name} (ID: {keep.id})")
    for app in github_apps.exclude(id=keep.id):
        print(f"Deleting: {app.name} (ID: {app.id})")
        app.delete()
    if not keep.sites.filter(id=site.id).exists():
        keep.sites.add(site)
        print(f"Added site to {keep.name}")
elif github_apps.count() == 1:
    app = github_apps.first()
    if not app.sites.filter(id=site.id).exists():
        app.sites.add(site)
        print("GitHub app linked to current site")
    print("GitHub: ✓ OK")

# Summary
print("\nFinal status:")
print(f"Google apps: {SocialApp.objects.filter(provider='google').count()}")
print(f"GitHub apps: {SocialApp.objects.filter(provider='github').count()}")
print("\n✓ Done!")
```

Then type `exit()` to quit.

---

### Option 2: Via Admin Panel

1. Go to http://localhost:8000/admin/
2. Login with superuser
3. Navigate to **Sites Framework → Sites** and make sure your domain is there
4. Navigate to **Socialaccount → Social Applications**
5. Look for duplicate entries (multiple Google or GitHub)
6. **Keep only ONE of each** provider
7. For each kept app, ensure it's linked to your site
8. Delete all others

---

### Option 3: Via Python Script

Run this from the project directory:

```bash
python manage.py shell < cleanup_social_apps.py
```

Where `cleanup_social_apps.py` is:

```python
from allauth.socialaccount.models import SocialApp
from django.contrib.sites.models import Site

site = Site.objects.get_current()

for provider in ['google', 'github']:
    apps = SocialApp.objects.filter(provider=provider)
    if apps.count() > 1:
        keep = apps.first()
        for app in apps.exclude(id=keep.id):
            app.delete()
        if not keep.sites.filter(id=site.id).exists():
            keep.sites.add(site)
        print(f"✓ Fixed {provider}")
```

---

## Verification

After cleanup, check the database:

```python
python manage.py shell

from allauth.socialaccount.models import SocialApp

# Should show exactly 1 Google, 1 GitHub (or 0 if not configured)
for app in SocialApp.objects.all():
    print(f"{app.provider}: {app.name} (ID: {app.id})")
```

Expected output:
```
google: Google (ID: 1)
github: GitHub (ID: 2)
```

Or if not configured:
```
(no output - no apps)
```

---

## Test the Fix

1. **Stop Django**: Ctrl+C
2. **Run Django**: `python manage.py runserver`
3. **Visit login page**: http://localhost:8000/login/
4. Should load without error ✓

---

## What Happens After Fix

### If OAuth is configured:
- ✓ Login page loads
- ✓ "Google" button is clickable
- ✓ "GitHub" button is clickable

### If OAuth is NOT configured:
- ✓ Login page loads
- ✓ OAuth buttons appear disabled (grayed out)
- ✓ Users can still login via Email + OTP
- ✓ No errors

---

## Prevention

To prevent future duplicates:

1. **Never manually create SocialApp in code**
   - Use admin interface instead
   
2. **Don't run setup scripts multiple times**
   - Always check database first
   
3. **Clean up test data**
   - Before deployment, remove test SocialApps

4. **Use environment variables**
   - Render auto-creates/updates SocialApp from env vars
   - No manual intervention needed

---

## If Still Having Issues

### Check logs:
```bash
tail -f logs/django.log
```

### Check database directly:
```python
python manage.py dbshell

# SQLite
SELECT * FROM socialaccount_socialapp;

# PostgreSQL
SELECT id, name, provider, client_id FROM socialaccount_socialapp;
```

### Check Site configuration:
```python
python manage.py shell

from django.contrib.sites.models import Site
site = Site.objects.get_current()
print(f"Site: {site.domain} (ID: {site.id})")
```

Must match your actual domain!

---

## Files to Check

| File | Purpose |
|------|---------|
| `settings.py` | SITE_ID = 1 |
| `login.html` | OAuth button template (conditional) |
| `views.py:login_view` | Passes OAuth credentials to template |
| Database | `socialaccount_socialapp` table |

---

## Status

After running the cleanup script:

- ✅ No duplicate SocialApp entries
- ✅ Each provider has at most 1 app
- ✅ All apps linked to correct site
- ✅ Login page loads without error
- ✅ OAuth works (if configured) or disables gracefully

---

**Quick Fix**: Run the Django shell commands above (Option 1)  
**Time**: 2 minutes  
**Difficulty**: Easy

Let me know if you need help running the cleanup!
