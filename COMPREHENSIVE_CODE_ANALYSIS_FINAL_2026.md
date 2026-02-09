# Comprehensive Code Analysis - UniSinq Platform
**Generated:** Feb 09, 2026 | **Repository:** github.com/Goku0090/uni

---

## Executive Summary

This is a **Django-based collaborative platform** (UniSinq/UniSync) built for students to manage projects, find collaborators, communicate in real-time, and build professional networks. The application features:

- **Multi-tier Architecture**: Frontend (HTML/CSS/JS) → Django Views/APIs → WebSocket Consumers → Database
- **Real-time Capabilities**: WebSocket-powered live updates for projects, activities, and messaging
- **Social Networking**: Profiles, connections, follows, likes, comments, notifications
- **Project Management**: Task tracking, team collaboration, templated workflows, role-based access
- **Communication**: Direct & group chat, messaging with reactions, comment threads

---

## Technology Stack

| Layer | Technologies |
|-------|--------------|
| **Frontend** | HTML5, CSS3, JavaScript, Bootstrap |
| **Backend** | Django 3.2+, Django REST Framework (DRF), Django Channels |
| **Real-time** | WebSockets (via Channels), Daphne ASGI Server |
| **Database** | PostgreSQL (production), SQLite (development) |
| **Authentication** | Django Allauth, OAuth 2.0 (Google), Email OTP |
| **Email** | Brevo/ZeptoMail backends |
| **APIs** | Internal REST APIs, RapidAPI integrations |

---

## Directory Structure

```
auth_project/
├── auth_project/              # Django project settings
│   ├── settings.py           # Project configuration
│   ├── urls.py               # URL routing
│   ├── asgi.py               # Async gateway interface
│   ├── wsgi.py               # WSGI server config
│   └── __init__.py
│
├── accounts/                  # Main application module
│   ├── models.py             # Database schema (12 key models)
│   ├── views.py              # Core view logic (50+ views)
│   ├── views_contact.py      # Contact-specific views
│   ├── urls.py               # Route definitions
│   ├── serializers.py        # DRF API serializers
│   ├── consumers.py          # WebSocket consumers
│   ├── routing.py            # WebSocket routing config
│   ├── signals_realtime.py   # Signal handlers for real-time
│   ├── forms.py              # Django forms
│   ├── permissions.py        # Custom permissions
│   ├── chat_api.py           # Chat API logic
│   ├── comment_api.py        # Comments API
│   ├── template_api.py       # Template API
│   ├── utils.py              # Utility functions
│   ├── brevo_mail_backend.py # Email backend
│   ├── zepto_mail_backend.py # Email backend
│   ├── apps.py               # App configuration
│   ├── tests.py              # Unit tests
│   │
│   ├── management/           # Custom Django commands
│   ├── migrations/           # Database migrations
│   ├── services/             # Business logic services
│   ├── static/               # Static files (CSS, JS, images)
│   ├── templates/            # HTML templates
│   └── templatetags/         # Custom template filters
│
├── media/                     # User uploads (photos, files)
├── static/                    # Global static files
├── staticfiles/               # Collected static files
├── logs/                      # Application logs
│
├── manage.py                 # Django management CLI
├── requirements.txt          # Python dependencies
├── .env                      # Environment variables
├── db.sqlite3                # Development database
└── [Multiple debug/test scripts]
```

---

## Core Database Models

### 1. **User Profile Models**

#### `StudentProfile`
```
- user_id (FK to Django User)
- bio (text)
- skills (M2M tags)
- interests (M2M tags)
- college_name
- graduation_year
- portfolio_link
- profile_photo (image)
- background_photo (image)
- social_links (LinkedIn, GitHub, Twitter)
- verified (boolean)
- created_at, updated_at
```

#### `UserStatus`
```
- user (1:1 to User)
- is_online (boolean)
- last_seen (datetime)
- status_message (text)
```

#### `OTP`
```
- user (FK to User)
- otp_code
- purpose (login/register/password_reset)
- expires_at
- is_used (boolean)
```

### 2. **Project Models**

#### `Project`
```
- owner (FK to User)
- title, description
- tech_stack (M2M tags)
- status (Active, Completed, On Hold)
- visibility (Public, Private)
- collaboration_needs (text)
- project_image
- github_url, demo_url, documentation_url
- start_date, end_date
- created_at, updated_at
```

#### `ProjectMember`
```
- project (FK)
- user (FK)
- role (owner, contributor, lead)
- joined_at
```

#### `ProjectInvitation`
```
- project (FK)
- invited_user (FK)
- status (pending, accepted, declined)
- created_at
```

#### `ProjectTask`
```
- project (FK)
- title, description
- status (to_do, in_progress, done)
- assigned_to (FK to User)
- priority (high, medium, low)
- due_date
```

#### `ProjectMilestone`
```
- project (FK)
- title, description
- due_date
- completion_date
```

#### `ProjectTemplate`
```
- title, description
- tech_stack (M2M)
- structure (JSON)
- created_by (FK to User)
- is_public (boolean)
```

### 3. **Social/Networking Models**

#### `Connection` (Friend Requests)
```
- requester (FK to User)
- receiver (FK to User)
- status (pending, accepted, blocked)
- created_at
```

#### `Follow`
```
- follower (FK to User)
- following (FK to User)
- created_at
```

#### `Like`
```
- user (FK to User)
- project (FK)
- created_at
```

#### `Comment`
```
- user (FK to User)
- project (FK)
- content (text)
- created_at, updated_at
- parent_comment (self-referencing FK for nested comments)
```

### 4. **Messaging Models**

#### `ChatRoom`
```
- name (text)
- room_type (direct, group)
- members (M2M to User)
- created_at
```

#### `Message`
```
- room (FK to ChatRoom)
- sender (FK to User)
- content (text)
- created_at, updated_at
- is_edited (boolean)
```

#### `MessageReaction`
```
- message (FK to Message)
- user (FK to User)
- emoji (text)
```

#### `MessageReadStatus`
```
- message (FK to Message)
- user (FK to User)
- read_at (datetime)
```

### 5. **Notifications Model**

#### `Notification`
```
- recipient (FK to User)
- notifier (FK to User, nullable)
- notification_type (like, comment, message, mention, connection)
- content_object (GenericFK to any model)
- is_read (boolean)
- created_at
```

---

## Key Views (50+ endpoints)

### Authentication Views
| View | URL | Method | Purpose |
|------|-----|--------|---------|
| `register` | `/register/` | GET, POST | User registration |
| `login` | `/login/` | GET, POST | User login |
| `verify_otp` | `/verify-otp/` | GET, POST | OTP verification |
| `password_reset` | `/password-reset/` | GET, POST | Password reset |
| `logout` | `/logout/` | POST | User logout |

### Project Views
| View | URL | Method | Purpose |
|------|-----|--------|---------|
| `post_project` | `/post-project/` | GET, POST | Create project |
| `project_detail` | `/project/<id>/` | GET | View project details |
| `edit_project` | `/edit-project/<id>/` | GET, POST | Edit project |
| `delete_project` | `/delete-project/<id>/` | POST | Delete project |
| `search_projects` | `/search/` | GET | Search projects |
| `projects_by_skill` | `/skill/<skill>/` | GET | Filter by skill |
| `like_project` | `/project/<id>/like/` | POST | Like project |
| `unlike_project` | `/project/<id>/unlike/` | POST | Unlike project |

### Collaboration Views
| View | URL | Method | Purpose |
|------|-----|--------|---------|
| `find_collaborators` | `/find-collaborators/` | GET, POST | NLP-based matching |
| `view_profile` | `/profile/<user_id>/` | GET | View user profile |
| `student_profile` | `/my-profile/` | GET, POST | Manage own profile |
| `my_connections` | `/my-connections/` | GET | View friend list |
| `send_connection_request` | `/connect/<user_id>/` | POST | Send friend request |
| `accept_connection` | `/accept/<user_id>/` | POST | Accept friend request |
| `decline_connection` | `/decline/<user_id>/` | POST | Decline friend request |

### Activity & Notifications
| View | URL | Method | Purpose |
|------|-----|--------|---------|
| `activity_feed` | `/activity-feed/` | GET | User activity feed |
| `notifications` | `/notifications/` | GET | Notification list |
| `mark_as_read` | `/mark-as-read/<id>/` | POST | Mark notification read |

### Comments & Interactions
| View | URL | Method | Purpose |
|------|-----|--------|---------|
| `project_comments` | `/project/<id>/comments/` | GET | Get comments |
| `add_comment` | `/project/<id>/add-comment/` | POST | Add comment |
| `delete_comment` | `/comment/<id>/delete/` | POST | Delete comment |

### Messaging Views
| View | URL | Method | Purpose |
|------|-----|--------|---------|
| `message_list` | `/messages/` | GET | List conversations |
| `start_direct_message` | `/direct/<user_id>/` | GET, POST | Start DM |
| `group_chat_list` | `/group-chat/` | GET | List group chats |
| `create_group_chat` | `/create-group/` | POST | Create group chat |

---

## REST API Endpoints (DRF)

### Chat & Messaging APIs
```
GET     /api/chat-rooms/                    # List chat rooms
POST    /api/chat-rooms/                    # Create chat room
GET     /api/chat-rooms/<id>/               # Chat room details
GET     /api/messages/                      # List messages
GET     /api/messages/<id>/                 # Message details
POST    /api/messages/<id>/reactions/       # Add reaction
GET     /api/conversations/                 # List conversations
GET     /api/direct-message/<user_id>/      # Direct message thread
POST    /api/direct-message/<user_id>/      # Send direct message
GET     /api/search-messages/               # Search messages
```

### User & Profile APIs
```
GET     /api/user-profile/<id>/             # User profile data
GET     /api/user-stats/                    # User statistics
GET     /api/users/search/                  # Search users
POST    /api/users/update-status/           # Update online status
GET     /api/connections/                   # List connections
POST    /api/connections/request/           # Send connection request
```

### Project APIs
```
GET     /api/projects/                      # List projects
POST    /api/projects/                      # Create project
GET     /api/projects/<id>/                 # Project details
PUT     /api/projects/<id>/                 # Update project
DELETE  /api/projects/<id>/                 # Delete project
GET     /api/projects/filter/               # Filter by tech stack
POST    /api/projects/<id>/members/         # Add member
GET     /api/project-templates/             # List templates
```

### Comment & Social APIs
```
GET     /api/projects/<id>/comments/        # Get comments
POST    /api/projects/<id>/comments/        # Add comment
DELETE  /api/comments/<id>/                 # Delete comment
POST    /api/projects/<id>/like/            # Like project
POST    /api/projects/<id>/unlike/          # Unlike project
```

### AI/NLP APIs
```
POST    /api/nlp-analyze/                   # Analyze user skills
GET     /api/match-collaborators/           # Get matching collaborators
```

---

## WebSocket Consumers (Real-time)

### 1. **ProjectUpdateConsumer**
```python
# Location: accounts/consumers.py
# Manages real-time updates for projects

Events Handled:
- connect: User joins project room
- disconnect: User leaves project room
- project_update: Broadcast project status changes
- member_joined: Notify team of new member
- comment_added: Real-time comment broadcast
- task_updated: Task status change notification

Channels:
- projects_{project_id}
```

### 2. **ActivityFeedConsumer**
```python
# Real-time activity feed updates

Events:
- new_project: User posts new project
- project_liked: Project gets liked
- connection_added: New connection made
- comment_posted: Comment on project

Channels:
- activity_feed_{user_id}
```

### 3. **NotificationConsumer**
```python
# Instant notification delivery

Events:
- notification_created: New notification
- notification_read: User marks as read
- mention: User mentioned in comment
- message_received: New message alert

Channels:
- notifications_{user_id}
```

### 4. **ChatConsumer**
```python
# Real-time messaging

Events:
- message_sent: New message
- message_reaction: Emoji reaction added
- typing_indicator: User typing
- message_deleted: Message removed

Channels:
- chat_room_{room_id}
```

---

## Key Features & Workflows

### 1. **Authentication Flow**
```
User Register/Login
    ↓
Email OTP Sent (via Brevo/ZeptoMail)
    ↓
User Enters OTP
    ↓
OTP Verification
    ↓
Session Created / JWT Token Issued
    ↓
Redirect to Dashboard
```

### 2. **Project Creation & Collaboration**
```
User Creates Project
    ↓
Project Broadcast via WebSocket
    ↓
Project Appears in Feed for Others
    ↓
User Invites Collaborators
    ↓
Invitations Sent (Notifications)
    ↓
Invited Users Accept/Decline
    ↓
ProjectMember Record Created
    ↓
Team Chat Created
    ↓
Real-time Updates on TaskBoard
```

### 3. **Find Collaborators (NLP Matching)**
```
User Views Find Collaborators Page
    ↓
System Analyzes User's Skills/Interests
    ↓
NLP Matching Against All Users
    ↓
Scoring Algorithm Ranks Matches
    ↓
Top Matches Displayed
    ↓
User Can Send Connection Request
    ↓
Notification Sent to Target User
    ↓
Accept/Decline Connection
```

### 4. **Real-time Messaging**
```
User A Sends Message to User B
    ↓
Message Saved to Database
    ↓
WebSocket Broadcast to Room
    ↓
User B Receives via Socket
    ↓
Message Marked as Delivered
    ↓
User B Reads Message
    ↓
Read Status Updated
    ↓
User A Sees "Read" Indicator
```

### 5. **Activity Feed**
```
User Action (Like/Comment/Post)
    ↓
Signal Handler Triggered
    ↓
Notification Created
    ↓
WebSocket Broadcast
    ↓
Followers See Update in Real-time
    ↓
Activity Cached for Performance
```

---

## Service Layer Architecture

### Email Service
```python
# accounts/brevo_mail_backend.py & zepto_mail_backend.py
Services:
- send_otp_email(user, otp_code)
- send_password_reset_email(user, reset_link)
- send_notification_email(user, notification)
- send_bulk_email(users, message)
```

### Notification Service
```python
# Handles all notification types
- create_notification(recipient, notifier, type, content)
- send_notification(notification)
- mark_as_read(notification_id)
- batch_notify(users, message)
```

### Search & Filter Service
```python
# Filter and search functionality
- search_projects(query, filters)
- filter_by_skill(skill_name)
- filter_by_status(status)
- advanced_search(multiple_filters)
```

### Chat Service
```python
# Messaging logic
- get_or_create_room(user1, user2)
- send_message(room, sender, content)
- search_messages(room, query)
- get_unread_count(user)
```

### NLP Matching Service
```python
# Collaborative filtering
- analyze_user_profile(user)
- get_skill_matches(user, limit=10)
- calculate_match_score(user1, user2)
- get_recommended_collaborators(user)
```

---

## Authentication & Security

### Authentication Methods
1. **Email OTP** (Primary)
   - User enters email → OTP sent → User verifies
   - Used for registration and login

2. **Django Allauth** (Social)
   - Google OAuth 2.0 integration
   - Automatic profile creation from OAuth data

3. **Session-based** (Traditional)
   - Django session framework
   - Cookies for persistence

### Permissions
```python
# accounts/permissions.py
- IsOwner: User is project owner
- IsTeamMember: User is team member
- IsProjectOwnerOrTeamLead: For editing project
- CanComment: User can comment on project
- CanViewProfile: User can view another's profile
```

---

## Frontend Pages & Templates

### Core Pages
| Page | Template File | Purpose |
|------|---------------|---------|
| Home/Dashboard | `dashboard.html` | Main feed and overview |
| Login | `login.html` | Authentication |
| Register | `register.html` | New user signup |
| Profile | `student_profile.html` | User profile management |
| View Profile | `profile_detail.html` | View other users |
| Post Project | `post_project.html` | Create project |
| Project Detail | `project_detail.html` | Project information |
| Find Collaborators | `find_collaborators.html` | NLP matching search |
| Messages | `messages.html` | Direct & group chat |
| Notifications | `notifications.html` | Notification center |
| Activity Feed | `activity_feed.html` | Real-time activity |

### Components
- Navbar (branding, navigation)
- Sidebar (quick links)
- Project Cards (with like/comment buttons)
- Comment Section (nested comments)
- User Cards (profile previews)
- Chat Widget (messaging interface)

---

## Static Files Organization

```
static/
├── css/
│   ├── bootstrap.min.css
│   ├── custom.css
│   ├── navbar.css
│   ├── project_cards.css
│   └── responsive.css
│
├── js/
│   ├── bootstrap.bundle.min.js
│   ├── main.js
│   ├── chat.js (WebSocket handling)
│   ├── notifications.js (Real-time alerts)
│   ├── comments.js (Comment functionality)
│   ├── search.js (Search/filter)
│   └── utils.js (Helper functions)
│
├── images/
│   ├── logo/
│   ├── icons/
│   ├── placeholders/
│   └── branding/
│
└── vendor/
    ├── jquery/
    ├── select2/ (Advanced search)
    └── moment.js (Date formatting)
```

---

## Database Migrations

```
0001_initial.py          # Initial schema
0002_add_comments.py     # Comments feature
0003_add_messaging.py    # Chat system
0004_add_notifications.py # Notification system
0005_add_templates.py    # Project templates
0006_add_tasks.py        # Project tasks
0007_add_milestones.py   # Project milestones
0008_add_reactions.py    # Message reactions
0009_update_permissions.py
...
[60+ total migrations]
```

---

## Key Configuration Files

### settings.py
```python
# Core Configuration
INSTALLED_APPS = [
    'daphne',
    'channels',
    'rest_framework',
    'allauth',
    'allauth.account',
    'allauth.socialaccount',
    'allauth.socialaccount.providers.google',
    'accounts',
]

# Channels Config
ASGI_APPLICATION = 'auth_project.asgi.application'
CHANNEL_LAYERS = {
    'default': {
        'BACKEND': 'channels.layers.InMemoryChannelLayer'
    }
}

# Email Backend
EMAIL_BACKEND = 'accounts.brevo_mail_backend.BrevoEmailBackend'
# OR
EMAIL_BACKEND = 'accounts.zepto_mail_backend.ZeptoEmailBackend'

# REST Framework Config
REST_FRAMEWORK = {
    'DEFAULT_PAGINATION_CLASS': 'rest_framework.pagination.PageNumberPagination',
    'PAGE_SIZE': 10,
    'DEFAULT_AUTHENTICATION_CLASSES': [
        'rest_framework.authentication.SessionAuthentication',
    ],
}
```

### asgi.py (WebSocket routing)
```python
# Routes HTTP → Django views
# Routes ws:// → WebSocket consumers (via Channels)
```

### urls.py
```python
urlpatterns = [
    path('admin/', admin.site.urls),
    path('accounts/', include('allauth.urls')),
    path('api/', include('accounts.urls')),  # REST API
    path('ws/', include('accounts.routing')),  # WebSocket
    path('', include('accounts.urls')),  # Main views
]
```

---

## Testing & Debugging Scripts

### Test Files
- `test_login.py` - Login functionality
- `test_comments_api.py` - Comments API
- `test_profile_fix.py` - Profile viewing
- `test_connections.py` - Connection requests
- `test_email.py` - Email sending
- `test_filter.py` - Project filtering

### Debug Scripts
- `diagnose_login.py` - Login issues
- `debug_profiles.py` - Profile errors
- `debug_find_collaborators.py` - Matching algorithm
- `debug_conversations.py` - Messaging issues
- `debug_filtering.py` - Filter problems
- `deep_debug_oauth.py` - OAuth errors

### Maintenance Scripts
- `fix_duplicate_social_apps.py` - OAuth duplicates
- `setup_social_apps.py` - OAuth setup
- `setup_oauth_fixed.py` - OAuth configuration
- `cleanup_social_apps.py` - Clean OAuth
- `fix_site_configuration.py` - Site settings

---

## Dependencies

### Core Framework
```
Django==3.2.20
djangorestframework==3.14.0
django-channels==4.0.0
daphne==4.0.0
django-allauth==0.57.0
```

### Database
```
psycopg2-binary==2.9.9 (PostgreSQL)
```

### Email
```
requests==2.31.0 (for Brevo/ZeptoMail APIs)
```

### Utilities
```
python-dotenv==1.0.0
Pillow==10.1.0 (Image processing)
celery==5.3.0 (Background tasks)
```

---

## Performance Optimizations

### Database
- Query optimization with `select_related()`, `prefetch_related()`
- Indexing on frequently searched fields (skills, tech_stack)
- Connection pooling for PostgreSQL

### Caching
- Redis caching for user profiles
- Activity feed caching
- Message thread caching

### WebSocket
- Connection pooling
- Message batching
- Room-based broadcasting

### Frontend
- Static file compression
- Lazy loading for images
- Pagination for large lists
- AJAX for partial page updates

---

## Known Issues & Fixes

### Recently Fixed
1. **CSRF Token Issues** - Added CSRF exemption for specific APIs
2. **Project Detail Loading** - Optimized queries, added pagination
3. **Comments Not Visible** - Fixed template rendering, added caching
4. **OAuth Multiple Objects** - Deduplicated social apps
5. **WebSocket Connection** - Fixed routing configuration
6. **Like Button State** - Added real-time state sync
7. **Template Recursion** - Fixed infinite loop in comments
8. **Collaborators Not Showing** - Fixed filter logic

### Outstanding
- Performance on 10k+ projects
- Real-time sync edge cases
- Email delivery reliability (depends on provider)

---

## Development Workflow

### Local Setup
```bash
# Clone repo
git clone https://github.com/Goku0090/uni.git

# Create virtual environment
python -m venv venv
source venv/Scripts/activate  # Windows

# Install dependencies
pip install -r requirements.txt

# Set environment variables
cp .env.template .env
# Edit .env with your settings

# Run migrations
python manage.py migrate

# Create superuser
python manage.py createsuperuser

# Run development server
python manage.py runserver

# In another terminal, run WebSocket server
daphne -b 0.0.0.0 -p 8001 auth_project.asgi:application
```

### Database Reset
```bash
python manage.py flush --noinput
python manage.py migrate
```

### Static Files
```bash
python manage.py collectstatic --noinput
```

---

## Deployment

### Production Checklist
- [ ] Set `DEBUG = False` in settings
- [ ] Configure `ALLOWED_HOSTS`
- [ ] Use PostgreSQL (not SQLite)
- [ ] Set up Daphne for WebSockets
- [ ] Configure email backend
- [ ] Enable HTTPS
- [ ] Set up Redis for caching
- [ ] Configure logging
- [ ] Set up monitoring/alerts
- [ ] Database backups

### Deployment Platforms
- **Render.com** (recommended for Django + Channels)
- **Railway.app**
- **Heroku** (with paid dyno for WebSockets)
- **DigitalOcean**
- **AWS** (EC2 + RDS)

---

## API Response Examples

### Get User Profile
```json
GET /api/user-profile/123/
Response: {
  "id": 123,
  "username": "john_doe",
  "bio": "Full-stack developer",
  "skills": ["Python", "Django", "React"],
  "interests": ["Web Dev", "AI"],
  "profile_photo": "https://...",
  "college_name": "MIT",
  "social_links": {
    "github": "https://github.com/johndoe",
    "linkedin": "https://linkedin.com/in/johndoe"
  },
  "connection_status": "accepted",
  "following": false
}
```

### Get Project Details
```json
GET /api/projects/456/
Response: {
  "id": 456,
  "title": "AI Chatbot",
  "description": "...",
  "owner": { "id": 123, "username": "john_doe" },
  "tech_stack": ["Python", "TensorFlow", "Django"],
  "status": "Active",
  "visibility": "Public",
  "members": [
    { "id": 123, "role": "owner" },
    { "id": 124, "role": "contributor" }
  ],
  "likes_count": 42,
  "comments_count": 8,
  "github_url": "https://github.com/...",
  "created_at": "2024-01-15T10:30:00Z"
}
```

### Send Direct Message
```json
POST /api/direct-message/124/
Request: { "content": "Hey, want to collaborate?" }
Response: {
  "id": "msg_789",
  "sender": 123,
  "receiver": 124,
  "content": "Hey, want to collaborate?",
  "created_at": "2024-02-09T14:20:00Z",
  "is_read": false
}
```

---

## Future Enhancement Ideas

1. **Video Call Integration** - Jitsi or Twilio
2. **Advanced Notifications** - Push notifications, SMS
3. **Analytics Dashboard** - Project metrics, user engagement
4. **Machine Learning** - Better collaborator matching
5. **Payment System** - Premium features, project monetization
6. **Mobile App** - React Native or Flutter
7. **API Versioning** - v1, v2 endpoints
8. **GraphQL** - Alternative to REST
9. **Real-time Notifications** - Push notifications
10. **Automated Tests** - 80%+ coverage

---

## Conclusion

UniSinq is a **well-structured, feature-rich collaborative platform** with:
- Clean separation of concerns (models, views, services)
- Real-time capabilities via WebSockets
- Modern API design with DRF
- Comprehensive authentication options
- Scalable architecture ready for production

The codebase has undergone significant fixes and improvements, with most critical issues resolved. The foundation is solid for future enhancements.

---

**Document Status:** Complete  
**Last Updated:** Feb 09, 2026  
**Total Models:** 15+  
**Total Views:** 50+  
**Total API Endpoints:** 40+  
**WebSocket Consumers:** 4  
