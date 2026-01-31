# UniSync Codebase Analysis

## Project Overview
**UniSync** is a Django-based web application for student collaboration and project management. It enables students to connect, share projects, and collaborate on initiatives across different colleges.

**Tech Stack:**
- **Backend:** Django 4.2.8, Django REST Framework
- **Database:** PostgreSQL (production), SQLite (development)
- **Authentication:** Django Auth + django-allauth (Google/GitHub OAuth)
- **Email:** Brevo API, ZeptoMail, or Gmail SMTP
- **OTP:** Custom implementation (6-digit, 5-minute expiry)
- **Real-time:** Channels, Channels-Redis
- **Task Queue:** Celery
- **File Storage:** Boto3, Django-Storages (S3)
- **Caching:** Redis
- **Monitoring:** Sentry

---

## Architecture Overview

### Directory Structure
```
auth_project/
├── auth_project/          # Django project settings
│   ├── settings.py        # Configuration, installed apps, middleware
│   ├── urls.py            # Main URL routing
│   ├── wsgi.py            # WSGI application
│   └── asgi.py            # ASGI application
│
├── accounts/              # Main application
│   ├── models.py          # Core data models
│   ├── views.py           # Request handlers (1400+ lines)
│   ├── urls.py            # URL routing
│   ├── serializers.py     # REST API serializers
│   ├── forms.py           # Django forms
│   ├── permissions.py     # Custom permissions
│   ├── utils.py           # Helper utilities
│   ├── views_contact.py   # Contact/static pages
│   ├── chat_api.py        # REST API for messaging
│   ├── brevo_mail_backend.py    # Email backend (Brevo)
│   ├── zepto_mail_backend.py    # Email backend (ZeptoMail)
│   ├── services/
│   │   └── auth_service.py      # Welcome emails, password resets
│   ├── templates/         # HTML templates
│   ├── static/            # CSS, JS assets
│   ├── migrations/        # Database migrations
│   └── migrations/

├── logs/                  # Application logs
├── media/                 # User uploads (avatars, files)
├── static/                # CSS, JS assets
├── manage.py              # Django management CLI
└── requirements.txt       # Python dependencies
```

---

## Database Models (Comprehensive)

### Core User Models

#### 1. **StudentProfile**
Extends Django User with profile information
- **Fields:**
  - full_name, bio, college, location
  - interests, skills, project_interests (JSONField arrays)
  - Social links: github, linkedin, portfolio, behance
  - profile_photo (ImageField with validation)
  - profile_completed (bool)
- **Relations:** OneToOne with User
- **Key Methods:**
  - `get_display_name()` - Returns full name or username

#### 2. **OTP**
One-time passwords for authentication
- **Fields:**
  - email, otp_code (6-digit string)
  - purpose (login/registration/reset)
  - is_used (bool), expires_at (5-min expiry)
- **Key Methods:**
  - `is_valid()` - Check validity and expiration
  - `verify_otp(code)` - Verify code against stored code
  - `generate_otp(email, purpose)` - Create new OTP (deactivates old ones)
  - `hash_otp(code)` - SHA-256 hashing (unused currently)

### Social Interaction Models

#### 3. **Connection**
Connection requests between users
- **Fields:**
  - sender, receiver (ForeignKey to User)
  - status (pending/accepted/rejected)
- **Constraints:** Unique together on sender+receiver
- **Use Case:** User-to-user relationship networking

#### 4. **Message**
Direct and group messages
- **Fields:**
  - sender, receiver (nullable for group chats)
  - chat_room (ForeignKey for group chats)
  - content, message_type (text/file/image/call)
  - call_type (voice/video)
  - reply_to (self-referential for threading)
- **Key Methods:**
  - `mark_as_read_by(user)` - Uses MessageReadStatus model
  - `is_read_by(user)` - Check read status
  - `get_read_count()` - Count readers
  - `get_unread_users()` - For group chats

#### 5. **MessageReadStatus**
Tracks message read receipts by users
- **Fields:**
  - message, user, read_at (DateTime)
- **Purpose:** Scalable read status tracking for group chats

#### 6. **File**
File uploads in messages
- **Fields:**
  - user, file (FileField)
  - filename, file_size, file_type
- **Relations:** Used by MessageFile model

#### 7. **MessageFile**
Association between messages and files
- **Relations:** ForeignKey to Message, File

#### 8. **MessageReaction**
Emoji reactions on messages
- **Fields:**
  - message, user, reaction (emoji)
- **Constraints:** Unique on (message, user, reaction)

### Project Models

#### 9. **Project**
Collaborative projects
- **Fields:**
  - title, description (rich text)
  - owner (ForeignKey to User)
  - technologies, looking_for (comma-separated strings)
  - category, timeline, collaboration_needs
  - github_link, visibility (public/private/draft)
  - created_at, updated_at
- **Relations:** Multiple members via ProjectMember

#### 10. **ProjectMember**
Team members with role-based access
- **Fields:**
  - project, user
  - role (owner/admin/contributor/viewer)
  - is_active, joined_at
- **Key Properties:**
  - can_manage_project, can_invite_members
  - can_manage_tasks, can_edit_project
- **Constraints:** Unique on (project, user)

#### 11. **ProjectInvitation**
Invites to join projects
- **Fields:**
  - project, invited_user, invited_by
  - role, message, status
  - expires_at (auto-calculated)
- **Key Methods:**
  - `accept()` - Creates ProjectMember, marks status
  - `decline()` - Sets status to declined

#### 12. **ProjectTask**
Tasks within projects
- **Fields:**
  - project, title, description
  - assigned_to, assigned_by
  - status (todo/in_progress/review/completed/cancelled)
  - priority (low/medium/high/urgent)
  - due_date, completed_at
- **Key Methods:**
  - `mark_completed()` - Sets status and timestamp

#### 13. **ProjectMilestone**
Project milestones/phases
- **Fields:**
  - project, title, description
  - due_date, is_completed
  - completed_by (User who marked complete)
- **Key Methods:**
  - `mark_completed(user)` - Track who completed it

### Activity & Analytics Models

#### 14. **Comment**
Comments on projects
- **Fields:**
  - project, user
  - content, created_at

#### 15. **Like**
Project likes/favorites
- **Fields:**
  - project, user
- **Constraints:** Unique on (project, user)

#### 16. **Follow**
User follows
- **Fields:**
  - follower, following (both Users)
- **Constraints:** Unique on (follower, following)

#### 17. **Activity**
User activity feed
- **Fields:**
  - user, activity_type (8+ types)
  - title, description
  - Related: project, target_user, connection
  - is_public, created_at
- **Activity Types:** profile_updated, project_created, project_liked, connection_made, message_sent, comment_added, user_followed, task_completed, milestone_completed

#### 18. **UserStats**
Cached user statistics
- **Fields:**
  - projects_created, connections_made, likes_received
  - comments_made, projects_joined, tasks_completed
  - followers_count, following_count
  - last_updated
- **Key Methods:**
  - `update_stats()` - Aggregate counts from related models

### Communication Models

#### 19. **ChatRoom**
Group chat rooms
- **Fields:**
  - name, description, creator (User)
  - chat_type (direct/private/public)
  - members (ManyToMany through ChatRoomMember)
  - created_at, updated_at

#### 20. **ChatRoomMember**
Members in chat rooms
- **Fields:**
  - chat_room, user, joined_at

#### 21. **Notification**
User notifications
- **Fields:**
  - user, from_user
  - notification_type, title, message
  - related_object_id, related_object_type
  - is_read, created_at

#### 22. **UserStatus**
Online/offline status
- **Fields:**
  - user, is_online, last_seen

### Model Aliases
```python
ProjectTeam = ProjectMember
ProjectTeamMember = ProjectMember
ProjectTeamInvitation = ProjectInvitation
```
(For backward compatibility)

---

## Core Views & Features

### Authentication Views

#### `register_view(request)`
- **Method:** POST
- **Validation:**
  - Username/email/password required
  - Password strength: min 8 chars, uppercase, digit
  - Email uniqueness check
- **Process:**
  1. Validate inputs
  2. Create User & StudentProfile
  3. Send welcome email via AuthService
  4. Generate OTP for verification
  5. Redirect to OTP verification

#### `login_view(request)`
- **Method:** POST
- **Authentication:**
  - Email or username support
  - OTP-based (generate OTP, send email)
  - Redirect to OTP verification
- **Optional:** Social login via allauth (Google/GitHub)

#### `verify_otp_view(request, purpose)`
- **Validates OTP code from user**
- **On success:** Authenticates user, creates session
- **On failure:** Logs attempt, allows retry

#### `forgot_password_view(request)`
- **Generates password reset OTP**
- **Sends reset email via AuthService**

#### `reset_password_view(request)`
- **Validates reset OTP**
- **Updates password** after verification

### Profile Views

#### `student_details_view(request)`
- **Multi-step form for profile completion**
- **Fields:** full_name, college, location, interests, bio
- **Saves to StudentProfile model**

#### `student_profile(request)`
- **Display user's profile**
- **Shows:** profile_photo, interests, skills, social links
- **Connections:** display my connections

#### `user_profile(request, username)`
- **View other user's public profile**
- **Shows connection status**

#### `edit_profile(request)`
- **Edit profile & upload avatar**
- **Validates image extensions (jpg, jpeg, png, gif)**
- **Redirects to profile on success**

### Project Views

#### `post_project(request)`
- **Create new project**
- **Fields:** title, description, technologies, looking_for, category, timeline, github_link
- **Creates Activity record**
- **Shows user's projects list**

#### `edit_project(request, project_id)`
- **Update project details**
- **Only project owner can edit**

#### `delete_project(request, project_id)`
- **Delete project (owner only)**

#### `project_detail(request, project_id)`
- **View project with:**
  - Comments, like count
  - Team members, tasks, milestones
  - Collaboration options

#### `explore_projects_view(request)`
- **Public project feed with filtering**
- **Uses ProjectVisibilityFilter utility**

### Social Features

#### `find_collaborators(request)`
- **Search & filter users by:**
  - Full name, college, location
  - Interests, skills, project_interests
  - Role preference
- **Suggests profiles by interest matching**
- **Displays connection statuses**
- **Features:**
  - 1400+ lines
  - NLP-based matching (StudentProfileNLP class)
  - Match scoring algorithm

#### `like_project(request, project_id)`
- **Toggle like on project**
- **AJAX endpoint (JsonResponse)**
- **Creates Activity if new like**

#### `send_connection_request(request, user_id)`
- **Create Connection with status 'pending'**
- **Prevents duplicate connections**

#### `accept_connection(request, connection_id)`
- **Sets Connection status to 'accepted'**
- **Creates Activity**

#### `reject_connection(request, connection_id)`
- **Sets Connection status to 'rejected'**

#### `my_connections(request)`
- **List accepted connections**

#### `follow_user(request, user_id)`
- **Create Follow relationship**
- **Creates Activity**

### Messaging Views

#### `message_view(request)`
- **List all conversations**
- **Shows unread counts, last message**

#### `chat_view(request, user_id)`
- **Direct message interface**
- **Loads conversation history**
- **Marks messages as read**

#### `enhanced_messages_view(request)`
- **Group chat listing**

#### `enhanced_chat_view(request, room_id)`
- **Group chat interface**
- **Shows members, typing indicators**

#### `create_group_chat(request)`
- **Create new ChatRoom**
- **Add initial members**

#### `add_reaction(request, message_id)`
- **Add emoji reaction to message**

### Utility Views

#### `dashboard_view(request)`
- **Simplified to redirect to main_home**

#### `main_home(request)`
- **Main dashboard/feed**
- **Shows projects, notifications, statistics**

#### `notifications_view(request)`
- **List all notifications**
- **Filters read/unread**

#### `mark_notification_read(request, notification_id)`
- **AJAX endpoint to mark notification as read**

#### `activity_feed(request)`
- **Chronological activity feed**
- **Filters by user interests**

---

## REST API Endpoints

### Chat/Messaging APIs (DRF)

**Imports from `chat_api.py`:**
```
POST   /chat-rooms/               - Create chat room
GET    /chat-rooms/               - List chat rooms
GET    /chat-rooms/<id>/          - Get room details
GET    /chat-rooms/<id>/members/  - List room members

POST   /direct-message/           - Create direct message
GET    /messages/                 - List messages
POST   /messages/                 - Create message
GET    /messages/<id>/            - Get message
DELETE /messages/<id>/            - Delete message
GET    /messages/search/          - Search messages
GET    /messages/<id>/status/     - Get read status
GET    /messages/<id>/reactions/  - Get reactions
POST   /messages/<id>/reactions/  - Add reaction

GET    /conversations/            - List conversations
GET    /drafts/                   - List drafts
POST   /drafts/                   - Create draft
POST   /typing/                   - Send typing indicator
```

### User/Profile APIs

```
GET    /user-profile/<user_id>/   - Get user profile
GET    /college-search/           - Search colleges (RapidAPI)
POST   /validate-college/         - Validate college input
GET    /user-stats/               - Get user stats
GET    /nlp-analyze/              - NLP analysis (StudentProfileNLP)
GET    /check-username/           - Check username availability
GET    /check-email/              - Check email availability
```

---

## Key Utility Classes

### `StudentProfileNLP` (utils.py)
**Purpose:** NLP analysis for profile matching
- Methods likely used by `find_collaborators` for interest matching
- Helps score profile similarity

### `ProjectVisibilityFilter` (utils.py)
**Purpose:** Filter projects by visibility & user permissions
- Filters public/private/draft projects
- Ensures users only see projects they should

---

## Email System

### Configuration (settings.py)
**Priority:**
1. **Brevo** (Production recommended) - `BrevoMailBackend`
2. **ZeptoMail** - `ZeptoMailBackend`
3. **Gmail SMTP** - Standard Django backend
4. **Console** (Development) - For testing

### Email Backends

#### `brevo_mail_backend.py`
- Uses Brevo API (`BREVO_API_KEY`)
- Sends transactional emails
- Used for OTP, welcome, password reset

#### `zepto_mail_backend.py`
- Alternative backend using ZeptoMail API
- Fallback when Brevo unavailable

### Email Types (auth_service.py)

1. **Welcome Email** - Sent on registration
   - Plain text + HTML
   - Onboarding steps, call-to-action

2. **Welcome Back Email** - Sent on returning user login
   - Features highlights
   - Journey continuation messaging

3. **Password Reset Email** - Sent on forgot password
   - Reset link (24-hour expiry)
   - Security warning

4. **OTP Email** - Sent for login/registration/reset
   - 6-digit code, 5-minute expiry
   - Plain text + HTML with styling

---

## Security Features

### CSRF Protection
- Middleware enabled: `CsrfViewMiddleware`
- Forms include CSRF tokens
- API uses session authentication

### Authentication
- Django ModelBackend + AllAuth backend
- Email/username login support
- OTP-based verification
- Social login (Google, GitHub)

### Input Sanitization
```python
def sanitize_input(text, max_length=None):
    # Strips HTML tags, removes dangerous chars
    # Trims whitespace, applies length limits
```
Used in views for XSS prevention

### Password Validation
- Minimum 8 characters
- Requires uppercase letter
- Requires digit
- Custom validators in settings

### Image Validation
- StudentProfile.profile_photo restricted to: jpg, jpeg, png, gif
- Prevents arbitrary file uploads

### SSL/TLS
- `SECURE_SSL_REDIRECT` configurable
- `SESSION_COOKIE_SECURE` configurable
- `CSRF_COOKIE_SECURE` configurable

---

## Logging System

### Handlers
1. **Console** - Real-time logs to stdout
2. **File** - Rotating log file (10MB, 5 backups)
3. **Error File** - Separate error-level logs

### Loggers
- `django` - Framework logs (INFO+)
- `accounts` - App logs (DEBUG in dev, INFO in prod)

### Log Locations
- `logs/django.log` - General logs
- `logs/error.log` - Errors only

---

## Configuration Management

### Environment Variables (Required)
```
DEBUG                    # Dev/prod mode
SECRET_KEY              # Django secret
ALLOWED_HOSTS           # Comma-separated domains
DATABASE_URL            # Render PostgreSQL URL
BREVO_API_KEY          # Brevo email API key
GOOGLE_CLIENT_ID       # OAuth
GOOGLE_CLIENT_SECRET
GITHUB_CLIENT_ID
GITHUB_CLIENT_SECRET
RAPIDAPI_KEY           # College search API
```

### Database
- **Production:** PostgreSQL via DATABASE_URL (Render)
- **Development:** Defaults to SQLite if no DB env vars
- **Connection pooling:** conn_max_age=600 (10 min)

### Static Files
- **URL:** `/static/`
- **Root:** `staticfiles/` (generated by `collectstatic`)
- **Directories:** `static/`

### Media Files
- **URL:** `/media/`
- **Root:** `media/` (user uploads)

---

## Installed Apps & Middleware

### Key Apps
- `django.contrib.auth` - User management
- `django.contrib.contenttypes` - Generic relations
- `django.contrib.sessions` - Session management
- `allauth`, `allauth.account`, `allauth.socialaccount` - Auth
- `rest_framework` - API framework
- `accounts` - Main app

### Middleware Stack
1. SecurityMiddleware
2. SessionMiddleware
3. CommonMiddleware
4. CsrfViewMiddleware
5. AuthenticationMiddleware
6. MessageMiddleware
7. XFrameOptionsMiddleware
8. AccountMiddleware (Allauth)

---

## Development Utilities

### Testing Helpers
Multiple test scripts in project root:
- `test_login.py` - Login flow testing
- `test_email.py` - Email delivery testing
- `test_profile_fix.py` - Profile operations
- `test_filter.py` - Filtering logic
- `test_search.py` - Search functionality
- `test_connections.py` - Connection requests

### Debug Scripts
- `debug_filtering.py` - Filter debugging
- `debug_profiles.py` - Profile issues
- `debug_find_collaborators.py` - Collaborator search
- `debug_profile_photo.py` - Image handling

### Diagnostic Tools
- `performance_monitor.py` - Monitor app performance
- `check_profiles.py` - Validate profile data
- `create_test_profiles.py` - Bulk test data creation

---

## Dependencies Summary

### Core Framework
- Django 4.2.8
- DRF 3.14.0
- django-allauth 0.61.1

### Databases
- PostgreSQL (psycopg2-binary)
- SQLite (built-in)
- dj-database-url

### Email
- zeptomail
- requests (HTTP client)

### Real-time & Async
- channels 4.0.0
- channels-redis 4.1.0
- celery 5.3.4
- redis 5.0.1

### Data Processing
- pandas 2.1.4
- nltk 3.8.1
- openpyxl 3.1.2

### File Storage
- boto3 (S3)
- django-storages

### Security & Performance
- django-cors-headers
- whitenoise (static files)
- sentry-sdk (error tracking)

### Development
- django-debug-toolbar
- pytest, pytest-django
- black, flake8, isort, mypy

---

## Key Workflows

### Registration Flow
1. User fills registration form
2. Server validates inputs
3. User created with StudentProfile
4. Welcome email sent
5. OTP generated and sent
6. User redirected to OTP verification
7. On verification, user logged in
8. Redirected to profile completion

### Login Flow
1. User enters email/username
2. OTP generated and sent to registered email
3. User enters OTP
4. On verification, user logged in
5. Redirected to dashboard

### Project Creation
1. User fills project form
2. Project created with owner=current_user
3. Activity record created
4. Redirect to projects list
5. Other users can find, comment, like, request to join

### Collaboration
1. User searches for collaborators
2. Profiles scored by interest matching (NLP)
3. User sends connection request
4. Receiver accepts/rejects
5. Connected users can message, add to projects

### Messaging
1. User initiates chat (direct or group)
2. Messages stored with timestamps
3. Read status tracked via MessageReadStatus
4. Notifications created for new messages
5. Optional reactions and file attachments

---

## Performance Considerations

### Caching
- Redis for session cache
- django-redis backend
- Cache page decorator available

### Database
- Connection pooling (conn_max_age=600)
- Pagination: 10 items per page (MAX 100)
- Search filters for efficiency

### Async Tasks
- Celery for background jobs (email, notifications)
- Redis broker for Celery

### Static Files
- WhiteNoise for efficient serving
- S3 storage optional (boto3)

---

## Known Issues & Gaps

1. **OTP Hashing Unused** - `hash_otp()` method exists but not used
2. **Profile Photo Circular Import Risk** - Import structure in views.py (line 36)
3. **View Size** - views.py is 1400+ lines, consider splitting
4. **Duplicate URL Patterns** - accounts.urls included in main urls twice
5. **Database Fallback** - Automatic SQLite fallback might hide config issues
6. **Email Test Endpoints** - Multiple test scripts in root (should be in tests/)
7. **StudentProfileNLP** - Implementation details not visible (utils.py not fully read)

---

## Deployment Notes

### Production Checklist
- [ ] Set SECRET_KEY in environment
- [ ] Set DEBUG=False
- [ ] Configure DATABASE_URL (Render PostgreSQL)
- [ ] Set BREVO_API_KEY or email backend
- [ ] Configure OAuth (Google/GitHub)
- [ ] Run migrations: `python manage.py migrate`
- [ ] Collect statics: `python manage.py collectstatic --noinput`
- [ ] Use Gunicorn as WSGI server
- [ ] Enable SSL/TLS redirect
- [ ] Configure Redis for caching & Celery
- [ ] Set up error tracking (Sentry)

### Local Development
```bash
python manage.py runserver           # Start dev server
python manage.py makemigrations      # Create migrations
python manage.py migrate             # Apply migrations
python manage.py createsuperuser    # Create admin user
```

---

## Summary

**UniSync** is a comprehensive Django application supporting:
- Multi-factor authentication (OTP + social login)
- Rich user profiles with NLP-based matching
- Project management with team collaboration
- Messaging system with group chat support
- Activity feeds and notifications
- Multiple email providers (Brevo, ZeptoMail, Gmail)
- REST API for mobile/external integrations
- Real-time features via WebSockets (Channels)
- Background task processing (Celery)

The architecture is modular, scalable, and production-ready with comprehensive security, logging, and monitoring features.
