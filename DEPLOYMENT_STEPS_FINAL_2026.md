# UniSinq Deployment - Step-by-Step Guide 2026

## Pre-Deployment Checklist ✅

- [x] Git initialized
- [x] Code on GitHub
- [x] render.yaml configured
- [x] build.sh updated
- [x] requirements.txt ready
- [x] .gitignore configured

---

## Step 1: Prepare Local Code (2 minutes)

### 1.1 Commit Changes

```bash
cd e:\login
git add .
git commit -m "Fix: Update build.sh path and render.yaml for correct backend directory"
```

### 1.2 Push to GitHub

```bash
git push origin fresh-main
```

**Expected output:**
```
Counting objects: 5, done.
...
To https://github.com/Goku0090/uni.git
   abc1234..def5678  fresh-main -> fresh-main
```

---

## Step 2: Setup Environment Variables

You need these environment variables on Render. Collect them now:

### Essential (Required)

```
DEBUG=False
SECRET_KEY=<generate below>
ALLOWED_HOSTS=your-app.onrender.com
DATABASE_URL=<auto from Render PostgreSQL>
```

### Generate SECRET_KEY

Open Python and run:
```python
import secrets
secret = secrets.token_urlsafe(50)
print(secret)
```

Copy the output and save it somewhere.

### Optional (For Features)

```
BREVO_API_KEY=your-api-key-from-brevo
GOOGLE_CLIENT_ID=your-google-client-id
GOOGLE_CLIENT_SECRET=your-google-client-secret
GITHUB_CLIENT_ID=your-github-client-id
GITHUB_CLIENT_SECRET=your-github-client-secret
```

---

## Step 3: Deploy on Render (5 minutes)

### 3.1 Sign Up on Render.com

1. Go to https://render.com
2. Click "Sign up"
3. Login with GitHub (easier)

### 3.2 Create New Service

1. Click "New +" button (top right)
2. Select "Web Service"
3. Choose repository: `Goku0090/uni`
4. Click "Connect"

### 3.3 Configure Deployment

**Fill in these fields:**

| Field | Value |
|-------|-------|
| Name | unisync |
| Environment | Python 3 |
| Build Command | `bash build.sh` |
| Start Command | `cd backend && gunicorn auth_project.wsgi:application --workers 3 --worker-class sync --bind 0.0.0.0:$PORT --timeout 120` |
| Region | Oregon (or closest) |
| Instance Type | Free |

### 3.4 Add Environment Variables

Click "Advanced" → "Add Environment Variable"

**Add each:**

1. `DEBUG` = `False`
2. `SECRET_KEY` = `<your-generated-key>`
3. `ALLOWED_HOSTS` = `<will-get-url-from-render>`
4. `PYTHONUNBUFFERED` = `1`
5. `PYTHONDONTWRITEBYTECODE` = `1`
6. `EMAIL_BACKEND` = `django.core.mail.backends.console.EmailBackend`

### 3.5 Create PostgreSQL Database

1. Click "New +" again
2. Select "PostgreSQL"
3. Name: `unisync-db`
4. Plan: Free
5. Click "Create Database"

### 3.6 Link Database to Web Service

1. Go back to Web Service
2. Click "Environment"
3. Add: `DATABASE_URL` = (will auto-populate from PostgreSQL)

### 3.7 Deploy!

Click "Create Web Service"

**Wait 5-10 minutes...**

---

## Step 4: Verify Deployment

### Check Build Progress

1. Dashboard → Your App → "Logs"
2. Look for:
   ```
   ========== Build Complete ==========
   App is ready to start!
   ```

### Check Running Status

1. Dashboard → Your App
2. Status should show: `Live` ✅

### Get Your URL

1. Dashboard → Your App → URL
2. Format: `https://unisync.onrender.com`

Copy this URL!

---

## Step 5: Update Settings

### 5.1 Add ALLOWED_HOSTS

1. Dashboard → Web Service → Environment
2. Update `ALLOWED_HOSTS` to your URL:
   ```
   unisync.onrender.com,localhost,127.0.0.1
   ```

### 5.2 Test Website

Open your URL in browser:
```
https://unisync.onrender.com
```

**You should see:** Login page ✅

---

## Step 6: Create Admin User (SSH)

### Option A: Via Render Console (Easy)

1. Dashboard → Web Service → "Shell"
2. Run:
   ```bash
   cd backend
   python manage.py createsuperuser
   ```

3. Enter:
   - Username: `admin`
   - Email: `your-email@example.com`
   - Password: `strong-password`

### Option B: Via Render CLI (Advanced)

```bash
render login
render ps
render ssh unisync
# Then same commands as above
```

---

## Step 7: Test Core Features

### 7.1 Test Login

1. Visit: `https://unisync.onrender.com`
2. Register with email
3. Should see: Verification email (in console logs)

### 7.2 Test Admin Panel

1. Visit: `https://unisync.onrender.com/admin/`
2. Login with admin credentials
3. Should see: Django admin interface

### 7.3 Check Logs for Errors

1. Dashboard → Logs
2. Look for any `ERROR` or `500` messages
3. If found, check Settings tab

---

## Step 8: Configure OAuth (Optional)

If you want Google/GitHub login:

### Google OAuth

1. Go to https://console.cloud.google.com
2. Create project: "UniSinq"
3. OAuth 2.0 Client ID
4. Authorized redirect URIs:
   ```
   https://unisync.onrender.com/accounts/google/login/callback/
   ```
5. Copy Client ID & Secret
6. Add to Render environment:
   - `GOOGLE_CLIENT_ID=xxx`
   - `GOOGLE_CLIENT_SECRET=yyy`

### GitHub OAuth

1. Go to https://github.com/settings/developers
2. New OAuth App
3. Authorization callback URL:
   ```
   https://unisync.onrender.com/accounts/github/login/callback/
   ```
4. Copy Client ID & Secret
5. Add to Render environment:
   - `GITHUB_CLIENT_ID=xxx`
   - `GITHUB_CLIENT_SECRET=yyy`

---

## Step 9: Configure Email (Optional)

### Using Brevo (Recommended)

1. Sign up at https://www.brevo.com
2. Get API key from Settings
3. Add to Render:
   - `BREVO_API_KEY=your-api-key`
   - `EMAIL_BACKEND=accounts.brevo_mail_backend.BrevoMailBackend`
   - `DEFAULT_FROM_EMAIL=noreply@unisinq.app`

---

## Troubleshooting

### Build Fails

**Check logs:** Dashboard → Logs

**Common issues:**
```
ModuleNotFoundError: No module named 'django'
→ requirements.txt missing dependencies

ImportError: cannot import name 'X'
→ Missing dependency, add to requirements.txt

No such file: requirements.txt
→ build.sh pointing to wrong directory
```

### App Won't Start

```
[ERROR] Application failed to start
→ Check ALLOWED_HOSTS includes your domain

[ERROR] Database connection refused
→ PostgreSQL service not created/connected

[ERROR] SECRET_KEY not found
→ Add SECRET_KEY environment variable
```

### 500 Error on Website

1. Check Logs tab in Dashboard
2. Look for specific error
3. Common fixes:
   - Add URL to ALLOWED_HOSTS
   - Migrate database: `python manage.py migrate`
   - Collect static: `python manage.py collectstatic`

### WebSocket Not Connecting

```
WebSocket connection failed
→ This is normal on free Render tier
→ Requires Redis or upgrade
→ For now, real-time features may not work
```

---

## Performance Optimization

### Render Free Tier Limitations

- Single dyno (may sleep)
- 0.5 GB RAM
- Shared CPU
- No real-time features (WebSocket)
- No persistent storage

### Upgrade When Needed

1. Dashboard → Plan
2. Upgrade from Free → Starter
3. Choose:
   - Starter Web Service: $7/month
   - Starter PostgreSQL: $15/month
   - Total: ~$22/month

---

## Monitoring & Maintenance

### Weekly

- [ ] Check error logs
- [ ] Verify app is responding
- [ ] Test login feature

### Monthly

- [ ] Review performance metrics
- [ ] Update dependencies
- [ ] Check database storage

### Annually

- [ ] Review security settings
- [ ] Update Django/libraries
- [ ] Test restore from backup

---

## Custom Domain (Optional)

### Add Your Domain

1. Dashboard → Web Service → Settings
2. Click "Add Custom Domain"
3. Enter: `yourdomain.com`
4. Add DNS records (shown in Render):
   ```
   Type: CNAME
   Name: @
   Value: cname.onrender.com
   ```
5. Wait 5-10 minutes for DNS propagation

---

## Next Steps

### Immediate (After Launch)

1. ✅ Test all authentication methods
2. ✅ Create sample projects
3. ✅ Test messaging
4. ✅ Test comments
5. ✅ Verify notifications in console

### Short Term (This Week)

1. Set up custom domain
2. Configure email (Brevo)
3. Setup OAuth (Google/GitHub)
4. Populate sample data
5. Get user feedback

### Medium Term (This Month)

1. Upgrade to paid tier if popular
2. Enable Redis for WebSocket
3. Setup monitoring/alerts
4. Optimize database queries
5. Add CDN for static files

---

## Support

### Render Documentation
- Docs: https://docs.render.com
- Status: https://render-status.com
- Support: https://render.com/support

### Django Documentation
- Deployment: https://docs.djangoproject.com/en/4.2/howto/deployment/

### Your App
- App URL: `https://unisync.onrender.com`
- Admin: `https://unisync.onrender.com/admin/`
- Logs: Render Dashboard

---

## Quick Reference

### Deployment Summary

```
Code → GitHub → Render → PostgreSQL
         ↓
    Automatic build
         ↓
    Start with gunicorn
         ↓
    Live on onrender.com
```

### File Structure on Render

```
/app
├── backend/
│   ├── manage.py
│   ├── auth_project/
│   ├── accounts/
│   ├── requirements.txt
│   └── static/
├── frontend/
├── build.sh
└── render.yaml
```

### Important URLs

| Purpose | URL |
|---------|-----|
| App | `https://unisync.onrender.com` |
| Admin | `https://unisync.onrender.com/admin/` |
| API | `https://unisync.onrender.com/api/` |
| Dashboard | https://dashboard.render.com |

---

## Done! 🎉

Your app is now live on the internet!

**Share your URL:** `https://unisync.onrender.com`

**Next:** Add custom domain, configure email, scale to paid tier

---

**Last Updated:** February 16, 2026
**Status:** Ready to Deploy
