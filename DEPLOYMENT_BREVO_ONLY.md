# Deployment Guide: Brevo Email Backend (UniSync)

## Issue Fixed
Removed non-existent PyPI packages:
- ❌ `zeptomail==1.0.0` (not available on PyPI)
- ❌ `rapidapi==1.0.0` (invalid package)

Now using **Brevo only** for email delivery.

## Updated Files
✅ `requirements.txt` - Cleaned (Brevo-only)
✅ `requirements_UPDATED.txt` - Cleaned (Brevo-only)
✅ `settings.py` - Removed ZeptoMail configuration

## Environment Variables Required

Add to your `.env` file:
```env
# Brevo Email Configuration
BREVO_API_KEY=your_brevo_api_key_here
DEFAULT_FROM_EMAIL=noreply@unisinq.app
```

## Get Your Brevo API Key
1. Go to https://www.brevo.com
2. Sign up / Log in to your account
3. Navigate to **Settings > SMTP & API**
4. Copy your **API v3 Key**
5. Add to your `.env` file

## Deployment Steps

### 1. Update Requirements (One-time)
```bash
# Option A: Use the cleaned requirements
pip install -r requirements.txt

# Option B: Fresh install
pip install Django==4.2.8 django-allauth==0.61.1 djangorestframework==3.14.0 \
  psycopg2-binary==2.9.9 brevo-python>=2.0.0 channels==4.0.0 \
  gunicorn==21.2.0 redis==5.0.1 whitenoise==6.6.0
```

### 2. Configure Environment Variables

**For Render.com:**
1. Go to your Render project
2. Click **Environment** tab
3. Add variable:
   ```
   BREVO_API_KEY = your_api_key_here
   ```

**For Railway.app:**
1. Go to your Railway project
2. Click **Variables** tab
3. Add:
   ```
   BREVO_API_KEY = your_api_key_here
   ```

**For Heroku:**
```bash
heroku config:set BREVO_API_KEY=your_api_key_here
```

### 3. Deploy
```bash
git add requirements.txt requirements_UPDATED.txt auth_project/auth_project/settings.py
git commit -m "fix: remove zepto mail, use brevo only"
git push origin main
```

### 4. Verify Email Backend
```bash
# SSH into your deployed instance
# Then run:
python manage.py shell
```

```python
from django.conf import settings
print(f"Email Backend: {settings.EMAIL_BACKEND}")
print(f"Brevo API Key Configured: {bool(settings.BREVO_API_KEY)}")
```

Expected output:
```
Email Backend: accounts.brevo_mail_backend.BrevoMailBackend
Brevo API Key Configured: True
```

## Test Email Delivery

### Via Django Shell
```python
from django.core.mail import send_mail

success = send_mail(
    subject='Test Email from UniSync',
    message='This is a test email from your Brevo backend',
    from_email='noreply@unisinq.app',
    recipient_list=['your-email@example.com'],
)
print(f"Email sent: {success}")
```

### Via OTP Test
1. Go to login page
2. Click "Login with OTP"
3. Enter your email
4. Check email inbox for OTP code
5. If received, Brevo is working ✅

## Troubleshooting

### "Email not received"
1. **Check Brevo API Key** in environment variables
2. **Check email domain** - verify sender domain is authorized in Brevo
3. **Check Brevo logs** at https://www.brevo.com/email/logs/
4. **Check spam folder** for test emails

### "Invalid API Key"
```bash
# Verify the key format (should be long alphanumeric string)
# Re-copy from Brevo dashboard
# Update environment variable
```

### "Backend not initialized"
```bash
# Restart your application after updating .env
# For Render: Re-deploy or manually restart
# For Railway: Kill and restart service
```

## Email Features Enabled
✅ OTP Login (6-digit codes)
✅ Password Reset (reset links)
✅ Notifications (comments, connections)
✅ Project Invitations
✅ Account Verification

## Fallback Options

If Brevo fails, Django will automatically fallback to:
1. Gmail SMTP (if `EMAIL_HOST_USER` configured)
2. Console output (development mode)

## Cost Estimation
**Brevo Pricing:**
- Free: 300 emails/day
- Starter: 10,000 emails/month for $20
- Most university projects fit in free tier

## Support
- Brevo Docs: https://developers.brevo.com/docs
- Brevo Support: https://www.brevo.com/contact/
- UniSync Docs: Check `CODEBASE_COMPLETE_ANALYSIS_2026.md`

---
**Deployment Status:** ✅ Ready to deploy with Brevo email backend
