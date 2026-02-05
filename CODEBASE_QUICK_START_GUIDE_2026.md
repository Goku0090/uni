# Unisync Codebase - Quick Start Guide 2026

## What is Unisync?
A Django-based platform for university students to:
- Share & discover projects
- Find team members for collaboration
- Connect with peers (messaging, profiles, activity feeds)
- Post projects with tech requirements

---

## 5-Minute Codebase Overview

### The Stack
```
Frontend:  Django Templates (HTML/CSS/JS)
Backend:   Django 4.2.8 + DRF (REST API)
Database:  PostgreSQL
Messaging: Redis + Channels (WebSocket)
Email:     Zeptomail / Brevo
Auth:      OTP + Google OAuth + GitHub OAuth
Storage:   AWS S3
Deploy:    Render
```

### Core App Structure
```
auth_project/           # Django project config
├── settings.py        # Everything: apps, databases, email, auth
├── urls.py            # Main routes
└── asgi.py            # WebSocket support

accounts/              # Main app (all business logic)
├── models.py          # 16 database models
├── views.py           # 50+ view functions
├── urls.py            # API + template routes
├── serializers.py     # API response formatters
├── forms.py           # Login/Registration forms
├── comment_api.py     # Comment endpoints
├── chat_api.py        # Messaging endpoints
└── services/          # Business logic services
```

---

## Key Database Models (Quick Reference)

### User & Profile
- **User** (Django built-in) - username, email, password
- **StudentProfile** - college, interests, skills, bio, profile photo
- **OTP** - 6-digit codes for login/signup (5-min expiry)

### Projects
- **Project** - title, description, tech stack, looking_for (who to find)
- **ProjectTeam** - team composition
- **ProjectTask** - individual tasks
- **Comment** - comments on projects
- **Like** - users liking projects

### Social
- **Connection** - friend requests (pending/accepted/rejected)
- **Follow** - users following each other
- **Activity** - activity feed (who did what)

### Messaging
- **Message** - sender → receiver OR ChatRoom
- **ChatRoom** - direct chat or group chat
- **ChatRoomMember** - who's in the room + role
- **MessageReadStatus** - who read what message
- **File** - file uploads

### Notifications
- **Notification** - alerts for connection requests, messages, likes, comments

---

## Most Important Files to Know

### 1. **settings.py** (The Brain)
- Configures EVERYTHING: databases, apps, email, auth, caching
- Where to add/remove features
- Environment variables loaded here

### 2. **models.py** (The Data)
- 16 models defining what data is stored
- Relationships between users, projects, messages, etc.
- Methods like `OTP.verify_otp()`, `Project.get_technologies_list()`

### 3. **views.py** (The Logic)
- 3300+ lines of business logic
- Key functions:
  - `register_view()` - Sign up with OTP
  - `login_view()` - Login with email/OTP
  - `project_feed()` - List projects
  - `create_project_view()` - Create new project
  - `student_profile_view()` - View user profile
  - `find_collaborators()` - Search for team members

### 4. **urls.py** (The Routes)
- Maps HTTP requests to view functions
- Defines both API endpoints and template routes

### 5. **serializers.py** (The API Formatter)
- Converts database models to JSON for API responses
- Used by DRF

---

## Common Workflows

### User Signup
```
1. User fills registration form
2. system generates 6-digit OTP
3. OTP sent to email (Zeptomail)
4. User enters OTP
5. views.otp_verification() validates OTP
6. User + StudentProfile created
7. User logged in
```

### Create & Share Project
```
1. User logs in
2. Clicks "Create Project"
3. Fills form: title, description, tech stack, "looking_for"
4. Form saved to database
5. Project appears in feed
6. Other users can like/comment
7. Activity logged to Activity model
```

### Send Message
```
1. User opens chat
2. Selects recipient OR group
3. Sends message
4. Message saved to Message model
5. MessageReadStatus updated when recipient opens
6. Notification created
7. Redis channels broadcast to WebSocket (real-time)
```

### Find Collaborators
```
1. User fills profile: interests, skills, project_interests
2. Clicks "Find Collaborators"
3. views.find_collaborators() called
4. StudentProfileNLP.match_profiles() calculates similarity
5. Returns ranked list of compatible users
6. User can send Connection requests
```

---

## API Endpoints (Quick Reference)

### Authentication
```
POST   /register/              Create new user + OTP
POST   /login/                 Login with OTP
POST   /otp-verify/            Verify OTP code
GET    /accounts/sociallogin/  Google/GitHub login
```

### Profile
```
GET    /api/user/profile/      Get logged-in user's profile
GET    /profile/<username>/    View another user's profile
POST   /edit-profile/          Update profile
```

### Projects
```
GET    /api/projects/          List all projects (paginated)
POST   /api/projects/          Create new project
GET    /api/projects/<id>/     Get project details
PUT    /api/projects/<id>/     Edit project
DELETE /api/projects/<id>/     Delete project
GET    /projects/              Project feed (template view)
```

### Comments
```
POST   /api/comments/          Add comment to project
GET    /api/comments/<id>/     Get comments on project
DELETE /api/comments/<id>/     Delete comment
```

### Messages
```
POST   /api/messages/          Send message
GET    /api/messages/          Get message history
GET    /messages/              Chat interface (template)
```

### Connections
```
GET    /api/connections/       List connections
POST   /api/connections/       Send connection request
PUT    /api/connections/<id>/  Accept/reject request
```

### Notifications
```
GET    /api/notifications/     Get user's notifications
PUT    /api/notifications/<id>/ Mark as read
DELETE /api/notifications/<id>/ Delete notification
```

---

## View Function Template

Most views follow this pattern:

```python
@login_required
def view_name(request):
    """Docstring explaining what this does"""
    
    # 1. Get data from database
    obj = Model.objects.get(id=request.GET.get('id'))
    
    # 2. Check permissions
    if obj.user != request.user:
        return HttpResponseForbidden()
    
    # 3. Handle POST requests
    if request.method == 'POST':
        form = SomeForm(request.POST, instance=obj)
        if form.is_valid():
            form.save()
            messages.success(request, "Success!")
            return redirect('some_url')
    else:
        form = SomeForm(instance=obj)
    
    # 4. Render template
    return render(request, 'template.html', {'form': form, 'obj': obj})
```

---

## Important Constants

### Project Categories
```python
CATEGORIES = [
    'web',        # Web Development
    'mobile',     # Mobile Apps
    'ai',         # AI/ML
    'data',       # Data Science
    'blockchain', # Blockchain
    'iot',        # IoT
    'game',       # Game Development
    'other',      # Other
]
```

### Notification Types
```python
NOTIFICATION_TYPES = [
    'connection_request',  # Someone asked to connect
    'connection_accepted', # Connection accepted
    'message',             # New message
    'project_like',        # Someone liked your project
    'project_comment',     # Someone commented
    'team_invitation',     # Invited to team
    'follow',              # Someone followed you
]
```

### Activity Types
```python
ACTIVITY_TYPES = [
    'profile_updated',     # User updated profile
    'project_created',     # User created project
    'project_liked',       # User liked project
    'connection_made',     # New connection
    'message_sent',        # Message sent
    'comment_added',       # Comment added
    'user_followed',       # User followed
    'task_completed',      # Task completed
]
```

### Connection Status
```python
STATUS_CHOICES = [
    'pending',   # Waiting for response
    'accepted',  # Connection accepted
    'rejected',  # Connection rejected
]
```

---

## How to Add a New Feature

### Example: Add "Recommended Projects" Feature

1. **Create Model** (models.py)
```python
class ProjectRecommendation(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    project = models.ForeignKey(Project, on_delete=models.CASCADE)
    score = models.FloatField()  # Matching score
    created_at = models.DateTimeField(auto_now_add=True)
```

2. **Create View** (views.py)
```python
@login_required
def get_recommended_projects(request):
    recommendations = ProjectRecommendation.objects.filter(
        user=request.user
    ).order_by('-score')[:10]
    return render(request, 'recommended.html', {'projects': recommendations})
```

3. **Add URL** (urls.py)
```python
path('recommended/', get_recommended_projects, name='recommended')
```

4. **Create Template** (templates/recommended.html)
```html
{% for rec in projects %}
    <div class="project-card">
        <h3>{{ rec.project.title }}</h3>
        <p>Match Score: {{ rec.score }}%</p>
    </div>
{% endfor %}
```

5. **Run Migration**
```bash
python manage.py makemigrations
python manage.py migrate
```

---

## Debugging Tips

### Check Logs
```python
import logging
logger = logging.getLogger(__name__)
logger.info(f"Debug: {variable}")  # Will show in console
```

### Django Shell
```bash
python manage.py shell

# Try queries
from accounts.models import Project
projects = Project.objects.all()
print(projects)
```

### Check Middleware/Request
```python
# In views.py
print(request.user)  # Current user
print(request.POST)  # Form data
print(request.GET)   # URL parameters
print(request.FILES) # Uploaded files
```

### Check Database
```bash
# Access Django admin
# http://localhost:8000/admin/

# Or use shell
python manage.py shell
>>> from accounts.models import Project
>>> Project.objects.filter(user__username='john')
```

---

## Common Gotchas

### Gotcha 1: User Not Logged In
```python
# ❌ Will crash if user not logged in
@login_required  # ✅ Add this decorator
def my_view(request):
    pass
```

### Gotcha 2: ForeignKey Not Loaded
```python
# ❌ Slow - queries database for each project owner
for project in Project.objects.all():
    print(project.user.username)  # Extra query!

# ✅ Better - load all owners in one query
projects = Project.objects.select_related('user')
for project in projects:
    print(project.user.username)
```

### Gotcha 3: Form Not Saving
```python
# ❌ Just checking is_valid() isn't enough
if form.is_valid():
    form.save()  # ✅ Must call save()

# ✅ Full pattern
if form.is_valid():
    form.save()
    messages.success(request, "Saved!")
    return redirect('success_url')
```

### Gotcha 4: OTP Expired
```
# OTP expires after 5 minutes
# If user takes too long, must generate new OTP
OTP.objects.filter(email=email).order_by('-created_at').first()
# Check: otp.is_valid()  # False if expired
```

---

## Performance Notes

### Fast Queries
```python
# ✅ Fast - uses index on user_id
Project.objects.filter(user=request.user)

# ✅ Fast - gets single object
Project.objects.get(id=1)

# ✅ Fast with prefetch
Project.objects.prefetch_related('comments').all()
```

### Slow Queries
```python
# ❌ Slow - no index
Project.objects.filter(description__contains="python")

# ❌ Slow - iterates all
Project.objects.all()  # Don't do this in production!

# ❌ Slow - N+1 problem
for project in Project.objects.all():
    print(project.user.username)  # Query per project!
```

---

## Deployment Checklist

Before deploying to Render:

- [ ] Set DEBUG=False in .env
- [ ] Set SECRET_KEY in .env (strong random string)
- [ ] Add ALLOWED_HOSTS in .env
- [ ] Configure PostgreSQL DATABASE_URL
- [ ] Set email credentials (Zeptomail/Brevo)
- [ ] Set AWS S3 credentials for file storage
- [ ] Set up Redis for caching/sessions
- [ ] Enable SSL (SECURE_SSL_REDIRECT=True)
- [ ] Run `python manage.py collectstatic`
- [ ] Run migrations: `python manage.py migrate`
- [ ] Create superuser if needed: `python manage.py createsuperuser`

---

## Quick Command Reference

```bash
# Setup
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt

# Database
python manage.py migrate
python manage.py makemigrations

# Run
python manage.py runserver

# Test
pytest
python manage.py test

# Admin
python manage.py createsuperuser
python manage.py shell

# Deployment
gunicorn auth_project.wsgi:application
```

---

## Files You'll Edit Most

1. **models.py** - Add/modify database tables
2. **views.py** - Add/modify business logic
3. **urls.py** - Add/modify routes
4. **templates/*.html** - Update UI
5. **serializers.py** - Modify API responses
6. **settings.py** - Configuration changes

---

## Getting Help

### Error Messages
- Check `logger.error()` in views
- Look at console output
- Check browser DevTools (Network tab)
- Django admin interface

### Documentation
- Django: https://docs.djangoproject.com
- DRF: https://www.django-rest-framework.org
- PostgreSQL: https://www.postgresql.org/docs

### Useful Files to Reference
- This file (CODEBASE_QUICK_START_GUIDE_2026.md)
- COMPLETE_CODEBASE_ANALYSIS_2026_FINAL.md
- Requirements.txt (all dependencies)
- .env.template (all configuration options)

---

**Last Updated**: February 2026
**Maintainer**: Development Team
**Repository**: https://github.com/Goku0090/uni
