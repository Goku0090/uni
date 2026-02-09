# UniSinq Platform - Architecture Diagram

## System Architecture Overview

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                            CLIENT LAYER                                      │
├─────────────────────────────────────────────────────────────────────────────┤
│                                                                               │
│  ┌──────────────────┐  ┌──────────────────┐  ┌──────────────────┐            │
│  │    Web Browser   │  │   Mobile Client  │  │   Desktop App    │            │
│  │  (HTML/CSS/JS)   │  │ (React Native)   │  │  (Electron)      │            │
│  └────────┬─────────┘  └──────────────────┘  └──────────────────┘            │
│           │                                                                    │
└─────────────────────────────────────────────────────────────────────────────┘
           │
           │ HTTP/HTTPS                         WebSocket
           │                                     (Real-time)
           ▼                                        ▼
┌──────────────────────────────────────────────────────────────────────────────┐
│                          NETWORKING LAYER                                     │
├──────────────────────────────────────────────────────────────────────────────┤
│                                                                                │
│  ┌────────────────────────────────────────────────────────────┐              │
│  │             Load Balancer / Reverse Proxy                   │              │
│  │                  (Nginx / HAProxy)                          │              │
│  └──────────┬──────────────────────────────┬───────────────────┘              │
│             │                              │                                  │
└─────────────┼──────────────────────────────┼──────────────────────────────────┘
              │                              │
              ▼                              ▼
┌──────────────────────────────────────────────────────────────────────────────┐
│                        APPLICATION LAYER                                      │
├──────────────────────────────────────────────────────────────────────────────┤
│                                                                                │
│  ┌─────────────────────────────────┐  ┌─────────────────────────────────┐   │
│  │   Django Application Server     │  │   Daphne WebSocket Server       │   │
│  │      (Gunicorn/uWSGI)           │  │   (ASGI Application)            │   │
│  │                                 │  │                                  │   │
│  │  ┌─────────────────────────────┐│  │  ┌──────────────────────────┐   │   │
│  │  │ Django Views (50+ views)    ││  │  │ WebSocket Consumers      │   │   │
│  │  │ - Authentication            ││  │  │ - ProjectUpdateConsumer  │   │   │
│  │  │ - Projects                  ││  │  │ - ActivityFeedConsumer   │   │   │
│  │  │ - Collaboration             ││  │  │ - NotificationConsumer   │   │   │
│  │  │ - Messaging                 ││  │  │ - ChatConsumer           │   │   │
│  │  │ - Profiles                  ││  │  │                          │   │   │
│  │  └─────────────────────────────┘│  │  └──────────────────────────┘   │   │
│  │                                 │  │                                  │   │
│  │  ┌─────────────────────────────┐│  │  ┌──────────────────────────┐   │   │
│  │  │ Django REST Framework       ││  │  │ Real-time Services       │   │   │
│  │  │ - Serializers               ││  │  │ - WebSocket Routing      │   │   │
│  │  │ - API Endpoints (40+)       ││  │  │ - Signal Handlers        │   │   │
│  │  │ - Permissions               ││  │  │ - Broadcast Logic        │   │   │
│  │  └─────────────────────────────┘│  │  └──────────────────────────┘   │   │
│  │                                 │  │                                  │   │
│  │  ┌─────────────────────────────┐│  │                                  │   │
│  │  │ Business Logic Layer        ││  │                                  │   │
│  │  │ - Services                  ││  │                                  │   │
│  │  │ - Utils                     ││  │                                  │   │
│  │  │ - Forms                     ││  │                                  │   │
│  │  │ - Permissions               ││  │                                  │   │
│  │  └─────────────────────────────┘│  │                                  │   │
│  │                                 │  │                                  │   │
│  └─────────────────────────────────┘  └──────────────────────────────────┘   │
│                                                                                │
└────────────┬───────────────────────────────────────────────────────────┬──────┘
             │                                                            │
             ▼                                                            ▼
┌──────────────────────────────────────────────────────────────────────────────┐
│                    DATA ACCESS & SERVICE LAYER                                │
├──────────────────────────────────────────────────────────────────────────────┤
│                                                                                │
│  ┌─────────────────────────────────────┐  ┌──────────────────────────────┐  │
│  │        ORM (Django Models)          │  │     External Services        │  │
│  │                                     │  │                              │  │
│  │  ┌─────────────────────────────┐   │  │  ┌──────────────────────┐    │  │
│  │  │ User & Authentication       │   │  │  │ Email Services       │    │  │
│  │  │ - User, StudentProfile      │   │  │  │ - Brevo API          │    │  │
│  │  │ - UserStatus                │   │  │  │ - ZeptoMail API      │    │  │
│  │  │ - OTP                       │   │  │  └──────────────────────┘    │  │
│  │  └─────────────────────────────┘   │  │                              │  │
│  │                                     │  │  ┌──────────────────────┐    │  │
│  │  ┌─────────────────────────────┐   │  │  │ OAuth Providers      │    │  │
│  │  │ Projects & Collaboration    │   │  │  │ - Google OAuth 2.0   │    │  │
│  │  │ - Project                   │   │  │  │ - Django Allauth     │    │  │
│  │  │ - ProjectMember             │   │  │  └──────────────────────┘    │  │
│  │  │ - ProjectTask               │   │  │                              │  │
│  │  │ - ProjectTemplate           │   │  │  ┌──────────────────────┐    │  │
│  │  └─────────────────────────────┘   │  │  │ External APIs        │    │  │
│  │                                     │  │  │ - RapidAPI           │    │  │
│  │  ┌─────────────────────────────┐   │  │  │ - NLP Services       │    │  │
│  │  │ Social & Networking         │   │  │  └──────────────────────┘    │  │
│  │  │ - Connection                │   │  │                              │  │
│  │  │ - Follow                    │   │  │  ┌──────────────────────┐    │  │
│  │  │ - Like                      │   │  │  │ Caching Layer        │    │  │
│  │  │ - Comment                   │   │  │  │ - Redis (optional)   │    │  │
│  │  │ - Notification              │   │  │  │ - In-Memory Cache    │    │  │
│  │  └─────────────────────────────┘   │  │  └──────────────────────┘    │  │
│  │                                     │  │                              │  │
│  │  ┌─────────────────────────────┐   │  └──────────────────────────────┘  │
│  │  │ Messaging & Chat            │   │                                    │
│  │  │ - ChatRoom                  │   │                                    │
│  │  │ - Message                   │   │                                    │
│  │  │ - MessageReaction           │   │                                    │
│  │  │ - MessageReadStatus         │   │                                    │
│  │  └─────────────────────────────┘   │                                    │
│  │                                     │                                    │
│  └─────────────────────────────────────┘                                    │
│                                                                              │
└────────────────┬─────────────────────────────────────────────────────┬──────┘
                 │                                                      │
                 ▼                                                      ▼
┌──────────────────────────────────────────────────────────────────────────────┐
│                        DATABASE LAYER                                         │
├──────────────────────────────────────────────────────────────────────────────┤
│                                                                                │
│  ┌────────────────────────────┐  ┌────────────────────────────────────────┐  │
│  │   PostgreSQL Database      │  │   SQLite Database (Development)        │  │
│  │   (Production)             │  │                                        │  │
│  │                            │  │  - Development & Testing               │  │
│  │ ┌──────────────────────┐   │  │  - Backup & Fixtures                 │  │
│  │ │ Primary Database     │   │  │  - Demo/Prototype                     │  │
│  │ │ - All Tables         │   │  │                                        │  │
│  │ │ - Indexes            │   │  └────────────────────────────────────────┘  │
│  │ │ - Constraints        │   │                                              │
│  │ └──────────────────────┘   │                                              │
│  │                            │                                              │
│  │ ┌──────────────────────┐   │                                              │
│  │ │ Replication          │   │                                              │
│  │ │ - Read Replicas      │   │                                              │
│  │ │ - Failover           │   │                                              │
│  │ └──────────────────────┘   │                                              │
│  │                            │                                              │
│  │ ┌──────────────────────┐   │                                              │
│  │ │ Backups              │   │                                              │
│  │ │ - Daily Backups      │   │                                              │
│  │ │ - Point-in-time      │   │                                              │
│  │ └──────────────────────┘   │                                              │
│  │                            │                                              │
│  └────────────────────────────┘                                              │
│                                                                                │
└──────────────────────────────────────────────────────────────────────────────┘

                                      │
                                      ▼
┌──────────────────────────────────────────────────────────────────────────────┐
│                        FILE STORAGE LAYER                                     │
├──────────────────────────────────────────────────────────────────────────────┤
│                                                                                │
│  ┌────────────────────────┐  ┌──────────────────┐  ┌───────────────────────┐ │
│  │ Local File System      │  │ S3 / Cloud       │  │ CDN (CloudFlare)      │ │
│  │ /media/                │  │ Storage          │  │ Image optimization    │ │
│  │ - Profile Photos       │  │ (AWS S3, GCS)    │  │ Caching               │ │
│  │ - Project Images       │  │ - Scalability    │  │ Global distribution   │ │
│  │ - Documents            │  │ - Redundancy     │  │                       │ │
│  │ /static/               │  │ - Cost-effective │  │                       │ │
│  │ - CSS, JS, Images      │  │                  │  │                       │ │
│  │                        │  │                  │  │                       │ │
│  └────────────────────────┘  └──────────────────┘  └───────────────────────┘ │
│                                                                                │
└──────────────────────────────────────────────────────────────────────────────┘
```

---

## Data Flow Diagrams

### 1. User Registration & OTP Flow

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                      USER REGISTRATION FLOW                                   │
└─────────────────────────────────────────────────────────────────────────────┘

User visits /register/
        │
        ▼
┌───────────────────────────────┐
│ Display Registration Form     │
│ (Email, Password, Name)       │
└───────────────────┬───────────┘
                    │
                    ▼
            User submits form
                    │
                    ▼
┌───────────────────────────────┐
│ Validate Input                │
│ Check if email exists         │
└───────────────────┬───────────┘
                    │
        ┌───────────┴───────────┐
        │ (Valid)               │ (Invalid)
        ▼                       ▼
    Generate OTP           Show error
        │                   message
        ▼
    Save OTP in DB
        │
        ▼
    Send OTP via Email
    (Brevo/ZeptoMail API)
        │
        ▼
    User receives email
        │
        ▼
    User visits /verify-otp/
        │
        ▼
    Enter OTP
        │
        ▼
┌──────────────────────────────┐
│ Verify OTP                   │
│ - Check if valid             │
│ - Check if expired           │
│ - Check if already used      │
└───────────────┬──────────────┘
                │
    ┌───────────┴───────────┐
    │ (Valid)               │ (Invalid)
    ▼                       ▼
Create User          Resend OTP
    │
    ▼
Create StudentProfile
    │
    ▼
Create ChatRoom (System Messages)
    │
    ▼
Create Notification (Welcome)
    │
    ▼
Issue Session / JWT Token
    │
    ▼
Redirect to Dashboard
```

---

### 2. Project Creation & Real-time Broadcast

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                    PROJECT CREATION FLOW                                      │
└─────────────────────────────────────────────────────────────────────────────┘

User visits /post-project/
        │
        ▼
┌────────────────────────────────┐
│ Display Project Form           │
│ - Title, Description           │
│ - Tech Stack, Status           │
│ - Collaboration Needs          │
└────────────┬───────────────────┘
             │
             ▼
     User submits form
             │
             ▼
┌────────────────────────────────┐
│ Validate Input                 │
│ Create Project Model Instance  │
└────────────┬───────────────────┘
             │
             ▼
      Save to Database
             │
             ▼
  Signal Handler Triggered
  (Django Signals)
             │
             ▼
┌────────────────────────────────┐
│ Create Notification            │
│ - Owner: Project Created       │
│ - Recipients: All followers    │
└────────────┬───────────────────┘
             │
             ▼
  WebSocket Broadcast
  (via ProjectUpdateConsumer)
             │
        ┌────┴─────────────────────────┐
        │                              │
        ▼                              ▼
  To project_room                 To activity_feed
  (Team members)                  (Followers)
        │                              │
        ▼                              ▼
  Real-time update in         Real-time update in
  Project Detail page          Activity Feed
        │
        ▼
Create ProjectMember (Owner)
        │
        ▼
Create ChatRoom (Team Chat)
        │
        ▼
Redirect to Project Detail
```

---

### 3. Real-time Messaging Flow

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                      MESSAGING FLOW                                           │
└─────────────────────────────────────────────────────────────────────────────┘

User A sends message to User B
        │
        ▼
   Text input submitted
        │
        ▼
   AJAX request to API
   POST /api/direct-message/user-b/
        │
        ▼
┌──────────────────────────────────────┐
│ View: send_direct_message()          │
│ - Get or Create ChatRoom             │
│ - Create Message instance            │
│ - Create MessageReadStatus (unread)  │
└──────────────────┬───────────────────┘
                   │
                   ▼
            Save to Database
                   │
                   ▼
        Signal Handler Triggered
                   │
                   ▼
┌──────────────────────────────────────┐
│ ChatConsumer broadcast message       │
│ - Room: chat_room_{room_id}          │
│ - Event: 'message_sent'              │
│ - Data: message, sender, timestamp   │
└──────────────────┬───────────────────┘
                   │
        ┌──────────┴──────────┐
        │ (To connected       │
        │  WebSocket clients) │
        │                     │
        ▼                     ▼
   User A sees           User B connected
   "Sent" status         to chat room
        │                     │
        │                     ▼
        │            Message appears
        │            in real-time
        │                     │
        │                     ▼
        │            User B clicks
        │            "Mark as Read"
        │                     │
        │                     ▼
        │         Create MessageReadStatus
        │                     │
        │                     ▼
        │         WebSocket update to A
        │                     │
        ▼                     ▼
   User A sees         User B sees
   "Read" timestamp    message as delivered

```

---

### 4. Find Collaborators (NLP Matching)

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                  FIND COLLABORATORS FLOW                                      │
└─────────────────────────────────────────────────────────────────────────────┘

User visits /find-collaborators/
        │
        ▼
┌──────────────────────────────┐
│ GET request                  │
│ Fetch current user profile   │
└──────────────┬───────────────┘
               │
               ▼
┌──────────────────────────────────────┐
│ Analyze User Profile                 │
│ - Extract skills                     │
│ - Extract interests                  │
│ - Extract tech stack preferences     │
└──────────────┬───────────────────────┘
               │
               ▼
┌──────────────────────────────────────┐
│ NLP Analysis (via RapidAPI)          │
│ - Skill vector extraction            │
│ - Interest matching                  │
│ - Experience level analysis          │
└──────────────┬───────────────────────┘
               │
               ▼
   Fetch all other StudentProfiles
               │
               ▼
┌──────────────────────────────────────┐
│ Calculate Match Scores               │
│ For each user:                       │
│ - skill_match (0-100)                │
│ - interest_match (0-100)             │
│ - experience_match (0-100)           │
│ - overall_score = weighted average   │
└──────────────┬───────────────────────┘
               │
               ▼
       Sort by score (DESC)
               │
               ▼
    Return top 10 matches
               │
               ▼
     Display in template
     (User cards with scores)
               │
               ▼
┌──────────────────────────────────────┐
│ User Action: Click "Connect"         │
└──────────────┬───────────────────────┘
               │
               ▼
  Create Connection Request
               │
               ▼
  Create Notification for target user
               │
               ▼
  WebSocket alert to target user
               │
               ▼
  Target user can Accept/Decline
```

---

### 5. Activity Feed Real-time Updates

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                    ACTIVITY FEED FLOW                                         │
└─────────────────────────────────────────────────────────────────────────────┘

User A performs action:
┌─────────────────────┐
│ - Likes a project   │
│ - Comments          │
│ - Posts project     │
│ - Follows user      │
└────────────┬────────┘
             │
             ▼
   Signal handler triggered
        (Django Signals)
             │
             ▼
┌──────────────────────────────────┐
│ Signal: post_like, post_comment  │
│ Receiver: Signal handler         │
│ Action: Create Notification      │
└──────────────┬────────────────────┘
               │
               ▼
    Find all followers of User A
               │
               ▼
    Create Notification for each follower
    - Type: like/comment/post
    - Content: action details
    - Link: target content
               │
               ▼
   Broadcast via WebSocket
   (ActivityFeedConsumer)
               │
        ┌──────┴──────────────────┐
        │                         │
        ▼                         ▼
   To activity_feed_{follower_id} rooms
        │
        ▼
   Connected followers receive update
        │
        ▼
   Real-time activity card appears
   in their feed
        │
        ▼
   Notification badge updated
   (if user not on activity feed)
        │
        ▼
   Optional: Send email notification
   (if user has enabled in settings)
```

---

## Component Interaction Diagram

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                    COMPONENT INTERACTIONS                                     │
└─────────────────────────────────────────────────────────────────────────────┘

             ┌─────────────────────────────┐
             │    Frontend Templates       │
             │  (HTML with JavaScript)     │
             └──────────┬──────────────────┘
                        │
         ┌──────────────┼──────────────────┐
         │              │                  │
         ▼              ▼                  ▼
    ┌────────────┐  ┌────────────┐  ┌────────────┐
    │  Django    │  │   DRF API  │  │ WebSocket  │
    │   Views    │  │Endpoints   │  │  Consumers │
    │ (50+ pages)│  │ (40+ APIs) │  │ (4 types)  │
    └─────┬──────┘  └─────┬──────┘  └─────┬──────┘
          │                │               │
          │                │               │
    ┌─────┴────────────────┴───────────────┴──────┐
    │                                              │
    ▼                                              ▼
┌────────────────────────┐            ┌─────────────────────────┐
│   ORM Models (15+)     │            │   Services              │
│ - StudentProfile       │            │ - EmailService          │
│ - Project              │            │ - NotificationService   │
│ - Comment              │            │ - ChatService           │
│ - Message              │            │ - SearchService         │
│ - ChatRoom             │            │ - NLPMatchingService    │
│ - Connection           │            │                         │
│ - etc.                 │            └────────────┬────────────┘
└────────┬───────────────┘                         │
         │                                         │
         │      ┌──────────────────────────────────┘
         │      │
         ▼      ▼
    ┌──────────────────────────┐
    │   Database (PostgreSQL)  │
    │ - Tables                 │
    │ - Indexes                │
    │ - Constraints            │
    │ - Transactions           │
    └──────────────────────────┘
         │
         ▼
    ┌──────────────────────────┐
    │   External Services      │
    │ - Email APIs             │
    │ - OAuth Providers        │
    │ - NLP APIs               │
    │ - Storage (S3)           │
    └──────────────────────────┘
```

---

## Authentication Flow Diagram

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                    AUTHENTICATION FLOW                                        │
└─────────────────────────────────────────────────────────────────────────────┘

                    User Access Request
                             │
            ┌────────────────┴────────────────┐
            │                                 │
            ▼                                 ▼
    ┌──────────────────┐          ┌──────────────────┐
    │ Email + OTP      │          │ Social Login     │
    │ Registration     │          │ (Google OAuth)   │
    └────────┬─────────┘          └────────┬─────────┘
             │                             │
             ▼                             ▼
    ┌──────────────────┐          ┌──────────────────┐
    │ Send OTP via     │          │ Redirect to      │
    │ Email            │          │ Google           │
    │ (Brevo/ZeptoMail)│          │ Authorization    │
    └────────┬─────────┘          └────────┬─────────┘
             │                             │
             ▼                             ▼
    ┌──────────────────┐          ┌──────────────────┐
    │ User Verifies    │          │ User grants      │
    │ OTP              │          │ permissions      │
    └────────┬─────────┘          └────────┬─────────┘
             │                             │
             └────────────────┬────────────┘
                              │
                              ▼
                    ┌──────────────────────┐
                    │ Create/Update User   │
                    │ & StudentProfile     │
                    └──────────┬───────────┘
                               │
                               ▼
                    ┌──────────────────────┐
                    │ Create Session       │
                    │ (Django Session)     │
                    │ OR JWT Token         │
                    └──────────┬───────────┘
                               │
                               ▼
                    ┌──────────────────────┐
                    │ Set Session Cookie   │
                    │ / Return JWT Token   │
                    └──────────┬───────────┘
                               │
                               ▼
                    ┌──────────────────────┐
                    │ Redirect to          │
                    │ Dashboard            │
                    └──────────────────────┘

Each subsequent request includes:
┌──────────────────────────────────┐
│ Cookie: sessionid=...            │
│ OR                               │
│ Authorization: Bearer <JWT>      │
└──────────────────────────────────┘

Middleware checks authentication:
┌──────────────────────────────────┐
│ - Validate session/token         │
│ - Get user from DB               │
│ - Attach to request              │
│ - Check permissions              │
└──────────────────────────────────┘
```

---

## Deployment Architecture

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                    DEPLOYMENT ARCHITECTURE                                    │
└─────────────────────────────────────────────────────────────────────────────┘

                            Internet
                                │
                                ▼
                    ┌──────────────────────┐
                    │  CloudFlare / CDN    │
                    │  (Static Assets)     │
                    └──────────┬───────────┘
                               │
                               ▼
                    ┌──────────────────────┐
                    │  Reverse Proxy       │
                    │  (Nginx / Load Bal.) │
                    └──────────┬───────────┘
                               │
                ┌──────────────┼──────────────┐
                │              │              │
                ▼              ▼              ▼
        ┌─────────────┐ ┌─────────────┐ ┌─────────────┐
        │   Instance  │ │  Instance   │ │  Instance   │
        │      1      │ │      2      │ │      3      │
        │             │ │             │ │             │
        │ Django App  │ │ Django App  │ │ Django App  │
        │ (Gunicorn)  │ │ (Gunicorn)  │ │ (Gunicorn)  │
        │             │ │             │ │             │
        │ Daphne      │ │ Daphne      │ │ Daphne      │
        │ (WebSocket) │ │ (WebSocket) │ │ (WebSocket) │
        └──────┬──────┘ └──────┬──────┘ └──────┬──────┘
               │               │               │
               └───────────────┼───────────────┘
                               │
                    ┌──────────┴──────────┐
                    │                     │
                    ▼                     ▼
        ┌───────────────────┐  ┌──────────────────┐
        │  PostgreSQL       │  │  Redis Cache     │
        │  Database         │  │  (optional)      │
        │                   │  │                  │
        │ - Primary         │  │ - Sessions       │
        │ - Replica 1       │  │ - User profiles  │
        │ - Replica 2       │  │ - Feed cache     │
        │                   │  │ - Message queue  │
        └────────┬──────────┘  └──────────────────┘
                 │
                 ▼
        ┌───────────────────┐
        │  S3 / Cloud       │
        │  Storage          │
        │                   │
        │ - Profile photos  │
        │ - Project images  │
        │ - Documents       │
        │ - Backups         │
        └───────────────────┘

Additional Services:
┌──────────────────────────────────────────────────────────┐
│ - Monitoring: Datadog / New Relic                        │
│ - Logging: CloudWatch / ELK Stack                        │
│ - Error Tracking: Sentry                                 │
│ - CI/CD: GitHub Actions / GitLab CI                      │
│ - DNS: CloudFlare / Route 53                             │
│ - SSL/TLS: Let's Encrypt / AWS Certificate Manager       │
└──────────────────────────────────────────────────────────┘
```

---

## Database Schema Overview

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                    DATABASE SCHEMA RELATIONSHIPS                              │
└─────────────────────────────────────────────────────────────────────────────┘

Users & Authentication
├── User (Django default)
│   ├── 1:1─── StudentProfile (bio, skills, college)
│   ├── 1:1─── UserStatus (online/offline)
│   ├── M─────  OTP (for login/registration)
│   └── 1:M─── Notification (as recipient)
│
Projects & Collaboration
├── Project
│   ├── 1:M─── ProjectMember (team)
│   ├── 1:M─── ProjectInvitation
│   ├── 1:M─── ProjectTask (To-Do items)
│   ├── 1:M─── ProjectMilestone
│   ├── 1:M─── Comment (on project)
│   ├── M─────  Like (users who liked)
│   ├── M─────  Notification (as content)
│   └── owner───FK─── User
│
Templates
├── ProjectTemplate
│   └── creator───FK─── User
│
Social & Networking
├── Connection (friend requests)
│   ├── requester───FK─── User
│   └── receiver───FK─── User
│
├── Follow
│   ├── follower───FK─── User
│   └── following───FK─── User
│
├── Like
│   ├── user───FK─── User
│   └── project───FK─── Project
│
├── Comment
│   ├── user───FK─── User
│   ├── project───FK─── Project
│   └── parent_comment───FK─── Comment (self)
│
├── Notification
│   ├── recipient───FK─── User
│   ├── notifier───FK─── User (nullable)
│   └── content_object───GenericFK─── Any model
│
Messaging
├── ChatRoom
│   ├── 1:M─── Message
│   ├── M:M─── User (members)
│   │
│   ├── Message
│   │   ├── sender───FK─── User
│   │   ├── room───FK─── ChatRoom
│   │   ├── 1:M─── MessageReaction
│   │   └── 1:M─── MessageReadStatus
│   │
│   ├── MessageReaction
│   │   ├── user───FK─── User
│   │   └── message───FK─── Message
│   │
│   └── MessageReadStatus
│       ├── user───FK─── User
│       └── message───FK─── Message
```

---

**Document Status:** Complete  
**Created:** Feb 09, 2026  
**Architecture Version:** 2.0
