# Fix: Django MultipleObjectsReturned Error on OAuth Login

## Error Analysis

```
django.core.exceptions.MultipleObjectsReturned
  File ".../allauth/socialaccount/adapter.py", line 299, in get_app
    raise MultipleObjectsReturned
```

### Root Causes

1. **Multiple SocialApp entries for Google** (most common)
2. **Multiple SocialApp entries for GitHub**
3. **One SocialApp linked to multiple Sites**
4. **Database migration issue** - stale data from development/testing

---

## Solution 1: Clean Database (Recommended)

### Step 1: Run Diagnostic Script

```bash
cd auth_project
python diagnose_oauth_error.py
```

Expected output:
```
Total SocialApps: 2
  - Google (ID: 1)
  - GitHub (ID: 2)

Google apps on current site: 1
GitHub apps on current site: 1
```

### Step 2: If Duplicates Found, Run Fix Script

```bash
python fix_duplicate_oauth.py
```

This script will:
- Identify duplicate SocialApp entries
- Keep the first one
- Delete all duplicates
- Verify the fix

---

## Solution 2: Manual Database Cleanup

### Option A: Django Shell

```bash
python manage.py shell
```

```python
from allauth.socialaccount.models import SocialApp
from django.contrib.sites.models import Site

# Get all Google apps
google_apps = SocialApp.objects.filter(provider='google')
print(f"Google apps: {google_apps.count()}")
for app in google_apps:
    print(f"  ID: {app.id}, Name: {app.name}")

# If more than 1, keep ID=1 and delete others
if google_apps.count() > 1:
    SocialApp.objects.filter(provider='google').exclude(id=1).delete()
    print("Deleted duplicate Google apps")

# Same for GitHub
github_apps = SocialApp.objects.filter(provider='github')
print(f"GitHub apps: {github_apps.count()}")
if github_apps.count() > 1:
    SocialApp.objects.filter(provider='github').exclude(id=1).delete()
    print("Deleted duplicate GitHub apps")

exit()
```

### Option B: Direct SQL

```sql
-- Check duplicates
SELECT provider, COUNT(*) FROM socialaccount_socialapp GROUP BY provider;

-- Delete duplicates (keep ID=1)
DELETE FROM socialaccount_socialapp 
WHERE provider='google' AND id > 1;

DELETE FROM socialaccount_socialapp 
WHERE provider='github' AND id > 1;
```

---

## Solution 3: Reset OAuth Configuration

### If the above doesn't work, reset SocialApps from scratch:

```bash
python manage.py shell
```

```python
from allauth.socialaccount.models import SocialApp
from django.contrib.sites.models import Site

# Delete all OAuth apps
SocialApp.objects.all().delete()
print("Deleted all SocialApps")

# Get the current site (should be localhost:8000)
site = Site.objects.first()
print(f"Current site: {site.domain}")

# Create fresh Google app
google = SocialApp.objects.create(
    provider='google',
    name='Google',
    client_id='YOUR_GOOGLE_CLIENT_ID',
    secret='YOUR_GOOGLE_CLIENT_SECRET'
)
google.sites.add(site)
print(f"Created Google app (ID: {google.id})")

# Create fresh GitHub app
github = SocialApp.objects.create(
    provider='github',
    name='GitHub',
    client_id='YOUR_GITHUB_CLIENT_ID',
    secret='YOUR_GITHUB_CLIENT_SECRET'
)
github.sites.add(site)
print(f"Created GitHub app (ID: {github.id})")

exit()
```

---

## Solution 4: Check Django Site Configuration

The error can also occur if your Site domain doesn't match your actual domain:

```bash
python manage.py shell
```

```python
from django.contrib.sites.models import Site

# List all sites
for site in Site.objects.all():
    print(f"Site ID: {site.id}, Domain: {site.domain}")

# Update if needed
site = Site.objects.get(id=1)
site.domain = 'localhost:8000'  # For development
site.name = 'Local Development'
site.save()

# Or for production
site.domain = 'yourdomain.com'
site.name = 'UniSync Production'
site.save()
```

---

## Solution 5: Clear Django Cache

Sometimes the cache holds stale data:

```bash
python manage.py shell
```

```python
from django.core.cache import cache

# Clear all cache
cache.clear()
print("Cache cleared")

# Or specific keys
cache.delete('socialaccount:apps')
print("SocialAccount cache cleared")
```

---

## Testing the Fix

### 1. Test OAuth Flow in Django Shell

```bash
python manage.py shell
```

```python
from allauth.socialaccount.models import SocialApp
from django.contrib.sites.models import Site

# This is what fails in the error
site = Site.objects.get(id=1)
google_apps = SocialApp.objects.filter(sites=site, provider='google')
print(f"Google apps: {google_apps.count()}")
assert google_apps.count() == 1, "Should have exactly 1 Google app!"

github_apps = SocialApp.objects.filter(sites=site, provider='github')
print(f"GitHub apps: {github_apps.count()}")
assert github_apps.count() == 1, "Should have exactly 1 GitHub app!"

print("SUCCESS: OAuth configuration is valid!")
```

### 2. Test in Browser

1. Clear browser cache & cookies
2. Navigate to: `http://localhost:8000/accounts/login/`
3. Click "Login with Google"
4. Should redirect to Google OAuth page

### 3. Check Logs

```bash
# On Windows
type logs/django.log | findstr "oauth"
type logs/django.log | findstr "google"

# On macOS/Linux
tail -100 logs/django.log | grep -i oauth
tail -100 logs/django.log | grep -i google
```

---

## Environment-Specific Notes

### Development (localhost:8000)

- OAuth redirect URI should be:
  - Google: `http://localhost:8000/accounts/google/login/callback/`
  - GitHub: `http://localhost:8000/accounts/github/login/callback/`

### Production (yourdomain.com)

- OAuth redirect URI should be:
  - Google: `https://yourdomain.com/accounts/google/login/callback/`
  - GitHub: `https://yourdomain.com/accounts/github/login/callback/`

- Update Django Site:
  ```bash
  python manage.py shell
  ```
  
  ```python
  from django.contrib.sites.models import Site
  site = Site.objects.get(id=1)
  site.domain = 'yourdomain.com'
  site.save()
  ```

---

## Prevention Tips

1. **Use only placeholder credentials in development**
   - Don't use real OAuth credentials for localhost testing

2. **Never run migrations in parallel**
   - Ensures SITE_ID stays consistent

3. **Always verify SocialApp count**
   ```bash
   python manage.py shell -c "from allauth.socialaccount.models import SocialApp; print(f'Google: {SocialApp.objects.filter(provider=\"google\").count()}, GitHub: {SocialApp.objects.filter(provider=\"github\").count()}')"
   ```

4. **Backup before production migration**
   ```bash
   python manage.py dumpdata > backup.json
   ```

---

## Quick Reference

| Issue | Solution |
|-------|----------|
| MultipleObjectsReturned on OAuth login | Run `fix_duplicate_oauth.py` |
| OAuth app not found | Verify Site domain matches |
| OAuth credentials invalid | Update SocialApp with real credentials |
| Cache contains stale data | Run `cache.clear()` |
| Site domain mismatch | Update via Django shell or admin panel |

---

**Status**: Ready to test  
**Last Updated**: 2026-02-08
