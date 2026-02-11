# UniSync: Quick Developer Reference Guide

## File Locations & Purposes

### Core Django Configuration
```
auth_project/
├── settings.py       → Database, apps, middleware, email config
├── urls.py          → Root URL patterns
├── wsgi.py          → Production server entry point
└── asgi.py          → WebSocket server entry point
```

### Main Application
```
accounts/
├── models.py        → 20+ database models (1000+ lines)
├── views.py         → 50+ view functions (3450+ lines)
├── urls.py          → 150+ URL patterns (141 lines)
├── serializers.py   → DRF serializers (165 lines)
├── forms.py         → Django forms
├── chat_api.py      → Messaging API endpoints
├── comment_api.py   → Comments functionality
├── template_api.py  → Template system (partial)
└── consumers.py     → WebSocket handlers
```

### Real-Time Features
```
accounts/
├── routing.py              → WebSocket URL routing
├── signals_realtime.py     → Event-based signals
└── templates/
    ├── enhanced_messages.html
    └── base.html
```

### Utilities & Helpers
```
accounts/
├── utils.py              → StudentProfileNLP, sanitization
├── permissions.py        → Custom permission classes
├── brevo_mail_backend.py → Email service
├── zepto_mail_backend.py → Alternative email
└── services/             → Business logic modules
```

---

## Common Code Patterns

### Pattern 1: Creating a View Function

```python
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .models import Project
from .forms import ProjectForm

@login_required
def post_project(request):
    """Handle project creation"""
    if request.method == 'POST':
        form = ProjectForm(request.POST)
        if form.is_valid():
            project = form.save(commit=False)
            project.owner = request.user
            project.save()
            messages.success(request, 'Project created successfully!')
            return redirect('project_detail', project_id=project.id)
    else:
        form = ProjectForm()
    
    return render(request, 'accounts/post_project.html', {'form': form})
```

### Pattern 2: Creating a DRF View

```python
from rest_framework import generics, permissions
from .models import Project
from .serializers import ProjectSerializer

class ProjectListView(generics.ListCreateAPIView):
    """List and create projects"""
    queryset = Project.objects.all()
    serializer_class = ProjectSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    
    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)
```

### Pattern 3: Creating a Model

```python
from django.db import models
from django.contrib.auth.models import User

class Project(models.Model):
    """Project model for collaboration"""
    VISIBILITY_CHOICES = [
        ('public', 'Public'),
        ('private', 'Private'),
    ]
    
    owner = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=255)
    description = models.TextField()
    visibility = models.CharField(max_length=20, choices=VISIBILITY_CHOICES)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['-created_at']
    
    def __str__(self):
        return self.title
```

### Pattern 4: Creating a Serializer

```python
from rest_framework import serializers
from .models import Project

class ProjectSerializer(serializers.ModelSerializer):
    """Serialize Project model to JSON"""
    owner_name = serializers.CharField(source='owner.username', read_only=True)
    
    class Meta:
        model = Project
        fields = ['id', 'title', 'description', 'owner', 'owner_name', 'created_at']
        read_only_fields = ['id', 'created_at']
```

### Pattern 5: Creating a Signal Handler

```python
from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import Comment, Activity

@receiver(post_save, sender=Comment)
def create_activity_on_comment(sender, instance, created, **kwargs):
    """Create activity when comment is posted"""
    if created:
        Activity.objects.create(
            user=instance.author,
            activity_type='comment',
            project=instance.project
        )
```

### Pattern 6: WebSocket Consumer

```python
from channels.generic.websocket import AsyncWebsocketConsumer
import json

class ChatConsumer(AsyncWebsocketConsumer):
    """Handle WebSocket connections for chat"""
    
    async def connect(self):
        self.room_id = self.scope['url_route']['kwargs']['room_id']
        self.room_group_name = f'chat_{self.room_id}'
        
        # Join room group
        await self.channel_layer.group_add(
            self.room_group_name,
            self.channel_name
        )
        await self.accept()
    
    async def receive(self, text_data):
        data = json.loads(text_data)
        message = data['message']
        
        # Broadcast to room group
        await self.channel_layer.group_send(
            self.room_group_name,
            {
                'type': 'chat_message',
                'message': message
            }
        )
    
    async def chat_message(self, event):
        """Send message to WebSocket"""
        await self.send(text_data=json.dumps({
            'message': event['message']
        }))
```

---

## Essential Management Commands

### Database Operations
```bash
# Show pending migrations
python manage.py showmigrations

# Create migration for changes
python manage.py makemigrations

# Apply migrations
python manage.py migrate

# Revert to previous state
python manage.py migrate accounts 0001
```

### Development
```bash
# Start development server
python manage.py runserver

# Start WebSocket worker
python manage.py runworker -v 3

# Create superuser
python manage.py createsuperuser

# Open interactive shell
python manage.py shell

# Create test data
python manage.py createsuperuser
python create_test_user.py
```

### Production
```bash
# Collect static files
python manage.py collectstatic

# Check deployment settings
python manage.py check --deploy

# Backup database
pg_dump DATABASE_NAME > backup.sql
```

---

## API Endpoint Cheat Sheet

### Authentication
```
POST /login/          → User login with email/OTP
POST /register/       → New user registration
GET  /logout/         → User logout
POST /forgot-password/ → Request password reset
```

### User Profile
```
GET  /api/profile/    → Get authenticated user profile
PUT  /api/profile/    → Update authenticated user profile
GET  /user/{username}/ → Get public user profile
```

### Projects
```
GET  /find-collaborators/        → List all projects (searchable)
POST /post-project/              → Create new project
GET  /project-detail/{id}/       → View project details
POST /edit-project/{id}/         → Update project
POST /delete-project/{id}/       → Delete project
POST /like-project/{id}/         → Like/unlike project
```

### Messaging
```
GET  /api/chat-rooms/            → List user's chat rooms
POST /api/chat-rooms/            → Create new chat room
GET  /api/messages/              → List messages in room
POST /api/messages/              → Send message
POST /api/direct-message/        → Start 1-on-1 chat
GET  /api/conversations/         → List all conversations
```

### Comments
```
GET  /api/projects/{id}/comments/  → Get project comments
POST /api/projects/{id}/comments/  → Add comment
PUT  /api/comments/{id}/           → Edit comment
DELETE /api/comments/{id}/         → Delete comment
```

### Social
```
POST /follow/{user_id}/           → Follow user
POST /connect/{user_id}/          → Send connection request
GET  /my-connections/             → List connections
POST /accept-connection/{id}/      → Accept connection
GET  /activity-feed/              → View activity stream
GET  /notifications/              → View notifications
```

---

## Database Query Examples

### Get Current User's Projects
```python
from .models import Project
from django.contrib.auth.models import User

# In a view
projects = Project.objects.filter(owner=request.user).order_by('-created_at')

# With related data (avoid N+1)
projects = Project.objects.filter(owner=request.user)\
    .select_related('owner')\
    .prefetch_related('comments', 'likes')\
    .order_by('-created_at')
```

### Search Projects
```python
from django.db.models import Q

search_term = 'AI'
projects = Project.objects.filter(
    Q(title__icontains=search_term) | 
    Q(description__icontains=search_term)
)
```

### Get User's Connections
```python
from .models import Connection

# Sent requests
sent = Connection.objects.filter(sender=request.user, status='pending')

# Received requests
received = Connection.objects.filter(receiver=request.user, status='pending')

# Accepted connections
connections = Connection.objects.filter(status='accepted')\
    .filter(Q(sender=request.user) | Q(receiver=request.user))
```

### Get Message History
```python
from .models import Message

# Get messages in a room, ordered by time
messages = Message.objects.filter(room=chat_room)\
    .select_related('sender')\
    .order_by('-created_at')[:50]  # Last 50 messages
```

---

## Template Cheat Sheet

### Display User Profile
```django
{{ user.username }}
{{ user.student_profile.full_name }}
{{ user.student_profile.profile_photo.url }}
{{ user.student_profile.bio }}
```

### Loop Through Projects
```django
{% for project in projects %}
    <div class="project-card">
        <h3>{{ project.title }}</h3>
        <p>{{ project.description }}</p>
        <p>By {{ project.owner.student_profile.full_name }}</p>
        <a href="{% url 'project_detail' project.id %}">View</a>
    </div>
{% empty %}
    <p>No projects found.</p>
{% endfor %}
```

### Display Comments
```django
{% for comment in project.comments.all %}
    <div class="comment">
        <strong>{{ comment.author.username }}</strong>
        <p>{{ comment.content }}</p>
        <small>{{ comment.created_at|date:"M d, Y" }}</small>
    </div>
{% endfor %}
```

### Forms
```django
<form method="post">
    {% csrf_token %}
    {{ form.as_p }}
    <button type="submit">Submit</button>
</form>
```

### Messages (Flash messages)
```django
{% if messages %}
    {% for message in messages %}
        <div class="alert alert-{{ message.tags }}">
            {{ message }}
        </div>
    {% endfor %}
{% endif %}
```

---

## Settings.py Key Configuration

### Database
```python
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': os.getenv('DB_NAME'),
        'USER': os.getenv('DB_USER'),
        'PASSWORD': os.getenv('DB_PASSWORD'),
        'HOST': os.getenv('DB_HOST', 'localhost'),
        'PORT': os.getenv('DB_PORT', '5432'),
    }
}
```

### Cache (Redis)
```python
CACHES = {
    'default': {
        'BACKEND': 'django_redis.cache.RedisCache',
        'LOCATION': os.getenv('REDIS_URL', 'redis://127.0.0.1:6379/1'),
    }
}
```

### WebSocket (Channels)
```python
CHANNEL_LAYERS = {
    'default': {
        'BACKEND': 'channels_redis.core.RedisChannelLayer',
        'CONFIG': {
            'hosts': [(os.getenv('REDIS_HOST', '127.0.0.1'), 6379)],
        },
    },
}
```

### Email
```python
EMAIL_BACKEND = 'accounts.brevo_mail_backend.BrevoEmailBackend'
EMAIL_HOST_USER = os.getenv('BREVO_API_KEY')
DEFAULT_FROM_EMAIL = os.getenv('EMAIL_FROM', 'noreply@unisync.com')
```

---

## Debugging Tips

### Enable Debug Mode
```python
# In settings.py
DEBUG = True

# Logs to console and file
LOGGING = {
    'version': 1,
    'handlers': {
        'console': {
            'class': 'logging.StreamHandler',
        },
        'file': {
            'class': 'logging.FileHandler',
            'filename': 'logs/debug.log',
        },
    },
    'loggers': {
        'accounts': {
            'handlers': ['console', 'file'],
            'level': 'DEBUG',
        },
    },
}
```

### Add Print Statements
```python
def my_view(request):
    print(f"User: {request.user}")
    projects = Project.objects.all()
    print(f"Projects: {projects.count()}")
    return render(request, 'template.html')
```

### Use Django Shell
```bash
python manage.py shell

>>> from accounts.models import Project
>>> Project.objects.count()
42
>>> p = Project.objects.first()
>>> print(p.title)
'AI Chat App'
```

### Query Logging
```python
# In settings.py (development only)
LOGGING = {
    'loggers': {
        'django.db.backends': {
            'level': 'DEBUG',
        },
    },
}
```

---

## Performance Optimization Tips

### 1. Use select_related() for ForeignKey
```python
# ✅ Good
projects = Project.objects.select_related('owner')

# ❌ Bad
projects = Project.objects.all()
for p in projects:
    print(p.owner.username)  # N database queries
```

### 2. Use prefetch_related() for reverse relations
```python
# ✅ Good
projects = Project.objects.prefetch_related('comments')

# ❌ Bad
projects = Project.objects.all()
for p in projects:
    print(p.comments.count())  # N database queries
```

### 3. Cache frequently accessed data
```python
from django.core.cache import cache

# Cache for 5 minutes
cache.set('user_projects', projects, timeout=300)

# Retrieve from cache
cached = cache.get('user_projects')
```

### 4. Use only() and defer() to limit fields
```python
# Only retrieve needed fields
projects = Project.objects.only('id', 'title', 'owner_id')

# Defer expensive fields
projects = Project.objects.defer('description')
```

### 5. Use values() or values_list() for aggregations
```python
# Get only needed columns
project_ids = Project.objects.values_list('id', 'title')

# Aggregate data
from django.db.models import Count
stats = Project.objects.values('category').annotate(count=Count('id'))
```

---

## Testing Patterns

### Unit Test Example
```python
from django.test import TestCase
from .models import Project
from django.contrib.auth.models import User

class ProjectModelTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user('testuser', 'test@example.com', 'pwd123')
    
    def test_project_creation(self):
        project = Project.objects.create(
            owner=self.user,
            title="Test Project",
            description="Test Description"
        )
        self.assertEqual(project.title, "Test Project")
        self.assertEqual(project.owner, self.user)
```

### API Test Example
```python
from rest_framework.test import APIClient
from django.test import TestCase

class ProjectAPITests(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create_user('testuser', 'test@example.com', 'pwd123')
    
    def test_project_list(self):
        response = self.client.get('/api/projects/')
        self.assertEqual(response.status_code, 200)
```

---

## Environment Variables (.env) Template

```env
# Server
DEBUG=True
SECRET_KEY=your-secret-key-here
ALLOWED_HOSTS=localhost,127.0.0.1

# Database
DATABASE_URL=postgresql://user:password@localhost:5432/unisync

# Cache & WebSocket
REDIS_URL=redis://localhost:6379/0
REDIS_HOST=localhost

# Email
BREVO_API_KEY=your-brevo-api-key
EMAIL_FROM=noreply@unisync.com

# OAuth
GOOGLE_OAUTH_CLIENT_ID=your-google-client-id
GOOGLE_OAUTH_SECRET=your-google-secret
GITHUB_OAUTH_CLIENT_ID=your-github-client-id
GITHUB_OAUTH_SECRET=your-github-secret

# Security
SECURE_SSL_REDIRECT=False
SESSION_COOKIE_SECURE=False
CSRF_COOKIE_SECURE=False
```

---

## Useful Links

- Django Docs: https://docs.djangoproject.com/
- DRF Docs: https://www.django-rest-framework.org/
- Django Channels: https://channels.readthedocs.io/
- django-allauth: https://django-allauth.readthedocs.io/

---

## Common Errors & Solutions

### Error: `User matching query does not exist`
```python
# ❌ Wrong
user = User.objects.get(id=999)  # Raises DoesNotExist

# ✅ Right
user = User.objects.filter(id=999).first()  # Returns None
user = User.objects.get_or_create(id=999)[0]
```

### Error: `Database integrity error`
```python
# ✅ Use atomic transactions
from django.db import transaction

@transaction.atomic
def create_project_with_team(request):
    project = Project.objects.create(...)
    ProjectTeam.objects.create(project=project)
```

### Error: `CSRF token missing or incorrect`
```django
<!-- ✅ Add CSRF token in forms -->
<form method="post">
    {% csrf_token %}
    <input type="submit">
</form>
```

### Error: `Permission denied`
```python
# ✅ Check permissions
if request.user != project.owner:
    return HttpResponseForbidden("Not your project")
```

---

## Quick Command Reference

```bash
# Install dependencies
pip install -r requirements.txt

# Run migrations
python manage.py migrate

# Create superuser
python manage.py createsuperuser

# Run development server
python manage.py runserver 0.0.0.0:8000

# Run tests
python manage.py test

# Open Django shell
python manage.py shell

# Collect static files
python manage.py collectstatic --noinput

# Check for issues
python manage.py check --deploy

# Start Channels worker
python manage.py runworker -v 3

# Start Redis
redis-server

# Create backup
pg_dump $DATABASE_URL > backup.sql
```

---

This reference guide covers the most essential information needed to work with UniSync. Refer to the comprehensive analysis documents for deeper details on specific components.
