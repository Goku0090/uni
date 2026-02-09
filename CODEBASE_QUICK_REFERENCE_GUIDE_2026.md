# UniSinq Platform - Quick Reference Guide
**Last Updated:** Feb 09, 2026

---

## 🎯 At a Glance

| Aspect | Details |
|--------|---------|
| **Project Type** | Django Web Application (Full-stack) |
| **Purpose** | Student Collaboration & Networking Platform |
| **Main Directory** | `/auth_project/` |
| **Core App** | `accounts` |
| **Database** | PostgreSQL (production), SQLite (dev) |
| **Real-time** | WebSockets via Django Channels |
| **API Framework** | Django REST Framework (DRF) |
| **Python Version** | 3.8+ |
| **Django Version** | 3.2+ |

---

## 📁 Directory Map

```
auth_project/
├── auth_project/          # Project settings & config
│   ├── settings.py        ⭐ Database, apps, email, OAuth config
│   ├── urls.py            ⭐ URL routing (main urls)
│   ├── asgi.py            ⭐ WebSocket routing (Channels)
│   └── wsgi.py            WSGI server config
│
├── accounts/              # Main application
│   ├── models.py          ⭐ 15+ database models
│   ├── views.py           ⭐ 50+ view functions
│   ├── urls.py            ⭐ View URL mapping
│   ├── serializers.py     ⭐ REST API serializers
│   ├── consumers.py       ⭐ WebSocket consumers
│   ├── routing.py         ⭐ WebSocket routing
│   ├── signals_realtime.py Real-time signal handlers
│   ├── chat_api.py        Messaging API logic
│   ├── comment_api.py     Comments API logic
│   ├── template_api.py    Templates API logic
│   ├── forms.py           Django forms
│   ├── permissions.py     Custom permissions
│   ├── utils.py           Utility functions
│   ├── services/          Business logic services
│   ├── static/            CSS, JS, images
│   ├── templates/         HTML templates
│   ├── migrations/        Database migrations
│   └── management/        Custom commands
│
├── manage.py              ⭐ Django management CLI
├── requirements.txt       ⭐ Python dependencies
├── .env                   ⭐ Environment variables
└── db.sqlite3             SQLite database (dev)

⭐ = Most important files
```

---

## 🗄️ Key Database Models (15+)

### User & Authentication
- **User** (Django default)
- **StudentProfile** - Bio, skills, interests, college
- **UserStatus** - Online/offline tracking
- **OTP** - Login/registration verification

### Projects
- **Project** - Main project model
- **ProjectMember** - Team members with roles
- **ProjectTask** - To-do items in project
- **ProjectMilestone** - Project phases
- **ProjectTemplate** - Pre-made blueprints
- **ProjectInvitation** - Team invitations

### Social
- **Connection** - Friend requests
- **Follow** - User following
- **Like** - Project likes
- **Comment** - Comments on projects

### Messaging
- **ChatRoom** - Direct/group chat
- **Message** - Chat messages
- **MessageReaction** - Message emoji reactions
- **MessageReadStatus** - Read receipts

### Other
- **Notification** - User notifications

---

## 🔧 Most Important Files (Quick Find)

| Task | File | Key Function |
|------|------|--------------|
| Add database field | `models.py` | Create model field |
| Create new page | `views.py` | Add view function |
| Create new API | `serializers.py` + `urls.py` | Add serializer + URL |
| WebSocket events | `consumers.py` | Add consumer method |
| Add button/feature | `templates/` | Edit HTML |
| Fix style | `static/css/` | Edit CSS |
| Setup OAuth | `settings.py` | Configure provider |
| Email template | `templates/` | Create email HTML |
| Permission logic | `permissions.py` | Create permission class |
| API response | `serializers.py` | Define serializer fields |
| URL routing | `urls.py` | Map path to view |
| Background task | `tasks.py` (if exists) or signals | Add handler |

---

## 📋 View/Endpoint Cheat Sheet

### Authentication
```
POST /register/                    # Register new user
POST /login/                       # User login
POST /verify-otp/                  # Verify OTP
POST /logout/                      # User logout
GET  /password-reset/              # Reset password form
```

### Projects
```
GET  /post-project/                # Create project form
POST /post-project/                # Submit new project
GET  /project/<id>/                # View project
POST /project/<id>/like/           # Like project
POST /project/<id>/unlike/         # Unlike project
GET  /search/                      # Search projects
```

### Collaboration
```
GET  /find-collaborators/          # Find collaborators
POST /connect/<user_id>/           # Send connection request
GET  /my-connections/              # View connections
POST /accept/<user_id>/            # Accept connection
```

### Profiles
```
GET  /profile/<user_id>/           # View user profile
GET  /my-profile/                  # My profile
POST /my-profile/                  # Update my profile
```

### Messaging
```
GET  /messages/                    # Message list
GET  /direct/<user_id>/            # Direct message thread
POST /direct/<user_id>/            # Send message
GET  /group-chat/                  # Group chats
```

### REST API
```
GET  /api/user-profile/<id>/       # Get user data
POST /api/direct-message/<user>/   # Send DM (API)
GET  /api/chat-rooms/              # List chats (API)
POST /api/projects/                # Create project (API)
GET  /api/projects/                # List projects (API)
```

---

## 🔌 WebSocket Events

### ProjectUpdateConsumer
```python
# Channels
projects_{project_id}

# Events
- project_update
- member_joined
- comment_added
- task_updated
```

### ChatConsumer
```python
# Channels
chat_room_{room_id}

# Events
- message_sent
- message_reaction
- typing_indicator
- message_deleted
```

### NotificationConsumer
```python
# Channels
notifications_{user_id}

# Events
- notification_created
- notification_read
```

---

## 🔐 Authentication Methods

1. **Email OTP** (Primary)
   - User enters email → OTP sent → Verify OTP → Login

2. **Google OAuth** (Social)
   - Configured via `django-allauth`
   - Set in `settings.py`: `SOCIALACCOUNT_PROVIDERS`

3. **Session-based** (Traditional)
   - Django session framework
   - Cookie: `sessionid`

---

## 🔑 Environment Variables (.env)

```bash
# Database
DATABASE_URL=postgresql://user:pass@host:5432/dbname

# Email
BREVO_API_KEY=your_brevo_key
ZEPTO_API_KEY=your_zepto_key
EMAIL_FROM=noreply@example.com

# OAuth
GOOGLE_OAUTH_CLIENT_ID=xxx.apps.googleusercontent.com
GOOGLE_OAUTH_SECRET=xxx

# Django
SECRET_KEY=your-secret-key
DEBUG=False
ALLOWED_HOSTS=example.com,www.example.com

# URLs
SITE_URL=https://example.com
CALLBACK_URL=https://example.com/oauth/callback

# Redis (optional)
REDIS_URL=redis://localhost:6379
```

---

## 🚀 Common Commands

### Django Management
```bash
# Migrations
python manage.py makemigrations              # Create migration
python manage.py migrate                     # Apply migrations
python manage.py showmigrations              # Show migrations

# Database
python manage.py flush --noinput             # Reset database
python manage.py dumpdata > backup.json      # Backup
python manage.py loaddata backup.json        # Restore

# Users
python manage.py createsuperuser             # Create admin
python manage.py shell                       # Python shell

# Static files
python manage.py collectstatic --noinput     # Collect static files

# Tests
python manage.py test                        # Run tests
python manage.py test accounts               # Run app tests

# Server
python manage.py runserver                   # Run dev server
```

### WebSocket Server
```bash
# Terminal 1: Django
python manage.py runserver

# Terminal 2: Daphne (WebSocket)
daphne -b 0.0.0.0 -p 8001 auth_project.asgi:application
```

---

## 🐛 Debugging Tips

### Check User Profile
```python
# In Django shell
python manage.py shell

from django.contrib.auth.models import User
from accounts.models import StudentProfile

user = User.objects.get(username='john')
profile = user.studentprofile
print(profile.bio, profile.skills.all())
```

### Check Messages
```python
from accounts.models import Message

messages = Message.objects.filter(room_id=1)
for msg in messages:
    print(f"{msg.sender}: {msg.content}")
```

### Check Connections
```python
from accounts.models import Connection

pending = Connection.objects.filter(status='pending')
for conn in pending:
    print(f"{conn.requester} → {conn.receiver}")
```

### View WebSocket Connections
```
Check browser DevTools → Network → WS tab
```

### Check Email Sending
```python
from django.core.mail import send_mail

send_mail(
    'Test Subject',
    'Test message',
    'from@example.com',
    ['to@example.com'],
    fail_silently=False,
)
```

---

## 📊 Common API Response Patterns

### Success (200)
```json
{
  "id": 123,
  "username": "john",
  "email": "john@example.com",
  "status": "success"
}
```

### List with Pagination
```json
{
  "count": 100,
  "next": "http://api.example.com/projects/?page=2",
  "previous": null,
  "results": [
    { "id": 1, "title": "Project 1" },
    { "id": 2, "title": "Project 2" }
  ]
}
```

### Error (400/500)
```json
{
  "error": "Invalid email",
  "detail": "Email already registered"
}
```

---

## 🎨 Template Tags & Filters

Common template usage in HTML:
```django
{% if user.is_authenticated %}
  <p>Welcome, {{ user.first_name }}!</p>
{% endif %}

{% for project in projects %}
  <h2>{{ project.title }}</h2>
  <p>{{ project.created_at|date:"Y-m-d" }}</p>
{% endfor %}

{% if projects %}
  <p>Found {{ projects.count }} projects</p>
{% else %}
  <p>No projects found</p>
{% endif %}
```

---

## 🔗 URL Patterns Quick Lookup

```python
# In accounts/urls.py

urlpatterns = [
    # Auth
    path('register/', views.register, name='register'),
    path('login/', views.login, name='login'),
    path('logout/', views.logout, name='logout'),
    
    # Projects
    path('post-project/', views.post_project, name='post_project'),
    path('project/<int:id>/', views.project_detail, name='project_detail'),
    
    # Profiles
    path('profile/<int:user_id>/', views.view_profile, name='view_profile'),
    path('my-profile/', views.student_profile, name='student_profile'),
    
    # Collaboration
    path('find-collaborators/', views.find_collaborators, name='find_collaborators'),
    path('connect/<int:user_id>/', views.send_connection_request, name='connect'),
    
    # Messaging
    path('messages/', views.message_list, name='messages'),
    path('direct/<int:user_id>/', views.start_direct_message, name='direct_message'),
    
    # API
    path('api/user-profile/<int:id>/', api.user_profile_api),
    path('api/projects/', api.ProjectListCreateAPIView.as_view()),
    # ... more API endpoints
]
```

---

## 🧠 Key Concepts

### Model Relationships
```
- **1:1** User ← → StudentProfile
- **1:M** Project → ProjectMember (team)
- **M:M** ChatRoom ← → User (members)
- **FK** ProjectMember.user → User
- **Self-referential** Comment.parent_comment → Comment
- **GenericFK** Notification.content_object → Any model
```

### View Types
```
- Function-based views (FBV): @csrf_exempt, @login_required
- Class-based views (CBV): APIView, ViewSet
- API views (DRF): ListCreateAPIView, RetrieveUpdateDestroyAPIView
```

### Decorators
```python
@login_required          # Require user to be logged in
@csrf_exempt             # Skip CSRF token check
@permission_required     # Check specific permission
@api_view(['GET', 'POST'])  # DRF: Allow specific methods
```

### Signals
```python
from django.db.models.signals import post_save
from django.dispatch import receiver

@receiver(post_save, sender=Project)
def notify_followers(sender, instance, created, **kwargs):
    if created:
        # Do something when Project is created
```

---

## 🧪 Testing Quick Start

```python
# accounts/tests.py

from django.test import TestCase, Client
from django.contrib.auth.models import User
from accounts.models import Project

class ProjectTestCase(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username='john',
            password='testpass123'
        )
        self.project = Project.objects.create(
            owner=self.user,
            title='Test Project',
            description='Test'
        )
    
    def test_project_creation(self):
        self.assertEqual(self.project.title, 'Test Project')
        self.assertEqual(self.project.owner, self.user)
    
    def test_project_view(self):
        client = Client()
        response = client.get(f'/project/{self.project.id}/')
        self.assertEqual(response.status_code, 200)
```

---

## 📦 Installing Dependencies

```bash
# Create virtual environment
python -m venv venv
source venv/Scripts/activate  # Windows: venv\Scripts\activate

# Install from requirements.txt
pip install -r requirements.txt

# Or install individually
pip install Django==3.2.20
pip install djangorestframework==3.14.0
pip install django-channels==4.0.0
pip install psycopg2-binary
pip install python-dotenv
pip install Pillow

# Check installed packages
pip list
```

---

## 🔍 Useful Queries for Debugging

```python
# Check user's projects
user.project_set.all()

# Get unread notifications
Notification.objects.filter(recipient=user, is_read=False)

# Find connections status
Connection.objects.filter(requester=user, status='accepted')

# Get user's messages
Message.objects.filter(sender=user).order_by('-created_at')

# Find projects by tech stack
Project.objects.filter(tech_stack__name='Python')

# Get likes count for project
project.like_set.count()

# Check if user is online
user.userstatus.is_online

# Find active projects
Project.objects.filter(status='Active')
```

---

## 📚 File Structure Checklist

When adding new feature, ensure:
- [ ] Add model to `models.py`
- [ ] Create migration: `python manage.py makemigrations`
- [ ] Add view/API endpoint
- [ ] Add URL route
- [ ] Create template (if needed)
- [ ] Add permission class (if needed)
- [ ] Update test file
- [ ] Handle WebSocket event (if real-time)
- [ ] Add signal handler (if notification needed)

---

## 🚨 Common Errors & Fixes

### `ModuleNotFoundError: No module named 'X'`
```bash
pip install -r requirements.txt
```

### `TemplateDoesNotExist`
Check template file exists in `templates/` folder and path in view is correct.

### `Database locked` (SQLite only)
Use PostgreSQL for production. Or stop other processes using DB.

### `CSRF token missing or incorrect`
Add `{% csrf_token %}` to forms or `@csrf_exempt` to view.

### `User is not authenticated`
Wrap view with `@login_required` or check `request.user.is_authenticated` in view.

### WebSocket `403 Forbidden`
Check `ALLOWED_HOSTS` in `settings.py` and CSRF exemption for WebSocket routes.

---

## 📈 Performance Tips

1. **Use `select_related()` for ForeignKey**
   ```python
   projects = Project.objects.select_related('owner')
   ```

2. **Use `prefetch_related()` for reverse relations**
   ```python
   users = User.objects.prefetch_related('project_set')
   ```

3. **Add database indexes**
   ```python
   class Project(models.Model):
       title = models.CharField(max_length=200, db_index=True)
   ```

4. **Paginate large lists**
   ```python
   paginator = Paginator(objects, 10)
   page_obj = paginator.get_page(page_number)
   ```

5. **Cache expensive queries**
   ```python
   from django.views.decorators.cache import cache_page
   
   @cache_page(60)  # 60 seconds
   def expensive_view(request):
       pass
   ```

---

**For detailed information, see:**
- `COMPREHENSIVE_CODE_ANALYSIS_FINAL_2026.md` - Full analysis
- `ARCHITECTURE_DIAGRAM_VISUAL_2026.md` - Architecture diagrams
- `README.md` - Project README

---

**Last Updated:** Feb 09, 2026  
**Version:** 2.0  
**Status:** Complete ✅
