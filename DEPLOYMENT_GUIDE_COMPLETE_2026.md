# Complete Deployment Guide - 2026

## TL;DR - Quick Deploy (5 minutes)

**Best for beginners:** Use **Render.com** (free tier available)

```bash
# 1. Prepare code
git init
git add .
git commit -m "Initial commit"
git branch -M main

# 2. Push to GitHub
git remote add origin https://github.com/YOUR_USERNAME/your-repo.git
git push -u origin main

# 3. Go to render.com
# Sign up → Connect GitHub repo → Deploy

# Done! Your app is live in 2-5 minutes
```

---

## Deployment Platforms Comparison

| Platform | Cost | Difficulty | Best For | Setup Time |
|----------|------|-----------|----------|-----------|
| **Render.com** | Free tier ✅ | Easy | Beginners | 5 min |
| **Railway.app** | Free tier ✅ | Easy | Beginners | 5 min |
| **Heroku** | Paid (discontinued free) | Easy | Prototyping | 5 min |
| **AWS** | Pay-as-you-go | Hard | Scale | 30 min |
| **DigitalOcean** | $4-6/month | Medium | Reliability | 20 min |
| **Fly.io** | Free tier ✅ | Medium | Global | 10 min |
| **VPS** (Linode/Vultr) | $5-10/month | Hard | Control | 45 min |

**Recommendation for learning:** Render.com or Railway.app

---

## Option 1: Deploy to Render.com (Recommended for Beginners)

### Step 1: Prepare Your Code

#### 1.1 Create `.gitignore`

```bash
# File: .gitignore
__pycache__/
*.py[cod]
*$py.class
*.so
.Python
venv/
env/
ENV/
.venv
db.sqlite3
.env
.env.local
node_modules/
dist/
build/
*.egg-info/
.DS_Store
logs/
media/
staticfiles/
```

#### 1.2 Initialize Git

```bash
cd e:/login
git init
git add .
git commit -m "Initial commit: UniSync application"
```

#### 1.3 Create GitHub Repository

1. Go to https://github.com/new
2. Create repo: `unisync` (or your name)
3. Don't initialize with README

```bash
git remote add origin https://github.com/YOUR_USERNAME/unisync.git
git branch -M main
git push -u origin main
```

### Step 2: Create Render Configuration

#### 2.1 Create `render.yaml`

File: `render.yaml` (in root)

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
      - key: PYTHON_VERSION
        value: 3.11
      - key: DEBUG
        value: false
      - key: ALLOWED_HOSTS
        value: ${{RENDER_EXTERNAL_HOSTNAME}}
      - key: SECRET_KEY
        sync: false
        # Generate on Render dashboard
      - key: DATABASE_URL
        fromDatabase:
          name: unisync_db
          property: connectionString
      - key: REDIS_URL
        fromService:
          name: redis
          property: connectionString
          envVarKey: REDIS_URL

  - type: postgres
    name: unisync_db
    ipAllowList: []

  - type: redis
    name: redis
    ipAllowList: []
```

#### 2.2 Update `backend/settings.py`

```python
# Add at bottom of settings.py

# Render specific
if 'RENDER' in os.environ:
    ALLOWED_HOSTS = os.getenv('ALLOWED_HOSTS', '').split(',')
    SECURE_SSL_REDIRECT = True
    SESSION_COOKIE_SECURE = True
    CSRF_COOKIE_SECURE = True
    SECURE_HSTS_SECONDS = 31536000
    SECURE_HSTS_INCLUDE_SUBDOMAINS = True
    SECURE_HSTS_PRELOAD = True
```

### Step 3: Deploy on Render

1. **Sign up:** https://render.com (GitHub login)
2. **Create Blueprint:** 
   - Click "New +" → "Blueprint"
   - Select your GitHub repo
   - Click "Deploy"

3. **Configure Environment Variables:**
   - Dashboard → Your App → Environment
   - Add:
     ```
     SECRET_KEY=your-generated-secret-key-here
     BREVO_API_KEY=your-api-key-here
     GOOGLE_CLIENT_ID=...
     GOOGLE_CLIENT_SECRET=...
     GITHUB_CLIENT_ID=...
     GITHUB_CLIENT_SECRET=...
     ```

4. **Wait for Deployment:**
   - Build: ~5 minutes
   - Database setup: ~2 minutes
   - Live: ✅

5. **Test:**
   - Visit: `https://your-app-name.onrender.com`
   - Check logs: Dashboard → Logs

### Step 4: Post-Deployment

```bash
# SSH into render container (via dashboard)
# Or use Render CLI

# Check migrations
python manage.py showmigrations

# Create admin user
python manage.py createsuperuser

# Access admin
https://your-app.onrender.com/admin/
```

---

## Option 2: Deploy to Railway.app

### Step 1: Prepare Code (Same as Render)

```bash
git init
git add .
git commit -m "Initial"
git push
```

### Step 2: Railway Configuration

File: `railway.json` (in root)

```json
{
  "build": {
    "builder": "dockerfile"
  }
}
```

Or use environment detection (Railway auto-detects Django)

### Step 3: Deploy

1. **Sign up:** https://railway.app (GitHub login)
2. **Create Project:**
   - Click "New Project" → "Deploy from GitHub"
   - Select repo
   - Click "Deploy"
3. **Add Services:**
   - PostgreSQL: Click "+" → Add PostgreSQL
   - Redis: Click "+" → Add Redis
4. **Set Variables:**
   - Project Settings → Variables
   - Add SECRET_KEY, BREVO_API_KEY, etc.

### Step 4: Configure Domain

- Settings → Domains → Generate Domain
- Or add custom domain (paid)

---

## Option 3: Deploy to AWS (for Scale)

### Step 1: Setup AWS Account

1. Create AWS account (https://aws.amazon.com)
2. Create IAM user with EC2/RDS access
3. Create security group

### Step 2: Option A - Elastic Beanstalk (Easier)

```bash
# Install Elastic Beanstalk CLI
pip install awsebcli

# Initialize
eb init -p python-3.11 unisync

# Create `.ebextensions/django.config`
option_settings:
  aws:elasticbeanstalk:container:python:
    WSGIPath: auth_project.wsgi:application
  aws:elasticbeanstalk:application:environment:
    DJANGO_SETTINGS_MODULE: auth_project.settings
    PYTHONPATH: /var/app/current/backend:$PYTHONPATH

# Deploy
eb create unisync-env
eb deploy
```

### Step 3: Option B - EC2 + RDS (More Control)

```bash
# 1. Launch EC2 instance (Ubuntu 22.04)
# 2. SSH into instance
ssh -i your-key.pem ec2-user@your-instance-ip

# 3. Install dependencies
sudo apt update
sudo apt install -y python3.11 python3.11-venv postgresql-client redis-tools

# 4. Clone repo
git clone https://github.com/YOUR_USERNAME/unisync.git
cd unisync/backend

# 5. Setup virtual environment
python3.11 -m venv venv
source venv/bin/activate
pip install -r requirements.txt

# 6. Setup RDS PostgreSQL
# In AWS console: Create RDS instance
# Configure SECURITY GROUPS to allow EC2 access

# 7. Set environment variables
# Create .env file with DATABASE_URL, SECRET_KEY, etc.

# 8. Migrate database
python manage.py migrate

# 9. Collect static files
python manage.py collectstatic --noinput

# 10. Install Gunicorn & Nginx
pip install gunicorn
sudo apt install -y nginx

# 11. Configure Nginx
# Create /etc/nginx/sites-available/unisync
# Point to Gunicorn on localhost:8000

# 12. Start Gunicorn
gunicorn auth_project.wsgi:application --bind 0.0.0.0:8000

# 13. Setup systemd service
# Create /etc/systemd/system/unisync.service
# Auto-start on boot
```

---

## Preparation Checklist

### Code Preparation

- [ ] Git repository initialized
- [ ] Code pushed to GitHub
- [ ] `.gitignore` created
- [ ] No secrets in code (use .env)
- [ ] requirements.txt up-to-date
- [ ] `build.sh` created for production build
- [ ] Dockerfile created (optional, but recommended)

### Django Settings

- [ ] Set `DEBUG=False` in production
- [ ] Configure `ALLOWED_HOSTS`
- [ ] Set `SECRET_KEY` to strong value
- [ ] Configure `STATIC_URL` and `STATIC_ROOT`
- [ ] Configure `MEDIA_URL` and `MEDIA_ROOT`
- [ ] Setup security headers
- [ ] Configure CORS if needed
- [ ] Setup logging

### Database

- [ ] PostgreSQL configured (or SQLite okay for small projects)
- [ ] Database backups planned
- [ ] Migrations tested locally
- [ ] Admin user will be created post-deploy

### Environment Variables

```
Required:
□ DEBUG=False
□ SECRET_KEY=your-strong-secret-key
□ ALLOWED_HOSTS=yourapp.onrender.com
□ DATABASE_URL=postgresql://user:pass@host:5432/db
□ REDIS_URL=redis://host:6379/1

Optional:
□ BREVO_API_KEY=your-api-key
□ GOOGLE_CLIENT_ID=...
□ GOOGLE_CLIENT_SECRET=...
□ GITHUB_CLIENT_ID=...
□ GITHUB_CLIENT_SECRET=...
```

### Build Script

Create `build.sh` (already in your repo):

```bash
#!/usr/bin/env bash
set -o errexit

echo "Collecting static files..."
python manage.py collectstatic --noinput --clear

echo "Running migrations..."
python manage.py migrate

echo "Build complete!"
```

---

## Production Settings Template

### Environment Variables (.env)

```
# Core
DEBUG=False
SECRET_KEY=django-insecure-your-generated-secret-key-here
ALLOWED_HOSTS=yourapp.onrender.com,www.yourapp.com

# Database
DATABASE_URL=postgresql://user:password@host:5432/unisync_db

# Cache & Sessions
REDIS_URL=redis://host:6379/1

# Email
EMAIL_BACKEND=accounts.brevo_mail_backend.BrevoMailBackend
BREVO_API_KEY=your-brevo-api-key

# OAuth
GOOGLE_CLIENT_ID=your-google-client-id
GOOGLE_CLIENT_SECRET=your-google-secret
GITHUB_CLIENT_ID=your-github-client-id
GITHUB_CLIENT_SECRET=your-github-secret

# Security
SECURE_SSL_REDIRECT=True
SESSION_COOKIE_SECURE=True
CSRF_COOKIE_SECURE=True
SECURE_HSTS_SECONDS=31536000

# File uploads
MEDIA_URL=/media/
MEDIA_ROOT=/var/www/media/
```

### Update `backend/settings.py`

```python
import os
from pathlib import Path

# Determine environment
ENVIRONMENT = os.getenv('ENVIRONMENT', 'development')

# Base
DEBUG = os.getenv('DEBUG', 'True').lower() == 'true'
SECRET_KEY = os.getenv('SECRET_KEY')
ALLOWED_HOSTS = os.getenv('ALLOWED_HOSTS', 'localhost').split(',')

# Database
DATABASE_URL = os.getenv('DATABASE_URL')
if DATABASE_URL:
    import dj_database_url
    DATABASES = {
        'default': dj_database_url.parse(DATABASE_URL, conn_max_age=600)
    }
else:
    # Fallback for local development
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.sqlite3',
            'NAME': BASE_DIR / 'db.sqlite3',
        }
    }

# Security
if not DEBUG:
    SECURE_SSL_REDIRECT = True
    SESSION_COOKIE_SECURE = True
    CSRF_COOKIE_SECURE = True
    SECURE_HSTS_SECONDS = 31536000
    SECURE_HSTS_INCLUDE_SUBDOMAINS = True
    SECURE_HSTS_PRELOAD = True
    SECURE_BROWSER_XSS_FILTER = True
    X_FRAME_OPTIONS = 'DENY'
    SECURE_CONTENT_SECURITY_POLICY = {
        'default-src': ("'self'",),
    }

# Cache
CACHES = {
    'default': {
        'BACKEND': 'django_redis.cache.RedisCache',
        'LOCATION': os.getenv('REDIS_URL', 'redis://localhost:6379/1'),
        'OPTIONS': {
            'CLIENT_CLASS': 'django_redis.client.DefaultClient',
            'CONNECTION_POOL_KWARGS': {'max_connections': 50}
        }
    }
}

# Static files
STATIC_URL = '/static/'
STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')

# Media files
MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')

# Logging
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'handlers': {
        'console': {
            'class': 'logging.StreamHandler',
        },
        'file': {
            'class': 'logging.FileHandler',
            'filename': os.path.join(BASE_DIR, 'logs', 'django.log'),
            'formatter': 'verbose',
        },
    },
    'formatters': {
        'verbose': {
            'format': '[{levelname}] {asctime} {module} {message}',
            'style': '{',
        },
    },
    'root': {
        'handlers': ['console', 'file'],
        'level': 'INFO',
    },
    'django': {
        'handlers': ['console', 'file'],
        'level': 'INFO',
        'propagate': False,
    },
}

# WebSocket
ASGI_APPLICATION = 'auth_project.asgi.application'
CHANNEL_LAYERS = {
    'default': {
        'BACKEND': 'channels_redis.core.RedisChannelLayer',
        'CONFIG': {
            'hosts': [os.getenv('REDIS_URL', 'redis://localhost:6379/1')],
        },
    },
}
```

---

## Deployment Process Step-by-Step

### 1. Local Testing (Make Sure It Works)

```bash
cd backend
python manage.py runserver
# Test all features locally
```

### 2. Create Production Build

```bash
# Collect static files
python manage.py collectstatic --noinput

# Run migrations locally first
python manage.py migrate --plan

# Create admin user
python manage.py createsuperuser
```

### 3. Prepare Git Repository

```bash
# Ensure .gitignore is correct
cat .gitignore

# Add all files
git add .
git commit -m "Deployment: ready for production"
git push origin main
```

### 4. Deploy (Choose Your Platform)

**Render.com (Easiest):**
- Push to GitHub ✓
- Visit render.com
- Click "New Project" → "Deploy from GitHub"
- Select repo → Deploy
- Set environment variables
- Done!

**Railway.app:**
- Push to GitHub ✓
- Visit railway.app
- New Project → Deploy from GitHub
- Railway auto-configures
- Done!

**AWS/Self-Hosted:**
- Follow platform-specific guides
- Use Dockerfile if available
- Configure environment variables
- Run migrations
- Create superuser
- Done!

### 5. Post-Deployment

```bash
# Check logs
# Render: Dashboard → Logs
# Railway: Project → Deployments → Logs

# Access admin
https://your-app.onrender.com/admin/
Username: admin (from createsuperuser)
Password: (your password)

# Create test data
# Upload a project, test chat, etc.

# Setup domain (optional)
# Point custom domain to Render/Railway
```

---

## Troubleshooting Deployment

### Issue: Database migration fails

**Cause:** Database not initialized

**Solution:**
```bash
# Render: Rerun the build
# Railway: Manual migration via dashboard
# Or SSH and run: python manage.py migrate
```

### Issue: Static files not showing

**Cause:** collectstatic didn't run

**Solution:**
```bash
python manage.py collectstatic --noinput --clear
```

### Issue: WebSocket not connecting

**Cause:** Redis not configured, Daphne not running

**Solution:**
- Ensure Redis service is created
- Use `daphne` for WebSocket support
- Check CHANNEL_LAYERS in settings

### Issue: OAuth login fails

**Cause:** Redirect URI mismatch

**Solution:**
1. Get your deployed URL: `https://your-app.onrender.com`
2. Go to OAuth provider (Google/GitHub)
3. Update redirect URIs:
   ```
   https://your-app.onrender.com/accounts/google/login/callback/
   https://your-app.onrender.com/accounts/github/login/callback/
   ```

### Issue: 500 Error

**Solution:**
1. Check logs (Dashboard → Logs)
2. Look for specific error
3. Check environment variables
4. Verify database is running

### Issue: "DEBUG=False" causes issues

**Solution:**
- Ensure ALLOWED_HOSTS includes your domain
- Set STATIC_URL correctly
- Run collectstatic

---

## Monitoring & Maintenance

### Setup Monitoring

**Render:**
- Built-in: Metrics, Logs
- Dashboard → Metrics tab

**Railway:**
- Built-in: Metrics, Logs
- Project → Deployments → Logs

### Enable Email Alerts

**Render:**
- Settings → Alerts
- Enable notifications

**Railway:**
- Settings → Integrations
- Configure Slack/Discord

### Database Backups

**Render PostgreSQL:**
- Automatic daily backups
- Download: Database → Backups

**Railway PostgreSQL:**
- Automatic backups
- Export via pgAdmin

### Regular Maintenance

- [ ] Check error logs weekly
- [ ] Monitor database usage
- [ ] Update dependencies monthly
- [ ] Review security settings
- [ ] Test restore from backup

---

## Performance Tips

### Before Deployment

```python
# settings.py

# Database connection pooling
DATABASES = {
    'default': {
        ...
        'CONN_MAX_AGE': 600,
        'OPTIONS': {
            'connect_timeout': 10,
        }
    }
}

# Cache frequently accessed data
CACHES['default']['OPTIONS']['CONNECTION_POOL_KWARGS'] = {
    'max_connections': 50
}

# Use PostgreSQL (not SQLite) in production
# Don't use in-memory channel layer
```

### After Deployment

1. Add CDN for static files
2. Enable gzip compression
3. Use database indexes
4. Cache API responses
5. Monitor performance
6. Set up APM (Application Performance Monitoring)

---

## Security Checklist

- [ ] DEBUG=False
- [ ] SECRET_KEY is random (50+ chars)
- [ ] ALLOWED_HOSTS configured
- [ ] SECURE_SSL_REDIRECT=True
- [ ] SESSION_COOKIE_SECURE=True
- [ ] CSRF_COOKIE_SECURE=True
- [ ] SECURE_HSTS_SECONDS set
- [ ] No secrets in code (use .env)
- [ ] Database has strong password
- [ ] Admin password is strong
- [ ] OAuth credentials kept secret
- [ ] Firewall configured
- [ ] Regular backups enabled

---

## Cost Estimates

### Free Tier (Good for learning/small projects)
- Render.com: Free with limitations
- Railway.app: $5 credits/month
- Total: ~$0/month

### Starter (Small production)
- Render.com: $10/month (web) + $15/month (PostgreSQL)
- Railway.app: ~$20/month
- Total: ~$25-30/month

### Growth (Medium production)
- Render.com: $25/month (web) + $50/month (PostgreSQL)
- Railway.app: ~$50-100/month
- Total: ~$50-100/month

### Scale (Large production)
- AWS: $100-500+/month
- DigitalOcean: $50-200+/month
- Custom VPS: $50-1000+/month
- Total: Depends on usage

---

## Quick Deployment Commands

### Render.com
```bash
# Push code
git add .
git commit -m "Deploy"
git push origin main
# Render auto-deploys from main branch
```

### Railway.app
```bash
# Push code
git add .
git commit -m "Deploy"
git push origin main
# Railway auto-deploys from main branch
```

### Heroku (legacy)
```bash
heroku login
heroku create your-app-name
heroku addons:create heroku-postgresql:hobby-dev
heroku config:set DEBUG=False
git push heroku main
```

### Self-Hosted (Docker)
```bash
docker build -t unisync .
docker run -p 8000:8000 unisync
```

---

## Next Steps After Deployment

1. **Test Thoroughly**
   - Login (email, OAuth)
   - Create project
   - Chat features
   - Admin panel

2. **Setup Domain**
   - Buy domain (namecheap.com, godaddy.com)
   - Point to deployment
   - Setup SSL (auto with Render/Railway)

3. **Monitor**
   - Check logs daily
   - Monitor errors
   - Track performance

4. **Improve**
   - Add caching
   - Optimize database
   - Setup CDN
   - Configure backups

5. **Scale**
   - Upgrade database
   - Add more servers
   - Use load balancer
   - Setup monitoring

---

## Resources

- **Render Docs:** https://docs.render.com
- **Railway Docs:** https://docs.railway.app
- **Django Deployment:** https://docs.djangoproject.com/en/4.2/howto/deployment/
- **Gunicorn:** https://gunicorn.org/
- **Nginx:** https://nginx.org/

---

## Summary

**Easiest Deployment:** Render.com or Railway.app (5 minutes)
**Best Control:** Self-hosted VPS
**Best Scale:** AWS
**Recommended for you:** Render.com (free tier, simple)

Pick Render → Push to GitHub → Deploy. Done! 🚀

