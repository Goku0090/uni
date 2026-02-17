# UniSync Codebase Analysis - Comprehensive Overview

**Project**: UniSync (Student Collaboration Platform)  
**Date**: February 2026  
**Stack**: Django + React/Vite + Django Channels (WebSockets) + PostgreSQL

---

## Table of Contents
1. [Architecture Overview](#architecture-overview)
2. [Database Models](#database-models)
3. [Backend API Endpoints](#backend-api-endpoints)
4. [Frontend Structure](#frontend-structure)
5. [Real-time Features](#real-time-features)
6. [Authentication System](#authentication-system)
7. [Key Features Implementation](#key-features-implementation)
8. [Data Flow](#data-flow)

---

## Architecture Overview

UniSync uses a **hybrid architecture**:

### Backend: Django (Multi-layered)
- **Django Framework**: Server-side rendering + REST API
- **Django Rest Framework (DRF)**: JSON APIs for frontend consumption
- **Django Channels**: WebSocket support for real-time collaboration
- **Database**: PostgreSQL (production), SQLite (development)

### Frontend: React/Vite
- Single Page Application (SPA) for dynamic project feed
- Server-side rendered HTML templates for traditional pages
- Axios for API communication
- WebSocket client for real-time updates

### Key Directories
```
backend/
├── accounts/              # Main Django app
│   ├── models.py         # Database schema
│   ├── views.py          # View handlers
│   ├── urls.py           # URL routing
│   ├── serializers.py    # DRF serializers
│   ├── consumers.py      # WebSocket consumers
│   ├── chat_api_improved.py    # Messaging APIs
│   ├── comment_api.py    # Comments system
│   ├── template_api.py   # Project templates
│   └── templates/        # HTML templates
├── auth_project/         # Django config
│   ├── settings.py       # Settings & env config
│   ├── urls.py          # Root URL routing
│   ├── asgi.py          # ASGI config (Channels)
│   └── wsgi.py          # WSGI config
└── manage.py            # Django CLI

frontend/
├── src/
│   ├── App.jsx          # React root component
│   ├── main.jsx         # Vite entry point
│   └── index.css        # Styling
└── package.json         # Dependencies
```

---

## Database Models

### Core User Management

#### **StudentProfile**
```
- user (OneToOne → User)
- full_name, college, location
- bio, profile_photo
- skills (JSON array)
- interests (JSON array)
- project_interests (JSON array)
- role_preference
- social_links (GitHub, LinkedIn, Portfolio, Behance)
- profile_completed (boolean)
```

#### **OTP** (Authentication)
```
- email
- otp_code (6-digit)
- purpose (login/registration/reset)
- is_used (boolean)
- created_at, expires_at (5 minutes)
```

### Project Management

#### **Project**
```
- owner (FK → User)
- title, description
- technologies (JSON array)
- collaboration_needs (text)
- visibility (public/private)
- team_size_min, team_size_max
- status (active/paused/completed)
- looking_for (JSON array of roles)
- application_deadline
- media (JSONField for images/videos)
- created_at, updated_at
```

#### **ProjectMember**
```
- project (FK → Project)
- user (FK → User)
- role (owner/lead/contributor/advisor)
- joined_at
- is_active (boolean)
```

#### **ProjectTask**
```
- project (FK → Project)
- title, description
- assigned_to (FK → User)
- assigned_by (FK → User)
- status (todo/in_progress/review/completed/cancelled)
- priority (low/medium/high/urgent)
- due_date
```

#### **ProjectMilestone**
```
- project (FK → Project)
- title, description
- due_date
- is_completed (boolean)
- completed_by (FK → User)
```

#### **ProjectTemplate**
```
- name, category (web/mobile/ai/data/blockchain/iot/game)
- description, icon
- template_title, template_description
- template_technologies (JSON)
- template_looking_for (JSON)
- difficulty_level (beginner/intermediate/advanced)
- suggested_timeline, suggested_team_size
- rating (0-5), usage_count
- is_featured (boolean)
```

### Communication & Social

#### **ChatRoom**
```
- name
- chat_type (direct/group)
- members (M2M → User via ChatRoomMember)
- created_at, updated_at
```

#### **ChatRoomMember**
```
- chat_room (FK → ChatRoom)
- user (FK → User)
- is_active (boolean)
- joined_at
```

#### **Message**
```
- sender (FK → User)
- receiver (FK → User, nullable for group chats)
- chat_room (FK → ChatRoom, nullable for DMs)
- content
- message_type (text/file/image/call)
- call_type (voice/video, nullable)
- reply_to (self FK for threading)
- created_at, updated_at
```

#### **MessageReadStatus**
```
- message (FK → Message)
- user (FK → User)
- read_at (DateTimeField)
```

#### **MessageReaction**
```
- message (FK → Message)
- user (FK → User)
- reaction (emoji/text)
```

#### **Comment**
```
- project (FK → Project)
- user (FK → User)
- content
- reply_to (self FK for nested comments)
- created_at, updated_at
```

### Social Features

#### **Connection**
```
- sender (FK → User)
- receiver (FK → User)
- status (pending/accepted/rejected)
- created_at, updated_at
```

#### **Follow**
```
- follower (FK → User)
- following (FK → User)
- created_at
```

#### **Like**
```
- user (FK → User)
- project (FK → Project)
- created_at
```

#### **Notification**
```
- user (FK → User)
- sender (FK → User)
- notification_type (message/comment/like/connection/invitation)
- related_project/related_message (FK, nullable)
- is_read (boolean)
- created_at
```

---

## Backend API Endpoints

### Authentication APIs

| Method | Endpoint | Description |
|--------|----------|-------------|
| POST | `/api/auth/register/` | User registration with email |
| POST | `/api/auth/login/` | Login with OTP |
| POST | `/api/auth/verify-otp/` | Verify OTP code |
| POST | `/api/auth/logout/` | User logout |
| POST | `/api/auth/password-reset/` | Password reset request |

### Project APIs

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/api/projects/` | List all projects (paginated) |
| POST | `/api/projects/` | Create new project |
| GET | `/api/projects/<id>/` | Get project details |
| PUT | `/api/projects/<id>/` | Update project |
| DELETE | `/api/projects/<id>/` | Delete project |
| GET | `/api/projects/search/` | Search projects |
| POST | `/api/projects/<id>/apply/` | Apply to join project |
| GET | `/api/projects/<id>/members/` | Get project members |
| POST | `/api/projects/<id>/invite/` | Invite user to project |

### Messaging APIs

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/api/chat-rooms/` | List chat rooms |
| POST | `/api/chat-rooms/` | Create chat room |
| GET | `/api/chat-rooms/<id>/` | Get chat room details |
| GET | `/api/chat-rooms/<id>/messages/` | Get messages in chat room |
| POST | `/api/messages/` | Send message |
| PUT | `/api/messages/<id>/` | Edit message |
| DELETE | `/api/messages/<id>/` | Delete message |
| POST | `/api/messages/<id>/react/` | Add reaction to message |

### Comments APIs

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/api/projects/<id>/comments/` | Get project comments |
| POST | `/api/projects/<id>/comments/` | Post comment |
| PUT | `/api/comments/<id>/` | Edit comment |
| DELETE | `/api/comments/<id>/` | Delete comment |

### Profile & Social APIs

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/api/user-profile/` | Get current user profile |
| PUT | `/api/user-profile/` | Update user profile |
| GET | `/api/users/<id>/profile/` | Get user profile |
| POST | `/api/connections/` | Send connection request |
| GET | `/api/connections/` | List connections |
| PUT | `/api/connections/<id>/` | Accept/reject connection |
| POST | `/api/likes/` | Like a project |
| DELETE | `/api/likes/<id>/` | Unlike a project |

### Template APIs

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/api/templates/` | List project templates |
| GET | `/api/templates/<id>/` | Get template details |
| POST | `/api/templates/<id>/use/` | Use template to create project |
| POST | `/api/templates/<id>/rate/` | Rate template |

### Notification APIs

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/api/notifications/` | Get user notifications |
| POST | `/api/notifications/<id>/read/` | Mark notification as read |

---

## Frontend Structure

### React Component Hierarchy

```
App.jsx (root)
├── Header (navigation, logo)
├── MainHome
│   ├── ProjectCard (list items)
│   │   ├── Comments section
│   │   └── Like/Share buttons
│   └── Project Feed (paginated)
├── Chat
│   ├── ChatRoomList
│   └── ChatWindow
│       ├── MessageList
│       └── MessageInput
├── Profile
│   ├── UserProfile
│   ├── StudentProfileForm
│   └── Skills/Interests editor
├── FindCollaborators
│   ├── SearchFilters
│   └── CollaboratorCard
├── ProjectDetail
│   ├── ProjectHeader
│   ├── ProjectMembers
│   ├── Tasks section
│   └── Activity feed
└── Footer
```

### State Management

**Current Approach**: React Hooks (`useState`, `useEffect`)

- **App.jsx**: Manages project feed state
  ```javascript
  const [projects, setProjects] = useState([])
  const [loading, setLoading] = useState(false)
  const [error, setError] = useState(null)
  ```

- **Chat components**: Message list, current room state
- **Profile components**: Form state, user data

### API Client

**Axios configuration** for API calls:
```javascript
const API_BASE_URL = 'http://localhost:8000/api/'
// Used for all REST API calls from React
```

### Key Frontend Pages

1. **Dashboard/Main Home** (`/`) - Project feed with real-time updates
2. **Project Detail** (`/projects/<id>/`) - Full project information
3. **Chat** (`/messages/`) - Messaging interface
4. **Find Collaborators** (`/find-collaborators/`) - Search and connect
5. **User Profile** (`/profile/`) - Student profile management
6. **Project Templates** (`/templates/`) - Browse and create from templates

---

## Real-time Features

### Django Channels Architecture

#### WebSocket Consumers

1. **ProjectUpdateConsumer** (`consumers.py`)
   - Broadcasts project changes to team members
   - Updates: title, description, team members, status
   - Groups: `project_{id}`

2. **ActivityFeedConsumer** (`consumers.py`)
   - Real-time activity feed updates
   - Broadcasts: comments, likes, new projects
   - Groups: `activity_feed`

3. **NotificationConsumer** (`consumers.py`)
   - Sends notifications to users
   - Types: messages, project invites, likes, comments
   - Groups: `notifications_{user_id}`

4. **ChatConsumer** (`consumers.py`)
   - Real-time messaging
   - Broadcasting messages to chat room members
   - Groups: `chat_{room_id}`

#### WebSocket Connection Flow

```
Client (React)
    ↓
WebSocket URL: ws://localhost:8000/ws/...
    ↓
Django Channels ASGI (routing.py)
    ↓
Consumer class (connect/receive/disconnect)
    ↓
Broadcast to group
    ↓
All connected clients in group receive
```

#### Routing Configuration

```python
# asgi.py
application = ProtocolTypeRouter({
    'http': ...,
    'websocket': AuthMiddlewareStack(
        URLRouter([
            path('ws/projects/<id>/', ProjectUpdateConsumer.as_asgi()),
            path('ws/chat/<id>/', ChatConsumer.as_asgi()),
            path('ws/notifications/', NotificationConsumer.as_asgi()),
            path('ws/activity-feed/', ActivityFeedConsumer.as_asgi()),
        ])
    )
})
```

### Real-time Signals

Django Signals trigger WebSocket broadcasts when models change:

```python
# signals_realtime.py
@receiver(post_save, sender=Comment)
def broadcast_comment(sender, instance, created, **kwargs):
    # Broadcast to activity feed when comment is added
    channel_layer.group_send(...)

@receiver(post_save, sender=Like)
def broadcast_like(sender, instance, created, **kwargs):
    # Broadcast when project is liked
    channel_layer.group_send(...)
```

---

## Authentication System

### OTP-Based Authentication

1. **Registration Flow**
   ```
   User enters email → OTP generated → Email sent → Verify OTP → Create User
   ```

2. **Login Flow**
   ```
   User enters email → OTP generated → Email sent → Verify OTP → Session created
   ```

3. **Password Reset**
   ```
   User requests reset → OTP sent → Verify OTP → Set new password
   ```

### OTP Implementation

```python
# models.py - OTP Model
class OTP(models.Model):
    email = EmailField()
    otp_code = CharField(max_length=6)  # 6-digit random code
    purpose = CharField(choices=['login', 'registration', 'reset'])
    is_used = BooleanField(default=False)
    expires_at = DateTimeField()  # 5 minutes from creation
    
    def is_valid(self):
        return not self.is_used and now() < self.expires_at
```

### Email Service Integration

**Email Backends**:
- **Brevo** (Primary)
- **Zepto** (Fallback)

```python
# brevo_mail_backend.py
class BrevoBackend(BaseEmailBackend):
    def send_messages(self, email_messages):
        # Uses Brevo API to send emails
```

### Google OAuth Integration

**Social Authentication**:
- Configured via django-allauth
- Providers: Google (primary)
- Flow: OAuth redirect → User authentication → Profile creation

---

## Key Features Implementation

### 1. Project Management

**Features**:
- Create/edit/delete projects
- Public/private visibility
- Team member management
- Role-based access (owner/lead/contributor/advisor)
- Task tracking with status and priority
- Milestones and timelines

**Implementation**:
- Models: `Project`, `ProjectMember`, `ProjectTask`, `ProjectMilestone`
- Views: `post_project()`, `edit_project()`, `project_detail()`
- APIs: REST endpoints in `urls.py`

### 2. Real-time Collaboration

**Features**:
- Live project updates (title, description, members)
- Real-time activity feed
- Live comments
- Real-time notifications

**Implementation**:
- Django Channels consumers for WebSocket
- `signals_realtime.py` for event broadcasting
- Group subscriptions via `channel_layer.group_send()`

### 3. Messaging System

**Features**:
- Direct messaging (1-to-1)
- Group chats
- Message threading/replies
- Read receipts
- Message reactions
- File sharing

**Implementation**:
- Models: `ChatRoom`, `Message`, `MessageReadStatus`, `MessageReaction`
- API: `chat_api_improved.py` with REST endpoints
- WebSocket: `ChatConsumer` for real-time delivery
- Database: Separate `MessageReadStatus` for scalability

### 4. Comments & Engagement

**Features**:
- Project comments
- Nested/threaded comments
- Like/reaction system
- Share functionality

**Implementation**:
- Model: `Comment` (with reply_to self-reference)
- API: `comment_api.py`
- Real-time: Broadcast via signals to activity feed

### 5. Project Templates

**Features**:
- Pre-made project templates by category
- Difficulty levels
- Resource recommendations
- User ratings and reviews
- Usage tracking

**Implementation**:
- Models: `ProjectTemplate`, `TemplateRating`, `TemplateUsageLog`
- API: `template_api.py`
- Categories: web, mobile, AI/ML, data science, blockchain, IoT, game dev

### 6. Social Features

**Features**:
- Connection requests
- User following
- Activity feeds
- Notifications
- Profile browsing

**Implementation**:
- Models: `Connection`, `Follow`, `Like`, `Notification`, `Activity`
- Signals: Auto-create notifications on actions
- API: `find_collaborators()` for search

---

## Data Flow

### Project Creation Flow

```
1. User submits form (frontend)
   ↓
2. POST /api/projects/ (REST API)
   ↓
3. post_project() view validates & creates Project
   ↓
4. Project model save() triggered
   ↓
5. Signals broadcast to activity feed (WebSocket)
   ↓
6. All connected clients receive update
   ↓
7. Frontend updates project list
```

### Message Sending Flow

```
1. User types & sends message (Chat component)
   ↓
2. WebSocket send() to ChatConsumer
   ↓
3. Message object created in database
   ↓
4. Consumer broadcasts to chat room group
   ↓
5. All room members receive in real-time
   ↓
6. MessageReadStatus tracked separately
```

### Comment & Notification Flow

```
1. User posts comment (Project detail page)
   ↓
2. POST /api/comments/ (REST API)
   ↓
3. Comment model created
   ↓
4. post_save signal triggered
   ↓
5. Broadcast to activity_feed group (WebSocket)
   ↓
6. Create Notification for project owner
   ↓
7. Notification sent via NotificationConsumer
   ↓
8. Frontend displays badge & real-time alert
```

---

## Performance Optimizations

### Database
- **Indexing**: Foreign keys, created_at fields
- **Caching**: Project list, user profiles (Django cache)
- **Pagination**: 10 items per page for feeds
- **Query optimization**: select_related(), prefetch_related()

### Frontend
- **Code splitting**: Vite for lazy loading
- **Asset compression**: CSS/JS minification
- **Lazy loading**: Images with intersection observer
- **State management**: Minimal re-renders with useEffect cleanup

### API
- **Response compression**: gzip enabled
- **Rate limiting**: IP-based throttling
- **CORS**: Configured for frontend origin
- **CSRF protection**: Token-based

---

## Deployment Architecture

### Local Development
- **Server**: Django development server (python manage.py runserver)
- **Database**: SQLite
- **WebSocket**: Daphne server (daphne -b 0.0.0.0 -p 8000 auth_project.asgi:application)
- **Frontend**: Vite dev server with HMR

### Production (Railway/Render)
- **Server**: Gunicorn/Daphne
- **Database**: PostgreSQL
- **Static files**: Whitenoise or separate CDN
- **Environment**: Docker container with compose

### Environment Variables

```
DJANGO_SECRET_KEY=...
DEBUG=False
ALLOWED_HOSTS=yourdomain.com
DATABASES_URL=postgresql://user:pass@host/db

# Email
EMAIL_BACKEND=accounts.brevo_mail_backend.BrevoBackend
BREVO_API_KEY=...

# OAuth
GOOGLE_CLIENT_ID=...
GOOGLE_CLIENT_SECRET=...
OAUTH_REDIRECT_URI=http://yourdomain.com/oauth/callback

# Storage
AWS_ACCESS_KEY_ID=...
AWS_SECRET_ACCESS_KEY=...
AWS_STORAGE_BUCKET_NAME=...
```

---

## Testing Strategy

### Backend Testing
- Unit tests for models (`models.py`)
- API endpoint tests (`test_views.py`)
- WebSocket consumer tests (`test_consumers.py`)
- Integration tests for flows

### Frontend Testing
- Component testing with React Testing Library
- E2E tests with Cypress/Playwright
- Manual testing for WebSocket features

### Test Commands
```bash
# Backend
python manage.py test accounts

# Frontend
npm test
npm run e2e
```

---

## Known Issues & Recent Fixes

1. **CSRF Token Errors**: Fixed by ensuring CSRF middleware properly enabled
2. **Template Recursion**: Fixed by removing recursive includes
3. **Like Button State**: Fixed state management in React components
4. **Project Detail Loading**: Optimized database queries with select_related()
5. **WebSocket Connection**: Fixed Daphne routing configuration
6. **Email Delivery**: Configured fallback from Brevo to Zepto
7. **OAuth Configuration**: Fixed redirect URI matching
8. **Django Signals**: Fixed signal imports to avoid circular dependencies

---

## Future Enhancements

1. **Video Calls**: Integration with Agora/Twilio
2. **Advanced Matching**: ML-based skill-project matching
3. **Analytics Dashboard**: Project performance metrics
4. **Automated Testing**: CI/CD pipeline setup
5. **Mobile App**: React Native version
6. **AI Assistant**: Project recommendation engine
7. **Payment Integration**: Subscription features
8. **Advanced Search**: Elasticsearch integration

---

## Quick Reference

### Important Files Location

| Purpose | File |
|---------|------|
| Database models | `backend/accounts/models.py` |
| URL routing | `backend/accounts/urls.py` |
| View handlers | `backend/accounts/views.py` |
| WebSocket setup | `backend/accounts/consumers.py` |
| Real-time signals | `backend/accounts/signals_realtime.py` |
| Chat API | `backend/accounts/chat_api_improved.py` |
| Comments API | `backend/accounts/comment_api.py` |
| Templates API | `backend/accounts/template_api.py` |
| Django settings | `backend/auth_project/settings.py` |
| ASGI config | `backend/auth_project/asgi.py` |
| React entry | `frontend/src/App.jsx` |
| React main | `frontend/src/main.jsx` |

### Quick Commands

```bash
# Backend
cd backend
python manage.py runserver
python manage.py makemigrations
python manage.py migrate
python manage.py shell
python manage.py test

# Frontend
cd frontend
npm install
npm run dev
npm run build

# WebSocket (production-like)
daphne -b 0.0.0.0 -p 8000 auth_project.asgi:application
```

---

**End of Analysis**  
This document provides a complete technical overview of the UniSync platform.
