# Google OAuth - Troubleshooting Guide

## Error Diagnostic Flowchart

```
ERROR: "redirect_uri_mismatch"
           ↓
    Did you register the callback URL
    in Google Cloud Console?
           ↓
    ┌──────┴───────┐
    NO             YES
    ↓              ↓
ADD URI TO      Does the registered URL
GOOGLE         match YOUR callback URL?
CONSOLE             ↓
    ↓          ┌────┴────┐
   FIX      NO           YES
                ↓            ↓
            UPDATE IN    Is server
            GOOGLE      restarted?
            CONSOLE         ↓
                ↓        ┌───┴───┐
               FIX      NO       YES
                            ↓
                       RESTART
                       SERVER
                            ↓
                          FIX
```

---

## Error Messages & Fixes

### Error 1: "redirect_uri_mismatch"

```
Error: redirect_uri_mismatch
The redirect URI provided is not registered with the authorization server
```

**Causes**:
1. Callback URL not registered in Google Cloud Console
2. Callback URL has typo
3. Different port than registered (8001 vs 8000)
4. Using 127.0.0.1 but registered localhost

**Fix**:
1. Go to Google Cloud Console → Credentials
2. Click your OAuth 2.0 Client ID
3. Find "Authorized redirect URIs"
4. Add: `http://localhost:8000/accounts/google/login/callback/`
5. Click SAVE
6. Restart Django: `python manage.py runserver`

---

### Error 2: "invalid_client"

```
Error: invalid_client
The OAuth client was not found
```

**Causes**:
1. GOOGLE_CLIENT_ID in .env is wrong
2. Client doesn't exist in Google Cloud
3. Typo in Client ID

**Fix**:
1. Go to Google Cloud Console
2. APIs & Services → Credentials
3. Find and click your OAuth Client
4. Copy Client ID
5. Update .env: `GOOGLE_CLIENT_ID=<copied_id>`
6. Restart server

---

### Error 3: "invalid_client_secret"

```
Error: invalid_client_secret
The OAuth client secret provided is invalid
```

**Causes**:
1. GOOGLE_CLIENT_SECRET in .env is wrong
2. Extra spaces in secret
3. Copied wrong secret

**Fix**:
1. Go to Google Cloud Console → Credentials
2. Click your OAuth Client
3. Copy the Client Secret (exact copy, no spaces)
4. Update .env: `GOOGLE_CLIENT_SECRET=<copied_secret>`
5. Restart server

---

### Error 4: "access_denied"

```
Error: access_denied
The user denied access to the app
```

**Causes**:
1. User clicked "Cancel" or denied permission
2. User's Google account has restrictions

**Fix**:
- Normal behavior (user rejected access)
- Try again and grant permission
- Check if user can use OAuth apps in their Google settings

---

### Error 5: "server_error"

```
Error: server_error
The authorization server encountered an unexpected condition
```

**Causes**:
1. Temporary Google service issue
2. Invalid ALLOWED_HOSTS
3. Django error in callback processing

**Fix**:
1. Check ALLOWED_HOSTS in .env:
   ```
   ALLOWED_HOSTS=localhost,127.0.0.1
   ```
2. Restart server
3. Clear cache: `python manage.py shell` → `cache.clear()`
4. Wait and try again

---

### Error 6: "Login with Google" button not visible

**Causes**:
1. django-allauth not installed
2. Social providers not in INSTALLED_APPS
3. Template doesn't include Google button

**Fix**:
1. Check INSTALLED_APPS in settings.py:
   ```python
   'allauth.socialaccount.providers.google',
   ```

2. Check login template includes:
   ```html
   {% load socialaccount %}
   <a href="{% provider_login_url 'google' %}">Login with Google</a>
   ```

3. If template wrong, use a working template

---

### Error 7: After login, redirect loop or blank page

**Causes**:
1. LOGIN_REDIRECT_URL doesn't exist
2. Permission issue with redirect view
3. Social account not created properly

**Fix**:
1. Check LOGIN_REDIRECT_URL in settings:
   ```python
   LOGIN_REDIRECT_URL = '/dashboard/'
   ```

2. Verify `/dashboard/` view exists

3. Check console for errors during redirect

---

## Common Scenarios

### Scenario 1: Local Development Stopped Working

**What happened**:
- You changed port from 8000 to 8001
- Or switched between localhost and 127.0.0.1

**Fix**:
1. Go to Google Console
2. Check all registered URIs
3. Add missing combinations:
   - `http://localhost:8000/accounts/google/login/callback/`
   - `http://127.0.0.1:8000/accounts/google/login/callback/`

---

### Scenario 2: Project Moved to Different Domain

**What happened**:
- You deployed to domain but OAuth still points to localhost
- Or you changed domain

**Fix**:
1. Add new domain to ALLOWED_HOSTS in .env
2. Add callback URL for new domain to Google Console:
   ```
   https://yourdomain.com/accounts/google/login/callback/
   ```
3. Update GOOGLE_CLIENT_ID and GOOGLE_CLIENT_SECRET if different project

---

### Scenario 3: Multiple Domains (With & Without www)

**What happened**:
- www.yourdomain.com doesn't work but yourdomain.com does
- Or vice versa

**Fix**:
In Google Cloud Console, add both:
```
https://yourdomain.com/accounts/google/login/callback/
https://www.yourdomain.com/accounts/google/login/callback/
```

In .env:
```
ALLOWED_HOSTS=yourdomain.com,www.yourdomain.com
```

---

### Scenario 4: Using Custom Port (Not 8000)

**What happened**:
- Running on port 8001 but Google expects 8000

**Fix**:
1. In Google Cloud Console, register:
   ```
   http://localhost:8001/accounts/google/login/callback/
   http://127.0.0.1:8001/accounts/google/login/callback/
   ```

2. Run server on that port:
   ```bash
   python manage.py runserver 8001
   ```

---

## Debugging Steps

### Step 1: Enable Django Logging

Add to settings.py:
```python
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'handlers': {
        'console': {
            'class': 'logging.StreamHandler',
        },
    },
    'loggers': {
        'allauth': {
            'level': 'DEBUG',
            'handlers': ['console'],
        },
    },
}
```

Then run: `python manage.py runserver`

Check console output for allauth errors.

---

### Step 2: Check OAuth Credentials

```bash
python manage.py shell
>>> from django.conf import settings
>>> config = settings.SOCIALACCOUNT_PROVIDERS.get('google', {})
>>> print("Client ID:", config.get('APP', {}).get('client_id'))
>>> print("Secret:", config.get('APP', {}).get('secret'))
```

Should show your credentials (first few chars).

---

### Step 3: Verify Callback URL

Check what your app expects:
```python
# This is fixed in django-allauth:
/accounts/google/login/callback/

# Your full URL should be:
http://localhost:8000/accounts/google/login/callback/
```

This URL is **NOT configurable** - it's built into django-allauth.

---

### Step 4: Check Site Configuration

```bash
python manage.py shell
>>> from django.contrib.sites.models import Site
>>> Site.objects.all()
```

Should show:
```
Site(domain='localhost:8000', name='example.com')
# or
Site(domain='yourdomain.com', name='your site name')
```

The domain should match your ALLOWED_HOSTS.

---

### Step 5: Clear All Caches

```bash
python manage.py shell
>>> from django.core.cache import cache
>>> from django.views.decorators.cache import cache.clear_all()
>>> cache.clear()
>>> 
>>> # Or delete session files
>>> import os
>>> import shutil
>>> if os.path.exists('sessions'):
...     shutil.rmtree('sessions')
>>> exit()
```

Restart server.

---

## Chrome Developer Tools Debugging

### Step 1: Open DevTools
Press F12 in browser

### Step 2: Network Tab
- Click "Login with Google"
- Watch the network requests
- Look for:
  - Request to `accounts.google.com` (should see this)
  - Redirect back to your app (should return)
  - If error, response should contain error message

### Step 3: Console Tab
- Check for JavaScript errors
- Check for CORS errors
- django-allauth errors might appear here

### Step 4: Cookies
- Right-click → Inspect → Application → Cookies
- Check if session cookie was created
- Check domain and path

---

## Testing the Complete Flow

### Manual Test Steps

1. **Start fresh**
   ```bash
   python manage.py runserver
   ```

2. **Open in incognito window**
   - Fresh cookies
   - No cache interference

3. **Visit login page**
   ```
   http://localhost:8000/accounts/login/
   ```

4. **Verify button visible**
   - Look for "Login with Google" button
   - If missing, check template

5. **Click button**
   - Should redirect to Google
   - Watch address bar

6. **On Google page**
   - Login with test account
   - Check permissions requested (profile, email)

7. **Grant permission**
   - Click "Allow" or "Grant"

8. **Verify redirect**
   - Should redirect back to your app
   - Watch address bar for callbacks

9. **Check result**
   - Should be logged in
   - Should see dashboard or home
   - Or see error message

---

## Performance Check

If login is slow:

### Check 1: Network Speed
- Open DevTools → Network
- Check time for each request
- Google auth typically takes 2-5 seconds

### Check 2: Django Queries
- Enable query logging
- Check if creating user takes too long

### Check 3: Email Verification
- Your settings have `ACCOUNT_EMAIL_VERIFICATION = 'none'`
- So no email sending delay (good)

---

## Security Verification

✅ **Your configuration has**:
- CSRF protection enabled
- Secret stored in .env (not code)
- django-allauth handles OAuth flow safely
- ALLOWED_HOSTS configured

⚠️ **For production**:
- Use HTTPS (set SECURE_SSL_REDIRECT=True)
- Set DEBUG=False
- Use strong SECRET_KEY
- Update ALLOWED_HOSTS to your domain

---

## Still Stuck?

### Collect Information

1. **Error message** - Exact error text
2. **URL** - What URL you're trying to use
3. **Credentials** - Client ID format (just first few chars)
4. **Console output** - Full error traceback

### Check Basics

- [ ] GOOGLE_CLIENT_ID in .env
- [ ] GOOGLE_CLIENT_SECRET in .env
- [ ] Callback URL registered in Google
- [ ] Server restarted
- [ ] Browser cache cleared
- [ ] ALLOWED_HOSTS includes your domain

### Read Docs

- [django-allauth docs](https://django-allauth.readthedocs.io/)
- [Google OAuth docs](https://developers.google.com/identity/protocols/oauth2)

---

## Quick Summary

| Issue | Check | Fix |
|-------|-------|-----|
| redirect_uri_mismatch | Google Console | Add callback URL |
| invalid_client | .env | Copy Client ID |
| invalid_client_secret | .env | Copy Client Secret |
| Button not showing | Template | Include provider_login_url |
| After login redirect fails | settings.py | Set valid LOGIN_REDIRECT_URL |
| Slow | Network | Check response times |
| Redirect loop | Views | Verify dashboard exists |

