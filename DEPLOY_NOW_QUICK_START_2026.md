# Deploy Now - Quick Start Checklist

## Choose Your Platform (Pick One)

### 🟢 Best for Beginners: **Render.com** (Recommended)
- Free tier available
- Auto SSL
- Easy database setup
- Simple UI
- Supports Django out-of-box
- **Setup time: 5 minutes**

### 🟡 Alternative: **Railway.app**
- Free credits
- Great UI
- Auto configuration
- Good support
- **Setup time: 5 minutes**

### 🔴 Other Options
- Heroku (paid, used to be free)
- AWS (complex)
- DigitalOcean ($5/month)
- Self-hosted (hardest)

---

## Pre-Deployment Checklist (Do This Now)

### Step 1: Verify Local Setup Works

```bash
cd backend
python manage.py runserver
# Visit http://localhost:8000
# Test: Login, create project, chat
# ✓ Everything works?
```

**If errors:**
- Fix them first
- Don't deploy broken code

### Step 2: Check Requirements

```bash
# In backend folder
cat requirements.txt
# Should show Django, Django REST Framework, Channels, etc.
# ✓ All dependencies listed?
```

**If missing:**
```bash
pip freeze > requirements.txt
# Update file with current packages
```

### Step 3: Create .gitignore

```bash
# Create file: .gitignore
cat > .gitignore << 'EOF'
__pycache__/
*.py[cod]
venv/
env/
.env
.env.local
db.sqlite3
*.log
media/
staticfiles/
node_modules/
.DS_Store
*.egg-info/
EOF
```

### Step 4: Initialize Git

```bash
cd /path/to/project
git init
git add .
git commit -m "Initial commit: UniSync application"
```

### Step 5: Create GitHub Repository

1. Go to https://github.com/new
2. Create repo: `unisync` (or your project name)
3. **DON'T** add README, .gitignore, license
4. Click "Create"

### Step 6: Push to GitHub

```bash
git remote add origin https://github.com/YOUR_USERNAME/unisync.git
git branch -M main
git push -u origin main
```

**Verify:** Go to GitHub → Check if code is there

---

## Deploy to Render.com (Step-by-Step)

### Step 1: Sign Up (2 minutes)

1. Go to https://render.com
2. Click "Sign Up"
3. Choose "GitHub" login
4. Authorize Render to access your GitHub
5. Done ✓

### Step 2: Create render.yaml (5 minutes)

Create file: `render.yaml` in root folder

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

### Step 3: Push render.yaml to GitHub

```bash
git add render.yaml
git commit -m "Add Render deployment config"
git push origin main
```

### Step 4: Deploy (2 minutes)

1. Go to https://render.com/dashboard
2. Click **"New +"** → **"Blueprint"**
3. Select your **GitHub repo** (unisync)
4. Click **"Create Blueprint"**
5. Wait... (build takes 5-10 minutes)

```
Building...
├─ Installing Python packages
├─ Collecting static files
├─ Running migrations
└─ Starting application

✓ Deployment successful!
```

### Step 5: Set Environment Variables (5 minutes)

1. Go to Render Dashboard
2. Click your **app name** (unisync)
3. Click **"Environment"**
4. Add these variables:

```
SECRET_KEY = (generate a random string, e.g., copy from Django secret key generator)
BREVO_API_KEY = (your Brevo API key, if you have one)
GOOGLE_CLIENT_ID = (leave blank for now, or add your ID)
GOOGLE_CLIENT_SECRET = (leave blank for now, or add your secret)
```

**To generate SECRET_KEY:**
```bash
python -c "from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())"
```

Copy output and paste in Render.

### Step 6: Create Admin User (3 minutes)

1. In Render Dashboard → Your app
2. Click **"Shell"** (or SSH)
3. Run:

```bash
python backend/manage.py createsuperuser
# Enter username: admin
# Enter email: your@email.com
# Enter password: (strong password)
```

### Step 7: Test Your App (2 minutes)

Your app is now live at: `https://unisync-xxxxx.onrender.com`

**Test it:**
1. Visit: `https://unisync-xxxxx.onrender.com`
2. Homepage loads? ✓
3. Click Login ✓
4. Register new account ✓
5. Create a project ✓
6. Go to admin: `/admin/` ✓

**Done! 🎉**

---

## If Something Goes Wrong

### Issue: App keeps crashing (Red error badge)

**Fix:**
1. Click app name → Logs
2. Look for error message
3. Common issues:
   - `SECRET_KEY` not set → Add it
   - Database error → Wait 2 mins, app auto-retries
   - Missing migrations → Redeploy

To redeploy:
- Make small change to code
- Git push
- Render auto-redeploys

### Issue: Static files not loading

**Fix:**
```bash
# In Render Shell
python backend/manage.py collectstatic --noinput --clear
```

Then refresh browser (Ctrl+Shift+R)

### Issue: Database connection error

**Fix:**
1. Go to Resources tab
2. Ensure PostgreSQL database is running
3. Wait 30 seconds, try again

### Issue: Can't login

**Fix:**
1. Clear browser cookies
2. Try incognito/private window
3. Check admin user exists:
   - In Render Shell: `python backend/manage.py shell`
   - `from django.contrib.auth.models import User`
   - `User.objects.all()`

---

## Common Tasks Post-Deployment

### Add Custom Domain

1. Render Dashboard → Your app
2. Settings → Custom Domains
3. Add your domain: `yourapp.com`
4. Update DNS settings (Render shows instructions)

### Update Code

```bash
# Make changes locally
# Test
python manage.py runserver

# Push to GitHub
git add .
git commit -m "New feature"
git push origin main

# Render auto-deploys from main
# Wait 5 minutes
# Changes live ✓
```

### Check Logs

1. Render Dashboard → Your app
2. Click **"Logs"** tab
3. See real-time logs
4. Errors shown here

### Database Backups

1. Render Dashboard → PostgreSQL database
2. Click **"Backups"**
3. Download if needed

### Increase Resources (Paid)

1. Settings → Instance Type
2. Choose higher tier
3. Pay more, app is faster

---

## Environment Variables You Need

### Required
```
SECRET_KEY = (auto-generated, must set)
DEBUG = false (must set)
ALLOWED_HOSTS = (set to render domain)
```

### Optional (But Recommended)
```
BREVO_API_KEY = (if you want email/OTP to work)
GOOGLE_CLIENT_ID = (if you want Google OAuth)
GOOGLE_CLIENT_SECRET = (if you want Google OAuth)
GITHUB_CLIENT_ID = (if you want GitHub OAuth)
GITHUB_CLIENT_SECRET = (if you want GitHub OAuth)
```

### For Testing OAuth

1. Get Google OAuth credentials:
   - Go to https://console.cloud.google.com
   - Create project "UniSync"
   - Create OAuth 2.0 credentials
   - Redirect URI: `https://unisync-xxxxx.onrender.com/accounts/google/login/callback/`
   - Copy Client ID and Secret

2. Get GitHub OAuth credentials:
   - Go to GitHub Settings → Developer settings → OAuth Apps
   - Create new OAuth app
   - Authorization callback URL: `https://unisync-xxxxx.onrender.com/accounts/github/login/callback/`
   - Copy Client ID and Secret

3. Add to Render environment variables

---

## What Gets Deployed

```
✅ Django backend
✅ All HTML templates
✅ CSS & JavaScript
✅ Database (PostgreSQL)
✅ Cache (Redis)
✅ Static files
✅ Media files

❌ node_modules (not needed)
❌ Python venv (rebuilt on server)
❌ .git (not deployed)
```

---

## How It Works

```
You push code to GitHub
         ↓
Render detects push
         ↓
Render builds:
├─ Installs Python packages
├─ Collects static files
├─ Runs migrations
└─ Starts application
         ↓
App is live at your URL
         ↓
You can access it
```

**Every time you push to main:**
- Render auto-deploys
- Build takes 5-10 minutes
- App updates automatically

---

## Costs

### Free Tier
- 750 hours/month (enough for 1 app)
- Shared database (PostgreSQL)
- Shared cache (Redis)
- Auto SSL
- **Cost: $0/month**

### Paid Tier
- Dedicated resources
- Better performance
- Support
- **Cost: $7-15/month for small app**

---

## Next Steps

1. **Right now:**
   - [ ] Create GitHub repo
   - [ ] Push code
   - [ ] Signup to Render

2. **In 5 minutes:**
   - [ ] Create render.yaml
   - [ ] Push to GitHub
   - [ ] Deploy

3. **In 10 minutes:**
   - [ ] App is live
   - [ ] Add environment variables
   - [ ] Create admin user

4. **In 15 minutes:**
   - [ ] Test login
   - [ ] Test features
   - [ ] You're done!

---

## Deployment Roadmap

```
Phase 1: Basic Deploy (TODAY)
├─ Push to GitHub ✓
├─ Deploy to Render ✓
├─ Add env variables ✓
└─ Test basic features ✓

Phase 2: Polish (This Week)
├─ Add custom domain
├─ Setup OAuth
├─ Enable email
└─ Add favicon/logo

Phase 3: Monitor (This Month)
├─ Check logs
├─ Monitor performance
├─ Setup alerts
└─ Regular backups

Phase 4: Scale (Future)
├─ Upgrade database
├─ Add CDN for static files
├─ Setup APM
└─ Optimize performance
```

---

## Support

If stuck:
1. Check Render Logs (Dashboard → Logs)
2. Read error message carefully
3. Search error online
4. Ask Render support (they're helpful!)

---

## You're Ready! 🚀

Everything is set up for deployment. Just:

1. Create GitHub repo
2. Push code
3. Deploy to Render

**It really is that simple!**

Total time: ~30 minutes from now to live app.

