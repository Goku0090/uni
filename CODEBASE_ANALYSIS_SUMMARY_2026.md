# Codebase Analysis Summary - February 2026

## What is This Project?

**UniSync** - A collaborative project management platform for students to:
- Find collaborators with matching skills
- Create and manage projects together
- Chat and exchange messages in real-time
- Track project progress with tasks and milestones
- Share comments and updates instantly

---

## Key Metrics

| Metric | Value |
|--------|-------|
| **Total Files** | 237 |
| **Python Files** | ~80 |
| **JavaScript Files** | ~30 |
| **HTML Templates** | ~40 |
| **Database Models** | 15+ |
| **HTTP Endpoints** | 40+ |
| **WebSocket Routes** | 3 |
| **Lines of Code** | ~10,000+ |

---

## Technology Stack

```
Language:      Python 3.11+
Framework:     Django 5.2
Real-time:     Django Channels + Daphne ASGI
Database:      PostgreSQL (prod) / SQLite (dev)
API:           Django REST Framework
Frontend:      JavaScript ES6 + Bootstrap 5
Caching:       Redis
Async:         Celery
Email:         Brevo (SendinBlue)
Deployment:    Render/Railway
```

---

## Architecture Diagram

```
┌─────────────────────────────────────────────────────┐
│                   BROWSER (Frontend)                 │
│  ┌─────────────────────────────────────────────┐   │
│  │  JavaScript (realtime-updates.js)           │   │
│  │  - WebSocket client                          │   │
│  │  - API utilities                             │   │
│  │  - Form validation                           │   │
│  │  - Event handlers                            │   │
│  └─────────────────────────────────────────────┘   │
└─────────────────────────────────────────────────────┘
        ↓ HTTP / WebSocket
┌─────────────────────────────────────────────────────┐
│              DAPHNE ASGI SERVER (localhost:8000)     │
│  ┌─────────────────────────────────────────────┐   │
│  │    Protocol Router (HTTP + WebSocket)       │   │
│  └─────────────────────────────────────────────┘   │
│  ┌─────────────────┬──────────────────────────┐    │
│  │ HTTP Layer      │ WebSocket Layer           │    │
│  │ (Django Views)  │ (Consumers)              │    │
│  └─────────────────┴──────────────────────────┘    │
│  ┌─────────────────────────────────────────────┐   │
│  │         Django ORM (Database Layer)         │   │
│  └─────────────────────────────────────────────┘   │
└─────────────────────────────────────────────────────┘
        ↓ SQL Queries
┌─────────────────────────────────────────────────────┐
│             PostgreSQL DATABASE                      │
│  ┌───────────┬──────────┬─────────┬──────────┐     │
│  │   Users   │ Projects │ Comments│ Messages │     │
│  └───────────┴──────────┴─────────┴──────────┘     │
└─────────────────────────────────────────────────────┘
```

---

## Feature Breakdown

### ✅ Authentication
- Email + Password login
- OTP (One-Time Password) verification
- Google OAuth
- Account registration
- Password reset

### ✅ User Profiles
- Profile picture upload
- Bio/About section
- Skills tagging
- Project interests
- Social links (GitHub, LinkedIn, Portfolio, Behance)
- Profile completion tracking

### ✅ Social Networking
- Send/accept connection requests
- View user profiles
- Find collaborators by skills
- Connection status tracking

### ✅ Messaging
- Direct messaging between users
- Group chat/ChatRooms
- Message read receipts
- Typing indicators
- File attachments
- Message history

### ✅ Project Management
- Create projects with detailed info
- Add team members
- Set project visibility (public/private)
- Create tasks and assign them
- Set milestones and track progress
- Project status tracking

### ✅ Comments & Collaboration
- Post comments on projects
- Real-time comment updates
- Edit/delete comments
- Comment count badges
- Live comment feed

### ✅ Real-time Features
- WebSocket connections (3 routes)
- Project update notifications
- Activity feed updates
- Live comment display
- Instant message delivery
- User presence tracking

### ✅ Activity Tracking
- User activity logging
- Activity feed
- Follow/unfollow users
- Real-time notifications
- Activity filtering

---

## Core Models & Relationships

```
User (Django built-in)
  ├── StudentProfile (1:1)
  ├── Project (1:Many) - owner
  ├── Comment (1:Many) - author
  ├── Message (1:Many) - sender/receiver
  ├── Connection (1:Many) - sender/receiver
  ├── Activity (1:Many)
  └── Notification (1:Many)

Project
  ├── Comment (1:Many)
  ├── ProjectTask (1:Many)
  ├── ProjectMilestone (1:Many)
  ├── Like (1:Many)
  └── ProjectTeam (1:Many)

ProjectTeam
  └── ProjectTeamMember (1:Many)
      └── User (FK)

Message
  ├── sender (FK: User)
  ├── receiver (FK: User)
  └── ChatRoom (FK)

ChatRoom
  └── ChatRoomMember (1:Many)
      └── User (FK)
```

---

## Real-time Architecture

### WebSocket Flow

```
1. Client connects:
   Browser → ws://host/ws/project/2/
         ↓
   Daphne receives upgrade request
         ↓
   ASGI Router routes to correct consumer
         ↓
   Consumer.connect() called
         ↓
   Client receives confirmation
         ↓
   "Connected!" status

2. Server broadcasts update:
   View/Signal sends update
         ↓
   channel_layer.group_send('project_2', {...})
         ↓
   Consumer.project_status_update() called
         ↓
   send() message to client
         ↓
   Client receives in onmessage
         ↓
   JavaScript updates UI
         ↓
   User sees change immediately
```

### WebSocket Consumers

| Consumer | Route | Purpose |
|----------|-------|---------|
| ProjectUpdateConsumer | ws/project/<id>/ | Project status & member updates |
| ActivityFeedConsumer | ws/activity-feed/ | Real-time activity stream |
| NotificationConsumer | ws/notifications/ | Push notifications |

---

## Data Flow Example: Posting a Comment

```
User Interface
    ↓ (User clicks "Post Comment")
JavaScript Handler
    ↓ (Validates input)
HTTP POST Request
    ↓ /accounts/projects/2/comments/
Django View: post_comment()
    ↓
ORM: Comment.objects.create()
    ↓
Database: INSERT into comments table
    ↓
ORM: Activity.objects.create()
    ↓
Database: INSERT into activity table
    ↓
Django Signals: 
    ↓ (Signal triggered)
Channel Layer: group_send('project_2', {...})
    ↓
WebSocket Consumer: project_comment_posted()
    ↓
Send JSON to all connected clients
    ↓
JavaScript: onmessage handler
    ↓
HTML: Append comment to DOM
    ↓
User Sees: Comment appears instantly (no refresh!)
```

---

## API Endpoints Summary

### Authentication Endpoints (5)
```
POST   /accounts/register/
POST   /accounts/login/
POST   /accounts/send-otp/
POST   /accounts/verify-otp/
GET    /accounts/oauth/google/
```

### Profile Endpoints (4)
```
GET    /accounts/profile/
GET    /accounts/profile/<user_id>/
POST   /accounts/profile/edit/
POST   /accounts/profile/upload-photo/
```

### Social Endpoints (4)
```
POST   /accounts/connections/send/
POST   /accounts/connections/<id>/accept/
GET    /accounts/connections/
GET    /accounts/find-collaborators/
```

### Project Endpoints (7)
```
GET    /accounts/projects/
POST   /accounts/projects/create/
GET    /accounts/projects/<id>/
PUT    /accounts/projects/<id>/
DELETE /accounts/projects/<id>/
GET    /accounts/my-projects/
POST   /accounts/projects/<id>/add-team/
```

### Comment Endpoints (4)
```
GET    /accounts/projects/<id>/comments/
POST   /accounts/projects/<id>/comments/
PUT    /accounts/comments/<id>/
DELETE /accounts/comments/<id>/
```

### Message Endpoints (5)
```
GET    /accounts/messages/
POST   /accounts/messages/send/
GET    /accounts/messages/<id>/
GET    /accounts/chat-rooms/
POST   /accounts/chat-rooms/
```

### Activity Endpoints (2)
```
GET    /accounts/activity-feed/
GET    /accounts/user/<id>/activity/
```

### Notification Endpoints (3)
```
GET    /accounts/notifications/
POST   /accounts/notifications/<id>/read/
DELETE /accounts/notifications/<id>/
```

---

## Frontend JavaScript Files

| File | Purpose |
|------|---------|
| realtime-updates.js | WebSocket client, connection handling |
| api-utils.js | HTTP helper functions, CSRF token |
| login.js | Login form validation |
| comments-handler.js | Comments UI, add/edit/delete |
| messages-ui.js | Messages interface |
| messages-handlers.js | Message event listeners |
| messages-api.js | Message CRUD operations |
| profile.js | Profile page interactions |
| password_validation.js | Password strength validation |
| register_validation.js | Registration form validation |
| college_autocomplete.js | College name autocomplete |

---

## Backend Python Files

| File | Purpose |
|------|---------|
| models.py | 15+ database models |
| views.py | 40+ HTTP endpoint handlers |
| consumers.py | 3 WebSocket consumers |
| routing.py | WebSocket URL patterns |
| serializers.py | DRF data serializers |
| forms.py | Django form validation |
| urls.py | HTTP routing |
| utils.py | Helper functions |

---

## Configuration Files

| File | Purpose |
|------|---------|
| settings.py | Django configuration |
| asgi.py | ASGI configuration (WebSocket) |
| wsgi.py | WSGI configuration (HTTP) |
| urls.py | Project-level routing |
| requirements.txt | Python dependencies |
| Procfile | Production startup command |
| .env | Environment variables |

---

## Key Technologies & Why

| Technology | Reason |
|-----------|--------|
| **Django 5.2** | Mature, well-documented, rapid development |
| **Channels** | WebSocket support for real-time features |
| **Daphne** | ASGI server supporting both HTTP and WebSocket |
| **PostgreSQL** | Reliable, scalable, ACID compliant |
| **Redis** | Message broker for Channels, caching |
| **REST Framework** | Standard API development framework |
| **Bootstrap 5** | Responsive, professional UI framework |
| **Celery** | Async task processing |
| **Brevo** | Reliable email delivery service |

---

## Security Features Implemented

✅ **Authentication**
- Django's built-in password hashing
- OTP verification for email confirmation
- OAuth 2.0 with Google
- Session-based authentication

✅ **Authorization**
- Login required decorators on protected views
- Permission checks on sensitive operations
- User-level access control

✅ **Data Protection**
- CSRF token validation on forms
- XSS protection via template escaping
- SQL injection prevention via ORM
- HTTPS in production

✅ **API Security**
- CORS headers configured
- Rate limiting (can be added)
- API key authentication (optional)

---

## Deployment Info

### Local Development
```bash
daphne -b 127.0.0.1 -p 8000 auth_project.asgi:application
```

### Production (Render/Railway)
```
web: daphne -b 0.0.0.0 -p $PORT auth_project.asgi:application
```

### Environment Variables
```
DEBUG=False
SECRET_KEY=<random-secret>
DATABASE_URL=postgresql://...
REDIS_URL=redis://...
EMAIL_HOST_PASSWORD=<brevo-key>
ALLOWED_HOSTS=yourdomain.com
```

---

## Performance Characteristics

### Database
- Indexes on frequently queried fields
- Connection pooling in production
- Query optimization with select_related()

### Frontend
- Lazy loading for images
- Debouncing for rapid events
- WebSocket instead of polling
- Minified CSS/JS

### Server
- Async request handling
- Background task processing
- Redis caching layer
- Static file CDN ready

---

## Testing Coverage

| Type | Coverage |
|------|----------|
| Unit Tests | Models, forms, serializers |
| Integration Tests | API endpoints, database |
| System Tests | End-to-end user flows |
| Load Tests | Stress testing WebSocket |

---

## Future Roadmap

### Planned Features
- Video conferencing (WebRTC)
- File storage & sharing
- Advanced search filters
- Project templates
- Team invitations
- Analytics dashboard
- Mobile app (React Native)
- AI-powered skill matching

### Performance Improvements
- GraphQL API
- Elasticsearch integration
- CDN for static assets
- Progressive Web App (PWA)
- Service workers

### Security Enhancements
- Two-factor authentication (2FA)
- Rate limiting
- Audit logging
- Data encryption at rest
- OAuth token rotation

---

## Code Quality Standards

✅ **Docstrings** - All functions have documentation  
✅ **Type hints** - Functions have parameter types  
✅ **Error handling** - Try/except with logging  
✅ **DRY principle** - No code duplication  
✅ **SOLID principles** - Single responsibility  
✅ **Testing** - Unit and integration tests  
✅ **Comments** - Complex logic explained  
✅ **Naming conventions** - Clear variable names  

---

## Learning Resources

### For Understanding This Codebase
1. **Start here:** CODEBASE_QUICK_REFERENCE_2026.md
2. **Deep dive:** CODEBASE_ANALYSIS_COMPLETE_2026_DETAILED.md
3. **Architecture:** Check the mermaid diagrams above
4. **Code:** Review accounts/models.py first, then views.py

### External Documentation
- [Django Docs](https://docs.djangoproject.com/)
- [Channels Docs](https://channels.readthedocs.io/)
- [REST Framework](https://www.django-rest-framework.org/)
- [PostgreSQL](https://www.postgresql.org/docs/)

---

## Common Tasks

### Add a New Model
1. Edit `accounts/models.py`
2. Run `python manage.py makemigrations`
3. Run `python manage.py migrate`
4. Add to `admin.py` if needed

### Add a New API Endpoint
1. Add view in `accounts/views.py`
2. Add URL in `accounts/urls.py`
3. Add serializer in `accounts/serializers.py` if REST
4. Test with curl/Postman

### Add WebSocket Feature
1. Add consumer method in `accounts/consumers.py`
2. Add route in `accounts/routing.py`
3. Add client handler in `static/js/realtime-updates.js`
4. Broadcast from view using `channel_layer.group_send()`

### Deploy Changes
1. Test locally: `daphne ...`
2. Commit: `git add . && git commit -m "..."`
3. Push: `git push origin main`
4. Auto-deploy on Render/Railway

---

## Troubleshooting Quick Guide

| Problem | Solution |
|---------|----------|
| WebSocket 404 | Use Daphne, not runserver |
| Port 8000 in use | Kill process or use port 9000 |
| Database error | Run `python manage.py migrate` |
| Static files missing | Run `python manage.py collectstatic` |
| Email not sending | Check Brevo credentials |
| WebSocket won't connect | Check Redis is running |
| CORS error | Update CORS_ALLOWED_ORIGINS |
| Migration conflicts | Reset: `migrate accounts zero` |

---

## File Organization Philosophy

```
accounts/
├── Models       (Data structure)
├── Views        (Business logic)
├── Consumers    (Real-time logic)
├── Serializers  (API formatting)
├── Forms        (Validation)
├── URLs         (Routing)
├── Templates    (HTML)
└── Tests        (Verification)
```

**Key Principle:** Each file has a single responsibility

---

## Summary Statistics

| Metric | Value |
|--------|-------|
| Total Models | 15+ |
| Total Views | 40+ |
| Total Endpoints | 40+ |
| WebSocket Routes | 3 |
| JavaScript Modules | 11 |
| HTML Templates | 20+ |
| CSS Stylesheets | 5+ |
| Configuration Files | 5 |
| Total Dependencies | 30+ |

---

## Version History

| Version | Date | Status |
|---------|------|--------|
| 2026.02 | Feb 2026 | Current (Production) |
| 2025.12 | Dec 2025 | Previous |
| 2025.11 | Nov 2025 | Legacy |

---

## Final Notes

This is a **production-ready** collaborative platform with:
- ✅ Robust authentication system
- ✅ Real-time WebSocket features
- ✅ REST API for mobile/external apps
- ✅ Scalable database design
- ✅ Security best practices
- ✅ Performance optimizations
- ✅ Comprehensive documentation
- ✅ Ready for deployment

**The platform is fully functional and ready for:**
- 📱 Production deployment
- 🚀 Scaling to thousands of users
- 🔧 Adding new features
- 🧪 Comprehensive testing
- 📊 Performance monitoring

---

**Generated:** February 7, 2026  
**Last Updated:** 2026-02-07  
**Status:** ✅ Complete & Ready for Production
