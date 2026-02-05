# UniSync - Complete Codebase Analysis 2026

## 1. PROJECT OVERVIEW

**Project Name**: UniSync (also called auth_project)  
**Repository**: https://github.com/Goku0090/uni  
**Tech Stack**: Django + PostgreSQL + REST API + WebSockets  
**Type**: Full-stack collaborative learning platform for university students  

### Core Purpose
UniSync is a collaborative learning platform that connects students to find collaborators, share projects, and manage team-based work.

---

## 2. TECHNOLOGY STACK

### Backend
- **Framework**: Django 4.2.8
- **REST API**: Django REST Framework (DRF) 3.14.0
- **Authentication**: django-allauth 0.61.1 (social login: Google, GitHub)
- **Database**: PostgreSQL (psycopg2-binary)
- **Real-time**: Channels 4.0.0 + Channels-Redis 4.1.0 (WebSockets)
- **Task Queue**: Celery 5.3.4
- **Caching**: Redis 5.0.1 + django-redis 5.4.0
- **Email**: ZeptoMail (zeptomail==1.0.0)

### Frontend
- **Templates**: Django Templates (HTML/CSS/JavaScript)
- **File Storage**: AWS S3 compatible (django-storages + boto3)

### Infrastructure
- **Production Server**: Gunicorn 21.2.0
- **Static Files**: WhiteNoise 6.6.0
- **Monitoring**: Sentry 1.38.0
- **Deployment**: Render/Railway ready (Procfile + docker support)

### Development Tools
- **Code Quality**: Black, Flake8, isort, mypy
- **Testing**: pytest, pytest-django, Selenium
- **Documentation**: Sphinx + RTD theme
- **API Docs**: drf-spectacular 0.26.5

---

## 3. PROJECT STRUCTURE

```
auth_project/
├── auth_project/                    # Django project configuration
│   ├── settings.py                  # Settings (database, apps, middleware)
│   ├── urls.py                      # Root URL routing
│   ├── wsgi.py                      # WSGI application
│   └── asgi.py                      # ASGI (WebSockets)
│
├── accounts/                        # Main application
│   ├── models.py                    # Database models (16 models)
│   ├── views.py                     # Main views (3311+ lines)
│   ├── views_contact.py             # Contact/privacy pages
│   ├── urls.py                      # URL routing (129 paths)
│   ├── serializers.py               # REST API serializers
│   ├── forms.py                     # Django forms
│   ├── permissions.py               # REST API permissions
│   ├── utils.py                     # Utility functions (NLP, filtering)
│   │
│   ├── chat_api.py                  # Chat API (wrapper)
│   ├── chat_api_improved.py         # Chat API implementation
│   ├── comment_api.py               # Comments system
│   │
│   ├── services/
│   │   └── auth_service.py          # Authentication utilities
│   │
│   ├── zepto_mail_backend.py        # ZeptoMail integration
│   ├── brevo_mail_backend.py        # Brevo email fallback
│   │
│   ├── migrations/                  # Database migrations
│   ├── templates/                   # HTML templates (50+ files)
│   ├── static/                      # CSS, JS, images
│   └── templatetags/                # Custom template tags
│
├── manage.py                        # Django management
├── requirements.txt                 # Python dependencies
├── .env                            # Environment variables
└── [test files]                    # Various test scripts
```

---

## 4. DATABASE MODELS (Django ORM)

### Core Models

#### 1. **StudentProfile** - Extended User Profile
```python
Fields:
- user (OneToOne with User)
- full_name, college, location
- bio, interests, skills, project_interests
- profile_photo (ImageField)
- social_links (github, linkedin, portfolio, behance)
- profile_completed (boolean)
- timestamps (created_at, updated_at)
```

#### 2. **Project** - User Projects/Ideas
```python
Key Fields:
- owner (ForeignKey User)
- title, description, technologies
- category, timeline
- collaboration_needs, looking_for
- github_link, visibility
- likes, comments (relationships)
- timestamps
```

#### 3. **Message & Chat System**
```python
Message:
- sender, receiver (ForeignKey User)
- chat_room (group chats)
- content, message_type
- reply_to (threading)
- read status tracking

ChatRoom:
- name, description
- chat_type (direct/group)
- members (ManyToMany)
- is_active

MessageReadStatus:
- tracks which users read specific messages
- solves scalability issue of read field

MessageReaction:
- emoji reactions to messages
```

#### 4. **Connection System**
```python
Connection:
- sender, receiver (User)
- status (pending/accepted/rejected)
- tracks collaboration requests
```

#### 5. **Project Collaboration**
```python
ProjectMember:
- project, user, role
- roles: owner, admin, contributor, viewer
- permissions based on role

ProjectInvitation:
- project invitations with expiry
- accept/decline methods

ProjectTask:
- title, description, assigned_to
- status, priority, due_date
- project tracking

ProjectMilestone:
- milestones for projects
- completion tracking
```

#### 6. **Social Features**
```python
Comment:
- user, project, content
- created_at, updated_at

Like:
- user, project
- unique together (one like per user per project)

Follow:
- follower, following (User)
- user follow tracking

Activity:
- user activity feed
- types: profile_updated, project_created, etc.
- public visibility control

Notification:
- notification_type (connection_request, etc.)
- from_user, to_user
- read_at tracking

UserStats:
- projects_created, connections_made
- likes_received, comments_made
- followers/following count
```

#### 7. **Messaging & Files**
```python
OTP:
- email, otp_code, purpose
- is_used, expires_at (5 min)
- validation methods

File:
- user, file, filename
- file_size, file_type

MessageFile:
- link files to messages

Draft:
- unsent message drafts
- content, recipient
```

---

## 5. CORE FEATURES ARCHITECTURE

### A. Authentication System
**Location**: `accounts/views.py` (login_view, register_view)

**Features**:
- Email/password registration
- OTP-based verification (5-minute expiry)
- Social login (Google, GitHub via django-allauth)
- Password reset flow
- Session management

**Key Functions**:
- `register_view()` - User registration with OTP
- `login_view()` - Email + password OR OTP
- `verify_otp_view()` - Validate OTP
- `forgot_password_view()` - Password reset initiation
- `reset_password_view()` - Set new password

### B. Profile Management
**Location**: `accounts/views.py` (student_profile, edit_profile, user_profile)

**Features**:
- Profile photo upload (AWS S3)
- Full profile setup (college, skills, interests)
- Bio and social links
- Profile completion tracking
- View other user profiles

**Key Functions**:
- `student_profile()` - Current user profile view
- `edit_profile()` - Update profile details
- `student_details_view()` - Initial setup wizard
- `user_profile()` - View any user's profile
- `user_profile_api()` - API endpoint for profile data

### C. Project Management
**Location**: `accounts/views.py` (post_project, project_detail, edit_project)

**Features**:
- Create/edit projects
- Project visibility (public/private/draft)
- Technology tags
- Collaboration needs specification
- Like/comment on projects
- Project filtering by visibility

**Key Functions**:
- `post_project()` - Create new project
- `project_detail()` - View project details
- `edit_project()` - Modify project
- `delete_project()` - Remove project
- `like_project()` - Like/unlike project
- `search_projects()` - Search with filters

### D. Collaboration & Connections
**Location**: `accounts/views.py` (connect_view, find_collaborators, team management)

**Features**:
- Send/accept/reject connection requests
- Find collaborators by skills/interests
- Invite users to projects
- Manage project team members
- Role-based permissions (owner/admin/contributor/viewer)

**Key Functions**:
- `connect_view()` - Send connection request
- `accept_connection()` - Accept request
- `find_collaborators()` - Search for collaborators
- `invite_to_team()` - Invite to project
- `respond_to_team_invitation()` - Accept/decline
- `remove_team_member()` - Remove from team

### E. Messaging & Chat
**Location**: `accounts/chat_api.py` + `accounts/chat_api_improved.py`

**Features**:
- Direct messaging (1-to-1)
- Group chats
- Message search
- Typing indicators
- Message reactions (emojis)
- Draft messages
- File attachments
- Read status tracking (scalable)
- Message threading/replies

**REST API Endpoints**:
```
POST   /accounts/chat-rooms/                      - Create chat room
GET    /accounts/chat-rooms/                      - List rooms
GET    /accounts/chat-rooms/<id>/                 - Room details
GET    /accounts/chat-rooms/<id>/members/         - Room members
POST   /accounts/direct-message/                  - Start direct chat
GET    /accounts/messages/                        - List messages
POST   /accounts/messages/                        - Send message
GET    /accounts/messages/<id>/                   - Message detail
POST   /accounts/messages/<id>/reactions/         - Add reaction
GET    /accounts/conversations/                   - Conversation list
```

### F. Comments System (Live Feed)
**Location**: `accounts/comment_api.py`

**Features**:
- Comment on projects
- Activity log for comments
- Notifications for project owners
- Comment editing/deletion
- Comment count tracking

**REST API Endpoints**:
```
GET    /accounts/api/projects/<id>/comments/      - Get all comments
POST   /accounts/api/projects/<id>/comments/add/  - Add comment
DELETE /accounts/api/comments/<id>/delete/        - Delete comment
PUT    /accounts/api/comments/<id>/edit/          - Edit comment
```

### G. Notifications
**Location**: `accounts/views.py` (notifications_view, create_notification)

**Features**:
- Real-time notifications
- Types: connection_request, project_comment, etc.
- Mark as read
- Notification feed

**Key Functions**:
- `notifications_view()` - Display notifications
- `mark_notification_read()` - Mark read
- `create_notification()` - Internal helper
- WebSocket support via Channels

### H. Activity Feed
**Location**: `accounts/views.py` (activity_feed)

**Features**:
- User activity tracking
- Public/private activities
- Types: profile_updated, project_created, comment_added, etc.
- Activity filtering

### I. Email System
**Location**: `accounts/zepto_mail_backend.py` + `accounts/brevo_mail_backend.py`

**Features**:
- ZeptoMail primary backend
- Brevo fallback
- Email backend for Django
- OTP email sending
- Transactional emails

---

## 6. URL ROUTING STRUCTURE

### Main Routes (`auth_project/urls.py`)
- Admin interface: `/admin/`
- App routes: `/accounts/...`
- API routes: `/accounts/api/...`

### Authentication Routes
```
/accounts/login/              - GET/POST login
/accounts/register/           - GET/POST registration
/accounts/logout/             - POST logout
/accounts/forgot-password/    - Password reset request
/accounts/reset-password/     - Reset with token
/accounts/verify-otp/         - Verify OTP code
/accounts/resend-otp/         - Resend OTP
```

### Core App Routes
```
/accounts/dashboard/          - User dashboard
/accounts/student-profile/    - View own profile
/accounts/student-details/    - Profile setup
/accounts/find-collaborators/ - Search collaborators
/accounts/post-project/       - Create project
/accounts/project-detail/     - View project
/accounts/my-projects/        - User's projects
/accounts/my-connections/     - Connections list
/accounts/notifications/      - Notification center
/accounts/activity-feed/      - Activity stream
```

### Messaging Routes
```
/accounts/messages/           - Message inbox
/accounts/chat/<user_id>/     - Direct chat
/accounts/create-group-chat/  - Create group
```

### Social Routes
```
/accounts/user/<username>/    - User profile
/accounts/follow/<user_id>/   - Follow user
/accounts/connect/<user_id>/  - Send connection
/accounts/like-project/<id>/  - Like project
```

---

## 7. REST API ENDPOINTS

### Chat/Messaging API
```
GET/POST  /accounts/chat-rooms/
GET/PUT   /accounts/chat-rooms/<id>/
GET       /accounts/chat-rooms/<id>/members/
POST      /accounts/direct-message/
GET/POST  /accounts/messages/
GET       /accounts/messages/<id>/
POST      /accounts/messages/<id>/reactions/
POST      /accounts/messages/<id>/status/
GET       /accounts/messages/search/
POST      /accounts/drafts/
POST      /accounts/typing/
GET       /accounts/conversations/
```

### Comments API
```
GET       /accounts/api/projects/<id>/comments/
POST      /accounts/api/projects/<id>/comments/add/
DELETE    /accounts/api/comments/<id>/delete/
PUT       /accounts/api/comments/<id>/edit/
```

### Utility APIs
```
POST      /accounts/college-search/
POST      /accounts/validate-college/
GET       /accounts/user-stats/
GET       /accounts/user-profile/<id>/
POST      /accounts/nlp-analyze/
GET       /accounts/check-username/
GET       /accounts/check-email/
```

---

## 8. KEY FUNCTIONALITY BREAKDOWN

### A. Login/Registration Flow
1. User visits login page
2. Enters email + password
3. Backend generates OTP (6 digits, 5-min expiry)
4. User enters OTP from email
5. Session created
6. Redirect to dashboard

### B. Project Creation Flow
1. User clicks "Post Project"
2. Fill: title, description, technologies, collaboration needs
3. Set visibility (public/private)
4. Submit → saved to database
5. Can edit/delete later
6. Appears in feeds if public

### C. Collaboration Flow
1. Find collaborators by searching
2. Send connection request
3. Recipient sees notification
4. Accept/reject connection
5. Once accepted, can invite to projects
6. Invited user gets notification
7. Can accept/decline team invitation
8. Team member roles: owner/admin/contributor/viewer

### D. Messaging Flow
1. Click user → start direct message
2. Both users in ChatRoom (direct type)
3. Messages sent/received in real-time (WebSockets)
4. Typing indicators show live
5. Message reactions available
6. Can search messages
7. Unread count tracked

### E. Comment System Flow
1. User viewing public project
2. Click "Add comment"
3. Comment saved to database
4. Project owner gets notification
5. Comment appears in live feed
6. Can edit/delete own comments

---

## 9. SETTINGS & CONFIGURATION

### Database Configuration
```python
# PostgreSQL connection
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': os.getenv('DB_NAME'),
        'USER': os.getenv('DB_USER'),
        'PASSWORD': os.getenv('DB_PASSWORD'),
        'HOST': os.getenv('DB_HOST'),
        'PORT': os.getenv('DB_PORT', '5432'),
    }
}
```

### Email Configuration
```python
EMAIL_BACKEND = 'accounts.zepto_mail_backend.ZeptoMailBackend'
ZEPTOMAIL_API_KEY = os.getenv('ZEPTOMAIL_API_KEY')
ZEPTOMAIL_FROM_EMAIL = 'unisync@zeptomail.com'
```

### Redis/Cache
```python
CACHES = {
    'default': {
        'BACKEND': 'django_redis.cache.RedisCache',
        'LOCATION': os.getenv('REDIS_URL'),
        'OPTIONS': {
            'CLIENT_CLASS': 'django_redis.client.DefaultClient',
        }
    }
}
```

### Channels/WebSocket
```python
ASGI_APPLICATION = 'auth_project.asgi.application'
CHANNEL_LAYERS = {
    'default': {
        'BACKEND': 'channels_redis.core.RedisChannelLayer',
        'CONFIG': {
            "hosts": [os.getenv('REDIS_URL')],
        },
    },
}
```

### AWS S3 Storage
```python
if not DEBUG:
    DEFAULT_FILE_STORAGE = 'storages.backends.s3boto3.S3Boto3Storage'
    AWS_STORAGE_BUCKET_NAME = os.getenv('AWS_BUCKET_NAME')
    AWS_S3_REGION_NAME = os.getenv('AWS_REGION', 'us-east-1')
```

### Social Login (django-allauth)
```python
SOCIALACCOUNT_PROVIDERS = {
    'google': {...},
    'github': {...},
}
```

---

## 10. SECURITY FEATURES

- **CSRF Protection**: Enabled via middleware
- **CORS Headers**: django-cors-headers for cross-origin requests
- **Password Hashing**: Django's default (PBKDF2)
- **OTP Expiry**: 5-minute validity window
- **Email Verification**: OTP-based registration
- **Permission System**: REST API permissions + view-level checks
- **Role-Based Access**: Project member roles
- **SSL/TLS**: Render/Railway automatic HTTPS

---

## 11. FILE & STORAGE STRUCTURE

### Static Files
```
accounts/static/
├── css/              - Stylesheets
├── js/               - JavaScript files
└── images/           - Static images
```

### Media Files (User Uploads)
```
media/
├── profile_photos/   - User avatars
├── chat_files/       - Message attachments
└── project_files/    - Project-related files
```

### Templates (50+ HTML files)
```
accounts/templates/
├── base.html                    - Base template
├── main.html, main_home.html    - Home page
├── login.html, register.html    - Auth pages
├── dashboard.html               - Main dashboard
├── student_profile.html         - Profile view
├── my_projects.html             - User projects
├── post_project.html            - Create project
├── project_detail.html          - Project view
├── find_collaborators*.html     - Search templates
├── messages.html                - Messaging
├── chat.html                    - Chat UI
├── notifications.html           - Notifications
├── activity_feed.html           - Activity stream
└── [other feature pages]        - Additional pages
```

---

## 12. KEY UTILITIES & HELPERS

### StudentProfileNLP (utils.py)
```python
# Natural Language Processing for profile analysis
- analyze_skills() - Parse skills from bio
- find_matching_projects() - Recommendation engine
- calculate_compatibility() - User-project matching
```

### ProjectVisibilityFilter (utils.py)
```python
# Filter projects based on visibility
- get_visible_projects() - Filter public/private
- check_project_access() - Permission validation
```

### create_notification() (views.py)
```python
# Internal helper for creating notifications
- Types: connection_request, project_comment, etc.
- Handles email + in-app notifications
```

---

## 13. IMPORTANT FILES OVERVIEW

| File | Lines | Purpose |
|------|-------|---------|
| models.py | ~718 | 16 Django models |
| views.py | 3311+ | Main view logic |
| urls.py | 129 | URL routing |
| settings.py | 356+ | Django configuration |
| chat_api_improved.py | ~400+ | Chat REST API |
| comment_api.py | ~243+ | Comments system |
| serializers.py | ~106+ | API serialization |
| permissions.py | ? | REST permissions |
| utils.py | ? | Helper functions |
| zepto_mail_backend.py | ? | Email integration |

---

## 14. DEPENDENCIES SUMMARY

### Core Framework
- Django 4.2.8
- DRF 3.14.0
- django-allauth 0.61.1

### Database
- psycopg2-binary 2.9.9
- dj-database-url 2.1.0

### APIs & Services
- Channels 4.0.0 (WebSockets)
- Celery 5.3.4 (Task queue)
- Redis 5.0.1 (Caching)
- boto3 1.34.34 (AWS S3)
- zeptomail 1.0.0 (Email)

### Data Processing
- pandas 2.1.4
- nltk 3.8.1 (NLP)
- Pillow 10.1.0 (Images)

### Development
- pytest 7.4.3
- black, flake8, mypy (Code quality)
- Sphinx (Documentation)

---

## 15. DEPLOYMENT CONFIGURATION

### Procfile (Render)
```bash
web: gunicorn auth_project.wsgi:application
release: python manage.py migrate
```

### render.yaml (Infrastructure)
```yaml
- PostgreSQL database
- Redis cache
- Environment variables
- Static file collection
```

### Key Environment Variables
```
DEBUG
SECRET_KEY
ALLOWED_HOSTS
DATABASE_URL
REDIS_URL
AWS_BUCKET_NAME
ZEPTOMAIL_API_KEY
BREVO_API_KEY
SOCIAL_AUTH_GOOGLE_OAUTH2_KEY
SOCIAL_AUTH_GITHUB_KEY
```

---

## 16. DATA FLOW DIAGRAMS

### Authentication Flow
```
User Registration
     ↓
Email + Password submitted
     ↓
OTP Generated (6 digits, 5 min)
     ↓
Email sent via ZeptoMail
     ↓
User enters OTP
     ↓
OTP validated
     ↓
User created + logged in
```

### Project & Comment Flow
```
User creates Project
     ↓
Saved to database
     ↓
Visibility set (public/private)
     ↓
Appears in feeds (if public)
     ↓
Other users can comment
     ↓
Comment saved + notification sent
     ↓
Comment appears in live feed
```

### Messaging Flow
```
User A initiates chat with User B
     ↓
ChatRoom created (direct type)
     ↓
Both added as members
     ↓
Message sent (WebSocket)
     ↓
Redis caches message
     ↓
Recipient notified
     ↓
Read status updated
```

---

## 17. SCALABILITY CONSIDERATIONS

### Current Optimizations
1. **Message Read Status**: Separate model instead of boolean field
2. **Redis Caching**: Reduces database hits
3. **Channels + Redis**: Real-time messaging at scale
4. **Database Indexing**: On frequently queried fields
5. **S3 Storage**: Offload media files
6. **Celery**: Background task processing
7. **Pagination**: Project and message lists

### Potential Improvements
1. Add database connection pooling (pgBouncer)
2. Implement activity aggregation (for feed)
3. Message archiving (old messages to separate table)
4. Cache warming for popular projects
5. Elasticsearch for advanced search

---

## 18. KNOWN ISSUES & FIXES

### Previous Fixes Applied
- ✅ Login form validation
- ✅ Profile photo upload
- ✅ Project card layout
- ✅ Comment posting system
- ✅ Message read status
- ✅ OTP expiry handling
- ✅ Email configuration

### Current Status
- 🟢 Authentication working
- 🟢 Profile management operational
- 🟢 Project CRUD functional
- 🟢 Messaging system active
- 🟢 Comment system live
- 🟢 Notifications enabled

---

## 19. TESTING STRUCTURE

### Test Files Present
```
test_login.py           - Authentication tests
test_profile_view.py    - Profile tests
test_search.py          - Search functionality
test_email.py           - Email backend
test_filter.py          - Visibility filtering
test_connections.py     - Connection system
test_services.py        - Service layer
```

### Testing Tools
- pytest + pytest-django
- Selenium (UI testing)
- Django test framework

---

## 20. FUTURE ENHANCEMENTS

### Planned Features
1. **AI Matching Algorithm** - Better collaborator recommendations
2. **Skill Verification** - Certifications/badges
3. **Project Portfolio** - Showcase completed projects
4. **Analytics Dashboard** - User stats and trends
5. **Mobile App** - Native iOS/Android
6. **Video Conferencing** - Built-in call system
7. **Payment Integration** - Premium features
8. **Machine Learning** - Skill predictions

---

## QUICK START COMMANDS

### Local Development
```bash
# Setup
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
pip install -r requirements.txt

# Create .env file with required variables
# Run migrations
python manage.py migrate

# Create superuser
python manage.py createsuperuser

# Run development server
python manage.py runserver

# Run Celery worker
celery -A auth_project worker -l info

# Run Channels with Daphne
daphne -b 0.0.0.0 -p 8000 auth_project.asgi:application
```

### Testing
```bash
pytest                          # Run all tests
pytest accounts/tests.py        # Run app tests
pytest --cov=accounts          # With coverage
```

### Deployment
```bash
# Render deployment
git push origin main            # Auto-deploys via Procfile

# Local production build
gunicorn auth_project.wsgi:application
```

---

## SUMMARY

UniSync is a **comprehensive Django-based collaborative learning platform** with:

✅ Complete user authentication (email + social login)  
✅ Advanced project management system  
✅ Real-time messaging with WebSockets  
✅ Comments & live feed system  
✅ Collaboration & connection management  
✅ Role-based project teams  
✅ Notifications system  
✅ Activity tracking  
✅ Cloud storage integration (S3)  
✅ Email infrastructure  
✅ REST API for mobile-ready features  
✅ Production-ready deployment setup  

The codebase is well-structured, follows Django best practices, and is ready for further enhancement and scaling.
