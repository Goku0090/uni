# UniSync Codebase Analysis - START HERE

## What is UniSync?

**UniSync** (also branded as **UniSinQ**) is a comprehensive **full-stack web application** for student collaboration and project discovery. It enables:

- 👥 Students to find and connect with potential collaborators
- 🚀 Project creation and team management  
- 💬 Real-time messaging and notifications
- 🤝 Networking and skill-based matching
- 📊 Activity feeds and engagement tracking

**Tech Stack:** Django + Django Channels + PostgreSQL + Vanilla JavaScript

---

## 📂 Where to Find Information

### 1. Full Technical Analysis
📄 **File:** `CODEBASE_COMPLETE_ANALYSIS_2026_FINAL_COMPLETE.md`

**Contains:**
- Complete architecture overview
- All 15+ data models explained
- REST API endpoint reference
- WebSocket implementation details
- Authentication flows
- Deployment configuration
- Performance optimizations
- Common issues & solutions

**Read this for:** Deep understanding of how the system works

---

### 2. Quick Navigation Guide  
📄 **File:** `CODEBASE_QUICK_NAVIGATION_GUIDE_2026.md`

**Contains:**
- Quick file location reference
- API endpoints quick map
- WebSocket event types
- View functions quick reference
- Common tasks (how to add features)
- Debugging tips
- Code patterns

**Read this for:** Quick lookups and "how do I..."

---

## 🏗️ Quick Architecture Overview

```
┌─────────────────────────────────────────────────┐
│           FRONTEND (Browser)                    │
│  - HTML Templates                              │
│  - JavaScript (realtime-updates.js)            │
│  - CSS Styling                                 │
└──────────────┬──────────────────────────────────┘
               │ HTTP & WebSocket
┌──────────────▼──────────────────────────────────┐
│         DJANGO BACKEND (Python)                 │
│  ┌─────────────────────────────────────────┐   │
│  │ Views (50+ functions)                   │   │
│  │ - Authentication (OTP, OAuth)           │   │
│  │ - Project Management                    │   │
│  │ - Messaging & Chat                      │   │
│  │ - Social Features                       │   │
│  └─────────────────────────────────────────┘   │
│  ┌─────────────────────────────────────────┐   │
│  │ REST API (DRF)                          │   │
│  │ - Chat API (chat_api.py)                │   │
│  │ - Comment API (comment_api.py)          │   │
│  │ - Profile Serializers                   │   │
│  └─────────────────────────────────────────┘   │
│  ┌─────────────────────────────────────────┐   │
│  │ WebSocket (Django Channels)             │   │
│  │ - Project Updates Consumer              │   │
│  │ - Activity Feed Consumer                │   │
│  │ - Notifications Consumer                │   │
│  └─────────────────────────────────────────┘   │
└──────────────┬──────────────────────────────────┘
               │ 
┌──────────────▼──────────────────────────────────┐
│    DATA & SERVICES                              │
│  ┌─────────────────────────────────────────┐   │
│  │ 15+ Django Models                       │   │
│  │ - Users, Profiles, Connections          │   │
│  │ - Projects, Teams, Tasks                │   │
│  │ - Messages, Chat Rooms                  │   │
│  │ - Notifications, Activities             │   │
│  └─────────────────────────────────────────┘   │
│  ┌─────────────────────────────────────────┐   │
│  │ Services & Utils                        │   │
│  │ - NLP-based matching                    │   │
│  │ - Permission checking                   │   │
│  │ - Email sending (Brevo)                 │   │
│  └─────────────────────────────────────────┘   │
└──────────────┬──────────────────────────────────┘
               │
┌──────────────▼──────────────────────────────────┐
│  DATABASE (PostgreSQL) + CACHE                  │
└──────────────────────────────────────────────────┘
```

---

## 🔑 Key Components

### 1. Authentication System
**Files:** `views.py`, `forms.py`, `models.py`

- **Email/OTP Login:** 6-digit codes via Brevo email
- **Social OAuth:** Google & GitHub login
- **Registration:** Email verification + profile creation

### 2. Messaging System  
**Files:** `chat_api.py`, `consumers.py`, `models.py`

- **Direct Messages:** One-on-one conversations
- **Group Chats:** Multiple users in ChatRoom
- **Real-time Delivery:** WebSocket for instant messaging
- **Read Status Tracking:** Per-user message read timestamps
- **Reactions & Replies:** Rich message features

### 3. Project Management
**Files:** `views.py`, `forms.py`, `models.py`

- **Create/Edit/Delete:** Full CRUD operations
- **Team Collaboration:** Team members with roles
- **Task Tracking:** Tasks with status & priority
- **Permissions:** Public/Private/Invited-only visibility

### 4. Real-time Updates
**Files:** `consumers.py`, `routing.py`, `realtime-updates.js`

- **WebSocket Connections:** 3 concurrent connections per user
- **Event Broadcasting:** Changes broadcast to all clients
- **Automatic Reconnection:** Handles dropped connections
- **Multiple Channels:** Projects, Activity, Notifications

### 5. Social Features
**Files:** `views.py`, `utils.py`, `models.py`

- **Skill Matching:** NLP-based collaborator recommendations
- **Connections:** Connect with other users
- **Likes & Comments:** Engage with projects
- **Follow Users:** Track activity from specific users

---

## 📊 Key Statistics

| Component | Count |
|-----------|-------|
| Data Models | 15+ |
| View Functions | 50+ |
| API Endpoints | 20+ |
| WebSocket Consumers | 3 |
| Templates | 20+ |
| JavaScript Modules | 5+ |
| Lines of Code (Python) | 5000+ |
| Lines of Code (HTML/CSS/JS) | 3000+ |

---

## 🚀 Getting Started

### Step 1: Understand the Architecture
**Time: 30 minutes**

Read the **Architecture Overview** section above and skim the data models.

### Step 2: Review File Structure
**Time: 15 minutes**

```
auth_project/
├── accounts/              # Main application
│   ├── models.py         # Data models (1000 lines)
│   ├── views.py          # View functions (3400 lines)
│   ├── urls.py           # URL routing
│   ├── chat_api.py       # REST API for chat
│   ├── consumers.py      # WebSocket consumers
│   ├── static/js/        # JavaScript code
│   └── templates/        # HTML templates
│
├── auth_project/         # Project config
│   ├── settings.py       # Django settings
│   ├── urls.py           # Main URL routing
│   └── asgi.py           # WebSocket config (ASGI)
│
└── requirements.txt      # Dependencies
```

### Step 3: Pick Your Interest Area
**Time: 1-2 hours**

**If interested in...**

**Authentication:** 
→ Read `CODEBASE_QUICK_NAVIGATION_GUIDE_2026.md` section "Authentication Flow"
→ Look at: `views.py` (register_view, login_view, verify_otp_view)
→ Look at: `models.py` (OTP, StudentProfile)

**Messaging:**
→ Look at: `chat_api.py` (REST endpoints)
→ Look at: `models.py` (Message, ChatRoom, ChatRoomMember)
→ Look at: `consumers.py` (WebSocket handling)

**Projects:**
→ Look at: `views.py` (post_project, project_detail, edit_project)
→ Look at: `models.py` (Project, ProjectTeam, ProjectTask)
→ Look at: `forms.py` (ProjectForm)

**Real-time:**
→ Look at: `consumers.py` (AsyncWebsocketConsumer)
→ Look at: `static/js/realtime-updates.js` (Client-side)
→ Look at: `signals_realtime.py` (Signal handlers)

**APIs:**
→ Look at: `serializers.py` (REST serializers)
→ Look at: `chat_api.py` (Chat endpoints)
→ Look at: `comment_api.py` (Comment endpoints)

### Step 4: Explore the Code
**Time: 2-4 hours**

Use the **CODEBASE_QUICK_NAVIGATION_GUIDE_2026.md** for specific locations:
- Find view functions → use "View Functions Quick Reference"
- Find API endpoints → use "API Endpoints Quick Map"
- Find models → use "Data Models Quick Reference"
- Find WebSocket events → use "WebSocket Connections"

---

## 💡 Common Questions

### Q: How does real-time messaging work?

**A:** When a user sends a message:
1. POST request to `/api/messages/` endpoint
2. Message saved to database
3. Django signal triggered
4. Signal sends event to WebSocket consumer
5. Consumer broadcasts to all connected clients
6. Browser receives event via WebSocket
7. Frontend updates UI immediately (no page refresh)

### Q: How are users authenticated?

**A:** Two methods:
- **Email/OTP:** User enters email → 6-digit code sent → Verify → Logged in
- **OAuth:** User clicks "Login with Google" → redirected to Google → redirected back → Logged in

Both create/update StudentProfile automatically.

### Q: How does skill matching work?

**A:** The `StudentProfileNLP` utility:
1. Extracts interests/skills from user bio using NLP
2. Compares with other users' profiles
3. Calculates match score
4. Recommends top matches

See `utils.py` for implementation.

### Q: Where are files uploaded?

**A:** 
- Profile photos → `/media/profile_photos/`
- Chat files → `/media/chat_files/`
- Configured in `settings.py` with MEDIA_ROOT & MEDIA_URL

### Q: How is permission checking done?

**A:** Three ways:
1. **View decorators:** `@check_project_owner`, `@check_team_owner`
2. **DRF permissions:** `IsProjectOwner`, `IsTeamMember` classes
3. **Manual checks:** `if project.owner != request.user: forbidden()`

See `permissions.py` for all options.

### Q: How do I add a new feature?

**A:** Typical flow:
1. Add model to `models.py`
2. Create migration: `python manage.py makemigrations`
3. Add serializer to `serializers.py`
4. Add API view to `chat_api.py` or new file
5. Add URL to `urls.py`
6. Add frontend template/JavaScript
7. Test with `python manage.py runserver` + WebSocket consumer (Daphne)

See **CODEBASE_QUICK_NAVIGATION_GUIDE_2026.md** "Common Tasks" section.

---

## 🔧 Development Setup

### Prerequisites
```bash
Python 3.8+
PostgreSQL 12+ (or use SQLite for dev)
pip & virtualenv
```

### Quick Start
```bash
# Clone repository
git clone https://github.com/Goku0090/uni.git
cd auth_project

# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Create .env file with settings
cp .env.template .env
# Edit .env with your settings

# Run migrations
python manage.py migrate

# Create superuser
python manage.py createsuperuser

# Run server (HTTP only)
python manage.py runserver

# In another terminal, run WebSocket server
daphne -b 127.0.0.1 -p 8000 auth_project.asgi:application
```

### Access Application
- **Main site:** http://localhost:8000
- **Admin panel:** http://localhost:8000/admin
- **WebSocket URL:** ws://localhost:8000/ws/project/1/

---

## 🎯 Next Steps

1. **Read the full analysis:**
   - `CODEBASE_COMPLETE_ANALYSIS_2026_FINAL_COMPLETE.md`

2. **Use the quick reference:**
   - `CODEBASE_QUICK_NAVIGATION_GUIDE_2026.md`

3. **Explore the code:**
   - Start with `models.py` to understand data structure
   - Then explore `views.py` to understand business logic
   - Then check `consumers.py` for real-time features

4. **Pick a feature and trace it:**
   - Example: "How does a user send a message?"
   - Find model → find serializer → find view → find frontend JS → find WebSocket consumer

5. **Start contributing:**
   - Find an issue in the code
   - Add a feature
   - Submit a pull request

---

## 📞 Quick Reference Links

Within This Repository:
- 📄 Full Analysis: `CODEBASE_COMPLETE_ANALYSIS_2026_FINAL_COMPLETE.md`
- 📄 Quick Guide: `CODEBASE_QUICK_NAVIGATION_GUIDE_2026.md`

Source Code:
- 📂 Main App: `auth_project/accounts/`
- 📄 Models: `auth_project/accounts/models.py`
- 📄 Views: `auth_project/accounts/views.py`
- 📄 APIs: `auth_project/accounts/chat_api.py`
- 📄 WebSocket: `auth_project/accounts/consumers.py`
- 📄 Settings: `auth_project/auth_project/settings.py`

---

## ✅ Verification Checklist

After reading this document, you should understand:

- [ ] What UniSync is and what problem it solves
- [ ] The overall architecture and components
- [ ] How many models, views, and API endpoints exist
- [ ] How authentication works (OTP and OAuth)
- [ ] How real-time messaging works
- [ ] Where to find specific features in the code
- [ ] How to add a new feature
- [ ] How to run the application locally

---

**Status:** ✅ Analysis Complete  
**Date:** 2026-02-09  
**Project:** UniSync / UniSinQ  
**Repository:** https://github.com/Goku0090/uni

---

## 📚 Additional Resources

- [Django Docs](https://docs.djangoproject.com/)
- [Django REST Framework](https://www.django-rest-framework.org/)
- [Django Channels](https://channels.readthedocs.io/)
- [JavaScript WebSocket API](https://developer.mozilla.org/en-US/docs/Web/API/WebSocket)
- [PostgreSQL Docs](https://www.postgresql.org/docs/)

**Happy coding!** 🚀
