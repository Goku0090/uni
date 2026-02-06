# COMPREHENSIVE CODEBASE ANALYSIS - UniSync Project

## Project Overview
**Project Name**: UniSync (University Collaboration & Project Management Platform)  
**Type**: Full-stack Django + JavaScript Web Application  
**Purpose**: Connect students across colleges for collaborative projects  
**Tech Stack**: Django, PostgreSQL, JavaScript, HTML/CSS  
**Repository**: https://github.com/Goku0090/uni  

---

## 1. ARCHITECTURE OVERVIEW

### High-Level Architecture
```
┌─────────────────────────────────────────────────────────────┐
│                    Frontend Layer                           │
│  (HTML Templates, JavaScript, CSS, Bootstrap)              │
│  - Dashboard                                                │
│  - Project Pages                                            │
│  - User Profiles                                            │
│  - Messaging & Notifications                               │
└────────────────────┬────────────────────────────────────────┘
                     │
                     ▼
┌─────────────────────────────────────────────────────────────┐
│                   Django Backend                            │
│  ├─ Views & ViewSets (REST & Template-based)              │
│  ├─ Models (Database Layer)                                │
│  ├─ Serializers (REST API)                                 │
│  ├─ URLs & Routing                                         │
│  └─ Authentication & Permissions                           │
└────────────────────┬────────────────────────────────────────┘
                     │
                     ▼
┌─────────────────────────────────────────────────────────────┐
│                  Database Layer                             │
│  - PostgreSQL / SQLite (Development)                       │
│  - Student Profiles, Projects, Messages, Notifications     │
└─────────────────────────────────────────────────────────────┘
```

---

## 2. CORE MODELS & DATABASE SCHEMA

### Primary Models

#### A. **StudentProfile**
- **Purpose**: Extended user profile for students
- **Key Fields**:
  - `user` (OneToOne to User)
  - `full_name`, `college`, `location`
  - `interests`, `skills`, `project_interests` (JSON arrays)
  - `profile_photo` (ImageField)
  - `bio`, `role_preference`
  - `github`, `linkedin`, `portfolio`, `behance` (social links)
  - `profile_completed` (Boolean)
  - `created_at`, `updated_at` (Timestamps)
- **Methods**:
  - `get_display_name()`: Returns full_name or username
- **Relationships**: One-to-One with Django User

#### B. **Project**
- **Purpose**: User-created collaborative projects
- **Key Fields**:
  - `title`, `description`, `category`
  - `owner` (ForeignKey to User)
  - `members` (ManyToMany to User)
  - `collaboration_needs` (JSON array)
  - `skills_required` (JSON array)
  - `visibility` (public/private)
  - `project_type` (collaborative/research/internship)
  - `status` (planning/active/completed)
  - `created_at`, `updated_at`
  - `likes_count`, `comments_count`
- **Methods**:
  - `add_member()`, `remove_member()`, `is_member()`
  - `get_collaboration_needs()`, `get_skills_required()`
- **Visibility**: Filtered via ProjectVisibilityFilter utility

#### C. **Connection** (Networking)
- **Purpose**: Track follower relationships between users
- **Key Fields**:
  - `from_user`, `to_user` (ForeignKey to User)
  - `is_following` (Boolean)
  - `created_at`
- **Purpose**: Enable user networking and collaboration discovery

#### D. **Message & Chat System**
Models: `Message`, `MessageFile`, `MessageReaction`, `MessageReadStatus`
- **Message**: Direct messages between users
  - `from_user`, `to_user`
  - `content`
  - `created_at`, `read_at`
  - Supports file attachments and reactions
- **Features**: File sharing, message reactions, read status tracking

#### E. **Notification System**
- **Model**: `Notification`
- **Fields**:
  - `user` (recipient)
  - `type` (message, like, comment, connection)
  - `related_object_id`, `related_object_type`
  - `is_read`
  - `created_at`
- **Purpose**: Alert users to important activities

#### F. **Comments & Interactions**
- **Model**: `Comment`
- **Fields**:
  - `project` (ForeignKey)
  - `user` (author)
  - `text` (comment content)
  - `created_at`, `updated_at`
- **Features**: Comments on projects with nested replies support

#### G. **Project Team Management**
Models: `ProjectTeam`, `ProjectTeamMember`, `ProjectTeamInvitation`
- **ProjectTeam**: Team for a specific project
- **ProjectTeamMember**: Team member with role assignment
- **ProjectTeamInvitation**: Invitation to join a team
- **Purpose**: Manage project team composition and roles

#### H. **Activity & Stats Tracking**
- **Models**: `Activity`, `UserStats`, `Like`
- **Activity**: Tracks all user actions (project creation, comments, etc.)
- **UserStats**: User engagement metrics
- **Like**: Track likes on projects/comments
- **Purpose**: Analytics and engagement tracking

#### I. **Chat & Real-time Communication**
- **Models**: `ChatRoom`, `ChatRoomMember`
- **Purpose**: Real-time messaging between users and groups
- **Features**: Room-based chat with member management

#### J. **Additional Models**
- **Follow**: Social following mechanism
- **UserStatus**: User online/offline status
- **File**: File upload tracking
- **ProjectTask**: Task management within projects
- **ProjectMilestone**: Project milestone tracking
- **OTP**: One-time password authentication

---

## 3. VIEWS & ENDPOINTS

### Authentication & User Management
- `login_view()` - User login with OTP verification
- `register_view()` - User registration
- `logout_view()` - User logout
- `edit_profile()` - Profile editing with avatar upload
- `student_profile()` - View user profile
- `user_profile_api()` - API endpoint for user profile
- `view_other_profile()` - View other user profiles

### Project Management
- `create_project()` - Create new project
- `edit_project()` - Edit project details
- `delete_project()` - Delete project
- `project_detail()` - View project details
- `project_feed()` - Paginated project listing
- `search_projects()` - Search & filter projects
- `add_collaborator()` - Add team member
- `remove_collaborator()` - Remove team member
- `find_collaborators()` - Find potential collaborators with advanced filtering

### Collaboration & Networking
- `connect_user()` - Follow another user
- `disconnect_user()` - Unfollow user
- `get_connections()` - List user connections
- `get_suggested_collaborators()` - Recommend collaborators

### Messaging & Notifications
- `send_message()` - Send direct message
- `view_messages()` - View message thread
- `get_notifications()` - Fetch user notifications
- `mark_notification_read()` - Mark notification as read

### Comments & Interactions
- `post_comment()` - Post comment on project
- `edit_comment()` - Edit existing comment
- `delete_comment()` - Delete comment
- `like_project()` - Like a project
- `unlike_project()` - Unlike a project

### API Endpoints (REST Framework)
- `/api/users/` - User list/create
- `/api/projects/` - Project list/create
- `/api/projects/<id>/` - Project detail
- `/api/messages/` - Message operations
- `/api/comments/` - Comment operations
- `/api/notifications/` - Notification management
- `/api/connections/` - Connection management

---

## 4. KEY UTILITIES & SERVICES

### A. **StudentProfileNLP** (accounts/utils.py)
- **Purpose**: NLP-based profile matching and recommendations
- **Features**:
  - Profile similarity scoring
  - Skill matching algorithm
  - Interest intersection calculation
  - Recommendation engine
- **Usage**: Recommend collaborators, suggest projects

### B. **ProjectVisibilityFilter** (accounts/utils.py)
- **Purpose**: Filter projects based on visibility rules
- **Logic**:
  - Public projects visible to all
  - Private projects only to owner
  - Team members can see team projects
- **Integration**: Used in project feed and search

### C. **Email Backends**
- **Files**: `brevo_mail_backend.py`, `zepto_mail_backend.py`
- **Purpose**: Send emails via third-party services
- **Features**:
  - OTP emails with HTML formatting
  - Rich email templates
  - Error handling & logging
- **Default**: Uses Django's default email backend (configurable in settings)

### D. **Chat API**
- **Files**: `chat_api.py`, `chat_api_improved.py`
- **Features**:
  - Real-time messaging endpoints
  - WebSocket support (optional)
  - Message history
  - Read receipts

### E. **Comment API** (comment_api.py)
- **Features**:
  - Post, edit, delete comments
  - Comment count tracking
  - Nested reply support
  - Notification on mentions

---

## 5. AUTHENTICATION & AUTHORIZATION

### Authentication Methods
1. **Email OTP Login** (Primary)
   - User enters email
   - OTP sent via email
   - User enters OTP code
   - Session created if valid

2. **Traditional Username/Password** (Alternative)
   - Supported but not primary
   - Uses Django's built-in authentication

3. **Social OAuth** (Optional)
   - Google OAuth integration
   - GitHub OAuth integration (setup provided)

### Authorization Mechanisms
- **Django Permissions**: Role-based access control
- **Custom Decorators**:
  - `@login_required` - Require authentication
  - `@handle_view_errors` - Error handling wrapper
- **DRF Permissions**: 
  - `IsAuthenticated`
  - `IsOwnerOrReadOnly`
  - Custom permission classes

### Roles & Permissions
- **Regular User**: Standard access
- **Project Owner**: Full project control
- **Team Member**: Limited project access
- **Admin**: Full system access

---

## 6. FORMS & VALIDATION

### Key Forms (accounts/forms.py)

#### A. **RegisterForm**
- Fields: email, password, password_confirm
- Validation: Unique email, password strength

#### B. **LoginForm**
- Fields: email/username, password (or otp)
- Validation: User existence, OTP validity

#### C. **OTPVerificationForm**
- Field: otp_code (6 digits)
- Validation: OTP format, expiration, usage

#### D. **StudentProfileForm**
- Fields: full_name, college, interests, skills, profile_photo, etc.
- Validation: Image file type, field lengths

#### E. **ProjectForm**
- Fields: title, description, category, visibility, collaboration_needs
- Validation: Required fields, category choices

---

## 7. STATIC & MEDIA FILES

### Directory Structure
```
auth_project/
├── static/
│   ├── css/
│   │   ├── style.css          # Main stylesheet
│   │   ├── dashboard.css      # Dashboard styles
│   │   ├── project_detail.css # Project page styles
│   │   └── responsive.css     # Responsive design
│   ├── js/
│   │   ├── main.js            # Global JavaScript
│   │   ├── projects.js        # Project handling
│   │   ├── messages.js        # Messaging logic
│   │   ├── notifications.js   # Notification handling
│   │   └── live-feed.js       # Live feed updates
│   └── images/
│       ├── logo.png
│       ├── icons/
│       └── backgrounds/
├── media/
│   └── profile_photos/        # User profile pictures
└── staticfiles/              # Collected static files
```

### Key CSS Features
- Bootstrap framework for responsive design
- Custom CSS variables for theming
- Mobile-first approach
- Dark mode support (optional)

### Key JavaScript Features
- AJAX for dynamic content loading
- Real-time notifications via WebSocket/polling
- Form validation
- Live project filtering
- Comment system with AJAX submission

---

## 8. TEMPLATES STRUCTURE

### Template Hierarchy
```
templates/
├── base.html               # Base layout
├── accounts/
│   ├── login.html
│   ├── register.html
│   ├── edit_profile.html
│   ├── student_profile.html
│   ├── view_other_profile.html
│   └── find_collaborators.html
├── projects/
│   ├── project_feed.html   # Main project listing
│   ├── project_detail.html # Project details page
│   ├── create_project.html
│   └── edit_project.html
├── messages/
│   ├── messages_list.html
│   └── message_detail.html
├── notifications/
│   ├── notifications.html
│   └── notification_detail.html
└── common/
    ├── navbar.html
    ├── sidebar.html
    ├── footer.html
    └── pagination.html
```

### Template Features
- Django template inheritance (base.html)
- CSRF token handling
- Context data rendering
- Conditional content (login_required)
- Form rendering with error messages

---

## 9. KEY FEATURES & WORKFLOWS

### A. User Registration & Authentication Flow
```
1. User visits /register
2. Fills registration form (email, password)
3. Account created in User model
4. StudentProfile auto-created via signal
5. Redirect to login page
6. User enters email on login
7. OTP sent via email
8. User enters OTP code
9. Session created, redirect to dashboard
```

### B. Project Creation & Collaboration Flow
```
1. User creates project (title, description, needs)
2. Project stored in database
3. User appears as owner
4. Other users can view/discover project
5. Collaborators can request to join
6. Owner approves/rejects requests
7. Approved members can:
   - Edit project details
   - Post comments
   - Manage tasks/milestones
```

### C. Messaging Flow
```
1. User sends message to another user
2. Message stored in database
3. Recipient notified
4. Recipient can read and reply
5. Read status tracked
6. Optional: Real-time updates via WebSocket
```

### D. Notification Flow
```
1. Action triggered (like, comment, follow)
2. Notification created in database
3. Notification fetched by recipient
4. Mark as read on view
5. Optional: Real-time push via WebSocket
```

### E. Collaborator Discovery Flow
```
1. User visits "Find Collaborators"
2. Filters applied (skills, interests, college)
3. Profile matching algorithm runs
4. Results sorted by relevance
5. User can view profiles and connect
6. Mutual follow creates connection
```

---

## 10. CONFIGURATION & SETTINGS

### Key Settings (auth_project/settings.py)
- **Database**: PostgreSQL (production) / SQLite (development)
- **Authentication Backend**: Email OTP + Django Auth
- **Email**: Brevo/ZeptoMail or default backend
- **Static Files**: WhiteNoise for production
- **CORS**: For API calls
- **Session**: Django default session framework
- **Cache**: Redis (optional) or database

### Environment Variables (.env)
- `DEBUG` - Development mode
- `SECRET_KEY` - Django secret
- `DATABASE_URL` - Database connection
- `EMAIL_BACKEND` - Email service choice
- `GOOGLE_OAUTH_ID`, `GOOGLE_OAUTH_SECRET` - OAuth config
- `ALLOWED_HOSTS` - Allowed domain

---

## 11. COMMON ISSUES & FIXES

### Issue #1: Comments Not Visible
- **Cause**: Template not rendering comments correctly
- **Fix**: Ensure comment template is included in project detail
- **Files**: `project_detail.html`, `comment_api.py`

### Issue #2: CSRF Token Errors
- **Cause**: Missing CSRF token in forms
- **Fix**: Add `{% csrf_token %}` to all POST forms
- **Files**: All templates with forms

### Issue #3: Profile Photos Not Uploading
- **Cause**: Missing MEDIA_URL/MEDIA_ROOT configuration
- **Fix**: Configure in settings.py, ensure nginx/server serves media
- **Files**: `settings.py`, web server config

### Issue #4: Collaborators Not Showing
- **Cause**: Visibility filter excluding valid users
- **Fix**: Debug filter logic in `find_collaborators()`
- **Files**: `accounts/utils.py`, `views.py`

### Issue #5: OTP Not Sending
- **Cause**: Email backend misconfiguration
- **Fix**: Verify email credentials, check email logs
- **Files**: `settings.py`, email backend files

### Issue #6: Project Detail Loading Slow
- **Cause**: N+1 query problem
- **Fix**: Use `select_related()` and `prefetch_related()`
- **Files**: `views.py`, model queries

---

## 12. DEPLOYMENT CONSIDERATIONS

### Production Setup
1. **Database**: Use PostgreSQL
2. **Static Files**: Collect with `python manage.py collectstatic`
3. **Media Files**: Serve via CDN or web server
4. **Email**: Configure production email service
5. **Security**:
   - Set `DEBUG=False`
   - Configure `ALLOWED_HOSTS`
   - Use HTTPS only
   - Set secure cookie flags
   - Enable CSRF protection

### Deployment Platforms
- **Render**: Recommended (PostgreSQL support)
- **Railway**: Alternative option
- **Heroku**: Legacy option
- **Self-hosted**: Linux + Nginx + Gunicorn

---

## 13. DEVELOPMENT QUICK REFERENCE

### Running Locally
```bash
# Setup
python manage.py migrate
python manage.py createsuperuser
python manage.py collectstatic

# Run
python manage.py runserver

# Access
Browser: http://localhost:8000
Admin: http://localhost:8000/admin
```

### Key Management Commands
```bash
python manage.py makemigrations     # Create migrations
python manage.py migrate            # Apply migrations
python manage.py createsuperuser    # Create admin user
python manage.py shell              # Django shell
python manage.py dbshell            # Database shell
python manage.py test               # Run tests
python manage.py runserver          # Development server
```

---

## 14. TECHNOLOGY STACK SUMMARY

| Component | Technology | Version |
|-----------|-----------|---------|
| Backend | Django | 4.x |
| Database | PostgreSQL/SQLite | Latest |
| Frontend | HTML/CSS/JavaScript | ES6+ |
| CSS Framework | Bootstrap | 5.x |
| REST API | Django REST Framework | 3.x |
| Authentication | Django Auth + OTP | Custom |
| Email | Brevo/ZeptoMail | Latest |
| Social Auth | django-allauth | Latest |
| Hosting | Render/Railway | Latest |
| VCS | Git/GitHub | Latest |

---

## 15. KEY FILES SUMMARY

| File | Purpose | Lines |
|------|---------|-------|
| models.py | Database models | 718+ |
| views.py | View logic & endpoints | 3387+ |
| urls.py | URL routing | - |
| serializers.py | DRF serializers | - |
| forms.py | Form definitions | - |
| utils.py | Utility functions | - |
| settings.py | Django configuration | - |
| manage.py | Django CLI | - |

---

## 16. PERFORMANCE OPTIMIZATIONS

### Database
- Use `select_related()` for ForeignKey
- Use `prefetch_related()` for M2M
- Add indexes on frequently queried fields
- Cache user profiles with Redis
- Use database query pagination

### Frontend
- Lazy load images
- Minify CSS/JavaScript
- Use CDN for static files
- Implement infinite scroll for feeds
- Cache AJAX responses

### API
- Return only needed fields in serializers
- Implement pagination (10-20 items/page)
- Use HTTP caching headers
- Compress responses (gzip)

---

## 17. NEXT STEPS & IMPROVEMENTS

### Short-term
1. Fix remaining bugs (comments, notifications)
2. Optimize database queries
3. Improve mobile responsiveness
4. Add comprehensive error handling

### Medium-term
1. Implement WebSocket for real-time updates
2. Add project analytics dashboard
3. Implement recommendation engine
4. Add video/screen sharing
5. Build mobile app

### Long-term
1. AI-powered skill matching
2. Project marketplace
3. Payment integration
4. Global collaboration features
5. Mobile apps (iOS/Android)

---

## CONCLUSION

UniSync is a comprehensive Django-based collaboration platform with:
- **Core Features**: User authentication, project management, messaging, notifications
- **Advanced Features**: Profile matching, team management, activity tracking
- **Scalable Architecture**: REST API, modular design, database-driven
- **Production-Ready**: Configured for deployment on Render/Railway

The codebase is well-structured with clear separation of concerns, making it easy to maintain and extend.

---

*Last Updated: February 6, 2026*
*Repository: https://github.com/Goku0090/uni*
