# Comprehensive Code Analysis - UniSync Project (2026)

## Executive Summary

This is a **Django-based student collaboration platform** built with **modern authentication, real-time features, and social connectivity**. The application enables students to create projects, find collaborators, engage in team chats, and manage project-based communities.

**Stack:**
- **Backend:** Django 4.x, Django Channels (WebSockets), Django REST Framework
- **Frontend:** HTML/CSS/JavaScript, AJAX, WebSocket Client
- **Database:** PostgreSQL
- **External Services:** Google OAuth (django-allauth), Brevo/Zepto Mail, Redis Cache
- **Deployment:** Render/Railway, Daphne for WebSocket support

---

## 📁 Project Structure

```
e:/login/auth_project/
├── auth_project/              # Django project settings
│   ├── settings.py           # Configuration (databases, apps, middleware)
│   ├── urls.py               # Root URL router
│   ├── wsgi.py              # WSGI application
│   ├── asgi.py              # ASGI configuration (channels/websockets)
│   └── __init__.py
│
├── accounts/                  # Main application
│   ├── models.py            # Database models (StudentProfile, Project, etc.)
│   ├── views.py             # Core views (~3400+ lines)
│   ├── serializers.py       # DRF serializers for APIs
│   ├── urls.py              # App URL patterns
│   ├── forms.py             # Django forms
│   ├── consumers.py         # WebSocket consumers (Channels)
│   ├── signals_realtime.py  # Django signals for real-time updates
│   ├── routing.py           # WebSocket routing
│   ├── permissions.py       # Custom DRF permissions
│   ├── utils.py             # Utility functions
│   │
│   ├── services/
│   │   └── auth_service.py  # Authentication logic
│   │
│   ├── chat_api.py          # Chat functionality API
│   ├── comment_api.py       # Comments functionality API
│   ├── template_api.py      # Template rendering API
│   ├── brevo_mail_backend.py    # Email backend (Brevo)
│   ├── zepto_mail_backend.py    # Email backend (Zepto)
│   │
│   ├── management/
│   │   └── commands/
│   │       └── create_templates.py  # Template management
│   │
│   ├── migrations/          # Database migrations
│   ├── templatetags/        # Custom template filters
│   ├── tests.py             # Test cases
│   └── apps.py              # App configuration
│
├── static/                   # Static files (CSS, JS, images)
├── media/                    # User uploads (profile photos, files)
├── templates/               # HTML templates
│
├── manage.py               # Django management script
├── requirements.txt        # Python dependencies
├── db.sqlite3             # SQLite database (development)
└── .env                   # Environment variables
```

---

## 🗄️ Core Models & Database Schema

### 1. **StudentProfile**
Extends Django's User model with student-specific information.

```python
class StudentProfile(models.Model):
    user = OneToOneField(User)
    full_name = CharField(max_length=100)
    college = CharField(max_length=200)
    location = CharField(max_length=100)
    interests = JSONField()  # Skills, hobbies, interests
    bio = TextField()
    profile_photo = ImageField(upload_to='profile_photos/')
    skills = JSONField()
    project_interests = JSONField()
    github, linkedin, portfolio, behance = URLFields()
    profile_completed = BooleanField(default=False)
    created_at, updated_at = DateTimeFields()
```

**Key Features:**
- Social links (GitHub, LinkedIn, Portfolio)
- JSON-based arrays for flexible skill/interest storage
- Profile completion tracking

### 2. **Project**
Core project model for collaborative work.

```python
class Project(models.Model):
    id = UUIDField(primary_key=True)
    title, description = CharField/TextField
    owner = ForeignKey(User)
    category = CharField(choices=[...])  # Web Dev, Mobile, Data Science, etc.
    visibility = CharField(default='public')  # Public/Private
    tech_stack = JSONField()  # Technologies used
    collaboration_needs = JSONField()  # Roles needed
    members = ManyToManyField(User, through='ProjectTeamMember')
    created_at, updated_at = DateTimeFields()
    likes_count = IntegerField(default=0)
    comments_count = IntegerField(default=0)
```

**Key Features:**
- UUID-based IDs for unique identification
- Flexible tech stack & collaboration needs via JSON
- Team member tracking through junction table

### 3. **Comment** (Post-like feature on projects)
Enables discussions on project cards/details.

```python
class Comment(models.Model):
    id = UUIDField(primary_key=True)
    project = ForeignKey(Project, on_delete=CASCADE)
    user = ForeignKey(User, on_delete=CASCADE)
    content = TextField()
    likes_count = IntegerField(default=0)
    created_at = DateTimeField(auto_now_add=True)
    updated_at = DateTimeField(auto_now=True)
```

### 4. **Message** (Direct messaging between users)
```python
class Message(models.Model):
    sender = ForeignKey(User, related_name='sent_messages')
    receiver = ForeignKey(User, related_name='received_messages')
    content = TextField()
    is_read = BooleanField(default=False)
    timestamp = DateTimeField(auto_now_add=True)
```

### 5. **ChatRoom** (Team chat channels)
```python
class ChatRoom(models.Model):
    id = UUIDField(primary_key=True)
    name = CharField(max_length=100)
    project = ForeignKey(Project, on_delete=CASCADE)
    members = ManyToManyField(User, through='ChatRoomMember')
    created_at = DateTimeField(auto_now_add=True)
    is_active = BooleanField(default=True)
```

### 6. **Connection** (User relationships/networking)
```python
class Connection(models.Model):
    from_user = ForeignKey(User)
    to_user = ForeignKey(User)
    status = CharField(choices=[('pending', 'Pending'), ('connected', 'Connected')])
    created_at = DateTimeField(auto_now_add=True)
```

### 7. **OTP** (One-time password for auth)
```python
class OTP(models.Model):
    email = EmailField()
    otp_code = CharField(max_length=6)
    purpose = CharField(choices=[('login', 'Login'), ('registration', 'Registration')])
    is_used = BooleanField(default=False)
    expires_at = DateTimeField()
    
    def is_valid(self): 
        return not self.is_used and timezone.now() < self.expires_at
```

### 8. **Notification**
```python
class Notification(models.Model):
    user = ForeignKey(User)
    type = CharField()  # 'like', 'comment', 'connection_request', etc.
    actor = ForeignKey(User, related_name='notifications_from')
    content_object = GenericForeignKey('content_type', 'object_id')
    is_read = BooleanField(default=False)
    created_at = DateTimeField(auto_now_add=True)
```

---

## 🔐 Authentication System

### OTP-Based Login Flow

```
1. User enters email on login page
2. POST /accounts/send-otp/
   └─> OTP.generate_otp(email, 'login')
       └─> Email sent via Brevo/Zepto
3. User receives email with 6-digit code
4. POST /accounts/verify-otp/
   └─> OTP.verify_otp(code)
   └─> If valid: Create session & redirect to dashboard
5. User logs in successfully
```

### Google OAuth Integration

**Setup via django-allauth:**
- Provider: Google OAuth
- Redirect URI: `/accounts/google/callback/`
- Automatic profile creation
- Social account linking to User

**Key Views:**
- `/accounts/google/login/` - Initiate OAuth
- `/accounts/google/callback/` - OAuth callback
- Automatic StudentProfile creation on first login

---

## 🎯 Core Views & Functionality

### Authentication Views

| View | Method | Purpose |
|------|--------|---------|
| `register_view()` | GET, POST | User registration with OTP |
| `login_view()` | GET, POST | Login with OTP or email/password |
| `logout_view()` | POST | User logout |
| `send_otp()` | POST | Generate & send OTP email |
| `verify_otp()` | POST | Verify OTP code |

### Project Management Views

| View | Method | Purpose |
|------|--------|---------|
| `project_detail()` | GET | View project with comments |
| `create_project()` | GET, POST | Create new project |
| `edit_project()` | GET, POST | Edit project |
| `delete_project()` | POST | Delete project |
| `project_feed()` | GET | List all projects (paginated) |
| `search_projects()` | GET | Search & filter projects |
| `find_collaborators()` | GET | Find users by skills/interests |
| `filter_projects()` | GET | Advanced project filtering |

### Collaboration Views

| View | Method | Purpose |
|------|--------|---------|
| `send_connection_request()` | POST | Send connection request |
| `accept_connection()` | POST | Accept connection |
| `view_profile()` | GET | View another user's profile |
| `edit_profile()` | GET, POST | Edit own profile |

### Chat & Comments Views

| View | Method | Purpose |
|------|--------|---------|
| `chat_room()` | GET | View chat room |
| `post_comment()` | POST | Add comment to project |
| `delete_comment()` | POST | Delete comment |
| `like_project()` / `unlike_project()` | POST | Like/unlike functionality |

---

## 🔗 API Endpoints (REST Framework)

### Projects API
```
GET    /api/projects/              - List all projects
POST   /api/projects/              - Create project
GET    /api/projects/{id}/         - Get project detail
PUT    /api/projects/{id}/         - Update project
DELETE /api/projects/{id}/         - Delete project
POST   /api/projects/{id}/like/    - Like project
POST   /api/projects/{id}/comment/ - Add comment
```

### User API
```
GET    /api/users/                 - List users
GET    /api/users/{id}/            - Get user detail
GET    /api/users/{id}/profile/    - Get user profile
PUT    /api/users/{id}/profile/    - Update profile
POST   /api/users/search/          - Search users
```

### Chat API
```
GET    /api/chat-rooms/            - List chat rooms
POST   /api/chat-rooms/            - Create room
POST   /api/messages/              - Send message
GET    /api/messages/{room_id}/    - Get room messages
```

### Comments API
```
GET    /api/comments/{project_id}/ - Get comments
POST   /api/comments/              - Add comment
DELETE /api/comments/{id}/         - Delete comment
```

---

## 🔄 WebSocket Architecture (Real-time Features)

### Components

**File:** `accounts/consumers.py`
```python
class ChatConsumer(AsyncWebsocketConsumer):
    async def connect():
        """User joins a chat room"""
        self.room_group_name = f'chat_{self.room_id}'
        await self.channel_layer.group_add(
            self.room_group_name, self.channel_name
        )
        await self.accept()
    
    async def receive():
        """Handle incoming messages"""
        # Broadcast to all users in room
        await self.channel_layer.group_send(
            self.room_group_name, {
                'type': 'chat_message',
                'message': data
            }
        )
```

**File:** `accounts/routing.py`
```python
websocket_urlpatterns = [
    path('ws/chat/<str:room_id>/', ChatConsumer.as_asgi()),
    path('ws/notifications/', NotificationConsumer.as_asgi()),
    path('ws/project-feed/', FeedConsumer.as_asgi()),
]
```

**Configuration:** `settings.py`
```python
CHANNEL_LAYERS = {
    'default': {
        'BACKEND': 'channels.layers.InMemoryChannelLayer'
    }
}

# For production (Redis):
# CHANNEL_LAYERS = {
#     'default': {
#         'BACKEND': 'channels_redis.core.RedisChannelLayer',
#         'CONFIG': {'hosts': [('127.0.0.1', 6379)]}
#     }
# }
```

### Real-time Features

1. **Live Chat** - Messages broadcast instantly to room members
2. **Activity Feed** - Projects updated in real-time for all users
3. **Notifications** - Comment/like notifications via WebSocket
4. **Live Comments** - Comments appear instantly on project detail

---

## 📧 Email Configuration

### Email Backends

**Brevo (Sendinblue):**
```python
# accounts/brevo_mail_backend.py
class BrevoBackend(BaseEmailBackend):
    def send_messages(self, email_messages):
        api_key = os.getenv('BREVO_API_KEY')
        # Uses Brevo SMTP service
        # Handles HTML & plain text emails
```

**Zepto Mail:**
```python
# accounts/zepto_mail_backend.py
class ZeptoBackend(BaseEmailBackend):
    def send_messages(self, email_messages):
        api_key = os.getenv('ZEPTO_API_KEY')
        # REST API-based email sending
```

**Usage:**
```python
# In settings.py
EMAIL_BACKEND = 'accounts.brevo_mail_backend.BrevoBackend'
# or
EMAIL_BACKEND = 'accounts.zepto_mail_backend.ZeptoBackend'

# Sending emails
from django.core.mail import EmailMultiAlternatives
email = EmailMultiAlternatives(
    subject='Welcome!',
    body='Plain text',
    from_email='noreply@unisinq.com',
    to=['user@example.com']
)
email.attach_alternative(html_content, "text/html")
email.send()
```

### OTP Email Template
```html
<h1>Your OTP Code</h1>
<p>Use this code to complete your login:</p>
<h2 style="color: blue; font-size: 24px;">{{ otp_code }}</h2>
<p>This code expires in 10 minutes.</p>
```

---

## 🔧 Service Layer

### StudentProfileNLP (Skill matching)
**File:** `accounts/utils.py`

```python
class StudentProfileNLP:
    @staticmethod
    def match_projects(user_profile, projects):
        """
        AI-based skill matching between user profile and projects
        - Analyze user skills & interests
        - Rank projects by relevance
        - Consider tech stack overlap
        """
        matching_scores = {}
        for project in projects:
            score = calculate_similarity(
                user_profile.skills,
                project.tech_stack
            )
            matching_scores[project] = score
        return sorted by score descending
```

### ProjectVisibilityFilter
```python
class ProjectVisibilityFilter:
    @staticmethod
    def get_visible_projects(user):
        """
        Filter projects based on visibility & permissions
        - Public: All users
        - Private: Only owner & team members
        - Hidden: Owner only
        """
        visible = Project.objects.filter(
            Q(visibility='public') |
            Q(owner=user) |
            Q(members=user)
        ).distinct()
        return visible
```

---

## 🛡️ Security Features

### CSRF Protection
```python
# Middleware enabled in settings.py
MIDDLEWARE = [
    '...',
    'django.middleware.csrf.CsrfViewMiddleware',
    '...'
]

# In templates: {% csrf_token %}
# In AJAX: Include X-CSRFToken header
```

### Authentication Decorators
```python
@login_required
def protected_view(request):
    """Only authenticated users can access"""
    pass

@require_http_methods(["POST"])
def api_endpoint(request):
    """Only allows POST requests"""
    pass
```

### Permissions
```python
# accounts/permissions.py
class IsOwner(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        return obj.owner == request.user

class IsTeamMember(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        return request.user in obj.members.all()
```

---

## 📊 Database Relationships

```
User (Django built-in)
├── StudentProfile (OneToOne)
├── Project (ForeignKey as owner)
├── Comment (ForeignKey)
├── Connection (ForeignKey as from_user/to_user)
├── Message (ForeignKey as sender/receiver)
├── Like (ForeignKey)
├── Follow (ForeignKey)
├── ChatRoom (through ChatRoomMember)
└── Notification (ForeignKey)

Project
├── Owner (ForeignKey to User)
├── Members (ManyToMany through ProjectTeamMember)
├── Comment (ForeignKey)
├── Like (ForeignKey)
├── Team (OneToOne to ProjectTeam)
└── ChatRooms (OneToMany)

ChatRoom
├── Project (ForeignKey)
├── Messages (OneToMany)
└── Members (ManyToMany through ChatRoomMember)
```

---

## 🚀 Key Features Implementation

### 1. Project Discovery & Search
```python
def search_projects(request):
    query = request.GET.get('q', '')
    projects = Project.objects.filter(
        Q(title__icontains=query) |
        Q(description__icontains=query) |
        Q(collaboration_needs__icontains=query)
    )
    return paginated_results
```

### 2. Skill-Based Collaborator Finding
```python
def find_collaborators(request):
    skills = request.GET.getlist('skills[]')
    interests = request.GET.getlist('interests[]')
    
    users = StudentProfile.objects.filter(
        Q(skills__contains=skills) |
        Q(interests__contains=interests)
    )
    return users
```

### 3. Real-time Project Activity Feed
```python
class FeedConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        await self.channel_layer.group_add(
            'project_feed',
            self.channel_name
        )
    
    async def project_activity(self, event):
        # Broadcast project updates to all connected users
        await self.send(json.dumps(event['data']))
```

### 4. Live Comments on Projects
```python
@login_required
def post_comment(request, project_id):
    comment = Comment.objects.create(
        project_id=project_id,
        user=request.user,
        content=request.POST['content']
    )
    
    # Broadcast to WebSocket
    channel_layer = get_channel_layer()
    async_to_sync(channel_layer.group_send)(
        f'project_{project_id}',
        {
            'type': 'comment_added',
            'comment': serialize(comment)
        }
    )
```

---

## 🔄 Data Flow Examples

### User Registration Flow
```
1. User submits registration form
   └─> POST /accounts/register/
   
2. Server validates email (unique)
   └─> Generate & send OTP
   
3. User receives OTP email
   └─> Provides 6-digit code
   
4. POST /accounts/verify-otp/
   └─> OTP.verify_otp()
   └─> Create User & StudentProfile
   └─> Redirect to profile setup
   
5. User fills profile info
   └─> Save StudentProfile with skills, interests
   
6. Redirect to dashboard/project feed
```

### Project Creation & Discovery Flow
```
1. User navigates to "Create Project"
   └─> GET /accounts/create-project/
   
2. User fills project form (title, description, tech stack, etc.)
   └─> POST /accounts/create-project/
   
3. Server validates & saves Project
   └─> Broadcast project_created event
   
4. WebSocket subscribers (project feed) receive update
   └─> New project appears in real-time feed
   
5. Other users see project
   └─> Can comment, like, request to join
   
6. Owner receives notifications
   └─> Comment/like/join notifications via WebSocket
```

### Collaboration Request Flow
```
1. User finds collaborator via search
   └─> GET /accounts/find-collaborators/?skills=Python&interests=AI
   
2. User clicks "Send Connection Request"
   └─> POST /accounts/send-connection/
   
3. Create Connection (status='pending')
   └─> Send notification to recipient
   
4. Recipient accepts request
   └─> Update Connection (status='connected')
   └─> Add to project team
   
5. Both users notified
   └─> Can now collaborate on shared projects
```

---

## 📱 Frontend Integration

### AJAX for Real-time Interactions
```javascript
// Like a project
document.getElementById('like-btn').addEventListener('click', function() {
    fetch(`/api/projects/${projectId}/like/`, {
        method: 'POST',
        headers: {
            'X-CSRFToken': csrfToken,
            'Content-Type': 'application/json'
        }
    })
    .then(response => response.json())
    .then(data => {
        // Update UI without full page reload
        updateLikeCount(data.likes_count);
    });
});
```

### WebSocket for Live Updates
```javascript
// Connect to chat room
const chatSocket = new WebSocket(`ws://localhost:8000/ws/chat/${roomId}/`);

chatSocket.onmessage = function(event) {
    const data = JSON.parse(event.data);
    addMessageToDOM(data.message);
};

// Send message
function sendMessage(content) {
    chatSocket.send(JSON.stringify({
        'type': 'chat_message',
        'message': content
    }));
}
```

### Template Tags for Dynamic Content
```html
<!-- In templates/project_detail.html -->
<div class="comments-section">
    {% for comment in project.comment_set.all %}
        <div class="comment">
            <img src="{{ comment.user.student_profile.profile_photo.url }}" alt="{{ comment.user.username }}">
            <p><strong>{{ comment.user.get_full_name }}</strong></p>
            <p>{{ comment.content }}</p>
            <small>{{ comment.created_at|date:"M d, Y H:i" }}</small>
        </div>
    {% endfor %}
</div>
```

---

## ⚙️ Configuration & Environment

### .env File Variables
```env
# Debug mode
DEBUG=True

# Secret key for production
SECRET_KEY=your-secret-key-here

# Database
DATABASE_URL=postgresql://user:password@localhost:5432/unisinq
REDIS_URL=redis://localhost:6379/0

# Email
EMAIL_BACKEND=accounts.brevo_mail_backend.BrevoBackend
BREVO_API_KEY=your-brevo-key
ZEPTO_API_KEY=your-zepto-key

# Google OAuth
SOCIALACCOUNT_PROVIDERS['google']['APP']['client_id']=...
SOCIALACCOUNT_PROVIDERS['google']['APP']['secret']=...

# Allowed hosts
ALLOWED_HOSTS=localhost,127.0.0.1,yourdomain.com

# CSRF & Security
CSRF_TRUSTED_ORIGINS=http://localhost:8000,https://yourdomain.com
SECURE_SSL_REDIRECT=True
SESSION_COOKIE_SECURE=True
```

### Running the Server

**Development:**
```bash
python manage.py runserver
```

**With WebSocket Support (Daphne):**
```bash
daphne -b 0.0.0.0 -p 8000 auth_project.asgi:application
```

**Production:**
```bash
gunicorn auth_project.wsgi:application
# With WebSocket:
daphne auth_project.asgi:application
```

---

## 🐛 Common Issues & Fixes

### CSRF Token Errors
**Symptom:** 403 Forbidden on POST requests
**Fix:** Ensure `{% csrf_token %}` in forms and `X-CSRFToken` header in AJAX

### WebSocket Connection Issues
**Symptom:** Chat not working, WebSocket connection refused
**Fix:** Use Daphne instead of runserver, configure ASGI properly

### Email Not Sending
**Symptom:** OTP emails not received
**Fix:** 
- Verify EMAIL_BACKEND setting
- Check API keys (BREVO_API_KEY, ZEPTO_API_KEY)
- Review email logs

### Profile Photo Not Displaying
**Symptom:** Broken image on profile
**Fix:** 
- Ensure MEDIA_ROOT & MEDIA_URL configured
- Run `python manage.py collectstatic`
- Check file permissions on server

---

## 📈 Performance Optimization

### Caching
```python
from django.core.cache import cache

# Cache project feed for 5 minutes
@cache_page(300)
def project_feed(request):
    return render(request, 'project_feed.html')

# Manual caching
cache.set('user_projects_' + str(user_id), projects, 300)
projects = cache.get('user_projects_' + str(user_id))
```

### Database Optimization
```python
# Use select_related for ForeignKey
projects = Project.objects.select_related('owner')

# Use prefetch_related for reverse ForeignKey & ManyToMany
projects = Project.objects.prefetch_related('comment_set', 'members')

# Use only/defer for field selection
users = User.objects.only('id', 'username', 'email')
```

### Pagination
```python
from django.core.paginator import Paginator

projects = Project.objects.all()
paginator = Paginator(projects, 10)  # 10 per page
page_obj = paginator.get_page(request.GET.get('page'))
```

---

## 🔍 Testing

**Test File:** `accounts/tests.py`

```python
from django.test import TestCase, Client
from django.contrib.auth.models import User
from .models import StudentProfile, Project

class StudentProfileTestCase(TestCase):
    def setUp(self):
        self.user = User.objects.create_user('testuser', 'test@example.com', 'pass123')
        self.profile = StudentProfile.objects.create(user=self.user)
    
    def test_profile_creation(self):
        self.assertEqual(self.profile.user, self.user)
        self.assertEqual(str(self.profile), f"{self.user.username}'s profile")

class ProjectTestCase(TestCase):
    def test_project_creation(self):
        user = User.objects.create_user('owner', 'owner@example.com', 'pass123')
        project = Project.objects.create(
            title='AI Chat App',
            owner=user,
            description='Build an AI chatbot'
        )
        self.assertEqual(project.owner, user)
```

---

## 🚀 Deployment Checklist

- [ ] Set DEBUG=False in production
- [ ] Configure ALLOWED_HOSTS with your domain
- [ ] Use environment variables for secrets
- [ ] Set SECURE_SSL_REDIRECT=True
- [ ] Enable CSRF protection
- [ ] Configure email backend (Brevo/Zepto)
- [ ] Set up PostgreSQL database
- [ ] Configure Redis for caching & WebSocket
- [ ] Run migrations: `python manage.py migrate`
- [ ] Collect static files: `python manage.py collectstatic`
- [ ] Use Daphne for WebSocket support
- [ ] Set up reverse proxy (Nginx)
- [ ] Enable HTTPS/SSL
- [ ] Monitor logs & errors

---

## 📚 Key Dependencies

```
Django==4.2.0
djangorestframework==3.14.0
django-allauth==0.51.0
django-channels==4.0.0
django-cors-headers==4.0.0
Pillow==9.5.0  # Image processing
psycopg2==2.9.6  # PostgreSQL adapter
redis==4.5.0
celery==5.2.7  # Task queue
python-dotenv==1.0.0
requests==2.31.0
```

---

## 🎓 Learning Resources

- Django Documentation: https://docs.djangoproject.com
- Django Channels: https://channels.readthedocs.io
- Django REST Framework: https://www.django-rest-framework.org
- PostgreSQL: https://www.postgresql.org/docs
- WebSockets: https://developer.mozilla.org/en-US/docs/Web/API/WebSocket

---

## 👥 Team & Collaboration

**Roles Supported:**
- Backend Developer
- Frontend Developer
- Designer
- Project Manager
- Data Scientist

**Collaboration Features:**
- Team projects with multiple members
- Project task tracking
- Chat channels per project
- Real-time notifications
- File sharing in messages

---

## 📞 Support & Troubleshooting

**Common Commands:**
```bash
# Create superuser
python manage.py createsuperuser

# Run migrations
python manage.py migrate

# Create migration
python manage.py makemigrations

# Load fixtures
python manage.py loaddata data.json

# Django shell
python manage.py shell

# Clear cache
python manage.py shell
>>> from django.core.cache import cache
>>> cache.clear()
```

---

## 📅 Version History & Updates (2026)

**Latest Updates:**
- ✅ Real-time WebSocket support for chat & notifications
- ✅ Comment system with live updates
- ✅ Skill-based collaborator matching
- ✅ Project visibility filtering (public/private)
- ✅ Email OTP authentication
- ✅ Google OAuth integration
- ✅ Activity feed with real-time updates
- ✅ Multiple email backend support (Brevo, Zepto)
- ✅ Responsive UI with Bootstrap/Tailwind
- ✅ Performance optimizations & caching

---

## 📄 Document Information

**Created:** February 9, 2026
**Last Updated:** February 9, 2026
**Status:** ✅ Complete & Production Ready
**Project:** UniSync - Student Collaboration Platform

---

**This comprehensive guide covers all aspects of the UniSync codebase architecture, from database models to WebSocket implementation. Use this as a reference for development, debugging, and deployment.**
