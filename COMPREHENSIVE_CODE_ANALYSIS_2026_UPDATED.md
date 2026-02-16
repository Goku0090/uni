# Comprehensive Code Analysis - UniSinq Platform 2026

## Project Overview

**Project Name**: UniSinq (University Sync/Synchronization)
**Tech Stack**: Django (Backend) + React/Vite (Frontend) + WebSockets
**Repository**: https://github.com/goku0090/uni
**Status**: Active Development with Multiple Features

---

## Architecture Summary

```
UniSinq Platform
├── Backend (Django)
│   ├── Core: auth_project (settings, URLs, WSGI/ASGI)
│   ├── App: accounts (main business logic)
│   └── Services: Email, Chat, Comments, WebSockets
│
└── Frontend (React + Vite)
    ├── Components: Pages, Cards, Forms
    ├── API: Client-side HTTP & WebSocket communication
    └── Build: Vite with optimized bundling
```

---

## Backend Architecture (Django)

### 1. Core Configuration
**Location**: `backend/auth_project/`

#### Files:
- **settings.py** (364 lines)
  - Environment-based configuration
  - Database: PostgreSQL (production) / SQLite (dev)
  - Email backends: Brevo (primary) → Gmail SMTP (fallback) → Console (dev)
  - Installed apps: Django core + Allauth + DRF + CORS + Channels
  - Authentication: Django ModelBackend + Allauth
  - Static/Media file handling

- **urls.py**
  - Root URL routing
  - API endpoints
  - OAuth/Social login integration

- **asgi.py**
  - Django Channels setup for WebSocket support
  - Async application gateway

- **wsgi.py**
  - WSGI application for production deployment

### 2. Main Application (accounts)
**Location**: `backend/accounts/`

#### Core Models (`models.py`)
Likely contains:
- User model extensions
- Project models
- Comment models
- Activity/Notification models
- Message models
- Chat/Conversation models
- Template models
- Collaboration/Skill matching models

#### Views & APIs
1. **views.py** - Main view handlers
2. **views_contact.py** - Contact form handling
3. **comment_api.py** - Comment CRUD operations
4. **template_api.py** - Project template endpoints
5. **chat_api.py** - Chat messaging (original)
6. **chat_api_improved.py** - Enhanced chat (new version)

#### Real-time Features
- **consumers.py** - WebSocket consumers for:
  - Live chat messages
  - Real-time notifications
  - Activity streams
  - Collaborator updates

- **routing.py** - WebSocket URL routing
- **signals_realtime.py** - Django signals for real-time event broadcasting

#### Authentication & Authorization
- **forms.py** - Registration/Login/Social signup forms
- **serializers.py** - DRF serializers for API responses
- **permissions.py** - Custom permission classes
- **auth_service.py** - Auth business logic (OTP, verification)

#### Email Systems
1. **brevo_mail_backend.py** - Brevo API integration (primary)
2. **zepto_mail_backend.py** - Zepto Mail integration (alternative)
   - OTP delivery
   - Transactional emails
   - Template emails

#### Utilities
- **utils.py** - Helper functions
- **custom_filters.py** - Django template filters

#### Management Commands
- **create_templates.py** - Initialize project templates

---

## Frontend Architecture (React + Vite)

**Location**: `frontend/`

### Build & Configuration
- **vite.config.js** - Build configuration, hot module replacement
- **package.json** - Dependencies and scripts
- **index.html** - Entry point
- **.env.local** - Local environment variables

### Source Structure
**Location**: `frontend/src/`

#### Main Entry
- **main.jsx** - React entry point
- **App.jsx** - Root component

#### API Client
- **api/client.js** - Axios/HTTP client setup
  - Base URL configuration
  - Request/response interceptors
  - CSRF token handling
  - Authentication headers

### Key Features Implemented

#### 1. Authentication
- Email/password login
- Social login (Google, GitHub)
- OTP verification
- Session management

#### 2. User Profiles
- User information display
- Profile picture management
- Bio/skills editing
- Account settings

#### 3. Projects
- Project creation/editing
- Project cards with metadata
- Project detail views
- Project filtering by visibility/skills/topics

#### 4. Collaboration
- Find collaborators feature
- Skill matching algorithm
- Collaboration requests
- Team formation

#### 5. Comments System
- Comments on projects
- Comment threads
- Real-time comment updates
- Comment badges/counts

#### 6. Messaging
- Direct messages
- Group chats/team channels
- Message read status
- Notifications for unread messages
- Real-time message delivery via WebSockets

#### 7. Activities & Notifications
- Activity feed
- User activity tracking
- Notification system
- Real-time notifications

#### 8. Advanced Features
- Project templates
- Skill-based matching
- Project analytics
- Video call integration (Agora/similar)
- GitHub integration

---

## Key Technologies & Libraries

### Backend
| Technology | Purpose |
|-----------|---------|
| Django 4.x | Web framework |
| Django REST Framework | API development |
| Django Channels | WebSocket support |
| Django Allauth | Authentication/OAuth |
| PostgreSQL | Database |
| Brevo API | Email delivery |
| dj-database-url | DB URL parsing |
| python-dotenv | Environment config |

### Frontend
| Technology | Purpose |
|-----------|---------|
| React 18+ | UI library |
| Vite | Build tool |
| Axios | HTTP client |
| WebSocket | Real-time communication |

---

## API Endpoints Architecture

### Authentication
- POST `/auth/login/` - Email/password login
- POST `/auth/register/` - User registration
- POST `/auth/otp/verify/` - OTP verification
- GET `/auth/logout/` - User logout
- GET `/oauth/google/` - Google OAuth flow
- GET `/oauth/github/` - GitHub OAuth flow

### Users
- GET `/api/users/` - List users
- GET `/api/users/{id}/` - User profile
- PUT `/api/users/{id}/` - Update profile
- GET `/api/users/{id}/projects/` - User's projects
- GET `/api/users/{id}/skills/` - User's skills

### Projects
- GET `/api/projects/` - List projects
- POST `/api/projects/` - Create project
- GET `/api/projects/{id}/` - Project detail
- PUT `/api/projects/{id}/` - Update project
- DELETE `/api/projects/{id}/` - Delete project
- GET `/api/projects/{id}/comments/` - Project comments

### Comments
- GET `/api/comments/` - List comments
- POST `/api/comments/` - Create comment
- PUT `/api/comments/{id}/` - Update comment
- DELETE `/api/comments/{id}/` - Delete comment

### Messages
- GET `/api/messages/` - List messages
- POST `/api/messages/` - Send message
- GET `/api/conversations/` - List conversations
- POST `/api/conversations/` - Start conversation

### Activities
- GET `/api/activities/` - Activity feed
- GET `/api/activities/{id}/` - Activity detail

### Notifications
- GET `/api/notifications/` - User notifications
- PUT `/api/notifications/{id}/read/` - Mark as read

---

## Database Schema Overview

### Core Tables
1. **User** (Django auth.User + extensions)
   - Profile picture
   - Skills
   - Interests
   - Activity tracking

2. **Project**
   - Creator/owner
   - Title, description
   - Technologies/skills
   - Visibility (public/private)
   - Created/updated timestamps

3. **Collaboration**
   - Project foreign key
   - Collaborators
   - Status (pending/active/completed)
   - Roles

4. **Comment**
   - Project foreign key
   - Author
   - Content
   - Created/updated timestamps
   - Nested replies support

5. **Message**
   - Sender/receiver
   - Conversation foreign key
   - Content
   - Read status
   - Timestamps

6. **Activity**
   - User foreign key
   - Action type
   - Related object (polymorphic)
   - Timestamp

7. **Notification**
   - User foreign key
   - Type
   - Related object
   - Read status
   - Timestamp

8. **ProjectTemplate**
   - Name, description
   - Template data
   - Usage logging
   - Rating system

---

## Real-time Communication Flow

### WebSocket Architecture
```
Frontend (Browser)
    ↓
    WebSocket Connection
    ↓
Daphne Server (ASGI)
    ↓
Channel Layer (In-Memory / Redis)
    ↓
Django Consumers (consumers.py)
    ↓
Django Models & Signals
    ↓
Broadcast to all connected clients
```

### Event Types
1. **Chat Messages** - Live message delivery
2. **Comments** - New comment notifications
3. **Notifications** - Real-time alerts
4. **Activity Updates** - Live feed updates
5. **Presence** - User online/offline status

---

## Authentication Flow

### Email/Password Flow
1. User enters credentials
2. Django validates against User model
3. Session created on success
4. CSRF token issued
5. Redirect to dashboard

### OTP Flow
1. User enters email
2. System generates 6-digit OTP
3. Brevo sends OTP via email
4. User verifies OTP
5. Account confirmed

### OAuth Flow (Google/GitHub)
1. Frontend redirects to OAuth provider
2. User authorizes
3. Provider redirects back with code
4. Django exchanges code for token
5. User profile auto-filled or created
6. Session established

---

## Email Systems

### Primary: Brevo
- Used for OTP delivery
- Transactional emails
- Configured via `BREVO_API_KEY`
- Fallback to Gmail SMTP if unavailable

### Fallback Chain
1. Brevo (production preferred)
2. Gmail SMTP (fallback)
3. Console (development only)

---

## Deployment Configuration

### Supported Platforms
- **Render.com** - Primary (PostgreSQL + Daphne)
- **Railway.com** - Alternative
- **Docker** - Containerized deployment

### Environment Variables Required
```
DEBUG=False
SECRET_KEY=<generated>
DATABASE_URL=postgresql://...
ALLOWED_HOSTS=yourdomain.com
SECURE_SSL_REDIRECT=True
SESSION_COOKIE_SECURE=True
CSRF_COOKIE_SECURE=True
CORS_ALLOWED_ORIGINS=https://yourdomain.com
BREVO_API_KEY=<api_key>
GOOGLE_CLIENT_ID=<client_id>
GOOGLE_CLIENT_SECRET=<secret>
GITHUB_CLIENT_ID=<client_id>
GITHUB_CLIENT_SECRET=<secret>
```

---

## Recent Bug Fixes & Improvements

### Documented Issues Fixed
1. **CSRF Token Errors** - Enhanced CSRF handling in API views
2. **Comment System** - Fixed visibility and posting issues
3. **Collaborator Matching** - Improved skill-based algorithm
4. **OAuth Integration** - Fixed Google/GitHub authentication
5. **WebSocket Connections** - Stabilized real-time updates
6. **Profile Loading** - Optimized database queries
7. **Like/Share Buttons** - Fixed state management
8. **Template System** - Resolved recursion issues
9. **Email Configuration** - Brevo primary with fallbacks
10. **Chat UI** - Enhanced visual improvements

---

## Project Structure Summary

```
login/
├── backend/
│   ├── manage.py
│   ├── requirements.txt
│   ├── Procfile
│   ├── auth_project/
│   │   ├── settings.py
│   │   ├── urls.py
│   │   ├── asgi.py
│   │   └── wsgi.py
│   ├── accounts/
│   │   ├── models.py
│   │   ├── views.py
│   │   ├── views_contact.py
│   │   ├── serializers.py
│   │   ├── forms.py
│   │   ├── urls.py
│   │   ├── consumers.py
│   │   ├── routing.py
│   │   ├── signals_realtime.py
│   │   ├── comment_api.py
│   │   ├── chat_api.py
│   │   ├── chat_api_improved.py
│   │   ├── template_api.py
│   │   ├── brevo_mail_backend.py
│   │   ├── zepto_mail_backend.py
│   │   ├── permissions.py
│   │   ├── utils.py
│   │   ├── services/
│   │   ├── management/
│   │   ├── migrations/
│   │   └── templatetags/
│   ├── docker/
│   ├── static/
│   ├── media/
│   └── logs/
│
├── frontend/
│   ├── package.json
│   ├── vite.config.js
│   ├── index.html
│   ├── src/
│   │   ├── main.jsx
│   │   ├── App.jsx
│   │   ├── api/
│   │   ├── components/
│   │   ├── pages/
│   │   └── styles/
│   ├── Dockerfile
│   └── nginx.conf
│
├── docker-compose.yml
├── Dockerfile
├── .gitignore
└── .env (not committed)
```

---

## Performance Considerations

### Database Optimization
- Query optimization in project detail views
- Pagination for list views
- Select_related/prefetch_related for relationships
- Database indexing on frequently filtered fields

### Caching
- Django cache framework
- Browser caching for static assets
- Redis caching for sessions (in production)

### Frontend Optimization
- Code splitting with Vite
- Lazy loading of components
- Image optimization
- Minimal bundle size

---

## Security Implementation

### CSRF Protection
- CSRF middleware enabled
- CSRF token in forms and AJAX requests
- Trusted origins configuration

### Authentication
- Secure password hashing (Django default)
- Session-based authentication
- OAuth for social login
- OTP for email verification

### CORS
- Whitelist allowed origins
- Credentials allowed
- Specific HTTP methods allowed

### Database Security
- Connection pooling
- SSL mode configuration
- Secure password policies

---

## Next Steps for Development

1. **Scale Database** - Migrate to production PostgreSQL
2. **Load Testing** - Test with concurrent users
3. **Monitoring** - Add application performance monitoring
4. **Caching Strategy** - Implement Redis for production
5. **Analytics** - Track user behavior
6. **API Rate Limiting** - Prevent abuse
7. **Automated Testing** - Expand test coverage
8. **Documentation** - API documentation (Swagger/OpenAPI)

---

## Key Files to Review

### Critical
- `backend/auth_project/settings.py` - All configuration
- `backend/accounts/models.py` - Data structure
- `backend/accounts/views.py` - Business logic
- `backend/accounts/consumers.py` - Real-time logic
- `frontend/src/api/client.js` - API communication

### Important
- `backend/accounts/serializers.py` - API responses
- `backend/accounts/forms.py` - User input validation
- `backend/accounts/urls.py` - API routing
- `backend/accounts/signals_realtime.py` - Event broadcasting
- `backend/accounts/brevo_mail_backend.py` - Email system

### Reference
- `frontend/src/App.jsx` - App structure
- `docker-compose.yml` - Local development
- `backend/requirements.txt` - Python dependencies
- `frontend/package.json` - Node dependencies

---

## Support & Debugging

### Common Issues
- **CSRF Token Errors**: Clear browser cache, verify CSRF_TRUSTED_ORIGINS
- **WebSocket Connection Fails**: Ensure Daphne is running, check port 8000
- **Email Not Sending**: Verify BREVO_API_KEY, check console output
- **OAuth Errors**: Verify callback URLs, check provider configuration
- **Database Connection**: Verify DATABASE_URL format, check credentials

### Logging
- Django logs: `backend/logs/django.log`
- Error logs: `backend/logs/error.log`
- Console output: Real-time debugging

---

**Last Updated**: February 16, 2026
**Project Status**: Active Development
**Deployment**: Render.com / Railway.com
