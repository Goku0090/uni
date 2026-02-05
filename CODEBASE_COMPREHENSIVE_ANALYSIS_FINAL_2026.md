# UniSync - Comprehensive Codebase Analysis 2026

## Overview
UniSync is a Django-based student collaboration platform that connects students for project collaboration, networking, and messaging. The application includes OTP-based authentication, social login (Google/GitHub), real-time messaging with group chat support, and project management capabilities.

---

## Architecture Overview

### Technology Stack
- **Backend**: Django 3.x/4.x
- **API Framework**: Django REST Framework
- **Database**: PostgreSQL (Render deployment) / SQLite (development)
- **Authentication**: Django Allauth (Social OAuth) + Custom OTP system
- **Email**: Brevo/Zeptomail + SMTP fallback
- **Frontend**: Django templates with HTML/CSS
- **Deployment**: Render.com or Railway

### Key Dependencies
- `djangorestframework` - REST API endpoints
- `django-allauth` - Social authentication (Google, GitHub)
- `Pillow` - Image processing
- `psycopg2` - PostgreSQL adapter
- `python-dotenv` - Environment configuration

---

## Database Models

### Core Authentication & User Management

#### **StudentProfile** (L12-53, models.py)
Extended user profile storing student-specific data.

**Fields:**
- `user` - OneToOneField (User) - FK to Django User
- `full_name` - CharField(100)
- `college` - CharField(200) - Student's institution
- `other_college` - CharField(200) - If not in dropdown
- `location` - CharField(100)
- `interests` - JSONField (array) - Tags/interests
- `bio` - TextField - About me section
- `profile_photo` - ImageField - Avatar image
- `skills` - JSONField (array) - Technical skills
- `project_interests` - JSONField (array) - Types of projects interested in
- `role_preference` - CharField(50) - Developer/Designer/PM/etc
- `github`, `linkedin`, `portfolio`, `behance` - URLFields - Social links
- `profile_completed` - BooleanField - Completion status
- `created_at`, `updated_at` - DateTimeFields

**Methods:**
- `get_display_name()` - Returns full_name or username fallback

---

#### **OTP** (L55-124, models.py)
One-Time Password for secure authentication flow.

**Fields:**
- `email` - EmailField - Associated email
- `otp_code` - CharField(6) - 6-digit code
- `purpose` - CharField(20) - Choice: login/registration/reset
- `is_used` - BooleanField - Validity flag
- `created_at`, `expires_at` - DateTimeFields

**Methods:**
- `is_valid()` - Checks if not used and not expired
- `verify_otp(otp_code)` - Validates OTP code
- `generate_otp(email, purpose)` - Creates new OTP (5-min TTL)
- `hash_otp(otp_code)` - SHA-256 hashing utility

---

#### **Connection** (L126-147, models.py)
Network/friendship connections between users.

**Fields:**
- `user1`, `user2` - ForeignKey (User) - Both sides of connection
- `status` - CharField - Choice: pending/accepted/rejected
- `initiated_by` - ForeignKey (User) - Who started the request
- `created_at`, `updated_at` - DateTimeFields

**Methods:**
- `__str__()` - Returns connection status between users

---

### Messaging Models

#### **ChatRoom** (L149-200, models.py)
Container for group chats or direct messaging channels.

**Fields:**
- `name` - CharField(100) - Room name (optional for DMs)
- `is_private` - BooleanField - Private=DM, False=Group
- `is_group` - BooleanField - Indicates group chat
- `members` - ManyToManyField (User) - Room participants
- `created_by` - ForeignKey (User) - Creator/admin
- `created_at`, `updated_at` - DateTimeFields
- `description` - TextField (optional) - For groups
- `avatar` - ImageField (optional) - Group icon

---

#### **Message** (L202-260, models.py)
Individual messages within ChatRoom.

**Fields:**
- `room` - ForeignKey (ChatRoom) - Parent room
- `sender` - ForeignKey (User) - Message author
- `text` - TextField - Message content
- `created_at` - DateTimeField - Timestamp
- `is_edited` - BooleanField - Edit flag
- `edited_at` - DateTimeField (optional) - Edit timestamp
- `is_deleted` - BooleanField - Soft delete flag

**Methods:**
- `mark_as_read(user)` - Marks message read for specific user
- `get_read_by()` - Returns list of users who read message

---

#### **MessageReadStatus** (L262-280, models.py)
Tracks which users have read which messages.

**Fields:**
- `message` - ForeignKey (Message)
- `user` - ForeignKey (User)
- `read_at` - DateTimeField

---

#### **MessageReaction** (L282-305, models.py)
Emoji reactions to messages (like Facebook reactions).

**Fields:**
- `message` - ForeignKey (Message)
- `user` - ForeignKey (User)
- `reaction` - CharField(10) - Emoji character
- `created_at` - DateTimeField

---

### Projects & Collaboration

#### **Project** (Referenced in serializers.py)
Student project posting for collaboration.

**Fields:**
- `owner` - ForeignKey (User)
- `title` - CharField
- `description` - TextField
- `collaboration_needs` - JSONField - Required skills/roles
- `created_at`, `updated_at` - DateTimeFields
- `is_visible` - BooleanField - Visibility filtering

---

#### **ProjectTeam**, **ProjectTeamMember**, **ProjectTeamInvitation** (models.py)
Team management and invitations for projects.

---

#### **Comment** (Referenced in comment_api.py)
Comments on projects (not fully detailed in model excerpt).

---

### Activity & Notifications

#### **Notification** (models.py)
User notifications (connection requests, likes, comments, etc).

**Fields:**
- `user` - ForeignKey (User) - Notification recipient
- `actor` - ForeignKey (User) - Who triggered notification
- `action_type` - CharField - Type of action
- `content_type` - ForeignKey - Generic FK to object
- `object_id` - PositiveIntegerField
- `is_read` - BooleanField
- `created_at` - DateTimeField

---

#### **Activity** (models.py)
Activity log for user actions.

**Fields:**
- `user` - ForeignKey (User)
- `action` - CharField - Description of action
- `timestamp` - DateTimeField
- Object references for context

---

### Additional Models

- **Follow** - Following relationships between users
- **Like** - Likes on projects/posts
- **UserStats** - User statistics (projects, connections, etc)
- **UserStatus** - Online/offline status
- **File** - File attachments
- **MessageFile** - Files within messages
- **ProjectTask**, **ProjectMilestone** - Project management
- **MessageReadStatus** - Read receipts
- **Draft** - Draft messages (in chat_api)

---

## Views & URLs Architecture

### Authentication Views (`views.py` L309-500)

#### **login_view()**
- Accepts email/password
- Generates OTP via email
- Renders login form
- **URL**: `/accounts/login/`

#### **verify_otp_view()**
- Validates OTP code
- Creates user session if valid
- **URL**: `/accounts/verify-otp/<purpose>/`

#### **register_view()**
- New account creation
- Sends registration OTP
- **URL**: `/accounts/register/`

#### **forgot_password_view()** / **reset_password_view()**
- Password recovery flow
- **URL**: `/accounts/forgot-password/`, `/accounts/reset-password/`

#### **logout_view()**
- Clears session
- **URL**: `/accounts/logout/`

---

### User Profile Views

#### **edit_profile()** (L49-61)
- Edit profile info and upload avatar
- Requires login
- **URL**: `/accounts/profile/edit/`

#### **student_profile()** / **student_details_view()**
- View user's own profile
- **URL**: `/accounts/student-profile/`, `/accounts/student-details/`

#### **user_profile(username)**
- View other user's public profile
- Shows connections, projects, stats
- **URL**: `/accounts/user/<username>/`

#### **profile_view()** / **UserProfileView (REST)**
- REST API endpoint for profile data
- **URL**: `/api/profile/` or `/accounts/profile/`

---

### Project Management Views

#### **post_project()** (views.py)
- Create new project posting
- Requires login
- **URL**: `/accounts/post-project/`

#### **project_detail(project_id)**
- Display project details
- Show collaborators, comments, likes
- **URL**: `/accounts/project-detail/<id>/` or `/project/<id>/`

#### **edit_project(project_id)** / **delete_project(project_id)**
- Edit/delete own project
- Owner-only access
- **URL**: `/accounts/edit-project/<id>/`, `/accounts/delete-project/<id>/`

#### **my_projects_view()** / **explore_projects_view()**
- List user's own projects
- Browse all projects with filtering
- **URL**: `/accounts/my-projects/`, `/accounts/explore-projects/`

#### **search_projects(query)** (L64-74)
- Search by title, description, needs
- **URL**: `/accounts/search/` (implied)

---

### Networking/Collaboration Views

#### **find_collaborators()** (L1398+, views.py)
- Find matching collaborators
- Filters by: college, interests, skills, role
- Uses `StudentProfileNLP` for matching
- **URL**: `/accounts/find-collaborators/`

#### **connect_view(user_id)** / **send_connection_request()**
- Send connection request
- **URL**: `/accounts/connect/<id>/`

#### **accept_connection(connection_id)** / **reject_connection()**
- Accept/reject connection request
- **URL**: `/accounts/accept-connection/<id>/`, `/accounts/reject-connection/<id>/`

#### **my_connections()**
- View user's network
- **URL**: `/accounts/my-connections/`

#### **follow_user(user_id)**
- Follow another user
- **URL**: `/accounts/follow/<id>/`

---

### Messaging Views

#### **message_view()**
- List of all conversations (DMs)
- **URL**: `/accounts/messages/`

#### **chat_view(user_id)**
- Open DM conversation with user
- **URL**: `/accounts/chat/<id>/`

#### **enhanced_messages_view()**
- List of all messaging sessions (DMs + groups)
- **URL**: `/accounts/enhanced-messages/`

#### **enhanced_chat_view(room_id)**
- Open chat room (DM or group)
- **URL**: `/accounts/enhanced-chat/<id>/`

#### **create_group_chat()**
- Create new group chat
- Add members
- **URL**: `/accounts/create-group-chat/`

#### **add_reaction(message_id)**
- Add emoji reaction to message
- **URL**: `/accounts/add-reaction/<id>/`

---

### Activity & Notifications

#### **notifications_view()**
- List user's notifications
- **URL**: `/accounts/notifications/`

#### **mark_notification_read(notification_id)**
- Mark notification as read
- **URL**: `/accounts/mark-notification-read/<id>/`

#### **activity_feed()**
- Timeline of user activities
- **URL**: `/accounts/activity-feed/`

---

### REST API Endpoints

#### Chat Room APIs (from `chat_api.py`)
```
POST   /api/chat-rooms/                      - Create new room
GET    /api/chat-rooms/                      - List rooms
GET    /api/chat-rooms/<id>/                 - Get room details
PATCH  /api/chat-rooms/<id>/                 - Update room
DELETE /api/chat-rooms/<id>/                 - Delete room
GET    /api/chat-rooms/<id>/members/         - Get room members
POST   /api/direct-message/                  - Create DM with user
```

#### Message APIs
```
GET    /api/messages/                        - List messages (paginated)
POST   /api/messages/                        - Create message
GET    /api/messages/<id>/                   - Get message details
PATCH  /api/messages/<id>/                   - Edit message
DELETE /api/messages/<id>/                   - Delete message
GET    /api/messages/search/                 - Search messages
GET    /api/messages/<id>/status/            - Get read receipts
POST   /api/messages/<id>/reactions/         - Add reaction
GET    /api/conversations/                   - List conversations
```

#### Draft & Typing APIs
```
GET    /api/drafts/                          - Get draft messages
POST   /api/drafts/                          - Create draft
POST   /api/typing/                          - Send typing indicator
```

---

#### Comments API (from `comment_api.py`)
```
POST   /api/comments/                        - Add comment to project
GET    /api/comments/<project_id>/           - Get comments for project
PUT    /api/comments/<comment_id>/           - Edit comment
DELETE /api/comments/<comment_id>/           - Delete comment
```

---

## URL Routing Structure (`urls.py`)

### Main Routes
```python
urlpatterns = [
    # Authentication (L22-29)
    path('accounts/login/', ...)
    path('accounts/register/', ...)
    path('accounts/logout/', ...)
    path('accounts/verify-otp/<purpose>/', ...)
    
    # Profiles (L31-34)
    path('accounts/student-profile/', ...)
    path('accounts/profile/', UserProfileView.as_view(), ...)
    
    # Projects (L39-43)
    path('accounts/post-project/', ...)
    path('accounts/project-detail/<id>/', ...)
    path('accounts/edit-project/<id>/', ...)
    
    # Networking (L45-57)
    path('accounts/find-collaborators/', ...)
    path('accounts/connect/<id>/', ...)
    path('accounts/accept-connection/<id>/', ...)
    
    # Chat & Messaging (L64-73)
    path('accounts/messages/', ...)
    path('accounts/chat/<id>/', ...)
    path('accounts/enhanced-chat/<id>/', ...)
    path('accounts/create-group-chat/', ...)
    
    # REST API (L78-100)
    path('api/chat-rooms/', ...)
    path('api/messages/', ...)
    path('api/conversations/', ...)
]
```

---

## Key Services & Utilities

### **StudentProfileNLP** (in `utils.py`)
Custom utility for collaborative filtering and NLP-based matching
- Matches users based on interests and skills
- Used in `find_collaborators()`

### **ProjectVisibilityFilter** (in `utils.py`)
Filtering logic for project visibility
- Applies filters: public/private, user's own projects, etc.
- Used in project listing views

### **Email Backends**
- **brevo_mail_backend.py** - Brevo email service
- **zepto_mail_backend.py** - Zeptomail service
- Fallback to Django's default SMTP

### **OTP Generation & Verification** (models.py, views.py)
- 6-digit random code
- 5-minute expiration
- Email delivery with HTML template

---

## Key Features Implementation

### 1. **OTP-Based Authentication**
- User enters email → OTP sent → OTP verified → Account created/logged in
- Supports: login, registration, password reset
- 5-minute TTL, single-use tokens

### 2. **Social Authentication**
- Google OAuth via django-allauth
- GitHub OAuth via django-allauth
- Automatic profile creation on first login

### 3. **Project Posting & Discovery**
- Users can post projects with requirements
- Search & filter by skills, keywords, needs
- Like & comment functionality

### 4. **Collaborative Matching**
- `find_collaborators()` - Matches students with similar interests/skills
- Uses college, interests, skills, role preferences
- NLP-based filtering

### 5. **Real-Time Messaging**
- Direct messages between users
- Group chat rooms
- Typing indicators
- Emoji reactions
- Draft messages
- Message search & filtering

### 6. **User Networking**
- Connection requests (pending/accepted)
- Follow system
- View user profiles
- Activity feed

### 7. **Notifications System**
- Connection request notifications
- Comment notifications
- Like notifications
- Message/chat notifications

---

## Configuration & Settings (`settings.py`)

### Database
- Detects `DATABASE_URL` from environment (Render)
- Falls back to SQLite for development
- Auto-migration support

### Email
- Uses `DEFAULT_FROM_EMAIL` from env
- Supports multiple backends (Brevo, Zeptomail, SMTP)
- HTML + Plaintext email templates

### Authentication
- Django Allauth configured for Google & GitHub
- Custom OTP backend
- Session-based authentication

### Security
- CSRF protection enabled
- `SECURE_SSL_REDIRECT`, `SESSION_COOKIE_SECURE`, `CSRF_COOKIE_SECURE` configurable
- Input sanitization in views

### Media Files
- Profile photos stored in `media/profile_photos/`
- File attachments in messages

### Static Files
- CSS, JS, images in `static/`
- Collected to `staticfiles/` for production

---

## Serializers (`serializers.py`)

### **UserProfileSerializer**
Serializes StudentProfile for REST API
- Fields: full_name, college, interests, skills, profile_photo, social links

### **ProjectSerializer**
Serializes Project model
- Fields: title, description, owner, created_at, likes_count, comments_count

### Custom Serializers for:
- Connections
- Messages
- ChatRooms
- Comments

---

## Key Files Summary

| File | Purpose | Key Classes/Functions |
|------|---------|----------------------|
| `models.py` | Database models | StudentProfile, OTP, Connection, Message, ChatRoom, Project, etc. |
| `views.py` | Request handlers | login_view, register_view, post_project, find_collaborators, etc. |
| `urls.py` | URL routing | All app routes and REST API endpoints |
| `serializers.py` | API serialization | UserProfileSerializer, ProjectSerializer, etc. |
| `forms.py` | Form validation | RegisterForm, LoginForm, StudentProfileForm, etc. |
| `chat_api.py` | Chat REST API | ChatRoomListCreateView, MessageListCreateView, etc. |
| `chat_api_improved.py` | Enhanced chat | Advanced REST endpoints for messaging |
| `comment_api.py` | Comments | add_comment, get_comments, edit_comment, delete_comment |
| `permissions.py` | Access control | IsOwner, IsConnected, etc. |
| `utils.py` | Utilities | StudentProfileNLP, ProjectVisibilityFilter, sanitize_input |
| `brevo_mail_backend.py` | Email service | Brevo integration |
| `zepto_mail_backend.py` | Email service | Zeptomail integration |
| `settings.py` | Configuration | Django settings, database, email, auth config |

---

## Common Code Patterns

### Error Handling
```python
@handle_view_errors  # Decorator
def my_view(request):
    try:
        # logic
    except Exception as e:
        logger.error(f"Error: {str(e)}", exc_info=True)
        messages.error(request, "An unexpected error occurred")
        return redirect('/')
```

### Input Sanitization
```python
text = sanitize_input(user_input, max_length=500)
# Removes HTML tags, dangerous chars, limits length
```

### OTP Email
```python
send_otp_email(email, otp_code, purpose)
# Sends HTML + plaintext OTP to email
```

### Login Required
```python
@login_required
def protected_view(request):
    # Only authenticated users
    pass
```

### REST API Views
```python
from rest_framework import generics

class ChatRoomListCreateView(generics.ListCreateAPIView):
    queryset = ChatRoom.objects.all()
    serializer_class = ChatRoomSerializer
    permission_classes = [permissions.IsAuthenticated]
```

---

## Testing & Debugging Scripts

Various test scripts in root directory:
- `test_login.py` - Login flow testing
- `test_otp.py`, `test_otp_simple.py` - OTP testing
- `test_comments_api.py` - Comments API testing
- `test_profile_fix.py` - Profile feature testing
- `test_email.py`, `test_brevo_email.py` - Email integration
- `debug_filtering.py` - Project filtering debug
- `debug_find_collaborators.py` - Collaborator matching debug
- `performance_monitor.py` - Performance analysis

---

## Deployment Configuration

### Environment Variables Required
```
DEBUG=False
SECRET_KEY=<generated>
DATABASE_URL=<postgres_url>
ALLOWED_HOSTS=yourdomain.com
DEFAULT_FROM_EMAIL=noreply@yourdomain.com
BREVO_API_KEY=<key>
GOOGLE_OAUTH_KEY=<key>
GOOGLE_OAUTH_SECRET=<secret>
```

### Deployment Targets
- **Render.com** - (render.yaml, Procfile)
- **Railway** - (railway.json)

### Static Files
```
python manage.py collectstatic
```

---

## Data Flow Diagrams

### Authentication Flow
```
User (Email) 
  → Login View 
  → Generate OTP 
  → Send Email 
  → Verify OTP View 
  → Create/Update User & Profile 
  → Set Session 
  → Redirect Dashboard
```

### Project Discovery Flow
```
User 
  → Explore Projects 
  → Filter/Search 
  → View Project Detail 
  → See Comments 
  → Like Project 
  → View Collaborators
```

### Collaboration Matching Flow
```
User 
  → Find Collaborators 
  → StudentProfileNLP Matching 
  → Filter by College/Interests 
  → Display Results 
  → Send Connection Request 
  → Other User Accepts
```

### Messaging Flow
```
User A 
  → Start Chat (or Create Group) 
  → Send Message 
  → Message Stored in DB 
  → User B Notified 
  → User B Reads Message 
  → Read Status Updated 
  → Typing Indicators Show Activity
```

---

## Security Features

1. **OTP Verification** - Prevents unauthorized access
2. **Django CSRF Protection** - Enabled in settings
3. **Input Sanitization** - HTML tag stripping, dangerous char removal
4. **Permission Decorators** - @login_required for protected views
5. **User Object Level Permissions** - Only owner can edit project/profile
6. **Social Auth Validation** - Allauth handles OAuth security
7. **Session-Based Auth** - Secure session handling

---

## Performance Optimizations

1. **Database Indexing** - Indexes on frequently queried fields
2. **Query Optimization** - Uses select_related(), prefetch_related()
3. **Caching** - @cache_page decorator for static views
4. **Pagination** - 10 items per page for project lists
5. **Image Optimization** - File extension validation
6. **Query Monitoring** - performance_monitor.py for analysis

---

## Known Issues & Recent Fixes

Based on documentation files:
- **Comments Badge Bug** - Fixed badge count visibility
- **Profile Picture Upload** - Fixed image not appearing after upload
- **Project Filtering** - Fixed visibility filter logic
- **Message Read Status** - Fixed read receipt tracking
- **Email OTP** - Configuration optimizations
- **Google Login** - OAuth setup and redirect handling
- **Performance Issues** - Database query optimization

---

## Future Enhancement Opportunities

1. **Real-Time Chat** - WebSocket integration (Channels)
2. **Video Calling** - WebRTC integration
3. **File Sharing** - Larger file upload support
4. **Project Timeline** - Gantt charts for milestones
5. **AI Recommendations** - Enhanced collaborator matching
6. **Mobile App** - React Native/Flutter app
7. **Analytics Dashboard** - User/project statistics
8. **Premium Features** - Subscription tier system

---

## Conclusion

UniSync is a well-structured Django application with:
- Clear separation of concerns (models, views, serializers)
- Comprehensive authentication system (OTP + OAuth)
- Robust messaging and networking features
- Scalable project management capabilities
- Multiple deployment options (Render, Railway)

The codebase is production-ready with established patterns for error handling, input validation, and user security.
