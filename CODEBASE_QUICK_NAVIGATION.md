# UniSync Codebase - Quick Navigation Guide

## 📂 PROJECT STRUCTURE AT A GLANCE

```
auth_project/
│
├── 📁 auth_project/              ← Django Project Settings
│   ├── settings.py               ← Database, Email, Cache, Security config
│   ├── urls.py                   ← Main URL routing (admin, accounts, api)
│   ├── asgi.py                   ← WebSocket configuration
│   ├── wsgi.py                   ← Production WSGI server
│   └── __init__.py
│
├── 📁 accounts/                  ← Main Application
│   ├── models.py                 ← All database models (16 models, 718 lines)
│   ├── views.py                  ← Core business logic (3311+ lines)
│   ├── views_contact.py          ← Contact/Privacy pages
│   ├── urls.py                   ← App URL routing (129 routes)
│   ├── serializers.py            ← REST API serializers
│   ├── forms.py                  ← Django forms for HTML forms
│   ├── permissions.py            ← REST API permissions
│   ├── utils.py                  ← Helper functions & NLP
│   │
│   ├── chat_api.py               ← Chat API wrapper
│   ├── chat_api_improved.py      ← Real messaging implementation
│   ├── comment_api.py            ← Comment system endpoints
│   │
│   ├── zepto_mail_backend.py     ← ZeptoMail email service
│   ├── brevo_mail_backend.py     ← Brevo email fallback
│   │
│   ├── 📁 services/              ← Business logic services
│   │   └── auth_service.py
│   │
│   ├── 📁 migrations/            ← Database migrations
│   │
│   ├── 📁 templates/             ← HTML templates (50+ files)
│   │   ├── base.html             ← Base layout template
│   │   ├── login.html            ← Login page
│   │   ├── register.html         ← Registration page
│   │   ├── dashboard.html        ← Main dashboard
│   │   ├── student_profile.html  ← Profile view
│   │   ├── project_detail.html   ← Project view
│   │   ├── messages.html         ← Messaging interface
│   │   └── [50+ other templates]
│   │
│   ├── 📁 static/                ← Static assets
│   │   ├── css/                  ← Stylesheets
│   │   ├── js/                   ← JavaScript files
│   │   └── images/               ← Static images
│   │
│   ├── 📁 templatetags/          ← Custom template filters
│   └── tests.py                  ← Unit tests
│
├── manage.py                     ← Django management CLI
├── requirements.txt              ← Python dependencies
├── .env                         ← Environment variables (NOT in git)
├── .env.template                ← Template for .env
├── Procfile                     ← Render deployment config
├── render.yaml                  ← Infrastructure config
└── [test files & docs]          ← Test scripts & documentation
```

---

## 🔍 FINDING CODE BY FEATURE

### AUTHENTICATION
| What | Where |
|------|-------|
| Login page | `accounts/templates/login.html` |
| Login logic | `views.py:login_view()` |
| Registration form | `accounts/templates/register.html` |
| Register logic | `views.py:register_view()` |
| OTP model | `models.py:OTP` (lines 55-123) |
| OTP sending | `views.py:verify_otp_view()` |
| Social auth config | `settings.py:allauth` |
| Password reset | `views.py:forgot_password_view()` |

### USER PROFILE
| What | Where |
|------|-------|
| Profile model | `models.py:StudentProfile` (lines 12-52) |
| Profile view page | `accounts/templates/student_profile.html` |
| Edit profile logic | `views.py:edit_profile()` |
| Edit profile form | `accounts/templates/edit_profile.html` |
| Other user profile | `views.py:user_profile()` |
| Profile API | `serializers.py:UserProfileSerializer` |
| Avatar upload | `models.py:profile_photo` field |

### PROJECTS
| What | Where |
|------|-------|
| Project model | `models.py:Project` (lines 270-303) |
| Create project page | `accounts/templates/post_project.html` |
| Create logic | `views.py:post_project()` |
| View project | `accounts/templates/project_detail.html` |
| Project details logic | `views.py:project_detail()` |
| Edit project | `views.py:edit_project()` |
| Delete project | `views.py:delete_project()` |
| Like project | `views.py:like_project()` |
| Like model | `models.py:Like` (lines 445-461) |
| Search projects | `views.py:search_projects()` |
| Project visibility | `views.py:ProjectVisibilityFilter` |

### CONNECTIONS & COLLABORATION
| What | Where |
|------|-------|
| Connection model | `models.py:Connection` (lines 126-146) |
| Send connection | `views.py:connect_view()` |
| Find collaborators | `views.py:find_collaborators()` |
| Accept connection | `views.py:accept_connection()` |
| Project member model | `models.py:ProjectMember` (lines 542-580) |
| Invite to team | `views.py:invite_to_team()` |
| Invitation model | `models.py:ProjectInvitation` (lines 582-634) |
| Team response | `views.py:respond_to_team_invitation()` |
| Remove member | `views.py:remove_team_member()` |

### MESSAGING & CHAT
| What | Where |
|------|-------|
| Message model | `models.py:Message` (lines 149-217) |
| ChatRoom model | `models.py:ChatRoom` (lines 252-308) |
| Chat template | `accounts/templates/chat.html` |
| Chat logic | `views.py:chat_view()` |
| Message API | `chat_api_improved.py` (full implementation) |
| Send message endpoint | `urls.py:89` (`/messages/`) |
| Message search | `chat_api_improved.py:MessageSearchView` |
| Read status | `models.py:MessageReadStatus` (lines 309-320) |
| Typing indicator | `chat_api_improved.py:TypingIndicatorView` |
| Reactions | `models.py:MessageReaction` (lines 230-241) |
| Draft messages | `models.py:Draft` (lines 347-368) |

### COMMENTS & SOCIAL
| What | Where |
|------|-------|
| Comment model | `models.py:Comment` (lines 384-418) |
| Comment API | `comment_api.py:add_comment()` |
| Get comments | `comment_api.py:get_comments()` |
| Edit comment | `comment_api.py:edit_comment()` |
| Delete comment | `comment_api.py:delete_comment()` |
| Follow model | `models.py:Follow` (lines 465-473) |
| Follow logic | `views.py:follow_user()` |
| Activity model | `models.py:Activity` (lines 475-508) |
| Activity feed | `views.py:activity_feed()` |

### NOTIFICATIONS
| What | Where |
|------|-------|
| Notification model | `models.py:Notification` (lines 322-383) |
| Notification view | `accounts/templates/notifications.html` |
| Notifications list | `views.py:notifications_view()` |
| Mark as read | `views.py:mark_notification_read()` |
| Create notification | `views.py:create_notification()` |
| Notification types | `models.py:Notification.TYPES` (lines 328-336) |

### EMAIL
| What | Where |
|------|-------|
| Email backend | `zepto_mail_backend.py` |
| Email config | `settings.py:EMAIL_BACKEND` |
| Brevo fallback | `brevo_mail_backend.py` |
| Contact form | `accounts/templates/contact_us.html` |
| Contact submission | `views_contact.py:contact_submit()` |

### FILES & STORAGE
| What | Where |
|------|-------|
| File model | `models.py:File` (lines 243-262) |
| AWS S3 config | `settings.py:DEFAULT_FILE_STORAGE` |
| Download file | `views.py:download_file()` |
| Profile photo | `models.py:StudentProfile.profile_photo` |

---

## 🛣️ URL ROUTING QUICK MAP

### Authentication Routes (all in accounts/)
```
/accounts/login/                     → login_view
/accounts/register/                  → register_view
/accounts/logout/                    → logout_view
/accounts/forgot-password/           → forgot_password_view
/accounts/reset-password/            → reset_password_view
/accounts/verify-otp/<purpose>/      → verify_otp_view
/accounts/resend-otp/<purpose>/      → resend_otp_view
```

### Profile Routes
```
/accounts/student-profile/           → student_profile
/accounts/student-details/           → student_details_view
/accounts/profile/                   → UserProfileView (API)
/accounts/user/<username>/           → user_profile
/accounts/user-profile/<id>/         → user_profile_api
```

### Project Routes
```
/accounts/post-project/              → post_project
/accounts/project-detail/<id>/       → project_detail
/accounts/edit-project/<id>/         → edit_project
/accounts/delete-project/<id>/       → delete_project
/accounts/like-project/<id>/         → like_project
/accounts/my-projects/               → my_projects
```

### Social Routes
```
/accounts/find-collaborators/        → find_collaborators
/accounts/connect/<user_id>/         → connect_view
/accounts/accept-connection/<id>/    → accept_connection
/accounts/reject-connection/<id>/    → reject_connection
/accounts/my-connections/            → my_connections
/accounts/follow/<user_id>/          → follow_user
/accounts/invite-to-team/<id>/       → invite_to_team
/accounts/respond-team-invitation/   → respond_to_team_invitation
```

### Messaging Routes
```
/accounts/messages/                  → message_view (HTML)
/accounts/chat/<user_id>/            → chat_view (HTML)
/accounts/enhanced-messages/         → enhanced_messages_view
/accounts/enhanced-chat/<room_id>/   → enhanced_chat_view
/accounts/create-group-chat/         → create_group_chat

# REST API
/accounts/chat-rooms/                → ChatRoomListCreateView
/accounts/chat-rooms/<id>/           → ChatRoomDetailView
/accounts/messages/                  → MessageListCreateView (API)
/accounts/messages/search/           → MessageSearchView
/accounts/conversations/             → ConversationListView
/accounts/typing/                    → TypingIndicatorView
```

### Comments API Routes
```
/accounts/api/projects/<id>/comments/      → get_comments
/accounts/api/projects/<id>/comments/add/  → add_comment
/accounts/api/comments/<id>/delete/        → delete_comment
/accounts/api/comments/<id>/edit/          → edit_comment
```

### Notification Routes
```
/accounts/notifications/             → notifications_view
/accounts/mark-notification-read/    → mark_notification_read
```

### Utility Routes
```
/accounts/dashboard/                 → dashboard_view
/accounts/activity-feed/             → activity_feed
/accounts/help/                      → help_center_view
/accounts/college-search/            → college_search_api
/accounts/validate-college/          → validate_college_api
/accounts/check-username/            → check_username_availability
/accounts/check-email/               → check_email_availability
/accounts/nlp-analyze/               → nlp_analyze_api
/accounts/user-stats/                → user_stats_api
```

### Static Routes
```
/accounts/privacy/                   → privacy_policy_view
/accounts/terms/                     → terms_of_service_view
/accounts/contact/                   → contact_us_view
/accounts/contact/submit/            → contact_submit
```

---

## 📋 MODELS QUICK REFERENCE

### Core Models (16 Total)
1. **StudentProfile** - User profile details
2. **OTP** - One-time password
3. **Connection** - User connections
4. **Message** - Direct messages
5. **ChatRoom** - Group chats
6. **MessageReadStatus** - Message read tracking
7. **MessageReaction** - Emoji reactions
8. **MessageFile** - File attachments
9. **File** - File storage
10. **Draft** - Draft messages
11. **Project** - User projects
12. **Like** - Project likes
13. **Comment** - Project comments
14. **Follow** - User follows
15. **Activity** - Activity feed
16. **Notification** - User notifications

### Support Models (6 Total)
- **ProjectMember** - Team membership
- **ProjectInvitation** - Team invitations
- **ProjectTask** - Project tasks
- **ProjectMilestone** - Project milestones
- **UserStats** - User statistics
- **ChatRoomMember** - Chat room membership

---

## 🔧 CONFIGURATION QUICK REFERENCE

### Settings File Location
`auth_project/settings.py`

### Key Configuration Sections
| Setting | Lines | Purpose |
|---------|-------|---------|
| DATABASE | 100-115 | PostgreSQL config |
| EMAIL_BACKEND | 130-135 | Email service |
| CACHES | 150-160 | Redis caching |
| CHANNEL_LAYERS | 140-150 | WebSocket config |
| AWS S3 | 200-210 | File storage |
| INSTALLED_APPS | 36-61 | Django apps |
| MIDDLEWARE | 64-73 | Request processing |
| TEMPLATES | 79-94 | Template config |

### Environment Variables (.env file)
```
DEBUG=True
SECRET_KEY=your_secret_key
ALLOWED_HOSTS=localhost,127.0.0.1

# Database
DB_NAME=unisync
DB_USER=postgres
DB_PASSWORD=password
DB_HOST=localhost
DB_PORT=5432

# Email
ZEPTOMAIL_API_KEY=your_api_key
ZEPTOMAIL_FROM_EMAIL=noreply@unisync.com
BREVO_API_KEY=your_brevo_key

# AWS S3
AWS_BUCKET_NAME=unisync-media
AWS_REGION=us-east-1

# Redis
REDIS_URL=redis://localhost:6379/0

# Social Auth
SOCIAL_AUTH_GOOGLE_OAUTH2_KEY=your_key
SOCIAL_AUTH_GOOGLE_OAUTH2_SECRET=your_secret
SOCIAL_AUTH_GITHUB_KEY=your_key
SOCIAL_AUTH_GITHUB_SECRET=your_secret
```

---

## 📝 COMMON TASKS & WHERE TO FIND CODE

### Task: Add a new model
**Location**: `models.py`  
**Steps**:
1. Define class inheriting from `models.Model`
2. Add fields
3. Add `__str__` method
4. Run `python manage.py makemigrations`
5. Run `python manage.py migrate`

### Task: Create a new view
**Location**: `views.py`  
**Steps**:
1. Define function or class-based view
2. Add to `urls.py`
3. Create template in `templates/`
4. Link from other templates using {% url %}

### Task: Add REST API endpoint
**Location**: `chat_api.py` or `comment_api.py`  
**Steps**:
1. Create DRF serializer
2. Create view class (ListCreateView, DetailView, etc.)
3. Add to `urls.py`
4. Test with curl/Postman

### Task: Send email
**Location**: `zepto_mail_backend.py`  
**Code**:
```python
from django.core.mail import send_mail
send_mail(
    'Subject',
    'Message body',
    'from@email.com',
    ['to@email.com'],
    html_message='<p>HTML body</p>'
)
```

### Task: Query database
**Location**: Any view file  
**Examples**:
```python
# Get all projects by user
projects = Project.objects.filter(user=request.user)

# Get single project
project = Project.objects.get(id=project_id)

# Count likes
like_count = Like.objects.filter(project=project).count()

# Get recent comments
comments = Comment.objects.filter(project=project).order_by('-created_at')[:10]
```

### Task: Cache data
**Location**: In any view  
**Code**:
```python
from django.core.cache import cache
# Set cache
cache.set('key', value, 300)  # 5 min
# Get cache
data = cache.get('key')
```

### Task: Create notification
**Location**: `views.py`  
**Code**:
```python
create_notification(
    user=recipient,
    notification_type='connection_request',
    title='New connection request',
    message='From user',
    from_user=sender
)
```

---

## 🧪 TESTING QUICK GUIDE

### Run Tests
```bash
# All tests
pytest

# Specific test file
pytest accounts/tests.py

# Specific test class
pytest accounts/tests.py::TestLoginView

# Specific test method
pytest accounts/tests.py::TestLoginView::test_valid_login

# With coverage
pytest --cov=accounts
```

### Test Files Available
- `test_login.py` - Authentication tests
- `test_profile_view.py` - Profile tests
- `test_connections.py` - Connection tests
- `test_email.py` - Email tests
- `test_filter.py` - Filtering tests

---

## 🚀 DEPLOYMENT QUICK GUIDE

### Local Development
```bash
# Setup
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt

# Migrations
python manage.py migrate

# Create user
python manage.py createsuperuser

# Run server
python manage.py runserver
```

### Production (Render)
```bash
# Just push to main branch
git push origin main
# Render auto-deploys via Procfile
```

### Environment Setup
1. Copy `.env.template` to `.env`
2. Fill in all variables
3. Set same variables in Render/Railway dashboard

---

## 📊 DATABASE SCHEMA RELATIONSHIPS

```
User (Django built-in)
├── StudentProfile (1:1)
├── sent_connections (1:Many) → Connection
├── received_connections (1:Many) → Connection
├── projects (1:Many) → Project
├── sent_messages (1:Many) → Message
├── received_messages (1:Many) → Message
├── chat_memberships (1:Many) → ChatRoomMember
├── likes (1:Many) → Like
├── comments (1:Many) → Comment
├── activities (1:Many) → Activity
├── followers (1:Many) → Follow (reverse)
└── following (1:Many) → Follow

Project
├── user → User
├── members (1:Many) → ProjectMember
├── invitations (1:Many) → ProjectInvitation
├── likes (1:Many) → Like
├── comments (1:Many) → Comment
├── tasks (1:Many) → ProjectTask
└── milestones (1:Many) → ProjectMilestone

Message
├── sender → User
├── receiver → User (optional)
├── chat_room → ChatRoom (optional)
├── reply_to → Message (optional, self-ref)
├── files (1:Many) → MessageFile
├── reactions (1:Many) → MessageReaction
└── read_statuses (1:Many) → MessageReadStatus
```

---

## 🔐 SECURITY CHECKLIST

✅ CSRF Protection enabled  
✅ Password hashing (PBKDF2)  
✅ SQL injection prevention (ORM)  
✅ XSS protection (template auto-escaping)  
✅ Email verification (OTP)  
✅ Role-based access control  
✅ HTTPS ready  
✅ Secure cookies  
✅ Environment variable secrets  
✅ Permission decorators  

---

## 📞 GETTING HELP

### For questions about:
- **Models**: Check `models.py` line comments
- **Views**: Check `views.py` docstrings
- **URLs**: Check `urls.py` for route mapping
- **APIs**: Check `chat_api_improved.py` or `comment_api.py`
- **Settings**: Check `settings.py` with line numbers
- **Email**: Check `zepto_mail_backend.py`

### Common Issues & Solutions

| Issue | Check |
|-------|-------|
| Import error | Ensure app in `INSTALLED_APPS` |
| Template not found | Check `TEMPLATES` config in settings |
| Email not sending | Check email backend in settings |
| Database error | Run migrations |
| Static files 404 | Run `collectstatic` |
| WebSocket not working | Check `CHANNEL_LAYERS` config |

---

## 📌 IMPORTANT FILE SIZES

| File | Lines | Type |
|------|-------|------|
| views.py | 3311+ | Main logic |
| models.py | 718 | Database |
| urls.py | 129 | Routing |
| settings.py | 356+ | Config |
| chat_api_improved.py | 400+ | API |
| comment_api.py | 243+ | API |
| requirements.txt | 84 | Dependencies |

---

**Last Updated**: Feb 2026  
**Project**: UniSync (Collaborative Learning Platform)  
**Status**: Production Ready ✅
