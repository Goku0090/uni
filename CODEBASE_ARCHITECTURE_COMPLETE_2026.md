# Complete Codebase Analysis 2026

## Project Overview
**Project**: UniSync (university student collaboration platform)
**Repository**: https://github.com/Goku0090/uni
**Tech Stack**: Django + React (Vite) + PostgreSQL
**Purpose**: Connect students for collaborative projects with features like skill matching, messaging, and real-time updates

---

## Architecture Overview

```
┌─────────────────────────────────────────────────────────────┐
│                     Frontend (React/Vite)                   │
│  - Components: App.jsx, Pages, API Integration              │
│  - State Management: React Router, Axios API Calls          │
│  - Styling: CSS, Responsive Design                          │
└────────────────────────┬────────────────────────────────────┘
                         │ HTTP/WebSocket
┌────────────────────────▼────────────────────────────────────┐
│              Django Backend (Port 8000)                      │
├──────────────────────────────────────────────────────────────┤
│  Core Apps:                                                  │
│  ├─ auth_project/  (Settings, URL routing, ASGI)            │
│  └─ accounts/      (Main app with all features)             │
├──────────────────────────────────────────────────────────────┤
│  Features:                                                   │
│  ├─ Authentication (OTP, Google/GitHub OAuth via Allauth)   │
│  ├─ User Profiles (StudentProfile with skills, interests)   │
│  ├─ Projects (Create, Edit, Browse, Join)                   │
│  ├─ Messaging & Chat (Direct + Group)                       │
│  ├─ Connections (Friend requests)                           │
│  ├─ Real-time Updates (WebSocket via Channels)              │
│  └─ Notifications                                           │
├──────────────────────────────────────────────────────────────┤
│  Key Libraries:                                              │
│  ├─ Django 4.2.8                                            │
│  ├─ Django REST Framework 3.14.0                            │
│  ├─ Django Channels 4.0.0 (WebSockets)                      │
│  ├─ Django-Allauth 0.61.1 (Social Auth)                     │
│  ├─ PostgreSQL (Production)                                 │
│  └─ Redis (Caching & WebSocket support)                     │
└──────────────────────┬──────────────────────────────────────┘
                       │
        ┌──────────────┴──────────────┐
        │                             │
   ┌────▼─────┐              ┌───────▼────┐
   │PostgreSQL│              │   Redis    │
   │Database  │              │   Cache    │
   └──────────┘              └────────────┘
```

---

## Backend Structure

### 1. **Django Project Configuration** (`auth_project/`)

#### settings.py
- **Security**: DEBUG mode, SECRET_KEY management, ALLOWED_HOSTS
- **Database**: PostgreSQL (Render) with SQLite fallback for dev
- **Authentication**: Django built-in + Allauth for social login
- **Email**: Brevo API (primary) → Gmail SMTP (fallback) → Console (dev)
- **CORS**: Configured for frontend at localhost:3000
- **Channel Layers**: In-memory for WebSocket support
- **Logging**: Console, file, error handlers

**Key Settings**:
```python
INSTALLED_APPS: [
    'django.contrib.admin/auth/contenttypes/sessions/messages/staticfiles/sites',
    'accounts',
    'allauth', 'allauth.account', 'allauth.socialaccount',
    'rest_framework', 'corsheaders'
]

MIDDLEWARE: [
    'corsheaders.middleware.CorsMiddleware',
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware'
]
```

#### urls.py
- Admin: `/admin/`
- Authentication: `/register/`, `/login/`, `/logout/`, `/verify-otp/`, `/forgot-password/`
- User Profiles: `/student-profile/`, `/student-details/`, `/profile/`
- Projects: `/post-project/`, `/project/<id>/`, `/my-projects/`, `/explore-projects/`
- Messaging: `/messages/`, `/chat/<user_id>/`, `/notifications/`
- Social: `/accounts/` (Allauth), `/accounts/profile/` (redirect)
- Connections: `/connect/`, `/accept-connection/`, `/reject-connection/`, `/my-connections/`
- Misc: `/dashboard/`, `/home/`, `/main_home/`, `/find-collaborators/`, `/about/`

#### asgi.py / wsgi.py
- ASGI for WebSocket support (Channels)
- WSGI for production deployment

---

### 2. **Main Application** (`accounts/`)

#### Models (models.py)

**Core User Models:**
- **StudentProfile**: Extended user profile with skills, interests, college, bio, social links
- **OTP**: 6-digit one-time passwords for login/registration/password reset (5-min expiry)
- **Connection**: Friend requests between users (pending/accepted/rejected)

**Messaging Models:**
- **Message**: Direct messages + group chat messages with threading support
- **ChatRoom**: Group chats with multiple members
- **MessageReadStatus**: Track read receipts for scalability
- **MessageFile**: File attachments to messages
- **MessageReaction**: Emoji reactions to messages
- **File**: File uploads with metadata

**Project Models:**
- **Project**: Main project entity (title, desc, technologies, status)
- **ProjectMember**: Users in projects with roles (lead, contributor)
- **ProjectInvitation**: Invites to join projects
- **ProjectTask**: Subtasks within projects (todo/in_progress/review/completed)
- **ProjectMilestone**: Project milestones with completion tracking

**Project Templates:**
- **ProjectTemplate**: Pre-made templates (web, mobile, AI, data science, etc.)
- **TemplateRating**: User ratings of templates
- **TemplateUsageLog**: Tracking when templates are used

**Other Models:**
- **Comment**: Comments on projects with parent-child threading
- **Like**: Likes on projects
- **Share**: Shares of projects
- **Notification**: User notifications
- **Activity**: Activity feed entries
- **University**: Cached university data from RapidAPI

#### Views (views.py & related)

**Authentication Views:**
- `register_view()`: User registration (traditional + OTP verification)
- `login_view()`: Login with email/username + password or OTP
- `logout_view()`: User logout
- `verify_otp_view()`: Verify OTP codes
- `forgot_password_view()`: Request password reset
- `reset_password_view()`: Reset password with OTP
- `resend_otp_view()`: Resend OTP codes
- `social_login_redirect()`: Allauth callback handler

**Profile Views:**
- `student_profile()`: User profile page
- `student_details_view()`: User details (read-only)
- `profile_view()`: Edit own profile

**Project Views:**
- `post_project()`: Create new project (GET form + POST submission)
- `project_detail()`: View project details with comments, likes, members
- `edit_project()`: Edit project (owner only)
- `delete_project()`: Delete project (owner only)
- `my_projects_view()`: User's own projects
- `explore_projects_view()`: Browse all projects (filtered)

**Messaging Views:**
- `message_view()`: Conversation list
- `chat_view()`: Direct message with user

**Navigation & Other:**
- `main()`: Homepage/landing page
- `main_home()`: Main dashboard
- `home_view()`: Home page
- `dashboard_view()`: User dashboard
- `find_collaborators()`: Find users with specific skills
- `about_view()`: About page
- `notifications_view()`: User's notifications
- `mark_notification_read()`: Mark notification as read
- `investor_dashboard()`: Investor-specific dashboard
- `premium_view()` / `upgrade_view()`: Premium features

**Connection Views:**
- `send_connection_request()`: Send friend request
- `accept_connection()`: Accept connection
- `reject_connection()`: Reject connection
- `my_connections()`: View all connections

#### Serializers (serializers.py)
- **UserSerializer**: Basic user data (username, email, first_name, last_name)
- **StudentProfileSerializer**: Profile data including skills, interests, social links
- **ProjectSerializer**: Project data with owner, members, status
- **CommentSerializer**: Comments with user info
- **LikeSerializer**: Like data
- **MessageSerializer**: Message data with sender/receiver
- **NotificationSerializer**: Notification data
- **ConnectionSerializer**: Connection request data

#### API Endpoints (accounts/urls.py)

**REST API Routes:**
```
/api/auth/
  - register/ (POST)
  - login/ (POST)
  - logout/ (POST)
  - verify-otp/ (POST)
  - forgot-password/ (POST)
  - reset-password/ (POST)

/api/user/
  - profile/ (GET, PUT)
  - profile/<id>/ (GET)
  - search/ (GET with q parameter)

/api/projects/
  - (GET all, POST create)
  - <id>/ (GET, PUT, DELETE)
  - <id>/comments/ (GET, POST)
  - <id>/like/ (POST)
  - <id>/unlike/ (POST)
  - <id>/share/ (POST)
  - <id>/members/ (GET, POST)
  - <id>/members/<member_id>/ (DELETE)
  - <id>/invitations/ (GET, POST)
  - <id>/tasks/ (GET, POST)
  - my-projects/ (GET)
  - featured/ (GET)
  - templates/ (GET)

/api/messages/
  - (GET list, POST new)
  - <id>/ (GET, DELETE)
  - <id>/mark-read/ (POST)
  - conversations/ (GET)

/api/connections/
  - (GET list)
  - <id>/accept/ (POST)
  - <id>/reject/ (POST)

/api/notifications/
  - (GET list)
  - <id>/read/ (POST)
```

#### Email Backends
1. **brevo_mail_backend.py**: Brevo API integration for transactional emails
2. **zepto_mail_backend.py**: Alternative Zepto mail backend

#### WebSocket Support
- **consumers.py**: Handles real-time messaging, notifications, activity updates
- **routing.py**: WebSocket routing configuration
- **signals_realtime.py**: Django signals for real-time updates

#### Other Utilities
- **forms.py**: Django forms (registration, login, profile)
- **utils.py**: Helper functions (email, OTP generation, etc.)
- **permissions.py**: DRF custom permissions
- **views_contact.py**: Contact form handling
- **template_api.py**: Project template API endpoints
- **comment_api.py**: Comment-related API endpoints
- **chat_api.py** / **chat_api_improved.py**: Chat/messaging APIs

#### Management Commands
- Data import/export utilities
- Database utilities

---

## Frontend Structure

### Technology Stack
- **Framework**: React 18.2.0 with Vite 5.0.0
- **Routing**: React Router 6.20.0
- **HTTP Client**: Axios 1.6.0
- **Build Tool**: Vite (fast bundling, HMR)
- **Styling**: CSS modules + responsive design

### Project Structure
```
frontend/
├── src/
│   ├── api/              # API utility functions
│   ├── App.jsx           # Main app component with routing
│   ├── App.css           # Global styles
│   ├── main.jsx          # Entry point
│   └── index.css         # CSS resets
├── index.html            # HTML template
├── vite.config.js        # Vite configuration
├── package.json          # Dependencies
├── nginx.conf            # Production nginx config
└── Dockerfile            # Container image
```

### Key Features
- **SPA**: Single Page Application with client-side routing
- **API Integration**: RESTful API calls via Axios
- **Responsive**: Mobile-first design
- **Real-time**: WebSocket integration for live updates
- **Authentication**: Token-based session auth with OAuth

---

## Database Schema

### Key Tables

**Django Auth Tables:**
- `auth_user` (ID, username, email, password_hash, is_active, is_staff, is_superuser)
- `auth_group`, `auth_permission`

**Custom Tables:**
- `accounts_studentprofile` (user_id, full_name, college, skills[], interests[], profile_photo)
- `accounts_otp` (email, otp_code, purpose, is_used, expires_at)
- `accounts_connection` (sender_id, receiver_id, status, created_at)
- `accounts_project` (owner_id, title, description, technologies[], status, created_at)
- `accounts_projectmember` (project_id, user_id, role, joined_at)
- `accounts_message` (sender_id, receiver_id, chat_room_id, content, created_at)
- `accounts_chatroom` (name, chat_type, created_by_id, created_at)
- `accounts_chatroomember` (chat_room_id, user_id, is_active)
- `accounts_notification` (user_id, message, is_read, created_at)
- `accounts_comment` (project_id, user_id, content, parent_id, created_at)
- `accounts_like` (user_id, project_id, created_at)
- `accounts_messagereadstatus` (message_id, user_id, read_at)

---

## Key Features Breakdown

### 1. Authentication System
**Flow:**
1. User enters email/username + password
2. Optional: OTP verification for extra security
3. Allauth handles Google/GitHub OAuth
4. Session tokens created on successful auth
5. Redirect to dashboard

**Files:**
- `views.py`: register_view, login_view, verify_otp_view
- `forms.py`: CustomSocialSignupForm, AuthenticationForm
- `models.py`: OTP model with generation/verification

**Email Delivery:**
- Brevo API (primary) for OTP codes
- Gmail SMTP (fallback)
- Console backend (development)

---

### 2. User Profiles & Discovery
**Features:**
- Extended profiles with skills, interests, college
- Profile completion status
- Social media links (GitHub, LinkedIn, Portfolio, Behance)
- Profile photos with validation
- Skill-based user discovery/search

**Files:**
- `models.py`: StudentProfile
- `serializers.py`: StudentProfileSerializer
- `views.py`: student_profile, profile_view, find_collaborators
- `urls.py`: /student-profile/, /find-collaborators/

---

### 3. Project Management
**Features:**
- Create projects with detailed descriptions
- Specify technologies, roles needed
- Project templates for quick start
- Project lifecycle: idea → active → completed
- Member management with roles (lead, contributor)
- Task tracking within projects
- Milestones for progress tracking

**Models:**
- Project, ProjectMember, ProjectTask, ProjectMilestone
- ProjectTemplate, TemplateRating, TemplateUsageLog

**Views:**
- post_project, project_detail, edit_project, delete_project
- my_projects_view, explore_projects_view

---

### 4. Real-time Messaging & Chat
**Features:**
- Direct messaging between users
- Group chat rooms (team channels)
- Message threading (reply to specific messages)
- File attachments
- Message reactions (emojis)
- Read receipts/read status
- Typing indicators (WebSocket)
- Online status

**Models:**
- Message, ChatRoom, ChatRoomMember
- MessageReadStatus, MessageFile, MessageReaction

**WebSocket:**
- channels.consumers for WebSocket handling
- Real-time message delivery
- Notification broadcasting

**Files:**
- `consumers.py`: WebSocket consumers
- `routing.py`: WebSocket routing
- `chat_api.py`, `chat_api_improved.py`: Chat endpoints
- `signals_realtime.py`: Real-time signal handling

---

### 5. Social Features
**Features:**
- Like projects
- Share projects
- Comment on projects (threaded)
- Project activity feed
- User connections/friendships
- Connection requests with accept/reject

**Models:**
- Like, Share, Comment, Connection
- Notification, Activity

**Views:**
- send_connection_request, accept_connection, reject_connection
- project_detail (includes comments/likes)

---

### 6. Notifications
**Features:**
- Notification center
- Mark as read/unread
- Real-time notification delivery
- Email notifications for important events

**Models:**
- Notification (user_id, message, is_read, created_at)

**Views:**
- notifications_view, mark_notification_read

---

### 7. Admin Panel
**Django Admin Features:**
- User management (create, edit, delete, permissions)
- Project management (approve, feature, delete)
- Template management (create, rate, feature)
- Notification management
- Activity logs
- Email logs

---

## Deployment & Infrastructure

### Environment Variables Required
```
# Security
DEBUG=False
SECRET_KEY=<generated>
ALLOWED_HOSTS=yourdomain.com

# Database
DATABASE_URL=postgresql://user:pass@host:port/db
# OR
DB_NAME=unisinq_db
DB_USER=unisinq_user
DB_PASSWORD=password
DB_HOST=localhost
DB_PORT=5432

# Email
BREVO_API_KEY=<your_key>
DEFAULT_FROM_EMAIL=noreply@unisinq.app
# OR
EMAIL_HOST_USER=your@gmail.com
EMAIL_HOST_PASSWORD=app_password

# OAuth Providers
GOOGLE_CLIENT_ID=<from Google Cloud>
GOOGLE_CLIENT_SECRET=<from Google Cloud>
GITHUB_CLIENT_ID=<from GitHub>
GITHUB_CLIENT_SECRET=<from GitHub>

# CORS & Security
CORS_ALLOWED_ORIGINS=https://yourdomain.com
CSRF_TRUSTED_ORIGINS=https://yourdomain.com
SECURE_SSL_REDIRECT=True
SESSION_COOKIE_SECURE=True
CSRF_COOKIE_SECURE=True

# RapidAPI (Universities)
RAPIDAPI_KEY=<your_key>
RAPIDAPI_HOST=universities-list.p.rapidapi.com
```

### Deployment Options
1. **Railway** (recommended - managed PostgreSQL, Redis)
2. **Render** (similar to Railway)
3. **Heroku** (legacy, deprecating)
4. **Docker** (self-hosted with docker-compose)

### Production Checklist
- [ ] Set DEBUG=False
- [ ] Configure SECRET_KEY
- [ ] Set ALLOWED_HOSTS
- [ ] Configure PostgreSQL
- [ ] Set up Redis
- [ ] Configure email backend (Brevo/Gmail)
- [ ] Set OAuth credentials
- [ ] Enable SSL (SECURE_SSL_REDIRECT=True)
- [ ] Collect static files (`python manage.py collectstatic`)
- [ ] Run migrations (`python manage.py migrate`)
- [ ] Set up Channels for WebSocket
- [ ] Configure nginx/reverse proxy
- [ ] Set up monitoring/logging

---

## Key Technologies & Libraries

### Backend
| Package | Version | Purpose |
|---------|---------|---------|
| Django | 4.2.8 | Web framework |
| djangorestframework | 3.14.0 | REST API |
| django-allauth | 0.61.1 | Social authentication |
| channels | 4.0.0 | WebSocket support |
| channels-redis | 4.1.0 | Redis channel layer |
| psycopg2 | 2.9.9 | PostgreSQL adapter |
| redis | 5.0.1 | Redis client |
| django-cors-headers | 4.3.1 | CORS middleware |
| pillow | 10.0.0 | Image processing |
| nltk | 3.8.1 | NLP (for text analysis) |
| spacy | 3.7.2 | NLP (advanced) |
| scikit-learn | 1.3.2 | Machine learning |
| pandas | 2.0.3 | Data processing |
| gunicorn | 21.2.0 | WSGI server |
| whitenoise | 6.6.0 | Static file serving |

### Frontend
| Package | Version | Purpose |
|---------|---------|---------|
| React | 18.2.0 | UI library |
| react-router-dom | 6.20.0 | Client routing |
| axios | 1.6.0 | HTTP client |
| vite | 5.0.0 | Build tool |

---

## Development Workflow

### Local Setup
```bash
# Clone repository
git clone https://github.com/Goku0090/uni.git
cd uni

# Backend setup
cd backend
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
pip install -r requirements.txt
cp .env.example .env  # Configure environment
python manage.py migrate
python manage.py createsuperuser
python manage.py runserver

# Frontend setup (in separate terminal)
cd frontend
npm install
npm run dev
```

### Running Servers
- **Django**: `python manage.py runserver` (port 8000)
- **Vite**: `npm run dev` (port 5173, proxies to :8000)
- **Daphne** (WebSocket): `daphne -b 0.0.0.0 -p 8000 auth_project.asgi:application`

### Testing
```bash
python manage.py test accounts
```

### Building for Production
```bash
# Backend
gunicorn auth_project.wsgi:application --bind 0.0.0.0:8000

# Frontend
npm run build
# Outputs to dist/
```

---

## Common Patterns & Best Practices

### API Response Format
```json
{
  "success": true,
  "data": { /* response data */ },
  "message": "Success message"
}
```

### Error Handling
```python
try:
    # do something
    return JsonResponse({'success': True, 'data': result})
except Exception as e:
    return JsonResponse({'success': False, 'message': str(e)}, status=400)
```

### WebSocket Message Format
```json
{
  "type": "message_new",
  "content": "...",
  "sender_id": 1,
  "timestamp": "2026-02-16T..."
}
```

### Database Query Patterns
- Use `select_related()` for foreign keys (avoid N+1)
- Use `prefetch_related()` for reverse relationships
- Filter early, select fields later
- Use pagination for large result sets

---

## Performance Considerations

1. **Caching**
   - Redis for session cache, query cache
   - Django cache framework for expensive computations

2. **Database**
   - Indexes on frequently queried fields
   - Connection pooling with `dj-database-url`
   - Lazy loading with `.select_related()` / `.prefetch_related()`

3. **Frontend**
   - Code splitting with Vite
   - Image optimization
   - Lazy loading components

4. **WebSocket**
   - Channel layer with Redis
   - Connection pooling
   - Message queuing for reliability

---

## Security Practices

1. **Authentication**
   - Session-based auth with CSRF protection
   - OTP for sensitive operations
   - OAuth 2.0 for social login

2. **Authorization**
   - Role-based access control (RBAC)
   - Model-level permissions (DRF)
   - View-level decorators (@login_required)

3. **Data Protection**
   - HTTPS enforcement in production
   - Secure cookie flags (HttpOnly, Secure, SameSite)
   - CORS whitelisting
   - SQL injection prevention (Django ORM)
   - XSS protection (template escaping)

4. **Secrets Management**
   - Environment variables for sensitive data
   - No hardcoded credentials
   - `.env` file not committed to git

---

## Troubleshooting Guide

### Common Issues

**Issue**: "Module 'channels' not found"
```bash
pip install channels channels-redis
```

**Issue**: WebSocket connection fails
```bash
# Ensure Channel Layer is configured
# Check CHANNEL_LAYERS in settings.py
# Restart server with Daphne
```

**Issue**: CORS errors on frontend
```python
# Check CORS_ALLOWED_ORIGINS includes frontend URL
CORS_ALLOWED_ORIGINS = ['http://localhost:3000']
```

**Issue**: OTP emails not sending
```python
# Check email backend configuration
# Brevo API Key set: BREVO_API_KEY
# OR Gmail credentials: EMAIL_HOST_USER, EMAIL_HOST_PASSWORD
```

**Issue**: Static files 404
```bash
python manage.py collectstatic --noinput
```

---

## Code Statistics

- **Backend Models**: 20+ (Users, Projects, Messages, Notifications, etc.)
- **Views/Endpoints**: 40+ (Authentication, Projects, Messaging, etc.)
- **API Routes**: 25+ (REST endpoints)
- **Frontend Pages**: Multiple (Dashboard, Projects, Messages, etc.)
- **WebSocket Consumers**: 2-3 (Chat, Notifications, Activity)
- **Total Database Tables**: 40+

---

## Next Steps for Developers

1. Read the models.py to understand data structure
2. Review views.py to understand business logic
3. Check serializers.py for API response formats
4. Test endpoints with Postman/Thunder Client
5. Review templates/ for frontend code
6. Check static/js/ for JavaScript functionality

---

## References

- Django Docs: https://docs.djangoproject.com/
- Django REST Framework: https://www.django-rest-framework.org/
- Django Channels: https://channels.readthedocs.io/
- React: https://react.dev/
- Vite: https://vitejs.dev/
- Allauth: https://django-allauth.readthedocs.io/

---

**Last Updated**: February 16, 2026
**Status**: Production Ready
