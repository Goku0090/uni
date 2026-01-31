# UniSync - Complete Project Documentation

## 📋 Table of Contents
1. [Project Overview](#project-overview)
2. [Tech Stack](#tech-stack)
3. [Architecture](#architecture)
4. [Database Models](#database-models)
5. [Features](#features)
6. [API Endpoints](#api-endpoints)
7. [Authentication System](#authentication-system)
8. [File Structure](#file-structure)
9. [Setup & Installation](#setup--installation)
10. [Deployment](#deployment)

---

## 🎯 Project Overview

**UniSync** is a comprehensive Django-based collaborative platform designed for university students to discover, post, and collaborate on academic and professional projects. The platform facilitates networking, team formation, and project management with real-time messaging and social features.

### Core Purpose
- Enable students to post projects and find collaborators
- Facilitate networking between students with similar interests
- Provide project management tools for team collaboration
- Offer real-time messaging and communication
- Support investor/startup ecosystem features

### Target Users
- University students (primary)
- Project managers and team leads
- Investors and mentors (via investor dashboard)
- Educators (premium tier)

---

## 🛠 Tech Stack

### Backend
| Component | Technology | Version |
|-----------|-----------|---------|
| Framework | Django | 4.2.8 |
| API | Django REST Framework | 3.14.0 |
| Authentication | Django Allauth | 0.61.1 |
| Database | PostgreSQL / SQLite | Latest |
| Server | Gunicorn | 21.2.0 |
| WebSockets | Django Channels | 4.0.0 |

### Frontend
- Django Templates (server-rendered)
- Bootstrap 5 (via crispy-bootstrap5)
- HTML5/CSS3
- JavaScript (vanilla + Bootstrap JS)

### External Services
| Service | Purpose |
|---------|---------|
| **Brevo** | Email delivery (OTP, transactional) |
| **ZeptoMail** | Alternative email service |
| **Gmail SMTP** | Fallback email service |
| **RapidAPI** | University database lookup |
| **Google OAuth** | Social authentication |
| **GitHub OAuth** | Social authentication |

### Supporting Libraries
```
Data Processing: pandas, openpyxl, nltk
Image Processing: Pillow
Caching: redis, django-redis
Task Queue: celery
Cloud Storage: boto3, django-storages
Real-time: channels, channels-redis
Testing: pytest, pytest-django, selenium
Code Quality: black, flake8, mypy
```

---

## 🏗 Architecture

### High-Level Architecture

```
┌─────────────────────────────────────────┐
│         Client Layer (Browser)          │
│    Django Templates + Bootstrap UI      │
└────────────────┬────────────────────────┘
                 │
┌────────────────▼────────────────────────┐
│       URL Routing (urls.py)             │
│  - Main routes (auth_project/urls.py)   │
│  - App routes (accounts/urls.py)        │
└────────────────┬────────────────────────┘
                 │
┌────────────────▼────────────────────────┐
│       Views Layer (views.py)            │
│  - View Functions (50+ endpoints)       │
│  - API Generic Views (DRF)              │
│  - Request handling & business logic    │
└────────────────┬────────────────────────┘
                 │
┌────────────────▼────────────────────────┐
│      Models Layer (models.py)           │
│  - Database ORM definitions             │
│  - 25+ models with relationships        │
│  - Business logic & validators          │
└────────────────┬────────────────────────┘
                 │
┌────────────────▼────────────────────────┐
│         Database Layer                  │
│    PostgreSQL (Prod) / SQLite (Dev)     │
└─────────────────────────────────────────┘
```

### Request Flow

```
1. User Request → Django WSGI/Channels
2. Middleware Processing (Auth, CSRF, Sessions)
3. URL Routing (urls.py matches pattern)
4. View Execution (Function-based or Class-based)
5. Model/Database Queries
6. Template Rendering (if needed)
7. Response to Client
```

### Authentication Flow

```
User Input (Email) 
    ↓
Email Validation
    ↓
OTP Generation (6-digit, 5-min validity)
    ↓
OTP Sent via Email
    ↓
User Enters OTP
    ↓
OTP Verification
    ↓
Session Creation
    ↓
Redirect to Dashboard
```

---

## 🗄 Database Models

### 1. Authentication Models

#### **User** (Django Built-in)
```python
- id: AutoField
- username: CharField (unique)
- email: EmailField (unique)
- password: CharField (hashed)
- is_active: BooleanField
- is_staff: BooleanField
- date_joined: DateTimeField
- last_login: DateTimeField
```

#### **OTP** (One-Time Password)
```python
- email: EmailField
- otp_code: CharField (6 digits)
- purpose: CharField (login, registration, reset)
- is_used: BooleanField (default=False)
- created_at: DateTimeField
- expires_at: DateTimeField (5 minutes)

Methods:
- is_valid(): Check if OTP is not used and not expired
- generate_otp(email, purpose): Class method to create new OTP
```

### 2. User Profile Models

#### **StudentProfile** (Extended User Profile)
```python
- user: OneToOneField(User)
- full_name: CharField (max 100)
- college: CharField (max 200)
- other_college: CharField (for custom college)
- location: CharField (max 100)
- interests: TextField (comma-separated)
- bio: TextField
- profile_photo: ImageField (jpg, jpeg, png, gif)
- skills: JSONField (array of selected skills)
- project_interests: JSONField (array of interests)
- role_preference: CharField (developer, designer, etc.)
- github: URLField
- linkedin: URLField
- portfolio: URLField
- behance: URLField
- profile_completed: BooleanField
- created_at: DateTimeField
- updated_at: DateTimeField

Methods:
- get_display_name(): Return full_name or username
```

### 3. Project Models

#### **Project** (Main project model)
```python
- owner: ForeignKey(User)
- title: CharField (max 200)
- description: TextField
- category: CharField (web, mobile, ai, data, etc.)
- technologies: JSONField (array of tech stack)
- looking_for: JSONField (roles needed)
- collaboration_needs: TextField
- timeline: CharField (estimated duration)
- github_link: URLField (optional)
- status: CharField (active, completed, paused)
- visibility: CharField (public, private)
- created_at: DateTimeField
- updated_at: DateTimeField

Relationships:
- owners: ManyToMany(User) for co-owners
- likes: Reverse from Like model
- comments: Reverse from Comment model
- tasks: Reverse from ProjectTask
- milestones: Reverse from ProjectMilestone
```

#### **ProjectTeam** (Team management)
```python
- project: OneToOneField(Project)
- name: CharField (max 100)
- description: TextField
- created_at: DateTimeField

Properties:
- active_members: Filter members where is_active=True
```

#### **ProjectTeamMember** (Team member with roles)
```python
- team: ForeignKey(ProjectTeam)
- user: ForeignKey(User)
- role: CharField (owner, admin, contributor, viewer)
- is_active: BooleanField
- joined_at: DateTimeField

Unique Constraint: (team, user)

Properties:
- can_manage_team: True if owner/admin
- can_invite_members: True if owner/admin
- can_manage_tasks: True if owner/admin/contributor
```

#### **ProjectTask** (Task management)
```python
- project: ForeignKey(Project)
- title: CharField (max 200)
- description: TextField
- assigned_to: ForeignKey(User, null=True)
- assigned_by: ForeignKey(User)
- status: CharField (todo, in_progress, review, completed, cancelled)
- priority: CharField (low, medium, high, urgent)
- due_date: DateField (null=True)
- completed_at: DateTimeField (null=True)
- created_at: DateTimeField
- updated_at: DateTimeField

Methods:
- mark_completed(): Change status and set completed_at
```

#### **ProjectMilestone** (Project milestones)
```python
- project: ForeignKey(Project)
- title: CharField (max 200)
- description: TextField
- due_date: DateField (null=True)
- is_completed: BooleanField
- completed_at: DateTimeField (null=True)
- completed_by: ForeignKey(User, null=True)
- created_at: DateTimeField
- updated_at: DateTimeField

Methods:
- mark_completed(user=None): Mark milestone as complete
```

### 4. Collaboration Models

#### **Connection** (User networking)
```python
- sender: ForeignKey(User, related_name='sent_connections')
- receiver: ForeignKey(User, related_name='received_connections')
- status: CharField (pending, accepted, rejected)
- created_at: DateTimeField
- updated_at: DateTimeField

Unique Constraint: (sender, receiver)
```

#### **Follow** (User following)
```python
- follower: ForeignKey(User, related_name='following')
- following: ForeignKey(User, related_name='followers')
- created_at: DateTimeField

Unique Constraint: (follower, following)
```

### 5. Social/Interaction Models

#### **Like** (Project likes)
```python
- project: ForeignKey(Project)
- user: ForeignKey(User)
- created_at: DateTimeField

Unique Constraint: (project, user)
```

#### **Comment** (Project comments)
```python
- project: ForeignKey(Project)
- user: ForeignKey(User)
- content: TextField
- created_at: DateTimeField
- updated_at: DateTimeField
```

#### **Activity** (User activity feed)
```python
- user: ForeignKey(User)
- activity_type: CharField (profile_updated, project_created, etc.)
- title: CharField (max 200)
- description: TextField
- project: ForeignKey(Project, null=True)
- target_user: ForeignKey(User, null=True) for mentions
- connection: ForeignKey(Connection, null=True)
- is_public: BooleanField
- created_at: DateTimeField
```

### 6. Messaging Models

#### **Message** (Direct messages)
```python
- sender: ForeignKey(User, related_name='sent_messages')
- receiver: ForeignKey(User, null=True, blank=True)
- chat_room: ForeignKey(ChatRoom, null=True, blank=True)
- content: TextField
- message_type: CharField (text, file, image, call)
- call_type: CharField (voice, video) - for calls
- reply_to: ForeignKey(self, null=True) - for threading
- is_read: BooleanField
- read_at: DateTimeField (null=True)
- created_at: DateTimeField
- updated_at: DateTimeField
```

#### **ChatRoom** (Group chats)
```python
- name: CharField (max 100, null=True)
- chat_type: CharField (direct, group, project)
- project: ForeignKey(Project, null=True)
- is_active: BooleanField
- created_at: DateTimeField
- created_by: ForeignKey(User, null=True)

Properties:
- display_name: Smart naming based on chat_type
```

#### **ChatRoomMember** (Chat room participants)
```python
- room: ForeignKey(ChatRoom)
- user: ForeignKey(User)
- joined_at: DateTimeField
- role: CharField (admin, member)

Unique Constraint: (room, user)
```

#### **MessageFile** (File attachments)
```python
- message: ForeignKey(Message)
- file: ForeignKey(File)
- uploaded_at: DateTimeField

Unique Constraint: (message, file)
```

#### **MessageReaction** (Message reactions)
```python
- message: ForeignKey(Message)
- user: ForeignKey(User)
- reaction: CharField (emoji or text)
- created_at: DateTimeField

Unique Constraint: (message, user, reaction)
```

#### **MessageReadStatus** (Read receipts)
```python
- message: ForeignKey(Message)
- user: ForeignKey(User)
- read_at: DateTimeField

Unique Constraint: (message, user)
```

#### **File** (File storage)
```python
- user: ForeignKey(User)
- file: FileField
- filename: CharField (max 255)
- file_size: PositiveIntegerField
- file_type: CharField (max 100) - MIME type
- uploaded_at: DateTimeField

Properties:
- is_image: Check if MIME type starts with 'image/'
```

### 7. Notification/Status Models

#### **Notification** (User notifications)
```python
- user: ForeignKey(User)
- notification_type: CharField
- title: CharField
- message: TextField
- from_user: ForeignKey(User, null=True)
- project: ForeignKey(Project, null=True)
- is_read: BooleanField
- created_at: DateTimeField
```

#### **UserStatus** (Online status)
```python
- user: OneToOneField(User)
- is_online: BooleanField
- last_seen: DateTimeField
```

### 8. Statistics Models

#### **UserStats** (User dashboard statistics)
```python
- user: OneToOneField(User)
- projects_created: PositiveIntegerField
- connections_made: PositiveIntegerField
- likes_received: PositiveIntegerField
- comments_made: PositiveIntegerField
- projects_joined: PositiveIntegerField
- tasks_completed: PositiveIntegerField
- followers_count: PositiveIntegerField
- following_count: PositiveIntegerField
- last_updated: DateTimeField

Methods:
- update_stats(): Calculate all statistics from database
```

### 9. Team Management Models

#### **ProjectTeamInvitation** (Team invitations)
```python
- team: ForeignKey(ProjectTeam)
- invited_user: ForeignKey(User)
- invited_by: ForeignKey(User)
- role: CharField (owner, admin, contributor, viewer)
- message: TextField (optional)
- status: CharField (pending, accepted, declined, expired)
- created_at: DateTimeField
- expires_at: DateTimeField
- responded_at: DateTimeField (null=True)

Methods:
- accept(): Add user to team if not expired
- decline(): Decline invitation
```

---

## ✨ Features

### 1. Authentication & Authorization
- ✅ **OTP-Based Login**: 6-digit OTP sent via email, 5-minute validity
- ✅ **User Registration**: Email + password + profile setup
- ✅ **Social Authentication**: Google OAuth 2.0 and GitHub OAuth
- ✅ **Password Reset**: Email-based password recovery
- ✅ **Session Management**: Django sessions with timeout

### 2. User Profiles
- ✅ **Student Profile**: Full name, college, location, bio, photo
- ✅ **Skills Tracking**: JSON array of selected technical skills
- ✅ **Project Interests**: Categories of projects user is interested in
- ✅ **Social Links**: GitHub, LinkedIn, Portfolio, Behance URLs
- ✅ **Role Preference**: Developer, Designer, Manager, etc.

### 3. Project Management
- ✅ **Create Projects**: Post projects with title, description, tech stack
- ✅ **Browse Projects**: Explore and search all projects
- ✅ **Filter & Search**: By technology, category, timeline, keywords
- ✅ **Project Details**: Full project page with team, tasks, milestones
- ✅ **Edit/Delete**: Manage your own projects
- ✅ **Project Status**: Active, Completed, Paused

### 4. Team Collaboration
- ✅ **Team Creation**: Automatic team setup with projects
- ✅ **Role-Based Access**: Owner, Admin, Contributor, Viewer
- ✅ **Team Invitations**: Invite users with role assignment
- ✅ **Member Management**: Add, remove, or change member roles
- ✅ **Task Assignment**: Assign tasks to team members
- ✅ **Task Tracking**: Monitor task status and completion

### 5. Task & Milestone Management
- ✅ **Create Tasks**: Assign tasks with priority and due dates
- ✅ **Task Status**: To-Do, In Progress, In Review, Completed, Cancelled
- ✅ **Priority Levels**: Low, Medium, High, Urgent
- ✅ **Milestones**: Track project milestones with completion status
- ✅ **Timeline Tracking**: Estimated vs. actual completion

### 6. Networking & Connections
- ✅ **Connection Requests**: Send/receive connection requests
- ✅ **Connection Status**: Pending, Accepted, Rejected
- ✅ **Find Collaborators**: Filter by skills, interests, projects
- ✅ **User Profiles**: View other users' profiles and projects
- ✅ **Follow System**: Follow users for updates
- ✅ **Connection Management**: Accept, reject, or cancel requests

### 7. Real-Time Messaging
- ✅ **Direct Messages**: One-to-one private messaging
- ✅ **Group Chats**: Create group chat rooms
- ✅ **Project Chats**: Team discussion channels
- ✅ **Message Types**: Text, Files, Images, Calls
- ✅ **Message Threading**: Reply to specific messages
- ✅ **Read Receipts**: Track message read status
- ✅ **Typing Indicators**: Show when someone is typing
- ✅ **Message Reactions**: React with emojis
- ✅ **File Sharing**: Share files in messages
- ✅ **Message Search**: Search message history
- ✅ **Draft Messages**: Save drafts before sending

### 8. Activity & Notifications
- ✅ **Activity Feed**: See user activities (projects, connections, etc.)
- ✅ **Notifications**: Real-time notifications for interactions
- ✅ **Notification Types**: Connections, messages, comments, etc.
- ✅ **Read/Unread**: Track notification status
- ✅ **Activity Types**: 9+ different activity types

### 9. Social Interactions
- ✅ **Like Projects**: Like/unlike projects
- ✅ **Comment on Projects**: Add comments to projects
- ✅ **Project Feed**: Discover new projects
- ✅ **Like Counters**: See project popularity
- ✅ **Comment Threads**: Discussion on projects

### 10. Premium Features
- ✅ **Investor Dashboard**: Special view for investors
- ✅ **Premium Tier**: Subscription-based features
- ✅ **Upgrade Path**: Free to Premium upgrade
- ✅ **Premium Benefits**: Extended features

### 11. Additional Features
- ✅ **College Search**: Search universities via RapidAPI
- ✅ **College Validation**: Validate college/university names
- ✅ **Help Center**: FAQ and support resources
- ✅ **Contact Form**: User contact/feedback
- ✅ **Privacy Policy**: Legal documentation
- ✅ **Terms of Service**: Terms and conditions
- ✅ **About Page**: Platform information

---

## 🔌 API Endpoints

### Base URL: `/api/` or `/accounts/`

### Authentication Endpoints
```
POST   /register/              - Register new user
POST   /login/                 - Login with credentials
POST   /logout/                - Logout user
POST   /forgot-password/       - Request password reset
POST   /reset-password/        - Reset password with token
POST   /verify-otp/<purpose>/  - Verify OTP code
GET    /resend-otp/<purpose>/  - Resend OTP
```

### Profile Endpoints
```
GET    /student-profile/       - Get logged-in user's profile
GET    /student-details/       - Get student details page
GET    /profile/               - API: User profile (DRF)
GET    /user/<username>/       - Get user public profile
GET    /user-profile/<user_id>/ - API: Get user by ID
```

### Project Endpoints
```
POST   /post-project/          - Create new project
GET    /explore-projects/      - Browse all projects
GET    /my-projects/           - Get user's projects
GET    /project-detail/<id>/   - Get project details
GET    /project/<id>/          - API: Get project by ID
PUT    /edit-project/<id>/     - Edit project
DELETE /delete-project/<id>/   - Delete project
GET    /like-project/<id>/     - Like/unlike project
```

### Connection/Networking Endpoints
```
POST   /connect/<user_id>/                    - Send connection request
POST   /send-connection/<user_id>/            - Alternative connect endpoint
POST   /send-connection-request/<user_id>/   - Another connect variant
GET    /my-connections/                      - Get user's connections
PUT    /accept-connection/<conn_id>/         - Accept connection
DELETE /reject-connection/<conn_id>/         - Reject connection
DELETE /cancel-connection/<conn_id>/         - Cancel pending request
GET    /find-collaborators/                  - Find collaborators page
POST   /follow/<user_id>/                    - Follow user
```

### Team Management Endpoints
```
POST   /invite-to-team/<project_id>/         - Invite to team
PUT    /respond-team-invitation/<inv_id>/   - Accept/decline invite
DELETE /remove-team-member/<proj_id>/<uid>/ - Remove team member
```

### Messaging Endpoints
```
GET    /messages/              - Message view (HTML)
GET    /chat/<user_id>/        - Chat with user (HTML)
GET    /enhanced-messages/     - Enhanced messaging page
GET    /enhanced-chat/<room_id>/ - Enhanced chat view
POST   /create-group-chat/     - Create group chat
POST   /add-reaction/<msg_id>/ - Add reaction to message
POST   /start-call/<room_id>/  - Start voice/video call
GET    /download-file/<id>/    - Download file attachment

REST API:
POST   /chat-rooms/                       - Create chat room
GET    /chat-rooms/                       - List chat rooms
GET    /chat-rooms/<id>/                 - Get chat room
GET    /chat-rooms/<room_id>/members/    - Get room members
POST   /direct-message/                  - Send direct message
GET    /messages/                        - List messages
POST   /messages/                        - Create message
GET    /messages/<id>/                  - Get message
GET    /messages/search/                - Search messages
GET    /messages/<msg_id>/status/       - Message status
POST   /messages/<msg_id>/reactions/    - Message reactions
GET    /drafts/                         - Get draft messages
POST   /typing/                         - Typing indicator
GET    /conversations/                  - Conversation list
```

### Notification Endpoints
```
GET    /notifications/                       - Get notifications
PUT    /mark-notification-read/<notif_id>/  - Mark as read
GET    /activity-feed/                      - Activity feed
```

### Utility Endpoints
```
GET    /college-search/          - Search colleges via RapidAPI
GET    /validate-college/        - Validate college name
GET    /check-username/          - Check username availability
GET    /check-email/             - Check email availability
POST   /nlp-analyze/             - NLP analysis endpoint
GET    /user-stats/              - User statistics
GET    /help/                    - Help center
GET    /contact/                 - Contact form
POST   /contact/submit/          - Submit contact form
GET    /privacy/                 - Privacy policy
GET    /terms/                   - Terms of service
```

### Dashboard & Main Endpoints
```
GET    /dashboard/               - User dashboard
GET    /main_home/               - Main homepage
GET    /investor-dashboard/      - Investor dashboard
GET    /premium/                 - Premium features page
GET    /upgrade/                 - Upgrade subscription
GET    /about/                   - About page
GET    /                         - API root
GET    /home/                    - API home (stats)
```

**Total: 60+ API endpoints**

### Response Format (JSON)
```json
{
  "id": 1,
  "status": "success",
  "message": "Operation completed",
  "data": {},
  "errors": []
}
```

---

## 🔐 Authentication System

### OTP-Based Authentication Flow

```
1. User Email Input
   ↓
2. Check if email exists/new
   ↓
3. Generate 6-digit OTP
   ↓
4. Send OTP via Email (HTML formatted)
   ↓
5. User enters OTP on verification page
   ↓
6. Validate OTP:
   - Check format (6 digits)
   - Check expiry (5 minutes)
   - Check if already used
   ↓
7. Mark OTP as used
   ↓
8. Create/Update User Account
   ↓
9. Create Session
   ↓
10. Redirect to Dashboard
```

### Authentication Backends
```python
AUTHENTICATION_BACKENDS = (
    'django.contrib.auth.backends.ModelBackend',      # Standard auth
    'allauth.account.auth_backends.AuthenticationBackend',  # Social auth
)
```

### Social Authentication (OAuth 2.0)
- **Google**: Requires GOOGLE_CLIENT_ID and GOOGLE_CLIENT_SECRET
- **GitHub**: Requires GITHUB_CLIENT_ID and GITHUB_CLIENT_SECRET

### Session Management
```python
SESSION_COOKIE_SECURE = False  # Enable in production
CSRF_COOKIE_SECURE = False     # Enable in production
SESSION_COOKIE_HTTPONLY = True
CSRF_COOKIE_HTTPONLY = True
```

### Login Redirects
```python
LOGIN_REDIRECT_URL = '/dashboard/'
LOGOUT_REDIRECT_URL = '/login/'
ACCOUNT_LOGOUT_REDIRECT_URL = '/login/'
```

---

## 📁 File Structure

```
e:/login/auth_project/
├── auth_project/               # Main Django project settings
│   ├── __init__.py
│   ├── settings.py             # Core configuration
│   ├── urls.py                 # Root URL routing
│   ├── wsgi.py                 # WSGI entry point
│   └── asgi.py                 # ASGI entry point (WebSockets)
│
├── accounts/                   # Main app (accounts app)
│   ├── migrations/             # Database migrations
│   ├── static/                 # Static files (CSS, JS, images)
│   ├── templates/              # HTML templates
│   │   ├── accounts/           # App-specific templates
│   │   ├── base.html           # Base template
│   │   ├── login.html
│   │   ├── register.html
│   │   ├── dashboard.html
│   │   ├── project_*.html
│   │   ├── chat_*.html
│   │   └── ...
│   ├── templatetags/           # Custom template tags
│   │
│   ├── __init__.py
│   ├── admin.py                # Django admin configuration
│   ├── apps.py                 # App configuration
│   ├── forms.py                # Form classes (50+ form fields)
│   ├── models.py               # Database models (25+ models)
│   ├── urls.py                 # App URL routing (60+ routes)
│   ├── views.py                # View functions (50+ views)
│   ├── serializers.py          # DRF serializers
│   ├── permissions.py          # Custom permissions
│   ├── utils.py                # Utility functions
│   │
│   ├── chat_api.py             # Chat/messaging API views
│   ├── chat_api_improved.py    # Enhanced chat API
│   ├── views_contact.py        # Contact form views
│   │
│   ├── zepto_mail_backend.py   # ZeptoMail email backend
│   ├── brevo_mail_backend.py   # Brevo email backend
│   │
│   ├── tests.py                # Unit tests
│   └── ...
│
├── media/                      # User uploads (profile photos, files)
│   ├── profile_photos/
│   ├── chat_files/
│   └── ...
│
├── static/                     # Static files (CSS, JS, images)
│   ├── css/
│   ├── js/
│   └── images/
│
├── staticfiles/                # Collected static files (production)
│
├── logs/                       # Application logs
│   ├── django.log
│   └── error.log
│
├── templates/                  # Project-level templates (if exists)
│
├── manage.py                   # Django management script
├── db.sqlite3                  # Development database
├── requirements.txt            # Python dependencies
├── .env                        # Environment variables (not in repo)
├── render.yaml                 # Render deployment config
├── build.sh                    # Build script
├── .gitignore
│
├── Test/Debug Files:
│   ├── test_otp.py
│   ├── test_otp_simple.py
│   ├── test_otp_console.py
│   ├── test_email.py
│   ├── test_brevo_email.py
│   ├── test_services.py
│   ├── test_connections.py
│   ├── test_search.py
│   ├── test_filter.py
│   ├── test_filtering_debug.py
│   ├── test_profile_upload.py
│   ├── test_zeptomail.py
│   ├── test_zepto_simple.py
│   ├── test_rapidapi.py
│   ├── check_profiles.py
│   ├── check_social_apps.py
│   ├── debug_profiles.py
│   ├── debug_filtering.py
│   ├── debug_find_collaborators.py
│   ├── debug_profile_photo.py
│   ├── performance_monitor.py
│   ├── performance_monitor_FIXED.py
│   ├── create_test_profiles.py
│   ├── create_test_user.py
│   ├── fix_pongal_now.py
│   ├── run_social_setup.py
│   └── ...
│
└── Documentation:
    ├── ✨_README_START_HERE.md
    ├── PROJECT_DOCUMENTATION.md (this file)
    ├── CODEBASE_COMPLETE_ANALYSIS_2025.md
    ├── QUICK_REFERENCE_GUIDE.md
    └── ...
```

---

## 🚀 Setup & Installation

### Prerequisites
- Python 3.9+
- PostgreSQL 12+ (or use SQLite for development)
- Redis 6+ (optional, for caching/WebSockets)
- Git

### Step 1: Clone Repository
```bash
git clone https://github.com/Goku0090/uni.git
cd e:/login/auth_project
```

### Step 2: Create Virtual Environment
```bash
python -m venv venv
.\venv\Scripts\activate  # Windows
source venv/bin/activate  # Linux/Mac
```

### Step 3: Install Dependencies
```bash
pip install -r requirements.txt
```

### Step 4: Environment Setup
Create `.env` file:
```bash
# Django
DEBUG=True
SECRET_KEY=your-secret-key-here
ALLOWED_HOSTS=localhost,127.0.0.1

# Database
DATABASE_URL=postgresql://user:password@localhost:5432/unisync_db
# OR for SQLite:
# DB_ENGINE=django.db.backends.sqlite3

# Email Configuration
BREVO_API_KEY=your-brevo-key
# OR
ZEPTO_MAIL_API_KEY=your-zepto-key
ZEPTO_MAIL_TOKEN=your-zepto-token

# Social Auth
GOOGLE_CLIENT_ID=your-google-client-id
GOOGLE_CLIENT_SECRET=your-google-secret
GITHUB_CLIENT_ID=your-github-client-id
GITHUB_CLIENT_SECRET=your-github-secret

# External Services
RAPIDAPI_KEY=your-rapidapi-key

# Redis (Optional)
REDIS_URL=redis://localhost:6379/0

# Email
DEFAULT_FROM_EMAIL=noreply@unisync.app
```

### Step 5: Database Migrations
```bash
python manage.py migrate
```

### Step 6: Create Superuser (Admin)
```bash
python manage.py createsuperuser
# Follow prompts to create admin account
```

### Step 7: Create Test Data (Optional)
```bash
python manage.py shell
>>> from accounts.models import StudentProfile
>>> from django.contrib.auth.models import User
>>> # Create test users and projects
```

### Step 8: Run Development Server
```bash
python manage.py runserver
```

Access at: `http://127.0.0.1:8000/`
- Admin: `http://127.0.0.1:8000/admin/`
- Login: `http://127.0.0.1:8000/login/`

### Step 9: Collect Static Files (for production)
```bash
python manage.py collectstatic --noinput
```

---

## 📦 Deployment

### Deployment Options

#### Option 1: Render (Recommended)
Files needed: `render.yaml`, `requirements.txt`

```yaml
# render.yaml configuration
services:
  - type: web
    name: unisync
    env: python
    buildCommand: pip install -r requirements.txt && python manage.py migrate && python manage.py collectstatic --noinput
    startCommand: gunicorn auth_project.wsgi:application
    envVars:
      - key: DATABASE_URL
        scope: DATABASE_URL
      - key: DEBUG
        value: false
      - key: SECRET_KEY
        generateValue: true
```

Deploy:
```bash
git push origin main
# Render auto-deploys
```

#### Option 2: Heroku
```bash
# Install Heroku CLI
heroku create unisync-app

# Set environment variables
heroku config:set DEBUG=False
heroku config:set SECRET_KEY=your-secret-key

# Deploy
git push heroku main

# Run migrations
heroku run python manage.py migrate
```

#### Option 3: Docker
Create `Dockerfile`:
```dockerfile
FROM python:3.11
WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY . .
RUN python manage.py collectstatic --noinput
CMD ["gunicorn", "auth_project.wsgi:application", "--bind", "0.0.0.0:8000"]
```

Build and run:
```bash
docker build -t unisync .
docker run -p 8000:8000 unisync
```

### Production Checklist
- [ ] Set DEBUG=False
- [ ] Configure SECRET_KEY (from environment)
- [ ] Configure ALLOWED_HOSTS
- [ ] Set up HTTPS/SSL
- [ ] Configure database (PostgreSQL)
- [ ] Set up email backend (Brevo or ZeptoMail)
- [ ] Configure social auth (Google, GitHub)
- [ ] Set up Redis for caching
- [ ] Configure WebSocket server (if using Channels)
- [ ] Set up background tasks (Celery)
- [ ] Configure monitoring (Sentry)
- [ ] Set up backups
- [ ] Configure CDN for static files
- [ ] Set up CI/CD pipeline

---

## 📊 Database Relationships Diagram

```
User (Django built-in)
├── StudentProfile (1:1)
├── Project (1:many) - as owner
├── ProjectTask (1:many) - as assigned_by
├── ProjectTeamMember (1:many)
├── Connection (1:many) - as sender/receiver
├── Message (1:many) - as sender
├── Like (1:many)
├── Comment (1:many)
├── Follow (1:many) - as follower/following
├── Activity (1:many)
├── Notification (1:many)
├── UserStats (1:1)
└── UserStatus (1:1)

Project
├── ProjectTeam (1:1)
├── ProjectTask (1:many)
├── ProjectMilestone (1:many)
├── ChatRoom (1:many)
├── Like (1:many)
├── Comment (1:many)
├── Activity (1:many)
└── ProjectTeamInvitation (via ProjectTeam)

ChatRoom
├── Message (1:many)
├── ChatRoomMember (1:many)
└── MessageFile (via Message)

Message
├── MessageFile (1:many)
├── MessageReaction (1:many)
├── MessageReadStatus (1:many)
└── reply_to (self-reference)
```

---

## 🔧 Common Tasks

### Create a New Project
```python
from accounts.models import Project, ProjectTeam

project = Project.objects.create(
    owner=request.user,
    title="My Awesome Project",
    description="Project description...",
    category='web',
    technologies=['django', 'react', 'postgresql'],
    looking_for=['frontend_dev', 'ui_ux_designer'],
    collaboration_needs="Looking for...",
    github_link="https://github.com/user/project"
)

# Auto-create team
team = ProjectTeam.objects.create(
    project=project,
    name=f"{project.title} Team"
)
```

### Send Connection Request
```python
from accounts.models import Connection

connection = Connection.objects.create(
    sender=current_user,
    receiver=target_user,
    status='pending'
)
```

### Send Message
```python
from accounts.models import Message, ChatRoom

message = Message.objects.create(
    sender=request.user,
    receiver=target_user,
    content="Hello!",
    message_type='text'
)
```

### Create Notification
```python
from accounts.models import Notification

notification = Notification.objects.create(
    user=target_user,
    notification_type='connection_request',
    title="New Connection Request",
    message=f"{current_user.username} sent you a connection request",
    from_user=current_user
)
```

---

## 📞 Support & Contact

For issues, questions, or contributions:
- GitHub: https://github.com/Goku0090/uni
- Email: support@unisync.app
- Documentation: See files in project root

---

## 📝 License

This project is part of the UniSync platform.

---

**Last Updated**: January 2025  
**Version**: 1.0.0  
**Status**: Production Ready
