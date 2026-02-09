# UniSync - Architecture & Data Flow Diagrams

## 1. System Architecture Overview

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                            UNISYNC PLATFORM                                 │
├─────────────────────────────────────────────────────────────────────────────┤
│                                                                             │
│  ┌─────────────────────────────────────────────────────────────────────┐  │
│  │                       USER INTERFACE LAYER                         │  │
│  │  ┌──────────────┐  ┌──────────────┐  ┌──────────────────────────┐ │  │
│  │  │ Login Page   │  │ Dashboard    │  │ Project Detail Page      │ │  │
│  │  │ - Email OTP  │  │ - Feed       │  │ - Comments (Real-time)   │ │  │
│  │  │ - OAuth      │  │ - Stats      │  │ - Members                │ │  │
│  │  └──────────────┘  └──────────────┘  └──────────────────────────┘ │  │
│  │                                                                    │  │
│  │  ┌──────────────┐  ┌──────────────┐  ┌──────────────────────────┐ │  │
│  │  │ Profile      │  │ Messages     │  │ Find Collaborators       │ │  │
│  │  │ - Avatar     │  │ - Threads    │  │ - Skill Matching         │ │  │
│  │  │ - Skills     │  │ - Reactions  │  │ - Filters                │ │  │
│  │  └──────────────┘  └──────────────┘  └──────────────────────────┘ │  │
│  └─────────────────────────────────────────────────────────────────────┘  │
│                    │                                          ▲           │
│                    │ HTTP + AJAX + WebSocket                 │           │
│                    ▼                                          │           │
│  ┌─────────────────────────────────────────────────────────────────────┐  │
│  │                     APPLICATION SERVER                             │  │
│  │  ┌─────────────────────────────────────────────────────────────┐  │  │
│  │  │ Django REST Framework APIs (50+ Endpoints)               │  │  │
│  │  │ - Authentication: /auth/login, /auth/verify-otp, etc.   │  │  │
│  │  │ - Projects: /api/projects/, /api/projects/<id>/         │  │  │
│  │  │ - Comments: /api/comments/, /api/comments/<id>/         │  │  │
│  │  │ - Messages: /api/messages/, /api/chat-rooms/            │  │  │
│  │  │ - Profiles: /api/users/profile/                         │  │  │
│  │  └─────────────────────────────────────────────────────────────┘  │  │
│  │  ┌─────────────────────────────────────────────────────────────┐  │  │
│  │  │ Django Views & Controllers                               │  │  │
│  │  │ - Authentication (login, OTP, OAuth)                    │  │  │
│  │  │ - Project Management (CRUD)                             │  │  │
│  │  │ - Dashboard & Feed                                      │  │  │
│  │  │ - Profile Management                                    │  │  │
│  │  └─────────────────────────────────────────────────────────────┘  │  │
│  │  ┌─────────────────────────────────────────────────────────────┐  │  │
│  │  │ WebSocket Consumers (Django Channels)                   │  │  │
│  │  │ - ProjectUpdateConsumer → /ws/project/<id>/            │  │  │
│  │  │ - ActivityFeedConsumer → /ws/activity/                 │  │  │
│  │  │ - NotificationConsumer → /ws/notifications/            │  │  │
│  │  └─────────────────────────────────────────────────────────────┘  │  │
│  └─────────────────────────────────────────────────────────────────────┘  │
│                    │                                          ▲           │
│                    │ SQL Queries + Signals                   │ Events    │
│                    ▼                                          │           │
│  ┌─────────────────────────────────────────────────────────────────────┐  │
│  │                        DATA LAYER                                   │  │
│  │  ┌──────────────────────────────────────────────────────────────┐  │  │
│  │  │ Django ORM (SQLAlchemy-like object mapper)               │  │  │
│  │  │ - QuerySet API                                           │  │  │
│  │  │ - Relationship handling                                  │  │  │
│  │  │ - Migration system                                       │  │  │
│  │  └──────────────────────────────────────────────────────────────┘  │  │
│  │  ┌──────────────────────────────────────────────────────────────┐  │  │
│  │  │ PostgreSQL Database                                      │  │  │
│  │  │ - Users, Profiles, Projects                             │  │  │
│  │  │ - Comments, Likes, Follows                              │  │  │
│  │  │ - Messages, Connections                                 │  │  │
│  │  │ - Notifications, Activities                             │  │  │
│  │  └──────────────────────────────────────────────────────────────┘  │  │
│  │  ┌──────────────────────────────────────────────────────────────┐  │  │
│  │  │ Redis Cache / InMemory Channel Layer                     │  │  │
│  │  │ - WebSocket channel routing                              │  │  │
│  │  │ - User stats caching (5 min TTL)                        │  │  │
│  │  └──────────────────────────────────────────────────────────────┘  │  │
│  └─────────────────────────────────────────────────────────────────────┘  │
│                           │                                              │
│                           ▼                                              │
│  ┌─────────────────────────────────────────────────────────────────────┐  │
│  │                    EXTERNAL SERVICES                                │  │
│  │  ┌──────────────┐  ┌──────────────┐  ┌──────────────────────────┐ │  │
│  │  │ Brevo Email  │  │ Google OAuth │  │ RapidAPI Universities   │ │  │
│  │  │ Service      │  │ Service      │  │ Data                     │ │  │
│  │  └──────────────┘  └──────────────┘  └──────────────────────────┘ │  │
│  └─────────────────────────────────────────────────────────────────────┘  │
│                                                                             │
└─────────────────────────────────────────────────────────────────────────────┘
```

---

## 2. Authentication Flow

```
┌─────────────────────────────────────────────────────────────────┐
│                  USER AUTHENTICATION FLOWS                      │
└─────────────────────────────────────────────────────────────────┘

┌────── EMAIL + OTP FLOW ───────┐
│                               │
│  User enters email            │
│        │                       │
│        ▼                       │
│  POST /auth/login/            │
│        │                       │
│        ▼                       │
│  Check if email exists        │
│        │                       │
│        ├─ NO → Error          │
│        │                       │
│        └─ YES ▼               │
│     Generate OTP (6 digits)   │
│        │                       │
│        ▼                       │
│   Send via Email              │
│  (Brevo/Zepto/Gmail)          │
│        │                       │
│        ▼                       │
│   Show OTP form               │
│        │                       │
│        ▼                       │
│   User enters code            │
│        │                       │
│        ▼                       │
│   POST /auth/verify-otp/      │
│        │                       │
│        ├─ Invalid → Error     │
│        ├─ Expired → Error     │
│        │                       │
│        └─ Valid ▼             │
│      Create session           │
│        │                       │
│        ▼                       │
│   Redirect to /dashboard/     │
│                               │
└───────────────────────────────┘

┌────── GOOGLE OAUTH FLOW ──────┐
│                               │
│  User clicks "Google Login"   │
│        │                       │
│        ▼                       │
│  Redirect to Google Consent   │
│  (accounts.google.com)        │
│        │                       │
│        ▼                       │
│  User authorizes             │
│        │                       │
│        ▼                       │
│  Google redirects back        │
│  with auth code              │
│        │                       │
│        ▼                       │
│  Django-allauth processes    │
│  auth code                    │
│        │                       │
│        ├─ User exists → Login │
│        │                       │
│        └─ New user ▼          │
│    Auto-create account       │
│        │                       │
│        ▼                       │
│   Create session             │
│        │                       │
│        ▼                       │
│   Redirect to /dashboard/    │
│                               │
└───────────────────────────────┘

┌────── SESSION MGMT ───────────┐
│                               │
│  Session ID stored in:        │
│  - Browser cookie             │
│  - Server session store       │
│                               │
│  Each request:                │
│  - Browser sends cookie       │
│  - Django validates           │
│  - @login_required works      │
│                               │
└───────────────────────────────┘
```

---

## 3. Comment & Real-Time Update Flow

```
┌──────────────────────────────────────────────────────────────────────┐
│         COMMENT POSTING & REAL-TIME UPDATE FLOW                     │
└──────────────────────────────────────────────────────────────────────┘

CLIENT SIDE                          BACKEND SIDE
│                                    │
│ 1. User types comment              │
│    "Great project!"                │
│        │                           │
│        ▼                           │
│ 2. Click "Post"                    │
│        │                           │
│        ├─ Set CSRF token ◄─────────┼─ Get from form
│        │                           │
│        ▼                           │
│ 3. POST /api/comments/             │
│    {content: "Great..."}      ────►│ 4. View: PostCommentView
│                                    │    │
│    [Wait for response]             │    ▼
│                                    │ 5. Validate & create
│                                    │    Comment object in DB
│                                    │    │
│                                    │    ▼
│                                    │ 6. @receiver(post_save)
│                                    │    signal triggered
│                                    │    │
│                                    │    ▼
│                                    │ 7. Signal handler:
│                                    │    get_channel_layer()
│                                    │    │
│                                    │    ▼
│                                    │ 8. group_send(
│                                    │      'project_2',
│                                    │      {...}
│                                    │    )
│                                    │    │
│ ◄────────────────────────────────┼─────┼─ 9. Broadcast to group
│                                    │    │
│ 10. WebSocket onmessage            │    ▼
│     {type: 'comment_added',  ◄────┼─ 10. Consumer.send()
│      comment: {...}}                │
│        │                           │
│        ▼                           │
│ 11. handleMessage()                │
│        │                           │
│        ▼                           │
│ 12. onCommentAdded()               │
│        │                           │
│        ▼                           │
│ 13. Create DOM element             │
│        │                           │
│        ▼                           │
│ 14. Insert into #comments-list     │
│        │                           │
│        ▼                           │
│ 15. Scroll to new comment          │
│        │                           │
│        ▼                           │
│ 16. USER SEES COMMENT!             │
│     (Instantly, no refresh)        │
│                                    │
│ [All other connected users         │
│  see it too via same flow]         │
```

---

## 4. Database Relationships

```
┌────────────────────────────────────────────────────────────────────────┐
│                    DATA MODEL RELATIONSHIPS                            │
└────────────────────────────────────────────────────────────────────────┘

                            User (Django)
                                 │
                    ┌────────────┬┴────┬────────────────┐
                    │            │     │                │
                    ▼            ▼     ▼                ▼
            StudentProfile   Projects  Messages     Notifications
                │             │        │                │
                │             │        │                │
                │             ├──▶ ProjectMember       Activity
                │             │     │
                │             │     ├──▶ ProjectTask
                │             │     │
                │             │     ├──▶ ProjectMilestone
                │             │     │
                │             │     └──▶ Comment ◀─────┘
                │             │           │
                │             │           ├──▶ CommentLike
                │             │           │
                │             │           └──▶ Comment (reply)
                │             │
                │             └──▶ Like
                │
                │
                ├──▶ Connection (sender/receiver)
                │
                ├──▶ Follow (follower/following)
                │
                └──▶ ChatRoom ──▶ ChatRoomMember
                                  │
                                  └──▶ Message
                                       │
                                       ├──▶ MessageReaction
                                       │
                                       └──▶ MessageReadStatus


┌─────────────────────────────────────┐
│ Key Relationships Summary            │
├─────────────────────────────────────┤
│ Project 1:N Members                 │
│ Project 1:N Comments                │
│ Project 1:N Tasks                   │
│ Project 1:N Likes                   │
│ User 1:N Projects (owner)           │
│ User 1:N Messages (sender)          │
│ User 1:N Messages (receiver)        │
│ User 1:N Comments                   │
│ Comment 1:N Replies                 │
│ User 1:N Notifications              │
│ User 1:N Connections                │
│ User 1:N Follows                    │
│ ChatRoom N:M Users                  │
│ ChatRoom 1:N Messages               │
└─────────────────────────────────────┘
```

---

## 5. Project Lifecycle

```
┌─────────────────────────────────────────────────────────────────┐
│              PROJECT LIFECYCLE & STATE TRANSITIONS              │
└─────────────────────────────────────────────────────────────────┘

  [No Project Yet]
        │
        │ User clicks "Post Project"
        ▼
    [Viewing Form]
        │
        │ Fill details:
        │ - Title: "Mobile App"
        │ - Description: "..."
        │ - Category: "Mobile"
        │ - Visibility: "Public"
        │
        ▼
   [Form Submitted]
        │
        │ POST /api/projects/
        │
        ▼
  [Project Created]
    (DB saved)
        │
        │ Signal: project_created
        │ Creates: ProjectMember (owner)
        │ Creates: Activity (feed)
        │
        ├─ Status: "active"
        ├─ Visibility: "public"
        ├─ Owner: current_user
        ├─ Members: 1 (owner)
        │
        ▼
  [Project Detail Page]
    (Accessible to all if public)
        │
        ├─ View project info
        ├─ See members
        ├─ Post comments
        ├─ Like project
        ├─ View tasks
        │
        ▼
  [Edit Project]
    (Owner only)
        │
        ├─ Update title/description
        ├─ Change visibility
        ├─ Invite members
        │
        ▼
  [Members Collaborate]
        │
        ├─ Add tasks
        ├─ Post comments (real-time)
        ├─ Update task status
        ├─ Create milestones
        │
        ▼
  [Project Completion]
        │
        │ Change status → "completed"
        │
        ├─ Activity: "Project completed"
        ├─ Still visible (archive)
        ├─ Comments still available
        │
        ▼
  [Optional: Delete]
        │
        │ Owner deletes
        ├─ Removes from public view
        ├─ Cascades: members, tasks,
        │             comments, etc.
        │
        ▼
   [Deleted]
    (Gone from DB)
```

---

## 6. Messaging Flow

```
┌─────────────────────────────────────────────────────────────────┐
│              MESSAGING SYSTEM FLOW                              │
└─────────────────────────────────────────────────────────────────┘

DIRECT MESSAGE (1:1)
│
├─ Sender: User A
├─ Receiver: User B
├─ Type: "text" or "image" or "file"
├─ Read Status: Tracked per user
├─ Reactions: 👍 😂 ❤️ etc.
│
└─ Flow:
   User A types message
      │
      ▼
   POST /api/messages/send/
   {sender: A, receiver: B, content: "Hi"}
      │
      ▼
   Message created in DB
      │
      ▼
   Signal triggers
      │
      ▼
   WebSocket broadcasts to both users
      │
      ▼
   User B's UI updates in real-time
      │
      ▼
   User B clicks message
      │
      ▼
   POST /api/messages/<id>/read/
      │
      ▼
   MessageReadStatus created
      │
      ▼
   User A sees "Read"
      │
      ▼
   User B adds reaction
      │
      ▼
   MessageReaction created + broadcast

GROUP MESSAGE (N:N)
│
├─ Container: ChatRoom
├─ Members: N users (chat_members)
├─ Messages: Visible to all room members
├─ Read Status: Per user per message
│
└─ Similar flow as DM but broadcasts to all members
```

---

## 7. Search & Filtering Flow

```
┌──────────────────────────────────────────────────────────────┐
│         SEARCH & FILTERING ARCHITECTURE                      │
└──────────────────────────────────────────────────────────────┘

SEARCH PROJECTS
│
├─ Input: query string (name/description)
├─ Filters: category, visibility, date range
├─ Sorting: newest, popular, trending
│
└─ Flow:
   GET /api/projects/search/?q=mobile&category=app
      │
      ▼
   DjangoFilterBackend processes filters
      │
      ├─ Filter by category
      ├─ Filter by visibility (public only if anon)
      ├─ Search in title, description
      │
      ▼
   Q objects combine conditions (OR logic)
      │
      ├─ (title__icontains='mobile') OR
      ├─ (description__icontains='mobile')
      │
      ▼
   QuerySet evaluated
      │
      ├─ select_related('user')
      ├─ prefetch_related('members')
      │
      ▼
   Paginate results
      │
      ├─ 10 per page
      ├─ Return page data
      │
      ▼
   JSON response
      │
      ├─ Total count
      ├─ Current page
      ├─ Results array
      │
      ▼
   Client displays results

FIND COLLABORATORS
│
├─ NLP Skill Matching
│ ├─ Parse user skills from JSON
│ ├─ Parse project needs
│ ├─ Calculate similarity (Jaccard/Cosine)
│ └─ Score match %
│
├─ Filters Applied
│ ├─ College (optional)
│ ├─ Location (optional)
│ ├─ Skill tags
│ ├─ Exclude self
│ └─ Exclude already connected
│
└─ Results Ranked by:
   ├─ Skill match score (primary)
   ├─ Profile completion
   └─ Number of projects
```

---

## 8. Performance Optimization Patterns

```
┌──────────────────────────────────────────────────────────────┐
│         PERFORMANCE OPTIMIZATION STRATEGIES                  │
└──────────────────────────────────────────────────────────────┘

QUERY OPTIMIZATION
│
├─ N+1 Query Problem
│  │
│  ├─ ❌ BAD: for p in projects: p.user.name  [N+1 queries]
│  │
│  └─ ✅ GOOD: select_related('user')  [1 query]
│
├─ Multiple Relations
│  │
│  ├─ ❌ BAD: for p in projects: p.comments.count()
│  │
│  └─ ✅ GOOD: annotate(count=Count('comments'))
│
├─ Related Objects (Many)
│  │
│  ├─ ❌ BAD: Project.objects.all() loads all comments in loop
│  │
│  └─ ✅ GOOD: prefetch_related('comments')
│
└─ Use Indices
   └─ Database indices on: user_id, project_id, created_at

CACHING PATTERNS
│
├─ User Stats
│  │
│  ├─ Cache key: user_stats_{user_id}
│  ├─ TTL: 5 minutes
│  ├─ Invalidate on: Follow, Project create
│  │
│  └─ Avoid recalculating counts
│
├─ Feed Results
│  │
│  ├─ Cache paginated results
│  ├─ Invalidate on: new comment, new project
│  │
│  └─ Fast repeat page loads
│
└─ Template Fragment Caching
   ├─ Cache navigation bar
   ├─ Cache sidebar
   └─ 1-hour TTL

FRONTEND OPTIMIZATION
│
├─ AJAX for Updates (not full page reload)
├─ Debounced Search (wait 300ms before API call)
├─ Lazy Loading (load images on scroll)
├─ Pagination (10-20 items per page, not 1000)
├─ Static File Compression (CSS/JS minified)
├─ Browser Caching (far-future expires headers)
└─ CDN for Static Files (CloudFlare)

DATABASE PARTITIONING (Future)
│
├─ Partition Comments by project_id
├─ Partition Messages by date
├─ Partition Activity by user_id
└─ Keep hot data (recent) in fast storage
```

---

## 9. Error Handling Flow

```
┌──────────────────────────────────────────────────────────────┐
│              ERROR HANDLING ARCHITECTURE                      │
└──────────────────────────────────────────────────────────────┘

FRONTEND ERROR
│
├─ Validation Error
│  │
│  ├─ Empty field
│  │
│  ├─ Toast/Alert shown to user
│  │
│  └─ No API call made
│
├─ API Error (4xx/5xx)
│  │
│  ├─ Fetch promise rejected
│  │
│  ├─ Error message extracted
│  │
│  ├─ Display to user
│  │
│  └─ Log to console/Sentry
│
└─ WebSocket Error
   │
   ├─ Socket.onerror triggered
   │
   ├─ Auto-reconnect attempted
   │
   ├─ Exponential backoff (1s, 2s, 4s, 8s...)
   │
   └─ After 5 failed: show user notice

BACKEND ERROR (Django)
│
├─ Validation Error
│  │
│  ├─ DRF Serializer validation fails
│  │
│  ├─ Return 400 Bad Request
│  │
│  └─ Include error details in JSON
│
├─ Permission Error
│  │
│  ├─ @login_required fails → Redirect to /login/
│  │
│  ├─ @permission_required fails → 403 Forbidden
│  │
│  └─ API: 403 with error message
│
├─ Database Error
│  │
│  ├─ try/except IntegrityError (unique constraint)
│  │
│  ├─ try/except ObjectDoesNotExist
│  │
│  ├─ Return 404 Not Found
│  │
│  └─ Log error to file
│
├─ Email Service Error
│  │
│  ├─ Brevo API timeout
│  │
│  ├─ Fall back to ZeptoMail
│  │
│  ├─ Fall back to Gmail SMTP
│  │
│  └─ Show user: "Email error, try again"
│
└─ Unhandled Exception
   │
   ├─ Catch in middleware
   │
   ├─ Log with traceback
   │
   ├─ Email admin
   │
   └─ Return 500 error page

ERROR LOGGING
│
├─ Console (development)
│  ├─ Format: [LEVEL] message
│  └─ Color coded
│
├─ File (production)
│  ├─ Path: logs/django.log
│  ├─ Rotating: 10MB per file, 5 backups
│  └─ Format: Timestamp, level, module, message
│
└─ Error Tracking (Sentry - future)
   ├─ Send exceptions to Sentry
   ├─ Aggregated error tracking
   └─ Alert on critical errors
```

---

## 10. Deployment Architecture

```
┌────────────────────────────────────────────────────────────────┐
│              DEPLOYMENT ARCHITECTURE (Render.com)             │
└────────────────────────────────────────────────────────────────┘

INTERNET
   │
   ▼
[Load Balancer / CDN]
   │
   ├─────────────────────────────────┐
   ▼                                 ▼
[Web Service - Gunicorn]    [WebSocket Service - Daphne]
├─ Instance: Standard        ├─ Instance: Standard
├─ Runtime: Python 3.10      ├─ Runtime: Python 3.10
├─ Replicas: 1-3            ├─ Replicas: 1-3
├─ Start: gunicorn           ├─ Start: daphne
│   auth_project.wsgi        │   -b 0.0.0.0
├─ Handles: HTTP requests   ├─ Handles: WebSocket conn.
│                            │
│  [Django App]             │  [Django App]
│  ├─ Views                 │  ├─ Consumers
│  ├─ API                   │  ├─ Routing
│  ├─ Static files (via     │  └─ Channel Layer
│  │  Render CDN)           │     (InMemory or Redis)
│  └─ Sessions              │
│                            │
└────────────────┬───────────┘
                 │
                 ▼
         [PostgreSQL Database]
         ├─ Hosted on Render
         ├─ Automated backups
         ├─ Connection pooling
         └─ Replica (optional)
                 │
                 ├─ Stores: All app data
                 │
                 └─ Migrations: Auto-run on deploy

[Static File CDN]
   │
   ├─ CSS, JS, Images
   ├─ Rendered CDN
   ├─ Far-future expires
   └─ Automatic purge on redeploy

[External Services]
   │
   ├─ Brevo Email API
   ├─ Google OAuth
   ├─ GitHub OAuth
   └─ RapidAPI (Universities)

DEPLOYMENT FLOW
│
├─ 1. Git push to main
├─ 2. Render detects change
├─ 3. Install dependencies (pip install -r requirements.txt)
├─ 4. Run migrations (python manage.py migrate)
├─ 5. Collect static files (python manage.py collectstatic)
├─ 6. Build complete
├─ 7. Deploy new service instances
├─ 8. Routes traffic to new instances
├─ 9. Old instances shut down
└─ 10. Site live with new code

CI/CD PIPELINE (GitHub)
│
├─ Pre-commit: Linting (flake8)
├─ Push to main: Run tests
├─ Tests pass: Build Docker image
├─ Deploy to Render
└─ Health check: Ping endpoints
```

---

This completes the visual architecture documentation. Use these diagrams to understand UniSync's system design, data flow, and deployment architecture.
