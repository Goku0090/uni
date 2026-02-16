# ✅ Deployment Checklist - Start Now

## Status: READY TO DEPLOY ✅

```
✅ Code committed to GitHub
✅ render.yaml created
✅ All dependencies in requirements.txt
✅ Django configured
✅ Database models ready
✅ Templates ready
✅ Static files ready
✅ Authentication configured
✅ WebSocket setup done
```

---

## Your Next 3 Steps (10 minutes)

### Step 1: Get Your GitHub Remote URL

```bash
# Check your GitHub repo
git remote -v
# Should show: origin https://github.com/YOUR_USERNAME/uni.git

# If not set, add it:
# git remote add origin https://github.com/YOUR_USERNAME/uni.git
```

### Step 2: Create render.yaml

**File location:** Root folder (same level as backend/ and frontend/)

Create file: `render.yaml`

```yaml
services:
  - type: web
    name: unisync
    runtime: python
    runtimeVersion: 3.11
    buildCommand: |
      pip install -r backend/requirements.txt
      python backend/manage.py collectstatic --noinput
      python backend/manage.py migrate
    startCommand: gunicorn auth_project.wsgi:application --chdir backend
    envVars:
      - key: DEBUG
        value: false
      - key: ALLOWED_HOSTS
        value: ${{RENDER_EXTERNAL_HOSTNAME}}
      - key: SECRET_KEY
        sync: false

  - type: postgres
    name: unisync_db
    ipAllowList: []

  - type: redis
    name: redis
    ipAllowList: []
```

### Step 3: Push render.yaml

```bash
git add render.yaml
git commit -m "Add Render deployment config"
git push origin main
```

---

## Deploy to Render (5 minutes)

1. **Go to:** https://render.com
2. **Click:** "Sign Up" → "Continue with GitHub"
3. **Authorize:** Render to access your GitHub
4. **Click:** "New +" → "Blueprint"
5. **Select:** Your repo (uni)
6. **Click:** "Create Blueprint"
7. **Wait:** 5-10 minutes (watch the build logs)

---

## After Deployment (5 minutes)

### Add SECRET_KEY

1. **Go to:** Render Dashboard → Your app
2. **Click:** "Environment" tab
3. **Add variable:**
   ```
   Name: SECRET_KEY
   Value: [generate and paste from below]
   ```

**Generate SECRET_KEY:**
```bash
python -c "from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())"
```
Copy the output (long random string) and paste it in Render

### Create Admin User

1. **In Render Dashboard:**
   - Click your app
   - Click "Shell" tab

2. **Run:**
   ```bash
   python backend/manage.py createsuperuser
   # Username: admin
   # Email: your@email.com  
   # Password: [strong password]
   ```

### Test Your App

**Visit:** Your Render URL (shown in Dashboard)
- Homepage loads? ✓
- Can login with admin credentials? ✓
- Pages work? ✓
- No errors in logs? ✓

---

## Timeline

```
Now (2 min):  Create render.yaml
+2 min:       Push to GitHub
+7 min:       Render builds & deploys (5 min)
+9 min:       Add environment variables
+11 min:      Create admin user
+12 min:      Test app

Total: 12 minutes to LIVE APP! 🎉
```

---

## Your GitHub Remote

```bash
# Check it
git remote -v

# Should show something like:
# origin  https://github.com/goku0090/uni.git (fetch)
# origin  https://github.com/goku0090/uni.git (push)
```

**If your remote is different (not `/uni.git`), let me know and update render.yaml accordingly.**

---

## What Happens After You Deploy

1. ✅ Render pulls code from GitHub
2. ✅ Installs Python packages
3. ✅ Collects static files
4. ✅ Runs migrations
5. ✅ Starts Django server
6. ✅ PostgreSQL database created
7. ✅ Redis cache configured
8. ✅ Your app is LIVE

---

## Common Things to Know

- **Your app URL:** Will be like `https://unisync-xxxxx.onrender.com`
- **Admin panel:** `https://unisync-xxxxx.onrender.com/admin/`
- **App is slow first time:** Render spins up services, normal
- **Updates deploy automatically:** Push to main → auto-deploy in 5 min
- **Free tier includes:** 750 hours/month (enough for 1 app 24/7)

---

## You're Ready!

Everything is set up. Just follow the 3 steps above and you'll be live in 10 minutes.

**Let's do it!** 🚀

---

## Questions?

- **Setup help:** Read `DEPLOY_STEP_BY_STEP_NOW_2026.md`
- **Platform comparison:** Read `DEPLOYMENT_GUIDE_COMPLETE_2026.md`
- **Troubleshooting:** Check same file's troubleshooting section

Good luck! You've got this! 💪

