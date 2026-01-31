# UniSync Project - Comprehensive Code Analysis

**Project**: UniSync (Collaborative Learning Platform)  
**Technology Stack**: Django + PostgreSQL + REST API  
**Analysis Date**: January 4, 2026

---

## 1. PROJECT OVERVIEW

UniSync is a Django-based web application designed to connect students, facilitate collaboration, manage projects, and enable real-time communication. The system supports OAuth2 (Google/GitHub), OTP-based authentication, and advanced project management features.

### Key Statistics
- **Primary App**: `accounts` (authentication, profiles, projects, messaging)
- **Database**: PostgreSQL (production) / SQLite (development)
- **Framework**: Django 3.x/4.x + Django REST Framework
- **Authentication**: Custom OTP + Django-Allauth
- **Real-time**: Chat rooms, notifications, activity feeds

---

## 2. ARCHITECTURE & DIRECTORY STRUCTURE

```
auth_project/
├── auth_project/          # Django project settings
│   ├── settings.py       # Configuration (DB, security, email)
│   ├── urls.py          # Main URL routing
│   ├── wsgi.py          # Production deployment
│   └── asgi.py          # Async support
├── accounts/            # Main application
│   ├── models.py        # 15+ models (User, Project, Message, Chat, etc.)
│   ├── views.py         # 3100+ lines, 50+ view functions
│   ├── forms.py         # Registration, login, OTP, profile forms
│   ├── urls.py          # API & web routes
│   ├── serializers.py   # REST API serializers
│   ├── permissions.py   # Custom permission classes
│   ├── utils.py         # NLP utilities, helpers
│   ├── chat_api.py      # WebSocket/Chat functionality
│   ├── views_contact.py # Contact form handling
│   ├── zepto_mail_backend.py    # Email service integration
│   ├── brevo_mail_backend.py    # Alternative email service
│   └── services/        # Business logic services
│       └── auth_service.py
├── requirements.txt     # Dependencies
├── manage.py           # Django CLI
└── db.sqlite3          # Local development database
```

---

## 3. CORE MODELS (models.py)

### 3.1 User & Profile Management

#### **StudentProfile**
- OneToOneField relationship with Django User
- Stores: full_name, college, location, interests (JSON), bio
- Profile photo upload with validation (jpg, jpeg, png, gif)
- Social links: GitHub, LinkedIn, portfolio, Behance
- Profile completion tracking

#### **OTP (One-Time Password)**
- Purpose choices: 'login', 'registration', 'reset'
- 6-digit alphanumeric code
- 5-minute expiration window
- Methods:
  - `generate_otp()` - Creates new OTP, deactivates old ones
  - `verify_otp()` - Validates code and expiry
  - `is_valid()` - Checks status and expiration

### 3.2 Social & Collaboration

#### **Connection**
- User-to-user relationship requests
- Status: pending, accepted, rejected
- Unique constraint: (sender, receiver)
- Used for discovering collaborators

#### **Message**
- Direct messages with threading support
- Types: text, file, image, call
- Supports group chats via ChatRoom FK
- Read status tracking via MessageReadStatus model

#### **ChatRoom**
- Direct or group chats
- Members tracked via ChatRoomMember
- Message history & read status

#### **Notification**
- Activity alerts for users
- Types: connection_request, message, project_invite, etc.
- Mark as read functionality

### 3.3 Project Management

#### **Project**
- Owner: FK to User
- Fields: title, description, technologies, looking_for, category
- Collaboration features: timeline, github_link, collaboration_needs
- Related: Like, Comment, ProjectTeam

#### **ProjectTeam**
- Team organization per project
- ProjectTeamMember: tracks roles (lead, member, contributor)
- ProjectTeamInvitation: invite management with pending status

#### **ProjectTask**
- Subtasks within projects
- Status: pending, in_progress, completed
- Assignments, due dates, descriptions

#### **ProjectMilestone**
- Project phases/milestones
- Completion tracking
- Timeline management

### 3.4 Community Features

#### **Follow**
- Users can follow other users
- Track follower/following relationships

#### **Like**
- Like projects
- User + Project unique constraint

#### **Comment**
- Comments on projects
- User, project, content relationship

#### **Activity**
- User activity log (project creation, likes, connections, etc.)
- Timestamps for activity feeds

#### **UserStats**
- Aggregated user statistics
- Projects count, connections count, followers count

---

## 4. AUTHENTICATION FLOW

### 4.1 Registration Flow
```
POST /register/
├── Validate username (not taken, 3+ chars)
├── Validate email (not taken, lowercase)
├── Validate password (8+ chars, uppercase, digit, match confirm)
├── Check terms agreement
└── Create User + StudentProfile
    └── Redirect to student_details
```

### 4.2 Login Flow
```
POST /login/
├── Form validation (username or email)
├── Django authenticate()
├── Generate OTP for email
├── Store user_id in session
└── Redirect to /verify-otp/login/

POST /verify-otp/login/
├── Retrieve stored user_id from session
├── Validate OTP code (6 digits, not expired)
├── Mark OTP as used
├── login() user
└── Redirect to main_home
```

### 4.3 Password Reset Flow
```
POST /forgot-password/
├── Email validation
├── Generate OTP
├── Store email in session
└── Redirect to /verify-otp/reset/

POST /reset-password/ (after OTP verification)
├── Check reset_verified session flag
├── Update user password
└── Redirect to login
```

### 4.4 OTP Email Template
- HTML + plaintext variants
- Branding: "🚀 Team"
- 5-minute validity message
- Professional styling

---

## 5. KEY VIEW FUNCTIONS (views.py - 3105+ lines)

### 5.1 Authentication Views

| View | Method | Purpose |
|------|--------|---------|
| `register_view()` | POST/GET | User registration with validation |
| `login_view()` | POST/GET | Login, OTP generation |
| `verify_otp_view()` | POST/GET | OTP verification (3 purposes) |
| `logout_view()` | GET | Session cleanup |
| `forgot_password_view()` | POST/GET | Password reset request |
| `reset_password_view()` | POST/GET | New password submission |
| `resend_otp_view()` | POST | Resend OTP email |

### 5.2 Profile Views

| View | Purpose |
|------|---------|
| `edit_profile()` | Edit profile + avatar upload |
| `student_profile()` | View user profile |
| `student_details_view()` | Profile completion wizard |
| `dashboard_view()` | User dashboard (projects, activities) |

### 5.3 Project Management Views

| View | Purpose |
|------|---------|
| `post_project()` | Create/list user projects |
| `project_detail()` | View project, comments, team |
| `edit_project()` | Modify project info |
| `delete_project()` | Remove project |
| `explore_projects_view()` | Browse all projects |
| `my_projects_view()` | User's project list |
| `like_project()` | Toggle like (AJAX) |

### 5.4 Collaboration Views

| View | Purpose |
|------|---------|
| `find_collaborators()` | Search users with filtering |
| `send_connection_request()` | Initiate connection |
| `accept_connection()` | Accept pending request |
| `reject_connection()` | Decline connection |
| `my_connections()` | View user's connections |

### 5.5 Messaging & Chat

| View | Purpose |
|------|---------|
| `message_view()` | Direct messages inbox |
| `chat_view()` | 1:1 conversation |
| `create_group_chat()` | Group chat creation |
| `add_chat_member()` | Add user to group |

### 5.6 Community Features

| View | Purpose |
|------|---------|
| `notifications_view()` | User notifications |
| `mark_notification_read()` | Mark notification as read |
| `main_home()` | Main feed + activities |

---

## 6. FORMS (forms.py)

### 6.1 **RegisterForm**
- Extends UserCreationForm
- Validates: username (3-150 chars), email, password strength, terms agreement
- Clean methods for duplicate checking (case-insensitive)

### 6.2 **LoginForm**
- Extends AuthenticationForm
- "Remember me" checkbox
- Accepts username OR email

### 6.3 **OTPVerificationForm**
- 6-digit OTP code input
- Numeric validation
- HTML5 pattern: [0-9]{6}

### 6.4 **StudentProfileForm**
- Model form for StudentProfile
- Profile photo upload
- JSON arrays: interests, skills, project_interests
- Social links validation

### 6.5 **ProjectForm**
- Create/edit projects
- Technologies, looking_for (comma-separated)
- Category selection
- GitHub link validation

---

## 7. EMAIL SYSTEM

### 7.1 Email Backends
Two configurable email services:

#### **Brevo (formerly Sendinblue)**
- File: `brevo_mail_backend.py`
- Configuration: API key in .env
- Use case: Transactional emails

#### **ZeptoMail**
- File: `zepto_mail_backend.py`
- Configuration: Domain, API key
- Use case: Alternative backend

### 7.2 OTP Email Sending
```python
send_otp_email(email, otp_code, purpose):
  - Creates HTML + plaintext message
  - Sends via Django's EmailMultiAlternatives
  - Logs success/failure
  - Notifies admin on failure
  - OTP still created even if email fails
```

### 7.3 Welcome Back Email
- Sent after successful login
- Via `AuthService.send_welcome_back_email()`
- Non-blocking (try/except wrapper)

---

## 8. SECURITY FEATURES

### 8.1 Authentication Security
- ✅ Password strength validation (uppercase, digit, 8+ chars)
- ✅ OTP-based login (not just password)
- ✅ Case-insensitive duplicate checks
- ✅ Session management (login_user_id storage)
- ✅ CSRF protection (middleware enabled)

### 8.2 Input Validation
```python
sanitize_input(text, max_length=None):
  - Strip HTML tags
  - Remove dangerous characters (<, >)
  - Trim whitespace
  - Apply length limits
```

### 8.3 Database Security
- Unique constraints on sensitive combinations
- FK relationships for referential integrity
- Proper indexing (created_at, user fields)

### 8.4 Configuration Security
- Environment variables for secrets
- Separate settings for DEBUG/PROD
- SSL/HTTPS redirects (configurable)
- Secure session cookies (configurable)

### 8.5 Error Handling
```python
@handle_view_errors decorator:
  - Catches all exceptions
  - Logs with full traceback
  - Displays user-friendly messages
  - Avoids redirect loops
```

---

## 9. DATABASE QUERIES & OPTIMIZATION

### 9.1 Query Patterns

#### **Select Related (Join Optimization)**
```python
# User connections with profile data
connected_users.select_related('sender', 'receiver')

# Chat members with user info
ChatRoomMember.objects.select_related('user__student_profile')
```

#### **Prefetch Related (Separate Queries)**
```python
# Project teams with active members
team.active_members.select_related('user__student_profile')
```

#### **Filtering Patterns**
```python
# Search projects
Q(title__icontains=query) | 
Q(description__icontains=query) |
Q(collaboration_needs__icontains=query)

# Find connections
Q(sender=user, status='accepted') |
Q(receiver=user, status='accepted')
```

### 9.2 Pagination
```python
from django.core.paginator import Paginator

paginator = Paginator(objects, 10)  # 10 per page
page_obj = paginator.get_page(page_number)
```

### 9.3 Caching
```python
from django.core.cache import cache
from django.views.decorators.cache import cache_page

@cache_page(60 * 5)  # Cache for 5 minutes
def view_func(request):
    ...
```

---

## 10. REST API ENDPOINTS

Located in `accounts/urls.py`:

### Authentication Routes
```
POST   /accounts/register/
POST   /accounts/login/
POST   /accounts/logout/
POST   /verify-otp/<purpose>/
POST   /forgot-password/
POST   /reset-password/
```

### Project Routes
```
POST   /post-project/              - Create project
GET    /project/<id>/              - Project details
POST   /project/<id>/like/         - Like project
GET    /explore-projects/          - Browse projects
GET    /my-projects/               - User's projects
PUT    /edit-project/<id>/         - Edit project
DELETE /delete-project/<id>/       - Delete project
```

### Collaboration Routes
```
GET    /find-collaborators/        - Search users
POST   /connect/<user_id>/         - Send connection
POST   /accept-connection/<id>/    - Accept request
POST   /reject-connection/<id>/    - Reject request
GET    /my-connections/            - List connections
```

### Messaging Routes
```
GET    /messages/                  - Message inbox
GET    /chat/<user_id>/            - 1:1 chat
POST   /chat/<user_id>/message/    - Send message
```

### Notification Routes
```
GET    /notifications/             - List notifications
POST   /notification/<id>/read/    - Mark as read
```

---

## 11. SETTINGS CONFIGURATION (settings.py)

### 11.1 Database Setup
```python
# Production (Render)
DATABASE_URL → dj_database_url.parse()

# Local Development
PostgreSQL (configurable) or SQLite fallback
Environment: DB_NAME, DB_USER, DB_PASSWORD, DB_HOST, DB_PORT
```

### 11.2 Email Configuration
```python
EMAIL_BACKEND = 'accounts.brevo_mail_backend.BrevoBackend'
DEFAULT_FROM_EMAIL = os.getenv('DEFAULT_FROM_EMAIL')
BREVO_API_KEY = os.getenv('BREVO_API_KEY')
```

### 11.3 Installed Apps
- Django core (admin, auth, sessions, etc.)
- **accounts** (custom app)
- **allauth** + social providers (Google, GitHub)
- **rest_framework** (DRF)

### 11.4 Security Middleware
```python
SecurityMiddleware
SessionMiddleware
AuthMiddleware
MessageMiddleware
AllAuth AccountMiddleware
```

### 11.5 Authentication Backends
```python
AUTHENTICATION_BACKENDS = [
    'django.contrib.auth.backends.ModelBackend',
    'allauth.account.auth_backends.AuthenticationBackend',
]
```

---

## 12. UTILITY FUNCTIONS

### 12.1 StudentProfileNLP (utils.py)
```python
class StudentProfileNLP:
  - Analyze interests/skills for recommendations
  - Find similar users (NLP-based)
  - Generate activity summaries
```

### 12.2 Helper Functions
```python
create_activity()          # Log user actions
send_notification()        # Create notifications
get_connection_status()    # Check user relationship
sanitize_input()          # Prevent XSS
```

---

## 13. POTENTIAL ISSUES & IMPROVEMENTS

### 13.1 Issues Found

| Issue | Location | Severity | Impact |
|-------|----------|----------|--------|
| Duplicate `dashboard_view` | views.py:78, 201 | Medium | Confusion, one redirects to main_home |
| CSRF disabled | settings.py:68 | High | Security risk, enable in production |
| Missing `.env` validation | settings.py:18-27 | Medium | Could crash in production without SECRET_KEY |
| Deprecated error handler | views.py:90-104 | Low | Works but uses old redirect pattern |
| No rate limiting | OTP views | High | Could enable brute force attacks |
| No API authentication | REST endpoints | Medium | Public access to sensitive data |
| Long view file | views.py (3105 lines) | Medium | Hard to maintain, should split |

### 13.2 Recommended Improvements

1. **Enable CSRF Protection**
   ```python
   # In settings.py, uncomment:
   'django.middleware.csrf.CsrfViewMiddleware'
   ```

2. **Add Rate Limiting**
   ```python
   # Use django-ratelimit on OTP views
   from django_ratelimit.decorators import ratelimit
   @ratelimit(key='user', rate='5/h', method='POST')
   ```

3. **Implement Token-based API Auth**
   ```python
   # Add DRF TokenAuthentication
   REST_FRAMEWORK = {
       'DEFAULT_AUTHENTICATION_CLASSES': [
           'rest_framework.authentication.TokenAuthentication',
       ]
   }
   ```

4. **Refactor Large Views**
   ```
   Split views.py into:
   - views_auth.py (auth views)
   - views_projects.py (project views)
   - views_messaging.py (chat/messages)
   - views_profile.py (profile views)
   - views_social.py (connections, follow, etc.)
   ```

5. **Add API Versioning**
   ```python
   REST_FRAMEWORK = {
       'DEFAULT_VERSIONING_CLASS': 'rest_framework.versioning.URLPathVersioning',
   }
   # Then: /api/v1/projects/, /api/v2/projects/
   ```

---

## 14. TESTING UTILITIES

Located in root directory:

```
test_*.py files:
  - test_login.py           # Login flow validation
  - test_email.py           # Email backend testing
  - test_connections.py     # Connection requests
  - test_filter.py          # Search functionality
  - test_search.py          # Project search
  - test_services.py        # Service layer tests
  - test_profile_upload.py  # File upload validation
  - test_brevo_email.py     # Brevo integration
  - test_zeptomail.py       # ZeptoMail integration
```

---

## 15. DEPLOYMENT CONFIGURATION

### 15.1 Render Deployment
```yaml
# render.yaml
services:
  - name: unisync
    runtime: python-3.x
    buildCommand: pip install -r requirements.txt && python manage.py migrate
    startCommand: gunicorn auth_project.wsgi:application
    envVars:
      - key: DATABASE_URL
      - key: SECRET_KEY
      - key: DEBUG
        value: false
```

### 15.2 Environment Variables
```
DEBUG=False
SECRET_KEY=<generate-secure-key>
ALLOWED_HOSTS=yourdomain.com,www.yourdomain.com
DATABASE_URL=postgresql://user:pass@host:5432/dbname
DEFAULT_FROM_EMAIL=noreply@yourdomain.com
BREVO_API_KEY=<api-key>
ZEPTO_API_KEY=<api-key>
GITHUB_CLIENT_ID=<oauth-id>
GOOGLE_CLIENT_ID=<oauth-id>
SECURE_SSL_REDIRECT=True
SESSION_COOKIE_SECURE=True
CSRF_COOKIE_SECURE=True
```

---

## 16. DATA FLOW DIAGRAM

```
User Registration:
  register_view() 
  → User + StudentProfile created
  → Validation applied
  → Redirect to student_details

User Login:
  login_view() 
  → OTP generated & emailed
  → Session stores user_id
  → verify_otp_view() logs in user
  → Activity recorded

Project Creation:
  post_project()
  → Project + Activity created
  → Timestamps recorded
  → Owner linked

Messaging:
  chat_view()
  → Message stored
  → MessageReadStatus tracked
  → Notification sent to receiver
  → Activity logged

Collaboration:
  find_collaborators()
  → Users filtered by interests/skills
  → Connection status checked
  → Suggestions generated
  → NLP similarity computed
```

---

## 17. CODE QUALITY METRICS

| Metric | Status | Notes |
|--------|--------|-------|
| **Code Organization** | 🟡 Good | Should split large files |
| **Documentation** | 🟡 Partial | Docstrings added to main views |
| **Error Handling** | 🟢 Good | Try/except wrappers, logging |
| **Security** | 🟡 Fair | Missing CSRF, rate limiting |
| **Testing** | 🟡 Partial | Test files exist, not comprehensive |
| **API Design** | 🟢 Good | RESTful endpoints, proper methods |
| **Database** | 🟢 Good | Proper relationships, indexing |
| **Performance** | 🟡 Fair | Uses select_related, could optimize more |

---

## 18. SUMMARY

**UniSync** is a feature-rich Django collaboration platform with:
- ✅ Robust authentication (password + OTP)
- ✅ Project management system
- ✅ Real-time messaging
- ✅ Connection/networking features
- ✅ Activity feeds & notifications
- ✅ Profile management with photos
- ⚠️ Needs CSRF re-enabled
- ⚠️ Needs rate limiting on auth endpoints
- ⚠️ Large views.py file should be refactored

**Recommended Priority**:
1. Enable CSRF protection (security)
2. Add rate limiting (security)
3. Refactor views.py (maintainability)
4. Add comprehensive tests (reliability)
5. Implement API authentication (security)

---

*Analysis completed: 2025-01-04*
