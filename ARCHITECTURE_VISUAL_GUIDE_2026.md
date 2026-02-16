# UniSync Architecture - Visual Guide 2026

## System Architecture Overview

```
┌─────────────────────────────────────────────────────────────────────┐
│                        CLIENT BROWSER (React)                        │
│  ┌──────────────────────────────────────────────────────────────┐  │
│  │ App.jsx                                                      │  │
│  │ ├─ Router (Navigation)                                       │  │
│  │ ├─ Components (Pages, Cards, Forms)                          │  │
│  │ ├─ State Management (Context/Props)                          │  │
│  │ └─ Styles (CSS/Tailwind)                                     │  │
│  └──────────────────────────────────────────────────────────────┘  │
└─────────────────────────────────────────────────────────────────────┘
                                    ↑
                    ┌───────────────┼───────────────┐
                    │               │               │
                    ↓ HTTP/REST     ↓ WebSocket    (Optional XHR)
┌─────────────────────────────────────────────────────────────────────┐
│                    DJANGO BACKEND (Python)                           │
│  ┌──────────────────────────────────────────────────────────────┐  │
│  │ REST API Layer (DRF)                                         │  │
│  │ ├─ ViewSets & Views                                          │  │
│  │ ├─ Serializers (JSON validation)                             │  │
│  │ ├─ Permissions & Authentication                              │  │
│  │ └─ URL Routing                                               │  │
│  └──────────────────────────────────────────────────────────────┘  │
│  ┌──────────────────────────────────────────────────────────────┐  │
│  │ WebSocket Layer (Django Channels)                            │  │
│  │ ├─ ChatConsumer (messages)                                   │  │
│  │ ├─ ProjectConsumer (updates)                                 │  │
│  │ ├─ NotificationConsumer (alerts)                             │  │
│  │ └─ Routing (asgi.py)                                         │  │
│  └──────────────────────────────────────────────────────────────┘  │
│  ┌──────────────────────────────────────────────────────────────┐  │
│  │ Business Logic Layer                                         │  │
│  │ ├─ Models (User, Project, Message, etc.)                     │  │
│  │ ├─ Django Signals (real-time events)                         │  │
│  │ ├─ Utils (NLP, Filters)                                      │  │
│  │ ├─ Authentication (Allauth, OTP)                             │  │
│  │ └─ Services (business functions)                             │  │
│  └──────────────────────────────────────────────────────────────┘  │
└─────────────────────────────────────────────────────────────────────┘
                                    ↑↓
           ┌────────────────────────┼────────────────────────┐
           │                        │                        │
           ↓                        ↓                        ↓
    ┌─────────────┐        ┌──────────────┐      ┌─────────────────┐
    │ PostgreSQL  │        │ Redis        │      │ File Storage    │
    │ Database    │        │ Cache/Broker │      │ (Media uploads) │
    │             │        │              │      │                 │
    │ ┌─────────┐ │        │ ┌──────────┐ │      │ ┌─────────────┐ │
    │ │ Users   │ │        │ │Sessions  │ │      │ │ Profiles    │ │
    │ ├─────────┤ │        │ ├──────────┤ │      │ │ Projects    │ │
    │ │Projects │ │        │ │Messages  │ │      │ │ Attachments │ │
    │ ├─────────┤ │        │ ├──────────┤ │      │ │ Documents   │ │
    │ │Messages │ │        │ │Cache     │ │      │ └─────────────┘ │
    │ ├─────────┤ │        │ │Data      │ │      └─────────────────┘
    │ │Comments │ │        │ └──────────┘ │
    │ └─────────┘ │        └──────────────┘
    └─────────────┘
```

---

## Request/Response Flow

### 1. REST API Request Flow
```
┌──────────┐
│  Browser │ GET /api/projects/
└────┬─────┘
     │ HTTP GET
     ↓
┌──────────────────────┐
│ Django URLconf       │ Match URL pattern
└──────┬───────────────┘
       │
       ↓
┌──────────────────────┐
│ View/ViewSet         │ Execute logic
└──────┬───────────────┘
       │
       ↓
┌──────────────────────┐
│ Database Query       │ SELECT * FROM projects
└──────┬───────────────┘
       │ Returns QuerySet
       ↓
┌──────────────────────┐
│ Serializer           │ Convert to JSON
└──────┬───────────────┘
       │ JSON string
       ↓
┌──────────────────────┐
│ HTTP Response        │ {"results": [...]}
└──────┬───────────────┘
       │ HTTP 200
       ↓
┌──────────────────────┐
│ Browser/React        │ Parse JSON & render
└──────────────────────┘
```

### 2. WebSocket Connection Flow
```
┌──────────────────┐
│ Browser          │ Connect to /ws/chat/123/
└────┬─────────────┘
     │ WebSocket Upgrade
     ↓
┌──────────────────────┐
│ Django Channels      │ ASGI layer
│ (routing.py)         │ Match route
└──────┬───────────────┘
       │
       ↓
┌──────────────────────┐
│ ChatConsumer         │ accept()
└──────┬───────────────┘
       │ Connected
       ↓
┌──────────────────────┐
│ Load Chat History    │ Query messages
└──────┬───────────────┘
       │ Send past messages
       ↓
┌──────────────────────┐
│ Add to Group         │ group_add()
└──────┬───────────────┘
       │ Now in broadcast group
       ↓
┌──────────────────────┐
│ Receive Loop         │ Wait for messages
└──────────────────────┘
```

### 3. Message Broadcasting Flow
```
┌──────────┐
│ User A   │ Send message
└────┬─────┘
     │ WebSocket message
     ↓
┌──────────────────────┐
│ ChatConsumer.receive │
└──────┬───────────────┘
       │
       ↓
┌──────────────────────────┐
│ Save to database         │ INSERT into Message
└──────┬───────────────────┘
       │
       ↓
┌──────────────────────────┐
│ Django Signal Triggered  │ post_save signal
└──────┬───────────────────┘
       │ (signals_realtime.py)
       ↓
┌──────────────────────────┐
│ Broadcast via Redis      │ group_send()
└──────┬───────────────────┘
       │ Pub/Sub
       ↓
┌──────────────────────────┐
│ All Connected Consumers  │ Receive event
└──────┬───────────────────┘
       │
       ├─→ User A
       ├─→ User B
       └─→ User C
```

---

## Database Schema Relationships

```
                    ┌─────────────┐
                    │    User     │ (Django Auth)
                    ├─────────────┤
                    │ id (pk)     │
                    │ username    │
                    │ email       │
                    │ password    │
                    └────┬────────┘
                         │ 1-to-1
                         ↓
                    ┌──────────────────┐
                    │ StudentProfile   │
                    ├──────────────────┤
                    │ full_name        │
                    │ bio              │
                    │ skills (JSON)    │
                    │ interests (JSON) │
                    │ profile_photo    │
                    └──────────────────┘

        ┌───────────────┬──────────────────────────┬─────────────┐
        │ 1-to-many     │                          │ 1-to-many   │
        ↓               ↓                          ↓
   ┌─────────┐  ┌────────────┐           ┌──────────────┐
   │ Project │  │ Connection │           │ Message      │
   └─────────┘  └────────────┘           └──────────────┘
        │
        │ 1-to-many
        ↓
   ┌──────────────────┐
   │ ProjectTeam      │
   │ → ProjectMember  │
   └──────────────────┘

   ┌────────────┐
   │ ChatRoom   │
   ├────────────┤
   │ name       │
   │ is_group   │
   └─────┬──────┘
         │ many-to-many
         ↓
   ┌──────────────┐
   │ ChatRoomMem  │
   ├──────────────┤
   │ user         │
   │ room         │
   │ joined_at    │
   └──────────────┘
         │
         │ 1-to-many
         ↓
      ┌─────────┐
      │ Message │
      └─────────┘
```

---

## Authentication Flow Diagram

### Email/Password with OTP
```
1. User enters email on login page
   ↓
2. Frontend: POST /api/auth/otp/generate/ {email: "user@example.com"}
   ↓
3. Backend:
   ├─ Generate random 6-digit code
   ├─ Set expiry to 5 minutes
   ├─ Save to OTP model
   └─ Send via Brevo SMTP
   ↓
4. Frontend shows "Enter OTP" form
   ↓
5. User enters OTP code
   ↓
6. Frontend: POST /api/auth/otp/verify/ {email, otp_code}
   ↓
7. Backend:
   ├─ Look up OTP record
   ├─ Verify code & expiry
   ├─ Mark OTP as used
   └─ Create user session / return token
   ↓
8. Frontend stores token in localStorage
   ↓
9. Frontend adds "Authorization: Bearer TOKEN" to API calls
   ↓
10. User authenticated ✓
```

### OAuth2 (Google/GitHub)
```
1. User clicks "Login with Google"
   ↓
2. Frontend redirects to Google OAuth URL
   ↓
3. Google shows login/consent screen
   ↓
4. User authorizes app
   ↓
5. Google redirects to callback URL with authorization code
   ↓
6. Backend (django-allauth):
   ├─ Exchange code for access token
   ├─ Get user info from Google API
   ├─ Look up or create User
   ├─ Update StudentProfile
   └─ Create session
   ↓
7. Frontend receives authenticated session
   ↓
8. User logged in ✓
```

---

## Real-time Updates Architecture

```
┌──────────────┐
│ Data Change  │
│ (e.g., new   │
│  comment)    │
└──────┬───────┘
       │
       ↓
┌─────────────────────────────┐
│ Django Signal               │
│ (post_save, post_delete)    │
└──────┬──────────────────────┘
       │
       ↓
┌──────────────────────────────────────────┐
│ Signal Handler                           │
│ (signals_realtime.py)                    │
│                                          │
│ async_to_sync(channel_layer.group_send) │
└──────┬───────────────────────────────────┘
       │
       ↓
┌──────────────────────────────────────┐
│ Redis Pub/Sub                        │
│ (Message Broker)                     │
└──────┬───────────────────────────────┘
       │ Publish to group
       │
       ├──→ Consumer Instance A
       ├──→ Consumer Instance B
       └──→ Consumer Instance C
       ↓
┌──────────────────────────────────┐
│ WebSocket Send to Client         │
│ (JSON event)                     │
└──────┬───────────────────────────┘
       │
       ↓
┌──────────────────────────────────┐
│ Browser Receives Event           │
└──────┬───────────────────────────┘
       │
       ↓
┌──────────────────────────────────┐
│ JavaScript Event Handler         │
└──────┬───────────────────────────┘
       │
       ↓
┌──────────────────────────────────┐
│ React State Update               │
└──────┬───────────────────────────┘
       │
       ↓
┌──────────────────────────────────┐
│ Component Re-render              │
│ (Real-time update visible)       │
└──────────────────────────────────┘
```

---

## API Endpoint Hierarchy

```
/api/
├─ /auth/
│  ├─ login/ (POST)
│  ├─ register/ (POST)
│  ├─ logout/ (POST)
│  ├─ user/ (GET)
│  ├─ otp/
│  │  ├─ generate/ (POST)
│  │  └─ verify/ (POST)
│  └─ google/ (POST)
│
├─ /projects/
│  ├─ (GET, POST)
│  ├─ <id>/ (GET, PUT, DELETE)
│  ├─ search/ (GET)
│  ├─ <id>/members/ (POST, DELETE)
│  └─ <id>/tasks/ (GET, POST)
│
├─ /messages/
│  ├─ conversations/ (GET)
│  └─ (POST, GET)
│
├─ /chatrooms/
│  ├─ (GET, POST)
│  └─ <id>/members/ (GET, POST, DELETE)
│
├─ /comments/
│  ├─ (GET, POST)
│  ├─ <id>/ (PUT, DELETE)
│  └─ <id>/like/ (POST)
│
├─ /connections/
│  ├─ (GET, POST)
│  └─ <id>/ (PUT)
│
├─ /follow/
│  ├─ (GET, POST)
│  └─ <id>/ (DELETE)
│
├─ /profiles/
│  ├─ <id>/ (GET)
│  └─ (PUT - own profile)
│
└─ /notifications/
   ├─ (GET)
   ├─ <id>/ (PUT)
   └─ read-all/ (POST)
```

---

## Component Hierarchy (Frontend)

```
App.jsx (Root)
├─ Header
│  ├─ Navbar
│  ├─ Logo
│  └─ UserMenu
├─ Main Content
│  ├─ LoginPage
│  │  ├─ EmailInput
│  │  ├─ OTPForm
│  │  └─ SocialButtons
│  ├─ DashboardPage
│  │  ├─ UserProfile
│  │  ├─ ProjectList
│  │  └─ ActivityFeed
│  ├─ ProjectsPage
│  │  ├─ SearchBar
│  │  ├─ FilterPanel
│  │  └─ ProjectCard (x many)
│  ├─ ProjectDetailPage
│  │  ├─ ProjectHeader
│  │  ├─ TeamSection
│  │  ├─ TaskList
│  │  └─ CommentSection
│  ├─ ChatPage
│  │  ├─ ConversationList
│  │  └─ ChatWindow
│  │     ├─ MessageList
│  │     └─ MessageInput
│  └─ ProfilePage
│     ├─ ProfileHeader
│     ├─ SkillsList
│     └─ ProjectHistory
└─ Footer
   ├─ Links
   └─ Copyright
```

---

## Caching Strategy

```
Browser Cache
  ↓ Local Storage
  ├─ auth_token
  ├─ user_id
  └─ preferences

Axios Interceptor
  ↓ Add token to headers

Backend
  ↓
  ├─ View processes request
  │
  ├─→ Check Redis Cache
  │   ├─ Cache HIT → Return cached data
  │   └─ Cache MISS → Proceed to database
  │
  ├─→ Query Database
  │
  ├─→ Cache in Redis
  │   ├─ Key: "projects:page:1"
  │   ├─ Value: JSON data
  │   └─ TTL: 30 minutes
  │
  └─→ Return to Client

Redis (In-memory cache)
  ├─ Sessions
  ├─ Search results
  ├─ Project listings
  └─ User profiles
```

---

## Deployment Architecture

```
┌────────────────────────────────────────────────────────────┐
│                     Production Environment                 │
│                     (Render.com / Railway)                 │
│                                                            │
│  ┌─────────────────────────────────────────────────────┐ │
│  │                Docker Container Network             │ │
│  │                                                     │ │
│  │  ┌──────────────┐  ┌──────────────┐               │ │
│  │  │  Frontend    │  │  Backend     │               │ │
│  │  │  Container   │  │  Container   │               │ │
│  │  │              │  │              │               │ │
│  │  │ React Build  │  │ Django App   │               │ │
│  │  │ Nginx        │  │ Gunicorn     │               │ │
│  │  │ Port 3000    │  │ Port 8000    │               │ │
│  │  └──────────────┘  └──────────────┘               │ │
│  │         │                   │                      │ │
│  │         └───────┬───────────┘                      │ │
│  │                 ↓                                  │ │
│  │  ┌────────────────────────────────────────────┐   │ │
│  │  │        PostgreSQL Container                │   │ │
│  │  │        (Persistent Volume)                 │   │ │
│  │  └────────────────────────────────────────────┘   │ │
│  │                 ↓                                  │ │
│  │  ┌────────────────────────────────────────────┐   │ │
│  │  │        Redis Container                     │   │ │
│  │  │        (Cache & Session Store)             │   │ │
│  │  └────────────────────────────────────────────┘   │ │
│  └─────────────────────────────────────────────────┘ │
│                                                       │
│  Environment Variables:                              │
│  • DEBUG=False                                       │
│  • ALLOWED_HOSTS=...                                │
│  • DATABASE_URL=...                                 │
│  • REDIS_URL=...                                    │
│  • SECRET_KEY=...                                   │
│  • BREVO_API_KEY=...                                │
└────────────────────────────────────────────────────────┘
           ↓
    ┌──────────────┐
    │  DNS / SSL   │
    │  (HTTPS)     │
    └──────────────┘
```

---

## Development Workflow

```
Developer Workstation
├─ Code Editor (VS Code)
├─ Terminal
│  ├─ Backend Server
│  │  python manage.py runserver
│  ├─ Frontend Dev Server
│  │  npm run dev
│  └─ Docker Compose
│     docker-compose up -d
├─ Browser
│  └─ http://localhost:5173 (Vite dev server)
└─ Database GUI
   └─ pgAdmin / Adminer

Changes Made
  ↓
Hot Reload
  ├─ Frontend: Vite HMR
  └─ Backend: Django auto-reload

Testing
  ├─ Backend: python manage.py test
  ├─ Frontend: npm test
  └─ Manual: Browser testing

Commit & Push
  ├─ git add .
  ├─ git commit -m "..."
  └─ git push origin branch

CI/CD Pipeline (GitHub Actions)
  ├─ Run tests
  ├─ Check linting
  └─ Deploy to production
```

---

## Error Handling Flow

```
User Action
  ↓
Frontend Validation
  ├─ No error → Send to backend
  └─ Error → Show error toast

Backend Validation
  ├─ Form validation
  ├─ Permission check
  ├─ Business logic validation
  │
  ├─ Success → Save to DB → Return 200
  │
  └─ Error:
     ├─ Validation Error → 400 Bad Request
     ├─ Permission Error → 403 Forbidden
     ├─ Not Found → 404 Not Found
     ├─ Server Error → 500 Internal Server Error
     └─ Return JSON error response

Frontend Error Handler
  ├─ Check status code
  ├─ Extract error message
  ├─ Display to user (toast/modal)
  └─ Log for debugging
```

---

## Key Integration Points

```
External Services
│
├─ Email Service (Brevo)
│  ├─ OTP emails
│  ├─ Notifications
│  └─ Contact form
│
├─ OAuth Providers
│  ├─ Google
│  │  └─ Authentication
│  └─ GitHub
│     └─ Authentication
│
└─ Deployment Platforms
   ├─ Render.com
   ├─ Railway.app
   └─ Docker Registry
```

---

## Summary

This visual guide illustrates:
- ✅ Request/response flows
- ✅ Database relationships
- ✅ Authentication mechanisms
- ✅ Real-time communication
- ✅ API structure
- ✅ Component hierarchy
- ✅ Caching strategy
- ✅ Deployment setup
- ✅ Development workflow
- ✅ Error handling

All these components work together to create UniSync's seamless collaboration experience.

