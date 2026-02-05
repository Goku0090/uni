# Unisync - Complete Codebase Analysis 2026

## Executive Summary

**Unisync** is a Django-based collaboration platform for university students to connect, share projects, and find team members. It combines social networking features with project management capabilities.

### Tech Stack
- **Backend**: Django 4.2.8 + Django REST Framework
- **Database**: PostgreSQL
- **Authentication**: Django Allauth (Email OTP, Google OAuth, GitHub OAuth)
- **Email**: Zeptomail & Brevo
- **Frontend**: Django Templates (HTML/CSS/JS)
- **Real-time**: Channels + Redis
- **Caching**: Redis
- **File Storage**: AWS S3 (boto3)
- **Task Queue**: Celery
- **Deployment**: Render

---

## Project Architecture

### Directory Structure
```
e:/login/auth_project/
├── auth_project/              # Django project configuration
│   ├── settings.py            # All configurations (DB, email, apps, middleware)
│   ├── urls.py                # Main URL routing
│   ├── wsgi.py                # Production server entry
│   └── asgi.py                # WebSocket support
│
├── accounts/                  # Main application (core business logic)
│   ├── models.py              # Database models (16 models)
│   ├── views.py               # View logic (3300+ lines)
│   ├── urls.py                # App-specific routing
│   ├── serializers.py         # DRF serializers for API
│   ├── forms.py               # Django forms (login, registration)
│   ├── permissions.py         # DRF custom permissions
│   ├── comment_api.py         # Comment endpoint logic
│   ├── chat_api.py            # Chat/messaging logic
│   ├── brevo_mail_backend.py  # Email backend (Brevo)
│   ├── zepto_mail_backend.py  # Email backend (Zeptomail)
│   ├── services/              # Business logic services
│   ├── static/                # JS, CSS files
│   ├── templates/             # HTML templates
│   └── migrations/            # Database migrations
│
├── manage.py                  # Django CLI
├── requirements.txt           # Python dependencies (80+ packages)
├── .env                       # Environment variables
└── Procfile                   # Render deployment config
```

---

## Core Models & Database Schema

### 1. **User & Authentication**
- **User** (Django built-in)
  - Contains: username, email, password, first_name, last_name
  
- **StudentProfile** (Extended Profile)
  - Linked to User (OneToOne)
  - Fields: full_name, college, location, bio, interests, skills, role_preference
  - Social links: GitHub, LinkedIn, Portfolio, Behance
  - Profile photo support

- **OTP** (One-Time Password)
  - Used for: Login, Registration, Password Reset
  - Features: 6-digit code, 5-minute expiry, multi-use prevention
  - Methods: `generate_otp()`, `verify_otp()`, `is_valid()`

### 2. **Projects & Collaboration**
- **Project**
  - Owner → User (ForeignKey)
  - Fields: title, description, technologies, looking_for, category, timeline, github_link
  - Status: is_active (boolean)
  - Categories: Web, Mobile, AI/ML, Data Science, Blockchain, IoT, Game Dev, Other

- **ProjectMember** / **ProjectTeam** / **ProjectTeamMember**
  - Tracks team composition and roles

- **ProjectTask** / **ProjectMilestone**
  - Project management features

### 3. **Social Features**
- **Connection**
  - Represents friend requests (pending/accepted/rejected)
  - Bidirectional relationship (sender/receiver)
  - Unique constraint: sender + receiver

- **Follow**
  - Users can follow each other
  - Tracks follower/following relationships

- **Like**
  - Projects can be liked
  - Users give likes (unique per user-project pair)

- **Comment**
  - Comments on projects
  - Linked to User → Project
  - Timestamps for creation/update

- **Activity**
  - Feed of user activities (project created, liked, connected, etc.)
  - Types: profile_updated, project_created, project_liked, connection_made, etc.

### 4. **Messaging & Communication**
- **Message**
  - Sender → Receiver (direct) or ChatRoom (group)
  - Types: text, file, image, call
  - Threading support: reply_to (self-reference)
  - Read status tracked separately

- **ChatRoom**
  - Types: direct, group, project
  - Members tracked with roles (owner, admin, member)

- **ChatRoomMember**
  - Role-based access control
  - Active/inactive status

- **MessageReadStatus**
  - Tracks which users read which messages
  - Scalable design (separate table)

- **MessageFile**
  - File attachments to messages

- **MessageReaction**
  - Emoji/reaction responses to messages

- **File**
  - General file uploads
  - Metadata: filename, size, type, timestamp

- **UserStatus**
  - Online/offline status
  - Last seen timestamp
  - Current WebSocket room

### 5. **Notifications**
- **Notification**
  - Types: connection_request, message, project_like, project_comment, team_invitation, follow
  - Tracks: related user, object (connection/message), read status
  - Timestamps for creation and read time

---

## Core Views & Business Logic

### Authentication Flow
```
views.py:
- register_view() → Form validation → OTP generation → Email send
- login_view() → OTP verification → Session creation
- otp_verification() → OTP.verify_otp() → User login
- social_login_callback() → Allauth handling → Profile creation
```

### Project Management
```
views.py:
- create_project_view() → Form save → Activity log
- project_detail() → ProjectVisibilityFilter check → Comments/Likes
- edit_project() → Permission check → Update
- delete_project() → Permission check → Soft delete
- project_feed() → Paginated list with filters
```

### Messaging System
```
chat_api.py:
- get_conversations() → User's active chats
- send_message() → Save to DB → Notification trigger
- get_messages() → Paginated message history
- mark_as_read() → MessageReadStatus update
```

### Notifications
```
views.py:
- get_notifications() → User's unread notifications
- mark_notification_read() → Update is_read flag
- delete_notification() → Soft delete
- notify_user() → Create Notification object
```

### Collaborator Search
```
views.py (lines 1453-1578):
- find_collaborators() → StudentProfileNLP.match_profiles()
- Uses: interests, skills, project_interests matching
- Returns: Ranked list of compatible users
```

---

## URL Routes & API Endpoints

### Main Routes (auth_project/urls.py)
```
/                          → home (TemplateView)
/admin/                    → Django admin
/accounts/                 → accounts app URLs
/accounts/sociallogin/     → Allauth social auth
/dashboard/                → dashboard_view
```

### App Routes (accounts/urls.py)
```
API ENDPOINTS:
GET    /api/user/profile/              → UserProfile API
GET    /api/projects/                  → Project list
POST   /api/projects/                  → Create project
GET    /api/projects/<id>/             → Project detail
POST   /api/comments/                  → Create comment
GET    /api/comments/<id>/             → Comment list
GET    /api/notifications/             → User notifications
POST   /api/messages/                  → Send message
GET    /api/messages/                  → Message list
GET    /api/connections/               → Connection list
POST   /api/connections/               → Request connection
```

### Template Routes
```
/login/                    → login_view
/register/                 → register_view
/otp-verify/              → otp_verification
/profile/<username>/      → student_profile_view
/edit-profile/            → edit_profile
/projects/                → project_feed
/create-project/          → create_project_view
/messages/                → chat_view
/dashboard/               → dashboard_view
```

---

## Key Features & Implementation

### 1. OTP-Based Authentication
- 6-digit OTP code generation
- 5-minute expiry
- Email delivery via Zeptomail/Brevo
- Multi-purpose: login, registration, password reset
- **File**: accounts/models.py lines 55-124

### 2. Social Login Integration
- Google OAuth (django-allauth)
- GitHub OAuth (django-allauth)
- Automatic profile creation on first login
- **Files**: settings.py (Allauth config), views.py (callbacks)

### 3. Project Visibility Filtering
- Private/Public projects
- Owned by user only flag
- Collaborator-only access
- **File**: utils.py (ProjectVisibilityFilter class)

### 4. Real-Time Messaging
- WebSocket support (Channels)
- Group chats + Direct messages
- Read receipts
- File sharing
- **Files**: chat_api.py, ChatRoom models

### 5. Collaborator Matching
- NLP-based profile matching
- Interest alignment
- Skills compatibility
- **File**: utils.py (StudentProfileNLP class)

### 6. Activity Feed
- User activity tracking
- Public/Private activities
- Types: profile updates, project creation, likes, connections
- **File**: accounts/models.py (Activity model)

### 7. Email Notifications
- Comment notifications
- Connection requests
- Message notifications
- Project activity updates
- **Files**: brevo_mail_backend.py, zepto_mail_backend.py

---

## Serializers & API Response Format

### Main Serializers (accounts/serializers.py)
1. **UserProfileSerializer**
   - Nested StudentProfile data
   - Includes: username, email, profile details, stats

2. **ProjectSerializer**
   - Owner info, technologies, team members
   - Comment count, like count

3. **NotificationSerializer**
   - Type, title, message, related objects

4. **MessageSerializer**
   - Sender info, content, timestamps, read status

5. **ConnectionSerializer**
   - Sender, receiver, status, timestamps

---

## Services & Business Logic

### accounts/services/ Directory
- **EmailService**: Email sending abstraction
- **NotificationService**: Create & dispatch notifications
- **ProjectService**: Project operations
- **MessageService**: Message handling
- **ProfileService**: Profile matching and search

### Utilities (accounts/utils.py)
- **StudentProfileNLP**: NLP-based matching algorithm
- **ProjectVisibilityFilter**: Permission checking

---

## Configuration & Settings

### Key Settings (settings.py)
```python
INSTALLED_APPS:
  - django core
  - accounts (main app)
  - allauth (authentication)
  - rest_framework (API)
  - channels (WebSocket)
  - corsheaders (CORS)
  - debug_toolbar (development)
  - storages (S3 storage)

DATABASES:
  - PostgreSQL (via dj-database-url)

CACHING:
  - Redis backend

EMAIL:
  - Zeptomail or Brevo backend (configurable)
  - Sender: admin email from .env

AUTHENTICATION:
  - Email OTP backend
  - Social OAuth (Google, GitHub)

FILE STORAGE:
  - AWS S3 (boto3)
  - Static files: WhiteNoise
```

### Environment Variables (.env)
```
DEBUG=True
SECRET_KEY=...
ALLOWED_HOSTS=localhost,127.0.0.1

DATABASE_URL=postgresql://user:pass@host/db

EMAIL_BACKEND=zeptomail|brevo
ZEPTOMAIL_API_KEY=...
BREVO_API_KEY=...

GOOGLE_OAUTH_CLIENT_ID=...
GOOGLE_OAUTH_CLIENT_SECRET=...

AWS_ACCESS_KEY_ID=...
AWS_SECRET_ACCESS_KEY=...
AWS_STORAGE_BUCKET_NAME=...

REDIS_URL=redis://...

ALLOWED_HOSTS=...
SECURE_SSL_REDIRECT=False
```

---

## Database & ORM Patterns

### Query Patterns
```python
# Get user profile
profile = StudentProfile.objects.get(user=user)

# Find collaborators
users = User.objects.filter(
    student_profile__interests__overlap=my_interests
)

# Get user projects with comments
projects = Project.objects.filter(
    user=user
).prefetch_related('comments', 'likes')

# Get unread messages
messages = Message.objects.filter(
    receiver=user
).exclude(
    id__in=MessageReadStatus.objects.filter(user=user).values('message_id')
)

# Connection management
Connection.objects.filter(sender=user, status='accepted')

# Activity feed
Activity.objects.filter(
    Q(user__in=following_users) | Q(is_public=True)
).order_by('-timestamp')
```

### Performance Optimizations
- `select_related()` for ForeignKey relationships
- `prefetch_related()` for M2M and reverse relationships
- Redis caching for frequently accessed data
- Database indexing on foreign keys and search fields

---

## Testing Strategy

### Test Files
- `test_login.py` - OTP login flow
- `test_profile_fix.py` - Profile endpoints
- `test_comments_api.py` - Comment functionality
- `test_connections.py` - Connection requests
- `test_profile_upload.py` - File upload
- `test_services.py` - Service layer

### Manual Testing Scripts
- `debug_profiles.py` - Profile debugging
- `debug_filtering.py` - Project filtering
- `performance_monitor.py` - Performance tracking

---

## Deployment

### Render Deployment (render.yaml)
- Automatic database URL setup
- Gunicorn server
- WhiteNoise for static files
- Environment variable injection

### Build Script (build.sh)
- Database migrations
- Static files collection
- Cache clearing

---

## Security Features

### Authentication
- CSRF protection enabled
- Session-based auth
- OTP verification
- Social login via OAuth

### Authorization
- Permission checking in views
- Custom permissions (permissions.py)
- Role-based access (ChatRoom roles)

### Data Protection
- Password hashing (Django default)
- Secure cookie settings (environment-based)
- SSL redirect (production-only)

### Rate Limiting
- Via middleware (can be extended)
- API throttling (DRF built-in)

---

## Performance Optimizations

### Caching Strategy
- Redis for session storage
- Cache frequently accessed profiles
- Pagination for list views (10 items per page)
- Lazy loading for relationships

### Database Optimization
- Indexed fields: user_id, created_at
- Proper use of select_related/prefetch_related
- Aggregation queries for counts

### Static Files
- WhiteNoise compression
- S3 storage for media
- CDN-ready configuration

---

## Common Issues & Fixes

### Login Issues
- **Cause**: OTP expiration (5 minutes)
- **Fix**: Generate new OTP or check email

### Profile Photo Not Showing
- **Cause**: S3 bucket not configured
- **Fix**: Check AWS credentials in .env

### Comments Not Visible
- **Cause**: ProjectVisibilityFilter check failed
- **Fix**: Verify user has permission to view project

### Messages Not Syncing
- **Cause**: Redis connection issue
- **Fix**: Check REDIS_URL in .env

---

## Development Workflow

### Local Setup
```bash
# Create virtual environment
python -m venv venv
source venv/Scripts/activate  # Windows
source venv/bin/activate      # Linux/Mac

# Install dependencies
pip install -r requirements.txt

# Setup .env
cp .env.template .env
# Edit .env with local settings

# Run migrations
python manage.py migrate

# Create superuser
python manage.py createsuperuser

# Run development server
python manage.py runserver
```

### Common Commands
```bash
# Migrations
python manage.py makemigrations
python manage.py migrate

# Shell
python manage.py shell

# Static files
python manage.py collectstatic

# Tests
python manage.py test
pytest

# Debugging
python manage.py shell_plus
python manage.py runserver --pdb
```

---

## Key Statistics

- **Total Models**: 16+
- **Views/Endpoints**: 50+
- **URL Routes**: 40+
- **Serializers**: 6+
- **Forms**: 5+
- **Email Backends**: 2
- **Auth Methods**: Email OTP + Google + GitHub
- **Database Tables**: 25+
- **Static Files**: CSS, JS for templates
- **Tests**: 10+ test files

---

## Next Steps & Recommendations

### Scalability
- Implement caching layer for hot data
- Use Celery tasks for heavy operations
- Add database read replicas
- Implement API rate limiting

### Features
- Add WebRTC for video calls
- Implement advanced search with Elasticsearch
- Add recommendation engine for project matching
- Implement project analytics dashboard

### Performance
- Add APM monitoring (Sentry already configured)
- Profile slow queries
- Optimize N+1 queries
- Implement full-text search

### Testing
- Increase test coverage to 80%+
- Add integration tests for API
- Load testing with Locust
- E2E testing with Selenium

---

## References

### Key Files for Understanding Each Feature
| Feature | File | Lines |
|---------|------|-------|
| Models | accounts/models.py | 1-718 |
| Views | accounts/views.py | 1-3315 |
| URLs | accounts/urls.py | 1-129 |
| Serializers | accounts/serializers.py | 1-200 |
| Messaging | chat_api.py | 1-500 |
| Comments | comment_api.py | 1-300 |
| Settings | auth_project/settings.py | 1-356 |

---

## Contact & Documentation

- **Repository**: https://github.com/Goku0090/uni
- **Deployment**: Render (render.yaml)
- **Database**: PostgreSQL
- **API Documentation**: Generated by DRF Spectacular

Generated: February 2026
