# OAuth Login Error - START HERE

## The Error You're Getting

```
Error 400: redirect_uri_mismatch
You can't sign in because this app sent an invalid request.
```

## What This Means

When you click "Sign in with Google/GitHub", your app sends a **redirect URL** that doesn't match what Google/GitHub expects.

It's like sending a package to address:
- ❌ App says: "123 Main St"  
- ❌ Google expects: "123 Main Street"
- ❌ Mismatch → Error

---

## The Fix (3 Steps - 10 Minutes)

### Step 1: Add Callback URL to Google (5 min)

1. Go to: https://console.cloud.google.com
2. Go to: **APIs & Services** → **Credentials**
3. Click your OAuth 2.0 Client ID
4. Scroll to **Authorized redirect URIs**
5. Add these **exactly** (with trailing slash):
   ```
   http://localhost:8000/accounts/google/login/callback/
   http://127.0.0.1:8000/accounts/google/login/callback/
   ```
6. Click **Save**

**Copy these values:**
- Client ID → Put in .env as `GOOGLE_CLIENT_ID`
- Client Secret → Put in .env as `GOOGLE_CLIENT_SECRET`

### Step 2: Add Callback URL to GitHub (3 min)

1. Go to: https://github.com/settings/developers
2. Click **OAuth Apps**
3. Click your app
4. Find **Authorization callback URL**
5. Set to **exactly**:
   ```
   http://localhost:8000/accounts/github/login/callback/
   ```
6. Click **Update application**

**Copy these values:**
- Client ID → Put in .env as `GITHUB_CLIENT_ID`
- Client Secret → Put in .env as `GITHUB_CLIENT_SECRET`

### Step 3: Update .env and Restart (2 min)

Update `.env` file:
```env
GOOGLE_CLIENT_ID=your_actual_id_here
GOOGLE_CLIENT_SECRET=your_actual_secret_here
GITHUB_CLIENT_ID=your_actual_id_here
GITHUB_CLIENT_SECRET=your_actual_secret_here
ALLOWED_HOSTS=localhost,127.0.0.1
```

Restart Django:
```bash
python manage.py runserver
```

Clear browser cookies and try logging in again.

---

## That's It!

You should now be able to:
- ✅ Click "Sign in with Google" → Works
- ✅ Click "Sign in with GitHub" → Works
- ✅ Get logged in successfully

---

## If Still Not Working

Read the detailed guide:
- **FIX_OAUTH_REDIRECT_URI_MISMATCH.md** - Full troubleshooting
- **OAUTH_SETUP_VISUAL_GUIDE.md** - Step-by-step with examples
- **OAUTH_QUICK_FIX_STEPS.txt** - Quick reference

---

## Key Points to Remember

✅ Exact URL must match (case-sensitive)
✅ Don't forget the trailing slash: `/callback/`
✅ Use `http://` not `https://` for local dev
✅ Use `localhost:8000` or `127.0.0.1:8000` with port
✅ Wait 5 minutes for OAuth settings to apply
✅ Clear browser cookies after changes
✅ Credentials must be in .env file

---

## Common Mistakes to Avoid

❌ Missing trailing slash
```
WRONG: /accounts/google/login/callback
RIGHT: /accounts/google/login/callback/
```

❌ Wrong protocol
```
WRONG: https://localhost:8000/...
RIGHT: http://localhost:8000/... (local dev)
```

❌ No port
```
WRONG: http://localhost/accounts/...
RIGHT: http://localhost:8000/accounts/...
```

❌ Empty credentials
```
WRONG: GOOGLE_CLIENT_ID=
RIGHT: GOOGLE_CLIENT_ID=123456789-abcdef...
```

---

## Exact Callback URLs

For local development (localhost:8000):
```
Google: http://localhost:8000/accounts/google/login/callback/
GitHub: http://localhost:8000/accounts/github/login/callback/
```

For production (Render):
```
Google: https://yourapp.onrender.com/accounts/google/login/callback/
GitHub: https://yourapp.onrender.com/accounts/github/login/callback/
```

---

## Files Created for Reference

1. **FIX_OAUTH_REDIRECT_URI_MISMATCH.md**
   - Complete troubleshooting guide
   - All common issues and solutions

2. **OAUTH_QUICK_FIX_STEPS.txt**
   - Fast reference checklist
   - Don't-do list

3. **OAUTH_SETUP_VISUAL_GUIDE.md**
   - Visual diagrams and examples
   - Step-by-step with screenshots

4. **START_HERE_OAUTH_FIX.md** (this file)
   - Quick start guide

---

## Status

✅ **FIXABLE** - Follow the 3 steps above and your OAuth login will work

Expected timeline: 10 minutes total
- Google setup: 5 min
- GitHub setup: 3 min
- Django restart: 2 min
- Testing: 1 min

Good luck! 🚀
