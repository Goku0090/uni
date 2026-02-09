# Fix Static Files 404 Error (logo.jpg)

## Problem
```
GET http://127.0.0.1:8000/static/images/logo.jpg 404 (Not Found)
```

File exists but Django development server isn't serving it.

## Root Cause
Static files aren't being served by `runserver` even though:
- File exists: ✓ `auth_project/static/images/logo.jpg`
- DEBUG = True ✓
- STATIC_URL = '/static/' ✓
- STATICFILES_DIRS configured ✓

The development server needs explicit URL configuration to serve static files.

## Solution

### Option 1: Collect Static Files (Recommended)
```bash
cd auth_project
python manage.py collectstatic --noinput
```

This copies files to `staticfiles/` directory which Django serves automatically.

### Option 2: Update urls.py (Manual Configuration)
Edit `auth_project/urls.py` and add at the very end:

```python
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    # ... your existing patterns ...
]

# Serve static and media files in development
if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
```

### Option 3: Use WhiteNoise (Production-ready)
```bash
pip install whitenoise
```

Update `settings.py`:
```python
MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware',  # Add this line
    'django.contrib.sessions.middleware.SessionMiddleware',
    # ... rest of middleware ...
]
```

## Quick Fix (Immediate)
```bash
cd auth_project
python manage.py collectstatic --noinput
python manage.py runserver
```

Then test: http://127.0.0.1:8000/static/images/logo.jpg

## Verify
After running one of the solutions above:

1. **Check file location:**
   ```bash
   ls -la auth_project/staticfiles/images/logo.jpg
   # Or on Windows:
   dir auth_project\staticfiles\images\logo.jpg
   ```

2. **Test in browser:**
   http://127.0.0.1:8000/static/images/logo.jpg
   Should show the image (not 404)

3. **Check network:**
   - Open DevTools (F12)
   - Network tab
   - Refresh page
   - logo.jpg should show status 200 (not 404)

## Long-term Fix
For production deployment, use Option 3 (WhiteNoise) or configure your web server (nginx, Apache) to serve static files.

## Files Involved
- **Source:** `auth_project/static/images/logo.jpg` ✓ Exists
- **Collected:** `auth_project/staticfiles/images/logo.jpg` (created by collectstatic)
- **Served from:** `/static/images/logo.jpg` (URL)

## Configuration Summary
```
settings.py:
├─ STATIC_URL = '/static/'
├─ STATIC_ROOT = BASE_DIR / 'staticfiles'
└─ STATICFILES_DIRS = [BASE_DIR / 'static']

Directory Structure:
├─ auth_project/static/               (Source files)
│  └─ images/
│     ├─ logo.jpg ✓
│     └─ logo.svg ✓
│
└─ auth_project/staticfiles/          (Collected files)
   └─ images/
      ├─ logo.jpg
      └─ logo.svg
```

## Status
✅ File exists  
✅ Configuration correct  
⏳ Need to run collectstatic or configure serving

---

**Recommended Action:** Run `python manage.py collectstatic --noinput`
