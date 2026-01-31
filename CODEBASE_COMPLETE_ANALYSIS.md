# UniSync - Complete Codebase Analysis

## Project Overview

**UniSync** is a Django-based web application designed to connect university students for collaboration on projects. It provides social networking, project management, and real-time messaging features.

**Repository:** https://github.com/Goku0090/uni  
**Environment:** Django 4.2.8 with PostgreSQL/SQLite  
**Python Version:** 3.8+

---

## 1. Technology Stack

### Core Framework
- **Django 4.2.8** - Web framework
- **Django REST Framework 3.14.0** - API endpoints
- **Python 3.8+** - Language

### Database & ORM
- **PostgreSQL** (Production) / **SQLite** (Development)
- **psycopg2-binary 2.9.9** - PostgreSQL adapter
- **dj-database-url 2.1.0** - Database URL parsing

### Authentication & Social Login
- **django-allauth 0.61.1** - User authentication
  - Google OAuth2
  - GitHub OAuth2
- **requests 2.31.0** - HTTP requests
- **requests-oauthlib 1.3.1** - OAuth support

### Email Services (Multi-backend)
1. **Brevo API** (Recommended for production)
   - `accounts.brevo_mail_backend.BrevoMailBackend`
   - Used for transactional emails and OTP
2. **ZeptoMail** (Alternative)
   - `accounts.zepto_mail_backend.ZeptoMailBackend`
3. **Gmail SMTP** (Fallback)
   - Standard Django SMTP backend
4. **Console Backend** (Development)
   - Prints OTP to console

### Real-time Features
- **Django Channels 4.0.0** - WebSocket support
- **channels-redis 4.1.0** - Redis backend for channels
- **redis 5.0.1** - In-memory cache/session store
- **django-redis 5.4.0** - Redis caching

### File Storage & Media
- **Pillow 10.1.0** - Image processing
- **boto3 1.34.34** - AWS S3 integration
- **django-storages 1.14.2** - Cloud storage backend

### Data Processing
- **pandas 2.1.4** - Data manipulation
- **openpyxl 3.1.2** - Excel file handling
- **NLTK 3.8.1** - Natural Language Processing

### External APIs
- **RapidAPI 1.0.0** - API aggregation (University search)

### Development & Deployment
- **gunicorn 21.2.0** - Production WSGI server
- **whitenoise 6.6.0** - Static file serving
- **django-cors-headers 4.3.1** - CORS support
- **django-debug-toolbar 4.2.0** - Development debugging
- **django-extensions 3.2.3** - Management commands

### Testing & Code Quality
- **pytest 7.4.3** - Testing framework
- **pytest-django 4.7.0** - Django integration
- **selenium 4.16.0** - Browser testing
- **black 23.12.1** - Code formatter
- **flake8 6.1.0** - Linter
- **isort 5.13.2** - Import sorter
- **mypy 1.7.1** - Type checking

### Monitoring & Logging
- **sentry-sdk 1.38.0** - Error tracking
- **django-performance-monitor 0.1.1** - Performance monitoring

### Documentation
- **sphinx 7.2.6** - Documentation generator
- **sphinx-rtd-theme 2.0.0** - ReadTheDocs theme
- **drf-spectacular 0.26.5** - OpenAPI/Swagger documentation

### Other Utilities
- **python-dotenv 1.0.0** - Environment variable management
- **django-filter 23.5** - Advanced filtering
- **django-crispy-forms 2.1** - Form rendering
- **crispy-bootstrap5 0.7** - Bootstrap 5 integration
- **celery 5.3.4** - Async task queue

---

## 2. Project Structure

```
auth_project/
├── auth_project/              # Main Django settings
│   ├── settings.py           # Configuration file
│   ├── urls.py               # Main URL routing
│   ├── wsgi.py               # WSGI entry point
│   ├── asgi.py               # ASGI entry point (WebSockets)
│   └── __init__.py
│
├── accounts/                  # Main application
│   ├── models.py            # Data models
│   ├── views.py             # View logic
│   ├── urls.py              # URL routes
│   ├── forms.py             # Form definitions
│   ├── serializers.py       # DRF serializers
│   ├── permissions.py       # Custom permissions
│   ├── utils.py             # Utility functions
│   ├── views_contact.py     # Contact form views
│   │
│   ├── services/            # Business logic
│   ├── migrations/          # Database migrations
│   ├── templates/           # HTML templates
│   ├── templatetags/        # Custom template tags
│   ├── static/              # CSS, JS, images
│   │
│   ├── brevo_mail_backend.py    # Brevo email backend
│   ├── zepto_mail_backend.py    # ZeptoMail backend
│   ├── chat_api.py              # Chat REST API
│   ├── chat_api_improved.py     # Improved chat API
│   └── tests.py             # Unit tests
│
├── logs/                      # Application logs
├── media/                     # User uploads (profile photos, files)
├── static/                    # Static assets
├── staticfiles/               # Collected static files (production)
│
├── manage.py                  # Django management CLI
├── requirements.txt           # Python dependencies
├── .env                       # Environment variables (secret)
├── .env.template             # Template for .env
├── db.sqlite3                # SQLite database (dev)
└── render.yaml               # Render.com deployment config
```

---

## 3. Core Data Models

### 3.1 User & Profile Models

#### **StudentProfile**
Extended user profile for detailed student information.

```python
Fields:
- user (OneToOneField) - Link to Django User
- full_name (CharField)
- college (CharField)
- other_college (CharField)
- location (CharField)
- interests (JSONField) - Array of interests
- bio (TextField)
- profile_photo (ImageField)
- skills (JSONField) - Technical skills
- project_interests (JSONField)
- role_preference (CharField)
- github, linkedin, portfolio, behance (URLFields)
- profile_completed (BooleanField)
- created_at, updated_at (DateTimeField)

Methods:
- get_display_name() - Return full name or username
```

#### **OTP (One-Time Password)**
Authentication via email OTP.

```python
Fields:
- email (EmailField)
- otp_code (CharField) - 6-digit code
- purpose (CharField) - 'login', 'registration', 'reset'
- is_used (BooleanField)
- created_at, expires_at (DateTimeField)

Methods:
- is_valid() - Check expiry & used status
- verify_otp() - Validate OTP code
- generate_otp() - Create new OTP

Properties:
- Expires in 5 minutes
- Old OTPs auto-deactivated on new generation
```

### 3.2 Social & Connection Models

#### **Connection**
User-to-user connection requests.

```python
Fields:
- sender (ForeignKey to User)
- receiver (ForeignKey to User)
- status (CharField) - 'pending', 'accepted', 'rejected'
- created_at, updated_at (DateTimeField)

Constraints:
- unique_together: ['sender', 'receiver']
```

#### **Follow**
User follow relationships.

```python
Fields:
- follower (ForeignKey to User)
- following (ForeignKey to User)
- created_at (DateTimeField)

Constraints:
- unique_together: ['follower', 'following']
```

### 3.3 Messaging Models

#### **Message**
Direct and group messages.

```python
Fields:
- sender (ForeignKey to User)
- receiver (ForeignKey to User) - For direct messages
- chat_room (ForeignKey to ChatRoom) - For group chats
- content (TextField)
- message_type (CharField) - 'text', 'file', 'image', 'call'
- call_type (CharField) - 'voice', 'video'
- reply_to (ForeignKey) - For threading
- created_at, updated_at (DateTimeField)

Methods:
- mark_as_read_by(user) - Record read status
- is_read_by(user) - Check if user read
- get_read_by_users() - Get all readers
- get_read_count() - Count readers
- get_unread_users() - Get non-readers
```

#### **ChatRoom**
Group chat containers.

```python
Fields:
- name (CharField)
- description (TextField)
- owner (ForeignKey to User)
- chat_type (CharField) - 'direct', 'group', 'project'
- is_archived (BooleanField)
- created_at, updated_at (DateTimeField)

Relations:
- members (through ChatRoomMember)
- messages (related_name='messages')
```

#### **ChatRoomMember**
Membership in chat rooms.

```python
Fields:
- chat_room (ForeignKey)
- user (ForeignKey)
- is_active (BooleanField)
- role (CharField) - 'admin', 'member'
- joined_at (DateTimeField)
```

#### **MessageReadStatus**
Track which users read which messages.

```python
Fields:
- message (ForeignKey to Message)
- user (ForeignKey to User)
- read_at (DateTimeField)

Constraints:
- unique_together: ['message', 'user']
```

#### **MessageReaction**
Emoji/reaction responses to messages.

```python
Fields:
- message (ForeignKey)
- user (ForeignKey)
- reaction (CharField) - Emoji or text
- created_at (DateTimeField)

Constraints:
- unique_together: ['message', 'user', 'reaction']
```

#### **File & MessageFile**
File attachments.

```python
File Fields:
- user (ForeignKey)
- file (FileField)
- filename (CharField)
- file_size (PositiveIntegerField)
- file_type (CharField)
- uploaded_at (DateTimeField)

MessageFile Fields:
- message (ForeignKey)
- file (ForeignKey)
- uploaded_at (DateTimeField)
```

### 3.4 Project & Collaboration Models

#### **Project**
Project postings for collaboration.

```python
Fields:
- user (ForeignKey to User) - Owner
- title (CharField)
- description (TextField)
- technologies (TextField) - CSV list
- looking_for (TextField) - Needed roles
- category (CharField)
- timeline (CharField)
- collaboration_needs (TextField)
- github_link (URLField)
- thumbnail (ImageField)
- is_pinned (BooleanField)
- created_at, updated_at (DateTimeField)

Relations:
- comments (related_name='comments')
- likes (through Like)
- team_members (through ProjectMember)
- invitations (through ProjectInvitation)
- tasks (through ProjectTask)
- milestones (through ProjectMilestone)
```

#### **ProjectMember**
Team membership in projects.

```python
Fields:
- project (ForeignKey)
- user (ForeignKey)
- role (CharField) - 'owner', 'admin', 'contributor', 'viewer'
- is_active (BooleanField)
- joined_at (DateTimeField)

Permissions:
- can_manage_project (owner/admin)
- can_invite_members (owner/admin)
- can_manage_tasks (owner/admin/contributor)
- can_edit_project (owner/admin/contributor)
```

#### **ProjectTask**
Tasks within projects.

```python
Fields:
- project (ForeignKey)
- title, description (CharField, TextField)
- assigned_to, assigned_by (ForeignKey to User)
- status (CharField) - 'todo', 'in_progress', 'review', 'completed', 'cancelled'
- priority (CharField) - 'low', 'medium', 'high', 'urgent'
- due_date (DateField)
- completed_at (DateTimeField)
- created_at, updated_at (DateTimeField)

Methods:
- mark_completed() - Mark as done
```

#### **ProjectMilestone**
Project milestones.

```python
Fields:
- project (ForeignKey)
- title, description (CharField, TextField)
- due_date (DateField)
- is_completed (BooleanField)
- completed_at (DateTimeField)
- completed_by (ForeignKey to User)
- created_at, updated_at (DateTimeField)

Methods:
- mark_completed(user) - Complete milestone
```

#### **ProjectInvitation**
Invitations to join projects.

```python
Fields:
- project, invited_user, invited_by (ForeignKey)
- role (CharField)
- message (TextField)
- status (CharField) - 'pending', 'accepted', 'declined', 'expired'
- created_at, expires_at, responded_at (DateTimeField)

Methods:
- accept() - Accept invitation
- decline() - Decline invitation
```

### 3.5 Social Features Models

#### **Like**
Project likes.

```python
Fields:
- user (ForeignKey)
- project (ForeignKey)
- created_at (DateTimeField)

Constraints:
- unique_together: ['user', 'project']
```

#### **Comment**
Project comments.

```python
Fields:
- user (ForeignKey)
- project (ForeignKey)
- content (TextField)
- created_at, updated_at (DateTimeField)
```

#### **Activity**
User activity feed.

```python
Fields:
- user (ForeignKey)
- activity_type (CharField) - Multiple types
- title, description (CharField, TextField)
- project, target_user, connection (ForeignKey)
- is_public (BooleanField)
- created_at (DateTimeField)

Activity Types:
- profile_updated
- project_created
- project_liked
- connection_made
- message_sent
- comment_added
- user_followed
- task_completed
- milestone_completed
```

#### **UserStats**
User statistics dashboard.

```python
Fields:
- user (OneToOneField)
- projects_created, connections_made, likes_received
- comments_made, projects_joined, tasks_completed
- followers_count, following_count
- last_updated (DateTimeField)

Methods:
- update_stats() - Recalculate all statistics
```

#### **Notification**
User notifications.

```python
Fields:
- user (ForeignKey)
- sender (ForeignKey)
- notification_type (CharField)
- title, message (CharField, TextField)
- is_read (BooleanField)
- created_at (DateTimeField)

Notification Types:
- connection_request, message, project_update
- comment, like, milestone_update
```

---

## 4. Authentication & Authorization

### 4.1 Authentication Methods

#### **OTP-based Email Authentication**
```python
Flow:
1. User enters email on login page
2. System generates 6-digit OTP
3. Email sent via configured backend (Brevo/ZeptoMail/SMTP)
4. OTP expires in 5 minutes
5. User enters OTP on verification page
6. Session created upon verification

Key Files:
- send_otp_email() in views.py
- OTP model in models.py
- verify_otp_view() in views.py
```

#### **Social Authentication (Allauth)**
```python
Providers:
- Google OAuth2
- GitHub OAuth2

Configuration:
- SOCIALACCOUNT_AUTO_SIGNUP = True
- SOCIALACCOUNT_LOGIN_ON_GET = True
- Custom form: CustomSocialSignupForm

Environment Variables:
- GOOGLE_CLIENT_ID, GOOGLE_CLIENT_SECRET
- GITHUB_CLIENT_ID, GITHUB_CLIENT_SECRET
```

### 4.2 Permission System

```python
DRF Defaults:
- DEFAULT_PERMISSION_CLASSES: AllowAny
- DEFAULT_AUTHENTICATION_CLASSES: SessionAuthentication

Custom Permissions (permissions.py):
- IsOwnerOrReadOnly - For owned objects
- IsProjectMember - For team members
- CanInviteToProject - For admin/owner
```

### 4.3 Authorization Backend

```python
AUTHENTICATION_BACKENDS = (
    'django.contrib.auth.backends.ModelBackend',  # Default
    'allauth.account.auth_backends.AuthenticationBackend',  # Allauth
)
```

---

## 5. Email Configuration

### 5.1 Email Backend Selection Logic

```python
Priority Order:
1. Brevo API (if BREVO_API_KEY set)
   - Backend: accounts.brevo_mail_backend.BrevoMailBackend
   - Recommended for production

2. ZeptoMail (if ZEPTO_MAIL_API_KEY + ZEPTO_MAIL_TOKEN set)
   - Backend: accounts.zepto_mail_backend.ZeptoMailBackend
   - Alternative service

3. Gmail SMTP (if EMAIL_HOST_USER + EMAIL_HOST_PASSWORD set)
   - Backend: django.core.mail.backends.smtp.EmailBackend
   - EMAIL_HOST: smtp.gmail.com
   - EMAIL_PORT: 587
   - EMAIL_USE_TLS: True
   - Fallback option

4. Console Backend (default for development)
   - Backend: django.core.mail.backends.console.EmailBackend
   - OTP printed to console
```

### 5.2 OTP Email Template

```html
HTML Email with:
- Logo & branding (🚀 Team)
- OTP code in large, centered box
- Blue background (#007bff)
- 5-minute expiry notice
- Security warning about sharing OTP
- Plain text alternative for compatibility
```

### 5.3 Email Configuration Variables

```env
DEFAULT_FROM_EMAIL=noreply@unisync.app
BREVO_API_KEY=[API key from Brevo]
ZEPTO_MAIL_API_KEY=[API key from ZeptoMail]
ZEPTO_MAIL_TOKEN=[Token from ZeptoMail]
EMAIL_HOST_USER=[Gmail address]
EMAIL_HOST_PASSWORD=[Gmail app password]
```

---

## 6. Database Configuration

### 6.1 PostgreSQL (Production)

```python
# Uses environment variable: DATABASE_URL
# Automatically parsed by dj-database-url

Example:
postgres://user:password@localhost:5432/unisync_db

Settings:
- CONN_MAX_AGE = 600 (persistent connections)
- SSLMODE from env (prefer/require)
```

### 6.2 SQLite (Development)

```python
# Fallback if DATABASE_URL not set
# Location: auth_project/db.sqlite3

Used when:
- DATABASE_URL not configured
- DB credentials incomplete
```

### 6.3 Database Selection Logic

```python
if DATABASE_URL:
    # Render/Production PostgreSQL
    import dj_database_url
    DATABASES = dj_database_url.parse(DATABASE_URL, conn_max_age=600)
elif all([DB_NAME, DB_USER, DB_PASSWORD]):
    # Local PostgreSQL
    DATABASES = PostgreSQL with env vars
else:
    # SQLite fallback
    DATABASES = SQLite (db.sqlite3)
```

---

## 7. Settings Configuration

### 7.1 Security Settings

```python
DEBUG = os.getenv('DEBUG', 'True').lower() in ('true', '1', 't', 'yes')
SECRET_KEY = os.getenv('SECRET_KEY') or secrets.token_urlsafe(50)
ALLOWED_HOSTS = os.getenv('ALLOWED_HOSTS', 'localhost,127.0.0.1').split(',')

SSL/Security:
SECURE_SSL_REDIRECT = False (unless env set)
SESSION_COOKIE_SECURE = False (unless env set)
CSRF_COOKIE_SECURE = False (unless env set)

CSRF Middleware:
- Re-enabled for security
- Requires CSRF token in POST forms
```

### 7.2 Installed Apps

```python
Django Built-in:
- admin, auth, contenttypes, sessions, messages, staticfiles
- sites, humanize

Project Apps:
- accounts (main application)

Third-party:
- allauth + social providers (Google, GitHub)
- rest_framework
- corsheaders, extensions, debug_toolbar, filter, crispy_forms
```

### 7.3 Middleware Stack

```python
1. SecurityMiddleware
2. SessionMiddleware
3. CommonMiddleware
4. CsrfViewMiddleware (CSRF Protection)
5. AuthenticationMiddleware
6. MessageMiddleware
7. XFrameOptionsMiddleware
8. allauth.account.middleware.AccountMiddleware
```

### 7.4 Templates Configuration

```python
BACKEND: DjangoTemplates
DIRS: [BASE_DIR.parent / 'templates']
APP_DIRS: True

Context Processors:
- debug, request, auth, messages
```

### 7.5 Static Files

```python
STATIC_URL = '/static/'
STATICFILES_DIRS = [BASE_DIR / 'static']
STATIC_ROOT = BASE_DIR / 'staticfiles'

Whitenoise middleware for production serving.
```

### 7.6 Media Files

```python
MEDIA_URL = '/media/'
MEDIA_ROOT = BASE_DIR / 'media'

Stores:
- Profile photos (profile_photos/)
- Chat files (chat_files/)
- User uploads
```

---

## 8. REST API Endpoints

### 8.1 Chat & Messaging APIs

```
Chat Room Management:
POST   /chat-rooms/                    - Create chat room
GET    /chat-rooms/                    - List rooms
GET    /chat-rooms/<id>/               - Room details
GET    /chat-rooms/<room_id>/members/  - Room members

Direct Messages:
POST   /direct-message/                - Start direct message

Messages:
POST   /messages/                      - Create message
GET    /messages/                      - List messages
GET    /messages/<pk>/                 - Message details
GET    /messages/search/               - Search messages
GET    /messages/<message_id>/status/  - Read status
POST   /messages/<message_id>/reactions/ - Add reaction

Conversations:
GET    /conversations/                 - List all conversations

Drafts:
GET    /drafts/                        - List draft messages

Typing:
POST   /typing/                        - Send typing indicator
```

### 8.2 User Profile APIs

```
Profiles:
GET    /user-profile/<user_id>/        - Get user profile
POST   /user-stats/                    - Get user statistics

Username/Email:
POST   /check-username/                - Check availability
POST   /check-email/                   - Check availability

NLP Analysis:
POST   /nlp-analyze/                   - Analyze interests with NLP
```

### 8.3 College Search API

```
GET    /college-search/                - Search colleges
POST   /validate-college/              - Validate college name
```

### 8.4 Authentication APIs

```
Login:
POST   /login/                         - Email/username login
POST   /verify-otp/                    - Verify OTP
POST   /resend-otp/                    - Resend OTP

Registration:
POST   /register/                      - Register new user

Password Reset:
POST   /forgot-password/               - Request reset
POST   /reset-password/                - Complete reset

Logout:
POST   /logout/                        - End session
```

---

## 9. View Functions & Controllers

### 9.1 Authentication Views

```python
Functions:
- register_view() - Handle registration with profile setup
- login_view() - Email-based login with OTP
- verify_otp_view() - Validate OTP code
- resend_otp_view() - Generate new OTP
- logout_view() - End session
- forgot_password_view() - Password reset request
- reset_password_view() - Update password after verification
```

### 9.2 User Profile Views

```python
Functions:
- student_profile() - View own profile
- edit_profile() - Edit profile and avatar
- student_details_view() - Set up profile details
- user_profile(username) - View other users' profiles
- user_profile_api(user_id) - API endpoint for profile
```

### 9.3 Project Views

```python
Functions:
- post_project() - Create/list projects
- edit_project(project_id) - Edit project details
- delete_project(project_id) - Remove project
- project_detail(project_id) - View project with comments
- search_projects(q) - Search by title/description
- like_project(project_id) - Toggle like status

Team Management:
- invite_to_team(project_id) - Send team invitation
- respond_to_team_invitation(invitation_id) - Accept/decline
- remove_team_member(project_id, user_id) - Kick member
```

### 9.4 Collaboration Views

```python
Functions:
- find_collaborators(q) - Search and suggest collaborators
- connect_view(user_id) - Send connection request
- send_connection_request(user_id) - API for connection
- accept_connection(connection_id) - Approve request
- reject_connection(connection_id) - Decline request
- cancel_connection_request(connection_id) - Cancel own request
- my_connections() - List accepted connections
```

### 9.5 Messaging Views

```python
Functions:
- message_view() - View direct messages inbox
- chat_view(user_id) - Chat with specific user
- enhanced_messages_view() - Group chat inbox
- enhanced_chat_view(room_id) - Group chat view
- create_group_chat() - Create new group
- add_reaction(message_id) - Add emoji reaction
- start_call(room_id) - Initiate call
- download_file(file_id) - Download attached file
```

### 9.6 Activity & Social Views

```python
Functions:
- activity_feed() - User activity stream
- notifications_view() - View notifications
- mark_notification_read(notification_id) - Mark read
- follow_user(user_id) - Follow/unfollow user
```

### 9.7 Dashboard & Main Views

```python
Functions:
- main() / main_home() - Home page
- dashboard_view() - Dashboard (redirects to main)
- help_center_view() - Help/support page
```

---

## 10. Key Utilities & Services

### 10.1 StudentProfileNLP (utils.py)

NLP-based profile matching and similarity scoring.

```python
Features:
- Interest analysis using NLTK
- Keyword extraction
- Similarity scoring between profiles
- Recommendation engine

Methods:
- calculate_profile_similarity()
- find_matching_interests()
- extract_skills()
```

### 10.2 Form Definitions (forms.py)

```python
RegisterForm - Registration with validation
LoginForm - Email/username login
OTPVerificationForm - OTP entry
StudentProfileForm - Profile editing
ProjectForm - Project creation/editing
CustomSocialSignupForm - Social auth signup
```

### 10.3 Serializers (serializers.py)

```python
UserProfileSerializer - User profile data
ProjectSerializer - Project information
MessageSerializer - Message data
ConnectionSerializer - Connection status
```

---

## 11. Logging Configuration

### 11.1 Log Handlers

```python
Console Handler:
- Format: [LEVEL] message
- Real-time output

File Handler (logs/django.log):
- Rotating: 10 MB max, 5 backups
- Format: [LEVEL] timestamp name funcName:lineno - message

Error File Handler (logs/error.log):
- Only ERROR level and above
- Rotating: 10 MB max, 5 backups

Auto-creates logs/ directory if missing
```

### 11.2 Logger Configuration

```python
'django' logger:
- Handlers: console, file, error_file
- Level: INFO

'accounts' logger:
- Handlers: console, file
- Level: DEBUG (dev), INFO (prod)
```

---

## 12. Important Security Considerations

### 12.1 CSRF Protection

```python
CSRF Middleware: Enabled
- POST, PUT, DELETE require CSRF token
- Token in forms or headers (X-CSRFToken)
```

### 12.2 SQL Injection Prevention

```python
- Uses Django ORM (parameterized queries)
- Never concatenates user input in queries
- Model methods handle complex queries safely
```

### 12.3 XSS Prevention

```python
Sanitization:
- Input sanitization function in views.py
- strip_tags() for HTML removal
- Template auto-escaping enabled
- {{variable}} automatically escaped
```

### 12.4 Password Security

```python
Password Validators:
- Minimum 8 characters
- At least one uppercase letter
- At least one digit
- Not similar to username/email
- Not in common password list
```

### 12.5 OTP Security

```python
- 6-digit random code
- Expires in 5 minutes
- Auto-deactivated on new generation
- Hashing available (not currently used)
- Never exposed in logs
```

### 12.6 Session Security

```python
Django Sessions:
- Secure cookie handling
- HTTPS-only in production (if enabled)
- HTTPOnly flag set
- Expires on logout
```

---

## 13. Deployment Configuration

### 13.1 Render.com Deployment (render.yaml)

```yaml
Configuration provided for:
- Build command
- Start command
- Environment variables
- PostgreSQL service
```

### 13.2 Production WSGI Server

```
gunicorn auth_project.wsgi:application
- Worker class: sync
- Workers: 4 (configurable)
- Timeout: 30 seconds
- Port: 8000 (mapped to 80/443)
```

### 13.3 Static File Serving

```
Whitenoise Middleware:
- Serves static files directly from Django
- Gzip compression enabled
- Cache headers optimized
- No separate web server needed
```

### 13.4 Environment Variables (Production)

```env
DJANGO_SETTINGS_MODULE=auth_project.settings
DEBUG=False
SECRET_KEY=[long random string]
ALLOWED_HOSTS=yourdomain.com,www.yourdomain.com
DATABASE_URL=postgresql://...
SECURE_SSL_REDIRECT=True
SESSION_COOKIE_SECURE=True
CSRF_COOKIE_SECURE=True
BREVO_API_KEY=[api key]
GOOGLE_CLIENT_ID=[oauth id]
GOOGLE_CLIENT_SECRET=[oauth secret]
GITHUB_CLIENT_ID=[oauth id]
GITHUB_CLIENT_SECRET=[oauth secret]
RAPIDAPI_KEY=[api key]
```

---

## 14. Database Migrations

### 14.1 Migration System

```python
Migrations stored in: accounts/migrations/
- Django auto-tracks schema changes
- Reversible migrations
- Version control friendly

Commands:
python manage.py makemigrations  # Create migrations
python manage.py migrate         # Apply migrations
python manage.py showmigrations  # View status
```

### 14.2 Key Models

All core models have migrations:
- StudentProfile
- OTP
- Project, ProjectTask, ProjectMilestone
- Message, ChatRoom, ChatRoomMember
- Connection, Follow, Like, Comment
- Activity, UserStats, Notification
- File, MessageFile, MessageReaction

---

## 15. Testing Structure

### 15.1 Test Files

```
accounts/tests.py - Unit tests
pytest.ini - Pytest configuration

Test Coverage:
- User authentication
- OTP generation & verification
- Profile CRUD
- Connection requests
- Message operations
- Project management
```

### 15.2 Testing Commands

```bash
pytest                          # Run all tests
pytest accounts/tests.py        # Run app tests
pytest -v                       # Verbose output
pytest --cov                    # Coverage report
python manage.py test           # Django test runner
```

---

## 16. Common Operations

### 16.1 User Registration Flow

```
1. User submits registration form (register_view)
2. Basic validation (username, email, password)
3. UserProfile created
4. OTP generated & sent via email
5. User verifies OTP (verify_otp_view)
6. User details form (student_details_view)
7. Account fully activated
```

### 16.2 OTP Login Flow

```
1. User enters email (login_view)
2. OTP generated & sent (send_otp_email)
3. User enters OTP (verify_otp_view)
4. Django session created
5. User redirected to dashboard
6. OTP marked as used
```

### 16.3 Project Collaboration Flow

```
1. User creates project (post_project)
2. Project posted to feed
3. Other users send connection request
4. Project owner invites to team (invite_to_team)
5. User accepts invitation (respond_to_team_invitation)
6. User becomes team member with role
7. Tasks assigned, progress tracked
8. Milestones set and completed
```

### 16.4 Real-time Messaging Flow

```
1. User opens chat (chat_view or enhanced_chat_view)
2. WebSocket connection established (Django Channels)
3. Message sent to database
4. MessageReadStatus created on viewing
5. Reactions added/removed
6. Files uploaded and linked
7. Message appears in activity feed
```

---

## 17. Performance Optimizations

### 17.1 Caching

```python
- Django cache framework configured
- Redis backend (if redis available)
- Cache decorators: @cache_page()
- Query optimization with select_related()
```

### 17.2 Database Optimization

```python
- Indexed foreign keys
- Unique constraints to prevent duplicates
- Proper pagination (10-100 items per page)
- Query analysis with django-debug-toolbar
```

### 17.3 File Uploads

```python
- Image validation (jpg, jpeg, png, gif only)
- File size limits (via validators)
- Media path organization
- Optional S3 storage (boto3 configured)
```

---

## 18. Frontend Integration

### 18.1 Template Rendering

```
Static Directory: auth_project/static/
Template Directory: templates/

Crispy Forms:
- Form rendering with Bootstrap 5
- Automatic field styling
- CSRF token injection
```

### 18.2 API Response Format

```json
Success Response:
{
  "success": true,
  "data": {...},
  "message": "Operation successful"
}

Error Response:
{
  "success": false,
  "error": "Error description",
  "code": "error_code"
}
```

### 18.3 WebSocket Integration (Channels)

```python
- Real-time message delivery
- Typing indicators
- Read status updates
- Active user lists

ASGI: asgi.py
```

---

## 19. Known Issues & Limitations

### 19.1 Current Issues

```
1. OLD model names still used in some places:
   - ProjectTeam vs ProjectMember
   - ProjectTeamMember vs ProjectMember
   - ProjectTeamInvitation vs ProjectInvitation
   - Aliases created for backward compatibility

2. Chat API has both old and improved versions:
   - chat_api.py (original)
   - chat_api_improved.py (refactored)
   - Both imported and potentially conflicting

3. Views.py has duplicate definitions:
   - dashboard_view appears twice
   - Some views may be incomplete (truncated)
```

### 19.2 Limitations

```
1. OTP hardcoded to 5-minute expiry
2. No rate limiting on OTP requests
3. Message read status requires manual database queries
4. No image compression for uploads
5. No automatic cleanup of expired OTPs
```

---

## 20. Development Workflow

### 20.1 Local Setup

```bash
# Clone repository
git clone https://github.com/Goku0090/uni.git
cd auth_project

# Create virtual environment
python -m venv venv
source venv/Scripts/activate  # Windows

# Install dependencies
pip install -r requirements.txt

# Configure environment
cp .env.template .env
# Edit .env with your settings

# Create databases
python manage.py migrate

# Create superuser (optional)
python manage.py createsuperuser

# Run development server
python manage.py runserver
```

### 20.2 Making Changes

```bash
# Create migrations
python manage.py makemigrations

# Apply migrations
python manage.py migrate

# Run tests
pytest

# Format code
black accounts/
isort accounts/

# Check quality
flake8 accounts/
mypy accounts/
```

### 20.3 Deployment

```bash
# Collect static files
python manage.py collectstatic --noinput

# Run migrations on production
python manage.py migrate

# Start gunicorn
gunicorn auth_project.wsgi:application
```

---

## 21. File Organization Summary

| Directory | Purpose |
|-----------|---------|
| `auth_project/` | Django configuration and settings |
| `accounts/` | Main application (models, views, URLs) |
| `accounts/services/` | Business logic and utilities |
| `accounts/migrations/` | Database schema versions |
| `accounts/templates/` | HTML templates |
| `accounts/static/` | CSS, JavaScript, images |
| `accounts/templatetags/` | Custom template filters/tags |
| `logs/` | Application logs |
| `media/` | User uploaded files |
| `static/` | App-wide static files |
| `staticfiles/` | Collected static (production) |

---

## 22. Key Contact Points for Customization

### 22.1 Adding New Features

```python
Models (accounts/models.py):
- Add new model class
- Add fields and relationships
- Create migration: makemigrations

Views (accounts/views.py):
- Add view function
- Add URL in accounts/urls.py
- Create template in accounts/templates/

Serializers (accounts/serializers.py):
- Add DRF serializer for API
- Register in views as ListCreateView, etc.

Forms (accounts/forms.py):
- Add Django Form class
- Use in views with form.is_valid()
```

### 22.2 Modifying Email Backend

```python
Update settings.py EMAIL_BACKEND selection logic
Implement custom backend inheriting from:
- django.core.mail.backends.base.BaseEmailBackend

Methods to implement:
- send(email_message)
- open()
- close()
```

### 22.3 Adding Social Providers

```python
In settings.py SOCIALACCOUNT_PROVIDERS:
1. Add provider configuration
2. Set CLIENT_ID and CLIENT_SECRET
3. Install provider: pip install django-allauth[provider]
4. Add to INSTALLED_APPS
5. Create OAuth app on provider platform
```

---

## 23. Architecture Decisions

### 23.1 Model Design

```
Benefits of current design:
- Normalized tables reduce redundancy
- Foreign keys maintain referential integrity
- JSONField for flexible data (interests, skills)
- Through models (ProjectMember) for relationships
- Status choices for state management

Trade-offs:
- More queries needed for complex data retrieval
- Potential N+1 query problems
- Care needed for cascading deletes
```

### 23.2 Authentication Strategy

```
OTP-based login chosen over passwords because:
- Reduces password compromise risk
- No password reset flow needed
- Works across devices
- Can be shared more easily than passwords
- 5-minute expiry balances security & UX

Email-only login simplifies:
- No username confusion
- Unique identifier (email)
- Standard verification method
```

### 23.3 Messaging Architecture

```
Separate models for:
- Message (content, metadata)
- ChatRoom (container)
- ChatRoomMember (membership)
- MessageReadStatus (scalable read tracking)
- MessageReaction (emoji responses)
- MessageFile (attachments)

Benefits:
- Scalable (read status not on message)
- Extensible (easy to add features)
- Clean separation of concerns
```

---

## Conclusion

UniSync is a comprehensive Django application with modern features for student collaboration. The codebase demonstrates solid architecture with models for authentication, social networking, project management, and real-time messaging. The multi-layered approach with models, views, serializers, and forms follows Django best practices.

Key strengths:
- Flexible email backend system
- Comprehensive permission/role system
- Scalable messaging architecture
- Social features (follows, connections, activity)
- Project collaboration tools

Areas for improvement:
- Deduplication of chat APIs
- Model naming consistency
- Rate limiting on OTP
- Automated cleanup of expired data
- N+1 query optimization
