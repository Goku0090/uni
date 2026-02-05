# UniSync: Complete Codebase Analysis

## Project Overview
**UniSync** is a Django-based student collaboration platform that enables users to connect, manage projects, and communicate seamlessly.

---

## 🏗️ Architecture Overview

### Technology Stack
- **Backend**: Django 4.x + Django REST Framework
- **Frontend**: HTML5, Tailwind CSS, JavaScript/HTMX
- **Database**: PostgreSQL (production) / SQLite (development)
- **Authentication**: Django Auth + Django-Allauth (Google, GitHub OAuth)
- **Email**: Brevo/ZeptoMail/Gmail SMTP
- **File Storage**: Local Media + Render PostgreSQL

---

## 📁 Directory Structure

```
auth_project/
├── accounts/                          # Main Django app
│   ├── models.py                     # Data models
│   ├── views.py                      # Main views (dashboards, projects, etc.)
│   ├── views_contact.py              # Contact/static pages
│   ├── comment_api.py                # Project comments API
│   ├── chat_api.py / chat_api_improved.py  # Messaging system
│   ├── forms.py                      # Django forms
│   ├── serializers.py                # DRF serializers
│   ├── permissions.py                # Custom permissions
│   ├── urls.py                       # URL routing
│   ├── utils.py                      # Utility functions
│   ├── brevo_mail_backend.py         # Email backend (Brevo)
│   ├── zepto_mail_backend.py         # Email backend (ZeptoMail)
│   ├── templatetags/                 # Custom template filters
│   ├── static/                       # CSS, JS, images
│   ├── templates/                    # HTML templates
│   │   ├── features/                 # Feature-specific templates
│   │   │   ├── messages.html         # Message system UI
│   │   │   ├── chat.html             # Chat interface
│   │   │   └── notifications.html    # Notifications
│   │   ├── dashboard.html            # Main dashboard
│   │   ├── profile.html              # User profile
│   │   ├── project_detail.html       # Project view
│   │   ├── find_collaborators.html   # Collaborator finder
│   │   ├── register.html             # Registration page
│   │   ├── verify_otp.html           # OTP verification
│   │   └── components/               # Reusable components
│   └── migrations/                   # Database migrations
│
├── auth_project/                      # Project settings
│   ├── settings.py                   # Django configuration
│   ├── urls.py                       # Root URL config
│   └── wsgi.py                       # WSGI application
│
└── manage.py                          # Django management
```

---

## 🗄️ Database Models

### 1. **StudentProfile**
User extended profile with academic and social information.

```
- user (OneToOne → User)
- full_name, college, location
- profile_photo (ImageField)
- bio, interests, skills, project_interests
- Social links (github, linkedin, portfolio, behance)
- Timestamps (created_at, updated_at)
```

### 2. **OTP**
One-time password system for secure authentication.

```
- email, otp_code (6-digit)
- purpose (login, registration, reset)
- is_used, expires_at
- Methods: is_valid(), verify_otp(), generate_otp()
```

### 3. **Connection**
User-to-user relationship networking.

```
- from_user (ForeignKey → User)
- to_user (ForeignKey → User)
- status (pending, accepted, blocked)
- created_at, updated_at
```

### 4. **Message**
Direct user-to-user messages.

```
- sender, receiver (ForeignKey → User)
- content, is_read
- created_at, attachment (optional)
- Linked to ChatRoom for group messaging
```

### 5. **ChatRoom**
Group messaging/collaboration spaces.

```
- name, description, icon
- created_by (ForeignKey → User)
- members (ManyToMany → ChatRoomMember)
- project (ForeignKey → Project, optional)
```

### 6. **Project**
Collaborative project management.

```
- title, description, overview
- created_by (ForeignKey → User)
- members (ManyToMany → ProjectMember)
- skills_required, members_count, timeline
- status, visibility (public/private)
- created_at, updated_at
```

### 7. **ProjectComment**
Comments on projects (social features).

```
- project (ForeignKey)
- user (ForeignKey → User)
- content, comment_count (likes)
- created_at, updated_at
```

### 8. **MessageReadStatus**
Tracks read receipts for messages.

```
- message (ForeignKey → Message)
- user (ForeignKey → User)
- read_at
```

### 9. **File** & **MessageFile**
File attachment system for messages.

```
- file (FileField), uploaded_by
- message (linked to Message)
```

---

## 🔑 Key Views & Endpoints

### Authentication & User Management
| Endpoint | Method | Purpose |
|----------|--------|---------|
| `/register/` | GET/POST | User registration with OTP |
| `/verify-otp/` | GET/POST | OTP verification |
| `/login/` | GET/POST | User login |
| `/logout/` | GET | User logout |
| `/reset-password/` | GET/POST | Password reset |
| `/accounts/google/login/` | GET | Google OAuth |
| `/accounts/github/login/` | GET | GitHub OAuth |

### Dashboard & Profiles
| Endpoint | Method | Purpose |
|----------|--------|---------|
| `/dashboard/` | GET | Main dashboard |
| `/profile/<username>/` | GET | View user profile |
| `/profile/edit/` | GET/POST | Edit own profile |
| `/my-profile/` | GET | View own profile |
| `/find-collaborators/` | GET | Find collaborators |
| `/api/users/search/` | GET | User search API |

### Projects
| Endpoint | Method | Purpose |
|----------|--------|---------|
| `/post-project/` | GET/POST | Create new project |
| `/project/<id>/` | GET | View project detail |
| `/project/<id>/edit/` | GET/POST | Edit project |
| `/project/<id>/delete/` | POST | Delete project |
| `/api/projects/` | GET | List projects with filtering |
| `/api/projects/feed/` | GET | Project feed (home) |
| `/project/<id>/join/` | POST | Join project |
| `/project/<id>/leave/` | POST | Leave project |

### Messaging & Chat
| Endpoint | Method | Purpose |
|----------|--------|---------|
| `/messages/` | GET | Messages list |
| `/chat/<user_id>/` | GET | Direct message with user |
| `/api/messages/` | GET | Get messages API |
| `/api/messages/send/` | POST | Send message |
| `/api/chat-rooms/` | GET/POST | Chat room management |
| `/api/chat-rooms/<id>/messages/` | GET | Get chat room messages |
| `/api/chat-rooms/<id>/send/` | POST | Send to chat room |
| `/api/messages/<id>/read/` | PATCH | Mark message as read |

### Comments & Social
| Endpoint | Method | Purpose |
|----------|--------|---------|
| `/api/projects/<id>/comments/` | GET/POST | Project comments |
| `/api/comments/<id>/` | GET/PATCH/DELETE | Comment management |
| `/api/comments/<id>/like/` | POST | Like comment |

### Notifications
| Endpoint | Method | Purpose |
|----------|--------|---------|
| `/notifications/` | GET | View notifications |
| `/api/notifications/` | GET | Notifications API |
| `/api/notifications/<id>/read/` | PATCH | Mark notification read |

---

## 🎨 Frontend Components

### Templates Structure

**Main Pages:**
- `dashboard.html` - Home feed with projects, connections
- `profile.html` - User profile with bio, skills, projects
- `project_detail.html` - Project info, members, comments
- `find_collaborators.html` - Search & filter users
- `register.html` - Registration & OTP flow
- `verify_otp.html` - OTP entry form

**Feature Templates:**
- `features/messages.html` - Direct messaging interface
- `features/chat.html` - Group chat/ChatRoom interface
- `features/notifications.html` - Notification center
- `features/messages_improved.html` - Enhanced messaging UI

**Components:**
- `components/footer.html` - Site footer
- `components/header.html` - Navigation bar
- Various partial templates for cards, lists

---

## 🔐 Authentication System

### Multi-Method Authentication
1. **Email + OTP** - Primary method
   - User enters email → OTP sent via Brevo/ZeptoMail
   - OTP expires in 10 minutes
   - Verified via `/verify-otp/`

2. **OAuth Social Login**
   - Google OAuth via django-allauth
   - GitHub OAuth via django-allauth
   - Auto-signup with custom form

3. **Traditional Username/Password**
   - Django built-in auth
   - Password reset via email

### Email Backends (Priority)
1. **Brevo** (Production) - Best for transactional email
2. **ZeptoMail** (Alternative) - High reliability
3. **Gmail SMTP** (Fallback) - Slower, rate-limited
4. **Console** (Development) - For testing

---

## 🔄 Core Features

### 1. Project Management
- **Create/Edit/Delete Projects**
- **Member Management** - Add members, assign roles
- **Visibility Control** - Public/Private projects
- **Skill Matching** - Find collaborators by skills
- **Project Comments** - Social engagement
- **Project Filtering** - By skills, status, timeline

### 2. Messaging & Chat
- **Direct Messaging** - One-to-one conversations
- **Group Chat** - ChatRoom-based messaging
- **Read Receipts** - Message read status
- **File Attachments** - Share files in messages
- **Message Reactions** - Emoji reactions
- **Live Updates** - Via JavaScript polling/WebSocket ready

### 3. User Networking
- **Connection System** - Follow/connect users
- **Profile Completion** - Comprehensive user profiles
- **Skill Showcase** - Display skills, projects, interests
- **Portfolio Links** - GitHub, LinkedIn, Behance

### 4. Notifications
- **Real-time Alerts** - Project invites, messages, comments
- **Notification Center** - View all notifications
- **Unread Badge** - Count unread notifications/messages

### 5. Search & Discovery
- **Project Search** - Full-text search by title, skills
- **User Search** - Find collaborators by interests
- **Advanced Filters** - By college, skills, availability

---

## 🚀 API Endpoints (REST Framework)

### REST Framework Configuration
- **Pagination**: 10 items per page, max 100
- **Authentication**: Session-based
- **Permissions**: AllowAny (custom checks in views)
- **Search**: Full-text search on name, email, bio
- **Ordering**: By created_at, activity

### Key API Endpoints
```
GET  /api/users/search/              - Search users
GET  /api/projects/                  - List projects
GET  /api/projects/feed/             - Home project feed
POST /api/projects/                  - Create project
GET  /api/projects/<id>/             - Project detail
GET  /api/projects/<id>/comments/    - Project comments
POST /api/projects/<id>/comments/    - Add comment
GET  /api/messages/                  - Get messages
POST /api/messages/send/             - Send message
GET  /api/chat-rooms/                - List chat rooms
POST /api/chat-rooms/                - Create chat room
GET  /api/notifications/             - Get notifications
PATCH /api/notifications/<id>/read/  - Mark read
```

---

## 📊 Key Business Logic

### Project Visibility Filtering
```
PUBLIC:  Visible to all authenticated users
PRIVATE: Only visible to project members
```

### Member Management
- **Owner**: Full control (edit, delete, add members)
- **Member**: Can view, comment, collaborate
- **Pending**: Invitation sent, awaiting acceptance

### Unread Message Tracking
- Uses `MessageReadStatus` model
- Badge count from unread messages
- Mark read on message view

### Search Features
- Search across user profiles (name, email, bio, skills)
- Search projects (title, description, skills)
- Filter by college, location, interests

---

## 🛠️ Utility Functions

### models.py
- `StudentProfile.get_display_name()` - Get display name
- `OTP.is_valid()` - Check OTP validity
- `OTP.verify_otp()` - Verify OTP code
- `OTP.generate_otp()` - Create new OTP

### views.py
- `dashboard_view()` - Main home feed
- `project_detail_view()` - Project info
- `find_collaborators()` - Collaborator search
- `post_project()` - Create project
- `register_view()` - User registration
- `verify_otp_view()` - OTP verification
- `chat_view()` - Messaging interface

### utils.py
- Helper functions for email, file handling
- Template tag registrations
- Common utilities

---

## ⚙️ Settings & Configuration

### Key Settings
- **DEBUG**: Enabled in development
- **ALLOWED_HOSTS**: localhost, 127.0.0.1, and production domain
- **SECRET_KEY**: Auto-generated in dev, must be set in production
- **DATABASE**: PostgreSQL (production), SQLite (dev)
- **EMAIL_BACKEND**: Brevo > ZeptoMail > Gmail > Console
- **STATIC_FILES**: Collected to `/staticfiles/`
- **MEDIA_ROOT**: `/media/` for uploads

### Environment Variables Required
```
# Database
DATABASE_URL (Render PostgreSQL)
DB_NAME, DB_USER, DB_PASSWORD, DB_HOST, DB_PORT

# Email
BREVO_API_KEY  (or)
ZEPTO_MAIL_API_KEY, ZEPTO_MAIL_TOKEN  (or)
EMAIL_HOST_USER, EMAIL_HOST_PASSWORD

# OAuth
GOOGLE_CLIENT_ID, GOOGLE_CLIENT_SECRET
GITHUB_CLIENT_ID, GITHUB_CLIENT_SECRET

# API
RAPIDAPI_KEY, RAPIDAPI_HOST

# Security
SECRET_KEY, DEBUG, ALLOWED_HOSTS
```

---

## 🧪 Testing Files

Test files for various features:
- `test_login.py` - Authentication testing
- `test_email.py` - Email backend testing
- `test_comments_api.py` - Comments API
- `test_connections.py` - Connection system
- `test_profile_view.py` - Profile views
- `test_feed_fix.py` - Dashboard feed

---

## 🔍 Important Code Patterns

### Form Submission (CSRF Protection)
```html
{% csrf_token %}
<form method="post">
  <!-- form fields -->
</form>
```

### API Error Handling
```python
try:
    # API logic
except Exception as e:
    return JsonResponse({'error': str(e)}, status=400)
```

### Template Context Passing
```python
def view(request):
    context = {
        'projects': projects,
        'user': request.user,
        'messages_count': messages.count()
    }
    return render(request, 'template.html', context)
```

### Model Filtering
```python
projects = Project.objects.filter(
    visibility='public',
    created_by=user
).order_by('-created_at')
```

---

## 📈 Performance Optimizations

### Database
- **Select_related**: For foreign key queries
- **Prefetch_related**: For reverse relations
- **Pagination**: Limit 10-100 items per page
- **Indexing**: On frequently searched fields

### Template
- **Caching**: Static assets versioning
- **Lazy Loading**: Images, heavy components
- **Minification**: CSS/JS in production

### Queries
- Avoid N+1 queries
- Use `.only()`, `.defer()` for field selection
- Use `.exists()` instead of `.count()` for existence checks

---

## 🚨 Known Fixes & Workarounds

### CSRF Token
- Disabled for API endpoints in some views
- Re-enabled for form security
- Use `@csrf_exempt` carefully for APIs

### Project Detail Loading
- Optimized with select_related/prefetch_related
- Cache project comments count
- Avoid nested loops in templates

### Message Read Status
- Mark messages as read on view
- Track via MessageReadStatus model
- Badge updates via AJAX

### Email Configuration
- Multiple backends with fallback logic
- Test with console backend first
- Use Brevo for production reliability

---

## 🔗 Component Dependencies

```
Views ─→ Models ─→ Database
  ↓
Templates ←─ Context Data
  ↓
Static Files (CSS, JS)

APIs ─→ Serializers ─→ Models

Auth ─→ User/StudentProfile ─→ Allauth
```

---

## 📝 File Navigation Guide

| Purpose | File |
|---------|------|
| Add new model | `accounts/models.py` |
| Add new view | `accounts/views.py` |
| Add new template | `accounts/templates/` |
| Configure app | `auth_project/settings.py` |
| Add URL route | `accounts/urls.py` |
| Create form | `accounts/forms.py` |
| Add API serializer | `accounts/serializers.py` |
| Static assets | `accounts/static/` |

---

## 🎯 Common Development Tasks

### Add New Feature
1. Create model in `models.py`
2. Run migrations: `python manage.py makemigrations && migrate`
3. Create view in `views.py`
4. Add URL in `urls.py`
5. Create template in `templates/`
6. Test with console/email backend

### Debug Issues
1. Check logs in `/logs/` directory
2. Use Django debug toolbar
3. Print debug info in console
4. Test with `manage.py shell`

### Deploy to Production (Render)
1. Set environment variables on Render
2. Ensure DATABASE_URL is set
3. Run `python manage.py collectstatic`
4. Push to GitHub (auto-deploys if connected)

---

## 📚 Documentation Files Created

Extensive documentation exists in the root directory covering:
- Fix summaries and implementation guides
- Feature delivery summaries
- Deployment instructions
- API endpoint references
- Testing guides
- Quick reference cards

---

## Summary

UniSync is a **fully-featured student collaboration platform** with:
- ✅ Multi-auth system (OTP, OAuth, password)
- ✅ Project management with member handling
- ✅ Real-time messaging and chat
- ✅ Social features (comments, connections, notifications)
- ✅ Advanced search and filtering
- ✅ Production-ready (PostgreSQL, Render-compatible)
- ✅ Responsive frontend with Tailwind CSS

All code is well-structured, documented, and production-ready for deployment.
