# UniSync - Comprehensive Code Analysis

## Project Overview
**UniSync** is a Django-based collaboration platform for students to find collaborators, work on projects together, and manage professional networking.

**Repository**: https://github.com/Goku0090/uni  
**Tech Stack**: Django 4.2.8 + PostgreSQL + Django REST Framework + Channels (WebSockets)

---

## Architecture Summary

### Technology Stack
| Component | Technology |
|-----------|-----------|
| **Backend Framework** | Django 4.2.8 |
| **REST API** | Django REST Framework 3.14.0 |
| **Database** | PostgreSQL (Production) / SQLite (Dev) |
| **Real-time** | Django Channels 4.0.0 + Redis |
| **Authentication** | django-allauth 0.61.1 (OAuth2, Social Login) |
| **Email** | ZeptoMail + Brevo (SMTP) |
| **File Storage** | AWS S3 (boto3) |
| **Caching** | Redis 5.0.1 |
| **Task Queue** | Celery 5.3.4 |
| **Frontend** | Django Templates + JavaScript + Bootstrap |
| **Performance** | django-performance-monitor, Sentry |

---

## Core Directory Structure

```
auth_project/                    # Main Django project
├── accounts/                    # Primary app
│   ├── models.py              # 13+ database models
│   ├── views.py               # 100+ view functions
│   ├── serializers.py         # REST API serializers
│   ├── urls.py                # API routes
│   ├── forms.py               # Django forms
│   ├── permissions.py         # DRF custom permissions
│   ├── utils.py               # Utility functions
│   ├── services/
│   │   ├── auth_service.py    # Authentication logic
│   ├── chat_api.py            # Real-time messaging
│   ├── comment_api.py         # Nested comments
│   ├── brevo_mail_backend.py  # Brevo email backend
│   ├── zepto_mail_backend.py  # ZeptoMail backend
│   ├── templates/             # 55+ HTML templates
│   ├── static/               # CSS, JavaScript, Images
│   └── migrations/           # Database migrations
│
├── auth_project/              # Django settings
│   ├── settings.py           # Configuration
│   ├── urls.py               # Root URL routing
│   ├── asgi.py               # Channels configuration
│   └── wsgi.py               # WSGI app
│
├── manage.py                 # Django CLI
└── requirements.txt          # Dependencies (84 packages)
```

---

## Database Models (Core Data Schema)

### User & Profile Management
1. **StudentProfile**
   - Extended user profile with full_name, college, location
   - Skills, interests (JSON arrays)
   - Profile photo with validation
   - Social links (GitHub, LinkedIn, Portfolio, Behance)
   - Profile completion tracking

2. **OTP**
   - Email-based one-time passwords
   - Purpose: Login, Registration, Password Reset
   - Expiration validation
   - SHA-256 hashing

3. **UserStatus**
   - Online/offline status tracking
   - Last activity timestamp

### Project Management
4. **Project**
   - Title, description, collaboration needs
   - Owner (ForeignKey to User)
   - Visibility (PUBLIC/PRIVATE)
   - Category, technologies
   - Timeline and status tracking
   - Team members and invitations

5. **ProjectTeam**
   - Project team container

6. **ProjectTeamMember**
   - Members with roles and permissions

7. **ProjectTask**
   - Task management within projects

8. **ProjectMilestone**
   - Project milestones

### Social Features
9. **Connection**
   - User-to-user connections
   - Request/pending/accepted status

10. **Message**
    - Direct messaging between users
    - Read status tracking
    - File attachments support

11. **MessageFile**
    - File storage for messages

12. **MessageReadStatus**
    - Track message read receipts

13. **MessageReaction**
    - Emoji reactions to messages

14. **ChatRoom**
    - Group chat rooms
    - Members management

15. **ChatRoomMember**
    - Group chat membership

### Content & Activity
16. **Comment**
    - Nested comments on projects
    - Timestamps and author tracking

17. **Like**
    - Like/upvote functionality

18. **Notification**
    - User notifications
    - Read status tracking

19. **Activity**
    - Activity feed logging

20. **Follow**
    - User following relationships

### Additional Models
21. **File**
    - File management

22. **UserStats**
    - User statistics tracking

---

## API Endpoints

### Authentication
- `POST /api/auth/register/` - User registration with OTP
- `POST /api/auth/login/` - OTP-based login
- `POST /api/auth/verify-otp/` - OTP verification
- `GET /api/auth/logout/` - Logout

### User Profile
- `GET /api/users/` - List all users
- `GET /api/users/{id}/` - Get user profile
- `PUT /api/users/{id}/` - Update user profile
- `POST /api/users/{id}/follow/` - Follow user
- `GET /api/users/{id}/collaborators/` - Find collaborators

### Projects
- `GET /api/projects/` - List all projects (paginated)
- `POST /api/projects/` - Create new project
- `GET /api/projects/{id}/` - Project details
- `PUT /api/projects/{id}/` - Update project
- `DELETE /api/projects/{id}/` - Delete project
- `GET /api/projects/{id}/collaborators/` - Project team
- `POST /api/projects/{id}/invite/` - Invite collaborator
- `GET /api/projects/search/` - Search projects

### Comments & Reactions
- `GET /api/projects/{id}/comments/` - Get comments
- `POST /api/projects/{id}/comments/` - Post comment
- `POST /api/comments/{id}/reply/` - Reply to comment
- `DELETE /api/comments/{id}/` - Delete comment
- `POST /api/comments/{id}/like/` - Like comment

### Messaging
- `GET /api/messages/` - Message list
- `POST /api/messages/` - Send message
- `GET /api/messages/{id}/` - Message detail
- `PUT /api/messages/{id}/read/` - Mark as read
- `POST /api/messages/{id}/react/` - React to message
- WebSocket: `/ws/chat/{room_id}/` - Real-time chat

### Notifications
- `GET /api/notifications/` - Get notifications
- `PATCH /api/notifications/{id}/read/` - Mark notification read

---

## Key Views & Functions

### Dashboard & Profile
- `dashboard_view()` - Main dashboard
- `edit_profile()` - Profile editor
- `student_profile()` - View user profile
- `search_projects()` - Project search

### Project Management
- `create_project()` - Create new project
- `project_detail()` - View project details
- `edit_project()` - Edit project
- `delete_project()` - Delete project
- `find_collaborators()` - Find potential collaborators

### Collaboration
- `send_connection_request()` - Send collaboration request
- `accept_connection()` - Accept request
- `reject_connection()` - Reject request
- `view_connections()` - View user connections

### Messaging & Chat
- `message_list()` - User messages
- `send_message()` - Send DM
- `chat_room()` - Group chat interface
- `create_chat_room()` - Create chat room

### Comments & Activity
- `project_comments()` - View comments
- `post_comment()` - Create comment
- `delete_comment()` - Remove comment
- `activity_feed()` - Activity timeline

---

## Service Layer

### AuthService (`services/auth_service.py`)
- OTP generation and validation
- Email verification workflow
- Social login integration (Google, GitHub)
- Token management
- Password reset handling

### StudentProfileNLP (`utils.py`)
- NLP-based profile analysis
- Skill extraction
- Interest matching
- Recommendation algorithm

### ProjectVisibilityFilter (`utils.py`)
- Access control logic
- Visibility filtering (PUBLIC/PRIVATE/DRAFT)
- Permission checking

### Email Backends
- **Brevo** (`brevo_mail_backend.py`)
- **ZeptoMail** (`zepto_mail_backend.py`)
- Custom SMTP configuration

---

## Frontend Templates

### User Account Templates
- `accounts/login.html` - Login page
- `accounts/register.html` - Registration form
- `accounts/otp_verification.html` - OTP entry
- `accounts/edit_profile.html` - Profile editor
- `accounts/student_profile.html` - Profile view
- `account/logout.html` - Logout confirmation

### Project Templates
- `accounts/project_feed.html` - Project list
- `accounts/project_detail.html` - Project view
- `accounts/create_project.html` - Create project
- `accounts/edit_project.html` - Edit project
- `accounts/search_projects.html` - Search interface

### Collaboration Templates
- `accounts/find_collaborators.html` - Find collaborators
- `accounts/find_collaborators_enhanced.html` - Enhanced search
- `accounts/find_collaborators_new_final.html` - New UI

### Messaging Templates
- `chat.html` - Chat interface
- `accounts/messages.html` - Messages page

### Other Templates
- `base.html` - Main layout
- `about.html` - About page
- `contact_us.html` - Contact form
- `help_center.html` - Help page

---

## Static Assets

### JavaScript Files
- `login.js` - Login form validation
- `api-utils.js` - API communication helper
- `profile.js` - Profile interactions
- `password_validation.js` - Password strength checker
- `college_autocomplete.js` - College name autocomplete
- `register_validation.js` - Registration validation

### CSS & Bootstrap
- Bootstrap 5 integration
- Custom styling for components
- Responsive design

---

## Testing & Utilities

### Test Files
- `test_login.py` - Login functionality
- `test_email.py` - Email delivery
- `test_comments_api.py` - Comments API
- `test_profile_view.py` - Profile viewing
- `test_filter.py` - Filtering logic
- `test_search.py` - Search functionality
- `test_connections.py` - Connection management
- `test_services.py` - Service layer tests

### Utility Scripts
- `setup_social_apps.py` - OAuth setup
- `create_test_profiles.py` - Test data generation
- `debug_*.py` - Debugging utilities
- `performance_monitor.py` - Performance tracking

---

## Configuration Files

### Environment Variables (.env)
```
DEBUG=True/False
SECRET_KEY=***
DATABASE_URL=postgresql://...
ALLOWED_HOSTS=localhost,127.0.0.1,...
```

### Django Settings (settings.py)
- INSTALLED_APPS configuration
- Database connection
- Email backend setup
- Static files & media storage
- CORS settings
- Cache configuration (Redis)
- Channels configuration
- Celery settings
- Sentry monitoring

### Deployment
- `Procfile` - Procfile for Heroku/Railway
- `render.yaml` - Render deployment config
- `requirements.txt` - Python dependencies

---

## Key Features Implemented

### 1. Authentication System
- ✅ Email/OTP login
- ✅ Social login (Google, GitHub)
- ✅ Password reset
- ✅ Session management
- ✅ JWT token support

### 2. User Profiles
- ✅ Profile creation & editing
- ✅ Profile photo upload
- ✅ Skills & interests management
- ✅ Social media links
- ✅ Profile completion tracking

### 3. Project Management
- ✅ Create/edit/delete projects
- ✅ Project visibility control (PUBLIC/PRIVATE)
- ✅ Team collaboration
- ✅ Task management
- ✅ Timeline tracking

### 4. Collaboration Features
- ✅ Find collaborators
- ✅ Connection requests
- ✅ Collaboration history
- ✅ Team invitations
- ✅ Member roles & permissions

### 5. Messaging System
- ✅ Direct messaging
- ✅ Real-time chat (WebSockets)
- ✅ Message read status
- ✅ File attachments
- ✅ Typing indicators
- ✅ Group chat rooms

### 6. Comments & Reactions
- ✅ Nested comments
- ✅ Comment reactions (emoji)
- ✅ @mention notifications
- ✅ Comment threads

### 7. Activity & Notifications
- ✅ Activity feed
- ✅ Push notifications
- ✅ Email notifications
- ✅ Notification preferences

### 8. Search & Discovery
- ✅ Full-text project search
- ✅ User search
- ✅ Skill-based matching
- ✅ Interest-based recommendations
- ✅ Advanced filtering

---

## Performance Optimizations

### Database
- Query optimization with `.select_related()` and `.prefetch_related()`
- Database indexing on frequently queried fields
- Connection pooling

### Caching
- Redis caching layer
- Cache invalidation strategies
- Session caching

### Frontend
- Static file compression
- WhiteNoise for static file serving
- CSS/JS minification

### Background Jobs
- Celery for async tasks
- Email sending in background
- Notification delivery async

---

## Security Features

### Authentication & Authorization
- CSRF protection
- Session-based authentication
- JWT token validation
- OAuth2 integration

### Data Protection
- Password hashing (Django default: PBKDF2)
- OTP hashing (SHA-256)
- HTTPS enforcement (in production)
- CORS configuration

### Input Validation
- Form validation (Django Forms)
- File upload validation
- Email verification
- Rate limiting

---

## Dependencies Summary (84 packages)

### Core Framework
- Django 4.2.8
- django-allauth 0.61.1
- djangorestframework 3.14.0

### Database & ORM
- psycopg2-binary 2.9.9
- dj-database-url 2.1.0

### Real-time & Messaging
- channels 4.0.0
- channels-redis 4.1.0
- zeptomail 1.0.0

### External Services
- requests 2.31.0
- requests-oauthlib 1.3.1
- boto3 1.34.34
- rapidapi 1.0.0

### Development & Testing
- pytest 7.4.3
- pytest-django 4.7.0
- selenium 4.16.0
- black 23.12.1
- flake8 6.1.0

---

## Data Flow Diagrams

### User Registration Flow
```
User Input (Registration Form)
    ↓
RegisterForm Validation
    ↓
Create User & StudentProfile
    ↓
Generate & Send OTP (Email)
    ↓
User Enters OTP
    ↓
OTP Verification
    ↓
Account Active
```

### Project Creation & Collaboration Flow
```
User Creates Project
    ↓
ProjectForm Validation
    ↓
Save Project to Database
    ↓
Set Visibility (PUBLIC/PRIVATE)
    ↓
Find Collaborators (NLP Matching)
    ↓
Send Invitations
    ↓
Collaborators Accept/Reject
    ↓
Update Project Team
```

### Real-time Messaging Flow
```
User Sends Message
    ↓
Message Serialized & Validated
    ↓
Stored in Database
    ↓
WebSocket Event (Channels)
    ↓
Broadcast to Chat Room Members
    ↓
Real-time Update in Browser
```

---

## Notable Fixes & Improvements

### Recent Fixes (Based on Documentation)
1. **Login Issues** - Form validation and OTP flow improvements
2. **Comments System** - Nested comments implementation and badge display fixes
3. **Profile System** - Photo upload and profile viewing optimizations
4. **Project Feed** - Visibility filtering and performance improvements
5. **Find Collaborators** - Enhanced search UI and matching algorithm
6. **Message Read Status** - Real-time read receipt updates
7. **Email Configuration** - Brevo & ZeptoMail backend setup
8. **Performance** - Database query optimization and caching

---

## Deployment Architecture

### Production Stack
- **App Server**: Gunicorn + Django
- **Database**: PostgreSQL (Render/Railway)
- **Cache/Message Queue**: Redis
- **Static Files**: WhiteNoise + S3 (optional)
- **Email**: Brevo/ZeptoMail SMTP
- **Monitoring**: Sentry

### Deployment Platforms
- Render.com (PostgreSQL, Redis)
- Railway.app
- Heroku (Procfile compatible)

---

## Development Workflow

### Local Setup
```bash
# Create virtual environment
python -m venv venv

# Install dependencies
pip install -r requirements.txt

# Run migrations
python manage.py migrate

# Create superuser
python manage.py createsuperuser

# Start dev server
python manage.py runserver
```

### Testing
```bash
# Run all tests
pytest

# Run specific test
pytest tests/test_login.py

# With coverage
pytest --cov=accounts
```

---

## Summary Statistics

| Metric | Count |
|--------|-------|
| **Database Models** | 22 |
| **View Functions** | 100+ |
| **Templates** | 55+ |
| **API Endpoints** | 50+ |
| **Test Files** | 20+ |
| **Static Files** | 200+ |
| **Dependencies** | 84 |
| **Total Lines of Code** | ~50,000+ |

---

## Next Steps & Recommendations

1. **API Documentation** - Generate OpenAPI/Swagger docs with drf-spectacular
2. **Performance Tuning** - Monitor database queries and add indexes
3. **Testing Coverage** - Increase unit and integration test coverage
4. **CI/CD Pipeline** - Set up GitHub Actions for automated testing
5. **Documentation** - Add comprehensive API documentation
6. **Load Testing** - Test scalability with tools like Locust
7. **Security Audit** - Conduct security review and penetration testing

---

**Generated**: 2026-02-04
**Codebase Size**: ~50,000+ lines of code
**Framework**: Django 4.2.8
**Status**: Production-ready with active development
