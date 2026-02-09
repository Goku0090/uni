# Fix: MultipleObjectsReturned Error at /login/

## Problem
```
MultipleObjectsReturned at /login/
No exception message supplied
```

**Root Cause**: Multiple OAuth (Social) Apps are configured in the database for the same provider (Google/GitHub).

---

## Quick Fix (2 minutes)

### Step 1: Run the Auto-Fix Script
```bash
cd auth_project
python cleanup_social_apps_now.py
```

**Expected Output:**
```
REMOVING DUPLICATE SOCIAL APPS - AUTO-FIX
Found 2 google apps
  🗑️  Deleting: ID=2, Name=...
  ✅ Kept: ID=1, Name=...
CLEANUP COMPLETE - Your login page should now work!
```

### Step 2: Test Login Page
```bash
python manage.py runserver
# Visit: http://127.0.0.1:8000/login/
```

✅ **Done!** Login page should work now.

---

## What's Happening

When you run setup scripts multiple times, it creates duplicate SocialApp entries:

```
Before (❌ Error):
├── Google App #1 (ID: 1)
├── Google App #2 (ID: 2)  ← DUPLICATE! Causes error
├── GitHub App #1 (ID: 3)
└── GitHub App #2 (ID: 4)  ← DUPLICATE! Causes error

After (✅ Fixed):
├── Google App #1 (ID: 1)  ← Kept
├── GitHub App #1 (ID: 3)  ← Kept
```

Django-allauth expects exactly **ONE app per provider**, but finds multiple, causing the error.

---

## Alternative Fix (Manual)

If the script doesn't work, use Django shell:

### Step 1: Open Django Shell
```bash
python manage.py shell
```

### Step 2: List All Apps
```python
from allauth.socialaccount.models import SocialApp

for app in SocialApp.objects.all():
    print(f"ID: {app.id}, Provider: {app.provider}, Name: {app.name}")
```

**Example Output:**
```
ID: 1, Provider: google, Name: UniSinq Google Dev
ID: 2, Provider: google, Name: UniSinq Local
ID: 3, Provider: github, Name: UniSinq GitHub
```

### Step 3: Delete Duplicates
```python
# Delete the duplicate Google app
SocialApp.objects.get(id=2).delete()  # Delete "UniSinq Local"
print("✅ Deleted duplicate Google app")

# If you have duplicate GitHub too:
SocialApp.objects.get(id=4).delete()
print("✅ Deleted duplicate GitHub app")
```

### Step 4: Verify
```python
SocialApp.objects.all().count()  # Should be 2 (one Google, one GitHub)
```

---

## Complete SQL View

### Step 1: Check Database
```bash
python manage.py dbshell
```

### Step 2: Run SQL Query
```sql
SELECT id, provider, name, client_id FROM socialaccount_socialapp;
```

**Example Output:**
```
id | provider |      name       |    client_id
---+----------+-----------------+----------------
 1 | google   | UniSinq Google  | abc123def456...
 2 | google   | Google Local    | xyz789uvw123...
 3 | github   | UniSinq GitHub  | ghi456jkl789...
 4 | github   | GitHub Dev      | mno012pqr345...
```

### Step 3: Delete Using SQL
```sql
-- Delete duplicate Google app (keep ID 1)
DELETE FROM socialaccount_socialapp WHERE id = 2;

-- Delete duplicate GitHub app (keep ID 3)
DELETE FROM socialaccount_socialapp WHERE id = 4;
```

---

## Why This Happens

1. You ran `setup_social_apps.py` multiple times
2. Each run creates new SocialApp entries instead of updating existing ones
3. Django-allauth queries get confused with multiple apps

---

## Prevention

### Option 1: Use the Cleanup Script
- Run `cleanup_social_apps_now.py` after running any setup scripts
- Automatically removes duplicates

### Option 2: Better Setup Script
```python
# Instead of always creating new apps:
app, created = SocialApp.objects.get_or_create(
    provider='google',
    defaults={
        'name': 'Google',
        'client_id': 'your-client-id',
        'secret': 'your-secret',
    }
)
# Only updates if it already exists
```

---

## Testing the Fix

### Test 1: Login Page Loads
```bash
python manage.py runserver
# Visit: http://127.0.0.1:8000/login/
# Should NOT show error
```

### Test 2: No Database Errors
```python
from allauth.socialaccount.models import SocialApp
SocialApp.objects.all().count()  # Should be 2
```

### Test 3: OAuth Links Work
On login page, check:
- Google button appears ✅
- GitHub button appears ✅
- Links are clickable ✅

---

## Verify Correct Configuration

### Step 1: Check Current Apps
```bash
cd auth_project
python manage.py shell
```

### Step 2: List Apps
```python
from allauth.socialaccount.models import SocialApp

google = SocialApp.objects.get(provider='google')
print(f"Google: {google.name}, Client ID: {google.client_id[:20]}")

github = SocialApp.objects.get(provider='github')
print(f"GitHub: {github.name}, Client ID: {github.client_id[:20]}")
```

### Step 3: Expected Output
```
Google: UniSinq Google, Client ID: abc123def456...
GitHub: UniSinq GitHub, Client ID: xyz789uvw123...
```

---

## Common Issues & Solutions

### Issue: Script Says "No duplicates" but still get error
**Solution**: 
```bash
python manage.py migrate
python manage.py runserver
# Restart server
```

### Issue: Can't connect to database
**Solution**:
```bash
# Check if database file exists
ls auth_project/db.sqlite3

# If using PostgreSQL:
# Check connection in settings.py
```

### Issue: Still getting MultipleObjectsReturned
**Solution**:
```python
# Delete ALL social apps and reconfigure
from allauth.socialaccount.models import SocialApp
SocialApp.objects.all().delete()

# Then run setup again
# Or use Django admin to create fresh apps
```

---

## Django Admin Alternative

### Step 1: Create Superuser (if needed)
```bash
python manage.py createsuperuser
```

### Step 2: Go to Admin
```
http://127.0.0.1:8000/admin/
```

### Step 3: Navigate to Social Applications
```
Admin Panel → Social Applications
```

### Step 4: Delete Duplicates
- Click each duplicate app
- Click "Delete"
- Confirm

---

## Summary

| Method | Time | Difficulty | Best For |
|--------|------|------------|----------|
| Auto-fix Script | 1 min | Easy | Everyone |
| Django Shell | 3 min | Medium | Developers |
| SQL Query | 2 min | Medium | DB Admins |
| Django Admin | 5 min | Easy | Non-technical |

---

## Final Checklist

After running fix:
- [ ] No error on /login/ page
- [ ] Google login button visible
- [ ] GitHub login button visible
- [ ] Database has only 1 Google app
- [ ] Database has only 1 GitHub app
- [ ] Can see app details in Django admin

---

## Files Provided

1. **cleanup_social_apps_now.py** - Auto-fix script (RECOMMENDED)
2. **fix_duplicate_social_apps.py** - Detailed diagnosis script

---

## Need Help?

Check the detailed diagnostic:
```bash
python fix_duplicate_social_apps.py
```

This will show:
- All apps currently in database
- Which providers have duplicates
- Manual deletion commands

---

**Status**: 🔧 Ready to Fix  
**Time to Fix**: < 5 minutes  
**Difficulty**: Easy  

**Next Step**: Run `python cleanup_social_apps_now.py`
