# UniSync - Quick Code Reference Guide

## Project at a Glance
- **Type**: Student collaboration platform
- **Framework**: Django 4.2.8 + DRF
- **Database**: PostgreSQL
- **Real-time**: Django Channels + Redis
- **Hosting**: Render/Railway ready

---

## Directory Map

```
auth_project/
├── accounts/               # Main app
│   ├── models.py          # 15+ core models
│   ├── views.py           # Page views & logic
│   ├── comment_api.py     # Comment endpoints
│   ├── chat_api.py        # Chat/messaging
│   ├── serializers.py     # DRF serializers
│   ├── forms.py           # Django forms
│   ├── urls.py            # API routes
│   ├── permissions.py     # Access control
│   ├── utils.py           # Helper functions
│   ├── services/
│   │   └── auth_service.py # Email services
│   ├── templates/         # HTML templates
│   ├── static/            # CSS/JS
│   └── migrations/        # DB migrations
├── auth_project/
│   ├── settings.py        # Django config
│   ├── urls.py            # Root URLs
│   ├── wsgi.py
│   └── asgi.py
├── requirements.txt       # Dependencies
├── manage.py             # CLI tool
├── Procfile              # Heroku config
├── render.yaml           # Render config
└── railway.json          # Railway config
```

---

## Core Models (Quick Reference)

| Model | Purpose | Key Fields |
|-------|---------|-----------|
| **User** | Django auth | username, email, password |
| **StudentProfile** | Extended profile | college, bio, profile_photo, skills, interests |
| **OTP** | Email auth | email, otp_code, purpose, expires_at |
| **Project** | Collaboration item | title, description, technologies, category |
| **Comment** | Project feedback | user, project, content, created_at |
| **Message** | Direct/group chat | sender, receiver, chat_room, content, created_at |
| **ChatRoom** | Message container | name, chat_type, members, created_at |
| **Connection** | Network request | sender, receiver, status |
| **Notification** | Activity alert | user, notification_type, is_read |
| **Activity** | User feed | user, activity_type, related object |
| **Like** | Project like | user, project |
| **Follow** | User follow | follower, following |

---

## Key API Routes

### Authentication
```
POST   /accounts/login/
POST   /accounts/register/
POST   /accounts/verify-otp/<purpose>/
POST   /accounts/forgot-password/
POST   /accounts/reset-password/
```

### Projects
```
POST   /accounts/post-project/
GET    /accounts/project-detail/<id>/
POST   /accounts/edit-project/<id>/
DELETE /accounts/delete-project/<id>/
GET    /accounts/explore-projects/
POST   /accounts/like-project/<id>/
```

### Comments (Live Feed)
```
GET    /api/projects/<id>/comments/
POST   /api/projects/<id>/comments/add/
DELETE /api/comments/<id>/delete/
PUT    /api/comments/<id>/edit/
```

### Messaging
```
GET/POST /api/chat-rooms/
POST     /api/direct-message/
GET/POST /api/messages/
POST     /api/messages/<id>/reactions/
```

### Network
```
POST /accounts/send-connection/<user_id>/
POST /accounts/accept-connection/<id>/
POST /accounts/follow/<user_id>/
GET  /accounts/user/<username>/
```

---

## Important Functions

### Authentication
```python
# In views.py
login_view()           # POST login form
register_view()        # POST registration
verify_otp_view()      # POST OTP verification
send_otp_email()       # Send OTP email
```

### Comments
```python
# In comment_api.py
add_comment()          # POST /api/projects/<id>/comments/add/
get_comments()         # GET /api/projects/<id>/comments/
delete_comment()       # DELETE /api/comments/<id>/delete/
edit_comment()         # PUT /api/comments/<id>/edit/
```

### Projects
```python
# In views.py
post_project()         # Create project
project_detail()       # View project
explore_projects_view() # Browse projects
like_project()         # Like project
```

### Messaging
```python
# In chat_api.py
ChatRoomListCreateView # GET/POST chat rooms
MessageListCreateView  # GET/POST messages
ConversationListView   # GET user conversations
```

---

## Common Code Patterns

### Create Model Instance
```python
from accounts.models import Comment, Project

# Create comment
comment = Comment.objects.create(
    user=request.user,
    project=project,
    content="Great project!"
)
```

### Query Model
```python
# Get all projects by user
projects = Project.objects.filter(user=request.user)

# Get recent comments
comments = Comment.objects.filter(project=project).order_by('-created_at')[:10]
```

### Send Email
```python
from accounts.services.auth_service import AuthService

AuthService.send_welcome_email(email, username)
AuthService.send_password_reset_email(email, username, reset_link)
```

### JSON Response
```python
from django.http import JsonResponse

return JsonResponse({
    'success': True,
    'message': 'Operation completed',
    'data': {'id': 1, 'name': 'example'}
})
```

### API Serializer
```python
from rest_framework import serializers
from accounts.models import StudentProfile

class StudentProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = StudentProfile
        fields = ['full_name', 'college', 'skills', 'interests']
```

---

## Important Settings

### Database
```python
# In settings.py
DATABASES = {
    'default': dj_database_url.config(
        default='sqlite:///db.sqlite3',
        conn_max_age=600
    )
}
```

### Email
```python
DEFAULT_FROM_EMAIL = os.getenv('DEFAULT_FROM_EMAIL')
EMAIL_BACKEND = 'accounts.brevo_mail_backend.BrevoBrevBackend'
# or
EMAIL_BACKEND = 'accounts.zepto_mail_backend.ZeptoMailBackend'
```

### Redis Cache
```python
CACHES = {
    'default': {
        'BACKEND': 'django_redis.cache.RedisCache',
        'LOCATION': os.getenv('REDIS_URL'),
    }
}
```

### Authentication
```python
INSTALLED_APPS = [
    'django.contrib.auth',
    'accounts',
    'allauth',
    'allauth.account',
    'allauth.socialaccount',
    'allauth.socialaccount.providers.google',
    'allauth.socialaccount.providers.github',
]
```

---

## File Locations

### Templates
- **Auth**: `accounts/templates/login.html`, `register.html`
- **Projects**: `accounts/templates/project_*.html`
- **Profile**: `accounts/templates/student_profile.html`
- **Chat**: `accounts/templates/chat.html`
- **Components**: `accounts/templates/components/`

### Static Files
- **CSS**: `accounts/static/css/`
- **JS**: `accounts/static/js/`
- **Images**: `accounts/static/images/`

### Forms
- All Django forms in `accounts/forms.py`

### Serializers
- All DRF serializers in `accounts/serializers.py`

---

## Environment Variables (.env)

```bash
DEBUG=True
SECRET_KEY=your-secret-key

# Database
DATABASE_URL=postgresql://user:password@localhost/dbname

# Redis
REDIS_URL=redis://localhost:6379/0

# Email
DEFAULT_FROM_EMAIL=noreply@unisync.com
EMAIL_BACKEND=accounts.brevo_mail_backend.BrevoBrevBackend
BREVO_API_KEY=your-api-key

# Social Auth
SOCIAL_AUTH_GOOGLE_OAUTH2_KEY=google-key
SOCIAL_AUTH_GOOGLE_OAUTH2_SECRET=google-secret
SOCIAL_AUTH_GITHUB_KEY=github-key
SOCIAL_AUTH_GITHUB_SECRET=github-secret

# Security
ALLOWED_HOSTS=localhost,127.0.0.1
SECURE_SSL_REDIRECT=False
SESSION_COOKIE_SECURE=False
```

---

## Testing Commands

```bash
# Run migrations
python manage.py migrate

# Create superuser
python manage.py createsuperuser

# Run development server
python manage.py runserver

# Make migrations
python manage.py makemigrations

# Run tests
pytest

# Run specific test
pytest accounts/tests.py::TestClassName

# Check code with linting
flake8 accounts/

# Format code
black accounts/

# Check type hints
mypy accounts/
```

---

## Common Tasks

### Add New Model
1. Define in `accounts/models.py`
2. Create migration: `python manage.py makemigrations`
3. Apply migration: `python manage.py migrate`
4. Create serializer in `accounts/serializers.py` (if API)
5. Create view/viewset
6. Register route in `accounts/urls.py`

### Add New API Endpoint
1. Create view in `accounts/views.py` or `chat_api.py`
2. Create serializer in `accounts/serializers.py`
3. Add route to `accounts/urls.py`
4. Test with `curl` or Postman
5. Add permission class if needed

### Send Email
1. Use `AuthService` class from `accounts/services/auth_service.py`
2. Or use Django `send_mail()` function
3. Configure email backend in settings
4. Set `DEFAULT_FROM_EMAIL` environment variable

### Handle Real-time Features
1. Use Django Channels for WebSockets
2. Define consumers in `accounts/consumers.py`
3. Configure `ASGI_APPLICATION` in settings
4. Use Redis as channel layer
5. Broadcast messages to groups

---

## Debugging Tips

### Check Logs
```bash
# View application logs
tail -f logs/django.log

# Filter specific error
grep -i "error" logs/django.log
```

### Django Shell
```bash
python manage.py shell

>>> from accounts.models import User, Project
>>> User.objects.count()
>>> Project.objects.filter(user__username='john')
```

### Debug Print
```python
import logging
logger = logging.getLogger(__name__)
logger.info("Debug message")
logger.error("Error message", exc_info=True)
```

### API Testing
```bash
# GET request
curl http://localhost:8000/api/user-profile/1/

# POST request with data
curl -X POST http://localhost:8000/api/comments/ \
  -H "Content-Type: application/json" \
  -d '{"content":"Great!","project_id":1}'

# With authentication
curl -H "Authorization: Token YOUR_TOKEN" \
  http://localhost:8000/api/messages/
```

---

## Key Dependencies

| Package | Version | Purpose |
|---------|---------|---------|
| Django | 4.2.8 | Web framework |
| djangorestframework | 3.14.0 | REST API |
| channels | 4.0.0 | WebSockets |
| django-allauth | 0.61.1 | Social auth |
| psycopg2-binary | 2.9.9 | PostgreSQL driver |
| redis | 5.0.1 | Caching |
| celery | 5.3.4 | Task queue |
| pillow | 10.1.0 | Image processing |
| nltk | 3.8.1 | NLP |
| gunicorn | 21.2.0 | Production server |

---

## Performance Tips

1. **Use select_related()** for ForeignKey joins
2. **Use prefetch_related()** for reverse relations
3. **Cache frequent queries** with Redis
4. **Paginate large result sets** (10-20 items)
5. **Index common filter fields** in models
6. **Use database-level constraints** for unique values
7. **Compress static files** with WhiteNoise
8. **Enable gzip** in production

---

## Security Checklist

- [ ] Set `DEBUG=False` in production
- [ ] Use strong `SECRET_KEY` (50+ chars)
- [ ] Enable `SECURE_SSL_REDIRECT` on HTTPS
- [ ] Set `SESSION_COOKIE_SECURE=True`
- [ ] Set `CSRF_COOKIE_SECURE=True`
- [ ] Configure `ALLOWED_HOSTS`
- [ ] Use environment variables for secrets
- [ ] Enable rate limiting on APIs
- [ ] Validate all user inputs
- [ ] Sanitize HTML/script tags in comments
- [ ] Keep dependencies updated
- [ ] Monitor error logs with Sentry

---

## Deployment Checklist

- [ ] Run `python manage.py collectstatic`
- [ ] Run migrations: `python manage.py migrate`
- [ ] Create superuser: `python manage.py createsuperuser`
- [ ] Set environment variables
- [ ] Configure PostgreSQL connection
- [ ] Configure Redis connection
- [ ] Set up email service credentials
- [ ] Configure social auth credentials
- [ ] Enable HTTPS/SSL
- [ ] Configure CDN for static files
- [ ] Set up monitoring (Sentry)
- [ ] Configure backups for database
- [ ] Test all endpoints in production

---

## Quick Links

- **Settings**: `auth_project/settings.py`
- **URLs**: `auth_project/urls.py` (root), `accounts/urls.py` (API)
- **Models**: `accounts/models.py`
- **Views**: `accounts/views.py`
- **API Views**: `accounts/chat_api.py`, `accounts/comment_api.py`
- **Forms**: `accounts/forms.py`
- **Serializers**: `accounts/serializers.py`
- **Services**: `accounts/services/auth_service.py`
- **Admin**: `/admin/` (requires superuser)

