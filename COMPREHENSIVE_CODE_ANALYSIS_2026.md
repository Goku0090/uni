# UniSync Platform - Comprehensive Code Analysis 2026

## Executive Summary

UniSync is a **Django-based student collaboration platform** that enables university students to discover project opportunities, build teams, and collaborate in real-time. The application integrates OAuth authentication, OTP verification, REST APIs, WebSocket-powered live updates, and email notification systems.

**Tech Stack:**
- **Backend:** Django 4.x, Django REST Framework, Django Channels (WebSockets)
- **Frontend:** HTML/CSS/JavaScript with AJAX/WebSocket clients
- **Database:** SQLite (dev) / PostgreSQL (production)
- **Authentication:** Django Allauth (Google/GitHub OAuth) + Custom OTP
- **Real-time:** Django Channels with Redis/In-Memory Layer
- **Email:** Brevo/ZeptoMail backends
- **Deployment:** Render/Railway

---

## Architecture Overview

### Core Components

```
auth_project/
├── auth_project/          # Main project configuration
│   ├── settings.py        # Django configuration
│   ├── urls.py            # Root URL routing
│   └── wsgi.py            # WSGI entry point
├── accounts/              # Main application
│   ├── models.py          # Database models
│   ├── views.py           # View logic
│   ├── serializers.py     # DRF serializers
│   ├── consumers.py       # WebSocket consumers
│   ├── urls.py            # App-level routing
│   ├── routing.py         # WebSocket routing
│   └── forms.py           # Form definitions
└── manage.py              # Django CLI
```

---

## Data Models

### 1. **StudentProfile** (Extended User Model)
Located: `accounts/models.py:12-53`

```python
class StudentProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    full_name, college, location, bio
    profile_photo (ImageField)
    skills, interests, project_interests (JSONField arrays)
    github, linkedin, portfolio, behance (URL fields)
    profile_completed (BooleanField)
    created_at, updated_at (DateTimeField)
```

**Purpose:** Extends Django's built-in User model with academic/professional details.

---

### 2. **OTP** (One-Time Password)
Located: `accounts/models.py:55-124`

```python
class OTP(models.Model):
    PURPOSE_CHOICES = ['login', 'registration', 'reset']
    
    email = models.EmailField()
    otp_code = models.CharField(max_length=6)  # 6-digit OTP
    purpose = models.CharField(choices=PURPOSE_CHOICES)
    is_used = models.BooleanField(default=False)
    created_at, expires_at (DateTimeField)
    
    Methods:
    - is_valid(): Check if OTP is not expired
    - verify_otp(otp_code): Validate OTP
    - generate_otp(email, purpose): Create new OTP (5-min expiry)
    - hash_otp(otp_code): SHA-256 hashing
```

**Purpose:** Secure email-based authentication and password reset.

---

### 3. **Connection** (User Relationships)
Located: `accounts/models.py:126-147`

```python
class Connection(models.Model):
    STATUS_CHOICES = ['pending', 'accepted', 'rejected']
    
    sender, receiver (ForeignKey to User)
    status, created_at, updated_at
    
    Constraint: unique_together['sender', 'receiver']
```

**Purpose:** Track collaboration requests and connections between students.

---

### 4. **Message** (Direct Messaging)
Located: `accounts/models.py:149-217`

```python
class Message(models.Model):
    MESSAGE_TYPES = ['text', 'file', 'image', 'call']
    
    sender, receiver (ForeignKey)
    chat_room (ForeignKey to ChatRoom, optional for group chats)
    content = models.TextField()
    message_type, call_type
    reply_to (Self-referential FK for threading)
    created_at, updated_at
    
    Methods:
    - mark_as_read_by(user): Update MessageReadStatus
    - is_read_by(user): Check read status
    - get_read_by_users(): Get list of readers
    - get_unread_users(): Get non-readers (groups)
```

**Purpose:** Direct & group messaging with read receipts.

---

### 5. **MessageReadStatus** (Scalable Read Tracking)
Located: `accounts/models.py` (referenced)

**Purpose:** Separate model to handle message read status without loading full recipient list.

---

### 6. **ChatRoom** (Group Chats)
Located: `accounts/models.py` (line ~300+)

```python
class ChatRoom(models.Model):
    CHAT_TYPES = ['direct', 'group', 'project']
    
    name, description
    chat_type, created_at, updated_at
    created_by (ForeignKey to User)
    members (M2M to ChatRoomMember)
```

**Purpose:** Support both direct and group messaging.

---

### 7. **Project** (Core Feature)
Located: `accounts/models.py` (~250-380 lines)

```python
class Project(models.Model):
    STATUS_CHOICES = ['active', 'completed', 'paused']
    VISIBILITY = ['public', 'private', 'draft']
    
    user (Owner)
    title, description, category
    collaboration_needs (JSONField - skills required)
    current_members, required_members
    logo, banner_image
    github_link, live_url
    is_active, is_public
    created_at, updated_at
    
    Methods:
    - get_team_members(): Fetch ProjectMember
    - add_member(user, role): Add team member
    - remove_member(user): Remove from team
    - get_like_count(), get_comment_count()
```

**Purpose:** Central project management with team coordination.

---

### 8. **Comment** (Project Discussions)
Located: `accounts/models.py` (~380-420)

```python
class Comment(models.Model):
    project (ForeignKey)
    user, content, created_at, updated_at
    likes_count, replies_count
```

**Purpose:** Allow discussions on projects.

---

### 9. **Like** (Project Engagement)
Located: `accounts/models.py` (~420-450)

```python
class Like(models.Model):
    project (ForeignKey)
    user (ForeignKey)
    created_at
    
    Constraint: unique_together['project', 'user']
```

**Purpose:** Track project popularity.

---

### 10. **Activity** (User Activity Feed)
Located: `accounts/models.py:475-508`

```python
class Activity(models.Model):
    ACTIVITY_TYPES = [
        'profile_updated', 'project_created', 'project_liked',
        'connection_made', 'message_sent', 'comment_added',
        'user_followed', 'task_completed', 'milestone_completed'
    ]
    
    user, activity_type, title, description
    project, target_user, connection (optional relations)
    is_public, created_at
```

**Purpose:** Real-time activity feed for dashboard.

---

### 11. **UserStats** (Dashboard Metrics)
Located: `accounts/models.py:510-540`

```python
class UserStats(models.Model):
    user (OneToOneField)
    projects_created, connections_made, likes_received
    comments_made, projects_joined, tasks_completed
    followers_count, following_count
    last_updated
    
    Method: update_stats() - Aggregate counts from related models
```

**Purpose:** Cache user metrics for dashboard performance.

---

### 12. **ProjectMember** (Team Management)
Located: `accounts/models.py:542-580`

```python
class ProjectMember(models.Model):
    ROLES = ['owner', 'admin', 'contributor', 'viewer']
    
    project, user (ForeignKeys)
    role, is_active
    joined_at
    
    Properties:
    - can_manage_project: owner/admin
    - can_invite_members: owner/admin
    - can_manage_tasks: owner/admin/contributor
    - can_edit_project: owner/admin/contributor
```

**Purpose:** Role-based project access control.

---

### 13. **ProjectTask** (Task Management)
Located: `accounts/models.py:636-678`

```python
class ProjectTask(models.Model):
    STATUS = ['todo', 'in_progress', 'review', 'completed', 'cancelled']
    PRIORITY = ['low', 'medium', 'high', 'urgent']
    
    project, title, description
    assigned_to, assigned_by
    status, priority, due_date
    completed_at, created_at, updated_at
    
    Method: mark_completed() - Update status and timestamp
```

**Purpose:** Task tracking within projects.

---

### 14. **ProjectMilestone** (Progress Tracking)
Located: `accounts/models.py:680-708`

```python
class ProjectMilestone(models.Model):
    project, title, description
    due_date, is_completed, completed_at
    completed_by (ForeignKey to User)
    
    Method: mark_completed(user) - Update completion status
```

**Purpose:** Track project progress milestones.

---

## Views Layer

### Authentication Views
Located: `accounts/views.py:201-370`

```python
def login_view(request):
    """Email-based OTP login"""
    1. Validate email
    2. Generate OTP via OTP.generate_otp()
    3. Send OTP email (via Brevo/ZeptoMail)
    4. Render OTP verification form

def verify_otp_view(request):
    """Verify OTP and create session"""
    1. Get OTP from form
    2. Validate via OTP.verify_otp()
    3. Authenticate user
    4. Create session + redirect to dashboard

def register_view(request):
    """New user registration"""
    1. Create StudentProfile
    2. Generate OTP for verification
    3. Send verification email
    4. Redirect to OTP verification
```

### Dashboard & Profile Views
Located: `accounts/views.py:65-88, 50-62`

```python
def dashboard_view(request):
    """Main dashboard with activity feed"""
    - Fetch user's projects
    - Get recent activities
    - Count unread messages/notifications
    - Render dashboard template

def edit_profile(request):
    """Edit profile and upload avatar"""
    - Handle StudentProfileForm
    - Process file upload to profile_photos/
    - Update StudentProfile model
    - Redirect to profile view

def student_profile(request, username):
    """View user profile (public)"""
    - Fetch StudentProfile by username
    - Get user's projects
    - Show connection status
    - Render profile template
```

### Project Management Views
Located: `accounts/views.py` (various)

```python
def create_project(request):
    """Create new project"""
    - Handle ProjectForm POST
    - Create Project instance (owner=request.user)
    - Redirect to project detail

def project_detail(request, project_id):
    """View project details + comments"""
    - Fetch Project by ID
    - Get ProjectMembers
    - Get Comments ordered by -created_at
    - Check if user can edit (owner check)
    - Count likes

def search_projects(request):
    """Search/filter projects"""
    - Get 'q' parameter
    - Filter by title, description, collaboration_needs
    - Return paginated results

def project_feed(request):
    """Main projects feed"""
    - Fetch all public projects
    - Apply ProjectVisibilityFilter
    - Paginate (10 per page)
    - Render feed template
```

### API Views
Located: `accounts/views.py` (REST endpoints)

```python
class UserProfileView(generics.RetrieveUpdateAPIView):
    """Get/Update user profile (DRF)"""
    serializer_class = UserProfileSerializer
    permission_classes = [IsAuthenticated]

class ProjectListView(generics.ListCreateAPIView):
    """Get all projects or create new"""
    queryset = Project.objects.all()

class CommentListView(generics.ListCreateAPIView):
    """Get/post comments on project"""
    queryset = Comment.objects.all()
```

---

## WebSocket Consumers (Real-Time)

Located: `accounts/consumers.py`

### 1. **ProjectUpdateConsumer** (Project Activity)
Lines: 16-274

```python
class ProjectUpdateConsumer(AsyncWebsocketConsumer):
    Routes: ws://localhost:8000/ws/project/<project_id>/
    
    async def connect():
        - Join group: f'project_{project_id}'
        - Send initial project data
        - Log connection
    
    async def receive(text_data):
        Messages:
        - 'status.update': Handle project status change
        - 'member.add': Add new team member
        - 'comment.post': Post new comment
    
    async def project_status_update(event):
        - Broadcast status change to all connected clients
    
    async def project_member_added(event):
        - Notify all: new member joined
    
    async def project_comment_posted(event):
        - Notify all: new comment posted
    
    @database_sync_to_async
    async def handle_status_update(new_status):
        - Verify user is project owner
        - Create Activity log
        - Broadcast via group_send()
    
    @database_sync_to_async
    async def handle_member_add(user_id):
        - Verify permission (owner only)
        - Create ProjectMember
        - Broadcast member addition
    
    @database_sync_to_async
    async def handle_new_comment(comment_text):
        - Create Comment in DB
        - Broadcast to all clients
```

**Key Event Format:**
```json
{
    "type": "project.status_update",
    "status": "completed",
    "changed_by": "username",
    "timestamp": "2026-02-08T10:30:00Z",
    "message": "Project status changed to completed"
}
```

---

### 2. **ActivityFeedConsumer** (Real-Time Feed)
Lines: 276-336

```python
class ActivityFeedConsumer(AsyncWebsocketConsumer):
    Routes: ws://localhost:8000/ws/activity-feed/
    
    async def connect():
        - Join: f'activity_feed_{user.id}'
        - Log connection
    
    async def activity_notification(event):
        - Broadcast activity to user's connected clients
        - Include activity type, project, actor, timestamp
        - Add emoji icon based on activity type
    
    get_activity_icon(activity_type):
        Maps: project.created → 🚀, member.added → 👥, etc.
```

---

### 3. **NotificationConsumer** (Real-Time Alerts)
Lines: 338-434

```python
class NotificationConsumer(AsyncWebsocketConsumer):
    Routes: ws://localhost:8000/ws/notifications/
    
    async def connect():
        - Join: f'notifications_{user.id}'
        - Send unread_count
    
    async def receive(text_data):
        - Handle 'mark_read' to update Notification model
    
    async def send_notification(event):
        - Send notification with title, message, type
        - Include sound flag for browser notification
    
    @database_sync_to_async
    get_unread_count():
        - Count Notification.is_read==False
    
    @database_sync_to_async
    mark_notification_read(notification_id):
        - Update Notification.is_read = True
```

---

## WebSocket Configuration

Located: `accounts/routing.py`

```python
websocket_urlpatterns = [
    path("ws/project/<int:project_id>/", ProjectUpdateConsumer.as_asgi()),
    path("ws/activity-feed/", ActivityFeedConsumer.as_asgi()),
    path("ws/notifications/", NotificationConsumer.as_asgi()),
]
```

Located: `auth_project/settings.py` (line 60+)

```python
INSTALLED_APPS = [
    'channels',  # WebSocket support
    'rest_framework',
    'allauth',
    'accounts',
]

ASGI_APPLICATION = 'auth_project.asgi.application'

CHANNEL_LAYERS = {
    'default': {
        'BACKEND': 'channels_redis.core.RedisChannelLayer',
        'CONFIG': {
            "hosts": [('redis-server', 6379)],  # or localhost:6379
        },
    }
}
```

---

## Authentication Flow

### OTP Login Process

```
1. User visits /login/
2. Enters email → POST to login_view()
3. login_view():
   - OTP.generate_otp(email, 'login')
   - Sends OTP email via email_backend
   - Renders OTP verification form
4. User enters OTP → POST to verify_otp_view()
5. verify_otp_view():
   - OTP.verify_otp(otp_code)
   - authenticate(username=email)
   - login(request, user)
   - Redirect to dashboard
```

### OAuth Login (Google/GitHub)

```
1. User clicks "Login with Google"
2. Redirects to: /accounts/google/login/
3. Django Allauth handles:
   - OAuth flow to provider
   - Exchanges code for token
   - Fetches user info
   - Creates/updates User + SocialAccount
4. Creates StudentProfile if new user
5. Redirect to dashboard
```

---

## REST API Endpoints

### User Profile APIs

| Endpoint | Method | Purpose |
|----------|--------|---------|
| `/api/user/profile/` | GET | Fetch current user profile |
| `/api/user/profile/` | PUT | Update profile |
| `/api/user/<username>/` | GET | View user public profile |
| `/api/user/<username>/projects/` | GET | Get user's projects |
| `/api/user/<username>/connections/` | GET | Get connections |

### Project APIs

| Endpoint | Method | Purpose |
|----------|--------|---------|
| `/api/projects/` | GET | List all projects |
| `/api/projects/` | POST | Create project |
| `/api/projects/<id>/` | GET | Project details |
| `/api/projects/<id>/` | PUT | Update project |
| `/api/projects/<id>/members/` | GET | Team members |
| `/api/projects/<id>/members/` | POST | Add member |
| `/api/projects/<id>/comments/` | GET | Comments |
| `/api/projects/<id>/comments/` | POST | Post comment |
| `/api/projects/<id>/like/` | POST | Like project |
| `/api/projects/<id>/unlike/` | POST | Unlike project |

### Message APIs

| Endpoint | Method | Purpose |
|----------|--------|---------|
| `/api/messages/` | GET | List conversations |
| `/api/messages/<user_id>/` | GET | Conversation thread |
| `/api/messages/send/` | POST | Send message |
| `/api/messages/<id>/read/` | POST | Mark as read |

### Notification APIs

| Endpoint | Method | Purpose |
|----------|--------|---------|
| `/api/notifications/` | GET | List notifications |
| `/api/notifications/<id>/read/` | POST | Mark as read |
| `/api/notifications/count/` | GET | Unread count |

---

## Email Notification System

### Supported Backends

1. **Brevo (Sendinblue)**
   - Located: `accounts/brevo_mail_backend.py`
   - Uses: `sib_api_v3_sdk` (Brevo Python SDK)

2. **ZeptoMail**
   - Located: `accounts/zepto_mail_backend.py`
   - Uses: Direct HTTP requests to ZeptoMail API

### Email Templates

```
OTP_EMAIL: "Your OTP: {otp_code}"
WELCOME_EMAIL: "Welcome to UniSync!"
PROJECT_INVITE: "You've been invited to project: {project_name}"
COMMENT_MENTION: "@{username} mentioned you in a comment"
CONNECTION_REQUEST: "{user} sent you a connection request"
```

---

## Project Visibility & Filtering

Located: `accounts/utils.py` (ProjectVisibilityFilter)

```python
class ProjectVisibilityFilter:
    """Filter projects based on visibility rules"""
    
    def get_visible_projects(user):
        if user.is_authenticated:
            # User sees: public + private (if owner) + draft (if owner)
            public = Project.objects.filter(is_public=True)
            own = Project.objects.filter(user=user)
            return (public | own).distinct()
        else:
            # Anonymous users see only public projects
            return Project.objects.filter(is_public=True)
```

---

## Caching Strategy

Located: `auth_project/settings.py`

```python
CACHES = {
    'default': {
        'BACKEND': 'django.core.cache.backends.redis.RedisCache',
        'LOCATION': 'redis://127.0.0.1:6379/1',
        'OPTIONS': {
            'CLIENT_CLASS': 'redis.Redis',
        }
    }
}

Cache Keys:
- user_stats:{user_id}: UserStats aggregates
- project_{id}_members: Project team members
- user_notifications:{user_id}: Notification count
- activity_feed_{user_id}: Activity feed
```

---

## Performance Optimizations

### 1. **Database Query Optimization**
- Use `select_related()` for foreign keys
- Use `prefetch_related()` for M2M/reverse FKs
- Add database indexes on frequently queried fields

### 2. **Caching**
- Cache UserStats (updated on activity)
- Cache project member lists
- Cache notification counts

### 3. **Pagination**
- All list views use Paginator (10 items/page)
- Reduces initial page load

### 4. **Message Read Status**
- Separate MessageReadStatus model (scalable)
- Avoids loading full recipient list for each message

### 5. **Activity Feed**
- Stored in Activity model (not calculated)
- Indexed by user + created_at
- Signals trigger Activity creation

---

## Signals & Real-Time Triggers

Located: `accounts/signals_realtime.py`

```python
@receiver(post_save, sender=Project)
def on_project_created(sender, instance, created, **kwargs):
    if created:
        # Create Activity log
        Activity.objects.create(
            user=instance.user,
            activity_type='project_created',
            title=f"Created project '{instance.title}'",
            project=instance
        )
        # Broadcast to activity feed consumers
        async_to_sync(channel_layer.group_send)(
            f'activity_feed_{instance.user.id}',
            {'type': 'activity.notification', ...}
        )

@receiver(post_save, sender=Comment)
def on_comment_posted(sender, instance, created, **kwargs):
    if created:
        # Broadcast to project consumers
        async_to_sync(channel_layer.group_send)(
            f'project_{instance.project.id}',
            {'type': 'project.comment_posted', ...}
        )

@receiver(post_save, sender=Like)
def on_project_liked(sender, instance, created, **kwargs):
    if created:
        # Update Activity, broadcast
        ...
```

---

## Frontend Integration

### JavaScript WebSocket Client

```javascript
// Connect to project updates
let socket = new WebSocket("ws://localhost:8000/ws/project/2/");

socket.onopen = () => console.log("✅ WORKING!");

socket.onmessage = (event) => {
    const data = JSON.parse(event.data);
    
    if (data.type === 'project.comment_posted') {
        // Add comment to DOM
        appendCommentToFeed(data);
    } else if (data.type === 'project.member_added') {
        // Update member list
        refreshMemberList(data.user_id);
    } else if (data.type === 'project.status_update') {
        // Update project status
        updateProjectStatus(data.status);
    }
};

socket.onerror = (error) => console.error("WebSocket error:", error);

socket.onclose = () => console.log("Connection closed");

// Send message to server
function postComment(text) {
    socket.send(JSON.stringify({
        type: 'comment.post',
        text: text
    }));
}
```

### Activity Feed JavaScript

```javascript
const activitySocket = new WebSocket("ws://localhost:8000/ws/activity-feed/");

activitySocket.onmessage = (event) => {
    const activity = JSON.parse(event.data);
    
    // Create notification badge
    const notification = `
        ${activity.icon} ${activity.action}
        ${activity.project_title}
        by ${activity.actor}
    `;
    
    // Add to top of feed
    insertActivityToFeed(notification);
    
    // Play sound
    if (!document.hidden) playNotificationSound();
};
```

### Notification WebSocket

```javascript
const notificationSocket = new WebSocket("ws://localhost:8000/ws/notifications/");

notificationSocket.onmessage = (event) => {
    const notification = JSON.parse(event.data);
    
    // Update badge count
    document.querySelector('.notification-badge').textContent = 
        notification.unread_count;
    
    // Show browser notification
    if (Notification.permission === 'granted') {
        new Notification(notification.title, {
            body: notification.message,
            icon: '/static/logo.png',
            tag: notification.notification_id
        });
    }
    
    // Mark as read when clicked
    document.addEventListener('click', (e) => {
        if (e.target.matches('.notification-item')) {
            notificationSocket.send(JSON.stringify({
                type: 'mark_read',
                notification_id: notification.notification_id
            }));
        }
    });
};
```

---

## Testing Coverage

Located: `auth_project/test_*.py`

- `test_login.py`: OTP login flow
- `test_profile_view.py`: Profile viewing/editing
- `test_comments_api.py`: Comment CRUD
- `test_email.py`: Email sending via backends
- `test_connections.py`: Connection requests
- `test_feed_fix.py`: Activity feed
- `test_filter.py`: Project filtering

---

## Known Issues & Fixes Applied

### 1. **Project Owner AttributeError**
- Issue: `project.owner` doesn't exist
- Fix: Use `project.user` instead (FK to User)

### 2. **CSRF Token Issues**
- Issue: POST requests returning 403
- Fix: Include `{% csrf_token %}` in forms

### 3. **WebSocket Connection Errors**
- Issue: Consumer not accepting connections
- Fix: Ensure `channels` installed + ASGI configured

### 4. **Message Read Status**
- Issue: Querying full message list slow
- Fix: Use separate MessageReadStatus model

### 5. **Email Backend Failures**
- Issue: OTP emails not sending
- Fix: Switch between Brevo/ZeptoMail backends

---

## Deployment Configuration

### Settings for Production

```python
# settings.py
DEBUG = False
ALLOWED_HOSTS = ['yourdomain.com', 'www.yourdomain.com']
SECURE_SSL_REDIRECT = True
SESSION_COOKIE_SECURE = True
CSRF_COOKIE_SECURE = True

# Redis Channel Layer (for WebSockets)
CHANNEL_LAYERS = {
    'default': {
        'BACKEND': 'channels_redis.core.RedisChannelLayer',
        'CONFIG': {
            "hosts": [('redis-server', 6379)],
        },
    }
}

# PostgreSQL Database
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': os.getenv('DB_NAME'),
        'USER': os.getenv('DB_USER'),
        'PASSWORD': os.getenv('DB_PASSWORD'),
        'HOST': os.getenv('DB_HOST'),
        'PORT': 5432,
    }
}
```

### Procfile (Render/Railway)

```procfile
web: gunicorn auth_project.wsgi
worker: python manage.py runworker project_update activity_feed notifications
```

---

## Key Code Patterns

### 1. **Django View Pattern**
```python
@login_required
def feature_view(request, object_id):
    obj = get_object_or_404(Model, id=object_id)
    
    if request.method == 'POST':
        form = MyForm(request.POST, instance=obj)
        if form.is_valid():
            form.save()
            messages.success(request, 'Saved!')
            return redirect('next_view')
    else:
        form = MyForm(instance=obj)
    
    return render(request, 'template.html', {'form': form, 'obj': obj})
```

### 2. **DRF APIView Pattern**
```python
class MyAPIView(generics.ListCreateAPIView):
    queryset = Model.objects.all()
    serializer_class = MySerializer
    permission_classes = [IsAuthenticated]
    
    def perform_create(self, serializer):
        serializer.save(user=self.request.user)
```

### 3. **WebSocket Consumer Pattern**
```python
async def receive(self, text_data):
    data = json.loads(text_data)
    
    if data['type'] == 'action':
        result = await self.handle_action(data)
        await self.channel_layer.group_send(
            self.group_name,
            {'type': 'action.result', 'data': result}
        )

async def action_result(self, event):
    await self.send(text_data=json.dumps(event))
```

### 4. **Signal Handler Pattern**
```python
@receiver(post_save, sender=MyModel)
def on_model_saved(sender, instance, created, **kwargs):
    if created:
        # Handle creation
        Task.objects.create(related=instance)
    
    # Broadcast real-time update
    async_to_sync(channel_layer.group_send)(
        'group_name',
        {'type': 'event.type', 'data': {...}}
    )
```

---

## Summary Table: Component Interaction

| Component | Communicates With | Purpose |
|-----------|-------------------|---------|
| **StudentProfile** | User, Project | Extended user data |
| **OTP** | Email Backend | Authentication |
| **Project** | ProjectMember, Comment, Like, Activity | Core feature |
| **Message** | ChatRoom, MessageReadStatus | Messaging |
| **Activity** | Signals, Consumers | Real-time feed |
| **Consumers** | Channel Layer, Database | WebSocket handling |
| **Signals** | Consumers, Cache | Trigger updates |
| **Email Backend** | OTP, Notification | Notifications |
| **Allauth** | OAuth Providers | Social login |
| **DRF** | Serializers, Permissions | REST API |

---

## Common Development Tasks

### Add New Feature (e.g., Skill Endorsements)

1. **Create Model** in `models.py`:
```python
class SkillEndorsement(models.Model):
    skill = models.CharField(max_length=100)
    endorsed_by = models.ForeignKey(User, related_name='endorsements_given')
    endorsed_for = models.ForeignKey(User, related_name='endorsements_received')
    created_at = models.DateTimeField(auto_now_add=True)
    class Meta:
        unique_together = ['skill', 'endorsed_by', 'endorsed_for']
```

2. **Create Serializer** in `serializers.py`:
```python
class SkillEndorsementSerializer(serializers.ModelSerializer):
    class Meta:
        model = SkillEndorsement
        fields = ['id', 'skill', 'endorsed_by', 'created_at']
```

3. **Create View** in `views.py`:
```python
class SkillEndorsementView(generics.CreateAPIView):
    serializer_class = SkillEndorsementSerializer
    permission_classes = [IsAuthenticated]
    
    def perform_create(self, serializer):
        serializer.save(endorsed_by=self.request.user)
```

4. **Add URL** in `urls.py`:
```python
path('api/endorsements/', SkillEndorsementView.as_view()),
```

5. **Create Signal** in `signals_realtime.py`:
```python
@receiver(post_save, sender=SkillEndorsement)
def on_skill_endorsed(sender, instance, created, **kwargs):
    if created:
        Activity.objects.create(
            user=instance.endorsed_by,
            activity_type='skill_endorsed',
            target_user=instance.endorsed_for,
            title=f"Endorsed {instance.endorsed_for.username} for {instance.skill}"
        )
```

---

## Next Steps / Improvements

1. **Add Search Filters**: Filter projects by skills, interests
2. **Implement Notifications UI**: Dashboard notification center
3. **Add File Upload**: Share documents in project
4. **Rate Limiting**: Prevent spam on APIs
5. **Audit Logging**: Track data changes
6. **Email Verification**: Verify email on signup
7. **Two-Factor Auth**: Optional TOTP
8. **Project Analytics**: Views, engagement metrics
9. **Advanced Search**: Elasticsearch integration
10. **Mobile App**: React Native or Flutter

---

**Generated:** 2026-02-08 | **Version:** 1.0
