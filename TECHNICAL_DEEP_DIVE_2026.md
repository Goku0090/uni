# Technical Deep Dive - UniSinq Platform 2026

## System Architecture Diagram

```
┌─────────────────────────────────────────────────────────────────┐
│                        USER BROWSER                             │
│  React App (Vite)  │  WebSocket Client                         │
└──────────────────────────────────────────────────────────────────┘
                            ↓↑
        ┌──────────────────────────────────────────┐
        │     FRONTEND: React + Vite               │
        │  ├── Components (Pages, Cards, Forms)   │
        │  ├── API Client (HTTP + WebSocket)      │
        │  └── State Management                   │
        └──────────────────────────────────────────┘
                            ↓↑
        ┌──────────────────────────────────────────┐
        │         REST API & WebSocket Layer       │
        │  Port 8000 (HTTP) | Port 8000 (WS)      │
        └──────────────────────────────────────────┘
                            ↓↑
        ┌──────────────────────────────────────────┐
        │  Django + Django Channels (ASGI/Daphne) │
        │                                          │
        │  ├── Views & ViewSets (DRF)             │
        │  ├── WebSocket Consumers                │
        │  ├── Middleware (CORS, CSRF, Auth)      │
        │  ├── Models (ORM)                       │
        │  └── Signals & Events                   │
        └──────────────────────────────────────────┘
                            ↓↑
        ┌──────────────────────────────────────────┐
        │      BUSINESS LOGIC LAYER                │
        │  ├── Authentication (Auth Service)      │
        │  ├── Email (Brevo Backend)              │
        │  ├── Chat & Comments API                │
        │  ├── Real-time Broadcasting             │
        │  └── Utility Functions                  │
        └──────────────────────────────────────────┘
                            ↓↑
        ┌──────────────────────────────────────────┐
        │      DATABASE LAYER                      │
        │  PostgreSQL (Production)                 │
        │  SQLite (Development)                    │
        │                                          │
        │  Tables:                                 │
        │  ├── Users & Profiles                   │
        │  ├── Projects & Collaborations          │
        │  ├── Comments & Messages                │
        │  ├── Activities & Notifications         │
        │  ├── Templates & Ratings                │
        │  └── Logs & Events                      │
        └──────────────────────────────────────────┘
```

---

## Core Module Dependencies

### Backend Dependencies Graph

```
Django Core
├── Channels (WebSocket)
├── REST Framework (API)
├── Allauth (Authentication)
│   ├── Google OAuth
│   └── GitHub OAuth
├── CORS Headers
└── Database
    ├── PostgreSQL (Production)
    └── SQLite (Development)

Accounts App
├── Models (ORM)
├── Views (HTTP Handlers)
├── Consumers (WebSocket)
├── Serializers (API)
├── Forms (Validation)
├── Signals (Event Broadcasting)
└── Services
    ├── Auth Service
    ├── Email Backend (Brevo)
    └── Chat/Comment APIs
```

---

## Request Flow Examples

### 1. User Login with Email/Password

```
Frontend (login form)
         ↓
POST /auth/login/ 
    ├─ Email validation
    ├─ Password check
    └─ Session creation
         ↓
Backend (views.py)
    ├─ Authenticate user
    ├─ Create session
    └─ Return session token + CSRF token
         ↓
Frontend
    ├─ Store session in cookies
    ├─ Store CSRF token
    └─ Redirect to /dashboard/
         ↓
Display user dashboard with personalized content
```

### 2. Create Project with Comment

```
Frontend (project form)
         ↓
POST /api/projects/
    ├─ Project data
    └─ Authorization check
         ↓
Backend (views.py)
    ├─ Validate input (serializer)
    ├─ Create Project instance
    ├─ Save to database
    └─ Trigger signals
         ↓
Signal Handler (signals_realtime.py)
    ├─ Create Activity record
    ├─ Broadcast notification
    └─ Update activity feed cache
         ↓
WebSocket (consumers.py)
    ├─ Send to connected clients
    └─ Update in real-time
         ↓
Frontend (via WebSocket)
    ├─ Update project list
    ├─ Show in activity feed
    └─ Update notification badge
```

### 3. Post Comment with Real-time Update

```
Frontend (comment form)
         ↓
POST /api/comments/
    ├─ Comment data (project_id, content, author)
    └─ CSRF token validation
         ↓
Backend (comment_api.py)
    ├─ Create Comment instance
    ├─ Save to database
    └─ Trigger django.db.models.signals
         ↓
Signal Handler (signals_realtime.py)
    ├─ Create Activity: "commented"
    ├─ Create Notification for project collaborators
    └─ Send WebSocket message
         ↓
WebSocket Consumer (consumers.py)
    ├─ Serialize comment data
    ├─ Broadcast to project channel
    ├─ Send to all connected clients in that group
    └─ Update comment count badge
         ↓
Frontend (WebSocket listener)
    ├─ Receive comment data
    ├─ Update comments list
    ├─ Increment badge count
    └─ Show notification toast
```

### 4. Send Message (Chat)

```
Frontend (message input)
         ↓
POST /api/messages/
    ├─ Message content
    ├─ Recipient/Conversation
    └─ CSRF + Auth headers
         ↓
Backend (chat_api.py)
    ├─ Validate conversation access
    ├─ Create Message instance
    ├─ Set read_status = False
    └─ Save to database
         ↓
Signal Handler (signals_realtime.py)
    ├─ Update conversation timestamp
    ├─ Create notification for recipient
    └─ Trigger WebSocket broadcast
         ↓
WebSocket (consumers.py)
    ├─ Send message to receiver's group
    ├─ Update conversation preview
    ├─ Increment unread badge
    └─ Play notification sound (optional)
         ↓
Receiver Frontend (WebSocket listener)
    ├─ Display new message
    ├─ Show notification
    └─ Mark as read when viewed
         ↓
PUT /api/messages/{id}/read/
    └─ Update read_status in database
```

---

## Database Relationships

### User Relationships
```
User
├─ Profile (OneToOne) - Avatar, bio, skills
├─ Projects (ForeignKey) - Created projects
├─ Comments (ForeignKey) - Posted comments
├─ Messages (ForeignKey) - Sent messages
├─ Conversations (ManyToMany) - Participant in
├─ Activities (ForeignKey) - User activities
├─ Notifications (ForeignKey) - User notifications
├─ Collaborations (ManyToMany) - Team memberships
└─ Skills (ManyToMany) - User expertise
```

### Project Relationships
```
Project
├─ Owner (ForeignKey → User)
├─ Collaborators (ManyToMany → User)
├─ Comments (ForeignKey ← Comment)
├─ Activities (ForeignKey ← Activity)
├─ Templates (ForeignKey ← ProjectTemplate)
├─ Tags (ManyToMany)
└─ Skills Required (ManyToMany)
```

### Comment Relationships
```
Comment
├─ Project (ForeignKey → Project)
├─ Author (ForeignKey → User)
├─ Parent Comment (ForeignKey, nullable) - For nested replies
├─ Created timestamp
└─ Updated timestamp
```

### Message Relationships
```
Message
├─ Conversation (ForeignKey → Conversation)
├─ Sender (ForeignKey → User)
├─ Content (TextField)
├─ Read Status (Boolean)
├─ Timestamp
└─ Attachments (Optional)
```

---

## Authentication Mechanisms

### 1. Session-Based (Traditional)
```python
# Settings
AUTHENTICATION_BACKENDS = [
    'django.contrib.auth.backends.ModelBackend',  # Default
    'allauth.account.auth_backends.AuthenticationBackend',
]

# Flow
Login → Authenticate → Create Session → Set Cookie
```

### 2. OTP-Based (Email Verification)
```python
# Flow
1. User enters email
2. System generates 6-digit OTP
3. Brevo sends OTP via email
4. User enters OTP
5. Account verified
6. Session created
```

### 3. OAuth (Social Login)
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

# Flow
1. Frontend redirects to provider
2. User authorizes app
3. Provider sends code to callback URL
4. Backend exchanges code for access token
5. Backend fetches user profile
6. Create or update local user
7. Create session
```

---

## Real-time Communication Architecture

### WebSocket Flow Diagram

```
Client 1                     Server                      Client 2
(Browser)                  (Daphne/ASGI)                (Browser)
   │                           │                           │
   │─── WebSocket Connect ─────→│                           │
   │                           │                           │
   │                      [Create Consumer]                │
   │                      [Add to Channel Group]           │
   │                           │                           │
   │                                                        │
   │                    (Both connected)                    │
   │                                                        │
   │─── Send Message ──────────→│                           │
   │                           │─── Broadcast to Group ───→│
   │                           │                      [Receive]
   │                           │                           │
   │                    (Post to database)                 │
   │                           │                           │
   │← ─ Real-time Update ──────│← ─ ACK Message ─────────│
   │                           │                           │
   │─── Receive in React ─────→│                           │
   │  [Update State]           │                           │
   │  [Re-render UI]           │                           │
   │                           │                           │
```

### Channel Groups (Django Channels)

```
Channel Groups:
├── chat_{conversation_id}
│   └── All users in conversation
├── project_{project_id}
│   └── All users viewing project
├── notifications_{user_id}
│   └── User-specific notifications
└── activity_feed
    └── All logged-in users
```

### Consumer Structure (consumers.py)

```python
class ChatConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        # Join channel group
        # Add to database
        # Send notification
    
    async def disconnect(self, close_code):
        # Remove from channel group
        # Update user status
    
    async def receive(self, text_data):
        # Parse message
        # Save to database
        # Broadcast to group
    
    async def message_broadcast(self, event):
        # Send to WebSocket
        # Format response
```

---

## Email System Architecture

### Email Backend Selection Logic

```
System Initialization
├─ Check BREVO_API_KEY
│  └─ YES → Use BrevoMailBackend ✓
├─ Check EMAIL_HOST_USER & PASSWORD
│  └─ YES → Use Django SMTP (Gmail) ✓
└─ DEFAULT → Use ConsoleEmailBackend
   └─ Print to console (development)
```

### Email Sending Flow

```
send_mail() called
    ↓
Select Backend
    ↓
Brevo Backend
├─ Build request to Brevo API
├─ HTTP POST /v3/smtp/email
├─ Handle response
└─ Return status
    ↓
Fallback Chain
├─ If Brevo fails → Try Gmail SMTP
├─ If SMTP fails → Print to console
└─ Log error
```

### OTP Email Example

```python
# OTP Generation
otp = generate_random.randint(100000, 999999)
user.otp = otp
user.otp_created = now()
user.save()

# Send Email
send_mail(
    subject="Your UniSinq OTP",
    message=f"Your OTP is: {otp}",
    from_email="noreply@unisinq.app",
    recipient_list=[user.email],
    fail_silently=False,
)

# Verification
if user.otp == submitted_otp and not otp_expired(user.otp_created):
    user.email_verified = True
    user.save()
    create_session(user)
```

---

## API Response Structure

### Success Response

```json
{
    "status": "success",
    "data": {
        "id": 1,
        "name": "My Project",
        "description": "...",
        "created_at": "2026-02-16T10:30:00Z"
    },
    "message": "Project created successfully"
}
```

### Error Response

```json
{
    "status": "error",
    "errors": {
        "field_name": ["Error message"]
    },
    "message": "Validation failed"
}
```

### Paginated Response

```json
{
    "count": 100,
    "next": "http://api.example.com/projects/?page=2",
    "previous": null,
    "results": [...]
}
```

---

## Security Mechanisms

### CSRF Protection

```
Request Flow:
1. GET /form/ → Django returns HTML with CSRF token
2. Token embedded in form or header
3. POST /form/ → Include CSRF token
4. Middleware validates token
5. Accept/reject request
```

### CORS Configuration

```python
CORS_ALLOWED_ORIGINS = [
    "http://localhost:3000",  # Dev
    "https://yourdomain.com",  # Prod
]
CORS_ALLOW_CREDENTIALS = True  # Allow cookies
```

### Password Security

```python
AUTH_PASSWORD_VALIDATORS = [
    # Min 8 chars
    # Not too similar to username
    # Not in common passwords list
    # Not all numeric
]

# Password hashing
from django.contrib.auth.hashers import make_password
hashed = make_password(plain_text_password)
```

---

## Deployment & Scaling

### Local Development
```bash
# Backend
python manage.py runserver

# Frontend (Vite)
npm run dev

# WebSocket (Daphne)
daphne -b 0.0.0.0 -p 8000 auth_project.asgi:application
```

### Production (Render/Railway)
```
Container: Python 3.11+
Runtime: Gunicorn + Daphne
Database: PostgreSQL
Static Files: Whitenoise
Email: Brevo API
```

### Docker Deployment
```dockerfile
# Backend
FROM python:3.11
WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY . .
CMD ["daphne", "-b", "0.0.0.0", "auth_project.asgi:application"]

# Frontend
FROM node:18
WORKDIR /app
COPY package.json .
RUN npm install
COPY . .
RUN npm run build
CMD ["serve", "-s", "dist"]
```

---

## Performance Optimization

### Database Optimization
```python
# Select related (FK relationships)
projects = Project.objects.select_related('owner')

# Prefetch related (M2M)
projects = Project.objects.prefetch_related('comments', 'collaborators')

# Only specific fields
projects = Project.objects.only('id', 'title', 'owner_id')

# Pagination
from rest_framework.pagination import PageNumberPagination
class StandardResultsSetPagination(PageNumberPagination):
    page_size = 10
    page_size_query_param = 'page_size'
    max_page_size = 100
```

### Caching Strategy
```python
# Cache view results
from django.views.decorators.cache import cache_page

@cache_page(60 * 15)  # 15 minutes
def get_projects(request):
    return projects

# Cache template fragments
{% cache 300 project_list %}
    ...template content...
{% endcache %}
```

### Frontend Optimization
```javascript
// Code splitting with Vite
const ProjectDetail = lazy(() => import('./pages/ProjectDetail'));

// Image optimization
<img src={imageUrl} alt="Project" loading="lazy" />

// Memoization
const ProjectCard = React.memo(({ project }) => {
    return <div>...</div>;
});
```

---

## Testing Strategy

### Backend Unit Tests
```python
# test_models.py
class UserTestCase(TestCase):
    def setUp(self):
        self.user = User.objects.create(username='testuser')
    
    def test_user_creation(self):
        self.assertTrue(self.user.pk)

# test_views.py
class ProjectViewTestCase(APITestCase):
    def test_create_project(self):
        response = self.client.post('/api/projects/', {...})
        self.assertEqual(response.status_code, 201)
```

### Integration Tests
```python
# Test full authentication flow
# Test comment creation → notification → WebSocket broadcast
# Test message sending → database → real-time delivery
```

### Frontend Tests
```javascript
// Component tests with React Testing Library
test('renders project card', () => {
    render(<ProjectCard project={mockProject} />);
    expect(screen.getByText('Project Name')).toBeInTheDocument();
});
```

---

## Monitoring & Logging

### Backend Logging
```python
# Configure in settings.py
LOGGING = {
    'version': 1,
    'handlers': {
        'file': {
            'class': 'logging.handlers.RotatingFileHandler',
            'filename': 'logs/django.log',
            'maxBytes': 10485760,  # 10MB
        },
    },
    'loggers': {
        'accounts': {
            'handlers': ['file'],
            'level': 'INFO',
        },
    },
}

# Usage
import logging
logger = logging.getLogger('accounts')
logger.info("Project created: %s", project.id)
logger.error("OTP failed: %s", error)
```

### Performance Monitoring
```python
# Measure execution time
import time
start = time.time()
# ... code ...
duration = time.time() - start
logger.info(f"Request took {duration:.2f}s")
```

---

## Troubleshooting Guide

### WebSocket Connection Issues
```
Problem: WebSocket connection refused
Solution:
1. Check Daphne is running on port 8000
2. Verify ASGI configuration
3. Check firewall/proxy settings
4. Enable debug logging

Problem: Messages not delivering in real-time
Solution:
1. Check channel layer configuration
2. Verify consumer is connected
3. Check database write is successful
4. Review server logs for errors
```

### Database Issues
```
Problem: "too many connections"
Solution:
1. Check CONN_MAX_AGE in settings
2. Reduce connection pool size
3. Kill idle connections
4. Monitor active connections

Problem: Slow queries
Solution:
1. Add database indexes
2. Use select_related/prefetch_related
3. Reduce query count (N+1)
4. Cache frequently accessed data
```

### Email Not Sending
```
Problem: OTP emails not received
Solution:
1. Verify BREVO_API_KEY is set
2. Check from_email is verified in Brevo
3. Review Brevo sending quota
4. Check spam folder
5. Review Django logs for errors
```

---

**Document Version**: 2026-02-16
**Framework Versions**: Django 4.x, React 18+, Channels 4.x
**Database**: PostgreSQL 12+
