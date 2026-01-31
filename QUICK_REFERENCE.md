# UniSync Quick Reference Guide

## File Navigation

### Core Application Files
| File | Purpose | Lines | Status |
|------|---------|-------|--------|
| `auth_project/settings.py` | Configuration, installed apps | 356 | ✅ |
| `accounts/models.py` | 22 database models | 718 | ✅ |
| `accounts/views.py` | 50+ view handlers | 1400+ | ✅ |
| `accounts/serializers.py` | DRF serializers | 106 | ✅ |
| `accounts/urls.py` | URL routing | 120 | ✅ |
| `accounts/forms.py` | Django forms | TBD | ✅ |
| `accounts/permissions.py` | Custom permissions | TBD | ✅ |
| `accounts/services/auth_service.py` | Email service | 470 | ✅ |
| `accounts/chat_api.py` | REST API for messaging | TBD | ✅ |
| `auth_project/urls.py` | Project-level routing | 60 | ✅ |

---

## Key Models Reference

### User & Auth
```python
User                    # Django built-in
StudentProfile          # Extended user profile
OTP                     # 6-digit one-time passwords
UserStatus              # Online/offline tracking
UserStats               # Cached user statistics
```

### Relationships
```python
Connection              # User-to-user requests (pending/accepted/rejected)
Follow                  # User following (separate from connections)
```

### Projects
```python
Project                 # Collaborative projects
ProjectMember           # Team members with roles (owner/admin/contributor/viewer)
ProjectTask             # Tasks within projects
ProjectMilestone        # Project phases
ProjectInvitation       # Team invitations with expiry
```

### Messaging
```python
Message                 # Direct & group messages
ChatRoom                # Group chat rooms
ChatRoomMember          # Room membership
MessageReadStatus       # Per-user read tracking (scalable)
MessageFile             # File attachments
MessageReaction         # Emoji reactions
File                    # Uploaded files storage
```

### Engagement
```python
Comment                 # Project comments
Like                    # Project likes/favorites
Activity                # User activity feed (8 event types)
Notification            # User notifications
```

---

## Key Views Reference

### Authentication
```
POST   /register/                      → register_view()
POST   /login/                         → login_view()
GET/POST /verify-otp/<purpose>/       → verify_otp_view()
GET/POST /resend-otp/<purpose>/       → resend_otp_view()
POST   /forgot-password/               → forgot_password_view()
POST   /reset-password/                → reset_password_view()
POST   /logout/                        → logout_view()
```

### Profiles
```
GET    /student-details/               → student_details_view()
GET    /student-profile/               → student_profile()
GET    /user/<username>/               → user_profile()
GET/POST /profile/edit/                → edit_profile()
GET    /profile/                       → UserProfileView (DRF)
```

### Projects
```
GET/POST /post-project/                → post_project()
GET    /project/<id>/                  → project_detail()
POST   /edit-project/<id>/             → edit_project()
POST   /delete-project/<id>/           → delete_project()
GET    /explore-projects/              → explore_projects_view()
POST   /like-project/<id>/             → like_project() [AJAX]
```

### Social Features
```
GET    /find-collaborators/            → find_collaborators()
POST   /send-connection/<id>/          → send_connection_request()
POST   /accept-connection/<id>/        → accept_connection()
POST   /reject-connection/<id>/        → reject_connection()
GET    /my-connections/                → my_connections()
POST   /follow/<id>/                   → follow_user()
```

### Messaging
```
GET    /messages/                      → message_view()
GET    /chat/<user_id>/                → chat_view()
GET    /enhanced-messages/             → enhanced_messages_view()
GET    /enhanced-chat/<room_id>/       → enhanced_chat_view()
POST   /create-group-chat/             → create_group_chat()
POST   /add-reaction/<msg_id>/         → add_reaction()
```

### Notifications
```
GET    /notifications/                 → notifications_view()
POST   /mark-notification-read/<id>/   → mark_notification_read()
GET    /activity-feed/                 → activity_feed()
```

---

## Email Sending

### Backend Selection (Priority)
```python
# settings.py line 234-252
if BREVO_API_KEY:
    EMAIL_BACKEND = 'accounts.brevo_mail_backend.BrevoMailBackend'
elif ZEPTO_MAIL_API_KEY and ZEPTO_MAIL_TOKEN:
    EMAIL_BACKEND = 'accounts.zepto_mail_backend.ZeptoMailBackend'
elif EMAIL_HOST_USER and EMAIL_HOST_PASSWORD:
    EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
else:
    EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'
```

### Email Types
```
AuthService.send_welcome_email()        → New user greeting
AuthService.send_welcome_back_email()   → Returning user greeting
AuthService.send_password_reset_email() → Password reset link
send_otp_email()                        → OTP codes (5-min expiry)
```

---

## Key Utility Classes

### StudentProfileNLP
**File:** `accounts/utils.py`  
**Purpose:** NLP-based profile matching for collaborator suggestions  
**Used by:** `find_collaborators()` view  
**Method:** Interest-based scoring and profile similarity

### ProjectVisibilityFilter
**File:** `accounts/utils.py`  
**Purpose:** Filter projects by visibility and user permissions  
**Used by:** `explore_projects_view()`  
**Logic:** public → all, private → owner/members, draft → owner only

---

## REST API Endpoints

### Chat & Messaging
```
POST   /chat-rooms/                    Create room
GET    /chat-rooms/                    List rooms
GET    /chat-rooms/<id>/               Room details
GET    /chat-rooms/<id>/members/       Room members

POST   /messages/                      Create message
GET    /messages/                      List messages
GET    /messages/<id>/                 Message details
DELETE /messages/<id>/                 Delete message
GET    /messages/search/               Search messages
GET    /messages/<id>/status/          Read status
POST   /messages/<id>/reactions/       Add reaction

GET    /conversations/                 Recent conversations
GET    /drafts/                        Draft messages
POST   /typing/                        Typing indicator
```

### User & Profile
```
GET    /profile/                       Current user profile
GET    /user-profile/<id>/             Get user profile
GET    /user-stats/                    User statistics
GET    /nlp-analyze/                   NLP analysis
GET    /check-username/                Username availability
GET    /check-email/                   Email availability
```

### External APIs
```
GET    /college-search/                RapidAPI college search
POST   /validate-college/              College validation
```

---

## Configuration Checklist

### Required Environment Variables
```bash
# Django
SECRET_KEY                             # Auto-generated in dev
DEBUG                                  # true/false
ALLOWED_HOSTS                          # localhost,127.0.0.1

# Database
DATABASE_URL                           # postgres://... (Render)
# OR
DB_NAME, DB_USER, DB_PASSWORD, DB_HOST, DB_PORT  # Local DB

# Email
BREVO_API_KEY                          # Primary email service
# OR
ZEPTO_MAIL_API_KEY + ZEPTO_MAIL_TOKEN  # Alternative
# OR
EMAIL_HOST_USER + EMAIL_HOST_PASSWORD  # Gmail SMTP

# OAuth
GOOGLE_CLIENT_ID                       # Google OAuth
GOOGLE_CLIENT_SECRET
GITHUB_CLIENT_ID                       # GitHub OAuth
GITHUB_CLIENT_SECRET

# External APIs
RAPIDAPI_KEY                           # College search
RAPIDAPI_HOST                          # universities-list.p.rapidapi.com

# SSL (Production)
SECURE_SSL_REDIRECT                    # true/false
SESSION_COOKIE_SECURE                  # true/false
CSRF_COOKIE_SECURE                     # true/false
```

---

## Development Commands

### Database Setup
```bash
python manage.py makemigrations        # Create migrations
python manage.py migrate               # Apply migrations
python manage.py createsuperuser       # Admin account
python manage.py collectstatic         # Gather static files
```

### Running Server
```bash
python manage.py runserver             # Development server
gunicorn auth_project.wsgi             # Production server
```

### Useful Admin Commands
```bash
python manage.py shell                 # Python shell with Django
python manage.py dbshell               # Database shell
python manage.py flush                 # Clear database
python manage.py dumpdata > data.json  # Backup data
python manage.py loaddata data.json    # Restore data
```

---

## Testing

### Run Tests
```bash
pytest                                 # Run all tests
pytest -v                              # Verbose output
pytest -k test_login                   # Specific test
pytest --cov=accounts                  # Coverage report
```

### Test Files Available
```
test_login.py                          Login flow testing
test_email.py                          Email delivery testing
test_profile_fix.py                    Profile operations
test_filter.py                         Filtering logic
test_search.py                         Search functionality
test_connections.py                    Connection requests
```

---

## Code Quality Tools

### Formatting
```bash
black accounts/                        # Auto-format code
isort accounts/                        # Sort imports
```

### Linting & Type Checking
```bash
flake8 accounts/                       # Code style
mypy accounts/                         # Type checking
```

### Documentation
```bash
sphinx-build -b html docs/ _build/     # Build docs
```

---

## Common Operations

### Register New User
1. POST `/register/` with username, email, password
2. Receive OTP email
3. POST `/verify-otp/login/` with OTP code
4. User authenticated, redirected to dashboard

### Create Project
1. GET `/post-project/` → view form
2. POST `/post-project/` → create project
3. Project visible in `/explore-projects/`
4. Invite team members via `/invite-to-team/`

### Send Message
1. GET `/chat/<user_id>/` → conversation
2. Submit message form
3. POST to API endpoint
4. Message visible in chat history
5. Read status tracked automatically

### Find Collaborators
1. GET `/find-collaborators/` → advanced search
2. Apply filters (college, interests, skills)
3. View suggested profiles with match scores
4. Send connection request
5. Message after connection accepted

---

## Performance Tips

### Caching
```python
from django.views.decorators.cache import cache_page

@cache_page(60 * 5)  # Cache for 5 minutes
def my_view(request):
    pass
```

### Query Optimization
```python
# Use select_related for ForeignKey
Profile.objects.select_related('user')

# Use prefetch_related for reverse relations
Project.objects.prefetch_related('members')

# Use only() to select specific fields
User.objects.only('username', 'email')
```

### Pagination
```python
from django.core.paginator import Paginator

paginator = Paginator(queryset, 10)
page_obj = paginator.get_page(page_number)
```

---

## Security Checklist

- [ ] Set unique SECRET_KEY in production
- [ ] Set DEBUG=False in production
- [ ] Enable SECURE_SSL_REDIRECT=True
- [ ] Enable SESSION_COOKIE_SECURE=True
- [ ] Enable CSRF_COOKIE_SECURE=True
- [ ] Configure ALLOWED_HOSTS properly
- [ ] Use strong database password
- [ ] Use strong email API keys
- [ ] Enable error tracking (Sentry)
- [ ] Regular database backups
- [ ] Monitor application logs
- [ ] Update dependencies regularly

---

## Troubleshooting

### Email Not Sending
1. Check EMAIL_BACKEND in settings.py
2. Verify API keys (BREVO_API_KEY, etc.)
3. Check logs in `logs/django.log`
4. Test with console backend (development)

### OTP Issues
1. Check OTP expiry (5 minutes)
2. Verify email was received
3. Check if OTP was already used (is_used=True)
4. Verify email spelling

### Login Problems
1. Check user exists in database
2. Verify email/username case sensitivity
3. Check OTP expiry
4. Clear browser cookies/cache

### Project Not Visible
1. Check project visibility (public/private/draft)
2. Verify user has permission to view
3. Check ProjectVisibilityFilter logic

### Connection/Message Issues
1. Verify users are not the same
2. Check connection status
3. Verify message receiver exists
4. Check ChatRoom membership

---

## Deployment Checklist

### Pre-deployment
- [ ] Run all tests and verify passing
- [ ] Check code with flake8/mypy
- [ ] Update dependencies
- [ ] Set up database backups
- [ ] Configure email backend
- [ ] Set up error tracking (Sentry)

### Deployment
- [ ] Set all environment variables
- [ ] Run migrations: `python manage.py migrate`
- [ ] Collect static files: `python manage.py collectstatic --noinput`
- [ ] Create superuser: `python manage.py createsuperuser`
- [ ] Start Gunicorn/Celery workers
- [ ] Configure reverse proxy (Nginx)
- [ ] Enable SSL certificate

### Post-deployment
- [ ] Test all features in production
- [ ] Monitor logs and errors
- [ ] Set up automated backups
- [ ] Configure monitoring/alerting
- [ ] Document deployment steps

---

## Key Statistics

| Metric | Value |
|--------|-------|
| Total Models | 22+ |
| Total Views | 50+ |
| Total API Endpoints | 40+ |
| URL Patterns | 70+ |
| Installed Apps | 13 |
| Installed Packages | 40+ |
| Lines of Code (Python) | 15,000+ |
| Database Tables | 22+ core |
| Email Backends | 4 |
| OAuth Providers | 2 |
| Message Types | 4 |
| Project Member Roles | 4 |
| Activity Types | 8+ |
| Task Statuses | 5 |
| Connection Statuses | 3 |

---

## Document Index

1. **CODEBASE_ANALYSIS.md** - Comprehensive codebase analysis
2. **FEATURE_MATRIX.md** - 180+ features with implementation status
3. **CODE_FLOW_EXAMPLES.md** - 10 detailed code flow diagrams
4. **ANALYSIS_SUMMARY.txt** - Executive summary
5. **QUICK_REFERENCE.md** - This file (quick lookup guide)

---

**Last Updated:** January 29, 2026  
**Analysis Scope:** Complete UniSync codebase  
**Coverage:** Settings, Models, Views, APIs, Services, Utils  
**Status:** Production-Ready ✅
