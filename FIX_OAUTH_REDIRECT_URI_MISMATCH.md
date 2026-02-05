# Fix OAuth Redirect URI Mismatch Error

## Error Message
```
Error 400: redirect_uri_mismatch
You can't sign in because this app sent an invalid request.
```

## What This Means

The redirect URI your Django app is sending **does not match** what's configured in:
- Google Developer Console, OR
- GitHub Developer Settings

---

## Root Cause

When you click "Sign in with Google/GitHub", the app constructs a redirect URI like:
```
https://yourdomain.com/accounts/google/login/callback/
```

But the OAuth provider (Google/GitHub) expects:
```
http://localhost:8000/accounts/google/login/callback/
```

If these don't match exactly, you get the error.

---

## Step 1: Identify Your Current URL

### Local Development
What's your current URL?
- `http://localhost:8000` - Local
- `http://127.0.0.1:8000` - Local with IP
- `http://yourdomain.com` - Production
- `https://yourdomain.com` - Production with SSL

### Production
If deployed to Render/Railway:
- `https://yourapp.onrender.com` - Render
- `https://yourapp.railway.app` - Railway

---

## Step 2: Find What's Configured in OAuth Provider

### For Google
1. Go to **Google Cloud Console** → https://console.cloud.google.com
2. Find your project
3. Go to **APIs & Services** → **Credentials**
4. Find your OAuth 2.0 Client ID
5. Click to edit
6. Check **Authorized redirect URIs**

**Example (what you should see):**
```
http://localhost:8000/accounts/google/login/callback/
```

### For GitHub
1. Go to **GitHub Settings** → https://github.com/settings/developers
2. Find your OAuth App
3. Look for **Authorization callback URL**

**Example (what you should see):**
```
http://localhost:8000/accounts/google/login/callback/
```

---

## Step 3: Add Missing Redirect URIs

### If Running Locally (localhost:8000)

**Google:**
1. Go to Google Cloud Console
2. Go to Credentials
3. Click on your OAuth Client ID
4. Add these URIs under **Authorized redirect URIs**:
   ```
   http://localhost:8000/accounts/google/login/callback/
   http://127.0.0.1:8000/accounts/google/login/callback/
   ```
5. Click **Save**

**GitHub:**
1. Go to GitHub Settings → Developer settings → OAuth Apps
2. Click on your app
3. Set **Authorization callback URL** to:
   ```
   http://localhost:8000/accounts/github/login/callback/
   ```
4. Click **Update application**

### If Running on Production (Render/Railway)

**Google:**
Add both:
```
https://yourapp.onrender.com/accounts/google/login/callback/
http://yourapp.onrender.com/accounts/google/login/callback/
```

**GitHub:**
```
https://yourapp.onrender.com/accounts/github/login/callback/
```

---

## Step 4: Check Django Configuration

### In `.env` file:

Make sure you have:
```env
GOOGLE_CLIENT_ID=your_client_id_here
GOOGLE_CLIENT_SECRET=your_client_secret_here
GITHUB_CLIENT_ID=your_github_app_id
GITHUB_CLIENT_SECRET=your_github_app_secret
```

### In `settings.py` (lines 273-291):

This should already be configured:
```python
SOCIALACCOUNT_PROVIDERS = {
    'google': {
        'SCOPE': ['profile', 'email'],
        'AUTH_PARAMS': {'access_type': 'online'},
        'APP': {
            'client_id': os.getenv('GOOGLE_CLIENT_ID', ''),
            'secret': os.getenv('GOOGLE_CLIENT_SECRET', ''),
            'name': 'Google'
        }
    },
    'github': {
        'SCOPE': ['user:email', 'read:user'],
        'APP': {
            'client_id': os.getenv('GITHUB_CLIENT_ID', ''),
            'secret': os.getenv('GITHUB_CLIENT_SECRET', ''),
            'name': 'GitHub'
        }
    }
}
```

---

## Step 5: Check ALLOWED_HOSTS

In `settings.py` (line 28):
```python
ALLOWED_HOSTS = os.getenv('ALLOWED_HOSTS', 'localhost,127.0.0.1').split(',')
```

For local development, this is fine.

For production, add your domain:
```env
ALLOWED_HOSTS=yourapp.onrender.com,yourapp.railway.app,yourdomain.com
```

---

## Step 6: Check Site Configuration (Django Admin)

1. Go to Django Admin: `http://localhost:8000/admin/`
2. Go to **Sites**
3. Edit the default site
4. Change **Domain name** to match your actual domain:
   - Local: `localhost:8000`
   - Production: `yourapp.onrender.com`

This is important! Django uses this for generating callback URLs.

---

## Common Redirect URI Patterns

### Local Development
```
Google: http://localhost:8000/accounts/google/login/callback/
GitHub: http://localhost:8000/accounts/github/login/callback/
```

### Render Deployment
```
Google: https://yourapp.onrender.com/accounts/google/login/callback/
GitHub: https://yourapp.onrender.com/accounts/github/login/callback/
```

### Railway Deployment
```
Google: https://yourapp.railway.app/accounts/google/login/callback/
GitHub: https://yourapp.railway.app/accounts/github/login/callback/
```

### Custom Domain
```
Google: https://yourdomain.com/accounts/google/login/callback/
GitHub: https://yourdomain.com/accounts/github/login/callback/
```

---

## Quick Fix Checklist

### For Local Development

- [ ] **Google Console:**
  - [ ] Add `http://localhost:8000/accounts/google/login/callback/`
  - [ ] Add `http://127.0.0.1:8000/accounts/google/login/callback/`
  - [ ] Click Save

- [ ] **GitHub Settings:**
  - [ ] Set callback URL to `http://localhost:8000/accounts/github/login/callback/`
  - [ ] Click Update application

- [ ] **Django Admin:**
  - [ ] Go to `/admin/sites/site/1/`
  - [ ] Change domain to `localhost:8000`
  - [ ] Save

- [ ] **Django Server:**
  - [ ] Restart: `python manage.py runserver`
  - [ ] Clear browser cache
  - [ ] Try login again

### For Production (Render)

- [ ] **Google Console:**
  - [ ] Add `https://yourapp.onrender.com/accounts/google/login/callback/`
  - [ ] Add `http://yourapp.onrender.com/accounts/google/login/callback/`
  - [ ] Click Save

- [ ] **GitHub Settings:**
  - [ ] Set callback URL to `https://yourapp.onrender.com/accounts/github/login/callback/`
  - [ ] Click Update application

- [ ] **Django Admin:**
  - [ ] Go to `/admin/sites/site/1/`
  - [ ] Change domain to `yourapp.onrender.com`
  - [ ] Save

- [ ] **Environment Variables (in Render Dashboard):**
  - [ ] Set `GOOGLE_CLIENT_ID=xxxxx`
  - [ ] Set `GOOGLE_CLIENT_SECRET=xxxxx`
  - [ ] Set `GITHUB_CLIENT_ID=xxxxx`
  - [ ] Set `GITHUB_CLIENT_SECRET=xxxxx`
  - [ ] Set `ALLOWED_HOSTS=yourapp.onrender.com`
  - [ ] Redeploy

---

## Exact Steps for Google

### Step 1: Get Your Callback URL
Your app's callback URLs are:
```
http://localhost:8000/accounts/google/login/callback/
http://127.0.0.1:8000/accounts/google/login/callback/
```

### Step 2: Go to Google Cloud Console
1. Visit https://console.cloud.google.com
2. Select your project
3. Go to **APIs & Services** → **Credentials**
4. Click on your OAuth 2.0 Client ID (type: Web application)

### Step 3: Add Redirect URIs
1. Scroll down to **Authorized redirect URIs**
2. Click **Add URI**
3. Paste: `http://localhost:8000/accounts/google/login/callback/`
4. Click **Add URI** again
5. Paste: `http://127.0.0.1:8000/accounts/google/login/callback/`
6. Click **Save**

### Step 4: Get Credentials
1. Copy your **Client ID**
2. Copy your **Client Secret**
3. Add to `.env`:
   ```env
   GOOGLE_CLIENT_ID=your_client_id
   GOOGLE_CLIENT_SECRET=your_client_secret
   ```

### Step 5: Restart Django
```bash
python manage.py runserver
```

### Step 6: Test
1. Go to login page
2. Click "Sign in with Google"
3. Should work now!

---

## Exact Steps for GitHub

### Step 1: Get Your Callback URL
Your app's callback URL is:
```
http://localhost:8000/accounts/github/login/callback/
```

### Step 2: Go to GitHub Developer Settings
1. Visit https://github.com/settings/developers
2. Click **OAuth Apps**
3. Click on your app (or create new if doesn't exist)

### Step 3: Set Authorization Callback URL
1. Scroll down to **Authorization callback URL**
2. Set to: `http://localhost:8000/accounts/github/login/callback/`
3. Click **Update application**

### Step 4: Get Credentials
1. Copy **Client ID**
2. Copy **Client Secret**
3. Add to `.env`:
   ```env
   GITHUB_CLIENT_ID=your_client_id
   GITHUB_CLIENT_SECRET=your_client_secret
   ```

### Step 5: Restart Django
```bash
python manage.py runserver
```

### Step 6: Test
1. Go to login page
2. Click "Sign in with GitHub"
3. Should work now!

---

## Troubleshooting

### Still Getting Error?

**Check 1: Clear Django's Site Cache**
```bash
python manage.py shell
from django.contrib.sites.models import Site
Site.objects.all().delete()
Site.objects.create(domain='localhost:8000', name='LocalHost')
```

**Check 2: Verify Redirect URI Exactly**
Look at the URL bar when error occurs - it shows the redirect URI.
Compare with what's in OAuth provider settings - must match EXACTLY:
- ✅ `http://localhost:8000/accounts/google/login/callback/`
- ❌ `http://localhost:8000/accounts/google/login/callback` (missing slash)
- ❌ `http://localhost/accounts/google/login/callback/` (different port)
- ❌ `https://localhost:8000/accounts/google/login/callback/` (wrong protocol)

**Check 3: Verify Credentials**
```bash
python manage.py shell
import os
print("Google Client ID:", os.getenv('GOOGLE_CLIENT_ID'))
print("Google Secret:", os.getenv('GOOGLE_CLIENT_SECRET'))
print("GitHub Client ID:", os.getenv('GITHUB_CLIENT_ID'))
print("GitHub Secret:", os.getenv('GITHUB_CLIENT_SECRET'))
```

All should show values, not empty.

**Check 4: Verify ALLOWED_HOSTS**
```bash
python manage.py shell
from django.conf import settings
print("ALLOWED_HOSTS:", settings.ALLOWED_HOSTS)
```

Should include your domain.

---

## If Still Stuck

1. **Check browser console** (F12 → Console tab) for JavaScript errors
2. **Check Django logs** (`logs/django.log`) for backend errors
3. **Verify OAuth provider settings** are correctly saved
4. **Wait 5 minutes** - sometimes OAuth settings take time to propagate
5. **Clear browser cookies** - old session data might interfere
6. **Test in incognito mode** - avoids cache issues

---

## Summary

| Step | Action | Common Issue |
|------|--------|---------------|
| 1 | Get your callback URL | Don't know format |
| 2 | Add to Google/GitHub | Forgot trailing slash |
| 3 | Add credentials to `.env` | Wrong client_id/secret |
| 4 | Update Django Site | Domain mismatch |
| 5 | Restart Django | Cache not cleared |
| 6 | Test login | Still same error |

---

## URLs Reference

| Service | Settings URL |
|---------|--------------|
| Google | https://console.cloud.google.com/apis/credentials |
| GitHub | https://github.com/settings/developers |
| Django Admin Sites | http://localhost:8000/admin/sites/site/1/ |
| Django Debug | http://localhost:8000/accounts/debug/ (if enabled) |

---

## Important Notes

1. **Trailing slash matters**: `/callback/` not `/callback`
2. **Protocol matters**: `http://` vs `https://`
3. **Port matters**: `localhost:8000` vs `localhost:3000`
4. **Wait after changes**: OAuth settings can take 5-10 minutes to propagate
5. **Clear cookies**: Old session data might cause issues
6. **Credentials matter**: Wrong client_id/secret will fail

---

**Status**: Follow this guide and your OAuth login will work!
