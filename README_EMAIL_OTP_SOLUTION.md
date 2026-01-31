# Email & OTP Solution - Complete Guide

## Overview

Your UniSync application has a fully functional email and OTP system, but **it's not configured yet**. This guide will walk you through setup.

### Current State

| Component | Status | Details |
|-----------|--------|---------|
| OTP Model | ✅ Working | Generates 6-digit codes, 5-min expiry |
| OTP Logic | ✅ Working | Stored in database, validated on use |
| Email Function | ✅ Working | HTML/text templates, error handling |
| Brevo Backend | ✅ Implemented | Production-ready API integration |
| ZeptoMail Backend | ✅ Implemented | Alternative with high volume limits |
| Gmail Backend | ✅ Implemented | Fallback for existing Gmail users |
| **Configuration** | ❌ Missing | Need `.env` file with credentials |

---

## Problem

When users try to login:
1. System generates OTP ✅
2. System tries to send email ❓
3. **Email doesn't arrive** ❌

**Why?** No email service is configured in `.env` file.

Currently, emails are sent to **console** (terminal output) instead of actual inbox.

---

## Solution

### Quick Start (2 minutes)

**Step 1:** Create file `e:\login\auth_project\.env`

**Step 2:** Add this content:
```
BREVO_API_KEY=xsua1234567890abcdefghijklmnopqrstuvwxyz
DEFAULT_FROM_EMAIL=noreply@unisync.app
SECRET_KEY=your-secret-key-here
DEBUG=True
ALLOWED_HOSTS=localhost,127.0.0.1
```

**Step 3:** Get `BREVO_API_KEY`:
1. Go to https://www.brevo.com/
2. Sign up (free)
3. Settings → SMTP & API → Copy API Key
4. Paste into .env

**Step 4:** Restart Django
```bash
python manage.py runserver
```

**Step 5:** Test
```bash
python quick_email_test.py
```

Expected: `✓ SUCCESS: Email send returned 1`

---

## Email Service Comparison

### Brevo (Recommended) ⭐

**Pros:**
- Free: 300 emails/day (sufficient for 100+ users)
- Industry-leading deliverability
- Simple API
- Built-in analytics
- Perfect for OTP/transactional emails

**Cost:** Free tier + paid options
**Setup:** 2 minutes
**Link:** https://www.brevo.com/

### ZeptoMail

**Pros:**
- Free: 10,000 emails/month
- Zoho ecosystem integration
- Good for high volume

**Cost:** Free tier + paid options  
**Setup:** 3 minutes
**Link:** https://www.zoho.com/zeptomail/

### Gmail SMTP

**Pros:**
- Uses existing Gmail account
- No signup needed
- Simple authentication

**Cons:**
- Limited to 500/day
- Harder to debug issues
- Not for business

**Cost:** Free
**Setup:** 3 minutes

---

## Detailed Setup

### Brevo Setup (Step-by-Step)

```
1. Visit https://www.brevo.com/
2. Click "Sign up free"
3. Enter email and create password
4. Check email for verification link
5. Click link to verify
6. You're logged in to dashboard
7. Click "Settings" (gear icon top right)
8. Select "SMTP & API" from left menu
9. Scroll to "API Keys" section
10. Click "Create a new API key"
11. Copy the key (40+ character string starting with "xsua")
12. Create .env file:
    e:\login\auth_project\.env
13. Add lines:
    BREVO_API_KEY=xsua...YOUR_KEY...
    DEFAULT_FROM_EMAIL=noreply@unisync.app
    SECRET_KEY=your-secret-key
    DEBUG=True
    ALLOWED_HOSTS=localhost,127.0.0.1
14. Save file
15. Restart Django: python manage.py runserver
16. You should see: [SUCCESS] EMAIL BACKEND: Using Brevo...
17. Done!
```

### ZeptoMail Setup (Step-by-Step)

```
1. Visit https://www.zoho.com/zeptomail/
2. Click "Sign up free"
3. Choose workspace name
4. Enter email
5. Create password
6. Complete verification
7. Add your email domain (follow prompts)
8. Verify domain (DNS records)
9. Go to Settings → SMTP
10. Copy API Key
11. Copy Mail Token
12. Create .env file:
    e:\login\auth_project\.env
13. Add lines:
    ZEPTO_MAIL_API_KEY=YOUR_API_KEY
    ZEPTO_MAIL_TOKEN=YOUR_MAIL_TOKEN
    DEFAULT_FROM_EMAIL=noreply@yourdomain.com
    SECRET_KEY=your-secret-key
    DEBUG=True
    ALLOWED_HOSTS=localhost,127.0.0.1
14. Save file
15. Restart Django
16. Done!
```

### Gmail Setup (Step-by-Step)

```
1. Ensure 2FA is enabled on Gmail
2. Visit https://myaccount.google.com/apppasswords
3. Select "Mail" and "Windows Computer"
4. Click Generate
5. Copy the 16-character password
6. Create .env file:
    e:\login\auth_project\.env
7. Add lines:
    EMAIL_HOST_USER=your-email@gmail.com
    EMAIL_HOST_PASSWORD=xxxx xxxx xxxx xxxx
    DEFAULT_FROM_EMAIL=your-email@gmail.com
    SECRET_KEY=your-secret-key
    DEBUG=True
    ALLOWED_HOSTS=localhost,127.0.0.1
8. Edit auth_project/settings.py line 242
9. Change:
    if BREVO_API_KEY:
        EMAIL_BACKEND = 'accounts.brevo_mail_backend.BrevoMailBackend'
    elif EMAIL_HOST_USER and EMAIL_HOST_PASSWORD:
        EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
        EMAIL_HOST = 'smtp.gmail.com'
        EMAIL_PORT = 587
        EMAIL_USE_TLS = True
10. Save settings.py
11. Restart Django
12. Done!
```

---

## Testing

### Test 1: Quick Test
```bash
cd e:\login\auth_project
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

### Test 2: Detailed Diagnostics
```bash
python test_email_diagnostic.py
```

This generates a comprehensive report including:
- Email backend configuration
- API keys status
- Email sending test
- Last 10 log entries

### Test 3: Full Flow
1. Open http://localhost:8000/login/
2. Enter username and password
3. Click Login
4. Wait 5-10 seconds
5. Check email inbox
6. Find email from noreply@unisync.app
7. Copy OTP code
8. Paste in verification form
9. Login successful ✅

---

## Troubleshooting

### Issue: "BREVO_API_KEY setting is required"

**Cause:** .env file not created or not loaded

**Solution:**
1. Verify `.env` file exists in `e:\login\auth_project\`
2. Verify it contains `BREVO_API_KEY=YOUR_KEY`
3. Restart Django server
4. Check startup message for `[SUCCESS]`

### Issue: Email not arriving in inbox

**Check 1:** Verify email was sent
```bash
tail -f logs/django.log | grep -i "email"
```

Look for: `Email sent successfully`

**Check 2:** Check spam folder
- Find email from noreply@unisync.app
- Mark as "Not Spam"

**Check 3:** Verify recipient email
- Use different email address
- Try personal email (not work email)

**Check 4:** Verify API key
- Check Brevo dashboard
- Ensure key is correct and active
- Try creating new API key if needed

### Issue: "Connection refused" or "Timeout"

**Cause:** Network/firewall blocking API

**Solution:**
1. Check internet connection
2. Disable VPN if using
3. Check company firewall
4. Try from home network

### Issue: Django won't start after .env changes

**Cause:** .env syntax error

**Solution:**
```
CORRECT SYNTAX:
BREVO_API_KEY=xsua123abc

INCORRECT SYNTAX:
BREVO_API_KEY = xsua123abc    (spaces around =)
BREVO_API_KEY=xsua123!@#      (special chars)
```

---

## Architecture

```
User Login
    ↓
views.login_view() [accounts/views.py:139]
    ↓
OTP.generate_otp() [accounts/models.py:74]
    ↓
send_otp_email() [accounts/views.py:139]
    ↓
EmailMultiAlternatives.send()
    ↓
settings.EMAIL_BACKEND ← Read from .env
    ↓
Email Service (Brevo/ZeptoMail/Gmail)
    ↓
User Email Inbox ✅
```

---

## Files Reference

### New Files Created

| File | Purpose | Location |
|------|---------|----------|
| `.env.template` | Template for .env | `auth_project/` |
| `quick_email_test.py` | Quick test script | `auth_project/` |
| `test_email_diagnostic.py` | Detailed diagnostics | `auth_project/` |

### Existing Implementation

| File | Purpose | Status |
|------|---------|--------|
| `auth_project/settings.py` | Email config | ✅ Ready |
| `accounts/models.py` | OTP model | ✅ Ready |
| `accounts/views.py` | OTP sending | ✅ Ready |
| `accounts/brevo_mail_backend.py` | Brevo API | ✅ Ready |
| `accounts/zepto_mail_backend.py` | ZeptoMail API | ✅ Ready |

---

## Checklist

Before considering done:

- [ ] .env file created
- [ ] Email service chosen (Brevo recommended)
- [ ] API key obtained from service
- [ ] API key added to .env
- [ ] DEFAULT_FROM_EMAIL set in .env
- [ ] Django server restarted
- [ ] Startup shows [SUCCESS] EMAIL BACKEND message
- [ ] `python quick_email_test.py` shows ✓ SUCCESS
- [ ] Logs show "Email sent successfully"
- [ ] Test email received in inbox
- [ ] OTP login flow works end-to-end

---

## Next Steps

1. **Create .env file NOW**
2. **Get Brevo API key NOW** (takes 2 minutes)
3. **Restart Django NOW**
4. **Test OTP NOW**

After email is working:
- Configure social login (Google/GitHub)
- Configure college API (RapidAPI)
- Set up database backups
- Deploy to production

---

## Support

### Quick Answers

**Q: Which email service should I choose?**
A: Brevo (free, 300/day, recommended)

**Q: How long does setup take?**
A: 5 minutes total

**Q: Can I change service later?**
A: Yes, just change .env file and restart

**Q: Will it work on Render?**
A: Yes, add .env to Render environment variables

**Q: Is it secure?**
A: Yes, API keys never exposed in code

---

## Contact

If you need help:
1. Run `python test_email_diagnostic.py`
2. Check logs: `tail -f logs/django.log`
3. See `STEP_BY_STEP_EMAIL_FIX.md` for detailed steps
4. See `EMAIL_OTP_FIXES.md` for troubleshooting

