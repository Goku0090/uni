# Complete Render Deployment Checklist

## Pre-Deployment Phase

### Code Preparation
- [ ] All code committed and pushed to GitHub
- [ ] No sensitive data in code (API keys, passwords)
- [ ] All dependencies listed in `requirements.txt`
- [ ] `.gitignore` excludes `.env`, `*.sqlite3`, `media/`, `staticfiles/`
- [ ] `build.sh` script exists and is executable
- [ ] `render.yaml` at repository root
- [ ] All migrations created: `python manage.py makemigrations`

### Settings & Configuration
- [ ] `DEBUG = False` for production
- [ ] `SECRET_KEY` will be set via environment variable
- [ ] `ALLOWED_HOSTS` includes Render domain
- [ ] Database configured for PostgreSQL fallback
- [ ] Email backend configured for production
- [ ] Static files configured with WhiteNoise
- [ ] Media files directory configured
- [ ] CORS settings appropriate for production
- [ ] Logging configured for production

### Security Review
- [ ] No hardcoded credentials anywhere
- [ ] CSRF protection enabled in production
- [ ] SECURE_SSL_REDIRECT = True
- [ ] SESSION_COOKIE_SECURE = True
- [ ] CSRF_COOKIE_SECURE = True
- [ ] All user inputs validated/sanitized
- [ ] SQL injection protection verified
- [ ] XSS protection enabled
- [ ] CORS properly configured

### Testing
- [ ] All tests pass locally: `python manage.py test`
- [ ] No migration conflicts
- [ ] Static files collect correctly: `python manage.py collectstatic`
- [ ] Can run locally with PostgreSQL
- [ ] Environment variables working via `.env`
- [ ] Email sending tested (or console backend)

---

## Render Dashboard Setup

### 1. Create Render Account
- [ ] Sign up at https://render.com
- [ ] Connect GitHub account
- [ ] Authorize repository access

### 2. Create Blueprint Deployment
- [ ] Click "New" → "Blueprint"
- [ ] Select repository
- [ ] Select branch (main/master)
- [ ] Review `render.yaml` configuration
- [ ] Click "Deploy"

### 3. PostgreSQL Setup (Auto-Created)
- [ ] Wait for PostgreSQL service to initialize
- [ ] Verify database name: `unisync_db`
- [ ] Verify database user: `unisync_user`
- [ ] Note the auto-generated `DATABASE_URL`

### 4. Web Service Setup
- [ ] Build process completes successfully
- [ ] Migrations run automatically via `build.sh`
- [ ] Service starts without errors
- [ ] Logs show successful startup

---

## Environment Variables Configuration

### In Render Dashboard → Settings → Environment

| Variable | Value | Required |
|----------|-------|----------|
| `DATABASE_URL` | Auto-generated | ✓ Auto |
| `SECRET_KEY` | Generate new | ✓ Required |
| `DEBUG` | false | ✓ Required |
| `ALLOWED_HOSTS` | yourdomain.onrender.com | ✓ Required |
| `DEFAULT_FROM_EMAIL` | noreply@unisync.app | ✓ Required |
| `BREVO_API_KEY` | Your API key | ⚠ Optional |
| `GOOGLE_CLIENT_ID` | Your client ID | ⚠ Optional |
| `GOOGLE_CLIENT_SECRET` | Your secret | ⚠ Optional |
| `GITHUB_CLIENT_ID` | Your client ID | ⚠ Optional |
| `GITHUB_CLIENT_SECRET` | Your secret | ⚠ Optional |
| `SECURE_SSL_REDIRECT` | true | ⚠ Optional |
| `SESSION_COOKIE_SECURE` | true | ⚠ Optional |
| `CSRF_COOKIE_SECURE` | true | ⚠ Optional |

### Generate SECRET_KEY

```bash
python -c "from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())"
```

Copy the output and paste into Render environment.

---

## Initial Deployment Steps

### Step 1: Deploy Infrastructure
```
1. Click "Deploy" in Render blueprint
2. Wait for PostgreSQL to initialize (2-5 minutes)
3. Wait for web service to build (3-10 minutes)
4. Watch logs for any errors
```

### Step 2: Verify Build
Check logs for:
```
✓ pip install requirements
✓ python manage.py collectstatic
✓ python manage.py migrate
✓ Application started on 0.0.0.0:10000
```

### Step 3: Database Initialization
In Render dashboard → your-service → Shell:
```bash
python manage.py migrate --check  # Verify migrations
python manage.py createsuperuser   # Create admin user
```

### Step 4: Access Application
- [ ] Navigate to `https://yourdomain.onrender.com`
- [ ] Verify homepage loads
- [ ] Test login page
- [ ] Test registration form
- [ ] Access admin at `/admin/`

---

## Post-Deployment Verification

### Core Functionality
- [ ] Homepage loads without errors
- [ ] Registration form works
- [ ] OTP sending works (check email or console)
- [ ] Login flow completes
- [ ] Dashboard displays correctly
- [ ] User profile page loads
- [ ] Project creation works
- [ ] File uploads work (test in messages)
- [ ] Search functionality works
- [ ] API endpoints return correct data

### Database
- [ ] Tables created: `\dt` in psql
- [ ] Data persists after refresh
- [ ] User data saved correctly
- [ ] Project data retrieves correctly
- [ ] Messages store properly
- [ ] Connections save properly

### Static Files
- [ ] CSS loads (check page source)
- [ ] JavaScript loads (check console)
- [ ] Images display correctly
- [ ] No 404 errors in network tab

### Email
- [ ] Registration OTP email sent
- [ ] Password reset email sent
- [ ] Notification emails sent
- [ ] No email errors in logs

### API
- [ ] `/api/home/` returns JSON
- [ ] `/api/check-username/?username=test` works
- [ ] `/api/check-email/?email=test@example.com` works
- [ ] `/api/user-stats/` returns user statistics
- [ ] Authentication required endpoints return 401 when not logged in

### Security
- [ ] HTTPS working (lock icon in browser)
- [ ] Redirect HTTP → HTTPS
- [ ] No mixed content warnings
- [ ] Admin site protected
- [ ] API endpoints require authentication (where applicable)
- [ ] CSRF tokens present in forms

---

## Monitoring & Logging

### Daily Checks
- [ ] Application logs show no errors
- [ ] Database connection healthy
- [ ] No 500 errors in logs
- [ ] Response times acceptable (<2s)
- [ ] Backup scheduled/completed

### Weekly Checks
- [ ] Database size reasonable
- [ ] Old OTP codes cleaned up
- [ ] Activity feed working
- [ ] Notifications sending properly
- [ ] File storage not full

### Monthly Checks
- [ ] Backup tested (restore test)
- [ ] Security patches applied
- [ ] Dependencies updated
- [ ] Performance metrics reviewed
- [ ] Usage patterns analyzed

### Monitoring Dashboard
```bash
# View logs in Render
render logs --service unisync-django

# View database logs
render logs --database unisync-postgres

# Check service status
render services
```

---

## Troubleshooting During Deployment

### Issue: Build Fails
**Solution:**
1. Check build logs in Render dashboard
2. Verify all dependencies in `requirements.txt`
3. Ensure `build.sh` is correct
4. Try building locally: `bash build.sh`

### Issue: Migrations Fail
**Solution:**
```bash
# Locally, resolve conflicts
python manage.py makemigrations accounts
python manage.py migrate --plan
# Fix any issues, then push to GitHub
```

### Issue: PostgreSQL Connection Fails
**Solution:**
1. Verify DATABASE_URL environment variable is set
2. Check PostgreSQL service is running (green indicator in Render)
3. Verify database credentials in `render.yaml`
4. Test connection: `python manage.py dbshell`

### Issue: Static Files Missing
**Solution:**
```bash
# In Render shell
python manage.py collectstatic --noinput --clear
```

### Issue: Email Not Sending
**Solution:**
1. Check email backend in settings: console vs Brevo/Gmail
2. Verify email credentials in environment variables
3. Check email logs: `python manage.py shell`
4. Test email: `django.core.mail.send_mail(...)`

---

## Data Migration (if transferring from existing DB)

### Backup Existing Data
```bash
# Export from old database
pg_dump -U user olddb > backup.sql
```

### Import to Render
1. Get DATABASE_URL from Render environment
2. Parse connection details
3. Import data:
```bash
# Set DATABASE_URL from Render env
export DATABASE_URL="postgresql://..."
psql "$DATABASE_URL" < backup.sql
```

### Verify Import
```bash
# In Render shell
python manage.py shell
>>> from django.contrib.auth.models import User
>>> User.objects.count()
>>> from accounts.models import Project
>>> Project.objects.count()
```

---

## Performance Optimization

### After Successful Deployment

1. **Enable Caching**
   - [ ] Configure Redis (if not free plan)
   - [ ] Add cache decorators to views
   - [ ] Cache database queries

2. **Database Optimization**
   - [ ] Run `ANALYZE` in PostgreSQL
   - [ ] Add indexes for frequently searched fields
   - [ ] Check slow queries in logs

3. **Static Files**
   - [ ] Verify WhiteNoise is enabled
   - [ ] Minify CSS/JavaScript
   - [ ] Compress images

4. **Monitoring**
   - [ ] Set up error alerting (Sentry)
   - [ ] Monitor database performance
   - [ ] Track API response times

---

## Scaling Plan

### Current Setup (Free Plan)
- Web: 0.5GB RAM, 1 shared CPU
- Database: 1GB PostgreSQL
- Good for: Development, testing, small user base (<100)

### When to Upgrade
- [ ] Response times > 3 seconds
- [ ] Database size > 500MB
- [ ] Concurrent users > 50
- [ ] Need for custom domain

### Upgrade Path
1. Change plan to "Standard" in Render dashboard
2. Update `render.yaml` plan field
3. Deploy again
4. No data migration needed (same database)

---

## Maintenance Schedule

### Weekly
- [ ] Check logs for errors
- [ ] Review user reports
- [ ] Verify backups exist
- [ ] Test critical features

### Monthly
- [ ] Update dependencies: `pip list --outdated`
- [ ] Optimize database: `VACUUM ANALYZE`
- [ ] Review performance metrics
- [ ] Clean old data

### Quarterly
- [ ] Security audit
- [ ] Code review
- [ ] Backup restore test
- [ ] Load testing

### Annually
- [ ] Full security assessment
- [ ] Architecture review
- [ ] Plan for scaling
- [ ] Update documentation

---

## Rollback Plan

### If Deployment Fails
1. In Render dashboard → "Deployments" tab
2. Find previous successful deployment
3. Click "Redeploy" button
4. Wait for rollback to complete
5. Investigate issue before next attempt

### If Data Corrupted
1. In Render dashboard → Database → Backups
2. Select backup point before corruption
3. Click "Restore"
4. Verify data integrity
5. Keep corrupted version isolated for investigation

---

## Success Criteria

Application is ready for production when:

✓ All core features working
✓ No critical errors in logs
✓ Response time < 2 seconds
✓ Database connections stable
✓ Backups automated & tested
✓ Monitoring & alerting configured
✓ Security audit passed
✓ Load testing completed
✓ Documentation complete
✓ Team trained on deployment process

---

## Support & Resources

### Render Documentation
- Render Docs: https://render.com/docs
- Django Guide: https://render.com/docs/deploy-django
- PostgreSQL: https://render.com/docs/databases

### Django Documentation
- Django Docs: https://docs.djangoproject.com
- Deployment: https://docs.djangoproject.com/en/stable/howto/deployment/
- Security: https://docs.djangoproject.com/en/stable/topics/security/

### PostgreSQL
- PostgreSQL Docs: https://www.postgresql.org/docs/
- Performance Tips: https://wiki.postgresql.org/wiki/Performance_Optimization

### Community
- Render Support: support@render.com
- Django Forum: https://forum.djangoproject.com
- Stack Overflow: Tag `django` and `render`

---

## Sign-Off

- [ ] Project Lead: _________________ Date: _______
- [ ] DevOps Engineer: _________________ Date: _______
- [ ] QA Lead: _________________ Date: _______

**Deployment Date**: _____________
**Deployed By**: _____________
**Approved By**: _____________

---

## Notes & Issues

Record any issues encountered during deployment for future reference:

```
Date: __________
Issue: __________
Resolution: __________

---
```
