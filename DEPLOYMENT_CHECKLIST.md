# UniSync Deployment Checklist

**Project:** UniSync Student Collaboration Platform  
**Repository:** https://github.com/Goku0090/uni_sync  
**Status:** Ready for Deployment

---

## Pre-Deployment (Do Before Deploying)

### Environment Setup
- [ ] Generate Django SECRET_KEY
- [ ] Set up Brevo account and get API key
- [ ] Create Google OAuth credentials
- [ ] Create GitHub OAuth credentials
- [ ] Get RapidAPI key (universities list)
- [ ] Prepare domain name (if using custom domain)
- [ ] Gather all required credentials in secure location

### Code Verification
- [ ] Code pushed to GitHub (https://github.com/Goku0090/uni_sync)
- [ ] `.env` file NOT in git (verified in .gitignore)
- [ ] `Procfile` exists in root directory
- [ ] `railway.json` exists in root directory
- [ ] `render.yaml` exists in root directory
- [ ] `requirements.txt` in auth_project/ directory
- [ ] `manage.py` in auth_project/ directory
- [ ] All imports working (no syntax errors)

### Database Preparation
- [ ] Identified database choice (PostgreSQL)
- [ ] Understand migration process
- [ ] Know how to create superuser

---

## OPTION A: Deploy to Render

### Create & Configure Render Service

**Step 1: Initial Setup**
- [ ] Create Render account (https://render.com)
- [ ] Connect GitHub repository to Render
- [ ] Create Web Service:
  - Name: `unisync`
  - Environment: Python
  - Plan: Starter (paid recommended) or Free
  - Branch: main
  - Build command: `pip install -r auth_project/requirements.txt && python auth_project/manage.py collectstatic --noinput`
  - Start command: `gunicorn auth_project.wsgi:application --bind 0.0.0.0:10000`

**Step 2: Create Database**
- [ ] Create PostgreSQL service in Render
- [ ] Name: `unisync-db`
- [ ] Same region as web service
- [ ] Note DATABASE_URL (provided automatically)

**Step 3: Set Environment Variables**
- [ ] DEBUG=False
- [ ] SECRET_KEY=<generated-key>
- [ ] ALLOWED_HOSTS=unisync.onrender.com,yourdomain.com
- [ ] BREVO_API_KEY=<your-key>
- [ ] GOOGLE_CLIENT_ID=<your-id>
- [ ] GOOGLE_CLIENT_SECRET=<your-secret>
- [ ] GITHUB_CLIENT_ID=<your-id>
- [ ] GITHUB_CLIENT_SECRET=<your-secret>
- [ ] RAPIDAPI_KEY=<your-key>
- [ ] DEFAULT_FROM_EMAIL=noreply@yourdomain.com
- [ ] SECURE_SSL_REDIRECT=True
- [ ] SESSION_COOKIE_SECURE=True
- [ ] CSRF_COOKIE_SECURE=True

**Step 4: Deploy**
- [ ] Click "Create Web Service"
- [ ] Monitor build process in Logs
- [ ] Deployment completes successfully
- [ ] Service shows "Live" status

### Post-Deployment

**Step 5: Run Migrations**
- [ ] Go to web service Shell
- [ ] Run: `python auth_project/manage.py migrate`
- [ ] Create superuser: `python auth_project/manage.py createsuperuser`
- [ ] Collect static: `python auth_project/manage.py collectstatic --noinput`

**Step 6: Verify Deployment**
- [ ] Access https://unisync.onrender.com in browser
- [ ] Login page loads
- [ ] Static files load (CSS visible)
- [ ] Create test user
- [ ] Test OTP email
- [ ] Test login

**Step 7: Configure Custom Domain (Optional)**
- [ ] Go to Web Service Settings
- [ ] Add custom domain
- [ ] Update DNS CNAME record
- [ ] Verify domain

**Step 8: Configure Django Admin**
- [ ] Access /admin
- [ ] Login with superuser
- [ ] Go to Sites → Update domain
- [ ] Go to Social Applications → Add Google OAuth
- [ ] Go to Social Applications → Add GitHub OAuth

---

## OPTION B: Deploy to Railway

### Create & Configure Railway Service

**Step 1: Initial Setup**
- [ ] Create Railway account (https://railway.app)
- [ ] Connect GitHub repository
- [ ] Select `uni_sync` repo
- [ ] Railway auto-detects Django app

**Step 2: Add PostgreSQL**
- [ ] Click "Add" → PostgreSQL
- [ ] Railway auto-creates and links
- [ ] DATABASE_URL automatically set

**Step 3: Set Environment Variables**
- [ ] DEBUG=False
- [ ] SECRET_KEY=<generated-key>
- [ ] ALLOWED_HOSTS=*.railway.app,yourdomain.com
- [ ] BREVO_API_KEY=<your-key>
- [ ] GOOGLE_CLIENT_ID=<your-id>
- [ ] GOOGLE_CLIENT_SECRET=<your-secret>
- [ ] GITHUB_CLIENT_ID=<your-id>
- [ ] GITHUB_CLIENT_SECRET=<your-secret>
- [ ] RAPIDAPI_KEY=<your-key>
- [ ] DEFAULT_FROM_EMAIL=noreply@yourdomain.com
- [ ] SECURE_SSL_REDIRECT=True
- [ ] SESSION_COOKIE_SECURE=True
- [ ] CSRF_COOKIE_SECURE=True

**Step 4: Deploy**
- [ ] Push code to GitHub (if not already)
- [ ] Railway auto-builds and deploys
- [ ] Monitor Deployments tab
- [ ] Deployment completes successfully

### Post-Deployment

**Step 5: Run Migrations**
- [ ] Go to web service Shell
- [ ] Run: `python auth_project/manage.py migrate`
- [ ] Create superuser: `python auth_project/manage.py createsuperuser`
- [ ] Collect static: `python auth_project/manage.py collectstatic --noinput`

**Step 6: Verify Deployment**
- [ ] Get domain from Settings → Domains
- [ ] Access app in browser
- [ ] Login page loads
- [ ] Static files load (CSS visible)
- [ ] Create test user
- [ ] Test OTP email
- [ ] Test login

**Step 7: Add Custom Domain (Optional)**
- [ ] Go to Settings → Domains
- [ ] Click "Add Domain"
- [ ] Enter domain
- [ ] Update DNS records as shown
- [ ] Verify domain

**Step 8: Configure Django Admin**
- [ ] Access /admin
- [ ] Login with superuser
- [ ] Go to Sites → Update domain
- [ ] Go to Social Applications → Add Google OAuth
- [ ] Go to Social Applications → Add GitHub OAuth

---

## Final Verification (Both Platforms)

### Functionality Testing
- [ ] **Authentication**
  - [ ] Login page loads
  - [ ] Register page works
  - [ ] OTP email sends
  - [ ] OTP verification works
  - [ ] Dashboard loads after login

- [ ] **Profiles**
  - [ ] Profile page loads
  - [ ] Edit profile works
  - [ ] Upload profile photo works
  - [ ] Profile saves correctly

- [ ] **Projects**
  - [ ] Create project works
  - [ ] Project appears in feed
  - [ ] Edit project works
  - [ ] Delete project works
  - [ ] Like/comment project works

- [ ] **Messaging**
  - [ ] Find collaborators works
  - [ ] Send message works
  - [ ] Message appears in chat
  - [ ] Create group chat works

- [ ] **Social Features**
  - [ ] Send connection request works
  - [ ] Accept connection works
  - [ ] Follow user works
  - [ ] Activity feed shows updates

- [ ] **Admin**
  - [ ] Admin panel accessible
  - [ ] Can view all models
  - [ ] Can create/edit/delete records

### Technical Verification
- [ ] **Database**
  - [ ] Database connected
  - [ ] All migrations applied
  - [ ] Tables created successfully

- [ ] **Email**
  - [ ] OTP emails send
  - [ ] Email content correct
  - [ ] Delivery reliable

- [ ] **Static Files**
  - [ ] CSS loads
  - [ ] JS works
  - [ ] Images display
  - [ ] No 404 errors

- [ ] **API**
  - [ ] REST endpoints accessible
  - [ ] Authentication works
  - [ ] CORS configured (if needed)

- [ ] **Security**
  - [ ] HTTPS redirects enabled
  - [ ] DEBUG=False in production
  - [ ] Secret key not visible
  - [ ] Credentials only in env vars

- [ ] **Logging**
  - [ ] Application logs visible
  - [ ] Error logs captured
  - [ ] No critical errors

---

## Production Readiness

### Before Going Live
- [ ] Set custom domain
- [ ] Update ALLOWED_HOSTS to include domain
- [ ] Enable HTTPS
- [ ] Test with real domain
- [ ] Set up monitoring/alerts
- [ ] Set up automated backups
- [ ] Create documentation
- [ ] Set up monitoring dashboard

### Ongoing Maintenance
- [ ] Monitor server logs daily
- [ ] Check error rates
- [ ] Monitor database size
- [ ] Backup database regularly
- [ ] Update dependencies monthly
- [ ] Monitor uptime
- [ ] Review security regularly
- [ ] Monitor storage usage

---

## Deployment Summary Template

```
DEPLOYMENT COMPLETED: [DATE]

Environment: [Render/Railway/Both]
Domain: [your-domain.com]
Branch: main
Commit: [commit-hash]

Services:
- Web Service: [status]
- Database: [status]
- Email: [Brevo/ZeptoMail/Gmail]
- OAuth: [Google + GitHub]

Environment Variables: [count] configured
Migrations: [count] applied
Superuser: [username]

Testing Status: [PASSED/FAILED]
Critical Issues: [NONE/list]
Next Steps: [list]

Deployment By: [your-name]
Approved By: [name]
```

---

## Rollback Plan (If Issues)

1. **Identify Issue**
   - Check logs
   - Identify root cause
   - Document error

2. **Render Rollback**
   - Go to Deployments
   - Select previous successful deployment
   - Click "Redeploy"

3. **Railway Rollback**
   - Go to Deployments
   - Click previous deployment
   - Click "Redeploy"

4. **Database Issues**
   - Keep recent backups
   - Restore from backup if needed
   - Re-run migrations if necessary

5. **Communication**
   - Notify users of issue
   - Provide ETA for fix
   - Update after resolution

---

## Post-Deployment Checklist (After Going Live)

**Week 1**
- [ ] Monitor error logs closely
- [ ] Check performance metrics
- [ ] Test all main features
- [ ] Verify email delivery
- [ ] Check database performance
- [ ] Monitor storage usage

**Month 1**
- [ ] Review error logs
- [ ] Optimize slow queries
- [ ] Review security
- [ ] Update documentation
- [ ] Plan scaling if needed
- [ ] Set up monitoring alerts

**Ongoing**
- [ ] Weekly log review
- [ ] Monthly backups check
- [ ] Quarterly security audit
- [ ] Update dependencies
- [ ] Monitor uptime/performance
- [ ] Plan improvements

---

## Support & Documentation

- **Deployment Guide:** DEPLOYMENT_RENDER_RAILWAY.md
- **Environment Setup:** ENVIRONMENT_SETUP_GUIDE.md
- **Code Analysis:** CODEBASE_COMPREHENSIVE_ANALYSIS_DETAILED.md
- **GitHub:** https://github.com/Goku0090/uni_sync

---

## Emergency Contacts

- Render Support: https://render.com/support
- Railway Support: https://railway.app/support
- Django Docs: https://docs.djangoproject.com
- Django REST: https://www.django-rest-framework.org

---

**Status: READY FOR DEPLOYMENT** ✅

Complete this checklist before going live!

Date Completed: __________
Completed By: __________
Verified By: __________
