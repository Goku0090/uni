# UniSync Platform - Comprehensive Code Analysis

## Executive Summary

UniSync is a Django-based full-stack web application for connecting students, facilitating project collaboration, and enabling real-time communication. It combines authentication, social networking, project management, and messaging features with RESTful APIs.

**Tech Stack:**
- **Backend:** Django 4.2.8, Django REST Framework 3.14.0
- **Database:** PostgreSQL with Redis caching
- **Frontend:** Django Templates + Static Assets
- **Authentication:** Django-Allauth (Google, GitHub OAuth)
- **Email:** Brevo/ZeptoMail integration
- **Real-time:** Channels, Celery for background jobs
- **Deployment:** Render.com with PostgreSQL

---

## 1. Project Structure Overview

```
auth_project/
├── auth_project/           # Django project settings & config
│   ├── settings.py         # Global configuration
│   ├── urls.py             # Root URL routing
│   ├── wsgi.py             # WSGI application
│   └── asgi.py             # ASGI application
├── accounts/               # Main application logic
│   ├── models.py           # Database models (14+ models)
│   ├── views.py            # View controllers (3300+ lines)
│   ├── serializers.py      # REST API serializers
│   ├── urls.py             # App-level URL routing
│   ├── forms.py            # Form definitions
│   ├── utils.py            # NLP & filtering utilities
│   ├── chat_api.py         # Chat API endpoints
│   ├── views_contact.py    # Contact/legal pages
│   ├── services/           # Business logic services
│   ├── static/             # CSS, JS, images
│   ├── templates/          # HTML templates
│   ├── migrations/         # Database migrations
│   └── templatetags/       # Custom template tags
├── static/                 # Global static files
├── media/                  # User uploads
├── logs/                   # Application logs
├── manage.py               # Django CLI
└── requirements.txt        # Dependencies
```

---

## 2. Core Data Models

### 2.1 User & Profile Management

#### **StudentProfile** (Extended User Profile)
- **Purpose:** Extends Django's User model with student-specific data
- **Key Fields:**
  - `full_name`, `college`, `location`
  - `interests` (JSONField - array)
  - `skills` (JSONField - array)
  - `project_interests` (JSONField - array)
  - `bio`, `role_preference`
  - `profile_photo` (ImageField with validation)
  - Social links: `github`, `linkedin`, `portfolio`, `behance`
  - `profile_completed` (boolean flag)
  - Timestamps: `created_at`, `updated_at`

**File:** `accounts/models.py:12-53`

#### **OTP** (One-Time Password)
- **Purpose:** Email-based authentication (login, registration, password reset)
- **Key Fields:**
  - `email`, `otp_code` (6-digit)
  - `purpose` (login | registration | reset)
  - `is_used`, `created_at`, `expires_at`
  - `is_valid()` - checks expiration & usage
  - `verify_otp()` - validates code
  - `generate_otp()` - creates new OTP
- **Expiration:** 10 minutes default

**File:** `accounts/models.py:55-125`

#### **UserStatus**
- **Purpose:** Track online/offline status for real-time features
- **Key Fields:**
  - `is_online` (boolean)
  - `last_seen` (datetime)
  - `current_room` (WebSocket room identifier)

---

### 2.2 Social Features

#### **Connection** (User Relationships)
- **Purpose:** Friend/network connections between users
- **Key Fields:**
  - `sender_id`, `receiver_id` (ForeignKey to User)
  - `status` (pending | accepted | rejected)
  - Timestamps

#### **Follow** (User Followers)
- **Purpose:** One-way follow relationships
- **Key Fields:**
  - `follower`, `following` (ForeignKey to User)
  - `created_at`

#### **Activity** (Activity Feed)
- **Purpose:** User activity logs for news feeds
- **Key Fields:**
  - `activity_type` (profile_updated | project_created | project_liked | connection_made | etc.)
  - `title`, `description`
  - Related: `project`, `target_user`, `connection`
  - `is_public` (privacy control)

#### **Notification**
- **Purpose:** User notifications
- **Key Fields:**
  - `notification_type` (connection_request | connection_accepted | message | project_like | project_comment | team_invitation | follow)
  - `title`, `message`
  - `from_user`, `connection`, `message_obj` (related objects)
  - `is_read`, `read_at`

---

### 2.3 Project Management

#### **Project** (Project Listings)
- **Purpose:** Main project listings where users post projects looking for collaborators
- **Key Fields:**
  - `user_id` (owner)
  - `title`, `description`
  - `technologies` (JSONField - array of tech stacks)
  - `looking_for` (JSONField - required roles/skills)
  - `category` (web | mobile | ai | data | blockchain | iot | game | other)
  - `timeline`, `collaboration_needs`
  - `github_link`
  - `is_active` (soft delete)
  - Timestamps

**File:** `accounts/models.py:403-449`

#### **Like** (Project Likes)
- **Purpose:** Like/vote on projects
- **Unique:** user + project

#### **Comment** (Project Comments)
- **Purpose:** Discussion on projects
- **Key Fields:**
  - `user_id`, `project_id`
  - `content`, timestamps

---

### 2.4 Project Collaboration

#### **ProjectMember**
- **Purpose:** Team members on a project with role-based permissions
- **Roles:** owner, admin, contributor, viewer
- **Permissions:**
  - `can_manage_project`
  - `can_invite_members`
  - `can_manage_tasks`
  - `can_edit_project`

#### **ProjectInvitation**
- **Purpose:** Invite users to join projects
- **Status:** pending | accepted | declined | expired
- **Methods:**
  - `accept()` - Creates ProjectMember
  - `decline()` - Rejects invitation

#### **ProjectTask** (Task Management)
- **Status:** todo | in_progress | review | completed | cancelled
- **Priority:** low | medium | high
- **Fields:** title, description, assigned_to, due_date

#### **ProjectMilestone**
- **Purpose:** Major project milestones
- **Fields:** title, description, target_date, status

#### **ProjectTeam & ProjectTeamMember**
- **Purpose:** Team grouping within projects
- **Supports:** Project team structure & collaboration

---

### 2.5 Messaging & Chat

#### **Message** (Direct Messages)
- **Purpose:** One-to-one and group messages
- **Key Fields:**
  - `sender_id`, `recipient_id`
  - `chat_room_id` (for group chats)
  - `content`
  - `message_type` (text | file | system)
  - `is_read`, `read_at`
  - Timestamps

**File:** `accounts/models.py:149-217`

#### **MessageFile** (File Attachments)
- **Purpose:** Attach files to messages
- **Fields:** `message_id`, `file_id`, upload info

#### **MessageReaction** (Message Reactions)
- **Purpose:** Emoji reactions on messages
- **Fields:** `message_id`, `user_id`, `reaction` (emoji string)

#### **MessageReadStatus** (Read Receipts)
- **Purpose:** Track message read status per user
- **Fields:** `message_id`, `user_id`, `read_at`

#### **ChatRoom** (Group Chats)
- **Purpose:** Group messaging rooms
- **Key Fields:**
  - `name`
  - `description`
  - `chat_type` (direct | group | channel)
  - `is_active`
  - Participants via ChatRoomMember

**File:** `accounts/models.py:279-307`

#### **ChatRoomMember** (Room Membership)
- **Purpose:** Members of chat rooms with roles
- **Roles:** owner, admin, member
- **Permissions:**
  - `can_invite_members`
  - `can_manage_room`

**File:** `accounts/models.py:309-335`

#### **File** (File Storage)
- **Purpose:** File metadata storage
- **Fields:** `file_path`, `file_type`, `uploaded_by`, `created_at`

---

### 2.6 Additional Models

#### **UserStats** (Dashboard Statistics)
- **Purpose:** Cache user activity metrics
- **Tracks:** projects_created, connections_made, likes_received, followers_count, etc.
- **Method:** `update_stats()` - Refreshes all statistics

**File:** `accounts/models.py:510-540`

---

## 3. Authentication System

### 3.1 Authentication Flow

```
Login/Register Process:
1. User enters email → Generate OTP
2. OTP sent via Brevo/ZeptoMail
3. User verifies OTP code
4. Create User + StudentProfile
5. Create UserStats record
6. Redirect to dashboard
```

### 3.2 Social Authentication (OAuth2)

**Supported Providers:**
- Google (via allauth)
- GitHub (via allauth)

**Configuration:** `settings.py:50-58`

### 3.3 OTP System

**Flow:**
1. **Generation:** 6-digit code, 10-minute expiry
2. **Storage:** OTP model with email, purpose, expiry
3. **Verification:** Code match + expiry check
4. **Mark Used:** Prevent replay attacks

**File:** `accounts/models.py:55-125`

---

## 4. REST API Layer

### 4.1 Chat API Endpoints

**Base:** `/accounts/`

| Endpoint | Method | Purpose |
|----------|--------|---------|
| `chat-rooms/` | GET/POST | List/create chat rooms |
| `chat-rooms/<id>/` | GET/PUT/DELETE | Room details & management |
| `chat-rooms/<id>/members/` | GET/POST | Room members management |
| `direct-message/` | POST | Create direct message conversation |
| `messages/` | GET/POST | List/create messages |
| `messages/<id>/` | GET/PUT/DELETE | Message details |
| `messages/search/` | GET | Search messages |
| `messages/<id>/reactions/` | GET/POST | Message reactions |
| `conversations/` | GET | List user conversations |

**File:** `accounts/urls.py:78-101`

### 4.2 Profile API

| Endpoint | Method | Purpose |
|----------|--------|---------|
| `user-profile/<user_id>/` | GET | User profile data |
| `profile/` | GET/PUT | Current user profile |

### 4.3 College & Validation APIs

| Endpoint | Method | Purpose |
|----------|--------|---------|
| `college-search/` | GET | Search colleges by name |
| `validate-college/` | POST | Validate college input |

**File:** `accounts/urls.py:104-107`

### 4.4 Utility APIs

| Endpoint | Method | Purpose |
|----------|--------|---------|
| `check-username/` | GET | Username availability |
| `check-email/` | GET | Email availability |
| `user-stats/` | GET | User statistics |
| `nlp-analyze/` | POST | NLP analysis for skills matching |

**File:** `accounts/urls.py:113-119`

---

## 5. Serializers

**File:** `accounts/serializers.py:1-106`

### 5.1 UserProfileSerializer
- **Source Model:** StudentProfile
- **Fields:** username, email, full_name, college, location, interests, bio, skills, profile_photo, social links, profile_completed
- **Read-only:** id, profile_completed

### 5.2 ProjectSerializer
- **Source Model:** Project
- **Related:** UserProfileSerializer (nested owner)
- **Computed Fields:** likes_count, comments_count
- **Read-only:** id, created_at, updated_at

### 5.3 MessageSerializer
- **Source Model:** Message
- **Related:** UserProfileSerializer (nested sender)
- **Computed Fields:** reactions (emoji reaction counts)

### 5.4 ConnectionSerializer
- **Nested:** Sender & Receiver profiles
- **Fields:** status, timestamps

### 5.5 NotificationSerializer
- **Nested:** from_user profile
- **Fields:** type, title, message, read status

---

## 6. Views & Controllers

**File:** `accounts/views.py:1-3311`

### 6.1 Authentication Views

| View | Method | Purpose |
|------|--------|---------|
| `login_view()` | GET/POST | Email/password login |
| `register_view()` | GET/POST | User registration |
| `logout_view()` | GET | Session logout |
| `verify_otp_view()` | GET/POST | OTP verification |
| `forgot_password_view()` | GET/POST | Password reset initiation |
| `reset_password_view()` | GET/POST | Password change |

### 6.2 Profile Management

| View | Purpose |
|------|---------|
| `student_profile()` | View own profile |
| `user_profile()` | View other user's profile |
| `edit_profile()` | Edit profile & avatar upload |
| `student_details_view()` | Extended profile details form |

### 6.3 Project Features

| View | Purpose |
|------|---------|
| `post_project()` | Create new project listing |
| `edit_project()` | Edit existing project |
| `delete_project()` | Delete project |
| `project_detail()` | View project details |
| `like_project()` | Like/unlike project |
| `search_projects()` | Project search & filtering |
| `find_collaborators()` | Find users for collaboration |

### 6.4 Social Features

| View | Purpose |
|------|---------|
| `connect_view()` | Send connection request |
| `accept_connection()` | Accept connection |
| `reject_connection()` | Reject connection |
| `my_connections()` | List user's connections |
| `follow_user()` | Follow another user |
| `activity_feed()` | View activity feed |

### 6.5 Messaging

| View | Purpose |
|------|---------|
| `message_view()` | List conversations |
| `chat_view()` | Direct message view |
| `enhanced_messages_view()` | Advanced messaging UI |
| `enhanced_chat_view()` | Group chat |
| `create_group_chat()` | Create chat room |
| `add_reaction()` | Add emoji reaction |

### 6.6 Dashboard & Analytics

| View | Purpose |
|------|---------|
| `dashboard_view()` | Main dashboard with stats |
| `notifications_view()` | User notifications |
| `help_center_view()` | Help documentation |

### 6.7 API Views (DRF)

| View | Purpose |
|------|---------|
| `UserProfileView` (APIView) | Profile serialization |
| Chat API Classes | Message, room, member endpoints |
| `college_search_api()` | College lookup |
| `user_stats_api()` | User statistics JSON |
| `nlp_analyze_api()` | Skill analysis |

---

## 7. Business Logic & Services

### 7.1 StudentProfileNLP (NLP Service)

**File:** `accounts/utils.py`

**Purpose:** Analyze and match skills using Natural Language Processing

**Key Methods:**
- `extract_skills()` - Extract skills from bio/description
- `match_projects()` - Find matching projects based on skills
- `calculate_relevance_score()` - Score user-project match

**Uses:** NLTK, pandas for NLP

### 7.2 ProjectVisibilityFilter (Search & Filtering)

**Purpose:** Filter projects based on visibility, category, technology, and skills

**Key Methods:**
- `filter_by_visibility()` - Public/private/archived
- `filter_by_category()` - Category filtering
- `filter_by_technology()` - Tech stack matching
- `filter_by_skills()` - Required skills matching
- `apply_all_filters()` - Combined filtering

### 7.3 Email Services

**File:** `accounts/brevo_mail_backend.py` & `zepto_mail_backend.py`

**Providers:**
- **Brevo:** Primary email service
- **ZeptoMail:** Backup/alternative provider

**Email Types:**
- OTP verification
- Password reset
- Connection notifications
- Project invitations
- Activity notifications

---

## 8. URL Routing

**File:** `accounts/urls.py:1-120`

### 8.1 Template Views (Browser Routes)

**Authentication:**
- `login/` → login_view
- `register/` → register_view
- `logout/` → logout_view
- `forgot-password/` → forgot_password_view
- `verify-otp/<purpose>/` → verify_otp_view

**Profiles:**
- `student-details/` → student_details_view
- `student-profile/` → student_profile
- `user/<username>/` → user_profile

**Projects:**
- `post-project/` → post_project
- `edit-project/<id>/` → edit_project
- `project-detail/<id>/` → project_detail

**Social:**
- `connect/<user_id>/` → connect_view
- `accept-connection/<id>/` → accept_connection
- `my-connections/` → my_connections
- `follow/<user_id>/` → follow_user
- `activity-feed/` → activity_feed

**Messaging:**
- `messages/` → message_view
- `chat/<user_id>/` → chat_view
- `enhanced-messages/` → enhanced_messages_view

### 8.2 REST API Routes

**Chat:**
- `chat-rooms/` - List/create
- `chat-rooms/<id>/` - Details
- `messages/` - List/create
- `conversations/` - List user conversations

**Profile:**
- `profile/` - Current user
- `user-profile/<id>/` - Any user

**Utilities:**
- `college-search/`
- `check-username/`
- `check-email/`
- `user-stats/`
- `nlp-analyze/`

---

## 9. Configuration & Settings

### 9.1 Django Settings

**File:** `auth_project/settings.py:1-356`

#### **Installed Apps:**
```python
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.sites',
    'django.contrib.humanize',
    'accounts',
    'allauth',
    'allauth.account',
    'allauth.socialaccount',
    'allauth.socialaccount.providers.google',
    'allauth.socialaccount.providers.github',
    'rest_framework',
]
```

#### **Middleware:**
```python
MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'allauth.account.middleware.AccountMiddleware',
]
```

#### **Database:**
- PostgreSQL (via dj-database-url)
- Render.com hosted
- Environment: `DATABASE_URL`

#### **Cache:**
- Redis (django-redis)
- Session storage
- Template caching

#### **Security:**
- CSRF Protection enabled
- Secure SSL redirect (production)
- Secure session cookies
- Secure CSRF cookies

#### **Email Configuration:**
- Backend: Custom Brevo/ZeptoMail
- Environment: `EMAIL_BACKEND`, `BREVO_API_KEY`, `ZEPTO_API_KEY`
- From: `DEFAULT_FROM_EMAIL`

---

## 10. Dependencies & Stack

**File:** `requirements.txt`

### 10.1 Core Framework
- Django 4.2.8
- djangorestframework 3.14.0
- django-allauth 0.61.1

### 10.2 Database & Caching
- psycopg2-binary 2.9.9 (PostgreSQL)
- dj-database-url 2.1.0
- redis 5.0.1
- django-redis 5.4.0

### 10.3 Authentication & OAuth
- requests 2.31.0
- requests-oauthlib 1.3.1
- django-cors-headers 4.3.1

### 10.4 Email & Communications
- zeptomail 1.0.0 (Email service)
- Brevo API (custom backend)

### 10.5 NLP & Data Processing
- nltk 3.8.1 (Natural Language Toolkit)
- pandas 2.1.4 (Data analysis)
- openpyxl 3.1.2 (Excel support)

### 10.6 Real-time Features
- channels 4.0.0 (WebSocket)
- channels-redis 4.1.0
- celery 5.3.4 (Task queue)

### 10.7 File Storage & Media
- Pillow 10.1.0 (Image processing)
- boto3 1.34.34 (AWS S3)
- django-storages 1.14.2

### 10.8 Performance & Monitoring
- gunicorn 21.2.0 (Production server)
- whitenoise 6.6.0 (Static files)
- sentry-sdk 1.38.0 (Error tracking)
- django-performance-monitor 0.1.1

### 10.9 Development & Testing
- django-debug-toolbar 4.2.0
- pytest 7.4.3
- pytest-django 4.7.0
- selenium 4.16.0 (Browser testing)
- black 23.12.1 (Code formatting)
- flake8 6.1.0 (Linting)

---

## 11. Key Features Summary

### 11.1 User Management
✅ Email/OTP-based registration & login
✅ Social login (Google, GitHub)
✅ Profile creation & editing
✅ Avatar upload with validation
✅ Profile completion tracking

### 11.2 Project Discovery
✅ Post & edit project listings
✅ Project categorization (8 categories)
✅ Technology stack tracking (JSONField)
✅ Collaboration needs specification
✅ Project search & filtering
✅ Project visibility control

### 11.3 Collaboration
✅ Connection/friend requests
✅ User following system
✅ Team member management with roles
✅ Project invitations with expiry
✅ Project task assignment
✅ Project milestone tracking

### 11.4 Messaging
✅ Direct messaging (1-to-1)
✅ Group chat rooms
✅ File attachments
✅ Message reactions (emoji)
✅ Read receipts
✅ Message search
✅ Typing indicators
✅ Draft messages

### 11.5 Social Features
✅ Activity feed
✅ User notifications (8 types)
✅ Like/comment on projects
✅ Follow/unfollow users
✅ User statistics dashboard

### 11.6 Smart Matching
✅ NLP-based skill extraction
✅ Project-user compatibility scoring
✅ Skill-based recommendations
✅ Collaborator discovery

### 11.7 Administrative
✅ Django admin interface
✅ User management
✅ Project moderation
✅ Activity logging
✅ Statistics tracking

---

## 12. Data Flow Diagrams

### 12.1 User Registration Flow
```
User Input Email
    ↓
Generate 6-digit OTP
    ↓
Send OTP via Brevo/ZeptoMail
    ↓
User Submits OTP Code
    ↓
Verify OTP (check code + expiry)
    ↓
Create User (Django Auth)
    ↓
Create StudentProfile
    ↓
Create UserStats
    ↓
Create UserStatus (tracking)
    ↓
Set Login Session
    ↓
Redirect to Dashboard
```

### 12.2 Project Creation & Discovery
```
User Posts Project
    ↓
Store: title, description, tech, categories, looking_for
    ↓
Create Activity Log Entry
    ↓
Send Notifications to Matched Users
    ↓
↓
Other Users Search/Browse Projects
    ↓
Filter by: category, technology, skills required
    ↓
Apply NLP Matching
    ↓
Sort by Relevance Score
    ↓
Display Results with User Profiles
    ↓
User Sends Connection/Join Request
```

### 12.3 Messaging Flow
```
User A → Start Chat/Message
    ↓
Create/Open ChatRoom or Direct Conversation
    ↓
Send Message (text/file/reaction)
    ↓
Save Message + MessageReadStatus
    ↓
Send Notification to User B
    ↓
User B Receives + Marks as Read
    ↓
Real-time Update via WebSocket (Channels)
```

### 12.4 Connection/Network Building
```
User A Sends Connection Request
    ↓
Create Connection (status=pending)
    ↓
Send Notification to User B
    ↓
User B Accepts/Rejects
    ↓
Update Connection Status
    ↓
Create Activity Entry
    ↓
Create Bilateral Follow Relationships
```

---

## 13. API Request/Response Examples

### 13.1 Create Message
**Endpoint:** `POST /accounts/messages/`

**Request:**
```json
{
  "content": "Hello, interested in your web project!",
  "recipient_id": 5,
  "message_type": "text"
}
```

**Response:**
```json
{
  "id": 123,
  "content": "Hello, interested in your web project!",
  "sender": {
    "id": 1,
    "username": "john_doe",
    "full_name": "John Doe",
    "profile_photo": "/media/profile_photos/john.jpg"
  },
  "created_at": "2024-01-15T10:30:00Z",
  "is_read": false,
  "message_type": "text",
  "reactions": {}
}
```

### 13.2 Search Messages
**Endpoint:** `GET /accounts/messages/search/?q=project`

**Response:**
```json
[
  {
    "id": 123,
    "content": "Let's discuss the project requirements",
    "sender": {...},
    "created_at": "2024-01-15T10:30:00Z"
  },
  {...}
]
```

### 13.3 Get User Profile
**Endpoint:** `GET /accounts/user-profile/5/`

**Response:**
```json
{
  "id": 5,
  "username": "alice_smith",
  "email": "alice@example.com",
  "full_name": "Alice Smith",
  "college": "MIT",
  "location": "Boston",
  "interests": ["AI", "Web Dev"],
  "bio": "Passionate about machine learning...",
  "skills": ["Python", "TensorFlow", "React"],
  "project_interests": ["AI/ML", "Web Development"],
  "role_preference": "Full Stack",
  "github": "https://github.com/alice",
  "profile_photo": "/media/profile_photos/alice.jpg",
  "profile_completed": true
}
```

### 13.4 Get Projects with Filters
**Endpoint:** `GET /accounts/projects/?category=ai&technology=python`

**Response:**
```json
[
  {
    "id": 42,
    "title": "ML Model for Image Recognition",
    "description": "Building an image recognition model...",
    "technologies": ["Python", "TensorFlow", "OpenCV"],
    "looking_for": ["Backend Developer", "DevOps"],
    "category": "ai",
    "timeline": "3 months",
    "owner": {...},
    "likes_count": 15,
    "comments_count": 3,
    "created_at": "2024-01-10T14:20:00Z"
  },
  {...}
]
```

### 13.5 Create Chat Room
**Endpoint:** `POST /accounts/chat-rooms/`

**Request:**
```json
{
  "name": "Web Dev Team",
  "description": "Team for web development project",
  "chat_type": "group"
}
```

**Response:**
```json
{
  "id": 1,
  "name": "Web Dev Team",
  "description": "Team for web development project",
  "chat_type": "group",
  "created_at": "2024-01-15T10:30:00Z",
  "is_active": true
}
```

---

## 14. Performance Considerations

### 14.1 Caching Strategy
- **Redis Cache** for:
  - User profiles
  - Project listings
  - Notification counts
  - Search results
  - Session data

### 14.2 Database Optimization
- **Indexes on:**
  - `user_id` (foreign keys)
  - `created_at` (sorting/pagination)
  - `status` (filtering)
  - `category` (project filtering)

### 14.3 Pagination
- Applied to project feeds, activity feeds, message lists
- Default: 10-20 items per page
- Configurable via `Paginator`

### 14.4 Background Jobs
- **Celery Tasks:**
  - Sending emails
  - Generating statistics
  - Cleaning up expired OTPs
  - Activity notifications

---

## 15. Security Features

### 15.1 Authentication
✅ Password hashing (Django default)
✅ OTP-based email verification
✅ CSRF protection
✅ Session management
✅ OAuth2 integration

### 15.2 Authorization
✅ Login required decorators
✅ Permission checks on views
✅ Role-based access (ProjectMember roles)
✅ Chat room membership validation

### 15.3 Data Protection
✅ File upload validation (extensions)
✅ Image format validation
✅ XSS protection (template auto-escape)
✅ SQL injection prevention (ORM usage)

### 15.4 API Security
✅ CORS headers
✅ Rate limiting (configurable)
✅ Input validation (forms, serializers)
✅ API endpoint authentication

---

## 16. Deployment

### 16.1 Render.com Configuration
**Files:** `render.yaml`, `Procfile`

**Services:**
- Web: Gunicorn + Whitenoise
- Database: PostgreSQL
- Cache: Redis

**Environment Variables:**
- `DEBUG` (False in production)
- `SECRET_KEY`
- `DATABASE_URL` (Render PostgreSQL)
- `ALLOWED_HOSTS`
- `BREVO_API_KEY`
- `ZEPTO_API_KEY`
- `GOOGLE_OAUTH_KEY`
- `GITHUB_OAUTH_KEY`

### 16.2 Static Files
- Collected via `collectstatic`
- Served via Whitenoise
- CloudFlare CDN optional

### 16.3 Media Files
- S3 storage via boto3
- Fallback to local media/ directory

---

## 17. Testing

### 17.1 Test Files Present
- `test_login_fix.py` - Authentication testing
- `test_otp.py`, `test_otp_simple.py` - OTP verification
- `test_profile_fix.py` - Profile functionality
- `test_feed_fix.py` - Activity feed
- `test_email.py`, `test_zepto_simple.py` - Email services
- `test_connections.py` - Social connections
- `test_search.py` - Search functionality

### 17.2 Test Tools
- pytest + pytest-django
- Selenium for browser testing
- Django TestCase support

---

## 18. Key Code Locations Reference

| Feature | File | Lines |
|---------|------|-------|
| **Models** | `accounts/models.py` | 1-718 |
| **Views** | `accounts/views.py` | 1-3311 |
| **Serializers** | `accounts/serializers.py` | 1-106 |
| **URLs** | `accounts/urls.py` | 1-120 |
| **Settings** | `auth_project/settings.py` | 1-356 |
| **Chat API** | `accounts/chat_api.py` | Full file |
| **Forms** | `accounts/forms.py` | Full file |
| **Utils** | `accounts/utils.py` | Full file |
| **Email Backends** | `accounts/brevo_mail_backend.py`, `zepto_mail_backend.py` | Full files |

---

## 19. Common Workflows

### 19.1 New User Onboarding
1. Register with email
2. Verify OTP
3. Complete profile
4. Add interests & skills
5. Upload profile photo
6. Browse projects
7. Connect with peers

### 19.2 Project Collaboration
1. Create project posting
2. Wait for interested users
3. Receive connection requests
4. Invite users to team
5. Create tasks & milestones
6. Collaborate via chat
7. Track progress

### 19.3 Finding Collaborators
1. Set interests & skills
2. Search projects
3. Filter by technology
4. NLP matching
5. View user profiles
6. Send connection requests
7. Start conversations

---

## 20. Future Enhancement Opportunities

- [ ] WebSocket chat improvements (real-time typing, presence)
- [ ] Advanced NLP matching algorithm
- [ ] Video calling integration
- [ ] Project analytics dashboard
- [ ] Mobile app (React Native)
- [ ] Payment system (Stripe)
- [ ] Gamification (badges, levels)
- [ ] AI-powered recommendations
- [ ] Email digest notifications
- [ ] Dark mode UI

---

**Generated:** February 3, 2026  
**Framework Version:** Django 4.2.8 + DRF 3.14.0  
**Repository:** https://github.com/Goku0090/uni
