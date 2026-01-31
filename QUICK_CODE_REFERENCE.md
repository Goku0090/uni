# UniSync - Quick Code Reference

## 30-Second Overview

**UniSync** = Django collaboration platform where students find teammates for projects.

**Core Loop**: Sign up → Post project → Search collaborators → Connect → Build team → Collaborate

---

## File Locations Cheat Sheet

| What | Where |
|------|-------|
| User authentication | `accounts/views.py` (lines 208-464) |
| User profiles | `accounts/models.py:StudentProfile` |
| Projects | `accounts/models.py:Project` + `accounts/views.py` (lines 1504-1720) |
| Messaging | `accounts/models.py:Message, ChatRoom` + `accounts/chat_api.py` |
| Collaboration | `accounts/views.py` (lines 1376-1500) |
| Forms validation | `accounts/forms.py` |
| Settings config | `auth_project/settings.py` |
| URL routing | `auth_project/urls.py` + `accounts/urls.py` |
| Email setup | `accounts/brevo_mail_backend.py`, `zepto_mail_backend.py` |
| Database schema | `accounts/models.py` |

---

## Key Models (At a Glance)

```python
# User
User (Django) → StudentProfile (OneToOne)
  Fields: full_name, college, interests, skills, profile_photo, bio

# Auth
OTP → email, otp_code, purpose, expires_at, is_used
Connection → sender, receiver, status (pending/accepted/rejected)

# Projects
Project → user, title, description, technologies, looking_for
ProjectTeam → project, members (through ProjectTeamMember)
ProjectTask → project, title, status, assigned_to
ProjectMilestone → project, title, due_date, is_completed
Like → user, project (project engagement)
Comment → user, project, content

# Messaging
Message → sender, receiver/chat_room, content, created_at
ChatRoom → chat_type (direct/group), name
ChatRoomMember → user, chat_room
MessageReadStatus → message, user, read_at

# Notifications & Activity
Notification → user, activity_type, content, is_read
Activity → user, activity_type, title, description
```

---

## Authentication Views

| View | Route | Method | Does |
|------|-------|--------|------|
| `register_view` | `/register/` | POST | Create user + StudentProfile |
| `login_view` | `/login/` | POST | Generate + send OTP |
| `verify_otp_view` | `/verify-otp/<purpose>/` | POST | Validate OTP, log in |
| `logout_view` | `/logout/` | GET | Destroy session |
| `forgot_password_view` | `/forgot-password/` | POST | Generate reset OTP |
| `reset_password_view` | `/reset-password/` | POST | Update password |
| `resend_otp_view` | `/resend-otp/<purpose>/` | POST | Resend OTP |

**Flow**: register → email OTP → verify OTP → login OR login → email OTP → verify → dashboard

---

## Project Views

| View | Route | Purpose |
|------|-------|---------|
| `post_project` | `/post-project/` | Create project, list mine |
| `project_detail` | `/project/<id>/` | View project + team + comments |
| `edit_project` | `/edit-project/<id>/` | Modify project |
| `delete_project` | `/delete-project/<id>/` | Remove project |
| `explore_projects_view` | `/explore-projects/` | Browse all projects |
| `my_projects_view` | `/my-projects/` | My projects list |
| `like_project` | `/project/<id>/like/` | Toggle like (AJAX) |
| `search_projects` | `/api/search-projects/` | Full-text search |

---

## Collaboration Views

| View | Route | Purpose |
|------|-------|---------|
| `find_collaborators` | `/find-collaborators/` | Search users by skills/interests |
| `send_connection_request` | `/connect/<user_id>/` | Request to connect |
| `accept_connection` | `/accept-connection/<id>/` | Approve request |
| `reject_connection` | `/reject-connection/<id>/` | Decline request |
| `my_connections` | `/my-connections/` | View my connections |

---

## Messaging & Notifications

| View | Route | Purpose |
|------|-------|---------|
| `message_view` | `/messages/` | Message inbox |
| `chat_view` | `/chat/<user_id>/` | 1:1 conversation |
| `notifications_view` | `/notifications/` | Notification list |
| `mark_notification_read` | `/notification/<id>/read/` | Mark as read |

---

## Important Code Snippets

### Registration Validation
```python
# Location: views.py lines 228-273
- Username: 3+ chars, not taken
- Email: valid format, case-insensitive, not taken
- Password: 8+ chars, uppercase, digit, matches confirm
- Terms: checkbox required
```

### OTP Generation
```python
# Location: models.py lines 94-117
OTP.generate_otp(email, purpose):
  - Create 6-digit code
  - Set 5-minute expiry
  - Deactivate old OTPs for same email/purpose
  - Return OTP object
```

### OTP Verification
```python
# Location: models.py lines 81-92
OTP.verify_otp(otp_code):
  - Check if valid (not used, not expired)
  - Compare code
  - Mark as used
  - Return (success, message)
```

### Email Sending
```python
# Location: views.py lines 136-196
send_otp_email(email, otp_code, purpose):
  - Create HTML + plaintext template
  - Send via EmailMultiAlternatives
  - Log success/failure
  - Notify admin on failure
```

### User Sanitization
```python
# Location: views.py lines 107-133
sanitize_input(text, max_length):
  - Strip HTML tags
  - Remove dangerous chars (<, >)
  - Trim whitespace
  - Apply length limit
```

### Find Collaborators with Filters
```python
# Location: views.py lines 1376-1500
find_collaborators(request):
  - Filter by: interests, skills, college, location
  - NLP similarity scoring
  - Connection status checking
  - Pagination
  - Activity aggregation
```

---

## Security Features

| Feature | Location | Status |
|---------|----------|--------|
| Password strength | forms.py | ✅ |
| Duplicate user checks | forms.py | ✅ |
| OTP generation | models.py | ✅ |
| OTP expiry (5 min) | models.py | ✅ |
| Input sanitization | views.py | ✅ |
| CSRF protection | settings.py | ❌ (disabled) |
| Rate limiting | - | ❌ (missing) |
| API authentication | - | ❌ (missing) |

---

## Email Setup

### Configuration (settings.py)
```python
EMAIL_BACKEND = 'accounts.brevo_mail_backend.BrevoBackend'
DEFAULT_FROM_EMAIL = os.getenv('DEFAULT_FROM_EMAIL')
BREVO_API_KEY = os.getenv('BREVO_API_KEY')
```

### Email Types
- **OTP Verification**: registration, login, password reset
- **Welcome Back**: after login
- **Team Invite**: project team invitation
- **Notifications**: new message, connection request

### Test Email
```bash
python manage.py shell
from django.core.mail import send_mail
send_mail('Test', 'Hello', 'noreply@unisync.com', ['user@example.com'])
```

---

## Database Models Hierarchy

```
User (Django built-in)
└── StudentProfile (OneToOne)
    ├── Projects (Owner)
    │   ├── ProjectTeam
    │   │   └── ProjectTeamMembers (roles)
    │   ├── ProjectTasks
    │   ├── ProjectMilestones
    │   ├── Comments
    │   └── Likes
    ├── Connections (Sender/Receiver)
    ├── Messages (Sender/Receiver)
    ├── ChatRooms (Members)
    ├── Notifications
    ├── Activity (Creator)
    └── Follow (Follower)
```

---

## Common Errors & Fixes

| Error | Cause | Fix |
|-------|-------|-----|
| `MultipleObjectsReturned` | Query returns > 1 result | Use `.first()` or filter more |
| `DoesNotExist` | Record not found | Use `get_object_or_404()` |
| `OTP expired` | > 5 minutes old | Call `resend_otp_view` |
| `Invalid OTP` | Wrong code entered | Retry or resend |
| `CSRF token missing` | CSRF disabled or form error | Enable CSRF middleware |
| `Email send failed` | Email service down | Check API key, email logs |
| `Profile not found` | StudentProfile doesn't exist | Create in signal or migration |
| `Duplicate username` | Username taken | Try different username |

---

## Configuration Quick Reference

### settings.py Key Variables
```python
DEBUG = os.getenv('DEBUG', 'True').lower() in ('true', '1', 't', 'yes')
SECRET_KEY = os.getenv('SECRET_KEY')
ALLOWED_HOSTS = os.getenv('ALLOWED_HOSTS', 'localhost,127.0.0.1').split(',')

# Database
DATABASE_URL = os.getenv('DATABASE_URL')  # PostgreSQL for production
DATABASES = {...}  # SQLite fallback for development

# Email
EMAIL_BACKEND = 'accounts.brevo_mail_backend.BrevoBackend'
DEFAULT_FROM_EMAIL = os.getenv('DEFAULT_FROM_EMAIL')

# Security
SECURE_SSL_REDIRECT = os.getenv('SECURE_SSL_REDIRECT', 'False').lower() == 'true'
SESSION_COOKIE_SECURE = os.getenv('SESSION_COOKIE_SECURE', 'False').lower() == 'true'
CSRF_COOKIE_SECURE = os.getenv('CSRF_COOKIE_SECURE', 'False').lower() == 'true'
```

### .env Template
```
# Django
DEBUG=True
SECRET_KEY=your-secret-key

# Database
DATABASE_URL=postgresql://user:pass@localhost/dbname
DB_NAME=unisync_db
DB_USER=unisync_user
DB_PASSWORD=password
DB_HOST=localhost
DB_PORT=5432

# Email
DEFAULT_FROM_EMAIL=noreply@unisync.com
BREVO_API_KEY=xxx
ZEPTO_API_KEY=xxx

# OAuth
GITHUB_CLIENT_ID=xxx
GITHUB_CLIENT_SECRET=xxx
GOOGLE_CLIENT_ID=xxx
GOOGLE_CLIENT_SECRET=xxx

# Security (production only)
ALLOWED_HOSTS=yourdomain.com
SECURE_SSL_REDIRECT=True
SESSION_COOKIE_SECURE=True
CSRF_COOKIE_SECURE=True
```

---

## Testing Quick Commands

```bash
# Run all tests
python manage.py test accounts

# Run specific test file
python manage.py test accounts.tests.TestLogin

# Run with verbosity
python manage.py test accounts -v 2

# Test email
python test_email.py

# Test login flow
python test_login.py

# Test connections
python test_connections.py

# Create test user
python create_test_user.py
```

---

## Deployment Commands

```bash
# Migrate database
python manage.py migrate

# Create superuser
python manage.py createsuperuser

# Collect static files
python manage.py collectstatic --noinput

# Run development server
python manage.py runserver

# Run production server (gunicorn)
gunicorn auth_project.wsgi:application --bind 0.0.0.0:8000

# Check for issues
python manage.py check --deploy
```

---

## View Function Template

```python
# Standard view template used throughout:
@login_required  # Protect if needed
def my_view(request):
    """Docstring describing what this view does"""
    
    if request.method == 'POST':
        # Handle form submission
        data = request.POST.get('field_name')
        
        try:
            # Process data
            messages.success(request, 'Success message')
            return redirect('next_page')
        except Exception as e:
            logger.error(f"Error: {str(e)}")
            messages.error(request, 'Error message')
            return redirect('current_page')
    
    # GET request - display form
    context = {
        'data': data,
    }
    return render(request, 'template.html', context)
```

---

## Model Query Examples

```python
# Get user's projects
projects = Project.objects.filter(user=request.user)

# Get active connections
connections = Connection.objects.filter(
    Q(sender=user, status='accepted') |
    Q(receiver=user, status='accepted')
)

# Search projects
projects = Project.objects.filter(
    Q(title__icontains=query) |
    Q(description__icontains=query)
)

# Get team members with profiles
members = team.members.select_related('user__student_profile')

# Create notification
Notification.objects.create(
    user=user,
    activity_type='message',
    content='New message from...',
    is_read=False
)

# Check if connected
connection = Connection.objects.filter(
    Q(sender=user, receiver=other_user) |
    Q(sender=other_user, receiver=user)
).first()
```

---

## URLs to Remember

### Local Development
```
http://localhost:8000/register/          - Sign up
http://localhost:8000/login/             - Sign in
http://localhost:8000/post-project/      - Create project
http://localhost:8000/explore-projects/  - Browse projects
http://localhost:8000/find-collaborators/ - Search users
http://localhost:8000/my-connections/    - My connections
http://localhost:8000/messages/          - Inbox
http://localhost:8000/notifications/     - Alerts
http://localhost:8000/profile/           - My profile
http://localhost:8000/admin/             - Admin panel
```

---

## Dependencies (requirements.txt)

```
Django==3.x or 4.x
djangorestframework
django-allauth
django-cors-headers
python-decouple
psycopg2-binary (PostgreSQL)
gunicorn (production)
dj-database-url (Render)
Pillow (image processing)
```

---

## Next Steps to Improve Code

1. **Security** (1-2 hours)
   - Uncomment CSRF middleware in settings.py
   - Add rate limiting to auth views
   - Add API token authentication

2. **Refactoring** (2-3 hours)
   - Split views.py into logical modules
   - Create service classes for business logic
   - Remove duplicate code (dashboard_view)

3. **Testing** (2-4 hours)
   - Write comprehensive unit tests
   - Add integration tests
   - Test email sending

4. **Performance** (1-2 hours)
   - Add query optimization (select_related, prefetch_related)
   - Implement caching for expensive operations
   - Add database indexes

---

*Quick Reference v1.0 - Generated 2025-01-04*
