# UniSync Codebase - Comprehensive Analysis

**Generated:** January 29, 2026  
**Project:** UniSync - Student Collaboration Platform  
**Repository:** https://github.com/Goku0090/uni  
**Framework:** Django 4.2.8 + Django REST Framework 3.14.0

---

## 1. PROJECT OVERVIEW

UniSync is a Django-based **student collaboration platform** designed to help students find collaborators, post projects, and manage team collaborations. It features:
- **User authentication** with OTP-based verification
- **Social login** (Google, GitHub via django-allauth)
- **Project management** system with team collaboration
- **Messaging system** for user communication
- **Connection system** for networking between students
- **Activity feed** for tracking user actions
- **Email notifications** with multiple backend support (Brevo, ZeptoMail, Gmail)

---

## 2. PROJECT STRUCTURE

```
auth_project/
├── accounts/                      # Main app for user management
│   ├── models.py                  # Database models
│   ├── views.py                   # View handlers (1700+ lines)
│   ├── forms.py                   # Form definitions
│   ├── urls.py                    # URL routing
│   ├── serializers.py             # DRF serializers
│   ├── permissions.py             # Custom permissions
│   ├── utils.py                   # Utility functions
│   ├── brevo_mail_backend.py      # Brevo email backend
│   ├── zepto_mail_backend.py      # ZeptoMail backend
│   ├── chat_api.py                # Messaging API
│   ├── chat_api_improved.py       # Enhanced messaging
│   ├── views_contact.py           # Contact view handlers
│   ├── services/                  # Business logic
│   ├── static/                    # CSS/JS files
│   ├── templates/                 # HTML templates
│   ├── migrations/                # DB migration history
│   └── templatetags/              # Custom template tags
├── auth_project/                  # Django project settings
│   ├── settings.py                # Main configuration
│   ├── urls.py                    # Root URL routing
│   ├── wsgi.py                    # WSGI app entry point
│   └── asgi.py                    # ASGI app entry point
├── manage.py                      # Django management tool
├── requirements.txt               # Python dependencies
├── .env                           # Environment variables (SECRET - not readable)
└── db.sqlite3 / PostgreSQL        # Database (SQLite dev, PostgreSQL prod)
```

---

## 3. CORE MODELS

### **User-Related Models**

#### **StudentProfile**
Extends Django's User model with student-specific data:
```python
- user (OneToOne)                 # Links to Django User
- full_name, college, location    # Basic info
- interests, bio, skills          # Professional data
- project_interests, role_preference
- profile_photo                   # Avatar upload
- social_links (github, linkedin, portfolio, behance)
- profile_completed (Boolean)
- timestamps (created_at, updated_at)
```
**Purpose:** Store extended profile information beyond Django's User model

#### **OTP (One-Time Password)**
Handles authentication via OTP codes:
```python
- email                           # Target email
- otp_code                        # 6-digit code
- purpose (login|registration|reset)
- is_used, expires_at            # Validity tracking
- created_at, expires_at         # Time management
Methods:
  - is_valid()                    # Check expiry and usage
  - verify_otp(code)              # Verify provided code
  - generate_otp(email, purpose)  # Create new OTP
```
**Expiry:** 5 minutes from creation
**Purpose:** Enable passwordless/multi-factor authentication

---

### **Connection & Messaging Models**

#### **Connection**
Manages user-to-user connection requests:
```python
- sender, receiver (ForeignKey to User)
- status (pending|accepted|rejected)
- timestamps
Constraint: Unique pair (sender, receiver)
```

#### **Message**
Direct messaging between users:
```python
- sender, receiver (ForeignKey to User)
- chat_room (ForeignKey - for group chats)
- content (TextField)
- message_type (text|file|image|call)
- reply_to (Self-referential for threading)
- timestamps
Methods:
  - mark_as_read_by(user)
  - is_read_by(user)
  - get_read_by_users()
  - get_read_count()
```

#### **MessageReadStatus**
Tracks read receipts for scalability:
```python
- message (ForeignKey)
- user (ForeignKey)
- read_at (DateTimeField)
Constraint: Unique (message, user)
```

#### **MessageFile, MessageReaction**
- **MessageFile**: Attach files to messages
- **MessageReaction**: Emoji/reaction support on messages

---

### **Project Collaboration Models**

#### **Project**
Main project model:
```python
- user (ForeignKey - project owner)
- title, description
- technologies, looking_for (comma-separated or arrays)
- category (web|mobile|ai|data|blockchain|iot|game|...)
- timeline, collaboration_needs
- github_link
- status (active|completed|archived)
- visibility (public|private)
- image
- timestamps
```

#### **ProjectMember / ProjectTeam**
Team membership with roles:
```python
- project (ForeignKey)
- user (ForeignKey)
- role (owner|admin|contributor|viewer)
- is_active, joined_at
Properties:
  - can_manage_project
  - can_invite_members
  - can_manage_tasks
  - can_edit_project
```

#### **ProjectInvitation**
Invite users to projects:
```python
- project, invited_user, invited_by
- role, message
- status (pending|accepted|declined|expired)
- expires_at, responded_at
Methods:
  - accept()
  - decline()
```

#### **ProjectTask**
Task management within projects:
```python
- project (ForeignKey)
- title, description
- assigned_to, assigned_by
- status (todo|in_progress|review|completed|cancelled)
- priority (low|medium|high|urgent)
- due_date, completed_at
Method: mark_completed()
```

#### **ProjectMilestone**
Track project milestones:
```python
- project
- title, description
- due_date
- is_completed, completed_at
- completed_by (User)
Method: mark_completed(user)
```

---

### **Activity & Social Models**

#### **Comment**
Project comments:
```python
- user, project
- content
- timestamps
```

#### **Like**
Project likes:
```python
- user, project
- created_at
Constraint: Unique (user, project)
```

#### **Follow**
User following system:
```python
- follower, following (both ForeignKey to User)
- created_at
Constraint: Unique (follower, following)
```

#### **Activity**
User activity feed:
```python
- user
- activity_type (profile_updated|project_created|project_liked|...)
- title, description
- project, target_user, connection (related objects)
- is_public
- created_at
```

#### **UserStats**
Aggregated user statistics:
```python
- user (OneToOne)
- projects_created, connections_made, likes_received
- comments_made, projects_joined, tasks_completed
- followers_count, following_count
- last_updated
Method: update_stats() - recalculate all counters
```

---

### **Notification & Chat Models**

#### **Notification**
User notifications:
```python
- user (ForeignKey)
- type (connection_request|project_invite|new_message|...)
- title, description
- is_read, read_at
- created_at
```

#### **ChatRoom**
Group chat support:
```python
- name, description
- chat_type (direct|group)
- created_by
- members (M2M via ChatRoomMember)
- created_at, updated_at
```

#### **ChatRoomMember**
Chat membership:
```python
- chat_room, user
- role (admin|member)
- joined_at
```

---

### **File Management**

#### **File**
File uploads:
```python
- user
- file (FileField)
- filename, file_size, file_type
- uploaded_at
```

#### **MessageFile**
Associates files with messages:
```python
- message, file
- uploaded_at
Constraint: Unique (message, file)
```

---

## 4. AUTHENTICATION & SECURITY

### **Authentication Methods**
1. **Username/Email + Password** (Traditional Django)
2. **OTP-based** (Email-only verification)
3. **Social Login** (Google, GitHub via django-allauth)

### **Password Requirements** (forms.py - RegisterForm)
- **Minimum 8 characters**
- **At least 1 uppercase letter**
- **At least 1 lowercase letter** (enforced in form clean)
- **At least 1 digit**

### **Security Features**
- CSRF protection enabled (middleware)
- Input sanitization (`sanitize_input()` function)
- Session-based authentication
- Email verification available
- Password hashing via Django's built-in system

### **Email Backends** (settings.py - lines 219-255)
Priority order:
1. **Brevo** (Production - recommended) - `accounts.brevo_mail_backend.BrevoMailBackend`
2. **ZeptoMail** (Alternative) - `accounts.zepto_mail_backend.ZeptoMailBackend`
3. **Gmail SMTP** (Fallback) - Standard Django SMTP
4. **Console** (Development) - Prints to stdout

---

## 5. URL ROUTING (urls.py)

### **Authentication Routes**
```
/register/              → register_view
/login/                 → login_view
/logout/                → logout_view
/verify-otp/<purpose>/  → verify_otp_view (purpose: login|registration|reset)
/forgot-password/       → forgot_password_view
/reset-password/        → reset_password_view
/resend-otp/<purpose>/  → resend_otp_view
```

### **Dashboard & Profile**
```
/dashboard/             → dashboard_view
/home/                  → home_view
/student-profile/       → student_profile
/student-details/       → student_details_view
/profile/               → profile_view
/edit-profile/          → edit_profile
```

### **Project Management**
```
/post-project/          → post_project
/project/<id>/          → project_detail
/edit-project/<id>/     → edit_project
/delete-project/<id>/   → delete_project
/my-projects/           → my_projects_view
/explore-projects/      → explore_projects_view
```

### **Social Features**
```
/find-collaborators/    → find_collaborators
/connect/<user_id>/     → send_connection_request
/accept-connection/<id>/ → accept_connection
/reject-connection/<id>/ → reject_connection
/my-connections/        → my_connections
```

### **Messaging & Notifications**
```
/messages/              → message_view
/chat/<user_id>/        → chat_view
/notifications/         → notifications_view
/notification/<id>/read/ → mark_notification_read
```

### **Other Routes**
```
/premium/               → premium_view
/upgrade/               → upgrade_view
/investor-dashboard/    → investor_dashboard
/about/                 → about_view
/main_home/             → main_home
/accounts/*             → django-allauth URLs (social login, email management)
/api/*                  → Custom API endpoints
/admin/                 → Django admin
```

---

## 6. FORMS (forms.py)

### **RegisterForm**
- **Fields**: username, email, password1, password2, terms_agree
- **Validation**: 
  - Username uniqueness (case-insensitive)
  - Email uniqueness (case-insensitive)
  - Password strength (8 chars, uppercase, lowercase, digit)
  - Password confirmation matching
  - Terms acceptance

### **LoginForm**
- **Fields**: username (accepts email or username), password, remember_me
- **Purpose**: Custom styling (form-control class)

### **OTPVerificationForm**
- **Field**: otp_code (6 digits only)
- **Validation**: Must be exactly 6 digits
- **Purpose**: Email OTP verification

### **StudentProfileForm**
- **Fields**: 
  - Text: full_name, college, other_college, location, bio
  - Image: profile_photo
  - Multi-select: skills, project_interests
  - Checkboxes for predefined skills/interests
- **Choices Include**: Python, JavaScript, React, Django, Node.js, Docker, AWS, ML, Data Science, UI/UX, etc.

### **ProjectForm**
- **Fields**:
  - Text: title (5-200 chars), description (20-5000 chars)
  - Multi-select: technologies, looking_for
  - Single select: category
  - Text: timeline, collaboration_needs, github_link
- **Validation**:
  - Title length (5-200 chars)
  - Description length (20-5000 chars)
  - GitHub URL validation (http/https, contains github.com)
- **Technology Choices** (60+): Python, JavaScript, React, Django, Node.js, PostgreSQL, MongoDB, Docker, Kubernetes, AWS, TensorFlow, etc.
- **Looking For Roles** (21 options): Frontend Dev, Backend Dev, UI/UX Designer, Data Scientist, DevOps Engineer, etc.
- **Categories** (18 options): Web Development, Mobile Apps, AI/ML, Data Science, Blockchain, IoT, Game Dev, etc.

### **CustomSocialSignupForm**
- **Purpose**: Capture additional data during social login
- **Fields**: full_name, college, interests
- **Method**: `signup(request, user)` - Creates/updates StudentProfile

---

## 7. KEY VIEWS (views.py - 1700+ lines)

### **Authentication Views**
```python
register_view(request)              # User registration with validation
login_view(request)                 # Traditional login
logout_view(request)                # Session cleanup
verify_otp_view(request, purpose)   # OTP verification
forgot_password_view(request)       # Password reset request
reset_password_view(request)        # Password reset with OTP
resend_otp_view(request, purpose)   # Resend OTP to email
social_login_redirect(request)      # Allauth integration
```

### **Profile & Dashboard Views**
```python
@login_required
student_profile(request)            # View student profile
edit_profile(request)               # Edit profile form
profile_view(request)               # User profile page
dashboard_view(request)             # Dashboard (redirect to main_home)
main_home(request)                  # Main dashboard view
main(request)                       # Homepage
home_view(request)                  # Home page
student_details_view(request)       # Student details form
```

### **Project Views**
```python
@login_required
post_project(request)               # Create/list user projects
project_detail(request, project_id) # View single project
edit_project(request, project_id)   # Edit project
delete_project(request, project_id) # Delete project
my_projects_view(request)           # User's projects list
explore_projects_view(request)      # Browse all projects
like_project(request, project_id)   # Toggle project like
search_projects(request)            # Search projects
```

### **Social/Collaboration Views**
```python
@login_required
find_collaborators(request)         # Search & filter users
send_connection_request(user_id)    # Send connection request
accept_connection(connection_id)    # Accept connection
reject_connection(connection_id)    # Reject connection
my_connections(request)             # View user's connections
```

### **Messaging Views**
```python
@login_required
message_view(request)               # Message list/inbox
chat_view(request, user_id)         # Chat with specific user
mark_message_as_read(message_id)    # Mark message read
```

### **Notification Views**
```python
@login_required
notifications_view(request)         # View notifications
mark_notification_read(notification_id) # Mark notification read
```

### **Premium & Other**
```python
premium_view(request)               # Premium features page
upgrade_view(request)               # Upgrade subscription
investor_dashboard(request)         # Investor view
about_view(request)                 # About page
```

---

## 8. EMAIL SYSTEM

### **OTP Email** (`send_otp_email()` function - views.py:136)
**Trigger**: User requests OTP for login/registration/password reset
**Content**:
- HTML-formatted email with styled OTP box
- 6-digit code prominently displayed
- Plaintext fallback
- 5-minute validity warning
- Brand name: "🚀 Team"

**Error Handling**:
- Logs email failures
- Notifies admin of failures
- OTP remains valid for retry
- Graceful degradation (logs but doesn't expose OTP in errors)

### **Email Backends Configuration**
1. **Brevo** (Settings enabled when `BREVO_API_KEY` set)
   - Custom backend: `accounts.brevo_mail_backend.BrevoMailBackend`
   - Production-recommended

2. **ZeptoMail** (Settings enabled when `ZEPTO_MAIL_API_KEY` + `ZEPTO_MAIL_TOKEN` set)
   - Custom backend: `accounts.zepto_mail_backend.ZeptoMailBackend`
   - Alternative option

3. **Gmail SMTP** (Settings when `EMAIL_HOST_USER` + `EMAIL_HOST_PASSWORD` set)
   - Host: smtp.gmail.com
   - Port: 587
   - TLS: Enabled

4. **Console Backend** (Default for development)
   - Prints emails to stdout
   - Useful for testing without sending actual emails

---

## 9. SECURITY & VALIDATION

### **Input Sanitization** (`sanitize_input()` - views.py:107)
```python
- Strips HTML tags
- Removes < and > characters
- Trims whitespace
- Enforces max length
- Purpose: Prevent XSS attacks
```

### **Error Handling** (`handle_view_errors()` decorator - views.py:90)
- Catches all exceptions in decorated views
- Logs errors with full traceback
- Displays user-friendly messages
- Prevents redirect loops (redirects to referrer or /)
- Wraps views prone to errors

### **CSRF Protection**
- Middleware enabled: `'django.middleware.csrf.CsrfViewMiddleware'`
- Required for all POST requests
- Exception: `@csrf_exempt` can be applied where needed (rare)

### **Session Security**
- Session middleware configured
- Optional: `SESSION_COOKIE_SECURE` (for HTTPS only)
- Optional: `CSRF_COOKIE_SECURE` (for HTTPS only)

---

## 10. DATABASE MODELS - RELATIONSHIPS

### **User-Centric Relations**
```
User (Django)
├─ StudentProfile (OneToOne)
├─ sent_connections (Reverse FK from Connection.sender)
├─ received_connections (Reverse FK from Connection.receiver)
├─ sent_messages (Reverse FK from Message.sender)
├─ received_messages (Reverse FK from Message.receiver)
├─ created_projects (Reverse FK from Project.user)
├─ activities (Reverse FK from Activity.user)
├─ user_stats (OneToOne via UserStats)
├─ followed_by (Reverse FK from Follow.follower)
└─ follows (Reverse FK from Follow.following)
```

### **Project-Centric Relations**
```
Project
├─ owner (FK to User)
├─ members (Reverse FK from ProjectMember)
├─ team (OneToOne ProjectTeam)
├─ tasks (Reverse FK from ProjectTask)
├─ milestones (Reverse FK from ProjectMilestone)
├─ likes (Reverse FK from Like)
├─ comments (Reverse FK from Comment)
├─ invitations (Reverse FK from ProjectInvitation)
└─ activities (Reverse FK from Activity.project)
```

### **Message-Centric Relations**
```
Message
├─ sender (FK to User)
├─ receiver (FK to User, optional)
├─ chat_room (FK to ChatRoom, optional)
├─ reply_to (FK to Message - threading)
├─ files (Reverse FK from MessageFile)
├─ reactions (Reverse FK from MessageReaction)
└─ read_statuses (Reverse FK from MessageReadStatus)
```

---

## 11. KEY FEATURES

### **User Discovery**
- **Find Collaborators**: Search by skills, interests, college
- **Project Browsing**: Browse all projects with filters
- **Connection Requests**: Send/accept connection requests
- **User Profiles**: View detailed student profiles
- **Statistics**: Show total users, projects, connections

### **Project Management**
- **Create/Edit/Delete Projects**: Full CRUD operations
- **Project Details**: Title, description, technologies, collaboration needs
- **Team Collaboration**: Invite members, assign roles
- **Task Management**: Create tasks, assign to team members
- **Milestones**: Track project milestones
- **Project Invitations**: Accept/decline invitations

### **Social Interaction**
- **Connections**: Send/accept/reject connection requests
- **Messaging**: Direct messages between users
- **Comments**: Comment on projects
- **Likes**: Like/unlike projects
- **Following**: Follow other users
- **Activity Feed**: Track user activities

### **Authentication**
- **OTP Login**: Email-based passwordless login
- **Social Login**: Google and GitHub (via django-allauth)
- **Email Verification**: Verify email during registration
- **Password Reset**: Reset password via OTP

### **Notifications**
- **Connection Requests**: Notify when receiving connection request
- **Project Invitations**: Notify when invited to project
- **New Messages**: Notify of new messages
- **Comments**: Notify when commented on
- **Likes**: Notify when liked
- **Activity Notifications**: Customizable notifications

---

## 12. INSTALLED APPS & DEPENDENCIES

### **Django Core**
- Django 4.2.8
- djangorestframework 3.14.0
- django-allauth 0.61.1
- drf-spectacular 0.26.5

### **Database**
- psycopg2-binary 2.9.9 (PostgreSQL)
- dj-database-url 2.1.0

### **Authentication & Social**
- requests 2.31.0
- requests-oauthlib 1.3.1

### **Email**
- zeptomail 1.0.0

### **Data Processing**
- pandas 2.1.4
- openpyxl 3.1.2
- nltk 3.8.1

### **APIs & External Services**
- rapidapi 1.0.0

### **Image Processing**
- Pillow 10.1.0

### **Caching & Sessions**
- redis 5.0.1
- django-redis 5.4.0

### **Real-Time (WebSockets)**
- channels 4.0.0
- channels-redis 4.1.0

### **File Storage**
- boto3 1.34.34 (AWS S3)
- django-storages 1.14.2

### **Background Jobs**
- celery 5.3.4

### **Production Server**
- gunicorn 21.2.0
- whitenoise 6.6.0

### **Monitoring & Logging**
- sentry-sdk 1.38.0
- django-performance-monitor 0.1.1

### **Development & Testing**
- pytest 7.4.3
- pytest-django 4.7.0
- django-debug-toolbar 4.2.0
- black 23.12.1
- flake8 6.1.0
- isort 5.13.2
- mypy 1.7.1

### **Other Utilities**
- django-filter 23.5
- django-crispy-forms 2.1
- crispy-bootstrap5 0.7
- django-extensions 3.2.3
- django-cors-headers 4.3.1
- sphinx 7.2.6 (Documentation)

---

## 13. CONFIGURATION (settings.py)

### **Core Settings**
- **DEBUG**: Configurable via `DEBUG` env var (default: True)
- **SECRET_KEY**: From environment, auto-generated fallback for dev
- **ALLOWED_HOSTS**: Configurable list (default: localhost, 127.0.0.1)

### **Database Configuration**
- **PostgreSQL** (Production): Via `DATABASE_URL` env var (Render deployment)
- **PostgreSQL** (Local): Via `DB_NAME`, `DB_USER`, `DB_PASSWORD`, `DB_HOST`, `DB_PORT`
- **SQLite** (Fallback): `db.sqlite3` if PostgreSQL not configured

### **Middleware Stack**
1. SecurityMiddleware
2. SessionMiddleware
3. CommonMiddleware
4. CsrfViewMiddleware
5. AuthenticationMiddleware
6. MessageMiddleware
7. XFrameOptionsMiddleware
8. AccountMiddleware (allauth)

### **Template Configuration**
- Template directory: `BASE_DIR.parent / 'templates'`
- App directories enabled
- Context processors for auth, messages, debug

### **Static & Media Files**
- **STATIC_URL**: `/static/`
- **STATIC_ROOT**: `BASE_DIR / 'staticfiles'`
- **MEDIA_URL**: `/media/`
- **MEDIA_ROOT**: `BASE_DIR / 'media'`

### **Internationalization**
- Language: English (en-us)
- Time Zone: UTC
- Use I18N: True
- Use L10N: True
- Use TZ: True

### **Logging Configuration**
- **Console Handler**: Simple format, all logs
- **File Handler**: Rotating file (10MB max, 5 backups)
- **Error File Handler**: Separate error log
- **Django Logger**: INFO level, console + file
- **Accounts Logger**: DEBUG (dev) / INFO (prod), console + file

### **REST Framework**
- Default permission: AllowAny
- Pagination: PageNumberPagination (10 per page, max 100)
- Search backends: SearchFilter, OrderingFilter
- Authentication: SessionAuthentication
- Search param: `?search=`
- Ordering param: `?ordering=`

---

## 14. MODELS SUMMARY TABLE

| Model | Purpose | Key Fields | Relations |
|-------|---------|-----------|-----------|
| User | Django auth | username, email, password | StudentProfile, connections, messages, projects |
| StudentProfile | Extended user data | full_name, college, skills, interests | OneToOne User |
| OTP | Email verification | email, otp_code, purpose, expires_at | - |
| Connection | User networking | sender, receiver, status | FK User x2 |
| Message | Direct messaging | sender, receiver, content, chat_room | FK User x2, ChatRoom |
| MessageReadStatus | Read receipts | message, user, read_at | FK Message, User |
| Project | Project collaboration | title, description, technologies, category | FK User, members, tasks |
| ProjectMember | Team membership | project, user, role | FK Project, User |
| ProjectTask | Task management | project, title, status, priority | FK Project, User |
| ProjectMilestone | Milestones | project, title, due_date, is_completed | FK Project, User |
| ProjectInvitation | Invite users | project, invited_user, role, status | FK Project, User x2 |
| Comment | Project comments | user, project, content | FK User, Project |
| Like | Project likes | user, project | FK User, Project |
| Follow | Follow users | follower, following | FK User x2 |
| Activity | Activity feed | user, activity_type, title, project | FK User, Project |
| UserStats | User statistics | projects_created, connections_made, likes_received | OneToOne User |
| ChatRoom | Group chat | name, members, chat_type | M2M User via ChatRoomMember |
| ChatRoomMember | Chat membership | chat_room, user, role | FK ChatRoom, User |
| File | File uploads | user, file, filename, file_size | FK User |
| MessageFile | Message files | message, file | FK Message, File |
| MessageReaction | Message reactions | message, user, reaction | FK Message, User |
| Notification | Notifications | user, type, title, is_read | FK User |
| UserStatus | User online status | user, status, last_seen | OneToOne User |

---

## 15. CRITICAL FUNCTIONS & UTILITIES

### **OTP Generation** (models.py)
```python
OTP.generate_otp(email, purpose)
- Generates 6-digit random code
- Sets 5-minute expiry
- Deactivates previous OTPs for same email+purpose
- Returns OTP object
```

### **OTP Verification** (models.py)
```python
otp_obj.verify_otp(otp_code)
- Checks expiry and usage
- Compares code (plaintext, not hashed)
- Marks as used if valid
- Returns (success_bool, message_string)
```

### **Connection Management** (models.py)
```python
Connection model:
- unique_together constraint prevents duplicate requests
- status transitions: pending → accepted/rejected
```

### **Project Member Permissions** (models.py)
```python
ProjectMember properties:
- can_manage_project (owner|admin)
- can_invite_members (owner|admin)
- can_manage_tasks (owner|admin|contributor)
- can_edit_project (owner|admin|contributor)
```

### **Message Read Tracking** (models.py)
```python
Message methods:
- mark_as_read_by(user) → Creates MessageReadStatus entry
- is_read_by(user) → Checks if MessageReadStatus exists
- get_read_count() → Counts distinct users who read
- get_unread_users() → Returns User objects who haven't read
```

### **User Search & Filtering** (views.py - find_collaborators)
- Full-text search by username, full_name, bio, college
- Filter by college, interests, skills
- Match scoring based on shared interests
- Limit to 20 results
- Include connection status for each user

### **Email Sending** (views.py - send_otp_email)
- HTML email with styled OTP box
- Plaintext fallback
- Error handling with admin notification
- OTP code NOT exposed in error logs

### **Input Sanitization** (views.py - sanitize_input)
- Strip HTML tags
- Remove < and > characters
- Trim whitespace
- Enforce max length
- Used in registration, profile editing

---

## 16. DEPLOYMENT CONFIGURATION

### **Environment Variables Required**
```
# Core Django
SECRET_KEY=<generated-or-provided>
DEBUG=False (production)
ALLOWED_HOSTS=example.com,www.example.com

# Database (Render PostgreSQL)
DATABASE_URL=postgresql://user:pass@host:5432/dbname

# Email Configuration (choose one)
BREVO_API_KEY=<brevo-api-key>        # OR
ZEPTO_MAIL_API_KEY=<zepto-api-key>   # OR
ZEPTO_MAIL_TOKEN=<zepto-token>       # OR
EMAIL_HOST_USER=<gmail-email>
EMAIL_HOST_PASSWORD=<gmail-app-password>

# Social Authentication
GOOGLE_CLIENT_ID=<google-oauth-client-id>
GOOGLE_CLIENT_SECRET=<google-oauth-secret>
GITHUB_CLIENT_ID=<github-oauth-client-id>
GITHUB_CLIENT_SECRET=<github-oauth-secret>

# External APIs
RAPIDAPI_KEY=<rapidapi-key>

# Optional - Security for HTTPS
SECURE_SSL_REDIRECT=True
SESSION_COOKIE_SECURE=True
CSRF_COOKIE_SECURE=True

DEFAULT_FROM_EMAIL=noreply@unisync.app
```

### **Database Initialization**
```bash
python manage.py migrate                # Run migrations
python manage.py createsuperuser        # Create admin user
python manage.py collectstatic          # Collect static files
```

### **Production Server**
- **WSGI**: Gunicorn (21.2.0)
- **Static Files**: WhiteNoise (6.6.0)
- **Database**: PostgreSQL with Render
- **Optional**: Redis for caching/sessions, Celery for background tasks

---

## 17. TESTING FILES

Several testing scripts exist in the project root:
- `test_login.py` - Login functionality tests
- `test_email.py` - Email sending tests
- `test_brevo_email.py` - Brevo backend tests
- `test_zeptomail.py` - ZeptoMail backend tests
- `test_otp.py` - OTP generation/verification tests
- `test_services.py` - Service layer tests
- `test_connections.py` - Connection system tests
- `test_profile_upload.py` - Profile photo upload tests

---

## 18. KNOWN ISSUES & NOTES

### **Potential Issues**
1. **OTP Plaintext Storage**: OTP codes stored plaintext, not hashed (consider hashing for security)
2. **Message Read Status**: Scalable approach but requires cleanup of old entries
3. **Project Status**: Field exists but not fully implemented in all views
4. **Activity Feed**: `timestamp` referenced in code but `created_at` defined in model
5. **Template Lookup**: Parent directory templates referenced (`BASE_DIR.parent / 'templates'`)
6. **Backward Compatibility**: Model aliases for old naming conventions present (ProjectTeam, etc.)

### **Implementation Gaps**
1. Some views incomplete (view.py cut off at line 1722 in project_detail)
2. Celery tasks not visible in provided code
3. WebSocket/Channels integration mentioned but implementation not visible
4. S3 storage configuration not visible in provided code

### **Code Quality**
- Well-documented with docstrings
- Input validation present
- Error handling with logging
- Middleware-based security
- Follows Django best practices mostly
- Some views are very long (>1700 lines) - consider modularization

---

## 19. ARCHITECTURE DIAGRAM

```
┌─────────────────────────────────────────────────────────┐
│                    Django Application                   │
├─────────────────────────────────────────────────────────┤
│                                                         │
│  ┌──────────────────────────────────────────────────┐  │
│  │           URL Router (urls.py)                   │  │
│  │  /register, /login, /post-project, /chat, etc   │  │
│  └──────────────────────────────────────────────────┘  │
│                        ↓                                 │
│  ┌──────────────────────────────────────────────────┐  │
│  │           Views (views.py)                       │  │
│  │  - register_view, login_view, post_project      │  │
│  │  - find_collaborators, message_view, etc        │  │
│  └──────────────────────────────────────────────────┘  │
│            ↓                              ↓              │
│  ┌──────────────────┐    ┌──────────────────────────┐  │
│  │  Forms (forms.py)│    │   Models (models.py)     │  │
│  │  - RegisterForm  │    │   - User, StudentProfile │  │
│  │  - LoginForm     │    │   - Project, Message     │  │
│  │  - ProjectForm   │    │   - Connection, Comment  │  │
│  └──────────────────┘    └──────────────────────────┘  │
│                                        ↓                 │
│  ┌──────────────────────────────────────────────────┐  │
│  │         Database (PostgreSQL/SQLite)             │  │
│  │  - User, StudentProfile, Project, Message, etc   │  │
│  └──────────────────────────────────────────────────┘  │
│                                                         │
│  ┌──────────────────────────────────────────────────┐  │
│  │        Email System                              │  │
│  │  - Brevo Backend (send_otp_email)               │  │
│  │  - ZeptoMail Backend                            │  │
│  │  - Gmail SMTP Fallback                          │  │
│  └──────────────────────────────────────────────────┘  │
│                                                         │
│  ┌──────────────────────────────────────────────────┐  │
│  │        Authentication (django-allauth)           │  │
│  │  - Traditional (username/password)              │  │
│  │  - Google OAuth                                 │  │
│  │  - GitHub OAuth                                 │  │
│  └──────────────────────────────────────────────────┘  │
│                                                         │
└─────────────────────────────────────────────────────────┘
         ↓
┌─────────────────────────────────────────────────────────┐
│         External Services                               │
├─────────────────────────────────────────────────────────┤
│  - Email Providers (Brevo, ZeptoMail, Gmail SMTP)      │
│  - OAuth Providers (Google, GitHub)                    │
│  - RapidAPI (Universities list)                        │
│  - AWS S3 (optional file storage)                      │
│  - Redis (optional caching)                            │
└─────────────────────────────────────────────────────────┘
```

---

## 20. QUICK REFERENCE

### **Key File Locations**
- **Settings**: `/auth_project/auth_project/settings.py` (356+ lines)
- **Models**: `/auth_project/accounts/models.py` (718+ lines)
- **Views**: `/auth_project/accounts/views.py` (1700+ lines)
- **Forms**: `/auth_project/accounts/forms.py` (583+ lines)
- **URLs**: `/auth_project/auth_project/urls.py` (60 lines)
- **Requirements**: `/auth_project/requirements.txt` (84 dependencies)

### **Database Models Count**: 20+ models

### **Main Features**
- ✅ User authentication (traditional + OTP + social)
- ✅ User profiles with extended fields
- ✅ Project management and collaboration
- ✅ Team collaboration with roles and tasks
- ✅ Direct messaging between users
- ✅ Social networking (connections, follows)
- ✅ Activity feed
- ✅ Notifications
- ✅ Email system with multiple backends
- ✅ Project search and filtering
- ✅ Collaborator discovery

### **Next Steps for Development**
1. Complete the truncated view functions (project_detail continues beyond line 1722)
2. Implement Celery tasks for async operations
3. Complete WebSocket integration for real-time messaging
4. Add more comprehensive error handling
5. Implement pagination everywhere (some views missing paginator)
6. Add rate limiting for API endpoints
7. Complete transaction handling for critical operations
8. Add comprehensive test coverage
9. Implement image optimization for profile photos
10. Add caching strategies for frequently accessed data

---

**End of Analysis**  
This comprehensive analysis covers the complete codebase structure, models, authentication, forms, views, email system, database relationships, deployment configuration, and key features of the UniSync application.
