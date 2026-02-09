# UniSinq - Comprehensive Code Analysis (2026)

## Executive Summary

**UniSinq** (formerly UniSync) is a full-stack collaboration platform built with **Django**, **Django REST Framework**, and **Django Channels** for real-time WebSocket communication. The application enables students to post projects, find collaborators, engage via comments, and communicate through messaging systems.

**Tech Stack:**
- **Backend**: Django 3.2+, Django REST Framework, Django Channels
- **Frontend**: HTML5, CSS3, JavaScript (Vanilla + jQuery)
- **Database**: PostgreSQL (production), SQLite (development)
- **Real-time**: Redis + WebSocket (Django Channels)
- **Authentication**: Email OTP, Google OAuth 2.0, GitHub OAuth
- **Email**: Brevo (formerly Sendinblue), Zepto Mail

---

## Architecture Overview

### System Diagram

```
┌─────────────────────────────────────────────────────────────────┐
│                     Frontend (Browser)                           │
│  - HTML Templates (Jinja2)                                       │
│  - JavaScript (WebSocket, AJAX, REST API calls)                  │
│  - CSS Styling, Bootstrap Components                             │
└──────────────────┬──────────────────────────────────────────────┘
                   │ HTTP/WebSocket
┌──────────────────▼──────────────────────────────────────────────┐
│                    Django Application                            │
├─────────────────────────────────────────────────────────────────┤
│ URL Router (urls.py)                                             │
│ ├─ Standard Views (views.py) → HTML Responses                   │
│ ├─ REST API (DRF) → JSON Responses                              │
│ └─ WebSocket Routes (routing.py) → Real-time                    │
├─────────────────────────────────────────────────────────────────┤
│ Middleware Layer                                                 │
│ ├─ Authentication (JWT, Session, OAuth)                         │
│ ├─ CSRF Protection                                              │
│ └─ CORS Headers                                                 │
├─────────────────────────────────────────────────────────────────┤
│ Business Logic                                                   │
│ ├─ Views & ViewSets (accounts/views.py)                         │
│ ├─ Serializers (serializers.py)                                 │
│ ├─ Permissions (permissions.py)                                 │
│ └─ Utilities (utils.py)                                         │
├─────────────────────────────────────────────────────────────────┤
│ Real-time Layer (Channels/ASGI)                                 │
│ ├─ WebSocket Consumers (consumers.py)                           │
│ ├─ Redis Channel Layer                                          │
│ └─ Group Broadcasting                                           │
├─────────────────────────────────────────────────────────────────┤
│ Data Models (ORM)                                               │
│ ├─ User, StudentProfile, OTP                                    │
│ ├─ Project, Comment, Activity                                   │
│ ├─ Connection, Message, Notification                            │
│ └─ Like, Follow, ProjectTeam                                    │
├─────────────────────────────────────────────────────────────────┤
│ External Services                                               │
│ ├─ Email Services (Brevo, Zepto)                                │
│ ├─ OAuth Providers (Google, GitHub)                             │
│ └─ Storage (S3, Local Media)                                    │
└──────────────────┬──────────────────────────────────────────────┘
                   │
        ┌──────────┼──────────┐
        │          │          │
    ┌───▼────┐ ┌──▼───┐  ┌──▼──────┐
    │ Redis  │ │ DB   │  │  Files  │
    │ Cache  │ │ PG   │  │  Media  │
    └────────┘ └──────┘  └─────────┘
```

---

## Core Components

### 1. Models (accounts/models.py)

#### 1.1 User & Profile Management

**StudentProfile** (Lines 12-53)
```python
class StudentProfile(models.Model):
    user = models.OneToOneField(User)
    full_name = CharField(max_length=100)
    college = CharField(max_length=200)
    bio = TextField()
    profile_photo = ImageField(validators=[jpg/png/gif])
    skills = JSONField(default=list)  # ["Python", "Django", "React"]
    project_interests = JSONField()
    role_preference = CharField()  # Developer, Designer, Manager
    
    # Social Links
    github = URLField()
    linkedin = URLField()
    portfolio = URLField()
    behance = URLField()
    
    profile_completed = BooleanField()
    created_at = DateTimeField(auto_now_add=True)
    updated_at = DateTimeField(auto_now=True)
```

**OTP** (Lines 55-125)
```python
class OTP(models.Model):
    email = EmailField()
    otp_code = CharField(max_length=6)  # "123456"
    purpose = CharField(choices=['login', 'registration', 'reset'])
    is_used = BooleanField(default=False)
    created_at = DateTimeField()
    expires_at = DateTimeField()  # Current time + 10 minutes
    
    Methods:
    - is_valid() → checks expiration and usage
    - verify_otp(code) → validates and marks as used
    - generate_otp(email, purpose) → creates new OTP
```

#### 1.2 Project & Engagement

**Project** (Lines 202+)
```python
class Project(models.Model):
    owner = ForeignKey(User)
    title = CharField(max_length=200)
    description = TextField()
    collaboration_needs = TextField()  # "Looking for Backend developer"
    skills_required = JSONField()
    
    # Visibility Control
    visibility = CharField(choices=['public', 'private', 'friends-only'])
    is_archived = BooleanField(default=False)
    
    # Engagement
    created_at = DateTimeField()
    updated_at = DateTimeField()
    
    # Many-to-Many
    team_members = ManyToManyField(User, through=ProjectTeamMember)
    liked_by = ManyToManyField(User, through=Like)
```

**Comment** (Lines 300+)
```python
class Comment(models.Model):
    project = ForeignKey(Project)
    author = ForeignKey(User)
    text = TextField()
    created_at = DateTimeField()
    updated_at = DateTimeField()
    
    # Nested comments
    parent_comment = ForeignKey(self, null=True, blank=True)
```

**Activity & Notification**
```python
class Activity(models.Model):
    user = ForeignKey(User)
    action_type = CharField()  # "liked_project", "commented", "connected"
    content_type = GenericForeignKey()
    created_at = DateTimeField()

class Notification(models.Model):
    recipient = ForeignKey(User)
    sender = ForeignKey(User)
    notification_type = CharField()
    read = BooleanField(default=False)
    created_at = DateTimeField()
```

#### 1.3 Networking & Messaging

**Connection** (Lines 126-200)
```python
class Connection(models.Model):
    from_user = ForeignKey(User)
    to_user = ForeignKey(User)
    status = CharField(choices=['pending', 'accepted', 'blocked'])
    created_at = DateTimeField()
    accepted_at = DateTimeField(null=True)
```

**Message & Chat**
```python
class ChatRoom(models.Model):
    name = CharField()
    participants = ManyToManyField(User)
    created_at = DateTimeField()
    is_group = BooleanField()

class Message(models.Model):
    chat_room = ForeignKey(ChatRoom)
    sender = ForeignKey(User)
    text = TextField()
    created_at = DateTimeField()
    read_by = ManyToManyField(User, through=MessageReadStatus)
```

---

### 2. Views & API Endpoints (accounts/views.py)

#### 2.1 Authentication Views

**Register & Login Flow**
```python
def register(request):
    # POST: Create user account
    # 1. Validate email (unique)
    # 2. Generate OTP and send via email
    # 3. Redirect to OTP verification
    # Returns: HTML form or JSON

def verify_otp(request):
    # POST: Verify OTP
    # 1. Check OTP validity & expiration
    # 2. If valid: mark as used, create user account
    # 3. Authenticate user session
    # Returns: Redirect to dashboard or JSON token

def login_view(request):
    # GET: Show login form
    # POST: Send OTP to email
    # 1. Check if user exists
    # 2. Generate OTP
    # 3. Send email with OTP code
    # Returns: Redirect to OTP verification
```

#### 2.2 Project Management

**Project CRUD**
```python
@login_required
def create_project(request):
    # POST: Create new project
    # Params: title, description, collaboration_needs, visibility
    # 1. Validate form
    # 2. Save to database (owner = request.user)
    # 3. Create Activity log
    # 4. Broadcast via WebSocket to activity feed
    # Returns: Redirect to project detail

@login_required
def edit_project(request, project_id):
    # GET: Show edit form
    # POST: Update project
    # Permission: Check if user is project owner
    # Returns: Update + Broadcast

@login_required
def delete_project(request, project_id):
    # POST: Archive project
    # Permission: Only owner or admin
    # Returns: Redirect to dashboard
```

**Project Filtering & Search**
```python
def project_feed(request):
    # GET: List projects with pagination
    # Filters: 
    #   - visibility (public/friends-only)
    #   - skills_required (match user skills)
    #   - collaboration_needs (text search)
    # Sort: newest first
    # Pagination: 10 per page
    # Returns: HTML + paginator OR JSON list

def search_projects(request):
    # GET: Search by title/description/needs
    # Query: q = "Python backend"
    # Returns: Filtered project list
```

#### 2.3 Engagement & Real-time

**Comments API**
```python
class CommentViewSet(viewsets.ModelViewSet):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer
    permission_classes = [IsAuthenticated]
    
    # POST /api/comments/
    # Create new comment on project
    # Broadcast: WebSocket → project_id group
    # Notify: Project owner + comment authors
    
    # PATCH /api/comments/{id}/
    # Edit comment (author only)
    
    # DELETE /api/comments/{id}/
    # Delete comment (author/owner/admin)
```

**Like & Unlike**
```python
def like_project(request, project_id):
    # POST: Add like
    # 1. Check if already liked
    # 2. Create Like record
    # 3. Increment like_count
    # 4. Broadcast: WebSocket notification
    # Returns: JSON {liked: true, count: 5}

def unlike_project(request, project_id):
    # POST: Remove like
    # 1. Delete Like record
    # 2. Decrement like_count
    # 3. Broadcast: WebSocket notification
    # Returns: JSON {liked: false, count: 4}
```

**Connections (Networking)**
```python
def send_connection_request(request, user_id):
    # POST: Send connection request
    # 1. Check if already connected/requested
    # 2. Create Connection(status='pending')
    # 3. Send notification email to target user
    # 4. Broadcast: WebSocket notification
    # Returns: JSON {status: 'pending'}

def accept_connection(request, connection_id):
    # POST: Accept connection
    # 1. Check if recipient
    # 2. Update status to 'accepted'
    # 3. Notify sender
    # 4. Broadcast: Real-time update
    # Returns: JSON {status: 'accepted'}
```

#### 2.4 Profile & User Management

**Student Profile**
```python
@login_required
def edit_profile(request):
    # GET: Show profile edit form
    # POST: Update StudentProfile
    # Fields: 
    #   - full_name, bio, college
    #   - skills (multiselect)
    #   - profile_photo (image upload)
    #   - social links (GitHub, LinkedIn, etc.)
    # 1. Validate form & image size
    # 2. Save to StudentProfile
    # 3. Mark profile_completed = True
    # Returns: Redirect to profile view

def view_profile(request, username):
    # GET: Display user profile
    # 1. Get StudentProfile for username
    # 2. Fetch user's projects
    # 3. Count connections, projects, likes
    # 4. Show "Connect" button if not connected
    # Returns: HTML profile page
```

---

### 3. Real-time Layer (accounts/consumers.py)

#### 3.1 WebSocket Architecture

**ProjectUpdateConsumer** (Lines 16-337)
```python
class ProjectUpdateConsumer(AsyncWebsocketConsumer):
    """
    Handles real-time project updates
    WebSocket URL: ws://localhost:8000/ws/project/{project_id}/
    """
    
    async def connect(self):
        # 1. Extract project_id from URL route
        # 2. Create group name: f'project_{project_id}'
        # 3. Join group via Redis channel layer
        # 4. Accept WebSocket connection
        # 5. Send initial project data to client
        # 6. Log connection
    
    async def disconnect(self, close_code):
        # 1. Remove from project group
        # 2. Broadcast "user left" to other clients
        # 3. Log disconnection
    
    async def receive(self, text_data):
        # Parse JSON message
        # Route by message type:
        # - 'status.update': Update project status
        # - 'member.add': Add team member
        # - 'comment.post': New comment
        # - 'like.toggle': Like/unlike
```

**Message Types & Broadcasting**

```python
# 1. Project Status Update
await channel_layer.group_send(
    f'project_{project_id}',
    {
        'type': 'project.status_update',
        'status': 'in_progress',
        'updated_by': username,
        'timestamp': now.isoformat()
    }
)

# 2. New Comment
await channel_layer.group_send(
    f'project_{project_id}',
    {
        'type': 'comment.created',
        'comment_id': comment.id,
        'author': author_name,
        'text': comment.text,
        'created_at': comment.created_at.isoformat()
    }
)

# 3. Activity Feed Update
await channel_layer.group_send(
    'activity_feed',
    {
        'type': 'activity.new',
        'action': 'project_created',
        'project_id': project.id,
        'title': project.title,
        'owner': owner_name
    }
)

# 4. Notification
await channel_layer.group_send(
    f'user_{recipient_id}',
    {
        'type': 'notification.new',
        'message': 'John liked your project',
        'notification_id': notification.id
    }
)
```

#### 3.2 Channel Layer Configuration

**settings.py (Channels config)**
```python
CHANNEL_LAYERS = {
    'default': {
        'BACKEND': 'channels_redis.core.RedisChannelLayer',
        'CONFIG': {
            'hosts': [('127.0.0.1', 6379)],
            'expiry': 86400,
        },
    },
}

INSTALLED_APPS = [
    'daphne',  # ASGI server
    'channels',
    'rest_framework',
    'corsheaders',
    'accounts',
    # ...
]
```

---

### 4. URL Routing (accounts/urls.py)

#### 4.1 Web Routes

```python
urlpatterns = [
    # Authentication
    path('register/', register, name='register'),
    path('verify-otp/', verify_otp, name='verify_otp'),
    path('login/', login_view, name='login'),
    path('logout/', logout_view, name='logout'),
    
    # Dashboard & Feed
    path('dashboard/', dashboard_view, name='dashboard'),
    path('feed/', project_feed, name='project_feed'),
    path('search/', search_projects, name='search_projects'),
    
    # Projects
    path('project/create/', create_project, name='create_project'),
    path('project/<int:project_id>/', project_detail, name='project_detail'),
    path('project/<int:project_id>/edit/', edit_project, name='edit_project'),
    path('project/<int:project_id>/delete/', delete_project, name='delete_project'),
    
    # User Profiles
    path('profile/edit/', edit_profile, name='edit_profile'),
    path('profile/<str:username>/', view_profile, name='view_profile'),
    path('profile/<int:user_id>/connect/', send_connection_request, name='connect'),
    
    # Messaging
    path('messages/', messages_list, name='messages'),
    path('messages/<int:user_id>/', start_chat, name='start_chat'),
    
    # Pages
    path('about/', about, name='about'),
    path('contact/', contact, name='contact'),
]
```

#### 4.2 REST API Routes

```python
router = DefaultRouter()
router.register(r'comments', CommentViewSet)
router.register(r'projects', ProjectViewSet)
router.register(r'connections', ConnectionViewSet)
router.register(r'notifications', NotificationViewSet)

urlpatterns += [
    path('api/', include(router.urls)),
    
    # Custom API endpoints
    path('api/projects/<int:project_id>/like/', like_project, name='like_project'),
    path('api/projects/<int:project_id>/unlike/', unlike_project, name='unlike_project'),
    path('api/users/<int:user_id>/profile/', UserProfileView.as_view(), name='user_profile_api'),
    path('api/search/projects/', SearchProjectsAPI.as_view(), name='search_projects_api'),
]
```

#### 4.3 WebSocket Routes (routing.py)

```python
websocket_urlpatterns = [
    path('ws/project/<int:project_id>/', ProjectUpdateConsumer.as_asgi()),
    path('ws/feed/', ActivityFeedConsumer.as_asgi()),
    path('ws/notifications/', NotificationConsumer.as_asgi()),
    path('ws/chat/<int:room_id>/', ChatConsumer.as_asgi()),
]
```

---

### 5. Authentication System

#### 5.1 OTP-based Email Login

**Flow:**
```
User submits email
  ↓
Backend generates 6-digit OTP
  ↓
Email OTP to user (Brevo/Zepto)
  ↓
User receives email with code
  ↓
User submits OTP on verification page
  ↓
Backend validates:
  - OTP matches database
  - OTP not expired (10 min)
  - OTP not already used
  ↓
Create Django session / JWT token
  ↓
Redirect to dashboard
```

**Implementation:**
```python
# views.py
def login_view(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        if not User.objects.filter(email=email).exists():
            messages.error(request, 'Email not registered')
            return redirect('login')
        
        # Generate OTP
        otp = OTP.generate_otp(email, 'login')
        
        # Send email
        send_otp_email(email, otp.otp_code)
        
        return redirect('verify_otp')

def verify_otp(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        otp_code = request.POST.get('otp_code')
        
        otp = OTP.objects.get(email=email, otp_code=otp_code)
        success, msg = otp.verify_otp(otp_code)
        
        if success:
            user = User.objects.get(email=email)
            login(request, user)
            return redirect('dashboard')
        else:
            messages.error(request, msg)
            return redirect('verify_otp')
```

#### 5.2 OAuth (Google & GitHub)

**Configured via django-allauth**
```python
# settings.py
INSTALLED_APPS = [
    'allauth',
    'allauth.account',
    'allauth.socialaccount',
    'allauth.socialaccount.providers.google',
    'allauth.socialaccount.providers.github',
]

SOCIALACCOUNT_PROVIDERS = {
    'google': {
        'APP': {
            'client_id': env('GOOGLE_CLIENT_ID'),
            'secret': env('GOOGLE_CLIENT_SECRET'),
        }
    },
    'github': {
        'APP': {
            'client_id': env('GITHUB_CLIENT_ID'),
            'secret': env('GITHUB_CLIENT_SECRET'),
        }
    }
}
```

**Flow:**
```
User clicks "Login with Google"
  ↓
Redirect to Google OAuth consent screen
  ↓
User authorizes access
  ↓
Google redirects to callback URL with code
  ↓
Backend exchanges code for access token
  ↓
Fetch user info (name, email, picture) from Google
  ↓
Check if user exists in database
  ↓
If new: Create User + StudentProfile
If exists: Login existing user
  ↓
Create session & redirect to dashboard
```

---

### 6. Serializers (accounts/serializers.py)

#### 6.1 Model Serializers

```python
class StudentProfileSerializer(serializers.ModelSerializer):
    user = serializers.StringRelatedField()
    
    class Meta:
        model = StudentProfile
        fields = ['user', 'full_name', 'college', 'bio', 'skills', 
                 'profile_photo', 'github', 'linkedin']

class ProjectSerializer(serializers.ModelSerializer):
    owner = StudentProfileSerializer(read_only=True)
    like_count = serializers.SerializerMethodField()
    comment_count = serializers.SerializerMethodField()
    
    class Meta:
        model = Project
        fields = ['id', 'owner', 'title', 'description', 
                 'visibility', 'like_count', 'comment_count', 'created_at']
    
    def get_like_count(self, obj):
        return obj.liked_by.count()

class CommentSerializer(serializers.ModelSerializer):
    author = serializers.StringRelatedField()
    
    class Meta:
        model = Comment
        fields = ['id', 'project', 'author', 'text', 'created_at']
```

#### 6.2 Custom Serializers

```python
class UserProfileSerializer(serializers.Serializer):
    username = serializers.CharField()
    email = serializers.EmailField()
    profile_photo = serializers.SerializerMethodField()
    skills = serializers.ListField()
    connections_count = serializers.SerializerMethodField()
    projects_count = serializers.SerializerMethodField()
    
    def get_profile_photo(self, obj):
        return obj.student_profile.profile_photo.url if obj.student_profile.profile_photo else None
```

---

### 7. Permissions (accounts/permissions.py)

```python
class IsProjectOwner(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        return obj.owner == request.user

class IsCommentAuthor(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        return obj.author == request.user

class CanViewProfile(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        if obj.visibility == 'public':
            return True
        if obj.owner == request.user:
            return True
        # Check if friends/connections
        return obj.owner in request.user.connections.all()
```

---

### 8. Frontend Integration

#### 8.1 HTML Templates Structure

**Base Template (base.html)**
```html
<!DOCTYPE html>
<html>
<head>
    <title>{% block title %}UniSinq{% endblock %}</title>
    <link rel="stylesheet" href="{% static 'css/style.css' %}">
</head>
<body>
    {% include 'components/navbar.html' %}
    
    <div class="container">
        {% if messages %}
            {% for message in messages %}
                <div class="alert alert-{{ message.tags }}">
                    {{ message }}
                </div>
            {% endfor %}
        {% endif %}
        
        {% block content %}{% endblock %}
    </div>
    
    {% include 'components/footer.html' %}
    
    <script src="{% static 'js/main.js' %}"></script>
    {% block scripts %}{% endblock %}
</body>
</html>
```

**Project Feed Template (project_feed.html)**
```html
{% extends 'base.html' %}

{% block content %}
<div class="feed">
    {% for project in page_obj %}
        <div class="project-card">
            <div class="project-header">
                <img src="{{ project.owner.student_profile.profile_photo.url }}" 
                     class="avatar" alt="avatar">
                <h3>{{ project.title }}</h3>
            </div>
            <p>{{ project.description }}</p>
            
            <div class="project-engagement">
                <button onclick="likeProject({{ project.id }})">
                    ❤️ Like ({{ project.like_count }})
                </button>
                <button onclick="openComments({{ project.id }})">
                    💬 Comments ({{ project.comment_count }})
                </button>
            </div>
        </div>
    {% empty %}
        <p>No projects found.</p>
    {% endfor %}
    
    <!-- Pagination -->
    {% if page_obj.has_other_pages %}
        <div class="pagination">
            {% for page_num in page_obj.paginator.page_range %}
                <a href="?page={{ page_num }}">{{ page_num }}</a>
            {% endfor %}
        </div>
    {% endif %}
</div>

{% block scripts %}
<script src="{% static 'js/realtime-updates.js' %}"></script>
{% endblock %}
{% endblock %}
```

#### 8.2 Real-time JavaScript

**WebSocket Connection (static/js/realtime-updates.js)**
```javascript
// Connect to WebSocket
const projectId = parseInt(document.querySelector('[data-project-id]').dataset.projectId);
const socket = new WebSocket(`ws://localhost:8000/ws/project/${projectId}/`);

socket.onopen = (event) => {
    console.log('✅ WebSocket connected to project', projectId);
};

socket.onmessage = (event) => {
    const data = JSON.parse(event.data);
    
    if (data.type === 'project.initial_data') {
        console.log('Project data:', data.data);
    }
    else if (data.type === 'comment.created') {
        // Append new comment to DOM
        const comment = document.createElement('div');
        comment.className = 'comment';
        comment.innerHTML = `
            <strong>${data.author}</strong>: ${data.text}
        `;
        document.getElementById('comments').appendChild(comment);
    }
    else if (data.type === 'like.updated') {
        // Update like count
        document.getElementById('like-count').textContent = data.count;
    }
};

socket.onerror = (error) => {
    console.error('❌ WebSocket error:', error);
};

socket.onclose = (event) => {
    console.log('🔌 WebSocket disconnected');
};

// Helper functions
function likeProject(projectId) {
    fetch(`/api/projects/${projectId}/like/`, { method: 'POST' })
        .then(r => r.json())
        .then(data => console.log('Liked:', data));
}

function postComment(projectId, text) {
    socket.send(JSON.stringify({
        type: 'comment.post',
        text: text
    }));
}
```

#### 8.3 AJAX API Calls

**API Utilities (static/js/api-utils.js)**
```javascript
const API_BASE = '/api';

async function getProjects(filters = {}) {
    const params = new URLSearchParams(filters);
    const response = await fetch(`${API_BASE}/projects/?${params}`);
    return response.json();
}

async function createComment(projectId, text) {
    const response = await fetch(`${API_BASE}/comments/`, {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
            'X-CSRFToken': getCookie('csrftoken')
        },
        body: JSON.stringify({
            project: projectId,
            text: text
        })
    });
    return response.json();
}

async function sendConnectionRequest(userId) {
    const response = await fetch(`/api/users/${userId}/connect/`, {
        method: 'POST',
        headers: { 'X-CSRFToken': getCookie('csrftoken') }
    });
    return response.json();
}

function getCookie(name) {
    let cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        const cookies = document.cookie.split(';');
        for (let i = 0; i < cookies.length; i++) {
            const cookie = cookies[i].trim();
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}
```

---

### 9. Email Services

#### 9.1 Brevo Mail Backend (brevo_mail_backend.py)

```python
from django.core.mail.backends.base import BaseEmailBackend
import requests

class BrevoEmailBackend(BaseEmailBackend):
    def __init__(self, fail_silently=False, **kwargs):
        super().__init__(fail_silently=fail_silently)
        self.api_key = settings.BREVO_API_KEY
        self.api_url = 'https://api.brevo.com/v3/smtp/email'
    
    def send_messages(self, email_messages):
        if not email_messages:
            return 0
        
        count = 0
        for message in email_messages:
            headers = {
                'api-key': self.api_key,
                'Content-Type': 'application/json'
            }
            
            payload = {
                'sender': {'name': 'UniSinq', 'email': settings.DEFAULT_FROM_EMAIL},
                'to': [{'email': recipient} for recipient in message.to],
                'subject': message.subject,
                'htmlContent': message.body
            }
            
            try:
                response = requests.post(self.api_url, json=payload, headers=headers)
                if response.status_code == 201:
                    count += 1
                else:
                    if not self.fail_silently:
                        raise Exception(f"Brevo API error: {response.text}")
            except Exception as e:
                if not self.fail_silently:
                    raise
        
        return count
```

#### 9.2 Email Sending Function

```python
def send_otp_email(email, otp_code):
    from django.core.mail import EmailMultiAlternatives
    from django.template.loader import render_to_string
    
    context = {
        'otp_code': otp_code,
        'expiry_minutes': 10
    }
    
    html_content = render_to_string('emails/otp.html', context)
    
    msg = EmailMultiAlternatives(
        subject='Your UniSinq Login Code',
        body=f'Your OTP is: {otp_code}',
        from_email='noreply@unisinq.com',
        to=[email]
    )
    msg.attach_alternative(html_content, 'text/html')
    msg.send()
```

---

### 10. Database Schema (Simplified)

```sql
-- User & Profile
users
├─ id (PK)
├─ username (UNIQUE)
├─ email (UNIQUE)
├─ password (hashed)
├─ is_active
└─ created_at

student_profiles
├─ id (PK)
├─ user_id (FK→users, UNIQUE)
├─ full_name
├─ college
├─ bio
├─ profile_photo (path)
├─ skills (JSON)
├─ github, linkedin, portfolio
└─ profile_completed

-- Projects & Engagement
projects
├─ id (PK)
├─ owner_id (FK→users)
├─ title
├─ description
├─ collaboration_needs
├─ visibility (public/private/friends)
├─ is_archived
├─ created_at
└─ updated_at

comments
├─ id (PK)
├─ project_id (FK→projects)
├─ author_id (FK→users)
├─ text
├─ parent_comment_id (FK→comments, NULL)
├─ created_at
└─ updated_at

likes
├─ id (PK)
├─ project_id (FK→projects)
├─ user_id (FK→users)
└─ created_at
(UNIQUE(project_id, user_id))

-- Networking
connections
├─ id (PK)
├─ from_user_id (FK→users)
├─ to_user_id (FK→users)
├─ status (pending/accepted/blocked)
├─ created_at
└─ accepted_at

-- Messaging
chat_rooms
├─ id (PK)
├─ name
├─ is_group
└─ created_at

chat_room_members (M2M)
├─ chat_room_id (FK→chat_rooms)
├─ user_id (FK→users)

messages
├─ id (PK)
├─ chat_room_id (FK→chat_rooms)
├─ sender_id (FK→users)
├─ text
├─ created_at
└─ updated_at

-- Notifications & Activity
notifications
├─ id (PK)
├─ recipient_id (FK→users)
├─ sender_id (FK→users)
├─ notification_type
├─ read
└─ created_at

activity
├─ id (PK)
├─ user_id (FK→users)
├─ action_type
├─ object_id
└─ created_at

-- OTP
otps
├─ id (PK)
├─ email
├─ otp_code
├─ purpose (login/registration/reset)
├─ is_used
├─ created_at
└─ expires_at
```

---

## Key Features Analysis

### 1. User Authentication
- **Email OTP**: 6-digit codes with 10-min expiry
- **Social Login**: Google & GitHub OAuth
- **Session Management**: Django sessions + CSRF protection

### 2. Project Management
- **CRUD Operations**: Create, read, update, delete projects
- **Visibility Control**: Public, private, friends-only
- **Filtering**: By skills, collaboration needs, date
- **Engagement**: Likes, comments, shares

### 3. Real-time Features
- **WebSocket Updates**: Live project status, comments, notifications
- **Activity Feed**: Broadcast new projects to all connected users
- **Notifications**: Typed notifications (like, comment, connection request)
- **Message Status**: Read/unread tracking

### 4. Collaboration Tools
- **Connection System**: Request/accept networking
- **Team Management**: Add members to projects
- **Direct Messaging**: 1:1 and group chats
- **Skill Matching**: NLP-based collaborator recommendations

### 5. Security
- **CSRF Tokens**: All POST/PUT/DELETE requests
- **Authentication Required**: `@login_required` decorators
- **Permission Classes**: DRF permissions for API access
- **Email Verification**: OTP-based verification
- **OAuth Verification**: Signature validation

---

## Technology Stack Summary

| Layer | Technology |
|-------|-----------|
| **Framework** | Django 3.2+ |
| **API** | Django REST Framework |
| **Real-time** | Django Channels + Redis |
| **Database** | PostgreSQL (prod), SQLite (dev) |
| **Authentication** | OTP, OAuth (Google/GitHub) |
| **Email** | Brevo, Zepto Mail |
| **Frontend** | HTML5, CSS3, JavaScript, jQuery |
| **Server** | Daphne (ASGI), Gunicorn (WSGI) |
| **Deployment** | Render, Railway, Heroku |

---

## Development Workflow

### 1. Local Setup
```bash
cd auth_project
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
pip install -r requirements.txt
python manage.py migrate
python manage.py runserver
# For WebSocket: daphne -b 0.0.0.0 -p 8000 auth_project.asgi:application
```

### 2. Creating New Features
1. **Add Model** → accounts/models.py
2. **Create Migration** → `python manage.py makemigrations accounts`
3. **Apply Migration** → `python manage.py migrate`
4. **Add View** → accounts/views.py
5. **Create Serializer** → accounts/serializers.py
6. **Register URL** → accounts/urls.py
7. **Create Template** → accounts/templates/
8. **Add JavaScript** → static/js/

### 3. Testing
```bash
python manage.py test accounts
```

### 4. Deployment
```bash
# Collect static files
python manage.py collectstatic --noinput

# Run migrations on production
python manage.py migrate --noinput

# Start server
gunicorn auth_project.wsgi:application
daphne auth_project.asgi:application  # For WebSocket
```

---

## Common Issues & Solutions

### WebSocket Connection Fails
- **Cause**: Redis not running or misconfigured
- **Fix**: Start Redis server, check `CHANNEL_LAYERS` settings

### OTP Email Not Sending
- **Cause**: BREVO_API_KEY not set or invalid
- **Fix**: Check `.env` file, verify API credentials in settings.py

### CSRF Token Errors
- **Cause**: Missing CSRF token in form or AJAX request
- **Fix**: Include `{% csrf_token %}` in forms, add header in AJAX

### Profile Photo Not Displaying
- **Cause**: Media files not collected or incorrect path
- **Fix**: Run `collectstatic`, check MEDIA_URL in settings.py

### OAuth Redirect URI Mismatch
- **Cause**: Registered URI doesn't match application callback
- **Fix**: Update OAuth provider settings to match deployment URL

---

## Performance Considerations

1. **Database Queries**: Use `select_related()` and `prefetch_related()` for N+1 issues
2. **Caching**: Implement Redis caching for frequently accessed data
3. **Pagination**: Always paginate large result sets
4. **Image Optimization**: Compress profile photos, use thumbnails
5. **WebSocket Optimization**: Use rooms/groups to reduce message broadcasting
6. **Async Tasks**: Use Celery for long-running operations (email, image processing)

---

This completes the comprehensive code analysis of UniSinq. The application is well-structured with clear separation of concerns between frontend, API, real-time, and database layers.
