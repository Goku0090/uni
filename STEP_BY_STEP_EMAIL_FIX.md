# Step-by-Step Email/OTP Fix Guide

## Current Issue
- OTP emails are not being sent
- System defaults to console backend (prints to console instead of sending)

## Why It's Happening
1. No email service credentials in `.env` file
2. Settings fall back to console backend
3. No actual email is being delivered

---

# QUICK FIX (5 Minutes)

## Step 1: Create .env File

Navigate to: `e:\login\auth_project\`

Create file named `.env` with this content:

```env
BREVO_API_KEY=YOUR_API_KEY_HERE
DEFAULT_FROM_EMAIL=noreply@unisync.app
SECRET_KEY=your-secret-key-change-this-in-production
DEBUG=True
ALLOWED_HOSTS=localhost,127.0.0.1
```

**How to get BREVO_API_KEY:**
1. Go to https://www.brevo.com/
2. Click "Sign up free"
3. Create account
4. Go to "Settings" → "SMTP & API"
5. Copy the "API Key" value
6. Paste into `.env` file above

---

## Step 2: Test Email Configuration

Open terminal in `e:\login\auth_project\` and run:

```bash
python quick_email_test.py
```

Expected output:
```
EMAIL_BACKEND: accounts.brevo_mail_backend.BrevoMailBackend
DEFAULT_FROM_EMAIL: noreply@unisync.app
BREVO_API_KEY: SET (first 10 chars: xsua1234...)
--- Testing Email Send ---
✓ SUCCESS: Email send returned 1
Email backend is working correctly!
```

---

## Step 3: Restart Django Server

Kill running Django server (Ctrl+C) and restart:

```bash
python manage.py runserver
```

Watch for success message:
```
[SUCCESS] EMAIL BACKEND: Using Brevo for OTP and transactional emails
```

---

## Step 4: Test OTP Flow

1. Open http://localhost:8000/login/
2. Enter valid username and password
3. You should see message: "OTP sent to your-email@gmail.com"
4. Check your email inbox (wait 10-30 seconds)
5. Find email from noreply@unisync.app with OTP code
6. Enter OTP to login

---

# DETAILED SETUP BY SERVICE

## Option A: Brevo (Recommended)

### Why Brevo?
- ✓ Free tier: 300 emails/day
- ✓ High deliverability
- ✓ Simple setup
- ✓ Best for OTP/transactional emails

### Setup

**1. Get API Key**
1. Visit https://www.brevo.com/
2. Click "Sign up free" (or login if existing account)
3. Complete signup
4. Go to Dashboard
5. Click "Settings" (gear icon top right)
6. Select "SMTP & API" from left menu
7. In "API Keys" section, click "Create a new API key"
8. Copy the key

**2. Configure .env**

Edit `e:\login\auth_project\.env`:
```env
# Email Service
BREVO_API_KEY=xsua1234567890abcdefghijklmnopqrstuvwxyz
DEFAULT_FROM_EMAIL=noreply@unisync.app

# Security
SECRET_KEY=django-insecure-abcdefghijklmnopqrstuvwxyz1234567890
DEBUG=True
ALLOWED_HOSTS=localhost,127.0.0.1
```

**3. Test**
```bash
python quick_email_test.py
```

**4. Verify in Logs**

After sending test OTP, check:
```bash
tail -f logs/django.log
```

Look for:
```
[SUCCESS] EMAIL BACKEND: Using Brevo for OTP and transactional emails
[SUCCESS] Email sent successfully to user@example.com via Brevo
```

---

## Option B: ZeptoMail

### Why ZeptoMail?
- ✓ Free tier: 10,000 emails/month
- ✓ Zoho ecosystem integration
- ✓ Good for high-volume

### Setup

**1. Get Credentials**
1. Visit https://www.zoho.com/zeptomail/
2. Sign up for free account
3. Complete verification
4. Go to Settings → SMTP
5. Copy:
   - **API Key** (for ZEPTO_MAIL_API_KEY)
   - **Mail Token** (for ZEPTO_MAIL_TOKEN)

**2. Configure .env**

Edit `e:\login\auth_project\.env`:
```env
# Email Service
ZEPTO_MAIL_API_KEY=your_api_key_here
ZEPTO_MAIL_TOKEN=your_mail_token_here
DEFAULT_FROM_EMAIL=noreply@unisync.app

# Security
SECRET_KEY=django-insecure-abcdefghijklmnopqrstuvwxyz1234567890
DEBUG=True
ALLOWED_HOSTS=localhost,127.0.0.1
```

**3. Test**
```bash
python quick_email_test.py
```

---

## Option C: Gmail SMTP

### Why Gmail?
- ✓ Already have Gmail account
- ✓ No signup needed
- ✓ Good for small volume

### Setup

**1. Get App Password**

1. Go to https://myaccount.google.com/apppasswords
2. Select "Mail" and "Windows Computer"
3. Generate password (you'll get 16 characters)
4. Copy the password

**2. Configure .env**

Edit `e:\login\auth_project\.env`:
```env
# Email Service (Gmail)
EMAIL_HOST_USER=your-email@gmail.com
EMAIL_HOST_PASSWORD=xxxx xxxx xxxx xxxx
DEFAULT_FROM_EMAIL=your-email@gmail.com

# Security
SECRET_KEY=django-insecure-abcdefghijklmnopqrstuvwxyz1234567890
DEBUG=True
ALLOWED_HOSTS=localhost,127.0.0.1
```

**3. Update settings.py**

Edit `e:\login\auth_project\auth_project\settings.py` around line 242:

```python
# Change from:
if BREVO_API_KEY:
    EMAIL_BACKEND = 'accounts.brevo_mail_backend.BrevoMailBackend'

# To:
elif EMAIL_HOST_USER and EMAIL_HOST_PASSWORD:
    EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
    EMAIL_HOST = 'smtp.gmail.com'
    EMAIL_PORT = 587
    EMAIL_USE_TLS = True
```

**4. Test**
```bash
python quick_email_test.py
```

---

# Troubleshooting

## Problem 1: "OTP not in email"

**Check 1:** Server shows email was sent?
```bash
# View logs
tail -f logs/django.log
```

Look for: `Email sent successfully`

**Check 2:** Email went to spam?
- Check Spam/Junk folder
- Mark as "Not Spam"
- Create filter to prevent future spam marking

**Check 3:** Email address is correct?
- On login page, check shown email matches your account email
- Use email that doesn't have spam filters

---

## Problem 2: "ValueError: BREVO_API_KEY setting is required"

**Cause:** .env file not created or not loaded

**Fix:**
1. Verify `.env` exists in `e:\login\auth_project\`
2. Verify file has `BREVO_API_KEY=...` line
3. Restart Django server
4. Check startup message for `[SUCCESS] EMAIL BACKEND:`

---

## Problem 3: Email sends but doesn't arrive

**Check 1:** Verify API key is correct
- Copy exactly from Brevo dashboard
- No extra spaces
- Complete key (usually 40+ characters)

**Check 2:** Test API key validity
```bash
# For Brevo, test with curl
curl -X GET "https://api.brevo.com/v3/account" \
  -H "api-key: YOUR_API_KEY" \
  -H "accept: application/json"
```

**Check 3:** Check recipient email
- Use different email address
- Try personal gmail account
- Check for typos

---

## Problem 4: "Connection refused" or "Timeout"

**Cause:** Network/firewall issue

**Fix:**
1. Check internet connection
2. Disable VPN if using
3. Check if company firewall blocks API calls
4. Try different network

---

## Problem 5: Server won't start after .env changes

**Cause:** Invalid .env syntax

**Fix:**
1. Check .env file for syntax errors
2. Remove special characters outside quotes
3. No spaces around `=`
4. Correct format: `KEY=value`

**Example of wrong vs right:**
```
# WRONG
BREVO_API_KEY = xsua123...  # spaces around =
BREVO_API_KEY=xsua123...!@# # special chars

# RIGHT
BREVO_API_KEY=xsua123abc...
```

---

# Verification Checklist

After setup, verify each step:

- [ ] `.env` file created in `e:\login\auth_project\`
- [ ] API key added to `.env`
- [ ] `DEFAULT_FROM_EMAIL` added to `.env`
- [ ] Django server restarted
- [ ] Server shows `[SUCCESS] EMAIL BACKEND:` message
- [ ] `python quick_email_test.py` shows ✓ SUCCESS
- [ ] Logs show `Email sent successfully` message
- [ ] Test email received in inbox
- [ ] Login with OTP works end-to-end

---

# Files Reference

| File | Purpose | Status |
|------|---------|--------|
| `e:\login\auth_project\.env` | **CREATE THIS** - Your credentials | ❌ Create Now |
| `e:\login\auth_project\.env.template` | Template reference | ✓ Exists |
| `e:\login\auth_project\quick_email_test.py` | Quick test script | ✓ Exists |
| `e:\login\auth_project\test_email_diagnostic.py` | Detailed diagnostics | ✓ Exists |
| `e:\login\auth_project\auth_project\settings.py` | Email config | ✓ Configured |
| `e:\login\auth_project\accounts\brevo_mail_backend.py` | Brevo backend | ✓ Implemented |
| `e:\login\auth_project\accounts\zepto_mail_backend.py` | ZeptoMail backend | ✓ Implemented |

---

# Next Steps

1. **NOW:** Create `.env` file with Brevo API key
2. **NOW:** Run `python quick_email_test.py`
3. **NOW:** Restart Django server
4. **NOW:** Test OTP login flow
5. **LATER:** Configure other services if needed (Google OAuth, RapidAPI, etc.)

---

# Support

**If still having issues:**

1. Check logs: `tail -f logs/django.log`
2. Run: `python test_email_diagnostic.py` (for detailed report)
3. Verify Brevo API key is valid in their dashboard
4. Try different email address as recipient
5. Check if Brevo has email limits reached

