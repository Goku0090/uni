# UniSync - Complete Codebase Analysis 2026

**Project**: UniSync (Collaboration Platform)  
**Tech Stack**: Django 4.x + PostgreSQL + Django Channels + DRF + Google OAuth  
**Last Updated**: February 8, 2026

---

## 📋 Table of Contents

1. [Project Overview](#project-overview)
2. [Architecture](#architecture)
3. [Core Models](#core-models)
4. [API Endpoints](#api-endpoints)
5. [Views & Controllers](#views--controllers)
6. [Real-Time Features](#real-time-features)
7. [Frontend Components](#frontend-components)
8. [Authentication & Security](#authentication--security)
9. [Email System](#email-system)
10. [Database Schema](#database-schema)
11. [Key Features Breakdown](#key-features-breakdown)

---

## Project Overview

### Purpose
UniSync is a web-based collaboration platform for students to:
- Create and manage projects
- Find and connect with collaborators
- Post project updates
- Comment on projects
- Direct messaging
- Real-time notifications
- User profiles with skill matching

### Key Technologies
- **Backend**: Django 4.x (Python web framework)
- **Database**: PostgreSQL (production) / SQLite (development)
- **Real-Time**: Django Channels + WebSockets
- **API**: Django Rest Framework (DRF)
- **Authentication**: Django-Allauth + Google OAuth + Email OTP
- **Email**: Brevo / ZeptoMail / Gmail SMTP
- **Frontend**: HTML5 + Bootstrap + Vanilla JavaScript
- **Deployment**: Render.com (Railway support)

---

## Architecture

### High-Level System Design

```
┌─────────────────────────────────────────────────────────────┐
│                      Frontend Layer                         │
│  (HTML Templates + Bootstrap + Vanilla JavaScript)          │
└────────────┬────────────────────────────────────────────────┘
             │ HTTP/AJAX                    │ WebSocket
             ▼                              ▼
┌─────────────────────────────────────────────────────────────┐
│                      Django Backend                         │
│  ┌──────────────────────────────────────────────────────┐  │
│  │  Views Layer                                         │  │
│  │  - Authentication Views                             │  │
│  │  - Project Management Views                         │  │
│  │  - Profile Management Views                         │  │
│  │  - Messaging Views                                  │  │
│  └──────────────────────────────────────────────────────┘  │
│  ┌──────────────────────────────────────────────────────┐  │
│  │  API Layer (DRF)                                     │  │
│  │  - REST Serializers                                 │  │
│  │  - Generic Views / ViewSets                         │  │
│  │  - Comment API                                      │  │
│  │  - Chat API                                         │  │
│  └──────────────────────────────────────────────────────┘  │
│  ┌──────────────────────────────────────────────────────┐  │
│  │  Models Layer (ORM)                                  │  │
│  │  - User Models                                      │  │
│  │  - Project Models                                   │  │
│  │  - Social Models (Messages, Comments, Connections)  │  │
│  │  - Activity & Notification Models                   │  │
│  └──────────────────────────────────────────────────────┘  │
│  ┌──────────────────────────────────────────────────────┐  │
│  │  WebSocket Consumers (Django Channels)               │  │
│  │  - Project Updates Consumer                         │  │
│  │  - Activity Feed Consumer                           │  │
│  │  - Notification Consumer                            │  │
│  └──────────────────────────────────────────────────────┘  │
│  ┌──────────────────────────────────────────────────────┐  │
│  │  Utilities & Services                                │  │
│  │  - Email Service (Brevo/ZeptoMail/Gmail)             │  │
│  │  - OTP Generation & Verification                    │  │
│  │  - Profile NLP Matching                             │  │
│  │  - Project Visibility Filtering                     │  │
│  │  - Signal Handlers (Real-time Updates)              │  │
│  └──────────────────────────────────────────────────────┘  │
└─────────────────────────────────────────────────────────────┘
             │                              │
             ▼                              ▼
┌──────────────────────┐      ┌──────────────────────┐
│  PostgreSQL DB       │      │  Redis/InMemory      │
│  - Users             │      │  Channel Layers      │
│  - Projects          │      │  (WebSocket Relay)   │
│  - Messages/Comments │      │                      │
│  - Profiles/Stats    │      │                      │
└──────────────────────┘      └──────────────────────┘
```

### Directory Structure

```
auth_project/                          # Django Project Root
├── auth_project/                      # Project Configuration
│   ├── settings.py                    # Django settings (DB, installed apps, middleware)
│   ├── urls.py                        # Main URL routing
│   ├── asgi.py                        # ASGI config for WebSockets
│   └── wsgi.py                        # WSGI config for HTTP
│
├── accounts/                          # Main Django App
│   ├── models.py                      # Database models (Core)
│   ├── views.py                       # Traditional views (Large - 3000+ lines)
│   ├── urls.py                        # App-level URL routing
│   ├── serializers.py                 # DRF Serializers
│   ├── forms.py                       # Django Forms
│   ├── consumers.py                   # WebSocket consumers
│   ├── routing.py                     # WebSocket routing
│   ├── signals_realtime.py            # Signal handlers for real-time updates
│   ├── comment_api.py                 # Comment API endpoints
│   ├── chat_api_improved.py           # Chat/Messaging API
│   ├── views_contact.py               # Contact form views
│   ├── utils.py                       # Utility functions
│   ├── brevo_mail_backend.py          # Brevo email backend
│   ├── zepto_mail_backend.py          # ZeptoMail email backend
│   │
│   ├── templates/                     # HTML Templates
│   │   ├── login.html                 # Login page
│   │   ├── register.html              # Registration page
│   │   ├── verify_otp.html            # OTP verification
│   │   ├── main_home.html             # Main feed/dashboard
│   │   ├── project_detail.html        # Project details page
│   │   ├── profile.html               # User profile page
│   │   ├── messages.html              # Messaging interface
│   │   ├── notifications.html         # Notifications page
│   │   ├── find_collaborators.html    # Collaborator search
│   │   ├── my_projects.html           # User's projects list
│   │   └── components/footer.html     # Reusable footer
│   │
│   └── static/js/                     # JavaScript
│       ├── realtime-updates.js        # WebSocket connection handler
│       ├── comments-handler.js        # Comment functionality
│       ├── messages-api.js            # Messaging API client
│       ├── messages-ui.js             # Message UI updates
│       └── login.js                   # Login form handling
│
├── static/                            # Global static files
│   ├── js/                            # Global JavaScript
│   ├── css/                           # Stylesheets
│   └── images/                        # Images & logos
│
├── media/                             # User uploads
│   └── profile_photos/                # Profile pictures
│
├── templates/                         # Global templates
└── manage.py                          # Django management script
```

---

## Core Models

### 1. **User-Related Models**

#### **StudentProfile**
```
Fields:
- user (OneToOneField → User)
- full_name, college, location
- bio, profile_photo (ImageField)
- interests, skills, project_interests (JSONField)
- role_preference (student, mentor, etc.)
- github, linkedin, portfolio, behance (URLs)
- profile_completed (Boolean)
- created_at, updated_at (DateTimeField)

Purpose: Extended user profile with skills and interests
```

#### **UserStatus**
```
Fields:
- user (OneToOneField)
- status (active/inactive/away)
- last_seen (DateTimeField)

Purpose: Track user availability for real-time updates
```

#### **UserStats**
```
Fields:
- user (OneToOneField)
- projects_created, connections_made
- likes_received, comments_made
- followers_count, following_count
- last_updated

Purpose: Cache user statistics for performance
```

---

### 2. **Project & Collaboration Models**

#### **Project**
```
Fields:
- user (ForeignKey → User, project owner)
- title, description, collaboration_needs (TextField)
- category (CharField - choices)
- project_image, thumbnail
- status (active/completed/paused)
- visibility (public/private/team-only)
- created_at, updated_at

Methods:
- get_collaborators() → returns all project members
- is_owner(user) → checks ownership
- get_comments_count() → returns comment count

Purpose: Core project model
```

#### **ProjectMember** (formerly ProjectTeamMember)
```
Fields:
- project (ForeignKey)
- user (ForeignKey)
- role (owner/admin/contributor/viewer) [CharField]
- is_active (Boolean)
- joined_at (DateTimeField)

Properties:
- can_manage_project → role in ['owner', 'admin']
- can_edit_project → role in ['owner', 'admin', 'contributor']
- can_manage_tasks → can edit if contributor+
- can_invite_members → admin/owner only

Purpose: Track project membership with permission levels
```

#### **ProjectInvitation**
```
Fields:
- project (ForeignKey)
- invited_user (ForeignKey)
- invited_by (ForeignKey)
- role (CharField, choices from ProjectMember.ROLES)
- status (pending/accepted/declined/expired)
- created_at, expires_at, responded_at

Methods:
- accept() → creates ProjectMember, marks as accepted
- decline() → marks as declined

Purpose: Track project invitations
```

#### **ProjectTask**
```
Fields:
- project (ForeignKey)
- title, description (TextField)
- assigned_to, assigned_by (ForeignKey → User)
- status (todo/in_progress/review/completed/cancelled)
- priority (low/medium/high/urgent)
- due_date, completed_at
- created_at, updated_at

Methods:
- mark_completed() → updates status & timestamp

Purpose: Task management within projects
```

#### **ProjectMilestone**
```
Fields:
- project (ForeignKey)
- title, description
- due_date, is_completed (Boolean)
- completed_at, completed_by
- created_at, updated_at

Methods:
- mark_completed(user) → marks as done

Purpose: Project milestone tracking
```

---

### 3. **Social & Communication Models**

#### **Connection** (User-to-User)
```
Fields:
- sender (ForeignKey → User)
- receiver (ForeignKey → User)
- status (pending/accepted/rejected)
- created_at, updated_at

Constraints:
- unique_together: ['sender', 'receiver']

Purpose: Track user connections/friend requests
```

#### **Message**
```
Fields:
- sender (ForeignKey → User)
- receiver (ForeignKey → User, null if group)
- chat_room (ForeignKey, null)
- content (TextField)
- message_type (text/file/image/call)
- reply_to (ForeignKey to self for threading)
- created_at, updated_at

Methods:
- mark_as_read_by(user) → creates MessageReadStatus
- is_read_by(user) → checks if read
- get_read_count() → returns read count
- get_unread_users() → returns who hasn't read

Purpose: Direct and group messaging
```

#### **MessageReadStatus**
```
Fields:
- message (ForeignKey)
- user (ForeignKey)
- read_at (DateTimeField)

Purpose: Track message read status for multiple users
```

#### **MessageReaction**
```
Fields:
- message (ForeignKey)
- user (ForeignKey)
- reaction (CharField - emoji/text)
- created_at

Constraints:
- unique_together: ['message', 'user', 'reaction']

Purpose: Emoji reactions to messages
```

#### **ChatRoom**
```
Fields:
- name (CharField)
- description (TextField)
- chat_type (direct/group)
- created_by (ForeignKey → User)
- created_at, updated_at

Purpose: Group chat containers
```

#### **ChatRoomMember**
```
Fields:
- chat_room (ForeignKey)
- user (ForeignKey)
- is_active (Boolean)
- joined_at

Purpose: Track chat room membership
```

#### **Comment**
```
Fields:
- project (ForeignKey)
- user (ForeignKey)
- content (TextField)
- parent_comment (ForeignKey to self, for nested)
- likes_count, replies_count (PositiveIntegerField)
- is_edited (Boolean)
- created_at, updated_at

Methods:
- get_replies() → returns nested comments
- like(user) → adds like
- unlike(user) → removes like

Purpose: Comment on projects
```

---

### 4. **Activity & Engagement Models**

#### **Like**
```
Fields:
- user (ForeignKey)
- project (ForeignKey)
- created_at

Purpose: Project likes/votes
```

#### **Follow**
```
Fields:
- follower (ForeignKey)
- following (ForeignKey)
- created_at

Purpose: User-to-user follows
```

#### **Activity**
```
Fields:
- user (ForeignKey)
- activity_type (CharField - profile_updated/project_created/etc)
- title (CharField)
- description (TextField)
- project (ForeignKey, optional)
- target_user (ForeignKey, optional)
- connection (ForeignKey, optional)
- is_public (Boolean)
- created_at

Purpose: User activity feed / audit trail
```

#### **Notification**
```
Fields:
- user (ForeignKey)
- activity (ForeignKey → Activity)
- message (TextField)
- is_read (Boolean)
- created_at

Purpose: User notifications
```

#### **OTP**
```
Fields:
- email (EmailField)
- otp_code (CharField, 6 digits)
- purpose (login/registration/reset)
- is_used (Boolean)
- created_at, expires_at (5 min expiry)

Methods:
- is_valid() → checks expiry and usage
- verify_otp(code) → verifies code
- generate_otp(email, purpose) → creates new OTP

Purpose: Email-based OTP authentication
```

---

## API Endpoints

### Base URL: `/api/`

### 1. **Authentication Endpoints**

| Method | Endpoint | Purpose |
|--------|----------|---------|
| POST | `/auth/register/` | User registration with email/password |
| POST | `/auth/login/` | Email + OTP login |
| POST | `/auth/verify-otp/` | Verify OTP code |
| POST | `/auth/logout/` | Logout user |
| POST | `/auth/forgot-password/` | Request password reset |
| POST | `/auth/reset-password/` | Reset password with OTP |

### 2. **User Profile Endpoints**

| Method | Endpoint | Purpose |
|--------|----------|---------|
| GET | `/users/profile/` | Get current user profile |
| PUT | `/users/profile/` | Update user profile |
| GET | `/users/<id>/profile/` | Get specific user profile |
| POST | `/users/profile/avatar/` | Upload profile photo |
| GET | `/users/search/` | Search users by name/skills |

### 3. **Project Endpoints**

| Method | Endpoint | Purpose |
|--------|----------|---------|
| GET | `/projects/` | List all projects (paginated) |
| POST | `/projects/` | Create new project |
| GET | `/projects/<id>/` | Get project details |
| PUT | `/projects/<id>/` | Update project |
| DELETE | `/projects/<id>/` | Delete project |
| GET | `/projects/<id>/members/` | Get project members |
| POST | `/projects/<id>/invite/` | Invite user to project |
| POST | `/projects/<id>/like/` | Like/unlike project |
| GET | `/projects/feed/` | Get user's project feed |
| POST | `/projects/search/` | Search projects |
| GET | `/projects/<id>/analytics/` | Get project analytics |

### 4. **Comment Endpoints**

| Method | Endpoint | Purpose |
|--------|----------|---------|
| GET | `/projects/<id>/comments/` | Get project comments |
| POST | `/projects/<id>/comments/` | Post comment |
| PUT | `/comments/<id>/` | Update comment |
| DELETE | `/comments/<id>/` | Delete comment |
| POST | `/comments/<id>/like/` | Like comment |
| POST | `/comments/<id>/reply/` | Reply to comment |

### 5. **Messaging Endpoints**

| Method | Endpoint | Purpose |
|--------|----------|---------|
| GET | `/messages/` | List user conversations |
| GET | `/messages/<user_id>/` | Get conversation with user |
| POST | `/messages/send/` | Send message |
| PUT | `/messages/<id>/` | Edit message |
| DELETE | `/messages/<id>/` | Delete message |
| POST | `/messages/<id>/read/` | Mark message as read |
| POST | `/chat-rooms/` | Create group chat |
| GET | `/chat-rooms/<id>/` | Get chat room |
| POST | `/chat-rooms/<id>/leave/` | Leave chat room |

### 6. **Connection/Follow Endpoints**

| Method | Endpoint | Purpose |
|--------|----------|---------|
| POST | `/connections/request/` | Send connection request |
| GET | `/connections/` | Get user connections |
| PUT | `/connections/<id>/accept/` | Accept connection |
| PUT | `/connections/<id>/reject/` | Reject connection |
| POST | `/follow/` | Follow user |
| POST | `/unfollow/` | Unfollow user |

### 7. **Notification Endpoints**

| Method | Endpoint | Purpose |
|--------|----------|---------|
| GET | `/notifications/` | Get user notifications |
| PUT | `/notifications/<id>/` | Mark as read |
| DELETE | `/notifications/<id>/` | Delete notification |

### 8. **Collaborator Search**

| Method | Endpoint | Purpose |
|--------|----------|---------|
| GET | `/collaborators/search/` | Advanced collaborator search with filters |
| GET | `/collaborators/suggestions/` | Get collaborator suggestions based on skills |

---

## Views & Controllers

### Key View Functions

#### **Authentication Views**
```python
File: accounts/views.py

1. register(request) → User registration with email/password
2. login_view(request) → Display login form
3. login_otp(request) → Send OTP to email
4. verify_otp_view(request) → Verify OTP code
5. logout_view(request) → Logout user
6. forgot_password(request) → Password reset flow
7. reset_password(request) → Complete password reset
```

#### **Dashboard & Feed Views**
```python
1. main_home(request) → Main feed (projects + activities)
2. dashboard_view(request) → User dashboard
3. project_feed(request) → User's project feed
4. activity_feed(request) → Activity feed
5. notifications_view(request) → Notifications page
```

#### **Project Management Views**
```python
1. post_project(request) → Create new project
2. project_detail(request, project_id) → Project details + comments
3. edit_project(request, project_id) → Edit project
4. delete_project(request, project_id) → Delete project
5. my_projects(request) → List user's projects
6. search_projects(request) → Project search with filters
7. find_collaborators(request) → Collaborator matching
```

#### **Profile Views**
```python
1. student_profile(request) → View own profile
2. view_profile(request, user_id) → View other user's profile
3. edit_profile(request) → Edit profile
4. upload_profile_photo(request) → Upload avatar
```

#### **Messaging Views**
```python
1. messages(request) → Messaging interface
2. send_message(request) → Send message (API)
3. get_conversation(request, user_id) → Get DM thread
4. mark_message_read(request, message_id) → Mark read
```

#### **API Views (DRF)**
```python
File: accounts/serializers.py + comment_api.py + chat_api_improved.py

1. UserProfileSerializer → Serialize user profiles
2. ProjectSerializer → Serialize projects
3. CommentSerializer → Serialize comments
4. MessageSerializer → Serialize messages
5. ProjectListView (generic.ListCreateAPIView) → List/create projects
6. ProjectDetailView (generic.RetrieveUpdateDestroyAPIView) → CRUD projects
```

---

## Real-Time Features

### WebSocket Implementation

#### **File: accounts/consumers.py**

**ProjectUpdateConsumer**
- Handles real-time project updates
- Groups: `project_<id>`
- Events: 
  - `member_added` → New team member
  - `task_created` → New task
  - `comment_added` → New comment
  - `project_updated` → Project info changed

**ActivityFeedConsumer**
- Streams activity feed updates
- Groups: `activity_user_<id>`
- Events:
  - `activity_created` → New activity
  - `activity_deleted` → Activity removed

**NotificationConsumer**
- Sends user notifications
- Groups: `notifications_<id>`
- Events:
  - `notify` → New notification
  - `notification_read` → Mark as read

#### **File: accounts/signals_realtime.py**

Signals handlers that trigger WebSocket broadcasts:

```python
@receiver(post_save, sender=Project)
def project_updated_signal(sender, instance, created, **kwargs):
    # Broadcast to project_<id> group
    
@receiver(post_save, sender=Comment)
def comment_created_signal(sender, instance, created, **kwargs):
    # Broadcast to project_<id> and activity groups

@receiver(post_save, sender=ProjectMember)
def member_joined_signal(sender, instance, created, **kwargs):
    # Broadcast to project_<id> group
```

#### **File: static/js/realtime-updates.js**

Client-side WebSocket handler:

```javascript
// Create WebSocket connection
let socket = new WebSocket("ws://localhost:8000/ws/project/2/");

socket.onopen = () => {
    console.log("✅ WebSocket connected");
};

socket.onmessage = (e) => {
    let data = JSON.parse(e.data);
    // Handle different event types
    if (data.type === 'comment_added') {
        updateComments(data.comment);
    } else if (data.type === 'member_added') {
        updateMembers(data.member);
    }
};

socket.onerror = (e) => {
    console.error("WebSocket error:", e);
    reconnectWithBackoff();
};
```

---

## Frontend Components

### Key Templates & JavaScript

#### **Main Pages**
1. **login.html** - Login form with Google OAuth
2. **register.html** - Registration form
3. **verify_otp.html** - OTP entry page
4. **main_home.html** - Main feed/dashboard
5. **project_detail.html** - Project page with comments/WebSocket updates
6. **profile.html** - User profile display
7. **messages.html** - Messaging interface
8. **find_collaborators.html** - Collaborator search with filters

#### **JavaScript Modules**

**realtime-updates.js**
- WebSocket connection management
- Auto-reconnect with exponential backoff
- Event parsing and routing
- Error handling

**comments-handler.js**
- Fetch and display comments
- Handle comment posting
- Like/unlike comments
- Nested comment support
- Real-time comment updates via WebSocket

**messages-api.js**
- Send/receive messages
- Mark as read
- Fetch message history
- Handle typing indicators

**messages-ui.js**
- Update message display
- Scroll to latest message
- Handle user online status
- Format timestamps

---

## Authentication & Security

### Authentication Methods

#### **1. Email + OTP (Primary)**
- Generate 6-digit OTP
- Send via Brevo/ZeptoMail/Gmail
- 5-minute expiry
- One-time use only
- Rate limiting (prevent brute force)

#### **2. Google OAuth 2.0**
- Use django-allauth
- Redirect to Google consent screen
- Auto-create account if doesn't exist
- Email verification via Google

#### **3. GitHub OAuth (Optional)**
- Similar to Google
- Via django-allauth

### Security Features

1. **CSRF Protection** - Enabled via Django middleware
2. **Session Security** - SessionMiddleware with secure cookies
3. **Password Hashing** - Django's PBKDF2-SHA256
4. **Rate Limiting** - OTP rate limiting (10 attempts/hour)
5. **HTTPS** - Enabled on production (Render)
6. **SQL Injection** - Prevented via ORM
7. **XSS Protection** - Django template escaping

### Settings Security

```python
# settings.py
SECURE_SSL_REDIRECT = True  # Production
SESSION_COOKIE_SECURE = True
CSRF_COOKIE_SECURE = True
CSRF_COOKIE_HTTPONLY = True

# Allowed hosts
ALLOWED_HOSTS = ['yourdomain.com', 'localhost']

# Authentication backends
AUTHENTICATION_BACKENDS = [
    'django.contrib.auth.backends.ModelBackend',
    'allauth.account.auth_backends.AuthenticationBackend',
]
```

---

## Email System

### Email Backends (Priority Order)

#### **1. Brevo (Recommended for Production)**
```python
# config: accounts/brevo_mail_backend.py
# Uses Brevo API for transactional emails
# Advantages: High deliverability, templates, tracking
# Set: BREVO_API_KEY in .env
```

#### **2. ZeptoMail (Alternative)**
```python
# config: accounts/zepto_mail_backend.py
# Uses ZeptoMail API
# Set: ZEPTO_MAIL_API_KEY, ZEPTO_MAIL_TOKEN in .env
```

#### **3. Gmail SMTP (Fallback)**
```python
# config: settings.py
# Uses Gmail's SMTP server
# Set: EMAIL_HOST_USER, EMAIL_HOST_PASSWORD in .env
```

#### **4. Console Backend (Development)**
- Prints emails to console
- Used when no production backend configured

### Email Use Cases

1. **OTP Emails** - Login/registration codes
2. **Welcome Emails** - New user onboarding
3. **Notification Emails** - Activity updates
4. **Password Reset** - Reset link emails
5. **Contact Form** - Support inquiries

---

## Database Schema

### Core Tables

```
User (Django)
├── id (Primary Key)
├── username (Unique)
├── email (Unique)
├── password (Hashed)
└── is_active, is_staff, created_at

StudentProfile
├── id
├── user_id (FK → User) [UNIQUE]
├── full_name, college, location
├── bio, profile_photo
├── interests (JSON)
├── skills (JSON)
├── github, linkedin, portfolio
└── created_at, updated_at

Project
├── id
├── user_id (FK → User, owner)
├── title, description
├── collaboration_needs
├── category, status, visibility
├── project_image, thumbnail
└── created_at, updated_at

ProjectMember
├── id
├── project_id (FK)
├── user_id (FK)
├── role (owner/admin/contributor/viewer)
├── is_active
└── joined_at

ProjectTask
├── id
├── project_id (FK)
├── title, description
├── assigned_to (FK → User)
├── status (todo/in_progress/etc)
├── priority, due_date
└── created_at, updated_at

Comment
├── id
├── project_id (FK)
├── user_id (FK)
├── content
├── parent_comment (FK to self)
├── likes_count, replies_count
└── created_at, updated_at

Like
├── id
├── user_id (FK)
├── project_id (FK)
└── created_at

Message
├── id
├── sender_id (FK)
├── receiver_id (FK)
├── chat_room_id (FK, optional)
├── content
├── message_type
├── reply_to (FK to self)
└── created_at, updated_at

Connection
├── id
├── sender_id (FK)
├── receiver_id (FK)
├── status (pending/accepted/rejected)
└── created_at, updated_at

Notification
├── id
├── user_id (FK)
├── activity_id (FK)
├── message
├── is_read
└── created_at

OTP
├── id
├── email
├── otp_code
├── purpose (login/registration/reset)
├── is_used
├── created_at, expires_at

Activity
├── id
├── user_id (FK)
├── activity_type (CharField)
├── title, description
├── project_id (FK, optional)
├── target_user_id (FK, optional)
└── created_at
```

---

## Key Features Breakdown

### 1. **Authentication & Authorization**

**Features:**
- Email + OTP login
- Google/GitHub OAuth
- Password reset
- Session management
- User roles (student, mentor)

**Files:**
- `accounts/views.py` (auth views)
- `accounts/forms.py` (login/register forms)
- `accounts/models.py` (OTP model)

---

### 2. **Project Management**

**Features:**
- Create/edit/delete projects
- Project visibility (public/private/team-only)
- Team collaboration with roles
- Task tracking
- Milestones
- Project analytics

**Files:**
- `accounts/models.py` (Project, ProjectMember, ProjectTask, ProjectMilestone)
- `accounts/views.py` (post_project, project_detail, edit_project)
- `accounts/serializers.py` (ProjectSerializer)
- `accounts/templates/project_detail.html`

---

### 3. **Real-Time Collaboration**

**Features:**
- Live comments on projects
- WebSocket updates for new comments/members
- Activity feed updates
- Notification streaming
- Typing indicators (future)

**Files:**
- `accounts/consumers.py` (WebSocket consumers)
- `accounts/routing.py` (WebSocket routing)
- `accounts/signals_realtime.py` (Signal handlers)
- `accounts/templates/project_detail.html` (WebSocket client)
- `static/js/realtime-updates.js` (JavaScript handler)

---

### 4. **Collaboration Matching**

**Features:**
- Search for collaborators by skills
- NLP-based skill matching
- Filter by college, interests
- View collaborator profiles

**Files:**
- `accounts/utils.py` (StudentProfileNLP)
- `accounts/views.py` (find_collaborators)
- `accounts/templates/find_collaborators.html`

---

### 5. **Messaging & Notifications**

**Features:**
- Direct messaging
- Group chats
- Message read status
- Message reactions
- Notification feed
- Email notifications

**Files:**
- `accounts/models.py` (Message, ChatRoom, Notification)
- `accounts/chat_api_improved.py` (Messaging API)
- `accounts/templates/messages.html`
- `static/js/messages-api.js`, `messages-ui.js`

---

### 6. **Activity & Feed**

**Features:**
- Project creation notifications
- Connection requests
- Comment notifications
- Like notifications
- Follow notifications
- Activity timeline

**Files:**
- `accounts/models.py` (Activity, Follow, Like)
- `accounts/views.py` (main_home, activity_feed)
- `accounts/templates/main_home.html`
- `static/js/realtime-updates.js`

---

### 7. **User Profiles & Stats**

**Features:**
- Extended profiles with skills/interests
- Profile photo upload
- Social links (GitHub, LinkedIn, etc)
- User statistics dashboard
- Profile completion tracking

**Files:**
- `accounts/models.py` (StudentProfile, UserStats)
- `accounts/views.py` (student_profile, edit_profile)
- `accounts/templates/profile.html`

---

## Configuration Files

### Key Configuration

#### **settings.py**
- Database connection (PostgreSQL/SQLite)
- Installed apps
- Middleware stack
- Email backend selection
- OAuth configuration
- Channel layers (WebSocket)
- Logging configuration

#### **.env (Environment Variables)**
```
DEBUG=True/False
SECRET_KEY=your-secret-key
ALLOWED_HOSTS=localhost,127.0.0.1

# Database
DATABASE_URL=postgresql://user:pass@host/db
DB_NAME=unisync_db
DB_USER=user
DB_PASSWORD=pass
DB_HOST=localhost
DB_PORT=5432

# Email
BREVO_API_KEY=key-here
ZEPTO_MAIL_API_KEY=key-here
ZEPTO_MAIL_TOKEN=token-here
EMAIL_HOST_USER=your@gmail.com
EMAIL_HOST_PASSWORD=password
DEFAULT_FROM_EMAIL=noreply@unisync.app

# OAuth
GOOGLE_CLIENT_ID=xxx
GOOGLE_CLIENT_SECRET=xxx
GITHUB_CLIENT_ID=xxx
GITHUB_CLIENT_SECRET=xxx

# APIs
RAPIDAPI_KEY=key-here

# Security
SECURE_SSL_REDIRECT=True
SESSION_COOKIE_SECURE=True
CSRF_COOKIE_SECURE=True
```

#### **Procfile (Deployment)**
```
web: gunicorn auth_project.wsgi
worker: daphne -b 0.0.0.0 -p $PORT auth_project.asgi:application
```

---

## Deployment

### Render.com Setup

1. **Install Requirements**
   ```bash
   pip install -r requirements.txt
   ```

2. **Environment Variables** (Set in Render dashboard)
   - All `.env` variables

3. **Build Command**
   ```bash
   python manage.py migrate && python manage.py collectstatic
   ```

4. **Start Commands**
   - Web service: `gunicorn auth_project.wsgi`
   - WebSocket service: `daphne -b 0.0.0.0 -p $PORT auth_project.asgi:application`

5. **Database** (Use Render PostgreSQL)
   - Render provides DATABASE_URL automatically

---

## Performance Optimizations

### Database
- Query optimization with `select_related()` and `prefetch_related()`
- Pagination for large result sets
- Indexing on frequently queried fields
- Caching user stats

### Frontend
- Static file compression
- CDN integration
- Lazy loading for images
- Debounced search
- AJAX for smooth UX

### Backend
- Async task handling (future: Celery)
- Response caching
- Database query optimization
- Connection pooling

---

## Common Issues & Solutions

### 1. WebSocket Connection Fails
**Cause:** Daphne not running  
**Solution:** Ensure Daphne service is deployed separately

### 2. Comments Not Showing
**Cause:** WebSocket not initialized  
**Solution:** Check browser console for errors, verify WebSocket URL

### 3. OAuth Redirect URI Mismatch
**Cause:** Domain mismatch in Google/GitHub settings  
**Solution:** Add exact redirect URI to OAuth provider settings

### 4. Static Files 404
**Cause:** Not collected  
**Solution:** Run `python manage.py collectstatic --noinput`

### 5. Email Not Sending
**Cause:** Backend not configured or API key invalid  
**Solution:** Check `.env` variables and verify email backend setting

---

## Future Enhancements

1. **Async Task Queue** - Celery for background tasks
2. **Push Notifications** - Mobile app notifications
3. **Video Calls** - WebRTC integration
4. **Typing Indicators** - Real-time typing status
5. **Message Search** - Full-text search in messages
6. **Project Templates** - Pre-made project structures
7. **Advanced Analytics** - Detailed project metrics
8. **AI-Powered Matching** - ML-based collaborator suggestions
9. **Mobile App** - React Native/Flutter client
10. **API Rate Limiting** - Prevent abuse

---

## Conclusion

UniSync is a comprehensive Django-based collaboration platform with:
- **Robust authentication** (Email OTP + OAuth)
- **Real-time features** (WebSocket-driven updates)
- **Project management** (Team collaboration, tasks, milestones)
- **Social networking** (Messaging, followers, activity feeds)
- **Scalable architecture** (DRF APIs, PostgreSQL, Channel layers)

The codebase is production-ready and deployed on Render.com with PostgreSQL backend.
