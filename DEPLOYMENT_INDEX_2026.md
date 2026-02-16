# Deployment Documentation Index

## 📋 Quick Links

### For Immediate Deployment
👉 **START HERE:** `DEPLOY_NOW_QUICK_START_2026.md`
- Step-by-step deployment to Render.com
- Takes 30 minutes start to finish
- All commands provided
- Troubleshooting included

### For In-Depth Understanding  
👉 `DEPLOYMENT_GUIDE_COMPLETE_2026.md`
- All deployment options (Render, Railway, AWS, etc.)
- Pre-deployment checklist
- Security considerations
- Monitoring & maintenance
- Cost estimates

---

## Deployment Paths

### Path 1: Render.com (Recommended for Beginners)

```
30 minutes total
├─ Step 1: Create GitHub repo (5 min)
├─ Step 2: Create render.yaml (5 min)
├─ Step 3: Deploy (10 min)
├─ Step 4: Set env variables (5 min)
└─ Step 5: Test app (5 min)

Cost: FREE (with limitations)
Effort: ⭐⭐ (Very Easy)
```

**Best for:** Learning, prototyping, small projects

### Path 2: Railway.app

```
25 minutes total
├─ Step 1: GitHub repo
├─ Step 2: Signup & connect
├─ Step 3: Deploy (auto-detects Django)
├─ Step 4: Add PostgreSQL
├─ Step 5: Add Redis

Cost: $5 credits/month FREE
Effort: ⭐⭐ (Very Easy)
```

**Best for:** Quick deployment, no config

### Path 3: Self-Hosted (VPS)

```
2 hours total
├─ Step 1: Rent VPS ($5-10/month)
├─ Step 2: Setup OS
├─ Step 3: Install dependencies
├─ Step 4: Clone code
├─ Step 5: Configure Nginx
├─ Step 6: Run Gunicorn
└─ Step 7: Setup SSL

Cost: $5-10/month
Effort: ⭐⭐⭐⭐⭐ (Very Hard)
```

**Best for:** Full control, learn DevOps, production

### Path 4: AWS

```
3 hours total
├─ Step 1: Create AWS account
├─ Step 2: Launch EC2
├─ Step 3: Setup RDS (database)
├─ Step 4: Configure security groups
├─ Step 5: Deploy app
└─ Step 6: Setup monitoring

Cost: $20-100+/month
Effort: ⭐⭐⭐⭐ (Hard)
```

**Best for:** Scaling, production, enterprise

---

## What You Need Before Deploying

### Pre-Deployment Checklist

- [ ] Code runs locally without errors
- [ ] `requirements.txt` is up-to-date
- [ ] `.gitignore` created and committed
- [ ] Code pushed to GitHub
- [ ] No hardcoded secrets in code
- [ ] `DEBUG=False` will be set in production
- [ ] Database migrations tested
- [ ] Static files will be collected

### Environment Variables Required

```
MUST SET:
├─ DEBUG=False
├─ SECRET_KEY=(generated value)
├─ ALLOWED_HOSTS=your-domain.com
└─ DATABASE_URL=(provided by platform)

OPTIONAL:
├─ BREVO_API_KEY (for email)
├─ GOOGLE_CLIENT_ID (for OAuth)
├─ GOOGLE_CLIENT_SECRET (for OAuth)
├─ GITHUB_CLIENT_ID (for OAuth)
└─ GITHUB_CLIENT_SECRET (for OAuth)
```

### Files to Create

```
render.yaml         ← Render deployment config
.gitignore          ← What to exclude from git
.env.example        ← Template for env variables
build.sh            ← Build script (already have this)
```

---

## Step-by-Step for Render.com

### 1. Create GitHub Repository (5 min)

```bash
# Initialize git
cd /path/to/project
git init
git add .
git commit -m "Initial commit"

# Create GitHub repo at https://github.com/new
# Then:
git remote add origin https://github.com/YOUR_USERNAME/unisync.git
git branch -M main
git push -u origin main
```

### 2. Create render.yaml (5 min)

```bash
# In root folder, create: render.yaml
# Copy content from DEPLOY_NOW_QUICK_START_2026.md
```

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

  - type: redis
    name: redis
```

### 3. Push to GitHub (2 min)

```bash
git add render.yaml
git commit -m "Add Render config"
git push origin main
```

### 4. Deploy on Render (10 min)

1. Go to https://render.com
2. Sign up with GitHub
3. Click "New +" → "Blueprint"
4. Select repo → "Create Blueprint"
5. Wait for build (5-10 min)

### 5. Set Environment Variables (5 min)

1. Render Dashboard → Your app → Environment
2. Add:
   ```
   SECRET_KEY = [generate and paste]
   BREVO_API_KEY = [your key or leave blank]
   GOOGLE_CLIENT_ID = [leave blank for now]
   GOOGLE_CLIENT_SECRET = [leave blank for now]
   ```

### 6. Create Admin User (3 min)

1. Render Dashboard → Your app → Shell
2. Run:
   ```bash
   python backend/manage.py createsuperuser
   ```

### 7. Test (5 min)

1. Visit: `https://your-app-name.onrender.com`
2. Test login, create project, chat
3. Success! ✓

---

## What Each Platform Provides

### Render.com

```
✅ Automatic SSL (HTTPS)
✅ Automatic deploys from GitHub
✅ Built-in PostgreSQL database
✅ Built-in Redis cache
✅ Environment variables
✅ Shell/SSH access
✅ Logs & monitoring
✅ Free tier available
❌ Limited to 750 hours/month free
```

### Railway.app

```
✅ Auto-detects Django
✅ Automatic SSL
✅ Built-in PostgreSQL
✅ Built-in Redis
✅ Beautiful UI
✅ $5 monthly credits
✅ Instant deploys
❌ Credits only last ~1 week
```

### AWS

```
✅ Unlimited scale
✅ Full control
✅ Pay-as-you-go
✅ All AWS services
❌ Complex setup
❌ Can be expensive
❌ Steep learning curve
```

### Self-Hosted (VPS)

```
✅ Full control
✅ Cheapest long-term
✅ No vendor lock-in
✅ Run anything
❌ You manage everything
❌ Security responsibility
❌ 24/7 monitoring needed
```

---

## Common Deployment Issues & Fixes

### Issue: "DEBUG=False causes 404"

**Fix:**
```python
# settings.py
ALLOWED_HOSTS = ['your-domain.com', 'www.your-domain.com']
STATIC_URL = '/static/'
STATIC_ROOT = BASE_DIR / 'staticfiles'
```

Then run:
```bash
python manage.py collectstatic --noinput
```

### Issue: "Static files not showing"

**Cause:** collectstatic not run during build

**Fix:** Add to build command:
```yaml
buildCommand: |
  pip install -r requirements.txt
  python manage.py collectstatic --noinput
```

### Issue: "OAuth login fails"

**Cause:** Redirect URI mismatch

**Fix:** Update in Google/GitHub settings:
```
Redirect URI: https://your-app.onrender.com/accounts/google/login/callback/
```

### Issue: "Database migration error"

**Cause:** Migrations not running

**Fix:** Add to build command:
```yaml
buildCommand: |
  python manage.py migrate
```

### Issue: "WebSocket not connecting"

**Cause:** Redis not configured or Daphne not running

**Fix:** Ensure:
1. Redis service is created
2. CHANNEL_LAYERS configured
3. Use `daphne` or `channels` for ASGI

---

## Post-Deployment Checklist

- [ ] App loads without errors
- [ ] Login works (email & OAuth)
- [ ] Create project works
- [ ] Chat sends messages
- [ ] Admin panel accessible
- [ ] Static files load (CSS, images)
- [ ] Database working
- [ ] Logs show no errors

---

## Monitoring After Deployment

### Daily
- Check error logs
- Monitor uptime

### Weekly
- Review performance metrics
- Check database size
- Test backup/restore

### Monthly
- Update dependencies
- Review security logs
- Test disaster recovery

---

## Performance Optimization

### Before Deployment
```python
# settings.py
CACHES = {
    'default': {
        'BACKEND': 'django_redis.cache.RedisCache',
        'LOCATION': os.getenv('REDIS_URL'),
    }
}

DATABASES['default']['CONN_MAX_AGE'] = 600
```

### After Deployment
- [ ] Enable CDN for static files
- [ ] Setup database indexes
- [ ] Enable gzip compression
- [ ] Setup monitoring/APM
- [ ] Configure caching headers

---

## Cost Breakdown (Monthly)

### Free Option
```
Render.com Free Tier: $0
├─ 750 hours/month (perfect for 1 app)
├─ Shared database
├─ Shared Redis
└─ No credit card needed
```

### Starter ($10-20/month)
```
Render.com Starter:
├─ Web dyno: $7/month
├─ PostgreSQL: $15/month
└─ Total: ~$22/month
```

### Growth ($50-100/month)
```
Render.com Growth:
├─ Web dyno: $25/month
├─ PostgreSQL: $60/month
├─ Redis: $15/month
└─ Total: ~$100/month
```

### Scale ($200+/month)
```
AWS/Self-Hosted:
├─ Compute: $50-200/month
├─ Database: $50-200/month
├─ Storage: $10-50/month
└─ Monitoring: $10-50/month
```

---

## Deployment Timeline

### Today (30 minutes)
- [ ] Create GitHub repo
- [ ] Deploy to Render
- [ ] App goes live

### This Week (1-2 hours)
- [ ] Add custom domain
- [ ] Setup OAuth (Google/GitHub)
- [ ] Enable email functionality
- [ ] Test all features

### This Month (ongoing)
- [ ] Monitor performance
- [ ] Fix bugs
- [ ] Optimize database
- [ ] Setup alerts

### Next Quarter
- [ ] Scale infrastructure
- [ ] Add CDN
- [ ] Setup APM
- [ ] Backup strategy

---

## Document Map

```
Deployment Documentation
├─ DEPLOY_NOW_QUICK_START_2026.md
│  └─ Fast deployment to Render (start here!)
│
├─ DEPLOYMENT_GUIDE_COMPLETE_2026.md
│  └─ All platforms, detailed setup
│
├─ DEPLOYMENT_INDEX_2026.md
│  └─ This file, navigation & overview
│
└─ Related Files
   ├─ START_HERE_REAL_STRUCTURE_2026.md (understand your app)
   ├─ DEVELOPMENT_SETUP_GUIDE_COMPLETE_2026.md (local setup)
   └─ QUICK_FACTS_YOUR_PROJECT_2026.md (quick reference)
```

---

## Quick Decision Tree

```
Where should I deploy?

├─ I want it FAST (today)
│  └─ Use Render.com ✓
│
├─ I want it FREE forever
│  └─ Use self-hosted VPS ($5/month)
│
├─ I want easy updates
│  └─ Use Render or Railway
│
├─ I want full control
│  └─ Use self-hosted VPS
│
├─ I need to scale big
│  └─ Use AWS
│
└─ I'm unsure
   └─ Start with Render.com, migrate later if needed
```

---

## Summary

1. **Best choice for you:** Render.com (fast, free tier, easy)
2. **Time to deploy:** 30 minutes
3. **Cost:** $0 (free tier) or $7-15/month (paid tier)
4. **Result:** Live app on internet
5. **Next:** Setup domain, OAuth, monitoring

---

## Start Now

👉 Read: `DEPLOY_NOW_QUICK_START_2026.md`
⏱️ Time: 30 minutes
🎯 Result: Live app

Let's go! 🚀

