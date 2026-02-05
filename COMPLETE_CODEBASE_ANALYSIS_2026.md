# UniSync - Complete Codebase Analysis 2026

## Project Overview

**UniSync** is a Django-based web application that serves as a student collaboration platform where students can discover and collaborate on projects, connect with peers, and build their professional networks.

**Repository**: https://github.com/Goku0090/uni
**Tech Stack**: Django 4.2.8 + DRF + PostgreSQL + Redis + Channels

---

## Architecture Overview

### Layer 1: Frontend
- **Technology**: Django Templates (HTML/CSS/JavaScript)
- **Static Files**: CSS, JavaScript, Images served via WhiteNoise
- **Media Files**: User profile photos, project assets

### Layer 2: Authentication & Security
- **Django Auth**: Standard Django user authentication
- **django-allauth**: Social login integration (Google, GitHub)
- **OTP System**: Email-based one-time password authentication
- **Middleware**: CSRF protection, security headers, session management

### Layer 3: API Layer
- **REST Framework**: DRF for RESTful API endpoints
- **Chat API**: Real-time messaging endpoints
- **Comment API**: Project feedback system
- **User Profile API**: User management and profile retrieval

### Layer 4: Business Logic & Services
- **AuthService**: Handles welcome emails and authentication-related operations
- **StudentProfileNLP**: NLP-based skill extraction and analysis
- **ProjectVisibilityFilter**: Manages project visibility and filtering logic

### Layer 5: Data Models
Core models representing the system's domain logic:
- **User**: Django's built-in User model extended with StudentProfile
- **StudentProfile**: Extended user information (bio, skills, college, interests)
- **Project**: Collaboration projects with technologies and team requirements
- **Message/ChatRoom**: Direct and group messaging system
- **Comment**: Project-specific comments and feedback
- **Connection**: User-to-user connection/networking requests
- **Notification**: Activity notifications and alerts
- **Activity**: User activity feed tracking

### Layer 6: Database & Cache
- **PostgreSQL**: Primary data store (configured via dj-database-url)
- **Redis**: Caching layer for sessions and message caching
- **Media Storage**: File uploads for profile photos and project assets

### Layer 7: External Services
- **Email**: Brevo/Zeptomail for email delivery
- **Social Auth**: Google & GitHub OAuth
- **NLP**: NLTK for natural language processing
- **RapidAPI**: External API integration

---

## Core Database Models

### Authentication Models

#### User (Django Built-in)
```python
- id (PK)
- username (unique)
- email (unique)
- password (hashed)
- first_name, last_name
- date_joined
- last_login
- is_active, is_staff, is_superuser
```

#### StudentProfile (1-to-1 with User)
**Purpose**: Extended user profile for student-specific information

Fields:
- `full_name`: Full name display
- `college`: Student's college/institution
- `location`: Geographic location
- `bio`: User biography/description
- `profile_photo`: Avatar image (ImageField)
- `interests`: JSONField array of interests
- `skills`: JSONField array of technical skills
- `project_interests`: JSONField array of project preferences
- `role_preference`: Preferred role in projects
- Social links: GitHub, LinkedIn, portfolio, Behance

#### OTP (One-Time Password)
**Purpose**: Email-based authentication for login/registration/password reset

Fields:
- `email`: Target email address
- `otp_code`: 6-digit code
- `purpose`: 'login', 'registration', or 'reset'
- `is_used`: Validation flag
- `created_at`, `expires_at`: Time tracking (5-minute expiry)

---

### Collaboration Models

#### Project
**Purpose**: Core collaboration item representing a project

Fields:
- `user`: ForeignKey to creator (User)
- `title`, `description`: Project information
- `technologies`: JSONField array of tech stack
- `looking_for`: JSONField array of required roles
- `category`: 'web', 'mobile', 'ai', 'data', 'blockchain', 'iot', 'game', 'other'
- `timeline`: Project timeline
- `collaboration_needs`: Text description of needs
- `github_link`: Project repository URL
- `is_active`: Status flag
- `created_at`, `updated_at`: Timestamps

#### ProjectTeam & ProjectTeamMember
**Purpose**: Team management for collaborative projects

Fields (ProjectTeam):
- `project`: ForeignKey to Project
- `name`: Team name
- `description`: Team description

Fields (ProjectTeamMember):
- `team`: ForeignKey to ProjectTeam
- `user`: ForeignKey to User
- `role`: 'owner', 'lead', 'member'
- `joined_at`: Membership timestamp

#### ProjectTeamInvitation
**Purpose**: Invite users to join project teams

Fields:
- `team`: ForeignKey to ProjectTeam
- `from_user`: Inviter (ForeignKey to User)
- `to_user`: Invitee (ForeignKey to User)
- `status`: 'pending', 'accepted', 'rejected'

---

### Social & Network Models

#### Connection
**Purpose**: User-to-user connection/networking requests

Fields:
- `sender`: ForeignKey to requesting user
- `receiver`: ForeignKey to receiving user
- `status`: 'pending', 'accepted', 'rejected'
- `created_at`, `updated_at`: Timestamps

#### Follow
**Purpose**: User following relationships

Fields:
- `follower`: ForeignKey to follower user
- `following`: ForeignKey to followed user
- `created_at`: Timestamp

#### Comment
**Purpose**: Comments on projects in live feed

Fields:
- `user`: ForeignKey to commenting user
- `project`: ForeignKey to Project
- `content`: Comment text (max 1000 chars)
- `created_at`, `updated_at`: Timestamps

#### Like
**Purpose**: Likes on projects

Fields:
- `user`: ForeignKey to user who liked
- `project`: ForeignKey to Project
- `created_at`: Timestamp

#### Activity
**Purpose**: User activity feed logging

Fields:
- `user`: ForeignKey to user performing activity
- `activity_type`: 'profile_updated', 'project_created', 'project_liked', 'connection_made', 'message_sent', 'comment_added', 'user_followed', 'task_completed', 'milestone_completed'
- `title`, `description`: Activity details
- `project`, `target_user`, `connection`: Related objects
- `is_public`: Visibility flag

---

### Messaging Models

#### ChatRoom
**Purpose**: Container for group chats, direct messages, or project chats

Fields:
- `name`: Room name (optional)
- `chat_type`: 'direct', 'group', 'project'
- `project`: ForeignKey to Project (for project chats)
- `is_active`: Status flag
- `created_at`, `created_by`: Metadata

#### ChatRoomMember
**Purpose**: Membership and permissions in chat rooms

Fields:
- `chat_room`: ForeignKey to ChatRoom
- `user`: ForeignKey to User
- `role`: 'owner', 'admin', 'member'
- `is_active`: Membership status
- `joined_at`: Timestamp

#### Message
**Purpose**: Individual messages in chat rooms or direct messages

Fields:
- `sender`: ForeignKey to sending user
- `receiver`: ForeignKey to receiving user (for DMs, null for group)
- `chat_room`: ForeignKey to ChatRoom (for group chats)
- `content`: Message text
- `message_type`: 'text', 'file', 'image', 'call'
- `call_type`: 'voice' or 'video' (for call messages)
- `reply_to`: Self-referencing FK for message threading
- `created_at`, `updated_at`: Timestamps

#### MessageReadStatus
**Purpose**: Track which users have read messages (scalable design)

Fields:
- `message`: ForeignKey to Message
- `user`: ForeignKey to reading user
- `read_at`: Timestamp when read

#### MessageReaction
**Purpose**: Emoji reactions to messages

Fields:
- `message`: ForeignKey to Message
- `user`: ForeignKey to reacting user
- `reaction`: Emoji or text reaction
- `created_at`: Timestamp

#### MessageFile
**Purpose**: File attachments in messages

Fields:
- `message`: ForeignKey to Message
- `file`: ForeignKey to File

#### File
**Purpose**: File upload tracking

Fields:
- `user`: ForeignKey to uploader
- `file`: FileField with upload_to='chat_files/'
- `filename`: Original filename
- `file_size`: Size in bytes
- `file_type`: MIME type
- `uploaded_at`: Timestamp

---

### Notification & Status Models

#### Notification
**Purpose**: Activity notifications for users

Fields:
- `user`: ForeignKey to recipient user
- `notification_type`: 'connection_request', 'connection_accepted', 'message', 'project_like', 'project_comment', 'team_invitation', 'follow'
- `title`, `message`: Notification content
- `from_user`: Source user (optional)
- `connection`, `message_obj`: Related objects
- `is_read`: Read status
- `read_at`: Timestamp when marked read
- `created_at`: Timestamp

#### UserStatus
**Purpose**: Track online/offline status and last activity

Fields:
- `user`: OneToOneField to User
- `is_online`: Current online status
- `last_seen`: Last activity timestamp
- `current_room`: WebSocket room name (optional)

---

### Project Management Models

#### ProjectTask
**Purpose**: Tasks within a project

Fields:
- `project`: ForeignKey to Project
- `title`, `description`: Task details
- `assigned_to`: ForeignKey to User (optional)
- `priority`: 'high', 'medium', 'low'
- `status`: 'todo', 'in_progress', 'done'
- `due_date`: Target completion date
- `created_at`, `updated_at`: Timestamps

#### ProjectMilestone
**Purpose**: Project milestones/phases

Fields:
- `project`: ForeignKey to Project
- `title`, `description`: Milestone details
- `target_date`: Completion date
- `is_completed`: Status flag
- `created_at`, `updated_at`: Timestamps

---

### Analytics Models

#### UserStats
**Purpose**: User statistics and metrics

Fields:
- `user`: OneToOneField to User
- `profile_views`: Counter
- `projects_created`: Counter
- `connections_count`: Counter
- `followers_count`: Counter
- `last_updated`: Timestamp

---

## API Endpoints

### Authentication Endpoints
| Method | Endpoint | Purpose |
|--------|----------|---------|
| POST | `/accounts/login/` | User login |
| POST | `/accounts/register/` | New user registration |
| GET | `/accounts/logout/` | User logout |
| POST | `/accounts/forgot-password/` | Forgot password request |
| POST | `/accounts/reset-password/` | Reset password with token |
| POST | `/accounts/verify-otp/<purpose>/` | Verify OTP |
| POST | `/accounts/resend-otp/<purpose>/` | Resend OTP |

### Profile Endpoints
| Method | Endpoint | Purpose |
|--------|----------|---------|
| GET | `/api/user-profile/<user_id>/` | Get user profile |
| GET | `/accounts/profile/` | User profile API view |
| POST | `/accounts/student-details/` | Create student profile |
| GET | `/accounts/student-profile/` | Get student profile |
| POST | `/accounts/check-username/` | Check username availability |
| POST | `/accounts/check-email/` | Check email availability |

### Project Endpoints
| Method | Endpoint | Purpose |
|--------|----------|---------|
| POST | `/accounts/post-project/` | Create project |
| GET | `/accounts/project-detail/<project_id>/` | Get project details |
| POST | `/accounts/edit-project/<project_id>/` | Edit project |
| DELETE | `/accounts/delete-project/<project_id>/` | Delete project |
| GET | `/accounts/my-projects/` | User's projects |
| GET | `/accounts/explore-projects/` | Browse all projects |
| POST | `/accounts/like-project/<project_id>/` | Like a project |

### Comment & Activity Endpoints
| Method | Endpoint | Purpose |
|--------|----------|---------|
| GET | `/api/projects/<project_id>/comments/` | Get project comments |
| POST | `/api/projects/<project_id>/comments/add/` | Add comment |
| DELETE | `/api/comments/<comment_id>/delete/` | Delete comment |
| PUT | `/api/comments/<comment_id>/edit/` | Edit comment |
| GET | `/accounts/activity-feed/` | User activity feed |

### Messaging Endpoints
| Method | Endpoint | Purpose |
|--------|----------|---------|
| GET/POST | `/api/chat-rooms/` | List/create chat rooms |
| GET | `/api/chat-rooms/<id>/` | Get chat room details |
| POST | `/api/direct-message/` | Send direct message |
| GET/POST | `/api/messages/` | List/create messages |
| GET | `/api/messages/<pk>/` | Get message details |
| POST | `/api/messages/<message_id>/reactions/` | Add reaction to message |
| GET | `/api/conversations/` | List conversations |

### Connection & Network Endpoints
| Method | Endpoint | Purpose |
|--------|----------|---------|
| POST | `/accounts/send-connection/<user_id>/` | Send connection request |
| POST | `/accounts/accept-connection/<connection_id>/` | Accept connection |
| POST | `/accounts/reject-connection/<connection_id>/` | Reject connection |
| GET | `/accounts/my-connections/` | User's connections |
| POST | `/accounts/follow/<user_id>/` | Follow user |
| GET | `/accounts/user/<username>/` | View user profile |

### Team & Collaboration Endpoints
| Method | Endpoint | Purpose |
|--------|----------|---------|
| POST | `/accounts/invite-to-team/<project_id>/` | Invite to project team |
| POST | `/accounts/respond-team-invitation/<invitation_id>/` | Respond to invitation |
| POST | `/accounts/remove-team-member/<project_id>/<user_id>/` | Remove team member |

### Utility Endpoints
| Method | Endpoint | Purpose |
|--------|----------|---------|
| GET | `/accounts/help/` | Help center |
| GET | `/accounts/find-collaborators/` | Find collaborators |
| POST | `/api/college-search/` | Search colleges |
| POST | `/api/validate-college/` | Validate college |
| GET | `/api/user-stats/` | Get user statistics |
| POST | `/api/nlp-analyze/` | NLP analysis |

---

## Key Features & Components

### 1. Authentication System
- **Standard Login/Registration**: Email and password-based
- **OTP Authentication**: 6-digit codes sent via email with 5-minute expiry
- **Social Login**: Google and GitHub OAuth integration via django-allauth
- **Password Reset**: Email-based password reset flow
- **Email Backends**: Support for Brevo and Zeptomail services

### 2. User Profiles
- Extended StudentProfile with skills, interests, and college information
- Profile photo upload with validation
- Social links (GitHub, LinkedIn, portfolio, Behance)
- Profile completion tracking
- NLP-based skill extraction from bio

### 3. Project Management
- Create and manage projects with technologies, timeline, and team requirements
- Project visibility filtering based on user preferences
- Project categories: Web, Mobile, AI/ML, Data Science, Blockchain, IoT, Game Dev
- Team management with invitations and role-based access
- Task and milestone tracking within projects
- GitHub repository integration

### 4. Collaboration Features
- **Comments**: Real-time project comments without connection requirement
- **Live Feed**: Activity stream showing project comments, likes, and updates
- **Project Discovery**: Browse and search projects with advanced filtering
- **Visibility Control**: Users can set project visibility preferences

### 5. Messaging System
- **Direct Messages**: One-to-one conversation between users
- **Group Chats**: Multiple users in chat rooms
- **Message Features**:
  - Text messages with rich content
  - File and image attachments
  - Message reactions (emojis)
  - Message threading/replies
  - Read receipts and status
  - Typing indicators
  - Draft message saving

### 6. Social Network
- **Connections**: Request/accept user connections
- **Following**: Follow users for activity updates
- **Notifications**: Real-time alerts for connections, comments, messages, likes
- **Activity Feed**: Public activity tracking for network visibility

### 7. Real-time Features
- WebSocket support via Django Channels
- Redis for message caching
- Online status tracking
- Typing indicators
- Real-time notifications

---

## Technology Stack Details

### Backend
- **Framework**: Django 4.2.8
- **API**: Django REST Framework (DRF) 3.14.0
- **Real-time**: Django Channels 4.0.0 with Channels Redis
- **Authentication**: django-allauth 0.61.1
- **Database Drivers**: psycopg2-binary 2.9.9

### Database & Cache
- **Primary DB**: PostgreSQL (via dj-database-url)
- **Cache**: Redis 5.0.1 with django-redis 5.4.0
- **ORM**: Django ORM with migrations

### Frontend Dependencies
- **Templating**: Django Templates
- **Styling**: Tailwind CSS (via CDN)
- **JavaScript**: Vanilla JS, some jQuery

### Email Services
- **Primary**: Brevo (formerly Sendinblue)
- **Fallback**: Zeptomail
- Custom email backends: `BrevoBrevBackend` and `ZeptoMailBackend`

### External Services
- **Social Auth**: Google OAuth 2.0, GitHub OAuth 2.0
- **NLP**: NLTK 3.8.1 for text processing
- **API Integration**: RapidAPI 1.0.0
- **File Processing**: Pandas 2.1.4, OpenPyXL 3.1.2
- **Image Processing**: Pillow 10.1.0

### Development & Deployment
- **Web Server**: Gunicorn 21.2.0
- **Static Files**: WhiteNoise 6.6.0
- **Environment**: python-dotenv 1.0.0
- **Code Quality**: Black, Flake8, isort, mypy
- **Testing**: pytest, pytest-django, Selenium
- **Monitoring**: Sentry SDK 1.38.0
- **Documentation**: Sphinx 7.2.6

### Security
- **CORS**: django-cors-headers 4.3.1
- **SSL/TLS**: SECURE_SSL_REDIRECT configuration
- **CSRF Protection**: Django middleware enabled
- **Security Headers**: X-Frame-Options, etc.

---

## Business Logic & Services

### AuthService
**Location**: `accounts/services/auth_service.py`

**Responsibilities**:
- `send_welcome_email()`: Send welcome email to new users
- `send_welcome_back_email()`: Send welcome back email to returning users
- `send_password_reset_email()`: Send password reset links

**Features**:
- HTML and plaintext email templates
- Gradient styling with brand colors
- Feature highlights in email body
- Professional footer with timestamps

### StudentProfileNLP
**Purpose**: Extract skills and interests from user bio using NLP

**Features**:
- Tokenization and lemmatization
- Skill extraction from text
- Interest categorization
- Integration with NLTK

### ProjectVisibilityFilter
**Purpose**: Filter projects based on user preferences and visibility rules

**Features**:
- Category-based filtering
- Skill-based recommendation
- College-based filtering (optional)
- Public/private project visibility
- Connection-based visibility

---

## Request/Response Flow Examples

### Login Flow
```
User POST /accounts/login/
  ↓
LoginView validates credentials
  ↓
OTP generated if enabled
  ↓
send_otp_email() via Email service
  ↓
User receives OTP in email
  ↓
User POST /accounts/verify-otp/login/
  ↓
verify_otp_view validates OTP
  ↓
Session created, user logged in
  ↓
Redirect to dashboard
```

### Project Comment Flow
```
User POST /api/projects/<id>/comments/add/
  ↓
add_comment() validates input
  ↓
Comment object created in DB
  ↓
Activity log created
  ↓
create_notification() for project owner
  ↓
Response returns comment with user info
```

### Direct Message Flow
```
User A POST /api/direct-message/
  ↓
DirectMessageView creates Message
  ↓
Message stored in DB
  ↓
WebSocket broadcast to Room
  ↓
Redis caches recent messages
  ↓
MessageReadStatus created for recipient
  ↓
Response confirms delivery
```

---

## Error Handling & Validation

### Input Validation
- `sanitize_input()`: Removes HTML tags and dangerous characters
- Field validators in forms and serializers
- Length limits on text fields (comments: 1000 chars max)
- Email validation using Django validators
- File type and size validation

### Error Responses
- Consistent JSON error format
- HTTP status codes (400, 401, 403, 404, 405, 500)
- User-friendly error messages
- Logging of errors for debugging
- Try-catch blocks with fallbacks

### Permission Checks
- `login_required` decorator for protected views
- Custom permission classes in DRF
- Ownership verification before updates/deletes
- Role-based access control (owner, admin, member)

---

## Database Relationships

### Key Foreign Key Relationships
```
User (1) ──→ (M) StudentProfile
User (1) ──→ (M) Project
User (1) ──→ (M) Comment
User (1) ──→ (M) Message
User (1) ──→ (M) Connection
User (1) ──→ (M) Notification
User (1) ──→ (M) Activity

Project (1) ──→ (M) Comment
Project (1) ──→ (M) Like
Project (1) ──→ (M) ProjectTeam
Project (1) ──→ (M) ChatRoom

ChatRoom (1) ──→ (M) Message
ChatRoom (1) ──→ (M) ChatRoomMember

Message (1) ──→ (M) MessageReadStatus
Message (1) ──→ (M) MessageReaction
Message (1) ──→ (M) MessageFile

ProjectTeam (1) ──→ (M) ProjectTeamMember
ProjectTeam (1) ──→ (M) ProjectTeamInvitation

User (M) ──→ (M) User [Connection]
User (M) ──→ (M) User [Follow]
```

### Unique Constraints
- User: username, email
- Connection: (sender, receiver)
- Like: (user, project)
- Follow: (follower, following)
- ChatRoomMember: (chat_room, user)
- MessageReadStatus: (message, user)
- MessageReaction: (message, user, reaction)
- MessageFile: (message, file)

---

## Performance Optimizations

### Caching Strategy
- Redis for session storage
- Message caching for recent conversations
- User status caching
- Database query result caching

### Query Optimization
- `select_related()` for ForeignKey relationships
- `prefetch_related()` for reverse ForeignKey/M2M
- Pagination for large result sets (10-20 items per page)
- Indexed fields: user IDs, timestamps, status flags

### Database Indexes
- Composite indexes on common filter combinations
- Timestamp indexes for ordering operations
- User ID indexes for joins

---

## Security Considerations

### Authentication
- OTP expiry validation (5 minutes)
- Password hashing using Django's PBKDF2
- Social login token validation
- Session timeout management

### Authorization
- Login required decorators
- Object-level permission checks
- Role-based access control
- CSRF token validation

### Data Protection
- Input sanitization to prevent XSS
- SQL injection prevention via ORM
- File upload validation
- Email validation

### Configuration
- Environment variables for sensitive data
- Secret key management
- Debug mode disabled in production
- SSL/TLS configuration options

---

## Development Workflow

### Project Structure
```
auth_project/          # Django project directory
├── accounts/          # Main application
│   ├── migrations/    # Database migrations
│   ├── services/      # Business logic services
│   ├── static/        # Static files
│   ├── templates/     # HTML templates
│   ├── models.py      # Database models
│   ├── views.py       # View functions/classes
│   ├── urls.py        # URL routing
│   ├── serializers.py # DRF serializers
│   ├── forms.py       # Django forms
│   ├── chat_api.py    # Chat endpoints
│   └── comment_api.py # Comment endpoints
├── auth_project/      # Project settings
│   ├── settings.py    # Configuration
│   ├── urls.py        # Root URL config
│   ├── wsgi.py        # WSGI app
│   └── asgi.py        # ASGI app (Channels)
├── media/             # User uploads
├── static/            # Collected static files
├── templates/         # Root templates
├── manage.py          # Django CLI
└── requirements.txt   # Dependencies
```

### Environment Configuration
Key environment variables:
- `DEBUG`: Enable/disable debug mode
- `SECRET_KEY`: Django secret key
- `ALLOWED_HOSTS`: Allowed domain names
- `DATABASE_URL`: PostgreSQL connection string
- `REDIS_URL`: Redis connection string
- `DEFAULT_FROM_EMAIL`: Sender email
- `EMAIL_BACKEND`: Email service configuration
- `SOCIAL_AUTH_GOOGLE_OAUTH2_KEY`: Google OAuth credentials
- `SOCIAL_AUTH_GITHUB_KEY`: GitHub OAuth credentials

---

## Testing & Quality

### Test Files
- Unit tests in `tests.py`
- API tests in `test_*.py` files
- Fixtures for test data
- Mocking for external services

### Code Quality Tools
- **Black**: Code formatting
- **Flake8**: Linting
- **isort**: Import sorting
- **mypy**: Type checking
- **pytest**: Test framework
- **pytest-django**: Django test utilities

### CI/CD Ready
- Debug toolbar for development
- Sentry integration for error monitoring
- Database URL configuration for deployment

---

## Deployment Configuration

### Production Deployment
Supports deployment to:
- **Render.com**: Via `render.yaml` configuration
- **Railway**: Via `railway.json` configuration
- **Heroku**: Via `Procfile` (legacy)

### Environment Considerations
- `SECURE_SSL_REDIRECT`: Force HTTPS
- `SESSION_COOKIE_SECURE`: Secure session cookies
- `CSRF_COOKIE_SECURE`: Secure CSRF cookies
- `STATIC_ROOT`: WhiteNoise static file collection
- `ALLOWED_HOSTS`: Production domain names

---

## Known Issues & Maintenance Notes

### Areas Requiring Attention
1. Email service configuration (Brevo/Zeptomail)
2. Social OAuth setup for production
3. Redis cache invalidation strategy
4. WebSocket/Channels connection pooling
5. File upload size limits and storage

### Performance Considerations
- Message archival for old conversations
- Activity feed pagination
- Comment count caching
- User online status cleanup

### Future Enhancements
- Full-text search for projects/comments
- Video conferencing integration
- Advanced project filtering
- Mobile app API optimization
- Real-time collaboration tools

---

## Summary

UniSync is a comprehensive student collaboration platform with:
- **Multi-factor authentication** (password + OTP + social)
- **Rich messaging** (DMs, groups, files, reactions)
- **Social networking** (connections, following, activity feed)
- **Project management** (CRUD, teams, tasks, milestones)
- **Real-time features** (WebSockets, notifications, typing indicators)
- **Scalable architecture** (PostgreSQL, Redis, REST API, separation of concerns)

The codebase follows Django best practices with clear separation of concerns, comprehensive models, and extensible API endpoints suitable for both web and mobile clients.
