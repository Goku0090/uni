# Quick Codebase Reference Guide 2026

## Project: UniSync - Student Collaboration Platform

### Stack Summary
| Component | Technology | Version |
|-----------|-----------|---------|
| **Backend** | Django | 4.2.8 |
| **API** | Django REST Framework | 3.14.0 |
| **Frontend** | React | 18.2.0 |
| **Build Tool** | Vite | 5.0.0 |
| **Real-time** | Django Channels | 4.0.0 |
| **Database** | PostgreSQL | - |
| **Cache** | Redis | 5.0.1 |
| **Auth** | django-allauth | 0.61.1 |

---

## Key Files by Purpose

### Authentication
- **Login/Register**: `backend/accounts/views.py` (lines ~500-900)
- **OAuth Setup**: `backend/auth_project/settings.py` (lines ~50-60)
- **OTP System**: `backend/accounts/models.py` (lines 55-124)
- **Email Backend**: `backend/accounts/brevo_mail_backend.py`

### Project Management
- **Models**: `backend/accounts/models.py` (Project, ProjectTeam, ProjectTask)
- **Views**: `backend/accounts/views.py` (ProjectCreateView, project_feed)
- **API**: `backend/accounts/views.py` (REST endpoints)
- **Filtering**: `backend/accounts/utils.py` (ProjectVisibilityFilter)

### Real-time Features
- **WebSocket Consumers**: `backend/accounts/consumers.py`
- **Routing**: `backend/accounts/routing.py`
- **Signals**: `backend/accounts/signals_realtime.py`
- **ASGI Config**: `backend/auth_project/asgi.py`

### Chat & Messaging
- **Chat API**: `backend/accounts/chat_api.py` or `chat_api_improved.py`
- **Chat Models**: `backend/accounts/models.py` (ChatRoom, Message, ChatRoomMember)
- **WebSocket**: `backend/accounts/consumers.py` (ChatConsumer)

### Comments
- **Comment API**: `backend/accounts/comment_api.py`
- **Model**: `backend/accounts/models.py` (Comment)
- **Real-time**: `backend/accounts/signals_realtime.py`

### Frontend
- **Main App**: `frontend/src/App.jsx`
- **Entry Point**: `frontend/src/main.jsx`
- **API Client**: `frontend/src/api/`
- **Build Config**: `frontend/vite.config.js`

---

## Common Tasks

### Run Development Server
```bash
# Backend (Terminal 1)
cd backend
python manage.py runserver 0.0.0.0:8000

# Frontend (Terminal 2)
cd frontend
npm run dev

# WebSocket (Terminal 3)
docker-compose up -d
daphne -b 0.0.0.0 -p 8001 auth_project.asgi:application
```

### Database Migrations
```bash
# Create migration
python manage.py makemigrations

# Apply migrations
python manage.py migrate

# View migration status
python manage.py showmigrations
```

### Create Superuser
```bash
python manage.py createsuperuser
# Then visit: http://localhost:8000/admin/
```

### Collect Static Files
```bash
python manage.py collectstatic --noinput
```

### Run Tests
```bash
python manage.py test
```

### Clear Cache
```bash
python manage.py shell
>>> from django.core.cache import cache
>>> cache.clear()
```

---

## Model Quick Reference

### User Related
```
User → StudentProfile (1-to-1)
     → Project (1-to-many, as owner)
     → Connection (1-to-many, as sender/receiver)
     → Message (1-to-many)
     → Comment (1-to-many)
     → Like (1-to-many)
     → Follow (1-to-many)
```

### Project Related
```
Project → ProjectTeam → ProjectTeamMember → User
        → ProjectTask (timeline tracking)
        → ProjectMilestone (goals)
        → Comment (discussions)
        → Like (engagement)
        → Activity (audit trail)
```

### Communication
```
Message → MessageFile (attachments)
        → MessageReaction (emoji reactions)
        → MessageReadStatus (tracking)

ChatRoom → ChatRoomMember → User
         → Message
```

---

## API Endpoints Quick List

### Auth
```
POST   /api/auth/login/
POST   /api/auth/register/
POST   /api/auth/otp/generate/
POST   /api/auth/otp/verify/
GET    /api/auth/user/
POST   /api/auth/logout/
```

### Projects
```
GET    /api/projects/                # List (paginated)
POST   /api/projects/                # Create
GET    /api/projects/<id>/           # Detail
PUT    /api/projects/<id>/           # Update
DELETE /api/projects/<id>/           # Delete
GET    /api/projects/search/         # Search
```

### Chat
```
GET    /api/messages/conversations/
POST   /api/messages/
GET    /api/messages/<id>/
POST   /api/chatrooms/
GET    /api/chatrooms/
WS     /ws/chat/<room_id>/
```

### Comments
```
GET    /api/comments/
POST   /api/comments/
DELETE /api/comments/<id>/
POST   /api/comments/<id>/like/
```

### Social
```
GET    /api/connections/
POST   /api/connections/
PUT    /api/connections/<id>/
GET    /api/follow/
POST   /api/follow/
GET    /api/profiles/<id>/
PUT    /api/profiles/
```

---

## Environment Variables

### Backend (.env)
```
DEBUG=True
SECRET_KEY=your-secret-key
DATABASE_URL=postgresql://user:password@localhost/dbname
REDIS_URL=redis://localhost:6379/1
ALLOWED_HOSTS=localhost,127.0.0.1
SECURE_SSL_REDIRECT=False

# Email
EMAIL_BACKEND=accounts.brevo_mail_backend.BrevoMailBackend
BREVO_API_KEY=your-api-key

# OAuth
GOOGLE_CLIENT_ID=your-client-id
GOOGLE_CLIENT_SECRET=your-secret
GITHUB_CLIENT_ID=your-client-id
GITHUB_CLIENT_SECRET=your-secret
```

### Frontend (.env.local)
```
VITE_API_URL=http://localhost:8000/api
```

---

## Directory Quick Navigation

| Path | Purpose |
|------|---------|
| `backend/auth_project/` | Django project settings |
| `backend/accounts/` | Main Django app |
| `backend/accounts/models.py` | Database models |
| `backend/accounts/views.py` | View logic |
| `backend/accounts/serializers.py` | API serializers |
| `backend/accounts/consumers.py` | WebSocket |
| `backend/accounts/routing.py` | WebSocket routing |
| `backend/accounts/signals_realtime.py` | Real-time events |
| `backend/accounts/chat_api.py` | Chat endpoints |
| `backend/accounts/comment_api.py` | Comment endpoints |
| `backend/accounts/utils.py` | Helper functions |
| `frontend/src/` | React components |
| `frontend/src/api/` | API client |

---

## Debugging Tips

### View SQL Queries
```python
from django.db import connection
from django.test.utils import CaptureQueriesContext

with CaptureQueriesContext(connection) as ctx:
    # Your code here
print(f"Queries: {len(ctx)}")
for query in ctx:
    print(query['sql'])
```

### Check WebSocket Connection
```javascript
// In browser console
ws = new WebSocket('ws://localhost:8001/ws/chat/1/')
ws.onmessage = (event) => console.log(JSON.parse(event.data))
ws.send(JSON.stringify({message: 'test'}))
```

### Debug Django Signals
```python
from django.db.models.signals import post_save
import logging
logger = logging.getLogger(__name__)

@receiver(post_save, sender=Project)
def debug_signal(sender, instance, **kwargs):
    logger.info(f"Project saved: {instance.id}")
```

### Test API Endpoint
```bash
# Using curl
curl -X GET http://localhost:8000/api/projects/ \
  -H "Authorization: Bearer YOUR_TOKEN"

# Using httpie
http GET http://localhost:8000/api/projects/ \
  Authorization:"Bearer YOUR_TOKEN"
```

---

## Common Issues & Solutions

| Issue | Cause | Solution |
|-------|-------|----------|
| WebSocket fails to connect | Redis not running | `redis-server` or `docker-compose up` |
| Static files 404 | Not collected | `python manage.py collectstatic` |
| OAuth callback error | Redirect URI mismatch | Check provider settings + Django admin |
| Database locked | Migration conflict | Delete `.sqlite3` + re-migrate |
| CORS error | Frontend origin not allowed | Check CORS_ALLOWED_ORIGINS in settings |
| Email not sending | Brevo creds missing | Verify BREVO_API_KEY in .env |
| Import error | Module not installed | `pip install -r requirements.txt` |

---

## Git Workflow

```bash
# Start new feature
git checkout -b feature/feature-name

# Make changes and commit
git add .
git commit -m "[FEATURE] Description"

# Push to remote
git push origin feature/feature-name

# Create pull request on GitHub
# After review, merge to main
```

---

## Deployment Checklist

- [ ] Set `DEBUG=False`
- [ ] Configure `ALLOWED_HOSTS`
- [ ] Set `SECURE_SSL_REDIRECT=True`
- [ ] Set `SESSION_COOKIE_SECURE=True`
- [ ] Set `CSRF_COOKIE_SECURE=True`
- [ ] Update `SECRET_KEY`
- [ ] Configure database URL
- [ ] Configure Redis URL
- [ ] Set up email (Brevo)
- [ ] Configure OAuth credentials
- [ ] Run migrations
- [ ] Collect static files
- [ ] Set up SSL certificate
- [ ] Configure domain in Render/Railway

---

## Performance Tips

### Backend
- Use `select_related()` for ForeignKey
- Use `prefetch_related()` for reverse relations
- Enable query caching with Redis
- Use pagination for large lists
- Index frequently queried fields

### Frontend
- Lazy load images
- Code split routes
- Minimize bundle size
- Use React.memo for expensive components
- Debounce search input

### Database
- Add indexes on ForeignKey fields
- Archive old data
- Run `VACUUM` on PostgreSQL
- Monitor slow queries

---

## Security Checklist

- [ ] CSRF tokens enabled
- [ ] SQL injection protected (ORM)
- [ ] XSS protected (template escaping)
- [ ] Passwords hashed (PBKDF2)
- [ ] Secrets in environment
- [ ] HTTPS enforced
- [ ] CORS headers validated
- [ ] Rate limiting configured
- [ ] File upload validation
- [ ] Input sanitization

---

## Useful Commands

```bash
# View all users
python manage.py shell
>>> from django.contrib.auth.models import User
>>> User.objects.all()

# Export data
python manage.py dumpdata > data.json

# Import data
python manage.py loaddata data.json

# Delete database
rm db.sqlite3
python manage.py migrate

# Create fixture
python manage.py dumpdata app_name.ModelName > fixture.json

# Interactive shell
python manage.py shell_plus  # requires django-extensions

# Run celery (if using async)
celery -A auth_project worker -l info
```

---

## Learning Resources

- **Django Docs**: https://docs.djangoproject.com/
- **DRF Docs**: https://www.django-rest-framework.org/
- **Channels Docs**: https://channels.readthedocs.io/
- **React Docs**: https://react.dev/
- **Vite Docs**: https://vitejs.dev/
- **Allauth Docs**: https://django-allauth.readthedocs.io/

---

## Contact & Support

For issues, refer to:
1. Existing documentation in root directory
2. GitHub issues
3. Project maintainers

Last Updated: February 2026

