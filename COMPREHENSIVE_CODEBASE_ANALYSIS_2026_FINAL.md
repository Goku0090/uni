# UniSinq Codebase - Comprehensive Code Analysis

## Project Overview
**UniSinq** (formerly UniSync) is a Django-based collaborative project platform for students and professionals. It features real-time updates, user authentication via OTP, social logins, messaging, and project management capabilities.

**Tech Stack:**
- Backend: Django 4.x + Django REST Framework (DRF)
- Real-time: Django Channels + WebSocket (ws://)
- Frontend: HTML5/CSS3/Vanilla JavaScript
- Database: PostgreSQL (SQLite for development)
- Authentication: Custom OTP + django-allauth (Google/GitHub OAuth)

---

## Database Models Architecture

### Core User Models

#### `StudentProfile` (Extended User Profile)
```python
# Extends Django's User model with additional fields
- full_name: str
- college: str (with autocomplete)
- location: str
- profile_photo: ImageField
- bio: TextField
- interests: JSONField (array of strings)
- skills: JSONField (array of strings)
- project_interests: JSONField (array)
- role_preference: str (designer, developer, etc.)
- github, linkedin, portfolio, behance: URLField
- profile_completed: bool
```

**Key Methods:**
- `get_display_name()`: Returns full_name or username fallback

#### `OTP` (One-Time Password)
```python
- email: EmailField
- otp_code: CharField (6 digits)
- purpose: choice (login, registration, reset)
- is_used: bool
- created_at, expires_at: DateTime
```

**Key Methods:**
- `is_valid()`: Checks expiry (5-minute window) and usage
- `verify_otp(code)`: Validates code and marks as used
- `generate_otp(email, purpose)`: Creates new OTP, deactivates old ones

### Connection & Relationship Models

#### `Connection` (User Connections)
```python
- sender, receiver: ForeignKey(User)
- status: choice (pending, accepted, rejected)
- created_at, updated_at: DateTime
- Unique constraint: [sender, receiver]
```

#### `Follow` (User Following)
```python
- follower, following: ForeignKey(User)
- created_at: DateTime
- Unique constraint: [follower, following]
```

### Project Management Models

#### `Project` (Main Project Model)
```python
- user: ForeignKey(User) [Project Owner]
- title, description: CharField/TextField
- category: choice (web, mobile, ai, data, blockchain, iot, game, other)
- technologies: JSONField (array of tech tags)
- looking_for: JSONField (array of required roles)
- timeline: CharField
- collaboration_needs: TextField
- github_link: URLField
- is_active: bool
- created_at, updated_at: DateTime
```

**Key Methods:**
- `get_technologies_list()`: Returns list for backward compatibility
- `get_looking_for_list()`: Returns list for backward compatibility

#### `ProjectMember` (Team Members with Roles)
```python
- project: ForeignKey(Project)
- user: ForeignKey(User)
- role: choice (owner, admin, contributor, viewer)
- is_active: bool
- joined_at: DateTime
- Unique constraint: [project, user]
```

**Key Properties:**
- `can_manage_project`: owner or admin
- `can_invite_members`: owner or admin
- `can_manage_tasks`: owner, admin, or contributor
- `can_edit_project`: owner, admin, or contributor

#### `ProjectInvitation` (Team Invitations)
```python
- project, invited_user, invited_by: ForeignKey(User)
- role: choice (from ProjectMember.ROLES)
- message: TextField
- status: choice (pending, accepted, declined, expired)
- created_at, expires_at, responded_at: DateTime
```

**Key Methods:**
- `accept()`: Creates ProjectMember, marks as accepted
- `decline()`: Marks as declined

#### `ProjectTask` (Work Items)
```python
- project: ForeignKey(Project)
- title, description: CharField/TextField
- assigned_to, assigned_by: ForeignKey(User)
- status: choice (todo, in_progress, review, completed, cancelled)
- priority: choice (low, medium, high, urgent)
- due_date: DateField
- completed_at: DateTime
- created_at, updated_at: DateTime
```

**Key Methods:**
- `mark_completed()`: Sets status to completed, records timestamp

#### `ProjectMilestone` (Project Milestones)
```python
- project: ForeignKey(Project)
- title, description: CharField/TextField
- due_date: DateField
- is_completed: bool
- completed_at, created_at, updated_at: DateTime
- completed_by: ForeignKey(User)
```

**Key Methods:**
- `mark_completed(user)`: Marks milestone as complete

### Interaction Models

#### `Comment` (Project Comments)
```python
- user: ForeignKey(User)
- project: ForeignKey(Project)
- content: TextField
- created_at, updated_at: DateTime
```

#### `Like` (Project Likes)
```python
- user, project: ForeignKey
- created_at: DateTime
- Unique constraint: [user, project] (one like per user per project)
```

#### `Activity` (User Activity Feed)
```python
- user: ForeignKey(User)
- activity_type: choice (profile_updated, project_created, project_liked, connection_made, message_sent, comment_added, user_followed, task_completed, milestone_completed)
- title, description: CharField/TextField
- project, target_user, connection: ForeignKey (optional)
- is_public: bool
- created_at: DateTime
```

#### `UserStats` (Dashboard Statistics)
```python
- user: OneToOne(User)
- projects_created, connections_made, likes_received: count
- comments_made, projects_joined, tasks_completed: count
- followers_count, following_count: count
- last_updated: DateTime
```

**Key Methods:**
- `update_stats()`: Recalculates all statistics from database

### Messaging Models

#### `ChatRoom` (Group & Direct Chats)
```python
- name: CharField (nullable for direct)
- chat_type: choice (direct, group, project)
- project: ForeignKey(Project, nullable)
- is_active: bool
- created_at, created_by: DateTime, ForeignKey(User)
```

**Key Properties:**
- `display_name`: Returns appropriate name based on type

#### `ChatRoomMember` (Chat Participants)
```python
- chat_room: ForeignKey(ChatRoom)
- user: ForeignKey(User)
- role: choice (owner, admin, member)
- is_active: bool
- joined_at: DateTime
- Unique constraint: [chat_room, user]
```

**Key Properties:**
- `can_invite_members`: owner or admin
- `can_manage_room`: owner or admin

#### `Message` (Chat Messages)
```python
- sender, receiver: ForeignKey(User)
- chat_room: ForeignKey(ChatRoom, nullable)
- content: TextField
- message_type: choice (text, file, image, call)
- call_type: choice (voice, video, nullable)
- reply_to: ForeignKey(self, nullable) [Threading]
- created_at, updated_at: DateTime
```

**Key Methods:**
- `mark_as_read_by(user)`: Creates/updates MessageReadStatus
- `is_read_by(user)`: Checks if user read message
- `get_read_by_users()`: Returns User queryset of readers
- `get_read_count()`: Returns number of readers
- `get_unread_users()`: Returns unread users for group chats

#### `MessageReadStatus` (Read Tracking)
```python
- message: ForeignKey(Message)
- user: ForeignKey(User)
- read_at: DateTime
- Unique constraint: [message, user]
```

#### `MessageReaction` (Emoji Reactions)
```python
- message: ForeignKey(Message)
- user: ForeignKey(User)
- reaction: CharField (emoji)
- created_at: DateTime
- Unique constraint: [message, user, reaction]
```

#### `MessageFile` (File Attachments)
```python
- message: ForeignKey(Message)
- file: ForeignKey(File)
- uploaded_at: DateTime
- Unique constraint: [message, file]
```

#### `File` (Uploaded Files)
```python
- user: ForeignKey(User)
- file: FileField (upload_to='chat_files/')
- filename, file_type: CharField
- file_size: PositiveIntegerField
- uploaded_at: DateTime
```

**Key Properties:**
- `is_image`: bool (checks if image MIME type)

### Notification & Status Models

#### `Notification` (User Notifications)
```python
- user: ForeignKey(User)
- notification_type: choice (connection_request, connection_accepted, message, project_like, project_comment, team_invitation, follow)
- title, message: CharField/TextField
- from_user, connection, message_obj: ForeignKey (optional)
- is_read: bool
- read_at: DateTime (nullable)
- created_at: DateTime
```

#### `UserStatus` (Online/Offline Status)
```python
- user: OneToOne(User)
- is_online: bool
- last_seen: DateTime
- current_room: CharField (WebSocket room identifier)
```

---

## Views & API Endpoints Architecture

### Authentication Views (`accounts/views.py`)

#### Registration & OTP Flow
```python
POST /auth/send-otp/
  Payload: { email: str, purpose: 'registration'|'login'|'reset' }
  Response: { message: str, otp_id: int }
  - Validates email format
  - Creates OTP record with 5-minute expiry
  - Sends email via Brevo/ZeptoMail

POST /auth/verify-otp/
  Payload: { email: str, otp_code: str, purpose: str }
  Response: { token: str, user: UserSerializer }
  - Verifies OTP validity and code
  - For registration: creates User + StudentProfile
  - For login: authenticates user
  - Returns JWT/Session token

POST /auth/register/
  Payload: { email: str, password: str, full_name: str }
  Response: { message: str }
  - Alternative registration without OTP
  - Validates password strength

POST /auth/login/
  Payload: { email: str, password: str }
  Response: { token: str, user: UserSerializer }
  - Traditional login (email + password)
```

#### Social Login Integration (django-allauth)
```python
GET /accounts/google/login/
  - Redirects to Google OAuth consent
  - Callback creates/updates User + StudentProfile

GET /accounts/github/login/
  - GitHub OAuth flow
  - Automatically creates profile from GitHub data
```

### Project Views

#### Project CRUD
```python
GET /projects/
  Response: [ProjectSerializer] (paginated)
  - Lists all active projects
  - Supports filtering by category, technologies
  - Supports search by title/description

POST /projects/
  Payload: { title, description, category, technologies, looking_for }
  Response: ProjectSerializer
  - Creates project for authenticated user
  - Auto-sets user as owner
  - Creates ProjectMember with 'owner' role

GET /projects/{id}/
  Response: ProjectSerializer + members + comments + tasks
  - Detailed project view with all relationships

PATCH /projects/{id}/
  Payload: { title, description, category, etc. }
  Response: ProjectSerializer
  - Updates project (owner only)
  - Creates Activity log entry

DELETE /projects/{id}/
  Response: { message: str }
  - Soft delete (sets is_active=False)
```

#### Team Management
```python
POST /projects/{id}/members/
  Payload: { user_id: int, role: str }
  Response: ProjectMemberSerializer
  - Adds member to project
  - Broadcasts via WebSocket

POST /projects/{id}/invite/
  Payload: { email: str, role: str, message: str }
  Response: ProjectInvitationSerializer
  - Creates invitation for external user
  - Sends email with invitation link

GET /projects/{id}/invitations/
  Response: [ProjectInvitationSerializer]
  - Lists pending invitations

POST /invitations/{id}/accept/
  Response: { message: str }
  - Accepts invitation, creates ProjectMember

POST /invitations/{id}/decline/
  Response: { message: str }
  - Declines invitation
```

#### Task Management
```python
GET /projects/{project_id}/tasks/
  Response: [ProjectTaskSerializer]

POST /projects/{project_id}/tasks/
  Payload: { title, description, assigned_to, priority, due_date }
  Response: ProjectTaskSerializer

PATCH /projects/{project_id}/tasks/{task_id}/
  Payload: { status, priority, etc. }
  Response: ProjectTaskSerializer
  - Updates task, broadcasts status change
  - Notifies assigned user

POST /projects/{project_id}/tasks/{task_id}/complete/
  Response: { message: str }
  - Marks task as complete
  - Records timestamp and creates Activity
```

### Comment & Interaction Views

#### Comments API
```python
GET /projects/{project_id}/comments/
  Response: [CommentSerializer] (ordered by created_at)

POST /projects/{project_id}/comments/
  Payload: { content: str }
  Response: CommentSerializer
  - Creates comment
  - Broadcasts via WebSocket
  - Notifies project owner

DELETE /comments/{id}/
  Response: { message: str }
  - Deletes comment (author or project owner)
```

#### Like & Share
```python
POST /projects/{id}/like/
  Response: { liked: bool, like_count: int }
  - Toggles like status
  - Creates/deletes Like record
  - Updates UserStats

GET /projects/{id}/likes/
  Response: { like_count: int, user_liked: bool, users: [UserSerializer] }
```

### User Profile Views

#### Profile Management
```python
GET /user/profile/
  Response: UserProfileSerializer
  - Returns authenticated user's profile

PATCH /user/profile/
  Payload: { full_name, college, interests, skills, bio, profile_photo }
  Response: UserProfileSerializer
  - Updates StudentProfile
  - Validates photo format (jpg, jpeg, png, gif)

POST /user/profile/upload-photo/
  Content-Type: multipart/form-data
  Payload: { profile_photo: File }
  Response: { photo_url: str }

GET /user/{username}/
  Response: UserProfileSerializer + stats + projects
  - Public profile view
```

#### Collaborator Discovery
```python
GET /search/collaborators/?q=skill&college=name&interests=ai
  Response: [UserProfileSerializer]
  - Filters by skills, college, interests
  - Supports faceted search

GET /search/projects/?category=web&tech=react
  Response: [ProjectSerializer]
  - Filters projects by category, technologies
```

### Messaging Views (REST API)

#### Chat Rooms
```python
GET /api/chat/rooms/
  Response: [ChatRoomSerializer]
  - Lists user's chat rooms (direct + group)

POST /api/chat/rooms/
  Payload: { name, chat_type, members: [user_ids] }
  Response: ChatRoomSerializer
  - Creates group chat room

PATCH /api/chat/rooms/{id}/
  Payload: { name, is_active }
  Response: ChatRoomSerializer
  - Updates room settings
```

#### Messages
```python
GET /api/chat/rooms/{room_id}/messages/
  Response: [MessageSerializer] (paginated, ordered by created_at)
  - Fetches message history
  - Marks all as read by current user

POST /api/chat/rooms/{room_id}/messages/
  Payload: { content, message_type, file }
  Response: MessageSerializer
  - Creates message
  - Broadcasts via WebSocket
  - Sends notifications

PUT /api/chat/messages/{id}/read/
  Response: { read_at: DateTime }
  - Marks message as read
  - Updates MessageReadStatus
```

#### Message Reactions
```python
POST /api/chat/messages/{id}/reactions/
  Payload: { reaction: str }
  Response: MessageReactionSerializer
  - Adds emoji reaction

DELETE /api/chat/messages/{id}/reactions/{reaction}/
  Response: { message: str }
  - Removes reaction
```

---

## WebSocket Real-Time Features

### Architecture: Django Channels

**Routing:** `accounts/routing.py`
```python
websocket_urlpatterns = [
    re_path(r'ws/project/(?P<project_id>\w+)/$', ProjectUpdateConsumer.as_asgi()),
    re_path(r'ws/activity/$', ActivityFeedConsumer.as_asgi()),
    re_path(r'ws/notifications/$', NotificationConsumer.as_asgi()),
    re_path(r'ws/chat/(?P<room_id>\w+)/$', ChatConsumer.as_asgi()),
]
```

### ProjectUpdateConsumer (`consumers.py:ProjectUpdateConsumer`)

**Broadcasts:**
- **project.initial_data**: Sends full project data on connect
- **project.status_update**: Project status/details changed
- **project.member_added**: New member joined team
- **project.comment_posted**: New comment on project
- **project.member_count**: Team size changed

**Receiving:**
- `status.update`: Changes project details
- `member.add`: Adds user to project
- `comment.post`: Posts new comment

**Group Name:** `project_{project_id}`
**Example Usage:**
```javascript
let socket = new WebSocket("ws://localhost:8000/ws/project/2/");
socket.onopen = () => console.log("✅ WORKING!");
socket.onmessage = (e) => {
    let data = JSON.parse(e.data);
    if (data.type === 'project.comment_posted') {
        console.log(`New comment: ${data.text}`);
    }
};
```

### ActivityFeedConsumer (`consumers.py:ActivityFeedConsumer`)

**Broadcasts:**
- **activity.update**: Any activity in user's feed
  - project.created, project.updated
  - member.added, comment.posted
  - status.changed, like.added

**Group Name:** `activity_feed_{user_id}`

### NotificationConsumer (`consumers.py:NotificationConsumer`)

**Broadcasts:**
- **notification.count**: Unread notification count (on connect)
- **notification.received**: New notification
  - connection_request, connection_accepted
  - message, project_like, project_comment
  - team_invitation, follow

**Receiving:**
- `mark_read`: Marks notification as read

**Group Name:** `notifications_{user_id}`

### Triggering WebSocket Events

**From Views/Signals:**
```python
from channels.layers import get_channel_layer
import asyncio

async def broadcast_comment(project_id, comment):
    channel_layer = get_channel_layer()
    await channel_layer.group_send(
        f'project_{project_id}',
        {
            'type': 'project.comment_posted',
            'comment_id': comment.id,
            'author': comment.user.username,
            'text': comment.content,
            'timestamp': comment.created_at.isoformat(),
        }
    )
```

---

## Frontend JavaScript Files

### Key Files (in `staticfiles/js/`)

#### `realtime-updates.js`
- Establishes WebSocket connections
- Handles reconnection logic
- Processes incoming messages
- Updates DOM in real-time

#### `comments-handler.js`
- Posts new comments
- Refreshes comment list
- Handles comment deletion
- Updates comment count badge

#### `messages-handlers.js`
- Sends/receives messages
- Marks messages as read
- Manages chat room switching
- Shows typing indicators (if implemented)

#### `messages-api.js`
- AJAX calls to message endpoints
- Fetches chat history
- Gets unread count
- Updates read status

#### `profile.js`
- Profile photo upload
- Form validation
- Updates user profile

#### `api-utils.js`
- CSRF token handling
- HTTP request wrappers
- Error handling
- Token management

---

## Key Features & Implementation Details

### 1. OTP-Based Authentication
- 6-digit OTP sent via email (Brevo/ZeptoMail)
- 5-minute expiry window
- One-time use enforcement
- Purpose tracking (login, registration, reset)
- Email validation before sending OTP

### 2. Social Login (OAuth 2.0)
- Google OAuth: `django-allauth` integration
- GitHub OAuth: Auto-creates profile from data
- Email verification on first login
- Auto-profile creation from social data

### 3. Project Collaboration
- Multiple team roles (owner, admin, contributor, viewer)
- Role-based permissions
- Invitation system with email notifications
- Project categorization (8 categories)
- Technology tagging (JSON array)
- Task management with priorities
- Milestone tracking

### 4. Real-Time Updates
- WebSocket connections for 3 main streams
- Channel Groups for broadcasting
- JSON message format
- Activity feed with emojis
- Notification delivery system
- Connection status tracking

### 5. Direct & Group Messaging
- Private direct messages
- Group chat rooms
- Project-specific chats
- Message threading (reply_to)
- Emoji reactions
- File attachments
- Read receipts (per-user tracking)
- Message types (text, file, image, call)

### 6. User Discovery
- Skill-based filtering
- College-based filtering
- Interest-based matching
- Full-text search
- Advanced skill matching algorithm

### 7. Activity & Statistics
- User activity feed (8 types)
- Real-time activity broadcasting
- User statistics dashboard
- Follow system
- Activity visibility (public/private)

---

## Database Relationships (ER Diagram)

```
User (Django Auth)
├── StudentProfile (1:1)
├── Projects (1:M) [as owner]
├── ProjectMembers (M:M via ProjectMember)
├── Comments (1:M)
├── Likes (1:M)
├── Activities (1:M)
├── Connections (M:M via Connection)
├── Follows (M:M via Follow)
├── Messages (1:M as sender/receiver)
├── ChatRoomMembers (M:M via ChatRoomMember)
├── Notifications (1:M)
└── UserStats (1:1)

Project (1:M to User)
├── ProjectMembers (1:M)
├── ProjectInvitations (1:M)
├── Comments (1:M)
├── Likes (1:M)
├── Tasks (1:M)
├── Milestones (1:M)
├── Activities (1:M)
└── ChatRooms (1:M as project chat)

Message (1:M to ChatRoom)
├── MessageReadStatus (1:M)
├── MessageReactions (1:M)
└── MessageFiles (1:M)

ChatRoom
├── ChatRoomMembers (1:M)
└── Messages (1:M)
```

---

## API Response Format

### Standard Success Response
```json
{
  "data": { /* object or array */ },
  "message": "Success message",
  "status": 200
}
```

### Standard Error Response
```json
{
  "error": "Error message",
  "status": 400,
  "details": { /* validation errors */ }
}
```

### Paginated Response
```json
{
  "count": 100,
  "next": "/api/projects/?page=2",
  "previous": null,
  "results": [ /* items */ ]
}
```

### WebSocket Message Format
```json
{
  "type": "event_type",
  "timestamp": "2026-02-09T10:30:00Z",
  "data": { /* event-specific data */ }
}
```

---

## Performance Considerations

### Database Optimizations
- **Prefetching:** Use `prefetch_related()` for M:M relationships
- **Filtering:** Index on frequently filtered fields (user_id, project_id, created_at)
- **Caching:** Cache user profiles, project lists
- **Pagination:** 20 items per page by default

### WebSocket Optimization
- Group-based broadcasting (efficient)
- Async operations with `@database_sync_to_async`
- Connection pooling for database
- Redis for channel layer (production)

### API Optimization
- JSON serialization for fast response
- Response compression (gzip)
- CORS headers configuration
- Rate limiting on auth endpoints

---

## Security Features

### Authentication
- CSRF token validation (Django middleware)
- CORS white-listing
- Session-based + Token-based auth
- OTP verification server-side

### Authorization
- Project owner/admin checks
- Role-based permissions (RBAC)
- User isolation (can't access others' private data)
- WebSocket authentication (via Django user)

### Data Validation
- Email format validation
- File extension validation (images)
- OTP code format (6 digits)
- Input sanitization (prevent XSS)

### Privacy
- Private profile option
- Activity visibility control (public/private)
- Message encryption (optional)
- GDPR-compliant data handling

---

## Error Handling

### Standard HTTP Status Codes
- **200 OK:** Successful request
- **201 Created:** Resource created
- **204 No Content:** Successful deletion
- **400 Bad Request:** Validation error
- **401 Unauthorized:** Auth required
- **403 Forbidden:** Permission denied
- **404 Not Found:** Resource doesn't exist
- **409 Conflict:** Duplicate entry
- **500 Internal Server Error:** Server error

### Common Error Messages
```python
"Invalid OTP code." # OTP mismatch
"OTP has expired or is invalid." # OTP expired
"Only project owner can update status" # Permission error
"User not found" # 404
"Email already registered" # Conflict
```

---

## Key Code Patterns

### Model Methods
```python
# Read status tracking
message.mark_as_read_by(user)
message.is_read_by(user)
message.get_read_count()

# Permission checks
member.can_manage_project
member.can_invite_members

# Data retrieval
project.get_technologies_list()
user_stats.update_stats()
```

### Serialization
```python
# DRF Serializers
class ProjectSerializer(serializers.ModelSerializer):
    owner = UserSimpleSerializer(source='user', read_only=True)
    members = ProjectMemberSerializer(many=True)
    comments_count = serializers.SerializerMethodField()
```

### WebSocket Patterns
```python
# Broadcasting
await channel_layer.group_send(group_name, event_dict)

# Receiving
async def event_type_name(self, event):
    await self.send(text_data=json.dumps(...))

# Database access in async
@database_sync_to_async
def get_data(self):
    return Model.objects.filter(...)
```

---

## Testing Recommendations

### Unit Tests
- OTP generation and validation
- Permission checks
- Model save methods

### Integration Tests
- User registration flow
- Project creation + team invitation
- Message send + read receipt

### WebSocket Tests
- Connection/disconnection handling
- Broadcasting to groups
- Message format validation

### End-to-End Tests
- Complete project collaboration workflow
- Social login flow
- Real-time updates display

---

## Deployment Checklist

### Environment Variables
```bash
DEBUG=False
SECRET_KEY=<generate-new>
ALLOWED_HOSTS=<domain>
DATABASE_URL=postgres://...
EMAIL_HOST=smtp.brevo.com
EMAIL_PORT=587
CHANNEL_LAYERS=redis://...
SOCIAL_AUTH_GOOGLE_OAUTH2_KEY=<key>
SOCIAL_AUTH_GITHUB_KEY=<key>
```

### Infrastructure
- PostgreSQL database
- Redis for channels + caching
- Daphne for ASGI (WebSocket support)
- Nginx reverse proxy
- SSL certificate (HTTPS)
- Email service (Brevo/ZeptoMail)

### Commands to Run
```bash
python manage.py migrate
python manage.py collectstatic
python manage.py createsuperuser
daphne -b 0.0.0.0 -p 8000 auth_project.asgi:application
```

---

## File Structure Reference

```
auth_project/
├── accounts/
│   ├── models.py (20+ models)
│   ├── views.py (40+ views)
│   ├── serializers.py (DRF serializers)
│   ├── urls.py (API routes)
│   ├── consumers.py (WebSocket handlers)
│   ├── routing.py (WebSocket routing)
│   ├── signals.py (Django signals)
│   ├── admin.py (Django admin config)
│   ├── apps.py
│   ├── tasks.py (Celery tasks, if used)
│   ├── templates/ (30+ HTML templates)
│   │   ├── login.html
│   │   ├── register.html
│   │   ├── dashboard.html
│   │   ├── project_detail.html
│   │   ├── profile.html
│   │   ├── chat.html
│   │   └── ...
│   └── migrations/ (database schema)
├── auth_project/
│   ├── settings.py (Django config)
│   ├── urls.py (main routing)
│   ├── asgi.py (Daphne config)
│   ├── wsgi.py (Gunicorn config)
│   └── ...
├── static/
│   └── js/
│       ├── realtime-updates.js
│       ├── comments-handler.js
│       ├── messages-handlers.js
│       ├── messages-api.js
│       ├── profile.js
│       └── ...
├── manage.py
└── requirements.txt
```

---

## Summary

UniSinq is a **feature-rich collaboration platform** with:
- ✅ Real-time updates (WebSocket)
- ✅ Multi-user authentication (OTP + OAuth)
- ✅ Project team management
- ✅ Direct & group messaging
- ✅ Activity feeds + notifications
- ✅ Advanced search + filtering
- ✅ Role-based permissions
- ✅ File sharing + attachments
- ✅ Task tracking + milestones

The codebase demonstrates **professional Django patterns** including async consumers, DRF APIs, signal handling, and comprehensive models with proper relationships and methods.
