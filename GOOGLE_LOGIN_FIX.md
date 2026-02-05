# Google Login - Redirect URI Mismatch Fix

## The Problem

You're seeing this error:
```
Error: redirect_uri_mismatch
The redirect URI provided does not match the one registered in Google Cloud Console
```

This happens because the callback URL your app is using doesn't match what you registered in Google Cloud Console.

---

## Root Cause Analysis

### What Google Expects
You registered certain redirect URIs in Google Cloud Console, like:
- `http://localhost:8000/accounts/google/login/callback/`
- `https://yourdomain.com/accounts/google/login/callback/`

### What Your App Sends
But your app might be trying to use:
- `http://127.0.0.1:8000/accounts/google/login/callback/`
- A different port
- A different domain

**They don't match** → Error!

---

## Step-by-Step Fix

### Step 1: Check Your Current Setup

**Your current configuration**:
- Framework: Django with django-allauth
- Provider: Google OAuth 2.0
- Callback pattern: `/accounts/google/login/callback/`

---

### Step 2: Get Your Current Redirect URI

Your app uses this format:

```
{PROTOCOL}://{DOMAIN}:{PORT}/accounts/google/login/callback/
```

**For localhost development**:
```
http://localhost:8000/accounts/google/login/callback/
```

**For your domain**:
```
https://yourdomain.com/accounts/google/login/callback/
```

---

### Step 3: Check Your Google Cloud Console

1. **Go to**: [Google Cloud Console](https://console.cloud.google.com)
2. **Select your project**
3. **Go to**: APIs & Services → Credentials
4. **Find your OAuth 2.0 Client ID** (named something like "Web client")
5. **Click it** to open the details
6. **Check the "Authorized redirect URIs"** section
7. **Note down** the exact URIs listed there

---

### Step 4: Update Google Cloud Console (If Needed)

**If your redirect URI is NOT in the list**, add it:

1. In Google Cloud Console → OAuth 2.0 Client ID details
2. Scroll to "Authorized redirect URIs"
3. Click "Add URI"
4. Enter the exact callback URL from Step 2
5. Click Save

**Example URIs to add** (choose which ones apply to you):

```
http://localhost:8000/accounts/google/login/callback/
http://127.0.0.1:8000/accounts/google/login/callback/
https://yourdomain.com/accounts/google/login/callback/
https://www.yourdomain.com/accounts/google/login/callback/
```

---

### Step 5: Verify Your .env File

Your `.env` file should have:

```bash
GOOGLE_CLIENT_ID=your_client_id_here.apps.googleusercontent.com
GOOGLE_CLIENT_SECRET=your_client_secret_here
ALLOWED_HOSTS=localhost,127.0.0.1,yourdomain.com
```

**Check that**:
- `GOOGLE_CLIENT_ID` matches Google Cloud Console
- `GOOGLE_CLIENT_SECRET` matches Google Cloud Console
- `ALLOWED_HOSTS` includes your domain

---

### Step 6: Clear Django Cache

Django caches social provider settings. Clear it:

```bash
cd e:/login/auth_project
python manage.py shell
>>> from django.core.cache import cache
>>> cache.clear()
>>> exit()
```

Or delete the database cache table:

```bash
python manage.py sqlclear socialaccount | python manage.py dbshell
```

---

### Step 7: Test

1. **Start server**:
   ```bash
   python manage.py runserver
   ```

2. **Visit login page**:
   ```
   http://localhost:8000/accounts/login/
   ```

3. **Click "Login with Google"**

4. **Should redirect to Google consent screen (not error)**

---

## Common Scenarios

### Scenario 1: Localhost Development

**You have**:
- Running on: `http://localhost:8000`
- Google redirect URI: `http://localhost:8000/accounts/google/login/callback/`

**To fix**:
1. Add to Google Cloud Console:
   - `http://localhost:8000/accounts/google/login/callback/`
   - `http://127.0.0.1:8000/accounts/google/login/callback/`
2. Update `.env`:
   ```
   ALLOWED_HOSTS=localhost,127.0.0.1
   ```

---

### Scenario 2: Production on Custom Domain

**You have**:
- Running on: `https://yourdomain.com`
- Need to add: `https://yourdomain.com/accounts/google/login/callback/`

**To fix**:
1. Add to Google Cloud Console:
   - `https://yourdomain.com/accounts/google/login/callback/`
   - `https://www.yourdomain.com/accounts/google/login/callback/` (if using www)
2. Update `.env`:
   ```
   ALLOWED_HOSTS=yourdomain.com,www.yourdomain.com
   ```

---

### Scenario 3: Render/Railway Deployment

**You have**:
- Running on: `https://your-app-random.onrender.com`
- Need to add: `https://your-app-random.onrender.com/accounts/google/login/callback/`

**To fix**:
1. Add to Google Cloud Console:
   - `https://your-app-random.onrender.com/accounts/google/login/callback/`
2. Update `.env` in Render/Railway:
   ```
   ALLOWED_HOSTS=your-app-random.onrender.com
   ```

---

## Detailed Steps: Google Cloud Console Setup

### Find Your OAuth Credentials

1. Go to [Google Cloud Console](https://console.cloud.google.com)
2. Click project dropdown (top left)
3. Select your project
4. Left sidebar → APIs & Services → Credentials
5. Under "OAuth 2.0 Client IDs", find your "Web client"
6. Click the pencil icon to edit

### Add Authorized Redirect URI

1. In the edit dialog, scroll to "Authorized redirect URIs"
2. Click "ADD URI"
3. Paste your callback URL
4. Click "SAVE"

**Example**:
```
http://localhost:8000/accounts/google/login/callback/
```

---

## Verify Callback URL Format

Your callback URL **MUST** be:
```
{your_app_url}/accounts/google/login/callback/
```

**✅ Correct**:
- `http://localhost:8000/accounts/google/login/callback/`
- `https://myapp.com/accounts/google/login/callback/`

**❌ Wrong**:
- `http://localhost:8000/accounts/google/callback/` (missing `login/`)
- `http://localhost:8000/google/login/callback/` (missing `accounts/`)
- `http://localhost:8000/accounts/googlelogin/callback/` (no slash)

---

## Django Settings Check

Your `settings.py` already has:

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
    }
}
```

This is correct. No changes needed here.

---

## Troubleshooting

### Error Still Appears?

**Step 1**: Verify you're using the EXACT callback URL
```bash
python manage.py shell
>>> from django.conf import settings
>>> print(settings.ALLOWED_HOSTS)
```

**Step 2**: Check Google Cloud Console credentials
- Copy-paste Client ID from Google
- Copy-paste Client Secret from Google
- Verify no extra spaces

**Step 3**: Restart Django server
```bash
python manage.py runserver
```

**Step 4**: Clear browser cache (Ctrl+Shift+Delete)

**Step 5**: Check database
```bash
python manage.py shell
>>> from django.contrib.sites.models import Site
>>> Site.objects.all()
```
Should show your domain.

---

## After Fix: Next Steps

1. **Test Google login**
   - Visit login page
   - Click "Login with Google"
   - Should show Google consent screen
   - Accept and redirect back to app

2. **Test signup flow**
   - New user login via Google
   - Should create account automatically

3. **Test existing user login**
   - Existing user login via Google
   - Should work without issues

---

## Reference: URL Patterns

Your app uses these URLs (defined in `accounts/urls.py`):

```python
path('login/', views.login_view, name='login'),
path('register/', views.register_view, name='register'),
path('accounts/', include('allauth.urls')),  # Includes Google callback
```

The Google callback is handled by django-allauth automatically at:
```
/accounts/google/login/callback/
```

---

## Still Having Issues?

### Check These:

1. **GOOGLE_CLIENT_ID** in .env
   - Should look like: `123456789.apps.googleusercontent.com`
   - Should match Google Cloud Console

2. **GOOGLE_CLIENT_SECRET** in .env
   - Should look like: `GOCSPX-xxxxxxxxxxxxx`
   - Should match Google Cloud Console

3. **Callback URL in Google Console**
   - Should be: `http://localhost:8000/accounts/google/login/callback/`
   - For production: `https://yourdomain.com/accounts/google/login/callback/`

4. **ALLOWED_HOSTS** in settings.py
   - Should include your domain
   - Should not include `/accounts/google/login/callback/`

---

## Quick Checklist

- [ ] Google OAuth credentials created in Cloud Console
- [ ] Client ID in .env as `GOOGLE_CLIENT_ID`
- [ ] Client Secret in .env as `GOOGLE_CLIENT_SECRET`
- [ ] Redirect URI added to Google Console (exact match to your callback URL)
- [ ] Domain added to ALLOWED_HOSTS in .env
- [ ] Django server restarted
- [ ] Browser cache cleared
- [ ] Test login attempt

---

## Example .env Setup for Development

```bash
# Google OAuth
GOOGLE_CLIENT_ID=1234567890.apps.googleusercontent.com
GOOGLE_CLIENT_SECRET=GOCSPX-abcdefghijklmnop

# Allowed domains
ALLOWED_HOSTS=localhost,127.0.0.1

# Other settings
DEBUG=True
SECRET_KEY=your-secret-key-here
```

---

## Example .env Setup for Production

```bash
# Google OAuth
GOOGLE_CLIENT_ID=1234567890.apps.googleusercontent.com
GOOGLE_CLIENT_SECRET=GOCSPX-abcdefghijklmnop

# Allowed domains
ALLOWED_HOSTS=yourdomain.com,www.yourdomain.com

# Other settings
DEBUG=False
SECRET_KEY=your-secret-key-here
SECURE_SSL_REDIRECT=True
```

---

## Need More Help?

If still not working:
1. Check Django error logs (console output)
2. Check browser console (F12 → Console)
3. Check Google OAuth error message carefully
4. Verify all credentials are copied exactly
5. Make sure you hit Save/Update in Google Console

