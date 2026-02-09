# Complete Codebase Analysis - UniSinQ Platform 2026

## 📋 Executive Summary

**UniSinQ** is a collaborative social networking platform built with Django, designed for students to connect, collaborate on projects, and manage team-based development work. The application integrates real-time messaging, OTP authentication, OAuth social logins, and comprehensive project management features.

**Technology Stack:**
- Backend: Django 4.x + Django REST Framework
- Frontend: Bootstrap 5, jQuery, Vanilla JavaScript
- Real-time: Django Channels (WebSocket)
- Database: PostgreSQL (production), SQLite (development)
- Authentication: Django Allauth (Google, GitHub OAuth)
- Email: Brevo/ZeptoMail API backends
- Deployment: Render.com

---

## 🏗️ Architecture Overview

```
UniSinQ Platform
├── Frontend Layer (HTML/CSS/JS)
├── Django Application Layer (Views/URLs)
├── Core Business Logic (Models/Services)
├── External Integrations (OAuth, Email, WebSocket)
└── Database Layer (PostgreSQL)
```

---

## 📁 Project Structure

```
auth_project/
├── auth_project/                    # Project configuration
│   ├── settings.py                  # Django settings, Email backends, OAuth config
│   ├── urls.py                      # Root URL routing
│   ├── asgi.py                      # Async server gateway interface
│   ├── wsgi.py                      # Web server gateway interface
│   └── routing.py                   # WebSocket routing
│
├── accounts/                        # Main application
│   ├── models.py                    # Database models (830+ lines)
│   ├── views.py                     # Main views (1000+ lines)
│   ├── views_contact.py             # Contact & policy views
│   ├── urls.py                      # App URL routing
│   ├── serializers.py               # DRF serializers
│   ├── permissions.py               # Custom permissions
│   ├── forms.py                     # Django forms
│   ├── consumers.py                 # WebSocket consumers
│   ├── routing.py                   # WebSocket routing
│   ├── signals_realtime.py          # Django signals
│   │
│   ├── APIs/
│   │   ├── chat_api.py              # Messaging REST API
│   │   ├── chat_api_improved.py     # Enhanced messaging
│   │   ├── comment_api.py           # Comments/live feed
│   │   └── template_api.py          # Project templates
│   │
│   ├── Email Backends/
│   │   ├── brevo_mail_backend.py    # Brevo email service
│   │   └── zepto_mail_backend.py    # ZeptoMail service
│   │
│   ├── templates/                   # HTML templates
│   │   ├── base.html                # Master template
│   │   ├── main_home.html           # Dashboard/feed
│   │   ├── project_detail.html      # Project view
│   │   ├── messages.html            # Messaging interface
│   │   ├── login.html               # Authentication
│   │   ├── profile.html             # User profile
│   │   └── ...                      # 20+ more templates
│   │
│   ├── static/                      # Static files
│   │   ├── js/
│   │   │   ├── comments-handler.js  # Comment functionality
│   │   │   ├── messages-api.js      # Messaging logic
│   │   │   ├── realtime-updates.js  # WebSocket handling
│   │   │   └── login.js             # Authentication logic
│   │   └── css/
│   │       └── styles.css           # Custom styling
│   │
│   ├── migrations/                  # Database migrations
│   ├── management/                  # Django management commands
│   ├── services/                    # Business logic services
│   └── templatetags/                # Custom template filters
│
├── manage.py                        # Django management interface
├── db.sqlite3                       # Development database
├── requirements.txt                 # Python dependencies
├── Procfile                         # Render deployment config
└── render.yaml                      # Render deployment spec
```

---

## 🗄️ Database Models (Core Data Structures)

### **1. User & Authentication Models**

#### `StudentProfile` (Extended User Data)
```python
- OneToOne link to Django User
- Profile metadata: full_name, college, location, bio
- Skills and interests (JSONField arrays)
- Social links: GitHub, LinkedIn, Portfolio, Behance
- Profile photo (image upload)
- Timestamps: created_at, updated_at
```

#### `OTP` (One-Time Password)
```python
- Email-based authentication
- 6-digit code generation
- 5-minute expiry
- Purpose: login, registration, reset
- Verification and validation methods
- Auto-expiring unused codes
```

#### `Connection` (Networking Requests)
```python
- User-to-user connection requests
- Status: pending, accepted, rejected
- Timestamps for tracking
- Unique constraint: one connection per sender-receiver pair
```

### **2. Project & Collaboration Models**

#### `Project` (Core Project Entity)
```python
- Owner (ForeignKey to User)
- Title, description, category
- Technologies and required roles
- Status: draft, active, completed, archived
- Visibility: public, private, invite-only
- Team size limits
- Timestamps and modification tracking
```

#### `ProjectMember` (Team Composition)
```python
- Project reference
- User reference
- Role: owner, lead, contributor, reviewer
- Join/leave timestamps
- Active status tracking
```

#### `ProjectInvitation` (Team Invitations)
```python
- Links project, invited_user, and inviter
- Role assignment on invitation
- Status: pending, accepted, declined, expired
- Message and expiry date support
```

#### `ProjectTask` (Task Management)
```python
- Assigned to project members
- Status: todo, in_progress, review, completed, cancelled
- Priority: low, medium, high, urgent
- Due dates and completion tracking
```

#### `ProjectMilestone` (Project Checkpoints)
```python
- Major project milestones
- Completion tracking with timestamps
- Linked to specific user completions
```

### **3. Messaging & Communication Models**

#### `Message` (Direct & Group Messages)
```python
- Sender and optional receiver (for direct messages)
- Chat room reference (for group messages)
- Content and message type
- Call type (voice/video) support
- Reply threading support
- Created/updated timestamps
```

#### `ChatRoom` (Conversation Containers)
```python
- Chat type: direct, group
- Name and description
- Member list (ManyToMany)
- Last message reference
- Timestamps
```

#### `ChatRoomMember` (Room Participation)
```python
- User and chat room relationship
- Joined/left timestamps
- Member type: creator, member, moderator
- Last read message for notification tracking
```

#### `MessageReadStatus` (Scalable Read Tracking)
```python
- Message and user relationship
- Read timestamp
- Unique constraint to prevent duplicates
```

#### `MessageReaction` (Message Reactions)
```python
- Message, user, and reaction emoji
- Creation timestamp
- Unique constraint per user per reaction per message
```

### **4. Content Models**

#### `Comment` (Live Feed Comments)
```python
- Project reference
- Author (user who commented)
- Content and timestamps
- Comment nesting support (parent_comment)
- Editing and deletion tracking
```

#### `ProjectTemplate` (Project Blueprints)
```python
- Pre-configured project templates
- Categories: web, mobile, AI/ML, data, blockchain, IoT, games
- Template metadata: name, description, icon
- Suggested technologies and roles
- Difficulty level and team size
- Learning resources and example projects
- Rating system with usage tracking
```

#### `TemplateRating` (User Feedback)
```python
- User ratings (1-5 stars)
- Review comments
- Helpful count tracking
```

### **5. Notification & Activity Models**

#### `Notification`
```python
- Recipient user
- Notification type
- Actor and related object references
- Read/unread status
- Timestamps
```

#### `ActivityFeed`
```python
- Activity tracking for users
- Action types
- Related object references
- Timestamps for chronological ordering
```

---

## 🔌 REST API Endpoints

### **Authentication & User Management**
| Endpoint | Method | Purpose |
|----------|--------|---------|
| `/login/` | POST | User login |
| `/register/` | POST | User registration |
| `/verify-otp/<purpose>/` | POST | OTP verification |
| `/forgot-password/` | POST | Password reset request |
| `/reset-password/` | POST | Complete password reset |

### **Profile Management**
| Endpoint | Method | Purpose |
|----------|--------|---------|
| `/student-profile/` | GET/POST | Profile data |
| `/user/<username>/` | GET | User profile view |
| `/user-profile/<user_id>/` | GET | Profile API |
| `/check-username/` | POST | Username availability |
| `/check-email/` | POST | Email availability |

### **Project Management**
| Endpoint | Method | Purpose |
|----------|--------|---------|
| `/post-project/` | POST | Create project |
| `/project-detail/<id>/` | GET | Project details |
| `/like-project/<id>/` | POST | Like project |
| `/edit-project/<id>/` | POST | Update project |
| `/delete-project/<id>/` | DELETE | Remove project |

### **Messaging APIs**
| Endpoint | Method | Purpose |
|----------|--------|---------|
| `/chat-rooms/` | GET/POST | List/create chat rooms |
| `/chat-rooms/<id>/` | GET | Room details |
| `/messages/` | GET/POST | Message list/create |
| `/messages/<id>/` | GET | Single message |
| `/direct-message/` | POST | Direct message |
| `/conversations/` | GET | Conversation list |

### **Comment & Social**
| Endpoint | Method | Purpose |
|----------|--------|---------|
| `/projects/<id>/comments/` | GET | Get comments |
| `/projects/<id>/comments/add/` | POST | Add comment |
| `/comments/<id>/edit/` | POST | Edit comment |
| `/comments/<id>/delete/` | DELETE | Delete comment |

### **Connections**
| Endpoint | Method | Purpose |
|----------|--------|---------|
| `/send-connection/<user_id>/` | POST | Request connection |
| `/accept-connection/<conn_id>/` | POST | Accept request |
| `/reject-connection/<conn_id>/` | POST | Reject request |
| `/my-connections/` | GET | User's connections |

---

## 🎨 Frontend Components & Templates

### **Key Templates**

#### `base.html` - Master Template
- Global navigation bar with logo
- User authentication state checks
- Bootstrap framework integration
- Static file loading
- Message display framework
- Footer with links

#### `main_home.html` - Dashboard/Feed
- Project feed with real-time updates
- Comment section for each project
- Like/share buttons
- Notification badge
- WebSocket integration for live updates
- Pagination for project feed

#### `project_detail.html` - Project Page
- Full project information
- Team member list
- Task list and milestones
- Comments thread
- Join/contribute buttons
- Edit controls for owner

#### `messages.html` - Messaging Interface
- Chat room list
- Message thread display
- Real-time message delivery
- Typing indicators
- Read status indicators
- File attachment preview

#### `profile.html` - User Profile
- User information display
- Skills and interests
- Social links
- Project history
- Connection options
- Profile editing

#### `login.html` / `register.html`
- OTP-based authentication
- Email verification
- Social OAuth buttons (Google, GitHub)
- Form validation
- Error messaging

### **Key JavaScript Files**

#### `comments-handler.js`
```javascript
- Load comments via AJAX
- Post new comments
- Edit/delete comments
- Real-time comment updates
- Error handling
```

#### `messages-api.js`
```javascript
- Send/receive messages
- Chat room operations
- Message reactions
- Read status tracking
- Typing indicators
```

#### `realtime-updates.js`
```javascript
- WebSocket connection management
- Real-time feed updates
- Notification handling
- Connection status indicator
- Auto-reconnection logic
```

#### `login.js`
```javascript
- Form validation
- OTP input handling
- Email verification
- Password reset flow
```

---

## 🔐 Authentication & Security

### **Authentication Methods**
1. **Email + OTP** (Primary)
   - 6-digit code sent via email
   - 5-minute expiry
   - Auto-deactivation after use

2. **Social OAuth**
   - Google OAuth 2.0
   - GitHub OAuth 2.0
   - Auto-signup after first login

3. **Traditional Login**
   - Username/password
   - Fallback method

### **Security Features**
- CSRF token protection
- Session authentication
- Secure password hashing (Django defaults)
- Email verification via OTP
- OAuth token management via Allauth
- SQL injection protection (ORM)

### **Configuration**
```python
AUTHENTICATION_BACKENDS = [
    'django.contrib.auth.backends.ModelBackend',
    'allauth.account.auth_backends.AuthenticationBackend',
]

INSTALLED_APPS = [
    'allauth',
    'allauth.account',
    'allauth.socialaccount',
    'allauth.socialaccount.providers.google',
    'allauth.socialaccount.providers.github',
]
```

---

## 📧 Email Service Architecture

### **Multi-Backend Support** (Priority-based fallback)

1. **Brevo** (Primary - Production)
   ```python
   - API-based transactional emails
   - BREVO_API_KEY environment variable
   - Backend: accounts.brevo_mail_backend.BrevoMailBackend
   ```

2. **ZeptoMail** (Alternative)
   ```python
   - API-based email service
   - ZEPTO_MAIL_API_KEY & ZEPTO_MAIL_TOKEN
   - Backend: accounts.zepto_mail_backend.ZeptoMailBackend
   ```

3. **Gmail SMTP** (Fallback)
   ```python
   - Traditional SMTP
   - EMAIL_HOST: smtp.gmail.com:587
   - Requires app password
   ```

4. **Console** (Development)
   ```python
   - Prints emails to console
   - Used when no API keys configured
   ```

### **Email Use Cases**
- OTP delivery for login/registration
- Password reset links
- Notification alerts
- Team invitations
- Project updates

---

## 🔄 Real-Time Features (WebSocket)

### **WebSocket Architecture**
- **Technology**: Django Channels
- **Backend**: In-memory channel layer (development)
- **Protocol**: WebSocket (ws://)

### **Consumers** (`consumers.py`)
- Message delivery consumer
- Chat room consumer
- Notification consumer
- Live feed updates consumer

### **Broadcasting**
```python
- Channel groups for chat rooms
- User-specific notification channels
- Project feed channels
```

### **Client Integration** (`realtime-updates.js`)
```javascript
- Connect to WebSocket on page load
- Listen for message events
- Update DOM in real-time
- Handle connection loss with auto-reconnect
- Display connection status
```

---

## 📦 Key Utility Functions & Services

### **Services Directory** (`services/`)
- Email sending utilities
- Notification creation
- Project filtering and search
- User matching algorithm
- Team management helpers

### **Common Utilities** (`utils.py`)
- OTP generation and verification
- File handling utilities
- Date/time helpers
- Notification helpers
- JSON serialization

### **Template Tags** (`templatetags/`)
- Custom filters for formatting
- Template functions for business logic

---

## 🔌 External Integrations

### **RapidAPI - University Search**
```python
API_HOST = 'universities-list.p.rapidapi.com'
RAPIDAPI_KEY = os.getenv('RAPIDAPI_KEY')
- College name validation
- Suggestions during signup
```

### **OAuth Providers**
```python
GOOGLE:
  - Scope: profile, email
  - Client ID from Google Cloud Console
  
GITHUB:
  - Scope: user:email, read:user
  - Client ID from GitHub OAuth App
```

---

## 🚀 Deployment Configuration

### **Render.com Deployment**
- **Procfile**: Defines how to start the app
- **render.yaml**: Service configuration
- **DATABASE_URL**: PostgreSQL connection string
- **Environment Variables**:
  - SECRET_KEY
  - DEBUG=False
  - ALLOWED_HOSTS
  - Email API keys
  - OAuth credentials

### **Static Files**
```
STATIC_URL = '/static/'
STATICFILES_DIRS = [BASE_DIR / 'static']
STATIC_ROOT = BASE_DIR / 'staticfiles'
```

### **Media Files**
```
MEDIA_URL = '/media/'
MEDIA_ROOT = BASE_DIR / 'media'
```

---

## 📊 Data Flow Examples

### **User Login Flow**
```
User Input → validate_email() → OTP.generate() → Email Service
→ OTP saved in DB → User receives email → User enters code
→ verify_otp() → User authenticated → Session created → Redirect
```

### **Project Posting Flow**
```
User fills form → POST /post-project/
→ Form validation → Create Project model → Create initial ProjectMember
→ Signal fired (project_created) → Notification sent to followers
→ Activity logged → Response returned
```

### **Real-Time Comment Flow**
```
User types comment → AJAX POST /add-comment/
→ Comment saved to DB → Signal fires → WebSocket broadcast to room
→ JavaScript receives message → DOM updated
→ All connected users see new comment instantly
```

### **Messaging Flow**
```
User sends message → POST /direct-message/
→ Message saved to DB → Signal fires → WebSocket emit to recipients
→ Message marked as sent → Recipient connects → Message delivered
→ Recipient reads → MessageReadStatus created → Sender sees "read"
```

---

## 🔍 Key Features Implementation

### **1. Project Filtering**
- By category, technology, team size
- Search across title and description
- Visibility filtering (public/private)
- Status-based filtering

### **2. Team Management**
- Add members via invitation
- Role-based access control
- Remove members
- Accept/decline invitations
- Task assignment within projects

### **3. Notifications**
- Connection requests
- Project invitations
- Comments on projects
- Team updates
- System notifications

### **4. Activity Feed**
- User connections
- Projects posted
- Team member additions
- Milestones completed
- Comments posted

### **5. Comments & Discussion**
- Nested commenting
- Edit/delete capability
- Real-time updates
- User mentions (preparation)

---

## 🛠️ Development Setup

### **Requirements**
```
Django>=4.2
djangorestframework>=3.14
django-allauth>=0.52
django-cors-headers>=4.0
channels>=4.0
psycopg2-binary>=2.9
dj-database-url>=1.2
python-dotenv>=0.21
```

### **Environment Variables** (`.env`)
```
DEBUG=True
SECRET_KEY=your-secret-key
DATABASE_URL=postgresql://user:pass@localhost/dbname
ALLOWED_HOSTS=localhost,127.0.0.1

BREVO_API_KEY=your-brevo-key
GOOGLE_CLIENT_ID=your-google-id
GOOGLE_CLIENT_SECRET=your-google-secret
GITHUB_CLIENT_ID=your-github-id
GITHUB_CLIENT_SECRET=your-github-secret
RAPIDAPI_KEY=your-rapidapi-key
```

### **Running Locally**
```bash
# Install dependencies
pip install -r requirements.txt

# Create database
python manage.py migrate

# Create superuser
python manage.py createsuperuser

# Collect static files
python manage.py collectstatic --noinput

# Run development server
python manage.py runserver

# Run WebSocket server (separate terminal)
daphne -b 0.0.0.0 -p 8001 auth_project.asgi:application
```

---

## 📈 Performance Considerations

### **Database Optimizations**
- Use `select_related()` for ForeignKey queries
- Use `prefetch_related()` for ManyToMany
- Index frequently queried fields
- Pagination for large datasets

### **Caching Strategy**
- Cache user profile data
- Cache project templates
- Cache notification counts
- Cache computed values

### **Frontend Performance**
- Lazy load images
- Compress JavaScript/CSS
- Minify static assets
- Use CDN for static files

---

## 🧪 Testing Infrastructure

### **Test Files**
Located in `accounts/` directory:
- `test_email.py` - Email backend tests
- `test_comments_api.py` - Comment API tests
- `test_login.py` - Authentication tests
- `test_profile_view.py` - Profile view tests

### **Running Tests**
```bash
python manage.py test accounts
python manage.py test accounts.tests.TestClassName
```

---

## 📝 Important Notes & Known Patterns

### **Model Relationships**
- Users have one StudentProfile (OneToOne)
- Projects have many ProjectMembers (OneToMany)
- Messages can be direct (User-to-User) or in ChatRoom (Many-to-Many)
- Comments are tied to Projects

### **Signal Handling** (`signals_realtime.py`)
- Auto-create StudentProfile on user creation
- Broadcast events on model changes
- Handle real-time notifications

### **Permission Classes** (`permissions.py`)
- IsOwner: Can only modify own content
- IsProjectMember: Can only access project they're member of
- IsAdmin: For admin-specific endpoints

### **Template Tags**
- Custom template filters for formatting
- Conditional logic in templates
- Reusable component rendering

---

## 🎯 Current Status & Next Steps

### **Completed Features**
✅ User authentication (OTP + OAuth)
✅ Project management (CRUD)
✅ Team collaboration
✅ Real-time messaging
✅ WebSocket integration
✅ Comment system
✅ Notification system
✅ Activity feed
✅ User profiles
✅ Email integration

### **Areas for Enhancement**
- Advanced search/filtering
- Analytics dashboard
- User recommendations engine
- Video conferencing integration
- File storage optimization
- API rate limiting
- Enhanced security (2FA)

---

## 📞 Support & Troubleshooting

### **Common Issues**
1. **WebSocket Connection Failed**: Check ASGI configuration and Channels setup
2. **Email Not Sending**: Verify email backend API keys in .env
3. **OAuth Redirect Error**: Ensure ALLOWED_HOSTS and callback URLs match
4. **Static Files 404**: Run `collectstatic` and check STATIC_ROOT

### **Debug Mode**
- Set `DEBUG=True` in `.env` for detailed error pages
- Check Django logs in `logs/` directory
- Use Django Debug Toolbar for performance profiling
- Monitor WebSocket connections in browser DevTools

---

## 📚 Documentation Index

- Settings Configuration: `auth_project/settings.py`
- Models Documentation: `accounts/models.py` (lines 1-100)
- Views Documentation: `accounts/views.py`
- API Documentation: `accounts/chat_api.py`, `comment_api.py`
- WebSocket Guide: `accounts/consumers.py`, `routing.py`
- Email Backend: `accounts/brevo_mail_backend.py`, `zepto_mail_backend.py`
- Template Guide: `accounts/templates/`

---

**Last Updated**: February 9, 2026
**Platform**: UniSinQ - Student Collaboration Hub
**Repository**: https://github.com/Goku0090/uni
