# UniSync Codebase Comprehensive Analysis

**Date:** January 29, 2026  
**Repository:** https://github.com/Goku0090/uni  
**Project Type:** Django-based Collaborative Learning Platform

---

## Table of Contents
1. [Project Overview](#project-overview)
2. [Architecture](#architecture)
3. [Core Components](#core-components)
4. [Database Models](#database-models)
5. [Authentication & Authorization](#authentication--authorization)
6. [Features Implementation](#features-implementation)
7. [API Endpoints](#api-endpoints)
8. [Email System](#email-system)
9. [Frontend Structure](#frontend-structure)
10. [Dependencies](#dependencies)
11. [Key Technologies](#key-technologies)
12. [Current Issues & Areas for Improvement](#current-issues--areas-for-improvement)

---

## Project Overview

**UniSync** is a Django-based web platform that enables:
- Student collaboration and project discovery
- Direct messaging and group chat
- Connection/networking between users
- Project management with team features
- User profiles and activity feeds
- OTP-based authentication
- Social login integration (Google, GitHub)

**Target Users:** Students and professionals looking for collaborators on projects

---

## Architecture

### High-Level Structure
```
auth_project/
├── auth_project/        # Django project config
│   ├── settings.py      # Configuration & environment setup
│   ├── urls.py          # Main URL routing
│   ├── wsgi.py          # Production server
│   └── asgi.py          # WebSocket support
├── accounts/            # Main application
│   ├── models.py        # Database schemas
│   ├── views.py         # Business logic & rendering
│   ├── forms.py         # Django forms
│   ├── urls.py          # App URL routing
│   ├── serializers.py   # REST API serialization
│   ├── services/        # Business logic services
│   ├── utils.py         # Utilities (NLP, filtering)
│   ├── chat_api.py      # Messaging API
│   ├── views_contact.py # Contact pages
│   ├── permissions.py   # Permission classes
│   └── templates/       # HTML templates
├── static/              # CSS, JS, images
├── media/               # User uploads
└── logs/                # Application logs
```

**Design Pattern:** MTV (Model-Template-View) + REST API

---

## Core Components

### 1. Django Configuration (settings.py)
**Purpose:** Central configuration hub for the entire application

**Key Features:**
- **Database:** PostgreSQL (production) / SQLite (development fallback)
- **Authentication:** Django's built-in + django-allauth (social login)
- **Email Backends:** Multiple support (Brevo, ZeptoMail, Gmail SMTP, Console)
- **REST Framework:** DRF with session authentication
- **Static/Media:** Configured for local development and cloud storage
- **Logging:** File rotation with separate error logs
- **Security:** CSRF protection, SSL redirect flags

**Email Priority System:**
1. Brevo API (production recommended)
2. ZeptoMail API (alternative)
3. Gmail SMTP (fallback)
4. Console backend (development)

### 2. URL Routing (urls.py)
**Core Routes:**
- Authentication: `/login/`, `/register/`, `/logout/`, `/verify-otp/`, `/reset-password/`
- Projects: `/post-project/`, `/edit-project/`, `/delete-project/`, `/explore-projects/`
- Messaging: `/messages/`, `/chat/`, `/enhanced-messages/`
- Social: `/find-collaborators/`, `/connect/`, `/my-connections/`
- Notifications: `/notifications/`, `/activity-feed/`
- REST API: `/api/chat-rooms/`, `/api/messages/`, `/api/conversations/`

### 3. Views Architecture
**Main View File:** `views.py` (3193 lines)

**View Categories:**
1. **Authentication Views**
   - `register_view()` - User registration with validation
   - `login_view()` - Login with email/username + OTP fallback
   - `verify_otp_view()` - OTP verification (login/registration/reset)
   - `forgot_password_view()` - Password reset initiation
   - `reset_password_view()` - Password reset completion

2. **Profile Views**
   - `student_profile()` - View user profile
   - `student_details_view()` - Edit profile details
   - `edit_profile()` - Avatar and profile updates
   - `user_profile()` - View other users' profiles

3. **Project Management**
   - `post_project()` - Create new project
   - `edit_project()` - Modify project
   - `delete_project()` - Remove project
   - `project_detail()` - View project with team & tasks
   - `explore_projects_view()` - Browse all projects (with filtering)
   - `my_projects_view()` - User's own projects

4. **Messaging & Chat**
   - `message_view()` - Direct messaging interface
   - `chat_view()` - 1-on-1 conversation
   - `enhanced_messages_view()` - Advanced messaging UI
   - `enhanced_chat_view()` - Group chat interface
   - `create_group_chat()` - Create chat room
   - `add_reaction()` - Message reactions

5. **Networking/Social**
   - `find_collaborators()` - Search for collaborators
   - `send_connection_request()` - Send connection
   - `accept_connection()` / `reject_connection()` - Connection responses
   - `my_connections()` - List connections
   - `follow_user()` - Follow functionality
   - `activity_feed()` - Activity stream

6. **Team Management**
   - `invite_to_team()` - Invite users to project
   - `respond_to_team_invitation()` - Accept/decline invites
   - `remove_team_member()` - Remove from team

7. **Utility Views**
   - `dashboard_view()` - User dashboard
   - `main_home()` / `main()` - Homepage
   - `notifications_view()` - Notification center
   - `help_center_view()` - Help/FAQ

---

## Database Models

### User-Related Models

**1. StudentProfile**
```
- OneToOne: User
- Fields: full_name, college, location, interests, bio, profile_photo
- Profile Links: github, linkedin, portfolio, behance
- Skills/Interests: skills[], project_interests[]
- Status: profile_completed, role_preference
- Timestamps: created_at, updated_at
```

**2. OTP**
```
- email (EmailField)
- otp_code (6-digit CharField)
- purpose (login/registration/reset)
- is_used (BooleanField)
- created_at, expires_at (DateTimeField)
- Methods: generate_otp(), verify_otp(), is_valid()
```

**3. UserStatus**
- Online/offline status tracking

**4. UserStats**
- OneToOne: User
- Counters: projects_created, connections_made, likes_received, followers_count, etc.
- Method: update_stats() - synchronizes with actual data

### Connection Models

**1. Connection**
```
- Foreign Keys: sender, receiver (User)
- Status: pending/accepted/rejected
- Unique constraint: (sender, receiver)
- Timestamps: created_at, updated_at
```

**2. Follow**
```
- Foreign Keys: follower, following (User)
- Unique constraint: (follower, following)
- Timestamp: created_at
```

### Project Models

**1. Project**
```
- Foreign Key: user (owner)
- Fields: title, description, category
- Visibility: visibility (public/private/collaborative)
- Collaboration:
  - technologies (JSONField array)
  - looking_for (JSONField array of roles)
  - collaboration_needs (TextField)
  - timeline (CharField)
- Social: likes_count, comments_count, views_count
- Status: is_completed, is_archived
- Timestamps: created_at, updated_at
```

**2. ProjectMember**
```
- Foreign Keys: project, user
- Roles: owner/admin/contributor/viewer
- Status: is_active
- Timestamp: joined_at
- Permissions: can_manage_project, can_edit_project, can_manage_tasks, can_invite_members
```

**3. ProjectInvitation**
```
- Foreign Keys: project, invited_user, invited_by
- Status: pending/accepted/declined/expired
- Role: project member role
- Methods: accept(), decline()
```

**4. ProjectTask**
```
- Foreign Key: project
- Status: todo/in_progress/review/completed/cancelled
- Priority: low/medium/high/urgent
- Fields: title, description, due_date
- Assignment: assigned_to (User), assigned_by (User)
- Method: mark_completed()
```

**5. ProjectMilestone**
```
- Foreign Key: project
- Status: is_completed
- Fields: title, description, due_date
- Method: mark_completed(user)
```

### Messaging Models

**1. Message**
```
- Foreign Keys: sender (User), receiver (User, nullable), chat_room (ChatRoom, nullable)
- Content: content (TextField), message_type (text/file/image/call)
- Threading: reply_to (ForeignKey to self)
- Metadata: call_type (voice/video)
- Timestamps: created_at, updated_at
- Methods: mark_as_read_by(), is_read_by(), get_read_count(), get_unread_users()
```

**2. MessageReadStatus**
```
- Foreign Keys: message, user
- Timestamp: read_at
- Purpose: Track read status at scale (vs read_by field)
```

**3. MessageFile**
```
- Foreign Keys: message, file
- Timestamp: uploaded_at
```

**4. MessageReaction**
```
- Foreign Keys: message, user
- Field: reaction (emoji/text)
- Unique constraint: (message, user, reaction)
```

**5. File**
```
- Foreign Key: user
- Fields: file (FileField), filename, file_size, file_type
- Timestamp: created_at
```

### Chat Room Models

**1. ChatRoom**
```
- Foreign Key: created_by (User)
- Fields: name, description, chat_type (direct/group)
- Timestamps: created_at, updated_at
```

**2. ChatRoomMember**
```
- Foreign Keys: chat_room, user
- Status: is_active
- Timestamp: joined_at
```

### Engagement Models

**1. Like**
```
- Foreign Keys: user, project
- Timestamp: created_at
```

**2. Comment**
```
- Foreign Keys: user, project
- Field: text (TextField)
- Threading: reply_to (ForeignKey to self)
- Timestamps: created_at, updated_at
```

**3. Notification**
```
- Foreign Key: user
- Fields: notification_type, title, message, is_read
- Foreign Keys: sender (User), project (nullable)
- Timestamp: created_at
```

**4. Activity**
```
- Foreign Key: user
- Type: profile_updated/project_created/project_liked/connection_made/etc.
- Fields: title, description
- Related: project, target_user, connection
- Timestamp: created_at
```

---

## Authentication & Authorization

### Authentication Flow

**1. Standard Registration**
```
1. User enters email, username, password (with validation)
2. Backend creates Django User + StudentProfile
3. OTP sent to email
4. User verifies OTP
5. Account created, user redirected to login
```

**2. OTP-Based Login**
```
1. User enters email
2. OTP sent to email
3. User verifies OTP code
4. Session created, user logged in
```

**3. Social Login (Google/GitHub)**
```
1. User clicks social provider
2. django-allauth handles OAuth flow
3. CustomSocialSignupForm collects additional profile data
4. StudentProfile created
```

**4. Password Reset**
```
1. User enters email in forgot password form
2. OTP sent to email
3. User verifies OTP
4. User sets new password
5. Password updated, user can login
```

### Authorization

**Model-Level Permissions:**
- `ProjectMember.can_manage_project` - owner/admin only
- `ProjectMember.can_edit_project` - owner/admin/contributor
- `ProjectMember.can_manage_tasks` - owner/admin/contributor
- `ProjectMember.can_invite_members` - owner/admin

**View-Level Protection:**
- `@login_required` decorator on protected views
- Permission checks for project ownership/membership
- Public/private project visibility logic

---

## Features Implementation

### 1. Project Management
**Creation:**
- Form-based with rich fields: title, description, category, technologies, timeline
- Team role selection (looking_for)
- GitHub link integration
- Collaboration needs description

**Visibility Control:**
- public: visible to all
- private: only to owner
- collaborative: visible to team members

**Team Management:**
- Add members via invitation (with role assignment)
- Accept/decline invitations (with expiry)
- Remove members
- Role-based permissions

**Project Features:**
- Likes/comments system
- View count tracking
- Task management with status/priority
- Milestones with completion tracking
- Activity logging

### 2. Messaging System

**Direct Messages:**
- 1-to-1 conversation tracking
- Message read status via MessageReadStatus model
- File attachments
- Message reactions (emoji)
- Message threading (reply_to)

**Group Chat:**
- ChatRoom model for group conversations
- Multiple members per chat
- Direct group messaging
- Enhanced messaging with rich features

**Advanced Features:**
- Typing indicators
- Message search
- Draft messages
- Call support (voice/video)
- Unread message counting

### 3. Networking/Collaboration
**Connection System:**
- Send/accept/reject connection requests
- Connection status tracking (pending/accepted)
- Mutual connection management

**Follow System:**
- Follow/unfollow users
- Follow count tracking
- Activity feed based on follows

**Collaborator Discovery:**
- Search by skills, interests, projects
- Filter by technology stack
- NLP-based recommendation

### 4. Profile System
**Student Profile:**
- Full name, college, location, bio
- Profile photo upload
- Skills (JSON array)
- Project interests (JSON array)
- Social links (GitHub, LinkedIn, Portfolio, Behance)
- Profile completion status
- View on public profile pages

**Activity Tracking:**
- User activity feed (projects, connections, follows, etc.)
- Public/private activity settings
- Timestamp tracking

### 5. Email System

**Multiple Backends:**

```python
# Priority: Brevo → ZeptoMail → Gmail → Console

if BREVO_API_KEY:
    EMAIL_BACKEND = 'accounts.brevo_mail_backend.BrevoMailBackend'
elif ZEPTO_MAIL_API_KEY:
    EMAIL_BACKEND = 'accounts.zepto_mail_backend.ZeptoMailBackend'
elif EMAIL_HOST_USER and EMAIL_HOST_PASSWORD:
    EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
    # Gmail SMTP config
else:
    EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'
```

**Email Use Cases:**
- OTP delivery for login, registration, password reset
- Welcome emails
- Notification emails
- Connection request notifications
- Project invitation emails

---

## API Endpoints

### REST API (DRF-based)

**Base URL:** `/api/`

**Chat Management:**
- `POST /chat-rooms/` - Create chat room
- `GET /chat-rooms/` - List chat rooms
- `GET /chat-rooms/<id>/` - Get room details
- `PUT /chat-rooms/<id>/` - Update room
- `GET /chat-rooms/<room_id>/members/` - Get room members

**Messaging:**
- `POST /messages/` - Create message
- `GET /messages/` - List messages
- `GET /messages/<pk>/` - Get message details
- `GET /messages/search/` - Search messages
- `GET /messages/<message_id>/status/` - Get message read status
- `POST /messages/<message_id>/reactions/` - Add reaction

**Direct Messages:**
- `POST /direct-message/` - Send direct message

**Utilities:**
- `GET /conversations/` - List conversations
- `POST /typing/` - Send typing indicator
- `GET /drafts/` - Get draft messages
- `POST /drafts/` - Create draft

**Other APIs:**
- `GET /college-search/` - Search colleges
- `POST /validate-college/` - Validate college
- `GET /user-profile/<user_id>/` - Get user profile
- `GET /user-stats/` - Get user statistics
- `POST /nlp-analyze/` - NLP analysis endpoint

---

## Forms Implementation

### Authentication Forms

**RegisterForm (UserCreationForm)**
- Validates username (uniqueness, length)
- Validates email (uniqueness, format)
- Validates password (min 8 chars, uppercase, lowercase, digit)
- Terms of service checkbox
- Comprehensive error messages

**LoginForm (AuthenticationForm)**
- Username/email field
- Password field
- Remember me checkbox
- Styled with Bootstrap classes

**OTPVerificationForm**
- 6-digit OTP input
- Pattern validation (numeric only)
- Placeholder and maxlength attributes

### Profile Forms

**StudentProfileForm (ModelForm)**
- Full name, college, location
- Bio (textarea)
- Profile photo upload (image validation)
- Skills (checkboxes - 16 options)
- Project interests (checkboxes - 12 options)
- Social links (GitHub, LinkedIn, Portfolio, Behance)
- Role preference dropdown

**ProjectForm (ModelForm)**
- Title (5-200 chars)
- Description (20-5000 chars)
- Technologies (checkboxes - 50+ options)
- Looking for (checkboxes - 21 roles)
- Category (dropdown - 18 categories)
- Timeline (text field)
- Collaboration needs (textarea)
- GitHub link (URL validation)

**CustomSocialSignupForm**
- Full name (required)
- College (optional)
- Interests (optional)
- Custom signup() method saves to StudentProfile

---

## Email System Architecture

### Brevo Backend (`brevo_mail_backend.py`)
```python
class BrevoMailBackend(EmailBackend):
    def send_messages(self, email_messages):
        # Uses Brevo API to send emails
        # Configuration: BREVO_API_KEY
        # Supports subject, body, recipients
```

### ZeptoMail Backend (`zepto_mail_backend.py`)
```python
class ZeptoMailBackend(EmailBackend):
    def send_messages(self, email_messages):
        # Uses Zeptomail API
        # Configuration: ZEPTO_MAIL_API_KEY, ZEPTO_MAIL_TOKEN
```

### Usage in Views
```python
# OTP Email
send_mail(
    subject='Your OTP Code',
    message=f'Your OTP is: {otp.otp_code}',
    from_email=settings.DEFAULT_FROM_EMAIL,
    recipient_list=[email],
    html_message=html_content  # Optional HTML
)
```

---

## Frontend Structure

### Templates Organization
```
templates/
├── accounts/
│   ├── base.html          # Base template
│   ├── login.html         # Login page
│   ├── register.html      # Registration page
│   ├── verify_otp.html    # OTP verification
│   ├── dashboard.html     # User dashboard
│   ├── student_profile.html
│   ├── project_*.html     # Project management
│   ├── chat_*.html        # Messaging
│   ├── messages.html      # Direct messages
│   └── explore_projects.html
└── allauth/
    └── account/           # Allauth templates
```

### Static Files
```
static/
├── css/
│   ├── base.css
│   ├── dashboard.css
│   ├── projects.css
│   └── responsive.css
├── js/
│   ├── main.js
│   ├── chat.js
│   ├── project_filtering.js
│   └── notifications.js
└── images/
    ├── logo.png
    └── placeholders/
```

---

## Dependencies

### Core Framework
- **Django 4.2.8** - Web framework
- **djangorestframework 3.14.0** - REST API
- **django-allauth 0.61.1** - Social authentication
- **psycopg2-binary 2.9.9** - PostgreSQL driver
- **dj-database-url 2.1.0** - Database URL parsing

### Email & Communications
- **zeptomail 1.0.0** - Email service
- **requests 2.31.0** - HTTP requests

### Data Processing
- **nltk 3.8.1** - Natural language toolkit
- **pandas 2.1.4** - Data manipulation
- **openpyxl 3.1.2** - Excel handling

### Security & Performance
- **django-cors-headers 4.3.1** - CORS handling
- **django-redis 5.4.0** - Redis caching
- **redis 5.0.1** - Redis client

### Real-time Features
- **channels 4.0.0** - WebSocket support
- **channels-redis 4.1.0** - Redis backend for channels

### File Storage
- **boto3 1.34.34** - AWS S3
- **django-storages 1.14.2** - Cloud storage

### Task Queue
- **celery 5.3.4** - Background tasks

### Development
- **pytest 7.4.3** - Testing framework
- **black 23.12.1** - Code formatter
- **flake8 6.1.0** - Linter
- **mypy 1.7.1** - Type checking

---

## Key Technologies

### Architecture Decisions

**1. Multi-Tenant Email System**
- Primary: Brevo (production-grade API)
- Fallback chain ensures robustness
- Console backend for development

**2. OTP-Based Auth**
- Supports email-only login
- Password recovery via OTP
- 5-minute expiry, single-use
- Customizable purpose (login/registration/reset)

**3. Social Login**
- Google OAuth via allauth
- GitHub OAuth via allauth
- Custom signup form for additional data

**4. Scalable Messaging**
- Separate MessageReadStatus model (vs boolean field)
- ChatRoom abstraction for group chats
- Message threading support
- Rich message types (text, file, image, call)

**5. Project Visibility Control**
- public: visible to all
- private: owner only
- collaborative: team members + explicit sharing

**6. NLP-Powered Features**
- Skill extraction from profile text
- Interest categorization
- Project recommendation
- Collaborator matching

---

## Current Issues & Areas for Improvement

### 1. Security Concerns
**Issue:** SECRET_KEY auto-generated in development
```python
# Current (development only):
if not SECRET_KEY:
    import secrets
    SECRET_KEY = secrets.token_urlsafe(50)
```
**Recommendation:** Always use environment variables, fail on missing SECRET_KEY in production

### 2. Database Performance
**Issue:** Potential N+1 queries in views
**Recommendation:** Add select_related/prefetch_related for:
- `Project.objects.select_related('user', 'user__student_profile')`
- `Message.objects.select_related('sender', 'receiver')`

### 3. Pagination
**Issue:** Manual pagination in some views, inconsistent approach
**Recommendation:** Standardize DRF pagination across all list views

### 4. Error Handling
**Issue:** Generic error messages in @handle_view_errors decorator
**Recommendation:** Implement specific error handling per view

### 5. Testing Coverage
**Issue:** Limited test files (tests.py mostly empty)
**Recommendation:** Add pytest fixtures and test suite

### 6. Code Organization
**Issue:** views.py is 3193 lines (monolithic)
**Recommendation:** Split into:
- views/auth.py
- views/projects.py
- views/messaging.py
- views/social.py
- views/profiles.py

### 7. Email Configuration
**Issue:** Multiple backends but no fallback retry logic
**Recommendation:** Implement retry mechanism and failure logging

### 8. Rate Limiting
**Issue:** No rate limiting on API endpoints
**Recommendation:** Add django-ratelimit or DRF throttling

### 9. Caching Strategy
**Issue:** Cache configuration exists but minimal usage
**Recommendation:** Cache frequently accessed data:
- User profiles
- Project listings
- Connection status
- Activity feeds

### 10. API Documentation
**Issue:** No API documentation (swagger/openapi)
**Recommendation:** Use drf-spectacular (already in requirements)

### 11. WebSocket Configuration
**Issue:** Channels installed but no WebSocket endpoints visible
**Recommendation:** Implement real-time messaging via WebSockets

### 12. Image Processing
**Issue:** Profile photos and project images uploaded without optimization
**Recommendation:** Add Pillow image optimization (easy-thumbnails)

### 13. Logging
**Issue:** Basic logging configuration
**Recommendation:** Enhance with Sentry integration (already in requirements)

---

## Summary Statistics

| Metric | Value |
|--------|-------|
| Main Models | 20+ |
| Views | 50+ |
| URL Patterns | 100+ |
| API Endpoints | 20+ |
| Django Apps | 1 (accounts) |
| Forms | 5+ |
| Email Backends | 4 |
| Authentication Methods | 4 |
| Project Categories | 18 |
| Skills (form) | 16 |
| Project Interests | 12 |
| Looking For Roles | 21 |
| Database Engines Supported | 3 (PostgreSQL, SQLite, MySQL) |

---

## Development Recommendations

1. **Immediate:** Fix security issues (SECRET_KEY, CSRF)
2. **Short-term:** Add comprehensive testing, split views.py
3. **Medium-term:** Implement WebSockets, optimize queries, add caching
4. **Long-term:** Microservices architecture, message queue optimization

---

## Deployment Checklist

- [ ] Set all required environment variables (.env.template provided)
- [ ] Configure PostgreSQL (Render or self-hosted)
- [ ] Set email backend (Brevo recommended)
- [ ] Configure social OAuth (Google/GitHub)
- [ ] Set SECRET_KEY securely
- [ ] Enable SECURE_SSL_REDIRECT for production
- [ ] Set SESSION_COOKIE_SECURE and CSRF_COOKIE_SECURE
- [ ] Configure allowed hosts
- [ ] Set up static files collection
- [ ] Configure media storage (S3 optional)
- [ ] Set up logging rotation
- [ ] Enable SENTRY_SDK for monitoring

---

**Generated:** 2026-01-29  
**Analysis Version:** 1.0
