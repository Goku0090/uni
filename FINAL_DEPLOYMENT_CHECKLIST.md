# Final Deployment Checklist for Render

## Files Ready ✅
- ✅ `render.yaml` - Uses Python 3.12
- ✅ `requirements.txt` - Cleaned & optimized
- ✅ `auth_project/wsgi.py` - Configured
- ✅ `auth_project/settings.py` - Email backend set

## Before Deploying

### 1. Push Files to GitHub
```bash
cd e:/login
git add -A
git commit -m "feat: deployment-ready with Python 3.12 and cleaned requirements"
git push origin main
```

### 2. Set Environment Variables on Render

Go to **Render Dashboard → Your Project → Settings → Environment**

Add these variables:

```env
# Django Configuration
DEBUG=False
ALLOWED_HOSTS=your-app-name.onrender.com,yourdomain.com
SECRET_KEY=your-secret-key-change-this

# Database (Render PostgreSQL)
DATABASE_URL=postgresql://user:password@host:port/database

# Email (Brevo)
BREVO_API_KEY=your-brevo-api-key-from-brevo.com
DEFAULT_FROM_EMAIL=noreply@yourdomain.com

# Redis (if using Render Redis)
REDIS_URL=redis://user:password@host:port

# AWS S3 (optional, for file uploads)
AWS_ACCESS_KEY_ID=xxx
AWS_SECRET_ACCESS_KEY=xxx
AWS_STORAGE_BUCKET_NAME=your-bucket-name

# Python
PYTHON_VERSION=3.12
PIP_DEFAULT_TIMEOUT=600
PYTHONUNBUFFERED=1
```

### 3. Get Your Brevo API Key

1. Go to https://www.brevo.com
2. Log in to your account
3. Go to **Settings → SMTP & API**
4. Copy **API v3 Key**
5. Paste into Render environment: `BREVO_API_KEY`

### 4. Generate Django Secret Key

```bash
python -c "from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())"
```

Copy the output and paste into Render: `SECRET_KEY`

### 5. Configure Database

**Option A: Use Render PostgreSQL**
1. In Render, create new **PostgreSQL** database
2. Copy connection string
3. Set `DATABASE_URL` in environment

**Option B: Use External PostgreSQL**
- Set `DATABASE_URL` directly

### 6. Deploy

Click **Deploy** in Render Dashboard

Watch the logs:
- Should see "Building..." → "Deploying..." → "Running" ✅
- Install time: ~3-5 minutes
- **NOT** 30+ minutes (which would indicate Python 3.13 issue)

## During Deployment

Expected output:
```
====== Building on Python-3.12
...
Collecting Django==4.2.8
...
Successfully installed ... (all packages)

====== Running migrations
...
Operations to perform:
  Apply all migrations: ...

====== Collecting static files
...

====== Web server starting
Listening on port...
```

## After Deployment

### 1. Test App
```
Visit: https://your-app-name.onrender.com
```

Should see your login page ✅

### 2. Test OTP Email
1. Go to login page
2. Click "Login with OTP"
3. Enter your email
4. Check inbox for OTP code
5. If received → Email works ✅

### 3. Check Logs
In Render Dashboard, check logs for errors:
- Should see no "ERROR" lines
- Occasional "WARNING" is OK

## Troubleshooting

### "Build Failed"
- Check if `render.yaml` is in root directory
- Check if Python version is 3.12
- Check `requirements.txt` exists

### "Email not sending"
- Verify `BREVO_API_KEY` is set correctly
- Check Brevo dashboard for quota limits
- Check spam folder for test emails

### "Database connection failed"
- Check `DATABASE_URL` is correct
- Verify PostgreSQL is running
- Check firewall/security groups

### "Static files not loading"
- Run: `python manage.py collectstatic --noinput`
- Check `STATIC_ROOT` in settings.py
- May need to set `WHITENOISE_USE_FINDERS=True`

### "ModuleNotFoundError"
- Check package is in `requirements.txt`
- Redeploy (Render caches old builds)
- Check Python version is 3.12

## Production Monitoring

### Enable Error Tracking
Uncomment in `requirements-full.txt`:
```bash
pip install sentry-sdk
```

Add to environment:
```env
SENTRY_DSN=your-sentry-dsn
```

### Enable Logging
In `settings.py`, configure logging to track errors.

### Monitor Email Delivery
Check Brevo dashboard at https://www.brevo.com/statistics/

## Rollback Plan

If deployment fails:

1. Revert git commit:
   ```bash
   git revert HEAD
   git push origin main
   ```

2. Render will auto-redeploy previous version

3. Check logs to find the issue

## Success Indicators

✅ App loads without 500 error
✅ Login page displays
✅ OTP email sends
✅ Can create account/project
✅ WebSocket connections working (check browser console)
✅ Real-time updates show

## Estimated Costs

**Render (Free Tier):**
- Web service: Free
- PostgreSQL: 90-day free, then $7/month
- Redis: Free up to 100MB

**Brevo Email:**
- Free: 300 emails/day
- Paid: $20/month for 10,000/month

**Total**: ~$27/month after free trials

---

**Ready to deploy!** 🚀

Push your changes and click Deploy on Render.
