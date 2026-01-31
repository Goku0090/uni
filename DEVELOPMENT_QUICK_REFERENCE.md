# UniSync Development Quick Reference

## Project Setup

### Environment Variables (.env)
```env
# Django Settings
DEBUG=True
SECRET_KEY=your-secret-key-here
ALLOWED_HOSTS=localhost,127.0.0.1

# Database (Optional - defaults to SQLite in dev)
DATABASE_URL=postgresql://user:password@localhost:5432/unisync_db
# OR
DB_NAME=unisync_db
DB_USER=unisync_user
DB_PASSWORD=password
DB_HOST=localhost
DB_PORT=5432
DB_SSLMODE=prefer

# Email (Choose one backend)
BREVO_API_KEY=your-brevo-key
# OR
ZEPTO_MAIL_API_KEY=your-zepto-key
ZEPTO_MAIL_TOKEN=your-zepto-token
# OR
EMAIL_HOST_USER=your-email@gmail.com
EMAIL_HOST_PASSWORD=your-password

DEFAULT_FROM_EMAIL=noreply@unisync.app

# Social OAuth
GOOGLE_CLIENT_ID=your-google-client-id
GOOGLE_CLIENT_SECRET=your-google-secret
GITHUB_CLIENT_ID=your-github-client-id
GITHUB_CLIENT_SECRET=your-github-secret

# API Keys
RAPIDAPI_KEY=your-rapidapi-key

# SSL (Production)
SECURE_SSL_REDIRECT=False
SESSION_COOKIE_SECURE=False
CSRF_COOKIE_SECURE=False
```

### Installation Steps
```bash
# 1. Clone and setup
git clone https://github.com/Goku0090/uni.git
cd login/auth_project

# 2. Create virtual environment
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate

# 3. Install dependencies
pip install -r requirements.txt

# 4. Create .env file
cp .env.template .env
# Edit .env with your settings

# 5. Run migrations
python manage.py makemigrations
python manage.py migrate

# 6. Create superuser
python manage.py createsuperuser

# 7. Collect static files
python manage.py collectstatic --noinput

# 8. Run development server
python manage.py runserver
```

Visit: http://localhost:8000

---

## Common Commands

### Database Operations
```bash
# Make migrations
python manage.py makemigrations

# Apply migrations
python manage.py migrate

# Revert to previous migration
python manage.py migrate accounts 0001

# Show migration status
python manage.py showmigrations

# Reset database (dev only)
python manage.py flush

# Create superuser
python manage.py createsuperuser

# Load fixtures
python manage.py loaddata fixture_name
```

### Development Server
```bash
# Run development server
python manage.py runserver

# Run on specific port
python manage.py runserver 8080

# Run on all interfaces
python manage.py runserver 0.0.0.0:8000
```

### Shell & Debugging
```bash
# Django shell with models imported
python manage.py shell

# Within shell:
from accounts.models import *
user = User.objects.first()
user.student_profile.full_name

# Run tests
python -m pytest
python -m pytest accounts/tests.py -v
```

### Static & Media Files
```bash
# Collect static files
python manage.py collectstatic --noinput

# Clean old static files
python manage.py collectstatic --clear
```

---

## Code Patterns & Examples

### Creating a User with Profile

```python
from django.contrib.auth.models import User
from accounts.models import StudentProfile

# Create user
user = User.objects.create_user(
    username='john_doe',
    email='john@example.com',
    password='SecurePass123'
)

# Create profile
profile = StudentProfile.objects.create(
    user=user,
    full_name='John Doe',
    college='MIT',
    location='Boston, MA',
    skills=['python', 'javascript'],
    project_interests=['web_dev', 'ai'],
    profile_completed=True
)
```

### Sending OTP

```python
from accounts.models import OTP
from django.core.mail import send_mail
from django.conf import settings

# Generate OTP
otp = OTP.generate_otp(email='user@example.com', purpose='login')

# Send via email
send_mail(
    subject='Your OTP Code',
    message=f'Your OTP is: {otp.otp_code}',
    from_email=settings.DEFAULT_FROM_EMAIL,
    recipient_list=[otp.email],
    fail_silently=False
)
```

### Verifying OTP

```python
from accounts.models import OTP

email = 'user@example.com'
otp_code = '123456'
purpose = 'login'

try:
    otp = OTP.objects.get(email=email, purpose=purpose, is_used=False)
    is_valid, message = otp.verify_otp(otp_code)
    if is_valid:
        # OTP verified, mark user as authenticated
        pass
except OTP.DoesNotExist:
    # No valid OTP found
    pass
```

### Creating a Project

```python
from accounts.models import Project
from django.contrib.auth.models import User

user = User.objects.first()
project = Project.objects.create(
    user=user,
    title='AI Chat Bot',
    description='Building an intelligent chatbot using NLP',
    category='ai',
    technologies=['python', 'tensorflow', 'flask'],
    looking_for=['backend_dev', 'ml_engineer'],
    timeline='2-3 months',
    collaboration_needs='Looking for ML engineers to improve NLP models',
    visibility='public',
    github_link='https://github.com/user/chatbot-project'
)
```

### Adding Team Members

```python
from accounts.models import Project, ProjectMember, ProjectInvitation
from django.utils import timezone

project = Project.objects.first()
target_user = User.objects.get(username='collaborator')

# Create invitation
invitation = ProjectInvitation.objects.create(
    project=project,
    invited_user=target_user,
    invited_by=project.user,
    role='contributor',
    message='Join our awesome project!',
    expires_at=timezone.now() + timezone.timedelta(days=7)
)

# Later, when user accepts:
invitation.accept()  # Creates ProjectMember with role='contributor'
```

### Sending a Message

```python
from accounts.models import Message
from django.utils import timezone

sender = User.objects.get(username='user1')
receiver = User.objects.get(username='user2')

message = Message.objects.create(
    sender=sender,
    receiver=receiver,
    content='Hey, how are you?',
    message_type='text'
)

# Mark as read
message.mark_as_read_by(receiver)
```

### Creating Project Tasks

```python
from accounts.models import Project, ProjectTask
from django.utils import timezone
import datetime

project = Project.objects.first()
assigned_to = User.objects.get(username='developer')

task = ProjectTask.objects.create(
    project=project,
    title='Implement login feature',
    description='Add OTP-based login functionality',
    assigned_to=assigned_to,
    assigned_by=project.user,
    status='todo',
    priority='high',
    due_date=datetime.date.today() + datetime.timedelta(days=7)
)

# Update status
task.status = 'in_progress'
task.save()

# Mark as completed
task.mark_completed()
```

### Using NLP Utilities

```python
from accounts.utils import StudentProfileNLP

text = "I'm proficient in Python, JavaScript, and React. Interested in web development and AI."

# Extract skills
skills = StudentProfileNLP.extract_skills(text)
# Output: ['python', 'javascript', 'react', 'web_dev', 'ai']

# Categorize interests
interests = StudentProfileNLP.categorize_interests(text)
# Output: {'web_dev': [...], 'ai_ml': [...]}

# Find similar profiles (for recommendations)
profile1 = StudentProfile.objects.first()
profile2 = StudentProfile.objects.get(pk=2)
similarity = StudentProfileNLP.calculate_profile_similarity(profile1, profile2)
```

### Filtering Projects

```python
from accounts.models import Project
from accounts.utils import ProjectVisibilityFilter

user = User.objects.first()

# Get visible projects for user
filter = ProjectVisibilityFilter(user)
visible_projects = filter.get_visible_projects()

# Filter by category
filter.filter_by_category('web')

# Filter by technology
filter.filter_by_technology('django')

# Get collaborative projects
collaborative = filter.get_collaborative_projects()
```

### REST API Usage

```python
# In a Django view or API endpoint
from rest_framework.response import Response
from rest_framework import status

# Create response
return Response({
    'status': 'success',
    'data': serializer.data
}, status=status.HTTP_200_OK)

# Error response
return Response({
    'status': 'error',
    'message': 'Invalid data'
}, status=status.HTTP_400_BAD_REQUEST)
```

---

## Model Query Examples

### Users & Profiles
```python
# Get user with profile
user = User.objects.select_related('student_profile').get(pk=1)

# Get all users with completed profiles
completed_profiles = StudentProfile.objects.filter(profile_completed=True)

# Get user's follower count
follower_count = Follow.objects.filter(following=user).count()
```

### Projects
```python
# Get user's projects
projects = Project.objects.filter(owner=user).order_by('-created_at')

# Get popular projects (by likes)
popular = Project.objects.order_by('-likes_count')[:10]

# Get projects by category
web_projects = Project.objects.filter(category='web')

# Get public projects
public = Project.objects.filter(visibility='public')
```

### Messages
```python
# Get unread messages
from accounts.models import MessageReadStatus

unread = Message.objects.exclude(
    id__in=MessageReadStatus.objects.filter(user=user).values('message_id')
)

# Get conversation between two users
from django.db.models import Q
conversation = Message.objects.filter(
    Q(sender=user1, receiver=user2) | Q(sender=user2, receiver=user1)
).order_by('created_at')

# Get messages in a chat room
room_messages = Message.objects.filter(chat_room=room).order_by('-created_at')
```

### Connections
```python
# Get pending connection requests
pending = Connection.objects.filter(receiver=user, status='pending')

# Get accepted connections
connections = Connection.objects.filter(
    (Q(sender=user) | Q(receiver=user)) & Q(status='accepted')
)
```

---

## Common Issues & Solutions

### Issue: OTP Not Sending
**Solution:**
1. Check email backend configuration in settings.py
2. Verify API keys are set in .env
3. Check logs: `logs/django.log`
4. Test with console backend (temporarily set in settings.py)

```python
# Temporary testing
EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'
```

### Issue: Social Login Not Working
**Solution:**
1. Verify OAuth credentials in .env
2. Check that SocialApp is configured in admin
3. Verify redirect URIs match OAuth provider settings
4. Check SOCIALACCOUNT_PROVIDERS in settings.py

### Issue: Database Connection Error
**Solution:**
1. Verify PostgreSQL is running
2. Check DATABASE_URL or DB_* environment variables
3. Run migrations: `python manage.py migrate`
4. Falls back to SQLite if PostgreSQL not configured

### Issue: Static Files Not Loading
**Solution:**
```bash
# Collect static files
python manage.py collectstatic --noinput --clear

# For development, serve from STATICFILES_DIRS
# settings.py: STATICFILES_DIRS = [BASE_DIR / 'static']
```

### Issue: CSRF Token Missing
**Solution:**
1. Include {% csrf_token %} in all POST forms
2. For AJAX, include CSRF token in headers
3. Check that CsrfViewMiddleware is enabled

### Issue: Permission Denied on Upload
**Solution:**
1. Check MEDIA_ROOT directory permissions
2. Verify MEDIA_ROOT is writable by Django process
3. Check file permissions: `chmod -R 755 media/`

---

## File Structure Overview

```
auth_project/
├── auth_project/              # Django config
│   ├── settings.py           # Main configuration
│   ├── urls.py               # URL routing
│   ├── wsgi.py               # Production server
│   └── asgi.py               # WebSocket server
│
├── accounts/                  # Main application
│   ├── models.py             # Database schemas (20+ models)
│   ├── views.py              # Views (3193 lines, needs splitting)
│   ├── forms.py              # Django forms (5+ forms)
│   ├── urls.py               # App URL patterns
│   ├── serializers.py        # REST API serializers
│   ├── utils.py              # Utilities (NLP, filtering)
│   ├── permissions.py        # Permission classes
│   ├── chat_api.py           # Messaging API views
│   ├── chat_api_improved.py  # Enhanced chat
│   ├── views_contact.py      # Contact pages
│   ├── brevo_mail_backend.py # Email backend
│   ├── zepto_mail_backend.py # Email backend
│   ├── services/
│   │   └── auth_service.py   # Auth business logic
│   ├── migrations/           # Database migrations
│   ├── templates/accounts/   # HTML templates
│   │   ├── base.html
│   │   ├── login.html
│   │   ├── register.html
│   │   ├── dashboard.html
│   │   └── ...
│   ├── static/               # CSS, JS, images
│   ├── templatetags/         # Custom template tags
│   └── tests.py              # Tests (needs expansion)
│
├── static/                    # Project-wide static files
│   ├── css/
│   ├── js/
│   └── images/
│
├── media/                     # User uploads
│   └── profile_photos/
│
├── logs/                      # Application logs
│   ├── django.log
│   └── error.log
│
├── manage.py                  # Django CLI
├── requirements.txt           # Python dependencies
└── .env.template              # Environment template
```

---

## Testing Guide

### Running Tests
```bash
# Run all tests
python -m pytest

# Run specific test file
python -m pytest accounts/tests.py

# Run with verbose output
python -m pytest accounts/tests.py -v

# Run specific test
python -m pytest accounts/tests.py::TestLogin -v
```

### Writing Tests
```python
# accounts/tests.py
import pytest
from django.contrib.auth.models import User
from accounts.models import StudentProfile

@pytest.mark.django_db
class TestStudentProfile:
    def test_create_profile(self):
        user = User.objects.create_user(
            username='test',
            email='test@example.com',
            password='test123'
        )
        profile = StudentProfile.objects.create(user=user)
        assert profile.user == user
```

---

## Performance Tips

### Database Optimization
```python
# ❌ Bad (N+1 queries)
projects = Project.objects.all()
for p in projects:
    print(p.owner.username)  # Extra query for each project

# ✅ Good
projects = Project.objects.select_related('owner')
for p in projects:
    print(p.owner.username)  # No extra queries

# For reverse foreign keys
projects = Project.objects.prefetch_related('comments')
for p in projects:
    for c in p.comments.all():
        print(c.text)  # No extra queries
```

### Caching
```python
from django.core.cache import cache

# Cache user profile
cache_key = f'profile_{user.id}'
profile = cache.get(cache_key)
if not profile:
    profile = StudentProfile.objects.get(user=user)
    cache.set(cache_key, profile, 3600)  # Cache for 1 hour
```

### Query Optimization
```python
# Use only() for partial data
users = User.objects.only('id', 'username')

# Use values() or values_list() for dictionaries
users = User.objects.values('id', 'username', 'email')

# Batch operations
User.objects.bulk_create([user1, user2, user3])
User.objects.filter(id__in=ids).bulk_update(users, batch_size=100)
```

---

## Deployment Guide

### Render.com Deployment
```bash
# 1. Push to GitHub
git push origin main

# 2. Connect GitHub to Render
# - Go to Render.com dashboard
# - Create new Web Service
# - Connect GitHub repo

# 3. Set environment variables in Render dashboard
# DATABASE_URL (auto-provided by Render PostgreSQL)
# EMAIL backend vars
# ALLOWED_HOSTS=your-app.onrender.com
# DEBUG=False
# SECRET_KEY=your-secret

# 4. Add render.yaml for configuration
```

### Gunicorn Production Server
```bash
# Install
pip install gunicorn

# Run
gunicorn auth_project.wsgi --workers 4 --bind 0.0.0.0:8000

# With systemd service
[Service]
ExecStart=/path/to/venv/bin/gunicorn auth_project.wsgi --workers 4
```

---

## Useful Links

- **Django Documentation:** https://docs.djangoproject.com/
- **Django REST Framework:** https://www.django-rest-framework.org/
- **django-allauth:** https://django-allauth.readthedocs.io/
- **Channels (WebSockets):** https://channels.readthedocs.io/
- **PostgreSQL:** https://www.postgresql.org/
- **Brevo Email API:** https://www.brevo.com/
- **RapidAPI:** https://rapidapi.com/

---

**Last Updated:** 2026-01-29  
**Compatible with:** Django 4.2.8, Python 3.8+
