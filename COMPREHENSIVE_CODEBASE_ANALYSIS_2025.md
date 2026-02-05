# UniSync - Comprehensive Codebase Analysis

**Project Name:** UniSync  
**Repository:** https://github.com/Goku0090/uni  
**Tech Stack:** Django + PostgreSQL/SQLite + Bootstrap  
**Last Updated:** February 2025

---

## Executive Summary

UniSync is a Django-based collaborative platform designed to connect university students for project collaboration. It features:

- **Authentication**: Email/OTP-based login, social login (Google/GitHub)
- **User Profiles**: Student profiles with skills, interests, project preferences
- **Project Management**: Create, edit, delete projects with visibility controls
- **Messaging System**: Real-time chat with group support, file sharing
- **Comments & Activity Feed**: Live comments on projects with activity tracking
- **Social Features**: Follow/Connect system, notifications, activity tracking
- **Search & Discovery**: Find collaborators, projects, and colleges

---

## Architecture Overview

### Layer Structure

```
┌─────────────────────────────────────────────────────────────┐
│                     Frontend (Templates/JS)                   │
│  - HTML Templates in accounts/templates/                      │
│  - Custom JavaScript (login.js, profile.js, api-utils.js)     │
│  - Bootstrap-based responsive UI                              │
└─────────────────┬───────────────────────────────────────────┘
                  │
┌─────────────────▼───────────────────────────────────────────┐
│              Django Application Layer (Backend)              │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐       │
│  │ URL Routing  │  │ Views/Logic  │  │ API Handlers │       │
│  │ (urls.py)    │  │ (views.py)   │  │ (*_api.py)   │       │
│  └──────────────┘  └──────────────┘  └──────────────┘       │
└─────────────────┬───────────────────────────────────────────┘
                  │
┌─────────────────▼───────────────────────────────────────────┐
│              Data Layer (Models)                              │
│  - User & StudentProfile                                      │
│  - Project, ProjectMember, ProjectTask, ProjectMilestone     │
│  - Message, ChatRoom, MessageReadStatus                      │
│  - Comment, Like, Follow, Connection                         │
│  - Activity, Notification, OTP                               │
└─────────────────┬───────────────────────────────────────────┘
                  │
┌─────────────────▼───────────────────────────────────────────┐
│              Database (PostgreSQL/SQLite)                     │
└─────────────────────────────────────────────────────────────┘
```

---

## Key Components

### 1. Authentication & Authorization

**Files:**
- `views.py`: `login_view()`, `register_view()`, `verify_otp_view()`, `reset_password_view()`
- `models.py`: `OTP` model
- `settings.py`: Allauth configuration for Google/GitHub OAuth

**Flow:**
```
1. User registers with email + password
2. OTP sent via email (Brevo/ZeptoMail/Gmail SMTP)
3. User verifies OTP
4. Account created + StudentProfile initialized
5. Login redirects to dashboard

Alternative: Social login via Google/GitHub (Allauth)
```

**Key Features:**
- 6-digit OTP with 5-minute expiry
- Multiple email backends (Brevo primary, ZeptoMail fallback, Gmail SMTP, console)
- OTP marking logic: `is_used` flag prevents reuse
- Password reset flow with OTP verification

### 2. User Profiles & Student Details

**Models:**
- `StudentProfile`: Full name, college, interests, skills, bio, social links, profile photo
- Extended User model via OneToOneField relationship

**API Endpoints:**
- `GET/POST /api/user-profile/<user_id>/` - Retrieve user profile
- `GET/POST /accounts/student-details/` - Student profile form
- `GET /accounts/student-profile/` - View student profile

**Features:**
- Profile completion tracking
- College autocomplete via RapidAPI
- Photo upload with validation (jpg, jpeg, png, gif)
- Skills/interests stored as JSON arrays

### 3. Project Management

**Models:**
- `Project`: title, description, visibility (public/private/friends), category, status
- `ProjectMember`: Associate users with roles (owner, admin, contributor, viewer)
- `ProjectTask`: Track tasks within projects (todo, in_progress, review, completed)
- `ProjectMilestone`: Track project milestones
- `ProjectInvitation`: Team invitations with acceptance/decline workflow

**API Endpoints:**
- `POST /accounts/post-project/` - Create new project
- `GET/POST /accounts/edit-project/<project_id>/` - Edit project
- `DELETE /accounts/delete-project/<project_id>/` - Delete project
- `GET /accounts/project-detail/<project_id>/` - View project details
- `POST /accounts/like-project/<project_id>/` - Like a project

**Features:**
- Visibility filtering (public/private/friends-only)
- Project member management with role-based permissions
- Team invitation system with expiry
- Task and milestone tracking
- Like counter for projects

### 4. Messaging System

**Models:**
- `Message`: Text, file, image, call types with threading support
- `ChatRoom`: Group chats and direct conversations
- `MessageReadStatus`: Track read receipts per user
- `MessageFile`: File attachments
- `MessageReaction`: Emoji/text reactions
- `File`: File storage and metadata

**API Endpoints:**
```
Chat Management:
  POST /api/chat-rooms/
  GET /api/chat-rooms/<id>/
  GET /api/chat-rooms/<room_id>/members/

Messages:
  GET/POST /api/messages/
  GET /api/messages/<pk>/
  GET /api/messages/search/
  POST /api/messages/<message_id>/status/
  POST /api/messages/<message_id>/reactions/

Direct Messages:
  POST /api/direct-message/
  
Conversations:
  GET /api/conversations/
```

**Features:**
- Real-time message sync
- Read status tracking
- Message threading/replies
- File upload & sharing
- Emoji reactions
- Typing indicators
- Draft messages
- Search functionality

### 5. Comments & Live Feed

**Models:**
- `Comment`: Project comments with replies support
- Related to `Project` and `User`

**API Endpoints:**
```
GET /api/projects/<project_id>/comments/          # Get all comments
POST /api/projects/<project_id>/comments/add/     # Add comment
DELETE /api/comments/<comment_id>/delete/         # Delete comment
POST /api/comments/<comment_id>/edit/             # Edit comment
```

**Features:**
- Nested comment threads (reply_to support)
- Live feed updates
- Comment editing/deletion
- User attribution

### 6. Social Features

**Models:**
- `Connection`: Send/accept/reject connection requests
- `Follow`: Follow users for activity tracking
- `Like`: Like projects
- `Activity`: Track user activities (profile_updated, project_created, etc.)
- `Notification`: Notify users of events

**API Endpoints:**
```
Connections:
  POST /accounts/send-connection/<user_id>/
  POST /accounts/accept-connection/<connection_id>/
  POST /accounts/reject-connection/<connection_id>/
  GET /accounts/my-connections/

Following:
  POST /accounts/follow/<user_id>/

Activity:
  GET /accounts/activity-feed/

Notifications:
  GET /accounts/notifications/
  POST /accounts/mark-notification-read/<notification_id>/
```

**Features:**
- Connection requests (pending → accepted/rejected)
- Follow system for activity tracking
- Like counter on projects
- Activity timestamps
- Notification system

### 7. Collaborator Discovery

**Models:**
- Leverages `StudentProfile`, `Project`, `Connection`, `Follow`

**API Endpoints:**
- `GET /accounts/find-collaborators/` - Discover collaborators
- `GET /accounts/user/<username>/` - View user profile

**Features:**
- Filter by college, skills, interests
- Search functionality
- Connection status display
- Project visibility

---

## Database Schema

### Core Tables

**Users & Profiles:**
- `auth_user` - Django User model
- `accounts_studentprofile` - Extended student info

**Projects:**
- `accounts_project` - Project metadata
- `accounts_projectmember` - Project team members
- `accounts_projecttask` - Tasks within projects
- `accounts_projectmilestone` - Project milestones
- `accounts_projectinvitation` - Team invitations

**Messaging:**
- `accounts_message` - Messages (text, files, calls)
- `accounts_chatroom` - Chat groups/conversations
- `accounts_messagereadstatus` - Read receipts
- `accounts_messagereaction` - Message reactions
- `accounts_file` - File uploads

**Social:**
- `accounts_connection` - Connection requests
- `accounts_follow` - Follow relationships
- `accounts_like` - Project likes
- `accounts_activity` - Activity log
- `accounts_notification` - User notifications

**Comments:**
- `accounts_comment` - Project comments

**Authentication:**
- `accounts_otp` - One-time passwords

### Relationships

```
User (1) ──────────────────── (1) StudentProfile
    │
    ├─────► (Many) Project (as creator/owner)
    ├─────► (Many) ProjectMember
    ├─────► (Many) Message (as sender)
    ├─────► (Many) ChatRoom (as member)
    ├─────► (Many) Comment
    ├─────► (Many) Connection (sent/received)
    ├─────► (Many) Follow
    ├─────► (Many) Like
    └─────► (Many) Activity

Project (1) ──────────────── (Many) ProjectMember
Project (1) ──────────────── (Many) ProjectTask
Project (1) ──────────────── (Many) ProjectMilestone
Project (1) ──────────────── (Many) Comment
Project (1) ──────────────── (Many) Like

Message (1) ──────────────── (Many) MessageReaction
Message (1) ──────────────── (Many) MessageReadStatus
Message (1) ──────────────── (Many) MessageFile
Message (0..1) ──────────── (1) ChatRoom
Message (0..1) ──────────── (1) Message (reply_to - self-referencing)

ChatRoom (1) ──────────────── (Many) ChatRoomMember
ChatRoom (1) ──────────────── (Many) Message
```

---

## Configuration & Settings

### Email Configuration (Priority Order)

1. **Brevo** (Primary - Recommended)
   - API Key: `BREVO_API_KEY`
   - Backend: `accounts.brevo_mail_backend.BrevoMailBackend`

2. **ZeptoMail** (Alternative)
   - Tokens: `ZEPTO_MAIL_API_KEY`, `ZEPTO_MAIL_TOKEN`
   - Backend: `accounts.zepto_mail_backend.ZeptoMailBackend`

3. **Gmail SMTP** (Fallback)
   - Credentials: `EMAIL_HOST_USER`, `EMAIL_HOST_PASSWORD`
   - Backend: `django.core.mail.backends.smtp.EmailBackend`

4. **Console** (Development)
   - Backend: `django.core.mail.backends.console.EmailBackend`

### Database Configuration

**Priority:**
1. `DATABASE_URL` (Render deployment)
2. PostgreSQL (env vars: `DB_NAME`, `DB_USER`, `DB_PASSWORD`, `DB_HOST`, `DB_PORT`)
3. SQLite (fallback for development)

### Social Authentication (Allauth)

**Providers:**
- Google (scope: profile, email)
- GitHub (scope: user:email, read:user)

**Config:**
```python
SOCIALACCOUNT_AUTO_SIGNUP = True
SOCIALACCOUNT_LOGIN_ON_GET = True
ACCOUNT_EMAIL_VERIFICATION = 'none'
```

### REST Framework Settings

```python
DEFAULT_PERMISSION_CLASSES: AllowAny
DEFAULT_AUTHENTICATION_CLASSES: SessionAuthentication
DEFAULT_PAGINATION_CLASS: PageNumberPagination
PAGE_SIZE: 10
MAX_PAGE_SIZE: 100
```

---

## File Structure

```
auth_project/
├── auth_project/                 # Project settings
│   ├── settings.py              # Django configuration
│   ├── urls.py                  # Main URL routing
│   ├── wsgi.py                  # WSGI application
│   └── asgi.py                  # ASGI application
│
├── accounts/                     # Main app
│   ├── models.py                # Data models (16+ models)
│   ├── views.py                 # View logic (login, register, dashboard, etc.)
│   ├── views_contact.py         # Contact/legal pages
│   ├── urls.py                  # App URL routing
│   ├── forms.py                 # Form definitions
│   ├── serializers.py           # DRF serializers
│   ├── permissions.py           # Custom permissions
│   ├── utils.py                 # Utility functions
│   ├── comment_api.py           # Comment API endpoints
│   ├── chat_api.py              # Messaging API endpoints
│   ├── chat_api_improved.py     # Enhanced chat API
│   ├── brevo_mail_backend.py    # Brevo email service
│   ├── zepto_mail_backend.py    # ZeptoMail service
│   │
│   ├── templates/               # HTML templates
│   │   ├── base.html            # Base template
│   │   ├── login.html
│   │   ├── register.html
│   │   ├── dashboard.html
│   │   ├── project_detail.html
│   │   ├── chat.html
│   │   ├── messages.html
│   │   ├── find_collaborators.html
│   │   ├── project_feed.html
│   │   └── ...
│   │
│   ├── static/                  # Static files
│   │   ├── js/
│   │   │   ├── login.js
│   │   │   ├── profile.js
│   │   │   ├── api-utils.js
│   │   │   └── ...
│   │   └── css/
│   │
│   └── templatetags/            # Custom template tags
│       └── custom_filters.py
│
├── static/                      # Project-wide static files
├── media/                       # User uploads (profiles, files)
├── logs/                        # Application logs
└── manage.py                    # Django management
```

---

## Key Features Implementation

### 1. OTP-Based Authentication

**Flow:**
1. User registers → POST /register/
2. Email validation → OTP generated with 5-min expiry
3. User enters OTP → POST /verify-otp/login/
4. OTP verified → mark as `is_used = True`
5. Account activated → redirect to login/dashboard

**Code Location:** `models.py` - OTP class, `views.py` - verify_otp_view()

### 2. Project Visibility & Filtering

**Visibility Levels:**
- `public` - Visible to all users
- `private` - Only owner can view
- `friends_only` - Only connected users can view

**Implementation:** Query filtering in views based on visibility and user permissions

### 3. Real-Time Messaging

**Features:**
- One-to-one direct messages
- Group chat rooms
- File/image sharing
- Read receipts (via MessageReadStatus)
- Message threading (reply_to)
- Typing indicators
- Draft message support

**API:** REST endpoints for CRUD + search

### 4. Live Comment Feed

**Features:**
- Nested comments (reply to parent comment)
- Edit/delete comments
- Real-time updates via API
- Comment timestamps
- User attribution

**Implementation:** API endpoints in comment_api.py

### 5. Activity & Notifications

**Activity Types:**
- profile_updated
- project_created
- project_liked
- connection_made
- message_sent
- comment_added
- user_followed
- task_completed
- milestone_completed

**Implementation:** Activity model logged on actions, notifications triggered

---

## Important Configuration Files

### .env Variables Required

```
# Core
DEBUG=True/False
SECRET_KEY=your_secret_key
ALLOWED_HOSTS=localhost,127.0.0.1

# Database
DATABASE_URL=postgresql://user:pass@host/dbname
DB_NAME=unisync_db
DB_USER=unisync_user
DB_PASSWORD=password
DB_HOST=localhost
DB_PORT=5432

# Email
BREVO_API_KEY=your_brevo_api_key
ZEPTO_MAIL_API_KEY=your_zepto_key
ZEPTO_MAIL_TOKEN=your_zepto_token
EMAIL_HOST_USER=your_email@gmail.com
EMAIL_HOST_PASSWORD=your_app_password
DEFAULT_FROM_EMAIL=noreply@unisync.app

# Social Auth
GOOGLE_CLIENT_ID=your_google_client_id
GOOGLE_CLIENT_SECRET=your_google_secret
GITHUB_CLIENT_ID=your_github_client_id
GITHUB_CLIENT_SECRET=your_github_secret

# APIs
RAPIDAPI_KEY=your_rapidapi_key
RAPIDAPI_HOST=universities-list.p.rapidapi.com

# Security (Production)
SECURE_SSL_REDIRECT=True
SESSION_COOKIE_SECURE=True
CSRF_COOKIE_SECURE=True
```

---

## Common Issues & Solutions

### Issue 1: Emails Not Sending
**Cause:** Email backend not configured  
**Solution:** Set BREVO_API_KEY or email credentials in .env

### Issue 2: OTP Expired
**Cause:** User takes >5 minutes to verify  
**Solution:** Resend OTP via /resend-otp/ endpoint

### Issue 3: Comments Not Showing
**Cause:** API endpoint URL mismatch or visibility filter  
**Solution:** Check project visibility and API response status

### Issue 4: Messages Not Syncing
**Cause:** MessageReadStatus not created properly  
**Solution:** Check ChatRoom members list and read_statuses relationship

### Issue 5: Project Not Visible in Feed
**Cause:** Visibility set to private or friends_only  
**Solution:** Update project visibility or add user as friend

---

## Testing & Development

**Test Files Present:**
- test_login.py - Login flow testing
- test_profile_fix.py - Profile functionality
- test_profile_upload.py - Photo upload
- test_filter.py - Filtering logic
- test_feed_fix.py - Feed display
- test_otp.py - OTP verification
- test_email.py - Email sending

**Run Tests:**
```bash
python manage.py test
python manage.py test accounts.tests
```

---

## Deployment

### Supported Platforms
- Render (PostgreSQL provided)
- Railway (PostgreSQL)
- Heroku (legacy)

### Configuration Files
- `Procfile` - Process configuration
- `render.yaml` - Render deployment config
- `railway.json` - Railway deployment config

### Deployment Steps
1. Set environment variables
2. Configure DATABASE_URL
3. Run migrations: `python manage.py migrate`
4. Collect static files: `python manage.py collectstatic --noinput`
5. Start server: `gunicorn auth_project.wsgi`

---

## Performance Considerations

### Optimizations
1. **Database Indexes:** Consider indexes on frequently queried fields
2. **Pagination:** REST API uses pagination (default PAGE_SIZE=10)
3. **Read Receipts:** MessageReadStatus prevents storing boolean per user-message
4. **Logging:** Rotating file handlers for log management
5. **Static Files:** Served via STATIC_ROOT/STATIC_URL

### Known Slow Operations
- Full profile search (no pagination mentioned)
- Activity feed without filtering
- Comments without pagination

---

## Security Observations

### Good Practices
✅ Password validation (validators configured)  
✅ CSRF protection enabled  
✅ Session security settings  
✅ Email verification via OTP  
✅ Social auth via Allauth (industry standard)

### Areas to Review
⚠️ REST API set to `AllowAny` permissions  
⚠️ ACCOUNT_EMAIL_VERIFICATION = 'none' (no email confirmation)  
⚠️ OTP stored in plaintext (consider hashing)  
⚠️ File uploads need validation beyond extension

---

## Recent Development Notes

The codebase shows signs of recent updates:
- Multiple email backend implementations (Brevo, ZeptoMail, Gmail)
- Enhanced messaging system with chat_api_improved.py
- Comment API for live feed
- Profile viewing improvements
- Message read status tracking
- Project visibility filtering

---

## Next Steps for Development

1. **Frontend Refactoring:** Consolidate duplicate templates
2. **API Documentation:** Add OpenAPI/Swagger docs
3. **Testing Coverage:** Expand test suite with fixtures
4. **Performance:** Add caching for frequently accessed data
5. **Real-Time Features:** Consider WebSockets for live updates
6. **Mobile Optimization:** Improve responsive design

---

*Analysis completed February 3, 2025*
