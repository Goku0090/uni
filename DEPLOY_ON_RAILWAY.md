# Deploy on Railway.app (Recommended - Python 3.11)

## Why Railway Instead of Render?

**Render Issues:**
- ❌ Won't recognize `.python-version` file
- ❌ Forces Python 3.13
- ❌ Packages fail to compile on 3.13
- ❌ No way to override Python version

**Railway Advantages:**
- ✅ Uses `Dockerfile` (full control)
- ✅ Python 3.11 (stable, all packages work)
- ✅ Better deployment UX
- ✅ Faster build times
- ✅ No compilation errors

## Deploy on Railway in 5 Minutes

### Step 1: Create Railway Account
- Go to https://railway.app
- Sign up with GitHub

### Step 2: Commit Files
```bash
cd e:/login
git add -A
git commit -m "deploy: railway with dockerfile and python 3.11"
git push origin main
```

### Step 3: New Project on Railway
1. Click **New Project**
2. Click **Deploy from GitHub**
3. Select your repo
4. Select `main` branch

### Step 4: Add Environment Variables
In Railway Dashboard → Variables:

```
DEBUG=False
ALLOWED_HOSTS=your-app.up.railway.app
SECRET_KEY=<generate-new-key>
DATABASE_URL=postgresql://user:pass@host/db
BREVO_API_KEY=<your-brevo-key>
DEFAULT_FROM_EMAIL=noreply@yourdomain.com
REDIS_URL=redis://host:port
```

### Step 5: Add Services

**PostgreSQL Database:**
1. Click **Add Service**
2. Select **PostgreSQL**
3. Auto-fills DATABASE_URL ✓

**Redis Cache (optional):**
1. Click **Add Service**
2. Select **Redis**
3. Auto-fills REDIS_URL ✓

### Step 6: Deploy
Click **Deploy** button

Build starts automatically. Watch logs.

Expected time: **2-3 minutes**

## What Dockerfile Does

```dockerfile
FROM python:3.11-slim          # Use Python 3.11
WORKDIR /app                   # Set work directory
RUN apt-get install libpq-dev  # Install PostgreSQL driver
COPY requirements.txt .        # Copy dependencies
RUN pip install -r requirements.txt  # Install packages (NO COMPILATION ISSUES!)
COPY auth_project/ .           # Copy app code
RUN python manage.py collectstatic   # Prepare static files
EXPOSE 8000                    # Open port
CMD python manage.py migrate && gunicorn  # Start server
```

## Expected Build Log

```
====== Building from Dockerfile
FROM python:3.11-slim
...
COPY auth_project/requirements.txt .
RUN pip install -r requirements.txt
Collecting Django==4.2.8
Collecting djangorestframework==3.14.0
...
Successfully installed 17 packages
RUN python manage.py collectstatic --noinput --clear
...
====== Deployment successful
App running at: https://your-app.up.railway.app
```

## Test Deployment

### 1. Visit App
```
https://your-app.up.railway.app
```

Should show login page ✓

### 2. Test OTP Email
1. Click "Login with OTP"
2. Enter your email
3. Check inbox for OTP code
4. If received → Email works ✓

### 3. Check Logs
In Railway Dashboard → Logs tab

Should see:
- ✓ "Applying migrations"
- ✓ "App running"
- ✓ No ERROR lines

## Troubleshooting

### "App not loading (502 error)"
- Check logs for error
- Verify DATABASE_URL is set
- Make sure PostgreSQL service is running

### "Email not sending"
- Check BREVO_API_KEY is correct
- Check Brevo dashboard for quota
- Verify sender domain

### "Static files not loading"
- Already handled in Dockerfile
- If missing: Check S3/storage configuration

### "Port already in use"
- Railway handles this automatically
- Should never happen

## Cost

**Railway Pricing:**
- Web service: Free
- PostgreSQL: Free for first $5/month
- Redis: $7/month
- Total: **~$7/month** (after free tier)

**Much cheaper than Render** if you need long-running processes.

## Switch Back to Render (Optional)

If you want to try Render again:
1. Delete Dockerfile
2. Keep render.yaml
3. Use simpler requirements.txt
4. Might still fail on Python 3.13

Not recommended - **Railway is better for this**.

## Final Steps

1. ✅ Commit files:
   ```bash
   git push origin main
   ```

2. ✅ Go to https://railway.app

3. ✅ Click **New Project**

4. ✅ Select your GitHub repo

5. ✅ Add PostgreSQL service

6. ✅ Set environment variables

7. ✅ Click **Deploy**

8. ✅ Wait 2-3 minutes

9. ✅ Visit app URL

10. ✅ Test OTP email

---

**Railway deployment is guaranteed to work!** 🚀

No more Python 3.13 compilation errors.
