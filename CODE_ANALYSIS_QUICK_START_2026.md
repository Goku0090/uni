# Code Analysis Quick Start Guide
## UniSync Platform - Implementation & Usage

**Status:** Complete & Production-Ready  
**Last Updated:** February 9, 2026

---

## 📋 Executive Summary

This document provides a quick reference for the complete Django + WebSocket application. It covers:

- **What the code does** (15 seconds)
- **How it's organized** (2 minutes)
- **Key components** (5 minutes)
- **How to run it** (3 minutes)
- **How to extend it** (5 minutes)

Total: ~30 minutes to understand everything

---

## 🎯 What This Code Does (15 seconds)

UniSync is a **collaborative project platform** where:

1. **Users create projects** and find collaborators
2. **Teams manage projects** with real-time updates
3. **Users interact socially** (comments, likes, follows)
4. **Everything updates in real-time** via WebSocket
5. **Authentication** via email OTP or OAuth (Google/GitHub)

---

## 📁 Code Organization (2 minutes)

```
Project Root: e:/login/auth_project/

MAIN FOLDERS:
├── auth_project/           Settings & configuration
├── accounts/               Main application code
├── media/                  User uploads (photos)
├── static/                 CSS, JS, images
└── templates/              HTML files

KEY FILES (READ IN THIS ORDER):
1. auth_project/settings.py  ← Configuration (30 min read)
2. auth_project/asgi.py      ← WebSocket setup (5 min)
3. accounts/models.py         ← Database structure (45 min)
4. accounts/views.py          ← Business logic (60 min)
5. accounts/consumers.py      ← Real-time features (20 min)
6. accounts/urls.py           ← URL routing (10 min)
7. accounts/serializers.py    ← API responses (10 min)
```

---

## 🧩 Key Components Explained

### 1. Models (Database Structure)
**File:** `accounts/models.py`  
**What:** Defines all database tables

**Key Models:**
- **StudentProfile**: User profiles with skills, interests, photos
- **Project**: Projects users create
- **Comment**: Comments on projects
- **Message**: Direct messages & group chats
- **Like**: User likes on projects
- **Follow**: User following system
- **Activity**: User activity feed
- **OTP**: One-time passwords for authentication

**Quick Example:**
```python
# A project in the database looks like:
project = Project.objects.create(
    title="AI Chat App",                    # Project name
    description="Real-time chat with AI",   # What it does
    owner=request.user,                     # Who created it
    technologies=["Python", "Django"],      # Tech used
    looking_for=["Frontend Dev"],           # What they need
)
```

### 2. Views (Business Logic)
**File:** `accounts/views.py`  
**What:** Handles user requests and returns responses

**Key Views:**
- **login/logout**: Authentication
- **student_profile**: View user profile
- **projects_feed**: List all projects
- **project_detail**: Show project details
- **like_project**: Like/unlike functionality
- **messages_page**: Messaging system
- **create_project**: Create new project

**Quick Example:**
```python
@login_required  # User must be logged in
def projects_feed(request):
    projects = Project.objects.all()  # Get all projects
    return render(request, 'projects.html', {
        'projects': projects  # Send to template
    })
```

### 3. WebSocket Consumers (Real-time Features)
**File:** `accounts/consumers.py`  
**What:** Handles real-time WebSocket connections

**Key Consumers:**
- **ProjectUpdateConsumer**: Real-time project updates
- **ActivityFeedConsumer**: Live activity feed
- **NotificationConsumer**: Push notifications

**How It Works:**
```
User opens browser
    ↓
Browser connects to WebSocket: ws://localhost:8000/ws/project/2/
    ↓
Consumer.connect() called
    ↓
Adds user to broadcast group
    ↓
When project updates: consumer sends update to all connected users
    ↓
All browsers update instantly (no page refresh needed)
```

### 4. Serializers (API Format)
**File:** `accounts/serializers.py`  
**What:** Converts database objects to JSON

**Key Serializers:**
- **UserProfileSerializer**: User profile as JSON
- **ProjectSerializer**: Project as JSON
- **CommentSerializer**: Comment as JSON
- **MessageSerializer**: Message as JSON

**Example:**
```python
# Database object
project = Project.objects.get(id=1)

# Convert to JSON
serializer = ProjectSerializer(project)
return JsonResponse(serializer.data)

# Output:
{
    "id": 1,
    "title": "AI Chat App",
    "description": "...",
    "owner": {...},
    "created_at": "2026-02-09T10:00:00Z"
}
```

### 5. URLs (Routing)
**File:** `accounts/urls.py`  
**What:** Maps URLs to views

**HTTP Routes:**
```
/accounts/login/              → login_view
/accounts/projects/           → projects_feed
/accounts/projects/2/         → project_detail
/accounts/projects/2/like/    → like_project
/api/projects/                → ProjectListView (API)
```

**WebSocket Routes:**
```
/ws/project/2/                → ProjectUpdateConsumer
/ws/activity-feed/            → ActivityFeedConsumer
/ws/notifications/            → NotificationConsumer
```

---

## 🚀 How to Run It (3 minutes)

### Option 1: Quick Start (5 minutes)
```bash
# 1. Navigate to project
cd e:\login\auth_project

# 2. Activate virtual environment
source venv/bin/activate  # Mac/Linux
# OR
venv\Scripts\activate     # Windows

# 3. Install dependencies
pip install -r requirements.txt

# 4. Run migrations (setup database)
python manage.py migrate

# 5. Start server with WebSocket support
daphne -b 127.0.0.1 -p 8000 auth_project.asgi:application

# 6. Open browser
# Go to: http://localhost:8000
```

### Option 2: Using Startup Script (2 minutes)

**Windows:**
```bash
cd e:\login
run_daphne.bat
# Opens at http://localhost:8000
```

**Mac/Linux:**
```bash
cd e:/login
bash run_daphne.sh
# Opens at http://localhost:8000
```

### Test WebSocket (1 minute)
```javascript
// Open browser console (F12)
// Paste this:
let socket = new WebSocket("ws://localhost:8000/ws/project/2/");
socket.onopen = () => console.log("✅ WebSocket Connected!");
socket.onerror = (e) => console.log("❌ Error:", e);
```

---

## 🔧 How to Extend It (5 minutes)

### Add a New Feature (Step-by-Step)

#### Example: Add a "Rating" feature for projects

**Step 1: Create Model**
```python
# In accounts/models.py, add:
class ProjectRating(models.Model):
    project = models.ForeignKey(Project, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    rating = models.IntegerField(choices=[(i, str(i)) for i in range(1, 6)])
    review = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        unique_together = ['project', 'user']
```

**Step 2: Create Migration**
```bash
python manage.py makemigrations
python manage.py migrate
```

**Step 3: Create Serializer**
```python
# In accounts/serializers.py, add:
class ProjectRatingSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProjectRating
        fields = ['id', 'rating', 'review', 'created_at']
```

**Step 4: Create View**
```python
# In accounts/views.py, add:
@login_required
def rate_project(request, project_id):
    project = get_object_or_404(Project, id=project_id)
    if request.method == 'POST':
        rating = request.POST.get('rating')
        review = request.POST.get('review')
        ProjectRating.objects.update_or_create(
            project=project,
            user=request.user,
            defaults={'rating': rating, 'review': review}
        )
        return redirect('project_detail', id=project_id)
```

**Step 5: Add URL**
```python
# In accounts/urls.py, add:
path('projects/<int:project_id>/rate/', rate_project, name='rate_project'),
```

**Step 6: Update Template**
```html
<!-- In template, add: -->
<form method="POST" action="{% url 'rate_project' project.id %}">
    {% csrf_token %}
    <select name="rating">
        <option>Rate this project...</option>
        <option value="1">1 Star</option>
        <option value="5">5 Stars</option>
    </select>
    <textarea name="review"></textarea>
    <button type="submit">Submit Rating</button>
</form>
```

---

## 🔐 Authentication Flow

### Email + OTP Login
```
User enters email
    ↓ (accounts/views.py)
Generate 6-digit OTP
    ↓
Send via email (Brevo/ZeptoMail)
    ↓
User enters OTP in form
    ↓ (accounts/models.py - OTP.verify_otp())
Verify OTP (must not be expired)
    ↓
Create session
    ↓
Redirect to dashboard
```

### Google OAuth Login
```
User clicks "Login with Google"
    ↓
Redirected to Google login
    ↓ (allauth library)
User grants permission
    ↓
Google redirects to callback URL
    ↓ (accounts/views.py - oauth_callback)
Get user info from Google
    ↓
Create/update user in database
    ↓
Create session
    ↓
Redirect to dashboard
```

---

## 💾 Database Structure (Quick Lookup)

### Most Important Tables

| Table | Columns | Purpose |
|-------|---------|---------|
| User | id, username, email, password | Django built-in user |
| StudentProfile | user_id, full_name, skills, bio, profile_photo | Extended profile |
| Project | id, title, description, owner_id, technologies | Projects |
| Comment | id, content, user_id, project_id, created_at | Project comments |
| Message | id, content, sender_id, receiver_id, created_at | Direct messages |
| ChatRoom | id, name, members (M2M) | Group chats |
| Like | id, user_id, project_id | Project likes |
| Follow | id, follower_id, following_id | User follows |
| Activity | id, user_id, activity_type, created_at | Activity feed |
| Notification | id, user_id, content, is_read | Notifications |

---

## 🌐 API Reference (Quick Lookup)

### Common Endpoints

```
# Projects
GET    /api/projects/                 List all projects
POST   /api/projects/                 Create project
GET    /api/projects/<id>/            Get project details
PUT    /api/projects/<id>/            Update project
DELETE /api/projects/<id>/            Delete project

# Users
GET    /api/users/<id>/               Get user profile
PUT    /api/users/<id>/               Update profile
GET    /api/users/<id>/projects/      Get user's projects

# Comments
GET    /api/projects/<id>/comments/   Get project comments
POST   /api/projects/<id>/comments/   Create comment

# Messages
GET    /api/messages/                 List conversations
POST   /api/messages/                 Send message
GET    /api/messages/<id>/            Get conversation

# Likes
POST   /api/projects/<id>/like/       Like project
DELETE /api/projects/<id>/like/       Unlike project

# WebSocket
WS     /ws/project/<id>/              Real-time project updates
WS     /ws/activity-feed/             Real-time activity
WS     /ws/notifications/             Real-time notifications
```

---

## 📊 Performance Tips

### Database Optimization
```python
# ❌ BAD: Multiple queries (N+1 problem)
for project in Project.objects.all():
    print(project.owner.name)  # Extra query for each project!

# ✅ GOOD: Single query with join
projects = Project.objects.select_related('owner')
for project in projects:
    print(project.owner.name)  # No extra queries
```

### Caching
```python
# ✅ Cache frequently accessed data
from django.views.decorators.cache import cache_page

@cache_page(60 * 5)  # Cache for 5 minutes
def projects_feed(request):
    return render(request, 'projects.html')
```

### Pagination
```python
# ✅ Don't load all 10,000 projects at once
from django.core.paginator import Paginator

paginator = Paginator(Project.objects.all(), 10)  # 10 per page
page = paginator.get_page(request.GET.get('page'))
```

---

## 🐛 Debugging Tips

### Enable Query Logging
```python
# In settings.py
LOGGING = {
    'version': 1,
    'handlers': {
        'console': {'class': 'logging.StreamHandler'},
    },
    'loggers': {
        'django.db.backends': {
            'handlers': ['console'],
            'level': 'DEBUG',
        }
    }
}
```

### Common Errors

**Error: "404 Not Found" on WebSocket**
```
Cause: Using Django runserver instead of Daphne
Solution: Use: daphne -b 127.0.0.1 -p 8000 auth_project.asgi:application
```

**Error: "CSRF Token mismatch"**
```
Cause: Missing {% csrf_token %} in form
Solution: Add: {% csrf_token %} in all forms
```

**Error: "User not found"**
```
Cause: User not logged in
Solution: Add @login_required decorator or check request.user.is_authenticated
```

---

## 📚 Documentation Files

| File | Purpose | Read Time |
|------|---------|-----------|
| COMPREHENSIVE_CODE_ANALYSIS_FINAL_2026.md | Full deep-dive | 2 hours |
| CODE_ANALYSIS_QUICK_START_2026.md | This file | 30 min |
| WEBSOCKET_DETAILED_ANALYSIS.md | WebSocket only | 1 hour |
| 00_WEBSOCKET_FIX_START_HERE.md | WebSocket setup | 10 min |
| COMPLETE_SOLUTION_SUMMARY.txt | Quick overview | 5 min |

---

## ✅ Development Checklist

### Before Starting
- [ ] Python 3.8+ installed
- [ ] Git installed
- [ ] PostgreSQL installed (optional, SQLite works for dev)
- [ ] Code editor (VS Code recommended)

### Initial Setup
- [ ] Clone repository
- [ ] Create virtual environment
- [ ] Install requirements.txt
- [ ] Copy .env.template to .env
- [ ] Run migrations
- [ ] Create superuser

### Development
- [ ] Start Daphne server
- [ ] Create models
- [ ] Create migrations
- [ ] Create views
- [ ] Create serializers
- [ ] Add URLs
- [ ] Create templates
- [ ] Test locally
- [ ] Commit to Git

### Deployment
- [ ] All tests pass
- [ ] No console errors
- [ ] No unhandled exceptions
- [ ] Environment variables set
- [ ] Push to GitHub
- [ ] Render/Railway auto-deploys

---

## 🚀 Next Steps

1. **Start the server** (see "How to Run It" section)
2. **Explore the interface** at http://localhost:8000
3. **Read COMPREHENSIVE_CODE_ANALYSIS_FINAL_2026.md** for deep understanding
4. **Add a feature** (see "How to Extend It" section)
5. **Deploy to production** (Render or Railway)

---

## 📞 Quick Help

**Q: How do I start the server?**
A: `daphne -b 127.0.0.1 -p 8000 auth_project.asgi:application`

**Q: How do I add a new feature?**
A: Model → Migration → Serializer → View → URL → Template

**Q: How do I test WebSocket?**
A: Browser console: `let socket = new WebSocket("ws://localhost:8000/ws/project/2/");`

**Q: How do I deploy?**
A: Push to GitHub → Render/Railway auto-deploys

**Q: What if something breaks?**
A: Check logs, revert last commit, ask for help

---

## 📖 Code References

### Key Files
```
accounts/models.py          15+ database models (718 lines)
accounts/views.py           Views & logic (3,462 lines)
accounts/consumers.py       WebSocket consumers (434 lines)
accounts/serializers.py     API serialization (150+ lines)
accounts/urls.py            URL routing (100+ lines)
accounts/forms.py           Form validation (100+ lines)
auth_project/settings.py    Configuration (500+ lines)
auth_project/asgi.py        WebSocket setup (50 lines)
```

### Most Important Functions
```
models.StudentProfile()          User profiles
models.Project()                 Projects
models.Message()                 Messaging
models.Comment()                 Comments
models.OTP.generate_otp()        Generate OTP
models.OTP.verify_otp()          Verify OTP
consumers.ProjectUpdateConsumer  Real-time updates
views.login_view()               Login
views.projects_feed()            Project list
views.project_detail()           Project detail
```

---

## Summary

This is a **complete Django + WebSocket application** with:

✅ User authentication (email + OAuth)
✅ Project management system
✅ Social features (comments, likes, follows)
✅ Real-time updates (WebSocket)
✅ Messaging system
✅ Activity feeds
✅ Production-ready (error handling, logging, caching)
✅ Fully documented

**Total code:** ~5,000 lines of Python/JavaScript  
**Total documentation:** 50+ pages  
**Total features:** 20+ major features  
**Total time to learn:** ~2 hours  

**Ready to:**
- ✅ Run locally
- ✅ Extend with new features
- ✅ Deploy to production
- ✅ Monitor and maintain

---

## Generated: February 9, 2026
Status: Complete & Production-Ready

For detailed analysis, see: COMPREHENSIVE_CODE_ANALYSIS_FINAL_2026.md
