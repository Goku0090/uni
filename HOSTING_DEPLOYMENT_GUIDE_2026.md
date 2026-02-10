# Complete Hosting & Deployment Guide - UniSinq Platform
**Date:** February 09, 2026  
**Project:** UniSinq Student Collaboration Platform  
**Repository:** https://github.com/Goku0090/uni

---

## 🎯 Quick Navigation

- **Choose Your Platform:** [Render](#render-recommended) | [Railway](#railway) | [AWS](#aws) | [DigitalOcean](#digitalocean) | [Heroku](#heroku)
- **Self-Hosted:** [VPS Setup](#vps-self-hosted)
- **Quick Deploy:** [5-Minute Setup](#quick-deployment-5-minutes)
- **Advanced:** [Production Checklist](#production-checklist)

---

## 🏆 Recommended Platforms (Ranked)

| Platform | Ease | Cost | WebSocket Support | Recommendation |
|----------|------|------|-------------------|-----------------|
| **Render** | ⭐⭐⭐⭐⭐ | $$$$ | ✅ Native | ⭐⭐⭐⭐⭐ BEST |
| **Railway** | ⭐⭐⭐⭐ | $$$ | ✅ Native | ⭐⭐⭐⭐⭐ EXCELLENT |
| **AWS** | ⭐⭐⭐ | $$ | ✅ Complex | ⭐⭐⭐⭐ Good |
| **DigitalOcean** | ⭐⭐⭐ | $$ | ✅ Setup needed | ⭐⭐⭐⭐ Good |
| **Heroku** | ⭐⭐⭐⭐ | $$$$ | ⚠️ Limited | ⭐⭐⭐ Fair |

---

## 🚀 RENDER (RECOMMENDED)

### Why Render?
✅ Native Django support  
✅ Built-in WebSocket support (via Daphne)  
✅ Free PostgreSQL tier available  
✅ Auto-deploy from GitHub  
✅ Simple configuration  
✅ Excellent for Django + Channels  

### Step 1: Prepare Repository

```bash
# Make sure everything is committed and pushed
git add .
git commit -m "chore: prepare for Render deployment"
git push origin main
```

### Step 2: Create Render Service

1. Visit https://render.com
2. Click "New +" → "Web Service"
3. Connect your GitHub account
4. Select repository: `Goku0090/uni`
5. Fill in details:

```
Name: unisync-app (or your preferred name)
Environment: Python 3
Region: Use closest to users
Branch: main
Build Command: pip install -r auth_project/requirements.txt
Start Command: daphne -b 0.0.0.0 -p 10000 auth_project.asgi:application
```

### Step 3: Configure Environment Variables

In Render Dashboard → Environment:

```
DEBUG=False
SECRET_KEY=your-secret-key-here
ALLOWED_HOSTS=your-app-name.onrender.com
DATABASE_URL=postgres://...  (provided by Render)
EMAIL_BACKEND=accounts.brevo_mail_backend.BrevoEmailBackend
BREVO_API_KEY=your-brevo-api-key
SITE_URL=https://your-app-name.onrender.com
```

### Step 4: Connect PostgreSQL

1. In Render Dashboard → Create new PostgreSQL
2. Select "PostgreSQL" database
3. Copy connection string
4. Set `DATABASE_URL` in environment variables

### Step 5: Run Migrations

After first deployment:

```bash
# In Render dashboard, go to your service
# Click "Shell" tab
python auth_project/manage.py migrate
python auth_project/manage.py createsuperuser
python auth_project/manage.py collectstatic --noinput
```

### Step 6: Deploy & Monitor

1. Render auto-deploys on GitHub push
2. Monitor in Render Dashboard
3. Check logs for errors
4. Visit `https://your-app-name.onrender.com`

### Cost on Render
- **Web Service:** Free - $7/month (minimum)
- **PostgreSQL:** Free - $15/month (minimum)
- **Total:** ~$22/month (or free with limitations)

---

## 🚂 RAILWAY (EXCELLENT ALTERNATIVE)

### Why Railway?
✅ Very easy setup  
✅ GitHub integration  
✅ WebSocket compatible  
✅ Free $5/month credit  
✅ Pay-as-you-go pricing  
✅ Excellent support  

### Step 1: Setup Railway Project

1. Visit https://railway.app
2. Click "Create New Project"
3. Select "Deploy from GitHub repo"
4. Authorize GitHub
5. Select `Goku0090/uni`

### Step 2: Add Services

Add PostgreSQL:
```bash
Click "Add Service" → Select "PostgreSQL"
Railway creates DATABASE_URL automatically
```

### Step 3: Configure Django Service

In Railway Dashboard:

**Build Command:**
```bash
pip install -r auth_project/requirements.txt && python auth_project/manage.py migrate && python auth_project/manage.py collectstatic --noinput
```

**Start Command:**
```bash
daphne -b 0.0.0.0 -p $PORT auth_project.asgi:application
```

### Step 4: Set Environment Variables

```
DEBUG=False
SECRET_KEY=generate-strong-key
ALLOWED_HOSTS=*.railway.app
EMAIL_BACKEND=accounts.brevo_mail_backend.BrevoEmailBackend
BREVO_API_KEY=your-key
SITE_URL=https://your-app.railway.app
```

Railway auto-provides: `DATABASE_URL`, `PORT`

### Step 5: Deploy

```bash
# Just push to GitHub
git push origin main
# Railway auto-deploys
```

### Cost on Railway
- **Starter Plan:** Free $5/month credit
- **Pay-as-you-go:** PostgreSQL ~$5/month, dyno ~$5/month
- **Total:** ~$10/month after free credit

---

## ☁️ AWS (SCALABLE)

### Architecture
```
CloudFront CDN
    ↓
Application Load Balancer
    ↓
ECS Fargate (Docker containers)
    ↓
RDS PostgreSQL
    ↓
S3 (Static files & media)
```

### Why AWS?
✅ Highly scalable  
✅ Enterprise-grade  
✅ Full control  
✅ AWS Free Tier available  
⚠️ More complex setup  

### Step 1: Create AWS Account

1. Visit https://aws.amazon.com
2. Create account
3. Setup billing alerts
4. Enable AWS Free Tier

### Step 2: Create RDS PostgreSQL Database

In AWS Console:
```
RDS → Create Database
Engine: PostgreSQL 14
Class: db.t3.micro (free tier eligible)
Storage: 20 GB (free tier)
DB name: unisync_db
Master username: admin
Master password: strong-password
```

### Step 3: Create ECR Repository (for Docker)

```bash
# Create Dockerfile
cat > auth_project/Dockerfile << 'EOF'
FROM python:3.10-slim

WORKDIR /app

RUN apt-get update && apt-get install -y \
    postgresql-client \
    && rm -rf /var/lib/apt/lists/*

COPY auth_project/requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

CMD ["daphne", "-b", "0.0.0.0", "-p", "8000", "auth_project.asgi:application"]
EOF

# Build image
docker build -t unisync:latest auth_project/

# Tag for ECR
docker tag unisync:latest YOUR_AWS_ACCOUNT_ID.dkr.ecr.us-east-1.amazonaws.com/unisync:latest

# Push to ECR
aws ecr get-login-password --region us-east-1 | docker login --username AWS --password-stdin YOUR_AWS_ACCOUNT_ID.dkr.ecr.us-east-1.amazonaws.com
docker push YOUR_AWS_ACCOUNT_ID.dkr.ecr.us-east-1.amazonaws.com/unisync:latest
```

### Step 4: Create ECS Cluster & Service

```
ECS → Create Cluster → EC2/Fargate
Task Definition:
  - Image: Your ECR image
  - Memory: 512 MB
  - CPU: 256
  - Port: 8000
  - Environment: Set DATABASE_URL, etc.
```

### Step 5: Create Application Load Balancer

```
EC2 → Load Balancers → Create
Type: Application Load Balancer
Port: 80/443
Target: ECS service
```

### Step 6: Setup S3 for Static Files

```
S3 → Create bucket: unisync-static
Configure for web hosting
Add CloudFront distribution
```

### Cost on AWS
- **Free Tier:** $0 for 12 months
- **Production:** $50-200/month depending on traffic
- **Scalable:** Can handle millions of users

### Create `render.yaml` for IaC
```yaml
services:
  - type: web
    name: unisync
    env: python
    buildCommand: pip install -r auth_project/requirements.txt
    startCommand: daphne -b 0.0.0.0 -p $PORT auth_project.asgi:application
    envVars:
      - key: DEBUG
        value: false
      - key: SECRET_KEY
        value: ${SECRET_KEY}
      - key: DATABASE_URL
        value: ${DATABASE_URL}

databases:
  - name: postgres
    plan: standard
```

---

## 💻 DIGITALOCEAN (VPS)

### Why DigitalOcean?
✅ Affordable VPS ($6/month)  
✅ Full control  
✅ Great documentation  
✅ App Platform for easy deployment  

### Option A: App Platform (Easy)

1. Visit https://cloud.digitalocean.com
2. "Create" → "Apps"
3. Connect GitHub repo
4. Configure:

```
Name: unisync
Build Command: pip install -r auth_project/requirements.txt
Run Command: daphne -b 0.0.0.0 -p 8080 auth_project.asgi:application
```

5. Add PostgreSQL database
6. Set environment variables
7. Deploy

### Option B: Droplet + Manual Setup

#### Create Droplet
```
Size: $6/month (1GB RAM, 1 CPU)
OS: Ubuntu 22.04
Region: Closest to you
```

#### Connect via SSH
```bash
ssh root@your-droplet-ip
```

#### Update System
```bash
apt update && apt upgrade -y
apt install -y python3 python3-pip python3-venv postgresql postgresql-contrib nginx git
```

#### Clone Project
```bash
cd /var/www
git clone https://github.com/Goku0090/uni.git
cd uni/auth_project
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

#### Configure PostgreSQL
```bash
sudo -u postgres psql
CREATE DATABASE unisync_db;
CREATE USER unisync_user WITH PASSWORD 'strong_password';
GRANT ALL PRIVILEGES ON DATABASE unisync_db TO unisync_user;
\q
```

#### Configure Django
```bash
# Create .env file
cat > .env << 'EOF'
DEBUG=False
SECRET_KEY=your-secret-key
ALLOWED_HOSTS=your-domain.com
DATABASE_URL=postgresql://unisync_user:password@localhost:5432/unisync_db
EMAIL_BACKEND=accounts.brevo_mail_backend.BrevoEmailBackend
BREVO_API_KEY=your-key
SITE_URL=https://your-domain.com
EOF

# Run migrations
python manage.py migrate
python manage.py createsuperuser
python manage.py collectstatic --noinput
```

#### Setup Gunicorn
```bash
pip install gunicorn

# Create systemd service
sudo cat > /etc/systemd/system/unisync.service << 'EOF'
[Unit]
Description=UniSync Django Application
After=network.target

[Service]
User=www-data
WorkingDirectory=/var/www/uni/auth_project
Environment="PATH=/var/www/uni/auth_project/venv/bin"
ExecStart=/var/www/uni/auth_project/venv/bin/gunicorn --workers 4 --bind 127.0.0.1:8000 auth_project.wsgi:application

[Install]
WantedBy=multi-user.target
EOF

sudo systemctl start unisync
sudo systemctl enable unisync
```

#### Setup Daphne for WebSocket
```bash
sudo cat > /etc/systemd/system/unisync-daphne.service << 'EOF'
[Unit]
Description=UniSync Daphne WebSocket Server
After=network.target

[Service]
User=www-data
WorkingDirectory=/var/www/uni/auth_project
Environment="PATH=/var/www/uni/auth_project/venv/bin"
ExecStart=/var/www/uni/auth_project/venv/bin/daphne -b 0.0.0.0 -p 8001 auth_project.asgi:application

[Install]
WantedBy=multi-user.target
EOF

sudo systemctl start unisync-daphne
sudo systemctl enable unisync-daphne
```

#### Setup Nginx
```bash
sudo cat > /etc/nginx/sites-available/unisync << 'EOF'
upstream unisync {
    server 127.0.0.1:8000;
}

upstream unisync_daphne {
    server 127.0.0.1:8001;
}

server {
    listen 80;
    server_name your-domain.com;
    client_max_body_size 100M;

    location / {
        proxy_pass http://unisync;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }

    location /ws/ {
        proxy_pass http://unisync_daphne;
        proxy_http_version 1.1;
        proxy_set_header Upgrade $http_upgrade;
        proxy_set_header Connection "upgrade";
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
    }

    location /static/ {
        alias /var/www/uni/auth_project/staticfiles/;
    }

    location /media/ {
        alias /var/www/uni/auth_project/media/;
    }
}
EOF

sudo ln -s /etc/nginx/sites-available/unisync /etc/nginx/sites-enabled/
sudo nginx -t
sudo systemctl restart nginx
```

#### Setup SSL with Let's Encrypt
```bash
sudo apt install certbot python3-certbot-nginx -y
sudo certbot --nginx -d your-domain.com
sudo systemctl restart nginx
```

#### Cost on DigitalOcean
- **Droplet:** $6/month
- **Managed Database:** $15/month
- **App Platform:** $12/month
- **Total:** $21-33/month

---

## 🔴 HEROKU (LIMITED WEBSOCKET)

### Why Heroku?
✅ Very easy deploy  
✅ GitHub integration  
✅ Free tier available  
⚠️ WebSocket support limited  
⚠️ Can be expensive  

### Setup (Quick)

```bash
# Install Heroku CLI
# Windows: Download from https://devcenter.heroku.com/articles/heroku-cli

# Login
heroku login

# Create app
heroku create your-app-name

# Add PostgreSQL
heroku addons:create heroku-postgresql:hobby-dev

# Set environment variables
heroku config:set DEBUG=False
heroku config:set SECRET_KEY=your-key
heroku config:set EMAIL_BACKEND=accounts.brevo_mail_backend.BrevoEmailBackend

# Create Procfile
cat > Procfile << 'EOF'
web: daphne -b 0.0.0.0 -p $PORT auth_project.asgi:application
EOF

# Push to Heroku
git push heroku main

# Run migrations
heroku run python auth_project/manage.py migrate

# Create superuser
heroku run python auth_project/manage.py createsuperuser
```

### Cost on Heroku
- **Free Tier:** 550 free dyno hours (outdated)
- **Paid:** $14+ per month for reliable WebSocket support
- **Database:** $15+ per month
- **Total:** $29+/month

---

## 📦 VPS SELF-HOSTED

### Complete Manual Setup

#### Prerequisites
```bash
# VPS from: Linode, Vultr, AWS EC2, etc.
# OS: Ubuntu 22.04 LTS recommended
# Min specs: 2GB RAM, 1 CPU, 50GB storage
```

#### Full Setup Script
```bash
#!/bin/bash

# Update system
sudo apt update && sudo apt upgrade -y

# Install dependencies
sudo apt install -y \
    python3 python3-pip python3-venv \
    postgresql postgresql-contrib \
    nginx git supervisor redis-server

# Clone project
cd /var/www
sudo git clone https://github.com/Goku0090/uni.git
cd uni/auth_project

# Setup Python environment
sudo python3 -m venv venv
source venv/bin/activate
pip install --upgrade pip
pip install -r requirements.txt

# Setup PostgreSQL database
sudo -u postgres psql << EOF
CREATE DATABASE unisync_db;
CREATE USER unisync_user WITH PASSWORD 'strong_password';
GRANT ALL PRIVILEGES ON DATABASE unisync_db TO unisync_user;
ALTER ROLE unisync_user SET client_encoding TO 'utf8';
ALTER ROLE unisync_user SET default_transaction_isolation TO 'read committed';
ALTER ROLE unisync_user SET default_transaction_deferrable TO on;
ALTER ROLE unisync_user SET timezone TO 'UTC';
EOF

# Django setup
python manage.py migrate
python manage.py createsuperuser
python manage.py collectstatic --noinput

# Setup services (see sections above for systemd files)
# Start all services
sudo systemctl start unisync unisync-daphne nginx redis-server
sudo systemctl enable unisync unisync-daphne nginx redis-server

echo "Setup complete!"
```

---

## ✅ QUICK DEPLOYMENT (5 MINUTES)

### Fastest Option: Railway

```bash
# 1. Push code
git add .
git commit -m "Deploy to Railway"
git push origin main

# 2. Create account at https://railway.app

# 3. Connect GitHub repo

# 4. Add PostgreSQL service

# 5. Configure environment variables

# 6. Wait 2-3 minutes for auto-deploy

# 7. Visit your-app.railway.app
```

---

## 📋 PRODUCTION CHECKLIST

Before deploying to production:

### Django Settings
```python
# settings.py
DEBUG = False
ALLOWED_HOSTS = ['your-domain.com', 'www.your-domain.com']
SECRET_KEY = 'long-random-string'  # Generate new
SECURE_SSL_REDIRECT = True
SESSION_COOKIE_SECURE = True
CSRF_COOKIE_SECURE = True
SECURE_HSTS_SECONDS = 31536000
SECURE_HSTS_INCLUDE_SUBDOMAINS = True
SECURE_HSTS_PRELOAD = True
```

### Database
- [ ] Use PostgreSQL (not SQLite)
- [ ] Setup regular backups
- [ ] Configure connection pooling
- [ ] Monitor database size

### Static Files & Media
- [ ] Collect static files: `python manage.py collectstatic`
- [ ] Setup S3 or CDN for media
- [ ] Configure appropriate permissions

### Email
- [ ] Configure email backend (Brevo/ZeptoMail)
- [ ] Test email sending
- [ ] Setup sender verification

### Security
- [ ] Enable HTTPS/SSL certificate
- [ ] Setup firewall rules
- [ ] Configure CORS headers
- [ ] Enable CSRF protection
- [ ] Setup rate limiting

### Monitoring
- [ ] Setup error tracking (Sentry)
- [ ] Configure logging
- [ ] Setup uptime monitoring
- [ ] Monitor resource usage

### Performance
- [ ] Enable caching (Redis)
- [ ] Setup CDN for static files
- [ ] Optimize database queries
- [ ] Monitor response times

### Backups
- [ ] Database backups (daily)
- [ ] Media files backup
- [ ] Code repository backup
- [ ] Test restore process

---

## 🌐 DOMAIN & SSL SETUP

### Using Render/Railway
```
1. Register domain (Namecheap, GoDaddy, etc.)
2. In provider settings:
   - Add CNAME record pointing to your app
3. In Render/Railway settings:
   - Add custom domain
   - Auto-provision SSL (Let's Encrypt)
4. Wait 5-10 minutes for DNS propagation
```

### Using DigitalOcean/Custom VPS
```bash
# Update DNS records at your domain registrar
A Record: your-domain.com → your-vps-ip
CNAME: www.your-domain.com → your-domain.com

# Install SSL with Let's Encrypt
sudo apt install certbot python3-certbot-nginx
sudo certbot certonly --nginx -d your-domain.com -d www.your-domain.com

# Update Nginx config (auto-updated by certbot)
sudo systemctl restart nginx
```

---

## 📊 ENVIRONMENT VARIABLES TEMPLATE

Create `.env` file:
```bash
# Django
DEBUG=False
SECRET_KEY=your-secret-key-here
ALLOWED_HOSTS=your-domain.com,www.your-domain.com

# Database
DATABASE_URL=postgresql://user:password@host:5432/dbname

# Email
EMAIL_BACKEND=accounts.brevo_mail_backend.BrevoEmailBackend
EMAIL_FROM=noreply@your-domain.com
BREVO_API_KEY=your-brevo-api-key

# OAuth
GOOGLE_OAUTH_CLIENT_ID=xxx.apps.googleusercontent.com
GOOGLE_OAUTH_SECRET=xxx

# URLs
SITE_URL=https://your-domain.com
CALLBACK_URL=https://your-domain.com/oauth/callback

# Optional
REDIS_URL=redis://localhost:6379
SENTRY_DSN=your-sentry-dsn
```

---

## 🚀 POST-DEPLOYMENT

### Immediate Tasks
```bash
# 1. Run migrations
python manage.py migrate

# 2. Create superuser
python manage.py createsuperuser

# 3. Collect static files
python manage.py collectstatic --noinput

# 4. Create initial data (optional)
python manage.py loaddata initial_data.json

# 5. Test features
# - Try login (OTP & OAuth)
# - Create a project
# - Test messaging
# - Check admin panel
```

### Monitoring
```
# Daily:
- Check error logs
- Monitor uptime
- Verify emails sent

# Weekly:
- Review performance metrics
- Check database size
- Monitor user growth

# Monthly:
- Analyze usage statistics
- Review security logs
- Plan improvements
```

---

## 💰 COST COMPARISON (Monthly)

| Platform | Cost | Notes |
|----------|------|-------|
| **Render** | $22 | Easiest for this project |
| **Railway** | $10 | Best value (free $5 credit) |
| **Heroku** | $29+ | Expensive for WebSockets |
| **DigitalOcean** | $21 | Good control, more setup |
| **AWS** | $0-200 | Free tier, scalable |
| **Self-hosted VPS** | $5-30 | Full control, more work |

---

## 📞 TROUBLESHOOTING

### WebSocket Connection Fails
```
Check:
- Ensure Daphne is running
- Check proxy configuration
- Verify ALLOWED_HOSTS
- Check firewall rules
- Look for CORS issues
```

### Migrations Error
```bash
# Reset database (development only!)
python manage.py migrate accounts zero
python manage.py migrate

# Or check specific app
python manage.py showmigrations accounts
```

### Static Files Not Loading
```bash
# Collect static files again
python manage.py collectstatic --noinput --clear

# Check STATIC_URL and STATIC_ROOT
python manage.py shell
>>> from django.conf import settings
>>> print(settings.STATIC_URL)
>>> print(settings.STATIC_ROOT)
```

### Email Not Sending
```bash
# Test email configuration
python manage.py shell
>>> from django.core.mail import send_mail
>>> send_mail('Test', 'Test message', 'from@example.com', ['to@example.com'])
```

---

## 🎯 RECOMMENDED PATH

**For Beginners:**
1. Render (easiest WebSocket support)
2. Cost: ~$22/month
3. Time: 30 minutes to deploy
4. Features: Everything included

**For Cost-Conscious:**
1. Railway (free $5 credit)
2. Cost: ~$10/month after credit
3. Time: 20 minutes to deploy
4. Features: Everything included

**For Control & Scalability:**
1. AWS or DigitalOcean
2. Cost: $20-50/month
3. Time: 2-4 hours initial setup
4. Features: Full flexibility

**For Learning:**
1. Self-hosted VPS
2. Cost: $5-30/month
3. Time: 4-6 hours setup
4. Features: Ultimate control

---

## 📚 NEXT STEPS

1. **Choose Platform** (See comparison above)
2. **Follow Platform Guide** (Render/Railway recommended)
3. **Setup Domain** (If deploying to production)
4. **Configure Email** (Brevo/ZeptoMail)
5. **Monitor & Maintain** (Daily checks)
6. **Scale When Needed** (Use metrics to plan)

---

## 🔗 Resources

- **Render:** https://render.com/docs
- **Railway:** https://docs.railway.app
- **AWS:** https://docs.aws.amazon.com
- **DigitalOcean:** https://www.digitalocean.com/docs
- **Django Deployment:** https://docs.djangoproject.com/en/stable/howto/deployment
- **Channels Deployment:** https://channels.readthedocs.io/en/latest/deploying.html

---

**Choose your platform above and get hosting in 30 minutes!** 🚀

---

**Status:** ✅ Complete Hosting Guide  
**Last Updated:** February 09, 2026  
**Platforms Covered:** 6  
**Quick Deploy Time:** 5-30 minutes
