# Comprehensive UniSync Codebase Analysis

## Project Overview

**Project Name:** UniSync  
**Type:** Django-based Web Application for University Student Collaboration  
**Repository:** https://github.com/Goku0090/uni  
**Framework:** Django 4.2.8 with Django REST Framework  
**Database:** PostgreSQL (psycopg2-binary)  

---

## Architecture Overview

```
auth_project/
├── auth_project/          # Django project settings
│   ├── settings.py       # Main configuration
│   ├── urls.py           # URL routing
│   ├── wsgi.py           # WSGI application
│   └── asgi.py           # ASGI for async
├── accounts/             # Main application
│   ├── models.py         # Data models
│   ├── views.py          # View functions
│   ├── urls.py           # URL patterns
│   ├── serializers.py    # DRF serializers
│   ├── forms.py          # Django forms
│   ├── services/         # Business logic
│   ├── templates/        # HTML templates
│   ├── static/           # CSS, JS, images
│   ├── migrations/       # Database migrations
│   ├── chat_api.py       # Messaging API
│   ├── comment_api.py    # Comments API
│   └── permissions.py    # Permission classes
```

---

## Core Models (10 Primary Models)

### 1. **StudentProfile**
- **Purpose:** Extended user profile for students
- **Key Fields:**
  - `user` (OneToOneField to User)
  - `full_name`, `college`, `location`
  - `interests`, `skills`, `project_interests` (JSON arrays)
  - `profile_photo` (ImageField with validation)
  - `bio`, `role_preference`
  - Social links: `github`, `linkedin`, `portfolio`, `behance`
  - `profile_completed` (Boolean)
  - `created_at`, `updated_at` (Timestamps)
- **Relationships:** One-to-one with User model

### 2. **OTP**
- **Purpose:** One-Time Password authentication
- **Fields:**
  - `email` (EmailField)
  - `otp_code` (6-digit string)
  - `purpose` (login/registration/reset)
  - `is_used` (Boolean)
  - `created_at`, `expires_at` (Timestamps)
- **Methods:**
  - `is_valid()` - Check if OTP is valid and not expired
  - `verify_otp()` - Verify OTP code
  - `generate_otp()` - Generate new OTP

### 3. **Connection**
- **Purpose:** User connections/following system
- **Fields:**
  - `from_user`, `to_user` (ForeignKeys to User)
  - `status` (pending/accepted/rejected)
  - `created_at`, `updated_at`
- **Use Case:** Connection requests and follower relationships

### 4. **Message**
- **Purpose:** Direct messaging between users
- **Fields:**
  - `sender`, `recipient` (ForeignKeys to User)
  - `content` (TextField)
  - `chat_room` (ForeignKey to ChatRoom, optional)
  - `message_type` (text/file/call)
  - `is_read` (Boolean)
  - `created_at`, `updated_at`
- **Related Models:** MessageFile, MessageReaction, MessageReadStatus

### 5. **ChatRoom**
- **Purpose:** Group chat management
- **Fields:**
  - `name`, `description`
  - `is_group` (Boolean)
  - `created_by` (ForeignKey to User)
  - `members` (ManyToManyField to User via ChatRoomMember)
  - `created_at`, `updated_at`
- **Related Models:** ChatRoomMember

### 6. **ChatRoomMember**
- **Purpose:** Membership tracking in chat rooms
- **Fields:**
  - `chat_room`, `user` (ForeignKeys)
  - `joined_at` (DateTime)
  - `is_admin` (Boolean)

### 7. **Project**
- **Purpose:** Project posting and collaboration
- **Fields:**
  - `title`, `description`, `status`
  - `owner` (ForeignKey to User)
  - `technologies`, `looking_for` (JSON arrays)
  - `category`, `visibility`
  - `collaboration_needs`
  - `github_link`
  - `created_at`, `updated_at`
- **Related Models:** Comment, Like, ProjectTeam

### 8. **Comment**
- **Purpose:** Comments on projects
- **Fields:**
  - `project`, `author` (ForeignKeys)
  - `content` (TextField)
  - `created_at`, `updated_at`
  - `likes` (ManyToManyField)
- **Features:** Likes on comments

### 9. **Notification**
- **Purpose:** User notifications
- **Fields:**
  - `user`, `actor` (ForeignKeys to User)
  - `notification_type`
  - `content`
  - `is_read` (Boolean)
  - `created_at`
- **Use Cases:** Likes, comments, follows, connection requests

### 10. **Activity**
- **Purpose:** Activity feed tracking
- **Fields:**
  - `user` (ForeignKey to User)
  - `activity_type`
  - `description`
  - `timestamp`

---

## Key Features & Functionality

### Authentication System
1. **Email/Password Login**
   - Form validation with Django forms
   - OTP verification for additional security
   
2. **Social Login**
   - Google OAuth via django-allauth
   - GitHub OAuth integration
   
3. **OTP-Based Authentication**
   - 6-digit OTP generation
   - Email delivery via ZeptoMail/Brevo
   - 10-minute expiration
   - Purpose-based OTPs (login/registration/reset)

### Messaging System
1. **Direct Messages**
   - One-to-one messaging between users
   - Read status tracking
   - Message reactions
   - File attachments
   
2. **Group Chats**
   - Create group chat rooms
   - Add/remove members
   - Admin controls
   - Typing indicators
   
3. **Advanced Features**
   - Message search
   - Draft messages
   - Message status indicators
   - Reaction system (emojis)

### Collaboration Features
1. **Project Management**
   - Create and edit projects
   - Specify collaboration needs
   - Filter by visibility (public/private)
   - Search and browse projects
   
2. **Commenting System**
   - Add comments to projects
   - Like comments
   - Edit/delete own comments
   - Live feed updates
   
3. **Team Management**
   - Invite users to project teams
   - Respond to team invitations
   - Remove team members
   - Project team member tracking

### User Discovery
1. **Find Collaborators**
   - Search for users by skills/interests
   - Filter by college, location, role
   - View user profiles
   - Send connection requests
   
2. **User Profiles**
   - Display profile information
   - Profile photo upload
   - Skills and interests showcase
   - Social links (GitHub, LinkedIn, Portfolio)
   - Profile completion tracking

### Activity & Feed
1. **Activity Feed**
   - Track user activities
   - Follow/unfollow users
   - Like projects and comments
   
2. **Notifications**
   - Real-time notifications
   - Notification badges
   - Mark as read functionality
   - Redirect on click

---

## API Endpoints Overview

### Authentication Endpoints
```
POST   /login/                          # User login
POST   /register/                       # User registration
GET    /logout/                         # User logout
POST   /verify-otp/<purpose>/          # OTP verification
POST   /resend-otp/<purpose>/          # Resend OTP
POST   /forgot-password/                # Password reset request
POST   /reset-password/                 # Reset password with OTP
```

### User Profile Endpoints
```
GET    /student-profile/               # Current user profile
GET    /user/<username>/                # User profile by username
POST   /student-details/                # Edit student details
GET    /user-profile/<user_id>/        # User profile API (JSON)
POST   /profile/                        # User profile endpoint
```

### Project Endpoints
```
GET    /                                # Projects feed/home
POST   /post-project/                   # Create project
PUT    /edit-project/<project_id>/     # Edit project
DELETE /delete-project/<project_id>/   # Delete project
GET    /project-detail/<project_id>/   # Project details
POST   /like-project/<project_id>/     # Like project
GET    /find-collaborators/            # Find collaborators
```

### Messaging Endpoints
```
GET/POST /messages/                     # Message list/create
POST     /chat/<user_id>/              # Direct chat
GET/POST /enhanced-messages/           # Enhanced messaging page
GET/POST /chat-rooms/                  # Chat room management
POST     /create-group-chat/           # Create group chat
POST     /add-reaction/<message_id>/   # Add message reaction
GET      /conversations/               # List conversations
```

### Comments Endpoints
```
GET    /projects/<project_id>/comments/      # Get comments
POST   /projects/<project_id>/comments/add/  # Add comment
DELETE /comments/<comment_id>/delete/        # Delete comment
PUT    /comments/<comment_id>/edit/          # Edit comment
```

### Social Endpoints
```
POST   /connect/<user_id>/                   # Send connection request
POST   /accept-connection/<connection_id>/   # Accept connection
POST   /reject-connection/<connection_id>/   # Reject connection
POST   /cancel-connection/<connection_id>/   # Cancel request
POST   /follow/<user_id>/                    # Follow user
GET    /my-connections/                      # List connections
```

### Notifications
```
GET    /notifications/                       # List notifications
POST   /mark-notification-read/<id>/        # Mark as read
```

---

## Technology Stack

### Backend
- **Framework:** Django 4.2.8
- **API:** Django REST Framework 3.14.0
- **Authentication:** django-allauth 0.61.1
- **Database:** PostgreSQL (psycopg2-binary 2.9.9)

### Frontend
- **Template Engine:** Django Templates
- **Styling:** CSS (Tailwind CSS likely)
- **JavaScript:** Vanilla JS (with AJAX for async operations)

### External Services
- **Email:** ZeptoMail/Brevo
- **File Storage:** AWS S3 (boto3)
- **Real-time:** Channels 4.0.0 (WebSockets)
- **Task Queue:** Celery 5.3.4
- **Cache:** Redis 5.0.1

### Development & DevOps
- **Deployment:** Render/Railway
- **Environment:** python-dotenv 1.0.0
- **Server:** Gunicorn 21.2.0, WhiteNoise 6.6.0
- **Monitoring:** Sentry 1.38.0

---

## Key Views & Functions (Major Implementations)

### Authentication Views
1. `login_view()` - Handle user login with email/OTP
2. `register_view()` - User registration
3. `logout_view()` - User logout
4. `verify_otp_view()` - Verify OTP code
5. `forgot_password_view()` - Password reset initiation
6. `reset_password_view()` - Complete password reset

### Project Views
1. `post_project()` - Create new project
2. `project_detail()` - Display project details
3. `edit_project()` - Edit project information
4. `delete_project()` - Delete project
5. `like_project()` - Like/unlike project
6. `search_projects()` - Search and filter projects
7. `project_feed()` - Display projects feed

### Messaging Views
1. `message_view()` - Display messaging page
2. `chat_view()` - One-to-one chat
3. `enhanced_messages_view()` - New messaging interface
4. `create_group_chat()` - Create group chat room
5. `add_reaction()` - Add emoji reaction to message

### User & Connection Views
1. `user_profile()` - Display user profile
2. `find_collaborators()` - Collaborator search page
3. `connect_view()` - Send connection request
4. `accept_connection()` - Accept connection
5. `follow_user()` - Follow user

### Comment Views
1. `add_comment()` - Add comment to project
2. `get_comments()` - Fetch comments (API)
3. `delete_comment()` - Delete comment
4. `edit_comment()` - Edit comment

---

## Database Relationships

```
User (Django Auth)
├── StudentProfile (1:1)
├── Project (1:N) [owner]
├── Message (1:N) [sender/recipient]
├── Connection (M:N) [from_user/to_user]
├── Notification (1:N)
├── ChatRoom (1:N) [created_by]
├── ChatRoomMember (1:N)
├── Comment (1:N) [author]
├── Like (1:N)
├── Follow (1:N)
└── Activity (1:N)

Project
├── Owner (User)
├── Comment (1:N)
├── Like (1:N)
├── ProjectTeam (1:1)
└── ProjectTeamMember (1:N)

Message
├── Sender (User)
├── Recipient (User)
├── ChatRoom (Project)
├── MessageFile (1:N)
├── MessageReaction (1:N)
└── MessageReadStatus (1:N)

ChatRoom
├── Creator (User)
├── Members (M:N via ChatRoomMember)
└── Messages (1:N)
```

---

## Security Features

### Authentication Security
- CSRF token protection
- Session-based authentication
- OTP email verification
- Password hashing (Django default)
- OAuth 2.0 with social providers

### Permission System
- Login required decorators (@login_required)
- Custom permission classes (IsOwnerOrReadOnly, etc.)
- User ownership validation
- Admin checks for certain operations

### Configuration
- Environment-based settings (.env)
- Secret key management
- ALLOWED_HOSTS configuration
- CORS headers support
- Secure session/cookie flags

---

## Performance Optimizations

### Caching
- Django cache framework
- Redis integration for cache backend
- Page-level caching decorators
- Query result caching

### Database Optimization
- Select_related and prefetch_related usage
- Database connection pooling
- PostgreSQL-specific optimizations

### Frontend
- Static file compression (WhiteNoise)
- CSS/JS minification
- Image optimization
- Lazy loading support

---

## Current Issues & Recent Fixes

### Implemented Fixes
1. **Comments System** - Live feed integration for project comments
2. **Login Functionality** - Email/OTP authentication working
3. **Profile Features** - Profile photo upload and display
4. **Project Filtering** - Visibility-based filtering
5. **Messaging System** - Direct messages and group chats
6. **Notifications** - Real-time notification badges
7. **Find Collaborators** - Enhanced UI with filtering

### Known Areas
- Performance optimization for large datasets
- WebSocket real-time updates (Channels configured)
- File upload handling improvements
- Email delivery reliability

---

## File Structure Summary

```
auth_project/
├── static/                # CSS, JavaScript, Images
├── templates/             # HTML templates
│   ├── base.html         # Base template
│   ├── dashboard.html    # Dashboard
│   ├── login.html        # Login page
│   ├── register.html     # Registration
│   ├── project_detail.html
│   ├── find_collaborators.html
│   ├── features/         # Feature templates
│   │   ├── messages.html # Messaging UI
│   │   ├── chat.html    # Chat UI
│   │   └── ...
│   └── ...
├── migrations/           # Database migrations
├── services/             # Business logic services
├── tests.py              # Unit tests
├── urls.py              # URL patterns
├── views.py             # Main views (3000+ lines)
├── models.py            # Database models
├── serializers.py       # API serializers
├── forms.py             # Django forms
├── permissions.py       # Permission classes
├── chat_api.py          # Chat API views
├── comment_api.py       # Comment API views
└── ...
```

---

## Configuration & Settings

### Key Settings
- **DEBUG:** Environment variable controlled
- **DATABASE_URL:** PostgreSQL connection string
- **ALLOWED_HOSTS:** Environment variable list
- **SECRET_KEY:** Environment variable (auto-generated for dev)
- **STATIC_URL:** `/static/`
- **MEDIA_URL:** `/media/`
- **EMAIL_BACKEND:** ZeptoMail or Brevo

### Installed Apps
- Django core (auth, admin, sessions, etc.)
- django-allauth (social auth)
- djangorestframework (API)
- channels (WebSockets)
- corsheaders (CORS)
- crispy_forms (Form rendering)

---

## Development & Deployment

### Local Development
```bash
python manage.py runserver
```

### Database Management
```bash
python manage.py makemigrations
python manage.py migrate
```

### Environment Setup
- `.env` file with configuration
- `.env.template` for reference
- PostgreSQL database required
- Optional: Redis for caching

### Deployment Targets
- **Render:** Primary deployment platform
- **Railway:** Alternative deployment option
- **Docker:** Containerization support (via Procfile/railway.json)

---

## Testing Infrastructure

### Test Files Present
- `test_login.py` - Authentication tests
- `test_email.py` - Email functionality tests
- `test_comments_api.py` - Comment API tests
- `test_profile_view.py` - Profile view tests
- `test_filter.py` - Filtering logic tests

### Test Frameworks
- pytest 7.4.3
- pytest-django 4.7.0
- Selenium 4.16.0 (browser automation)

---

## Code Quality Tools

- **Black:** Code formatting
- **Flake8:** Style guide enforcement
- **isort:** Import sorting
- **mypy:** Type checking

---

## Summary Statistics

- **Primary Models:** 10+
- **API Endpoints:** 50+
- **URL Patterns:** 129
- **View Functions:** 100+
- **Templates:** 40+
- **Services:** Custom utilities for NLP, filtering, profile analysis
- **Authentication Methods:** 3 (Email/OTP, Google OAuth, GitHub OAuth)

---

## Next Steps & Recommendations

1. **Performance:** Implement database query optimization
2. **Real-time:** Enable WebSocket connections for live updates
3. **Testing:** Expand test coverage to 80%+
4. **Monitoring:** Configure Sentry for error tracking
5. **Caching:** Implement Redis caching for frequently accessed data
6. **API:** Add API documentation with drf-spectacular
7. **Security:** Implement rate limiting on API endpoints

---

**Analysis Date:** February 5, 2026  
**Codebase Status:** Production-Ready with Recent Enhancements  
**Last Major Update:** Comments system, messaging improvements, notifications

