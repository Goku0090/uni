# UniSync Codebase - Comprehensive Analysis Report

**Date:** January 31, 2026  
**Project:** UniSync (Student Collaboration Platform)  
**Repository:** https://github.com/Goku0090/uni  
**Tech Stack:** Django 4.2.8 + REST Framework + PostgreSQL

---

## 1. PROJECT OVERVIEW

**UniSync** is a comprehensive student collaboration platform enabling:
- User authentication with OTP-based login
- Student profile management with social features
- Project posting and team management
- Real-time messaging with group chat support
- Notification system
- Activity feed and social connections

**Application Type:** Full-stack Django web application with REST API backend

---

## 2. ARCHITECTURE DIAGRAM

```
┌─────────────────────────────────────────────────────────────┐
│                    UniSync Frontend                          │
│              (Django Templates + Static JS)                 │
└────────────────────┬────────────────────────────────────────┘
                     │
        ┌────────────┼────────────┐
        │            │            │
   ┌────▼────┐  ┌───▼───┐  ┌────▼──────┐
   │  Views  │  │ API   │  │ Static    │
   │(HTML)   │  │(REST) │  │(CSS/JS)   │
   └────┬────┘  └───┬───┘  └───────────┘
        │           │
        └───────────┼──────────────────┐
                    │                  │
            ┌───────▼───────┐  ┌──────▼──────┐
            │ Django Apps   │  │ External    │
            │ (accounts)    │  │ Services    │
            └───────┬───────┘  └─────────────┘
                    │
        ┌───────────┼──────────────┐
        │           │              │
   ┌────▼────┐  ┌──▼────┐  ┌─────▼──┐
   │ Models  │  │Utils  │  │Services│
   │(DB)     │  │(Logic)│  │(Email) │
   └────┬────┘  └───────┘  └────────┘
        │
   ┌────▼──────────────────┐
   │   PostgreSQL/SQLite    │
   │   Database             │
   └───────────────────────┘
```

---

## 3. PROJECT STRUCTURE

```
auth_project/
├── auth_project/              # Project config
│   ├── settings.py           # Django settings (Database, Email, Auth)
│   ├── urls.py               # URL routing
│   ├── wsgi.py              # WSGI application
│   └── __init__.py
│
├── accounts/                 # Main Django app
│   ├── migrations/           # Database migrations
│   ├── models.py            # Database models (15+ models)
│   ├── views.py             # View functions (50+ views)
│   ├── chat_api.py          # REST API for messaging
│   ├── chat_api_improved.py # Enhanced messaging API
│   ├── serializers.py       # API serializers
│   ├── forms.py             # Django forms
│   ├── urls.py              # URL patterns
│   ├── utils.py             # Helper utilities
│   ├── permissions.py       # DRF permissions
│   │
│   ├── Email Backends:
│   │   ├── brevo_mail_backend.py    # Brevo email service
│   │   └── zepto_mail_backend.py    # ZeptoMail service
│   │
│   ├── templates/           # HTML templates
│   │   ├── accounts/        # App-specific templates
│   │   └── base.html       # Base template
│   │
│   ├── static/             # Static assets
│   │   ├── js/            # JavaScript files
│   │   ├── css/           # Stylesheets
│   │   └── images/        # Images/icons
│   │
│   ├── services/          # Business logic
│   └── tests.py          # Test cases
│
├── templates/             # Global templates
├── static/               # Global static files
├── media/                # User uploads
├── logs/                 # Application logs
├── manage.py            # Django CLI
└── requirements.txt     # Python dependencies
```

---

## 4. DATABASE MODELS (Core Data Structure)

### A. Authentication & User Management

**StudentProfile** (`accounts/models.py#L12-L53`)
- Extends Django User model
- Fields: full_name, college, interests, bio, profile_photo
- Skills, project_interests, role_preference
- Social links (GitHub, LinkedIn, Portfolio, Behance)
- Status: profile_completed flag

**OTP** (`accounts/models.py#L55-L124`)
- Email-based one-time passwords
- Purpose types: login, registration, password_reset
- Validation: 5-minute expiry, single-use enforcement
- Methods: `generate_otp()`, `verify_otp()`, `is_valid()`

### B. Social Features

**Connection** (`accounts/models.py#L126-L147`)
- Bidirectional user connections
- Status: pending, accepted, rejected
- Unique constraint on (sender, receiver)

**Follow** (`accounts/models.py#L463-L472`)
- Unidirectional following relationship
- For activity feed tracking

**Notification** (`accounts/models.py#L429-L450`)
- User notifications
- Types: connection_request, message, project_update
- Read status tracking

### C. Messaging System

**ChatRoom** (`accounts/models.py#L279-L310`)
- Types: direct (1:1), group (group chat), project (project-based)
- Members: through ChatRoomMember model
- Supports custom room naming and descriptions

**Message** (`accounts/models.py#L149-L217`)
- Supports text, file, image, call message types
- Threading: reply_to field for message threads
- Read status: via MessageReadStatus model
- Methods: `mark_as_read_by()`, `is_read_by()`, `get_read_by_users()`

**MessageReadStatus** (`accounts/models.py#L318-L336`)
- Scalable read status tracking
- Prevents duplicate read records (unique_together)

**MessageReaction** (`accounts/models.py#L230-L241`)
- Emoji/reaction support
- Unique constraint per (message, user, reaction)

### D. Project Management

**Project** (`accounts/models.py#L264-L277`)
- Fields: title, description, technologies, timeline
- Looking for: collaboration needs
- Categories and visibility settings
- Related: Owner, Members, Tasks, Milestones

**ProjectMember** (`accounts/models.py#L542-L580`)
- Roles: owner, admin, contributor, viewer
- Permission methods: `can_manage_project()`, `can_invite_members()`, `can_manage_tasks()`

**ProjectTask** (`accounts/models.py#L636-L677`)
- Status: todo, in_progress, review, completed, cancelled
- Priority: low, medium, high, urgent
- Assignment tracking: assigned_to, assigned_by

**ProjectMilestone** (`accounts/models.py#L680-L708`)
- Project timeline tracking
- Completion tracking with user attribution

**ProjectInvitation** (`accounts/models.py#L582-L634`)
- Invite users to projects
- Status: pending, accepted, declined, expired
- Methods: `accept()`, `decline()`

### E. Community & Engagement

**Comment** (`accounts/models.py#L450-L462`)
- Comments on projects
- Hierarchical structure for nested comments

**Like** (`accounts/models.py#L251-L263`)
- Project likes/reactions
- User attribution

**Activity** (`accounts/models.py#L475-L508`)
- Activity feed entries
- Types: profile_updated, project_created, connection_made, etc.

**UserStats** (`accounts/models.py#L510-L540`)
- Performance metrics
- Projects created, connections, likes received, followers
- Method: `update_stats()`

---

## 5. AUTHENTICATION FLOW

### OTP-Based Login Process

```
1. User visits /login/
2. Enters email → POST to login_view()
3. OTP generated via OTP.generate_otp()
4. Email sent via send_otp_email()
   - Supports: Brevo, ZeptoMail, Gmail, Console (dev)
5. User submits OTP code
6. Verification at verify_otp_view()
7. User authenticated and redirected to dashboard
```

### Email Backend Selection (settings.py#L234-L255)

Priority order:
1. **Brevo** (Production - Recommended)
   - Backend: `accounts.brevo_mail_backend.BrevoMailBackend`
   - Config: `BREVO_API_KEY`

2. **ZeptoMail** (Alternative)
   - Backend: `accounts.zepto_mail_backend.ZeptoMailBackend`
   - Config: `ZEPTO_MAIL_API_KEY`, `ZEPTO_MAIL_TOKEN`

3. **Gmail SMTP** (Fallback)
   - Backend: Django's SMTP
   - Config: `EMAIL_HOST_USER`, `EMAIL_HOST_PASSWORD`

4. **Console** (Development)
   - Prints OTP to console

---

## 6. KEY VIEWS & ENDPOINTS

### Authentication Views (accounts/views.py)

| View | URL | Purpose |
|------|-----|---------|
| `login_view()` | `/login/` | Login page with OTP request |
| `register_view()` | `/register/` | User registration |
| `verify_otp_view()` | `/verify-otp/<purpose>/` | OTP verification |
| `logout_view()` | `/logout/` | User logout |
| `forgot_password_view()` | `/forgot-password/` | Password reset request |
| `reset_password_view()` | `/reset-password/` | Password reset form |

### Profile & Social Views

| View | URL | Purpose |
|------|-----|---------|
| `student_profile()` | `/student-profile/` | View own profile |
| `user_profile()` | `/user/<username>/` | View other user's profile |
| `edit_profile()` | `/edit-profile/` | Edit profile and upload avatar |
| `connect_view()` | `/connect/<user_id>/` | Send connection request |
| `accept_connection()` | `/accept-connection/<id>/` | Accept connection |
| `follow_user()` | `/follow/<user_id>/` | Follow user |

### Project Management

| View | URL | Purpose |
|------|-----|---------|
| `post_project()` | `/post-project/` | Create new project |
| `project_detail()` | `/project-detail/<id>/` | View project |
| `edit_project()` | `/edit-project/<id>/` | Edit project |
| `delete_project()` | `/delete-project/<id>/` | Delete project |
| `like_project()` | `/like-project/<id>/` | Like project |
| `find_collaborators()` | `/find-collaborators/` | Search for team members |

### Messaging Views

| View | URL | Purpose |
|------|-----|---------|
| `message_view()` | `/messages/` | Direct message list |
| `chat_view()` | `/chat/<user_id>/` | Direct message conversation |
| `enhanced_messages_view()` | `/enhanced-messages/` | Group messaging interface |
| `enhanced_chat_view()` | `/enhanced-chat/<room_id>/` | Group chat room |
| `create_group_chat()` | `/create-group-chat/` | Create group chat |

### Dashboard & Feed

| View | URL | Purpose |
|------|-----|---------|
| `dashboard_view()` | `/dashboard/` | User dashboard |
| `activity_feed()` | `/activity-feed/` | Activity feed |
| `notifications_view()` | `/notifications/` | Notifications |
| `main()` | `/` | Home page |

---

## 7. REST API ENDPOINTS

### Chat API (accounts/chat_api.py)

**Chat Rooms**
```
GET/POST   /chat-rooms/              - List/create chat rooms
GET/PUT    /chat-rooms/<id>/          - Get/update chat room
GET        /chat-rooms/<id>/members/  - Get room members
POST       /direct-message/           - Start direct conversation
```

**Messages**
```
GET/POST   /messages/                - List/create messages
GET        /messages/<id>/           - Get message
DELETE     /messages/<id>/           - Delete message
GET        /messages/search/         - Search messages
GET/POST   /messages/<id>/status/    - Message read status
GET/POST   /messages/<id>/reactions/ - Message reactions
```

**Additional Endpoints**
```
GET/POST   /drafts/                  - Draft messages
POST       /typing/                  - Typing indicator
GET        /conversations/           - List conversations
```

### User & Profile APIs

```
GET        /user-profile/<id>/       - Get user profile
GET/POST   /profile/                 - Current user profile (REST)
GET        /user-stats/              - User statistics
GET        /college-search/          - Search colleges (RapidAPI)
POST       /validate-college/        - Validate college
```

### Search & NLP

```
GET        /nlp-analyze/             - NLP analysis of project text
GET        /check-username/          - Username availability check
GET        /check-email/             - Email availability check
```

---

## 8. DEPENDENCIES & EXTERNAL SERVICES

### Core Django Stack
- **Django 4.2.8** - Web framework
- **Django REST Framework 3.14.0** - API development
- **django-allauth 0.61.1** - Social authentication (Google, GitHub)

### Database
- **PostgreSQL** (Production) via `psycopg2-binary`
- **SQLite** (Development fallback)
- **dj-database-url** - Parse DATABASE_URL

### Email Services
- **Brevo API** - Primary transactional email
- **ZeptoMail** - Alternative email service
- **Gmail SMTP** - Fallback SMTP

### Real-Time & Messaging
- **Channels 4.0.0** - WebSockets support
- **Channels-Redis** - Channel layer

### Cache & Sessions
- **Redis** - Caching and session storage
- **django-redis** - Redis backend for Django

### File & Media
- **Pillow** - Image processing
- **boto3 + django-storages** - S3 file storage
- **WhiteNoise** - Static file serving

### Data & NLP
- **NLTK** - Natural language processing
- **Pandas** - Data analysis
- **openpyxl** - Excel file handling

### Background Jobs
- **Celery** - Task queue
- **RabbitMQ/Redis** - Message broker

### Monitoring & Logging
- **Sentry** - Error tracking
- **Python logging** - Built-in logging

### Development & Testing
- **Pytest + pytest-django** - Testing framework
- **Selenium** - Browser automation
- **Django Debug Toolbar** - Development debugging
- **Black, Flake8, isort, mypy** - Code quality

---

## 9. SETTINGS CONFIGURATION (settings.py)

### Database Configuration
```python
# Production: PostgreSQL via DATABASE_URL
# Development: SQLite fallback or local PostgreSQL

DATABASE_URL = os.getenv('DATABASE_URL')
if DATABASE_URL:
    DATABASES = {'default': dj_database_url.parse(DATABASE_URL)}
else:
    DATABASES = {'default': {'ENGINE': 'django.db.backends.sqlite3'}}
```

### Security Settings
- `DEBUG = False` in production
- `SECURE_SSL_REDIRECT = True` in production
- `SESSION_COOKIE_SECURE = True` in production
- `CSRF_COOKIE_SECURE = True` in production
- CSRF middleware enabled for form protection

### Authentication Backends
- Django default: `django.contrib.auth.backends.ModelBackend`
- Allauth: `allauth.account.auth_backends.AuthenticationBackend`

### Installed Apps
```python
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.sites',
    'django.contrib.humanize',
    'accounts',
    'allauth',
    'allauth.account',
    'allauth.socialaccount',
    'allauth.socialaccount.providers.google',
    'allauth.socialaccount.providers.github',
    'rest_framework',
]
```

### Redirects
- `LOGIN_REDIRECT_URL = '/dashboard/'`
- `LOGOUT_REDIRECT_URL = '/login/'`

### REST Framework Config
```python
REST_FRAMEWORK = {
    'DEFAULT_PERMISSION_CLASSES': ['rest_framework.permissions.AllowAny'],
    'DEFAULT_AUTHENTICATION_CLASSES': ['rest_framework.authentication.SessionAuthentication'],
    'DEFAULT_PAGINATION_CLASS': 'rest_framework.pagination.PageNumberPagination',
    'PAGE_SIZE': 10,
}
```

---

## 10. FORMS & VALIDATION (accounts/forms.py)

**Built-in Forms:**
- `LoginForm` - Login with email
- `RegisterForm` - User registration
- `OTPVerificationForm` - OTP validation
- `StudentProfileForm` - Profile editing
- `ProjectForm` - Project creation/editing
- `CustomSocialSignupForm` - Social auth signup

**Validation Features:**
- Email format validation
- Username uniqueness check
- Password strength validation
- File extension validation for avatars (JPG, PNG, GIF)

---

## 11. UTILITY FUNCTIONS (accounts/utils.py)

### ProjectVisibilityFilter
- Filters projects based on:
  - User ownership
  - Public/private visibility
  - Collaboration type
  - Category matching
  - Skill requirements

### StudentProfileNLP
- Analyzes project descriptions
- Extracts skills and technologies
- Suggests collaborators based on NLP

### Cache Utilities
- Project listing caching
- User profile caching
- Feed caching with TTL

---

## 12. SERIALIZERS (REST API)

**UserProfileSerializer**
- Serializes StudentProfile with User data
- Exports: username, email, college, interests, skills, social links

**ProjectSerializer**
- Project data with owner information
- Aggregates likes_count and comments_count

**MessageSerializer**
- Message content, sender, creation time
- Reaction aggregation

**ConnectionSerializer & NotificationSerializer**
- Connection status and metadata
- Notification types and read status

---

## 13. PERMISSION CLASSES (accounts/permissions.py)

- Custom permission classes for:
  - Project ownership verification
  - Team member access control
  - Message recipient verification
  - Profile ownership confirmation

---

## 14. STATIC FILES & TEMPLATES

### Frontend Assets
- **CSS Frameworks:** Bootstrap (likely)
- **JavaScript:** Vanilla JS or jQuery
- **Templates:** Django templates in `accounts/templates/`

### Key Templates
- Base template with navigation
- Login/Register pages
- Dashboard
- Profile management
- Project posting/viewing
- Messaging interface
- Activity feed

---

## 15. LOGGING SYSTEM

**Log Handlers:**
- Console output
- Rotating file handler (10 MB limit)
- Error log file (separate)

**Log Levels:**
- Django: INFO
- Accounts app: DEBUG (dev) / INFO (prod)

**Log Location:** `logs/django.log` and `logs/error.log`

---

## 16. TESTING STRUCTURE

**Test Files:**
- `test_login.py` - Login flow testing
- `test_email.py` - Email backend testing
- `test_profile_view.py` - Profile view testing
- `test_filter.py` - Project filtering
- `test_connections.py` - Connection management
- Other test files for specific features

**Testing Tools:**
- Pytest + pytest-django
- Django TestCase
- API testing via REST client

---

## 17. DEPLOYMENT CONFIGURATION

### Render Deployment (render.yaml)
- Auto-deploys from GitHub
- Configured for PostgreSQL on Render
- Uses environment variables for configuration

### Environment Variables Required
```
DEBUG=False
SECRET_KEY=<secure-key>
ALLOWED_HOSTS=<domain>
DATABASE_URL=<render-postgres-url>
BREVO_API_KEY=<email-api-key>
DEFAULT_FROM_EMAIL=<sender-email>
GOOGLE_CLIENT_ID=<google-oauth-id>
GOOGLE_CLIENT_SECRET=<google-oauth-secret>
GITHUB_CLIENT_ID=<github-oauth-id>
GITHUB_CLIENT_SECRET=<github-oauth-secret>
RAPIDAPI_KEY=<rapidapi-key>
```

---

## 18. SECURITY FEATURES

### Authentication
- OTP-based multi-step verification
- Session-based authentication
- Social login (Google, GitHub)

### Protection
- CSRF token validation
- SQL injection prevention (ORM usage)
- XSS protection via template escaping
- Input sanitization in views
- Password hashing with Django's built-in validators

### Data Security
- File extension validation
- Secure file uploads to media/
- S3 file storage option

---

## 19. PERFORMANCE OPTIMIZATIONS

### Caching
- Cache framework with Redis
- Page-level caching
- Object-level caching

### Database
- Connection pooling (conn_max_age=600)
- Query optimization via select_related, prefetch_related
- Pagination for large datasets

### Static Files
- WhiteNoise for efficient serving
- S3 storage for scalability
- CSS/JS minification ready

---

## 20. CODE QUALITY

### Tools
- **Black** - Code formatting
- **Flake8** - Linting
- **isort** - Import sorting
- **mypy** - Type checking

### Best Practices
- Docstrings on major functions
- Decorator for error handling
- Input sanitization
- Organized code structure
- Separation of concerns (models, views, serializers)

---

## 21. EXTENSIBILITY & SCALABILITY

### Future-Ready Features
- **Celery integration** - Async task processing
- **Channels** - Real-time WebSocket support
- **S3/Cloud storage** - Scalable file handling
- **Redis caching** - Performance at scale
- **Sentry monitoring** - Error tracking in production

### Modular Architecture
- Apps separated by functionality
- Reusable serializers and permissions
- Service layer for business logic
- Utility functions for shared operations

---

## 22. WORKFLOW DIAGRAMS

### Authentication Flow
```
[User] → [Login Page] → [Enter Email] → [OTP Generated]
  ↓
[Email Backend Selected] → [Send via Brevo/ZeptoMail/SMTP]
  ↓
[User Receives OTP] → [Enters OTP Code] → [Verify OTP]
  ↓
[Create Django Session] → [Login] → [Redirect to Dashboard]
```

### Message Flow
```
[User1] → [Compose Message] → [Create Message Record]
  ↓
[Store in ChatRoom] → [Mark as Unread] → [Notification Created]
  ↓
[User2 Receives] → [Read Message] → [MessageReadStatus Created]
  ↓
[Activity Updated] → [Feed Refreshed]
```

### Project Posting Flow
```
[User] → [Post Project Form] → [Validate Input]
  ↓
[Create Project Record] → [Create ProjectMember (Owner)]
  ↓
[Create Activity Entry] → [Notify Followers] → [Add to Feed]
  ↓
[Project Visible to Others] → [Can Like/Comment] → [Receive Requests]
```

---

## 23. CRITICAL FILES & THEIR ROLES

| File | Lines | Purpose |
|------|-------|---------|
| `settings.py` | 356 | Django configuration, DB, email, security |
| `models.py` | 718 | 15+ database models with relationships |
| `views.py` | 3311 | 50+ view functions for all features |
| `urls.py` | 120 | URL routing (web + REST API) |
| `chat_api.py` | ? | REST endpoints for messaging |
| `serializers.py` | 106 | API data serialization |
| `forms.py` | ? | Django form classes |
| `utils.py` | ? | Helper functions (NLP, filtering) |

---

## 24. KNOWN INTEGRATION POINTS

### External Services
1. **Email:** Brevo API, ZeptoMail, Gmail SMTP
2. **Social Auth:** Google OAuth 2.0, GitHub OAuth
3. **College Database:** RapidAPI (universities-list)
4. **Error Tracking:** Sentry
5. **File Storage:** AWS S3 (optional)

### Internal Integrations
- Django signals for activity creation
- ORM relationships for data querying
- REST API for frontend communication
- WebSocket support for real-time features

---

## 25. SUMMARY

**UniSync** is a **production-ready, feature-rich student collaboration platform** with:

✅ **Robust authentication** - OTP-based login with multiple email backends  
✅ **Comprehensive data models** - 18+ interconnected models  
✅ **Full REST API** - DRF-based messaging and user APIs  
✅ **Real-time support** - Django Channels + Redis integration  
✅ **Scalable architecture** - Celery, caching, cloud storage ready  
✅ **Security-first design** - CSRF, XSS, SQL injection protections  
✅ **Professional monitoring** - Logging, Sentry, performance tracking  
✅ **Social features** - Connections, follows, notifications, activity feed  
✅ **Project management** - Tasks, milestones, team roles, invitations  
✅ **Flexible deployment** - Render-ready with environment configuration  

The codebase is well-structured, maintainable, and ready for production deployment.

---

**End of Analysis**
