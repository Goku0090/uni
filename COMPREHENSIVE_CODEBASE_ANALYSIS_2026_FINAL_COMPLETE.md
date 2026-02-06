# UniSync Codebase - Complete Analysis (2026)

## Executive Summary

**UniSync** is a comprehensive Django-based collaborative platform for students to create, share, and collaborate on projects. It integrates social features (connections, followers, likes), real-time messaging, comments, activity tracking, and project management with a robust authentication system supporting both traditional and OAuth login.

---

## 1. TECHNOLOGY STACK

### Backend
- **Framework**: Django 4.x
- **API**: Django REST Framework (DRF)
- **Database**: PostgreSQL (production) / SQLite (development)
- **Authentication**: Django Allauth (OAuth2 for Google/GitHub)
- **Email**: Brevo/ZeptoMail backend services

### Frontend
- **Templates**: Django templates (Jinja2-like)
- **Static Files**: CSS, JavaScript
- **Real-time Features**: WebSocket support via Django Channels (planned)

### Deployment
- **Platforms**: Render.com, Railway.app
- **Environment**: .env for configuration
- **Docker**: Support via Procfile

---

## 2. PROJECT STRUCTURE

```
auth_project/
├── accounts/                    # Main application
│   ├── models.py               # 20+ data models
│   ├── views.py                # Authentication & page views
│   ├── views_contact.py        # Contact & policy views
│   ├── urls.py                 # URL routing
│   ├── forms.py                # Django forms
│   ├── serializers.py          # DRF serializers
│   ├── permissions.py          # Custom permissions
│   ├── utils.py                # Utility functions
│   ├── comment_api.py          # Comment endpoints
│   ├── chat_api_improved.py    # Messaging API
│   ├── zepto_mail_backend.py   # Email backend
│   ├── brevo_mail_backend.py   # Alternative email
│   ├── services/
│   │   └── auth_service.py     # Auth business logic
│   ├── migrations/             # Database migrations
│   ├── templates/              # HTML templates
│   │   ├── account/            # Auth templates
│   │   └── components/         # Reusable components
│   └── templatetags/           # Custom filters
├── auth_project/
│   ├── settings.py             # Django configuration
│   ├── urls.py                 # Root URL config
│   ├── wsgi.py                 # WSGI application
│   └── asgi.py                 # ASGI application
├── media/                      # User uploads
├── static/                     # Static assets
├── templates/                  # Base templates
├── .env                        # Environment variables
└── manage.py                   # Django CLI
```

---

## 3. CORE DATA MODELS (21 Models)

### Authentication & Profiles
| Model | Purpose | Key Fields |
|-------|---------|-----------|
| **User** | Django's built-in | username, email, password |
| **StudentProfile** | Extended user info | full_name, college, bio, skills, interests, profile_photo, social_links |
| **OTP** | One-time passwords | email, otp_code, purpose, expires_at, is_used |

### Project Management
| Model | Purpose | Key Fields |
|-------|---------|-----------|
| **Project** | Main project entity | title, description, owner, visibility, status, category, tags |
| **ProjectMember** | Team members with roles | project, user, role, is_active, joined_at |
| **ProjectTask** | Tasks within projects | title, assigned_to, status, priority, due_date, completed_at |
| **ProjectMilestone** | Project milestones | title, due_date, is_completed, completed_by |
| **ProjectInvitation** | Join invitations | project, invited_user, role, status, expires_at |

### Social & Engagement
| Model | Purpose | Key Fields |
|-------|---------|-----------|
| **Connection** | User connections | sender, receiver, status (pending/accepted/rejected) |
| **Follow** | User followers | follower, following |
| **Like** | Project likes | user, project, created_at |
| **Comment** | Project comments | user, project, content, parent (for threads), is_deleted |

### Messaging & Chat
| Model | Purpose | Key Fields |
|-------|---------|-----------|
| **Message** | DM & group messages | sender, receiver, chat_room, content, message_type, reply_to |
| **ChatRoom** | Group chat containers | chat_type, name, is_active, created_by, members |
| **ChatRoomMember** | Chat room participants | chat_room, user, is_active, joined_at |
| **MessageReadStatus** | Read receipts | message, user, read_at |
| **MessageFile** | Message attachments | message, file |
| **MessageReaction** | Message emojis | message, user, reaction |
| **File** | File uploads | user, file, filename, file_size, file_type |

### Activity & Analytics
| Model | Purpose | Key Fields |
|-------|---------|-----------|
| **Activity** | User action feed | user, activity_type, title, project, target_user |
| **UserStats** | Dashboard statistics | projects_created, connections_made, likes_received, etc. |
| **Notification** | User notifications | user, activity, is_read, created_at |

---

## 4. KEY FEATURES & WORKFLOWS

### 4.1 Authentication Flow
```
User Registration
  ↓
Form Validation → OTP Generation → Email Send
  ↓
OTP Verification → StudentProfile Creation → Session Start
```

**Key Components:**
- `RegisterForm` (accounts/forms.py) - Validation & field handling
- `send_otp_email()` (accounts/views.py) - Email dispatch
- `OTP.verify_otp()` (accounts/models.py) - Verification logic
- OAuth integration via Allauth for social login

### 4.2 Project Visibility Filtering
```
ProjectVisibilityFilter (utils.py)
  ↓
Filters projects based on:
  • User ownership (visible to owner always)
  • Visibility setting (public/private)
  • Team membership
  • Connection status
```

**Filter Logic:**
- Owner can always see their project
- Public projects visible to all authenticated users
- Private projects visible only to team members
- Restricted projects visible only to explicitly added members

### 4.3 Comments System
**Endpoints:**
- `POST /api/projects/{id}/comments/` - Add comment
- `GET /api/projects/{id}/comments/` - List comments
- `DELETE /api/comments/{id}/` - Remove comment
- `PUT /api/comments/{id}/` - Edit comment

**Features:**
- Thread replies (nested comments)
- Comment count badge on project cards
- Deletion with is_deleted flag for soft delete
- Real-time updates via activity feed

### 4.4 Messaging Architecture
**Direct Messages:**
- 1-to-1 user communication
- Read status tracking
- Message reactions
- File attachments

**Group Chats:**
- Multiple members per room
- Chat room ownership
- Member management
- Typing indicators

**Optimization:**
- MessageReadStatus model (scalable design)
- Separate MessageFile & MessageReaction models
- Query optimization with select_related/prefetch_related

### 4.5 Social Engagement
**Connections:**
- Pending → Accepted workflow
- Unique constraint prevents duplicate requests
- Activity feed integration

**Follows:**
- One-way relationship
- Separate from connections
- Unique follower/following pair

**Likes:**
- Per-project engagement metric
- User can like/unlike
- Counted in UserStats

---

## 5. API ENDPOINTS

### Authentication
```
POST   /accounts/register/          - User registration
POST   /accounts/login/              - User login
POST   /accounts/otp-verify/         - OTP verification
POST   /accounts/logout/             - Logout
POST   /accounts/password-reset/     - Password reset
```

### Projects
```
GET    /api/projects/                - List (with filtering)
POST   /api/projects/                - Create project
GET    /api/projects/{id}/           - Project detail
PUT    /api/projects/{id}/           - Update project
DELETE /api/projects/{id}/           - Delete project
POST   /api/projects/{id}/like/      - Toggle like
GET    /api/projects/feed/           - Activity feed
```

### Comments
```
POST   /api/projects/{id}/comments/  - Add comment
GET    /api/projects/{id}/comments/  - List comments
PUT    /api/comments/{id}/           - Edit comment
DELETE /api/comments/{id}/           - Delete comment
```

### Messaging
```
GET    /api/chat-rooms/              - List chat rooms
POST   /api/chat-rooms/              - Create chat room
GET    /api/messages/                - List messages
POST   /api/messages/                - Send message
PUT    /api/messages/{id}/           - Update message
POST   /api/messages/{id}/read/      - Mark as read
```

### Social
```
POST   /api/connections/             - Send connection request
GET    /api/connections/             - List connections
PUT    /api/connections/{id}/        - Accept/Reject
GET    /api/follow/{user}/           - Follow user
DELETE /api/follow/{user}/           - Unfollow
GET    /api/profile/{user}/          - View profile
```

---

## 6. KEY CLASSES & FUNCTIONS

### Models

#### StudentProfile
```python
- get_display_name()           # Returns full_name or username
- profile_completed            # Boolean flag for onboarding
- Social links: github, linkedin, portfolio, behance
```

#### Project
```python
- visibility: 'public', 'private', 'restricted'
- status: 'draft', 'active', 'completed', 'archived'
- is_archived, is_published flags
- get_team_members()           # ProjectMember.objects.filter()
- get_member_count()           # Count team size
```

#### ProjectVisibilityFilter (utils.py)
```python
- filter_projects(user)        # Returns filtered QuerySet
- Logic: ownership > team membership > connections > public
```

#### Comment
```python
- user, project, content
- parent (for thread replies)
- is_deleted flag (soft delete)
- created_at, updated_at
```

### Views

#### Authentication Views (views.py)
- `register_view()` - Handle registration flow with OTP
- `login_view()` - Email-based login
- `send_otp_email()` - Email dispatch with templating

#### Project Views
- `project_feed()` - Filtered project list
- `search_projects()` - Full-text search
- `edit_profile()` - Profile management

#### API Views (DRF)
- `MessageListCreateView` - Message CRUD
- `ChatRoomListCreateView` - Chat room management
- `MessageStatusView` - Read receipt tracking

### Utils (utils.py)

#### StudentProfileNLP
```python
- analyze_interests()          # Parse skill/interest data
- generate_recommendations()   # Suggest collaborators
```

#### ProjectVisibilityFilter
```python
- filter_projects(user)        # Main filtering logic
- For each project:
    1. Check ownership (always visible)
    2. Check visibility setting
    3. Check team membership
    4. Check connections
    5. Allow public access
```

---

## 7. REQUEST/RESPONSE FLOW

### Project Feed Request
```
GET /project_feed/
  ↓
project_feed() view
  ↓
ProjectVisibilityFilter.filter_projects(user)
  ↓
Query projects with:
  - select_related('user')
  - prefetch_related('members', 'comments', 'likes')
  ↓
Template rendering (base_with_footer.html)
  ↓
HTML response with cards
```

### Comment Addition
```
POST /api/projects/{id}/comments/
  ↓
add_comment() (comment_api.py)
  ↓
Validate: user authenticated, project exists
  ↓
Create Comment object
  ↓
Update project comment count
  ↓
Create Activity entry
  ↓
Return JSON response
```

### Message Send
```
POST /api/messages/
  ↓
MessageListCreateView.create()
  ↓
Validate: user in chat_room (ChatRoomMember check)
  ↓
Create Message object
  ↓
Optionally attach files
  ↓
Mark as read by sender
  ↓
Return message detail
```

---

## 8. SECURITY FEATURES

### Authentication
- **CSRF Protection**: Enabled middleware
- **OTP Verification**: 6-digit, 5-min expiry
- **OAuth2**: Allauth with Google/GitHub
- **Password Hashing**: Django's PBKDF2

### Authorization
- **Custom Permissions**: 
  - `IsChatRoomMember` - Chat access control
  - `IsProjectOwnerOrTeamMember` - Project editing
- **Decorators**: 
  - `@check_chat_room_member` - Function-level checks
  - `@check_project_owner` - Ownership verification

### Data Protection
- **Soft Deletes**: Comments use is_deleted flag
- **File Validation**: 
  - Image types only for profile photos
  - File size limits
- **SQL Injection Prevention**: Django ORM parameterization

### Privacy
- **Project Visibility**: Enforced at model/view level
- **Message Filtering**: Only visible to room members
- **Activity Filtering**: Only shows public activities

---

## 9. PERFORMANCE OPTIMIZATIONS

### Database
- **Select Related**: Used for foreign key relationships
- **Prefetch Related**: For reverse/M2M queries
- **Indexing**: On frequently queried fields (user_id, project_id)
- **Pagination**: Implemented in list views

### Caching (Potential)
- User profiles
- Project visibility filters
- User statistics
- Message counts

### Query Optimization
```python
# Good: Minimal queries
projects = Project.objects.filter(user=user).select_related('user')

# Bad: N+1 queries
for project in projects:
    print(project.user.username)  # Query per project
```

---

## 10. COMMON ISSUES & FIXES

### Known Issues
1. **Comment Badge**: Comment count not updating real-time
   - Solution: Refresh on page load or use WebSocket
2. **Profile Photo Not Loading**: Permission issues
   - Solution: Check media folder permissions and CDN setup
3. **Message Read Status**: Delayed synchronization
   - Solution: Use MessageReadStatus model instead of Message.is_read
4. **Login Issues**: OTP expired or not received
   - Solution: Check email configuration and OTP generation

### Debugging Tools
- `debug_profiles.py` - Profile inspection
- `debug_find_collaborators.py` - Collaborator filtering
- `test_comments_api.py` - Comment endpoint testing
- `test_email.py` - Email configuration validation

---

## 11. DEPLOYMENT CHECKLIST

### Environment Variables Required
```
DEBUG=False
SECRET_KEY=<secure-key>
DATABASE_URL=postgresql://user:pass@host/db
EMAIL_BACKEND=accounts.zepto_mail_backend.ZeptoMailBackend
ZEPTO_API_KEY=<key>
ALLOWED_HOSTS=yourdomain.com
SECURE_SSL_REDIRECT=True
SESSION_COOKIE_SECURE=True
CSRF_COOKIE_SECURE=True
```

### Pre-Deployment Tasks
1. Run migrations: `python manage.py migrate`
2. Collect static files: `python manage.py collectstatic --noinput`
3. Create superuser: `python manage.py createsuperuser`
4. Set up OAuth apps in Django admin
5. Configure email backend

### Post-Deployment
1. Verify CSRF protection
2. Test OAuth flow
3. Validate email delivery
4. Monitor error logs
5. Check database backups

---

## 12. FUTURE ENHANCEMENTS

### Planned Features
1. **Real-time Chat**: WebSocket integration (Django Channels)
2. **Video Calls**: Twilio or Agora integration
3. **File Sharing**: S3 integration
4. **Advanced Analytics**: Project performance metrics
5. **Mobile App**: React Native or Flutter
6. **AI Recommendations**: Collaborator suggestions
7. **Notifications**: Push notifications via FCM

### Performance Improvements
1. Celery for async tasks (emails, notifications)
2. Redis for caching/sessions
3. CDN for static assets
4. GraphQL API alternative
5. Database query optimization

---

## 13. FILE REFERENCE GUIDE

### Critical Files
| File | Purpose |
|------|---------|
| `settings.py` | Django config, database, apps, middleware |
| `models.py` | All 21 data models |
| `views.py` | Authentication & page rendering |
| `urls.py` | URL routing |
| `forms.py` | Form validation |
| `serializers.py` | DRF serializers for API |
| `comment_api.py` | Comment endpoints |
| `chat_api_improved.py` | Messaging API |
| `permissions.py` | Authorization checks |
| `utils.py` | Business logic (filtering, NLP) |

### Important Templates
| Template | Purpose |
|----------|---------|
| `base_with_footer.html` | Main layout wrapper |
| `project_detail.html` | Project display with comments |
| `account/student_profile.html` | User profile view |
| `my_projects.html` | User's projects |
| `find_collaborators.html` | Collaborator search |

---

## 14. QUICK START FOR DEVELOPERS

### Setup
```bash
# Clone & navigate
git clone <repo>
cd auth_project

# Create virtual environment
python -m venv venv
source venv/bin/activate  # Linux/Mac
venv\Scripts\activate     # Windows

# Install dependencies
pip install -r requirements.txt

# Setup environment
cp .env.template .env
# Edit .env with your config

# Database setup
python manage.py migrate

# Create superuser
python manage.py createsuperuser

# Run server
python manage.py runserver
```

### Common Commands
```bash
# Create migration
python manage.py makemigrations

# Apply migration
python manage.py migrate

# Create superuser
python manage.py createsuperuser

# Collect static files
python manage.py collectstatic

# Run tests
python manage.py test

# Interactive shell
python manage.py shell
```

---

## 15. CONCLUSION

UniSync is a **production-grade Django application** with:
- ✅ Robust authentication (traditional + OAuth)
- ✅ Comprehensive data models (21 models)
- ✅ REST API with DRF
- ✅ Social features (connections, likes, follows)
- ✅ Real-time messaging
- ✅ Project management
- ✅ Comments & engagement
- ✅ Role-based access control
- ✅ Activity tracking

The codebase is **well-structured**, **scalable**, and **deployment-ready** with proper security, error handling, and optimization patterns in place.

