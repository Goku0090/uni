# Google Login - Quick Fix (5 minutes)

## The Error You're Getting
```
Error: redirect_uri_mismatch
The redirect URI provided is not registered with the authorization server
```

## Why
The callback URL in Google Cloud Console **doesn't match** the URL your app is using.

---

## The Fix

### Step 1: Find Your Callback URL

**For localhost**:
```
http://localhost:8000/accounts/google/login/callback/
```

**For production domain**:
```
https://yourdomain.com/accounts/google/login/callback/
```

### Step 2: Add to Google Cloud Console

1. Go to [Google Cloud Console](https://console.cloud.google.com)
2. APIs & Services → Credentials
3. Click your OAuth 2.0 Client ID
4. Under "Authorized redirect URIs", click "ADD URI"
5. Paste your callback URL from Step 1
6. Click "SAVE"

### Step 3: Update .env File

Make sure your `.env` has:

```bash
GOOGLE_CLIENT_ID=your_client_id_from_google.apps.googleusercontent.com
GOOGLE_CLIENT_SECRET=your_client_secret_from_google
ALLOWED_HOSTS=localhost,127.0.0.1
```

(Or use your actual domain instead of localhost)

### Step 4: Restart Server

```bash
python manage.py runserver
```

### Step 5: Test

Visit: `http://localhost:8000/accounts/login/`

Click "Login with Google"

**Should work!** ✅

---

## Most Common Issues

| Issue | Solution |
|-------|----------|
| Using `127.0.0.1` but registered `localhost` | Add both to Google Cloud Console |
| Different port (8001 vs 8000) | Add exact port to Google Cloud Console |
| Missing trailing slash | Callback URL MUST end with `/` |
| Typo in Client ID/Secret | Copy-paste from Google Cloud Console |
| Forgot to click SAVE | Always click SAVE after adding URI |

---

## Exact Callback URL

The callback URL is **automatically generated** by django-allauth.

It will always be:
```
{your_domain}/accounts/google/login/callback/
```

You just need to register it in Google Cloud Console.

---

## Google Cloud Console: Step by Step

1. **Visit**: console.cloud.google.com
2. **Select your project** (top left dropdown)
3. **Go to**: APIs & Services (left sidebar)
4. **Click**: Credentials (left sidebar)
5. **Find**: "OAuth 2.0 Client IDs" section
6. **Click**: Your "Web client" entry
7. **Scroll down**: To "Authorized redirect URIs"
8. **Click**: "ADD URI" button
9. **Paste**: `http://localhost:8000/accounts/google/login/callback/`
10. **Click**: "SAVE" button (top right)
11. **Wait**: 30 seconds for changes to take effect

---

## If Still Not Working

**Clear Django Cache**:
```bash
cd e:/login/auth_project
python manage.py shell
>>> from django.core.cache import cache
>>> cache.clear()
>>> exit()
```

**Restart Server**:
```bash
python manage.py runserver
```

**Clear Browser Cache**:
- Press Ctrl+Shift+Delete
- Clear cookies and cache
- Try again

---

## Verify Your Credentials

**Check if credentials are correct**:
```bash
python manage.py shell
>>> import os
>>> print(os.getenv('GOOGLE_CLIENT_ID'))  # Should print your Client ID
>>> print(os.getenv('GOOGLE_CLIENT_SECRET'))  # Should print your Client Secret
```

If empty, update your `.env` file.

---

## That's It!

Most of the time, this fixes the issue:
1. Add callback URL to Google Cloud Console ✅
2. Update .env file ✅
3. Restart server ✅
4. Clear browser cache ✅
5. Test ✅

For more details, read: `GOOGLE_LOGIN_FIX.md`

