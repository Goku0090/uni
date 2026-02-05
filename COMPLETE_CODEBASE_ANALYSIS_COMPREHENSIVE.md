# Complete Codebase Analysis - UniSync Platform

## Project Overview

**Project Name:** UniSync (Student Collaboration Platform)
**Framework:** Django 4.x with Django REST Framework
**Frontend:** HTML5, CSS, JavaScript (Vanilla + AJAX)
**Database:** PostgreSQL (Production) / SQLite (Development)
**Authentication:** Django Allauth with OAuth2 (Google, GitHub) + Email OTP
**Email Service:** Brevo / ZeptoMail / Gmail SMTP

---

## 1. ARCHITECTURE OVERVIEW

### Technology Stack

```
┌─────────────────────────────────────────────────────────┐
│                    FRONTEND LAYER                        │
│  HTML Templates │ JavaScript │ CSS │ Static Assets      │
└────────────────────────┬────────────────────────────────┘
                         │ HTTP Requests
┌─────────────────────────▼────────────────────────────────┐
│                 DJANGO BACKEND LAYER                      │
│  URLs → Views → Models → Database                        │
│                                                           │
│  Services:                                               │
│  • Authentication (Allauth, OTP)                         │
│  • REST APIs (Messaging, Comments, Projects)            │
│  • Email Service (OTP, Notifications)                   │
│  • File Management (Profile Photos, Uploads)            │
└─────────────────────────┬────────────────────────────────┘
                         │ Database Queries
┌─────────────────────────▼────────────────────────────────┐
│                   DATA LAYER                              │
│  PostgreSQL / SQLite + Media Storage                     │
└─────────────────────────────────────────────────────────┘
```

### Project Structure

```
auth_project/
├── auth_project/                    # Django project settings
│   ├── settings.py                 # Configuration (DB, Email, Auth)
│   ├── urls.py                     # Main URL router
│   ├── wsgi.py                     # WSGI application
│   └── asgi.py                     # ASGI application
│
├── accounts/                        # Main application
│   ├── models.py                   # Data models
│   ├── views.py                    # View functions
│   ├── urls.py                     # URL routing
│   ├── serializers.py              # REST serializers
│   ├── forms.py                    # Django forms
│   ├── permissions.py              # Custom permissions
│   ├── utils.py                    # Utility functions
│   │
│   ├── chat_api.py                 # Messaging REST API
│   ├── comment_api.py              # Comments REST API
│   ├── views_contact.py            # Contact page views
│   │
│   ├── services/
│   │   └── auth_service.py         # Authentication service
│   │
│   ├── templatetags/
│   │   └── custom_filters.py       # Custom Jinja filters
│   │
│   ├── static/                     # Static files
│   │   └── js/
│   │       ├── login.js            # Login form validation
│   │       ├── api-utils.js        # API helper functions
│   │       └── ...
│   │
│   ├── templates/                  # HTML templates
│   │   ├── base.html               # Base template
│   │   ├── find_collaborators_enhanced.html
│   │   ├── project_detail.html
│   │   ├── messages.html
│   │   ├── login.html
│   │   ├── register.html
│   │   └── ...
│   │
│   ├── migrations/                 # Database migrations
│   │
│   ├── brevo_mail_backend.py       # Brevo email backend
│   ├── zepto_mail_backend.py       # ZeptoMail backend
│   └── tests.py
│
├── media/                          # User uploads (profile photos, etc)
├── static/                         # Static assets
├── staticfiles/                    # Collected static files
├── logs/                           # Application logs
│
├── manage.py                       # Django CLI
├── requirements.txt                # Python dependencies
└── .env                            # Environment variables
```

---

## 2. DATABASE SCHEMA & MODELS

### Core Models

#### User Authentication
- **User (Django Built-in)**
  - username, email, password
  - first_name, last_name
  - is_active, is_staff
  - date_joined, last_login

#### StudentProfile
```python
- user (OneToOne → User)
- full_name, college, other_college, location
- bio, profile_photo
- interests (JSONField)
- skills (JSONField)
- project_interests (JSONField)
- role_preference
- social_links (github, linkedin, portfolio, behance)
- profile_completed (Boolean)
- created_at, updated_at
```

#### Project Management
```python
Project:
- user (ForeignKey → User) [Creator]
- title, description, image
- link (external URL)
- visibility (private/public)
- status (active/completed)
- created_at, updated_at
- likes_count (count), comments_count (count)

ProjectMember:
- project (ForeignKey → Project)
- user (ForeignKey → User)
- role (owner, admin, contributor, viewer)
- is_active (Boolean)
- joined_at

ProjectTask:
- project (ForeignKey → Project)
- title, description
- assigned_to (ForeignKey → User)
- status (todo, in_progress, review, completed, cancelled)
- priority (low, medium, high, urgent)
- due_date, completed_at

ProjectMilestone:
- project (ForeignKey → Project)
- title, description
- due_date, is_completed
```

#### Social Features
```python
Connection:
- sender (ForeignKey → User)
- receiver (ForeignKey → User)
- status (pending, accepted, rejected)
- unique_together: [sender, receiver]

Follow:
- follower (ForeignKey → User)
- following (ForeignKey → User)
- unique_together: [follower, following]

Like:
- user (ForeignKey → User)
- project (ForeignKey → Project)

Comment:
- user (ForeignKey → User)
- project (ForeignKey → Project)
- content (TextField)
- created_at, updated_at

Notification:
- recipient (ForeignKey → User)
- sender (ForeignKey → User, nullable)
- notification_type (connection_request, project_comment, etc)
- is_read (Boolean)
```

#### Messaging
```python
Message:
- sender (ForeignKey → User)
- receiver (ForeignKey → User, nullable)
- chat_room (ForeignKey → ChatRoom, nullable)
- content (TextField)
- message_type (text, file, image, call)
- reply_to (ForeignKey → Message, nullable)
- created_at, updated_at

ChatRoom:
- name, description
- chat_type (direct, group)
- created_by (ForeignKey → User)
- created_at, updated_at

ChatRoomMember:
- chat_room (ForeignKey → ChatRoom)
- user (ForeignKey → User)
- is_active (Boolean)
- joined_at

MessageReadStatus:
- message (ForeignKey → Message)
- user (ForeignKey → User)
- read_at (DateTime)
- unique_together: [message, user]

MessageReaction:
- message (ForeignKey → Message)
- user (ForeignKey → User)
- reaction (emoji/text)
- unique_together: [message, user, reaction]
```

#### Authentication
```python
OTP:
- email (EmailField)
- otp_code (CharField, 6 digits)
- purpose (login, registration, reset)
- is_used (Boolean)
- created_at, expires_at (5 minutes)

UserStats:
- user (OneToOne → User)
- projects_created, connections_made
- likes_received, comments_made
- followers_count, following_count
- last_updated
```

---

## 3. AUTHENTICATION FLOW

### Login Flow (Email + OTP)

```
User enters email on login page
         ↓
Check if email exists in User model
         ↓
Generate OTP (6 digits, 5 min expiry)
         ↓
Send OTP via email (Brevo/ZeptoMail)
         ↓
User receives OTP in inbox
         ↓
User enters OTP on verify page
         ↓
Backend validates OTP (not expired, matches)
         ↓
Create session + redirect to dashboard
```

**Key Files:**
- `views.py:login_view()` - Email input
- `views.py:verify_otp_view()` - OTP verification
- `models.OTP.generate_otp()` - OTP generation
- `views.py:send_otp_email()` - Email sending
- `brevo_mail_backend.py` / `zepto_mail_backend.py` - Email backends

### Social Login (Google OAuth)

```
User clicks "Login with Google"
         ↓
Redirect to Google OAuth consent screen
         ↓
User authorizes + Google returns access token
         ↓
Allauth processes token → Create/update User
         ↓
Apply CustomSocialSignupForm (add email, college, etc)
         ↓
Create StudentProfile + redirect to dashboard
```

**Key Files:**
- `settings.py` - Allauth configuration & Google/GitHub providers
- `forms.py:CustomSocialSignupForm` - Custom social signup
- Django-allauth handles OAuth flow

---

## 4. CORE FEATURES & VIEWS

### A. Authentication & Profile

| Feature | URL | View | Template | Purpose |
|---------|-----|------|----------|---------|
| Register | `/register/` | `register_view()` | `register.html` | New user signup |
| Login | `/login/` | `login_view()` | `login.html` | Email/OTP login |
| Verify OTP | `/verify-otp/<purpose>/` | `verify_otp_view()` | `verify_otp.html` | Confirm OTP |
| Student Profile | `/student-profile/` | `student_profile()` | `profile.html` | Edit profile |
| User Profile API | `/profile/` | `UserProfileView` (REST) | JSON | Get user data |
| View Profile | `/user/<username>/` | `user_profile()` | `profile.html` | View other users |

**Models Used:** User, StudentProfile, OTP

### B. Projects Management

| Feature | URL | View | Template | Purpose |
|---------|-----|------|----------|---------|
| Post Project | `/post-project/` | `post_project()` | `post_project.html` | Create new project |
| Project Detail | `/project-detail/<id>/` | `project_detail()` | `project_detail.html` | View project + comments |
| Edit Project | `/edit-project/<id>/` | `edit_project()` | `post_project.html` | Modify project |
| Delete Project | `/delete-project/<id>/` | `delete_project()` | - | Remove project |
| My Projects | `/my-projects/` | `my_projects_view()` | `my_projects.html` | User's projects |
| Explore Projects | `/explore-projects/` | `explore_projects_view()` | `explore_project.html` | Browse all projects |
| Like Project | `/like-project/<id>/` | `like_project()` | - | Add/remove like |

**Models Used:** Project, Like, ProjectMember, ProjectTask, ProjectMilestone, Comment

### C. Collaboration Features

| Feature | URL | View | Purpose |
|---------|-----|------|---------|
| Find Collaborators | `/find-collaborators/` | `find_collaborators()` | Search & filter users |
| Connect User | `/connect/<user_id>/` | `send_connection_request()` | Send connection request |
| My Connections | `/my-connections/` | `my_connections()` | View accepted connections |
| Accept Connection | `/accept-connection/<id>/` | `accept_connection()` | Accept request |
| Reject Connection | `/reject-connection/<id>/` | `reject_connection()` | Decline request |
| Cancel Connection | `/cancel-connection/<id>/` | `cancel_connection_request()` | Cancel pending request |

**Models Used:** Connection, StudentProfile, Follow

### D. Messaging & Chat

| Feature | URL | View | Type | Purpose |
|---------|-----|------|------|---------|
| Messages | `/messages/` | `message_view()` | Template | Conversation list |
| Direct Chat | `/chat/<user_id>/` | `chat_view()` | Template | Direct message |
| Enhanced Messages | `/enhanced-messages/` | `enhanced_messages_view()` | Template | Group/thread chat |
| Chat Rooms (API) | `/chat-rooms/` | `ChatRoomListCreateView` | REST | CRUD chat rooms |
| Messages (API) | `/messages/` | `MessageListCreateView` | REST | Send/receive messages |
| Message Status | `/messages/<id>/status/` | `MessageStatusView` | REST | Read receipts |

**Models Used:** Message, ChatRoom, ChatRoomMember, MessageReadStatus, MessageReaction

### E. Comments System

| Feature | URL | Endpoint | Type | Purpose |
|---------|-----|----------|------|---------|
| Get Comments | `/projects/<id>/comments/` | `get_comments()` | REST GET | Fetch project comments |
| Add Comment | `/projects/<id>/comments/add/` | `add_comment()` | REST POST | Post new comment |
| Delete Comment | `/comments/<id>/delete/` | `delete_comment()` | REST DELETE | Remove comment |
| Edit Comment | `/comments/<id>/edit/` | `edit_comment()` | REST PUT | Update comment |

**Models Used:** Comment, Project, User

### F. Notifications & Activity

| Feature | URL | View | Purpose |
|---------|-----|------|---------|
| Notifications | `/notifications/` | `notifications_view()` | Display user notifications |
| Mark Read | `/mark-notification-read/<id>/` | `mark_notification_read()` | Set notification as read |
| Activity Feed | `/activity-feed/` | `activity_feed()` | User activity timeline |

**Models Used:** Notification, Activity

### G. Additional Pages

| Feature | URL | View | Purpose |
|---------|-----|------|---------|
| Dashboard | `/dashboard/` | `dashboard_view()` | User home/overview |
| Main/Home | `/` | `main()` | Landing page |
| Help Center | `/help/` | `help_center_view()` | FAQ/support |
| Contact | `/contact/` | `contact_us_view()` | Contact form |
| Privacy Policy | `/privacy/` | `privacy_policy_view()` | Legal |
| Terms of Service | `/terms/` | `terms_of_service_view()` | Legal |

---

## 5. API ENDPOINTS (REST Framework)

### Chat Rooms API
```
GET    /chat-rooms/                      List all chat rooms
POST   /chat-rooms/                      Create new chat room
GET    /chat-rooms/<id>/                 Get room details
PUT    /chat-rooms/<id>/                 Update room
DELETE /chat-rooms/<id>/                 Delete room
GET    /chat-rooms/<id>/members/         Get room members
```

### Messages API
```
GET    /messages/                        List messages
POST   /messages/                        Create/send message
GET    /messages/<id>/                   Get message details
PUT    /messages/<id>/                   Update message
DELETE /messages/<id>/                   Delete message
GET    /messages/<id>/status/            Get read status
POST   /messages/<id>/reactions/         Add reaction
GET    /messages/search/                 Search messages
```

### Comments API (Live Feed)
```
GET    /projects/<id>/comments/          Get all comments for project
POST   /projects/<id>/comments/add/      Add comment to project
PUT    /comments/<id>/edit/              Edit comment
DELETE /comments/<id>/delete/            Delete comment
```

### User APIs
```
GET    /user-stats/                      Get user statistics
GET    /user-profile/<id>/               Get user profile
POST   /check-username/                  Validate username availability
POST   /check-email/                     Validate email availability
```

### Project APIs
```
GET    /explore-projects/                List projects
POST   /post-project/                    Create project
GET    /project-detail/<id>/             Get project details
```

### Other APIs
```
GET    /college-search/                  Search colleges (RapidAPI)
POST   /validate-college/                Validate college name
POST   /nlp-analyze/                     NLP analysis endpoint
```

---

## 6. EMAIL CONFIGURATION

### Email Backends (Priority Order)

1. **Brevo** (Primary - Recommended)
   - Email backend: `brevo_mail_backend.BrevoMailBackend`
   - Env var: `BREVO_API_KEY`
   - Use case: Production OTP & transactional emails

2. **ZeptoMail** (Alternative)
   - Email backend: `zepto_mail_backend.ZeptoMailBackend`
   - Env vars: `ZEPTO_MAIL_API_KEY`, `ZEPTO_MAIL_TOKEN`
   - Use case: Fallback for Brevo

3. **Gmail SMTP** (Fallback)
   - Email backend: Django's SMTP
   - Env vars: `EMAIL_HOST_USER`, `EMAIL_HOST_PASSWORD`
   - Host: smtp.gmail.com:587 (TLS)

4. **Console** (Development)
   - Email backend: `django.core.mail.backends.console.EmailBackend`
   - Output: Prints emails to console
   - Use case: Local development

### Email Sending Flow

```
generate_otp(email, purpose)
         ↓
Generate 6-digit OTP + 5-min expiry
         ↓
Save OTP to database
         ↓
send_otp_email(email, otp_code, purpose)
         ↓
Select email backend (Brevo → ZeptoMail → Gmail → Console)
         ↓
Send email with OTP code
         ↓
Store in OTP table for verification
```

**Key Files:**
- `settings.py` - Email backend selection
- `brevo_mail_backend.py` - Brevo implementation
- `zepto_mail_backend.py` - ZeptoMail implementation
- `views.py:send_otp_email()` - Email sending logic

---

## 7. AUTHENTICATION BACKENDS

### Django Allauth Configuration

**Installed:**
- `allauth` - Main package
- `allauth.account` - Basic auth
- `allauth.socialaccount` - Social login
- `allauth.socialaccount.providers.google` - Google OAuth
- `allauth.socialaccount.providers.github` - GitHub OAuth

**Authentication Backends:**
```python
AUTHENTICATION_BACKENDS = (
    'django.contrib.auth.backends.ModelBackend',          # Standard Django auth
    'allauth.account.auth_backends.AuthenticationBackend', # Allauth auth
)
```

**Social Provider Configuration:**
```python
SOCIALACCOUNT_PROVIDERS = {
    'google': {
        'SCOPE': ['profile', 'email'],
        'AUTH_PARAMS': {'access_type': 'online'},
        'APP': {
            'client_id': os.getenv('GOOGLE_CLIENT_ID'),
            'secret': os.getenv('GOOGLE_CLIENT_SECRET'),
        }
    },
    'github': {
        'SCOPE': ['user:email', 'read:user'],
        'APP': {
            'client_id': os.getenv('GITHUB_CLIENT_ID'),
            'secret': os.getenv('GITHUB_CLIENT_SECRET'),
        }
    }
}
```

**Custom Signup Form:**
```python
SOCIALACCOUNT_FORMS = {
    'signup': 'accounts.forms.CustomSocialSignupForm',
}
```

---

## 8. SETTINGS & CONFIGURATION

### Security Settings

| Setting | Value | Purpose |
|---------|-------|---------|
| `DEBUG` | True (dev), False (prod) | Enable debug mode |
| `SECURE_SSL_REDIRECT` | False (dev), True (prod) | Force HTTPS |
| `SESSION_COOKIE_SECURE` | False (dev), True (prod) | HTTPS-only cookies |
| `CSRF_COOKIE_SECURE` | False (dev), True (prod) | HTTPS-only CSRF |
| `ALLOWED_HOSTS` | localhost,127.0.0.1 | Allowed domains |

### Database Configuration

**Production (Render):**
```python
DATABASE_URL = os.getenv('DATABASE_URL')  # Auto-set by Render
DATABASES = dj_database_url.parse(DATABASE_URL)
```

**Development:**
```python
PostgreSQL:
  DB_NAME: unisync_db
  DB_USER: unisync_user
  DB_PASSWORD: <password>
  DB_HOST: localhost
  DB_PORT: 5432

Fallback to SQLite (db.sqlite3)
```

### Installed Apps

```python
INSTALLED_APPS = [
    # Django core
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.sites',
    'django.contrib.humanize',
    
    # Custom
    'accounts',
    
    # Third-party
    'allauth',
    'allauth.account',
    'allauth.socialaccount',
    'allauth.socialaccount.providers.google',
    'allauth.socialaccount.providers.github',
    'rest_framework',
]
```

### Middleware Stack

```python
MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',       # Security headers
    'django.contrib.sessions.middleware.SessionMiddleware', # Sessions
    'django.middleware.common.CommonMiddleware',           # Common utilities
    'django.middleware.csrf.CsrfViewMiddleware',           # CSRF protection
    'django.contrib.auth.middleware.AuthenticationMiddleware', # Auth
    'django.contrib.messages.middleware.MessageMiddleware',  # Messages
    'django.middleware.clickjacking.XFrameOptionsMiddleware', # X-Frame-Options
    'allauth.account.middleware.AccountMiddleware',        # Allauth
]
```

### REST Framework Configuration

```python
REST_FRAMEWORK = {
    'DEFAULT_PERMISSION_CLASSES': ['rest_framework.permissions.AllowAny'],
    'DEFAULT_PAGINATION_CLASS': 'rest_framework.pagination.PageNumberPagination',
    'DEFAULT_FILTER_BACKENDS': [
        'rest_framework.filters.SearchFilter',
        'rest_framework.filters.OrderingFilter',
    ],
    'DEFAULT_AUTHENTICATION_CLASSES': [
        'rest_framework.authentication.SessionAuthentication',
    ],
    'PAGE_SIZE': 10,
    'MAX_PAGE_SIZE': 100,
    'SEARCH_PARAM': 'search',
    'ORDERING_PARAM': 'ordering',
}
```

---

## 9. KEY FUNCTIONS & UTILITIES

### Authentication Utils

```python
send_otp_email(email, otp_code, purpose)
  - Generate and send OTP to email
  - Uses configured email backend
  - Sets 5-minute expiry

verify_otp_view(request, purpose)
  - Validate OTP code
  - Check expiry + usage
  - Create session for user

get_otp_purpose_from_url(request)
  - Extract OTP purpose (login, register, reset)
```

### Profile Utils

```python
student_details_view(request)
  - Render student details form
  - POST: Save profile data

student_profile(request)
  - GET: Display profile edit page
  - POST: Update StudentProfile

user_profile(request, username)
  - View other user's public profile
  - Display projects, connections, stats
```

### Project Utils

```python
project_detail(request, project_id)
  - Display project with comments
  - GET: Show project + comments
  - POST: Add comment (JS handles)

post_project(request)
  - Create new project
  - GET: Show form
  - POST: Save project

like_project(request, project_id)
  - Toggle like on project
  - AJAX endpoint
```

### Collaboration Utils

```python
find_collaborators(request)
  - Display enhanced collaborator search
  - Filters: college, interests, skills, role
  - AJAX-based filtering

send_connection_request(request, user_id)
  - Create pending connection
  - Send notification to target user

accept_connection(request, connection_id)
  - Change connection status to 'accepted'
  - Create Follow record

reject_connection(request, connection_id)
  - Change connection status to 'rejected'
```

### Messaging Utils

```python
message_view(request)
  - Display conversation list
  - GET: Load conversations

chat_view(request, user_id)
  - Open direct message chat
  - GET: Load messages
  - AJAX: Send new messages

enhanced_messages_view(request)
  - Group chat interface
  - ChatRoom support
```

### Comments API

```python
get_comments(request, project_id)
  - REST API: GET /projects/<id>/comments/
  - Return JSON list of comments

add_comment(request, project_id)
  - REST API: POST /projects/<id>/comments/add/
  - Create Comment + update count

delete_comment(request, comment_id)
  - REST API: DELETE /comments/<id>/delete/
  - Remove comment

edit_comment(request, comment_id)
  - REST API: PUT /comments/<id>/edit/
  - Update comment content
```

---

## 10. FRONTEND COMPONENTS

### HTML Templates Key Features

**find_collaborators_enhanced.html**
- Search box with filtering
- Collaborator cards with fade-in animation
- Filter sidebar (college, interests, skills, role)
- Connect button with CSRF token
- Responsive grid layout

**project_detail.html**
- Project header (title, image, description)
- Comments section (live feed)
- Comment form with AJAX submission
- Team members display
- Like button

**messages.html**
- Conversation list
- Message search
- Online status indicators
- Unread message badges
- Notification count

**profile.html**
- Profile info (bio, college, skills)
- Profile photo upload
- Social links (GitHub, LinkedIn, etc)
- Edit form with validation
- Project list

### JavaScript Utilities

**api-utils.js**
- `makeAPICall()` - Generic API request wrapper
- `getCSRFToken()` - Extract CSRF token from DOM
- `handleError()` - Standard error handling
- Handles JSON requests/responses

**login.js**
- Form validation
- Password strength indicator
- Email format check
- Real-time feedback

---

## 11. FILE & MEDIA MANAGEMENT

### Media Storage

**Profile Photos:**
```
media/profile_photos/<user_id>.jpg
```

**Project Images:**
```
media/project_images/<project_id>.jpg
```

**Chat Files:**
```
media/chat_files/<timestamp>_<filename>
```

**Settings:**
```python
MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')
```

### File Model

```python
class File(models.Model):
    user (FK → User)
    file (FileField)
    filename (str)
    file_size (int)
    file_type (str)
    uploaded_at (DateTime)
```

---

## 12. LOGGING CONFIGURATION

### Log Handlers

```python
console  - Stream to console
file     - Django.log (rotating 10MB)
error_file - Error.log (rotating 10MB)
```

### Log Levels

```
Django           - INFO (DEBUG in dev)
Accounts app     - DEBUG (DEBUG in dev)
```

### Log Location

```
logs/django.log     - All logs
logs/error.log      - Errors only
```

---

## 13. ENVIRONMENT VARIABLES

### Required Variables

```
DEBUG                      True/False
SECRET_KEY                 Random string (auto-generated in dev)
ALLOWED_HOSTS              localhost,127.0.0.1
DATABASE_URL               postgresql://user:pass@host/db (Render)
BREVO_API_KEY              Brevo account API key
ZEPTO_MAIL_API_KEY         ZeptoMail account key
ZEPTO_MAIL_TOKEN           ZeptoMail token
EMAIL_HOST_USER            Gmail address
EMAIL_HOST_PASSWORD        Gmail app password
GOOGLE_CLIENT_ID           Google OAuth client ID
GOOGLE_CLIENT_SECRET       Google OAuth secret
GITHUB_CLIENT_ID           GitHub OAuth client ID
GITHUB_CLIENT_SECRET       GitHub OAuth secret
DEFAULT_FROM_EMAIL         sender@unisync.app
RAPIDAPI_KEY               RapidAPI key (college search)
```

### Optional Development Variables

```
DB_NAME                    unisync_db (PostgreSQL)
DB_USER                    unisync_user
DB_PASSWORD                your_password
DB_HOST                    localhost
DB_PORT                    5432
SECURE_SSL_REDIRECT        False (dev), True (prod)
SESSION_COOKIE_SECURE      False (dev), True (prod)
CSRF_COOKIE_SECURE         False (dev), True (prod)
```

---

## 14. COMMON WORKFLOWS

### Workflow: New User Registration

1. User visits `/register/`
2. View renders registration form
3. User submits form with email, username, password
4. View validates form + checks duplicate email/username
5. Creates User + StudentProfile
6. Sends welcome email
7. Redirects to login or dashboard

**Files Involved:**
- `urls.py` - Route registration
- `views.py:register_view()`
- `forms.py` - Registration form
- `models.py` - User, StudentProfile
- `templates/register.html`

### Workflow: Email + OTP Login

1. User visits `/login/`
2. Enters email address
3. System generates OTP + sends email
4. User receives OTP in inbox
5. Enters OTP on `/verify-otp/login/`
6. OTP validated (not expired, correct code)
7. Session created, redirected to dashboard

**Files Involved:**
- `views.py:login_view()`, `verify_otp_view()`
- `models.py:OTP`
- `settings.py` - Email configuration
- `brevo_mail_backend.py` / `zepto_mail_backend.py`
- `templates/login.html`, `verify_otp.html`

### Workflow: Create & View Project

1. User navigates to `/post-project/`
2. Fills project form (title, description, image)
3. Submits POST request
4. View creates Project + ProjectMember (owner role)
5. Redirects to `/project-detail/<id>/`
6. Other users can view project + add comments
7. Comments displayed via AJAX

**Files Involved:**
- `models.py:Project`, `ProjectMember`, `Comment`
- `views.py:post_project()`, `project_detail()`
- `comment_api.py:add_comment()`, `get_comments()`
- `templates/post_project.html`, `project_detail.html`

### Workflow: Find & Connect Collaborators

1. User navigates to `/find-collaborators/`
2. System filters students by college, interests, skills
3. Displays collaborator cards with profiles
4. User clicks "Connect" button
5. Creates Connection (pending status)
6. Sends notification to target user
7. Target accepts → status changes to "accepted"
8. Both appear in `/my-connections/`

**Files Involved:**
- `models.py:Connection`, `StudentProfile`
- `views.py:find_collaborators()`, `send_connection_request()`, `accept_connection()`
- `templates/find_collaborators_enhanced.html`

### Workflow: Direct Messaging

1. User A clicks chat with User B
2. System finds/creates direct Message records
3. Displays message thread
4. User A types + sends message (AJAX)
5. View creates Message object
6. Marks read status when User B views
7. Notification sent to User B

**Files Involved:**
- `models.py:Message`, `ChatRoom`, `MessageReadStatus`
- `views.py:chat_view()`
- `chat_api.py:MessageListCreateView`, `MessageStatusView`
- `templates/chat.html`

---

## 15. POTENTIAL ISSUES & NOTES

### Known Areas

1. **CSRF Token Issues**
   - Ensure CSRF token in forms + AJAX headers
   - Check middleware order

2. **Database Migrations**
   - Always run `python manage.py migrate` after model changes
   - Check migration files in `accounts/migrations/`

3. **Email Delivery**
   - Verify email backend is configured correctly
   - Check .env variables (BREVO_API_KEY, etc)
   - Test with console backend first

4. **Static Files**
   - Run `python manage.py collectstatic` before deployment
   - Verify STATIC_URL and STATICFILES_DIRS

5. **Media Files**
   - Ensure media directory writable
   - Configure S3 for production uploads

6. **CORS Issues**
   - Not configured - same-origin only
   - May need django-cors-headers for cross-origin APIs

7. **Permissions**
   - REST APIs have `AllowAny` permission
   - Consider adding permission classes for sensitive endpoints

---

## 16. DEPLOYMENT NOTES

### Render Deployment

**Environment Variables:**
- Render auto-sets `DATABASE_URL`
- Must set SECRET_KEY, email vars, OAuth secrets
- Use PostgreSQL (recommended)

**Commands:**
```bash
Build: pip install -r requirements.txt
Run:   python manage.py migrate && gunicorn auth_project.wsgi
```

**Static Files:**
```bash
python manage.py collectstatic --noinput
```

### Local Development

```bash
# Create virtual environment
python -m venv venv
source venv/Scripts/activate  # Windows

# Install dependencies
pip install -r requirements.txt

# Setup .env
cp .env.template .env
# Edit .env with local settings

# Run migrations
python manage.py migrate

# Create superuser (optional)
python manage.py createsuperuser

# Start development server
python manage.py runserver
```

---

## 17. KEY TECHNICAL PATTERNS

### View Pattern (Function-Based Views)

```python
def view_name(request):
    if request.method == 'GET':
        # Handle GET
        context = {...}
        return render(request, 'template.html', context)
    
    elif request.method == 'POST':
        # Handle POST
        # Validate form
        # Create/update model
        # Redirect or render
        return redirect('next_page')
```

### REST API Pattern (Class-Based Views)

```python
class APIEndpointView(APIView):
    def get(self, request):
        # Fetch data
        serializer = MySerializer(data)
        return Response(serializer.data)
    
    def post(self, request):
        # Create data
        serializer = MySerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=201)
        return Response(serializer.errors, status=400)
```

### AJAX Pattern (JavaScript)

```javascript
// Get CSRF token
const token = document.querySelector('[name=csrfmiddlewaretoken]').value;

// Make POST request
fetch('/api/endpoint/', {
    method: 'POST',
    headers: {
        'Content-Type': 'application/json',
        'X-CSRFToken': token,
    },
    body: JSON.stringify(data)
})
.then(res => res.json())
.then(data => {
    console.log('Success:', data);
    // Update DOM
})
.catch(err => console.error('Error:', err));
```

---

## 18. MODEL RELATIONSHIPS DIAGRAM

```
User (Django Built-in)
├── StudentProfile (1:1)
├── Project (1:many) [Creator]
├── Connection (1:many) [sender/receiver]
├── Message (1:many) [sender]
├── Comment (1:many)
├── Like (1:many)
├── Follow (1:many) [follower/following]
├── Notification (1:many) [recipient]
├── ChatRoom (1:many) [creator]
├── ChatRoomMember (1:many)
├── MessageReadStatus (1:many)
├── ProjectMember (1:many)
├── ProjectTask (1:many) [assigned_to/assigned_by]
├── Activity (1:many)
└── UserStats (1:1)

Project (1:many)
├── Like (1:many)
├── Comment (1:many)
├── ProjectMember (1:many)
├── ProjectTask (1:many)
├── ProjectMilestone (1:many)
├── Activity (1:many)
└── ProjectInvitation (1:many)

Message (1:many)
├── ChatRoom (FK, nullable)
├── MessageFile (1:many)
├── MessageReaction (1:many)
├── MessageReadStatus (1:many)
└── Message (Self, nullable) [reply_to]

ChatRoom (1:many)
├── ChatRoomMember (1:many)
├── Message (1:many)
└── DraftMessage (1:many)
```

---

## 19. SUMMARY

This is a comprehensive Django-based student collaboration platform with:

- **Authentication**: Email OTP + Google/GitHub OAuth
- **Projects**: Creation, management, collaboration
- **Social**: Connections, followers, activity feed
- **Messaging**: Direct + group chats with read receipts
- **Comments**: Live commenting on projects
- **Profiles**: Student profiles with skills & interests
- **Notifications**: Connection requests, comments, messages
- **APIs**: REST endpoints for core features
- **Email**: Multi-backend support (Brevo, ZeptoMail, Gmail)
- **Database**: PostgreSQL (production) / SQLite (dev)

All code follows Django best practices with separation of concerns, proper ORM usage, REST API design, and comprehensive model relationships.

---

**Last Updated:** February 2026
**Total Models:** 25+
**Total Views:** 40+
**Total URL Patterns:** 80+
**Total Templates:** 30+
