# UniSync Quick Start Guide

**For developers new to the codebase**

---

## What is UniSync?

UniSync is a web platform that helps university students find collaborators and manage projects together. Think of it as a combination of LinkedIn (for professional connections), GitHub (for project management), and Slack (for team communication).

**Key Users:**
- Students looking for project team members
- Investors seeking promising student projects
- Professors managing capstone projects

---

## Project Structure at a Glance

```
auth_project/
├── manage.py              ← Run commands with this
├── requirements.txt       ← Python dependencies
│
├── accounts/              ← Main application
│   ├── views.py           ← Page logic and API endpoints
│   ├── models.py          ← Database structure
│   ├── urls.py            ← URL routing
│   ├── forms.py           ← Form definitions
│   ├── templates/         ← HTML pages
│   ├── static/            ← CSS, JS, images
│   ├── comment_api.py     ← Comment functionality
│   ├── chat_api.py        ← Messaging functionality
│   └── [other files]      ← Supporting modules
│
├── auth_project/          ← Django configuration
│   ├── settings.py        ← Main settings file
│   ├── urls.py            ← Project URL routing
│   └── [other files]      ← WSGI/ASGI
│
└── [other folders]        ← Media, logs, static files
```

---

## Installation in 5 Minutes

### Step 1: Clone & Navigate
```bash
git clone https://github.com/Goku0090/uni.git
cd auth_project
```

### Step 2: Virtual Environment
```bash
# Windows
python -m venv venv
venv\Scripts\activate

# macOS/Linux
python -m venv venv
source venv/bin/activate
```

### Step 3: Install Dependencies
```bash
pip install -r requirements.txt
```

### Step 4: Configure Environment
```bash
cp .env.template .env
# Edit .env with your settings (see below)
```

### Step 5: Run
```bash
python manage.py migrate
python manage.py runserver
# Open http://localhost:8000
```

---

## Essential .env Variables

```bash
# Minimal setup for local development
DEBUG=True
SECRET_KEY=your-secret-key-here
ALLOWED_HOSTS=localhost,127.0.0.1

# Email (use console for testing)
# Leave empty to print OTP to console

# Database (SQLite by default)
# Don't set DB_* variables for SQLite
```

---

## Core Features Explained

### 1. User Registration & Login

**File:** `views.py` → `register_view()`, `login_view()`

**Flow:**
```
User enters email/password
      ↓
Email validation
      ↓
6-digit OTP sent to email
      ↓
User enters OTP
      ↓
Account created
      ↓
Student profile initialized
```

**Models:**
- `User` - Django's built-in user model
- `StudentProfile` - Extended profile with college, skills, interests
- `OTP` - One-time password for verification

---

### 2. Projects

**File:** `views.py` → `post_project()`, `project_detail()`

**What users can do:**
- Create a project with title, description, needed skills/roles
- Set visibility: public, private, or friends-only
- Add team members with different roles (owner, admin, contributor, viewer)
- Track tasks and milestones
- Like projects, comment on them

**Models:**
```
Project → ProjectMember → User
        → ProjectTask
        → ProjectMilestone
        → Comment
        → Like
```

---

### 3. Messaging

**File:** `chat_api.py`, `chat_api_improved.py`

**Features:**
- Direct messages between users
- Group chat rooms
- File sharing
- Message read receipts
- Reactions (emoji)
- Message threading/replies

**Models:**
```
ChatRoom → ChatRoomMember → User
        → Message
                ├─ MessageFile
                ├─ MessageReaction
                └─ MessageReadStatus
```

---

### 4. Social Features

**Files:** `views.py` with various social endpoints

**Features:**
- Connect with other students (connection requests)
- Follow users to see their activity
- Like projects
- Get notifications
- View activity feed

**Models:**
```
Connection - Request to connect
Follow - Subscribe to user activity
Like - Like on a project
Activity - Log of user actions
Notification - Notify users of events
```

---

### 5. Comments & Live Feed

**File:** `comment_api.py`

**Features:**
- Comment on projects
- Reply to comments (threading)
- Edit/delete your comments
- Real-time updates

**API Endpoints:**
```
GET    /api/projects/<id>/comments/         - Get all comments
POST   /api/projects/<id>/comments/add/     - Add comment
POST   /api/comments/<id>/edit/             - Edit comment
DELETE /api/comments/<id>/delete/           - Delete comment
```

---

## Most Important Files to Know

### 1. `models.py` - Database Schema
**Why:** Defines all data structures  
**Key Models:**
- `User`, `StudentProfile` - User data
- `Project`, `ProjectMember` - Projects
- `Message`, `ChatRoom` - Messaging
- `Comment` - Comments
- `Connection`, `Follow` - Social

### 2. `views.py` - Main Logic
**Why:** Handles all page requests and API calls  
**Key Functions:**
- `login_view()` - Login logic
- `register_view()` - Registration
- `post_project()` - Create project
- `project_detail()` - View project
- `message_view()` - Messaging page

### 3. `urls.py` - URL Routing
**Why:** Maps URLs to functions  
**Example:**
```
/accounts/login/        → login_view()
/accounts/post-project/ → post_project()
/api/messages/          → MessageListCreateView
```

### 4. `settings.py` - Configuration
**Why:** Django settings, email, database, etc.  
**Key Sections:**
- `INSTALLED_APPS` - Active apps
- `DATABASES` - Database config
- `EMAIL_BACKEND` - Email service
- `SOCIALACCOUNT_PROVIDERS` - OAuth

### 5. `forms.py` - Input Validation
**Why:** Validates user input  
**Examples:**
- Login form validation
- Project creation validation
- Profile update validation

### 6. `comment_api.py` - Comments
**Why:** All comment operations  
**Functions:**
- `add_comment()` - Create comment
- `get_comments()` - Fetch comments
- `edit_comment()` - Update comment
- `delete_comment()` - Remove comment

### 7. `chat_api.py` - Messaging
**Why:** All messaging operations  
**Key Classes:**
- `ChatRoomListCreateView` - Create chat rooms
- `MessageListCreateView` - Send/receive messages
- `DirectMessageView` - DM functionality

---

## Common Development Tasks

### Task 1: Add a New Page

**Steps:**
1. Create template in `accounts/templates/my_page.html`
2. Add view function in `views.py`
3. Add URL in `urls.py`
4. Add link in base template

**Example:**
```python
# views.py
def my_page(request):
    data = {}
    return render(request, 'my_page.html', data)

# urls.py
path('my-page/', views.my_page, name='my_page'),
```

### Task 2: Create a New API Endpoint

**Steps:**
1. Create serializer in `serializers.py` (if needed)
2. Create view class in `views.py` or separate file
3. Add URL in `urls.py`

**Example:**
```python
# views.py
from rest_framework.views import APIView
from rest_framework.response import Response

class MyAPIView(APIView):
    def get(self, request):
        return Response({'message': 'Hello'})

# urls.py
from rest_framework.urls import path
path('api/my-endpoint/', MyAPIView.as_view(), name='my-api'),
```

### Task 3: Add a Database Model

**Steps:**
1. Create model in `models.py`
2. Create migration: `python manage.py makemigrations`
3. Apply migration: `python manage.py migrate`

**Example:**
```python
# models.py
class MyModel(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField()
    created_at = models.DateTimeField(default=timezone.now)
```

### Task 4: Send an Email

**Code:**
```python
from django.core.mail import send_mail

send_mail(
    subject='Welcome to UniSync',
    message='Thanks for signing up!',
    from_email='noreply@unisync.app',
    recipient_list=['user@example.com'],
)
```

### Task 5: Debug an Issue

**Tools:**
```bash
# Django shell - test code interactively
python manage.py shell
>>> from accounts.models import User
>>> User.objects.all()

# Check database
python manage.py dbshell
# Then run SQL commands

# Enable debug toolbar (add to INSTALLED_APPS in settings.py)
# Visit http://localhost:8000/__debug__/

# Check logs
cat logs/django.log
```

---

## Key Concepts

### OTP (One-Time Password)
- 6-digit code sent to email
- Expires after 5 minutes
- Cannot be reused (marked as `is_used = True`)
- Used for login, registration, password reset

### Project Visibility
- **public** - Anyone can see and join
- **private** - Only owner can see
- **friends_only** - Only connected users can see

### Message Read Status
- Tracked separately via `MessageReadStatus` model
- Not a boolean on Message (for scalability)
- Shows who has read the message

### Comment Threading
- Comments can reply to other comments
- Uses `reply_to` field (self-referencing ForeignKey)
- Forms a tree structure

### Activity Feed
- Logs major user actions (created project, liked, commented, etc.)
- Used to show activity to followers
- Timestamps for chronological ordering

---

## Testing the Application

### Test an Endpoint
```bash
# Using curl
curl http://localhost:8000/api/projects/

# Using Python requests
python
>>> import requests
>>> r = requests.get('http://localhost:8000/api/projects/')
>>> r.json()
```

### Test Email
```bash
python manage.py shell
>>> from django.core.mail import send_mail
>>> send_mail('Test', 'This is a test', 'from@example.com', ['to@example.com'])
```

### Test OTP
```bash
python manage.py shell
>>> from accounts.models import OTP
>>> otp = OTP.generate_otp('user@example.com', 'login')
>>> print(otp.otp_code)  # In console mode, will print to screen
```

---

## Deployment Checklist

- [ ] Set `DEBUG = False` in .env
- [ ] Configure `SECRET_KEY`
- [ ] Set up PostgreSQL database
- [ ] Configure email backend
- [ ] Set up social authentication keys
- [ ] Run migrations: `python manage.py migrate`
- [ ] Collect static: `python manage.py collectstatic`
- [ ] Run security check: `python manage.py check --deploy`
- [ ] Set up HTTPS/SSL
- [ ] Configure allowed hosts

---

## Useful Commands

```bash
# Run server
python manage.py runserver

# Create migrations
python manage.py makemigrations

# Apply migrations
python manage.py migrate

# Create admin user
python manage.py createsuperuser

# Access admin panel
# Navigate to http://localhost:8000/admin/

# Run tests
python manage.py test

# Django shell (interactive Python)
python manage.py shell

# Database shell
python manage.py dbshell

# Collect static files
python manage.py collectstatic

# Clear cache
python manage.py clear_cache

# Check for issues
python manage.py check
python manage.py check --deploy

# See all available commands
python manage.py help
```

---

## Common Error Messages & Solutions

| Error | Cause | Solution |
|-------|-------|----------|
| ModuleNotFoundError: No module named 'accounts' | Missing INSTALLED_APPS | Add 'accounts' to INSTALLED_APPS in settings.py |
| ProgrammingError: relation "accounts_user" does not exist | Database not migrated | Run `python manage.py migrate` |
| SMTPAuthenticationError | Wrong email credentials | Check EMAIL_HOST_USER and EMAIL_HOST_PASSWORD |
| DoesNotExist: User matching query does not exist | User not found | Check user_id or use .filter() instead of .get() |
| ConnectionRefusedError (Redis) | Redis not running | Start Redis: `redis-server` |
| CSRF token missing or incorrect | CSRF protection issue | Ensure {% csrf_token %} in POST forms |

---

## Next Steps to Learn

1. **Read the code:** Start with `views.py` and `models.py`
2. **Add a feature:** Implement a simple new page or endpoint
3. **Run tests:** Execute `python manage.py test` to see what breaks
4. **Deploy:** Try deploying to Render or Railway
5. **Optimize:** Profile the application and find bottlenecks

---

## Resources

- **Django Docs:** https://docs.djangoproject.com/
- **DRF Docs:** https://www.django-rest-framework.org/
- **PostgreSQL:** https://www.postgresql.org/docs/
- **Bootstrap:** https://getbootstrap.com/docs/
- **GitHub Issues:** Check the uni repo for reported issues

---

## Questions?

Check these files first:
1. `COMPREHENSIVE_CODEBASE_ANALYSIS_2025.md` - Architecture overview
2. `API_ENDPOINTS_REFERENCE_2025.md` - All API endpoints
3. `TECHNICAL_STACK_GUIDE_2025.md` - Dependencies and setup
4. Code comments in relevant files

---

*Last Updated: February 3, 2025*
