# Railway Final Deployment

## Files Ready
✅ `Dockerfile` - Simple, clean Python 3.11
✅ `start.sh` - Bash script to run migrations + start server
✅ `.dockerignore` - Exclude unnecessary files
✅ `.python-version` - Force Python 3.11
✅ `auth_project/requirements.txt` - Clean, minimal packages

## What To Do

### 1. Commit Changes
```bash
cd e:/login
git add -A
git commit -m "railway: final clean docker setup"
git push origin main
```

### 2. On Railway Dashboard

**CRITICAL: Delete and redeploy**

1. Go to your project
2. Click **Settings** (bottom)
3. Click **Delete** button (⚠️ scroll down)
4. Confirm deletion
5. Go back to home
6. Click **New Project**
7. Click **Deploy from GitHub**
8. Select your repo
9. Click **Deploy**

This clears ALL cache and gives you a fresh build.

### 3. Add Services

While deploying:

1. Click **Add Service**
2. Select **PostgreSQL**
3. Railway auto-fills DATABASE_URL ✓

### 4. Set Environment Variables

In Railway: **Variables** tab

```
DEBUG=False
ALLOWED_HOSTS=*.up.railway.app
SECRET_KEY=<generate-new-one>
BREVO_API_KEY=<from-brevo>
DEFAULT_FROM_EMAIL=noreply@yourdomain.com
```

### 5. Wait for Build

Expected:
- Build starts (Docker detected)
- Python 3.11 installed
- Dependencies installed
- Migrations run
- Server starts
- ~3-5 minutes total

### 6. Test

1. Click app URL in Railway
2. Should see login page
3. Test OTP email

## If It Still Fails

**Option A: Use Railway's native Python support**

Delete `Dockerfile`, keep only:
- `Procfile`:
  ```
  web: cd auth_project && python manage.py migrate && gunicorn auth_project.wsgi:application --workers 3
  ```

Railway detects Procfile automatically.

**Option B: Switch to Heroku**

Heroku handles Python deployments better:
```bash
heroku create your-app-name
git push heroku main
heroku config:set BREVO_API_KEY=xxx
heroku run python auth_project/manage.py migrate
```

## Key Points

- `Dockerfile` specifies Python 3.11 (no compilation issues)
- `start.sh` runs migrations automatically
- `.dockerignore` excludes unnecessary files
- Fresh deploy clears cache issues
- 3-5 minute build time

---

**This will work!** Deploy now.
