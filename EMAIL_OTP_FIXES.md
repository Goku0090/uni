# Email & OTP Configuration Fix Guide

## Issue
OTP emails are not being sent to user mailboxes. The system defaults to console backend in development.

---

## Root Causes

### 1. **Email Backend Not Configured** (Primary)
- Settings fallback to `django.core.mail.backends.console.EmailBackend`
- This prints emails to console instead of sending them
- **Location:** `auth_project/settings.py` lines 234-255

### 2. **Missing Environment Variables**
Environment variables required for email backends are not set:
```
BREVO_API_KEY         # For Brevo email service (recommended)
ZEPTO_MAIL_API_KEY    # For ZeptoMail service (alternative)
ZEPTO_MAIL_TOKEN      # ZeptoMail authentication token
EMAIL_HOST_USER       # For Gmail SMTP (fallback)
EMAIL_HOST_PASSWORD   # For Gmail SMTP (fallback)
```

### 3. **Incorrect Email Backend Priority**
Settings checks for credentials but may not have them configured.

---

## Solution: Choose One Email Service

### Option 1: Use Brevo (Recommended - Free, Reliable)

**Step 1: Get Brevo API Key**
1. Go to https://www.brevo.com/
2. Sign up for free account
3. Get API key from: Dashboard → Settings → API Keys
4. Free tier: 300 emails/day

**Step 2: Configure Environment**

Create or update `.env` file in `e:\login\auth_project\`:
```env
# Email Configuration
BREVO_API_KEY=xsua...your_api_key_here...
DEFAULT_FROM_EMAIL=noreply@yourdomain.com

# Other variables
SECRET_KEY=your-secret-key
DEBUG=True
ALLOWED_HOSTS=localhost,127.0.0.1
```

**Step 3: Verify Configuration**
```python
# auth_project/settings.py (already correct)
EMAIL_BACKEND = 'accounts.brevo_mail_backend.BrevoMailBackend'
BREVO_API_KEY = os.getenv('BREVO_API_KEY')
```

---

### Option 2: Use ZeptoMail (Alternative)

**Step 1: Get ZeptoMail Credentials**
1. Go to https://www.zoho.com/zeptomail/
2. Sign up for free account
3. Get API Key from dashboard
4. Get Mail Token from SMTP settings
5. Free tier: 10,000 emails/month

**Step 2: Configure Environment**

Add to `.env`:
```env
ZEPTO_MAIL_API_KEY=your_api_key_here
ZEPTO_MAIL_TOKEN=your_mail_token_here
DEFAULT_FROM_EMAIL=noreply@yourdomain.com
```

---

### Option 3: Use Gmail SMTP (Fallback)

**Step 1: Setup Gmail**
1. Enable 2-factor authentication on Gmail
2. Generate App Password: https://myaccount.google.com/apppasswords
3. Use the 16-character password generated

**Step 2: Configure Environment**

Add to `.env`:
```env
EMAIL_HOST_USER=your-email@gmail.com
EMAIL_HOST_PASSWORD=your-16-char-app-password
DEFAULT_FROM_EMAIL=your-email@gmail.com
```

**Step 3: Update Settings** (if using Gmail)
```python
# auth_project/settings.py lines 242-248
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = 'smtp.gmail.com'
EMAIL_PORT = 587
EMAIL_USE_TLS = True
EMAIL_HOST_USER = os.getenv('EMAIL_HOST_USER')
EMAIL_HOST_PASSWORD = os.getenv('EMAIL_HOST_PASSWORD')
```

---

## Testing Email Configuration

### Method 1: Using Test Script

Run the diagnostic script:
```bash
cd e:\login\auth_project
python test_email_diagnostic.py
```

Expected output:
```
EMAIL BACKEND: accounts.brevo_mail_backend.BrevoMailBackend
BREVO_API_KEY: ✓ SET
DEFAULT_FROM_EMAIL: noreply@unisync.app
TESTING EMAIL SEND...
  - OTP Generated: 123456
  - Email Send Result: 1 (1=success)
  ✓ EMAIL SENT SUCCESSFULLY
```

### Method 2: Django Shell Test

```bash
cd e:\login\auth_project
python manage.py shell
```

```python
from django.core.mail import send_mail
from django.conf import settings

result = send_mail(
    'Test Email',
    'This is a test message',
    settings.DEFAULT_FROM_EMAIL,
    ['your-test-email@gmail.com'],
)
print(f"Email sent: {result}")
```

### Method 3: Test OTP Flow

1. Go to http://localhost:8000/login/
2. Enter username and password
3. System should send OTP email
4. Check your email inbox

---

## Troubleshooting

### Email Still Not Sending

**Check 1: Verify .env file is loaded**
```python
# In Django shell
from django.conf import settings
print(settings.BREVO_API_KEY)  # Should print your API key, not None
```

**Check 2: Check logs**
```bash
tail -f e:\login\auth_project\logs\django.log
tail -f e:\login\auth_project\logs\error.log
```

**Check 3: Verify email backend is correct**
```python
# In Django shell
from django.conf import settings
print(settings.EMAIL_BACKEND)  # Should show your chosen backend
```

**Check 4: Test Brevo API key**
```bash
curl -X GET "https://api.brevo.com/v3/account" \
  -H "api-key: YOUR_API_KEY" \
  -H "accept: application/json"
```

### Common Errors

**Error 1: "BREVO_API_KEY setting is required"**
- Solution: Set `BREVO_API_KEY` in `.env` file
- Verify `.env` is in `e:\login\auth_project\` directory

**Error 2: "ZEPTO_MAIL_API_KEY setting is required"**
- Solution: Set both `ZEPTO_MAIL_API_KEY` and `ZEPTO_MAIL_TOKEN`

**Error 3: "SMTPAuthenticationError" (Gmail)**
- Solution: Use App Password, not regular password
- Verify 2FA is enabled

**Error 4: "Connection timeout"**
- Solution: Check internet connection
- Verify API endpoint is accessible

---

## Quick Fix Checklist

- [ ] Choose one email service (Brevo recommended)
- [ ] Get API key/credentials from service
- [ ] Create `.env` file in `e:\login\auth_project\`
- [ ] Add email configuration to `.env`
- [ ] Restart Django server
- [ ] Run test script to verify
- [ ] Test OTP flow in browser
- [ ] Check email inbox

---

## File Locations

| File | Purpose |
|------|---------|
| `e:\login\auth_project\.env` | Environment variables (CREATE THIS) |
| `e:\login\auth_project\auth_project\settings.py` | Email config (lines 214-270) |
| `e:\login\auth_project\accounts\brevo_mail_backend.py` | Brevo backend implementation |
| `e:\login\auth_project\accounts\zepto_mail_backend.py` | ZeptoMail backend implementation |
| `e:\login\auth_project\accounts\views.py` | OTP sending logic (line 139) |
| `e:\login\auth_project\test_email_diagnostic.py` | Test script |
| `e:\login\auth_project\logs\django.log` | Debug logs |

---

## Email Backend Decision Matrix

| Service | Cost | Speed | Limit | Complexity | Notes |
|---------|------|-------|-------|------------|-------|
| **Brevo** | Free (300/day) | Fast | 300/day free | Low | ✓ Recommended |
| ZeptoMail | Free (10k/month) | Fast | 10k/month free | Medium | Zoho ecosystem |
| Gmail | Free | Medium | 500/day | Low | Personal email only |
| Console | Free | N/A | N/A | None | Dev only, prints to console |

---

## Next Steps

1. **Immediate:** Create `.env` file with chosen email service credentials
2. **Test:** Run diagnostic script to verify email sending
3. **Deploy:** Email will work automatically on Render/production with same `.env`
4. **Monitor:** Check logs for any email errors in `logs/django.log`

