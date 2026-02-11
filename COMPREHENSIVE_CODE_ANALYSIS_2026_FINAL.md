# UniSync: Comprehensive Code Analysis 2026

## Project Overview

**UniSync** is a Django-based collaborative platform for students to discover, create, and collaborate on projects. It features:
- User authentication (Email OTP + Social OAuth)
- Project discovery and management
- Real-time messaging with WebSocket support
- Team collaboration and invitations
- Comment and feedback system
- Project templates and analytics

---

## 1. Architecture & Technology Stack

### Backend Framework
- **Django 4.2.8**: Core web framework
- **Django Rest Framework 3.14.0**: RESTful API
- **Channels 4.0.0**: WebSocket support for real-time messaging
- **Django-allauth 0.61.1**: Multi-provider authentication (Google, GitHub)

### Database & Caching
- **PostgreSQL** (via psycopg2-binary): Primary database
- **Redis 5.0.1**: In-memory cache + WebSocket message broker
- **Django-redis 5.4.0**: Redis integration

### Frontend Technologies
- **Django Templates**: Server-side rendering
- **JavaScript**: Client-side interactivity
- **HTML/CSS**: Markup and styling

### Infrastructure
- **Gunicorn 21.2.0**: Production WSGI server
- **WhiteNoise 6.6.0**: Static file serving
- **dj-database-url**: Database URL parsing

---

## 2. Project Structure

```
auth_project/
├── auth_project/          # Django project settings
│   ├── settings.py        # Configuration
│   ├── urls.py            # Root URL routing
│   ├── wsgi.py            # WSGI application
│   └── asgi.py            # ASGI (WebSocket) application
│
├── accounts/              # Main Django app
│   ├── models.py          # Database models
│   ├── views.py           # View logic (3450+ lines)
│   ├── serializers.py     # DRF serializers
│   ├── urls.py            # App URL routing
│   ├── forms.py           # Django forms
│   ├── chat_api.py        # Messaging API
│   ├── comment_api.py     # Comments functionality
│   ├── consumers.py       # WebSocket consumers
│   ├── routing.py         # WebSocket routing
│   ├── signals_realtime.py # Real-time event signals
│   ├── permissions.py     # Custom permissions
│   ├── utils.py           # Utility functions
│   ├── brevo_mail_backend.py  # Email service
│   ├── templates/         # HTML templates
│   ├── static/            # CSS, JS, images
│   ├── services/          # Business logic
│   ├── management/        # Management commands
│   └── migrations/        # Database migrations
│
├── media/                 # User uploads (profile photos, files)
├── static/                # Static assets
├── manage.py              # Django CLI
├── requirements.txt       # Python dependencies
└── db.sqlite3            # Local development database
```

---

## 3. Core Models & Database Schema

### User & Profile Management

#### StudentProfile
```python
- user (FK -> User): One-to-one relationship with Django User
- full_name: Display name for the user
- college: Institution name
- location: Geographic location
- interests: JSON array of interests
- bio: Short biography
- profile_photo: Image upload
- skills: JSON array of technical skills
- project_interests: JSON array of project domains
- role_preference: Preferred role (Developer, Designer, etc.)
- social_links: GitHub, LinkedIn, Portfolio, Behance URLs
- profile_completed: Boolean flag
- created_at, updated_at: Timestamps
```

#### UserStatus
- Tracks online/offline status and last activity

#### UserStats
- Statistics tracking (projects, connections, followers)

---

### Project Management

#### Project
```python
- owner (FK -> User): Project creator
- title: Project name
- description: Detailed description
- category: Project type (e.g., "Web Development")
- technologies: JSON array of tech stack
- looking_for: Skills being sought
- collaboration_needs: Detailed requirements
- github_link: Repository URL
- visibility: Public/Private
- status: Active/Completed/Archived
- created_at, updated_at: Timestamps
- tags: JSON array for categorization
```

#### ProjectTeam
```python
- project (FK -> Project)
- team_name: Team identifier
- description: Team details
- max_members: Team size limit
```

#### ProjectTeamMember
```python
- team (FK -> ProjectTeam)
- user (FK -> User)
- role: Team member role
- joined_at: Timestamp
```

#### ProjectTeamInvitation
```python
- team (FK -> ProjectTeam)
- inviter (FK -> User)
- invitee (FK -> User)
- status: Pending/Accepted/Rejected
```

#### ProjectTask & ProjectMilestone
- Track project progress and deliverables

---

### Collaboration & Social Features

#### Connection
```python
- sender (FK -> User)
- receiver (FK -> User)
- status: Pending/Accepted/Blocked
- created_at: Request timestamp
```

#### Follow
```python
- follower (FK -> User)
- following (FK -> User)
- created_at: Timestamp
```

#### Like
```python
- user (FK -> User)
- project (FK -> Project)
- created_at: Timestamp
```

#### Comment
```python
- project (FK -> Project)
- author (FK -> User)
- content: Comment text
- created_at, updated_at: Timestamps
```

#### Activity
```python
- user (FK -> User)
- activity_type: Action performed
- project (FK -> Project, nullable)
- timestamp: When activity occurred
- is_read: Notification read status
```

---

### Messaging System

#### ChatRoom
```python
- name: Room identifier
- is_group: Boolean for group chats
- members (M2M -> User)
- created_at, updated_at: Timestamps
```

#### ChatRoomMember
```python
- room (FK -> ChatRoom)
- user (FK -> User)
- joined_at: Membership timestamp
- is_admin: Admin privileges
```

#### Message
```python
- room (FK -> ChatRoom)
- sender (FK -> User)
- content: Message text
- message_type: Text/File/System
- created_at: Timestamp
- is_read: Read status
```

#### MessageFile
- Handles file attachments in messages

#### MessageReaction
```python
- message (FK -> Message)
- user (FK -> User)
- reaction: Emoji or reaction type
```

#### MessageReadStatus
```python
- message (FK -> Message)
- user (FK -> User)
- read_at: When message was read
```

---

### Authentication & OTP

#### OTP Model
```python
- email: Target email address
- otp_code: 6-digit code
- purpose: login/registration/reset
- is_used: Validation flag
- created_at, expires_at: Timing
- Methods: is_valid(), verify_otp(), generate_otp()
```

---

### Project Templates

#### ProjectTemplate
```python
- name: Template name
- description: Use case description
- content: Template structure (JSON)
- category: Template type
- created_by (FK -> User)
- created_at, updated_at: Timestamps
```

#### TemplateRating
```python
- template (FK -> ProjectTemplate)
- user (FK -> User)
- rating: 1-5 stars
- created_at: Timestamp
```

#### TemplateUsageLog
- Tracks template usage analytics

---

## 4. API Endpoints & Views

### Authentication Endpoints
| Method | Path | Purpose |
|--------|------|---------|
| GET/POST | `/login/` | Email/password authentication |
| GET/POST | `/register/` | New user registration |
| GET/POST | `/forgot-password/` | Password reset request |
| POST | `/reset-password/` | Reset password with OTP |
| POST | `/verify-otp/<purpose>/` | OTP verification |
| POST | `/resend-otp/<purpose>/` | Resend OTP code |
| GET | `/logout/` | User logout |

### Profile Management
| Method | Path | Purpose |
|--------|------|---------|
| GET | `/` | Home/main page |
| GET | `/dashboard/` | User dashboard |
| GET/POST | `/student-details/` | User profile setup |
| GET | `/student-profile/` | View profile |
| GET/PUT | `/api/profile/` | API profile endpoint (DRF) |
| GET | `/user/<username>/` | View another user's profile |

### Project Management
| Method | Path | Purpose |
|--------|------|---------|
| GET | `/find-collaborators/` | Browse projects |
| POST | `/post-project/` | Create new project |
| GET | `/project-detail/<id>/` | View project details |
| POST | `/edit-project/<id>/` | Update project |
| POST | `/delete-project/<id>/` | Delete project |
| POST | `/like-project/<id>/` | Like/unlike project |

### Comments System
| Method | Path | Purpose |
|--------|------|---------|
| GET | `/api/projects/<id>/comments/` | Get project comments |
| POST | `/api/projects/<id>/comments/` | Add comment |
| PUT | `/api/comments/<id>/` | Edit comment |
| DELETE | `/api/comments/<id>/` | Delete comment |

### Messaging (Real-time)
| Method | Path | Purpose |
|--------|------|---------|
| GET | `/messages/` | Message inbox |
| GET/POST | `/api/chat-rooms/` | Create/list chat rooms |
| GET | `/api/chat-rooms/<id>/` | Chat room details |
| POST | `/api/direct-message/` | Initiate 1-on-1 chat |
| GET/POST | `/api/messages/` | Send/receive messages |
| POST | `/api/message-reactions/` | Add emoji reaction |
| GET | `/api/conversations/` | List all conversations |

### Social Features
| Method | Path | Purpose |
|--------|------|---------|
| POST | `/follow/<user_id>/` | Follow user |
| POST | `/connect/<user_id>/` | Send connection request |
| GET | `/my-connections/` | View connections |
| POST | `/accept-connection/<id>/` | Accept connection |
| POST | `/reject-connection/<id>/` | Reject connection |
| GET | `/activity-feed/` | Activity stream |
| GET | `/notifications/` | User notifications |

### Team Management
| Method | Path | Purpose |
|--------|------|---------|
| POST | `/invite-to-team/<project_id>/` | Invite members |
| POST | `/respond-team-invitation/<id>/` | Accept/reject invitation |
| POST | `/remove-team-member/<project_id>/<user_id>/` | Remove member |

---

## 5. Key Views & Business Logic

### Authentication Flow

**Registration (`register_view`)**
```
1. User submits registration form
2. OTP generated and sent to email
3. User verifies OTP
4. StudentProfile created
5. User logged in
```

**Login (`login_view`)**
```
1. Email/password submission
2. OTP sent to registered email
3. User verifies OTP
4. Session created
```

**Password Reset (`reset_password_view`)**
```
1. Email submission
2. OTP verification
3. New password set
```

### Project Discovery (`find_collaborators`)
```
1. Apply visibility filters (ProjectVisibilityFilter)
2. Search by title/description/tech stack
3. Filter by category, timeline
4. Apply skill matching (StudentProfileNLP)
5. Return paginated results
```

### Messaging System (`chat_api.py`)
- **ChatRoomListCreateView**: Create/list chat rooms
- **DirectMessageView**: Initiate private chats
- **MessageListCreateView**: Send/receive messages
- **MessageReactionView**: Add emoji reactions
- **TypingIndicatorView**: Real-time typing status
- **ConversationListView**: Conversation history

### Comments System (`comment_api.py`)
- **get_comments**: Fetch project comments
- **add_comment**: Post new comment
- **edit_comment**: Update existing comment
- **delete_comment**: Remove comment

### Real-time Updates (`consumers.py`)
- **ChatConsumer**: WebSocket handler for messaging
- Message broadcasting
- Typing indicators
- Read receipts

---

## 6. Serializers (DRF)

### UserProfileSerializer
```python
Fields:
- username, email, full_name, date_joined
- college, location, interests, bio, profile_photo
- skills, project_interests, role_preference
- github, linkedin, portfolio, behance
- profile_completed, is_online
```

### ProjectSerializer
```python
Fields:
- id, title, description, technologies
- looking_for, category, timeline
- collaboration_needs, github_link
- created_at, updated_at
- owner (nested UserProfileSerializer)
- likes_count, comments_count (computed)
```

### MessageSerializer
```python
Fields:
- id, content, sender (nested)
- created_at, is_read
- message_type, reactions
```

### ConnectionSerializer
- Handles connection requests with status

### NotificationSerializer
- Manages user notifications

---

## 7. Utilities & Helpers

### StudentProfileNLP (`utils.py`)
Advanced matching for finding collaborators:
- Skill matching algorithm
- Interest alignment scoring
- Role compatibility analysis

### ProjectVisibilityFilter
```python
Logic:
- Public: Visible to all
- Private: Only owner and team
- Invite-only: Shared with specific users
```

### Email Backends
- **Brevo** (Sendinblue) email service
- **Zepto Mail**: Alternative email provider
- HTML + plain text email templates

---

## 8. Authentication Methods

### Email + OTP
```
1. User registers with email
2. 6-digit OTP sent
3. OTP valid for 5 minutes
4. Marked as used after verification
```

### OAuth (Social Login)
- **Google**: Via django-allauth
- **GitHub**: Via django-allauth
- Automatic StudentProfile creation

---

## 9. Security Features

### CSRF Protection
- CSRF middleware enabled
- CSRF token in forms

### Password Hashing
- Django's default (PBKDF2)

### SQL Injection Prevention
- ORM query construction

### XSS Protection
- `sanitize_input()` utility
- HTML tag stripping
- Template auto-escaping

### Input Validation
- Form validation
- Serializer validation
- Custom validators

---

## 10. Real-time Features

### WebSocket Architecture
```
Client <---> Channel Layer <---> Chat Consumer
             (Redis)

Flow:
1. User connects: WebSocket handshake
2. Message sent: Consumer receives, broadcasts
3. Typing indicator: Real-time status
4. Message read: Update status, notify sender
```

### Signals & Realtime Updates (`signals_realtime.py`)
- Post-save signals for Activity creation
- Real-time notification propagation
- Activity feed updates

---

## 11. Caching Strategy

### Redis Configuration
```python
CACHES = {
    'default': {
        'BACKEND': 'django_redis.cache.RedisCache',
        'LOCATION': 'redis://127.0.0.1:6379/1',
        'OPTIONS': {
            'CLIENT_CLASS': 'django_redis.client.DefaultClient'
        }
    }
}
```

### Cached Views
- Project listings (with 5-min TTL)
- User profiles
- Notification counts

---

## 12. Performance Optimizations

### Database Optimization
- `select_related()` for foreign keys
- `prefetch_related()` for reverse relationships
- Indexed fields (user, project, created_at)

### Query Patterns
```python
# Good: Single query with prefetch
projects = Project.objects.prefetch_related('owner__student_profile')

# Good: Using select_related
messages = Message.objects.select_related('sender', 'room')

# Avoid: N+1 queries
for project in projects:
    print(project.owner.username)  # Database hit per iteration
```

### Pagination
- Default: 10-20 items per page
- Implemented in all list views

---

## 13. Configuration & Settings

### Environment Variables (.env)
```
DEBUG=True
SECRET_KEY=your-secret-key
ALLOWED_HOSTS=localhost,127.0.0.1
DATABASE_URL=postgresql://...
REDIS_URL=redis://localhost:6379/0
EMAIL_BACKEND=brevo/zepto
EMAIL_HOST_USER=your-api-key
GOOGLE_OAUTH_CLIENT_ID=...
GOOGLE_OAUTH_SECRET=...
```

### Django Settings Highlights
- **INSTALLED_APPS**: Django core, accounts, allauth, DRF
- **MIDDLEWARE**: Security, session, CSRF, auth
- **TEMPLATES**: Django templates with context processors
- **DATABASES**: PostgreSQL with environment URL
- **CHANNEL_LAYERS**: Redis for WebSocket messaging

---

## 14. File Handling

### Media Storage
```
media/
├── profile_photos/     # User avatars
├── project_files/      # Project attachments
├── message_files/      # Message attachments
└── document_uploads/   # Document storage
```

### Static Files
```
static/
├── css/                # Stylesheets
├── js/                 # JavaScript
├── images/             # Site images
└── vendor/             # Third-party libraries
```

---

## 15. Testing Infrastructure

### Test Files
- `test_login.py`: Authentication tests
- `test_profile_fix.py`: Profile tests
- `test_comments_api.py`: Comments functionality
- `test_services.py`: Business logic tests
- `test_email.py`: Email service tests

### Test Coverage
- Unit tests for models
- Integration tests for views
- API endpoint tests
- Email delivery tests

---

## 16. Deployment Configuration

### Production Settings
```python
DEBUG=False
SECURE_SSL_REDIRECT=True
SESSION_COOKIE_SECURE=True
CSRF_COOKIE_SECURE=True
ALLOWED_HOSTS=['yourdomain.com']
```

### WSGI Server
- Gunicorn (21.2.0) with multiple workers
- Static file serving via WhiteNoise

### Database
- PostgreSQL in production
- Migrations managed via `manage.py migrate`

---

## 17. Key Dependencies & Versions

| Package | Version | Purpose |
|---------|---------|---------|
| Django | 4.2.8 | Web framework |
| DRF | 3.14.0 | REST API |
| Channels | 4.0.0 | WebSocket support |
| django-allauth | 0.61.1 | OAuth providers |
| Redis | 5.0.1 | Message broker & cache |
| Gunicorn | 21.2.0 | Production server |
| psycopg2 | 2.9.9 | PostgreSQL driver |

---

## 18. Development Workflow

### Local Setup
```bash
# Install dependencies
pip install -r requirements.txt

# Database setup
python manage.py migrate

# Create superuser
python manage.py createsuperuser

# Start dev server
python manage.py runserver

# Start Redis (for WebSocket)
redis-server

# Start Channels worker
python manage.py runworker -v 3
```

### Debug Scripts
- `debug_profiles.py`: Profile debugging
- `debug_conversations.py`: Messaging debugging
- `diagnose_login.py`: Auth troubleshooting
- `test_email.py`: Email service testing

---

## 19. Common Workflows

### User Creates Project
```
1. Navigates to /post-project/
2. Fills ProjectForm
3. View validates and saves
4. Activity record created (signal)
5. Notifications sent to followers
6. Project appears in feed
```

### User Sends Message
```
1. WebSocket connects to /ws/chat/<room_id>/
2. Message sent via ChatConsumer
3. Broadcasted to room members
4. Message stored in database
5. Read receipt tracked
6. Real-time notification to recipients
```

### Project Comment Flow
```
1. User posts comment via /api/projects/<id>/comments/
2. Comment object created
3. Activity record generated
4. Project owner notified
5. Updated comment count
6. Appears in project detail
```

---

## 20. Summary Statistics

- **Models**: 20+ database models
- **Views**: 50+ view functions and classes
- **API Endpoints**: 40+ REST endpoints
- **URLs**: 150+ URL patterns
- **Templates**: 30+ HTML templates
- **JavaScript Files**: 10+ client-side scripts
- **Lines of Code**: 10,000+

---

## Architecture Diagram

```
┌─────────────────────────────────────────────────────┐
│                    Frontend (Browser)               │
│          - HTML Templates                          │
│          - JavaScript (Interactive)                │
│          - CSS Styling                             │
└────────────────┬────────────────────────────────────┘
                 │ HTTP/WebSocket
┌────────────────▼────────────────────────────────────┐
│           Django Application Server                 │
│  ┌─────────────────────────────────────────┐      │
│  │  URL Router (accounts/urls.py)          │      │
│  │  - /login/, /register/                  │      │
│  │  - /post-project/, /project-detail/     │      │
│  │  - /api/messages/, /api/chat-rooms/     │      │
│  └──────────┬──────────────────────────────┘      │
│  ┌──────────▼──────────────────────────────┐      │
│  │  View Layer (views.py, chat_api.py)     │      │
│  │  - Request handling                     │      │
│  │  - Business logic                       │      │
│  │  - Response rendering                   │      │
│  └──────────┬──────────────────────────────┘      │
│  ┌──────────▼──────────────────────────────┐      │
│  │  Models Layer (models.py)               │      │
│  │  - User, Project, Message               │      │
│  │  - Connection, Activity, Comment        │      │
│  └──────────┬──────────────────────────────┘      │
└────────────────┬────────────────────────────────────┘
                 │ Query
┌────────────────▼────────────────────────────────────┐
│  PostgreSQL Database                               │
│  - User tables                                     │
│  - Project data                                    │
│  - Messages & Chat rooms                           │
│  - Activities & Notifications                      │
└────────────────────────────────────────────────────┘

┌────────────────────────────────────────────────────┐
│              Redis Cache & Message Broker          │
│  - Session storage                                │
│  - WebSocket message distribution                │
│  - Real-time notifications                        │
└────────────────────────────────────────────────────┘

┌────────────────────────────────────────────────────┐
│          External Services                         │
│  - Google OAuth                                   │
│  - GitHub OAuth                                   │
│  - Email (Brevo/Zepto)                           │
└────────────────────────────────────────────────────┘
```

---

## Conclusion

UniSync is a well-structured, feature-rich collaborative platform with:
- Robust user authentication
- Real-time messaging
- Project discovery and collaboration
- Social features (likes, comments, followers)
- Team management
- Production-ready deployment configuration

The codebase follows Django best practices with proper separation of concerns, comprehensive error handling, and security implementations.
