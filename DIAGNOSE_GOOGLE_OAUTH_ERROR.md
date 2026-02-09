# Diagnose: Google OAuth Login Error

**Status:** HTTP 200 received, but something fails after callback  
**Diagnosis Required:** What exactly goes wrong?

---

## What We Know

✅ **HTTP 200 Response** - OAuth callback received successfully twice
✅ **Code Parameter** - Authorization code from Google received  
✅ **Scope** - Email and profile data requested
✅ **State** - CSRF validation passed (state parameter matches)

❌ **Something Fails After** - Despite 200 status, user reports error

---

## What Likely Happened

1. **Callback received** (HTTP 200) ← Success here
2. **User data retrieved** from Google ← Probably OK
3. **Profile form shown** (CustomSocialSignupForm) ← Might fail here
4. **Profile saved** ← Or here
5. **Redirect to dashboard** ← Or here

---

## Diagnostic Steps

### Step 1: Check Browser Console (F12)

Open Developer Tools (F12) and go to **Console** tab.

**Look for:**
- Red error messages
- Network request failures
- JavaScript errors

**Screenshot what you see and share.**

---

### Step 2: Check Server Logs

**Look for errors in terminal/console where Django is running:**

```bash
# Common OAuth errors:
- "redirect_uri_mismatch"
- "invalid_client"
- "invalid_code"
- "User matching query does not exist"
- "IntegrityError"
- "ValidationError"
```

**Copy the error message from server console and share.**

---

### Step 3: Check What Page You're On

After clicking "Login with Google":
1. Does it show a **form** asking for additional info?
2. Does it **redirect to dashboard**?
3. Does it show an **error page**?
4. Does it **go back to login**?
5. Does it **stay blank/loading**?

**Tell me what happens.**

---

### Step 4: Check Database

```bash
python manage.py shell
from django.contrib.auth.models import User
from accounts.models import StudentProfile

# Check if user was created
print("Users:", User.objects.count())
users = User.objects.all()
for user in users:
    print(f"  - {user.username} (email: {user.email})")

# Check if profile was created
print("Profiles:", StudentProfile.objects.count())
```

**Tell me:**
- How many users exist?
- Is your Google account user there?
- Does that user have a profile?

---

## Most Common OAuth Issues

### Issue #1: Missing Environment Variables

**Check if you have these in `.env`:**
```
GOOGLE_CLIENT_ID=xxx.apps.googleusercontent.com
GOOGLE_CLIENT_SECRET=xxxxxxxxxxxxx
```

**If missing:**
```bash
# Go to Google Cloud Console
# Copy your credentials
# Add to .env file
# Restart Django
```

---

### Issue #2: Redirect URI Mismatch

**The error would show:**
```
Error: redirect_uri_mismatch
The redirect_uri parameter does not match the registered redirect_uri
```

**Fix:**
1. Go to [Google Cloud Console](https://console.cloud.google.com/)
2. Find your OAuth 2.0 credentials
3. Click edit
4. Make sure this is registered:
   ```
   http://127.0.0.1:8000/accounts/google/login/callback/
   ```
5. Save and try again

---

### Issue #3: Form Submission Error

**The error would be:**
- Form asking for full name but form validation fails
- Page shows form with error message

**Check:**
```bash
python manage.py shell
from accounts.forms import CustomSocialSignupForm

# Try to validate the form
form = CustomSocialSignupForm(data={'full_name': 'Test User'})
if not form.is_valid():
    print(form.errors)
```

---

### Issue #4: Profile Creation Error

**The error would be:**
- Form submits but nothing happens
- Page reloads blank or shows 500 error

**Check:**
```bash
# Look for IntegrityError or ValidationError in logs
tail -f logs/error.log
tail -f logs/django.log
```

---

### Issue #5: Redirect Configuration

**Check settings.py:**
```python
LOGIN_REDIRECT_URL = '/dashboard/'  # ← Should be here
ACCOUNT_LOGIN_ON_GET = True
SOCIALACCOUNT_AUTO_SIGNUP = True
```

**If wrong redirect is configured, user gets sent to wrong page.**

---

## Quick Diagnostic Checklist

- [ ] **Browser Console (F12)**
  - Any red errors shown?
  - What's the exact error message?
  
- [ ] **Server Console**
  - Any exception tracebacks?
  - What's the exact error message?
  
- [ ] **Current Page After Login**
  - Does it show a form?
  - Does it show an error?
  - Does it redirect somewhere?
  - Does it stay loading?
  
- [ ] **Database State**
  - Was user created?
  - Was profile created?
  - Check with Django shell
  
- [ ] **Environment Variables**
  - Is `.env` file correct?
  - Does it have GOOGLE_CLIENT_ID?
  - Does it have GOOGLE_CLIENT_SECRET?
  
- [ ] **Google Cloud Console**
  - Is redirect URI registered correctly?
  - Is callback URL exactly matching?

---

## What To Share With Me

Please provide:

1. **Exact error message from browser console (F12 → Console)**
   ```
   [Copy and paste any red text]
   ```

2. **Exact error message from server terminal**
   ```
   [Copy and paste any exceptions]
   ```

3. **What happens after Google redirects**
   - [ ] Shows form asking for info
   - [ ] Shows error message
   - [ ] Goes to dashboard
   - [ ] Goes back to login
   - [ ] Stays loading
   - [ ] Other: _______

4. **URL shown in browser address bar after callback**
   ```
   http://127.0.0.1:8000/xxxxx
   ```

5. **Screenshot of what you see** (if possible)

---

## Temporary Fix (If Urgent)

While we diagnose, you can login with email/password instead:

1. Go to `/register/` 
2. Create account with email
3. Verify OTP
4. Login with email/password

This bypasses OAuth entirely and lets you test the rest of the app.

---

## Related Files

If you want to review the OAuth setup:
- `settings.py` lines 279-298 (OAuth config)
- `forms.py` lines 533-584 (Signup form)
- `urls.py` lines 14-15 (Allauth URLs)

---

**Once you provide the above information, I can pinpoint the exact issue and fix it.**

What error do you see?
