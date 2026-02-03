# UniSync Code Reference - Quick Start

## 🚀 Project Overview
**Type**: Django REST API + Web Application  
**Purpose**: Student collaboration & project matching platform  
**Tech Stack**: Django 4.2, PostgreSQL, Redis, Channels, DRF  
**Status**: Production-ready  

---

## 📍 File Locations (Key Files)

```
e:/login/auth_project/
├── auth_project/
│   ├── settings.py          (356+ lines) - Configuration
│   ├── urls.py              (60 lines)   - URL routing
│   ├── wsgi.py              - Production server
│   └── asgi.py              - WebSocket support
├── accounts/
│   ├── models.py            (718 lines) - Database models
│   ├── views.py             (3311+ lines) - View functions
│   ├── forms.py             (583+ lines) - Form validation
│   ├── serializers.py       - REST serializers
│   ├── urls.py              (120 lines) - API routes
│   ├── permissions.py       - Custom permissions
│   ├── chat_api.py          - Messaging endpoints
│   ├── utils.py             - Helper functions
│   ├── views_contact.py     - Contact page
│   ├── auth_service.py      - Auth logic
│   ├── brevo_mail_backend.py - Email (Brevo)
│   ├── zepto_mail_backend.py - Email (ZeptoMail)
│   └── migrations/          - Database migrations
├── templates/               - HTML templates
├── static/                  - CSS/JS files
├── media/                   - User uploads
└── requirements.txt         - Dependencies
```

---

## 🗄️ Core Models (Quick Reference)

### User Models
```python
# Core user (Django built-in)
User.objects.filter(username='john')

# Extended profile
StudentProfile
  - full_name, college, location, bio
  - profile_photo (image)
  - skills, interests (JSON arrays)
  - social links (GitHub, LinkedIn, etc.)

# User stats
UserStats
  - projects_created, connections_made
  - likes_received, tasks_completed
```

### Authentication
```python
# OTP model
OTP
  - email, otp_code, purpose (login/register/reset)
  - expires_at (5 minutes)
  - is_used flag

# Get OTP
otp = OTP.objects.get(email='user@example.com', is_used=False)
otp.verify_otp('123456')  # Returns (bool, message)

# Generate OTP
new_otp = OTP.generate_otp('user@example.com', 'login')
```

### Projects
```python
# Main project model
Project
  - title, description, owner
  - visibility (public/private/invite-only)
  - skills_required (JSON), members_needed
  - category, status, timestamps

# Project team members
ProjectMember
  - project, user, role (owner/admin/contributor/viewer)
  - permissions based on role

# Project invitations
ProjectInvitation
  - project, invited_user, invited_by
  - status (pending/accepted/declined/expired)
  - role assignment

# Project tasks
ProjectTask
  - title, description, assigned_to
  - status (todo/in_progress/review/completed)
  - priority (low/medium/high/urgent)
  - due_date

# Project milestones
ProjectMilestone
  - title, due_date, is_completed
  - completion tracking
```

### Messaging
```python
# Messages
Message
  - sender, receiver (or chat_room for group)
  - content, message_type (text/file/image/call)
  - reply_to (threading)

# Chat rooms (group chat)
ChatRoom
  - name, chat_type (direct/group)
  - members (via ChatRoomMember)

# Read status (scalable)
MessageReadStatus
  - message, user, read_at
  - get_read_count(), get_unread_users()

# Message reactions
MessageReaction
  - message, user, reaction (emoji)

# File attachments
MessageFile → File relationship
```

### Social
```python
# Connection requests
Connection
  - sender, receiver
  - status (pending/accepted/rejected)

# Following
Follow
  - follower, following

# Activity feed
Activity
  - user, activity_type
  - title, description
  - related object (project, connection, etc.)

# Notifications
Notification
  - user, title, description
  - is_read flag

# Project interactions
Like
  - project, user

Comment
  - project/message, user, content
```

---

## 🔑 Key Functions & Methods

### Authentication Service
```python
# File: accounts/services/auth_service.py

# Login with OTP
from accounts.services.auth_service import generate_otp, verify_otp

# Generate OTP
otp_obj = OTP.generate_otp('user@example.com', 'login')
# Email sent automatically

# Verify OTP
otp = OTP.objects.get(email='user@example.com')
is_valid, message = otp.verify_otp('123456')

# Password reset
from accounts.views import reset_password_view
```

### Project Filtering
```python
# File: accounts/utils.py - ProjectVisibilityFilter

from accounts.utils import ProjectVisibilityFilter

filter = ProjectVisibilityFilter(user)
# Filters projects based on visibility & permissions

public_projects = filter.get_visible_projects()
owned_projects = filter.get_owned_projects()
invited_projects = filter.get_invited_projects()
```

### StudentProfile NLP
```python
# File: accounts/utils.py - StudentProfileNLP

from accounts.utils import StudentProfileNLP

nlp = StudentProfileNLP(profile)
skills = nlp.extract_skills()
interests = nlp.extract_interests()
score = nlp.compatibility_score(other_profile)
```

### Email Sending
```python
# Automatic backend selection in settings.py
from django.core.mail import send_mail

send_mail(
    subject='Hello',
    message='Content',
    from_email='noreply@unisync.app',
    recipient_list=['user@example.com'],
)
```

---

## 📊 Common Query Examples

### Get User's Projects
```python
from accounts.models import Project

# Own projects
projects = Project.objects.filter(owner=request.user)

# Joined projects
projects = Project.objects.filter(members=request.user)

# Public projects
public = Project.objects.filter(visibility='public')

# With pagination
from django.core.paginator import Paginator
paginator = Paginator(projects, 10)
page = paginator.get_page(1)
```

### Get User Messages
```python
from accounts.models import Message, MessageReadStatus

# Received messages
messages = Message.objects.filter(receiver=request.user)

# Mark as read
for msg in messages:
    msg.mark_as_read_by(request.user)

# Get unread count
unread = Message.objects.filter(
    receiver=request.user
).exclude(
    read_statuses__user=request.user
).count()

# Get read receipts
readers = msg.get_read_by_users()
read_count = msg.get_read_count()
```

### Get Connections
```python
from accounts.models import Connection

# Sent requests
sent = Connection.objects.filter(
    sender=request.user,
    status='pending'
)

# Received requests
received = Connection.objects.filter(
    receiver=request.user,
    status='pending'
)

# Accepted connections
connected = Connection.objects.filter(
    models.Q(sender=request.user) | models.Q(receiver=request.user),
    status='accepted'
)
```

### Get User Stats
```python
from accounts.models import UserStats

stats = request.user.userstats
stats.update_stats()  # Update all stats

# Access stats
print(stats.projects_created)
print(stats.followers_count)
print(stats.connections_made)
```

---

## 🔌 REST API Endpoints

### Authentication
```
POST   /login/                 - Login
POST   /register/              - Register
GET    /logout/                - Logout
POST   /verify-otp/<purpose>/  - Verify OTP
POST   /resend-otp/<purpose>/  - Resend OTP
POST   /forgot-password/       - Reset password
POST   /reset-password/        - Complete reset
```

### User/Profile
```
GET    /student-profile/       - View profile
POST   /student-details/       - Update profile
GET    /user/<username>/       - View user profile
GET    /user-profile/<id>/     - API endpoint
POST   /edit-profile/          - Edit profile
GET    /user-stats/            - Get statistics
```

### Projects
```
GET    /explore-projects/      - Browse projects
GET    /my-projects/           - User's projects
POST   /post-project/          - Create project
GET    /project/<id>/          - Project details
PUT    /edit-project/<id>/     - Edit project
DELETE /delete-project/<id>/   - Delete project
POST   /like-project/<id>/     - Like project
GET    /search_projects/       - Search projects
```

### Messaging
```
GET    /messages/              - Message list
POST   /messages/              - Send message
GET    /chat/<user_id>/        - Direct chat
GET    /conversations/         - List conversations
POST   /messages/<id>/status/  - Mark read
POST   /messages/<id>/reactions/ - Add reaction
POST   /chat-rooms/            - Create group
GET    /chat-rooms/<id>/       - Group details
POST   /typing/                - Typing indicator
```

### Social
```
GET    /activity-feed/         - Activity feed
GET    /notifications/         - Notifications
POST   /mark-notification-read/<id>/ - Mark read
GET    /my-connections/        - Connections
POST   /connect/<user_id>/     - Send request
POST   /accept-connection/<id>/ - Accept
POST   /reject-connection/<id>/ - Reject
POST   /follow/<user_id>/      - Follow user
GET    /find-collaborators/    - Find partners
```

---

## 🛠️ View Functions (Key)

### Authentication Views
```python
# File: accounts/views.py

def login_view(request):
    # Handle login with username/email or OTP

def register_view(request):
    # User registration with StudentProfile creation

def verify_otp_view(request, purpose):
    # Verify OTP code, create user session

def forgot_password_view(request):
    # Send OTP for password reset

def reset_password_view(request):
    # Verify OTP, update password
```

### Profile Views
```python
def student_profile(request):
    # Display user's profile

def edit_profile(request):
    # Edit profile with avatar upload

def user_profile(request, username):
    # View other user's profile

class UserProfileView(generics.RetrieveUpdateAPIView):
    # REST API endpoint for profile
```

### Project Views
```python
def post_project(request):
    # Create new project

def edit_project(request, project_id):
    # Edit project (owner only)

def project_detail(request, project_id):
    # View project details

def like_project(request, project_id):
    # Like/unlike project

def explore_projects_view(request):
    # Browse all projects with filtering
```

### Messaging Views
```python
def message_view(request):
    # List messages

def chat_view(request, user_id):
    # Direct message chat with user

def enhanced_chat_view(request, room_id):
    # Group chat view

class MessageListCreateView(generics.ListCreateAPIView):
    # REST API for messages
```

---

## 📝 Forms

### Register Form
```python
from accounts.forms import RegisterForm

# Fields: username, email, password1, password2, terms_agree
# Validation:
#   - Username: 3-150 chars, not taken
#   - Email: valid, not taken
#   - Password: 8+ chars, upper, lower, digit
```

### Login Form
```python
from accounts.forms import LoginForm

# Fields: username/email, password
# Optional: remember_me
```

### Student Profile Form
```python
from accounts.forms import StudentProfileForm

# Fields: full_name, college, bio, profile_photo, etc.
# File validation: JPG, PNG, GIF only
```

### Project Form
```python
from accounts.forms import ProjectForm

# Fields: title, description, skills_required, visibility
# Validation: Required fields, valid JSON arrays
```

---

## ⚙️ Environment Variables

```env
# Core
DEBUG=True/False
SECRET_KEY=your_secret_key
ALLOWED_HOSTS=localhost,127.0.0.1

# Database
DATABASE_URL=postgresql://user:pass@host:5432/db
# OR individual vars:
DB_NAME=unisync_db
DB_USER=unisync_user
DB_PASSWORD=password
DB_HOST=localhost
DB_PORT=5432

# Email
BREVO_API_KEY=your_brevo_key
# OR
ZEPTO_MAIL_API_KEY=your_zepto_key
ZEPTO_MAIL_TOKEN=your_token
# OR
EMAIL_HOST_USER=your_email@gmail.com
EMAIL_HOST_PASSWORD=your_password

# Social Auth
GOOGLE_CLIENT_ID=your_google_id
GOOGLE_CLIENT_SECRET=your_google_secret
GITHUB_CLIENT_ID=your_github_id
GITHUB_CLIENT_SECRET=your_github_secret

# External APIs
RAPIDAPI_KEY=your_rapidapi_key

# Optional
SECURE_SSL_REDIRECT=False
SESSION_COOKIE_SECURE=False
CSRF_COOKIE_SECURE=False
DEFAULT_FROM_EMAIL=noreply@unisync.app
```

---

## 🚀 Running the Application

### Development Server
```bash
cd auth_project

# Install dependencies
pip install -r requirements.txt

# Create migrations
python manage.py makemigrations

# Apply migrations
python manage.py migrate

# Create superuser
python manage.py createsuperuser

# Run server
python manage.py runserver
# Access: http://localhost:8000
```

### Production Deployment
```bash
# Collect static files
python manage.py collectstatic --noinput

# Run with gunicorn
gunicorn auth_project.wsgi --bind 0.0.0.0:8000
```

---

## 📚 Useful Management Commands

```bash
# Create test user
python manage.py shell
>>> from django.contrib.auth.models import User
>>> User.objects.create_user('testuser', 'test@example.com', 'password123')

# Reset database
python manage.py flush

# Create superuser
python manage.py createsuperuser

# Check for issues
python manage.py check

# View SQL queries
python manage.py sqlmigrate accounts 0001

# Create sample data
python manage.py shell < create_test_user.py
```

---

## 🧪 Testing

### Run Tests
```bash
# Run all tests
pytest

# Run specific test
pytest auth_project/test_login.py

# Run with coverage
pytest --cov=accounts

# Run Django tests
python manage.py test accounts
```

### Test Files Available
- test_login.py
- test_email.py
- test_profile_*.py
- test_filter.py
- test_feed_fix.py
- test_services.py

---

## 📊 Useful Debugging

### Django Shell
```bash
python manage.py shell

# Query examples
from accounts.models import Project, User
user = User.objects.first()
projects = Project.objects.filter(owner=user)

# OTP testing
from accounts.models import OTP
otp = OTP.generate_otp('test@example.com', 'login')
print(otp.otp_code)  # Print OTP to console
```

### View Logs
```bash
# Application logs
tail -f auth_project/logs/django.log

# Error logs only
tail -f auth_project/logs/error.log
```

---

## 🔒 Security Checklist

- [ ] Set SECRET_KEY in production
- [ ] Set DEBUG=False in production
- [ ] Configure DATABASE_URL for PostgreSQL
- [ ] Setup email backend (Brevo recommended)
- [ ] Configure ALLOWED_HOSTS
- [ ] Enable HTTPS (SECURE_SSL_REDIRECT=True)
- [ ] Set secure cookies (SESSION_COOKIE_SECURE=True)
- [ ] Configure CSRF protection
- [ ] Setup Sentry monitoring
- [ ] Enable rate limiting
- [ ] Rotate API keys regularly

---

## 📞 Support & Resources

### Django Documentation
- https://docs.djangoproject.com/

### Django REST Framework
- https://www.django-rest-framework.org/

### Django Channels (WebSockets)
- https://channels.readthedocs.io/

### django-allauth (Social Login)
- https://django-allauth.readthedocs.io/

### Project Repository
- https://github.com/Goku0090/uni

---

**Created**: February 02, 2025  
**UniSync Version**: 2025 Q1  
**Status**: Production Ready
