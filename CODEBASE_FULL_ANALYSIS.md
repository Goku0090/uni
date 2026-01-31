# UniSync Codebase - Complete Analysis Report

**Project**: University Student Collaboration Platform  
**Framework**: Django 4.2.8 + Django REST Framework 3.14.0  
**Database**: PostgreSQL (Production) / SQLite (Development)  
**Deployment**: Render.com  
**Last Updated**: January 29, 2026

---

## 1. PROJECT OVERVIEW

### Purpose
UniSync is a comprehensive platform enabling university students to:
- **Post and manage projects** with detailed specifications
- **Find collaborators** based on skills and interests
- **Direct messaging** and real-time communication
- **Profile management** with rich student profiles
- **Social features** (connections, followers, activity feeds)
- **Authentication** via traditional login and social providers (Google, GitHub)

### Tech Stack
- **Backend**: Django 4.2.8, Django REST Framework
- **Database**: PostgreSQL (Render), SQLite (local dev)
- **Email**: Brevo (primary), ZeptoMail (fallback), Gmail SMTP
- **Task Queue**: Celery 5.3.4
- **Real-time**: Channels 4.0.0, Channels-Redis 4.1.0
- **File Storage**: AWS S3 (boto3), Django-Storages
- **Monitoring**: Sentry SDK, Django Debug Toolbar
- **Testing**: pytest, Selenium

---

## 2. ARCHITECTURE OVERVIEW

### High-Level Component Flow
```
Client (Templates/Frontend)
    ↓
URL Router (urls.py)
    ↓
Views/Controllers (views.py)
    ↓
Business Logic (forms.py, utils.py, services/)
    ↓
Data Models (models.py)
    ↓
Database (PostgreSQL/SQLite)
```

### Key Design Patterns
- **MTV Pattern**: Django's Model-Template-View architecture
- **Middleware-based Security**: CSRF protection, CORS headers, SSL/TLS
- **Email Backend Strategy**: Pluggable email backends (Brevo > ZeptoMail > Gmail > Console)
- **REST API**: DRF for API endpoints
- **ORM**: Django ORM for database abstraction

---

## 3. CORE COMPONENTS ANALYSIS

### 3.1 Settings Configuration (`auth_project/settings.py`)

**Key Features:**
- **Environment-based configuration** using `python-dotenv`
- **Multi-database support**: Automatic selection (Render PostgreSQL → Local PostgreSQL → SQLite)
- **Email backend priority system**: Brevo → ZeptoMail → Gmail → Console
- **Security settings**: CSRF, SSL redirect, secure cookies (configurable by environment)
- **Social authentication**: Google OAuth, GitHub OAuth via django-allauth
- **Logging configuration**: File-based rotating logs + console output
- **Static files**: WhiteNoise for production serving

**Security Implementation:**
```python
- SECRET_KEY: Required in production, auto-generated in dev
- DEBUG: Environment-configurable
- ALLOWED_HOSTS: Environment-configurable
- SECURE_SSL_REDIRECT: Disabled by default (enabled in production)
- SESSION_COOKIE_SECURE: Disabled by default (enabled in production)
- CSRF_COOKIE_SECURE: Disabled by default (enabled in production)
```

**Email Configuration Logic:**
```
If BREVO_API_KEY exists:
    ├─ Use BrevoMailBackend (accounts/brevo_mail_backend.py)
Elif ZEPTO_MAIL_API_KEY and ZEPTO_MAIL_TOKEN exist:
    ├─ Use ZeptoMailBackend (accounts/zepto_mail_backend.py)
Elif EMAIL_HOST_USER and EMAIL_HOST_PASSWORD exist:
    ├─ Use Gmail SMTP backend
Else:
    └─ Use Console backend (prints OTP to stdout)
```

### 3.2 Models (`accounts/models.py`)

**Core Model Structure:**

#### User & Profile Models
```python
StudentProfile (OneToOne → User)
├─ personal_data: full_name, college, location, bio
├─ skills: JSONField (list)
├─ interests: JSONField (list)
├─ social_links: github, linkedin, portfolio, behance
├─ profile_photo: ImageField with validation
├─ profile_completed: Boolean flag
└─ timestamps: created_at, updated_at
```

#### Authentication Models
```python
OTP
├─ email: EmailField
├─ otp_code: 6-digit string
├─ purpose: login/registration/reset
├─ is_used: Boolean
├─ expires_at: DateTimeField (5-minute expiry)
└─ Methods: is_valid(), verify_otp(), generate_otp()
```

#### Project Management Models
```python
Project
├─ owner: ForeignKey → User
├─ title: CharField (5-200 chars)
├─ description: TextField (20-5000 chars)
├─ category: Project type (web, mobile, ai, etc.)
├─ technologies: JSONField (array)
├─ looking_for: Roles needed (JSONField)
├─ timeline: CharField
├─ collaboration_needs: TextField
├─ github_link: URLField
├─ visibility: private/public
├─ status: active/archived
└─ timestamps: created_at, updated_at

ProjectMember (role-based access)
├─ roles: owner, admin, contributor, viewer
├─ permissions: properties for can_manage_project, can_invite_members, etc.

ProjectTask
├─ status: todo, in_progress, review, completed, cancelled
├─ priority: low, medium, high, urgent
├─ assigned_to, assigned_by, due_date
└─ timestamps + completion tracking

ProjectMilestone
├─ title, description, due_date
├─ is_completed, completed_at, completed_by
└─ Progress tracking
```

#### Social & Messaging Models
```python
Connection
├─ sender, receiver: ForeignKey → User
├─ status: pending, accepted, rejected
└─ unique_together: [sender, receiver]

Message
├─ sender, receiver: ForeignKey → User
├─ content: TextField
├─ message_type: text, file, image, call
├─ call_type: voice, video (optional)
├─ reply_to: Self-referential ForeignKey (threading)
├─ chat_room: ForeignKey → ChatRoom (for group chats)
└─ Methods: mark_as_read_by(), is_read_by(), get_read_count()

MessageReadStatus
├─ message, user: ForeignKey
├─ read_at: DateTimeField
└─ Purpose: Scalable read status tracking

MessageFile, MessageReaction
├─ Message attachments and emoji reactions
└─ unique_together constraints

ChatRoom
├─ name, description: CharField, TextField
├─ chat_type: direct, group
├─ created_by: ForeignKey → User
├─ members: ManyToMany → ChatRoomMember

ChatRoomMember
├─ user, chat_room
├─ role: member, moderator, admin
├─ joined_at: DateTimeField
```

#### Content & Social Features
```python
Like
├─ user, project: ForeignKey
└─ unique_together: [user, project]

Comment
├─ user, project: ForeignKey
├─ content: TextField
├─ edited: Boolean tracking
└─ timestamps

Follow
├─ follower, following: ForeignKey → User
├─ unique_together: [follower, following]

Activity
├─ user: ForeignKey
├─ activity_type: profile_updated, project_created, project_liked, etc.
├─ project, target_user, connection: Optional ForeignKeys
├─ is_public: Boolean
└─ timestamps

UserStats
├─ OneToOne → User
├─ counters: projects_created, connections_made, likes_received, etc.
├─ followers_count, following_count
└─ update_stats() method for cache updates

Notification
├─ user: ForeignKey
├─ notification_type: message, like, comment, connection, etc.
├─ from_user: ForeignKey
├─ title, message: CharField, TextField
├─ is_read: Boolean
└─ timestamps

UserStatus
├─ user: OneToOne
├─ is_online: Boolean
├─ last_seen: DateTimeField
```

---

## 4. AUTHENTICATION & AUTHORIZATION FLOW

### 4.1 Registration Flow
```
User → /register/ (GET)
    ↓ [RegisterForm Template]
    → /register/ (POST)
        ↓ [Form Validation]
        ├─ Email uniqueness check
        ├─ Username uniqueness check
        ├─ Password strength (8+ chars, uppercase, lowercase, digit)
        └─ Terms agreement required
    → Create User + StudentProfile
    → Send welcome email
    → Redirect to /login/
```

### 4.2 OTP-Based Login
```
User → /login/ (GET)
    ↓ [LoginForm]
    → /login/ (POST)
        ↓ [Email/Username validation]
        ├─ Check if email exists
        ├─ Generate 6-digit OTP
        ├─ Set 5-minute expiry
        ├─ Deactivate previous OTPs
        └─ Send via email (Brevo/ZeptoMail)
    → Session: stored_email = user_email
    → Redirect to /verify-otp/login/
    
    ↓ [OTP Verification]
    /verify-otp/login/ (GET)
        ↓ [OTPVerificationForm]
    /verify-otp/login/ (POST)
        ↓ [OTP Lookup & Validation]
        ├─ Check OTP exists for email/purpose
        ├─ Check OTP not expired (5 minutes)
        ├─ Check OTP not already used
        ├─ Verify OTP code matches
        └─ Mark OTP as used
    → Authenticate user (django.contrib.auth.login)
    → Redirect to /dashboard/
```

### 4.3 Social OAuth Login
```
User → "Sign in with Google/GitHub"
    ↓ [django-allauth flow]
    → OAuth provider authorization
    → Provider callback
    → Create/Update User
    → CustomSocialSignupForm (for additional data)
    → Create StudentProfile if not exists
    → Redirect to /dashboard/
```

### 4.4 Password Reset Flow
```
User → /forgot-password/ (GET)
    ↓ [Email form]
    → /forgot-password/ (POST)
        ├─ Generate OTP (purpose='reset')
        ├─ Send via email
        └─ Session: reset_email = user_email
    
    → /verify-otp/reset/ (GET/POST)
        ├─ Verify OTP
        └─ Redirect to /reset-password/
    
    → /reset-password/ (GET/POST)
        ├─ Get new password
        ├─ Update user.set_password()
        └─ Redirect to /login/
```

### 4.5 Email Service Chain
```
send_otp_email(email, otp_code, purpose)
    ├─ Subject: "🚀 - Your {purpose} OTP Code"
    ├─ Generate plaintext message
    ├─ Generate HTML template
    │   ├─ Styled container
    │   ├─ OTP box with large font
    │   ├─ 5-minute expiry notice
    │   └─ "🚀 Team" branding
    ├─ Try sending via EMAIL_BACKEND
    │   ├─ Success: log success
    │   ├─ Failure: log error + notify admins
    │   └─ OTP still created for retry
    └─ Returns None (fire-and-forget)
```

---

## 5. VIEWS & CONTROLLERS ANALYSIS

### 5.1 Authentication Views (from `views.py`)

**Key Views:**
- `register_view()` - User registration with form validation
- `login_view()` - OTP generation and email sending
- `verify_otp_view(purpose)` - OTP verification (supports login/registration/reset)
- `forgot_password_view()` - Initiate password reset
- `reset_password_view()` - Update password after OTP verification
- `logout_view()` - Django logout + session cleanup

**Important Features:**
- **Input Sanitization**: `sanitize_input()` function removes HTML tags and dangerous characters
- **Error Handling**: `@handle_view_errors` decorator for exception handling
- **Resend OTP**: `resend_otp_view(purpose)` - Rate-limited OTP resending

### 5.2 Project Management Views

**CRUD Operations:**
- `post_project()` - Create new project (ProjectForm)
- `project_detail(project_id)` - View project details
- `edit_project(project_id)` - Edit own project
- `delete_project(project_id)` - Soft delete project
- `my_projects_view()` - User's own projects
- `explore_projects_view()` - Browse all projects (filtered/paginated)

**Filtering & Search:**
- `search_projects()` - Query title, description, collaboration_needs
- **ProjectVisibilityFilter**: Role-based project filtering
  - Owners see all their projects
  - Public projects visible to all
  - Private projects visible only to members
  - Filtering by category, technology, role requirements

### 5.3 Messaging & Communication Views

**Direct Messaging:**
- `message_view()` - Inbox/conversation list
- `chat_view(user_id)` - Direct message thread with specific user
- `mark_message_read()` - Update read status
- **MessageReadStatus model**: Scalable read tracking

**Group Chat:**
- `ChatRoom` model support
- `ChatRoomMember` with role-based access (member/moderator/admin)
- Threaded conversations (reply_to field)
- Message reactions and file attachments

### 5.4 Social Features Views

**Connections:**
- `send_connection_request(user_id)` - Create pending connection
- `accept_connection(connection_id)` - Accept connection request
- `reject_connection(connection_id)` - Decline connection request
- `my_connections()` - View accepted connections

**Followers:**
- `Follow` model for user-to-user following
- Public activity feed via `Activity` model

**Notifications:**
- `notifications_view()` - Unread notification list
- `mark_notification_read(notification_id)` - Mark as read
- **Notification Types**: message, like, comment, connection, mention

### 5.5 Profile & Dashboard Views

**User Profiles:**
- `student_profile()` - View user profile (public)
- `profile_view()` - Edit own profile
- `edit_profile()` - Update StudentProfile with avatar upload
- **ProfilePhoto**: ImageField with validation (jpg, jpeg, png, gif)

**Dashboard:**
- `dashboard_view()` - User stats and recent activities
- `main_home()` - Landing page
- `explore_projects_view()` - Featured/trending projects

**Special Features:**
- `find_collaborators()` - Search collaborators by skills/interests
- `investor_dashboard()` - Premium feature for investors
- **StudentProfileNLP**: Natural Language Processing utilities for profile matching

---

## 6. FORMS & VALIDATION

### 6.1 Authentication Forms

**RegisterForm (UserCreationForm)**
```python
Fields:
├─ username: 3-150 chars, unique, case-insensitive check
├─ email: Required, unique check
├─ password1: 8+ chars, uppercase, lowercase, digit
├─ password2: Confirm password
└─ terms_agree: Boolean (required)

Validation:
├─ clean_username(): Case-insensitive uniqueness
├─ clean_email(): Lowercased, uniqueness check
├─ clean_password1(): Strength requirements
└─ clean(): Password match verification
```

**LoginForm (AuthenticationForm)**
```python
Fields:
├─ username: Can be username or email
├─ password: Plain text input
└─ remember_me: Optional checkbox

Note: Username field accepts both username and email
```

**OTPVerificationForm**
```python
Field:
└─ otp_code: 6 digits, numeric only, case-sensitive

Validation:
├─ Must be exactly 6 digits
└─ Must contain only digits
```

### 6.2 Project Management Forms

**ProjectForm**
```python
Fields:
├─ title: 5-200 chars
├─ description: 20-5000 chars
├─ technologies: MultipleChoiceField (50+ tech options)
├─ looking_for: MultipleChoiceField (21 role options)
├─ category: ChoiceField (18 categories)
├─ timeline: e.g., "3-6 months"
├─ collaboration_needs: Detailed text
└─ github_link: Optional URL

Validations:
├─ clean_title(): Length checks (5-200)
├─ clean_description(): Length checks (20-5000)
└─ clean_github_link(): URL format + GitHub domain check

Technologies Supported (50+):
├─ Languages: Python, JavaScript, Java, C++, C#, PHP, Ruby, Go, Rust, Swift, Kotlin
├─ Frontend: React, Angular, Vue.js, HTML/CSS, Bootstrap, Tailwind, SASS
├─ Backend: Django, Flask, Laravel, Rails, Spring Boot, Node.js, Express
├─ Databases: SQL, MongoDB, PostgreSQL, MySQL, Redis
├─ Cloud & DevOps: Docker, Kubernetes, AWS, GCP, Azure
├─ ML/Data: TensorFlow, PyTorch, Pandas, NumPy, Jupyter, R, Tableau, PowerBI
├─ Design: Figma, Sketch, Photoshop, Illustrator, Blender
└─ Gaming: Unity, Unreal Engine, Android, iOS, Flutter, React Native
```

### 6.3 Profile Forms

**StudentProfileForm (ModelForm)**
```python
Fields:
├─ full_name: CharField
├─ college: CharField
├─ other_college: CharField (if not in list)
├─ location: CharField
├─ interests: Comma-separated text
├─ bio: Textarea
├─ profile_photo: ImageField
├─ skills: MultipleChoiceField (16 skill options)
├─ project_interests: MultipleChoiceField (12 interests)
├─ role_preference: CharField
├─ github, linkedin, portfolio, behance: URLFields
└─ timestamps (auto)

Skills (16 options):
├─ Languages: Python, JavaScript, Java, C++
├─ Frontend: React, HTML/CSS
├─ Backend: Django, Node.js
├─ Database: SQL
├─ Tools: Git, Docker, AWS
├─ Specialized: Machine Learning, Data Science, UI/UX Design, Mobile Development

Project Interests (12 options):
├─ Web Development, Mobile Apps, AI/ML
├─ Data Science, Blockchain, IoT, Game Dev
├─ Open Source, Research, Startup, Social Impact, Education
```

---

## 7. API & SERIALIZERS

### 7.1 REST Framework Configuration

```python
REST_FRAMEWORK = {
    'DEFAULT_PERMISSION_CLASSES': [
        'rest_framework.permissions.AllowAny',  # Note: Open access
    ],
    'DEFAULT_PAGINATION_CLASS': 'rest_framework.pagination.PageNumberPagination',
    'DEFAULT_FILTER_BACKENDS': [
        'rest_framework.filters.SearchFilter',
        'rest_framework.filters.OrderingFilter',
    ],
    'DEFAULT_AUTHENTICATION_CLASSES': [
        'rest_framework.authentication.SessionAuthentication',
    ],
    'PAGE_SIZE': 10,
    'MAX_PAGE_SIZE': 100,
}
```

**Security Note**: Default permission is `AllowAny` - this is appropriate for public endpoints but should be restricted for protected resources.

### 7.2 Serializers

**UserProfileSerializer**
```python
Source: StudentProfile
Fields:
├─ id, username, email (read-only)
├─ full_name (from user.get_full_name)
├─ date_joined (from user.date_joined)
├─ college, location, interests, bio
├─ skills, project_interests, role_preference
├─ github, linkedin, portfolio, behance
├─ profile_photo
└─ is_online, profile_completed
```

**ProjectSerializer**
```python
Source: Project
Fields:
├─ id, title, description
├─ technologies, looking_for
├─ category, timeline, collaboration_needs
├─ github_link
├─ owner: Nested UserProfileSerializer
├─ likes_count: SerializerMethodField
├─ comments_count: SerializerMethodField
└─ created_at, updated_at
```

**MessageSerializer**
```python
Source: Message
Fields:
├─ id, content
├─ sender: Nested UserProfileSerializer
├─ message_type
├─ is_read
├─ reactions: Dict of {emoji: count}
└─ created_at
```

**ConnectionSerializer, NotificationSerializer**
- Similar nested structure with related user objects
- Read-only IDs and timestamps

---

## 8. UTILITY & SERVICE MODULES

### 8.1 StudentProfileNLP (`utils.py`)

**Purpose**: Natural Language Processing for profile matching

**Features**:
- Parse interests and skills from text
- Tokenization and stemming
- Similarity scoring between profiles
- Recommend collaborators based on NLP analysis

### 8.2 ProjectVisibilityFilter (`utils.py`)

**Purpose**: Role-based project visibility filtering

**Logic**:
```python
def filter_visible_projects(user):
    if user.is_anonymous:
        return Project.objects.filter(visibility='public')
    else:
        return Project.objects.filter(
            Q(visibility='public') |                    # Public projects
            Q(owner=user) |                             # User's own projects
            Q(members__user=user) |                     # Projects user is member of
            Q(invitations__invited_user=user)           # Pending invitations
        ).distinct()
```

### 8.3 Authentication Service (`services/auth_service.py`)

Encapsulates authentication business logic:
- User creation
- OTP management
- Email sending
- Password reset workflows

---

## 9. URL ROUTING STRUCTURE

### Main Routes (`auth_project/urls.py`)

```
/admin/ → Django admin
/accounts/ → django-allauth (social auth)
/accounts/profile/ → social_login_redirect

Authentication:
├─ /register/ → RegisterForm
├─ /login/ → OTP generation
├─ /logout/ → Session cleanup
├─ /verify-otp/<purpose>/ → OTP verification
├─ /forgot-password/ → Reset password initiation
├─ /reset-password/ → Update password
└─ /resend-otp/<purpose>/ → Resend OTP

Core Features:
├─ /dashboard/ → User dashboard
├─ /home/ → Homepage
├─ /main_home/ → Alternative homepage
└─ /about/ → About page

Project Management:
├─ /post-project/ → Create project
├─ /project/<id>/ → View project
├─ /edit-project/<id>/ → Edit project
├─ /delete-project/<id>/ → Delete project
├─ /my-projects/ → User's projects
└─ /explore-projects/ → Browse all projects

Messaging:
├─ /messages/ → Inbox
├─ /chat/<user_id>/ → Direct message thread
└─ /notifications/ → Notification list

Social:
├─ /connect/<user_id>/ → Send connection
├─ /accept-connection/<id>/ → Accept
├─ /reject-connection/<id>/ → Decline
├─ /my-connections/ → View connections
├─ /find-collaborators/ → Find users

Profile:
├─ /profile/ → View own profile
├─ /student-profile/ → View any profile
└─ /edit-profile/ → Edit profile

Premium:
├─ /premium/ → Premium info
├─ /upgrade/ → Upgrade action
└─ /investor-dashboard/ → Investor view

Static:
├─ /media/ → User uploads (dev only)
├─ /static/ → CSS, JS, images
└─ Catch-all: / → Main homepage
```

---

## 10. SECURITY FEATURES

### 10.1 Authentication Security

- **OTP-based authentication**: More secure than password-only
- **Email verification**: Required for registration
- **Rate limiting**: (Not explicitly shown, should be added for OTP endpoints)
- **CSRF protection**: Enabled by default in middleware
- **Password strength requirements**: 8+ chars, uppercase, lowercase, digit

### 10.2 Data Protection

```python
Input Sanitization:
├─ sanitize_input(): Removes HTML tags and dangerous characters
├─ Used in: Forms, user-submitted content
└─ Protection against: XSS attacks

SQL Injection:
├─ Django ORM prevents parameterized queries
└─ No raw SQL queries in main views

Authorization:
├─ @login_required decorators on protected views
├─ ProjectMember role-based checks
├─ Ownership verification (only owner can edit/delete)
└─ ChatRoomMember role-based access
```

### 10.3 Recommended Security Enhancements

1. **Rate Limiting**: Add rate limiting to OTP endpoints (e.g., 5 attempts per 15 minutes)
2. **Token Expiry**: Implement JWT tokens with expiration for API
3. **XSS Protection**: Add Content Security Policy headers
4. **CORS Configuration**: Explicitly configure allowed origins
5. **Logging**: Audit log authentication attempts
6. **Two-Factor Authentication**: Optional 2FA for sensitive operations

---

## 11. DATABASE SCHEMA SUMMARY

### Tables (20+ models)

```
Authentication Layer:
├─ auth_user (Django built-in)
├─ auth_group (Permission groups)
├─ accounts_studentprofile
├─ accounts_otp
└─ allauth_* (Social auth tables)

Social Layer:
├─ accounts_connection
├─ accounts_follow
├─ accounts_notification
├─ accounts_userstatus
└─ accounts_userstats

Content Layer:
├─ accounts_project
├─ accounts_projectmember
├─ accounts_projectinvitation
├─ accounts_projecttask
├─ accounts_projectmilestone
├─ accounts_like
├─ accounts_comment
└─ accounts_activity

Messaging Layer:
├─ accounts_message
├─ accounts_messagereadstatus
├─ accounts_messagefile
├─ accounts_messagereaction
├─ accounts_file
├─ accounts_chatroom
└─ accounts_chatroommember
```

### Key Relationships

```
User
├─ 1:1 → StudentProfile
├─ 1:M → Project (owner)
├─ 1:M → Message (sender/receiver)
├─ 1:M → Connection (sender/receiver)
├─ 1:M → Follow (follower/following)
├─ 1:M → Like
├─ 1:M → Comment
├─ 1:M → Activity
└─ M:M → ChatRoom (via ChatRoomMember)

Project
├─ M:1 → User (owner)
├─ 1:M → ProjectMember
├─ 1:M → ProjectTask
├─ 1:M → ProjectMilestone
├─ 1:M → Like
├─ 1:M → Comment
└─ 1:M → Activity

Message
├─ M:1 → User (sender/receiver)
├─ M:1 → ChatRoom (optional)
├─ 1:M → MessageReadStatus
├─ 1:M → MessageReaction
└─ 1:M → MessageFile
```

---

## 12. DEPLOYMENT CONSIDERATIONS

### Environment Variables Required

**Core:**
- `DEBUG`: Boolean (development vs production)
- `SECRET_KEY`: Required for production
- `ALLOWED_HOSTS`: Comma-separated domain list

**Database:**
- `DATABASE_URL`: Render PostgreSQL (auto-provided)
- `DB_NAME`, `DB_USER`, `DB_PASSWORD`, `DB_HOST`, `DB_PORT`: Local PostgreSQL
- Falls back to SQLite if not configured

**Email:**
- `BREVO_API_KEY`: Brevo transactional email
- `ZEPTO_MAIL_API_KEY`, `ZEPTO_MAIL_TOKEN`: ZeptoMail
- `EMAIL_HOST_USER`, `EMAIL_HOST_PASSWORD`: Gmail SMTP
- `DEFAULT_FROM_EMAIL`: Sender email address

**Social Auth:**
- `GOOGLE_CLIENT_ID`, `GOOGLE_CLIENT_SECRET`: Google OAuth
- `GITHUB_CLIENT_ID`, `GITHUB_CLIENT_SECRET`: GitHub OAuth

**External Services:**
- `RAPIDAPI_KEY`, `RAPIDAPI_HOST`: API data (universities)
- AWS credentials (if using S3 storage)

### Production Checklist

```
[ ] Set DEBUG=False
[ ] Set SECRET_KEY to strong random value
[ ] Configure ALLOWED_HOSTS
[ ] Enable SECURE_SSL_REDIRECT=True
[ ] Enable SESSION_COOKIE_SECURE=True
[ ] Enable CSRF_COOKIE_SECURE=True
[ ] Set up database backups
[ ] Configure email backend (Brevo recommended)
[ ] Set up Redis for caching/sessions
[ ] Configure Celery for background tasks
[ ] Set up Sentry for error monitoring
[ ] Configure S3 for static files (WhiteNoise for fallback)
[ ] Run django-admin collectstatic
[ ] Enable rate limiting on OTP endpoints
[ ] Configure CORS headers appropriately
[ ] Set up SSL/TLS certificate
[ ] Test email sending end-to-end
[ ] Run security check: python manage.py check --deploy
```

---

## 13. TESTING INFRASTRUCTURE

### Test Files (Root directory)
- `test_login.py` - Login flow tests
- `test_email.py` - Email sending tests
- `test_otp.py`, `test_otp_simple.py`, `test_otp_console.py` - OTP tests
- `test_profile_upload.py` - Profile upload tests
- `test_search.py` - Search functionality tests
- `test_connections.py` - Connection feature tests
- `test_filter.py`, `test_filtering_debug.py` - Filtering logic tests
- `test_services.py` - Service layer tests
- `test_rapidapi.py` - External API tests
- `test_zeptomail.py`, `test_zepto_simple.py` - Email backend tests
- `test_brevo_email.py` - Brevo email backend tests

### Test Framework
- `pytest` with `pytest-django`
- `Selenium` for browser-based testing
- Helper scripts: `check_*.py`, `debug_*.py`, `diagnose_*.py`

---

## 14. CACHING STRATEGY

### Configured Backends
- **Django Cache**: Default memory cache
- **Redis**: Optional (redis==5.0.1, django-redis==5.4.0)
  - Session backend (recommended for scalability)
  - Cache backend for view/query caching

### Cache Usage
- Dashboard view: `@cache_page` decorator (configurable TTL)
- Project listings: Paginated with optional caching
- UserStats: Updated on demand, cache invalidated on activity

---

## 15. ERROR HANDLING & LOGGING

### Logging Configuration

**Handlers:**
1. Console: Real-time output for development
2. File (`logs/django.log`): Rotating file handler (10MB max, 5 backups)
3. Error file (`logs/error.log`): Errors only, rotating

**Loggers:**
- `django`: INFO level, all handlers
- `accounts`: DEBUG/INFO depending on DEBUG setting
- Custom loggers: Optional in views for business logic

### Error Handling Strategy

**Decorator-based:**
```python
@handle_view_errors
def view_function(request):
    # Catches exceptions, logs, shows user-friendly message
    # Redirects to referrer or home
```

**Try-except blocks:**
- Email sending errors logged but not exposed to user
- Admin notified via email_admins()
- OTP still created even if email fails

---

## 16. PERFORMANCE OPTIMIZATION

### Strategies Implemented

1. **Database Optimization**:
   - Connection pooling (conn_max_age=600 in Render)
   - Indexes on foreign keys and frequently queried fields
   - Selective field queries (use values/values_list where possible)

2. **Caching**:
   - Redis for sessions and cache
   - Page caching with @cache_page decorator
   - Query result caching (manually managed)

3. **Static Files**:
   - WhiteNoise for production serving
   - GZIP compression enabled by default

4. **Async Tasks**:
   - Celery for background jobs (configured, see requirements)
   - Email sending should be async (implement task)

### Recommended Optimizations

1. Implement Celery tasks for:
   - Email sending (non-blocking OTP delivery)
   - Bulk notifications
   - Profile NLP processing

2. Add database indexes:
   - Project.visibility + Project.created_at
   - Message.receiver + Message.is_read
   - UserStats.user (OneToOne already indexed)

3. Implement pagination everywhere:
   - API responses (already configured)
   - Template views (partially done)

4. Add API rate limiting:
   - DRF throttle classes
   - OTP endpoint protection

---

## 17. KNOWN ISSUES & TECHNICAL DEBT

### From Documentation Files

1. **Login Issues**: Mentioned in multiple FIX_* documents
   - Resolved with OTP implementation
   - Email backend fallback chain working

2. **Project Filtering**: Extensively documented in separate analysis
   - Visibility filter implemented
   - Suggested optimizations for large datasets

3. **Message Read Status**:
   - Migrated to MessageReadStatus model (scalable)
   - Read receipts implemented

4. **Email Configuration**:
   - Multiple backend support working
   - Console fallback for development

5. **Profile Photo Upload**:
   - ImageField with validation
   - File extension checks (jpg, jpeg, png, gif)

### Code Quality Issues

1. **Missing Rate Limiting**: OTP endpoints vulnerable to brute force
2. **Incomplete Test Coverage**: Not all views/models tested
3. **Hardcoded Values**: Some magic numbers in views (should be settings)
4. **Async Tasks**: Celery configured but not utilized
5. **Pagination**: Inconsistent across different views

---

## 18. DEPENDENCIES BREAKDOWN

### Framework & Core (7 packages)
```
Django==4.2.8
django-allauth==0.61.1
djangorestframework==3.14.0
dj-database-url==2.1.0
python-dotenv==1.0.0
requests==2.31.0
requests-oauthlib==1.3.1
```

### Database (1 package)
```
psycopg2-binary==2.9.9  # PostgreSQL adapter
```

### Email (1 package)
```
zeptomail==1.0.0  # ZeptoMail support (Brevo via custom backend)
```

### Data Processing (3 packages)
```
nltk==3.8.1       # NLP for profile matching
pandas==2.1.4     # Data analysis (Excel import, project stats)
openpyxl==3.1.2   # Excel file support
```

### File Handling (2 packages)
```
Pillow==10.1.0               # Image processing (profile photos)
django-storages==1.14.2      # S3 storage backend
boto3==1.34.34               # AWS SDK
```

### Real-time & Async (3 packages)
```
channels==4.0.0         # WebSocket support
channels-redis==4.1.0   # Channel layer backend
celery==5.3.4           # Background task queue
redis==5.0.1            # Redis client
django-redis==5.4.0     # Django Redis backend
```

### Monitoring & Security (2 packages)
```
sentry-sdk==1.38.0  # Error tracking
django-cors-headers==4.3.1  # CORS support
```

### Development (10+ packages)
```
django-debug-toolbar==4.2.0
django-extensions==3.2.3
django-filter==23.5
django-crispy-forms==2.1
crispy-bootstrap5==0.7
drf-spectacular==0.26.5  # API documentation
black==23.12.1           # Code formatting
flake8==6.1.0            # Linting
isort==5.13.2            # Import sorting
mypy==1.7.1              # Type checking
pytest==7.4.3            # Testing
pytest-django==4.7.0     # Django testing
sphinx==7.2.6            # Documentation
sphinx-rtd-theme==2.0.0  # Doc theme
```

### Production (2 packages)
```
gunicorn==21.2.0    # WSGI server
whitenoise==6.6.0   # Static file serving
```

---

## 19. KEY FILES REFERENCE

| File | Purpose | Key Classes/Functions |
|------|---------|----------------------|
| `settings.py` | Configuration | Database, email, auth setup |
| `urls.py` | Routing | URL patterns, redirect setup |
| `models.py` | Data layer | 20+ model classes, relationships |
| `views.py` | Controllers | 50+ view functions, business logic |
| `forms.py` | Input validation | 5 form classes with validation |
| `serializers.py` | API responses | 6 serializer classes |
| `utils.py` | Utilities | NLP, filtering, sanitization |
| `services/auth_service.py` | Auth logic | User creation, OTP management |
| `brevo_mail_backend.py` | Email backend | Brevo SMTP implementation |
| `zepto_mail_backend.py` | Email backend | ZeptoMail API implementation |

---

## 20. SUMMARY & RECOMMENDATIONS

### Strengths
✅ **Comprehensive feature set**: Authentication, projects, messaging, social  
✅ **Flexible email configuration**: Multiple backend support  
✅ **Modern Django patterns**: MTV architecture, ORM, REST Framework  
✅ **Security-conscious**: CSRF, password validation, input sanitization  
✅ **Scalable database design**: Proper indexing, query optimization options  
✅ **Extensible**: Async tasks ready, API documented, service layer  

### Areas for Improvement
⚠️ **Rate limiting**: Add throttling to authentication endpoints  
⚠️ **API security**: Use token authentication instead of session auth  
⚠️ **Async tasks**: Implement Celery for non-blocking operations  
⚠️ **Comprehensive testing**: Increase test coverage (integration tests)  
⚠️ **Pagination consistency**: Apply pagination uniformly across views  
⚠️ **Documentation**: Generate API docs with drf-spectacular  
⚠️ **Monitoring**: Set up Sentry alerts for production errors  
⚠️ **Performance**: Implement query optimization for large datasets  

### Next Steps
1. Complete API documentation using drf-spectacular
2. Add comprehensive test suite (target: 80% coverage)
3. Implement rate limiting and throttling
4. Set up Celery tasks for email and notifications
5. Configure Sentry for production monitoring
6. Implement JWT token authentication
7. Add API versioning strategy
8. Create admin dashboard for content moderation
9. Implement search optimization (Elasticsearch optional)
10. Add WebSocket support via Channels for real-time features

---

**End of Analysis Report**
*Generated: January 29, 2026*
