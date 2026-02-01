# 🚀 START YOUR DEPLOYMENT HERE

**Welcome!** Your UniSync application is ready to deploy on Render and Railway.

This document will guide you through the entire process in simple steps.

---

## What is UniSync?

A modern student collaboration platform with:
- User authentication (email + OTP)
- Student profiles
- Project management
- Real-time messaging
- Notifications
- Social features

---

## Choose Your Platform

### Option A: Deploy to BOTH (Recommended) ⭐⭐⭐
- Start with Railway (free $5/month credit)
- Then deploy to Render (for production)
- Both auto-update from GitHub

**Time needed:** ~2 hours

### Option B: Render Only (Stable & Professional)
- Industry standard choice
- $12/month minimum
- Excellent support
- Used by major companies

**Time needed:** ~1 hour

### Option C: Railway Only (Fast & Modern)
- $5/month free credit
- Faster deployments
- Growing platform
- Good for prototyping

**Time needed:** ~1 hour

---

## Before You Start (30 minutes)

You need to get credentials from these services:

### 1. Email Service - Brevo
**Get your API key in 5 minutes:**
1. Go to https://www.brevo.com
2. Sign up (free)
3. Go to Settings → API Keys
4. Click "Create"
5. Copy the API key
6. Save it: `BREVO_API_KEY`

### 2. Google OAuth
**Get credentials in 10 minutes:**
1. Go to https://console.cloud.google.com
2. Click "New Project" → Name it "UniSync"
3. Search for "Google+ API" → Enable it
4. Go to "Credentials" → "Create Credentials" → "OAuth 2.0 Client ID"
5. Application Type: "Web application"
6. Authorized JavaScript origins: 
   ```
   https://yourdomain.onrender.com
   https://yourdomain.up.railway.app
   ```
7. Authorized redirect URIs:
   ```
   https://yourdomain.onrender.com/accounts/google/login/callback/
   https://yourdomain.up.railway.app/accounts/google/login/callback/
   ```
8. Copy: `Client ID` and `Client Secret`
9. Save them: `GOOGLE_CLIENT_ID` and `GOOGLE_CLIENT_SECRET`

### 3. GitHub OAuth
**Get credentials in 10 minutes:**
1. Go to GitHub → Settings → Developer settings → OAuth Apps
2. Click "New OAuth App"
3. Fill in:
   - App name: "UniSync"
   - Homepage URL: "https://yourdomain.com"
   - Authorization callback URLs:
     ```
     https://yourdomain.onrender.com/accounts/github/login/callback/
     https://yourdomain.up.railway.app/accounts/github/login/callback/
     ```
4. Copy: `Client ID` and `Client Secret`
5. Save them: `GITHUB_CLIENT_ID` and `GITHUB_CLIENT_SECRET`

### 4. RapidAPI
**Get key in 5 minutes:**
1. Go to https://rapidapi.com
2. Sign up
3. Search for "Universities List"
4. Click "Subscribe" (free tier available)
5. Copy your API Key
6. Save it: `RAPIDAPI_KEY`

---

## Your Environment Variables

**You'll need these values ready:**

```
DEBUG=False
SECRET_KEY=<generate below>
ALLOWED_HOSTS=yourdomain.com,yourdomain.onrender.com,yourdomain.up.railway.app

BREVO_API_KEY=<your-brevo-key>
DEFAULT_FROM_EMAIL=noreply@yourdomain.com

GOOGLE_CLIENT_ID=<your-google-id>
GOOGLE_CLIENT_SECRET=<your-google-secret>

GITHUB_CLIENT_ID=<your-github-id>
GITHUB_CLIENT_SECRET=<your-github-secret>

RAPIDAPI_KEY=<your-rapidapi-key>

SECURE_SSL_REDIRECT=True
SESSION_COOKIE_SECURE=True
CSRF_COOKIE_SECURE=True
```

### Generate SECRET_KEY

Open Python (or Python terminal):
```python
from django.core.management.utils import get_random_secret_key
print(get_random_secret_key())
```

Copy the output → that's your `SECRET_KEY`

---

## STEP 1: Deploy to Render (10 minutes)

### 1.1 Create Render Account
1. Go to https://render.com
2. Click "Sign up"
3. Click "Continue with GitHub"
4. Authorize Render

### 1.2 Connect Repository
1. Click "New Web Service"
2. Click "Connect a repository"
3. Select "uni_sync"
4. Click "Connect"

### 1.3 Configure Service
1. **Name:** `unisync`
2. **Environment:** Python
3. **Plan:** Starter (recommended) or Free
4. **Branch:** main
5. **Build Command:**
   ```
   pip install -r auth_project/requirements.txt && python auth_project/manage.py collectstatic --noinput
   ```
6. **Start Command:**
   ```
   gunicorn auth_project.wsgi:application --bind 0.0.0.0:10000
   ```

### 1.4 Create Database
1. Click "New" → "PostgreSQL"
2. **Name:** `unisync-db`
3. Same region as web service
4. Click "Create Database"

### 1.5 Add Environment Variables
In Web Service, click "Environment":
```
DEBUG=False
SECRET_KEY=<your-key>
ALLOWED_HOSTS=unisync.onrender.com,yourdomain.com
BREVO_API_KEY=<your-key>
GOOGLE_CLIENT_ID=<your-id>
GOOGLE_CLIENT_SECRET=<your-secret>
GITHUB_CLIENT_ID=<your-id>
GITHUB_CLIENT_SECRET=<your-secret>
RAPIDAPI_KEY=<your-key>
DEFAULT_FROM_EMAIL=noreply@yourdomain.com
SECURE_SSL_REDIRECT=True
SESSION_COOKIE_SECURE=True
CSRF_COOKIE_SECURE=True
```

### 1.6 Deploy!
1. Click "Create Web Service"
2. Watch the build in "Logs"
3. When done, you'll see a URL like: `unisync.onrender.com`

### 1.7 Run Initial Setup
1. Click Web Service → "Shell"
2. Run these commands:
   ```bash
   python auth_project/manage.py migrate
   python auth_project/manage.py createsuperuser
   python auth_project/manage.py collectstatic --noinput
   ```
3. For createsuperuser:
   - Username: `admin`
   - Email: your email
   - Password: something secure

### 1.8 Test It!
1. Go to your Render URL: `https://unisync.onrender.com`
2. Try to register
3. Check email for OTP
4. Verify you can login

**✅ Render deployment done!**

---

## STEP 2: Deploy to Railway (10 minutes)

### 2.1 Create Railway Account
1. Go to https://railway.app
2. Click "Get Started"
3. Click "Continue with GitHub"
4. Authorize Railway

### 2.2 Create New Project
1. Click "New Project"
2. Click "Deploy from GitHub repo"
3. Select "uni_sync"
4. Railway starts building!

### 2.3 Add PostgreSQL
1. Click "Add"
2. Select "PostgreSQL"
3. Railway auto-creates database

### 2.4 Add Environment Variables
1. Click "Variables" tab
2. Add each variable:
```
DEBUG=False
SECRET_KEY=<your-key>
ALLOWED_HOSTS=*.railway.app,yourdomain.com
BREVO_API_KEY=<your-key>
GOOGLE_CLIENT_ID=<your-id>
GOOGLE_CLIENT_SECRET=<your-secret>
GITHUB_CLIENT_ID=<your-id>
GITHUB_CLIENT_SECRET=<your-secret>
RAPIDAPI_KEY=<your-key>
DEFAULT_FROM_EMAIL=noreply@yourdomain.com
SECURE_SSL_REDIRECT=True
SESSION_COOKIE_SECURE=True
CSRF_COOKIE_SECURE=True
```

### 2.5 Railway Deploys Automatically
1. Watch the deployment in "Logs"
2. When done, go to "Settings" → "Domains"
3. You'll see your Railway domain

### 2.6 Run Initial Setup
1. Click Web Service → "Shell"
2. Run these commands:
   ```bash
   python auth_project/manage.py migrate
   python auth_project/manage.py createsuperuser
   python auth_project/manage.py collectstatic --noinput
   ```

### 2.7 Test It!
1. Get your Railway domain from Settings → Domains
2. Visit that URL in browser
3. Try to register
4. Check email for OTP
5. Verify you can login

**✅ Railway deployment done!**

---

## STEP 3: Configure Admin (5 minutes)

For each deployment (Render & Railway):

1. Go to `/admin`
   - Example: `https://unisync.onrender.com/admin`
   
2. Login with your superuser credentials

3. Go to **Sites**
   - Change domain to your actual domain
   - Click "Save"

4. Go to **Social Applications**
   - Click "Add"
   - Provider: Google
   - Name: Google
   - Client ID: `<your-google-client-id>`
   - Secret: `<your-google-client-secret>`
   - Sites: Select your site
   - Click "Save"

5. Add GitHub OAuth too
   - Click "Add"
   - Provider: GitHub
   - Name: GitHub
   - Client ID: `<your-github-client-id>`
   - Secret: `<your-github-client-secret>`
   - Sites: Select your site
   - Click "Save"

---

## VERIFY EVERYTHING WORKS

### Check These Features

**Registration & Login**
- [ ] Click "Register"
- [ ] Enter email and password
- [ ] Request OTP
- [ ] Check email for OTP code
- [ ] Paste OTP code
- [ ] Login successful?

**Profile**
- [ ] Click on profile
- [ ] Edit profile
- [ ] Upload profile picture
- [ ] Save changes
- [ ] Picture appears?

**Projects**
- [ ] Click "Post Project"
- [ ] Create test project
- [ ] Project appears in feed?
- [ ] Can like/comment?

**Messaging**
- [ ] Create another test account
- [ ] Find that user
- [ ] Send message
- [ ] Message appears?

**Admin**
- [ ] Visit `/admin`
- [ ] Login
- [ ] See all models
- [ ] Can edit users/projects?

---

## If Something Breaks

### Static Files Return 404
```bash
# In Shell:
python manage.py collectstatic --clear --noinput
```

### Email Not Sending
- Check BREVO_API_KEY is correct
- Check DEFAULT_FROM_EMAIL is set
- Test in Django shell:
  ```python
  from django.core.mail import send_mail
  send_mail('Test', 'Test message', 'from@example.com', ['to@example.com'])
  ```

### OAuth Not Working
- Check redirect URLs in Google/GitHub settings
- Make sure domain is in ALLOWED_HOSTS
- Verify Client ID/Secret are correct

### Database Error
- DATABASE_URL is auto-provided (check Variables)
- Make sure migrations have run
- Check logs for connection errors

### Look at the Logs!
- **Render:** Service → "Logs" tab
- **Railway:** Service → "Logs" tab
- Logs will tell you what's wrong

---

## Add Custom Domain (Optional)

### For Render:
1. Go to Web Service → "Settings"
2. Scroll to "Custom Domains"
3. Add your domain
4. Update DNS CNAME to render domain
5. Wait for verification

### For Railway:
1. Go to "Settings" → "Domains"
2. Click "Add Domain"
3. Follow DNS instructions
4. Verify domain

---

## Keep It Running

### Check Weekly:
- [ ] App still loading?
- [ ] No errors in logs?
- [ ] Email sending correctly?

### Update Environment Variables:
If you change email/OAuth credentials:
1. Update in Render/Railway environment
2. Redeploy (auto if set up)

### Monitor Performance:
- Render: Dashboard → Metrics
- Railway: Dashboard → Analytics

---

## You're Done! 🎉

Congratulations! Your UniSync app is live!

### What You've Built:
✅ User authentication with OTP  
✅ Student profiles  
✅ Project management  
✅ Real-time messaging  
✅ Notifications  
✅ Social networking  

### Your URLs:
- **Render:** https://unisync.onrender.com
- **Railway:** https://yourdomain.up.railway.app
- **Admin:** https://yourdomain/admin

---

## Need Help?

### In Your Repository:
- `DEPLOYMENT_RENDER_RAILWAY.md` - Detailed guide
- `ENVIRONMENT_SETUP_GUIDE.md` - Service setup
- `DEPLOYMENT_CHECKLIST.md` - Full checklist

### Online:
- Django: https://docs.djangoproject.com
- Render: https://render.com/docs
- Railway: https://docs.railway.app

---

## Summary

```
Time needed:
- Get credentials:    30 minutes
- Deploy to Render:   15 minutes
- Deploy to Railway:  15 minutes
- Test & verify:      15 minutes
                      ─────────────
Total:               ~1.5 hours

Your app will be LIVE after that!
```

---

## Ready? Let's Go! 🚀

Choose your platform above and follow the steps.

**Estimated time to production: 1.5-2 hours**

Good luck! 💪
