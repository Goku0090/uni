# Quick Fix: OAuth MultipleObjectsReturned Error

## Issue
When clicking "Login with Google" or "Login with GitHub", you get:
```
django.core.exceptions.MultipleObjectsReturned
```

## Root Cause
The `allauth` adapter is trying to find a SocialApp (OAuth configuration) and either:
1. Found multiple apps for the same provider, OR
2. The adapter is being called without a request object (missing context)

## Quick Fix (5 minutes)

### Run This:
```bash
cd auth_project
python manage.py shell
```

### Then Execute:
```python
# Option 1: Reset all OAuth apps completely
from allauth.socialaccount.models import SocialApp
from django.contrib.sites.models import Site

# Delete all
SocialApp.objects.all().delete()

# Get current site
site = Site.objects.get(id=1)

# Create fresh Google app  
google = SocialApp.objects.create(
    provider='google',
    name='Google',
    client_id='your-google-client-id',
    secret='your-google-client-secret'
)
google.sites.add(site)
print(f"Created Google app: ID={google.id}")

# Create fresh GitHub app
github = SocialApp.objects.create(
    provider='github',
    name='GitHub',
    client_id='your-github-client-id',
    secret='your-github-client-secret'
)
github.sites.add(site)
print(f"Created GitHub app: ID={github.id}")

exit()
```

### Then in browser:
1. Go to `http://localhost:8000/admin/socialaccount/socialapp/`
2. Click on Google app
3. Update `Client id` and `Client secret` with real values from Google Cloud Console
4. Same for GitHub app
5. Save

## Alternative: Clear and Test

```python
from django.core.cache import cache
from django.db import connection

# Clear cache
cache.clear()

# Verify count
from allauth.socialaccount.models import SocialApp
print(f"Google apps: {SocialApp.objects.filter(provider='google').count()}")
print(f"GitHub apps: {SocialApp.objects.filter(provider='github').count()}")

exit()
```

## Expected Result
- Should show exactly 1 Google app
- Should show exactly 1 GitHub app
- OAuth login should work

## If Still Failing

Check your settings:
```bash
python manage.py shell
```

```python
from django.conf import settings
from django.contrib.sites.models import Site

print(f"SITE_ID: {settings.SITE_ID}")
print(f"Current site: {Site.objects.get(id=settings.SITE_ID).domain}")

# Make sure SITE_ID matches database
exit()
```

## Last Resort: Reset Database

```bash
# Backup first!
python manage.py dumpdata > backup.json

# Reset
python manage.py migrate accounts zero
python manage.py migrate
python manage.py createsuperuser  # New admin user

# Recreate OAuth apps via script
python reset_oauth_config.py
```

---

**This should fix the error in < 5 minutes.**

If not, check your Django logs:
```bash
tail -50 logs/django.log
```
