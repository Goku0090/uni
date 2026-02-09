# OAuth 500 Error - START HERE

## The Problem
When you try to login with Google or GitHub, you get:
```
GET http://127.0.0.1:8000/accounts/3rdparty/signup/ 500 (Internal Server Error)
```

Instead of being redirected to the OAuth provider's consent screen.

---

## The Solution - 3 Simple Steps

### Step 1: Run the Setup Script (1 minute)
```bash
cd auth_project
python setup_oauth_fixed.py
```

**You should see:**
```
[OK] Google OAuth UPDATED
[OK] GitHub OAuth CREATED
[SUCCESS] OAuth Setup Complete!
```

### Step 2: Add Your OAuth Credentials (10 minutes)
Update `auth_project/.env` file:

```ini
GOOGLE_OAUTH_CLIENT_ID=YOUR_GOOGLE_CLIENT_ID_HERE
GOOGLE_OAUTH_SECRET_KEY=YOUR_GOOGLE_SECRET_KEY_HERE
GITHUB_OAUTH_CLIENT_ID=YOUR_GITHUB_CLIENT_ID_HERE  
GITHUB_OAUTH_SECRET_KEY=YOUR_GITHUB_SECRET_KEY_HERE
```

**How to get these:**
- **Google:** https://console.cloud.google.com/ → Create OAuth 2.0 Credential
- **GitHub:** https://github.com/settings/developers → New OAuth App

### Step 3: Restart and Test (2 minutes)
```bash
python manage.py runserver
```

Go to: http://localhost:8000/login/
- Click "Login with Google" button
- Should show Google consent screen ✅
- NOT a 500 error!

---

## What Just Happened?

**Before:**
- OAuth configuration was missing from database
- Django-allauth couldn't find Google/GitHub settings
- Result: 500 error

**After:**
- OAuth configuration created in database
- Django-allauth finds credentials and redirects to Google/GitHub
- Result: Smooth OAuth login! ✅

---

## Documentation

Choose based on your needs:

| Document | Purpose | Read Time |
|----------|---------|-----------|
| **This file** | Quick overview | 2 min |
| `QUICK_FIX_OAUTH_500.txt` | Fast implementation | 5 min |
| `ACTION_FIX_OAUTH_NOW.txt` | Step-by-step with verification | 10 min |
| `OAUTH_ERROR_REFERENCE_CARD.txt` | Complete reference | 15 min |
| `OAUTH_500_ERROR_FIX.md` | Detailed technical guide | 20 min |
| `OAUTH_FIX_SUMMARY_2026.md` | Complete analysis | 30 min |

---

## Verification Checklist

After running the script, verify everything works:

- [ ] Setup script ran successfully
- [ ] `.env` has real OAuth credentials
- [ ] Server restarted
- [ ] Visit admin: http://localhost:8000/admin/socialaccount/socialapp/
  - [ ] See "Google" and "GitHub" apps listed
- [ ] Click "Login with Google" button
  - [ ] Redirected to Google consent screen (not 500 error!)
- [ ] Approve and test full OAuth flow
  - [ ] Auto-logged in to dashboard

---

## What Files Were Changed

**New Files:**
- `setup_oauth_fixed.py` - Automatic setup script

**Modified Files:**
- `accounts/signals_realtime.py` - Fixed encoding issue (line 271)

**Configuration:**
- `.env` - Added OAuth credentials

---

## Still Having Issues?

**Check these in order:**

1. **SocialApps exist in database?**
   ```bash
   python manage.py shell
   >>> from allauth.socialaccount.models import SocialApp
   >>> SocialApp.objects.count()  # Should be 2 or more
   ```

2. **Credentials in .env?**
   ```bash
   python manage.py shell
   >>> import os
   >>> os.getenv('GOOGLE_OAUTH_CLIENT_ID')  # Should print your Google ID
   ```

3. **Server restarted after .env changes?**
   - Kill runserver (Ctrl+C)
   - Start new instance: `python manage.py runserver`

4. **Redirect URLs match OAuth provider settings?**
   - Google: `http://localhost:8000/accounts/google/login/callback/`
   - GitHub: `http://localhost:8000/accounts/github/login/callback/`
   - Must be EXACT match!

5. **Check Django logs:**
   - Look at terminal output while running runserver
   - Look for error messages or tracebacks

---

## Production Deployment

When deploying to production (yourdomain.com):

1. Update Site domain:
   ```bash
   python manage.py shell
   >>> from django.contrib.sites.models import Site
   >>> site = Site.objects.get(id=1)
   >>> site.domain = 'yourdomain.com'
   >>> site.save()
   ```

2. Update OAuth redirect URLs in provider settings:
   - Google: `https://yourdomain.com/accounts/google/login/callback/`
   - GitHub: `https://yourdomain.com/accounts/github/login/callback/`

3. Get production OAuth credentials (different from dev)

4. Update `.env` on production server

5. Run script on production:
   ```bash
   python setup_oauth_fixed.py
   ```

6. Restart application

---

## Quick Reference

| Task | Command |
|------|---------|
| Run setup | `cd auth_project && python setup_oauth_fixed.py` |
| Check SocialApps | `python manage.py shell` then `from allauth.socialaccount.models import SocialApp; SocialApp.objects.all()` |
| Check Site | `python manage.py shell` then `from django.contrib.sites.models import Site; Site.objects.get(id=1)` |
| Start server | `python manage.py runserver` |
| Check credentials | `python manage.py shell` then `import os; os.getenv('GOOGLE_OAUTH_CLIENT_ID')` |

---

## Timeline

- **Setup script:** < 1 minute
- **Get credentials:** 10-20 minutes (depending on provider)
- **Update config:** 2 minutes
- **Restart & test:** 2 minutes

**Total: 15-25 minutes**

---

## Security Notes

✓ Credentials stored in `.env` (not in code)
✓ `.env` is in `.gitignore` (won't be committed)  
✓ Safe to share code publicly without exposing secrets
✓ Each environment has its own credentials (dev, staging, production)

---

## Next Steps

1. **Immediate:** Run `python setup_oauth_fixed.py`
2. **Soon:** Add OAuth credentials to `.env`
3. **Now:** Restart server and test
4. **Later:** Deploy to production with production credentials

---

## Support

- **Quick fix:** This file + `QUICK_FIX_OAUTH_500.txt`
- **Detailed guide:** `OAUTH_500_ERROR_FIX.md`
- **Reference:** `OAUTH_ERROR_REFERENCE_CARD.txt`
- **Complete analysis:** `OAUTH_FIX_SUMMARY_2026.md`

---

**Status:** ✅ OAuth error fixed and ready to deploy  
**Generated:** February 7, 2026  
**Version:** Final
