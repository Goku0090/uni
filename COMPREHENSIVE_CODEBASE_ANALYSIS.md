# UniSync - Comprehensive Codebase Analysis

## Overview

UniSync is a Django-based collaboration platform connecting university students to form projects and teams. It's a full-stack application with authentication, social features, messaging, and project management capabilities.

---

## Architecture Stack

### Technology Stack
- **Backend Framework**: Django 4.2.8
- **API Framework**: Django REST Framework 3.14.0
- **Database**: PostgreSQL (with SQLite fallback for development)
- **Authentication**: Django Allauth (local + social OAuth: Google, GitHub)
- **Real-time Features**: Django Channels, Redis
- **Email Services**: Brevo (primary), ZeptoMail (fallback), Gmail SMTP
- **Storage**: AWS S3 via boto3, WhiteNoise for static files
- **Task Queue**: Celery with Redis
- **Frontend**: HTML/CSS/JavaScript templates (Django templates)

### Key Dependencies
```
Django==4.2.8
djangorestframework==3.14.0
django-allauth==0.61.1
channels==4.0.0
celery==5.3.4
redis==5.0.1
psycopg2-binary==2.9.9
Pillow==10.1.0 (image processing)
pandas==2.1.4 (data handling)
nltk==3.8.1 (NLP)
```

---

## Core Application Structure

### Directory Layout

```
auth_project/                       # Django Project Root
├── auth_project/                   # Project Configuration
│   ├── settings.py                 # Django settings
│   ├── urls.py                     # URL routing
│   ├── wsgi.py                     # WSGI application
│   └── asgi.py                     # ASGI application (Channels)
│
├── accounts/                       # Main Application
│   ├── models.py                   # Database models
│   ├── views.py                    # View logic (3300+ lines)
│   ├── urls.py                     # URL patterns
│   ├── forms.py                    # Form definitions
│   ├── serializers.py              # DRF serializers
│   ├── permissions.py              # Custom permissions
│   ├── utils.py                    # Utility functions
│   │
│   ├── services/                   # Business Logic Services
│   │   ├── auth_service.py         # Authentication service
│   │   └── __init__.py
│   │
│   ├── chat_api.py                 # Chat/Messaging API
│   ├── comment_api.py              # Comments API
│   ├── views_contact.py            # Contact form views
│   │
│   ├── brevo_mail_backend.py       # Brevo email backend
│   ├── zepto_mail_backend.py       # ZeptoMail backend
│   │
│   ├── templates/                  # HTML templates
│   ├── static/                     # CSS, JS, images
│   ├── migrations/                 # Database migrations
│   └── templatetags/               # Custom template filters
│
├── media/                          # User uploads (profile photos)
├── static/                         # Global static files
├── logs/                           # Application logs
│
├── manage.py                       # Django CLI
└── requirements.txt                # Python dependencies
```

---

## Database Models

### Core Models

#### 1. **StudentProfile**
User extended profile with academic and professional information.

```python
StudentProfile
├── user (OneToOneField → User)
├── full_name, college, location
├── interests, bio, skills, project_interests
├── profile_photo (ImageField)
├── Social links: github, linkedin, portfolio, behance
├── role_preference, profile_completed
└── Timestamps: created_at, updated_at
```

#### 2. **OTP** (One-Time Password)
Authentication via email OTP for login/registration.

```python
OTP
├── email, otp_code (6-digit)
├── purpose (login/registration/reset)
├── is_used, created_at, expires_at
└── Methods: is_valid(), verify_otp(), generate_otp()
```

#### 3. **Project**
Main content model for collaborative projects.

```python
Project
├── owner (ForeignKey → User)
├── title, description, collaboration_needs
├── team (ManyToManyField → User)
├── technologies (JSONField array)
├── status (active/completed/paused)
├── visibility (public/private/college_specific)
├── likes_count, comments_count
├── File attachments, images
└── Timestamps: created_at, updated_at
```

#### 4. **Connection**
User relationship and connection requests.

```python
Connection
├── sender, receiver (ForeignKey → User)
├── status (pending/accepted/rejected)
├── Unique: (sender, receiver)
└── Timestamps: created_at, updated_at
```

#### 5. **Message**
Direct messaging between users.

```python
Message
├── sender, recipient (ForeignKey → User)
├── content (TextField)
├── is_read (BooleanField)
├── has_files (BooleanField)
└── Timestamps: sent_at, read_at
```

#### 6. **ChatRoom**
Group chat functionality.

```python
ChatRoom
├── name, description
├── owner (ForeignKey → User)
├── members (ManyToManyField → User via ChatRoomMember)
├── is_group (BooleanField)
├── last_activity
└── Timestamps: created_at, updated_at
```

#### 7. **Comment**
Project comments/discussion.

```python
Comment
├── project (ForeignKey → Project)
├── author (ForeignKey → User)
├── content (TextField)
├── likes_count
├── is_edited, edited_at
└── Timestamps: created_at, updated_at
```

#### 8. **Notification**
User notifications for activities.

```python
Notification
├── user (ForeignKey → User)
├── actor (ForeignKey → User)
├── action_type (like/comment/follow/connect)
├── content_type (Project/Comment/User)
├── object_id, is_read
└── Timestamps: created_at
```

#### 9. **Activity**
Activity feed tracking user actions.

```python
Activity
├── user (ForeignKey → User)
├── action_type (project_posted/project_liked/comment_added)
├── description
├── Timestamps: timestamp
```

#### 10. **Follow**
User following relationships.

```python
Follow
├── follower, following (ForeignKey → User)
├── Unique: (follower, following)
└── Timestamps: created_at
```

#### 11. **ProjectTeam**
Team management for projects.

```python
ProjectTeam
├── project (ForeignKey → Project)
├── name, description
├── team_lead (ForeignKey → User)
├── members (ManyToManyField → User via ProjectTeamMember)
├── max_members, status
└── Timestamps: created_at, updated_at
```

#### 12. **MessageFile**
File attachments in messages.

```python
MessageFile
├── message (ForeignKey → Message)
├── file (FileField)
├── file_type (document/image/other)
├── file_size
└── Timestamps: uploaded_at
```

### Supporting Models
- **Notification**: Activity notifications
- **Like**: Project/Comment likes
- **UserStatus**: Online/offline status
- **MessageReadStatus**: Message read tracking
- **Draft**: Message drafts
- **UserStats**: User statistics
- **File**: General file model
- **MessageReaction**: Emoji reactions on messages
- **ProjectTask**: Task management within projects
- **ProjectMilestone**: Project milestones
- **ProjectTeamInvitation**: Team invite management

---

## Key Views & Functionality

### Authentication Views

#### Login/Registration
- `login_view()`: OTP-based or username/password login
- `register_view()`: User registration with email verification
- `verify_otp_view()`: OTP verification for login/registration
- `resend_otp_view()`: Resend OTP functionality

#### Password Management
- `forgot_password_view()`: Initiate password reset
- `reset_password_view()`: Complete password reset with OTP

### Profile Management
- `edit_profile()`: Update user profile information
- `student_profile()`: View user's own profile
- `student_details_view()`: Detailed profile view
- `user_profile()`: View other user's profile
- `user_profile_api()`: REST API endpoint for user profile

### Project Management
- `post_project()`: Create new project
- `project_detail()`: View project details
- `edit_project()`: Modify project
- `delete_project()`: Remove project
- `search_projects()`: Search and filter projects

### Social Features
- `find_collaborators()`: Discover and filter users by interests/skills
- `connect_view()`: Send connection request
- `accept_connection()`: Accept connection
- `reject_connection()`: Reject connection
- `follow_user()`: Follow a user
- `my_connections()`: View user's connections

### Messaging
- `message_view()`: Message inbox
- `chat_view()`: Direct chat with user
- `enhanced_messages_view()`: Enhanced messaging UI
- `create_group_chat()`: Create group chat room

### Notifications & Feed
- `notifications_view()`: User notifications
- `activity_feed()`: Activity feed
- `dashboard_view()`: User dashboard

### Comments & Interactions
- `like_project()`: Like a project
- `add_comment()`: Add comment to project
- `delete_comment()`: Remove comment
- `edit_comment()`: Modify comment

### Utility Endpoints
- `college_search_api()`: Search colleges (RapidAPI)
- `check_username_availability()`: Validate username
- `check_email_availability()`: Validate email
- `nlp_analyze_api()`: NLP analysis for projects

---

## REST API Architecture

### Chat API Endpoints (chat_api.py)
```
POST   /chat-rooms/                    - Create chat room
GET    /chat-rooms/                    - List chat rooms
GET    /chat-rooms/<id>/               - Get room details
GET    /chat-rooms/<room_id>/members/  - Get room members
POST   /messages/                      - Create message
GET    /messages/                      - List messages
GET    /messages/<pk>/                 - Get message detail
GET    /messages/search/               - Search messages
GET    /messages/<id>/status/          - Get message status
POST   /messages/<id>/reactions/       - Add reaction

POST   /drafts/                        - Save draft
POST   /typing/                        - Send typing indicator
GET    /conversations/                 - List conversations
POST   /direct-message/                - Send direct message
```

### Comment API Endpoints (comment_api.py)
```
GET    /projects/<id>/comments/        - Get comments
POST   /projects/<id>/comments/add/    - Add comment
DELETE /comments/<id>/delete/          - Delete comment
PUT    /comments/<id>/edit/            - Edit comment
```

### Legacy API Endpoints (views.py)
```
GET    /                               - API root
GET    /home/                          - Home feed
GET    /check-username/                - Username availability
GET    /check-email/                   - Email availability
GET    /user-stats/                    - User statistics
GET    /user-profile/<id>/             - User profile
POST   /nlp-analyze/                   - NLP analysis
GET    /college-search/                - College search
GET    /validate-college/              - Validate college
```

---

## Email System

### Architecture
Multi-backend email support with automatic fallback:

1. **Brevo** (Primary)
   - Production-ready API
   - Transactional email
   - Backend: `accounts.brevo_mail_backend.BrevoMailBackend`

2. **ZeptoMail** (Alternative)
   - RESTful API
   - Backend: `accounts.zepto_mail_backend.ZeptoMailBackend`

3. **Gmail SMTP** (Fallback)
   - Standard SMTP
   - Backend: `django.core.mail.backends.smtp.EmailBackend`

4. **Console** (Development)
   - Prints to console
   - Backend: `django.core.mail.backends.console.EmailBackend`

### Email Types
- OTP codes (login, registration, password reset)
- Welcome emails
- Notification emails
- Password reset confirmation

---

## Authentication System

### Methods
1. **OTP-based Login**
   - Email OTP (6-digit, 5-minute expiry)
   - No password storage required
   - Process: Generate → Send Email → Verify → Login

2. **Traditional Login**
   - Username/password authentication
   - Django's `ModelBackend`

3. **Social OAuth**
   - Google OAuth 2.0 (via django-allauth)
   - GitHub OAuth (via django-allauth)
   - Auto-signup on first login

### Flow
```
User Registration
├── Email verification via OTP
├── Profile creation (StudentProfile)
├── Add academic details (college, interests)
└── Ready to use

User Login
├── OTP-based: Email → OTP → Verify
├── Password-based: Username → Password → Verify
└── Social: OAuth → Allauth → Auto-signup/login
```

---

## Key Features

### 1. Project Discovery & Management
- Create projects with description, needs, technologies
- Public/private/college-specific visibility
- Rich text editor for descriptions
- File attachments and images
- Like and comment on projects
- Project team management with invitations

### 2. User Collaboration
- Find collaborators by interests/skills/college
- Connection requests (pending/accepted/rejected)
- User profiles with portfolio links
- Follow other users
- Activity feed tracking

### 3. Messaging System
- Direct messages between users
- Group chats
- Message reactions (emojis)
- File sharing in messages
- Message read status
- Typing indicators
- Draft messages

### 4. Comments & Discussions
- Comments on projects
- Edit and delete comments
- Like comments
- Real-time comment updates

### 5. Notifications
- Activity-based notifications
- Like/comment/follow notifications
- Connection request notifications
- Real-time updates (via Channels/WebSockets)

### 6. User Profiles
- Extended student profile
- Skills and interests
- Portfolio links (GitHub, LinkedIn, Behance)
- Profile pictures
- Bio and role preference
- Profile completion status

---

## Security Features

### Implemented
- ✅ CSRF Protection (enabled in middleware)
- ✅ Password validation (minimum length, complexity)
- ✅ Email verification via OTP
- ✅ Session authentication
- ✅ User permissions (login_required decorators)
- ✅ Input sanitization (XSS prevention)
- ✅ Secure cookie settings (configurable SSL)

### Configuration
```python
CSRF_COOKIE_SECURE = False (dev) / True (prod)
SESSION_COOKIE_SECURE = False (dev) / True (prod)
SECURE_SSL_REDIRECT = False (dev) / True (prod)
```

---

## Performance Optimizations

### Caching
- Redis-backed caching
- Page-level caching with `@cache_page` decorator
- Query optimization with `select_related()` and `prefetch_related()`

### Database
- PostgreSQL with connection pooling (conn_max_age=600)
- Indexed lookups on frequently queried fields
- Pagination for large datasets (default 10 items/page)

### Static Files
- WhiteNoise for efficient static file serving
- Compression enabled
- CDN-ready with cloud storage (S3) support

---

## Configuration & Environment

### Environment Variables
```
# Security
DEBUG=True (dev) / False (prod)
SECRET_KEY=<auto-generated or set>
ALLOWED_HOSTS=localhost,127.0.0.1

# Database
DATABASE_URL=<PostgreSQL URL>
DB_NAME=unisync_db
DB_USER=unisync_user
DB_PASSWORD=***
DB_HOST=localhost
DB_PORT=5432

# Email
BREVO_API_KEY=<API key>
ZEPTO_MAIL_API_KEY=<API key>
ZEPTO_MAIL_TOKEN=<token>
EMAIL_HOST_USER=***
EMAIL_HOST_PASSWORD=***
DEFAULT_FROM_EMAIL=noreply@unisync.app

# Social Auth
GOOGLE_CLIENT_ID=***
GOOGLE_CLIENT_SECRET=***
GITHUB_CLIENT_ID=***
GITHUB_CLIENT_SECRET=***

# External APIs
RAPIDAPI_KEY=<API key>
```

---

## Deployment Configuration

### Supported Platforms
- **Render**: PostgreSQL + gunicorn deployment
- **Railway**: Cloud deployment support
- **Local Development**: SQLite fallback

### WSGI & ASGI
- WSGI: `auth_project.wsgi.application` (HTTP)
- ASGI: `auth_project.asgi.application` (WebSockets)

### Static Files
- Collected to `staticfiles/` directory
- Served via WhiteNoise
- S3 cloud storage option available

---

## Testing & Monitoring

### Testing Tools
- pytest, pytest-django
- Selenium for integration testing
- Manual test scripts provided

### Logging
- Console logging
- File-based rotating logs (10 MB max)
- Separate error log file
- Sentry integration available

### Performance Monitoring
- django-performance-monitor
- Logging of slow queries
- Activity tracking

---

## Key Business Logic

### Project Visibility Filter
`ProjectVisibilityFilter` in `utils.py` handles:
- Public projects (visible to all)
- Private projects (only owner)
- College-specific projects (college members only)

### User Collaboration NLP
`StudentProfileNLP` in `utils.py`:
- Analyzes user interests and skills
- Matches compatible collaborators
- Project recommendation engine

### Connection Status
- Pending: Initial request sent
- Accepted: Mutual connection established
- Rejected: Request declined

---

## Frontend Integration

### Templates Directory
- Main templates in parent directory: `templates/`
- App-specific templates in `accounts/templates/`

### Static Files
- CSS: `accounts/static/css/`
- JavaScript: `accounts/static/js/`
- Images: `accounts/static/images/`

### Context Processors
- User authentication context
- Messages context
- Site framework context

---

## Error Handling

### Decorator Pattern
```python
@handle_view_errors
def view_function(request):
    # Automatic exception catching
    # User-friendly error messages
    # Logging of errors
```

### 404/403 Handling
- Custom error pages
- Proper HTTP status codes
- Redirect to dashboard on error

---

## API Design Patterns

### REST Framework Usage
- Generic views: `ListCreateAPIView`, `RetrieveUpdateDestroyAPIView`
- Pagination: 10 items default
- Filtering: SearchFilter, OrderingFilter
- Authentication: Session-based
- Permissions: Flexible, can be restricted per-view

### Serializers
- Used for API responses
- `UserProfileSerializer`: User profile API
- Custom serializers for Chat, Message, Comment

---

## Known Issues & Fixes Applied

### Fixed Issues
- ✅ CSRF token warnings (re-enabled CSRF protection)
- ✅ Comments not visible (API endpoint fixes)
- ✅ Profile picture not appearing (file path corrections)
- ✅ Collaborators not showing (visibility filter corrections)
- ✅ Project detail loading performance (query optimization)
- ✅ Login form validation (form error handling)
- ✅ Email configuration fallback (multi-backend support)

---

## Code Quality Standards

### Applied
- Type hints in utility functions
- Docstrings for major functions
- Input sanitization
- Error handling with try-except
- Logging throughout application
- Comments for complex logic

### Tools
- Black (code formatting)
- Flake8 (linting)
- isort (import sorting)
- mypy (type checking)

---

## Future Enhancement Opportunities

1. **Real-time Notifications**
   - WebSocket integration with Channels
   - Redis pub/sub for scalability

2. **Advanced Search**
   - Elasticsearch integration
   - Full-text search on projects/users

3. **Analytics**
   - User engagement tracking
   - Project success metrics
   - Recommendation engine improvements

4. **AI Features**
   - Skill matching
   - Project recommendations
   - Intelligent notifications

5. **Scalability**
   - Database replication
   - Caching layer optimization
   - Load balancing
   - Microservices architecture (future)

---

## Summary

UniSync is a well-structured Django application with:
- ✅ Modular architecture with separated concerns
- ✅ Comprehensive model design for collaborative features
- ✅ Multi-backend email system for reliability
- ✅ REST API for modern frontend integration
- ✅ Security best practices implemented
- ✅ Performance optimizations in place
- ✅ Flexible authentication (OTP + OAuth)
- ✅ Real-time communication ready (Channels)
- ✅ Production-ready deployment configuration

The codebase is well-documented, tested, and ready for scaling.
