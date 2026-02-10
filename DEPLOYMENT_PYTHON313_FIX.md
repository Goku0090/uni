# Deployment Fix: Python 3.13 Compatibility

## Problem
Multiple packages fail to build on Python 3.13:
- ❌ `pandas==2.1.4` - Cython compilation errors
- ❌ `sentry-sdk==1.38.0` - Build issues
- ❌ Other C-extension packages

## Solution

### Option 1: Use Minimal Requirements (Recommended)
```bash
pip install -r requirements.txt
```

This file includes only packages with Python 3.13 wheels (pre-compiled binaries).

**All essential features work:**
- ✅ Django + REST Framework
- ✅ Authentication (OAuth, OTP)
- ✅ WebSockets (real-time updates)
- ✅ Brevo Email (via `requests`)
- ✅ Database (PostgreSQL)
- ✅ File Storage
- ✅ Caching/Redis
- ✅ Message Queues (Celery)

**Removed (Optional):**
- Analytics (pandas)
- Text processing (nltk)
- Error tracking (sentry)
- Development tools

### Option 2: Use Full Requirements (Python 3.11/3.12 only)
```bash
pip install -r requirements-full.txt
```

Only use on Python 3.11 or 3.12, not 3.13.

## Deployment Steps

### For Render.com
1. **Add build command** in `render.yaml`:
   ```yaml
   buildCommand: pip install -r requirements.txt
   ```

2. Or set environment variable in dashboard:
   ```
   PIP_DEFAULT_TIMEOUT=600
   ```

### For Railway.app
1. Set build command:
   ```bash
   pip install -r requirements.txt --timeout=600
   ```

### For Heroku
```bash
heroku config:set PIP_DEFAULT_TIMEOUT=600
git push heroku main
```

## What's Included

**Core Django Stack:**
- Django 4.2.8
- Django REST Framework 3.14.0
- Django Allauth (social login)

**Real-time Features:**
- Channels 4.0.0
- Redis 5.0.1
- Celery (task queue)

**Email & Storage:**
- Requests (Brevo API calls)
- Boto3 + Django Storages (S3)

**Security:**
- CORS headers
- CSRF protection (Django built-in)

## Testing Installation

After installation, verify:
```bash
python manage.py test accounts
python manage.py check
```

Or test in Python shell:
```python
from django.conf import settings
print(f"Database: {settings.DATABASES['default']['ENGINE']}")
print(f"Email Backend: {settings.EMAIL_BACKEND}")
print(f"Channels: {settings.INSTALLED_APPS}")
```

## If You Need Pandas

On Python 3.11/3.12:
```bash
pip install pandas==2.0.3 openpyxl==3.1.2 nltk==3.8.1
```

On Python 3.13:
```bash
# Wait for pandas 2.2.0+ release with Python 3.13 support
# Or use an alternative: polars, dask, etc.
```

## Environment Variables Required

```env
# Django
DEBUG=False
SECRET_KEY=your-secret-key
ALLOWED_HOSTS=your-domain.com

# Database
DATABASE_URL=postgresql://user:pass@host:5432/db

# Email (Brevo)
BREVO_API_KEY=your-brevo-api-key
DEFAULT_FROM_EMAIL=noreply@yourdomain.com

# Redis
REDIS_URL=redis://localhost:6379/0

# AWS S3 (optional)
AWS_ACCESS_KEY_ID=xxx
AWS_SECRET_ACCESS_KEY=xxx
AWS_STORAGE_BUCKET_NAME=your-bucket
```

## Production Checklist

- ✅ Python 3.13 compatible dependencies installed
- ✅ `.env` file configured
- ✅ Database migrated
- ✅ Static files collected
- ✅ Brevo API key set
- ✅ Redis configured
- ✅ Allowed hosts configured

## Troubleshooting

### "ModuleNotFoundError: No module named 'pandas'"
- It's optional. Remove from your code if unused.
- Or install separately on Python 3.11/3.12

### "Email not sending"
- Check `BREVO_API_KEY` in environment
- Verify email domain in Brevo dashboard
- Check OTP functionality (test at login page)

### "WebSocket connection failed"
- Ensure Redis is running
- Check Channels configuration in `settings.py`
- Verify `ASGI_APPLICATION` is set

---

**Deployment Status:** ✅ Ready for Python 3.13 with minimal requirements
