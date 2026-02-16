# Quick Code Reference Guide 2026

## File Navigation Map

### Core Configuration
| File | Purpose | Key Items |
|------|---------|-----------|
| `backend/auth_project/settings.py` | Django settings | Database, email, CORS, security |
| `backend/auth_project/urls.py` | URL routing | All URL patterns and views |
| `backend/auth_project/asgi.py` | WebSocket config | Channels routing |
| `backend/auth_project/wsgi.py` | Production WSGI | Gunicorn entry point |
| `frontend/vite.config.js` | Frontend build | Vite bundler config |
| `frontend/package.json` | Dependencies | NPM packages |

### Models & Data
| File | Purpose | Key Items |
|------|---------|-----------|
| `backend/accounts/models.py` | Database models | 20+ models defining data |
| `backend/accounts/serializers.py` | API serializers | Convert models to JSON |
| `backend/accounts/migrations/` | DB schema | Version control for DB |

### API & Views
| File | Purpose | Key Items |
|------|---------|-----------|
| `backend/accounts/views.py` | Main views | 40+ view functions |
| `backend/accounts/urls.py` | API routes | REST endpoint definitions |
| `backend/accounts/chat_api.py` | Chat endpoints | Messaging API |
| `backend/accounts/comment_api.py` | Comment endpoints | Comment API |
| `backend/accounts/template_api.py` | Template endpoints | Template API |

### Authentication
| File | Purpose | Key Items |
|------|---------|-----------|
| `backend/accounts/forms.py` | Form classes | Login, registration, profile forms |
| `backend/accounts/utils.py` | Helper functions | Email sending, OTP generation |
| `backend/accounts/brevo_mail_backend.py` | Brevo integration | Email via Brevo API |

### Real-time & WebSocket
| File | Purpose | Key Items |
|------|---------|-----------|
| `backend/accounts/consumers.py` | WebSocket handlers | Message, notification consumers |
| `backend/accounts/routing.py` | WS routing | Channels protocol router |
| `backend/accounts/signals_realtime.py` | Event signals | Real-time event broadcasting |

### Frontend
| File | Purpose | Key Items |
|------|---------|-----------|
| `frontend/src/App.jsx` | Root component | Routes, layout |
| `frontend/src/main.jsx` | Entry point | React app initialization |
| `frontend/src/api/` | API functions | Axios wrappers |

---

## Common Code Patterns

### Authentication Pattern
```python
# Decorator for views requiring login
from django.contrib.auth.decorators import login_required

@login_required(login_url='login')
def my_view(request):
    user = request.user
    # ... user is guaranteed to be authenticated
```

### API Response Pattern
```python
# Standardized JSON response
from django.http import JsonResponse

def my_api_view(request):
    try:
        # ... do something
        return JsonResponse({
            'success': True,
            'data': result,
            'message': 'Operation successful'
        })
    except Exception as e:
        return JsonResponse({
            'success': False,
            'message': str(e),
            'error': 'Error type'
        }, status=400)
```

### Model Query Pattern
```python
# Efficient database queries
from accounts.models import Project

# Get with optimization
projects = Project.objects.select_related('owner')\
                          .prefetch_related('members')\
                          .filter(status='active')\
                          .order_by('-created_at')[:20]

# Get single object
project = Project.objects.get(id=1)

# Check existence
exists = Project.objects.filter(id=1).exists()

# Count records
total = Project.objects.count()
```

### Serializer Usage Pattern
```python
# Serialize data for API response
from accounts.serializers import ProjectSerializer
from accounts.models import Project

project = Project.objects.get(id=1)
serializer = ProjectSerializer(project)
return JsonResponse(serializer.data)

# Deserialize request data
serializer = ProjectSerializer(data=request.data)
if serializer.is_valid():
    project = serializer.save()
else:
    return JsonResponse(serializer.errors, status=400)
```

### Permission Check Pattern
```python
# Check user permissions
if project.owner != request.user and \
   not project.members.filter(user=request.user).exists():
    return JsonResponse({'success': False, 'message': 'Not allowed'}, status=403)
```

### WebSocket Message Pattern
```python
# Send message through WebSocket
from asgiref.sync import async_to_sync
from channels.layers import get_channel_layer

channel_layer = get_channel_layer()
async_to_sync(channel_layer.group_send)(
    f"chat_room_{room_id}",
    {
        'type': 'chat.message',
        'message': 'Hello',
        'user_id': request.user.id
    }
)
```

### Email Sending Pattern
```python
# Send email (auto-routes to Brevo/Gmail/Console)
from django.core.mail import send_mail

send_mail(
    subject='Your OTP Code',
    message='Your code is: 123456',
    from_email='noreply@unisinq.app',
    recipient_list=[email],
    fail_silently=False
)
```

---

## Key Model Methods

### StudentProfile
```python
profile = StudentProfile.objects.get(user=user)
profile.get_display_name()  # Returns full_name or username
```

### OTP
```python
# Generate OTP
otp = OTP.generate_otp(email='user@example.com', purpose='login')

# Verify OTP
is_valid, message = otp.verify_otp('123456')

# Check validity
if otp.is_valid():
    # OTP not expired and not used
```

### Project
```python
project = Project.objects.get(id=1)
project.total_likes()  # Count likes
project.total_comments()  # Count comments
project.total_members()  # Count team members
project.can_edit(user)  # Check if user can edit
```

### Message
```python
message = Message.objects.get(id=1)
message.is_read_by(user)  # Check if user read
message.mark_as_read_by(user)  # Mark as read
message.get_read_count()  # How many read
```

---

## Common Queries

### Find Users by Skills
```python
from accounts.models import StudentProfile
from django.db.models import Q
import json

# Search users with specific skill
skill = 'Python'
users = StudentProfile.objects.filter(
    skills__contains=[skill]
).select_related('user')
```

### Find Active Projects
```python
from accounts.models import Project

active = Project.objects.filter(
    status='active'
).order_by('-created_at')
```

### Get User's Messages
```python
from accounts.models import Message

messages = Message.objects.filter(
    Q(sender=user) | Q(receiver=user)
).select_related('sender', 'receiver')\
 .order_by('-created_at')
```

### Get Unread Notifications
```python
from accounts.models import Notification

unread = Notification.objects.filter(
    user=user,
    is_read=False
).order_by('-created_at')
```

---

## Debugging Tips

### View Response Format
```python
# Check what's being returned
import json
response = serializer.data
print(json.dumps(response, indent=2, default=str))
```

### Log Debug Info
```python
import logging
logger = logging.getLogger(__name__)

logger.debug(f"User: {request.user}")
logger.info(f"Project created: {project.id}")
logger.error(f"Error: {str(e)}")
```

### Database Query Inspection
```python
from django.db import connection
from django.test.utils import CaptureQueriesContext

with CaptureQueriesContext(connection) as queries:
    projects = Project.objects.all()
    
print(f"Total queries: {len(queries)}")
for query in queries:
    print(query['sql'])
```

### Test API Endpoints
```bash
# Using curl
curl -X GET http://localhost:8000/api/projects/ \
  -H "Authorization: Token YOUR_TOKEN"

# Using httpie
http GET localhost:8000/api/projects/ \
  Authorization:"Token YOUR_TOKEN"

# Using Python requests
import requests
response = requests.get(
    'http://localhost:8000/api/projects/',
    headers={'Authorization': 'Token YOUR_TOKEN'}
)
print(response.json())
```

---

## Frequent Tasks

### Add New Project Field
1. Edit `models.py` → add field to Project model
2. Run: `python manage.py makemigrations`
3. Run: `python manage.py migrate`
4. Update `serializers.py` → add field to ProjectSerializer
5. Update `views.py` → handle field in view

### Add New API Endpoint
1. Create view function in `views.py`
2. Add URL pattern in `urls.py`
3. Create serializer in `serializers.py` if needed
4. Add permission checks
5. Return JSON response
6. Test with curl/Postman

### Send Email Alert
1. Create email template in `templates/`
2. Use `send_mail()` in view
3. Configure backend in `settings.py`
4. Test with `EMAIL_BACKEND = 'console'` first

### Add WebSocket Event
1. Handle in `consumers.py`
2. Define in `routing.py`
3. Send from view using `channel_layer.group_send()`
4. Receive in frontend JavaScript
5. Update UI on event

### Create Migration
```bash
# After changing models.py
python manage.py makemigrations accounts
python manage.py migrate
```

### Create Admin Interface
1. Edit `admin.py`
2. Register model with admin.site.register()
3. Create ModelAdmin class with list_display, search_fields, etc.
4. Access at /admin/

---

## Environment Variables Checklist

**Required for Development:**
- `DEBUG=True`
- `SECRET_KEY=dev-key`
- `ALLOWED_HOSTS=localhost,127.0.0.1`

**Database (choose one):**
- PostgreSQL: `DATABASE_URL` or `DB_NAME`, `DB_USER`, etc.
- SQLite: (default, no config needed)

**Email (at least one):**
- `BREVO_API_KEY` (Recommended)
- `EMAIL_HOST_USER` + `EMAIL_HOST_PASSWORD` (Gmail)
- Or use console: `EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'`

**OAuth (optional):**
- `GOOGLE_CLIENT_ID` + `GOOGLE_CLIENT_SECRET`
- `GITHUB_CLIENT_ID` + `GITHUB_CLIENT_SECRET`

**Frontend (optional):**
- `VITE_API_URL=http://localhost:8000`

---

## Code Style Standards

### Python (Backend)
- Follow PEP 8
- Use 4 spaces for indentation
- Docstrings for functions/classes
- Type hints optional but appreciated

### JavaScript/React (Frontend)
- Use ES6+ features
- Functional components preferred
- Use hooks (useState, useEffect, etc.)
- CamelCase for variables/functions
- PascalCase for components

### Naming Conventions
- Models: PascalCase (Project, StudentProfile)
- Views: snake_case (project_detail, my_projects)
- URLs: kebab-case (/my-projects/, /find-collaborators/)
- Fields: snake_case (created_at, is_active)

---

## Performance Tips

### Database
- Use `.select_related()` for foreign keys
- Use `.prefetch_related()` for reverse relationships
- Index frequently queried fields
- Use `.values()` to select specific fields
- Avoid N+1 queries (check queries in debug)

### Caching
- Cache expensive computations in Redis
- Cache API responses for static data
- Set appropriate TTL for cache keys

### Frontend
- Lazy load components with React.lazy()
- Code split with dynamic imports
- Cache API responses locally
- Minimize bundle size

### API
- Use pagination for large result sets
- Filter early, select late
- Return only needed fields
- Compress responses

---

## Security Checklist

- [ ] CSRF tokens on all forms
- [ ] Input validation on all fields
- [ ] SQL injection protection (Django ORM)
- [ ] XSS protection (template escaping)
- [ ] CORS whitelisting
- [ ] HTTPS in production
- [ ] Secure session cookies
- [ ] Rate limiting on auth endpoints
- [ ] Password hashing (Django auth)
- [ ] No sensitive data in logs
- [ ] Environment variables for secrets
- [ ] Regular dependency updates

---

## Useful Commands

```bash
# Django Commands
python manage.py runserver                    # Start dev server
python manage.py migrate                      # Apply migrations
python manage.py makemigrations               # Create migrations
python manage.py createsuperuser              # Create admin user
python manage.py shell                        # Python shell
python manage.py test                         # Run tests
python manage.py collectstatic                # Collect static files
python manage.py dumpdata > backup.json       # Backup database
python manage.py loaddata backup.json         # Restore database

# Frontend Commands
npm install                                   # Install dependencies
npm run dev                                   # Start dev server
npm run build                                 # Build for production
npm run preview                               # Preview production build

# Docker Commands
docker build -t myapp .                       # Build image
docker run -p 8000:8000 myapp                 # Run container
docker-compose up                             # Start all services
docker-compose down                           # Stop services

# Git Commands
git status                                    # Check changes
git add .                                     # Stage all changes
git commit -m "message"                       # Commit changes
git push                                      # Push to GitHub
git pull                                      # Pull latest changes
```

---

## Resources

### Official Docs
- Django: https://docs.djangoproject.com/
- DRF: https://www.django-rest-framework.org/
- Channels: https://channels.readthedocs.io/
- React: https://react.dev/
- Vite: https://vitejs.dev/

### Learning
- Django for Beginners: https://djangoforbeginners.com/
- Real Python: https://realpython.com/
- MDN Web Docs: https://developer.mozilla.org/

### Tools
- Postman: https://www.postman.com/ (API testing)
- DB Browser: https://sqlitebrowser.org/ (SQLite)
- VS Code: https://code.visualstudio.com/ (Editor)

---

**Last Updated**: February 16, 2026
**Version**: 1.0
