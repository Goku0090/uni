# ⚡ QUICK FIX: Duplicate Social Apps (2 Minutes)

## What's Wrong
Login page shows 500 error: `MultipleObjectsReturned`

## What It Means
You have duplicate OAuth app configurations (2+ Google apps or 2+ GitHub apps)

## How to Fix (Choose ONE option)

---

## ✅ OPTION 1: Django Shell (EASIEST)

```bash
# In your project directory
python manage.py shell
```

Copy-paste this code:

```python
from allauth.socialaccount.models import SocialApp
from django.contrib.sites.models import Site

site = Site.objects.get_current()
print(f"Fixing duplicates on: {site.domain}\n")

for provider in ['google', 'github']:
    apps = SocialApp.objects.filter(provider=provider)
    count = apps.count()
    
    if count > 1:
        print(f"❌ Found {count} {provider} apps - removing duplicates")
        keep = apps.first()
        print(f"   ✓ Keeping: {keep.name} (ID: {keep.id})")
        
        for app in apps.exclude(id=keep.id):
            print(f"   ✗ Deleting: {app.name} (ID: {app.id})")
            app.delete()
        
        # Link to site
        if not keep.sites.filter(id=site.id).exists():
            keep.sites.add(site)
            print(f"   ✓ Linked to {site.domain}")
    elif count == 1:
        print(f"✓ {provider.capitalize()}: OK (1 app)")
    else:
        print(f"ℹ {provider.capitalize()}: Not configured (0 apps)")

print("\n✓ Done! Type: exit()")
```

Type `exit()` to quit shell.

---

## ✅ OPTION 2: Admin Panel

1. Go to: http://localhost:8000/admin/
2. Click: **Socialaccount → Social Applications**
3. Look for duplicate entries (e.g., multiple "Google")
4. **Keep the first one, DELETE the rest**
5. Refresh login page

---

## ✅ OPTION 3: SQL Command

Replace `google` with `github` if needed:

### SQLite:
```bash
python manage.py dbshell
```

```sql
DELETE FROM socialaccount_socialapp 
WHERE provider='google' 
AND id > (SELECT MIN(id) FROM socialaccount_socialapp WHERE provider='google');

DELETE FROM socialaccount_socialapp 
WHERE provider='github' 
AND id > (SELECT MIN(id) FROM socialaccount_socialapp WHERE provider='github');
```

### PostgreSQL:
Same commands as SQLite

---

## After Cleanup

```bash
# Stop server (Ctrl+C)
# Restart
python manage.py runserver
```

Visit: http://localhost:8000/login/

**Should see:**
- ✅ Page loads (no error)
- ✅ Email+OTP login form
- ✅ OAuth buttons (if configured)

---

## Verify It Worked

```bash
python manage.py shell
```

```python
from allauth.socialaccount.models import SocialApp

# Should show 0 or 1 of each
for app in SocialApp.objects.all():
    print(f"{app.provider}: {app.name}")

exit()
```

---

## Still Not Working?

Check logs:
```bash
tail -f logs/django.log
```

If you see new errors, post them in:
`MULTIPLEOBJECTSRETURNED_FIX.md` (full troubleshooting guide)

---

**Time**: 2 minutes  
**Risk**: Very low (just cleaning data)  
**Result**: Login page works ✅
