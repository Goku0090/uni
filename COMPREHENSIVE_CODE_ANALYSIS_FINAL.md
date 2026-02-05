# UniSync - Comprehensive Code Analysis (Feb 2026)

## Project Overview

**UniSync** is a Django-based collaborative platform designed for university students to connect, collaborate on projects, and manage team interactions. The application features user authentication (OTP + Email), messaging, project management, comments, and social features.

**Tech Stack:**
- Backend: Django 4.x, Django REST Framework
- Frontend: HTML5, Tailwind CSS, JavaScript (Vanilla + Lucide Icons)
- Database: PostgreSQL (production), SQLite (development)
- Authentication: Email OTP, Google OAuth
- Email Service: Brevo (formerly Sendinblue), ZeptoMail backends
- Deployment: Render, Railway

---

## Directory Structure

```
auth_project/
├── accounts/                          # Main Django app
│   ├── models.py                      # 14 database models
│   ├── views.py                       # Core view logic (~3300+ lines)
│   ├── urls.py                        # URL routing
│   ├── forms.py                       # Django forms
│   ├── serializers.py                 # DRF serializers
│   ├── permissions.py                 # Custom permissions
│   ├── utils.py                       # Helper functions
│   ├── services/
│   │   └── auth_service.py           # Authentication logic
│   ├── comment_api.py                 # Comment endpoints
│   ├── chat_api.py                    # Messaging API
│   ├── chat_api_improved.py          # Enhanced chat API
│   ├── zepto_mail_backend.py         # ZeptoMail integration
│   ├── brevo_mail_backend.py         # Brevo integration
│   ├── migrations/                    # Database migrations
│   ├── templatetags/
│   │   └── custom_filters.py         # Custom template filters
│   └── templates/
│       ├── features/
│       │   ├── messages.html          # Messaging interface
│       │   ├── projects.html          # Project listing
│       │   ├── profile.html           # User profile
│       │   └── [other feature templates]
│       └── [other templates]
├── auth_project/                      # Django settings
│   ├── settings.py                    # Configuration
│   ├── urls.py                        # URL dispatcher
│   ├── asgi.py                        # ASGI config
│   └── wsgi.py                        # WSGI config
├── manage.py                          # Django CLI
├── requirements.txt                   # Dependencies
└── [test files and utilities]
```

---

## Database Models (14 Core Models)

### 1. **StudentProfile** (Extended User Profile)
```python
Relationship: OneToOne with User
Key Fields:
- full_name, college, location
- interests, skills, project_interests (JSON arrays)
- profile_photo (image upload)
- profile_completed (boolean flag)
- Social links: github, linkedin, portfolio, behance
Purpose: Extended user information beyond Django's User model
```

### 2. **OTP** (One-Time Password)
```python
Purpose: Email-based authentication
Key Features:
- 6-digit alphanumeric codes
- 5-minute expiry
- Purpose types: login, registration, password_reset
- Methods: generate_otp(), verify_otp(), hash_otp()
```

### 3. **Connection** (User Network)
```python
Represents: Friendship/Connection requests between users
Status: pending, accepted, rejected
Unique constraint: sender + receiver (no duplicate connections)
```

### 4. **Message** (Direct & Group Messages)
```python
Key Features:
- Supports direct messages (receiver) and group chats (chat_room)
- Message types: text, file, image, call
- Threading support (reply_to field)
- Read status tracking via MessageReadStatus model
Methods: mark_as_read_by(), is_read_by(), get_read_count()
```

### 5. **MessageReadStatus** (Message Read Tracking)
```python
Purpose: Scalable read status tracking for messages
Avoids: BooleanField on Message model for performance
Tracks: Which users read which messages and when
```

### 6. **MessageReaction** (Message Emojis)
```python
Purpose: Emoji reactions to messages
Unique constraint: message + user + reaction (one reaction per user per message)
```

### 7. **File** (Chat File Uploads)
```python
Stores: File uploads for chat messages
Fields: filename, file_size, file_type
Related: MessageFile (M2M relationship with Message)
```

### 8. **ChatRoom** (Group Chats)
```python
Types: direct, group, team_chat
Key Fields:
- name, description
- creator, created_at
- chat_type
- members (M2M via ChatRoomMember)
Methods: add_member(), remove_member(), get_active_members()
```

### 9. **ChatRoomMember** (Chat Membership)
```python
Tracks: User membership in chat rooms
Fields: user, chat_room, is_active, joined_at
Purpose: Manage who's in which conversation
```

### 10. **Notification** (User Notifications)
```python
Tracks:
- notification_type (message, connection_request, project_invitation, etc.)
- related_user, related_project
- read status
- created_at timestamp
```

### 11. **Comment** (Project Comments)
```python
Threaded: reply_to field for nested comments
Related: project, user
Fields: content, likes_count, created_at
Purpose: Collaborative feedback on projects
```

### 12. **Project** (User Projects)
```python
Key Fields:
- title, description, long_description
- owner, team_members (M2M via ProjectMember)
- status, visibility (public, private, draft)
- tags, tech_stack, budget, timeline
- logo, cover_image
Methods: is_owner(), can_edit()
```

### 13. **Like** (Project Likes)
```python
Relationships: user, project
Unique constraint: user + project (one like per user per project)
Purpose: Track project appreciation
```

### 14. **Follow** (User Following)
```python
Relationships: follower, following (both User)
Unique constraint: follower + following
Purpose: Social network following system
```

**Additional Models:**
- ProjectMember, ProjectInvitation, ProjectTask, ProjectMilestone
- UserStatus, Activity, UserStats

---

## Core Features & Architecture

### 1. **Authentication System**
```
Login Flow:
  1. User enters email
  2. Backend generates 6-digit OTP via Brevo/ZeptoMail
  3. User receives email and enters OTP
  4. OTP verified against database
  5. Session/JWT token created
  6. User redirected to dashboard

Key Files:
  - auth_service.py: Core auth logic
  - OTP model: OTP generation, verification, expiry
  - views.py: login_otp_send(), login_otp_verify(), register()
```

### 2. **Messaging System**
```
Architecture:
  - Direct Messages: Message model with receiver field
  - Group Chats: Message model with chat_room field
  - Read Status: MessageReadStatus model (one entry per reader)
  - Notifications: Real-time updates on new messages

API Endpoints (chat_api.py, chat_api_improved.py):
  GET/POST /api/messages/
  GET /api/messages/{id}/
  POST /api/messages/{id}/read/
  GET /api/chat-rooms/
  POST /api/chat-rooms/
  POST /api/chat-rooms/{id}/members/
```

### 3. **Project Management**
```
Features:
  - Create/Edit/Delete projects
  - Team collaboration (ProjectMember with roles)
  - Visibility control (public/private/draft)
  - Tasks and milestones
  - Comments and feedback
  - Likes/appreciation tracking

Roles:
  - Owner: Full control
  - Admin: Manage project (except delete)
  - Contributor: Can modify tasks/content
  - Viewer: Read-only access

Key Views:
  - project_list(): Display all projects with filtering
  - project_detail(): View single project with team/tasks
  - create_project(): Form submission for new projects
  - project_feed(): Personalized feed based on interests
```

### 4. **Comments & Feedback**
```
Features:
  - Nested comments (threaded replies)
  - Like counting on comments
  - Real-time updates
  - User mentions (@username)

API Endpoints (comment_api.py):
  GET /api/projects/{id}/comments/
  POST /api/projects/{id}/comments/
  PUT /api/comments/{id}/
  DELETE /api/comments/{id}/
  POST /api/comments/{id}/like/
```

### 5. **Activity Feed**
```
Tracked Activities:
  - profile_updated
  - project_created
  - project_liked
  - connection_made
  - message_sent
  - comment_added
  - user_followed
  - task_completed
  - milestone_completed

Purpose: Show user and network activity in real-time
```

### 6. **User Search & Discovery**
```
Search Types:
  1. Project Search: title, description, tags, tech_stack
  2. User Search: username, full_name, college, interests
  3. Message Search: by content, participants

Filtering:
  - By college, location, interests
  - By project status, visibility, tech_stack
  - By date range, popularity (likes)
```

### 7. **Social Features**
```
Connection System:
  - Send connection requests
  - Accept/Reject connections
  - View connections list
  - Message connections

Follow System:
  - Follow other users
  - See follower feed
  - Get notifications on followed user activities
```

### 8. **Email Integration**
```
Backends Configured:
  1. Brevo (Sendinblue) - Primary
  2. ZeptoMail - Fallback

Email Types:
  - OTP emails (login, registration, password reset)
  - Notification emails
  - Project invitations
  - Connection requests

Templates:
  - Custom HTML templates for branded emails
  - Dynamic content injection (user name, OTP code, etc.)
```

---

## Frontend Components

### 1. **Messages Page** (messages.html - 1294 lines)
```
Sections:
  - Header with search and new message button
  - Conversation list (scrollable sidebar)
  - Message thread view (center)
  - Message input area (bottom)

Features:
  - Search conversations (API integration)
  - Mark messages as read
  - File uploads
  - Emoji reactions
  - User online status
  - Unread message badge

JavaScript Functions:
  - loadConversations(): Fetch all conversations
  - sendMessage(): POST new message
  - markAsRead(): Update read status
  - searchMessages(): Full-text search
  - showNotification(): Toast notifications
```

### 2. **Projects Page** (projects.html)
```
Sections:
  - Project grid/list view
  - Filtering sidebar (tech_stack, status, visibility)
  - Project cards with:
    - Title, description, team count
    - Tech stack tags
    - Like button
    - Quick view action

Features:
  - Responsive grid layout
  - Infinite scroll or pagination
  - Trending projects
  - User projects filter
  - Create new project button
```

### 3. **Profile Page** (profile.html)
```
Sections:
  - Profile header (avatar, name, bio)
  - Stats section (projects, connections, followers)
  - Projects section
  - Activity feed
  - Social links

Features:
  - Edit profile modal
  - Upload avatar
  - Update bio, interests, skills
  - View/manage connections
  - Settings menu
```

### 4. **Navigation/Header Components**
```
Elements:
  - Logo with branding
  - Search bar with autocomplete
  - User menu (profile, settings, logout)
  - Notification bell with badge
  - Messages icon with unread count
  - Mobile menu toggle

Responsive:
  - Desktop: Full nav bar
  - Mobile: Hamburger menu with slide-out drawer
```

---

## API Endpoints Summary

### Authentication
```
POST   /accounts/register/           - Email registration
POST   /accounts/login-otp-send/     - Send OTP to email
POST   /accounts/login-otp-verify/   - Verify OTP and login
POST   /accounts/logout/             - End session
POST   /accounts/password-reset/     - Initiate password reset
```

### Users & Profiles
```
GET    /accounts/profile/            - Get current user profile
PUT    /accounts/profile/            - Update profile
GET    /accounts/user/{id}/          - Get other user profile
GET    /accounts/search/             - Search users
GET    /api/users/{id}/              - User API endpoint
```

### Messaging
```
GET    /api/messages/                - List conversations
GET    /api/messages/{id}/           - Get conversation messages
POST   /api/messages/                - Send message
POST   /api/messages/{id}/read/      - Mark message as read

GET    /api/chat-rooms/              - List chat rooms
POST   /api/chat-rooms/              - Create group chat
POST   /api/chat-rooms/{id}/members/ - Add member to chat
```

### Projects
```
GET    /accounts/projects/           - List all projects
POST   /accounts/projects/           - Create project
GET    /accounts/projects/{id}/      - Get project details
PUT    /accounts/projects/{id}/      - Update project
DELETE /accounts/projects/{id}/      - Delete project

GET    /accounts/projects/feed/      - Personalized feed
GET    /accounts/projects/trending/  - Trending projects
POST   /accounts/projects/{id}/join/ - Join project
```

### Comments
```
GET    /api/projects/{id}/comments/  - Get comments
POST   /api/projects/{id}/comments/  - Post comment
PUT    /api/comments/{id}/           - Edit comment
DELETE /api/comments/{id}/           - Delete comment
POST   /api/comments/{id}/like/      - Like comment
```

### Connections
```
GET    /accounts/connections/        - List connections
POST   /accounts/connections/        - Send request
PUT    /accounts/connections/{id}/   - Accept/Reject
```

### Notifications
```
GET    /accounts/notifications/      - List notifications
POST   /accounts/notifications/{id}/read/ - Mark as read
```

---

## Key Implementation Details

### 1. **Message Read Status Handling**
```python
# In models.py - Message model
def mark_as_read_by(self, user):
    MessageReadStatus.objects.get_or_create(
        message=self,
        user=user,
        defaults={'read_at': timezone.now()}
    )

# In views.py - API endpoint
@login_required
def mark_message_read(request, message_id):
    message = get_object_or_404(Message, id=message_id)
    message.mark_as_read_by(request.user)
    return JsonResponse({'status': 'success'})
```

### 2. **OTP Generation & Verification**
```python
# Generate OTP
otp_obj = OTP.generate_otp(email='user@example.com', purpose='login')
# Returns 6-digit code with 5-minute expiry

# Verify OTP
is_valid, message = otp_obj.verify_otp('123456')
# Returns tuple (bool, message)
```

### 3. **Project Visibility Filter**
```python
# In utils.py - ProjectVisibilityFilter
projects = Project.objects.filter(visibility='public')
# or based on user ownership/membership for private projects

# Implementation:
def get_visible_projects(user):
    # Public projects
    public = Project.objects.filter(visibility='public')
    
    # User's own projects
    owned = Project.objects.filter(owner=user)
    
    # User is a team member
    member = Project.objects.filter(
        members__user=user,
        visibility__in=['private', 'public']
    )
    
    return public | owned | member
```

### 4. **Email Sending Integration**
```python
# In settings.py
EMAIL_BACKEND = 'accounts.brevo_mail_backend.BrevoEmailBackend'
# or 'accounts.zepto_mail_backend.ZeptoMailBackend'

# In views.py
from django.core.mail import EmailMultiAlternatives

def send_otp_email(email, otp_code):
    subject = 'Your UniSync Login Code'
    html_content = f'<h1>Your OTP is: {otp_code}</h1>'
    
    email_msg = EmailMultiAlternatives(subject, '', 'noreply@unisync.com', [email])
    email_msg.attach_alternative(html_content, "text/html")
    email_msg.send()
```

### 5. **Pagination & Performance**
```python
# In views.py
from django.core.paginator import Paginator

def project_feed(request):
    projects = Project.objects.all().order_by('-created_at')
    paginator = Paginator(projects, 10)  # 10 per page
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    return render(request, 'projects.html', {'page_obj': page_obj})
```

---

## Frontend JavaScript Utilities

### API Utilities (in messages.html)
```javascript
const apiUtils = {
    // Fetch with error handling
    async fetch(url, options = {}) {
        const response = await fetch(url, {
            ...options,
            headers: {
                'X-CSRFToken': document.querySelector('[name=csrfmiddlewaretoken]').value,
                ...options.headers
            }
        });
        return response.json();
    },
    
    // Show toast notifications
    showErrorNotification(message, type) {
        // Creates floating notification with icon
    },
    
    // Load data with loading state
    async loadWithLoading(url, callback) {
        // Manages loading UI while fetching
    }
};
```

### Message Management
```javascript
// Load conversations
async function loadConversations() {
    const data = await apiUtils.fetch('/api/messages/');
    renderConversations(data.conversations);
}

// Send message
async function sendMessage(content, recipientId) {
    const response = await apiUtils.fetch('/api/messages/', {
        method: 'POST',
        body: JSON.stringify({
            content: content,
            receiver: recipientId
        })
    });
    return response.id;
}

// Mark as read
async function markAsRead(messageId) {
    await apiUtils.fetch(`/api/messages/${messageId}/read/`, {
        method: 'POST'
    });
}
```

---

## Configuration & Settings

### Django Settings (settings.py)
```python
# Key configurations:
INSTALLED_APPS = [
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'accounts',
    'rest_framework',
    'corsheaders',
]

# Email backend
EMAIL_BACKEND = 'accounts.brevo_mail_backend.BrevoEmailBackend'
EMAIL_HOST = 'smtp-relay.brevo.com'
EMAIL_PORT = 587

# Database
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': os.getenv('DB_NAME'),
        'USER': os.getenv('DB_USER'),
        ...
    }
}

# Cache
CACHES = {
    'default': {
        'BACKEND': 'django.core.cache.backends.locmem.LocMemCache',
    }
}

# Media files (uploads)
MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')
```

### Environment Variables (.env)
```
SECRET_KEY=your-secret-key
DEBUG=False
ALLOWED_HOSTS=yourdomain.com
DB_NAME=unisync_db
DB_USER=postgres
DB_PASSWORD=your-password
BREVO_API_KEY=your-brevo-key
ZEPTO_API_KEY=your-zepto-key
GOOGLE_CLIENT_ID=your-google-id
GOOGLE_CLIENT_SECRET=your-google-secret
```

---

## Development Workflow

### Running the Application
```bash
# Install dependencies
pip install -r requirements.txt

# Run migrations
python manage.py migrate

# Create superuser
python manage.py createsuperuser

# Run development server
python manage.py runserver

# Access admin panel
# http://localhost:8000/admin/
```

### Testing
```bash
# Run tests
python manage.py test

# Test email sending
python manage.py shell
>>> from accounts.models import OTP
>>> otp = OTP.generate_otp('test@example.com', 'login')

# Test API endpoints
curl http://localhost:8000/api/messages/
```

### Deployment
```bash
# Collect static files
python manage.py collectstatic

# Run Gunicorn
gunicorn auth_project.wsgi:application --bind 0.0.0.0:8000

# Or use Docker (see Dockerfile if exists)
```

---

## Known Issues & Improvements

### Identified Issues
1. **Message pagination**: Large conversation threads may be slow
   - Solution: Implement cursor-based pagination

2. **Real-time updates**: Currently polling-based
   - Solution: Implement WebSockets (Django Channels)

3. **Image optimization**: Profile photos not compressed
   - Solution: Use Pillow with compression settings

4. **Search performance**: Full-text search on large datasets
   - Solution: Use PostgreSQL full-text search or Elasticsearch

### Performance Improvements Made
- MessageReadStatus model for scalability
- Pagination for project feeds
- Caching for static user profiles
- Indexed database queries on frequently filtered fields

---

## Security Features

1. **CSRF Protection**: Django middleware with CSRF tokens
2. **OTP Expiry**: 5-minute validity window
3. **Password Hashing**: Django's PBKDF2 algorithm
4. **Email Verification**: Required for account creation
5. **Permission Checks**: User-based access control on views
6. **SQL Injection Prevention**: ORM parameterized queries

---

## Summary

UniSync is a fully-featured collaboration platform with:
- Robust authentication (OTP + OAuth)
- Real-time messaging with read status
- Project management and teamwork
- Social networking (connections, follows)
- Comment threading and feedback
- Activity tracking and notifications
- Email integration (Brevo, ZeptoMail)
- Responsive frontend (Tailwind CSS)

The codebase is well-structured with clear separation of concerns between views, models, API endpoints, and frontend components. Most recent work focused on messaging, comments, and project visibility filtering.

