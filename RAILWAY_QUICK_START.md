# Railway Deployment - Quick Start

## Files Ready
✅ `Dockerfile` - Uses Python 3.11
✅ `start.sh` - Runs migrations & starts app
✅ `railway.json` - Railway configuration
✅ `auth_project/requirements.txt` - Dependencies

## Deploy in 3 Steps

### Step 1: Commit & Push
```bash
cd e:/login
git add -A
git commit -m "railway: docker deployment with python 3.11"
git push origin main
```

### Step 2: Create Railway Account
- Go to https://railway.app
- Click **Sign in**
- Choose **GitHub** 
- Authorize Railway

### Step 3: Deploy
1. Click **New Project**
2. Click **Deploy from GitHub repo**
3. Select your repo
4. Click **Deploy**

That's it! Railway will:
1. ✅ Detect `Dockerfile`
2. ✅ Use Python 3.11
3. ✅ Install dependencies
4. ✅ Run migrations
5. ✅ Start server
6. ✅ Get public URL

**Build time:** 3-5 minutes

## Add Database

In Railway Dashboard:

1. Click **Add Service**
2. Select **PostgreSQL**
3. Railway auto-fills `DATABASE_URL` ✓

## Add Environment Variables

Click **Variables** tab, add:

```
DEBUG=False
ALLOWED_HOSTS=*.up.railway.app,yourdomain.com
SECRET_KEY=<generate-new-django-secret-key>
BREVO_API_KEY=<your-brevo-api-key>
DEFAULT_FROM_EMAIL=noreply@yourdomain.com
```

## Test

1. Click public URL in Railway dashboard
2. Should see login page ✓
3. Test OTP email ✓

## How Docker Fixes Everything

```
OLD (Render + Python 3.13):
❌ Python 3.13 forced
❌ Packages can't compile
❌ Build fails

NEW (Railway + Docker + Python 3.11):
✅ Dockerfile specifies Python 3.11
✅ All packages have 3.11 wheels
✅ No compilation needed
✅ Build succeeds in 3-5 minutes
```

## Expected Log

```
=== Building from Dockerfile ===
FROM python:3.11-slim
...
RUN pip install -r auth_project/requirements.txt
Successfully installed Django-4.2.8 ...
...
=== Deployment successful ===
App URL: https://your-app.up.railway.app
```

## Cost

**Free tier covers:**
- First $5/month usage
- Includes 1 web service + 1 database

**Typical cost after free tier:**
- Web service: ~$5/month
- PostgreSQL: ~$5/month
- **Total:** ~$10/month

## If Something Goes Wrong

### 1. Check Logs
Railway Dashboard → Logs tab

Look for errors starting with "ERROR"

### 2. Common Issues

**"No module named 'django'"**
- Requirements didn't install
- Check Docker logs

**"Port already in use"**
- Railway handles this
- Shouldn't happen

**"Database connection failed"**
- Add PostgreSQL service
- Set DATABASE_URL

**"502 Bad Gateway"**
- App crashed
- Check logs for error

### 3. Redeploy
Click **Redeploy** in Railway dashboard

Clears cache and rebuilds.

## Delete & Restart

If you want to completely restart:

1. In Railway Dashboard, delete the project
2. Reconnect GitHub repo
3. Deploy fresh

---

**Ready!** 🚀

```bash
git push origin main
```

Then deploy on Railway. Will work in 3-5 minutes.
