# OAuth Fix for 127.0.0.1:8000 Users

## Your Situation

You're accessing your app at:
```
http://127.0.0.1:8000/
```

This is different from:
```
http://localhost:8000/
```

Both are the same computer, but they're **different URLs** to OAuth providers!

---

## The Problem

You probably added only:
```
http://localhost:8000/accounts/google/login/callback/
http://localhost:8000/accounts/github/login/callback/
```

But you're using:
```
http://127.0.0.1:8000/accounts/google/login/callback/
http://127.0.0.1:8000/accounts/github/login/callback/
```

**They don't match → Error 400**

---

## The Fix (2 Options)

### Option A: Use Both (Recommended)

Add **BOTH** callback URLs to your OAuth settings:

#### Google Setup:
1. Go to: https://console.cloud.google.com/apis/credentials
2. Click your OAuth Client ID
3. Scroll to **Authorized redirect URIs**
4. Add ALL of these:
   ```
   http://localhost:8000/accounts/google/login/callback/
   http://127.0.0.1:8000/accounts/google/login/callback/
   http://localhost:8000/
   http://127.0.0.1:8000/
   ```
5. Click **Save**

#### GitHub Setup:
1. Go to: https://github.com/settings/developers
2. Click your OAuth App
3. Set **Authorization callback URL** to ONE of these:
   ```
   http://127.0.0.1:8000/accounts/github/login/callback/
   ```
4. Click **Update application**

**Note**: GitHub only allows ONE callback URL, so if you need both localhost and 127.0.0.1, you'll need TWO separate OAuth apps (one for each).

---

### Option B: Stick with One (Easier)

Pick ONE way to access your app and use only that:

#### If you prefer using 127.0.0.1:

**Google:**
```
http://127.0.0.1:8000/accounts/google/login/callback/
http://127.0.0.1:8000/accounts/github/login/callback/
```

**GitHub:**
```
http://127.0.0.1:8000/accounts/github/login/callback/
```

#### If you prefer using localhost:

Change your .env or browser bookmarks to use:
```
http://localhost:8000
```

Instead of:
```
http://127.0.0.1:8000
```

---

## Step-by-Step Fix for 127.0.0.1:8000

### Step 1: Update Google Settings (5 min)

1. Go to: https://console.cloud.google.com/apis/credentials
2. Click your OAuth 2.0 Client ID
3. Scroll down to **Authorized redirect URIs**
4. Click **Add URI**
5. Add: `http://127.0.0.1:8000/accounts/google/login/callback/`
6. If you also use localhost, add: `http://localhost:8000/accounts/google/login/callback/`
7. Click **Save**

### Step 2: Update GitHub Settings (3 min)

1. Go to: https://github.com/settings/developers
2. Click OAuth Apps
3. Click your app
4. Set **Authorization callback URL** to: `http://127.0.0.1:8000/accounts/github/login/callback/`
5. Click **Update application**

### Step 3: Update Django Site Configuration (2 min)

1. Go to: `http://127.0.0.1:8000/admin/`
2. Click **Sites** (under Django Admin)
3. Click the site (usually id=1)
4. Change **Domain name** to: `127.0.0.1:8000`
5. Click **Save**

### Step 4: Verify .env (1 min)

Make sure your `.env` has:
```env
GOOGLE_CLIENT_ID=your_actual_client_id
GOOGLE_CLIENT_SECRET=your_actual_secret
GITHUB_CLIENT_ID=your_actual_id
GITHUB_CLIENT_SECRET=your_actual_secret
```

### Step 5: Restart & Test (2 min)

```bash
# Restart Django
python manage.py runserver

# In browser:
# 1. Go to http://127.0.0.1:8000/accounts/login/
# 2. Click "Sign in with Google"
# 3. Should work now!
```

---

## Why This Matters

To OAuth providers (Google, GitHub), these are **completely different** domains:
- `localhost:8000` → localhost computer
- `127.0.0.1:8000` → 127.0.0.1 computer

Even though they point to the same machine!

So you must tell OAuth which one you're using.

---

## Complete Callback URLs for 127.0.0.1:8000

### Google
```
http://127.0.0.1:8000/accounts/google/login/callback/
```

### GitHub
```
http://127.0.0.1:8000/accounts/github/login/callback/
```

---

## Verification Checklist

- [ ] Google Console has `http://127.0.0.1:8000/accounts/google/login/callback/`
- [ ] GitHub settings has `http://127.0.0.1:8000/accounts/github/login/callback/`
- [ ] Django Site domain is set to `127.0.0.1:8000`
- [ ] .env has GOOGLE_CLIENT_ID and GOOGLE_CLIENT_SECRET
- [ ] .env has GITHUB_CLIENT_ID and GITHUB_CLIENT_SECRET
- [ ] Django restarted with `python manage.py runserver`
- [ ] Browser cookies cleared (Ctrl+Shift+Delete)
- [ ] Go to `http://127.0.0.1:8000/accounts/login/`
- [ ] Click "Sign in with Google" → Works
- [ ] Click "Sign in with GitHub" → Works

---

## If You Want to Use localhost Instead

Just remember:

1. **Change your browser**: Type `http://localhost:8000` instead of `http://127.0.0.1:8000`

2. **Keep OAuth URLs**: 
   ```
   http://localhost:8000/accounts/google/login/callback/
   http://localhost:8000/accounts/github/login/callback/
   ```

3. **Update Django Site**: 
   - Go to `/admin/sites/site/1/`
   - Change domain to `localhost:8000`

Both work exactly the same, it's just your preference!

---

## Why You Have This Error

Most people add `http://localhost:8000/...` to their OAuth settings but then access the app via `http://127.0.0.1:8000/...`

The OAuth provider says: "I only accept callbacks from `localhost`, not `127.0.0.1`"

Result: Error 400

**Solution**: Add `127.0.0.1` to your OAuth settings!

---

## Summary

Your current URL: `http://127.0.0.1:8000/`

Your callback URLs should be:
```
Google:  http://127.0.0.1:8000/accounts/google/login/callback/
GitHub:  http://127.0.0.1:8000/accounts/github/login/callback/
```

Add these to Google Console and GitHub settings, restart Django, and you're done!

**Expected time: 10 minutes**
