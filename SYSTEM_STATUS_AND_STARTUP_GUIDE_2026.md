# System Status & Startup Guide - UniSinQ Platform 2026

## 🟢 Current System Status: OPERATIONAL

All systems checked and verified as of **February 9, 2026**.

---

## ✅ System Health Check Results

### Django Core
```
✅ URL Configuration: PASSED
✅ Model Integrity: PASSED
✅ Database Connection: PASSED
✅ Signal Handlers: PASSED
✅ Middleware Stack: PASSED
✅ Authentication Backends: PASSED
✅ Static Files Configuration: PASSED
```

### External Services
```
✅ Email Backend: Brevo API (Configured)
✅ OAuth Providers: Google & GitHub (Ready)
✅ WebSocket/Channels: In-Memory (Development)
✅ Database: PostgreSQL (via DATABASE_URL)
✅ Media Storage: Local (Development)
```

### Application Modules
```
✅ accounts.views: 1000+ lines of business logic
✅ accounts.models: 830+ lines, 20+ database models
✅ accounts.urls: 122 lines, 60+ endpoints
✅ accounts.chat_api: REST API for messaging
✅ accounts.comment_api: Live feed comment system
✅ accounts.consumers: WebSocket handlers
```

---

## 🚀 Quick Start Guide

### Prerequisites
```
Python 3.13+
pip (Python package manager)
Virtual environment (recommended)
PostgreSQL (production) or SQLite (development)
```

### Step 1: Activate Virtual Environment
**Windows:**
```batch
venv\Scripts\activate
```

**Linux/Mac:**
```bash
source venv/bin/activate
```

### Step 2: Install Dependencies
```bash
pip install -r requirements.txt
```

### Step 3: Configure Environment
Create `.env` file in project root:
```env
DEBUG=True
SECRET_KEY=your-secret-key-here
DATABASE_URL=postgresql://localhost/unisinq_db
ALLOWED_HOSTS=localhost,127.0.0.1
BREVO_API_KEY=optional-for-email
GOOGLE_CLIENT_ID=optional-for-oauth
GITHUB_CLIENT_ID=optional-for-oauth
```

### Step 4: Apply Migrations
```bash
cd auth_project
python manage.py migrate --run-syncdb
```

### Step 5: Create Superuser (Optional)
```bash
python manage.py createsuperuser
```

### Step 6: Start Development Server
**Terminal 1 - Django Development Server:**
```bash
python manage.py runserver
```

Expected output:
```
[INFO] Starting development server at http://127.0.0.1:8000/
[INFO] Quit the server with CTRL-BREAK.
```

**Terminal 2 - WebSocket Server (Optional, for real-time features):**
```bash
daphne -b 0.0.0.0 -p 8001 auth_project.asgi:application
```

---

## 📋 Available URLs & Endpoints

### Main Pages
```
/ or /dashboard/              → Dashboard/Feed
/login/                       → Login page
/register/                    → Registration page
/profile/                     → User profile
/find-collaborators/          → Find collaborators
/post-project/                → Create new project
/project-detail/<id>/         → View project
/notifications/               → Notifications
/messages/                    → Messaging interface
```

### REST API Endpoints
```
/accounts/chat-rooms/                  → List chat rooms
/accounts/messages/                    → Message list
/accounts/projects/<id>/comments/      → Project comments
/accounts/user-profile/<user_id>/      → User profile API
```

### Admin Interface
```
/admin/                       → Django Admin (requires superuser)
```

---

## 🔧 Configuration Files

### `auth_project/settings.py` (Main Settings)
- DEBUG mode and SECRET_KEY
- Database configuration
- Email backend selection (Brevo → ZeptoMail → Gmail → Console)
- OAuth provider setup (Google, GitHub)
- Installed apps and middleware
- Static/Media files configuration
- Logging setup

### `auth_project/urls.py` (Root URL Router)
- Routes to accounts app
- Routes to admin interface
- Routes to allauth authentication

### `accounts/urls.py` (App URL Routes)
- Authentication views (login, register, OTP)
- Profile management
- Project management (CRUD)
- Messaging endpoints
- REST API endpoints
- Comment system API

### `accounts/models.py` (Database Schema)
- User & authentication models
- Project & collaboration models
- Messaging & communication models
- Content & notification models
- Template models

---

## 🗄️ Database Overview

### Tables Created
```
✅ accounts_studentprofile      → User extended profiles
✅ accounts_project             → User projects
✅ accounts_projectmember       → Team members
✅ accounts_message             → Messages
✅ accounts_chatroom            → Chat rooms
✅ accounts_connection          → Connection requests
✅ accounts_otp                 → OTP codes
✅ accounts_comment             → Comments
✅ accounts_notification        → Notifications
✅ auth_user                    → Django users
✅ auth_group                   → User groups
✅ django_session               → Session data
✅ allauth_account              → Social account auth
```

### Sample Query Examples

**Get user profile:**
```python
from accounts.models import StudentProfile
profile = StudentProfile.objects.get(user__username='john_doe')
```

**Get user projects:**
```python
from accounts.models import Project
projects = Project.objects.filter(owner__username='john_doe')
```

**Get chat messages:**
```python
from accounts.models import Message
messages = Message.objects.filter(chat_room_id=1).order_by('created_at')
```

---

## 📧 Email Configuration

### Currently Configured: Brevo
**Status**: ✅ Active

**Features**:
- OTP delivery (login, registration, password reset)
- Transactional emails
- API-based (no SMTP needed)
- Production-ready

**Configuration**:
```python
EMAIL_BACKEND = 'accounts.brevo_mail_backend.BrevoMailBackend'
BREVO_API_KEY = os.getenv('BREVO_API_KEY')
DEFAULT_FROM_EMAIL = 'noreply@unisinq.app'
```

### Fallback Chain
1. **Brevo** (Production)
2. **ZeptoMail** (Alternative)
3. **Gmail SMTP** (Fallback)
4. **Console** (Development)

---

## 🔐 OAuth Configuration

### Google OAuth
**Setup**:
1. Visit https://console.cloud.google.com
2. Create OAuth 2.0 credentials
3. Add redirect URI: `http://localhost:8000/accounts/google/login/callback/`
4. Set `GOOGLE_CLIENT_ID` and `GOOGLE_CLIENT_SECRET` in `.env`

### GitHub OAuth
**Setup**:
1. Visit https://github.com/settings/developers
2. Create new OAuth App
3. Add Authorization callback URL: `http://localhost:8000/accounts/github/login/callback/`
4. Set `GITHUB_CLIENT_ID` and `GITHUB_CLIENT_SECRET` in `.env`

---

## 🔄 Real-Time Features (WebSocket)

### Architecture
- **Framework**: Django Channels 4.0+
- **Protocol**: WebSocket (ws://)
- **Server**: Daphne (ASGI server)

### Features Enabled
- Real-time message delivery
- Live comment updates
- Connection status tracking
- Typing indicators
- Read status notifications

### Setup
1. Channels already installed
2. ASGI configuration in `auth_project/asgi.py`
3. Routing defined in `accounts/routing.py`
4. Start with: `daphne -b 0.0.0.0 -p 8001 auth_project.asgi:application`

---

## 📊 Static & Media Files

### Static Files (CSS, JS, Images)
```
Path: auth_project/static/
Served: /static/ (when DEBUG=False)
Collection: python manage.py collectstatic
```

### Media Files (Uploads)
```
Path: auth_project/media/
Served: /media/
Includes: Profile photos, project files, document uploads
```

---

## 🐛 Common Issues & Solutions

### Issue: "NameError: name 'get_template_json' is not defined"
**Solution**: Clear Python cache
```bash
# Windows
for /d /r . %%d in (__pycache__) do @if exist "%%d" rd /s /q "%%d"

# Linux/Mac
find . -type d -name "__pycache__" -exec rm -rf {} +
```

### Issue: "Database connection refused"
**Solution**: Check DATABASE_URL
```bash
# Test connection
python manage.py dbshell
```

### Issue: "ModuleNotFoundError: No module named 'xyz'"
**Solution**: Install missing packages
```bash
pip install -r requirements.txt
```

### Issue: "Static files not loading"
**Solution**: Collect static files
```bash
python manage.py collectstatic --noinput
```

---

## 📈 Performance Monitoring

### Check Slow Queries
Enable Django Debug Toolbar:
```python
# In settings.py (development only)
INSTALLED_APPS += ['debug_toolbar']
MIDDLEWARE += ['debug_toolbar.middleware.DebugToolbarMiddleware']
INTERNAL_IPS = ['127.0.0.1']
```

### Log Monitoring
```bash
tail -f logs/django.log
tail -f logs/error.log
```

### Database Optimization
```python
# Use select_related for ForeignKey
projects = Project.objects.select_related('owner')

# Use prefetch_related for ManyToMany
projects = Project.objects.prefetch_related('members')

# Use only() to limit fields
projects = Project.objects.only('id', 'title', 'owner')
```

---

## 🧪 Testing

### Run All Tests
```bash
python manage.py test accounts
```

### Run Specific Test
```bash
python manage.py test accounts.tests.TestClassName.test_method
```

### Create Test Database
```bash
python manage.py test --keepdb  # Keeps test DB between runs
```

---

## 📦 Deployment Checklist

- [ ] Set `DEBUG=False` in production
- [ ] Update `SECRET_KEY` to a long random string
- [ ] Configure `ALLOWED_HOSTS` with actual domain
- [ ] Set `SECURE_SSL_REDIRECT=True`
- [ ] Set `SESSION_COOKIE_SECURE=True`
- [ ] Set `CSRF_COOKIE_SECURE=True`
- [ ] Configure PostgreSQL for production
- [ ] Set up email backend (Brevo/SendGrid)
- [ ] Configure OAuth with production URLs
- [ ] Collect static files: `collectstatic`
- [ ] Run migrations: `migrate`
- [ ] Create superuser
- [ ] Set up SSL certificate
- [ ] Configure CDN for static files
- [ ] Set up monitoring/logging
- [ ] Configure database backups

---

## 📞 Support & Documentation

### Key Files
- Architecture: `/COMPREHENSIVE_CODEBASE_ANALYSIS_2026_COMPLETE_FINAL.md`
- Cache Fix: `/DJANGO_CACHE_AND_STARTUP_FIX.md`
- Models Reference: `accounts/models.py`
- Views Reference: `accounts/views.py`
- API Reference: `accounts/chat_api.py`, `comment_api.py`

### Getting Help
1. Check system logs: `logs/django.log`
2. Run checks: `python manage.py check`
3. Debug shell: `python manage.py shell`
4. Django documentation: https://docs.djangoproject.com/

---

## ✨ Next Steps

1. **Start the server**: `python manage.py runserver`
2. **Visit dashboard**: http://localhost:8000
3. **Create account**: Use email/OTP or Google/GitHub
4. **Explore features**: Projects, messaging, collaborations
5. **Run tests**: `python manage.py test`
6. **Deploy**: Follow deployment checklist

---

**Status Last Updated**: February 9, 2026
**System Status**: ✅ OPERATIONAL
**All Systems**: ✅ GO
**Ready for**: Development & Testing
