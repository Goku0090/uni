# UniSync - Comprehensive Codebase Analysis

**Date:** February 3, 2026  
**Repository:** https://github.com/Goku0090/uni  
**Project Type:** Full-stack Django + Frontend Collaboration Platform

---

## Executive Summary

UniSync is a sophisticated **university collaboration platform** designed to connect students for project collaboration, networking, and skill-sharing. The application combines a Django REST backend with a full-featured frontend for managing projects, messaging, profiles, and social networking features.

### Key Metrics
- **Framework:** Django 4.2.8
- **Database:** PostgreSQL (production), SQLite (development)
- **API Style:** REST API + Traditional Django Views
- **Key Features:** Authentication, OTP, Social Login, Projects, Messaging, Comments, Notifications
- **Deployment:** Render/Railway ready

---

## Architecture Overview

### Technology Stack

```
┌─────────────────────────────────────────────────────────┐
│                    FRONTEND LAYER                       │
│  HTML Templates (Django) | JavaScript | Bootstrap 5    │
└─────────────────────────────────────────────────────────┘
                           ↓
┌─────────────────────────────────────────────────────────┐
│                   DJANGO VIEWS LAYER                    │
│  • Function-Based Views (FBV)                           │
│  • Class-Based Views (CBV) for REST API                │
│  • Decorators for auth & error handling                 │
└─────────────────────────────────────────────────────────┘
                           ↓
┌─────────────────────────────────────────────────────────┐
│                   BUSINESS LOGIC LAYER                  │
│  • Models (ORM)                                         │
│  • Serializers (DRF)                                    │
│  • NLP Utils (TextBlob, spaCy, NLTK)                   │
│  • Email Backends (Brevo, ZeptoMail, Gmail)            │
└─────────────────────────────────────────────────────────┘
                           ↓
┌─────────────────────────────────────────────────────────┐
│                   DATA LAYER                            │
│  PostgreSQL | SQLite | Redis (optional)                │
└─────────────────────────────────────────────────────────┘
```

---

## Project Structure

```
auth_project/
├── auth_project/              # Project configuration
│   ├── settings.py           # Django settings (comprehensive)
│   ├── urls.py               # Main URL router
│   ├── wsgi.py               # WSGI application
│   └── asgi.py               # ASGI for WebSockets
│
├── accounts/                 # Main application
│   ├── models.py             # 15+ data models
│   ├── views.py              # 100+ view functions (3000+ lines)
│   ├── views_contact.py      # Contact-related views
│   ├── urls.py               # App URL routing
│   ├── serializers.py        # REST API serializers
│   ├── forms.py              # Django forms
│   ├── permissions.py        # DRF permissions
│   ├── utils.py              # NLP utilities & helpers
│   ├── chat_api.py           # Messaging REST API
│   ├── chat_api_improved.py  # Enhanced messaging
│   ├── comment_api.py        # Comment system
│   ├── brevo_mail_backend.py # Email via Brevo
│   ├── zepto_mail_backend.py # Email via ZeptoMail
│   ├── tests.py              # Unit tests
│   └── templates/            # HTML templates (40+ files)
│
├── static/                   # Static files
│   ├── js/                   # JavaScript files
│   ├── css/                  # Stylesheets
│   └── images/               # Images & assets
│
├── media/                    # User uploads
│   └── profile_photos/       # Profile pictures
│
├── requirements.txt          # Python dependencies
├── manage.py                 # Django CLI
└── db.sqlite3               # Local database
```

---

## Core Models (Database Schema)

### 1. **User & Profile Management**

#### StudentProfile
- **Purpose:** Extended user profile with skills and interests
- **Key Fields:**
  - `full_name`, `college`, `location`, `bio`
  - `profile_photo` (ImageField)
  - `skills`, `interests`, `project_interests` (JSON arrays)
  - `github`, `linkedin`, `portfolio`, `behance` (URLs)
  - `profile_completed` (boolean)
  - Timestamps: `created_at`, `updated_at`

#### OTP
- **Purpose:** One-time passwords for authentication/registration
- **Key Fields:**
  - `email`, `otp_code` (6-digit), `purpose` (login/registration/reset)
  - `is_used`, `created_at`, `expires_at` (5 minutes)
- **Methods:**
  - `is_valid()` - Check validity
  - `verify_otp()` - Verify provided code
  - `generate_otp()` - Create new OTP

---

### 2. **Social & Networking**

#### Connection
- **Purpose:** Connection requests between users
- **Fields:** `sender`, `receiver`, `status` (pending/accepted/rejected)
- **Use Cases:** Friend requests, collaboration requests

#### Follow
- **Purpose:** User follower system
- **Fields:** `follower`, `following`, `created_at`
- **Unique Constraint:** One follow per pair

#### Notification
- **Purpose:** User activity notifications
- **Fields:** `user`, `from_user`, `content`, `notification_type`
- **Types:** Connection, message, like, comment, project, follow

---

### 3. **Projects & Collaboration**

#### Project
- **Purpose:** Main collaborative projects
- **Key Fields:**
  - `title`, `description`, `category`
  - `technologies` (JSON), `looking_for` (JSON)
  - `collaboration_needs`, `timeline`, `status`
  - `owner` (ForeignKey to User)
  - `visibility` (public/private/draft)
  - `github_link`, `live_demo_link`
  - Timestamps: `created_at`, `updated_at`

#### ProjectMember
- **Purpose:** Team members with role-based access
- **Roles:** owner, admin, contributor, viewer
- **Permissions:**
  - `can_manage_project` (owner, admin)
  - `can_invite_members` (owner, admin)
  - `can_manage_tasks` (owner, admin, contributor)

#### ProjectInvitation
- **Purpose:** Invitations to join projects
- **Fields:** `project`, `invited_user`, `role`, `status`, `expires_at`
- **Methods:** `accept()`, `decline()`

#### ProjectTask
- **Purpose:** Tasks within projects
- **Status:** todo, in_progress, review, completed, cancelled
- **Priority:** low, medium, high, urgent
- **Fields:** `title`, `assigned_to`, `assigned_by`, `due_date`

#### ProjectMilestone
- **Purpose:** Major milestones in projects
- **Fields:** `title`, `due_date`, `is_completed`, `completed_by`

---

### 4. **Messaging & Communication**

#### ChatRoom
- **Purpose:** Group or direct chat rooms
- **Types:** direct, group
- **Fields:** `name`, `description`, `creator`, `members` (M2M)
- **Methods:** `add_member()`, `remove_member()`, `get_last_message()`

#### Message
- **Purpose:** Individual messages in chat rooms
- **Fields:**
  - `sender`, `receiver`, `chat_room`
  - `content`, `message_type` (text/file/image/call)
  - `reply_to` (self-referential for threading)
  - Timestamps: `created_at`, `updated_at`
- **Methods:**
  - `mark_as_read_by()` - Mark read
  - `is_read_by()` - Check if user read
  - `get_read_count()` - Count readers

#### MessageReadStatus
- **Purpose:** Track message read receipts
- **Fields:** `message`, `user`, `read_at`
- **Optimization:** Separate model for scalability

#### MessageReaction
- **Purpose:** Emoji reactions to messages
- **Fields:** `message`, `user`, `reaction` (emoji/text)

#### MessageFile
- **Purpose:** File attachments to messages
- **Fields:** `message`, `file`, `uploaded_at`

#### File
- **Purpose:** File uploads
- **Fields:** `user`, `file`, `filename`, `file_size`, `file_type`

---

### 5. **Comments & Feedback**

#### Comment
- **Purpose:** Comments on projects
- **Fields:**
  - `project`, `user`, `content`
  - `created_at`, `updated_at`
- **Hierarchy:** Can have parent comments (replies)

#### Like
- **Purpose:** Project likes
- **Fields:** `user`, `project`, `created_at`
- **Constraint:** One like per user-project pair

---

### 6. **Activity & Engagement**

#### Activity
- **Purpose:** User activity feed
- **Types:**
  - profile_updated, project_created, project_liked
  - connection_made, message_sent, comment_added, user_followed
- **Fields:** `user`, `activity_type`, `title`, `description`, `is_public`

#### UserStats
- **Purpose:** User statistics dashboard
- **Fields:**
  - `projects_created`, `connections_made`, `likes_received`
  - `comments_made`, `followers_count`, `following_count`
- **Methods:** `update_stats()`

#### UserStatus
- **Purpose:** Online/offline status
- **Fields:** `user`, `is_online`, `last_seen`

---

## Key Features Breakdown

### 1. **Authentication System**

#### Traditional Login/Register
```python
# Login Flow:
1. User submits credentials
2. Views validate via LoginForm
3. Django authenticates via ModelBackend
4. Session created
5. Redirect to dashboard

# Register Flow:
1. User submits registration form
2. Form validates: username, email, password, terms
3. User created with hashed password
4. StudentProfile created automatically
5. OTP sent for verification
6. Email confirmed via OTP
```

#### OTP Authentication
```python
# For Login/Reset:
1. User enters email
2. 6-digit OTP generated (5-min expiry)
3. Sent via email (Brevo/ZeptoMail)
4. User submits OTP
5. Account authenticated/reset
6. Old OTPs invalidated
```

#### Social Login (OAuth)
```python
# Google OAuth via django-allauth:
- Users can login with Google
- Auto-fetches email, profile picture
- Creates/links StudentProfile
- Supports SOCIALACCOUNT_AUTO_SIGNUP

# GitHub OAuth via django-allauth:
- Similar to Google
- Fetches user:email, read:user scopes
- Auto-signup with email verification
```

---

### 2. **Project Management**

#### Project Creation
```python
# POST /post-project/
- Form: ProjectForm (title, description, technologies)
- Create Project object
- Set creator as owner
- Create ProjectMember with owner role
- Notify followers
- Redirect to project detail

# Key Fields:
- visibility: public/private/draft
- collaboration_needs: JSON array of needs
- technologies: JSON array of tech stack
- status: active/completed/archived
```

#### Project Filtering & Search
```python
# Available Filters:
- By visibility (public/private)
- By category (web, mobile, AI, etc.)
- By technologies
- By creator
- By status
- Text search (title, description, needs)

# Implementation:
- Uses Q() for complex queries
- ProjectVisibilityFilter utility class
- CASE expressions for sorting
```

#### Project Visibility Control
```python
# Visibility Rules:
- Public: Anyone can view
- Private: Only members can view
- Draft: Only owner can view

# Implementation:
- Filter at view level
- Check in detail view
- API respects visibility
```

---

### 3. **Messaging System**

#### Direct Messaging
```python
# Chat Flow:
1. User A initiates chat with User B
2. DirectMessageView creates chat room
3. Messages exchanged in real-time
4. Read receipts tracked via MessageReadStatus
5. Typing indicators shown
6. File attachments supported

# Features:
- Message threading (reply_to)
- Reactions (emoji)
- Read receipts
- Typing indicators
- Message search
- Message drafts
```

#### Group Messaging
```python
# Group Chat:
1. Creator creates ChatRoom (group type)
2. Invites members
3. Members see all messages
4. Read status per user
5. Admin can remove members
6. Notifications for new messages

# Scalability:
- Separate MessageReadStatus model
- Indexed queries
- Pagination support
```

---

### 4. **Comments & Collaboration**

#### Comment System
```python
# Comment Flow:
1. User views project detail
2. Comments section loads (async)
3. User submits comment
4. Comment saved to database
5. Comment displayed in real-time
6. Notifications sent to watchers

# Features:
- Nested replies (parent_comment)
- Edit/delete own comments
- Real-time loading
- Pagination
```

#### Live Feed
```python
# Activity Feed:
1. User opens dashboard
2. Feed loads from Activity model
3. Shows recent activities:
   - Profile updates
   - Projects created
   - Connections made
   - Comments added
4. Filterable by type

# Implementation:
- Activity model with ForeignKeys
- Signals for auto-creation
- Ordering by -created_at
```

---

### 5. **Email System**

#### Multi-Backend Email Support
```python
# Priority Stack:
1. Brevo (Primary)
   - API-based
   - High deliverability
   - For OTP & transactional

2. ZeptoMail (Alternative)
   - Alternative provider
   - Similar API

3. Gmail SMTP (Fallback)
   - Standard SMTP
   - Less reliable for bulk

4. Console (Development)
   - Prints to console
   - For testing

# Configuration:
- Environment-based selection
- Automatic fallback
- Custom backends in accounts/
```

#### OTP Email
```python
# OTP Email Content:
To: user@example.com
Subject: Your OTP Code

Your OTP for [login/registration/password reset]:
[6-digit code]

This code expires in 5 minutes.
```

---

### 6. **Search & Discovery**

#### Project Search
```python
# Search Flow:
1. User enters search query
2. View filters projects:
   - Title match (icontains)
   - Description match
   - Technologies match
   - Collaboration needs match
3. Results paginated
4. Filterable by category, tech

# Implementation:
- Q() objects for OR queries
- icontains for case-insensitive
- Paginator for 10 per page
```

#### Collaborator Discovery
```python
# Find Collaborators:
1. View shows filtered users
2. Filters:
   - By interests
   - By skills
   - By college
   - By project interests
3. Connection suggestions
4. Skill matching

# NLP Integration:
- StudentProfileNLP analyzes profiles
- Extracts skills from bio
- Matches similar interests
- Recommends collaborators
```

---

## API Endpoints

### Authentication Endpoints
```
POST   /login/                    - User login
POST   /register/                 - User registration
POST   /logout/                   - User logout
POST   /forgot-password/          - Request password reset
POST   /reset-password/           - Reset password with OTP
POST   /verify-otp/<purpose>/     - Verify OTP
POST   /resend-otp/<purpose>/     - Resend OTP
```

### Profile Endpoints
```
GET    /profile/                  - Get user profile
PUT    /profile/                  - Update user profile
POST   /student-details/          - Complete student profile
GET    /user/<username>/          - View user profile
GET    /user-profile/<user_id>/   - Get user profile (API)
```

### Project Endpoints
```
GET    /explore-projects/         - List all projects
POST   /post-project/             - Create project
GET    /project-detail/<id>/      - Get project details
PUT    /edit-project/<id>/        - Edit project
DELETE /delete-project/<id>/      - Delete project
GET    /my-projects/              - User's projects
POST   /like-project/<id>/        - Like project
GET    /search-projects/          - Search projects
```

### Messaging Endpoints
```
GET    /messages/                 - Get conversations
GET    /chat/<user_id>/           - Open direct chat
POST   /chat-rooms/               - Create chat room
GET    /chat-rooms/<id>/          - Get chat room
GET    /messages/                 - Get messages
POST   /messages/                 - Send message
POST   /messages/<id>/reactions/  - Add reaction
```

### Social Endpoints
```
POST   /connect/<user_id>/        - Send connection request
POST   /accept-connection/<id>/   - Accept connection
POST   /reject-connection/<id>/   - Reject connection
GET    /my-connections/           - Get connections
POST   /follow/<user_id>/         - Follow user
GET    /activity-feed/            - Get activity feed
```

### Comment Endpoints
```
GET    /api/projects/<id>/comments/          - Get comments
POST   /api/projects/<id>/comments/add/      - Add comment
DELETE /api/comments/<id>/delete/            - Delete comment
PUT    /api/comments/<id>/edit/              - Edit comment
```

### Utility Endpoints
```
POST   /check-username/           - Check username availability
POST   /check-email/              - Check email availability
POST   /college-search/           - Search colleges (RapidAPI)
POST   /validate-college/         - Validate college
GET    /user-stats/               - Get user statistics
POST   /nlp-analyze/              - NLP analysis
```

---

## Views (Controllers)

### Authentication Views
1. **register_view()** - User registration with form validation
2. **login_view()** - Login with email/password or OTP
3. **logout_view()** - Logout and session cleanup
4. **verify_otp_view()** - OTP verification for login/reset
5. **forgot_password_view()** - Request password reset
6. **reset_password_view()** - Reset password with OTP
7. **resend_otp_view()** - Resend OTP code

### Project Views
1. **post_project()** - Create new project
2. **project_detail()** - View project with comments, members
3. **edit_project()** - Edit project details
4. **delete_project()** - Delete project
5. **my_projects_view()** - User's own projects
6. **explore_projects_view()** - Browse all projects
7. **like_project()** - Like/unlike project
8. **search_projects()** - Search and filter projects

### Profile Views
1. **student_profile()** - View own/others' profile
2. **user_profile()** - User profile detail page
3. **edit_profile()** - Edit profile information
4. **dashboard_view()** - Main dashboard with stats

### Messaging Views
1. **message_view()** - Conversations list
2. **chat_view()** - Direct chat with user
3. **enhanced_messages_view()** - Advanced messaging
4. **enhanced_chat_view()** - Group chat
5. **create_group_chat()** - Create new group
6. **add_reaction()** - Add emoji reaction
7. **start_call()** - Initiate voice/video call

### Social Views
1. **find_collaborators()** - Find users to collaborate with
2. **connect_view()** - Send connection request
3. **accept_connection()** - Accept connection
4. **reject_connection()** - Reject connection
5. **my_connections()** - View all connections
6. **follow_user()** - Follow user
7. **activity_feed()** - User activity feed

### API Views
1. **UserProfileView** - CBV for user profiles
2. **ChatRoomListCreateView** - Chat room management
3. **MessageListCreateView** - Message CRUD
4. **MessageSearchView** - Search messages
5. **ConversationListView** - Conversation list
6. **college_search_api()** - Search colleges via RapidAPI
7. **user_stats_api()** - User statistics

---

## Serializers (DRF)

### Core Serializers
```python
UserProfileSerializer
  - user.username, email, full_name, date_joined
  - college, location, interests, bio, skills
  - social links, profile_completed, is_online

ProjectSerializer
  - title, description, technologies, looking_for
  - category, timeline, github_link
  - owner (nested UserProfileSerializer)
  - likes_count, comments_count (method fields)

MessageSerializer
  - content, sender (nested)
  - created_at, message_type
  - reactions (method field with counts)

ConnectionSerializer
  - sender, receiver (nested)
  - status, created_at

NotificationSerializer
  - from_user (nested)
  - content, notification_type
  - is_read, created_at
```

---

## Utilities & Helpers

### StudentProfileNLP
```python
# NLP Analysis for Profiles
- preprocess_text(): Tokenize, lemmatize, remove stopwords
- extract_skills(): Find tech skills in bio/interests
- analyze_interests(): Categorize interests
- extract_keywords(): TF-IDF based keywords
- find_similar_profiles(): Cosine similarity for recommendations
- match_with_projects(): Find relevant projects

# Data:
- TECH_SKILLS: 50+ programming languages/frameworks
- INTEREST_CATEGORIES: 8 major categories (AI, Web, Mobile, etc.)
```

### ProjectVisibilityFilter
```python
# Filter projects by visibility
- get_visible_projects(): Return projects user can see
- Rules:
  - Owner sees all
  - Public visible to all
  - Private visible to members only
  - Draft visible to owner only
```

### Email Backends
```python
# BrevoMailBackend
- Uses Brevo API
- Handles OTP and transactional emails
- Tracks delivery

# ZeptoMailBackend
- Alternative email provider
- Similar to Brevo

# Standard EmailBackend
- SMTP fallback
- Gmail/Office 365 compatible
```

---

## Key Dependencies

### Framework & ORM
- `Django==4.2.8` - Web framework
- `djangorestframework==3.14.0` - REST API
- `psycopg2-binary==2.9.9` - PostgreSQL driver
- `dj-database-url==2.1.0` - Database URL parsing

### Authentication & Social
- `django-allauth==0.61.1` - Social auth, OAuth
- `requests==2.31.0` - HTTP client
- `requests-oauthlib==1.3.1` - OAuth 1/2

### Email & Communications
- `zeptomail==1.0.0` - ZeptoMail integration

### Data Processing & NLP
- `nltk==3.8.1` - Natural language toolkit
- `pandas==2.1.4` - Data manipulation
- `openpyxl==3.1.2` - Excel handling
- `textblob` - Text analysis (implicit)
- `scikit-learn` - ML utilities (implicit)
- `spacy` - NLP (implicit)

### Image & File Handling
- `Pillow==10.1.0` - Image processing

### Caching & Performance
- `redis==5.0.1` - Redis client
- `django-redis==5.4.0` - Django Redis integration

### Real-time Features
- `channels==4.0.0` - WebSockets
- `channels-redis==4.1.0` - Redis backend for channels

### File Storage
- `boto3==1.34.34` - AWS S3
- `django-storages==1.14.2` - Storage backends

### Monitoring
- `sentry-sdk==1.38.0` - Error tracking

### Production
- `gunicorn==21.2.0` - Application server
- `whitenoise==6.6.0` - Static file serving

### Development
- `django-debug-toolbar==4.2.0` - Debugging
- `pytest==7.4.3` - Testing framework
- `black==23.12.1` - Code formatter
- `flake8==6.1.0` - Linting

---

## Settings Configuration

### Database
```python
# PostgreSQL (Production via Render)
if DATABASE_URL:
    DATABASES = dj_database_url.parse(DATABASE_URL)

# SQLite (Local Development)
else:
    DATABASES = {'default': {'ENGINE': 'django.db.backends.sqlite3'}}
```

### Email Backend Selection
```python
if BREVO_API_KEY:
    EMAIL_BACKEND = 'accounts.brevo_mail_backend.BrevoMailBackend'
elif ZEPTO_MAIL_API_KEY:
    EMAIL_BACKEND = 'accounts.zepto_mail_backend.ZeptoMailBackend'
elif EMAIL_HOST_USER:
    EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
else:
    EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'
```

### Authentication Backends
```python
AUTHENTICATION_BACKENDS = (
    'django.contrib.auth.backends.ModelBackend',  # Default
    'allauth.account.auth_backends.AuthenticationBackend',  # Social
)
```

### REST Framework
```python
REST_FRAMEWORK = {
    'DEFAULT_PERMISSION_CLASSES': ['rest_framework.permissions.AllowAny'],
    'DEFAULT_PAGINATION_CLASS': 'rest_framework.pagination.PageNumberPagination',
    'PAGE_SIZE': 10,
    'DEFAULT_FILTER_BACKENDS': ['rest_framework.filters.SearchFilter'],
}
```

### Social Login Providers
```python
SOCIALACCOUNT_PROVIDERS = {
    'google': {
        'SCOPE': ['profile', 'email'],
        'AUTH_PARAMS': {'access_type': 'online'},
    },
    'github': {
        'SCOPE': ['user:email', 'read:user'],
    }
}
```

### Logging
```python
LOGGING = {
    'version': 1,
    'handlers': {
        'console': {...},
        'file': {...},
        'error_file': {...}
    },
    'loggers': {
        'django': {...},
        'accounts': {...}
    }
}
```

---

## Templates (Frontend)

### Key Template Files (40+)

#### Authentication Templates
- `register.html` - Registration form
- `login.html` - Login form
- `verify_otp.html` - OTP verification
- `forgot_password.html` - Password reset request
- `reset_password.html` - Password reset form

#### Project Templates
- `project_feed.html` - Browse projects
- `project_detail.html` - Project details with comments
- `post_project.html` - Create project form
- `edit_project.html` - Edit project form
- `my_projects.html` - User's projects

#### Profile Templates
- `profile.html` - User profile page
- `student_profile.html` - Student profile view
- `edit_profile.html` - Edit profile form
- `find_collaborators.html` - Collaborator discovery

#### Messaging Templates
- `messages.html` - Conversations list
- `chat.html` - Direct message chat
- `enhanced_messages.html` - Advanced messaging UI

#### Utility Templates
- `dashboard.html` - Main dashboard
- `home.html` - Homepage
- `base.html` - Base template with navbar
- `activity_feed.html` - Activity feed
- `notifications.html` - Notifications page
- `help_center.html` - Help/documentation
- `premium.html` - Premium features
- `terms_of_service.html` - Terms
- `privacy_policy.html` - Privacy policy

---

## Security Features

### CSRF Protection
```python
# Enabled via middleware
'django.middleware.csrf.CsrfViewMiddleware'

# Templates use {% csrf_token %}
# AJAX requests include CSRF token
```

### Password Validation
```python
# Validators:
- UserAttributeSimilarityValidator (not similar to username/email)
- MinimumLengthValidator (min 8 characters)
- CommonPasswordValidator (not in common list)
- NumericPasswordValidator (not all numeric)

# Custom validation in RegisterForm:
- Uppercase required
- Lowercase required
- Digit required
```

### SSL/HTTPS
```python
SECURE_SSL_REDIRECT = os.getenv('SECURE_SSL_REDIRECT', 'False')
SESSION_COOKIE_SECURE = os.getenv('SESSION_COOKIE_SECURE', 'False')
CSRF_COOKIE_SECURE = os.getenv('CSRF_COOKIE_SECURE', 'False')
```

### Authentication Backends
```python
# Django ModelBackend + Allauth
# Session authentication for REST API
# OAuth support via django-allauth
```

---

## Data Flow Examples

### User Registration Flow
```
1. User fills RegisterForm (username, email, password, terms)
2. Form validates:
   - Username unique
   - Email unique & valid
   - Password meets requirements
   - Passwords match
3. User saved with hashed password
4. StudentProfile created (empty)
5. Verification email sent with OTP
6. User verifies OTP
7. Account activated
8. Redirect to complete profile
```

### Project Creation & Discovery Flow
```
1. User clicks "Post Project"
2. ProjectForm opened
3. User enters:
   - Title, description
   - Technologies (JSON array)
   - Looking for (roles needed)
   - Collaboration needs
   - GitHub link
4. Project saved
   - visibility = 'public' (default)
   - owner = current user
   - status = 'active'
5. ProjectMember created (owner role)
   - Activity logged
   - Followers notified

6. Another user explores projects
   - Filters by category/tech
   - Searches keywords
   - Sees public projects
   - Can comment/like
   - Can request to join
```

### Messaging Flow
```
1. User A opens chat with User B
2. DirectMessageView creates ChatRoom (type='direct')
3. ChatRoomMember added for both users
4. User A sends message:
   - Message created
   - content, sender, receiver, chat_room
   - created_at = now
5. User B receives notification
   - Notification created
6. User B opens chat:
   - Messages loaded
   - Message.mark_as_read_by(User B)
   - MessageReadStatus created
7. User A sees read receipt
   - Checks message.is_read_by(User B)
   - Shows "Read" indicator
```

### Comment & Like Flow
```
1. User views project_detail
2. Comments load async via API
3. User submits comment:
   - Comment created (project, user, content)
   - Activity created (project owner notified)
4. Like button clicked:
   - Like object created or deleted
   - like_count updated
   - Activity logged (if new)
5. Real-time update:
   - JavaScript refreshes counts
   - Comments reloaded
```

---

## Performance Optimizations

### Database
```python
# Query Optimization:
- select_related() for ForeignKey
- prefetch_related() for M2M
- only() for specific fields
- defer() to exclude heavy fields

# Indexes:
- user_id (Activity, Comment, Like)
- created_at (queries ordering)
- project_id (filtering)

# Pagination:
- 10 items per page (configurable)
- Reduces data transfer
- Faster page loads
```

### Caching
```python
# Redis Integration:
- SESSION_ENGINE = 'django_redis...'
- Cache queries if configured
- Cache API responses

# Cache Decorator:
- @cache_page(60) for stable data
- Reduces database queries
```

### File Storage
```python
# Local Development:
- MEDIA_ROOT = 'media/'
- Simple FileStorage

# Production:
- AWS S3 via django-storages
- CDN integration possible
- Offloads from server
```

### Static Files
```python
# WhiteNoise:
- Serves static files in production
- No separate web server needed
- Compression support
- Cache headers
```

---

## Testing

### Test Files
```
accounts/tests.py          # Unit tests
test_login.py              # Login functionality
test_profile_fix.py        # Profile views
test_otp.py                # OTP generation/verification
test_email.py              # Email sending
test_filtering_debug.py    # Project filtering
```

### Test Coverage
- Authentication tests
- Profile CRUD tests
- Project visibility tests
- Message read status tests
- Connection request tests

---

## Deployment

### Environment Variables Required
```bash
# Core
SECRET_KEY=your_secret_key
DEBUG=False
ALLOWED_HOSTS=yourdomain.com

# Database
DATABASE_URL=postgresql://...

# Email
BREVO_API_KEY=your_api_key
# OR
ZEPTO_MAIL_API_KEY=...
ZEPTO_MAIL_TOKEN=...
# OR
EMAIL_HOST_USER=...
EMAIL_HOST_PASSWORD=...

# Social Login
GOOGLE_CLIENT_ID=...
GOOGLE_CLIENT_SECRET=...
GITHUB_CLIENT_ID=...
GITHUB_CLIENT_SECRET=...

# External Services
RAPIDAPI_KEY=...
```

### Deployment Targets
- **Render** - Recommended (render.yaml configured)
- **Railway** - Alternative (railway.json configured)
- **Heroku** - Traditional (Procfile provided)

---

## Common Issues & Solutions

### Email Not Sending
```python
# Check priority order:
1. BREVO_API_KEY set? → Use BrevoMailBackend
2. ZEPTO credentials set? → Use ZeptoMailBackend
3. Gmail credentials set? → Use SMTP
4. Fall back to console for development

# Logs:
- Check logs/django.log
- Console output shows which backend
```

### Profile Photo Not Displaying
```python
# Check:
1. Profile.profile_photo exists
2. Media files configured in settings
3. URL patterns include media serving
4. File permissions allow reading

# Debug:
- Check MEDIA_URL in template: {{ profile.profile_photo.url }}
- Ensure static files collected: python manage.py collectstatic
```

### Visibility Filter Not Working
```python
# Root Cause:
- ProjectVisibilityFilter not checking owner
- Public/private logic reversed

# Fix:
- Check visibility field in filter
- Ensure owner check: user == project.owner
```

### OTP Expires Too Fast
```python
# Check:
- expires_at calculation: timezone.now() + timedelta(minutes=5)
- is_valid() checks expiration: timezone.now() < self.expires_at

# Configuration:
- Change timedelta(minutes=5) to desired timeout
```

---

## Code Quality Standards

### Naming Conventions
- Snake_case for files, functions, variables
- PascalCase for classes
- UPPER_CASE for constants
- Descriptive, meaningful names

### Documentation
- Docstrings on classes and functions
- Inline comments for complex logic
- README and guide files

### Best Practices
- DRY principle (Don't Repeat Yourself)
- SOLID principles
- Model validation in forms
- Error handling with try/except
- Logging important operations

---

## Summary Statistics

| Metric | Count |
|--------|-------|
| Models | 15+ |
| Views | 100+ |
| Templates | 40+ |
| API Endpoints | 40+ |
| Test Files | 10+ |
| Lines of Code | 10,000+ |
| Dependencies | 50+ |

---

## Next Steps for Development

### Quick Wins
1. Add message encryption
2. Implement real-time notifications (WebSockets)
3. Add video calling (Twilio)
4. Improve project recommendations (ML)

### Medium-term
1. Mobile app (React Native)
2. Advanced analytics dashboard
3. Skill certification system
4. Project portfolio showcasing

### Long-term
1. Marketplace for project gigs
2. Mentor matching system
3. Internship listings
4. University partnerships

---

**End of Analysis**  
Generated: 2026-02-03
