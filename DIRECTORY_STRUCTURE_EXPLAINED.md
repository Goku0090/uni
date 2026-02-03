# UniSync Directory Structure & File Guide

---

## Root Directory (`/auth_project`)

```
auth_project/
├── auth_project/                 # Django project configuration
├── accounts/                     # Main application
├── static/                       # Static assets
├── staticfiles/                  # Collected static files (production)
├── media/                        # User uploads
├── logs/                         # Application logs
├── templates/                    # Global templates (optional)
├── db.sqlite3                    # Local SQLite database
├── manage.py                     # Django CLI tool
├── requirements.txt              # Python dependencies
├── Procfile                      # Heroku deployment
├── railway.json                  # Railway deployment config
├── render.yaml                   # Render deployment config
└── .env / .env.template         # Environment variables
```

---

## Core Django Configuration: `auth_project/`

### **settings.py** (356 lines)
The heart of Django configuration.

**Key Sections:**
1. **Base Setup** (lines 1-27)
   - DEBUG mode configuration
   - SECRET_KEY with environment fallback
   - BASE_DIR and DATA_DIR setup

2. **Database Config** (lines 99-138)
   - PostgreSQL for production (DATABASE_URL)
   - SQLite fallback for development
   - dj-database-url integration

3. **Installed Apps** (lines 35-61)
   - Django core: admin, auth, sessions, messages
   - Custom: accounts app
   - Third-party: allauth (Google, GitHub OAuth)
   - REST Framework

4. **Middleware** (lines 63-73)
   - Security, sessions, CSRF protection
   - Authentication, messages
   - Allauth integration

5. **Email Backend** (lines 214-257)
   - Brevo (primary)
   - ZeptoMail (alternative)
   - Gmail SMTP (fallback)
   - Console (development)

6. **Allauth & OAuth** (lines 180-194, 272-291)
   - Google OAuth configuration
   - GitHub OAuth configuration
   - Auto-signup settings

7. **REST Framework** (lines 195-212)
   - Default permissions: AllowAny
   - Pagination: 10 items per page
   - Search filters enabled
   - Session authentication

8. **Logging** (lines 297-355)
   - Console and file handlers
   - Rotating file handler (10MB files)
   - Separate error.log
   - DEBUG and INFO level logging

### **urls.py** (60 lines)
Main URL router.

**Structure:**
```python
# Admin
path('admin/', admin.site.urls)

# Custom accounts URLs
path('accounts/', include('accounts.urls'))

# Allauth URLs (OAuth, email verification)
path('accounts/', include('allauth.urls'))

# API routes
path('api/', include('accounts.urls'))

# View-based routes
path('login/', views.login_view, name='login')
path('dashboard/', views.dashboard_view, name='dashboard')
... (20+ routes)

# Media file serving (DEBUG=True)
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, ...)
```

### **wsgi.py**
WSGI application for production deployment.
- Gunicorn uses this for serving
- No modifications usually needed

### **asgi.py**
ASGI application for WebSockets/async.
- For real-time features (optional)
- Channels integration ready

---

## Main Application: `accounts/`

### **models.py** (718 lines)
Complete data model definitions.

**Model Groups:**

1. **User & Profile** (15-53)
   - StudentProfile: Extended user data
   - Includes: skills, interests, college, profile_photo

2. **Authentication** (55-124)
   - OTP: One-time passwords
   - 6-digit codes, 5-minute expiry
   - Multiple purposes: login, registration, reset

3. **Social Features** (126-473)
   - Connection: Friend requests
   - Follow: Follower system
   - Notification: Activity notifications
   - Activity: User activity feed

4. **Projects** (250+)
   - Project: Main project model
   - ProjectMember: Team members with roles
   - ProjectInvitation: Invite to join
   - ProjectTask: Tasks in projects
   - ProjectMilestone: Project milestones

5. **Messaging** (149-310)
   - ChatRoom: Group/direct chats
   - Message: Individual messages
   - MessageReadStatus: Read receipts (optimized)
   - MessageReaction: Emoji reactions
   - MessageFile: File attachments
   - File: File uploads storage

6. **Content** (350-390)
   - Comment: Comments on projects
   - Like: Project likes

7. **Statistics** (510-540)
   - UserStats: Dashboard statistics
   - UserStatus: Online status

### **views.py** (3000+ lines)
Primary view handlers.

**View Categories:**

**Authentication Views** (~300 lines)
- `register_view()` - User signup
- `login_view()` - User login
- `logout_view()` - Logout
- `verify_otp_view()` - OTP verification
- `forgot_password_view()` - Reset request
- `reset_password_view()` - Password reset
- `resend_otp_view()` - OTP resend

**Project Views** (~600 lines)
- `post_project()` - Create project
- `project_detail()` - View project
- `edit_project()` - Edit project
- `delete_project()` - Delete project
- `my_projects_view()` - User's projects
- `explore_projects_view()` - Browse projects
- `like_project()` - Like/unlike
- `search_projects()` - Search functionality

**Profile Views** (~300 lines)
- `student_profile()` - View profile
- `user_profile()` - Another user's profile
- `edit_profile()` - Edit own profile
- `dashboard_view()` - Main dashboard
- `find_collaborators()` - Collaborator search

**Messaging Views** (~400 lines)
- `message_view()` - Conversation list
- `chat_view()` - Direct chat
- `enhanced_messages_view()` - Advanced UI
- `enhanced_chat_view()` - Group chat
- `create_group_chat()` - New group
- `add_reaction()` - Add emoji reaction
- `start_call()` - Video/voice call

**Social Views** (~300 lines)
- `send_connection_request()` - Send request
- `accept_connection()` - Accept request
- `reject_connection()` - Reject request
- `my_connections()` - View connections
- `follow_user()` - Follow user
- `activity_feed()` - Activity timeline

**API Views** (~500 lines)
- `UserProfileView` - Profile REST API
- `ChatRoomListCreateView` - Chat management
- `MessageListCreateView` - Message CRUD
- `college_search_api()` - College search
- `user_stats_api()` - Stats endpoint

### **urls.py** (129 lines)
App-specific URL routing.

**Route Groups:**

**Authentication** (lines 22-29)
```
/login/, /register/, /logout/
/forgot-password/, /reset-password/
/verify-otp/<purpose>/
```

**Profiles** (lines 31-34)
```
/profile/, /student-profile/
/user/<username>/
```

**Projects** (lines 36-43)
```
/post-project/, /edit-project/<id>/
/delete-project/<id>/, /project-detail/<id>/
/like-project/<id>/
```

**Messaging** (lines 64-99)
```
/messages/, /chat/<user_id>/
/chat-rooms/, /messages/
/messages/<id>/reactions/
/drafts/, /typing/
```

**Comments** (lines 124-128)
```
/api/projects/<id>/comments/
/api/projects/<id>/comments/add/
/api/comments/<id>/delete/
```

### **serializers.py** (106 lines)
REST API serialization.

**Serializers:**
- `UserProfileSerializer` - User profile data
- `ProjectSerializer` - Project with counts
- `MessageSerializer` - Messages with reactions
- `ConnectionSerializer` - Connection requests
- `NotificationSerializer` - Notifications

### **forms.py** (609 lines)
Django form definitions.

**Forms:**
- `RegisterForm` - Registration with validation
- `LoginForm` - Login form
- `StudentProfileForm` - Profile information
- `ProjectForm` - Project creation
- `OTPVerificationForm` - OTP input
- `CommentForm` - Comment submission

**Features:**
- Custom validation methods
- Bootstrap CSS classes
- Error messages
- Field help text

### **utils.py** (479 lines)
Utility functions and helpers.

**Classes:**
1. **StudentProfileNLP** (35-479)
   - `preprocess_text()` - Clean text
   - `extract_skills()` - Find tech skills
   - `analyze_interests()` - Categorize interests
   - `extract_keywords()` - TF-IDF keywords
   - `find_similar_profiles()` - Recommendations
   - `match_with_projects()` - Project matching

   **Data:**
   - TECH_SKILLS: 50+ languages/frameworks
   - INTEREST_CATEGORIES: 8 major categories

2. **ProjectVisibilityFilter**
   - Filter projects by visibility rules
   - Owner, public, private, draft logic

### **email_backends/**

**brevo_mail_backend.py**
- Brevo API integration
- Primary email provider
- High deliverability for OTP/transactional

**zepto_mail_backend.py**
- ZeptoMail API integration
- Alternative provider
- Similar functionality to Brevo

### **permissions.py**
REST API permission classes.

**Permissions:**
- IsOwnerOrReadOnly - Can modify own objects
- IsAuthenticated - Requires login
- IsAdminOrReadOnly - Admin or read-only

### **chat_api.py** (300+ lines)
REST API for messaging.

**Views (CBV):**
- ChatRoomListCreateView - Create/list rooms
- ChatRoomDetailView - Retrieve room
- MessageListCreateView - Create/list messages
- MessageSearchView - Search messages
- ConversationListView - List conversations
- TypingIndicatorView - Typing status
- MessageReactionView - Add reactions

### **comment_api.py**
REST API for comments.

**Functions:**
- `add_comment()` - Create comment
- `get_comments()` - Retrieve comments
- `edit_comment()` - Update comment
- `delete_comment()` - Remove comment

### **views_contact.py**
Utility views.

**Views:**
- `privacy_policy_view()` - Privacy policy page
- `terms_of_service_view()` - Terms page
- `contact_us_view()` - Contact form page
- `contact_submit()` - Process contact form

### **tests.py**
Unit tests.

**Tests:**
- Authentication tests
- Profile CRUD tests
- Project visibility tests
- Message tests
- Connection tests

---

## Static Files: `static/`

### **js/** (JavaScript)
```
js/
├── login.js              # Login page interactions
├── api-utils.js          # API helper functions
├── profile.js            # Profile page functions
├── register_validation.js # Form validation
├── password_validation.js # Password strength check
└── college_autocomplete.js# College search autocomplete
```

### **css/** (Stylesheets)
```
css/
├── bootstrap.css         # Bootstrap framework
├── custom.css            # Custom styles
├── navbar.css            # Navigation styling
├── project_card.css      # Project card design
├── messages.css          # Chat interface
└── responsive.css        # Mobile responsive
```

### **images/** (Assets)
```
images/
├── logo.png              # UniSync logo
├── favicon.ico           # Browser tab icon
├── default-avatar.png    # Default profile picture
└── icons/                # UI icons
```

---

## Templates: `accounts/templates/`

### **Authentication Templates**
```
register.html              # Registration page
login.html                # Login page
verify_otp.html           # OTP verification
forgot_password.html      # Password reset request
reset_password.html       # Password reset form
```

### **Profile Templates**
```
profile.html              # User profile page
student_profile.html      # Student profile view
edit_profile.html         # Edit profile form
find_collaborators.html   # Find collaborators
find_collaborators_new.html
```

### **Project Templates**
```
project_detail.html       # Project details with comments
project_feed.html         # Browse projects feed
post_project.html         # Create project form
edit_project.html         # Edit project form
my_projects.html          # User's own projects
search_projects.html      # Search results
```

### **Messaging Templates**
```
messages.html             # Conversations list
chat.html                 # Direct message chat
enhanced_messages.html    # Advanced messaging UI
enhanced_chat.html        # Group chat interface
```

### **Utility Templates**
```
base.html                 # Base template with navbar
home.html                 # Homepage
dashboard.html            # Main dashboard
activity_feed.html        # Activity feed
notifications.html        # Notifications page
help_center.html          # Help/FAQ
premium.html              # Premium features page
terms_of_service.html     # Terms page
privacy_policy.html       # Privacy policy page
api_root.html             # API documentation
```

---

## Media Files: `media/`

```
media/
├── profile_photos/       # User profile pictures
│   ├── photo_1.jpg
│   ├── photo_2.jpg
│   └── ...
├── project_images/       # Project cover images
├── chat_files/           # Uploaded chat files
│   ├── document.pdf
│   ├── image.png
│   └── ...
└── uploads/              # Other user uploads
```

**Usage:**
- Profile photo: `profile.profile_photo.url`
- File download: `/download-file/<file_id>/`
- Storage: Local filesystem (configurable to S3)

---

## Logs: `logs/`

```
logs/
├── django.log            # All Django logs (rotated)
├── django.log.1          # Backup 1
├── django.log.2          # Backup 2
├── error.log             # Error logs only
└── error.log.1
```

**Log Levels:**
- INFO: General information
- DEBUG: Detailed debugging
- WARNING: Warning messages
- ERROR: Errors and exceptions

**Rotation:**
- Max 10MB per file
- Keep 5 backups
- Automatic rotation

---

## Database Schema

### **SQLite (Development)**
- File: `db.sqlite3`
- Location: Project root
- Single file database

### **PostgreSQL (Production)**
- Via `DATABASE_URL` environment variable
- On Render or Railway
- Automatic via dj-database-url

### **Tables:**
20+ tables from models:
- `auth_user` - Django User model
- `accounts_studentprofile` - Student profiles
- `accounts_project` - Projects
- `accounts_message` - Messages
- `accounts_comment` - Comments
- `accounts_otp` - OTP codes
- ... and more

---

## Configuration Files

### **.env / .env.template**
Environment variables template.

**Keys:**
- `DEBUG` - Development mode
- `SECRET_KEY` - Django secret
- `DATABASE_URL` - Database connection
- `BREVO_API_KEY` - Email provider
- `GOOGLE_CLIENT_ID` - OAuth
- `ALLOWED_HOSTS` - Domain whitelist

### **Procfile** (Heroku)
```
web: gunicorn auth_project.wsgi
```

### **railway.json** (Railway)
Railway-specific deployment config.

### **render.yaml** (Render)
Render-specific deployment config with:
- Services definition
- Build command
- Start command
- Environment variables

### **requirements.txt** (84 lines)
Python dependencies:
- Django 4.2.8
- DRF 3.14.0
- Channels 4.0.0
- Pandas, NLTK for NLP
- Celery for tasks
- And 50+ more packages

---

## Dependencies Management

### **Core Django Stack**
```
Django==4.2.8
djangorestframework==3.14.0
django-allauth==0.61.1
psycopg2-binary==2.9.9
```

### **Real-time & WebSockets**
```
channels==4.0.0
channels-redis==4.1.0
```

### **Email & Communications**
```
zeptomail==1.0.0
```

### **NLP & Data Processing**
```
nltk==3.8.1
pandas==2.1.4
openpyxl==3.1.2
textblob (implicit)
scikit-learn (implicit)
spacy (implicit)
```

### **File Storage**
```
Pillow==10.1.0
boto3==1.34.34
django-storages==1.14.2
```

### **Performance & Caching**
```
redis==5.0.1
django-redis==5.4.0
```

### **Production Server**
```
gunicorn==21.2.0
whitenoise==6.6.0
```

### **Development Tools**
```
django-debug-toolbar==4.2.0
black==23.12.1
flake8==6.1.0
pytest==7.4.3
pytest-django==4.7.0
```

---

## Key File Relationships

```
settings.py
  ↓ imports
urls.py
  ↓ includes
accounts/urls.py
  ↓ includes
accounts/views.py
  ↓ uses
accounts/models.py + forms.py
  ↓ rendered by
accounts/templates/*.html
  ↓ styled by
static/css/*.css
  ↓ enhanced by
static/js/*.js
  ↓ store files in
media/
```

---

## File Access Patterns

### **User Authentication Flow**
1. `register.html` → `forms.RegisterForm` → `register_view()` → `models.User/StudentProfile`

### **Project Creation Flow**
1. `post_project.html` → `forms.ProjectForm` → `post_project()` → `models.Project/ProjectMember`

### **Message Sending Flow**
1. `chat.html` → `chat_api.py:MessageListCreateView` → `models.Message`

### **Comment on Project Flow**
1. `project_detail.html` → `comment_api.py:add_comment()` → `models.Comment`

---

## Development Workflow

### **Making Changes**
1. Edit `.py` files (models, views, etc.)
2. Edit `.html` templates
3. Restart server: `python manage.py runserver`
4. Check logs: `tail logs/django.log`

### **Database Changes**
1. Modify `models.py`
2. `python manage.py makemigrations`
3. `python manage.py migrate`

### **Adding Dependencies**
1. Install: `pip install package_name`
2. Add to `requirements.txt`
3. Update production deployment

---

**End of Directory Structure Guide**
