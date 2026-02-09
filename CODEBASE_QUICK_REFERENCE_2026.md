# Codebase Quick Reference - 2026

## Project at a Glance

**Type:** Collaborative Project Management Platform  
**Stack:** Django 5.2 + Channels + PostgreSQL + Bootstrap 5  
**Status:** Production-Ready  
**Users:** Students finding collaborators and managing projects  

---

## Key Models (Database Tables)

| Model | Purpose | Key Fields |
|-------|---------|-----------|
| **User** | Django built-in user | username, email, password |
| **StudentProfile** | Extended profile | full_name, bio, skills, photo |
| **Project** | User projects | title, description, team, status |
| **Comment** | Project comments | text, author, project, timestamp |
| **Message** | Direct messages | sender, receiver, content |
| **ChatRoom** | Group messages | name, members, created_by |
| **Connection** | User connections | sender, receiver, status |
| **Task** | Project tasks | title, assigned_to, status |
| **Milestone** | Project progress | name, target_date, status |
| **Activity** | Activity log | user, action, timestamp |
| **Notification** | User alerts | user, type, content, read |

---

## Key Views (HTTP Endpoints)

### Authentication
```
register_view()       - /accounts/register/
login_view()          - /accounts/login/
verify_otp()          - /accounts/verify-otp/
oauth_callback()      - /accounts/oauth/google/callback/
logout_view()         - /accounts/logout/
```

### Profiles
```
student_profile()     - /accounts/profile/
view_profile()        - /accounts/profile/<user_id>/
edit_profile()        - /accounts/profile/edit/
upload_profile_photo() - /accounts/profile/upload/
```

### Social
```
send_connection()     - /accounts/connections/send/
accept_connection()   - /accounts/connections/<id>/accept/
find_collaborators()  - /accounts/find-collaborators/
my_connections()      - /accounts/connections/
```

### Projects
```
create_project()      - /accounts/projects/create/
project_list()        - /accounts/projects/
project_detail()      - /accounts/projects/<id>/
my_projects()         - /accounts/my-projects/
search_projects()     - /accounts/search-projects/
add_team_member()     - /accounts/projects/<id>/add-team/
```

### Comments
```
project_comments()    - /accounts/projects/<id>/comments/
post_comment()        - /accounts/projects/<id>/comments/ (POST)
edit_comment()        - /accounts/comments/<id>/ (PUT)
delete_comment()      - /accounts/comments/<id>/ (DELETE)
```

### Messages
```
messages_view()       - /accounts/messages/
send_message()        - /accounts/messages/send/
message_detail()      - /accounts/messages/<id>/
create_chat_room()    - /accounts/chat-rooms/
```

### Activity
```
activity_feed()       - /accounts/activity-feed/
user_activity()       - /accounts/user/<id>/activity/
```

---

## Key WebSocket Routes (Real-time)

| Route | Consumer | Purpose |
|-------|----------|---------|
| `ws://host/ws/project/<id>/` | ProjectUpdateConsumer | Project updates |
| `ws://host/ws/activity-feed/` | ActivityFeedConsumer | Live activity |
| `ws://host/ws/notifications/` | NotificationConsumer | Real-time alerts |

### WebSocket Messages

**ProjectUpdateConsumer:**
```json
{
  "type": "project.status_update",
  "status": "in_progress",
  "timestamp": "2026-02-07T10:30:00Z"
}
```

```json
{
  "type": "project.comment_posted",
  "text": "Great work!",
  "author": "john_doe"
}
```

**ActivityFeedConsumer:**
```json
{
  "type": "activity.new",
  "action": "created_project",
  "user": "jane_smith",
  "timestamp": "2026-02-07T10:30:00Z"
}
```

---

## File Locations Quick Lookup

### Backend Core
```
auth_project/
├── accounts/models.py         ← Database models
├── accounts/views.py          ← HTTP endpoint logic
├── accounts/consumers.py       ← WebSocket handlers
├── accounts/routing.py        ← WebSocket URL patterns
├── accounts/serializers.py    ← API data formatters
├── accounts/forms.py          ← Form validation
├── accounts/urls.py           ← URL routing
└── accounts/templates/        ← HTML templates
```

### Configuration
```
auth_project/
├── auth_project/settings.py   ← Django settings
├── auth_project/asgi.py       ← ASGI (WebSocket)
├── auth_project/wsgi.py       ← WSGI (HTTP)
└── auth_project/urls.py       ← Project routing
```

### Frontend
```
auth_project/
├── static/js/
│   ├── realtime-updates.js    ← WebSocket client
│   ├── api-utils.js           ← HTTP utilities
│   ├── comments-handler.js    ← Comments UI
│   └── messages-ui.js         ← Messages UI
└── templates/                 ← HTML files
```

---

## Common Patterns

### Creating a Model
```python
# In accounts/models.py
class MyModel(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=200)
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return self.title
```

### Creating a View
```python
# In accounts/views.py
@login_required
def my_view(request):
    """View docstring"""
    if request.method == 'POST':
        # Handle form submission
        messages.success(request, 'Success!')
        return redirect('view_name')
    
    # GET request
    context = {}
    return render(request, 'template.html', context)
```

### Creating an API Endpoint
```python
# In accounts/serializers.py
class MySerializer(serializers.ModelSerializer):
    class Meta:
        model = MyModel
        fields = ['id', 'title', 'created_at']

# In accounts/views.py (REST)
class MyListView(generics.ListCreateAPIView):
    queryset = MyModel.objects.all()
    serializer_class = MySerializer
    permission_classes = [permissions.IsAuthenticated]
```

### Broadcasting via WebSocket
```python
# In accounts/views.py
from channels.layers import get_channel_layer

async_to_sync(get_channel_layer().group_send)(
    'group_name',
    {
        'type': 'message.sent',
        'message': 'Hello!'
    }
)
```

### Handling WebSocket Message
```python
# In accounts/consumers.py
async def message_sent(self, event):
    """Receive message from group"""
    await self.send(text_data=json.dumps({
        'type': 'message',
        'message': event['message']
    }))
```

---

## Settings & Configuration

### Enable Features in settings.py

```python
# Add to INSTALLED_APPS
INSTALLED_APPS = [
    'channels',
    'rest_framework',
    'corsheaders',
    'accounts',
]

# Configure Channels
ASGI_APPLICATION = 'auth_project.asgi.application'

CHANNEL_LAYERS = {
    'default': {
        'BACKEND': 'channels_redis.core.RedisChannelLayer',
        'CONFIG': {
            'hosts': [('127.0.0.1', 6379)],
        },
    },
}

# REST Framework
REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': [
        'rest_framework.authentication.SessionAuthentication',
    ],
    'DEFAULT_PERMISSION_CLASSES': [
        'rest_framework.permissions.IsAuthenticated',
    ],
}

# CORS
CORS_ALLOWED_ORIGINS = [
    'http://localhost:3000',
    'https://yourdomain.com',
]

# Email
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = 'smtp-relay.brevo.com'
EMAIL_PORT = 587
EMAIL_USE_TLS = True
EMAIL_HOST_USER = 'your-email@example.com'
EMAIL_HOST_PASSWORD = 'your-api-key'
```

---

## Deployment Checklist

- [ ] Set `DEBUG = False` in settings.py
- [ ] Configure `ALLOWED_HOSTS` with your domain
- [ ] Set `SECRET_KEY` to random value
- [ ] Configure database (PostgreSQL)
- [ ] Configure Redis for Channels
- [ ] Set up email backend
- [ ] Configure static files
- [ ] Enable HTTPS
- [ ] Set up CORS properly
- [ ] Update Procfile to use Daphne
- [ ] Deploy to Render/Railway
- [ ] Run `python manage.py migrate`
- [ ] Create superuser
- [ ] Test WebSocket connection

---

## Common Commands

### Django Management
```bash
# Create migrations
python manage.py makemigrations

# Apply migrations
python manage.py migrate

# Create superuser
python manage.py createsuperuser

# Run development server (HTTP only)
python manage.py runserver

# Run with Daphne (HTTP + WebSocket)
daphne -b 127.0.0.1 -p 8000 auth_project.asgi:application

# Collect static files
python manage.py collectstatic

# Shell (interact with models)
python manage.py shell

# Run tests
python manage.py test

# Flush database
python manage.py flush
```

### Git
```bash
# Add changes
git add .

# Commit
git commit -m "Fix: Description"

# Push
git push origin main

# Pull
git pull origin main
```

### Database
```bash
# Reset migrations
python manage.py migrate accounts zero

# Create backup
pg_dump DATABASE_NAME > backup.sql

# Restore backup
psql DATABASE_NAME < backup.sql
```

---

## Troubleshooting Quick Links

### Issue: 404 on WebSocket
- **Cause:** Using `python manage.py runserver` (HTTP only)
- **Fix:** Use Daphne: `daphne -b 127.0.0.1 -p 8000 auth_project.asgi:application`
- **Reference:** COMPLETE_SOLUTION_SUMMARY.txt

### Issue: Port 8000 Already in Use
- **Command:** `lsof -i :8000` (Linux/Mac) or `netstat -ano | findstr :8000` (Windows)
- **Fix:** Kill the process or use different port: `daphne -b 127.0.0.1 -p 9000 ...`

### Issue: Database Migration Errors
- **Fix:** `python manage.py migrate --fake accounts zero && python manage.py migrate`

### Issue: Static Files Not Loading
- **Fix:** `python manage.py collectstatic --noinput`

### Issue: Email Not Sending
- **Check:** Email credentials in settings.py
- **Check:** Brevo account active and API key valid
- **Test:** `python manage.py shell` then test sending

### Issue: WebSocket Connection Refused
- **Check:** Daphne running and listening on correct port
- **Check:** Browser console for CORS errors
- **Check:** Redis connection available

---

## Performance Tips

### Database
- Add `.select_related()` for ForeignKey fields
- Add `.prefetch_related()` for ManyToMany fields
- Use `.only()` or `.defer()` to limit fields
- Add database indexes for frequently queried fields
- Use `.count()` instead of `len()` on querysets

### Frontend
- Lazy load images with `loading="lazy"`
- Debounce rapid function calls
- Use WebSocket instead of polling
- Cache API responses locally
- Minify CSS/JavaScript

### Server
- Enable Redis caching
- Use connection pooling
- Configure Gunicorn workers properly
- Use CDN for static files
- Enable gzip compression

---

## Testing Examples

```python
# In accounts/tests.py
from django.test import TestCase
from django.test.client import Client
from accounts.models import StudentProfile, Project
from django.contrib.auth.models import User

class StudentProfileTestCase(TestCase):
    def setUp(self):
        self.user = User.objects.create_user('testuser', 'test@test.com', 'pass123')
        self.profile = StudentProfile.objects.create(user=self.user, full_name='Test User')
    
    def test_profile_creation(self):
        self.assertEqual(self.profile.user, self.user)
        self.assertEqual(self.profile.full_name, 'Test User')
    
    def test_profile_update(self):
        self.profile.bio = 'Updated bio'
        self.profile.save()
        self.assertEqual(self.profile.bio, 'Updated bio')

class ProjectViewTestCase(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user('testuser', 'test@test.com', 'pass123')
        self.project = Project.objects.create(
            owner=self.user,
            title='Test Project',
            description='Test Description'
        )
    
    def test_project_list_view(self):
        response = self.client.get('/accounts/projects/')
        self.assertEqual(response.status_code, 200)
    
    def test_project_detail_view(self):
        response = self.client.get(f'/accounts/projects/{self.project.id}/')
        self.assertEqual(response.status_code, 200)
    
    def test_project_creation(self):
        self.client.login(username='testuser', password='pass123')
        response = self.client.post('/accounts/projects/create/', {
            'title': 'New Project',
            'description': 'New Description',
            'category': 'Web Development'
        })
        self.assertEqual(Project.objects.count(), 2)
```

---

## API Usage Examples

### Create a Project (via Fetch)
```javascript
const response = await fetch('/accounts/projects/create/', {
    method: 'POST',
    headers: {
        'Content-Type': 'application/json',
        'X-CSRFToken': getCookie('csrftoken')
    },
    body: JSON.stringify({
        title: 'My Project',
        description: 'Project description',
        category: 'Web Development'
    })
});

const data = await response.json();
console.log(data);
```

### Send a Message
```javascript
const response = await fetch('/accounts/messages/send/', {
    method: 'POST',
    headers: {
        'Content-Type': 'application/json',
        'X-CSRFToken': getCookie('csrftoken')
    },
    body: JSON.stringify({
        receiver_id: 123,
        content: 'Hello!'
    })
});
```

### Get Comments
```javascript
const response = await fetch(`/accounts/projects/${projectId}/comments/`);
const comments = await response.json();
console.log(comments);
```

---

## Resources

### Documentation Files
- `CODEBASE_ANALYSIS_COMPLETE_2026_DETAILED.md` - Full architecture
- `COMPLETE_SOLUTION_SUMMARY.txt` - WebSocket fix
- `COMPREHENSIVE_CODE_ANALYSIS_2026_FINAL.md` - Detailed analysis

### Key Files to Study
1. `accounts/models.py` - Understand data structure
2. `accounts/views.py` - Understand business logic
3. `accounts/consumers.py` - Understand real-time features
4. `auth_project/asgi.py` - Understand WebSocket routing
5. `static/js/realtime-updates.js` - Understand frontend

### External References
- Django 5.2 Docs: https://docs.djangoproject.com/en/5.2/
- Django Channels: https://channels.readthedocs.io/
- REST Framework: https://www.django-rest-framework.org/
- PostgreSQL: https://www.postgresql.org/docs/

---

## Contact & Support

For questions about:
- **Code Structure:** See CODEBASE_ANALYSIS_COMPLETE_2026_DETAILED.md
- **WebSocket Issues:** See COMPLETE_SOLUTION_SUMMARY.txt
- **Deployment:** See Procfile and railway.json
- **Testing:** See accounts/tests.py

---

Generated: February 7, 2026  
Last Updated: 2026-02-07  
Status: Current & Complete ✅
