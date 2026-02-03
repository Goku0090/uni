# Comprehensive Codebase Analysis - UniSync 2025

## 📋 Executive Summary

**Project**: UniSync - A Django-based collaborative student platform  
**Repository**: https://github.com/Goku0090/uni  
**Framework**: Django 4.2.8 + Django REST Framework 3.14.0  
**Database**: PostgreSQL (production) / SQLite (development)  
**Status**: Fully functional with OTP authentication, social login, messaging, and project management

---

## 📁 Project Structure

```
auth_project/
├── auth_project/              # Django project configuration
│   ├── settings.py           # Main configuration
│   ├── urls.py               # URL routing
│   ├── wsgi.py              # WSGI application
│   └── asgi.py              # ASGI application
├── accounts/                 # Main application
│   ├── models.py            # Database models (25+ models)
│   ├── views.py             # View logic (~3311 lines)
│   ├── forms.py             # Django forms
│   ├── urls.py              # API endpoints
│   ├── serializers.py       # DRF serializers
│   ├── permissions.py       # Custom permissions
│   ├── chat_api.py          # Messaging/chat endpoints
│   ├── utils.py             # Utility functions
│   ├── services/
│   │   └── auth_service.py  # Authentication service
│   ├── views_contact.py     # Contact page handling
│   ├── brevo_mail_backend.py # Email backend (Brevo)
│   ├── zepto_mail_backend.py # Email backend (ZeptoMail)
│   └── migrations/          # Database migrations
├── static/                   # Static files (JS, CSS)
├── media/                    # User uploads
├── templates/                # HTML templates
├── logs/                     # Application logs
├── manage.py                # Django management script
└── requirements.txt         # Dependencies
```

---

## 🗄️ Database Models (25+ Models)

### Authentication & Users
- **User** (Django built-in): Standard Django user model
- **StudentProfile**: Extended user profile with:
  - `full_name`, `college`, `location`
  - `profile_photo`, `bio`, `interests`
  - `skills`, `project_interests`, `role_preference`
  - Social links (GitHub, LinkedIn, Portfolio, Behance)
  - Profile completion status

### Authentication Security
- **OTP**: One-time passwords for login/registration/password reset
  - Supports multiple purposes (login, registration, reset)
  - Automatic expiry (5 minutes)
  - Prevents reuse (marks as used)

### Messaging & Communication
- **Message**: Direct/group messages with:
  - Support for text, file, image, call types
  - Reply threading
  - Read status tracking
- **MessageReadStatus**: Scalable read status tracking
- **MessageReaction**: Message reactions/emojis
- **MessageFile**: File attachments
- **File**: User uploads with file metadata
- **ChatRoom**: Group chats and direct message rooms
- **ChatRoomMember**: Chat room membership with roles
- **Notification**: User notifications
- **UserStatus**: Online/offline status

### Social & Connections
- **Connection**: Connection requests between users
  - Status: pending, accepted, rejected
  - Unique constraint: sender + receiver
- **Follow**: User following/follower relationships
- **Activity**: User activity feed
  - 8 activity types (profile_updated, project_created, etc.)

### Projects & Collaboration
- **Project**: Main project model with:
  - `title`, `description`, `collaboration_needs`
  - `visibility` (public, private, invite-only)
  - `skills_required`, `members_needed`
  - `owner`, `collaborators`, `category`
  - Created/updated timestamps
- **ProjectMember/ProjectTeam**: Team membership with roles:
  - Roles: owner, admin, contributor, viewer
  - Permissions: manage_project, invite_members, manage_tasks, edit_project
- **ProjectInvitation**: Invitations with:
  - Status: pending, accepted, declined, expired
  - Role assignment
  - Expiry handling
- **ProjectTask**: Task management:
  - Status: todo, in_progress, review, completed, cancelled
  - Priority: low, medium, high, urgent
  - Assigned to specific user
  - Due date tracking
- **ProjectMilestone**: Project milestones with:
  - Completion tracking
  - Assigned user
  - Due dates

### Analytics & Stats
- **Like**: Project likes
- **Comment**: Project/message comments
- **UserStats**: User statistics dashboard
  - Projects created, connections, likes, comments
  - Tasks completed, followers/following

---

## 🔐 Authentication System

### Multi-Method Authentication
1. **Username/Email + Password**
   - Custom validation (uppercase, lowercase, digits)
   - Minimum 8 characters
   
2. **OTP-Based Login** (Primary for mobile/email)
   - Generate 6-digit OTP
   - 5-minute expiry
   - Multiple purposes supported
   - Sends via configured email backend
   
3. **Social Login** (via django-allauth)
   - Google OAuth
   - GitHub OAuth
   - Automatic user creation/linking

### Email Backends (Priority Order)
1. **Brevo** (Production recommended)
2. **ZeptoMail** (Alternative)
3. **Gmail SMTP** (Fallback)
4. **Console** (Development)

---

## 🌐 API Endpoints Structure

### Authentication Routes
- `POST /login/` - Login with credentials
- `POST /register/` - User registration
- `GET /logout/` - Logout
- `POST /forgot-password/` - Initiate password reset
- `POST /reset-password/` - Complete password reset
- `POST /verify-otp/<purpose>/` - Verify OTP
- `POST /resend-otp/<purpose>/` - Resend OTP

### Profile Routes
- `GET /student-profile/` - View student profile
- `POST /student-details/` - Update student details
- `GET /user/<username>/` - View user profile
- `GET /user-profile/<user_id>/` - API endpoint for user profile
- `POST /edit-profile/` - Edit own profile

### Project Routes
- `GET /explore-projects/` - Discover projects
- `GET /my-projects/` - User's projects
- `POST /post-project/` - Create project
- `GET /project/<project_id>/` - Project details
- `PUT /edit-project/<project_id>/` - Edit project
- `DELETE /delete-project/<project_id>/` - Delete project
- `POST /like-project/<project_id>/` - Like project
- `GET /college-search/` - Search colleges (via RapidAPI)
- `POST /validate-college/` - Validate college

### Messaging Routes
- `GET /messages/` - View messages
- `GET /chat/<user_id>/` - Direct message chat
- `GET /conversations/` - List conversations
- `POST /messages/` - Send message
- `POST /messages/<message_id>/status/` - Update read status
- `POST /messages/<message_id>/reactions/` - Add reaction
- `POST /chat-rooms/` - Create group chat
- `POST /typing/` - Send typing indicator

### Social Routes
- `GET /activity-feed/` - User activity feed
- `GET /notifications/` - View notifications
- `POST /notifications/<id>/read/` - Mark notification read
- `GET /my-connections/` - List connections
- `POST /connect/<user_id>/` - Send connection request
- `POST /accept-connection/<connection_id>/` - Accept connection
- `POST /reject-connection/<connection_id>/` - Reject connection
- `POST /follow/<user_id>/` - Follow user
- `GET /find-collaborators/` - Find collaboration partners

### Team Management
- `POST /invite-to-team/<project_id>/` - Invite team member
- `POST /respond-team-invitation/<invitation_id>/` - Respond to invitation
- `DELETE /remove-team-member/<project_id>/<user_id>/` - Remove member

### Utility Routes
- `GET /dashboard/` - User dashboard
- `GET /help/` - Help center
- `GET /privacy/` - Privacy policy
- `GET /terms/` - Terms of service
- `POST /contact/submit/` - Contact form
- `GET /download-file/<file_id>/` - Download file

---

## 🔧 Key Features Implementation

### 1. OTP-Based Authentication
```python
# Location: accounts/models.py - OTP class
- Automatic 6-digit code generation
- 5-minute expiry time
- Purpose-based OTP management
- Prevents reuse
- Hash verification support
```

### 2. Project Visibility & Filtering
```python
# Location: accounts/utils.py - ProjectVisibilityFilter
- Public: Visible to all users
- Private: Only owner
- Invite-only: Specific invited users
- Smart filtering based on user permissions
```

### 3. Student Profile NLP
```python
# Location: accounts/utils.py - StudentProfileNLP
- Profile analysis
- Skill extraction
- Interest matching
- Collaboration compatibility scoring
```

### 4. Messaging System
```python
# Key Features:
- Direct messages between users
- Group chat rooms
- File attachments
- Message reactions
- Read status tracking (scalable design)
- Typing indicators
- Message threading/replies
```

### 5. REST API Framework
```python
# Location: accounts/chat_api.py, serializers.py
- DRF-based API endpoints
- Token/session authentication
- Pagination support
- Search and filtering
- CORS enabled
```

---

## 📦 Dependencies (84 packages)

### Core Framework
- Django 4.2.8
- djangorestframework 3.14.0
- django-allauth 0.61.1

### Database
- psycopg2-binary 2.9.9 (PostgreSQL)
- dj-database-url 2.1.0

### Email & Communication
- zeptomail 1.0.0
- Custom Brevo integration

### Authentication
- requests 2.31.0
- requests-oauthlib 1.3.1

### Data & Processing
- pandas 2.1.4
- nltk 3.8.1
- openpyxl 3.1.2

### Cloud & Storage
- boto3 1.34.34 (AWS S3)
- django-storages 1.14.2

### Real-Time Features
- channels 4.0.0 (WebSockets)
- channels-redis 4.1.0

### Performance & Caching
- redis 5.0.1
- django-redis 5.4.0
- whitenoise 6.6.0 (static files)

### Development & Testing
- pytest 7.4.3
- pytest-django 4.7.0
- black 23.12.1 (code formatting)
- flake8 6.1.0 (linting)
- mypy 1.7.1 (type checking)

### Monitoring
- sentry-sdk 1.38.0

### Additional
- Pillow 10.1.0 (image processing)
- celery 5.3.4 (background tasks)
- gunicorn 21.2.0 (production server)

---

## 🚀 Configuration & Settings

### Security Settings
```python
# Location: auth_project/settings.py

DEBUG = Environment variable
SECRET_KEY = Required in production
ALLOWED_HOSTS = Configurable
SECURE_SSL_REDIRECT = Optional
SESSION_COOKIE_SECURE = Optional
CSRF_COOKIE_SECURE = Optional
```

### Database Configuration
```python
# Priority:
1. DATABASE_URL (Render environment)
2. PostgreSQL (via individual env vars)
3. SQLite (fallback for development)
```

### Email Configuration
```python
# Priority Backend Selection:
1. Brevo (BREVO_API_KEY)
2. ZeptoMail (ZEPTO_MAIL_API_KEY + ZEPTO_MAIL_TOKEN)
3. Gmail SMTP (EMAIL_HOST_USER + EMAIL_HOST_PASSWORD)
4. Console (development)
```

### Social OAuth Providers
```python
# Configured:
- Google: GOOGLE_CLIENT_ID, GOOGLE_CLIENT_SECRET
- GitHub: GITHUB_CLIENT_ID, GITHUB_CLIENT_SECRET
```

### External APIs
```python
# RapidAPI for university search:
- RAPIDAPI_KEY
- RAPIDAPI_HOST (universities-list.p.rapidapi.com)
```

### REST Framework Configuration
```python
- DEFAULT_PERMISSION_CLASSES: AllowAny
- SESSION_AUTHENTICATION enabled
- PAGINATION: PageNumberPagination (10 per page, max 100)
- SEARCH: Supported on filtered endpoints
- ORDERING: Supported on filtered endpoints
```

---

## 📊 View Functions (Major)

### Authentication Views
- `login_view()` - Handles OTP + credential login
- `register_view()` - User registration with email verification
- `logout_view()` - Logout and cleanup
- `forgot_password_view()` - Password reset initiation
- `reset_password_view()` - Password reset completion
- `verify_otp_view()` - OTP verification
- `resend_otp_view()` - OTP resend

### Profile Views
- `student_profile()` - View student profile
- `student_details_view()` - Edit student details
- `edit_profile()` - Edit profile with avatar upload
- `user_profile()` - View other user's profile
- `UserProfileView.as_view()` - REST API profile endpoint

### Project Views
- `post_project()` - Create new project
- `edit_project()` - Edit project details
- `delete_project()` - Delete project
- `project_detail()` - View project details
- `like_project()` - Like/unlike project
- `explore_projects_view()` - Browse all projects
- `my_projects_view()` - User's projects
- `search_projects()` - Search projects

### Social Views
- `activity_feed()` - User activity feed
- `notifications_view()` - View notifications
- `mark_notification_read()` - Mark notification read
- `find_collaborators()` - Find collaboration partners
- `user_profile()` - View user profile

### Connection Views
- `send_connection_request()` - Send connection
- `accept_connection()` - Accept connection
- `reject_connection()` - Reject connection
- `my_connections()` - View connections
- `follow_user()` - Follow user

### Messaging Views
- `message_view()` - Message list
- `chat_view()` - Direct message chat
- `enhanced_messages_view()` - Group chat
- `enhanced_chat_view()` - Group chat detail
- `create_group_chat()` - Create group chat
- `add_reaction()` - Add message reaction

### Team Views
- `invite_to_team()` - Invite team member
- `respond_to_team_invitation()` - Accept/reject invitation
- `remove_team_member()` - Remove team member

---

## 🎯 Advanced Features

### Project Visibility & Filtering
- **Public Projects**: Visible to all authenticated users
- **Private Projects**: Only owner can view
- **Invite-only Projects**: Specific invited users only
- **Filter by**: Skills, visibility, status, date range

### User Recommendations
- NLP-based profile analysis
- Skill matching for collaboration
- Interest-based project suggestions
- Compatibility scoring

### Real-Time Features
- WebSocket support via Django Channels
- Typing indicators
- Online/offline status
- Live message updates

### File Management
- File upload to project
- File attachments to messages
- File storage (S3/local)
- Download tracking

### Activity & Stats
- User activity feed
- Project creation/update tracking
- Connection activity logging
- Statistics dashboard
- Performance monitoring

---

## 🔍 Code Quality & Testing

### Test Files
Located in `auth_project/` directory:
- `test_login.py` - Login functionality tests
- `test_profile_*.py` - Profile view tests
- `test_email.py` - Email backend tests
- `test_filter.py` - Project filtering tests
- `test_feed_fix.py` - Activity feed tests
- `test_services.py` - Service layer tests

### Code Quality Tools
- **black** - Code formatting
- **flake8** - Linting
- **mypy** - Type checking
- **isort** - Import sorting
- **pytest** - Testing framework

### Logging Configuration
```python
# Location: auth_project/settings.py
- Console logging
- File logging (django.log)
- Error file logging (error.log)
- Rotating file handlers (10 MB max, 5 backups)
- Verbose formatting with timestamps
```

---

## 🚢 Deployment Configuration

### Environment Files
- `.env` - Development configuration
- `.env.template` - Template for required variables

### Deployment Platforms
- **Render**: Primary deployment target
  - PostgreSQL via Render
  - DATABASE_URL environment variable
  - Procfile for process management
- **Railway**: Secondary option
  - railway.json configuration

### Static Files
- WhiteNoise for static file serving
- S3/boto3 support for cloud storage
- Media files handling

---

## 📝 Logging & Monitoring

### Logging Configuration
```
Levels:
- DEBUG: Detailed development logs
- INFO: General information
- ERROR: Error-specific logs

Outputs:
- Console: Real-time monitoring
- django.log: All logs
- error.log: Errors only
```

### Monitoring Tools
- Sentry SDK integration for error tracking
- Performance monitoring middleware

---

## ⚙️ Key Technical Decisions

1. **Database**: PostgreSQL for production, SQLite fallback for development
2. **Authentication**: Multi-method (credentials, OTP, OAuth)
3. **Email**: Priority-based backend selection (Brevo > ZeptoMail > SMTP)
4. **Messaging**: Scalable design with MessageReadStatus model
5. **API**: REST-based with DRF
6. **Real-Time**: Django Channels for WebSocket support
7. **Storage**: Cloud-ready (S3 support via boto3)
8. **Caching**: Redis for performance
9. **Background Jobs**: Celery for async tasks
10. **Monitoring**: Sentry for error tracking

---

## 📌 Important Files Summary

| File | Purpose | Lines |
|------|---------|-------|
| settings.py | Django configuration | 356+ |
| models.py | Database models | 718 |
| views.py | View logic | 3311+ |
| forms.py | Django forms | 583+ |
| urls.py | URL routing | 120 |
| serializers.py | DRF serializers | ? |
| chat_api.py | Messaging endpoints | ? |
| permissions.py | Custom permissions | ? |

---

## 🔑 Recent Fixes & Enhancements

Based on directory listing, recent work includes:
- OTP-based login implementation
- Email integration (Brevo/ZeptoMail)
- Social login (Google/GitHub)
- Project visibility filtering
- Message read status tracking
- Profile viewing implementation
- Notification badge updates
- Performance optimizations
- PostgreSQL integration
- Render.com deployment

---

## 📋 Setup Requirements

### Environment Variables
```
# Core
DEBUG=True/False
SECRET_KEY=your_secret_key
ALLOWED_HOSTS=localhost,127.0.0.1

# Database
DATABASE_URL=postgresql://...
OR
DB_NAME, DB_USER, DB_PASSWORD, DB_HOST, DB_PORT

# Email
BREVO_API_KEY=...
OR
ZEPTO_MAIL_API_KEY, ZEPTO_MAIL_TOKEN
OR
EMAIL_HOST_USER, EMAIL_HOST_PASSWORD

# Social Auth
GOOGLE_CLIENT_ID, GOOGLE_CLIENT_SECRET
GITHUB_CLIENT_ID, GITHUB_CLIENT_SECRET

# External APIs
RAPIDAPI_KEY

# Optional
SECURE_SSL_REDIRECT, SESSION_COOKIE_SECURE, CSRF_COOKIE_SECURE
```

---

## 🎓 Learning Paths

### Developers should understand:
1. Django ORM and QuerySet API
2. Django REST Framework concepts
3. Celery task queue basics
4. WebSocket fundamentals (Django Channels)
5. PostgreSQL/SQLite differences
6. OAuth 2.0 flow
7. Email service integration
8. File upload handling

---

## 🐛 Known Areas to Monitor

1. **Message Read Status**: Scalable design, monitor for performance
2. **File Uploads**: Validate file sizes and types
3. **Email Delivery**: Monitor all email backends
4. **WebSocket Connections**: Handle connection drops
5. **Database Queries**: Monitor N+1 query problems
6. **Cache Invalidation**: Ensure proper cache cleanup
7. **Social OAuth**: Handle token expiry

---

**Generated**: February 02, 2025  
**Project**: UniSync Collaborative Platform  
**Version**: 2025 Q1 Release
