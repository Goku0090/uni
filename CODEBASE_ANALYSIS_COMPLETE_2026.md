# UniSync Codebase Analysis - Complete 2026

## Project Overview

**UniSync** is a collaborative student project platform built with **Django** backend and **HTML/CSS/JavaScript** frontend. It enables university students to discover projects, connect with collaborators, manage teams, and communicate in real-time.

---

## Technology Stack

### Backend
- **Framework**: Django 4.2.8
- **API**: Django REST Framework 3.14.0
- **Database**: PostgreSQL (via psycopg2)
- **Authentication**: Django-Allauth 0.61.1 (with Google & GitHub OAuth)
- **Task Queue**: Celery 5.3.4
- **Caching**: Redis 5.0.1
- **Real-time**: Channels 4.0.0, Channels-Redis 4.1.0
- **Email**: Zeptomail 1.0.0 (primary), Brevo (secondary)
- **File Storage**: AWS S3 via Boto3
- **Monitoring**: Sentry-SDK 1.38.0
- **Server**: Gunicorn 21.2.0, Whitenoise 6.6.0

### Frontend
- **Templates**: Django Templates (HTML)
- **JavaScript**: Vanilla JS for interactivity
- **Styling**: CSS with Bootstrap/Crispy Forms
- **Static Files**: Collected via Whitenoise

---

## Project Structure

```
e:/login/auth_project/
├── auth_project/                  # Django project settings
│   ├── settings.py               # Configuration
│   ├── urls.py                   # URL routing
│   ├── wsgi.py                   # WSGI app
│   ├── asgi.py                   # ASGI app (WebSockets)
│   └── __init__.py
│
├── accounts/                      # Main application
│   ├── migrations/                # Database migrations
│   ├── services/                  # Business logic
│   │   └── auth_service.py       # Authentication service
│   ├── static/                    # CSS, JS, images
│   │   └── js/
│   ├── templates/                 # HTML templates
│   ├── templatetags/              # Custom template filters
│   │   └── custom_filters.py
│   │
│   ├── models.py                  # Database models
│   ├── views.py                   # Main view functions
│   ├── views_contact.py           # Contact/Legal page views
│   ├── urls.py                    # App URL patterns
│   ├── forms.py                   # Django forms
│   ├── serializers.py             # DRF serializers
│   ├── permissions.py             # Custom permissions
│   │
│   ├── chat_api.py                # Legacy chat API
│   ├── chat_api_improved.py       # Improved chat API endpoints
│   ├── comment_api.py             # Comment CRUD endpoints
│   ├── utils.py                   # Utility classes
│   │
│   ├── brevo_mail_backend.py      # Email backend (Brevo)
│   ├── zepto_mail_backend.py      # Email backend (Zeptomail)
│   ├── permissions.py             # Permission checks
│   └── tests.py                   # Test cases
│
├── manage.py                      # Django management
├── requirements.txt               # Python dependencies
├── .env                           # Environment variables
└── db.sqlite3                     # Local database (dev only)
```

---

## Core Models

### 1. **StudentProfile**
Extended user profile with college, interests, skills, social links
- Fields: full_name, college, location, bio, profile_photo, skills, project_interests
- Relationships: OneToOne with User

### 2. **OTP (One-Time Password)**
Email-based authentication codes
- Fields: email, otp_code, purpose (login/registration/reset), expires_at
- Methods: generate_otp(), verify_otp(), is_valid()

### 3. **Connection**
Connection requests between users
- Status: pending, accepted, rejected
- ForeignKeys: sender, receiver (User)

### 4. **Message & MessageReadStatus**
Direct messages with read status tracking
- Fields: content, sender, receiver, created_at, is_read
- Related: MessageFile, MessageReaction

### 5. **Project**
Collaborative project listings
- Fields: title, description, owner, team_members, visibility (public/private/draft)
- Related: ProjectTeam, ProjectTask, ProjectMilestone, Comment, Activity

### 6. **Comment**
Project and activity comments
- Fields: content, author, project, created_at, updated_at
- Methods: get_comments(), add_comment(), edit_comment(), delete_comment()

### 7. **Notification**
User notifications for activities
- Fields: user, notification_type, message, is_read, created_at
- Triggers: connections, project updates, comments, messages

### 8. **ChatRoom & ChatRoomMember**
Group chat functionality
- ChatRoom: name, members (ManyToMany via ChatRoomMember)
- ChatRoomMember: user, room, join_date

### 9. **Activity & Follow & Like**
Social features for projects
- Activity: user action tracking
- Follow: user follows projects/people
- Like: project/comment likes

### 10. **ProjectTeam, ProjectTask, ProjectMilestone**
Project management
- ProjectTeam: collaborative team with members
- ProjectTask: individual tasks with status
- ProjectMilestone: project phases/deadlines

---

## Key Features

### 1. Authentication & Authorization
**Files**: `views.py`, `auth_service.py`, `permissions.py`

- **Email OTP Login**: Generate 6-digit OTP, send via email, verify
- **Social Login**: Google & GitHub OAuth via Django-Allauth
- **Token-based API**: DRF TokenAuthentication
- **Permission Classes**: IsChatRoomMember, IsProjectOwnerOrTeamMember
- **Decorators**: check_chat_membership(), check_project_owner(), check_team_ownership()

**Key Functions**:
```python
send_otp_email(email, otp_code, purpose)  # Send OTP via email
register_view(request)                    # New user registration
login_view(request)                       # Email/password login
```

### 2. Project Management
**Files**: `views.py`, `serializers.py`, `comment_api.py`

- **Create/Edit Projects**: StudentProfileForm, ProjectForm
- **Visibility Control**: Public, Private (for team only), Draft
- **Team Management**: Invite members, manage roles
- **Project Tasks**: Create subtasks with status tracking
- **Milestones**: Set deadlines and phases
- **Comments**: Add comments to projects (live feed)
- **Activity Log**: Track all project changes

**Key Functions**:
```python
def project_feed(request)          # Display all projects
def search_projects(request)       # Search & filter projects
def add_comment(request, project_id)       # Add project comment
def get_comments(request, project_id)      # Fetch comments
def edit_comment(request, comment_id)      # Update comment
def delete_comment(request, comment_id)    # Remove comment
```

### 3. Direct Messaging
**Files**: `chat_api_improved.py`, `views.py`

- **One-on-One Messages**: Send/receive direct messages
- **Group Chat**: ChatRoom with multiple members
- **Message Status**: Track read/unread status
- **Drafts**: Save draft messages
- **Typing Indicator**: Real-time typing notifications
- **File Sharing**: Attach files to messages
- **Message Reactions**: Emoji reactions on messages

**Key API Endpoints**:
```
POST   /api/messages/                    # Send message
GET    /api/messages/                    # List messages
POST   /api/chat-rooms/                  # Create chat room
GET    /api/chat-rooms/                  # List rooms
POST   /api/messages/{id}/status/        # Mark as read
```

### 4. Notifications
**Files**: `views.py`, `models.py`

- **Real-time Updates**: Connection requests, project invites
- **Message Notifications**: Unread message count
- **Project Updates**: Comments, team changes, task updates
- **Activity Feed**: Follow updates from connected users

### 5. User Profiles
**Files**: `views.py`, `serializers.py`, `edit_profile` view

- **Profile Completion**: Full name, college, bio, photo
- **Skills & Interests**: Searchable tags
- **Social Links**: GitHub, LinkedIn, Portfolio, Behance
- **Profile Photo Upload**: Image validation & storage
- **Public Profile View**: View other users' profiles

### 6. Search & Discovery
**Files**: `views.py`, `utils.py`

- **Project Search**: By title, description, collaboration needs
- **User Search**: Find collaborators by skills/interests
- **Filtering**: By college, role, technology stack
- **NLP-Based Matching**: StudentProfileNLP class for skill matching

**Key Class**:
```python
class StudentProfileNLP:
    # Extract skills/interests from text
    # Match projects to users
    # Recommend collaborators
```

### 7. Project Visibility Filter
**Files**: `utils.py`

```python
class ProjectVisibilityFilter:
    # Filter projects based on user permissions
    # Public: visible to all
    # Private: visible to team only
    # Draft: visible to owner only
```

---

## API Endpoints Reference

### Authentication
```
POST   /api/auth/register/         # Register new user
POST   /api/auth/login/            # Login with email/password
POST   /api/auth/otp/send/         # Request OTP
POST   /api/auth/otp/verify/       # Verify OTP and login
POST   /api/auth/logout/           # Logout user
POST   /api/auth/password-reset/   # Request password reset
```

### User Profile
```
GET    /api/users/{id}/            # Get user profile
PUT    /api/users/{id}/            # Update profile
GET    /api/users/{id}/projects/   # Get user's projects
POST   /api/users/{id}/follow/     # Follow user
POST   /api/users/{id}/unfollow/   # Unfollow user
```

### Projects
```
GET    /api/projects/              # List all projects
POST   /api/projects/              # Create project
GET    /api/projects/{id}/         # Get project details
PUT    /api/projects/{id}/         # Update project
DELETE /api/projects/{id}/         # Delete project
GET    /api/projects/{id}/comments/ # Get comments
```

### Comments
```
POST   /api/comments/              # Add comment
GET    /api/comments/?project={id} # Get project comments
PUT    /api/comments/{id}/         # Edit comment
DELETE /api/comments/{id}/         # Delete comment
```

### Messages & Chat
```
GET    /api/messages/              # List messages
POST   /api/messages/              # Send message
GET    /api/messages/{id}/         # Get message detail
PUT    /api/messages/{id}/         # Edit message
DELETE /api/messages/{id}/         # Delete message

GET    /api/chat-rooms/            # List chat rooms
POST   /api/chat-rooms/            # Create room
GET    /api/chat-rooms/{id}/members/ # Room members
POST   /api/messages/{id}/status/  # Mark as read
```

### Connections
```
POST   /api/connections/send/      # Send connection request
POST   /api/connections/{id}/accept/ # Accept request
POST   /api/connections/{id}/reject/ # Reject request
GET    /api/connections/           # Get connections
```

### Notifications
```
GET    /api/notifications/         # Get notifications
POST   /api/notifications/{id}/read/ # Mark as read
DELETE /api/notifications/{id}/    # Delete notification
```

---

## Views Breakdown

### Main Views (`views.py`)
- **project_feed()**: Display projects with pagination
- **edit_profile()**: Update user profile
- **search_projects()**: Search and filter projects
- **dashboard_view()**: User dashboard
- **register_view()**: User registration with profile creation
- **login_view()**: Email/password login with OTP
- **verify_otp_view()**: Verify OTP code

### Contact/Legal Views (`views_contact.py`)
- **privacy_policy_view()**: Display privacy policy
- **terms_of_service_view()**: Display terms of service
- **contact_us_view()**: Contact form page
- **contact_submit()**: Process contact form submission

### Chat API (`chat_api_improved.py`)
- **ChatRoomListCreateView**: Create and list chat rooms
- **ChatRoomDetailView**: Get, update, delete chat room
- **ChatRoomMembersView**: List room members
- **DirectMessageView**: Send direct message
- **MessageListCreateView**: List and create messages
- **MessageDetailView**: Get, update, delete message
- **MessageStatusView**: Mark message as read
- **TypingIndicatorView**: Send typing status

### Comment API (`comment_api.py`)
- **add_comment()**: Create comment on project
- **get_comments()**: Fetch project comments
- **edit_comment()**: Update comment
- **delete_comment()**: Remove comment

---

## Forms

### Authentication Forms
- **RegisterForm**: User registration with email validation
- **LoginForm**: Email/password login form
- **OTPVerificationForm**: OTP code verification

### Profile Forms
- **StudentProfileForm**: Edit profile (name, college, bio, photo, skills)
- **ProjectForm**: Create/edit project details

### Other Forms
- **CustomSocialSignupForm**: Social login data collection
- **CommentForm**: Add comments to projects
- **ContactForm**: Contact/feedback submission

---

## Serializers (DRF)

- **UserProfileSerializer**: Serialize StudentProfile
- **ProjectSerializer**: Serialize Project with related data
- **MessageSerializer**: Serialize Message and read status
- **ConnectionSerializer**: Serialize connection requests
- **NotificationSerializer**: Serialize notifications

---

## Email Backends

### Zeptomail Backend (`zepto_mail_backend.py`)
- Primary email provider
- Used for OTP, password reset, notifications
- Configuration via environment variables

### Brevo Backend (`brevo_mail_backend.py`)
- Secondary email provider
- Fallback option for email delivery
- Marketing emails

---

## Utilities & Helpers

### StudentProfileNLP (`utils.py`)
NLP-based profile analysis:
- Extract skills and interests from text
- Match projects to user skills
- Recommend collaborators
- Analyze project descriptions

### ProjectVisibilityFilter (`utils.py`)
Project access control:
- Public: visible to all authenticated users
- Private: visible to team members only
- Draft: visible to owner only

### Custom Template Filters (`templatetags/custom_filters.py`)
- `split`: Split strings by delimiter
- `get_item`: Get dictionary values in templates
- `strip`: Remove whitespace

---

## Frontend Templates

### Main Templates
- **base.html**: Base layout with navbar, footer
- **main.html**: Dashboard/home page
- **main_home.html**: Landing page
- **login.html**: Login form with email/OTP
- **register.html**: Registration form
- **verify_otp.html**: OTP verification page

### User Pages
- **profile.html**: User profile view
- **edit_profile.html**: Profile editing page
- **my_connections.html**: User connections list

### Project Pages
- **project_detail.html**: Single project view with comments
- **project_feed.html**: Project listing/feed
- **search_projects.html**: Project search interface

### Communication
- **messages.html**: Direct messaging interface
- **chat_room.html**: Group chat interface

### Other Pages
- **terms_of_service.html**: ToS page
- **privacy.html**: Privacy policy page
- **contact.html**: Contact form page
- **upgrade.html**: Premium features page

---

## Static Files & Assets

### JavaScript Files
- **login.js**: Login form validation & OTP handling
- **register_validation.js**: Registration form validation
- **profile.js**: Profile editing functionality
- **password_validation.js**: Password strength checking
- **college_autocomplete.js**: College autocomplete
- **api-utils.js**: API utility functions

### CSS & Styling
- Bootstrap 5 for responsive design
- Crispy Forms for form rendering
- Custom CSS for branding

---

## Security Features

### Authentication
- Email OTP verification
- Social OAuth (Google, GitHub)
- Password hashing with Django's default
- Session-based authentication

### Authorization
- Permission classes for API endpoints
- Object-level permissions (project ownership)
- Role-based access (team member, owner)

### CSRF Protection
- CSRF middleware enabled
- CSRF tokens in forms

### Other Security
- Input validation and sanitization
- SQL injection protection (Django ORM)
- XSS protection
- Environment variable configuration

---

## Email Configuration

### OTP Email (`send_otp_email`)
Sends 6-digit OTP code to user's email
- Purpose: registration, login, password reset
- Expiry: 5 minutes
- Template: HTML email with OTP code

### Password Reset
Sends password reset link to email

### Notifications
Sends activity notifications to users

---

## Caching & Performance

### Redis Configuration
```python
CACHES = {
    'default': {
        'BACKEND': 'django_redis.cache.RedisCache',
        'LOCATION': 'redis://...',
    }
}
```

### Cache Usage
- User profiles (30 minutes)
- Project listings (15 minutes)
- Search results (5 minutes)

### Database Optimization
- Select_related for foreign keys
- Prefetch_related for reverse relations
- Database indexing on frequently queried fields

---

## Deployment Configuration

### Render.com / Railway
- **Database**: PostgreSQL hosted
- **Redis**: Redis cache service
- **Environment**: Production environment variables
- **Static Files**: Whitenoise with S3 storage

### Procfile
```
web: gunicorn auth_project.wsgi
```

### Environment Variables (.env)
```
DEBUG=False
SECRET_KEY=<production-key>
DATABASE_URL=postgres://...
ALLOWED_HOSTS=your-domain.com
SECURE_SSL_REDIRECT=True
SESSION_COOKIE_SECURE=True
CSRF_COOKIE_SECURE=True
```

---

## Testing

### Test Files
- `test_login.py`: Login functionality
- `test_filter.py`: Project filtering
- `test_comments_api.py`: Comment endpoints
- `test_profile_fix.py`: Profile editing
- `test_connections.py`: Connection requests

### Test Commands
```bash
python manage.py test                    # Run all tests
pytest                                   # Run with pytest
pytest -v accounts/tests.py              # Specific tests
```

---

## Common Issues & Fixes

### Issue: Comments not visible
**Fix**: Clear cache, verify Comment model migration

### Issue: OTP not sending
**Fix**: Check email backend configuration, verify API keys

### Issue: Profile photo not uploading
**Fix**: Check media directory permissions, verify Pillow installation

### Issue: Projects not showing in feed
**Fix**: Apply ProjectVisibilityFilter, verify user permissions

---

## Development Workflow

### Setup
```bash
python -m venv venv
source venv/bin/activate  # or venv\Scripts\activate on Windows
pip install -r requirements.txt
python manage.py migrate
python manage.py runserver
```

### Database Operations
```bash
python manage.py makemigrations    # Create migration
python manage.py migrate            # Apply migration
python manage.py createsuperuser    # Create admin user
python manage.py dumpdata > backup.json
python manage.py loaddata backup.json
```

### Static Files
```bash
python manage.py collectstatic      # Collect static files
```

---

## Key Dependencies & Their Purpose

| Package | Purpose |
|---------|---------|
| Django 4.2.8 | Web framework |
| djangorestframework | API framework |
| django-allauth | Social authentication |
| psycopg2 | PostgreSQL driver |
| Channels | WebSocket support |
| Celery | Task queue |
| Redis | Caching & message broker |
| Pillow | Image processing |
| NLTK | NLP for skill matching |
| Boto3 | AWS S3 storage |
| Sentry | Error tracking |
| Gunicorn | Production server |

---

## Future Enhancement Areas

1. **Real-time Notifications**: Implement WebSocket notifications
2. **Advanced Search**: Elasticsearch for full-text search
3. **AI Recommendations**: ML-based project/collaborator matching
4. **Video Conferencing**: Integrate Jitsi or similar
5. **Progress Tracking**: Better milestone/task management
6. **Analytics**: User activity and project metrics
7. **API Documentation**: Auto-generated Swagger/OpenAPI docs
8. **Rate Limiting**: API rate limiting for protection
9. **Payment Integration**: Premium features with Stripe
10. **Mobile App**: React Native mobile application

---

## Monitoring & Logging

### Sentry Integration
Error tracking for production issues
```python
import sentry_sdk
sentry_sdk.init(dsn=SENTRY_DSN)
```

### Logging Configuration
```python
logger = logging.getLogger(__name__)
logger.error("Error message")
logger.info("Info message")
```

### Performance Monitoring
- Database query monitoring
- Slow query logging
- API response time tracking

---

## Summary

UniSync is a comprehensive student collaboration platform with:
- ✅ Multi-auth (Email OTP, OAuth)
- ✅ Project management with teams
- ✅ Real-time messaging & chat
- ✅ Comments & activity feeds
- ✅ Connection management
- ✅ Advanced search & filtering
- ✅ Responsive frontend
- ✅ Production-ready deployment
- ✅ Monitoring & error tracking
- ✅ Scalable architecture

The codebase is well-organized, follows Django best practices, and implements modern web development patterns for both backend and frontend.
