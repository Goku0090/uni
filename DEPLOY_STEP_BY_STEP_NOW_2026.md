# Deploy Step-by-Step (Do This Right Now)

## 🎯 Goal: Deploy to Render.com in 30 Minutes

Let's go live! Follow these steps **exactly**.

---

## ⏰ Timeline

```
Step 1: Prepare Code (5 min)
Step 2: Create render.yaml (5 min)
Step 3: Push to GitHub (2 min)
Step 4: Deploy on Render (10 min)
Step 5: Set Environment Variables (5 min)
Step 6: Create Admin User (3 min)
Step 7: Test (5 min)

Total: 35 minutes
```

---

## Step 1: Prepare Your Code (5 minutes)

### 1.1 Open Terminal

**Windows:** Open PowerShell or Command Prompt
**Mac/Linux:** Open Terminal

```bash
# Navigate to your project
cd e:\login
# Or wherever your project is
```

### 1.2 Verify Code is Clean

```bash
# Check if git is initialized
git log
# Should show commits

# If NOT initialized, do this:
git init
git add .
git commit -m "Initial commit: UniSync"
```

### 1.3 Create .gitignore (if not exists)

```bash
# Check if .gitignore exists
cat .gitignore
# If not, create it:
```

Create file: `.gitignore` in root

```
__pycache__/
*.py[cod]
*$py.class
.Python
venv/
env/
.venv
db.sqlite3
.env
.env.local
.DS_Store
node_modules/
dist/
build/
logs/
media/
staticfiles/
*.egg-info/
.pytest_cache/
.ruff_cache/
```

### 1.4 Commit .gitignore

```bash
git add .gitignore
git commit -m "Add .gitignore"
```

---

## Step 2: Create render.yaml (5 minutes)

### 2.1 Create File

**Location:** Root folder (same level as `backend/` and `frontend/`)
**File name:** `render.yaml`

```bash
# Verify you're in root
pwd  # Should show: /e/login or c:\Users\...\login
ls   # Should show: backend/, frontend/, manage.py (if in backend), etc.
```

### 2.2 Copy Content

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

### 2.3 Verify File Created

```bash
# Check if render.yaml exists
cat render.yaml
# Should show the YAML content
```

---

## Step 3: Push to GitHub (2 minutes)

### 3.1 Initialize GitHub Repo

If you **don't have a GitHub repo yet**:

1. Go to https://github.com/new
2. **Repository name:** `unisync` (or your choice)
3. **Description:** "UniSync - Student collaboration platform"
4. Select **Public** (easier for deployment)
5. **DO NOT** check "Add a README file"
6. **DO NOT** add .gitignore or license
7. Click **"Create repository"**

### 3.2 Push Code to GitHub

```bash
# Add remote
git remote add origin https://github.com/YOUR_USERNAME/unisync.git
# Replace YOUR_USERNAME with your GitHub username

# Rename branch
git branch -M main

# Push code
git push -u origin main
# Will ask for credentials, enter GitHub username & password (or use GitHub CLI)
```

### 3.3 Verify on GitHub

1. Go to https://github.com/YOUR_USERNAME/unisync
2. You should see all your code files
3. Check that `render.yaml` is there ✓

---

## Step 4: Deploy on Render (10 minutes)

### 4.1 Sign Up to Render

1. Go to https://render.com
2. Click **"Sign Up"** (or "Get Started")
3. Choose **"Continue with GitHub"**
4. Click **"Authorize render"**
5. Done ✓

### 4.2 Create Blueprint

1. In Render Dashboard, click **"New +"** button
2. Select **"Blueprint"**
3. You'll see "Select Repository"
4. Choose your repo: **unisync**
5. Click **"Create Blueprint"**

### 4.3 Wait for Build

Render will now build and deploy your app:

```
🔨 Building...
├─ Installing Python packages (1 min)
├─ Collecting static files (30 sec)
├─ Running migrations (1 min)
└─ Starting application (1 min)

🎉 Deployment successful!
```

**This takes 5-10 minutes.** Watch the logs scroll. Don't close this page.

### 4.4 Get Your URL

Once build succeeds, you'll see:

```
https://unisync-xxxxx.onrender.com
```

**Your app is now LIVE!** (but not fully configured yet)

---

## Step 5: Set Environment Variables (5 minutes)

### 5.1 Generate SECRET_KEY

```bash
# In your terminal, run:
python -c "from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())"

# Copy the output (long random string)
# Example: django-insecure-xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx
```

### 5.2 Add to Render

1. In Render Dashboard
2. Click your app name: **unisync**
3. Click **"Environment"** tab
4. Click **"Add Environment Variable"**

Add these variables:

```
Name: SECRET_KEY
Value: [paste the key you just generated]
Click Add
```

```
Name: DEBUG
Value: false
Click Add
```

### 5.3 Check Other Variables

Your app should already have:
- `ALLOWED_HOSTS` (auto-set)
- `DATABASE_URL` (auto-set)
- `REDIS_URL` (auto-set)

**Don't change these!** They're auto-configured by Render.

### 5.4 (Optional) Add Email/OAuth

If you want email or OAuth login to work:

```
BREVO_API_KEY: [your key, if you have one]
GOOGLE_CLIENT_ID: [your ID, if you have one]
GOOGLE_CLIENT_SECRET: [your secret, if you have one]
```

You can skip these for now. Email/OAuth will show errors but app will work.

### 5.5 Deploy Changes

After adding variables:
1. Render auto-redeploys (takes 1-2 minutes)
2. Check Logs to confirm success

---

## Step 6: Create Admin User (3 minutes)

### 6.1 Access Shell

In Render Dashboard:
1. Click your app: **unisync**
2. Click **"Shell"** tab
3. You'll see a terminal prompt

### 6.2 Create Superuser

```bash
# In Render Shell, type:
python backend/manage.py createsuperuser

# It will ask:
# Username: admin
# Email: your@email.com
# Password: [enter strong password, won't show]
# Password (again): [confirm]
# Bypass password validation? y

# Done!
```

### 6.3 Verify

```bash
# Still in shell, run:
python backend/manage.py shell

# Then type:
from django.contrib.auth.models import User
User.objects.all()

# You should see: <QuerySet [<User: admin>]>

# Exit:
exit()
```

---

## Step 7: Test Your App (5 minutes)

### 7.1 Visit Your App

1. Go to: `https://unisync-xxxxx.onrender.com`
2. You should see your **homepage** ✓

### 7.2 Test Login

1. Click **Login**
2. Username: `admin`
3. Password: [the one you set]
4. Click **Login** ✓
5. You're logged in!

### 7.3 Test Features

- [ ] Go to homepage (works?)
- [ ] Try to create a project (works?)
- [ ] Visit admin: `/admin/` (login works?)
- [ ] Check database (data saved?)

### 7.4 Check Logs for Errors

1. In Render Dashboard → **Logs** tab
2. Look for red errors
3. If no errors (all green) = ✅ Success!

---

## 🎉 You're Done!

Your app is now **LIVE** on the internet!

```
✅ App deployed
✅ Database connected
✅ Cache working
✅ Admin user created
✅ Features tested
✅ Ready for users!
```

---

## What's Your App URL?

In Render Dashboard, look for:

```
Name: unisync
Domain: https://unisync-xxxxx.onrender.com
```

**Share this URL** with anyone to let them use your app!

---

## Now What?

### Immediate (Today)

1. **Test more thoroughly**
   - Try all features
   - Create test data
   - Test on phone browser

2. **Share with friends**
   - Send them the URL
   - Get feedback
   - Fix bugs they find

### This Week

1. **Add custom domain** (optional)
   - Buy domain: namecheap.com
   - Point to Render
   - Auto HTTPS

2. **Setup OAuth** (optional)
   - Get Google credentials
   - Add to Render env vars
   - Users can login with Google

3. **Setup Email** (optional)
   - Get Brevo API key
   - Add to Render env vars
   - OTP login will work

### How to Update Your App

```bash
# Make changes locally
# Test with: python manage.py runserver

# Push to GitHub
git add .
git commit -m "Your changes"
git push origin main

# Render automatically redeploys!
# Wait 5 minutes
# Your changes are LIVE
```

---

## Common Issues & Quick Fixes

### Issue: App shows "Error" after deployment

**Fix:**
1. Click app → Logs tab
2. Look for error message
3. Most common:
   - `SECRET_KEY` not set → Add it in Environment
   - Database connection → Wait 2 minutes, auto-retries
   - Missing migration → Render runs `migrate` automatically

### Issue: Static files not loading (CSS broken)

**Fix:**
```bash
# In Render Shell:
python backend/manage.py collectstatic --noinput --clear
```

### Issue: Login doesn't work

**Fix:**
- Clear browser cookies
- Try incognito window
- Check if admin user exists (Step 6)

### Issue: Can't access shell

**Fix:**
- Reload Render page
- Try again
- If still broken, email Render support (they're helpful!)

---

## Verification Checklist

Your app is successfully deployed when:

- [ ] App URL works: `https://unisync-xxxxx.onrender.com`
- [ ] Homepage loads without errors
- [ ] Admin login works (username: admin)
- [ ] Can create new account
- [ ] Can login with new account
- [ ] Can create a project
- [ ] Can navigate pages
- [ ] No red errors in logs

**All checked?** 🎉 **Congratulations! You're live!**

---

## Keep It Running

### Free Tier Works Well If:
- You're learning
- Small number of users
- Testing features
- Prototyping

### Upgrade When:
- App gets 100+ daily users
- Need always-on (no spin down)
- Want better performance
- Need dedicated database

To upgrade:
1. Render Dashboard → Your app
2. Settings → Instance Type
3. Choose higher tier
4. Confirm

---

## Need Help?

### Render Issues
- Check Logs (Dashboard → Logs)
- Read: https://docs.render.com
- Email Render support

### Django Issues
- Check: https://docs.djangoproject.com
- Search error message on Google

### My Deployment Guide Issues
- Read: `DEPLOYMENT_GUIDE_COMPLETE_2026.md`
- Check troubleshooting section

---

## You Did It! 🚀

Your Django app is now:
- ✅ Deployed on Render
- ✅ Live on the internet
- ✅ Running with PostgreSQL
- ✅ Using Redis cache
- ✅ Connected to admin panel
- ✅ Ready for real users

**Share your app URL with others!**

```
https://unisync-xxxxx.onrender.com
```

---

## Next Steps (Optional)

1. **Custom domain** - Make it look professional
2. **OAuth setup** - Let users login with Google
3. **Email setup** - Enable OTP & notifications
4. **Monitoring** - Watch logs & performance
5. **Scale** - Upgrade when needed

---

## Celebrate! 🎊

You just deployed a full-stack Django application!

That's awesome. You should be proud.

Now go share it with the world! 🌍

---

**Questions?** Re-read the relevant section above.
**Still stuck?** Check `DEPLOYMENT_GUIDE_COMPLETE_2026.md`

