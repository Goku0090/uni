# Email Setup - Quick Guide (3 Minutes)

## Status
✅ Brevo backend file created  
⏳ Now you need environment variables

## Fastest Setup: Gmail SMTP

### Step 1: Create `.env` file
**Location**: `e:\login\.env`

```
EMAIL_HOST_USER=your-email@gmail.com
EMAIL_HOST_PASSWORD=your-app-password
DEFAULT_FROM_EMAIL=your-email@gmail.com
```

### Step 2: Get Gmail App Password
1. Go to: https://myaccount.google.com/security
2. Enable "2-Step Verification" (if not enabled)
3. Click "App passwords"
4. Select: Mail → Windows Computer
5. Copy 16-character password
6. Paste into `.env` as `EMAIL_HOST_PASSWORD`

### Step 3: Restart Server
```bash
# Stop: Ctrl+C
# Start: python manage.py runserver
```

### Step 4: Check Console Output
Should see:
```
[SUCCESS] EMAIL BACKEND: Using Gmail SMTP
```

---

## Test Email

### Via Django Shell
```bash
python manage.py shell
>>> from django.core.mail import send_mail
>>> send_mail(
...     'Test Subject',
...     'Test message body',
...     'your-email@gmail.com',
...     ['your-email@gmail.com'],
... )
1  # Returns 1 if successful
>>> exit()
```

### Via Login
1. Go to login page
2. Enter credentials
3. Check inbox for OTP email

---

## Alternative: Brevo (Free, Professional)

### Step 1: Create Account
Go to: https://www.brevo.com/ → Sign up

### Step 2: Get API Key
- Dashboard → Settings → SMTP & API
- Copy API Key

### Step 3: Update `.env`
```
BREVO_API_KEY=your-api-key-here
DEFAULT_FROM_EMAIL=noreply@unisync.app
```

### Step 4: Restart & Test
Same as Gmail steps 3-4 above

---

## .env File Location
```
e:/login/
├── .env                    ← Create here
├── manage.py
├── auth_project/
│   ├── settings.py
│   └── ...
└── ...
```

---

## Common Problems

| Issue | Solution |
|-------|----------|
| "Using console backend" | Add credentials to .env, restart |
| Gmail auth fails | Use App Password, not Gmail password |
| Email not received | Check spam folder, verify email service |
| "API key invalid" | Copy exact key from Brevo dashboard |

---

## Verify Setup

Check these logs when server starts:
```bash
# Good
[SUCCESS] EMAIL BACKEND: Using Gmail SMTP
[SUCCESS] EMAIL BACKEND: Using Brevo...

# Bad
[WARNING] EMAIL BACKEND: Using console backend
```

---

## Next: Test OTP Email
1. Go to: http://localhost:8000/login/
2. Enter username/email
3. Submit
4. Check email inbox for OTP code
5. If received → Email working! ✅

---

## Important
- Never commit `.env` to git
- Keep API keys secret
- Use environment variables in production

Done! Your emails should now work.
