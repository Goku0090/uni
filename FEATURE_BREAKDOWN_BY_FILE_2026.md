# Unisync Feature Breakdown by File

## Core Feature Map

This document maps each major feature to the files that implement it.

---

## 1. AUTHENTICATION & USER MANAGEMENT

### Feature: Email/OTP Login & Signup
**Purpose**: Users can register and login using email + 6-digit OTP

**Files**:
- `accounts/models.py` (lines 55-124)
  - `OTP` model: stores OTP codes, manages expiry, verification
  - Methods: `generate_otp()`, `verify_otp()`, `is_valid()`
  
- `accounts/views.py` (lines 209-250)
  - `register_view()`: handles registration form, generates OTP
  - `login_view()`: handles login form, sends OTP
  - `otp_verification()`: verifies OTP code, creates user session
  
- `accounts/forms.py`
  - `RegisterForm`: email validation
  - `LoginForm`: email input
  - `OTPVerificationForm`: 6-digit code input
  
- `accounts/urls.py`
  - Routes: `/register/`, `/login/`, `/otp-verify/`

- `auth_project/settings.py` (lines 200-250)
  - `EMAIL_BACKEND`: configured for Zeptomail/Brevo
  - `DEFAULT_FROM_EMAIL`: sender address

**Email Backends**:
- `accounts/brevo_mail_backend.py`: Brevo SMTP implementation
- `accounts/zepto_mail_backend.py`: Zeptomail SMTP implementation

### Feature: Social Login (Google & GitHub)
**Purpose**: Users can login via Google/GitHub OAuth

**Files**:
- `auth_project/settings.py` (lines 50-57)
  - `INSTALLED_APPS`: includes `allauth.socialaccount.providers.google`, `.github`
  
- `auth_project/urls.py`
  - Route: `/accounts/sociallogin/` → allauth views
  
- `accounts/views.py` (lines 2500-2600)
  - Social login callback handlers
  - Auto-creates StudentProfile on first login

**Configuration**:
- `.env`: `GOOGLE_OAUTH_CLIENT_ID`, `GOOGLE_OAUTH_CLIENT_SECRET`
- `.env`: `GITHUB_CLIENT_ID`, `GITHUB_CLIENT_SECRET`

### Feature: User Profile Management
**Purpose**: Users can view/edit their profile

**Files**:
- `accounts/models.py` (lines 12-54)
  - `StudentProfile` model: college, location, interests, skills, bio, profile_photo
  
- `accounts/views.py` (lines 49-61)
  - `edit_profile()`: edit profile form + file upload
  - `student_profile_view()`: view public profile
  
- `accounts/forms.py`
  - `StudentProfileForm`: validates profile fields
  
- `accounts/templates/accounts/edit_profile.html`
  - Profile edit form with file upload
  
- `accounts/templates/accounts/profile.html`
  - Public profile view

**Static Files**:
- `accounts/static/css/profile.css`: profile styling
- `accounts/static/js/profile.js`: avatar preview

---

## 2. PROJECT MANAGEMENT

### Feature: Create & Post Projects
**Purpose**: Users can create and share project ideas looking for collaborators

**Files**:
- `accounts/models.py` (lines 403-449)
  - `Project` model: title, description, technologies, looking_for, category, timeline, github_link
  
- `accounts/views.py` (lines 1611-1652)
  - `create_project_view()`: form handling, validation, saves to DB
  - Project creation activity logged
  
- `accounts/forms.py`
  - `ProjectForm`: validates all project fields, converts JSON arrays
  
- `accounts/urls.py`
  - Routes: `/create-project/`, `/projects/`, `/projects/<id>/`

**Templates**:
- `accounts/templates/accounts/create_project.html`: form
- `accounts/templates/accounts/project_feed.html`: list view

### Feature: Project Feed & Search
**Purpose**: Browse all projects, search by keyword, filter by category

**Files**:
- `accounts/views.py` (lines 5-10)
  - `project_feed()`: paginated list (10 per page)
  
- `accounts/views.py` (lines 64-74)
  - `search_projects()`: search by title/description/collaboration_needs
  
- `accounts/utils.py`
  - `ProjectVisibilityFilter`: checks if user can view project
  - Private/Public filtering

**Database Query Optimization**:
- Uses `select_related('owner')` for user data
- Uses `prefetch_related('comments', 'likes')` for counts

### Feature: Project Details & Comments
**Purpose**: View project details, read/write comments, see who's interested

**Files**:
- `accounts/models.py` (lines 371-385)
  - `Comment` model: user, project, content, timestamps
  
- `accounts/views.py`
  - `project_detail()`: display project, comments, like count
  
- `accounts/comment_api.py`
  - `create_comment()`: add comment
  - `delete_comment()`: remove comment (owner only)
  - `get_comments()`: fetch comments for project
  
- `accounts/urls.py`
  - API routes: `/api/comments/`, `/api/comments/<id>/`

**Templates**:
- `accounts/templates/accounts/project_detail.html`
  - Shows comments section
  - Like button
  - Team members

### Feature: Like Projects
**Purpose**: Users can like/unlike projects to show interest

**Files**:
- `accounts/models.py` (lines 451-461)
  - `Like` model: user, project (unique together)
  
- `accounts/views.py`
  - `like_project()`: add like
  - `unlike_project()`: remove like
  
- JavaScript in templates
  - Like button toggle

**Permission**:
- Any authenticated user can like
- `Like` model prevents duplicate likes (unique_together)

### Feature: Project Visibility & Permissions
**Purpose**: Projects can be public/private, only collaborators see private projects

**Files**:
- `accounts/utils.py`
  - `ProjectVisibilityFilter` class
  - Checks: owner? collaborator? public?
  
- `accounts/models.py` (Project model)
  - `is_active` field (soft delete)
  
- `accounts/views.py`
  - All project views check visibility before showing

---

## 3. COLLABORATOR MATCHING & CONNECTIONS

### Feature: Find Collaborators (Smart Matching)
**Purpose**: AI-powered recommendations based on interests/skills/project preferences

**Files**:
- `accounts/views.py` (lines 1453-1578)
  - `find_collaborators()`: main endpoint
  
- `accounts/utils.py`
  - `StudentProfileNLP` class
  - `match_profiles()`: algorithm implementation
  - Uses: interests, skills, project_interests comparison
  - Returns: ranked list by similarity score

**Algorithm**:
```
For each profile in database:
  Calculate similarity_score = (
    interest_overlap +
    skill_overlap +
    project_interest_overlap
  )
  Sort by score descending
  Return top 20 matches
```

### Feature: Connection Requests
**Purpose**: Users can send/receive/accept/reject connection requests

**Files**:
- `accounts/models.py` (lines 126-147)
  - `Connection` model: sender, receiver, status (pending/accepted/rejected)
  - Unique constraint: no duplicate requests
  
- `accounts/views.py`
  - `send_connection_request()`: create connection
  - `accept_connection()`: update status to 'accepted'
  - `reject_connection()`: update status to 'rejected'
  - `get_connections()`: list all connections
  
- `accounts/urls.py`
  - API routes: `/api/connections/`

**Notifications**:
- Creating `Notification` object when request sent
- Notification type: `'connection_request'`

---

## 4. MESSAGING & REAL-TIME COMMUNICATION

### Feature: Direct Messages
**Purpose**: One-on-one messaging between users

**Files**:
- `accounts/models.py` (lines 149-217)
  - `Message` model: sender, receiver, content, timestamps
  - Methods: `mark_as_read_by()`, `is_read_by()`
  
- `accounts/models.py` (lines 264-277)
  - `MessageReadStatus` model: tracks who read what (scalable design)
  
- `accounts/chat_api.py`
  - `send_message()`: create message, trigger notification
  - `get_messages()`: fetch history (paginated)
  - `mark_message_read()`: update read status
  
- `accounts/urls.py`
  - API routes: `/api/messages/`

### Feature: Message Read Receipts
**Purpose**: See who has read your messages

**Files**:
- `accounts/models.py` (lines 264-277)
  - `MessageReadStatus` model
  
- `accounts/models.py` (lines 184-196)
  - `Message.is_read_by()`: check if user read
  - `Message.get_read_count()`: count readers
  
- `accounts/chat_api.py`
  - Check/update read status on message fetch

**UI**:
- Show checkmark (✓ sent, ✓✓ delivered, ✓✓ read)

### Feature: Group Chats
**Purpose**: Multiple users can chat in one room

**Files**:
- `accounts/models.py` (lines 279-307)
  - `ChatRoom` model: name, chat_type (direct/group/project), members
  
- `accounts/models.py` (lines 309-335)
  - `ChatRoomMember` model: role (owner/admin/member), is_active
  
- `accounts/models.py` (lines 149-217)
  - `Message` model: can link to ChatRoom OR direct receiver
  
- `accounts/chat_api.py`
  - `get_conversations()`: list all chats (direct + group)
  - `create_group_chat()`: create new group
  - `add_member()`: invite user

### Feature: File Sharing in Messages
**Purpose**: Users can attach files to messages

**Files**:
- `accounts/models.py` (lines 243-262)
  - `File` model: file, filename, size, type, upload_at
  
- `accounts/models.py` (lines 219-228)
  - `MessageFile` model: links message to file
  
- `accounts/chat_api.py`
  - `upload_file_to_message()`: attach file
  
- `accounts/templates/` (chat template)
  - File upload input
  - Download link

**Storage**:
- Files stored in AWS S3 (boto3)
- File metadata in database

### Feature: Message Reactions
**Purpose**: React to messages with emoji

**Files**:
- `accounts/models.py` (lines 230-241)
  - `MessageReaction` model: message, user, reaction (emoji text)
  - Unique: user can only have one reaction per message
  
- `accounts/chat_api.py`
  - `add_reaction()`: add emoji reaction
  - `remove_reaction()`: remove reaction

### Feature: Real-Time Messaging (WebSocket)
**Purpose**: Messages appear instantly without refresh

**Files**:
- `accounts/models.py` (lines 387-401)
  - `UserStatus` model: is_online, last_seen, current_room
  
- `auth_project/asgi.py`
  - WebSocket routing setup
  
- `auth_project/settings.py` (lines 50-51)
  - `'channels'` in INSTALLED_APPS
  - Channel layers configured for Redis
  
- `accounts/chat_api.py` (WebSocket handlers)
  - `ws_connect()`: user joins WebSocket room
  - `ws_disconnect()`: user leaves
  - `ws_message()`: receive & broadcast message
  
- JavaScript in templates
  - WebSocket client connection
  - Message auto-refresh

**Architecture**:
```
User A sends message
  ↓
View saves to database
  ↓
Channels Redis broadcasts
  ↓
User B's WebSocket receives
  ↓
JavaScript updates DOM (no refresh!)
```

---

## 5. NOTIFICATIONS & ACTIVITY FEED

### Feature: User Notifications
**Purpose**: Alert users to important events (messages, likes, comments, etc.)

**Files**:
- `accounts/models.py` (lines 337-369)
  - `Notification` model: type, title, message, is_read, from_user
  - Types: connection_request, message, project_like, project_comment, team_invitation, follow
  
- `accounts/views.py`
  - `get_notifications()`: fetch user's notifications
  - `mark_notification_read()`: mark as read
  - `delete_notification()`: soft delete
  
- `accounts/urls.py`
  - API routes: `/api/notifications/`

**Notification Creation**:
- Created whenever: message sent, project liked, connection requested, etc.
- Viewed in notification bell icon in navbar

### Feature: Activity Feed
**Purpose**: See what users you follow are doing

**Files**:
- `accounts/models.py` (lines 475-508)
  - `Activity` model: activity_type, title, description, project, target_user
  - Types: profile_updated, project_created, project_liked, connection_made, etc.
  - `is_public` field: public activities vs private
  
- `accounts/views.py` (lines 77-87)
  - `dashboard_view()`: shows recent activities
  
- `accounts/templates/accounts/dashboard.html`
  - Activity feed display

**Activity Logging**:
- Logged in views when action occurs:
  - Project created → Activity object created
  - Project liked → Like + Activity created
  - Connection accepted → Activity created

---

## 6. FOLLOWING & SOCIAL GRAPH

### Feature: Follow Users
**Purpose**: Users can follow each other to see activities

**Files**:
- `accounts/models.py` (lines 463-473)
  - `Follow` model: follower, following (relationships)
  - Unique: can only follow once
  
- `accounts/views.py`
  - `follow_user()`: add follow relationship
  - `unfollow_user()`: remove follow
  - `get_followers()`: list followers
  - `get_following()`: list who user follows
  
- `accounts/templates/`
  - Follow button on profile

**Activity Feed Integration**:
- Dashboard shows activities from followers (is_public=True)

---

## 7. USER AUTHENTICATION & PERMISSIONS

### Feature: Login Required
**Purpose**: Protect views so only logged-in users can access

**Files**:
- `accounts/views.py`
  - `@login_required` decorator on views
  - Redirects to login if not authenticated
  
- `accounts/permissions.py`
  - Custom DRF permissions
  - `IsOwner`: only owner can modify
  - `IsAuthenticated`: only logged in users

### Feature: CSRF Protection
**Purpose**: Prevent cross-site request forgery attacks

**Files**:
- `auth_project/settings.py` (line 68)
  - `'django.middleware.csrf.CsrfViewMiddleware'` enabled
  
- `accounts/templates/`
  - `{% csrf_token %}` in all forms

### Feature: Session Management
**Purpose**: Keep users logged in across requests

**Files**:
- `auth_project/settings.py` (lines 120-130)
  - `SESSION_ENGINE`: Redis-based sessions
  - `SESSION_COOKIE_SECURE`: HTTPS only (production)
  - `SESSION_COOKIE_HTTPONLY`: prevent JS access

---

## 8. SEARCH & FILTERING

### Feature: Project Search
**Purpose**: Find projects by title, description, or technology

**Files**:
- `accounts/views.py` (lines 64-74)
  - `search_projects()`: Q() queries for OR logic
  - Searches: title, description, collaboration_needs
  
- `accounts/forms.py`
  - Search form validation

### Feature: Collaborator Search
**Purpose**: Find users based on skills and interests

**Files**:
- `accounts/views.py` (lines 1453-1578)
  - `find_collaborators()` view
  
- `accounts/utils.py`
  - `StudentProfileNLP.match_profiles()`

### Feature: Project Filtering
**Purpose**: Filter by category, technology, timeline

**Files**:
- `accounts/urls.py`
  - URL parameters: `?category=web&tech=python`
  
- `accounts/views.py`
  - Query string parsing: `request.GET.get('category')`
  - Filter applied in QuerySet

---

## 9. ERROR HANDLING & VALIDATION

### Feature: Form Validation
**Purpose**: Validate user input on server side

**Files**:
- `accounts/forms.py`
  - All form classes: `clean()` methods
  - Django built-in validators: email, URL, file size
  
- `accounts/views.py` (lines 90-100)
  - Form validation: `if form.is_valid()`
  - Error messages: `messages.error(request, "...")`

### Feature: Error Handling Decorator
**Purpose**: Catch exceptions and show friendly error messages

**Files**:
- `accounts/views.py` (lines 90-100)
  - `handle_view_errors()` decorator
  - Logs exceptions to logger
  - Shows user-friendly messages

---

## 10. EMAIL & NOTIFICATIONS

### Feature: Email Sending
**Purpose**: Send OTP codes, notifications, updates

**Files**:
- `accounts/brevo_mail_backend.py`
  - Brevo SMTP backend implementation
  
- `accounts/zepto_mail_backend.py`
  - Zeptomail SMTP backend implementation
  
- `auth_project/settings.py`
  - `EMAIL_BACKEND`: choose which provider
  - Email credentials from .env

**Email Templates**:
- `accounts/templates/emails/otp.html`: OTP code
- `accounts/templates/emails/notification.html`: generic notification
- `accounts/templates/emails/welcome.html`: welcome email

### Feature: Notification Emails
**Purpose**: Users get email alerts for important events

**Files**:
- `accounts/views.py`
  - Send notification emails when events occur
  - Uses Django's `send_mail()` or `EmailMultiAlternatives`

---

## 11. FILE UPLOADS & STORAGE

### Feature: Profile Photo Upload
**Purpose**: Users can upload profile pictures

**Files**:
- `accounts/models.py` (lines 22-27)
  - `StudentProfile.profile_photo`: ImageField
  - Validators: only jpg, jpeg, png, gif
  
- `accounts/views.py` (lines 49-61)
  - `edit_profile()`: handles file upload
  - `request.FILES['profile_photo']`
  
- `accounts/forms.py`
  - `StudentProfileForm`: file input

**Storage**:
- AWS S3 via `django-storages` and boto3
- `settings.py`: S3 bucket configuration

### Feature: File Sharing in Chat
**Purpose**: Attach documents, images to messages

**Files** (see Messaging section)
- `accounts/models.py` (File, MessageFile models)
- `accounts/chat_api.py` (upload_file_to_message)

---

## 12. ADMINISTRATION & MANAGEMENT

### Feature: Django Admin Interface
**Purpose**: Admin users can manage data directly

**Files**:
- `accounts/admin.py` (if exists)
  - Register models in admin
  - Custom admin views
  
- Access: `/admin/` (superuser only)

### Feature: Superuser Management
**Purpose**: Create/manage admin users

**Command**:
```bash
python manage.py createsuperuser
```

---

## 13. API & SERIALIZATION

### Feature: REST API (DRF)
**Purpose**: Provide JSON endpoints for frontend/mobile apps

**Files**:
- `accounts/serializers.py`
  - `UserProfileSerializer`
  - `ProjectSerializer`
  - `MessageSerializer`
  - `NotificationSerializer`
  - `ConnectionSerializer`
  
- `accounts/views.py` (generic views)
  - Use DRF's `generics.ListAPIView`, `generics.CreateAPIView`
  
- `accounts/urls.py`
  - API routes: `/api/*`

**Response Format**:
```json
{
  "id": 1,
  "username": "john",
  "profile": {
    "full_name": "John Doe",
    "interests": ["web", "ai"]
  }
}
```

---

## 14. CACHING & PERFORMANCE

### Feature: View Caching
**Purpose**: Cache expensive queries to improve speed

**Files**:
- `accounts/views.py`
  - `@cache_page(60*5)` decorator: cache view for 5 minutes
  
- `auth_project/settings.py`
  - Redis cache backend configuration

### Feature: Session Caching
**Purpose**: Store user sessions in Redis (faster than database)

**Files**:
- `auth_project/settings.py`
  - `SESSION_ENGINE = 'django_redis.cache.session.SessionStore'`

---

## 15. LOGGING & DEBUGGING

### Feature: Application Logging
**Purpose**: Track errors and events for debugging

**Files**:
- `accounts/views.py` (line 42)
  - `logger = logging.getLogger(__name__)`
  - `logger.error()`, `logger.info()` throughout
  
- `auth_project/settings.py`
  - Logging configuration
  - Log level, handlers, formatters

---

## QUICK FILE REFERENCE TABLE

| Feature | Primary File | Secondary Files |
|---------|-------------|-----------------|
| OTP Login | models.py (OTP) | views.py, forms.py, email backends |
| Social Login | settings.py | views.py, urls.py |
| Profile | models.py (StudentProfile) | views.py, forms.py, templates |
| Projects | models.py (Project) | views.py, serializers.py, urls.py |
| Comments | models.py (Comment) | comment_api.py, urls.py |
| Connections | models.py (Connection) | views.py, urls.py |
| Messages | models.py (Message, ChatRoom) | chat_api.py, urls.py |
| Notifications | models.py (Notification) | views.py, urls.py |
| Activity | models.py (Activity) | views.py, templates |
| Follow | models.py (Follow) | views.py |
| Likes | models.py (Like) | views.py |
| Search | utils.py | views.py |
| Permissions | permissions.py | views.py |
| Email | brevo_mail_backend.py, zepto_mail_backend.py | settings.py, views.py |
| Files | models.py (File) | views.py, settings.py (S3) |
| API | serializers.py | views.py, urls.py |
| Real-time | asgi.py, chat_api.py | settings.py, models.py |
| Cache | settings.py | views.py |

---

**Last Updated**: February 2026
