# UniSync Codebase Analysis - Executive Summary
**Date:** February 6, 2026

---

## Quick Navigation

📄 **Main Analysis:** `COMPREHENSIVE_CODE_ANALYSIS_2026_FINAL.md` (16 sections, 400+ lines)

---

## Project Overview

**UniSync** is a Django-based platform for student collaboration featuring project sharing, real-time messaging, and peer networking.

### Key Metrics
| Metric | Value |
|--------|-------|
| **Framework** | Django 4.2.8 |
| **Database Models** | 25+ |
| **View Functions** | 100+ |
| **API Endpoints** | 64 |
| **Dependencies** | 40+ |
| **Lines of Code (Models)** | 718 |
| **Lines of Code (Views)** | 3,387+ |
| **Authentication Methods** | 3 (Username, OTP, OAuth2) |

---

## Technology Stack

### Backend
```
Django 4.2.8          - Web framework
Python 3.9+           - Language
PostgreSQL            - Production database
SQLite                - Development database
Gunicorn              - WSGI server
```

### Real-time & Communication
```
Django Channels       - WebSocket support
channels-redis        - Message broker
Brevo/ZeptoMail       - Email delivery
```

### APIs & Services
```
Django REST Framework - REST API
django-allauth        - OAuth2/Social auth
RapidAPI              - University data
```

### Development
```
pytest                - Testing
Black                 - Code formatting
flake8                - Linting
redis                 - Caching
```

---

## Architecture at a Glance

### Folder Structure
```
auth_project/
├── auth_project/          ← Django config
├── accounts/              ← Main application
│   ├── models.py          ← 25+ models
│   ├── views.py           ← 100+ views
│   ├── urls.py            ← 64 endpoints
│   ├── forms.py           ← Form validation
│   ├── serializers.py     ← REST serializers
│   ├── services/          ← Business logic
│   ├── comment_api.py     ← Comment endpoints
│   ├── chat_api.py        ← Chat endpoints
│   └── consumers.py       ← WebSocket handlers
├── templates/             ← HTML templates
├── static/                ← CSS/JS/images
└── media/                 ← User uploads
```

### Layer Breakdown
```
┌─────────────────────────────────────┐
│   Web Browser / Mobile App           │ ← Client
├─────────────────────────────────────┤
│   HTML Templates + Static Assets    │ ← Presentation
├─────────────────────────────────────┤
│   Django Views + Forms + Serializers │ ← Request Handler
├─────────────────────────────────────┤
│   Services + Utilities + APIs        │ ← Business Logic
├─────────────────────────────────────┤
│   Django Models (25+ models)         │ ← Data Layer
├─────────────────────────────────────┤
│   PostgreSQL + Redis Cache          │ ← Persistence
└─────────────────────────────────────┘
```

---

## Database Schema Overview

### Core User Models (3)
| Model | Purpose | Key Fields |
|-------|---------|-----------|
| **User** | Django auth | username, email, password |
| **StudentProfile** | Extended profile | full_name, college, bio, photo |
| **OTP** | One-time codes | code, purpose, expires_at |

### Relationships (3)
| Model | Purpose | Relationship |
|-------|---------|--------------|
| **Connection** | Peer networking | user A ↔ user B |
| **Follow** | User following | follower → following |
| **Activity** | Action logging | user → activity |

### Projects (7)
| Model | Purpose | Key Fields |
|-------|---------|-----------|
| **Project** | Main project | title, visibility, status |
| **ProjectMember** | Team member | role (owner/admin/contributor) |
| **ProjectTask** | Task tracking | status, priority, due_date |
| **ProjectMilestone** | Milestones | title, due_date, completed |
| **ProjectInvitation** | Team invites | status, expires_at |
| **ProjectTeam** | Alias | Same as ProjectMember |
| **ProjectTeamMember** | Alias | Same as ProjectMember |

### Messaging (6)
| Model | Purpose | Key Fields |
|-------|---------|-----------|
| **Message** | Text messages | content, sender, receiver |
| **ChatRoom** | Group chats | members, chat_type |
| **ChatRoomMember** | Chat membership | is_active |
| **MessageFile** | File attachments | file reference |
| **MessageReaction** | Reactions | emoji/text |
| **MessageReadStatus** | Read tracking | read_at |

### Social (3)
| Model | Purpose | Key Fields |
|-------|---------|-----------|
| **Comment** | Project comments | content, created_at |
| **Like** | Project appreciation | unique: user+project |
| **UserStats** | Analytics | projects_created, likes_received |

### Supporting (3)
| Model | Purpose | Key Fields |
|-------|---------|-----------|
| **File** | General uploads | file, filename, file_size |
| **Notification** | User alerts | type, is_read |
| **Draft** | Message drafts | content, chat_room |

---

## Key Features Explained

### 1️⃣ Authentication (3 Methods)

#### Traditional Login
```
Email + Password → User.objects.authenticate() → Session
```

#### OTP Authentication
```
Email → Generate 6-digit code → Email delivery → Verify → Create User
```

#### OAuth2 Social Login
```
Click "Login with Google/GitHub" → allauth redirect → Callback → Auto-create User
```

**Implementation:** `accounts/views.py` (lines 200-700), `accounts/forms.py`

---

### 2️⃣ Project Management

**Features:**
- Create/edit/delete projects
- Role-based team members
- Task tracking with status
- Milestones for planning
- Async team invitations

**Model:** Project (20+ fields)  
**Relations:** User (owner), ProjectMember (team), ProjectTask, ProjectMilestone

**Visibility Control:**
```python
VISIBILITY_CHOICES = [
    ('public', 'Everyone'),           # Discoverable
    ('private', 'Owner only'),        # Hidden
    ('connection_only', 'Connections'), # Network restricted
]
```

---

### 3️⃣ Comments & Live Feed

**Feature:** Comment on projects without connection requirement

**Endpoints:**
```
POST   /api/projects/<id>/comments/add/    ← Add comment
GET    /api/projects/<id>/comments/        ← Get all
DELETE /api/comments/<id>/delete/          ← Delete (owner)
PUT    /api/comments/<id>/edit/            ← Edit (author)
```

**Implementation:** `comment_api.py` (243 lines)

**Auto-features:**
- Notification to project owner
- Activity logging
- Profile photo display
- Permission checking

---

### 4️⃣ Real-time Messaging

**Tech:** Django Channels + WebSocket + Redis

**Features:**
- Direct messaging
- Group chats
- Typing indicators
- Message reactions
- File sharing
- Read receipts
- Message threading

**Models:**
- Message (with read_status tracking)
- ChatRoom (direct/group)
- MessageFile (attachments)
- MessageReaction (emojis)

---

### 5️⃣ Collaborator Discovery

**Algorithm:** NLP-based matching using StudentProfileNLP utility

**Filters:**
- Skills (JSON array matching)
- College (exact match)
- Interests (keyword match)
- Excludes self & existing connections

**Endpoint:** `GET /find-collaborators/?skills=python,django&college=MIT`

---

### 6️⃣ Connection System

**States:** pending → accepted/rejected

**Flow:**
1. User A sends connection request to User B
2. Creates `Connection(sender=A, receiver=B, status='pending')`
3. Notification sent to User B
4. User B accepts → status='accepted'
5. Auto-activity log created

**Endpoints:**
```
POST /send-connection/<user_id>/     ← Send request
POST /accept-connection/<conn_id>/   ← Accept
POST /reject-connection/<conn_id>/   ← Reject
GET  /my-connections/                ← List accepted
```

---

### 7️⃣ Email System

**Dynamic Backend Selection:**
1. ✅ Brevo (primary) - if `BREVO_API_KEY` set
2. ✅ ZeptoMail (backup) - if `ZEPTO_MAIL_*` set
3. ✅ Gmail SMTP - if `EMAIL_HOST_*` set
4. ℹ️ Console - development fallback

**Email Types:**
- Welcome (new registration)
- Welcome Back (returning user)
- OTP codes (login/reset)
- Notifications (comments, connections)
- Password Reset

**Implementation:** `services/auth_service.py` (470 lines)

---

### 8️⃣ Activity & Analytics

**Activity Tracking:**
- Project created/liked
- Connections made
- Comments added
- User followed
- Tasks completed

**User Statistics:**
```python
UserStats.update_stats() updates:
  - projects_created
  - connections_made
  - likes_received
  - comments_made
  - followers/following count
  - tasks_completed
```

---

## API Architecture

### Base URL
```
http://localhost:8000/api/
```

### Endpoint Categories

#### Authentication (2)
```
POST   /check-username/              ← Availability
POST   /check-email/                 ← Availability
```

#### User Profile (3)
```
GET    /user-profile/<id>/           ← User profile
GET    /user-stats/                  ← Statistics
GET    /user/<username>/             ← By username
```

#### Projects (5)
```
GET    /projects/                    ← List
POST   /projects/                    ← Create
GET    /projects/<id>/               ← Detail
PUT    /projects/<id>/               ← Update
DELETE /projects/<id>/               ← Delete
```

#### Comments (4)
```
GET    /projects/<id>/comments/      ← Get all
POST   /projects/<id>/comments/add/  ← Create
DELETE /comments/<id>/delete/        ← Delete
PUT    /comments/<id>/edit/          ← Update
```

#### Messaging (5)
```
GET    /chat-rooms/                  ← List rooms
POST   /chat-rooms/                  ← Create
GET    /messages/                    ← List messages
POST   /messages/                    ← Create
GET    /conversations/               ← Conversation list
```

#### Search & Discovery (3)
```
POST   /college-search/              ← Find college
POST   /validate-college/            ← Validate
GET    /nlp-analyze/                 ← NLP matching
```

---

## View Functions Summary

### Authentication Views (6)
| Function | Path | Method | Purpose |
|----------|------|--------|---------|
| register_view | /register/ | GET/POST | User signup |
| login_view | /login/ | GET/POST | User login |
| logout_view | /logout/ | POST | User logout |
| verify_otp_view | /verify-otp/ | GET/POST | Verify code |
| forgot_password_view | /forgot-password/ | GET/POST | Reset flow |
| reset_password_view | /reset-password/ | GET/POST | Set new pwd |

### Profile Views (5)
| Function | Path | Method |
|----------|------|--------|
| student_profile | /student-profile/ | GET |
| student_details_view | /student-details/ | GET/POST |
| user_profile | /user/<username>/ | GET |
| user_profile_api | /api/user-profile/<id>/ | GET |
| edit_profile | /edit-profile/ | GET/POST |

### Project Views (7)
| Function | Path | Method |
|----------|------|--------|
| post_project | /post-project/ | GET/POST |
| project_detail | /project-detail/<id>/ | GET |
| edit_project | /edit-project/<id>/ | GET/POST |
| delete_project | /delete-project/<id>/ | POST |
| my_projects_view | /my-projects/ | GET |
| explore_projects_view | /explore-projects/ | GET |
| like_project | /like-project/<id>/ | POST |

### Social Views (6)
| Function | Path | Method |
|----------|------|--------|
| find_collaborators | /find-collaborators/ | GET |
| send_connection_request | /send-connection/<id>/ | POST |
| accept_connection | /accept-connection/<id>/ | POST |
| reject_connection | /reject-connection/<id>/ | POST |
| my_connections | /my-connections/ | GET |
| follow_user | /follow/<id>/ | POST |

### Messaging Views (4)
| Function | Path | Method |
|----------|------|--------|
| message_view | /messages/ | GET |
| chat_view | /chat/<user_id>/ | GET/POST |
| enhanced_messages_view | /enhanced-messages/ | GET |
| enhanced_chat_view | /enhanced-chat/<room_id>/ | GET/POST |

---

## Forms Overview

### RegisterForm
```python
Fields:
  - username (3-150 chars, unique)
  - email (required, unique)
  - password1 (8+ chars, mixed case, digits)
  - password2 (confirmation)
  - terms_agree (checkbox)

Validation:
  ✓ Username uniqueness
  ✓ Email uniqueness
  ✓ Password complexity
  ✓ Password match
```

### StudentProfileForm
```python
Fields:
  - full_name
  - college (validated)
  - location
  - bio
  - interests (JSON)
  - skills (JSON)
  - profile_photo
  - social links (github, linkedin, etc.)

Validation:
  ✓ Image file validation
  ✓ College RapidAPI lookup
```

### ProjectForm
```python
Fields:
  - title
  - description
  - category
  - tags (JSON)
  - collaboration_needs
  - visibility
  - status
  - funding info

Validation:
  ✓ Title required
  ✓ Visibility choices
  ✓ Tag format
```

### OTPVerificationForm
```python
Fields:
  - otp_code (6 digits)

Validation:
  ✓ Exactly 6 digits
  ✓ Matches stored code
  ✓ Not expired
  ✓ Not already used
```

---

## Security Features

### CSRF Protection
✅ Middleware enabled  
✅ {% csrf_token %} in forms  
✅ X-CSRFToken header in AJAX  
✅ Cookie-based tokens

### Password Security
✅ Hashed with Django's default (PBKDF2)  
✅ Complexity validation (length, case, digits)  
✅ Not stored in logs

### SQL Injection Prevention
✅ ORM parameterized queries  
✅ No raw SQL in views

### XSS Prevention
✅ Template auto-escaping  
✅ Safe filter for HTML

### Authentication
✅ Session-based for web  
✅ OAuth2 for social login  
✅ OTP for password reset

### Authorization
✅ @login_required decorators  
✅ Permission checks in views  
✅ Role-based access (ProjectMember)

---

## Performance Optimizations

### Database Queries
✅ select_related() for ForeignKey joins  
✅ prefetch_related() for M2M  
✅ Database-level unique constraints  
✅ Proper indexing

### Caching
✅ Redis backend  
✅ User profile cache  
✅ Project listing cache  
✅ Collaborator results cache

### Pagination
✅ Default 10 items per page  
✅ Max 100 items per page  
✅ Cursor pagination capable

### File Handling
✅ AWS S3 support (boto3)  
✅ File size limits  
✅ Image optimization (Pillow)

---

## Environment Configuration

### Required Variables
```env
# Security
DEBUG=True/False
SECRET_KEY=your_key
ALLOWED_HOSTS=localhost,127.0.0.1

# Database
DATABASE_URL=postgresql://user:pass@host/db
OR
DB_NAME=unisync_db
DB_USER=unisync_user
DB_PASSWORD=password
DB_HOST=localhost
DB_PORT=5432

# Email (one required)
BREVO_API_KEY=key
OR
ZEPTO_MAIL_API_KEY=key
ZEPTO_MAIL_TOKEN=token
OR
EMAIL_HOST_USER=email@gmail.com
EMAIL_HOST_PASSWORD=app_password

# OAuth (optional)
GOOGLE_CLIENT_ID=id
GOOGLE_CLIENT_SECRET=secret
GITHUB_CLIENT_ID=id
GITHUB_CLIENT_SECRET=secret

# External APIs
RAPIDAPI_KEY=key
```

---

## Deployment Configuration

### Procfile (Render)
```
web: gunicorn auth_project.wsgi:application
```

### render.yaml
```yaml
services:
  - type: web
    name: unisync
    env: python
    buildCommand: pip install -r requirements.txt && python manage.py migrate
    startCommand: gunicorn auth_project.wsgi:application
```

### Key Production Settings
```python
DEBUG = False
SECURE_SSL_REDIRECT = True
SESSION_COOKIE_SECURE = True
CSRF_COOKIE_SECURE = True
ALLOWED_HOSTS = [production_domain]
```

---

## Known Issues & Resolutions

### Issue 1: CSRF Token Warnings
**Status:** ✅ FIXED  
**Solution:** Correct middleware order in settings.py

### Issue 2: Template Recursion
**Status:** ✅ FIXED  
**Solution:** Fix template inheritance order

### Issue 3: Like Button State
**Status:** ✅ FIXED  
**Solution:** Implement cache invalidation on like/unlike

### Issue 4: Comment Visibility
**Status:** ✅ FIXED  
**Solution:** Add proper permission checks in API

### Issue 5: Project Detail Loading
**Status:** ✅ FIXED  
**Solution:** Optimize with select_related/prefetch_related

---

## Code Quality

### Strengths
✅ Clear separation of concerns  
✅ DRY principle applied  
✅ Comprehensive docstrings  
✅ Consistent naming conventions  
✅ Error handling with logging  
✅ Form validation  
✅ API documentation  
✅ Proper use of Django best practices

### Areas for Enhancement
📝 Add comprehensive API documentation (drf-spectacular)  
📝 Increase test coverage  
📝 Add GraphQL support (optional)  
📝 Implement rate limiting  
📝 Add monitoring (Sentry)  
📝 Add logging to all critical paths

---

## Testing Capability

### Testing Tools Available
```
pytest==7.4.3          - Test framework
pytest-django==4.7.0   - Django plugin
selenium==4.16.0       - Browser testing
```

### Test Structure
```
tests/
├── test_models.py      - Model tests
├── test_views.py       - View tests
├── test_forms.py       - Form validation
├── test_api.py         - API endpoint tests
└── test_integration.py - Integration tests
```

---

## Development Workflow

### Setup
```bash
# Create virtual environment
python -m venv venv
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Set up environment
cp .env.template .env
# Edit .env with your settings

# Run migrations
python manage.py migrate

# Create superuser
python manage.py createsuperuser

# Run development server
python manage.py runserver
```

### Development Tools
```bash
# Code formatting
black accounts/

# Linting
flake8 accounts/

# Testing
pytest

# Database shell
python manage.py dbshell

# Django shell
python manage.py shell
```

---

## File Organization

### Key Files
```
auth_project/
├── settings.py         (356 lines) - All configuration
├── urls.py             (60 lines)  - URL routing
├── asgi.py             (15 lines)  - WebSocket config
└── wsgi.py             (15 lines)  - Production config

accounts/
├── models.py           (718 lines) - 25+ models
├── views.py            (3387 lines)- 100+ views
├── urls.py             (129 lines) - 64 API routes
├── forms.py            (609 lines) - Form classes
├── serializers.py      (200+ lines)- DRF serializers
├── comment_api.py      (243 lines) - Comment endpoints
├── chat_api.py         (500+ lines)- Chat endpoints
├── consumers.py        (300+ lines)- WebSocket handlers
└── services/
    └── auth_service.py (470 lines) - Email service
```

---

## Database Schema Visualization

```
User (Django)
  ├─ 1:1 → StudentProfile
  ├─ 1:M → Connection (as sender/receiver)
  ├─ 1:M → Message
  ├─ 1:M → Project (as owner)
  ├─ 1:M → Comment
  ├─ 1:M → Like
  ├─ 1:M → Activity
  ├─ 1:M → Follow (as follower/following)
  └─ 1:M → ChatRoomMember

Project
  ├─ 1:M → ProjectMember (team)
  ├─ 1:M → ProjectTask
  ├─ 1:M → ProjectMilestone
  ├─ 1:M → Comment
  ├─ 1:M → Like
  └─ 1:M → Activity

ChatRoom
  ├─ 1:M → Message
  └─ 1:M → ChatRoomMember

Message
  ├─ 1:M → MessageFile
  ├─ 1:M → MessageReaction
  └─ 1:M → MessageReadStatus
```

---

## Next Steps for Development

### High Priority
1. [ ] Add comprehensive API documentation (drf-spectacular)
2. [ ] Implement rate limiting (DRF throttling)
3. [ ] Add search functionality (Elasticsearch)
4. [ ] Set up monitoring (Sentry)

### Medium Priority
5. [ ] Implement Celery tasks for async operations
6. [ ] Add API caching layer
7. [ ] Implement GraphQL support
8. [ ] Add mobile app API versioning

### Low Priority
9. [ ] Add machine learning recommendations
10. [ ] Implement payment processing
11. [ ] Add video/voice calling
12. [ ] Build admin dashboard

---

## Summary Statistics

| Category | Count |
|----------|-------|
| Models | 25+ |
| Views | 100+ |
| API Endpoints | 64 |
| Forms | 8+ |
| Serializers | 10+ |
| Middleware | 8 |
| Email Templates | 6+ |
| Dependencies | 40+ |
| Database Tables | 25+ |
| Permissions Levels | 4 (role-based) |
| Authentication Methods | 3 |
| Feature Areas | 8 |

---

## Conclusion

UniSync is a **well-architected, feature-complete** student collaboration platform with:

✅ **Solid Foundation** - Clean Django structure with best practices  
✅ **Comprehensive Features** - 25+ models supporting 8 major features  
✅ **API-First Design** - RESTful architecture with 64 endpoints  
✅ **Real-time Capability** - WebSocket support for live messaging  
✅ **Security Focus** - CSRF, XSS, injection protections  
✅ **Scalability Ready** - Caching, async support, database optimization  
✅ **Production Deployable** - Render/Railway ready with proper config

The codebase is ready for **further enhancement** and **production deployment**.

---

**Document Version:** 1.0  
**Date:** February 6, 2026  
**Status:** Complete Analysis
