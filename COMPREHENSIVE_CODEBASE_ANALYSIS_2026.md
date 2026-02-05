# UniSync - Comprehensive Codebase Analysis

## Project Overview
**Project Name**: UniSync  
**Type**: Full-stack Django + Frontend Collaboration Platform  
**Repository**: https://github.com/Goku0090/uni  
**Primary Purpose**: A student collaboration platform that helps users find collaborators, create projects, manage teams, communicate, and build together.

---

## Architecture Overview

```
┌─────────────────────────────────────────────────────────────┐
│                    UniSync Platform                          │
├─────────────────────────────────────────────────────────────┤
│                                                               │
│  ┌──────────────────┐  ┌──────────────────┐                 │
│  │   Frontend       │  │   Backend        │                 │
│  │   (Templates)    │  │   (Django)       │                 │
│  └──────────────────┘  └──────────────────┘                 │
│                             │                                 │
│        ┌────────────────────┼────────────────────┐           │
│        │                    │                    │           │
│    ┌───▼────────┐    ┌─────▼────────┐  ┌────────▼──┐       │
│    │  Auth      │    │   Projects   │  │ Messaging │       │
│    │  System    │    │   & Feed     │  │  System   │       │
│    └────────────┘    └──────────────┘  └───────────┘       │
│                                                               │
│  ┌─────────────────────────────────────────────────────────┐│
│  │         Database Layer (PostgreSQL/SQLite)               ││
│  │  - Users & Profiles  - Projects - Comments               ││
│  │  - Connections       - Messages - Activities             ││
│  │  - Tasks & Milestones                                    ││
│  └─────────────────────────────────────────────────────────┘│
│                                                               │
└─────────────────────────────────────────────────────────────┘
```

---

## Directory Structure

### Root Level
```
e:/login/auth_project/
├── auth_project/              # Django project settings
│   ├── settings.py           # Configuration, email, databases, apps
│   ├── urls.py               # URL routing
│   ├── wsgi.py               # WSGI application
│   └── asgi.py               # ASGI application
│
├── accounts/                  # Main Django app
│   ├── models.py             # Database models
│   ├── views.py              # View logic (1500+ lines)
│   ├── urls.py               # App URL patterns
│   ├── forms.py              # User forms
│   ├── serializers.py        # DRF serializers
│   ├── permissions.py        # Custom permissions
│   ├── comment_api.py        # Comments API
│   ├── chat_api.py           # Messaging API
│   ├── utils.py              # Utility functions
│   │
│   ├── services/             # Business logic
│   │   └── notification_service.py
│   │
│   ├── templates/            # HTML templates
│   │   ├── base.html
│   │   ├── login.html
│   │   ├── register.html
│   │   ├── dashboard.html
│   │   ├── project_detail.html
│   │   ├── find_collaborators.html
│   │   └── ... (many more)
│   │
│   ├── static/               # CSS, JS, images
│   │   ├── css/
│   │   ├── js/
│   │   └── images/
│   │
│   ├── migrations/           # Database migrations
│   └── templatetags/         # Custom template tags
│
├── media/                     # User uploads (profile photos, files)
├── static/                    # Project-wide static files
├── logs/                      # Application logs
│
├── manage.py                 # Django management script
├── requirements.txt          # Python dependencies
├── .env                      # Environment variables
├── db.sqlite3                # Development database
└── Procfile                  # Deployment configuration
```

---

## Core Models (Database Schema)

### 1. User & Profile Models
```python
# User (Django built-in with extensions)
├── StudentProfile
│   ├── full_name
│   ├── college, location
│   ├── interests (JSON array)
│   ├── bio, skills (JSON array)
│   ├── profile_photo (image upload)
│   ├── social_links (GitHub, LinkedIn, Portfolio, Behance)
│   └── profile_completed (boolean)
│
└── UserStatus
    └── (Online/offline tracking)
```

### 2. Connection & Social Models
```python
Connection
├── sender, receiver (ForeignKey to User)
├── status (pending, accepted, rejected)
└── created_at, updated_at

Follow
├── follower, following
└── created_at

Notification
├── user, related_user
├── notification_type
├── is_read, created_at
└── project/connection/message (optional relations)
```

### 3. Project Models
```python
Project
├── user (owner)
├── title, description, category
├── technologies, looking_for
├── timeline, collaboration_needs
├── github_link, project_link
├── visibility (private/public)
├── created_at, updated_at
└── members (through ProjectMember)

ProjectMember
├── project, user
├── role (owner, admin, contributor, viewer)
├── is_active, joined_at

ProjectTask
├── project, assigned_to
├── title, description
├── status (todo, in_progress, review, completed)
├── priority (low, medium, high, urgent)
├── due_date, completed_at

ProjectMilestone
├── project
├── title, description
├── due_date, is_completed
└── completed_by, completed_at

ProjectInvitation
├── project, invited_user, invited_by
├── role, message
├── status (pending, accepted, declined, expired)
```

### 4. Messaging & Comments
```python
ChatRoom
├── name, chat_type (direct/group)
├── members (through ChatRoomMember)
└── created_at, updated_at

Message
├── sender, receiver (null for group chats)
├── chat_room (for group messages)
├── content, message_type (text, file, image, call)
├── reply_to (threading)
└── created_at, updated_at

MessageReadStatus
├── message, user
├── read_at

Comment
├── user, project
├── content, parent (for threading)
├── is_approved, created_at
└── updated_at
```

### 5. Activity & Stats Models
```python
Activity
├── user, activity_type
├── title, description
├── related_user, project, connection
├── is_public, created_at

Like
├── user, project
└── created_at

UserStats
├── user
├── projects_created, connections_made
├── likes_received, comments_made
├── followers_count, following_count
└── last_updated

OTP
├── email, otp_code
├── purpose (login, registration, reset)
├── is_used, created_at, expires_at
└── validation methods
```

---

## Key Features & Implementation

### 1. Authentication System
**Location**: `accounts/views.py` + `accounts/forms.py`

**Features**:
- ✅ OTP-based email authentication
- ✅ Traditional username/password login
- ✅ Social login (Google OAuth, GitHub OAuth)
- ✅ Email verification
- ✅ Password reset with OTP

**Email Backends**:
- Primary: Brevo (transactional email)
- Fallback 1: ZeptoMail
- Fallback 2: Gmail SMTP
- Development: Console backend

**Key Views**:
```python
- register_view()          # Registration with validation
- login_view()             # Login with OTP or password
- generate_otp()           # OTP generation
- verify_otp()             # OTP verification
- password_reset()         # Password reset flow
- logout_view()            # Logout handler
```

### 2. Project Management System
**Location**: `accounts/views.py` (project_detail, post_project, edit_project)

**Features**:
- ✅ Project creation with metadata (tech stack, collaboration needs)
- ✅ Project visibility control (public/private/hidden)
- ✅ Project filtering by:
  - Category, technology, timeline
  - Collaboration needs
  - Visibility status
- ✅ Team management with roles
- ✅ Project invitations
- ✅ Task management
- ✅ Milestone tracking
- ✅ Project likes

**Key Views**:
```python
- project_detail()         # View project with comments & team
- post_project()           # Create new project
- edit_project()           # Edit project info
- delete_project()         # Delete project
- like_project()           # Toggle like
- get_projects_feed()      # Paginated project feed
```

### 3. Collaboration Features
**Location**: `accounts/views.py` + `comment_api.py` + `chat_api.py`

**Features**:
- ✅ Find Collaborators page with search/filter
- ✅ Connection requests (send/accept/reject)
- ✅ User follow system
- ✅ Direct messaging
- ✅ Group chat support
- ✅ Message threading/replies
- ✅ File attachments
- ✅ Message read status
- ✅ Message reactions/emojis

**Key Functions**:
```python
- find_collaborators()     # Search with filtering
- send_connection()        # Create connection request
- accept_connection()      # Accept connection
- send_message()           # Send direct message
- post_comment()           # Comment on project
```

### 4. Notification System
**Location**: `accounts/models.py` + `services/notification_service.py`

**Features**:
- ✅ Real-time notifications for:
  - Connection requests
  - Project comments
  - Project likes
  - New messages
  - Profile follows
- ✅ Notification badge counts
- ✅ Mark as read functionality
- ✅ Activity feed

### 5. User Profile System
**Location**: `accounts/views.py` + templates

**Features**:
- ✅ Extended StudentProfile model
- ✅ Profile photo upload
- ✅ Bio, interests, skills
- ✅ Social links (GitHub, LinkedIn, Portfolio, Behance)
- ✅ Public profile viewing
- ✅ Profile completion tracking

---

## Key Technologies & Configuration

### Backend Stack
```
Framework: Django 3.x/4.x
API: Django REST Framework (DRF)
Authentication: django-allauth (OAuth support)
Database: PostgreSQL (production) / SQLite (development)
Logging: Python logging with rotating file handlers
Email: Multiple backends (Brevo, ZeptoMail, Gmail SMTP)
```

### Frontend Stack
```
Template Engine: Django Templates
CSS Framework: Bootstrap/Tailwind (inferred from HTML)
JavaScript: Vanilla JS + jQuery (inferred)
File Upload: Django media handling
```

### Key Dependencies (from settings.py)
```python
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'accounts',
    'rest_framework',
    'allauth',
    'allauth.account',
    'allauth.socialaccount',
    'allauth.socialaccount.providers.google',
    'allauth.socialaccount.providers.github',
]
```

---

## API Endpoints & Routes

### Authentication
```
POST   /api/register/              Register new user
POST   /api/login/                 Login with OTP/password
POST   /api/generate-otp/          Generate OTP
POST   /api/verify-otp/            Verify OTP
POST   /api/logout/                Logout
POST   /api/password-reset/        Initiate password reset
```

### Projects
```
GET    /projects/                  Project feed (paginated)
POST   /projects/create/           Create new project
GET    /projects/<id>/             Project detail
POST   /projects/<id>/update/      Update project
DELETE /projects/<id>/delete/      Delete project
POST   /projects/<id>/like/        Toggle like
GET    /projects/<id>/comments/    Get comments
POST   /projects/<id>/comment/     Post comment
```

### Collaborators
```
GET    /find-collaborators/        Search collaborators with filters
POST   /connection/send/           Send connection request
POST   /connection/<id>/accept/    Accept connection
POST   /connection/<id>/reject/    Reject connection
```

### Messaging
```
GET    /messages/                  Message history
POST   /messages/send/             Send message
GET    /messages/<room>/           Chat room messages
POST   /messages/<room>/send/      Send group message
POST   /messages/<id>/read/        Mark message as read
```

### Profile
```
GET    /profile/<username>/        View user profile
POST   /profile/edit/              Edit own profile
GET    /profile/stats/             User statistics
POST   /profile/follow/            Follow user
```

---

## Configuration & Environment

### Database Configuration
```python
# Production (Render)
DATABASE_URL = postgres://...  (auto-parsed)

# Development
DB_ENGINE: postgresql
DB_NAME: unisync_db
DB_USER: unisync_user
DB_PASSWORD: ***
DB_HOST: localhost
DB_PORT: 5432

# Fallback
SQLite for development if PostgreSQL not configured
```

### Email Configuration
```python
# Priority order:
1. BREVO_API_KEY             (Recommended - transactional)
2. ZEPTO_MAIL_API_KEY        (Alternative)
3. EMAIL_HOST_USER/PASSWORD  (Gmail SMTP fallback)
4. Console backend           (Development)

Default sender: noreply@unisync.app
```

### Security Settings
```python
SECURE_SSL_REDIRECT: False (configurable)
SESSION_COOKIE_SECURE: False (configurable)
CSRF_COOKIE_SECURE: False (configurable)
SECRET_KEY: Generated or from .env
ALLOWED_HOSTS: localhost,127.0.0.1 (configurable)
```

### Social OAuth Providers
```python
Google OAuth:
  - GOOGLE_CLIENT_ID
  - GOOGLE_CLIENT_SECRET
  
GitHub OAuth:
  - GITHUB_CLIENT_ID
  - GITHUB_CLIENT_SECRET
```

---

## Data Flow Diagrams

### User Registration & OTP Flow
```
┌──────────────┐
│ User inputs  │
│ credentials  │
└────────┬─────┘
         │
         ▼
┌─────────────────────────┐
│ Validation              │
│ - Password strength     │
│ - Email uniqueness      │
│ - Username uniqueness   │
└────────┬────────────────┘
         │
         ▼
┌─────────────────────────┐
│ Create User & Profile   │
└────────┬────────────────┘
         │
         ▼
┌─────────────────────────┐
│ Generate & Send OTP     │
│ (via Brevo/ZeptoMail)   │
└────────┬────────────────┘
         │
         ▼
┌─────────────────────────┐
│ User Verification Page  │
└────────┬────────────────┘
         │
         ▼
┌─────────────────────────┐
│ Verify OTP              │
│ - Check expiry (5 min)  │
│ - Mark as used          │
└────────┬────────────────┘
         │
         ▼
┌─────────────────────────┐
│ Account Activated       │
│ Redirect to Dashboard   │
└─────────────────────────┘
```

### Project Creation & Discovery Flow
```
┌──────────────────────┐
│ User Creates Project │
└──────────┬───────────┘
           │
           ▼
┌──────────────────────────┐
│ Project Model Created    │
│ - Assign owner           │
│ - Set visibility         │
│ - Store metadata         │
└──────────┬───────────────┘
           │
           ▼
┌──────────────────────────┐
│ Create Activity Entry    │
│ (for feed)               │
└──────────┬───────────────┘
           │
           ▼
┌──────────────────────────┐
│ Update ProjectTeam       │
│ (add owner as member)    │
└──────────┬───────────────┘
           │
           ▼
┌──────────────────────────┐
│ Visible in:              │
│ - Home feed              │
│ - Search results         │
│ - Filtered views         │
└──────────────────────────┘
```

### Messaging Flow
```
┌─────────────┐
│ User A      │
│ Types msg   │
└──────┬──────┘
       │
       ▼
┌─────────────────────┐
│ Send Message        │
│ - Create Message    │
│ - Link to receiver  │
│ - Set timestamp     │
└──────┬──────────────┘
       │
       ▼
┌─────────────────────┐
│ Notify User B       │
│ - Create badge      │
│ - Send email (opt)  │
└──────┬──────────────┘
       │
       ▼
┌─────────────────────┐
│ User B receives     │
│ - Views message     │
│ - Mark as read      │
└──────┬──────────────┘
       │
       ▼
┌─────────────────────┐
│ Send read receipt   │
│ (to User A)         │
└─────────────────────┘
```

---

## Performance Considerations

### Database Optimizations
1. **select_related()**: Used in project_detail for user profile fetching
2. **Pagination**: Projects & comments paginated (10-20 per page)
3. **Caching**: Available via Django cache framework
4. **Indexing**: Primary keys, foreign keys (auto-indexed)

### Query Patterns
```python
# Project list with related data
Project.objects.select_related('user__student_profile')

# Comments with user info
Comment.objects.select_related('user__student_profile')

# Filtered queries
projects = Project.objects.filter(visibility='public')
```

### Potential Bottlenecks
- Large user datasets in find_collaborators view
- Comment loading on project detail page
- Real-time notification counting
- File upload processing

---

## Security Features

### Input Validation
```python
- sanitize_input()       # Remove XSS threats
- Password validators    # Strength requirements
- Email verification     # Confirm email ownership
- File validators        # Image file extensions only
```

### CSRF Protection
```python
CSRF_COOKIE_SECURE = True (for HTTPS)
CSRF middleware enabled
```

### Authentication
```python
- OTP expiry (5 minutes)
- Password hashing (Django built-in)
- Session management
- OAuth token validation
```

### Permissions
```python
- @login_required on views
- User ownership checks
- Project member role validation
```

---

## Known Issues & Areas for Improvement

### Current Status (from documentation)
✅ Authentication system working
✅ OTP-based login functional
✅ Project creation & management
✅ Comments system (recently fixed)
✅ Find collaborators feature
✅ Messaging system
✅ Profile viewing
✅ Notifications

### Areas for Enhancement
- Real-time updates (WebSocket for live chat)
- Activity feed optimization
- Search performance at scale
- Mobile responsiveness
- Dark mode support
- Two-factor authentication
- Rate limiting on API endpoints
- Advanced analytics

---

## Deployment Configuration

### Deployment Files
- **Procfile**: For Render/Heroku deployment
- **render.yaml**: Render-specific configuration
- **railway.json**: Railway deployment config
- **requirements.txt**: Python dependencies

### Environment Variables Required
```bash
SECRET_KEY=<your-secret-key>
DEBUG=False (for production)
ALLOWED_HOSTS=yourdomain.com
DATABASE_URL=postgresql://...
BREVO_API_KEY=<api-key>
GOOGLE_CLIENT_ID=<oauth-id>
GOOGLE_CLIENT_SECRET=<oauth-secret>
DEBUG=True (for development)
```

---

## Testing

### Test Files Present
- test_login.py
- test_email.py
- test_profile_view.py
- test_filter.py
- test_comments_api.py
- test_zeptomail.py

### Testing Recommendations
- Unit tests for models
- Integration tests for API endpoints
- Form validation tests
- Permission tests

---

## Summary

UniSync is a **fully-featured collaboration platform** built with Django that enables students to:

1. **Find collaborators** through intelligent search and filtering
2. **Create & manage projects** with team members and roles
3. **Communicate** via direct messaging and project comments
4. **Collaborate** on tasks and milestones
5. **Build networks** through connections and follows
6. **Stay engaged** with activity feeds and notifications

The codebase demonstrates:
- ✅ Proper separation of concerns (models, views, serializers)
- ✅ Django best practices (login_required, get_object_or_404)
- ✅ Scalable data models with proper relationships
- ✅ Multiple authentication methods
- ✅ API-first design with DRF
- ✅ Comprehensive logging and error handling
- ✅ Environment-based configuration

The platform is production-ready and currently deployed on Render/Railway with PostgreSQL backing.
