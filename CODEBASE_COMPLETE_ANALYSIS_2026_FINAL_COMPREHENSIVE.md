# Complete Codebase Analysis - UniSync Platform 2026

## Executive Summary

**UniSync** is a full-stack collaborative platform built with Django (backend) and React (frontend). It enables university students to discover, manage, and collaborate on projects in real-time. The application features OAuth authentication, WebSocket-powered real-time communication, and advanced project management capabilities.

---

## 1. Technology Stack Overview

### Backend
- **Framework**: Django 4.2.8 with Django REST Framework 3.14.0
- **Real-time**: Django Channels 4.0.0 with Redis 5.0.1
- **Authentication**: django-allauth 0.61.1 (OAuth2 + Email/OTP)
- **Database**: PostgreSQL (via psycopg2-binary)
- **Cache**: Redis 5.0.1
- **Server**: Gunicorn with WhiteNoise for static files
- **API Documentation**: drf-spectacular 0.26.5
- **Security**: Cryptography, CSRF protection

### Frontend
- **Framework**: React 18.2.0
- **Build Tool**: Vite 5.0.0
- **HTTP Client**: Axios 1.6.0
- **Routing**: React Router DOM 6.20.0
- **Development**: Node.js with npm

### External Services
- **Email**: Brevo SMTP (via custom backend)
- **OAuth Providers**: Google OAuth, GitHub OAuth
- **WebSocket**: Django Channels with Redis broker

---

## 2. Directory Structure

```
project-root/
├── backend/
│   ├── auth_project/                 # Django project settings
│   │   ├── settings.py              # Configuration (DB, cache, auth, apps)
│   │   ├── urls.py                  # Main URL routing
│   │   ├── asgi.py                  # WebSocket config
│   │   ├── wsgi.py                  # WSGI application
│   │   └── __init__.py
│   │
│   ├── accounts/                     # Main app
│   │   ├── models.py                # Database models (User, Project, etc.)
│   │   ├── views.py                 # View functions & class-based views
│   │   ├── serializers.py           # DRF serializers
│   │   ├── urls.py                  # App URL routing
│   │   ├── forms.py                 # Django forms
│   │   │
│   │   ├── API Layer/
│   │   │   ├── chat_api.py          # Chat endpoints
│   │   │   ├── chat_api_improved.py # Enhanced chat
│   │   │   ├── comment_api.py       # Comments endpoints
│   │   │   └── template_api.py      # Project templates
│   │   │
│   │   ├── WebSocket Layer/
│   │   │   ├── consumers.py         # WebSocket consumers
│   │   │   ├── routing.py           # WebSocket routing
│   │   │   └── signals_realtime.py  # Real-time signals
│   │   │
│   │   ├── Utils & Services/
│   │   │   ├── utils.py             # Helper functions
│   │   │   ├── permissions.py       # Permission classes
│   │   │   ├── services/            # Business logic
│   │   │   └── brevo_mail_backend.py # Email backend
│   │   │
│   │   ├── Django Internals/
│   │   │   ├── migrations/          # Database migrations
│   │   │   ├── management/          # Custom commands
│   │   │   ├── static/              # Static assets
│   │   │   ├── templates/           # HTML templates
│   │   │   └── templatetags/        # Custom template tags
│   │   │
│   │   └── Meta Files/
│   │       ├── apps.py              # App configuration
│   │       ├── tests.py             # Test suite
│   │       └── __init__.py
│   │
│   ├── docker/                       # Docker configuration
│   ├── logs/                         # Application logs
│   ├── media/                        # User uploads
│   ├── static/                       # Static files
│   ├── staticfiles/                  # Collected static files
│   ├── manage.py                     # Django CLI
│   ├── requirements.txt              # Python dependencies
│   ├── Procfile                      # Deployment config
│   └── db.sqlite3                    # Development database
│
├── frontend/
│   ├── src/
│   │   ├── api/                      # API client utilities
│   │   ├── App.jsx                   # Main App component
│   │   ├── main.jsx                  # React entry point
│   │   ├── App.css                   # Global styles
│   │   └── index.css                 # Reset styles
│   │
│   ├── index.html                    # HTML entry point
│   ├── vite.config.js                # Vite configuration
│   ├── package.json                  # Dependencies
│   ├── Dockerfile                    # Container config
│   └── nginx.conf                    # Web server config
│
├── docker-compose.yml                # Local dev orchestration
├── Dockerfile                        # Production Docker image
├── render.yaml                       # Render.com deployment config
└── .gitignore
```

---

## 3. Core Models & Database Schema

### User & Authentication
```
User (Django Auth)
├─ username, email, password
├─ first_name, last_name
└─ is_active, is_staff, date_joined

StudentProfile (1-to-1 with User)
├─ full_name, college, location
├─ interests, skills, project_interests (JSON)
├─ bio, profile_photo
├─ github, linkedin, portfolio, behance (social links)
├─ role_preference
└─ profile_completed, timestamps

OTP
├─ email, otp_code
├─ purpose (login/registration/reset)
├─ is_used, created_at, expires_at
└─ Methods: generate_otp(), verify_otp(), is_valid()
```

### Collaboration & Connections
```
Project
├─ owner, title, description
├─ status, visibility (public/private)
├─ skills_required, collaboration_needs (JSON)
├─ budget, timeline
├─ tags, category
├─ members, attachments
├─ created_at, updated_at
└─ Methods: add_member(), remove_member()

Connection
├─ sender, receiver (ForeignKey User)
├─ status (pending/accepted/rejected)
├─ created_at, updated_at
└─ Unique constraint: (sender, receiver)

ProjectTeam
├─ project, name, description
├─ team_type (core/collaborators)
├─ created_by, created_at
└─ members through ProjectTeamMember

ProjectTeamMember
├─ team, user, role
├─ joined_at
└─ Methods: promote(), demote()

ProjectTeamInvitation
├─ team, invited_user, invited_by
├─ status, created_at
└─ Methods: accept(), reject()
```

### Communication
```
Message
├─ sender, receiver
├─ content, created_at
├─ is_read, read_at
├─ attachment_count
└─ Relationships: MessageFile, MessageReaction

ChatRoom
├─ name, description, is_group
├─ members (ManyToMany)
├─ created_by, created_at
└─ Methods: add_member(), remove_member()

ChatRoomMember
├─ room, user, joined_at

Comment
├─ user, project (ForeignKey)
├─ content, timestamp
├─ likes_count, replies (self-referential)

MessageReadStatus
├─ message, user
├─ read_at
└─ Unique constraint: (message, user)
```

### Activity & Engagement
```
Activity
├─ user, action_type
├─ project, related_model
├─ description, timestamp
└─ is_public

Like
├─ user, project
├─ created_at
└─ Unique constraint: (user, project)

Follow
├─ follower, followee (User)
├─ created_at

UserStatus
├─ user, status, updated_at
└─ Status: online/offline/idle

Notification
├─ user, actor, action_type
├─ related_model, is_read
├─ created_at

UserStats
├─ user, projects_created, projects_joined
├─ connections_count, followers_count
└─ updated_at
```

### File Management
```
File
├─ project, uploaded_by
├─ file, filename, filesize
├─ uploaded_at

MessageFile
├─ message, file

ProjectTask
├─ project, title, description
├─ assigned_to, status, priority
├─ deadline, created_at

ProjectMilestone
├─ project, title, description
├─ target_date, completed_at
└─ progress_percentage
```

---

## 4. Backend Architecture

### 4.1 Django Configuration (settings.py)

**Key Settings:**
- **Debug Mode**: Controlled by `DEBUG` env variable
- **Allowed Hosts**: Configured from `ALLOWED_HOSTS` env variable
- **Database**: PostgreSQL with `dj-database-url`
- **Cache**: Redis backend for sessions and caching
- **Static Files**: WhiteNoise middleware for efficient serving

**Installed Apps:**
```python
- django.contrib.* (core apps)
- accounts (main app)
- allauth, allauth.account (OAuth/auth)
- allauth.socialaccount.providers.google
- allauth.socialaccount.providers.github
- rest_framework (API)
- corsheaders (CORS support)
```

**Middleware Stack:**
1. CorsMiddleware (CORS handling)
2. SecurityMiddleware (security headers)
3. SessionMiddleware (sessions)
4. CommonMiddleware
5. CsrfViewMiddleware (CSRF protection)
6. AuthenticationMiddleware
7. MessageMiddleware
8. XFrameOptionsMiddleware (clickjacking)
9. AccountMiddleware (allauth)

### 4.2 API Layer (REST Framework)

**Main Views (views.py):**
- `dashboard_view()` - User dashboard
- `edit_profile()` - Profile management
- `search_projects()` - Project search & filtering
- `project_feed()` - Paginated project feed
- Various auth views (login, register, logout)

**Chat API (chat_api.py / chat_api_improved.py):**
- `get_conversations()` - List user conversations
- `create_chat_room()` - Create group chat
- `send_message()` - Send DM or room message
- `fetch_messages()` - Load message history
- `mark_as_read()` - Update read status

**Comment API (comment_api.py):**
- `post_comment()` - Create comment on project
- `get_comments()` - Fetch all comments
- `delete_comment()` - Remove comment
- `like_comment()` - Like/unlike

**Template API (template_api.py):**
- `get_templates()` - List project templates
- `create_from_template()` - Create project from template
- `save_template()` - Save project as template

**Serializers (serializers.py):**
```python
UserProfileSerializer
ProjectSerializer
ChatMessageSerializer
CommentSerializer
NotificationSerializer
```

### 4.3 WebSocket Layer (Real-time)

**Consumers (consumers.py):**
```python
ChatConsumer
├─ Groups: chat_<room_id>
├─ Events: chat_message, user_join, user_leave
└─ Methods: receive_chat_message(), connect(), disconnect()

ProjectConsumer
├─ Groups: project_<id>
├─ Events: project_update, member_join
└─ Real-time project updates

NotificationConsumer
├─ Groups: user_<user_id>
├─ Events: notification_created
└─ Broadcast notifications
```

**Routing (routing.py):**
```python
websocket_urlpatterns = [
    path('ws/chat/<room_id>/', ChatConsumer.as_asgi()),
    path('ws/project/<project_id>/', ProjectConsumer.as_asgi()),
    path('ws/notifications/', NotificationConsumer.as_asgi()),
]
```

**Real-time Signals (signals_realtime.py):**
```python
@receiver(post_save, sender=Message)
def broadcast_message(sender, instance, created, **kwargs):
    # Emit to ChatConsumer group
    
@receiver(post_save, sender=Comment)
def broadcast_comment(sender, instance, created, **kwargs):
    # Emit to ProjectConsumer group
    
@receiver(post_save, sender=Notification)
def broadcast_notification(sender, instance, created, **kwargs):
    # Emit to NotificationConsumer group
```

### 4.4 Authentication System

**OAuth2 Flow (via django-allauth):**
```
User → "Login with Google/GitHub" → OAuth Provider
    ↓
OAuth Provider → Callback URL → django-allauth
    ↓
allauth → User lookup/creation → Create session
    ↓
User authenticated → Redirect to dashboard
```

**OTP Email Flow:**
```
User → Enter email → Generate OTP (6-digit)
    ↓
Send via Brevo SMTP → User inbox
    ↓
User → Enter OTP → Verify in database
    ↓
OTP marked used → Create session
```

**Authentication Backends:**
- `EmailBackend` - Email/password authentication
- `OTPBackend` - OTP verification
- `GoogleOAuth2Adapter` (from allauth)
- `GithubOAuth2Adapter` (from allauth)

### 4.5 Business Logic & Utils

**StudentProfileNLP (utils.py):**
```python
class StudentProfileNLP:
    - analyze_skills(profile_text)
    - extract_interests(description)
    - match_projects(profile, projects)
    - calculate_relevance_score(user, project)
```

**ProjectVisibilityFilter (utils.py):**
```python
class ProjectVisibilityFilter:
    - filter_visible_projects(user, queryset)
    - check_project_access(user, project)
    - apply_privacy_rules(user, project)
```

**Email Backends:**
- `BrevoMailBackend` - Brevo SMTP integration
- `ZeptoMailBackend` - Alternative email provider

---

## 5. Frontend Architecture

### 5.1 React App Structure

**Entry Point (main.jsx):**
```javascript
import React from 'react'
import ReactDOM from 'react-dom/client'
import App from './App.jsx'
import './index.css'

ReactDOM.createRoot(document.getElementById('root')).render(
  <React.StrictMode>
    <App />
  </React.StrictMode>,
)
```

**Main App Component (App.jsx):**
```javascript
// Features:
- React Router setup
- Authentication context
- API client initialization
- Global state management
- Page routing
```

**API Client (api/):**
```javascript
// Axios instance with:
- Base URL configuration
- Authorization header injection
- Error handling
- Request/response interceptors
```

### 5.2 Component Organization

**Typical Component Structure:**
```javascript
- /pages
  - Dashboard.jsx
  - Projects.jsx
  - ProjectDetail.jsx
  - Profile.jsx
  - Chat.jsx
  - FindCollaborators.jsx

- /components
  - Header/Navbar.jsx
  - Footer.jsx
  - ProjectCard.jsx
  - UserCard.jsx
  - ChatMessage.jsx
  - CommentSection.jsx

- /hooks
  - useAuth.js
  - useProject.js
  - useChat.js
  - useFetch.js

- /context
  - AuthContext.jsx
  - ProjectContext.jsx
  - ChatContext.jsx
```

### 5.3 Key Features

**Authentication Flow:**
1. User enters email/password
2. Submit to `/api/login/`
3. Backend validates & returns token
4. Frontend stores token in localStorage
5. Axios interceptor adds token to headers

**Real-time Chat:**
1. Connect to WebSocket: `/ws/chat/<room_id>/`
2. Send message → emit to room
3. Receive updates from other users
4. Update local state & re-render

**Project Discovery:**
1. Fetch projects from `/api/projects/`
2. Apply filters (skills, category, status)
3. Display paginated results
4. Click project → load details

**Comments & Engagement:**
1. Load comments from `/api/comments/?project=<id>`
2. Post comment to `/api/comments/`
3. WebSocket broadcasts new comment
4. Real-time update to all viewers

---

## 6. Data Flow Examples

### 6.1 User Registration Flow

```
Frontend
  ↓ User submits form
Backend (views.py)
  ↓ Validate input
  ↓ Create User & StudentProfile
  ↓ Generate OTP
  ↓ Send email via Brevo
  ↓ Return success
Frontend
  ↓ Show OTP verification form
Backend (OTP verification)
  ↓ Check OTP validity
  ↓ Mark OTP as used
  ↓ Create session
  ↓ Return auth token
Frontend
  ↓ Store token
  ↓ Redirect to dashboard
```

### 6.2 Project Collaboration Flow

```
User A (Frontend)
  ↓ Search projects
  ↓ GET /api/projects/
Backend
  ↓ Query database
  ↓ Apply visibility filter
  ↓ Return paginated results
Frontend
  ↓ Display project cards
User A (clicks project)
  ↓ GET /api/projects/<id>/
Backend
  ↓ Check permissions
  ↓ Load full project + members
  ↓ Return data
Frontend
  ↓ Display project detail
User A (sends collaboration request)
  ↓ POST /api/connections/
Backend
  ↓ Create Connection model
  ↓ Broadcast via WebSocket
  ↓ Create Notification
User B (receives notification)
  ↓ WebSocket receives event
  ↓ Real-time notification appears
  ↓ Can accept/reject
```

### 6.3 Real-time Chat Flow

```
User A (Frontend)
  ↓ Open chat room
  ↓ WebSocket connect to /ws/chat/<room_id>/
Backend (ChatConsumer)
  ↓ Accept connection
  ↓ Load message history
  ↓ Add user to group
Frontend
  ↓ Display chat history

User A (types message)
  ↓ Submit form
  ↓ WebSocket send message
Backend (ChatConsumer)
  ↓ Receive message
  ↓ Save to database
  ↓ Broadcast to group
Backend (signals)
  ↓ Message saved signal
  ↓ Emit via WebSocket to group
Backend → All users in room
  ↓ Receive message event
  ↓ Update chat UI
```

---

## 7. Key Features & Implementation

### 7.1 Authentication Features

| Feature | Implementation |
|---------|----------------|
| Email/Password Login | `LoginView` in views.py |
| OTP Login | `OTPVerificationView` + Brevo |
| Google OAuth | `GoogleOAuth2Adapter` (allauth) |
| GitHub OAuth | `GithubOAuth2Adapter` (allauth) |
| Session Management | Redis + Django sessions |
| CSRF Protection | Middleware + token validation |

### 7.2 Project Management

| Feature | Implementation |
|---------|----------------|
| Create Project | `ProjectCreateView` |
| List Projects | `project_feed()` with pagination |
| Search & Filter | `search_projects()` + Q objects |
| Visibility Control | `ProjectVisibilityFilter` |
| Member Management | `ProjectTeam` + invitations |
| Task Tracking | `ProjectTask` model |

### 7.3 Communication Features

| Feature | Implementation |
|---------|----------------|
| Direct Messages | `Message` model + `ChatConsumer` |
| Group Chat | `ChatRoom` with WebSocket |
| Comments | `Comment` model + real-time broadcast |
| Notifications | `Notification` + `NotificationConsumer` |
| Read Status | `MessageReadStatus` tracking |
| Reactions | `MessageReaction` on messages |

### 7.4 Real-time Features

| Feature | Implementation |
|---------|----------------|
| Chat Messages | WebSocket + `ChatConsumer` |
| Comments | `signals_realtime.py` |
| Notifications | `NotificationConsumer` group |
| User Status | `UserStatus` model + broadcast |
| Project Updates | `ProjectConsumer` |
| Connection Requests | WebSocket event broadcast |

---

## 8. Database Schema Relationships

```
User
├─ has_one: StudentProfile
├─ has_many: Project (as owner)
├─ has_many: Message (as sender/receiver)
├─ has_many: Connection (as sender/receiver)
├─ has_many: Comment
├─ has_many: Activity
├─ has_many: Like
├─ has_many: Follow (as follower/followee)
├─ has_many: Notification (as user/actor)
├─ has_many: ChatRoomMember
└─ has_many: ProjectTeamMember

Project
├─ belongs_to: User (owner)
├─ has_many: Comment
├─ has_many: Like
├─ has_many: ProjectTeam
├─ has_many: ProjectTask
├─ has_many: ProjectMilestone
├─ has_many: File
└─ has_many: Activity

ChatRoom
├─ has_many: ChatRoomMember
├─ has_many: Message
└─ has_many: User (through ChatRoomMember)

Message
├─ belongs_to: User (sender)
├─ has_many: MessageFile
├─ has_many: MessageReaction
└─ has_many: MessageReadStatus
```

---

## 9. API Endpoints Summary

### Authentication
```
POST   /api/auth/login/              - Email/password login
POST   /api/auth/register/           - New user registration
POST   /api/auth/otp/generate/       - Generate OTP
POST   /api/auth/otp/verify/         - Verify OTP
POST   /api/auth/google/             - Google OAuth callback
POST   /api/auth/github/             - GitHub OAuth callback
POST   /api/auth/logout/             - Logout
GET    /api/auth/user/               - Current user info
```

### Projects
```
GET    /api/projects/                - List projects (paginated)
POST   /api/projects/                - Create project
GET    /api/projects/<id>/           - Project details
PUT    /api/projects/<id>/           - Update project
DELETE /api/projects/<id>/           - Delete project
GET    /api/projects/search/         - Search & filter
POST   /api/projects/<id>/members/   - Add member
DELETE /api/projects/<id>/members/   - Remove member
```

### Chat & Messages
```
GET    /api/messages/conversations/  - List conversations
POST   /api/messages/                - Send message
GET    /api/messages/<id>/           - Fetch messages
POST   /api/chatrooms/               - Create chat room
GET    /api/chatrooms/               - List chat rooms
WS     /ws/chat/<room_id>/           - WebSocket chat
```

### Comments & Engagement
```
GET    /api/comments/                - List comments
POST   /api/comments/                - Post comment
DELETE /api/comments/<id>/           - Delete comment
POST   /api/comments/<id>/like/      - Like comment
POST   /api/likes/                   - Like project
DELETE /api/likes/<id>/              - Unlike project
```

### Social Features
```
GET    /api/connections/             - List connections
POST   /api/connections/             - Send connection request
PUT    /api/connections/<id>/        - Accept/reject
GET    /api/follow/                  - List followers
POST   /api/follow/                  - Follow user
POST   /api/profiles/<id>/           - Get user profile
PUT    /api/profiles/                - Update own profile
```

### Notifications
```
GET    /api/notifications/           - List notifications
PUT    /api/notifications/<id>/      - Mark as read
POST   /api/notifications/read-all/  - Mark all as read
WS     /ws/notifications/            - WebSocket notifications
```

---

## 10. Caching Strategy

### Redis Cache Usage

```python
# Session Cache
CACHES = {
    'default': {
        'BACKEND': 'django_redis.cache.RedisCache',
        'LOCATION': 'redis://localhost:6379/1',
    }
}

# Specific Cache Keys
- project:<id>              # Project details (30 min)
- user:<id>:profile        # User profile (1 hour)
- messages:<room_id>       # Chat history (2 hours)
- search:projects:<query>  # Search results (15 min)
- notifications:<user_id>  # User notifications (live)
```

---

## 11. Security Considerations

### Implemented
- CSRF token protection on all forms
- SQL injection prevention (ORM)
- XSS protection (template auto-escaping)
- CORS headers validation
- Content Security Policy headers
- Secure password hashing (Django default)
- OAuth2 for third-party auth
- Permission-based access control

### In Transit
- HTTPS required in production
- Secure session cookies
- CSRF tokens in AJAX requests

### In Storage
- Passwords hashed with PBKDF2
- Sensitive data in environment variables
- Media files outside web root
- Database backups encrypted

---

## 12. Deployment Architecture

### Docker Containers
```dockerfile
# Backend Container
- Django application (Gunicorn)
- Python environment
- Static files collected

# Frontend Container
- React build
- Nginx reverse proxy
- Vite optimized bundles

# Database Container
- PostgreSQL
- Volume for persistence

# Cache Container
- Redis
- Session & cache storage
```

### Deployment Platforms
- **Render.com** - Primary deployment
- **Railway.app** - Alternative
- **Docker Compose** - Local development

---

## 13. Performance Optimizations

### Backend
- Database query optimization (select_related, prefetch_related)
- Redis caching for frequently accessed data
- Pagination for large datasets
- Asynchronous task processing (optional Celery)
- Connection pooling with psycopg2

### Frontend
- Code splitting with Vite
- Lazy loading of routes
- Image optimization
- Local state management
- Debouncing search queries

### WebSocket
- Redis pub/sub for scalability
- Connection pooling
- Message compression
- Automatic reconnection

---

## 14. Testing Structure

```
backend/accounts/
├─ tests.py              # Unit tests
│  ├─ TestUserModel
│  ├─ TestProjectModel
│  ├─ TestAuthentication
│  ├─ TestAPI
│  └─ TestWebSocket

Frontend (if exists)
├─ __tests__/
│  ├─ App.test.jsx
│  ├─ components/*.test.jsx
│  └─ api/*.test.js
```

---

## 15. Development Workflow

### Setting Up Development Environment

```bash
# Backend
cd backend
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
pip install -r requirements.txt
python manage.py migrate
python manage.py runserver

# Frontend
cd frontend
npm install
npm run dev

# WebSocket/Cache (Docker)
docker-compose up -d
```

### Key Development Files
- `.env.local` - Environment configuration
- `docker-compose.yml` - Local services
- `manage.py` - Django CLI
- `vite.config.js` - Frontend build config

---

## 16. Common Patterns & Code Examples

### Creating a Model
```python
class NewModel(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=200)
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return self.title
    
    class Meta:
        ordering = ['-created_at']
```

### Creating a View
```python
@login_required
def my_view(request):
    data = MyModel.objects.filter(user=request.user)
    return render(request, 'template.html', {'data': data})
```

### Creating an API Endpoint
```python
class MySerializer(serializers.ModelSerializer):
    class Meta:
        model = MyModel
        fields = '__all__'

class MyViewSet(viewsets.ModelViewSet):
    queryset = MyModel.objects.all()
    serializer_class = MySerializer
    permission_classes = [IsAuthenticated]
```

### WebSocket Consumer
```python
class MyConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        await self.accept()
    
    async def receive(self, text_data):
        # Process message
        await self.send(text_data=json.dumps(response))
```

### Real-time Signal
```python
@receiver(post_save, sender=MyModel)
def my_signal(sender, instance, created, **kwargs):
    async_to_sync(channel_layer.group_send)(
        'my_group',
        {'type': 'my_event', 'data': instance}
    )
```

---

## 17. Troubleshooting & Common Issues

### Issue: WebSocket Connection Fails
**Causes:**
- Redis not running
- Daphne server not started
- ASGI configuration incorrect

**Solution:**
```bash
# Start Redis
redis-server

# Start Daphne
daphne -b 0.0.0.0 -p 8000 auth_project.asgi:application
```

### Issue: OAuth Callback Error
**Causes:**
- Redirect URI mismatch
- Client credentials wrong
- Settings not updated

**Solution:**
1. Check OAuth app config in Django admin
2. Verify redirect URI matches provider
3. Update CLIENT_ID and CLIENT_SECRET

### Issue: Static Files Not Loading
**Causes:**
- Collectstatic not run
- Wrong STATIC_ROOT/URL
- WhiteNoise not configured

**Solution:**
```bash
python manage.py collectstatic --noinput
```

---

## 18. Monitoring & Logging

### Backend Logging
```python
logger = logging.getLogger(__name__)
logger.error("Error message")
logger.info("Info message")
```

**Log Files:**
- `backend/logs/` directory
- Django development server logs
- Gunicorn access/error logs

### Frontend Errors
```javascript
console.error('Error:', error)
console.log('Debug:', variable)
```

---

## 19. Contributing Guidelines

### Code Style
- Follow PEP 8 for Python
- Use ESLint for JavaScript
- 4-space indentation (Python)
- 2-space indentation (JavaScript)

### Commit Messages
```
[FEATURE] Add new feature
[BUGFIX] Fix specific issue
[REFACTOR] Improve code structure
[DOCS] Update documentation
```

### Testing Before Commit
```bash
# Backend
python manage.py test

# Frontend
npm run test
```

---

## 20. Future Enhancements

- [ ] Video call integration (WebRTC)
- [ ] Advanced analytics dashboard
- [ ] AI-powered project recommendations
- [ ] Mobile app (React Native)
- [ ] Project templates library
- [ ] Team chat channels
- [ ] Integration with GitHub/GitLab
- [ ] Advanced search with Elasticsearch
- [ ] Notification preferences
- [ ] Two-factor authentication (2FA)

---

## Conclusion

UniSync is a comprehensive full-stack platform that leverages modern web technologies for real-time collaboration. The architecture is modular, scalable, and production-ready. Key strengths include robust authentication, real-time communication via WebSocket, comprehensive project management, and a clean separation between frontend and backend.

For questions or support, refer to the existing documentation or community resources.

