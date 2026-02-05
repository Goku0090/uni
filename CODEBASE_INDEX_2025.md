# UniSync Codebase - Complete Index

**Your guide to navigating the entire codebase**

---

## 📚 Documentation Files (Read These First)

| Document | Purpose | Read When |
|----------|---------|-----------|
| **QUICK_START_GUIDE_2025.md** | 5-minute introduction for new developers | You're new to the project |
| **COMPREHENSIVE_CODEBASE_ANALYSIS_2025.md** | Complete architecture and feature breakdown | You need to understand the whole system |
| **API_ENDPOINTS_REFERENCE_2025.md** | All API endpoints with examples | You're building frontend or integrating APIs |
| **TECHNICAL_STACK_GUIDE_2025.md** | Dependencies, setup, and deployment | You need to set up the environment |
| **CODEBASE_INDEX_2025.md** | This file - navigation guide | You're looking for specific files |

---

## 🗂️ Project Structure

### Root Directory
```
/login/
├── auth_project/           ← Main Django project
├── unisync-/               ← Alternative project folder
├── venv/                   ← Virtual environment
├── .git/                   ← Git repository
├── .gitignore              ← Git ignore rules
├── .env.template           ← Environment template
├── requirements.txt        ← Python dependencies
├── Procfile                ← Deployment (Heroku/Render)
├── render.yaml             ← Render deployment config
├── railway.json            ← Railway deployment config
└── [Many documentation files from previous work]
```

---

## 🎯 Core Application Files

### Django Configuration (`auth_project/auth_project/`)

| File | Purpose | Key Content |
|------|---------|-------------|
| **settings.py** | Main Django configuration | Database, email, apps, middleware, security |
| **urls.py** | Project URL routing | Maps all URLs to views |
| **wsgi.py** | WSGI application | For production servers (Gunicorn) |
| **asgi.py** | ASGI application | For WebSocket support (Channels) |

### Main Application (`auth_project/accounts/`)

#### Core Model Files
| File | Purpose | Models |
|------|---------|--------|
| **models.py** | Database models | User, StudentProfile, Project, Message, Comment, etc. (16+ models) |
| **serializers.py** | REST API serializers | Converts models to/from JSON |
| **forms.py** | HTML form definitions | Login, Register, Profile, Project forms |
| **permissions.py** | Custom permissions | Check user access rights |
| **utils.py** | Utility functions | Helper functions used across app |

#### View/API Files
| File | Purpose | Key Functions/Classes |
|------|---------|-----------|
| **views.py** | Main view logic | 50+ functions for pages and APIs |
| **views_contact.py** | Contact/legal pages | Privacy, terms, contact forms |
| **comment_api.py** | Comment operations | add_comment, get_comments, edit_comment, delete_comment |
| **chat_api.py** | Messaging API | ChatRoomListCreateView, MessageListCreateView, etc. |
| **chat_api_improved.py** | Enhanced messaging | Improved chat implementation |

#### Email/Backend Files
| File | Purpose | Provides |
|------|---------|----------|
| **brevo_mail_backend.py** | Brevo email integration | Email sending via Brevo API |
| **zepto_mail_backend.py** | ZeptoMail integration | Email sending via ZeptoMail API |

#### Other Files
| File | Purpose |
|------|---------|
| **urls.py** | App URL routing (all endpoints) |
| **tests.py** | Basic test cases |
| **templatetags/custom_filters.py** | Custom Django template filters |
| **admin.py** | Django admin configuration |

---

## 📁 Templates Directory (`auth_project/accounts/templates/`)

### Authentication Templates
```
login.html                 ← Login page
register.html             ← Registration page
forgot_password.html      ← Password recovery
reset_password.html       ← Password reset form
```

### Main Pages
```
base.html                 ← Base template (header, nav, footer)
dashboard.html            ← User dashboard
main.html                 ← Home page
home_api.html             ← API home
```

### Project Management
```
find_collaborators.html           ← Find collaborators page
find_collaborators_new.html       ← Improved version
project_detail.html               ← View project details
edit_project.html                 ← Edit project form
project_feed.html                 ← Projects feed
explore_project.html              ← Explore projects
search_projects.html              ← Search projects
```

### Messaging
```
messages.html             ← Messages list
chat.html                 ← Chat interface
enhanced-messages.html    ← Improved messaging
chat_improved.html        ← Enhanced chat
create_group_chat.html    ← Create group chat
```

### Social Features
```
investor_dashboard.html   ← Investor dashboard
notifications.html        ← Notifications page
activity_feed.html        ← Activity feed
user_profile.html         ← User profile view
```

### Footer/Legal
```
contact_us.html           ← Contact form
privacy.html              ← Privacy policy
terms_of_service.html     ← Terms of service
```

---

## 🎨 Static Files (`auth_project/static/` and `accounts/static/`)

### JavaScript
```
js/
├── login.js              ← Login form validation
├── profile.js            ← Profile page interactions
├── api-utils.js          ← Shared API functions
├── password_validation.js ← Password validation
├── register_validation.js ← Registration validation
├── college_autocomplete.js ← College search autocomplete
└── [many more from DRF and admin]
```

### CSS
```
css/
├── styles.css            ← Custom styles
└── [Bootstrap, DRF styles]
```

---

## 🧪 Test Files (`auth_project/`)

| File | Tests |
|------|-------|
| test_login.py | Login functionality |
| test_profile_fix.py | Profile operations |
| test_profile_upload.py | Photo upload |
| test_filter.py | Project filtering |
| test_feed_fix.py | Feed display |
| test_otp.py | OTP verification |
| test_email.py | Email sending |
| test_search.py | Search functionality |
| test_connections.py | User connections |
| test_services.py | Service integrations |

---

## 📊 Database Models Quick Reference

### User & Profile Models
- **User** (Django) - Built-in user model (username, password, email)
- **StudentProfile** - Extended profile (college, skills, interests, photo)

### Project Models
- **Project** - Project metadata (title, description, visibility, status)
- **ProjectMember** - Team members with roles (owner, admin, contributor, viewer)
- **ProjectTask** - Tasks within projects (status, priority, assignment)
- **ProjectMilestone** - Project milestones (due date, completion tracking)
- **ProjectInvitation** - Invitations to join projects

### Messaging Models
- **Message** - Individual messages (text, files, calls, threading)
- **ChatRoom** - Group conversations and direct messages
- **MessageReadStatus** - Track read receipts per user
- **MessageFile** - File attachments
- **MessageReaction** - Emoji/text reactions
- **File** - File storage and metadata

### Social Models
- **Connection** - Connection requests (pending → accepted/rejected)
- **Follow** - Follow relationships for activity tracking
- **Like** - Likes on projects
- **Activity** - User activity log
- **Notification** - User notifications
- **UserStats** - Statistics tracking

### Other Models
- **Comment** - Project comments with threading
- **OTP** - One-time passwords for authentication

---

## 🔌 API Endpoint Categories

### Authentication APIs
```
POST   /login/
POST   /register/
POST   /logout/
POST   /verify-otp/<purpose>/
POST   /resend-otp/<purpose>/
POST   /forgot-password/
POST   /reset-password/
```

### User Profile APIs
```
GET    /api/user-profile/<user_id>/
POST   /accounts/student-details/
GET    /accounts/user/<username>/
GET    /api/user-stats/
```

### Project APIs
```
GET    /accounts/dashboard/
POST   /accounts/post-project/
GET    /accounts/project-detail/<id>/
POST   /accounts/edit-project/<id>/
DELETE /accounts/delete-project/<id>/
POST   /accounts/like-project/<id>/
GET    /accounts/find-collaborators/
```

### Comment APIs
```
GET    /api/projects/<id>/comments/
POST   /api/projects/<id>/comments/add/
POST   /api/comments/<id>/edit/
DELETE /api/comments/<id>/delete/
```

### Messaging APIs
```
POST   /api/chat-rooms/
GET    /api/chat-rooms/
GET    /api/messages/
POST   /api/direct-message/
GET    /api/conversations/
POST   /api/messages/<id>/reactions/
```

### Social APIs
```
POST   /accounts/send-connection/<user_id>/
POST   /accounts/accept-connection/<id>/
POST   /accounts/follow/<user_id>/
GET    /accounts/activity-feed/
GET    /accounts/notifications/
```

---

## 🔑 Key Functions in views.py

| Function | Purpose |
|----------|---------|
| **login_view()** | Handle login with email/username and password |
| **register_view()** | User registration with email and OTP |
| **verify_otp_view()** | Verify OTP code for login/registration/reset |
| **dashboard_view()** | Main dashboard after login |
| **post_project()** | Create new project |
| **project_detail()** | View project with team, tasks, comments |
| **edit_project()** | Update project information |
| **delete_project()** | Remove project |
| **find_collaborators()** | Search for users to collaborate with |
| **user_profile()** | View other user's profile |
| **message_view()** | Messaging interface |
| **chat_view()** | Direct chat interface |
| **connect_view()** | Send connection request |
| **activity_feed()** | View user activity timeline |
| **notifications_view()** | View user notifications |

---

## ⚙️ Configuration Sections in settings.py

| Section | Purpose | Key Variables |
|---------|---------|---|
| **Security** | Authentication and CSRF | SECRET_KEY, ALLOWED_HOSTS, DEBUG |
| **Installed Apps** | Enabled apps | INSTALLED_APPS list |
| **Middleware** | Request processing | MIDDLEWARE list |
| **Templates** | Template engine | TEMPLATES configuration |
| **Database** | Database config | DATABASE_URL, DATABASES |
| **Email** | Email backends | EMAIL_BACKEND, BREVO_API_KEY |
| **REST Framework** | DRF settings | REST_FRAMEWORK dict |
| **Allauth** | Social auth | SOCIALACCOUNT_PROVIDERS |
| **Static/Media Files** | File handling | STATIC_URL, MEDIA_ROOT |
| **Logging** | Log configuration | LOGGING dict |

---

## 📦 Dependencies Overview

### Web Framework
- Django 4.2.8
- Django REST Framework 3.14.0
- Channels 4.0.0 (WebSockets)

### Database
- PostgreSQL (psycopg2-binary)
- SQLite (built-in)

### Authentication
- django-allauth 0.61.1 (Google, GitHub OAuth)

### Email
- Custom Brevo backend
- Custom ZeptoMail backend
- Gmail SMTP fallback

### Real-time
- Channels 4.0.0
- Redis 5.0.1

### Processing
- Pillow (Image processing)
- Pandas (Data handling)
- NLTK (NLP)

### Deployment
- Gunicorn (WSGI server)
- WhiteNoise (Static files)

### Development
- Django Debug Toolbar
- Pytest + pytest-django

---

## 🚀 How Features Work

### Feature: User Authentication
**Files:** views.py, models.py (OTP), settings.py, templates  
**Flow:** Register → OTP sent → Verify → Account created → Login

### Feature: Project Management  
**Files:** views.py, models.py (Project), templates  
**Flow:** Create → Add members → Create tasks → Add milestones → Comment

### Feature: Messaging
**Files:** chat_api.py, models.py (Message), templates  
**Flow:** Create room → Add members → Send message → Read receipt

### Feature: Comments
**Files:** comment_api.py, models.py (Comment), templates  
**Flow:** Add comment → Can reply → Edit/Delete → Live update

### Feature: Notifications
**Files:** views.py, models.py (Notification), templates  
**Flow:** User action → Activity logged → Followers notified

---

## 🔍 Finding What You Need

### I want to modify...

| What | Where to Look |
|------|---|
| Login page | templates/login.html, views.py (login_view) |
| User profile | templates/find_collaborators.html, models.py (StudentProfile) |
| Projects list | templates/project_feed.html, views.py (project_feed) |
| Comments | comment_api.py, templates/project_detail.html |
| Messages | chat_api.py, templates/chat.html |
| Email sending | brevo_mail_backend.py, settings.py |
| Database schema | models.py |
| API endpoints | urls.py (all routes), comment_api.py, chat_api.py |
| Form validation | forms.py |
| Styling | static/css/, templates/base.html |
| Admin panel | admin.py |

---

## 🐛 Common File Edits

### Add a new view
**File:** accounts/views.py  
**Add:** New function or class

### Add a new model
**File:** accounts/models.py  
**Add:** New Model class  
**Then:** Run makemigrations, migrate

### Add a new URL
**File:** accounts/urls.py  
**Add:** path() entry

### Add a new template
**File:** accounts/templates/mytemplate.html  
**Create:** New HTML file

### Add a new API endpoint
**File:** accounts/urls.py + views.py (or separate file)  
**Add:** API view class + URL pattern

---

## 📈 Code Statistics

| Metric | Value |
|--------|-------|
| Models | 16+ |
| Views/API Functions | 50+ |
| URL Patterns | 100+ |
| Templates | 30+ |
| Test Files | 15+ |
| Python dependencies | 40+ |

---

## 🔐 Security Checklist

- [ ] SECRET_KEY configured
- [ ] DEBUG = False for production
- [ ] ALLOWED_HOSTS set correctly
- [ ] HTTPS enforced
- [ ] CSRF protection enabled
- [ ] Password validators configured
- [ ] Email backend secured
- [ ] Database credentials in .env
- [ ] API permissions set
- [ ] File uploads validated

---

## 📚 Learning Path

1. **Week 1:** Read QUICK_START_GUIDE, run the app locally
2. **Week 2:** Read COMPREHENSIVE_CODEBASE_ANALYSIS, explore models.py and views.py
3. **Week 3:** Read API_ENDPOINTS_REFERENCE, test various endpoints
4. **Week 4:** Make a small feature (new page or API endpoint)
5. **Week 5+:** Deep dive into specific areas as needed

---

## 🎓 Resources for Each Topic

### Django
- Official docs: https://docs.djangoproject.com/
- Database models: https://docs.djangoproject.com/en/stable/topics/db/models/
- Views: https://docs.djangoproject.com/en/stable/topics/http/views/
- Forms: https://docs.djangoproject.com/en/stable/topics/forms/

### REST Framework
- Official docs: https://www.django-rest-framework.org/
- Serializers: https://www.django-rest-framework.org/api-guide/serializers/
- Views: https://www.django-rest-framework.org/api-guide/views/

### Real-time
- Channels: https://channels.readthedocs.io/
- WebSockets: https://en.wikipedia.org/wiki/WebSocket

### Deployment
- Render: https://render.com/docs/
- Railway: https://docs.railway.app/

---

## 💡 Quick Tips

1. **Always use virtual environment:** `source venv/bin/activate`
2. **Run migrations after model changes:** `python manage.py migrate`
3. **Use Django shell to test:** `python manage.py shell`
4. **Check logs:** `tail -f logs/django.log`
5. **Format code:** `black accounts/`
6. **Type check:** `mypy accounts/`
7. **Run tests:** `pytest accounts/`
8. **Check security:** `python manage.py check --deploy`

---

## 📞 Getting Help

1. **Check the documentation files** - They contain most answers
2. **Read the code comments** - Functions are documented
3. **Look at similar code** - Find working examples
4. **Test in Django shell** - Verify functionality
5. **Check error logs** - They usually tell you what's wrong
6. **Search GitHub issues** - Common problems are documented

---

*Last Updated: February 3, 2025*

**Next Step:** Open QUICK_START_GUIDE_2025.md to get started!
