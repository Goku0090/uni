# Complete Codebase Analysis - UniSync (UniSinQ) Platform

## Project Overview

**Project Name**: UniSync (Rebranded to UniSinQ)  
**Technology Stack**: Django + Django REST Framework + Channels (WebSockets) + SQLite/PostgreSQL  
**Frontend**: HTML/CSS/JavaScript with real-time WebSocket updates  
**Purpose**: Collaborative platform for university students to discover projects, find collaborators, and manage teamwork

---

## Architecture Overview

### Technology Stack
- **Backend**: Django 4.x + DRF (Django REST Framework)
- **Real-time**: Django Channels (WebSockets) for live messaging and notifications
- **Database**: SQLite (development) / PostgreSQL (production)
- **Email**: Brevo/ZeptoMail for OTP and notifications
- **Frontend**: HTML5, CSS3, Vanilla JavaScript, Bootstrap
- **Authentication**: Django auth + google-oauth2 + OTP-based login
- **Deployment**: Render/Railway

---

## Project Structure

```
auth_project/
├── accounts/                    # Main Django app
│   ├── models.py               # Database models
│   ├── views.py                # View logic (3467 lines)
│   ├── urls.py                 # URL routing
│   ├── serializers.py          # DRF serializers
│   ├── forms.py                # Django forms
│   ├── consumers.py            # WebSocket consumers
│   ├── routing.py              # WebSocket routing
│   ├── signals_realtime.py     # Django signals for real-time
│   ├── comment_api.py          # Comment API endpoints
│   ├── chat_api.py             # Chat API endpoints
│   ├── permissions.py          # DRF permissions
│   ├── utils.py                # Utility functions
│   ├── templates/              # HTML templates
│   ├── static/                 # CSS, JS files
│   └── services/               # Service layer
├── auth_project/               # Django settings
│   ├── settings.py
│   ├── urls.py
│   ├── asgi.py                 # WebSocket config
│   └── wsgi.py
├── manage.py                   # Django management
└── requirements.txt
```

---

## Core Database Models

### 1. **StudentProfile** (Extended User Profile)
```python
Fields:
- full_name, college, location, bio
- profile_photo (ImageField)
- skills, interests (JSONField - arrays)
- project_interests, role_preference
- Social links: github, linkedin, portfolio, behance
- Profile completion tracking
```

### 2. **Project** (Core Entity)
```python
Fields:
- title, description, category
- technologies, collaboration_needs
- timeline, github_link
- owner (ForeignKey to User)
- visibility: public/private/draft
- budget, location
- Status tracking
```

### 3. **User Relationships**
- **Connection**: Pending/Accepted/Rejected connection requests between users
- **Follow**: User following system
- **Message**: Direct messages with read status tracking
- **ChatRoom**: Group chat support with members
- **ProjectTeam/ProjectMember**: Project team members with roles

### 4. **Project Management**
- **ProjectTask**: Tasks within projects (status, priority, assigned_to)
- **ProjectMilestone**: Project milestones
- **ProjectInvitation**: Invitations to join projects

### 5. **Social Features**
- **Comment**: Comments on projects (live feed)
- **Like**: Likes on projects
- **Activity**: Activity feed tracking
- **Notification**: User notifications
- **Follow**: Follow system

### 6. **Messaging**
- **Message**: Messages (text, file, image, call)
- **MessageReadStatus**: Read status tracking for scalability
- **MessageReaction**: Emoji reactions to messages
- **MessageFile**: File attachments
- **File**: File uploads

### 7. **Support Models**
- **OTP**: One-time passwords for authentication
- **UserStatus**: Online/offline status
- **Draft**: Message drafts
- **TypingIndicator**: Real-time typing indicators

---

## Core Features Implemented

### 1. **Authentication System**
- Email/Password login
- OTP-based login/registration
- Google OAuth integration
- Password reset with OTP
- Social login support (Gmail, Google)

**Key Files**:
- `views.py`: login_view, register_view, verify_otp_view, forgot_password_view
- `models.py`: OTP model with verification logic
- Email backends: `brevo_mail_backend.py`, `zepto_mail_backend.py`

### 2. **User Profile Management**
- Profile creation with avatar upload
- Skill/interest management
- Social links (GitHub, LinkedIn, Portfolio, Behance)
- Profile completion status
- View other user profiles

**Key Views**:
- `student_details_view()`: Create initial profile
- `student_profile()`: View own profile
- `user_profile()`: View other users
- `edit_profile()`: Edit profile
- `UserProfileView`: REST API for profile

### 3. **Project Management**
- Create, edit, delete projects
- Project filtering by visibility, category, technology
- Project search and discovery
- Project detail view with comments
- Like/Unlike projects
- Advanced skill matching for collaborators

**Key Views**:
- `post_project()`: Create project
- `project_detail()`: View project with comments
- `like_project()`: Like/unlike
- `search_projects()`: Search and filter
- `find_collaborators()`: Skill-based search

### 4. **Collaboration Features**
- Find collaborators by skills
- Connection requests (pending/accepted/rejected)
- Team member management
- Project team invitations
- Role-based permissions (owner, admin, contributor, viewer)

**Key Views**:
- `find_collaborators()`: Search collaborators
- `connect_view()`: Send connection request
- `invite_to_team()`: Invite to project
- `accept_connection()`: Accept requests
- Connection status management

### 5. **Real-Time Messaging**
- Direct messages between users
- Group chat support
- Message reactions (emoji)
- Read receipts
- Typing indicators
- File sharing in messages
- Voice/Video call initiation

**Architecture**:
- Django Channels for WebSocket connections
- `consumers.py`: WebSocket handlers
- `routing.py`: WebSocket URL routing
- `chat_api.py`: REST endpoints
- Real-time updates via signals

**Key Views**:
- `message_view()`: Direct messages
- `enhanced_messages_view()`: Group chats
- `enhanced_chat_view()`: Group chat detail
- `ChatRoomListCreateView`: REST API

### 6. **Comment System (Live Feed)**
- Comments on projects
- Real-time comment updates
- Comment editing/deletion
- Comment count badges

**Key Files**:
- `comment_api.py`: add_comment, get_comments, edit_comment, delete_comment
- WebSocket integration for live updates
- Activity tracking for comments

### 7. **Notifications & Activity Feed**
- Notification system (connection requests, comments, likes)
- Mark notifications as read
- Activity feed showing user actions
- Real-time notification delivery

**Key Views**:
- `notifications_view()`: View all notifications
- `activity_feed()`: User activity feed
- `mark_notification_read()`: Mark as read

### 8. **Social Features**
- Follow/Unfollow users
- Activity feed
- User stats dashboard
- Connection network

**Key Functionality**:
- `follow_user()`: Follow/unfollow
- User relationship tracking
- Stats aggregation

### 9. **Search & Discovery**
- Project search by title, description, tech stack
- Collaborator search by skills
- College autocomplete
- Advanced filtering

**Key Files**:
- `utils.py`: ProjectVisibilityFilter, StudentProfileNLP
- `search_projects()`: Search implementation
- `college_search_api()`: College autocomplete

### 10. **Admin & Moderation**
- User statistics
- Activity monitoring
- Content management

---

## API Endpoints Overview

### Authentication Endpoints
```
POST   /login/
POST   /register/
GET    /logout/
POST   /forgot-password/
POST   /verify-otp/<purpose>/
POST   /resend-otp/<purpose>/
```

### Profile Endpoints
```
GET    /student-profile/
POST   /student-details/
PUT    /profile/
GET    /user/<username>/
GET    /user-profile/<user_id>/
```

### Project Endpoints
```
GET    /                              # Home/Project Feed
POST   /post-project/
GET    /project-detail/<id>/
PUT    /edit-project/<id>/
DELETE /delete-project/<id>/
POST   /like-project/<id>/
GET    /search-projects/
```

### Collaboration Endpoints
```
GET    /find-collaborators/
POST   /connect/<user_id>/
GET    /my-connections/
POST   /accept-connection/<id>/
POST   /reject-connection/<id>/
POST   /invite-to-team/<project_id>/
POST   /follow/<user_id>/
```

### Messaging Endpoints
```
GET    /messages/
GET    /chat/<user_id>/
POST   /enhanced-messages/
GET    /enhanced-chat/<room_id>/
POST   /create-group-chat/
```

### REST API Endpoints
```
GET    /chat-rooms/
POST   /messages/
GET    /messages/<id>/
POST   /conversations/
GET    /user-stats/
GET    /user-profile/<id>/
```

### Comment System
```
GET    /projects/<id>/comments/
POST   /projects/<id>/comments/add/
DELETE /comments/<id>/delete/
PUT    /comments/<id>/edit/
```

---

## Key Technical Features

### 1. **Real-Time Updates**
- WebSocket implementation via Django Channels
- Live message delivery
- Real-time comment updates
- Online/offline status
- Typing indicators
- Read receipts

**Implementation**:
- `consumers.py`: ChatConsumer, NotificationConsumer
- `routing.py`: WebSocket URL routing
- `signals_realtime.py`: Signal-based real-time triggers

### 2. **Email System**
- OTP delivery via email
- Notification emails
- Support for multiple backends (Brevo, ZeptoMail)
- HTML email templates

**Files**:
- `brevo_mail_backend.py`: Brevo SMTP backend
- `zepto_mail_backend.py`: ZeptoMail backend
- Email configuration in settings

### 3. **Performance Optimizations**
- Pagination for project lists (10 per page)
- Database query optimization (select_related, prefetch_related)
- Caching for user profiles and stats
- CSS/JS minification in production
- Database indexing on frequently queried fields

### 4. **Security**
- CSRF protection (csrf_exempt selectively)
- XSS protection
- SQL injection prevention (ORM)
- Password hashing (Django default)
- Permission-based access control
- Rate limiting ready (in comments API)

### 5. **Error Handling**
- Try-catch blocks in API endpoints
- User-friendly error messages
- Logging for debugging
- 404/403 error handling
- Form validation

### 6. **Frontend Integration**
- AJAX for seamless interactions
- Real-time WebSocket connection management
- Dynamic UI updates without page reload
- Loading indicators
- Error notifications

---

## Key JavaScript Files

### 1. **realtime-updates.js**
- WebSocket connection management
- Real-time comment delivery
- Live feed updates
- Connection status tracking

### 2. **messages-handlers.js**
- Message sending/receiving
- Read receipt handling
- Typing indicators
- File upload handling

### 3. **comments-handler.js**
- Comment creation, editing, deletion
- Real-time comment updates
- Badge count updates

### 4. **api-utils.js**
- API request utilities
- Token management
- Error handling

### 5. **profile.js**
- Profile picture upload
- Profile data management

---

## Template Structure

### Base Templates
- `base.html`: Basic layout
- `base_with_footer.html`: Layout with footer
- `main.html`: Main app layout

### Feature Templates
- `login.html`: Login page
- `register.html`: Registration page
- `verify_otp.html`: OTP verification
- `profile.html`: User profile view
- `main_home.html`: Dashboard/Feed
- `project_detail.html`: Project detail with comments
- `find_collaborators.html`: Collaborator search
- `messages.html`: Direct messaging
- `chat.html`: Chat interface
- `notifications.html`: Notifications page
- `activity_feed.html`: Activity feed
- `my_projects.html`: User's projects
- `edit_project.html`: Project editing
- `user_profile.html`: Other user's profile
- `post_project.html`: Create project form

---

## Recent Bug Fixes & Improvements

### Fixed Issues
1. **Login Error**: Fixed form validation and OTP handling
2. **Profile Picture**: Fixed upload and display
3. **Project Detail Loading**: Performance optimization
4. **Comments Visibility**: Fixed real-time comment updates
5. **Collaborators Not Showing**: Fixed filtering logic
6. **OAuth Redirect URI**: Fixed Google OAuth configuration
7. **CSRF Token Issues**: Fixed connect button and form submissions
8. **WebSocket Errors**: Fixed consumer routing
9. **Like Button**: Fixed state tracking
10. **Navbar/Footer**: Completed branding updates

### Recent Improvements
1. **Enhanced Chat UI**: Improved messaging interface
2. **Real-Time Comments**: Live comment updates on projects
3. **Advanced Skill Matching**: Better collaborator recommendations
4. **Branding Update**: UniSync → UniSinQ
5. **Performance**: Optimized queries and caching

---

## Development Setup

### Requirements
- Python 3.9+
- Django 4.x
- PostgreSQL (production) / SQLite (dev)
- Redis (optional, for caching)

### Installation
```bash
# Create virtual environment
python -m venv venv
source venv/Scripts/activate  # Windows

# Install dependencies
pip install -r requirements.txt

# Run migrations
python manage.py migrate

# Create superuser
python manage.py createsuperuser

# Run development server
python manage.py runserver

# Run Daphne (WebSocket server)
daphne -b 0.0.0.0 -p 8001 auth_project.asgi:application
```

### Environment Variables
```
DEBUG=True
SECRET_KEY=your_secret_key
DATABASE_URL=sqlite:///db.sqlite3
EMAIL_BACKEND=accounts.brevo_mail_backend.BrevoEmailBackend
BREVO_API_KEY=your_brevo_key
GOOGLE_OAUTH_CLIENT_ID=your_client_id
GOOGLE_OAUTH_CLIENT_SECRET=your_client_secret
```

---

## File Count & Complexity

### Python Files: ~60+
- models.py: 718 lines (13 models + backward compatibility aliases)
- views.py: 3467 lines (40+ view functions)
- urls.py: 129 lines (40+ URL patterns)
- serializers.py: 106 lines (5+ serializers)
- consumers.py: WebSocket handlers
- comment_api.py: Comment endpoints
- chat_api.py: Messaging API

### Templates: 40+
- Main layouts and feature pages
- Includes for reusable components
- Real-time update handling

### JavaScript: 10+ files
- Real-time WebSocket handling
- API utilities
- Frontend state management
- Message/Comment handlers

### CSS: Bootstrap + Custom styles
- Responsive design
- Component styling
- Branding colors (UniSinQ)

---

## Database Schema Summary

**Core Tables**:
- auth_user (Django built-in)
- accounts_studentprofile
- accounts_project
- accounts_connection
- accounts_message
- accounts_chatroom
- accounts_comment
- accounts_notification
- accounts_activity
- accounts_like
- accounts_follow

**Supporting Tables**:
- accounts_otp
- accounts_userstatus
- accounts_messagereadstatus
- accounts_file
- accounts_messagefile
- accounts_messagereaction
- accounts_projectmember
- accounts_projectinvitation
- accounts_projecttask
- accounts_projectmilestone
- accounts_userstats

---

## Testing & Quality

### Test Files
- test_login.py, test_email.py, test_profile_view.py
- test_comments_api.py, test_connections.py
- Various diagnostic scripts for debugging

### Debug Scripts
- debug_profiles.py, debug_filtering.py
- diagnose_login.py, diagnose_oauth_error.py
- Performance monitoring scripts

---

## Deployment Status

- **Backend**: Render/Railway ready
- **Database**: PostgreSQL configured
- **Static Files**: Configured for production
- **Email**: Integrated with Brevo/ZeptoMail
- **WebSockets**: Daphne configured

---

## Key Configurations

### Django Settings
- Authentication backends: Django auth + Google OAuth
- Installed apps: Django admin, auth, DRF, Channels, allauth
- Middleware: CSRF, Security, Session management
- Static files: WhiteNoise for production
- Database: PostgreSQL with connection pooling

### WebSocket Configuration
- Channels integration
- Redis channel layer (optional)
- Consumer message routing
- Room-based broadcasting

---

## Summary

This is a **comprehensive Django-based collaborative platform** with:
- Full user authentication (email, OTP, OAuth)
- Real-time messaging and notifications via WebSockets
- Project discovery and collaboration matching
- Team management and invitations
- Comments and likes system
- Activity tracking and feeds
- 3000+ lines of core view logic
- 40+ API endpoints
- 40+ HTML templates
- Production-ready deployment configuration

The codebase shows significant development effort with bug fixes, performance optimizations, and feature enhancements across multiple iterations.
