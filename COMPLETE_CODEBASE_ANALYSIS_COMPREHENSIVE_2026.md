# 🏗️ Complete Codebase Analysis - Unisinq Platform
**Generated:** Feb 09, 2026 | **Status:** Comprehensive | **Type:** Social Collaboration Platform

---

## 📊 Executive Summary

**Unisinq** is a Django-based social collaboration platform enabling students to:
- **Create & share projects** with collaborative features
- **Find collaborators** through advanced skill matching (NLP-based)
- **Real-time communication** via WebSocket (live project updates, messages, notifications)
- **Project management** with tasks, milestones, team roles
- **Social features** (connections, followers, likes, comments, activity feed)
- **Multi-channel authentication** (Email OTP, Google OAuth, GitHub OAuth)

---

## 🗂️ Project Structure

```
auth_project/
├── auth_project/              # Django project settings & config
│   ├── settings.py            # Complete Django configuration
│   ├── urls.py                # Main URL routing
│   ├── asgi.py                # WebSocket/ASGI config
│   └── wsgi.py                # WSGI application
│
├── accounts/                  # Main application
│   ├── models.py              # 20+ database models
│   ├── views.py               # 60+ view functions (3400+ lines)
│   ├── serializers.py         # REST API serializers
│   ├── urls.py                # API routing
│   ├── forms.py               # Django forms
│   ├── consumers.py           # WebSocket consumers
│   ├── routing.py             # WebSocket routing
│   ├── signals_realtime.py    # Django signals
│   ├── permissions.py         # Custom permissions
│   ├── utils.py               # Helper utilities
│   ├── comment_api.py         # Comment endpoints
│   ├── chat_api.py            # Chat endpoints
│   ├── zepto_mail_backend.py  # Email backend
│   ├── brevo_mail_backend.py  # Email backend
│   ├── static/                # Frontend JS & CSS
│   └── templates/             # HTML templates
│
├── static/                    # Global static files
│   └── js/
│       ├── realtime-updates.js    # WebSocket client
│       ├── comments-handler.js    # Comment UI logic
│       ├── messages-ui.js         # Messaging UI
│       └── api-utils.js           # API helper functions
│
├── media/                     # User uploads (images, files)
├── logs/                      # Application logs
├── db.sqlite3                 # Development database
└── requirements.txt           # Python dependencies
```

---

## 🗄️ Database Models (20+)

### Core User Models
| Model | Purpose | Key Fields |
|-------|---------|-----------|
| **User** (Django) | Authentication & authorization | username, email, password |
| **StudentProfile** | Extended user profile | full_name, college, bio, profile_photo, skills, interests |
| **OTP** | One-time passwords | email, otp_code, purpose, expires_at |
| **Connection** | User connections/requests | sender, receiver, status (pending/accepted/rejected) |
| **Follow** | User followers system | follower, following |
| **UserStatus** | Online/offline status | user, status, updated_at |

### Project Models
| Model | Purpose | Key Fields |
|-------|---------|-----------|
| **Project** | Main project entity | title, description, owner, category, visibility, likes_count |
| **ProjectMember** | Team members with roles | project, user, role (owner/admin/contributor/viewer) |
| **ProjectTask** | Project tasks | title, status (todo/in_progress/review/completed), assigned_to, due_date |
| **ProjectMilestone** | Project milestones | title, is_completed, due_date |
| **ProjectTeam** | Alias for ProjectMember | (backward compatibility) |
| **ProjectInvitation** | Team invitations | project, invited_user, status, expires_at |

### Social & Communication Models
| Model | Purpose | Key Fields |
|-------|---------|-----------|
| **Comment** | Project/activity comments | user, project, content, created_at |
| **Like** | Project likes | user, project, created_at |
| **Message** | Direct messages | sender, receiver, chat_room, content, message_type |
| **ChatRoom** | Group chat rooms | name, chat_type (direct/group), members |
| **ChatRoomMember** | Chat participants | chat_room, user, is_active |
| **MessageReadStatus** | Message read tracking | message, user, read_at |
| **MessageReaction** | Emoji reactions | message, user, reaction |
| **Activity** | Activity feed | user, activity_type, project, created_at |
| **Notification** | User notifications | user, title, content, is_read, notification_type |

### Utility Models
| Model | Purpose | Key Fields |
|-------|---------|-----------|
| **File** | File uploads in chat | user, file, filename, file_size |
| **MessageFile** | Message attachments | message, file, uploaded_at |
| **UserStats** | User statistics | projects_created, connections_made, likes_received, etc. |

---

## 🔄 Data Flow Architecture

### 1. Authentication Flow
```
Login Request
    ↓
[email/username + password] → Views: login_view()
    ↓
[Option A: Email OTP]
  - Generate OTP → OTP model
  - Send via Brevo/ZeptoMail
  - User verifies in verify_otp_view()
    ↓
[Option B: Google OAuth]
  - Redirect to Google
  - Callback to allauth
  - Auto-create StudentProfile via signal
    ↓
Session Created → User logged in
```

### 2. Project Creation Flow
```
User submits ProjectForm
    ↓
post_project() view validates
    ↓
Project.objects.create(owner=user)
    ↓
Signal triggered: auto_update_stats()
    ↓
Activity.objects.create(type='project_created')
    ↓
WebSocket broadcast to ActivityFeedConsumer
    ↓
All connected clients receive notification
```

### 3. Real-Time Updates (WebSocket)
```
Client connects: new WebSocket("ws://localhost:8000/ws/project/1/")
    ↓
ProjectUpdateConsumer.connect()
    ↓
Joins group: project_1
    ↓
On project change (via signal):
  - async_to_sync(channel_layer.group_send)()
  - Consumer receives: project_status_update event
  - Sends JSON to client
    ↓
Client JavaScript: receive message → Update DOM
```

### 4. Comment Workflow
```
User posts comment on project
    ↓
comment_api.py: CommentCreateAPIView
    ↓
[Save to DB]
Comment.objects.create(user, project, content)
    ↓
[Trigger Signal]
signals_realtime.py: auto_update_stats()
    ↓
[Send WebSocket]
ActivityFeedConsumer broadcasts to all clients
    ↓
[Update Page]
comments-handler.js: render new comment
```

---

## 🔌 API Endpoints Reference

### Authentication
| Method | Endpoint | Purpose |
|--------|----------|---------|
| POST | `/register/` | User registration |
| POST | `/login/` | Email/password login |
| POST | `/verify-otp/<purpose>/` | Verify OTP |
| POST | `/forgot-password/` | Initiate password reset |
| GET | `/logout/` | User logout |
| GET | `/accounts/google/login/` | Google OAuth |

### Projects
| Method | Endpoint | Purpose |
|--------|----------|---------|
| POST | `/post-project/` | Create new project |
| GET | `/project/<id>/` | View project details |
| PUT | `/api/project/<id>/update/` | Update project |
| DELETE | `/delete-project/<id>/` | Delete project |
| GET | `/my-projects/` | User's projects |
| GET | `/explore-projects/` | Browse all projects |
| POST | `/api/project/<id>/members/` | Add team member |

### Comments
| Method | Endpoint | Purpose |
|--------|----------|---------|
| POST | `/api/comments/create/` | Create comment |
| GET | `/api/comments/<project_id>/` | Get project comments |
| DELETE | `/api/comments/<id>/delete/` | Delete comment |

### Messages & Chat
| Method | Endpoint | Purpose |
|--------|----------|---------|
| GET | `/messages/` | Message inbox |
| GET | `/chat/<user_id>/` | Open direct chat |
| POST | `/api/messages/send/` | Send message |
| PUT | `/api/messages/<id>/read/` | Mark as read |
| POST | `/api/chat/group/create/` | Create group chat |

### User Profile & Connections
| Method | Endpoint | Purpose |
|--------|----------|---------|
| GET | `/profile/` | User profile page |
| PUT | `/api/profile/update/` | Update profile |
| POST | `/connect/<user_id>/` | Send connection request |
| PUT | `/accept-connection/<id>/` | Accept request |
| GET | `/my-connections/` | View connections |
| GET | `/find-collaborators/` | Find collaborators (with filtering) |

### Activity & Notifications
| Method | Endpoint | Purpose |
|--------|----------|---------|
| GET | `/notifications/` | User notifications |
| GET | `/api/activity/feed/` | Activity feed |
| PUT | `/notification/<id>/read/` | Mark notification read |

---

## 🚀 Key Features Deep Dive

### 1. Advanced Skill Matching (NLP)
**File:** `accounts/utils.py` - `StudentProfileNLP` class

```python
class StudentProfileNLP:
    """
    NLP-based skill matching for finding collaborators
    - Extracts skills/interests from user profile
    - Uses similarity scoring (TF-IDF, cosine similarity)
    - Filters by college, role preference
    """
    
    def extract_interests(profile) → list
    def match_collaborators(user, limit=10) → QuerySet
    def calculate_compatibility_score(user1, user2) → float
```

**Usage:** `/find-collaborators/` view uses this to recommend compatible users.

### 2. Real-Time WebSocket System
**Files:** `accounts/consumers.py`, `accounts/routing.py`

**Three WebSocket Consumers:**
1. **ProjectUpdateConsumer** - Live project status changes
2. **ActivityFeedConsumer** - Activity feed updates
3. **NotificationConsumer** - Real-time notifications

**Usage Example:**
```javascript
// Client-side (realtime-updates.js)
let socket = new WebSocket("ws://localhost:8000/ws/project/2/");
socket.onopen = () => console.log("Connected to project updates");
socket.onmessage = (event) => {
    let data = JSON.parse(event.data);
    updateProjectUI(data);
};
```

### 3. Multi-Channel Email System
**Files:** `brevo_mail_backend.py`, `zepto_mail_backend.py`

**Priority:** Brevo (Primary) → ZeptoMail → Gmail SMTP → Console (Development)

```python
# settings.py determines email backend
if BREVO_API_KEY:
    EMAIL_BACKEND = 'accounts.brevo_mail_backend.BrevoMailBackend'
elif ZEPTO_MAIL_API_KEY:
    EMAIL_BACKEND = 'accounts.zepto_mail_backend.ZeptoMailBackend'
```

### 4. Project Visibility & Permissions
**File:** `accounts/utils.py` - `ProjectVisibilityFilter` class

```python
class ProjectVisibilityFilter:
    """
    Controls project visibility and access:
    - Public: visible to all
    - Private: only owner & members
    - Draft: only owner
    """
    
    def filter_projects(user) → QuerySet
    def can_view_project(user, project) → bool
    def can_edit_project(user, project) → bool
```

### 5. Django Signals for Real-Time Updates
**File:** `signals_realtime.py`

**Key Signals:**
- `post_save(User)` → Auto-create StudentProfile
- `post_save(Project)` → Update UserStats, create Activity
- `post_save(Comment)` → Broadcast to WebSocket
- `post_save(Message)` → Update read status

---

## 🔐 Security & Authentication

### 1. CSRF Protection
- ✅ Enabled in `settings.py`: `CsrfViewMiddleware`
- CSRF tokens required for POST/PUT/DELETE
- Validated in forms and AJAX requests

### 2. Permission Classes
**File:** `permissions.py`

```python
class IsOwnerOrReadOnly
class IsProjectMember
class IsCommentAuthor
class CanInviteToProject
```

### 3. OAuth Providers
- **Google:** `allauth.socialaccount.providers.google`
- **GitHub:** `allauth.socialaccount.providers.github`

### 4. OTP-Based Authentication
- 6-digit OTP, 5-minute expiry
- Sent via Brevo/ZeptoMail
- Purpose-based (login, registration, password reset)

---

## 📱 Frontend Components

### Key JavaScript Files

| File | Purpose | Key Functions |
|------|---------|---------------|
| `realtime-updates.js` | WebSocket client | Connects to ws://, handles messages, updates DOM |
| `comments-handler.js` | Comment UI logic | Post, delete, render comments |
| `messages-ui.js` | Messaging interface | Send/receive messages, read status |
| `api-utils.js` | API helpers | fetch() wrappers, error handling |
| `login.js` | Login form logic | Validation, OTP handling |
| `profile.js` | Profile page logic | Upload avatar, edit profile |

### Key Templates

| Template | Purpose |
|----------|---------|
| `main_home.html` | Homepage with project feed |
| `project_detail.html` | Single project page + comments |
| `messages.html` | Messaging interface |
| `profile.html` | User profile page |
| `find_collaborators.html` | Collaborator discovery |
| `my_projects.html` | User's projects list |

---

## 🔧 Configuration & Environment

### Required Environment Variables
```bash
# Django
DEBUG=True
SECRET_KEY=your-secret-key-here
ALLOWED_HOSTS=localhost,127.0.0.1

# Database
DATABASE_URL=postgresql://user:pass@localhost/dbname
# OR
DB_NAME=unisinq_db
DB_USER=unisinq_user
DB_PASSWORD=password
DB_HOST=localhost
DB_PORT=5432

# Email
BREVO_API_KEY=your-brevo-api-key  # Primary
ZEPTO_MAIL_API_KEY=your-zepto-key  # Alternative
EMAIL_HOST_USER=your-email@gmail.com
EMAIL_HOST_PASSWORD=app-password

# OAuth
GOOGLE_CLIENT_ID=your-google-client-id
GOOGLE_CLIENT_SECRET=your-google-secret
GITHUB_CLIENT_ID=your-github-client-id
GITHUB_CLIENT_SECRET=your-github-secret

# RapidAPI (for university list)
RAPIDAPI_KEY=your-rapidapi-key
```

### Key Settings
```python
# settings.py highlights:
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'accounts',  # Main app
    'allauth',   # Authentication
    'rest_framework',  # API
]

CHANNEL_LAYERS = {
    'default': {
        'BACKEND': 'channels.layers.InMemoryChannelLayer'
    }
}

REST_FRAMEWORK = {
    'DEFAULT_PERMISSION_CLASSES': ['rest_framework.permissions.AllowAny'],
    'DEFAULT_PAGINATION_CLASS': 'rest_framework.pagination.PageNumberPagination',
    'PAGE_SIZE': 10,
}
```

---

## 📊 Data Statistics Models

### UserStats Model
Tracks per-user metrics:
```python
class UserStats:
    projects_created: int
    connections_made: int
    likes_received: int
    comments_made: int
    followers_count: int
    following_count: int
    last_updated: DateTime
```

**Updated by signals** whenever activities occur.

---

## 🔗 Key Relationships

### User → Projects
```
User (1) ←→ (∞) Project (owner)
User (∞) ←→ (∞) Project (members via ProjectMember)
```

### Project → Team
```
Project (1) ←→ (∞) ProjectMember
ProjectMember has roles: owner, admin, contributor, viewer
```

### User → User Social
```
User (1) ←→ (∞) Connection (sender/receiver)
User (1) ←→ (∞) Follow (follower/following)
User (1) ←→ (∞) Message (sender/receiver)
User (1) ←→ (∞) ChatRoom (members)
```

### Project → Content
```
Project (1) ←→ (∞) Comment
Project (1) ←→ (∞) Like
Project (1) ←→ (∞) Activity
```

---

## 🐛 Known Issues & Fixes Applied

### Recent Fixes
1. ✅ **CSRF Token Warnings** - Fixed in forms, added {% csrf_token %} to all POST forms
2. ✅ **Comments Not Visible** - Fixed signal broadcasting to all clients
3. ✅ **Like Button State** - Fixed caching issue, proper read/write of Like model
4. ✅ **Project Owner Attribute Error** - Fixed inconsistent owner field access
5. ✅ **WebSocket Connection Errors** - Fixed consumer routing and channel layer config
6. ✅ **Profile Photo Not Displaying** - Fixed media URL configuration

---

## 🚀 Deployment Ready

### Render Deployment
- ✅ Uses PostgreSQL (DATABASE_URL)
- ✅ Static files collected in `staticfiles/`
- ✅ Email configured with Brevo
- ✅ WebSocket support (ASGI)
- ✅ Environment variables via .env

### Production Checklist
- [ ] Set `DEBUG=False`
- [ ] Generate new `SECRET_KEY`
- [ ] Configure `ALLOWED_HOSTS`
- [ ] Enable SSL: `SECURE_SSL_REDIRECT=True`
- [ ] Configure secure cookies
- [ ] Set up proper email backend
- [ ] Run migrations
- [ ] Collect static files: `python manage.py collectstatic`

---

## 📈 Performance Optimizations

### Implemented
- ✅ User count caching in stats models
- ✅ Pagination for project lists (10 per page)
- ✅ Database query optimization (select_related, prefetch_related)
- ✅ Project visibility filtering (avoid N+1 queries)
- ✅ WebSocket for real-time (instead of polling)

### Recommended
- [ ] Add Redis for caching
- [ ] Use database indexing on frequently filtered fields
- [ ] Implement lazy loading for images
- [ ] Add CDN for static files
- [ ] Use async views for long-running tasks

---

## 🧪 Testing

### Test Files Present
- `test_login.py` - Authentication tests
- `test_comments_api.py` - Comment endpoint tests
- `test_profile_view.py` - Profile view tests
- `test_email.py` - Email backend tests

---

## 📚 Technologies Stack

| Layer | Technologies |
|-------|--------------|
| **Backend** | Django 3.x, Django REST Framework, Channels |
| **Frontend** | HTML5, Bootstrap, Vanilla JavaScript, WebSocket |
| **Database** | PostgreSQL (prod), SQLite (dev) |
| **Email** | Brevo API, ZeptoMail, Gmail SMTP |
| **Authentication** | django-allauth, OTP |
| **Deployment** | Render, Gunicorn, ASGI |

---

## 🎯 Next Steps / Improvements

1. **Add Redis** for WebSocket scaling & caching
2. **Implement Search** with Elasticsearch or database FTS
3. **Add Notifications** email digests for activity
4. **Project Analytics** - views count, engagement metrics
5. **Advanced Permissions** - granular role-based access
6. **File Uploads** - s3 integration for media files
7. **Rate Limiting** - prevent abuse
8. **Full-Text Search** - across projects & comments

---

## 📖 File Reference Quick Links

- **Main Config:** `auth_project/settings.py` (363 lines)
- **URL Routing:** `auth_project/urls.py` (61 lines)
- **Models:** `accounts/models.py` (718 lines)
- **Views:** `accounts/views.py` (3400+ lines)
- **WebSocket:** `accounts/consumers.py` (434 lines)
- **Signals:** `accounts/signals_realtime.py`
- **Serializers:** `accounts/serializers.py`
- **Forms:** `accounts/forms.py`

---

**End of Analysis** | Last Updated: Feb 09, 2026
