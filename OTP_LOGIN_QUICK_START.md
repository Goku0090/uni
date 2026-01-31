# OTP Login - Quick Start (5 Steps)

## Status: ✅ READY TO USE

The OTP login flow has been restored and is fully functional. Here's the fastest way to test it.

---

## 5-Minute Setup

### Step 1: Setup Database (1 minute)

```bash
cd e:/login/auth_project
python manage.py migrate
```

### Step 2: Create Test User (1 minute)

```bash
python manage.py shell
```

Paste this:
```python
from django.contrib.auth.models import User
from accounts.models import StudentProfile

User.objects.create_user(
    username='testuser',
    email='test@example.com',
    password='TestPassword123'
)

StudentProfile.objects.create(
    user=User.objects.get(username='testuser'),
    full_name='Test User',
    college='Test College'
)

exit()
```

### Step 3: Configure Email (1-3 minutes)

**Fastest Option: Use Console (Development)**
- No setup needed
- OTP codes print to terminal
- Perfect for testing

**Better Option: Setup Brevo (Free)**
1. Go to: https://www.brevo.com/
2. Sign up
3. Get API key from Settings → API
4. Add to .env:
   ```
   BREVO_API_KEY=your-key-here
   ```

See `EMAIL_CONFIGURATION_GUIDE.md` for detailed setup of other options.

### Step 4: Start Server (1 minute)

```bash
python manage.py runserver
```

You should see:
```
Starting development server at http://127.0.0.1:8000/
```

### Step 5: Test OTP Login (1 minute)

**Go to:** `http://127.0.0.1:8000/accounts/login/`

**Enter:**
- Username: `testuser`
- Password: `TestPassword123`
- Click: "Login to UniSync"

**Expected:**
1. ✅ Success message: "OTP sent to test@example.com"
2. ✅ Redirected to OTP verification page
3. ✅ Get OTP code:
   - If email configured: Check email inbox
   - If console backend: Check Django console/terminal for 6-digit code

**Enter OTP:**
- Paste the 6-digit code
- Click: "Verify OTP"

**Final Result:**
1. ✅ Success message: "Login successful!"
2. ✅ Redirected to dashboard
3. ✅ User is logged in ✅

---

## The Complete Flow (What Happens)

```
Login Page
    ↓
User: testuser / TestPassword123
    ↓
[Server] Authenticate user
    ↓
[Server] Generate OTP: 123456 (random)
    ↓
[Server] Send OTP email to test@example.com
    ↓
OTP Verification Page
    ↓
User: Enter OTP (check email or console)
    ↓
[Server] Validate OTP
    ↓
[Server] Create session
    ↓
[Server] Send welcome email
    ↓
Dashboard
    ↓
✅ User Logged In!
```

---

## Where to Find OTP Code

### If Email Configured:
1. Check your email inbox
2. Look for subject: "🚀 - Your login OTP Code"
3. Copy the 6-digit code

### If Using Console Backend:
1. Look at Django console/terminal
2. Search for: "OTP email sent"
3. Find 6-digit number in output
4. Copy and paste into form

**Example console output:**
```
Your OTP for login is: 456789
This OTP is valid for 5 minutes only.
```

---

## Code Changes

**File Modified:** `accounts/views.py`

**What Changed:**
- ✅ Removed direct login
- ✅ Re-enabled OTP requirement
- ✅ Added proper error handling
- ✅ Session stores user data during OTP process

**Key Functions:**
1. `login_view()` (Line 309) - Authenticate + Generate OTP
2. `verify_otp_view()` (Line 384) - Validate OTP + Create session
3. `send_otp_email()` (Line 136) - Send OTP via email

---

## Security Features

✅ **6-digit OTP codes** - 1 million combinations
✅ **5-minute expiry** - Short window
✅ **One-time use** - Code deleted after use
✅ **Email verification** - Requires email access
✅ **Logging** - All attempts logged
✅ **Password hashing** - PBKDF2 with salt

---

## Troubleshooting

### "OTP sent but no email received"

**Check 1:** Email backend configured?
```bash
python manage.py shell
from django.conf import settings
print(settings.EMAIL_BACKEND)
# Should NOT be: ConsoleEmailBackend (unless testing)
exit()
```

**Check 2:** Using console backend?
- Look in Django console for OTP code
- Should appear when you try to login

**Check 3:** Check spam folder
- Gmail, Outlook, etc. might mark as spam
- Add sender to safe list

**Check 4:** Test email directly
```bash
python manage.py shell
from django.core.mail import send_mail
from django.conf import settings
send_mail('Test', 'Test', settings.DEFAULT_FROM_EMAIL, ['your-email@gmail.com'])
# Wait 30 seconds and check email
exit()
```

### "Invalid OTP" error

**Possible causes:**
1. ❌ Entered wrong code → Check email again
2. ❌ OTP expired (> 5 minutes) → Click "Resend OTP"
3. ❌ Already used code → Get new OTP by logging in again
4. ❌ Extra spaces in code → Enter code without spaces

### "OTP has expired"

**Solution:** Click "Resend OTP" button
- This generates a new code
- Valid for 5 more minutes

### "Session expired. Please login again."

**Cause:** Took too long to navigate to OTP page
**Solution:** Start login process again

---

## Files You Need to Know

| File | Purpose |
|------|---------|
| `accounts/views.py` | Login & OTP verification logic |
| `accounts/models.py` | OTP model definition |
| `accounts/forms.py` | OTP form validation |
| `accounts/templates/login.html` | Login page |
| `accounts/templates/verify_otp.html` | OTP entry page |
| `.env` | Email configuration |

---

## Commands Reference

```bash
# Run migrations
python manage.py migrate

# Create shell
python manage.py shell

# Run server
python manage.py runserver

# Clear database (careful!)
python manage.py flush

# Test email
python manage.py shell
# Then: from django.core.mail import send_mail
# Then: send_mail('Test', 'Test', 'noreply@example.com', ['test@gmail.com'])
```

---

## Checklist

- [ ] Run migrations: `python manage.py migrate`
- [ ] Create test user
- [ ] Configure email (or use console)
- [ ] Start server: `python manage.py runserver`
- [ ] Go to login page: `http://127.0.0.1:8000/accounts/login/`
- [ ] Enter testuser / TestPassword123
- [ ] Receive OTP (in email or console)
- [ ] Enter OTP code
- [ ] Verify successful login
- [ ] Check you're redirected to dashboard

---

## Next Steps

1. **Complete the 5-minute setup above**
2. **Test OTP login flow**
3. **Configure proper email service** (see EMAIL_CONFIGURATION_GUIDE.md)
4. **Deploy to production** (when ready)

---

## Need More Details?

- **Email setup:** See `EMAIL_CONFIGURATION_GUIDE.md`
- **Complete OTP flow:** See `OTP_LOGIN_FLOW_GUIDE.md`
- **Troubleshooting:** See troubleshooting section above

---

**Status:** ✅ Ready to test OTP login

**Time to test:** 5 minutes

**Difficulty:** Easy - Just follow the 5 steps above
