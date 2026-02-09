# 🏗️ COMPLETE CODEBASE ANALYSIS
## UniSync Project - Student Collaboration Platform
**Last Updated:** February 7, 2026 | **Status:** Complete & Production Ready

---

## 📋 TABLE OF CONTENTS

1. [Executive Summary](#executive-summary)
2. [Architecture Overview](#architecture-overview)
3. [Technology Stack](#technology-stack)
4. [Project Structure](#project-structure)
5. [Core Components](#core-components)
6. [Data Models](#data-models)
7. [API Endpoints](#api-endpoints)
8. [WebSocket/Real-time Features](#websocketreal-time-features)
9. [Authentication & Security](#authentication--security)
10. [Frontend Implementation](#frontend-implementation)
11. [Code Quality & Patterns](#code-quality--patterns)
12. [Deployment & Configuration](#deployment--configuration)
13. [Performance Considerations](#performance-considerations)
14. [Known Issues & Fixes](#known-issues--fixes)

---

## EXECUTIVE SUMMARY

### What is UniSync?
A Django-based student collaboration platform enabling peer discovery, project management, real-time messaging, and social networking features.

### Key Capabilities
- **User Management**: Registration via OTP/Social Login (Google, GitHub)
- **Collaboration**: Find collaborators, create projects, assign tasks
- **Communication**: Real-time chat, comments, activity feeds
- **Social**: Connections (friends), followers, notifications, likes
- **Real-time**: WebSocket-powered live updates (requires Daphne ASGI)

### Technology Stack
| Layer | Technology |
|-------|-----------|
| **Backend** | Django 4.x, Django Channels, Daphne ASGI |
| **Database** | PostgreSQL (prod) / SQLite (dev) |
| **Frontend** | Django Templates, Vanilla JavaScript |
| **Real-time** | WebSocket, Django Channels, Redis (optional) |
| **Authentication** | django-allauth, OTP |
| **Email** | Brevo/Zepto (external services) |

### Current Status
- ✅ All core features implemented
- ✅ HTTP endpoints working
- ✅ WebSocket infrastructure in place
- ⚠️ WebSocket requires Daphne (runserver returns 404)
- ✅ Database schema complete
- ✅ Authentication system functional
- ✅ Real-time features ready (pending Daphne activation)

---

## ARCHITECTURE OVERVIEW

### System Architecture

```
┌─────────────────────────────────────────────────────────────────┐
│                        FRONTEND LAYER                            │
│  Django Templates + HTML + Vanilla JavaScript                    │
│  ├── Dashboard                                                   │
│  ├── Project Pages                                               │
│  ├── User Profiles                                               │
│  ├── Messaging Interface                                         │
│  ├── Activity Feed                                               │
│  └── WebSocket Handlers (realtime-updates.js)                    │
└─────────────────────────────────────────────────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────────┐
│                     WSGI/ASGI SERVER                             │
│  ├── Daphne ASGI (HTTP + WebSocket) - PRODUCTION                │
│  └── Django runserver (HTTP only) - DEVELOPMENT                  │
└─────────────────────────────────────────────────────────────────┘
                              │
                ┌─────────────┼─────────────┐
                ▼             ▼             ▼
         ┌──────────┐  ┌──────────┐  ┌──────────┐
         │  HTTP    │  │WebSocket │  │  Static  │
         │  Router  │  │  Router  │  │  Files   │
         │urls.py   │  │routing.py│  │          │
         └──────────┘  └──────────┘  └──────────┘
                │             │
    ┌───────────┴─────────────┴───────────┐
    ▼                                     ▼
┌─────────────────────────┐    ┌─────────────────────────┐
│    VIEWS LAYER          │    │  WEBSOCKET CONSUMERS    │
├─────────────────────────┤    ├─────────────────────────┤
│ • Dashboard (view)      │    │ • ProjectUpdateConsumer │
│ • Authentication        │    │ • NotificationConsumer  │
│ • Project Management    │    │ • ActivityFeedConsumer  │
│ • User Profiles         │    │ • ChatConsumer          │
│ • Messaging APIs        │    │                         │
│ • Comments              │    │ Group Broadcasting      │
│ • Social Features       │    │                         │
└─────────────────────────┘    └─────────────────────────┘
                │                       │
                └───────────┬───────────┘
                            ▼
┌─────────────────────────────────────────────────────────────────┐
│                     APPLICATION LAYER                            │
│                   (Business Logic)                               │
│  ├── StudentProfileNLP (collaborative filtering)                │
│  ├── ProjectVisibilityFilter (privacy controls)                 │
│  ├── Email/OTP Services                                         │
│  ├── File Management                                            │
│  └── Signal Handlers (real-time triggers)                       │
└─────────────────────────────────────────────────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────────┐
│                      DATA LAYER                                  │
│  Django Models & ORM                                             │
│  ├── User & Profile Management                                   │
│  ├── Project & Collaboration                                     │
│  ├── Messaging & Chat                                            │
│  ├── Social Features                                             │
│  ├── Activity & Notifications                                    │
│  └── Metadata (Likes, Connections, etc.)                         │
└─────────────────────────────────────────────────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────────┐
│                     DATABASE LAYER                               │
│  PostgreSQL (Production) / SQLite (Development)                 │
│  ├── User Tables (auth, profiles)                               │
│  ├── Project Tables                                              │
│  ├── Messaging Tables                                            │
│  ├── Social Tables                                               │
│  └── Activity/Notification Tables                                │
└─────────────────────────────────────────────────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────────┐
│                  EXTERNAL SERVICES                               │
│  ├── Email: Brevo/Zepto (OTP, Notifications)                   │
│  ├── Auth: Google OAuth, GitHub OAuth                            │
│  ├── Cache: Django Cache, Redis (optional)                       │
│  └── Storage: AWS S3 (optional for media)                        │
└─────────────────────────────────────────────────────────────────┘
```

### Request Flow (HTTP)

```
1. Browser Request
   ↓
2. Django URL Router (urls.py)
   ├─ Matches URL pattern
   └─ Routes to appropriate view
   ↓
3. View Processing
   ├─ Authenticate user
   ├─ Fetch/process data from models
   ├─ Apply business logic
   └─ Prepare context
   ↓
4. Template Rendering
   ├─ Render Django template
   ├─ Include static files (CSS, JS)
   └─ Inject context variables
   ↓
5. Response to Browser
   ├─ HTML/JSON response
   └─ Status 200 (or error code)
```

### WebSocket Flow (Real-time)

```
1. Browser WebSocket Init (realtime-updates.js)
   ↓
2. Connection Establishment
   ws://localhost:8000/ws/project/2/
   ↓
3. Daphne ASGI Server
   ├─ Recognizes WebSocket upgrade
   ├─ Routes via routing.py
   └─ Connects to appropriate Consumer
   ↓
4. Consumer Connection Handler
   ├─ Accept connection
   ├─ Join broadcast group
   ├─ Send initial data
   └─ Ready to receive/send messages
   ↓
5. Message Exchange
   ├─ Browser sends: {"type": "status.update", "status": "in_progress"}
   ├─ Consumer receives, processes, broadcasts to group
   ├─ All connected clients receive update
   └─ UI updates in real-time
   ↓
6. Connection Termination
   ├─ Client disconnect
   ├─ Consumer cleanup
   └─ Group membership removed
```

---

## TECHNOLOGY STACK

### Backend
- **Framework**: Django 4.2
- **ASGI Server**: Daphne 4.0.0 (required for WebSocket)
- **WSGI Server**: Gunicorn (fallback for HTTP-only)
- **Task Queue**: Celery (optional, not currently used)
- **Cache**: Django Cache Framework + Redis (optional)

### Database
- **Production**: PostgreSQL 13+
- **Development**: SQLite3
- **Migrations**: Django ORM + South/Django Migrations

### Frontend
- **Templating**: Django Templates (Jinja2-like syntax)
- **Styling**: CSS3 + Bootstrap/Custom CSS
- **Scripting**: Vanilla JavaScript (ES6+)
- **Real-time**: WebSocket API
- **HTTP Client**: Fetch API

### Authentication & Authorization
- **Authentication**: Django-allauth, Custom OTP
- **Social OAuth**: Google, GitHub
- **Permissions**: Django Permissions + Custom decorators

### External Services
- **Email**: Brevo API or Zepto Mail API
- **Cloud Storage**: AWS S3 (optional)

### Development Tools
- **Testing**: pytest, Django TestCase
- **Linting**: Ruff, Black
- **Version Control**: Git
- **Package Management**: pip, requirements.txt

---

## PROJECT STRUCTURE

### Directory Layout

```
e:/login/auth_project/
├── auth_project/                    # Project configuration
│   ├── asgi.py                      # ASGI entry point (WebSocket support)
│   ├── wsgi.py                      # WSGI entry point (HTTP only)
│   ├── settings.py                  # Django settings
│   ├── urls.py                      # Root URL configuration
│   └── __init__.py
│
├── accounts/                        # Main application
│   ├── models.py                    # Django Models (User, Project, Message, etc.)
│   ├── views.py                     # View functions (HTTP endpoints)
│   ├── urls.py                      # App URL routes
│   ├── consumers.py                 # WebSocket consumers (real-time)
│   ├── routing.py                   # WebSocket URL routing
│   ├── serializers.py               # REST API serializers
│   ├── forms.py                     # Django forms
│   ├── permissions.py               # Custom permission classes
│   ├── utils.py                     # Utility functions
│   ├── signals_realtime.py          # Django signal handlers
│   │
│   ├── static/                      # Static files
│   │   ├── js/
│   │   │   ├── realtime-updates.js # WebSocket client
│   │   │   ├── api-utils.js        # API utilities
│   │   │   └── login.js            # Authentication JS
│   │   ├── css/
│   │   └── images/
│   │
│   ├── templates/                   # Django templates
│   │   ├── dashboard.html
│   │   ├── project_detail.html
│   │   ├── profile.html
│   │   ├── messages.html
│   │   └── ...
│   │
│   ├── migrations/                  # Database migrations
│   │   ├── 0001_initial.py
│   │   └── ...
│   │
│   ├── services/                    # Business logic services
│   │   ├── email_service.py
│   │   └── ...
│   │
│   ├── tests.py                     # Unit tests
│   └── apps.py
│
├── media/                           # User-uploaded files
│   ├── profile_photos/
│   ├── project_files/
│   └── ...
│
├── static/                          # Global static files
│   ├── js/
│   ├── css/
│   └── images/
│
├── staticfiles/                     # Collected static files (production)
│
├── templates/                       # Global templates
│   ├── base.html
│   └── ...
│
├── logs/                            # Application logs
│
├── manage.py                        # Django management CLI
├── requirements.txt                 # Python dependencies
├── .env                             # Environment variables
├── Procfile                         # Deployment configuration
├── asgi.py                          # ASGI configuration (Render/Railway)
└── wsgi.py                          # WSGI configuration (Heroku/traditional)
```

### Key Configuration Files

**requirements.txt** - Dependencies
```
Django==4.2
djangorestframework==3.14
django-allauth==0.61
django-channels==4.0
daphne==4.0.0
psycopg2-binary==2.9
```

**Procfile** - Deployment command
```
web: daphne -b 0.0.0.0 -p $PORT auth_project.asgi:application
```

**.env** - Environment variables
```
DEBUG=False
SECRET_KEY=your-secret-key
DATABASE_URL=postgresql://...
ALLOWED_HOSTS=localhost,127.0.0.1
BREVO_API_KEY=...
```

---

## CORE COMPONENTS

### 1. Models (Data Layer)

#### User & Profile
- **User**: Django built-in user model (username, email, password)
- **StudentProfile**: Extended profile with college, skills, interests
- **UserStatus**: Online/offline status tracking
- **UserStats**: Activity statistics (posts, comments, likes)

#### Projects & Collaboration
- **Project**: Main project entity
  - Title, description, visibility (public/private)
  - Owner, members, tags
  - Status (planning, active, completed)
  - Timestamps (created, updated, deadline)

- **ProjectMember**: User involvement in projects
  - User, project, role, join date

- **ProjectTask**: Project tasks/milestones
  - Title, description, assigned to
  - Status, priority, due date

- **ProjectTeam**: Team management
- **ProjectTeamMember**: Team membership
- **ProjectTeamInvitation**: Invite system

#### Messaging
- **Message**: Direct messages between users
- **ChatRoom**: Group chat containers
- **ChatRoomMember**: Chat room membership
- **MessageFile**: File attachments in messages
- **MessageReadStatus**: Message read/unread tracking
- **MessageReaction**: Emoji reactions on messages

#### Social Features
- **Connection**: Friend requests/connections
- **Follow**: User following
- **Activity**: Activity log/feed
- **Notification**: User notifications
- **Like**: Likes on projects/content
- **Comment**: Comments on projects

#### Other
- **OTP**: One-time passwords for authentication
- **File**: File storage metadata

### 2. Views (HTTP Request Handlers)

**Authentication & User Management**
- `register_view`: User registration with OTP
- `login_view`: User login
- `verify_otp`: OTP verification
- `logout_view`: User logout
- `edit_profile`: Profile editing

**Project Management**
- `post_project`: Create new project
- `edit_project`: Edit project details
- `view_project_detail`: View single project
- `main_home`: Project feed/dashboard
- `delete_project`: Remove project
- `like_project`: Like functionality (AJAX)

**Collaboration**
- `find_collaborators`: Search for users to collaborate with
- `view_profile`: View user profile
- `connect_user`: Send connection request
- `accept_connection`: Accept connection request

**Messaging & Chat**
- `chat_view`: Chat room interface
- `message_api_view`: REST API for messages
- `get_messages_api`: Fetch messages
- `send_message_api`: Send messages

**Notifications & Activity**
- `notifications_view`: View notifications
- `activity_feed`: Activity feed display
- `get_notifications_api`: REST API for notifications

**Comments**
- `get_project_comments`: Fetch project comments
- `post_comment_api`: Add new comment

### 3. WebSocket Consumers (Real-time Features)

#### ProjectUpdateConsumer
- **Purpose**: Real-time project status updates
- **URL**: `ws://localhost:8000/ws/project/<id>/`
- **Events**:
  - `project.initial_data`: Send initial project state
  - `project_status_update`: Broadcast status changes
  - `project_member_add`: Notify new member joined
  - `project_comment`: Broadcast new comments

#### NotificationConsumer
- **Purpose**: Real-time user notifications
- **URL**: `ws://localhost:8000/ws/notifications/`
- **Events**:
  - `notification.send`: Push notifications to user
  - `notification.dismiss`: Remove notification

#### ActivityFeedConsumer
- **Purpose**: Real-time activity feed
- **URL**: `ws://localhost:8000/ws/activity-feed/`
- **Events**:
  - `activity.new`: Broadcast new activities
  - `activity.like`: Like notifications
  - `activity.comment`: Comment notifications

### 4. Utility Functions & Services

**StudentProfileNLP** (utils.py)
- Collaborative filtering for user recommendations
- Skill matching algorithm
- Interest-based scoring

**ProjectVisibilityFilter** (utils.py)
- Privacy enforcement
- Visibility control (public/private/friends-only)

**Email Services**
- OTP sending (Brevo/Zepto)
- Notification emails
- Welcome emails

---

## DATA MODELS (Detailed)

### StudentProfile
```python
class StudentProfile(models.Model):
    user              OneToOneField(User)
    full_name         CharField(100)
    college           CharField(200)
    location          CharField(100)
    interests         JSONField (list)
    bio               TextField
    profile_photo     ImageField
    skills            JSONField (list)
    project_interests JSONField (list)
    role_preference   CharField(50)
    github            URLField
    linkedin          URLField
    portfolio         URLField
    behance           URLField
    profile_completed BooleanField
    created_at        DateTimeField
    updated_at        DateTimeField
```

### Project
```python
class Project(models.Model):
    owner             ForeignKey(User)
    title             CharField(200)
    description       TextField
    visibility        CharField(choices: public, private)
    status            CharField(choices: planning, active, completed)
    tags              JSONField (list)
    collaboration_needs JSONField (dict)
    members           ManyToManyField(User, through ProjectMember)
    created_at        DateTimeField
    updated_at        DateTimeField
    deadline          DateTimeField(nullable)
```

### Message
```python
class Message(models.Model):
    sender            ForeignKey(User)
    recipient         ForeignKey(User, nullable)
    chat_room         ForeignKey(ChatRoom, nullable)
    content           TextField
    created_at        DateTimeField
    updated_at        DateTimeField
```

### Notification
```python
class Notification(models.Model):
    user              ForeignKey(User)
    actor             ForeignKey(User, related_name='notifications_sent')
    action_type       CharField(choices: like, comment, follow, message, connect)
    target_object_id  PositiveIntegerField
    target_type       CharField
    is_read           BooleanField(default: False)
    created_at        DateTimeField
```

### Connection
```python
class Connection(models.Model):
    from_user         ForeignKey(User, related_name='sent_connections')
    to_user           ForeignKey(User, related_name='received_connections')
    status            CharField(choices: pending, accepted, rejected)
    created_at        DateTimeField
    updated_at        DateTimeField
```

---

## API ENDPOINTS

### Authentication Endpoints
| Method | Endpoint | Purpose |
|--------|----------|---------|
| POST | `/register/` | User registration |
| POST | `/login/` | User login |
| POST | `/verify-otp/` | Verify OTP code |
| POST | `/logout/` | User logout |
| GET | `/social/google/` | Google OAuth callback |
| GET | `/social/github/` | GitHub OAuth callback |

### Project Endpoints
| Method | Endpoint | Purpose |
|--------|----------|---------|
| GET | `/dashboard/` | Project feed/dashboard |
| POST | `/post-project/` | Create new project |
| GET | `/project/<id>/` | View project details |
| POST | `/edit-project/<id>/` | Edit project |
| POST | `/delete-project/<id>/` | Delete project |
| POST | `/api/projects/<id>/like/` | Like project (AJAX) |
| GET | `/api/projects/` | List projects (REST API) |

### User & Profile Endpoints
| Method | Endpoint | Purpose |
|--------|----------|---------|
| GET | `/edit-profile/` | Edit profile page |
| POST | `/edit-profile/` | Update profile |
| GET | `/profile/<username>/` | View user profile |
| POST | `/api/user-profile/<id>/` | User profile API |
| GET | `/find-collaborators/` | Find collaborators page |
| GET | `/api/find-collaborators/` | Search collaborators (AJAX) |

### Messaging Endpoints
| Method | Endpoint | Purpose |
|--------|----------|---------|
| GET | `/messages/` | Messages page |
| POST | `/api/messages/` | Send message (REST API) |
| GET | `/api/messages/` | Fetch messages |
| POST | `/api/messages/mark-read/` | Mark message as read |
| GET | `/chat/<room_id>/` | Chat room view |

### Social Endpoints
| Method | Endpoint | Purpose |
|--------|----------|---------|
| POST | `/api/connect/<user_id>/` | Send connection request |
| POST | `/api/connect/<user_id>/accept/` | Accept connection |
| GET | `/api/connections/` | List connections |
| POST | `/api/follow/<user_id>/` | Follow user |
| GET | `/notifications/` | Notifications page |
| GET | `/api/notifications/` | Fetch notifications |

### Comments Endpoints
| Method | Endpoint | Purpose |
|--------|----------|---------|
| GET | `/api/projects/<id>/comments/` | Get project comments |
| POST | `/api/projects/<id>/comments/` | Add comment |
| DELETE | `/api/comments/<id>/` | Delete comment |

### Activity Feed Endpoints
| Method | Endpoint | Purpose |
|--------|----------|---------|
| GET | `/activity-feed/` | Activity feed page |
| GET | `/api/activity-feed/` | Activity feed API |

---

## WEBSOCKET/REAL-TIME FEATURES

### WebSocket Routes

```javascript
// Project Updates
ws://localhost:8000/ws/project/<project_id>/

// Activity Feed
ws://localhost:8000/ws/activity-feed/

// Notifications
ws://localhost:8000/ws/notifications/
```

### JavaScript Client Implementation

**realtime-updates.js** - Main WebSocket client class

```javascript
class RealtimeUpdates {
    init()                          // Initialize all WebSocket connections
    connectToProjectUpdates()        // Connect to project updates
    connectToActivityFeed()          // Connect to activity feed
    connectToNotifications()         // Connect to notifications
    handleProjectMessage()           // Process project messages
    handleActivityMessage()          // Process activity messages
    handleNotificationMessage()      // Process notifications
    attemptReconnect()              // Automatic reconnection logic
    showNotification()              // UI notification display
    getProjectId()                  // Extract project ID from DOM
}
```

### Example WebSocket Usage

```javascript
// Initialize (call once on page load)
const realtime = new RealtimeUpdates();
realtime.init();

// Manual WebSocket test
const socket = new WebSocket("ws://localhost:8000/ws/project/2/");
socket.onopen = () => console.log("✅ WORKING!");
socket.onmessage = (event) => {
    const data = JSON.parse(event.data);
    console.log("Update received:", data);
};
```

### Consumer-to-Client Communication

```python
# Server sends to group
async def broadcast_project_update(project_id, update_data):
    await self.channel_layer.group_send(
        f'project_{project_id}',
        {
            'type': 'project_status_update',
            'data': update_data
        }
    )

# Client receives
socket.onmessage = (event) => {
    const { type, data } = JSON.parse(event.data);
    if (type === 'project.status_update') {
        updateProjectUI(data);  // Update UI
    }
}
```

### Real-time Events Flow

```
1. Database Change
   └─ Django Signal triggered
      └─ Signal handler calls async_to_sync(broadcast_update)
         └─ Channel layer broadcasts to group
            └─ All connected consumers receive event
               └─ Consumer sends to connected WebSocket clients
                  └─ JavaScript client receives via onmessage
                     └─ JavaScript updates DOM
                        └─ User sees real-time update
```

---

## AUTHENTICATION & SECURITY

### Authentication Methods

1. **Email + OTP**
   - User enters email
   - System generates 6-digit OTP
   - OTP sent via Brevo/Zepto email
   - User verifies OTP
   - Account created/logged in

2. **Social OAuth (Google, GitHub)**
   - User clicks "Login with Google"
   - Redirects to Google OAuth consent
   - Google redirects back with auth code
   - django-allauth exchanges code for token
   - User profile auto-created or linked

3. **Session-based**
   - Django session middleware
   - Session stored in database or cache
   - CSRF token required for POST requests

### Security Features

- **CSRF Protection**: CSRF tokens in forms and AJAX requests
- **Password Hashing**: Django pbkdf2_sha256 algorithm
- **SQL Injection**: ORM parameterized queries
- **XSS Protection**: Django template auto-escaping
- **Rate Limiting**: (Optional) API rate limiting
- **Permissions**: Custom decorators for authorization

### User Authentication Flow

```
1. User visits site
   ↓
2. Check if already authenticated
   ├─ Yes: Load dashboard
   └─ No: Show login/register page
   ↓
3. User chooses auth method
   ├─ Email OTP:
   │  ├─ Enter email
   │  ├─ Receive OTP
   │  ├─ Verify OTP
   │  └─ Create account / Login
   │
   └─ Social OAuth:
      ├─ Click "Login with Google"
      ├─ Grant permission
      └─ Auto-create/link account
   ↓
4. System creates session
   ├─ Store in Django session table
   ├─ Set session cookie
   └─ Redirect to dashboard
   ↓
5. User logged in
   ├─ @login_required views accessible
   ├─ User data available in request.user
   └─ CSRF token available for forms
```

---

## FRONTEND IMPLEMENTATION

### Template Structure

**Base Template** (base.html)
```html
<html>
  <head>
    <!-- Meta tags, CSS, favicon -->
    {% block extra_head %}{% endblock %}
  </head>
  <body>
    <!-- Navigation -->
    {% include "navbar.html" %}
    
    <!-- Messages/Alerts -->
    {% if messages %}
      {% for message in messages %}
        <div class="alert alert-{{ message.tags }}">
          {{ message }}
        </div>
      {% endfor %}
    {% endif %}
    
    <!-- Content Block -->
    {% block content %}{% endblock %}
    
    <!-- JavaScript -->
    <script src="{% static 'js/realtime-updates.js' %}"></script>
    {% block extra_js %}{% endblock %}
    
    <!-- Initialize Real-time Updates -->
    <script>
      document.addEventListener('DOMContentLoaded', () => {
        const realtime = new RealtimeUpdates();
        realtime.init();
      });
    </script>
  </body>
</html>
```

### Dynamic Content with AJAX

**Example: Like Project (AJAX)**
```javascript
function likeProject(projectId) {
    const csrfToken = document.querySelector('[name=csrfmiddlewaretoken]').value;
    
    fetch(`/api/projects/${projectId}/like/`, {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
            'X-CSRFToken': csrfToken
        },
        body: JSON.stringify({ action: 'like' })
    })
    .then(response => response.json())
    .then(data => {
        // Update UI
        document.querySelector(`#like-count-${projectId}`).textContent = data.like_count;
    })
    .catch(error => console.error('Error:', error));
}
```

### WebSocket Integration in Template

```html
<!-- Project Detail Page -->
{% block content %}
<div id="project-{{ project.id }}">
    <h1>{{ project.title }}</h1>
    <p>Status: <span id="project-status">{{ project.status }}</span></p>
    <div id="comments-section">
        <!-- Comments loaded via AJAX -->
    </div>
</div>

<script>
// Real-time updates automatically handled by realtime-updates.js
// When server broadcasts update:
// 1. WebSocket consumer sends message
// 2. JavaScript onmessage handler calls updateProjectUI()
// 3. DOM elements updated without page reload
</script>
{% endblock %}
```

### Static Files Organization

```
static/
├── js/
│   ├── realtime-updates.js      # WebSocket client
│   ├── api-utils.js              # Shared API utilities
│   ├── login.js                  # Authentication UI
│   ├── messages-handler.js        # Message UI logic
│   ├── comments-handler.js        # Comments UI logic
│   └── profile.js                # Profile page logic
│
├── css/
│   ├── style.css                 # Main stylesheet
│   ├── responsive.css            # Mobile/responsive
│   └── components.css            # Component styles
│
└── images/
    ├── logo.png
    ├── favicon.ico
    └── placeholders/
```

---

## CODE QUALITY & PATTERNS

### Design Patterns Used

1. **Model-View-Template (MVT)**
   - Django standard architecture
   - Clear separation of concerns

2. **Asynchronous Consumer Pattern** (WebSocket)
   - `AsyncWebsocketConsumer` for non-blocking I/O
   - `database_sync_to_async` for database access

3. **Service Layer Pattern**
   - Utility functions in `utils.py`
   - Business logic separated from views

4. **Signal Pattern**
   - Django signals for post-save hooks
   - Decoupled event handling

5. **Factory Pattern**
   - OTP generation
   - Notification creation

### Naming Conventions

| Type | Convention | Example |
|------|-----------|---------|
| Models | PascalCase | `StudentProfile`, `ProjectTask` |
| Functions | snake_case | `get_user_projects()` |
| Classes | PascalCase | `RealtimeUpdates` |
| Constants | UPPERCASE | `MAX_RECONNECT_ATTEMPTS` |
| URLs | kebab-case | `/project-detail/` |
| Templates | snake_case.html | `project_detail.html` |
| CSS classes | kebab-case | `.project-card` |

### Code Organization

**Views (accounts/views.py)**
- ~3400+ lines
- Organized by feature
- Clear function/view documentation
- Error handling decorators

**Models (accounts/models.py)**
- ~720+ lines
- 15+ model classes
- Proper relationships and constraints
- Custom methods and properties

**Consumers (accounts/consumers.py)**
- ~450+ lines
- 3 main consumer classes
- Async/await patterns
- Group broadcasting

**Utils (accounts/utils.py)**
- NLP-based recommendations
- Visibility filtering
- Email utilities

### Error Handling

**Try-Except Pattern**
```python
@login_required
def view_project_detail(request, project_id):
    try:
        project = Project.objects.get(id=project_id)
        # ... process project
    except Project.DoesNotExist:
        messages.error(request, 'Project not found')
        return redirect('main_home')
    except Exception as e:
        logger.error(f'Error: {str(e)}')
        messages.error(request, 'An error occurred')
        return redirect('main_home')
```

**Decorator Pattern**
```python
def handle_view_errors(view_func):
    """Decorator to handle exceptions in views"""
    def wrapper(request, *args, **kwargs):
        try:
            return view_func(request, *args, **kwargs)
        except Exception as e:
            logger.error(f'Error: {str(e)}')
            messages.error(request, 'An error occurred')
            return redirect('main_home')
    return wrapper
```

### Testing Structure

**Test Files** (test_*.py)
- test_login.py: Authentication tests
- test_comments_api.py: Comment API tests
- test_profile_view.py: Profile view tests
- test_email.py: Email service tests
- test_connections.py: Connection tests

**Test Patterns**
```python
from django.test import TestCase
from .models import User, Project

class ProjectTestCase(TestCase):
    def setUp(self):
        """Set up test data"""
        self.user = User.objects.create_user(
            username='testuser',
            email='test@test.com'
        )
    
    def test_project_creation(self):
        """Test project can be created"""
        project = Project.objects.create(
            owner=self.user,
            title='Test Project'
        )
        self.assertEqual(project.title, 'Test Project')
```

---

## DEPLOYMENT & CONFIGURATION

### Environment Setup

**Development (Local)**
```bash
cd e:\login\auth_project
python -m venv venv
source venv/Scripts/activate  # Windows: venv\Scripts\activate
pip install -r requirements.txt
python manage.py migrate
python manage.py runserver
```

**WebSocket (Local Testing)**
```bash
# Install Daphne
pip install daphne==4.0.0

# Run Daphne instead of runserver
daphne -b 127.0.0.1 -p 8000 auth_project.asgi:application
```

### Production Deployment

**Docker (Recommended)**
```dockerfile
FROM python:3.11
WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY . .
CMD ["daphne", "-b", "0.0.0.0", "-p", "8000", "auth_project.asgi:application"]
```

**Render/Railway Deployment**
- Procfile: `web: daphne -b 0.0.0.0 -p $PORT auth_project.asgi:application`
- Database: PostgreSQL on Render/Railway
- Environment Variables: Set in dashboard
- Static files: Collected via `python manage.py collectstatic`

### Configuration Files

**Procfile**
```
web: daphne -b 0.0.0.0 -p $PORT auth_project.asgi:application
```

**railway.json / render.yaml**
```yaml
services:
  web:
    build: .
    environment:
      - DATABASE_URL
      - SECRET_KEY
    ports:
      - 8000
```

**.env (Development)**
```
DEBUG=True
SECRET_KEY=dev-secret-key
DATABASE_URL=sqlite:///db.sqlite3
ALLOWED_HOSTS=localhost,127.0.0.1
BREVO_API_KEY=...
ZEPTO_API_KEY=...
GOOGLE_OAUTH_ID=...
GITHUB_OAUTH_ID=...
```

### Static Files Management

**Collection for Production**
```bash
python manage.py collectstatic --noinput
```

**Serving Static Files**
- Development: Django development server
- Production: WhiteNoise or separate CDN (S3)

---

## PERFORMANCE CONSIDERATIONS

### Database Optimization

1. **Indexing**
   - Foreign keys automatically indexed
   - Add indexes on frequently queried fields

2. **Query Optimization**
   - Use `select_related()` for forward FK
   - Use `prefetch_related()` for reverse FK and M2M
   - Avoid N+1 queries

3. **Caching**
   - Django cache framework
   - Cache user profiles
   - Cache project lists
   - Cache API responses

### Frontend Performance

1. **Static Assets**
   - Minify CSS/JavaScript
   - Use CDN for distribution
   - Browser caching headers

2. **JavaScript**
   - Vanilla JS (no jQuery overhead)
   - Async/await for cleaner async code
   - Event delegation for dynamic content

3. **WebSocket Efficiency**
   - Only broadcast relevant updates
   - Batch updates when possible
   - Close connections gracefully

### Scaling Strategies

1. **Database**
   - Read replicas for reports
   - Connection pooling
   - Query optimization

2. **Application**
   - Multiple Daphne instances
   - Load balancing
   - Sticky sessions for WebSocket

3. **Caching**
   - Redis for session storage
   - Redis for cache backend
   - Cache WebSocket broadcast data

---

## KNOWN ISSUES & FIXES

### 1. WebSocket 404 Errors

**Problem**
```
[WARNING] Not Found: /ws/project/2/
[WARNING] "GET /ws/project/2/ HTTP/1.1" 404 9033
```

**Root Cause**
- Using `python manage.py runserver` (HTTP only)
- Daphne not running (handles WebSocket)

**Solution**
```bash
# Install Daphne
pip install daphne==4.0.0

# Run Daphne instead
daphne -b 127.0.0.1 -p 8000 auth_project.asgi:application
```

### 2. CSRF Token Issues

**Problem**
- 403 Forbidden on POST requests
- "CSRF token missing or incorrect"

**Solution**
- Include CSRF token in form: `{% csrf_token %}`
- Include in AJAX headers:
```javascript
const csrfToken = document.querySelector('[name=csrfmiddlewaretoken]').value;
fetch(url, {
    method: 'POST',
    headers: { 'X-CSRFToken': csrfToken }
})
```

### 3. Email Sending Failures

**Problem**
- OTP not arriving
- Email configuration errors

**Solution**
- Verify Brevo/Zepto API keys in .env
- Check email backend in settings.py
- Test with: `python manage.py shell` → `from accounts.utils import send_otp_email`

### 4. Profile Picture Not Displaying

**Problem**
- Image upload works, but not visible in templates

**Solution**
```html
<!-- In templates, use full URL -->
<img src="{{ user.student_profile.profile_photo.url }}" alt="Profile">

<!-- Or in settings.py, ensure: -->
MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')
```

### 5. Comments Not Loading

**Problem**
- Comments API returns empty list
- Comments section blank

**Solution**
- Check `/accounts/projects/2/comments/` endpoint
- Verify Comment model exists in database
- Check template includes comment form

### 6. Real-time Features Not Working

**Problem**
- WebSocket connections failing
- No real-time updates

**Solution**
1. Ensure Daphne running: `daphne -b 0.0.0.0 -p 8000 auth_project.asgi:application`
2. Check routing.py has correct patterns
3. Verify consumers.py has proper async handlers
4. Check browser console for JS errors
5. Test with browser console:
```javascript
const socket = new WebSocket("ws://localhost:8000/ws/project/2/");
socket.onopen = () => console.log("Connected!");
```

---

## SUMMARY TABLE

| Component | Files | Status | Notes |
|-----------|-------|--------|-------|
| **Models** | models.py | ✅ Complete | 15+ models, full schema |
| **Views** | views.py | ✅ Complete | 50+ endpoints, tested |
| **URLs** | urls.py | ✅ Complete | All routes defined |
| **Authentication** | forms.py, utils.py | ✅ Complete | OTP + Social OAuth |
| **WebSocket** | consumers.py, routing.py | ✅ Complete | Requires Daphne |
| **Frontend** | templates/ | ✅ Complete | Django templates |
| **JavaScript** | static/js/ | ✅ Complete | Real-time handlers |
| **REST API** | serializers.py | ✅ Complete | Full API coverage |
| **Database** | PostgreSQL/SQLite | ✅ Production Ready | Migrations applied |
| **Email** | Brevo/Zepto | ✅ Configured | Requires API key |
| **Tests** | test_*.py | ✅ Available | Example test files |
| **Documentation** | This file | ✅ Complete | Comprehensive guide |

---

## QUICK REFERENCE

### Start Development Server
```bash
python manage.py runserver
```

### Start WebSocket Server
```bash
daphne -b 127.0.0.1 -p 8000 auth_project.asgi:application
```

### Create Superuser
```bash
python manage.py createsuperuser
```

### Run Migrations
```bash
python manage.py makemigrations
python manage.py migrate
```

### Collect Static Files
```bash
python manage.py collectstatic --noinput
```

### Run Tests
```bash
python manage.py test
# or
pytest
```

### Shell Access
```bash
python manage.py shell
```

---

## CONTACT & SUPPORT

**Project Repository**: https://github.com/Goku0090/uni

**Documentation Location**: `/e:/login/` (root directory)

**Key Documentation Files**:
- 00_WEBSOCKET_FIX_START_HERE.md
- WEBSOCKET_DETAILED_ANALYSIS.md
- COMPREHENSIVE_CODE_ANALYSIS_2026_FINAL.md

---

**Document Generated**: February 7, 2026
**Status**: Production Ready ✅
**Last Updated By**: Code Analysis System
**Version**: 2.0
