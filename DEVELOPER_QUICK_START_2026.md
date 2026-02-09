# 🚀 DEVELOPER QUICK START GUIDE 2026
## UniSync Platform - Complete Reference

---

## ⚡ SUPER QUICK START (5 minutes)

### 1. Clone & Setup
```bash
cd e:\login\auth_project
python -m venv venv
source venv/Scripts/activate  # Windows: venv\Scripts\activate
pip install -r requirements.txt
```

### 2. Configure Database
```bash
python manage.py migrate
python manage.py createsuperuser
```

### 3. Run Local Dev Server
```bash
# HTTP Only (no WebSocket)
python manage.py runserver

# OR with WebSocket support
pip install daphne==4.0.0
daphne -b 127.0.0.1 -p 8000 auth_project.asgi:application
```

### 4. Access Application
```
Homepage: http://localhost:8000/
Admin: http://localhost:8000/admin/
```

---

## 📁 PROJECT STRUCTURE QUICK REFERENCE

```
auth_project/
├── accounts/                  # Main app
│   ├── models.py             # Database models (15+ classes)
│   ├── views.py              # View functions (50+ endpoints)
│   ├── urls.py               # URL routing
│   ├── consumers.py           # WebSocket handlers
│   ├── routing.py            # WebSocket routing
│   ├── serializers.py        # REST API serializers
│   ├── forms.py              # Django forms
│   ├── utils.py              # Helper functions
│   │
│   ├── static/js/            # JavaScript
│   │   ├── realtime-updates.js   # WebSocket client
│   │   ├── api-utils.js          # API helpers
│   │   └── login.js              # Auth JS
│   │
│   ├── templates/            # HTML files
│   │   ├── dashboard.html
│   │   ├── project_detail.html
│   │   ├── profile.html
│   │   └── ...
│   │
│   ├── migrations/           # Database migrations
│   ├── services/             # Business logic
│   └── tests.py              # Unit tests
│
├── auth_project/             # Project config
│   ├── asgi.py              # ASGI (WebSocket)
│   ├── wsgi.py              # WSGI (HTTP)
│   ├── settings.py          # Django settings
│   └── urls.py              # Root URLs
│
├── media/                    # User uploads
├── static/                   # Static files
├── manage.py                 # Django CLI
└── requirements.txt          # Dependencies
```

---

## 🔑 KEY FILES TO KNOW

| File | Purpose | Key Classes/Functions |
|------|---------|----------------------|
| **models.py** | Database schema | User, Project, Message, Connection |
| **views.py** | HTTP endpoints | dashboard_view, post_project, chat_view |
| **consumers.py** | WebSocket handlers | ProjectUpdateConsumer, NotificationConsumer |
| **routing.py** | WebSocket URLs | websocket_urlpatterns |
| **serializers.py** | API data format | UserProfileSerializer, ProjectSerializer |
| **utils.py** | Helper functions | StudentProfileNLP, send_otp_email |
| **forms.py** | Form validation | ProjectForm, StudentProfileForm |
| **settings.py** | Configuration | Database, email, installed apps |
| **urls.py** | URL routing | All HTTP endpoints |
| **realtime-updates.js** | WebSocket client | RealtimeUpdates class |

---

## 🏗️ ARCHITECTURE AT A GLANCE

```
Browser (HTML/CSS/JS)
    ↓↑ HTTP/WebSocket
Django/Daphne Server
    ├─ urls.py (HTTP routes)
    ├─ routing.py (WebSocket routes)
    ├─ views.py (HTTP handlers)
    └─ consumers.py (WebSocket handlers)
    ↓↑
Models (Database ORM)
    ├─ User/Auth
    ├─ Projects
    ├─ Messages
    ├─ Social
    └─ Activity
    ↓↑
PostgreSQL/SQLite Database
```

---

## 📚 MAIN COMPONENTS EXPLAINED

### Models (Data Layer)
**What**: Database structure and relationships
**File**: `accounts/models.py`
**Key Models**:
- `StudentProfile`: User profile with skills, college, bio
- `Project`: Main project entity
- `Message`: Direct messages
- `Notification`: User notifications
- `Connection`: Friend requests
- `Activity`: Activity log
- `Comment`: Project comments
- `Like`: Like tracking

**Example**:
```python
# View all projects by a user
projects = Project.objects.filter(owner=user)

# Get all notifications for user
notifications = Notification.objects.filter(
    user=request.user, is_read=False
)
```

### Views (HTTP Layer)
**What**: Handle HTTP requests and return responses
**File**: `accounts/views.py`
**Common Views**:
- `register_view()`: User registration
- `dashboard_view()`: Main feed
- `post_project()`: Create project
- `view_project_detail()`: Show project
- `chat_view()`: Messaging
- `find_collaborators()`: Search users

**Example**:
```python
@login_required
def view_project_detail(request, project_id):
    project = get_object_or_404(Project, id=project_id)
    context = {
        'project': project,
        'comments': project.comment_set.all()
    }
    return render(request, 'project_detail.html', context)
```

### Templates (Frontend Layer)
**What**: HTML pages with Django template tags
**Folder**: `accounts/templates/`
**Features**:
- `{% for item in items %}` loops
- `{{ variable }}` variable interpolation
- `{% if condition %}` conditionals
- `{% csrf_token %}` CSRF protection
- `{% static 'path' %}` static files
- `{% url 'view_name' %}` URL generation

**Example**:
```html
<h1>{{ project.title }}</h1>
<p>{{ project.description }}</p>

{% if user.is_authenticated %}
  <button onclick="likeProject({{ project.id }})">
    Like ({{ project.like_set.count }})
  </button>
{% endif %}

<div id="comments">
  {% for comment in comments %}
    <div>{{ comment.author }} said: {{ comment.text }}</div>
  {% endfor %}
</div>
```

### WebSocket Consumers (Real-time)
**What**: Handle WebSocket connections for live updates
**File**: `accounts/consumers.py`
**Main Consumers**:
- `ProjectUpdateConsumer`: Project status updates
- `NotificationConsumer`: Push notifications
- `ActivityFeedConsumer`: Live activity feed

**Example**:
```python
class ProjectUpdateConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        # User connected to WebSocket
        await self.accept()
        
    async def receive(self, text_data):
        # User sent message
        data = json.loads(text_data)
        # Process and broadcast
        
    async def disconnect(self, code):
        # User disconnected
        pass
```

### JavaScript Client
**What**: Client-side real-time handling
**File**: `accounts/static/js/realtime-updates.js`
**Main Class**: `RealtimeUpdates`

**Example**:
```javascript
const realtime = new RealtimeUpdates();
realtime.init();  // Start WebSocket connections

// Manual WebSocket connection
const socket = new WebSocket("ws://localhost:8000/ws/project/2/");
socket.onopen = () => console.log("Connected");
socket.onmessage = (event) => {
    const data = JSON.parse(event.data);
    updateUI(data);
};
```

---

## 🔌 COMMON TASKS

### Add a New Model
```python
# 1. Edit accounts/models.py
class MyModel(models.Model):
    name = models.CharField(max_length=100)
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return self.name

# 2. Create migration
python manage.py makemigrations

# 3. Apply migration
python manage.py migrate

# 4. Register in admin (optional)
from django.contrib import admin
admin.site.register(MyModel)
```

### Add a New View
```python
# 1. Edit accounts/views.py
@login_required
def my_view(request):
    items = MyModel.objects.all()
    return render(request, 'my_template.html', {
        'items': items
    })

# 2. Edit accounts/urls.py
path('my-path/', views.my_view, name='my_view')

# 3. Create template
# accounts/templates/my_template.html
```

### Add API Endpoint
```python
# 1. Edit accounts/serializers.py
from rest_framework import serializers
class MySerializer(serializers.ModelSerializer):
    class Meta:
        model = MyModel
        fields = '__all__'

# 2. Edit accounts/views.py
from rest_framework.decorators import api_view
@api_view(['GET', 'POST'])
def my_api_view(request):
    if request.method == 'GET':
        items = MyModel.objects.all()
        serializer = MySerializer(items, many=True)
        return Response(serializer.data)

# 3. Edit accounts/urls.py
path('api/my-endpoint/', views.my_api_view)
```

### Add WebSocket Endpoint
```python
# 1. Create consumer in accounts/consumers.py
class MyConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        await self.accept()
    
    async def receive(self, text_data):
        # Handle message
        pass
    
    async def disconnect(self, code):
        pass

# 2. Add to accounts/routing.py
websocket_urlpatterns = [
    re_path(r'ws/my-endpoint/', consumers.MyConsumer.as_asgi()),
]

# 3. Connect in JavaScript
const socket = new WebSocket("ws://localhost:8000/ws/my-endpoint/");
```

### Modify Database Schema
```bash
# 1. Make changes to models.py
# 2. Create migration
python manage.py makemigrations

# 3. Review migration file
# 4. Apply migration
python manage.py migrate

# 5. For Django admin
python manage.py createsuperuser
# Visit /admin/
```

---

## 🧪 TESTING

### Run All Tests
```bash
python manage.py test
# or
pytest
```

### Run Specific Test
```bash
python manage.py test accounts.tests.ProjectTestCase
```

### Create Test
```python
# accounts/tests.py
from django.test import TestCase
from .models import Project

class ProjectTestCase(TestCase):
    def setUp(self):
        self.user = User.objects.create_user('test', 'test@test.com')
    
    def test_project_creation(self):
        project = Project.objects.create(
            owner=self.user,
            title='Test'
        )
        self.assertEqual(project.title, 'Test')
```

---

## 🐛 DEBUGGING

### Django Debug Toolbar
```python
# settings.py
INSTALLED_APPS = [
    'debug_toolbar',
]

MIDDLEWARE = [
    'debug_toolbar.middleware.DebugToolbarMiddleware',
]

INTERNAL_IPS = ['127.0.0.1']
```

### View SQL Queries
```python
from django.db import connection
from django.test.utils import CaptureQueriesContext

with CaptureQueriesContext(connection) as context:
    projects = Project.objects.all()
    for query in context.captured_queries:
        print(query['sql'])
```

### Print Debugging
```python
import logging
logger = logging.getLogger(__name__)

logger.debug("Debug message")
logger.info("Info message")
logger.error("Error message")
```

### Browser Console
```javascript
// Open DevTools with F12
console.log("Debug message");
console.error("Error");

// Check WebSocket
const socket = new WebSocket("ws://localhost:8000/ws/project/2/");
socket.onopen = () => console.log("✅ Connected!");
socket.onerror = (e) => console.error("❌ Error:", e);
```

---

## 🚀 DEPLOYMENT

### Local Testing
```bash
python manage.py runserver
# or
daphne -b 127.0.0.1 -p 8000 auth_project.asgi:application
```

### Production (Render/Railway)
```bash
# 1. Create Procfile
web: daphne -b 0.0.0.0 -p $PORT auth_project.asgi:application

# 2. Create requirements.txt (already done)

# 3. Connect repository
# 4. Set environment variables
# 5. Deploy (auto on git push)
```

### Environment Variables
```bash
# .env file (development)
DEBUG=True
SECRET_KEY=your-secret-key
DATABASE_URL=sqlite:///db.sqlite3
ALLOWED_HOSTS=localhost,127.0.0.1

# Render/Railway dashboard (production)
# Set all variables there
```

---

## 📊 DATABASE OPERATIONS

### Create Superuser
```bash
python manage.py createsuperuser
# Enter: username, email, password
```

### Access Database Shell
```bash
python manage.py dbshell
# SQL commands
```

### Django Shell
```bash
python manage.py shell

# Then:
from accounts.models import Project, User
user = User.objects.get(username='test')
projects = Project.objects.filter(owner=user)
```

### Reset Database (Development Only)
```bash
# Delete SQLite file
rm auth_project/db.sqlite3

# Recreate
python manage.py migrate
python manage.py createsuperuser
```

---

## 🔐 IMPORTANT SECURITY NOTES

### CSRF Token Required for POST
```html
<form method="POST">
    {% csrf_token %}
    <!-- form fields -->
</form>
```

### AJAX CSRF Token
```javascript
const csrfToken = document.querySelector('[name=csrfmiddlewaretoken]').value;
fetch(url, {
    method: 'POST',
    headers: { 'X-CSRFToken': csrfToken }
});
```

### Authentication Check
```python
# In views
@login_required
def my_view(request):
    # user is authenticated

# Manual check
if request.user.is_authenticated:
    # user logged in
```

### Permissions
```python
# Check project ownership
if project.owner != request.user:
    return HttpResponseForbidden()

# Using decorator
@user_passes_test(lambda u: u.is_staff)
def admin_view(request):
    pass
```

---

## 📞 TROUBLESHOOTING

### Port Already in Use
```bash
# Find process using port 8000
lsof -i :8000  # Mac/Linux
netstat -ano | findstr :8000  # Windows

# Kill process
kill -9 <PID>  # Mac/Linux
taskkill /PID <PID> /F  # Windows

# Use different port
python manage.py runserver 8001
```

### Database Locked (SQLite)
```bash
# Solution: Use PostgreSQL or close other connections
rm auth_project/db.sqlite3
python manage.py migrate
```

### WebSocket 404
```bash
# Solution: Use Daphne, not runserver
daphne -b 127.0.0.1 -p 8000 auth_project.asgi:application
```

### Module Not Found
```bash
# Activate virtual environment
source venv/Scripts/activate  # Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt
```

### Email Not Sending
```python
# Check settings
EMAIL_BACKEND = 'accounts.brevo_mail_backend.BrevoEmailBackend'
BREVO_API_KEY = 'your-key'

# Test
from django.core.mail import send_mail
send_mail('Test', 'Test message', 'from@example.com', ['to@example.com'])
```

---

## 📚 USEFUL COMMANDS

```bash
# Development Server
python manage.py runserver

# WebSocket Server
daphne -b 0.0.0.0 -p 8000 auth_project.asgi:application

# Database
python manage.py migrate
python manage.py makemigrations
python manage.py createsuperuser

# Static Files
python manage.py collectstatic

# Testing
python manage.py test
pytest

# Shell
python manage.py shell
python manage.py dbshell

# Admin
python manage.py changepassword username

# Clean Up
python manage.py flush  # WARNING: Deletes all data
```

---

## 🎯 DEVELOPMENT WORKFLOW

```
1. Create feature branch
   git checkout -b feature/my-feature

2. Make changes
   - Edit models.py
   - Create migrations
   - Run migrations
   - Edit views/templates
   - Test locally

3. Test thoroughly
   python manage.py test
   python manage.py runserver
   (Manual testing)

4. Commit changes
   git add .
   git commit -m "Add feature: my-feature"

5. Push to GitHub
   git push origin feature/my-feature

6. Create Pull Request
   (Request review)

7. Merge to main
   (Auto-deploy on production)
```

---

## 📖 FURTHER READING

| Topic | Resource |
|-------|----------|
| Django Docs | https://docs.djangoproject.com |
| Django Channels | https://channels.readthedocs.io |
| DRF Docs | https://www.django-rest-framework.org |
| Daphne | https://github.com/django/daphne |
| django-allauth | https://django-allauth.readthedocs.io |

---

## ✅ QUICK CHECKLIST

Before committing:
- [ ] Tests pass (`python manage.py test`)
- [ ] Code follows PEP 8 style
- [ ] Database migrations created
- [ ] No hardcoded secrets
- [ ] Error handling added
- [ ] Docstrings written
- [ ] CSRF tokens in forms
- [ ] Debug = False in production

Before deploying:
- [ ] All tests pass
- [ ] Environment variables set
- [ ] Database backed up
- [ ] Static files collected
- [ ] Migrations applied
- [ ] Email service configured
- [ ] WebSocket tested
- [ ] Deployment scripts ready

---

**Last Updated**: February 7, 2026
**Status**: Ready for Development ✅
**Next Steps**: Choose a feature to implement or bug to fix!
