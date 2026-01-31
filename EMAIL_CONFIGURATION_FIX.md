# Email Configuration Fix - OTP Emails Not Sending

## Problem
Emails (OTP codes) are not being sent to users during login/registration.

## Root Cause Analysis

### Email Backend Configuration
**Current Priority** (settings.py, lines 234-254):
1. ✅ **Brevo** - If `BREVO_API_KEY` is set
2. ✅ **ZeptoMail** - If `ZEPTO_MAIL_API_KEY` + `ZEPTO_MAIL_TOKEN` set
3. ✅ **Gmail SMTP** - If `EMAIL_HOST_USER` + `EMAIL_HOST_PASSWORD` set
4. ⚠️ **Console Backend** - Default (emails print to console only)

### Likely Issue
**No `.env` file or environment variables set** → System defaults to **Console Backend**

When Console Backend is active:
- ❌ Emails NOT sent to actual email addresses
- ✅ OTP code printed to Django server console
- ✅ Can test locally without email service

---

## Solution: Enable Email Sending

### Option 1: Use Gmail SMTP (Easiest for Testing)

**Step 1**: Create/Update `.env` file in project root

```bash
# Create file at: e:/login/.env

# ===== EMAIL CONFIGURATION =====
EMAIL_HOST_USER=your-email@gmail.com
EMAIL_HOST_PASSWORD=your-app-password
DEFAULT_FROM_EMAIL=your-email@gmail.com

# Optional: Brevo or ZeptoMail (comment out Gmail to use these)
# BREVO_API_KEY=your-brevo-key
# ZEPTO_MAIL_API_KEY=your-zepto-key
# ZEPTO_MAIL_TOKEN=your-zepto-token
```

**Step 2**: Generate Gmail App Password
1. Go to: https://myaccount.google.com/security
2. Enable "2-Step Verification"
3. Go to "App passwords"
4. Select "Mail" and "Windows Computer"
5. Copy generated password (16 characters)
6. Use this as `EMAIL_HOST_PASSWORD` (NOT your regular Gmail password)

**Step 3**: Restart Django server
```bash
python manage.py runserver
```

**Result**: Server output should show:
```
[SUCCESS] EMAIL BACKEND: Using Gmail SMTP
```

---

### Option 2: Use Brevo (Production Recommended)

**Step 1**: Create Brevo Account
- Go to: https://www.brevo.com/
- Sign up and create account
- Go to Settings → SMTP & API
- Copy API Key

**Step 2**: Create Brevo Backend File

**File**: `accounts/brevo_mail_backend.py`

```python
"""
Brevo Email Backend for Django
Sends emails using Brevo transactional email service.
"""

import json
import logging
from django.core.mail.backends.base import BaseEmailBackend
from django.conf import settings
import requests

logger = logging.getLogger(__name__)


class BrevoMailBackend(BaseEmailBackend):
    """
    A Django email backend that uses Brevo API to send emails.
    """

    def __init__(self, api_key=None, fail_silently=False, **kwargs):
        super().__init__(fail_silently=fail_silently, **kwargs)
        
        self.api_key = api_key or getattr(settings, 'BREVO_API_KEY', None)
        self.api_url = 'https://api.brevo.com/v3/smtp/email'
        
        if not self.api_key:
            raise ValueError("BREVO_API_KEY setting is required for Brevo backend")
        
        self.headers = {
            'Accept': 'application/json',
            'Content-Type': 'application/json',
            'api-key': self.api_key
        }
        
        logger.info("Brevo backend initialized successfully")

    def send_messages(self, email_messages):
        """Send emails using Brevo API."""
        if not email_messages:
            return 0
        
        sent_count = 0
        
        for message in email_messages:
            try:
                payload = self._prepare_payload(message)
                response = requests.post(
                    self.api_url,
                    headers=self.headers,
                    json=payload,
                    timeout=30
                )
                
                if response.status_code == 201:
                    sent_count += 1
                    logger.info(f"Email sent successfully to {message.to} via Brevo")
                else:
                    logger.error(f"Brevo API error {response.status_code}: {response.text}")
                    if not self.fail_silently:
                        raise Exception(f"Brevo API error: {response.text}")
                        
            except Exception as e:
                logger.error(f"Failed to send email: {str(e)}")
                if not self.fail_silently:
                    raise
        
        return sent_count

    def _prepare_payload(self, message):
        """Convert Django EmailMessage to Brevo API format."""
        payload = {
            "sender": {
                "name": "UniSync",
                "email": message.from_email
            },
            "to": [
                {"email": email, "name": email.split('@')[0]}
                for email in message.to
            ],
            "subject": message.subject,
        }
        
        # Handle HTML and text content
        if hasattr(message, 'alternatives') and message.alternatives:
            for content, mime_type in message.alternatives:
                if mime_type == 'text/html':
                    payload["htmlContent"] = content
                elif mime_type == 'text/plain':
                    payload["textContent"] = content
        else:
            payload["textContent"] = message.body
        
        # Add CC/BCC if present
        if message.cc:
            payload["cc"] = [{"email": email} for email in message.cc]
        if message.bcc:
            payload["bcc"] = [{"email": email} for email in message.bcc]
        
        return payload

    def open(self):
        """Open connection (REST API, no persistent connection needed)."""
        return True

    def close(self):
        """Close connection (REST API, no cleanup needed)."""
        pass
```

**Step 3**: Update `.env`
```
BREVO_API_KEY=your-api-key-here
DEFAULT_FROM_EMAIL=noreply@unisync.app
```

---

### Option 3: Use ZeptoMail (Alternative)

**Step 1**: Create ZeptoMail Account
- Go to: https://www.zeptomail.com/
- Sign up for account
- Get API Key and Mail Token from dashboard

**Step 2**: Update `.env`
```
ZEPTO_MAIL_API_KEY=your-api-key
ZEPTO_MAIL_TOKEN=your-mail-token
DEFAULT_FROM_EMAIL=noreply@unisync.app
```

---

## Verification

### Check Current Backend
When Django starts, you should see one of:
```
✅ [SUCCESS] EMAIL BACKEND: Using Gmail SMTP
✅ [SUCCESS] EMAIL BACKEND: Using Brevo for OTP and transactional emails
✅ [SUCCESS] EMAIL BACKEND: Using ZeptoMail for OTP and transactional emails
⚠️ [WARNING] EMAIL BACKEND: Using console backend - OTP codes will be printed to console
```

### Test Email Sending

**Option A: Using Django Shell**
```bash
python manage.py shell
>>> from django.core.mail import EmailMultiAlternatives
>>> msg = EmailMultiAlternatives(
...     subject="Test Email",
...     body="This is a test",
...     from_email="noreply@unisync.app",
...     to=["your-email@gmail.com"]
... )
>>> msg.send()
>>> exit()
```

If successful, you should receive the email in seconds.

**Option B: Trigger OTP Email**
1. Go to login page
2. Enter username and click "Login"
3. Check:
   - Django console for "Email sent successfully" message
   - Your inbox for OTP email
   - Spam folder if not in inbox

---

## File Structure

After implementation:
```
auth_project/
├── accounts/
│   ├── brevo_mail_backend.py       ✅ CREATE THIS
│   ├── zepto_mail_backend.py       ✅ ALREADY EXISTS
│   ├── views.py                    ✅ Has send_otp_email()
│   └── ...
├── .env                            ✅ CREATE THIS
├── auth_project/
│   └── settings.py                 ✅ Email config
└── manage.py
```

---

## .env File Template

Create file: `e:/login/.env`

```bash
# ===== EMAIL CONFIGURATION =====
# Choose ONE option below:

# Option 1: Gmail SMTP (Recommended for Testing)
EMAIL_HOST_USER=your-email@gmail.com
EMAIL_HOST_PASSWORD=your-app-password
DEFAULT_FROM_EMAIL=your-email@gmail.com

# Option 2: Brevo API (Recommended for Production)
# BREVO_API_KEY=your-brevo-api-key
# DEFAULT_FROM_EMAIL=noreply@unisync.app

# Option 3: ZeptoMail API
# ZEPTO_MAIL_API_KEY=your-zepto-key
# ZEPTO_MAIL_TOKEN=your-zepto-token
# DEFAULT_FROM_EMAIL=noreply@unisync.app

# ===== DATABASE CONFIGURATION =====
DB_NAME=unisync_db
DB_USER=unisync_user
DB_PASSWORD=your_password
DB_HOST=localhost
DB_PORT=5432

# ===== SECURITY =====
SECRET_KEY=your-secret-key-here
DEBUG=True
ALLOWED_HOSTS=localhost,127.0.0.1

# ===== SOCIAL AUTH =====
GOOGLE_CLIENT_ID=your-google-client-id
GOOGLE_CLIENT_SECRET=your-google-secret
GITHUB_CLIENT_ID=your-github-id
GITHUB_CLIENT_SECRET=your-github-secret

# ===== APIS =====
RAPIDAPI_KEY=your-rapidapi-key
RAPIDAPI_HOST=universities-list.p.rapidapi.com
```

---

## Troubleshooting

### Issue 1: "EMAIL BACKEND: Using console backend"
**Solution**: Add email credentials to `.env` file

### Issue 2: "Failed to send OTP email"
**Check**:
1. Is .env file in project root? (e:/login/.env)
2. Did you restart Django server?
3. Are API keys/credentials correct?
4. Check logs: `logs/django.log`

### Issue 3: Gmail Authentication Fails
**Solution**: 
- Use App Password, NOT regular Gmail password
- Enable 2-Step Verification
- See Step 2 above

### Issue 4: Brevo/ZeptoMail API Errors
**Solution**:
- Verify API key is correct
- Check API key hasn't expired
- Verify sender email is verified in service

---

## Testing Checklist

After configuration:
- [ ] .env file created with email credentials
- [ ] Django server restarted
- [ ] Console shows correct EMAIL BACKEND
- [ ] Test email sent successfully via shell
- [ ] OTP email received in inbox
- [ ] Email appears quickly (within 10 seconds)
- [ ] Email is not in spam folder

---

## Production Deployment

For production:
1. **Use Brevo** (Most reliable)
2. **Set BREVO_API_KEY** in environment variables
3. **Use verified sender email** in Brevo account
4. **Monitor logs** for email failures
5. **Set up email logging** with proper rotation

---

## Important Notes

⚠️ **Never commit .env file to git**
```bash
# Add to .gitignore
echo ".env" >> .gitignore
```

✅ **Use environment variables in production**
Set via:
- Platform settings (Render, Heroku, etc.)
- Docker environment variables
- Kubernetes secrets
- CI/CD pipeline secrets

---

## Quick Comparison

| Service | Setup | Speed | Reliability | Cost |
|---------|-------|-------|-------------|------|
| **Gmail SMTP** | Easy | ⭐⭐⭐ | ⭐⭐⭐ | Free |
| **Brevo** | Medium | ⭐⭐⭐⭐ | ⭐⭐⭐⭐ | Free tier 300/day |
| **ZeptoMail** | Medium | ⭐⭐⭐⭐ | ⭐⭐⭐⭐ | Free tier 100/day |
| **Console** | Instant | - | Dev only | Free |

---

## Next Steps

1. ✅ Choose email service (Gmail for testing)
2. ✅ Create .env file with credentials
3. ✅ Create brevo_mail_backend.py if needed
4. ✅ Restart Django server
5. ✅ Test email sending
6. ✅ Verify OTP emails work
