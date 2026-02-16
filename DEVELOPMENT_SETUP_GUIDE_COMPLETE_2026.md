# Complete Development Setup Guide - 2026

## Quick Start (TL;DR)

```bash
# Terminal 1 - Backend
cd backend
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
pip install -r requirements.txt
python manage.py migrate
python manage.py runserver

# Terminal 2 - Frontend
cd frontend
npm install
npm run dev

# Browser
# Visit http://localhost:3000 for React app
# Backend API available at http://localhost:8000/api
```

---

## Step-by-Step Setup

### Part 1: Backend Setup

#### 1.1 Create Virtual Environment

**Windows:**
```powershell
cd backend
python -m venv venv
venv\Scripts\activate
```

**macOS/Linux:**
```bash
cd backend
python3 -m venv venv
source venv/bin/activate
```

#### 1.2 Install Dependencies

```bash
pip install -r requirements.txt
# This installs:
# - Django 4.2.8
# - djangorestframework 3.14.0
# - django-allauth 0.61.1
# - django-channels 4.0.0
# - psycopg2-binary (PostgreSQL driver)
# - redis (cache client)
# - ... and 25+ more packages
```

#### 1.3 Create Environment File

Create `backend/.env`:
```
DEBUG=True
SECRET_KEY=your-dev-secret-key-here
ALLOWED_HOSTS=localhost,127.0.0.1

# Database (choose one)
# Option A: SQLite (easiest for development)
DB_ENGINE=sqlite3
DB_NAME=db.sqlite3

# Option B: PostgreSQL
# DATABASE_URL=postgresql://user:password@localhost:5432/unisinq_db

# Cache
REDIS_URL=redis://localhost:6379/1

# Email (for OTP)
EMAIL_BACKEND=accounts.brevo_mail_backend.BrevoMailBackend
BREVO_API_KEY=your-brevo-api-key  # optional for development

# Security
SECURE_SSL_REDIRECT=False
SESSION_COOKIE_SECURE=False
CSRF_COOKIE_SECURE=False
```

#### 1.4 Initialize Database

**Option A: SQLite (recommended for quick start)**
```bash
python manage.py migrate
# Creates db.sqlite3 with all tables
```

**Option B: PostgreSQL (production-like)**

First, make sure PostgreSQL is running:
```bash
# Windows (using WSL or PgAdmin)
# macOS (using Homebrew)
brew services start postgresql
# Linux
sudo service postgresql start

# Create database
createdb unisinq_db
createuser unisinq_user -P  # Enter password when prompted
```

Then in `.env`:
```
DATABASE_URL=postgresql://unisinq_user:your_password@localhost:5432/unisinq_db
```

Then migrate:
```bash
python manage.py migrate
```

#### 1.5 Create Superuser (Admin Account)

```bash
python manage.py createsuperuser
# Follow prompts:
# Username: admin
# Email: admin@example.com
# Password: (enter password)
```

#### 1.6 Start Backend Server

```bash
python manage.py runserver
# Output:
# Django version 4.2.8, using settings 'auth_project.settings'
# Starting development server at http://127.0.0.1:8000/
# Quit the server with CONTROL-C.
```

**Test backend is working:**
```bash
# In another terminal
curl http://localhost:8000/admin/
# Should get HTML response (Django admin page)
```

---

### Part 2: Frontend Setup

#### 2.1 Install Node Dependencies

```bash
cd frontend
npm install
# This installs:
# - react 18.2.0
# - react-dom 18.2.0
# - react-router-dom 6.20.0
# - axios 1.6.0
# - vite 5.0.0
# - @vitejs/plugin-react 4.2.0
```

#### 2.2 Create Frontend Environment File

Create `frontend/.env.local`:
```
VITE_API_URL=http://localhost:8000/api
VITE_WS_URL=ws://localhost:8000
```

#### 2.3 Start Frontend Dev Server

```bash
npm run dev
# Output:
# VITE v5.0.0 ready in XXX ms
# ➜ Local: http://localhost:3000/
# ➜ press h to show help
```

**Test frontend is working:**
1. Visit `http://localhost:3000` in browser
2. Should see React app
3. Check browser console for errors (F12 → Console tab)

---

### Part 3: Optional Services

#### 3.1 PostgreSQL + Redis with Docker

Create `docker-compose.yml` in root (if not exists):

```yaml
version: '3.8'

services:
  postgres:
    image: postgres:15-alpine
    environment:
      POSTGRES_DB: unisinq_db
      POSTGRES_USER: unisinq_user
      POSTGRES_PASSWORD: your_password
    ports:
      - "5432:5432"
    volumes:
      - postgres_data:/var/lib/postgresql/data

  redis:
    image: redis:7-alpine
    ports:
      - "6379:6379"
    volumes:
      - redis_data:/data

volumes:
  postgres_data:
  redis_data:
```

Start services:
```bash
docker-compose up -d
# -d runs in background

# Check status
docker-compose ps

# Stop services
docker-compose down
```

---

## Verification Checklist

### Backend Verification

- [ ] Virtual environment activated
- [ ] Dependencies installed: `pip list | grep Django`
- [ ] Database migrated: `python manage.py showmigrations | grep accounts`
- [ ] Superuser created: `python manage.py shell` → `User.objects.all()`
- [ ] Server running: `http://localhost:8000/admin` loads
- [ ] API accessible: `http://localhost:8000/api/projects/`

### Frontend Verification

- [ ] Node modules installed: `node_modules/` folder exists
- [ ] Dev server running: Terminal shows "ready"
- [ ] App loads: `http://localhost:3000` shows React app
- [ ] No console errors: F12 → Console tab (no red errors)
- [ ] API proxy works: Network tab shows requests to `/api` are to `8000`

### Integration Verification

```bash
# Test API call
curl http://localhost:8000/api/projects/

# Test WebSocket readiness
curl http://localhost:8000/ws/test/  # Should give WebSocket error (expected)

# Test database connection
python manage.py shell
>>> from django.contrib.auth.models import User
>>> User.objects.count()  # Should return number of users
```

---

## Common Issues & Solutions

### Issue: "ModuleNotFoundError: No module named 'django'"

**Cause:** Virtual environment not activated

**Solution:**
```bash
# Windows
venv\Scripts\activate

# macOS/Linux
source venv/bin/activate

# Should show (venv) at start of terminal line
```

### Issue: "Port 8000 already in use"

**Cause:** Another process using port 8000

**Solution:**
```bash
# Find and kill process
lsof -i :8000  # macOS/Linux
netstat -ano | findstr :8000  # Windows

# Kill specific process (Windows)
taskkill /PID <PID> /F

# Run on different port
python manage.py runserver 8001
```

### Issue: "Port 3000 already in use"

**Same as above, but for port 3000**

```bash
# Run on different port
npm run dev -- --port 3001
```

### Issue: Database "table doesn't exist"

**Cause:** Migrations not run

**Solution:**
```bash
python manage.py migrate
python manage.py migrate accounts  # Specific app
```

### Issue: "No such table: auth_user"

**Same as above**

### Issue: "CORS error" in browser console

**Cause:** Backend not allowing frontend origin

**Solution:** In `backend/auth_project/settings.py`, add:
```python
CORS_ALLOWED_ORIGINS = [
    "http://localhost:3000",
    "http://127.0.0.1:3000",
]
```

### Issue: WebSocket connection fails

**Cause:** 
- Redis not running
- Daphne not installed
- Settings not configured

**Solution:**
```bash
# Install channels dependencies
pip install daphne
pip install channels-redis

# Run with Daphne (if needed for async)
daphne -b 0.0.0.0 -p 8000 auth_project.asgi:application

# Or use development server (simpler)
python manage.py runserver
```

### Issue: "SyntaxError: Unexpected token '<'"

**Cause:** Frontend trying to load Python error page as JSON

**Solution:**
1. Check backend is running
2. Check vite.config.js proxy settings
3. Check API endpoint exists
4. Check for typos in URL

### Issue: npm install fails

**Cause:** Node version mismatch or npm cache issue

**Solution:**
```bash
# Clear npm cache
npm cache clean --force

# Delete node_modules and reinstall
rm -rf node_modules package-lock.json
npm install

# Or use npm ci (cleaner install)
npm ci
```

---

## Development Workflow

### Daily Development

```bash
# 1. Start backend (Terminal 1)
cd backend
source venv/bin/activate
python manage.py runserver

# 2. Start frontend (Terminal 2)
cd frontend
npm run dev

# 3. Start optional services (Terminal 3)
docker-compose up -d

# 4. Open browser
# Visit http://localhost:3000
```

### Making Changes

#### Backend Changes
1. Edit `backend/accounts/views.py`, `models.py`, etc.
2. Django auto-reloads on file change
3. Test in browser or with curl

#### Frontend Changes
1. Edit `frontend/src/App.jsx`, components, etc.
2. Vite hot-reloads automatically
3. Changes appear instantly in browser

#### Database Changes
1. Edit `backend/accounts/models.py`
2. Run: `python manage.py makemigrations`
3. Run: `python manage.py migrate`
4. Test API

### Testing

#### Backend Tests
```bash
cd backend
python manage.py test
# Runs all tests in accounts/tests.py
```

#### Frontend Tests
```bash
cd frontend
npm test
# If test script configured in package.json
```

### Debugging

#### Backend Debugging
```bash
# Python shell
python manage.py shell

# Import and test
>>> from accounts.models import User, Project
>>> User.objects.all()
>>> Project.objects.filter(owner__username='admin')

# Database query logging
# In settings.py, add:
LOGGING = {
    'version': 1,
    'handlers': {'console': {'class': 'logging.StreamHandler'}},
    'loggers': {
        'django.db.backends': {
            'handlers': ['console'],
            'level': 'DEBUG',
        },
    },
}
```

#### Frontend Debugging
```bash
# Browser DevTools (F12)
# - Console tab: errors, logs
# - Network tab: API requests
# - Application tab: localStorage, cookies
# - Sources tab: step through code

# React DevTools extension (recommended)
# https://react-devtools-tutorial.vercel.app/
```

---

## Production-like Testing

To test closer to production before deploying:

### 1. Build Frontend
```bash
cd frontend
npm run build
# Creates frontend/dist/ folder with optimized build
```

### 2. Copy to Backend Static
```bash
# Windows (PowerShell)
Copy-Item -Recurse frontend\dist\* backend\static\

# macOS/Linux
cp -r frontend/dist/* backend/static/
```

### 3. Collect Static Files
```bash
cd backend
python manage.py collectstatic --noinput
# Gathers all static files into STATIC_ROOT
```

### 4. Set Debug=False
```
# In .env
DEBUG=False
```

### 5. Run Server
```bash
python manage.py runserver
# Now serves built React app from /static/
```

### 6. Test
```bash
# Visit http://localhost:8000
# Should see production-like setup
# (single server, no dev server)
```

---

## Project Structure Recap

```
project/
├── backend/
│   ├── venv/                   # Virtual environment
│   ├── auth_project/           # Django config
│   ├── accounts/               # Main app
│   ├── static/                 # Static files (CSS, JS, images)
│   ├── db.sqlite3              # SQLite database
│   ├── manage.py
│   ├── requirements.txt        # Python dependencies
│   └── .env                    # Environment variables
│
├── frontend/
│   ├── node_modules/           # npm packages
│   ├── src/                    # React source
│   ├── public/                 # Public assets
│   ├── dist/                   # Built frontend (after npm run build)
│   ├── package.json            # npm config
│   ├── vite.config.js          # Vite config
│   ├── index.html              # HTML template
│   └── .env.local              # Frontend env vars
│
├── docker-compose.yml          # Database & cache services
└── build.sh                    # Production build script
```

---

## Environment Variable Guide

### Backend `.env`

```
# Core
DEBUG=True                                    # Dev mode
SECRET_KEY=dev-key-change-in-production       # Secret key
ALLOWED_HOSTS=localhost,127.0.0.1             # Allowed domains

# Database
# SQLite (default)
DB_ENGINE=sqlite3
DB_NAME=db.sqlite3

# PostgreSQL (production)
DATABASE_URL=postgresql://user:pass@localhost:5432/db

# Cache
REDIS_URL=redis://localhost:6379/1

# Email
EMAIL_BACKEND=accounts.brevo_mail_backend.BrevoMailBackend
BREVO_API_KEY=your-api-key

# OAuth (optional)
GOOGLE_CLIENT_ID=your-client-id
GOOGLE_CLIENT_SECRET=your-secret
GITHUB_CLIENT_ID=your-client-id
GITHUB_CLIENT_SECRET=your-secret

# Security
SECURE_SSL_REDIRECT=False                    # Set to True in production
SESSION_COOKIE_SECURE=False                  # Set to True in production
CSRF_COOKIE_SECURE=False                     # Set to True in production
```

### Frontend `.env.local`

```
# API Configuration
VITE_API_URL=http://localhost:8000/api
VITE_WS_URL=ws://localhost:8000
```

---

## Useful Commands Reference

### Django Commands

```bash
python manage.py runserver              # Start dev server
python manage.py migrate                # Apply database changes
python manage.py makemigrations         # Create migration files
python manage.py createsuperuser        # Create admin user
python manage.py shell                  # Interactive Python shell
python manage.py test                   # Run tests
python manage.py collectstatic          # Gather static files
python manage.py flush                  # Clear database
python manage.py dumpdata > backup.json # Backup database
python manage.py loaddata backup.json   # Restore database
```

### npm Commands

```bash
npm install                 # Install dependencies
npm run dev                 # Start dev server
npm run build               # Build for production
npm run preview             # Preview production build
npm test                    # Run tests
npm audit                   # Check for vulnerabilities
npm update                  # Update dependencies
```

### Docker Commands

```bash
docker-compose up -d        # Start services (background)
docker-compose down         # Stop services
docker-compose ps           # List running services
docker-compose logs postgres # View logs
redis-cli ping              # Test Redis connection
```

---

## Next Steps

Once setup is complete:

1. **Explore the Codebase**
   - Read `ANALYSIS_SUMMARY_EXECUTIVE_2026_FINAL.md`
   - Review `QUICK_CODEBASE_REFERENCE_2026.md`

2. **Understand the Architecture**
   - Read `FRONTEND_BACKEND_ARCHITECTURE_EXPLAINED_2026.md`
   - Review `ARCHITECTURE_VISUAL_GUIDE_2026.md`

3. **Start Development**
   - Edit React components in `frontend/src/`
   - Edit Django views in `backend/accounts/views.py`
   - Models in `backend/accounts/models.py`

4. **Test Features**
   - Login with email/OTP
   - Create a project
   - Chat with other users
   - Comment on projects

5. **Deploy to Production**
   - See deployment section in main analysis docs
   - Use Render.com or Railway.app

---

## Support

If stuck:
1. Check this guide's troubleshooting section
2. Review main codebase analysis docs
3. Check backend/frontend logs
4. Use browser DevTools (F12)
5. Search GitHub issues

---

**You're all set!** 🚀

Happy developing!

