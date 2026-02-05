# OAuth Setup - Visual Guide

## The Problem in Simple Terms

Your app says: "Send me to `http://localhost:8000/callback/`"
But Google/GitHub are looking for: "Send me to `http://localhost:8000/auth/callback/`"

They don't match → ERROR

---

## Google OAuth Setup

### Finding the Right Place

```
Step 1: Go to https://console.cloud.google.com
         ↓
Step 2: Click your project name (top left)
         ↓
Step 3: Navigate to "APIs & Services"
         ↓
Step 4: Click "Credentials" in left menu
         ↓
Step 5: You should see a table with OAuth 2.0 Client IDs
         ↓
Step 6: Click on your app (type should be "Web application")
```

### What You'll See

```
┌─────────────────────────────────────────────────────────────┐
│ OAuth 2.0 Client ID Details                                 │
├─────────────────────────────────────────────────────────────┤
│ Client ID: 123456789-abcdefg.apps.googleusercontent.com    │
│ Client Secret: GOCSPX-xxxxxxxxxxxxxxxxxxxxx                │
│                                                             │
│ Authorized JavaScript origins:                              │
│  • http://localhost:8000                                    │
│                                                             │
│ Authorized redirect URIs:                                   │
│  • http://localhost:8000/accounts/google/login/callback/   │ ← ADD THIS
│  • http://127.0.0.1:8000/accounts/google/login/callback/  │ ← AND THIS
│                                                             │
│ [Edit] [Delete]                                             │
└─────────────────────────────────────────────────────────────┘
```

### Action Items

```
1. Scroll down to "Authorized redirect URIs" section
   
2. Click "Add URI" button
   
3. Type exactly:
   http://localhost:8000/accounts/google/login/callback/
   
4. Click "Add URI" button again
   
5. Type exactly:
   http://127.0.0.1:8000/accounts/google/login/callback/
   
6. Click "Save" button at bottom
   
7. Wait 5 minutes for changes to apply
```

---

## GitHub OAuth Setup

### Finding the Right Place

```
Step 1: Go to https://github.com/settings/developers
         ↓
Step 2: Click "OAuth Apps" (or "GitHub Apps" if you have that)
         ↓
Step 3: Click on your app
         ↓
Step 4: You'll see app details page
```

### What You'll See

```
┌─────────────────────────────────────────────────────────────┐
│ My Application                                              │
├─────────────────────────────────────────────────────────────┤
│ Application name: UniSync                                   │
│ Homepage URL: http://localhost:8000                         │
│ Application description: (optional)                         │
│ Authorization callback URL:                                 │
│ http://localhost:8000/accounts/github/login/callback/      │ ← SET THIS
│                                                             │
│ Client ID: abcd1234efgh5678                                │
│ Client Secret: (hidden - click to reveal) ghij9012klmn3456 │
│                                                             │
│ [Edit] [Delete] [Reset client secret]                       │
└─────────────────────────────────────────────────────────────┘
```

### Action Items

```
1. Find "Authorization callback URL" field
   
2. Set it to exactly:
   http://localhost:8000/accounts/github/login/callback/
   
3. Scroll down and click "Update application"
   
4. Wait a moment for changes to apply
```

---

## Django Admin - Site Configuration

### Finding the Right Place

```
Step 1: Go to http://localhost:8000/admin/
         ↓
Step 2: Log in with superuser account
         ↓
Step 3: Scroll down to "Sites" section
         ↓
Step 4: Click on "Sites"
         ↓
Step 5: Click on the one site listed (usually id=1)
```

### What You'll See

```
┌─────────────────────────────────────────────────────────────┐
│ Site Object                                                 │
├─────────────────────────────────────────────────────────────┤
│ Domain name: *                                              │ ← SET THIS
│ Display name: example.com                                   │
│                                                             │
│ [Save]                                                      │
└─────────────────────────────────────────────────────────────┘
```

### Action Items

```
1. Click in "Domain name" field
   
2. Change to: localhost:8000
   
3. Click "Save" button
   
4. Done! Django will use this domain for OAuth callbacks
```

---

## .env File Configuration

### What to Add

```env
# Google OAuth Credentials
GOOGLE_CLIENT_ID=123456789-abcdefghijklmnop.apps.googleusercontent.com
GOOGLE_CLIENT_SECRET=GOCSPX-xxxxxxxxxxxxxxxxxxxxxxxxxx

# GitHub OAuth Credentials  
GITHUB_CLIENT_ID=abc123def456
GITHUB_CLIENT_SECRET=ghijk789lmnop012qrst345uvwx678

# Also important
ALLOWED_HOSTS=localhost,127.0.0.1
DEBUG=True
```

### Where to Find Each Value

**Google:**
1. Go to https://console.cloud.google.com/apis/credentials
2. Click your OAuth Client ID
3. Copy "Client ID" → GOOGLE_CLIENT_ID
4. Copy "Client Secret" → GOOGLE_CLIENT_SECRET

**GitHub:**
1. Go to https://github.com/settings/developers
2. Click "OAuth Apps"
3. Click your app
4. Copy "Client ID" → GITHUB_CLIENT_ID
5. Click "Generate a new client secret"
6. Copy it → GITHUB_CLIENT_SECRET

---

## The OAuth Flow Explained

### What Happens When You Click "Sign in with Google"

```
Your App (Django)           Browser                Google
    │                          │                      │
    ├──> Create signin URL ────┤                      │
    │      with callback_uri    │                      │
    │                           │                      │
    │     [User clicks button]  │                      │
    │                           ├─ Go to Google ──────>│
    │                           │ (with callback URL)  │
    │                           │                      │
    │                           │<─ Google checks ─────┤
    │                           │    callback URL      │
    │                           │    matches config?   │
    │                           │                      │
    │ NO MATCH? ◄────────────────────── ERROR 400 ────┤
    │                           │                      │
    │ MATCH? ◄────────────────────────── Auth Page ───┤
    │                           │ [Sign in with Google]│
    │                           │                      │
    │                           │<─ User approves ─────┤
    │                           │                      │
    │<────────── Redirect back with code ─────────────│
    │      (to callback_uri)     │                      │
    │                            │                      │
    ├──> Verify code with Google                       │
    │                                                   │
    ├──> Create user session                           │
    │                                                   │
    └──> Redirect to dashboard                         │
```

**The Critical Point:** The callback URL must match EXACTLY or you get Error 400!

---

## Complete Setup Checklist

### Google Cloud Console

- [ ] Have Google account and project created
- [ ] OAuth 2.0 Client ID created (type: Web application)
- [ ] Authorized JavaScript origins includes `http://localhost:8000`
- [ ] Authorized redirect URIs includes:
  - [ ] `http://localhost:8000/accounts/google/login/callback/`
  - [ ] `http://127.0.0.1:8000/accounts/google/login/callback/`
- [ ] Client ID copied to .env as GOOGLE_CLIENT_ID
- [ ] Client Secret copied to .env as GOOGLE_CLIENT_SECRET
- [ ] Settings saved
- [ ] Waited 5 minutes for propagation

### GitHub Developer Settings

- [ ] OAuth App created
- [ ] Homepage URL set to `http://localhost:8000`
- [ ] Authorization callback URL set to:
  - [ ] `http://localhost:8000/accounts/github/login/callback/`
- [ ] Client ID copied to .env as GITHUB_CLIENT_ID
- [ ] Client Secret copied to .env as GITHUB_CLIENT_SECRET
- [ ] Settings updated

### Django Configuration

- [ ] .env file has GOOGLE_CLIENT_ID and GOOGLE_CLIENT_SECRET
- [ ] .env file has GITHUB_CLIENT_ID and GITHUB_CLIENT_SECRET
- [ ] ALLOWED_HOSTS includes localhost,127.0.0.1
- [ ] Django Admin Sites domain set to `localhost:8000`
- [ ] Django restarted: `python manage.py runserver`
- [ ] Browser cache cleared

### Testing

- [ ] Go to login page
- [ ] Click "Sign in with Google"
- [ ] Successfully authenticate and redirect to app
- [ ] Click "Sign in with GitHub"  
- [ ] Successfully authenticate and redirect to app

---

## URL References

| What | URL |
|------|-----|
| Google Cloud Console | https://console.cloud.google.com |
| Google Credentials | https://console.cloud.google.com/apis/credentials |
| GitHub Developer Settings | https://github.com/settings/developers |
| GitHub OAuth Apps | https://github.com/settings/developers/oauth-apps |
| Django Admin | http://localhost:8000/admin/ |
| Django Admin Sites | http://localhost:8000/admin/sites/site/1/ |
| Django Login | http://localhost:8000/accounts/login/ |

---

## Exact Callback URLs for UniSync

Your Django app uses django-allauth, which generates these exact URLs:

```
/accounts/google/login/callback/
/accounts/github/login/callback/
```

So the full URLs are:
- Local: `http://localhost:8000/accounts/google/login/callback/`
- Local: `http://localhost:8000/accounts/github/login/callback/`
- Production: `https://yourapp.onrender.com/accounts/google/login/callback/`
- Production: `https://yourapp.onrender.com/accounts/github/login/callback/`

---

## Common Issues & Solutions

### Issue: "Client ID is empty"
**Solution**: Check .env file has GOOGLE_CLIENT_ID and GITHUB_CLIENT_ID set

### Issue: "Still getting Error 400 after changes"
**Solution**: 
1. Wait 5 minutes
2. Clear browser cookies (Ctrl+Shift+Delete)
3. Verify callback URL matches exactly (case-sensitive, trailing slash, protocol)

### Issue: "Wrong client secret"
**Solution**: 
1. Go to Google Cloud / GitHub
2. Generate new secret / copy current secret
3. Paste exactly into .env
4. Restart Django

### Issue: "Can't access Django admin"
**Solution**: You need a superuser account
```bash
python manage.py createsuperuser
```

### Issue: "Settings won't save"
**Solution**:
1. Make sure you're clicking "Save" button
2. Wait for page to reload
3. Refresh to confirm changes saved

---

## Testing the Fix

### Quick Test
```bash
1. Restart Django: python manage.py runserver
2. Go to http://localhost:8000/accounts/login/
3. Click "Sign in with Google"
4. Should see Google login screen (not Error 400)
5. Sign in successfully
6. Should redirect to dashboard
```

### Verification
```bash
python manage.py shell
import os
print("Google ID:", os.getenv('GOOGLE_CLIENT_ID'))
print("GitHub ID:", os.getenv('GITHUB_CLIENT_ID'))

from django.contrib.sites.models import Site
print("Django site domain:", Site.objects.first().domain)
```

Both should show actual values, not empty.

---

## Success Indicators

✅ Google login page appears (not error)
✅ GitHub login page appears (not error)
✅ User successfully authenticates
✅ User redirected to dashboard
✅ No Error 400 messages
✅ No "redirect_uri_mismatch" errors

---

## Summary

The OAuth error happens because:
1. You define a callback URL in your app
2. You define a callback URL in Google/GitHub settings
3. They must match exactly
4. If they don't, you get Error 400

To fix:
1. Know your callback URL format
2. Add it to Google Cloud Console
3. Add it to GitHub settings
4. Add credentials to .env
5. Restart Django
6. Test

Good luck! 🚀
