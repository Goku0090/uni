# UniSync Code Analysis - Visual Guide

## Quick Reference

### What is UniSync?
A Django-based **collaborative learning platform** where students can:
- Create user profiles with interests, skills, and photos
- Post projects seeking collaborators
- Search for teammates based on skills/interests
- Connect with other students
- Send direct messages & group chats
- View real-time notifications
- Organize teams with roles & tasks
- Track project progress with milestones

---

## Technology Stack at a Glance

```
Frontend:         HTML/CSS/JavaScript (Django Templates)
Backend:          Django 3.x/4.x + Django REST Framework
Database:         PostgreSQL (prod) / SQLite (dev)
Authentication:   Custom OTP + Django-Allauth (Google/GitHub OAuth)
Email:            Brevo / ZeptoMail
Hosting:          Render.com
Caching:          Django Cache Framework
```

---

## File Organization

```
auth_project/
│
├── manage.py                    🚀 Django CLI entry point
├── requirements.txt             📦 Python dependencies
│
├── auth_project/               ⚙️ Project Settings
│   ├── settings.py            (DB, email, security config)
│   ├── urls.py                (Main URL routing)
│   ├── wsgi.py                (Production WSGI)
│   └── asgi.py                (WebSocket support)
│
└── accounts/                   💼 Main Application
    ├── models.py              (15+ database models)
    ├── views.py               (50+ view functions - 3105 lines)
    ├── forms.py               (Form validation)
    ├── urls.py                (API & web routes)
    ├── serializers.py         (REST API serializers)
    ├── permissions.py         (Access control)
    ├── utils.py               (Helper functions & NLP)
    ├── chat_api.py            (Chat/WebSocket)
    ├── zepto_mail_backend.py  (Email service)
    ├── brevo_mail_backend.py  (Alternative email)
    ├── views_contact.py       (Contact form)
    ├── tests.py               (Unit tests)
    │
    ├── services/
    │   └── auth_service.py    (Business logic)
    │
    ├── static/                (CSS, JS, images)
    ├── templates/             (HTML templates)
    ├── migrations/            (Database migrations)
    └── __pycache__/           (Cached Python files)
```

---

## Core Concepts

### 1. User System

```
┌─────────────────────────────────────────┐
│  Django User (Django built-in)          │
│  • username                             │
│  • email                                │
│  • password (hashed)                    │
│  • is_active, is_staff, is_superuser    │
└─────────────────────────────────────────┘
              ↓ (OneToOne)
┌─────────────────────────────────────────┐
│  StudentProfile (Custom Model)          │
│  • full_name                            │
│  • college                              │
│  • location                             │
│  • interests (JSON array)               │
│  • skills (JSON array)                  │
│  • profile_photo (ImageField)           │
│  • bio                                  │
│  • social links (GitHub, LinkedIn, etc) │
│  • profile_completed (boolean)          │
└─────────────────────────────────────────┘
```

### 2. Authentication Modes

#### Traditional Login
```
Password Login → OTP Verification → Session Created
```

#### Social Login
```
Google/GitHub OAuth → Auto-create User → Session Created
```

### 3. Projects & Collaboration

```
Project
  ├── Owner (User FK)
  ├── ProjectTeam
  │   ├── TeamMembers (roles: lead, member, contributor)
  │   └── Invitations (pending/accepted)
  ├── ProjectTasks (subtasks with status)
  ├── ProjectMilestones (timeline phases)
  ├── Comments (discussion)
  ├── Likes (engagement)
  └── Activity Log (history)
```

### 4. Social Graph

```
User ←→ Connection (pending/accepted/rejected)
  │
  ├── Followers / Following
  │
  ├── Direct Messages
  │   └── ChatRoom (1:1 or group)
  │       └── ChatRoomMember
  │           └── MessageReadStatus
  │
  └── Notifications
      └── Activity-based triggers
```

---

## Key Views at a Glance

### Authentication Views (10 views)
| View | What it does |
|------|-------------|
| `register_view()` | Sign up new users |
| `login_view()` | Login → OTP generation |
| `verify_otp_view()` | Verify 6-digit OTP |
| `logout_view()` | Sign out |
| `forgot_password_view()` | Password reset request |
| `reset_password_view()` | Set new password |
| `resend_otp_view()` | Resend OTP email |
| `home_view()` | Dashboard redirect |
| `student_details_view()` | Complete profile wizard |
| `social_login_redirect()` | Allauth callback |

### Project Views (8 views)
| View | What it does |
|------|-------------|
| `post_project()` | Create new project |
| `project_detail()` | View project + comments + team |
| `edit_project()` | Modify project info |
| `delete_project()` | Remove project |
| `explore_projects_view()` | Browse all projects |
| `my_projects_view()` | List my projects |
| `like_project()` | Like project (AJAX) |
| `search_projects()` | Full-text search |

### Collaboration Views (6 views)
| View | What it does |
|------|-------------|
| `find_collaborators()` | Search users with filters |
| `send_connection_request()` | Request to connect |
| `accept_connection()` | Approve connection |
| `reject_connection()` | Decline connection |
| `my_connections()` | View my connections |
| `get_connection_status()` | Check relationship |

### Messaging Views (4 views)
| View | What it does |
|------|-------------|
| `message_view()` | Message inbox |
| `chat_view()` | 1:1 conversation |
| `create_group_chat()` | Group chat setup |
| `add_chat_member()` | Add user to group |

### Other Views (5+ views)
| View | What it does |
|------|-------------|
| `main_home()` | Activity feed |
| `main()` | Landing page |
| `profile_view()` | User's own profile |
| `student_profile()` | Another user's profile |
| `notifications_view()` | Notification inbox |
| `mark_notification_read()` | Mark as read |
| `dashboard_view()` | Main dashboard |

---

## Data Models (15 Models)

```
1. StudentProfile         👤 User extended profile
2. OTP                    🔐 One-time password
3. Connection             🤝 User relationships
4. Message                💬 Direct messages
5. ChatRoom               💬 Group chats
6. ChatRoomMember         👥 Chat participants
7. MessageReadStatus      ✓ Read tracking
8. MessageFile            📎 File attachments
9. MessageReaction        👍 Message reactions
10. Notification          🔔 User alerts
11. Project               📋 Collaboration projects
12. ProjectTeam           👨‍💼 Team management
13. ProjectTeamMember     👤 Team roster
14. ProjectTeamInvitation 📧 Team invites
15. ProjectTask           ✓ Subtasks
16. ProjectMilestone      🎯 Timeline phases
17. Comment               💬 Project comments
18. Like                  ❤️ Project likes
19. Activity              📈 Action log
20. Follow                👁️ Follow users
21. UserStats             📊 User statistics
22. File                  📎 File storage
23. UserStatus            🟢 Online status
```

---

## Authentication Flow (Step-by-Step)

### Registration
```
1. User fills: username, email, password, confirm_password, terms
2. Backend validates:
   - Username: 3+ chars, not taken
   - Email: valid format, not taken (case-insensitive)
   - Password: 8+ chars, uppercase, digit, matches confirm
   - Terms: checkbox must be checked
3. Create User & StudentProfile records
4. Log user in
5. Redirect to /student-details (profile completion)
```

### Login
```
1. User enters: username/email + password
2. Django authenticate():
   - Find user by username or email
   - Check password hash
3. If valid:
   - Generate 6-digit OTP
   - Send email with OTP
   - Store user_id in session['login_user_id']
   - Redirect to /verify-otp/login/
4. User enters OTP
5. Backend validates:
   - OTP exists and not expired (5 min)
   - OTP matches input
   - Mark as used
6. Create session, log user in
7. Send welcome-back email
8. Redirect to main_home
```

### Password Reset
```
1. User enters email
2. Generate OTP → send email
3. User enters OTP
4. Set reset_verified flag in session
5. Redirect to reset_password form
6. User enters new password
7. Update user password
8. Redirect to login
```

---

## Security Features ✅

### Authentication
- ✅ Strong password requirements (8+ chars, uppercase, digit)
- ✅ OTP-based login (not just password)
- ✅ Email verification
- ✅ Session management
- ✅ Password hashing (Django's PBKDF2)

### Input Validation
- ✅ Sanitize user input (strip HTML, remove dangerous chars)
- ✅ Case-insensitive duplicate checks
- ✅ File upload validation (images only: jpg, jpeg, png, gif)

### Database
- ✅ Unique constraints (no duplicate connections, etc.)
- ✅ Foreign key integrity
- ✅ Proper indexing

### API
- ⚠️ CSRF protection (currently disabled in settings, should re-enable)
- ❌ Rate limiting on auth endpoints (missing - security risk)
- ❌ API token authentication (missing)

---

## Email Configuration

### Two Email Services Supported

#### Brevo (Sendinblue)
- File: `brevo_mail_backend.py`
- Use: Transactional emails
- Setup: `BREVO_API_KEY` env var

#### ZeptoMail
- File: `zepto_mail_backend.py`
- Use: Alternative backend
- Setup: `ZEPTO_API_KEY` env var

### Email Types Sent
1. **OTP Email** (registration, login, password reset)
2. **Welcome Back** (after login)
3. **Team Invitation** (project team invite)
4. **Connection Request** (user connection)
5. **Message Notification** (new message alert)

---

## Database Schema (Simplified)

```sql
-- Users
User (Django built-in)
StudentProfile (OneToOne to User)

-- Authentication
OTP (email, otp_code, purpose, expires_at, is_used)

-- Social Network
Connection (sender, receiver, status)
Follow (follower, following)
Activity (user, activity_type, title, description)
UserStats (user, projects_count, connections_count, etc)

-- Messaging
Message (sender, receiver, content, created_at)
ChatRoom (chat_type, name)
ChatRoomMember (user, chat_room)
MessageReadStatus (message, user, read_at)

-- Projects
Project (user, title, description, technologies)
ProjectTeam (project)
ProjectTeamMember (team, user, role, is_active)
ProjectTeamInvitation (team, invited_user, status)
ProjectTask (project, title, status, assigned_to)
ProjectMilestone (project, title, due_date, is_completed)

-- Engagement
Comment (user, project, content)
Like (user, project)
Notification (user, activity_type, is_read)
```

---

## Configuration Files

### settings.py (Main Configuration)
```python
# Database
DATABASE_URL (from environment)
DATABASES (fallback to SQLite if not set)

# Email
EMAIL_BACKEND = 'accounts.brevo_mail_backend.BrevoBackend'
DEFAULT_FROM_EMAIL = os.getenv('DEFAULT_FROM_EMAIL')
BREVO_API_KEY = os.getenv('BREVO_API_KEY')

# Security
DEBUG = os.getenv('DEBUG', 'True')
SECRET_KEY = os.getenv('SECRET_KEY')
ALLOWED_HOSTS = os.getenv('ALLOWED_HOSTS', '...').split(',')
CSRF_COOKIE_SECURE = os.getenv('CSRF_COOKIE_SECURE', 'False')
SESSION_COOKIE_SECURE = os.getenv('SESSION_COOKIE_SECURE', 'False')

# Apps
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'accounts',
    'allauth',
    'rest_framework',
]

# Authentication
AUTHENTICATION_BACKENDS = [
    'django.contrib.auth.backends.ModelBackend',
    'allauth.account.auth_backends.AuthenticationBackend',
]
```

### .env (Environment Variables)
```
DEBUG=True
SECRET_KEY=your-secret-key-here
ALLOWED_HOSTS=localhost,127.0.0.1

DATABASE_URL=postgresql://user:pass@host:5432/dbname
DB_NAME=unisync_db
DB_USER=unisync_user
DB_PASSWORD=password
DB_HOST=localhost
DB_PORT=5432

DEFAULT_FROM_EMAIL=noreply@unisync.com
BREVO_API_KEY=your-brevo-key
ZEPTO_API_KEY=your-zepto-key

GITHUB_CLIENT_ID=xxx
GITHUB_CLIENT_SECRET=xxx
GOOGLE_CLIENT_ID=xxx
GOOGLE_CLIENT_SECRET=xxx

SECURE_SSL_REDIRECT=False
SESSION_COOKIE_SECURE=False
CSRF_COOKIE_SECURE=False
```

---

## API Endpoints

### Auth Endpoints
```
POST   /accounts/register/              Register new user
POST   /accounts/login/                 Login (sends OTP)
POST   /accounts/logout/                Logout
POST   /verify-otp/<purpose>/           Verify OTP code
POST   /forgot-password/                Request password reset
POST   /reset-password/                 Set new password
POST   /resend-otp/<purpose>/           Resend OTP
```

### Project Endpoints
```
GET    /post-project/                   List my projects
POST   /post-project/                   Create project
GET    /project/<id>/                   View project detail
POST   /edit-project/<id>/              Edit project
DELETE /delete-project/<id>/            Delete project
GET    /explore-projects/               Browse all projects
POST   /project/<id>/like/              Like project
GET    /api/search-projects/            Search projects
```

### Collaboration
```
GET    /find-collaborators/             Search users
POST   /connect/<user_id>/              Send connection request
POST   /accept-connection/<id>/         Accept connection
POST   /reject-connection/<id>/         Reject connection
GET    /my-connections/                 View my connections
```

### Messaging
```
GET    /messages/                       Message inbox
GET    /chat/<user_id>/                 1:1 chat
POST   /chat/<user_id>/message/         Send message
GET    /api/messages/<user_id>/         Get message history
```

### Other
```
GET    /notifications/                  View notifications
POST   /notification/<id>/read/         Mark as read
GET    /profile/                        My profile
GET    /student-profile/                View profile
GET    /main_home/                      Main feed
GET    /dashboard/                      Dashboard
```

---

## Common Workflows

### 1. User Signs Up and Creates Profile
```
User → /register/ (form)
  ↓ Submit
  ✓ User created
  ✓ StudentProfile created
  → /student-details/ (profile form)
  ↓ Submit
  ✓ Profile completed
  → /main_home (dashboard)
```

### 2. User Posts a Project
```
User → /post-project/ (form)
  ↓ Submit
  ✓ Project created
  ✓ Activity logged
  → Show project in explore
  → Can receive team invites
```

### 3. Find and Connect with Collaborators
```
User A → /find-collaborators?q=python
  ↓ Search
  ← Results: Users with "python" interest
  ↓ Click Connect on User B
  → /connect/<user_b_id>/
  ✓ Connection request sent
  ↓ User B receives notification
  User B → Accept/Reject
  ✓ Connection status updated
```

### 4. Invite to Project Team
```
User A (project owner)
  → /project/<id>/ (team section)
  → Click "Add Member"
  → Select User B (if connected)
  → Send invitation
  ✓ User B receives notification
  User B → Accept invite
  ✓ User B joins team
  → Can create/assign tasks
```

---

## Issues to Fix

### 🔴 High Priority
1. **CSRF Protection Disabled**
   - Location: settings.py line 68
   - Risk: Cross-site request forgery attacks
   - Fix: Uncomment `'django.middleware.csrf.CsrfViewMiddleware'`

2. **No Rate Limiting on Auth**
   - Location: login_view, verify_otp_view
   - Risk: Brute force attacks
   - Fix: Add `@ratelimit` decorator

### 🟡 Medium Priority
3. **Large views.py File (3105 lines)**
   - Maintainability issue
   - Fix: Split into logical modules

4. **No API Authentication**
   - Risk: Public access to sensitive endpoints
   - Fix: Add DRF TokenAuthentication

5. **Duplicate dashboard_view()**
   - Lines 78 and 201
   - Remove one definition

### 🟢 Low Priority
6. Add comprehensive test coverage
7. Implement API versioning
8. Add pagination to all list endpoints
9. Add caching for expensive queries

---

## Deployment Checklist

- [ ] Set DEBUG=False in production
- [ ] Generate secure SECRET_KEY
- [ ] Configure PostgreSQL DATABASE_URL
- [ ] Set up email service (Brevo API key)
- [ ] Configure OAuth (Google, GitHub)
- [ ] Enable CSRF protection
- [ ] Enable SSL/HTTPS
- [ ] Set SECURE_SSL_REDIRECT=True
- [ ] Set ALLOWED_HOSTS properly
- [ ] Run migrations: `python manage.py migrate`
- [ ] Collect static files: `python manage.py collectstatic`
- [ ] Use gunicorn: `gunicorn auth_project.wsgi:application`
- [ ] Monitor logs for errors

---

## Performance Optimizations

### ✅ Already Implemented
- `select_related()` for FK relationships
- `prefetch_related()` for reverse relationships
- Pagination on project lists
- Caching support via Django cache framework

### 📋 Recommendations
- Add database indexes on frequently filtered columns
- Implement lazy loading for large querysets
- Cache expensive NLP computations
- Use async tasks for email sending (Celery)
- Add CDN for static files
- Implement database query monitoring

---

## Testing Files Available

```
test_login.py             # Login flow tests
test_email.py             # Email backend tests
test_connections.py       # Connection feature tests
test_profile_upload.py    # File upload tests
test_brevo_email.py       # Brevo integration tests
test_zeptomail.py         # ZeptoMail integration tests
test_services.py          # Service layer tests
test_filter.py            # Search/filter tests
```

Run tests:
```bash
python manage.py test accounts
```

---

## Summary

**UniSync** is a well-structured Django application with:
- ✅ Solid foundation (models, forms, views)
- ✅ Feature-rich (projects, messaging, teams)
- ✅ Security basics (password hashing, OTP)
- ⚠️ Needs: CSRF re-enabled, rate limiting, refactoring
- 📈 Growth potential: Mobile API, real-time notifications, analytics

**Next Steps**:
1. Enable CSRF + rate limiting (security)
2. Refactor views.py (maintainability)
3. Add comprehensive tests (reliability)
4. Implement async email (performance)

---

*Generated: 2025-01-04*
