# 🎯 UniSync Complete Code Analysis - Start Here

**February 3, 2025**

---

## What You've Got

A comprehensive Django web application (**UniSync**) that helps university students collaborate on projects. Think LinkedIn + GitHub + Slack for students.

---

## 📚 Documentation Created (Read in This Order)

### 1. **QUICK_START_GUIDE_2025.md** (Read First!) ⭐
- **Length:** ~400 lines
- **Time to read:** 10 minutes
- **What you'll learn:** Basic project overview, installation steps, how to test it
- **Best for:** New developers who want to get running quickly

### 2. **COMPREHENSIVE_CODEBASE_ANALYSIS_2025.md**
- **Length:** ~600 lines  
- **Time to read:** 20 minutes
- **What you'll learn:** Complete architecture, all features explained, database schema
- **Best for:** Understanding the overall system

### 3. **API_ENDPOINTS_REFERENCE_2025.md**
- **Length:** ~1000 lines
- **Time to read:** 30 minutes (reference, not sequential)
- **What you'll learn:** Every API endpoint with parameters and responses
- **Best for:** When building frontend or integrating APIs

### 4. **TECHNICAL_STACK_GUIDE_2025.md**
- **Length:** ~500 lines
- **Time to read:** 15 minutes
- **What you'll learn:** Dependencies, setup, deployment, troubleshooting
- **Best for:** Environment setup, dependency management

### 5. **CODEBASE_INDEX_2025.md**
- **Length:** ~700 lines
- **Time to read:** 15 minutes (reference)
- **What you'll learn:** File-by-file breakdown, where to find everything
- **Best for:** Navigating the codebase, finding specific features

---

## 🏗️ Architecture at a Glance

```
┌─────────────────────────────────────┐
│   Frontend (HTML/JS/Bootstrap)       │
│  - 30+ templates in accounts/        │
│  - Custom JS files                   │
└────────────┬────────────────────────┘
             │
┌────────────▼────────────────────────┐
│   Django Backend                     │
│  ├─ 50+ view functions & API classes │
│  ├─ 16+ database models              │
│  ├─ RESTful API endpoints             │
│  └─ Email/social integration         │
└────────────┬────────────────────────┘
             │
┌────────────▼────────────────────────┐
│   Database (PostgreSQL/SQLite)       │
│  - Users, profiles, projects         │
│  - Messages, comments, connections   │
└─────────────────────────────────────┘
```

---

## 🎯 Core Features

| Feature | What It Does | Files |
|---------|-------------|-------|
| **Authentication** | Email/OTP login, social auth (Google/GitHub) | views.py, models.py (OTP) |
| **User Profiles** | Student info, college, skills, interests, photo | models.py (StudentProfile) |
| **Projects** | Create, manage, team, tasks, milestones | models.py (Project*) |
| **Messaging** | Direct messages, group chats, file sharing | chat_api.py, models.py (Message*) |
| **Comments** | Project comments with threading | comment_api.py, models.py (Comment) |
| **Social** | Connect, follow, like, notifications | views.py, models.py (Connection, Follow, Activity) |
| **Discover** | Find collaborators, search projects | views.py (find_collaborators) |

---

## 📂 Key Files (The Most Important)

### Must Know
1. **settings.py** - Django configuration (database, email, security)
2. **models.py** - Database structure (all 16+ models)
3. **views.py** - Main logic for 50+ endpoints
4. **urls.py** - URL routing for entire app

### Important
5. **comment_api.py** - Comment functionality
6. **chat_api.py** - Messaging API
7. **forms.py** - Input validation
8. **templates/base.html** - Base HTML template

### Reference
9. **serializers.py** - DRF serializers for APIs
10. **permissions.py** - Custom access control

---

## 🚀 Quick Start (2 Steps)

### Step 1: Install
```bash
# Clone
git clone https://github.com/Goku0090/uni.git
cd auth_project

# Virtual environment
python -m venv venv
source venv/bin/activate  # or venv\Scripts\activate on Windows

# Install dependencies
pip install -r requirements.txt

# Setup
cp .env.template .env
python manage.py migrate
```

### Step 2: Run
```bash
python manage.py runserver
# Open http://localhost:8000
```

---

## 💾 Database Models (Quick Reference)

```
User Models:
  User → StudentProfile

Project Models:
  Project → ProjectMember, ProjectTask, ProjectMilestone
         → ProjectInvitation
         → Comment, Like

Message Models:
  ChatRoom → ChatRoomMember → User
          → Message → MessageFile, MessageReaction, MessageReadStatus

Social Models:
  Connection, Follow, Like, Activity, Notification, UserStats
```

---

## 🔌 API Endpoints (By Category)

```
Authentication:        /login/, /register/, /verify-otp/
Profiles:              /user-profile/, /student-details/
Projects:              /post-project/, /project-detail/, /like-project/
Comments:              /api/projects/<id>/comments/
Messages:              /api/messages/, /api/chat-rooms/
Connections:           /send-connection/, /accept-connection/
Activity:              /activity-feed/, /notifications/
Collaboration:         /find-collaborators/, /invite-to-team/
```

See **API_ENDPOINTS_REFERENCE_2025.md** for complete list with parameters.

---

## 🛠️ Tech Stack

| Layer | Technology |
|-------|-----------|
| **Framework** | Django 4.2.8 + Django REST Framework 3.14.0 |
| **Database** | PostgreSQL (prod) / SQLite (dev) |
| **Real-time** | Channels + Redis |
| **Auth** | django-allauth (Google, GitHub OAuth) |
| **Email** | Brevo, ZeptoMail, Gmail SMTP |
| **Image** | Pillow |
| **Server** | Gunicorn + WhiteNoise |
| **Frontend** | Bootstrap 5, JavaScript |

Full details: **TECHNICAL_STACK_GUIDE_2025.md**

---

## 🔑 Environment Setup

### Minimal .env for Development
```bash
DEBUG=True
SECRET_KEY=your_secret_key
ALLOWED_HOSTS=localhost,127.0.0.1
# Database and email optional (console email for testing)
```

### Production .env
```bash
DEBUG=False
SECRET_KEY=very_secure_key
ALLOWED_HOSTS=yourdomain.com
DATABASE_URL=postgresql://user:pass@host/db
BREVO_API_KEY=your_key
GOOGLE_CLIENT_ID=your_id
GITHUB_CLIENT_SECRET=your_secret
# ... and 10+ more variables
```

---

## 📊 Project Stats

| Metric | Value |
|--------|-------|
| **Models** | 16+ |
| **Views/APIs** | 50+ |
| **URL Routes** | 100+ |
| **Templates** | 30+ |
| **Python Files** | 40+ |
| **Test Files** | 15+ |
| **Dependencies** | 40+ packages |
| **Lines of Code** | ~10,000+ |

---

## 🎓 What to Do Next

### Day 1: Understand the Basics
- [ ] Read QUICK_START_GUIDE_2025.md
- [ ] Install and run the project locally
- [ ] Create a test account
- [ ] Explore the UI

### Day 2: Understand Architecture
- [ ] Read COMPREHENSIVE_CODEBASE_ANALYSIS_2025.md
- [ ] Read models.py (database structure)
- [ ] Read views.py (page logic)
- [ ] Check out templates/base.html

### Day 3: Know the APIs
- [ ] Read API_ENDPOINTS_REFERENCE_2025.md
- [ ] Test endpoints with curl or Postman
- [ ] Look at comment_api.py and chat_api.py
- [ ] Read urls.py (routing)

### Day 4+: Deep Dives
- [ ] Pick a feature (e.g., messaging)
- [ ] Trace through the code
- [ ] Make a small modification
- [ ] Deploy to Render or Railway

---

## 🐛 Common Tasks

### Add a New Page
1. Create template in `accounts/templates/`
2. Add view function in `views.py`
3. Add URL in `urls.py`

### Add a Database Model
1. Define in `models.py`
2. Run: `python manage.py makemigrations`
3. Run: `python manage.py migrate`

### Send an Email
```python
from django.core.mail import send_mail
send_mail('Subject', 'Message', 'from@example.com', ['to@example.com'])
```

### Create an API Endpoint
1. Add view class in `views.py` or separate file
2. Create serializer in `serializers.py`
3. Add URL in `urls.py`

### Test the Application
```bash
python manage.py test                    # Run all tests
python manage.py shell                   # Interactive Python
python manage.py dbshell                 # Database shell
python manage.py runserver               # Start server
```

---

## ✅ Deployment Checklist

- [ ] Set `DEBUG=False`
- [ ] Configure PostgreSQL
- [ ] Set up email service (Brevo)
- [ ] Configure OAuth (Google/GitHub)
- [ ] Run migrations
- [ ] Collect static files
- [ ] Set up HTTPS
- [ ] Configure allowed hosts
- [ ] Deploy to Render or Railway

---

## 🔐 Security Notes

✅ **Good:**
- Password validators enabled
- CSRF protection
- Session security
- Email verification via OTP
- Allauth for OAuth

⚠️ **Review:**
- REST API set to AllowAny (should have auth)
- OTP stored in plaintext (consider hashing)
- File uploads need validation

---

## 📞 Where to Find Things

| Question | Answer |
|----------|--------|
| How does login work? | views.py (login_view), models.py (OTP) |
| How are projects created? | views.py (post_project), templates/edit_project.html |
| How does messaging work? | chat_api.py, models.py (Message, ChatRoom) |
| How are comments displayed? | comment_api.py, templates/project_detail.html |
| How is email sent? | brevo_mail_backend.py, settings.py |
| What's the database structure? | models.py (all models defined there) |
| What APIs are available? | urls.py (all routes), API_ENDPOINTS_REFERENCE_2025.md |
| How to add a new feature? | See "Common Tasks" section above |

---

## 🎯 Your First Task Ideas

### Easy (1-2 hours)
- [ ] Add a new field to StudentProfile (e.g., "website")
- [ ] Create a simple static page (privacy policy, about)
- [ ] Add a new template filter

### Medium (2-4 hours)
- [ ] Create a new API endpoint for user statistics
- [ ] Add filtering to the projects feed
- [ ] Implement project search

### Hard (4+ hours)
- [ ] Build a real-time notifications system
- [ ] Create an admin dashboard for moderators
- [ ] Implement project recommendations

---

## 📚 External Resources

| Topic | Resource |
|-------|----------|
| Django | https://docs.djangoproject.com/ |
| DRF | https://www.django-rest-framework.org/ |
| Channels | https://channels.readthedocs.io/ |
| PostgreSQL | https://www.postgresql.org/docs/ |
| Bootstrap | https://getbootstrap.com/docs/ |
| Render | https://render.com/docs/ |
| Railway | https://docs.railway.app/ |

---

## 💡 Pro Tips

1. **Use virtual environment always:** Prevents dependency conflicts
2. **Check migrations:** `python manage.py showmigrations`
3. **Use Django shell:** `python manage.py shell` for testing
4. **Format code:** `black accounts/` before commits
5. **Check logs:** `tail -f logs/django.log` for debugging
6. **Test endpoints:** Use Postman or curl to test APIs
7. **Read docstrings:** Functions have documentation
8. **Debug with breakpoints:** Use `pdb.set_trace()` or IDE debugger

---

## 🎓 Learning Outcomes

After working through the documentation and codebase, you'll understand:

✅ How a full-stack Django application is structured  
✅ How to implement authentication (email + OTP + OAuth)  
✅ How to build REST APIs with Django  
✅ How to manage complex relationships in databases  
✅ How to implement real-time features (Channels)  
✅ How to integrate external services (email, OAuth)  
✅ How to deploy to cloud platforms  
✅ How to write tests and maintain code quality

---

## 🚀 Ready to Start?

### Read in This Order:
1. **QUICK_START_GUIDE_2025.md** ← Start here
2. **COMPREHENSIVE_CODEBASE_ANALYSIS_2025.md**
3. **CODEBASE_INDEX_2025.md** (reference)
4. **API_ENDPOINTS_REFERENCE_2025.md** (reference)
5. **TECHNICAL_STACK_GUIDE_2025.md**

### Then:
- Install the project locally
- Create a test account
- Explore the UI
- Read the code
- Make a small change
- Deploy it

---

## 📝 Document Overview

| Document | Lines | Time | Focus |
|----------|-------|------|-------|
| QUICK_START_GUIDE_2025.md | ~400 | 10 min | Getting started |
| COMPREHENSIVE_CODEBASE_ANALYSIS_2025.md | ~600 | 20 min | Architecture |
| API_ENDPOINTS_REFERENCE_2025.md | ~1000 | 30 min | API reference |
| TECHNICAL_STACK_GUIDE_2025.md | ~500 | 15 min | Setup/deployment |
| CODEBASE_INDEX_2025.md | ~700 | 15 min | Navigation |
| **TOTAL** | **~3200 lines** | **~90 min** | Complete guide |

---

## ❓ FAQ

**Q: Is this production-ready?**
A: Mostly yes, but review security notes above. Add error tracking (Sentry), set up HTTPS, and configure proper database backups.

**Q: Can I deploy this?**
A: Yes! See TECHNICAL_STACK_GUIDE_2025.md for Render/Railway deployment steps.

**Q: How do I add a new feature?**
A: 1) Update models.py if needed, 2) Run migrations, 3) Add view/API endpoint, 4) Create template, 5) Add URL route, 6) Test

**Q: What if something breaks?**
A: Check error logs, use Django shell to debug, look at similar working code, test with `python manage.py check`

**Q: How do I contribute?**
A: Fork repo, create branch, make changes, test, push, create pull request.

---

## 🎉 Summary

You now have:
- ✅ Complete understanding of the codebase
- ✅ 5 comprehensive documentation files
- ✅ API reference for all endpoints
- ✅ Setup guide for local development
- ✅ Deployment instructions
- ✅ Common tasks and solutions

**Next Step:** Open **QUICK_START_GUIDE_2025.md** and start building!

---

**Last Updated:** February 3, 2025  
**Project:** UniSync - Student Collaboration Platform  
**Repository:** https://github.com/Goku0090/uni
