# UniSync Deployment Guide: Render & Railway

**Date:** January 31, 2026  
**Application:** UniSync Student Collaboration Platform  
**Repository:** https://github.com/Goku0090/uni_sync

---

## Table of Contents
1. [Render Deployment](#render-deployment)
2. [Railway Deployment](#railway-deployment)
3. [Environment Configuration](#environment-configuration)
4. [Database Setup](#database-setup)
5. [Email Configuration](#email-configuration)
6. [Post-Deployment](#post-deployment)

---

# RENDER DEPLOYMENT

## Overview
**Pros:**
- Free tier available
- Built-in PostgreSQL support
- Auto-deploy from GitHub
- Good documentation
- Easy SSL/HTTPS setup

**Cons:**
- Cold starts on free tier
- Limited resources on free tier

---

## Step 1: Prepare GitHub Repository

✅ Already done! Your code is at:
https://github.com/Goku0090/uni_sync

Ensure `render.yaml` exists in root:

```yaml
services:
  - type: web
    name: unisync
    env: python
    plan: standard
    buildCommand: "pip install -r auth_project/requirements.txt && python auth_project/manage.py collectstatic --noinput"
    startCommand: "gunicorn auth_project.wsgi:application"
    envVars:
      - key: PYTHON_VERSION
        value: 3.11
```

---

## Step 2: Create Render Account

1. Go to https://render.com
2. Sign up with GitHub
3. Click "New +" → Select "Web Service"

---

## Step 3: Connect GitHub Repository

1. **Authorize GitHub:**
   - Click "Connect a repository"
   - Select your GitHub account
   - Choose `uni_sync` repository

2. **Configure Service:**
   - **Name:** `unisync`
   - **Environment:** Python
   - **Plan:** Starter (paid) or Free
   - **Region:** Choose closest to you
   - **Branch:** main
   - **Root Directory:** Leave blank (uses root)

---

## Step 4: Build & Start Commands

### Build Command:
```bash
pip install -r auth_project/requirements.txt && python auth_project/manage.py collectstatic --noinput
```

### Start Command:
```bash
gunicorn auth_project.wsgi:application --bind 0.0.0.0:10000
```

---

## Step 5: Environment Variables

Click "Environment" and add:

### Essential Variables
```
DEBUG=False
SECRET_KEY=<generate-strong-key>
ALLOWED_HOSTS=unisync.onrender.com,yourdomain.com
```

### Database
Render provides `DATABASE_URL` automatically. If using external PostgreSQL:
```
DATABASE_URL=postgresql://user:password@hostname:5432/dbname
```

### Email (Choose One)

**Option A: Brevo (Recommended)**
```
BREVO_API_KEY=<your-brevo-api-key>
```

**Option B: ZeptoMail**
```
ZEPTO_MAIL_API_KEY=<your-zepto-api-key>
ZEPTO_MAIL_TOKEN=<your-zepto-token>
```

**Option C: Gmail**
```
EMAIL_HOST_USER=your-email@gmail.com
EMAIL_HOST_PASSWORD=<app-specific-password>
```

### Social Authentication
```
GOOGLE_CLIENT_ID=<your-google-client-id>
GOOGLE_CLIENT_SECRET=<your-google-client-secret>
GITHUB_CLIENT_ID=<your-github-client-id>
GITHUB_CLIENT_SECRET=<your-github-client-secret>
```

### External Services
```
RAPIDAPI_KEY=<your-rapidapi-key>
DEFAULT_FROM_EMAIL=noreply@yourdomain.com
```

### Security (Production)
```
SECURE_SSL_REDIRECT=True
SESSION_COOKIE_SECURE=True
CSRF_COOKIE_SECURE=True
```

---

## Step 6: Create Render PostgreSQL Database

1. Click "New +" → Select "PostgreSQL"
2. **Name:** `unisync-db`
3. **Region:** Same as web service
4. **PostgreSQL Version:** 14+
5. **Create Database**

Render will provide `DATABASE_URL` automatically.

---

## Step 7: Deploy

1. Click **"Create Web Service"**
2. Render will automatically build and deploy
3. Watch the logs in the "Logs" tab
4. Once deployed, you'll get a URL: `https://unisync.onrender.com`

---

## Step 8: Run Migrations

Once deployment succeeds:

1. Click the web service
2. Go to **"Shell"** tab
3. Run commands:
```bash
python auth_project/manage.py migrate
python auth_project/manage.py createsuperuser
python auth_project/manage.py collectstatic --noinput
```

---

## Step 9: Configure Allowed Hosts

Update in Render environment:
```
ALLOWED_HOSTS=unisync.onrender.com,www.unisync.onrender.com
```

---

## Render Troubleshooting

### Build Failed
Check build logs - common issues:
- Missing `requirements.txt` location
- Python version mismatch
- Build timeout

### Application Crashed
Check runtime logs:
- Missing environment variables
- Database connection error
- Import errors

### Static Files Not Loading
```bash
python manage.py collectstatic --clear --noinput
```

---

---

# RAILWAY DEPLOYMENT

## Overview
**Pros:**
- Very fast deployment
- Generous free tier ($5/month credit)
- Simple UI
- Good for quick deployments
- Automatic database provisioning

**Cons:**
- Smaller community than Render
- Less documentation

---

## Step 1: Create Railway Account

1. Go to https://railway.app
2. Sign up with GitHub
3. Authorize Railway to access your repositories

---

## Step 2: Create New Project

1. Click **"New Project"**
2. Select **"Deploy from GitHub repo"**
3. Select `uni_sync` repository
4. Click **"Deploy Now"**

---

## Step 3: Add PostgreSQL Service

In Railway dashboard:

1. Click **"Add"** (+ icon)
2. Select **"PostgreSQL"**
3. Railway creates and links automatically
4. Generates `DATABASE_URL` automatically

---

## Step 4: Configure Application

Railway auto-detects Django application.

### Create `Procfile` in root:
```
web: gunicorn auth_project.wsgi:application --bind 0.0.0.0:$PORT
```

### Create `railway.json` (optional):
```json
{
  "buildCommand": "pip install -r auth_project/requirements.txt && python auth_project/manage.py collectstatic --noinput",
  "startCommand": "gunicorn auth_project.wsgi:application --bind 0.0.0.0:$PORT"
}
```

Push to GitHub:
```bash
git add Procfile railway.json
git commit -m "Add deployment configuration"
git push origin main
```

---

## Step 5: Set Environment Variables

In Railway dashboard → Variables:

### Essential
```
DEBUG=False
SECRET_KEY=<generate-strong-key>
ALLOWED_HOSTS=*.railway.app,yourdomain.com
PORT=8000
```

### Email Configuration
```
# Choose one option

# Option A: Brevo
BREVO_API_KEY=<your-brevo-api-key>

# Option B: ZeptoMail
ZEPTO_MAIL_API_KEY=<your-zepto-api-key>
ZEPTO_MAIL_TOKEN=<your-zepto-token>

# Option C: Gmail
EMAIL_HOST_USER=your-email@gmail.com
EMAIL_HOST_PASSWORD=<app-specific-password>

DEFAULT_FROM_EMAIL=noreply@yourdomain.com
```

### Social Authentication
```
GOOGLE_CLIENT_ID=<your-google-client-id>
GOOGLE_CLIENT_SECRET=<your-google-client-secret>
GITHUB_CLIENT_ID=<your-github-client-id>
GITHUB_CLIENT_SECRET=<your-github-client-secret>
```

### External Services
```
RAPIDAPI_KEY=<your-rapidapi-key>
```

### Security
```
SECURE_SSL_REDIRECT=True
SESSION_COOKIE_SECURE=True
CSRF_COOKIE_SECURE=True
```

---

## Step 6: Configure Database Connection

Railway auto-provides `DATABASE_URL`. Verify in Variables:
```
DATABASE_URL=postgresql://user:password@host:port/dbname
```

---

## Step 7: Deploy

1. Push code to GitHub
2. Railway automatically builds and deploys
3. Check **"Deployments"** tab for status
4. Once deployed, get URL from **"Settings"** → **"Domains"**

---

## Step 8: Run Migrations

Via Railway shell:

1. Click the web service
2. Go to **"Shell"** tab
3. Run:
```bash
python auth_project/manage.py migrate
python auth_project/manage.py createsuperuser
python auth_project/manage.py collectstatic --noinput
```

---

## Step 9: Add Custom Domain (Optional)

In Railway dashboard → Settings → Domains:
1. Click "Add Domain"
2. Enter your domain (e.g., `unisync.com`)
3. Update DNS records as shown
4. Click "Verify"

---

## Railway Troubleshooting

### Build Fails
- Check buildCommand in railway.json
- Verify Python version compatibility
- Check for missing files

### Deployment Fails
- Check environment variables
- Verify database connection
- Check application logs

### Database Connection Error
Railway auto-provides `DATABASE_URL`. Ensure it's set:
```bash
echo $DATABASE_URL
```

---

---

# ENVIRONMENT CONFIGURATION

## Generate Secret Key

In Python shell:
```python
from django.core.management.utils import get_random_secret_key
print(get_random_secret_key())
```

Or use:
```bash
python -c 'from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())'
```

---

## Configure Email Services

### Brevo (Recommended)

1. Sign up at https://www.brevo.com
2. Get API Key from **Settings → API Keys → Create**
3. Add to Render/Railway:
```
BREVO_API_KEY=xsw...
```

### ZeptoMail

1. Sign up at https://www.zeptomail.com
2. Create API token
3. Add to environment:
```
ZEPTO_MAIL_API_KEY=xyz...
ZEPTO_MAIL_TOKEN=abc...
```

### Gmail (Less Recommended)

1. Enable 2FA on Gmail account
2. Generate App Password
3. Add to environment:
```
EMAIL_HOST_USER=your-email@gmail.com
EMAIL_HOST_PASSWORD=xxxx xxxx xxxx xxxx
```

---

## Configure Google OAuth

1. Go to https://console.cloud.google.com
2. Create new project
3. Enable **Google+ API**
4. Create **OAuth 2.0 Client ID** (Web application)
5. Authorized redirect URIs:
   ```
   https://yourdomain.com/accounts/google/login/callback/
   https://yourdomain.onrender.com/accounts/google/login/callback/
   https://yourdomain.up.railway.app/accounts/google/login/callback/
   ```
6. Add Client ID & Secret to environment:
```
GOOGLE_CLIENT_ID=xxx.apps.googleusercontent.com
GOOGLE_CLIENT_SECRET=xxx
```

---

## Configure GitHub OAuth

1. Go to GitHub → Settings → Developer settings → OAuth Apps
2. Click "New OAuth App"
3. **Authorization callback URL:**
   ```
   https://yourdomain.com/accounts/github/login/callback/
   https://yourdomain.onrender.com/accounts/github/login/callback/
   https://yourdomain.up.railway.app/accounts/github/login/callback/
   ```
4. Copy Client ID & Secret:
```
GITHUB_CLIENT_ID=xxx
GITHUB_CLIENT_SECRET=xxx
```

---

## Configure RapidAPI

1. Sign up at https://rapidapi.com
2. Search "Universities List" API
3. Subscribe to it
4. Get API Key from dashboard
5. Add to environment:
```
RAPIDAPI_KEY=xxx
```

---

---

# DATABASE SETUP

## PostgreSQL Configuration

### Render
- Automatically created with web service
- `DATABASE_URL` provided automatically
- No configuration needed

### Railway
- Automatically created as service
- `DATABASE_URL` provided automatically
- No configuration needed

---

## Initial Database Setup

After deployment, run:

```bash
# Run migrations
python auth_project/manage.py migrate

# Create superuser
python auth_project/manage.py createsuperuser
# Username: admin
# Email: your-email@example.com
# Password: [secure password]

# Collect static files
python auth_project/manage.py collectstatic --noinput
```

---

## Database Backup (Render)

1. Go to Render dashboard
2. Click PostgreSQL service
3. Go to "Backups" tab
4. Enable automated backups
5. Download manual backups as needed

---

## Database Backup (Railway)

1. Click PostgreSQL service
2. Go to "Backups"
3. Enable automated backups
4. Backups stored in Railway

---

---

# EMAIL CONFIGURATION

## Test Email Service

After deployment, test with:

```bash
python auth_project/manage.py shell
```

```python
from django.core.mail import send_mail
send_mail(
    'Test Subject',
    'Test message',
    'from@example.com',
    ['to@example.com'],
    fail_silently=False,
)
```

---

## Email Verification for Brevo

Add verified sender email in Brevo dashboard:
1. Settings → Sender & IP Management
2. Add verified email
3. Verify via email link
4. Use this email in `DEFAULT_FROM_EMAIL`

---

## Test OTP Flow

1. Access deployed app: `https://yourdomain.com`
2. Click "Register"
3. Enter email and request OTP
4. Check email for OTP code
5. Verify OTP works

---

---

# POST-DEPLOYMENT

## Verification Checklist

- [ ] Application loads at `https://yourdomain.com`
- [ ] Login page works
- [ ] OTP email sends and works
- [ ] Database migrations completed
- [ ] Static files loaded (CSS, JS)
- [ ] Images/media display properly
- [ ] Social login (Google/GitHub) works
- [ ] Create test user and login
- [ ] Create test project
- [ ] Test messaging system
- [ ] Test notifications

---

## Monitor Deployment

### Render
- **Logs:** Click service → "Logs" tab
- **Metrics:** Click service → "Metrics" tab
- **Usage:** Dashboard shows usage

### Railway
- **Logs:** Click service → "Logs" tab
- **Metrics:** Click service → "Metrics" tab
- **Deployments:** Track past deployments

---

## Common Issues & Fixes

### Static Files Not Loading
```bash
python manage.py collectstatic --clear --noinput
```

### Database Migration Errors
```bash
python manage.py migrate --noinput
```

### Import Error on Deployment
- Check requirements.txt is in correct location
- Verify all imports in models, views
- Check for version conflicts

### Cold Start (Render Free Tier)
- Upgrade to Starter plan
- Use Railway (faster cold starts)
- Or use paid tier

### Email Not Sending
- Verify API keys in environment
- Check email backend in settings.py
- Test with `python manage.py shell`

---

## Performance Optimization

### Add Redis Cache
For Render/Railway, add Redis service:

1. Click "Add" → Select "Redis"
2. Get `REDIS_URL` from environment
3. Add to env:
```
REDIS_URL=redis://...
```

4. Update settings.py:
```python
if os.getenv('REDIS_URL'):
    CACHES = {
        'default': {
            'BACKEND': 'django_redis.cache.RedisCache',
            'LOCATION': os.getenv('REDIS_URL'),
        }
    }
```

---

## Setup Custom Domain

### Render
1. Dashboard → Web Service → Settings
2. Custom Domains → Add Domain
3. Add DNS CNAME record:
   ```
   CNAME yourdomain.com → unisync.onrender.com
   ```

### Railway
1. Dashboard → Settings → Domains
2. Add Domain
3. Follow DNS setup instructions
4. Verify domain

---

## Enable HTTPS

Both Render and Railway provide free HTTPS automatically.

Enable in Django:
```
SECURE_SSL_REDIRECT=True
SESSION_COOKIE_SECURE=True
CSRF_COOKIE_SECURE=True
```

---

## Monitoring & Alerts

### Render
- Set up email alerts in Settings
- Monitor error logs regularly
- Check memory usage

### Railway
- View analytics dashboard
- Set up integrations
- Monitor resource usage

---

---

# COMPARISON: Render vs Railway

| Feature | Render | Railway |
|---------|--------|---------|
| **Free Tier** | Limited | $5/month credit (generous) |
| **Ease of Setup** | Very Easy | Very Easy |
| **Auto Deploy** | Yes | Yes |
| **PostgreSQL** | Yes (auto) | Yes (auto) |
| **Uptime** | 99.9% | High |
| **Cold Start** | Slower | Faster |
| **Documentation** | Excellent | Good |
| **Support** | Good | Good |
| **Custom Domain** | Yes | Yes |
| **Pricing** | Starter $12/mo | Pay-as-you-go |

---

## Recommendation

**For Starting Out:** Railway
- Better free tier
- Faster deployments
- Simpler to get running

**For Production:** Render
- Better SLA
- More features
- Industry standard

**Best Practice:** Deploy to Both
- Test on Railway (free)
- Promote to Render (production)
- Load balance between them

---

---

# QUICK REFERENCE

## Render Deployment Commands
```bash
# After deployment, run in Shell:
python auth_project/manage.py migrate
python auth_project/manage.py createsuperuser
python auth_project/manage.py collectstatic --noinput
```

## Railway Deployment Commands
```bash
# After deployment, run in Shell:
python auth_project/manage.py migrate
python auth_project/manage.py createsuperuser
python auth_project/manage.py collectstatic --noinput
```

## Environment Variables Checklist
```
[ ] DEBUG=False
[ ] SECRET_KEY=<generated>
[ ] ALLOWED_HOSTS=<your-domain>
[ ] DATABASE_URL=<auto-provided>
[ ] BREVO_API_KEY=<key> or EMAIL_HOST_USER=<email>
[ ] GOOGLE_CLIENT_ID=<id>
[ ] GOOGLE_CLIENT_SECRET=<secret>
[ ] GITHUB_CLIENT_ID=<id>
[ ] GITHUB_CLIENT_SECRET=<secret>
[ ] DEFAULT_FROM_EMAIL=<email>
```

---

## Support Links

- **Render Docs:** https://render.com/docs
- **Railway Docs:** https://docs.railway.app
- **Django Docs:** https://docs.djangoproject.com
- **Gunicorn:** https://docs.gunicorn.org
- **Django REST Framework:** https://www.django-rest-framework.org

---

**Status: READY FOR DEPLOYMENT** ✅

Your UniSync application is ready to deploy on Render and/or Railway!

Choose Render for production reliability, or Railway for quick prototyping.
