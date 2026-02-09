# UniSync Codebase - Quick Navigation & Reference Guide

## 🚀 Quick Start

**What to read first:**
1. `CODEBASE_COMPLETE_ANALYSIS_2026_FINAL_COMPLETE.md` - Full architecture overview
2. This file - Quick navigation and common tasks

**Key File Locations:**
```
Models:        auth_project/accounts/models.py (1000+ lines)
Views:         auth_project/accounts/views.py (3400+ lines)
WebSocket:     auth_project/accounts/consumers.py
API:           auth_project/accounts/chat_api.py, comment_api.py
Frontend JS:   auth_project/static/js/realtime-updates.js
Settings:      auth_project/auth_project/settings.py
URLs:          auth_project/accounts/urls.py
```

---

## 📊 Data Models Quick Reference

### User & Authentication
```python
StudentProfile      # Extended user (profile, skills, interests)
OTP                 # One-time passwords (login, registration)
User (Django)       # Built-in Django user model
```

### Relationships
```python
Connection          # Connection requests between users
Follow              # User following relationships
```

### Messaging
```python
Message             # Direct messages & chat messages
ChatRoom            # Group chat rooms
ChatRoomMember      # Room membership & roles
MessageReadStatus   # Read status tracking per user
MessageReaction     # Emoji/text reactions to messages
MessageFile         # File attachments
```

### Projects & Teams
```python
Project             # Project definition & metadata
ProjectTeam         # Team for collaboration
ProjectTeamMember   # Team member with role
ProjectTeamInvitation  # Team joining invitations
ProjectTask         # Task tracking within project
ProjectMilestone    # Project milestones
```

### Activity & Engagement
```python
Activity            # User activities (posts, likes, follows)
Like                # Project likes
Comment             # Project comments
Notification        # Real-time notifications
```

---

## 🔌 API Endpoints Quick Map

### Chat & Messaging
```
GET/POST   /api/chat-rooms/                    # List/create chat rooms
GET        /api/chat-rooms/<id>/               # Get room details
GET        /api/chat-rooms/<id>/members/       # Get room members
GET/POST   /api/messages/                      # List/send messages
GET        /api/messages/search/               # Search messages
POST       /api/direct-message/                # Start direct chat
GET/POST   /api/drafts/                        # Draft messages
POST       /api/typing/                        # Typing indicator
```

### Comments
```
GET        /api/projects/<id>/comments/        # List comments
POST       /api/projects/<id>/comments/        # Add comment
PUT        /api/comments/<id>/                 # Edit comment
DELETE     /api/comments/<id>/                 # Delete comment
```

### User Profile
```
GET/PUT    /api/profile/                       # Your profile
GET        /api/users/<username>/              # View other profile
```

---

## 🔄 WebSocket Connections

### URL Patterns
```
ws://localhost/ws/project/<project_id>/       # Project updates
ws://localhost/ws/activity-feed/              # Activity feed
ws://localhost/ws/notifications/              # Notifications
```

### Event Types Received
```
project.initial_data                # Initial project state
project.status_update               # Status changed
project.member_added                # Team member joined
project.comment_posted              # New comment
project.task_updated                # Task status
activity.new_post                   # New project posted
activity.like                       # Project liked
notification.message                # New message
notification.connection_request     # Connection request
```

### Sending Events
```
status.update                       # Change project status
member.add                          # Add team member
comment.post                        # Post comment
task.update                         # Update task
```

---

## 🌐 View Functions Quick Reference

### Authentication (views.py)
```
/login/                  → login_view()
/register/               → register_view()
/verify-otp/<purpose>/   → verify_otp_view()
/logout/                 → logout_view()
/forgot-password/        → forgot_password_view()
/reset-password/         → reset_password_view()
```

### Projects
```
/post-project/           → post_project()
/project/<id>/           → project_detail()
/edit-project/<id>/      → edit_project()
/delete-project/<id>/    → delete_project()
/like-project/<id>/      → like_project()
/explore-projects/       → explore_projects_view()
/my-projects/            → my_projects_view()
```

### Social Features
```
/find-collaborators/     → find_collaborators()
/user/<username>/        → user_profile()
/student-profile/        → student_profile()
/connect/<user_id>/      → send_connection_request()
/accept-connection/<id>/ → accept_connection()
/reject-connection/<id>/ → reject_connection()
/my-connections/         → my_connections()
/follow/<user_id>/       → follow_user()
/activity-feed/          → activity_feed()
```

### Messaging
```
/messages/               → message_view()
/chat/<user_id>/         → chat_view()
/enhanced-messages/      → enhanced_messages_view()
/enhanced-chat/<room_id>/ → enhanced_chat_view()
/create-group-chat/      → create_group_chat()
```

### Other
```
/dashboard/              → dashboard_view()
/notifications/          → notifications_view()
/about/                  → about_view()
/help/                   → help_center_view()
```

---

## 🔐 Authentication Flow

### Email/OTP Login
```
1. User submits email on /login/
2. OTP.generate_otp(email, 'login') creates code
3. Email sent via Brevo/ZeptoMail
4. User goes to /verify-otp/login/
5. verify_otp_view() validates code
6. Session created, redirect to /dashboard/
```

### Social OAuth (Google, GitHub)
```
1. User clicks "Login with Google"
2. Redirected to OAuth provider
3. Provider redirects back with auth code
4. django-allauth handles code exchange
5. User authenticated & StudentProfile created
6. Redirect to dashboard
```

### Registration
```
1. User fills RegisterForm on /register/
2. register_view() validates email/password
3. OTP sent for email verification
4. User verifies with OTP
5. User account + StudentProfile created
```

---

## 🔍 Finding Things in the Codebase

### Where to find specific functionality:

**User Authentication**
- Models: `StudentProfile`, `OTP`, `User`
- Views: `register_view()`, `login_view()`, `verify_otp_view()`
- Forms: `RegisterForm`, `LoginForm`, `OTPVerificationForm`
- Email: `accounts/brevo_mail_backend.py`

**Messaging System**
- Models: `Message`, `ChatRoom`, `MessageReadStatus`
- Views: `message_view()`, `chat_view()`, `enhanced_chat_view()`
- API: `accounts/chat_api.py`
- Frontend: `static/js/api-utils.js`

**Project Management**
- Models: `Project`, `ProjectTeam`, `ProjectTask`
- Views: `post_project()`, `project_detail()`, `edit_project()`
- Forms: `ProjectForm`
- API: REST endpoints in `serializers.py`

**Real-time Updates**
- WebSocket: `accounts/consumers.py`
- Routing: `accounts/routing.py`
- Frontend: `static/js/realtime-updates.js`
- Signals: `accounts/signals_realtime.py`

**Collaboration Features**
- Models: `Connection`, `ProjectTeam`, `ProjectTeamInvitation`
- Views: `send_connection_request()`, `invite_to_team()`
- NLP: `StudentProfileNLP` in `utils.py`

**Notifications**
- Models: `Notification`, `Activity`
- Views: `notifications_view()`, `mark_notification_read()`
- API: Serialized in REST endpoints

---

## 📝 Common Tasks

### Add a New API Endpoint

1. Create serializer in `accounts/serializers.py`:
   ```python
   class MySerializer(serializers.ModelSerializer):
       class Meta:
           model = MyModel
           fields = ['id', 'field1', 'field2']
   ```

2. Create view in `accounts/chat_api.py` or create new API file:
   ```python
   from rest_framework import generics
   
   class MyListView(generics.ListCreateAPIView):
       queryset = MyModel.objects.all()
       serializer_class = MySerializer
   ```

3. Add URL in `accounts/urls.py`:
   ```python
   path('api/my-endpoint/', MyListView.as_view(), name='my-endpoint'),
   ```

4. Frontend JavaScript:
   ```javascript
   fetch('/api/my-endpoint/', {
       method: 'GET',
       headers: {
           'X-CSRFToken': getCookie('csrftoken')
       }
   }).then(r => r.json()).then(data => console.log(data));
   ```

### Add a New WebSocket Event

1. Create method in consumer (`accounts/consumers.py`):
   ```python
   async def my_custom_event(self, event):
       await self.send(json.dumps({
           'type': 'my.custom_event',
           'data': event['data']
       }))
   ```

2. Send from signal or view:
   ```python
   from channels.layers import get_channel_layer
   
   channel_layer = get_channel_layer()
   await channel_layer.group_send(
       'my_group_name',
       {'type': 'my.custom_event', 'data': {...}}
   )
   ```

3. Handle in frontend JavaScript:
   ```javascript
   socket.onmessage = (event) => {
       const data = JSON.parse(event.data);
       if (data.type === 'my.custom_event') {
           // Handle event
       }
   };
   ```

### Send an Email via Brevo

1. Configure in `settings.py`:
   ```python
   EMAIL_BACKEND = 'accounts.brevo_mail_backend.BrevoEmailBackend'
   BREVO_API_KEY = os.getenv('BREVO_API_KEY')
   ```

2. Use Django's send_mail:
   ```python
   from django.core.mail import send_mail
   
   send_mail(
       'Subject',
       'Message body',
       'from@example.com',
       ['to@example.com'],
       html_message='<p>HTML content</p>'
   )
   ```

3. Or use the backend directly:
   ```python
   from accounts.brevo_mail_backend import BrevoMailBackend
   backend = BrevoMailBackend()
   backend.send_messages([email_message])
   ```

### Implement Permission Check

1. Create permission class in `accounts/permissions.py`:
   ```python
   from rest_framework import permissions
   
   class IsProjectOwner(permissions.BasePermission):
       def has_object_permission(self, request, view, obj):
           return obj.owner == request.user
   ```

2. Use in view:
   ```python
   from rest_framework import viewsets
   from .permissions import IsProjectOwner
   
   class ProjectViewSet(viewsets.ModelViewSet):
       queryset = Project.objects.all()
       serializer_class = ProjectSerializer
       permission_classes = [IsProjectOwner]
   ```

3. Or use as decorator:
   ```python
   from .permissions import check_project_owner
   
   @check_project_owner
   def edit_project(request, project_id):
       # Only project owner can reach here
   ```

### Add Real-time Notification

1. Create signal handler in `accounts/signals_realtime.py`:
   ```python
   from django.db.models.signals import post_save
   from django.dispatch import receiver
   
   @receiver(post_save, sender=MyModel)
   def my_model_saved(sender, instance, created, **kwargs):
       if created:
           # Broadcast event
           channel_layer = get_channel_layer()
           async_to_sync(channel_layer.group_send)(
               'notifications',
               {
                   'type': 'notification.new_event',
                   'message': f'New {instance}'
               }
           )
   ```

2. Handle in NotificationConsumer:
   ```python
   async def notification_new_event(self, event):
       await self.send(json.dumps(event))
   ```

3. Listen in frontend:
   ```javascript
   const notifySocket = new WebSocket('ws://.../ws/notifications/');
   notifySocket.onmessage = (e) => {
       const data = JSON.parse(e.data);
       if (data.type === 'notification.new_event') {
           showNotification(data.message);
       }
   };
   ```

---

## 🐛 Debugging Tips

### Enable Debug Logging
```python
# In settings.py
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'handlers': {
        'console': {'class': 'logging.StreamHandler'},
    },
    'root': {'handlers': ['console'], 'level': 'DEBUG'},
}
```

### Test WebSocket Connection
```javascript
// In browser console
const ws = new WebSocket('ws://localhost:8000/ws/project/1/');
ws.onopen = () => console.log('✅ Connected');
ws.onmessage = (e) => console.log('📨', JSON.parse(e.data));
ws.onerror = (e) => console.error('❌', e);
```

### Check Database State
```bash
# SSH into server or local terminal
python manage.py shell

# Check a model
from accounts.models import Project
Project.objects.filter(owner__username='alice').values()

# Check WebSocket connections
from channels.layers import get_channel_layer
channel_layer = get_channel_layer()
```

### Monitor API Requests
```javascript
// In browser DevTools Network tab:
// Look for WebSocket connections
// Check Request/Response Headers for CSRF token
// Verify response status codes (200, 201, 404, 403, 500, etc.)
```

### Test Email Sending
```bash
python manage.py shell
from django.core.mail import send_mail
send_mail('Test', 'Hello', 'from@example.com', ['to@example.com'])
```

---

## 📚 Important Code Patterns

### Handling Project Visibility
```python
from accounts.utils import ProjectVisibilityFilter

# Get visible projects for current user
visible = ProjectVisibilityFilter.get_visible_projects(request.user)

# Check if user can view specific project
can_view = ProjectVisibilityFilter.can_view_project(request.user, project)
```

### NLP-based Skill Matching
```python
from accounts.utils import StudentProfileNLP

# Find similar users
similar = StudentProfileNLP.find_similar_users(request.user)

# Extract interests from text
interests = StudentProfileNLP.extract_skills('Python, JavaScript, Django')

# Calculate match score
score = StudentProfileNLP.calculate_match_score(user1, user2)
```

### Async WebSocket Broadcast
```python
from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync

channel_layer = get_channel_layer()
async_to_sync(channel_layer.group_send)(
    'activity_feed',  # Group name
    {
        'type': 'activity.event',  # Handler method
        'message': 'New activity',
        'data': {...}
    }
)
```

### Pagination Pattern
```python
from django.core.paginator import Paginator

def my_view(request):
    items = Model.objects.all()
    paginator = Paginator(items, 10)  # 10 per page
    page_obj = paginator.get_page(request.GET.get('page'))
    
    return render(request, 'template.html', {'page_obj': page_obj})
```

### Caching Pattern
```python
from django.core.cache import cache

def get_user_profile(user_id):
    # Try cache first
    cached = cache.get(f'profile_{user_id}')
    if cached:
        return cached
    
    # Fall back to database
    profile = StudentProfile.objects.get(user_id=user_id)
    
    # Store in cache (1 hour)
    cache.set(f'profile_{user_id}', profile, 3600)
    return profile
```

---

## 🔗 External Resources

- [Django Documentation](https://docs.djangoproject.com/)
- [Django REST Framework](https://www.django-rest-framework.org/)
- [Django Channels](https://channels.readthedocs.io/)
- [django-allauth](https://django-allauth.readthedocs.io/)
- [WebSocket Browser API](https://developer.mozilla.org/en-US/docs/Web/API/WebSocket)

---

## 📞 Quick Contacts & Config

### Environment Variables Needed
```
SECRET_KEY              # Django secret key
DEBUG                   # True for dev, False for production
DATABASE_URL           # PostgreSQL connection string
BREVO_API_KEY          # Email service API key
GOOGLE_OAUTH_KEY       # Google OAuth client ID
GOOGLE_OAUTH_SECRET    # Google OAuth secret
ALLOWED_HOSTS          # Comma-separated domain list
```

### Running Locally
```bash
# Start PostgreSQL
psql -U unisinq_user -d unisinq_db

# Run migrations
python manage.py migrate

# Create superuser
python manage.py createsuperuser

# Run development server (HTTP only)
python manage.py runserver

# Run with WebSocket support (separate terminal)
daphne -b 127.0.0.1 -p 8000 auth_project.asgi:application
```

### Production Deployment (Render)
```yaml
# render.yaml already configured
# Just push to GitHub and Render auto-deploys
git push origin main
```

---

## 🎯 Key Takeaways

1. **Models** - 15+ interconnected Django models
2. **Views** - 50+ view functions handling all business logic
3. **API** - REST endpoints for chat, messages, profiles, projects
4. **WebSocket** - Real-time updates via Django Channels
5. **Frontend** - Vanilla JS with CSS (no framework dependencies)
6. **Authentication** - Email/OTP + OAuth2
7. **Database** - PostgreSQL with proper relationships & indexes
8. **Deployment** - Ready for Render with ASGI/Daphne

---

**Last Updated:** 2026-02-09  
**Project:** UniSync/UniSinQ  
**Status:** ✅ Complete
