# UniSync - Quick Reference Guide

## File Structure At a Glance

```
auth_project/
├── auth_project/          # Django config
│   ├── settings.py        # All settings: DB, email, auth, logging
│   ├── urls.py            # Main URL router
│   └── wsgi.py / asgi.py  # Application servers
│
├── accounts/              # Main app
│   ├── models.py          # 15+ models (User, Project, Message, etc.)
│   ├── views.py           # 100+ views (3300+ lines)
│   ├── urls.py            # 130+ URL patterns
│   ├── forms.py           # Registration, login, profile forms
│   ├── serializers.py     # REST API serializers
│   ├── permissions.py     # Custom permissions
│   ├── utils.py           # NLP, filtering, sanitization
│   │
│   ├── services/auth_service.py    # Auth business logic
│   ├── chat_api.py        # Chat/messaging REST API
│   ├── comment_api.py     # Comments REST API
│   ├── views_contact.py   # Contact page
│   │
│   ├── *_mail_backend.py  # Email backends (Brevo, ZeptoMail)
│   │
│   ├── templates/         # HTML templates
│   ├── static/            # CSS, JS, images
│   ├── migrations/        # Database migrations
│   └── templatetags/      # Custom template filters
│
├── requirements.txt       # 50+ dependencies
├── manage.py             # Django CLI
└── Procfile / Render config
```

---

## Most Important Files

| File | Purpose | Lines | Key Classes/Functions |
|------|---------|-------|----------------------|
| `models.py` | Database schemas | 718 | StudentProfile, Project, OTP, Message, Comment, Connection, ChatRoom |
| `views.py` | Business logic | 3373 | login_view, register_view, post_project, find_collaborators, etc. |
| `settings.py` | Configuration | 356 | DB, email, auth, logging, static files |
| `urls.py` | URL routing | 129 | 130+ endpoints (auth, projects, messaging, API) |
| `forms.py` | Form validation | - | RegisterForm, LoginForm, StudentProfileForm |
| `serializers.py` | API responses | - | UserProfileSerializer, ChatRoomSerializer |
| `chat_api.py` | Messaging API | - | ChatRoomListCreateView, MessageListCreateView |
| `comment_api.py` | Comments API | - | add_comment, get_comments, delete_comment |
| `utils.py` | Utilities | - | StudentProfileNLP, ProjectVisibilityFilter, sanitize_input |
| `auth_service.py` | Auth service | 470 | AuthService.send_welcome_back_email |

---

## Core Models (Cheat Sheet)

### User-related
- **User** (Django built-in) - username, email, password
- **StudentProfile** - full_name, college, bio, skills, interests, profile_photo
- **UserStatus** - online/offline status
- **UserStats** - counters (projects, connections, followers)

### Content
- **Project** - title, description, team, status, visibility
- **Comment** - content, author, project
- **Like** - user, project/comment

### Social
- **Connection** - sender, receiver, status (pending/accepted/rejected)
- **Follow** - follower, following
- **Notification** - user, actor, action_type, is_read

### Messaging
- **ChatRoom** - name, members, owner, is_group
- **Message** - room, sender, content, is_read
- **ChatRoomMember** - chat room members
- **MessageFile** - file attachments
- **MessageReaction** - emoji reactions
- **Draft** - message drafts
- **MessageReadStatus** - read tracking

### Projects
- **ProjectTeam** - team management
- **ProjectTeamMember** - team members
- **ProjectTeamInvitation** - team invites
- **ProjectTask** - task management
- **ProjectMilestone** - project milestones

### Activity
- **Activity** - action tracking (project_posted, comment_added, etc.)
- **OTP** - login/registration/reset codes

---

## Authentication Methods

### OTP-Based (Recommended)
```
Login: Email → Generate 6-digit OTP → Email OTP → Verify → Logged in
```
- Expires in 5 minutes
- No password storage needed
- Multiple fallback email backends

### Password-Based
```
Login: Username + Password → Django ModelBackend → Logged in
```

### Social OAuth
```
Google/GitHub OAuth → Allauth → Auto-signup/login
```

---

## API Endpoint Categories

### Authentication (6)
- `/login/`, `/register/`, `/logout/`
- `/verify-otp/{purpose}/`, `/resend-otp/{purpose}/`
- `/forgot-password/`, `/reset-password/`

### Profile (5)
- `/student-profile/`, `/student-details/`
- `/user-profile/{id}/`, `/user/{username}/`
- `/edit-profile/`

### Projects (5)
- `/post-project/`, `/edit-project/{id}/`, `/delete-project/{id}/`
- `/project-detail/{id}/`, `/like-project/{id}/`

### Social (7)
- `/find-collaborators/`, `/send-connection-request/{id}/`
- `/accept-connection/{id}/`, `/reject-connection/{id}/`
- `/my-connections/`, `/follow/{id}/`

### Messaging (8)
- `/chat-rooms/`, `/chat-rooms/{id}/`
- `/messages/`, `/messages/{id}/`
- `/messages/search/`, `/direct-message/`

### Comments (4)
- `/projects/{id}/comments/`, `/projects/{id}/comments/add/`
- `/comments/{id}/delete/`, `/comments/{id}/edit/`

### Notifications (2)
- `/notifications/`, `/mark-notification-read/{id}/`

### Utilities (5)
- `/check-username/`, `/check-email/`, `/user-stats/`
- `/college-search/`, `/validate-college/`

---

## Configuration Checklist

### Database
- [ ] PostgreSQL configured (or SQLite for dev)
- [ ] DATABASE_URL set in .env
- [ ] Migrations applied: `python manage.py migrate`

### Email
- [ ] BREVO_API_KEY set (primary)
- [ ] ZEPTO_MAIL_API_KEY set (fallback)
- [ ] EMAIL_HOST_USER/PASSWORD set (SMTP fallback)
- [ ] DEFAULT_FROM_EMAIL set

### Security
- [ ] SECRET_KEY set in .env
- [ ] DEBUG=False in production
- [ ] ALLOWED_HOSTS configured
- [ ] SECURE_SSL_REDIRECT=True in production
- [ ] SESSION_COOKIE_SECURE=True in production
- [ ] CSRF_COOKIE_SECURE=True in production

### Social Auth
- [ ] GOOGLE_CLIENT_ID/SECRET set
- [ ] GITHUB_CLIENT_ID/SECRET set
- [ ] OAuth redirect URLs configured

### External APIs
- [ ] RAPIDAPI_KEY set for college search
- [ ] AWS S3 configured (optional, for storage)

---

## Common Code Patterns

### Protect View with Login
```python
@login_required
def my_view(request):
    # User must be logged in
    return render(request, 'template.html')
```

### Check User Has Permission
```python
def my_view(request):
    if not request.user.is_authenticated:
        return HttpResponseForbidden("Access denied")
    # Continue
```

### Send Email
```python
from django.core.mail import send_mail

send_mail(
    subject="Your OTP Code",
    message=f"Your OTP is: {otp_code}",
    from_email=settings.DEFAULT_FROM_EMAIL,
    recipient_list=[email],
)
```

### Create Notification
```python
Notification.objects.create(
    user=recipient,
    actor=current_user,
    action_type="like",
    content=f"{current_user.username} liked your project"
)
```

### Query Filter
```python
# Find projects by user's college
projects = Project.objects.filter(
    owner__student_profile__college=user_college
).order_by('-created_at')

# Search projects
projects = Project.objects.filter(
    Q(title__icontains=query) | Q(description__icontains=query)
)
```

### REST API View
```python
from rest_framework import generics

class ProjectListView(generics.ListCreateAPIView):
    queryset = Project.objects.all()
    serializer_class = ProjectSerializer
    permission_classes = [permissions.IsAuthenticated]
```

---

## Deployment Steps

### Local Development
```bash
cd auth_project
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
pip install -r requirements.txt
cp .env.template .env
# Edit .env with your settings
python manage.py migrate
python manage.py runserver
```

### Production (Render)
```bash
1. Push code to GitHub
2. Connect Render to GitHub repo
3. Set environment variables in Render dashboard
4. Deploy from main branch
5. Run migrations: python manage.py migrate
6. Collect static: python manage.py collectstatic
```

---

## Troubleshooting

### OTP not sending
- Check email backend in settings.py
- Verify email credentials (.env)
- Check logs in `logs/django.log`
- Try console backend: EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'

### Login page redirects infinitely
- Check LOGIN_URL setting
- Ensure session middleware is enabled
- Clear browser cookies and cache

### Profile picture not appearing
- Check MEDIA_URL and MEDIA_ROOT in settings
- Verify file uploaded successfully
- Check file permissions
- Use full URL: `{{ user.student_profile.profile_photo.url }}`

### Project not showing in feed
- Check project visibility setting
- Verify user's college matches (if college-specific)
- Check pagination (might be on page 2)
- Check ProjectVisibilityFilter logic

### Comments not loading
- Verify comment_api.py endpoints are correct
- Check CSRF token in POST requests
- Inspect network tab in browser dev tools
- Check Django logs for errors

### Performance slow
- Check database queries (Django debug toolbar)
- Clear Redis cache
- Enable query caching
- Check static file compression
- Monitor with `django-performance-monitor`

---

## Database Query Examples

### Find users with Python skill
```python
from accounts.models import StudentProfile
users = StudentProfile.objects.filter(skills__contains='Python')
```

### Count projects by college
```python
from django.db.models import Count
stats = StudentProfile.objects.values('college').annotate(
    projects=Count('user__project')
).order_by('-projects')
```

### Get unread messages
```python
unread = Message.objects.filter(is_read=False, recipient=user)
```

### Get pending connections
```python
pending = Connection.objects.filter(receiver=user, status='pending')
```

### Get recent activity
```python
recent = Activity.objects.filter(user=user).order_by('-timestamp')[:10]
```

---

## Settings Overview

| Setting | Default | Purpose |
|---------|---------|---------|
| DEBUG | True | Development mode |
| SECRET_KEY | Auto-generated | Session/CSRF security |
| ALLOWED_HOSTS | localhost,127.0.0.1 | Allowed domains |
| DATABASE_URL | SQLite (dev) | Database connection |
| EMAIL_BACKEND | Console (dev) | Email service |
| SECURE_SSL_REDIRECT | False | Enforce HTTPS |
| SESSION_COOKIE_SECURE | False | HTTPS-only cookies |
| CSRF_COOKIE_SECURE | False | HTTPS-only CSRF |
| INSTALLED_APPS | 13 apps | Django modules + accounts |
| MIDDLEWARE | 8 handlers | Request/response processing |
| REST_FRAMEWORK | Settings | DRF configuration |

---

## Logging

### Log Files
- `logs/django.log` - All application logs
- `logs/error.log` - Error-level logs only

### Log Levels (by importance)
1. **DEBUG** - Detailed debugging info
2. **INFO** - General info messages
3. **WARNING** - Warning messages
4. **ERROR** - Error messages
5. **CRITICAL** - Critical errors

### View Logs
```bash
# Last 100 lines
tail -100 logs/django.log

# Follow in real-time
tail -f logs/django.log

# Search for errors
grep ERROR logs/error.log
```

---

## Performance Tips

1. **Enable Caching**
   - Set up Redis
   - Add `@cache_page(60*15)` to views
   - Cache expensive queries

2. **Optimize Queries**
   - Use `select_related()` for ForeignKey
   - Use `prefetch_related()` for M2M
   - Limit fields with `.values()`

3. **Static Files**
   - Run `collectstatic` in production
   - Use WhiteNoise for serving
   - Set far-future Cache-Control headers

4. **Database**
   - Index frequently searched fields
   - Use pagination (default 10/page)
   - Monitor slow queries

5. **Frontend**
   - Minify CSS/JS
   - Lazy load images
   - Compress responses (gzip)

---

## Testing

### Run Tests
```bash
# All tests
pytest

# Specific test file
pytest tests/test_auth.py

# With coverage
pytest --cov=accounts

# Verbose output
pytest -v
```

### Test Database
- Uses separate test database
- Transactions rolled back after each test
- Fixtures in `tests/fixtures/`

---

## Commands Reference

```bash
# Django management
python manage.py runserver                 # Start dev server
python manage.py migrate                   # Apply migrations
python manage.py makemigrations            # Create migrations
python manage.py createsuperuser           # Create admin user
python manage.py collectstatic             # Collect static files
python manage.py shell                     # Interactive Python shell

# Git
git status                                 # Check changes
git add .                                  # Stage files
git commit -m "message"                    # Commit changes
git push origin main                       # Push to GitHub

# Virtual environment
python -m venv venv                        # Create venv
source venv/bin/activate                  # Activate (Linux/Mac)
venv\Scripts\activate                      # Activate (Windows)
pip install -r requirements.txt            # Install packages
pip freeze > requirements.txt              # Update requirements
```

---

## Support Resources

- **Django Docs**: https://docs.djangoproject.com/
- **DRF Docs**: https://www.django-rest-framework.org/
- **Allauth Docs**: https://django-allauth.readthedocs.io/
- **Channels Docs**: https://channels.readthedocs.io/
- **Celery Docs**: https://docs.celeryproject.org/

---

## Last Updated
January 15, 2024

---

## Contributors
- Backend development team
- Frontend team
- DevOps team

---

## License
MIT (or your license here)
