# Environment Variables Setup Guide

## ⚠️ SECURITY FIRST

**NEVER commit `.env` files to Git!**
- Your `.gitignore` already excludes them (good!)
- These files contain secrets that should never be public
- Always use `.env.example` as template

---

## Files You Need

### Local Development (Create These)

1. **`backend/.env`** - Backend environment variables
   - Copy from: `backend/.env.example`
   - Never commit to Git
   - Contains: Database, email, OAuth secrets

2. **`frontend/.env.local`** - Frontend environment variables (already exists)
   - Contains: API endpoint URL
   - Already excluded from Git

3. **`.env`** - Root level (optional, for Docker)
   - Copy from: `.env.example`
   - For local Docker development

### Templates (Reference Only)

- **`.env.example`** - Root template (safe to commit)
- **`backend/.env.example`** - Backend template (safe to commit)
- **`frontend/.env.local`** - Frontend local (exists, excluded)

---

## Step 1: Create Backend `.env`

### For Local Development

1. **Copy template:**
   ```bash
   cp backend/.env.example backend/.env
   ```

2. **Edit `backend/.env`:**
   ```
   DEBUG=True              # True for development
   SECRET_KEY=generate-with-secrets.token_urlsafe(50)
   DATABASE_URL=sqlite:///db.sqlite3    # For local SQLite
   ALLOWED_HOSTS=localhost,127.0.0.1
   EMAIL_BACKEND=django.core.mail.backends.console.EmailBackend
   ```

3. **Generate SECRET_KEY:**
   ```python
   python -c "import secrets; print(secrets.token_urlsafe(50))"
   ```
   Copy output and paste in `.env`

### For Production (Render)

- **DON'T create `.env` file**
- Instead, set variables in **Render Dashboard** → Environment
- See: `DEPLOYMENT_STEPS_FINAL_2026.md`

---

## Step 2: Create Frontend `.env.local`

Your `frontend/.env.local` already exists. Check its contents:

**Should contain:**
```
VITE_API_URL=http://localhost:8000
```

Or for production:
```
VITE_API_URL=https://your-app.onrender.com
```

---

## Step 3: Gather Your Secrets

Before filling in values, collect them:

### Required (Must Have)

| Secret | Where to Get | Why |
|--------|-------------|-----|
| SECRET_KEY | Generate: `secrets.token_urlsafe(50)` | Django security |
| DATABASE_URL | PostgreSQL connection string | Database access |

### Optional (For Features)

| Secret | Where to Get | Why |
|--------|-------------|-----|
| BREVO_API_KEY | https://www.brevo.com (Settings) | Email delivery |
| GOOGLE_CLIENT_ID | https://console.cloud.google.com | Google login |
| GOOGLE_CLIENT_SECRET | https://console.cloud.google.com | Google login |
| GITHUB_CLIENT_ID | https://github.com/settings/developers | GitHub login |
| GITHUB_CLIENT_SECRET | https://github.com/settings/developers | GitHub login |

---

## Step 4: Database Setup

### PostgreSQL (Local)

```bash
# Install PostgreSQL
# Create database
createdb unisinq_db

# Create user
createuser unisinq_user

# Set password
# psql -U postgres
# ALTER USER unisinq_user WITH PASSWORD 'password';
# GRANT ALL PRIVILEGES ON DATABASE unisinq_db TO unisinq_user;

# Update .env
DATABASE_URL=postgresql://unisinq_user:password@localhost:5432/unisinq_db
```

### SQLite (Local - Easiest)

```bash
# Just use SQLite
DATABASE_URL=sqlite:///db.sqlite3
```

---

## Step 5: Run Migrations

Once `.env` is set up:

```bash
cd backend
python manage.py migrate
python manage.py createsuperuser
```

---

## Step 6: Email Setup (Optional)

### Console Backend (Development - Default)
```
EMAIL_BACKEND=django.core.mail.backends.console.EmailBackend
```
✅ Prints emails to console instead of sending

### Brevo (Production)

1. Sign up: https://www.brevo.com
2. Get API key from Settings
3. Add to `.env`:
   ```
   BREVO_API_KEY=your-api-key
   EMAIL_BACKEND=accounts.brevo_mail_backend.BrevoMailBackend
   DEFAULT_FROM_EMAIL=noreply@unisinq.app
   ```

### Gmail (Fallback)

1. Setup Gmail app password (2FA required)
2. Add to `.env`:
   ```
   EMAIL_HOST_USER=your-email@gmail.com
   EMAIL_HOST_PASSWORD=your-app-password
   EMAIL_BACKEND=django.core.mail.backends.smtp.EmailBackend
   ```

---

## Step 7: OAuth Setup (Optional)

### Google OAuth

1. Go to: https://console.cloud.google.com
2. Create new project
3. Create OAuth 2.0 Client ID
4. Add authorized redirect URIs:
   ```
   http://localhost:8000/accounts/google/login/callback/
   https://your-app.onrender.com/accounts/google/login/callback/
   ```
5. Copy Client ID & Secret
6. Add to `.env`:
   ```
   GOOGLE_CLIENT_ID=xxx
   GOOGLE_CLIENT_SECRET=yyy
   ```

### GitHub OAuth

1. Go to: https://github.com/settings/developers
2. Create new OAuth App
3. Set Authorization callback URL:
   ```
   http://localhost:8000/accounts/github/login/callback/
   https://your-app.onrender.com/accounts/github/login/callback/
   ```
4. Copy Client ID & Secret
5. Add to `.env`:
   ```
   GITHUB_CLIENT_ID=xxx
   GITHUB_CLIENT_SECRET=yyy
   ```

---

## Minimal `.env` for Quick Start

If you just want to test locally, minimum required:

```bash
# backend/.env

DEBUG=True
SECRET_KEY=dev-secret-key-not-for-production-12345678901234567890
DATABASE_URL=sqlite:///db.sqlite3
ALLOWED_HOSTS=localhost,127.0.0.1
PYTHONUNBUFFERED=1
PYTHONDONTWRITEBYTECODE=1
EMAIL_BACKEND=django.core.mail.backends.console.EmailBackend
CORS_ALLOWED_ORIGINS=http://localhost:3000,http://localhost:8000
```

---

## For Production Deployment

**Do NOT create `.env` files**

Instead:

1. Go to Render Dashboard
2. Select your Web Service
3. Click "Environment"
4. Add each variable individually:
   - DEBUG = False
   - SECRET_KEY = (generate)
   - DATABASE_URL = (auto from PostgreSQL)
   - etc.

See: `DEPLOYMENT_STEPS_FINAL_2026.md` for details

---

## Testing Your Setup

Once `.env` is created and filled:

```bash
cd backend

# Check Django loads
python manage.py check

# Run migrations
python manage.py migrate

# Create superuser
python manage.py createsuperuser

# Start server
python manage.py runserver

# Visit: http://localhost:8000
```

---

## Common Issues

### "ModuleNotFoundError: No module named 'django'"
→ Install requirements: `pip install -r requirements.txt`

### "DJANGO_SETTINGS_MODULE is undefined"
→ Django looks for `.env` automatically
→ Make sure it's in `backend/.env`

### "Database connection refused"
→ Check DATABASE_URL is correct
→ Make sure PostgreSQL/SQLite exists
→ Check credentials

### "Secret key setting is undefined"
→ Add `SECRET_KEY` to `.env`
→ Generate with: `secrets.token_urlsafe(50)`

### "ALLOWED_HOSTS error"
→ Add your domain to `ALLOWED_HOSTS` in `.env`

---

## Security Checklist

- [ ] `.env` NOT committed to Git
- [ ] `backend/.env` is in `.gitignore`
- [ ] `.env.example` has no real secrets
- [ ] SECRET_KEY is strong (50+ chars)
- [ ] Passwords are strong
- [ ] API keys are from official sources
- [ ] Database password is secure
- [ ] No secrets in code comments

---

## Next Steps

1. **Create `backend/.env`** from template
2. **Fill in required values** (SECRET_KEY, DATABASE_URL)
3. **Add optional values** (email, OAuth)
4. **Run migrations** and test
5. **For deployment**: Use Render environment variables (not `.env` file)

---

## Files Reference

| File | Should Exist | Safe to Commit | Contains Secrets |
|------|-------------|----------------|------------------|
| `.env` | ❌ Local only | ❌ NO | ✅ YES |
| `.env.example` | ✅ Yes | ✅ YES | ❌ NO |
| `backend/.env` | ❌ Local only | ❌ NO | ✅ YES |
| `backend/.env.example` | ✅ Yes | ✅ YES | ❌ NO |
| `frontend/.env.local` | ✅ Yes (exists) | ❌ NO | ⚠️ Semi |

---

**Remember**: Templates (`.example`) are for reference. Real `.env` files are ignored by Git and contain your actual secrets.

**Status**: Ready to setup local environment 🚀
