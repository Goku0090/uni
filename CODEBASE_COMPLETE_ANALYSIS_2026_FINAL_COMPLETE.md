# UniSync/UniSinQ - Complete Codebase Analysis 2026

**Project:** Full-Stack Python/Django Collaboration Platform  
**Repository:** https://github.com/Goku0090/uni  
**Stack:** Django + Django Channels + REST Framework + PostgreSQL  
**Real-time:** WebSocket via Django Channels  

---

## Executive Summary

This is a **comprehensive social collaboration platform** built with Django, enabling students and professionals to discover projects, connect with collaborators, and communicate in real-time. It combines traditional Django MVC patterns with modern WebSocket-based real-time updates and a rich REST API.

### Key Features
- **User Authentication**: Email/OTP login, Google/GitHub OAuth
- **Project Management**: Create, edit, share projects with team collaboration
- **Messaging**: Direct messages, group chats with read status tracking
- **Real-time Updates**: WebSocket notifications, activity feeds, project status
- **Collaboration**: Connection requests, team invitations, skill matching
- **Social Features**: Like projects, follow users, comments, activity tracking
- **Profile System**: Extended student profiles with skills, interests, portfolio links

---

## 1. Architecture Overview

### 1.1 Technology Stack

| Component | Technology |
|-----------|-----------|
| **Backend Framework** | Django 4.x |
| **Real-time** | Django Channels + AsyncIO |
| **REST API** | Django REST Framework |
| **Database** | PostgreSQL (production) / SQLite (dev) |
| **Frontend** | HTML5 + CSS3 + Vanilla JavaScript |
| **Email** | Brevo/ZeptoMail with OAuth |
| **Authentication** | Django-allauth (OAuth2) + Custom OTP |
| **Hosting** | Render (with PostgreSQL) |

### 1.2 Project Structure

```
auth_project/
├── auth_project/              # Project configuration
│   ├── settings.py           # Django settings (DB, middleware, installed apps)
│   ├── urls.py               # Main URL routing
│   ├── wsgi.py               # WSGI application
│   ├── asgi.py               # ASGI for WebSocket (Channels)
│
├── accounts/                 # Main app
│   ├── models.py            # 15+ data models
│   ├── views.py             # 50+ view functions
│   ├── urls.py              # Route definitions
│   ├── forms.py             # Django forms with validation
│   ├── serializers.py       # REST API serializers
│   ├── consumers.py         # WebSocket consumers
│   ├── routing.py           # WebSocket URL patterns
│   ├── permissions.py       # Custom DRF permissions
│   ├── signals_realtime.py  # Django signals for real-time
│   ├── chat_api.py          # Chat/messaging REST endpoints
│   ├── comment_api.py       # Comments API
│   ├── utils.py             # Utilities (NLP, filtering)
│   ├── services/            # Business logic
│   ├── static/              # CSS, JS, images
│   │   ├── js/
│   │   │   ├── realtime-updates.js   # WebSocket client
│   │   │   ├── api-utils.js          # API helpers
│   │   │   └── login.js              # Auth JS
│   │   └── css/
│   └── templates/           # HTML templates
│
├── static/                  # Global static files
├── media/                   # User uploads (profiles, files)
├── manage.py               # Django CLI
└── requirements.txt        # Python dependencies
```

---

## 2. Data Models (15+ Models)

### 2.1 User & Authentication

#### **StudentProfile** (Extended User)
```python
class StudentProfile(models.Model):
    user                  # OneToOne with Django User
    full_name            # Display name
    college              # Educational institution
    location            # Geographic location
    bio                 # User biography
    profile_photo       # Avatar image
    skills              # JSONField array
    project_interests   # JSONField array
    interests           # JSONField array
    role_preference     # Desired role (e.g., "Developer", "Designer")
    github, linkedin, portfolio, behance  # Social links
    profile_completed   # Completion flag
    created_at, updated_at
```

#### **OTP** (One-Time Password)
```python
class OTP(models.Model):
    email               # Target email
    otp_code           # 6-digit code
    purpose            # login/registration/reset
    is_used            # Expiration flag
    created_at, expires_at  # Timestamps
```

### 2.2 Relationships & Networking

#### **Connection** (User Connections)
```python
class Connection(models.Model):
    sender              # User initiating connection
    receiver            # Target user
    status              # pending/accepted/rejected
    created_at, updated_at
    
    # Unique constraint: one connection per sender-receiver pair
```

#### **Follow**
```python
class Follow(models.Model):
    follower            # Following user
    following           # Followed user
    created_at
```

### 2.3 Messaging & Chat

#### **Message**
```python
class Message(models.Model):
    sender              # User sending
    receiver            # Direct recipient (nullable for group chat)
    chat_room           # Group chat reference
    content             # Message text
    message_type        # text/file/image/call
    reply_to            # Threading support
    created_at, updated_at
    
    # Methods:
    mark_as_read_by(user)
    is_read_by(user)
    get_read_count()
```

#### **ChatRoom** (Group Chats)
```python
class ChatRoom(models.Model):
    name                # Room name
    chat_type           # direct/group/project
    project             # Associated project
    created_by          # Creator user
    is_active           # Status flag
    created_at
    
    # Relationship:
    - ChatRoomMember (many)
    - Message (many)
```

#### **ChatRoomMember**
```python
class ChatRoomMember(models.Model):
    chat_room           # Room reference
    user                # Member user
    role                # owner/admin/member
    is_active          # Status
    joined_at
```

#### **MessageReadStatus**
```python
class MessageReadStatus(models.Model):
    message             # Message reference
    user                # Reader
    read_at             # Read timestamp
    
    # Unique: one read status per message-user pair
```

#### **MessageReaction**
```python
class MessageReaction(models.Model):
    message             # Reacted message
    user                # Reacting user
    reaction            # emoji or text
    created_at
```

### 2.4 Projects & Collaboration

#### **Project**
```python
class Project(models.Model):
    title               # Project name
    description         # Detailed description
    owner               # ForeignKey User
    status              # idea/in-progress/completed/on-hold
    visibility          # public/private/invited-only
    collaboration_needs # Text field for required skills
    github_link         # Repository URL
    live_link           # Live demo URL
    category            # Project domain
    tags                # JSONField array
    is_active           # Soft delete flag
    created_at, updated_at
```

#### **ProjectTeam**
```python
class ProjectTeam(models.Model):
    project             # Project reference
    name                # Team name
    description         # Team purpose
    created_at
```

#### **ProjectTeamMember**
```python
class ProjectTeamMember(models.Model):
    team                # Team reference
    user                # Member user
    role                # developer/designer/manager/etc
    joined_at
```

#### **ProjectTeamInvitation**
```python
class ProjectTeamInvitation(models.Model):
    team                # Team reference
    user                # Invitee
    status              # pending/accepted/declined
    invited_by          # Inviter
    created_at, responded_at
```

#### **ProjectTask & ProjectMilestone**
```python
class ProjectTask(models.Model):
    project, team       # References
    title, description  # Content
    assigned_to         # User
    status              # todo/in-progress/done
    priority            # low/medium/high
    due_date            # Target date
    created_at, updated_at

class ProjectMilestone(models.Model):
    project             # Project reference
    title               # Milestone name
    target_date         # Deadline
    completed_date      # Actual completion
    status              # pending/completed
```

### 2.5 Activity & Engagement

#### **Activity**
```python
class Activity(models.Model):
    user                # Actor
    activity_type       # post/like/comment/follow/etc
    target_user         # Subject (optional)
    project             # Related project
    description         # Activity detail
    timestamp           # When it happened
```

#### **Like**
```python
class Like(models.Model):
    user                # Liker
    project             # Liked project
    created_at
    
    # Unique: one like per user-project pair
```

#### **Comment**
```python
class Comment(models.Model):
    author              # Commenter
    project             # Target project
    content             # Comment text
    created_at, updated_at
```

#### **Notification**
```python
class Notification(models.Model):
    user                # Recipient
    notification_type   # connection_request/message/project_like/etc
    sender              # Originator
    message             # Description
    is_read             # Read status
    created_at
```

### 2.6 Files & Storage

#### **File**
```python
class File(models.Model):
    user                # Uploader
    file                # FileField
    filename            # Display name
    file_size           # Bytes
    file_type           # MIME type
    uploaded_at
```

#### **MessageFile**
```python
class MessageFile(models.Model):
    message             # Message reference
    file                # File reference
    uploaded_at
    
    # Unique: one file per message
```

---

## 3. API Endpoints (REST Framework)

### 3.1 Chat & Messaging APIs

**Base Path:** `/api/`

#### Chat Room Management
```
GET     /chat-rooms/                      # List all rooms
POST    /chat-rooms/                      # Create new room
GET     /chat-rooms/<id>/                 # Get room details
PUT     /chat-rooms/<id>/                 # Update room
DELETE  /chat-rooms/<id>/                 # Delete room
GET     /chat-rooms/<id>/members/         # Get room members
POST    /direct-message/                  # Start direct chat
```

#### Messages
```
GET     /messages/                        # List messages
POST    /messages/                        # Send message
GET     /messages/<pk>/                   # Get message
PUT     /messages/<pk>/                   # Update message
DELETE  /messages/<pk>/                   # Delete message
GET     /messages/search/                 # Search messages
GET     /messages/<id>/status/            # Get read status
POST    /messages/<id>/reactions/         # Add reaction
```

#### Drafts & Typing
```
GET     /drafts/                          # List draft messages
POST    /drafts/                          # Save draft
POST    /typing/                          # Send typing indicator
```

#### Conversations
```
GET     /conversations/                   # List conversations
```

### 3.2 Comments API

```
GET     /projects/<id>/comments/          # List comments
POST    /projects/<id>/comments/          # Post comment
PUT     /comments/<id>/                   # Edit comment
DELETE  /comments/<id>/                   # Delete comment
```

### 3.3 User Profile API

```
GET     /profile/                         # Get logged-in user profile
PUT     /profile/                         # Update profile
GET     /users/<username>/                # Get public user profile
```

---

## 4. WebSocket Implementation

### 4.1 Routing Configuration

**File:** `accounts/routing.py`

```python
websocket_urlpatterns = [
    re_path(r'ws/project/(?P<project_id>\w+)/$', ProjectUpdateConsumer.as_asgi()),
    re_path(r'ws/activity-feed/$', ActivityFeedConsumer.as_asgi()),
    re_path(r'ws/notifications/$', NotificationConsumer.as_asgi()),
]
```

### 4.2 Consumer Classes

#### **ProjectUpdateConsumer**
```python
class ProjectUpdateConsumer(AsyncWebsocketConsumer):
    # Event types:
    - project.initial_data          # Send initial project state
    - project.status_update         # Status changed
    - project.member_added          # Team member joined
    - project.comment_posted        # New comment
    - project.task_updated          # Task status change
    
    # Incoming messages:
    - status.update                 # Change project status
    - member.add                    # Add team member
    - comment.post                  # Post comment
    - task.update                   # Update task
```

#### **ActivityFeedConsumer**
Broadcasts activity events to all connected users:
- New projects posted
- Projects liked
- Comments made
- Users followed

#### **NotificationConsumer**
Delivers real-time notifications:
- Connection requests
- Message arrivals
- Project updates
- Team invitations

### 4.3 Client-Side WebSocket

**File:** `static/js/realtime-updates.js`

```javascript
class RealtimeUpdates {
    init()                              // Initialize all sockets
    connectToProjectUpdates(projectId)  // Project socket
    connectToActivityFeed()              // Activity socket
    connectToNotifications()             // Notification socket
    handleProjectMessage(data)           // Process project updates
    sendStatusUpdate(newStatus)          // Send status change
    attemptReconnect(callback)           // Auto-reconnect logic
}
```

**Usage:**
```javascript
const realtime = new RealtimeUpdates();
realtime.init();

// Example: Monitor project updates
const wsUrl = `ws://${window.location.host}/ws/project/2/`;
socket = new WebSocket(wsUrl);
socket.onopen = () => console.log("✅ WORKING!");
socket.onmessage = (event) => {
    const data = JSON.parse(event.data);
    // Handle live update
};
```

---

## 5. Authentication Flow

### 5.1 Email/OTP Login

```
1. User enters email on login page
2. System generates 6-digit OTP
3. OTP sent via Brevo/ZeptoMail
4. User verifies OTP in login_view()
5. Session created & user redirected to dashboard
```

**Key Functions:**
- `OTP.generate_otp(email, purpose)` - Generate code
- `verify_otp_view(request, purpose)` - Verify code
- `OTP.verify_otp(code)` - Validation logic

### 5.2 Social OAuth (Google, GitHub)

```
1. User clicks "Login with Google/GitHub"
2. Redirected to OAuth provider
3. Provider authenticates user
4. Callback to django-allauth
5. StudentProfile auto-created
6. User logged in & redirected
```

**Configuration:**
- Django-allauth handles OAuth2 flow
- Social providers configured in settings
- Custom signup form: `CustomSocialSignupForm`
- Post-signup signal creates StudentProfile

### 5.3 Registration

```
1. User fills RegisterForm
2. Email validation
3. Password requirements checked
4. OTP sent for email verification
5. User account created with StudentProfile
```

---

## 6. View Functions & Pages

### 6.1 Authentication Views

| Function | Route | Purpose |
|----------|-------|---------|
| `register_view()` | `/register/` | User registration |
| `login_view()` | `/login/` | Email/OTP login |
| `verify_otp_view()` | `/verify-otp/<purpose>/` | OTP verification |
| `logout_view()` | `/logout/` | Session logout |
| `forgot_password_view()` | `/forgot-password/` | Password reset |
| `reset_password_view()` | `/reset-password/` | Confirm reset |

### 6.2 Project Management Views

| Function | Route | Purpose |
|----------|-------|---------|
| `post_project()` | `/post-project/` | Create new project |
| `project_detail()` | `/project/<id>/` | View project details |
| `edit_project()` | `/edit-project/<id>/` | Edit project info |
| `delete_project()` | `/delete-project/<id>/` | Delete project |
| `like_project()` | `/like-project/<id>/` | Like/unlike project |
| `explore_projects_view()` | `/explore-projects/` | Browse all projects |
| `my_projects_view()` | `/my-projects/` | User's projects |

### 6.3 Social & Collaboration Views

| Function | Route | Purpose |
|----------|-------|---------|
| `find_collaborators()` | `/find-collaborators/` | Search for team members |
| `user_profile()` | `/user/<username>/` | View user profile |
| `student_profile()` | `/student-profile/` | Edit own profile |
| `send_connection_request()` | `/connect/<user_id>/` | Send connection |
| `accept_connection()` | `/accept-connection/<id>/` | Accept connection |
| `reject_connection()` | `/reject-connection/<id>/` | Reject connection |
| `my_connections()` | `/my-connections/` | List connections |
| `follow_user()` | `/follow/<user_id>/` | Follow user |
| `activity_feed()` | `/activity-feed/` | View activities |

### 6.4 Messaging Views

| Function | Route | Purpose |
|----------|-------|---------|
| `message_view()` | `/messages/` | Direct messages list |
| `chat_view()` | `/chat/<user_id>/` | Direct message thread |
| `enhanced_messages_view()` | `/enhanced-messages/` | Modern chat interface |
| `enhanced_chat_view()` | `/enhanced-chat/<room_id>/` | Group chat interface |
| `create_group_chat()` | `/create-group-chat/` | New group |

### 6.5 Notification Views

| Function | Route | Purpose |
|----------|-------|---------|
| `notifications_view()` | `/notifications/` | All notifications |
| `mark_notification_read()` | `/notification/<id>/read/` | Mark as read |

---

## 7. Key Services & Utilities

### 7.1 StudentProfileNLP

**File:** `utils.py`

Performs NLP analysis on:
- Profile bio → Extract interests & skills
- Project description → Match with collaborators
- Find similar users based on interests
- Recommend connections

```python
class StudentProfileNLP:
    def analyze_bio(user_bio) -> dict          # Extract interests
    def extract_skills(text) -> list           # Identify skills
    def find_similar_users(user) -> queryset   # Get similar profiles
    def calculate_match_score(user1, user2) -> float
```

### 7.2 ProjectVisibilityFilter

Implements permission-based project visibility:
- **Public** - Visible to all authenticated users
- **Private** - Only owner sees
- **Invited-only** - Only team members see

```python
class ProjectVisibilityFilter:
    def get_visible_projects(user) -> queryset  # User's accessible projects
    def can_view_project(user, project) -> bool # Permission check
```

### 7.3 Email Services

#### Brevo Backend
```python
class BrevoMailBackend:
    - Sends OTP emails
    - Handles template rendering
    - Tracks deliverability
```

#### ZeptoMail Backend
```python
class ZeptoMailBackend:
    - Alternative email provider
    - OAuth-based authentication
    - Used for production
```

### 7.4 Custom Signals

**File:** `signals_realtime.py`

Django signals for real-time updates:
```python
@receiver(post_save, sender=Project)
def project_created_signal()              # Broadcast project.created

@receiver(post_save, sender=Like)
def like_created_signal()                 # Broadcast like event

@receiver(post_save, sender=Comment)
def comment_created_signal()              # Broadcast comment event

@receiver(post_save, sender=Connection)
def connection_request_signal()           # Send notification
```

---

## 8. Forms & Validation

### 8.1 Authentication Forms

```python
class RegisterForm(forms.Form)
    email               # Email field + validation
    username           # Username + uniqueness check
    password1, password2  # Password + match verification

class LoginForm(forms.Form)
    email              # Email field
    password           # Password field (optional for OTP)

class OTPVerificationForm(forms.Form)
    otp_code           # 6-digit field
```

### 8.2 Profile Forms

```python
class StudentProfileForm(forms.ModelForm)
    full_name          # CharField
    college           # CharField
    location          # CharField
    bio               # Textarea
    profile_photo     # ImageField
    skills            # JSONField
    interests         # JSONField
    role_preference   # ChoiceField
    github, linkedin, portfolio  # URLFields

class ProjectForm(forms.ModelForm)
    title             # CharField
    description       # Textarea
    collaboration_needs  # CharField
    status            # ChoiceField
    visibility        # ChoiceField
    category          # CharField
    tags              # CharField (comma-separated)
    github_link, live_link  # URLFields
```

### 8.3 Comment Form

```python
class CommentForm(forms.ModelForm)
    content           # Textarea
```

---

## 9. Serializers (REST API)

### 9.1 User & Profile

```python
class UserProfileSerializer(serializers.ModelSerializer)
    user              # Nested user data
    full_name, college, bio  # Profile fields
    profile_photo     # Image URL
    skills, interests  # JSONField arrays
    github, linkedin   # Social URLs

class UserSerializer(serializers.ModelSerializer)
    id, username, email  # User fields
```

### 9.2 Project & Collaboration

```python
class ProjectSerializer(serializers.ModelSerializer)
    owner             # Nested owner info
    title, description, status  # Content
    visibility, category, tags  # Metadata
    created_at, updated_at  # Timestamps

class ConnectionSerializer(serializers.ModelSerializer)
    sender, receiver  # User relationships
    status            # Connection status
```

### 9.3 Messaging

```python
class MessageSerializer(serializers.ModelSerializer)
    sender, receiver  # User references
    content, message_type  # Message data
    is_read_by(user)  # Read status check
    created_at, updated_at

class ChatRoomSerializer(serializers.ModelSerializer)
    name, chat_type   # Room info
    members           # Nested members
    message_count     # Count of messages
```

### 9.4 Notifications

```python
class NotificationSerializer(serializers.ModelSerializer)
    user, sender      # Recipient and source
    notification_type # Event type
    message           # Description
    is_read, created_at
```

---

## 10. Middleware & Security

### 10.1 Middleware Stack

```python
MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',          # CSRF protection
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'allauth.account.middleware.AccountMiddleware',       # Social auth
]
```

### 10.2 Custom Permissions

**File:** `permissions.py`

```python
class IsOwner(BasePermission)              # Object ownership check
class IsProjectOwner(BasePermission)       # Project ownership
class IsTeamMember(BasePermission)         # Team membership
class IsChatRoomMember(BasePermission)    # Chat room access

# Decorators:
@check_project_owner                       # View-level check
@check_chat_room_member                    # Chat access
@check_team_owner                          # Team leadership
```

### 10.3 Security Settings

```python
DEBUG = False                              # Production
SECURE_SSL_REDIRECT = True                # Force HTTPS
SESSION_COOKIE_SECURE = True              # HTTPS-only cookies
CSRF_COOKIE_SECURE = True                 # CSRF token security
SECURE_BROWSER_XSS_FILTER = True          # XSS protection
```

---

## 11. Database Configuration

### 11.1 Production (Render)

```python
DATABASE_URL = os.getenv('DATABASE_URL')  # Render PostgreSQL
# Automatically parsed with dj_database_url
```

### 11.2 Development (Local)

```python
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'unisinq_db',
        'USER': 'unisinq_user',
        'PASSWORD': os.getenv('DB_PASSWORD'),
        'HOST': 'localhost',
        'PORT': '5432',
    }
}

# Fallback to SQLite:
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}
```

### 11.3 Channel Layers (WebSocket)

```python
CHANNEL_LAYERS = {
    'default': {
        'BACKEND': 'channels.layers.InMemoryChannelLayer'
    }
}
# In production, use Redis or other persistent backend
```

---

## 12. Frontend Architecture

### 12.1 Static Files Structure

```
static/
├── js/
│   ├── realtime-updates.js       # WebSocket client class
│   ├── api-utils.js              # API helper functions
│   ├── login.js                  # Authentication logic
│   └── messages-handlers.js      # Chat event handlers
├── css/
│   ├── base.css                  # Global styles
│   ├── dashboard.css             # Dashboard styling
│   └── chat.css                  # Chat UI styling
└── images/
    ├── logo.svg
    └── branding/
```

### 12.2 Template Hierarchy

```
templates/
├── base.html                     # Base layout
├── accounts/
│   ├── login.html               # Login page
│   ├── register.html            # Registration
│   ├── dashboard.html           # Dashboard
│   ├── student_profile.html     # Profile edit
│   ├── find_collaborators.html  # Collaborator search
│   ├── project_detail.html      # Project view
│   ├── post_project.html        # Project creation
│   ├── messages.html            # Direct messages
│   ├── enhanced_messages.html   # Modern chat
│   └── notifications.html       # Notification center
```

### 12.3 Key JavaScript Modules

#### realtime-updates.js
- Manages 3 WebSocket connections (projects, activity, notifications)
- Handles auto-reconnection with exponential backoff
- Updates DOM with real-time data
- Shows toast notifications

#### api-utils.js
- Wrapper functions for REST API calls
- CSRF token handling
- Error handling & user feedback
- Request/response formatting

---

## 13. Key Features Implementation

### 13.1 Real-time Project Status Updates

```python
# Backend (views.py):
def update_project_status(request, project_id):
    project = Project.objects.get(id=project_id)
    project.status = request.POST['new_status']
    project.save()
    
    # Signal triggers WebSocket broadcast
    # → ProjectUpdateConsumer sends to all connected clients

# Frontend (realtime-updates.js):
socket.onmessage = (event) => {
    data = JSON.parse(event.data);
    if (data.type === 'project.status_update') {
        updateProjectUI(data.status);  // Real-time DOM update
    }
}
```

### 13.2 Live Activity Feed

```python
# Broadcasting to all users:
class ActivityFeedConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        await self.channel_layer.group_add('activity_feed', self.channel_name)
    
    async def activity_event(self, event):
        # Broadcast to all connected clients
        await self.send(json.dumps(event))
```

### 13.3 Direct Messaging with Read Status

```python
# Message read status tracking:
message = Message.objects.get(id=1)
message.mark_as_read_by(user)           # Mark as read
is_read = message.is_read_by(user)      # Check status
read_count = message.get_read_count()   # Count of readers

# API response:
{
    'id': 1,
    'content': 'Hello!',
    'read_by_count': 2,
    'unread_users': [...]
}
```

### 13.4 Team Invitations & Acceptance

```python
# Create invitation:
invite = ProjectTeamInvitation.objects.create(
    team=project.team,
    user=target_user,
    invited_by=request.user
)  # Notification sent automatically via signal

# Accept invitation:
invite.status = 'accepted'
ProjectTeamMember.objects.create(team=invite.team, user=invite.user)
```

### 13.5 Skill-Based Matching

```python
# NLP-based matching:
similar_users = StudentProfileNLP.find_similar_users(request.user)

# Algorithm:
1. Extract interests from user bio
2. Calculate similarity score with other users
3. Filter by shared skills
4. Sort by match percentage
5. Return top 10 matches
```

---

## 14. Deployment Configuration

### 14.1 Render Configuration

**File:** `render.yaml`

```yaml
services:
  - type: web
    name: unisinq-web
    env: python
    buildCommand: pip install -r requirements.txt && python manage.py migrate
    startCommand: daphne -b 0.0.0.0 -p 10000 auth_project.asgi:application
    
  - type: postgresql
    name: unisinq-db
    version: 15
```

### 14.2 Environment Variables

```
DEBUG=False
SECRET_KEY=your-secret-key
ALLOWED_HOSTS=your-domain.com
DATABASE_URL=postgresql://...
EMAIL_BACKEND=accounts.brevo_mail_backend.BrevoEmailBackend
BREVO_API_KEY=...
SOCIAL_AUTH_GOOGLE_OAUTH2_KEY=...
SOCIAL_AUTH_GOOGLE_OAUTH2_SECRET=...
```

### 14.3 ASGI Configuration (WebSocket)

```python
# auth_project/asgi.py
import os
from django.core.asgi import get_asgi_application
from channels.routing import ProtocolTypeRouter, URLRouter
from channels.auth import AuthMiddlewareStack
from accounts.routing import websocket_urlpatterns

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'auth_project.settings')

application = ProtocolTypeRouter({
    'http': get_asgi_application(),
    'websocket': AuthMiddlewareStack(
        URLRouter(websocket_urlpatterns)
    )
})
```

---

## 15. Common Issues & Solutions

### 15.1 WebSocket Connection Failures

**Problem:** `WebSocket is closed` error  
**Solution:**
- Check ASGI server running (Daphne)
- Verify WebSocket URL matches routing patterns
- Ensure user is authenticated (AuthMiddleware)
- Check browser console for CORS issues

### 15.2 CSRF Token Errors

**Problem:** `403 CSRF token missing`  
**Solution:**
- Include `{% csrf_token %}` in all forms
- Send `X-CSRFToken` header in AJAX requests
- Use `api-utils.js` helper functions

### 15.3 Email Not Sending

**Problem:** OTP emails not received  
**Solution:**
- Verify Brevo/ZeptoMail API key in settings
- Check email configuration in admin
- Test with `python manage.py shell`
- Monitor logs for delivery errors

### 15.4 Database Connection Issues

**Problem:** `Could not connect to database`  
**Solution:**
- For PostgreSQL: `psql -U user -d database` to test
- Check DATABASE_URL format
- Verify firewall/network access
- Ensure migrations run: `python manage.py migrate`

### 15.5 Real-time Updates Not Working

**Problem:** WebSocket messages not received  
**Solution:**
- Verify ChannelLayers config (may need Redis for production)
- Check `consumers.py` for async/await issues
- Monitor server logs for connection errors
- Test with browser DevTools Network tab

---

## 16. Performance Optimizations

### 16.1 Database Queries

```python
# Use select_related for ForeignKeys:
projects = Project.objects.select_related('owner').all()

# Use prefetch_related for reverse relations:
users = User.objects.prefetch_related('connections').all()

# Add database indexes on frequently queried fields:
class Project(models.Model):
    title = models.CharField(max_length=200, db_index=True)
    owner = models.ForeignKey(User, db_index=True, ...)
```

### 16.2 Caching

```python
# Cache user profile:
cache.set(f'profile_{user_id}', profile, 3600)  # 1 hour
cached = cache.get(f'profile_{user_id}')

# Cache queryset:
@cache_page(60 * 5)  # 5 minute cache
def explore_projects_view(request):
    projects = Project.objects.all()
```

### 16.3 Pagination

```python
# All project lists use pagination:
paginator = Paginator(projects, 10)  # 10 items per page
page_obj = paginator.get_page(request.GET.get('page'))
```

---

## 17. Testing Strategy

### 17.1 Unit Tests

```python
# Test models:
def test_otp_generation():
    otp = OTP.generate_otp('test@example.com', 'login')
    assert otp.is_valid()
    assert not otp.is_used

def test_connection_creation():
    sender = User.objects.create(username='alice')
    receiver = User.objects.create(username='bob')
    conn = Connection.objects.create(sender=sender, receiver=receiver)
    assert conn.status == 'pending'
```

### 17.2 Integration Tests

```python
# Test API endpoints:
def test_login_otp_flow():
    response = client.post('/login/', {'email': 'test@example.com'})
    assert response.status_code == 200
    
    otp = OTP.objects.latest('created_at')
    response = client.post('/verify-otp/login/', {'otp_code': otp.otp_code})
    assert response.status_code == 302  # Redirect to dashboard
```

### 17.3 WebSocket Tests

```python
# Test WebSocket connection:
async def test_project_websocket():
    communicator = WebsocketCommunicator(
        ProjectUpdateConsumer.as_asgi(),
        "ws/project/1/"
    )
    connected, _ = await communicator.connect()
    assert connected
    
    data = await communicator.receive_json_from()
    assert data['type'] == 'project.initial_data'
```

---

## 18. File Structure Summary

```
e:/login/
├── auth_project/                    # Django project root
│   ├── accounts/                    # Main application
│   │   ├── models.py               # 15+ data models
│   │   ├── views.py                # 50+ view functions (3400+ lines)
│   │   ├── urls.py                 # URL routing
│   │   ├── forms.py                # Django forms
│   │   ├── serializers.py          # REST serializers
│   │   ├── consumers.py            # WebSocket consumers
│   │   ├── routing.py              # WebSocket routing
│   │   ├── permissions.py          # Custom DRF permissions
│   │   ├── signals_realtime.py     # Django signals
│   │   ├── chat_api.py             # Chat REST endpoints
│   │   ├── comment_api.py          # Comment endpoints
│   │   ├── utils.py                # Utilities (NLP, filtering)
│   │   ├── services/               # Business logic modules
│   │   ├── static/                 # CSS, JS, images
│   │   │   ├── js/
│   │   │   │   ├── realtime-updates.js
│   │   │   │   ├── api-utils.js
│   │   │   │   └── login.js
│   │   │   └── css/
│   │   └── templates/              # HTML templates
│   │
│   ├── auth_project/               # Project configuration
│   │   ├── settings.py             # Django settings
│   │   ├── urls.py                 # Main URL routing
│   │   ├── wsgi.py                 # WSGI application
│   │   └── asgi.py                 # ASGI for WebSocket
│   │
│   ├── static/                     # Global static files
│   ├── media/                      # User uploads
│   ├── logs/                       # Application logs
│   ├── manage.py                   # Django CLI
│   ├── requirements.txt            # Python dependencies
│   └── db.sqlite3                  # Development database
│
├── venv/                           # Virtual environment
├── .git/                           # Git repository
└── [500+ documentation files]      # Analysis & guides
```

---

## 19. Dependency Summary

### Core Dependencies
```
Django==4.2.x
djangorestframework==3.14.x
django-allauth==0.54.x
django-channels==4.x
daphne==4.x
```

### Database & Cache
```
psycopg2==2.9.x
dj-database-url==1.2.x
```

### Email
```
brevo==3.x
```

### Utilities
```
python-dotenv==0.x
Pillow==9.x (Image processing)
numpy, scipy (NLP analysis)
```

---

## 20. Future Enhancement Opportunities

1. **Caching Layer**: Implement Redis for session/cache management
2. **Search**: Elasticsearch integration for project/user search
3. **Analytics**: Track user engagement, project popularity
4. **Video Calls**: WebRTC integration for team meetings
5. **AI Matching**: ML-based collaborator recommendations
6. **Mobile App**: React Native or Flutter client
7. **Notifications**: Push notifications to mobile devices
8. **Monetization**: Premium features, team plans
9. **Moderation**: Admin tools for content/user management
10. **API Documentation**: Swagger/OpenAPI specs

---

## Conclusion

This is a **production-ready, full-featured collaboration platform** with:
- ✅ Complete user authentication system
- ✅ Real-time WebSocket communication
- ✅ Comprehensive REST API
- ✅ Advanced permission system
- ✅ Scalable database design
- ✅ Modern frontend with real-time updates
- ✅ Ready for deployment on Render

The codebase is well-structured, documented, and follows Django best practices throughout.

---

**Generated:** 2026-02-09  
**Project:** UniSync/UniSinQ  
**Status:** Analysis Complete ✅
