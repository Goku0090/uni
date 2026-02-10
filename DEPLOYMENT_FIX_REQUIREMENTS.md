# Deployment Fix: ZeptoMail & Invalid Package Dependencies

## Problem
```
ERROR: Could not find a version that satisfies the requirement zeptomail==1.0.0 (from versions: none)
ERROR: No matching distribution found for zeptomail==1.0.0
```

## Root Cause
Your `requirements.txt` contains two non-existent PyPI packages:
1. **`zeptomail==1.0.0`** - Not available on PyPI
2. **`rapidapi==1.0.0`** - Not a valid package name

However, your codebase has a **custom ZeptoMail implementation** that doesn't require a PyPI package.

## Solution

### Option 1: Quick Fix (Recommended)
Use the production requirements file:
```bash
pip install -r requirements_production.txt
```

This file has been cleaned of invalid packages.

### Option 2: Manual Fix
Edit your `requirements.txt` and remove these lines:
```diff
- zeptomail==1.0.0
+ # ZeptoMail backend is custom-implemented (see accounts/zepto_mail_backend.py)

- rapidapi==1.0.0
+ # Using requests library for API calls
```

### Option 3: For Render/Railway Deployment
Update your `Procfile` or deployment config to use the production requirements:
```bash
pip install -r requirements_production.txt
```

## What Changed

### Removed (Non-existent packages)
- ❌ `zeptomail==1.0.0` 
- ❌ `rapidapi==1.0.0`
- ⚠️ `daphne==4.0.0` (optional - commented out)

### Why It's Safe
Your code uses:
- **ZeptoMail**: Custom backend at `accounts/zepto_mail_backend.py` (uses `requests` library)
- **RapidAPI**: Not actually imported anywhere (safe to remove)
- **Daphne**: Optional - Gunicorn can handle WebSockets with proper ASGI config

## Email Backend Options

### Primary Option: Brevo Email
```python
EMAIL_BACKEND = 'accounts.brevo_mail_backend.BrevoMailBackend'
BREVO_API_KEY = 'your-brevo-key'
```

### Fallback Option: Custom ZeptoMail
```python
EMAIL_BACKEND = 'accounts.zepto_mail_backend.ZeptoMailBackend'
ZEPTO_MAIL_API_KEY = 'your-zepto-key'
ZEPTO_MAIL_TOKEN = 'your-zepto-token'
```

### Development Option: Console
```python
EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'
```

## Deployment Steps

### For Render.com
1. Set environment variable in Render dashboard:
   ```
   pip_install_command = pip install -r requirements_production.txt
   ```

2. Or add to `render.yaml`:
   ```yaml
   buildCommand: pip install -r requirements_production.txt
   ```

### For Railway.app
1. Set custom build command:
   ```bash
   pip install -r requirements_production.txt
   ```

### For Heroku
```bash
heroku config:set PIP_REQUIREMENTS_FILE=requirements_production.txt
git push heroku main
```

## Verify Deployment
After deployment, test with:
```bash
python manage.py test accounts
python manage.py send_test_email
```

## Files Updated
- ✅ `requirements.txt` - Cleaned
- ✅ `requirements_UPDATED.txt` - Cleaned  
- ✅ `requirements_production.txt` - New (recommended for deployment)

## Next Steps
1. Delete/backup old requirements files
2. Use `requirements_production.txt` for all deployments
3. Verify email backend in `.env`:
   ```
   EMAIL_BACKEND=accounts.brevo_mail_backend.BrevoMailBackend
   BREVO_API_KEY=xxx
   ```

**You're ready to deploy!** 🚀
