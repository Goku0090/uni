# UniSync Codebase Analysis - Executive Summary

**Analysis Date:** January 29, 2026  
**Project:** UniSync - Collaborative Learning Platform  
**Repository:** https://github.com/Goku0090/uni  
**Technology Stack:** Django 4.2.8 + PostgreSQL/SQLite + DRF

---

## Quick Facts

| Metric | Value |
|--------|-------|
| **Main Language** | Python (Django) |
| **Framework** | Django 4.2.8 |
| **API Framework** | Django REST Framework |
| **Database** | PostgreSQL (prod) / SQLite (dev) |
| **Authentication** | OTP + Social OAuth (Google/GitHub) |
| **Email Backends** | Brevo, ZeptoMail, Gmail SMTP, Console |
| **Real-time** | Channels (WebSockets) |
| **Task Queue** | Celery |
| **Caching** | Redis |
| **File Storage** | Local + S3 (boto3) |
| **Lines of Code (Views)** | ~3,193 |
| **Database Models** | 20+ |
| **URL Routes** | 100+ |
| **API Endpoints** | 20+ |
| **Django Apps** | 1 (accounts) |

---

## What This Platform Does

**UniSync** enables:

1. **User Collaboration**
   - Register with email/OTP or social login
   - Create detailed profiles with skills & interests
   - Search for collaborators by skills/interests

2. **Project Management**
   - Create projects with detailed descriptions
   - Invite team members with role-based permissions
   - Manage tasks with status/priority tracking
   - Set milestones and track completion
   - Public/private/collaborative visibility controls

3. **Direct Messaging**
   - 1-to-1 direct messages between users
   - Read status tracking (scalable via MessageReadStatus)
   - File attachments
   - Message reactions (emoji)
   - Message threading (replies)

4. **Group Chat**
   - Create group chat rooms
   - Multiple participants
   - Same features as direct messages
   - Member management

5. **Social Networking**
   - Send/accept connection requests
   - Follow users and see their activity
   - Activity feeds tracking all actions
   - Notifications for interactions

6. **Engagement**
   - Like projects
   - Comment on projects
   - Track statistics (projects created, connections, followers)
   - View counts for popularity metrics

---

## Architecture Overview

```
Presentation Layer (HTML/CSS/JS)
         ↓
URL Routing (urls.py)
         ↓
View Layer (views.py - 3193 lines)
    ├─ Authentication Views
    ├─ Project Views
    ├─ Messaging Views
    ├─ Social Views
    └─ Profile Views
         ↓
Business Logic Layer
    ├─ Services (auth_service.py)
    ├─ NLP Utils (StudentProfileNLP)
    ├─ Filtering (ProjectVisibilityFilter)
    └─ Forms & Validation
         ↓
Data Layer (ORM Models)
    └─ 20+ Models
         ↓
Database
    ├─ PostgreSQL (production)
    └─ SQLite (development fallback)
         ↓
External Services
    ├─ Email (Brevo/ZeptoMail)
    ├─ OAuth (Google/GitHub)
    └─ Storage (S3/Local)
```

---

## Key Features Breakdown

### 1. Authentication System
- **Standard Registration** → Creates User + StudentProfile + OTP verification
- **OTP Login** → Email OTP without password
- **Social Login** → Google/GitHub OAuth + CustomSocialSignupForm
- **Password Reset** → OTP-based recovery
- **Security:** CSRF protection, session-based auth, password validation

### 2. Project Management
**Models:** Project, ProjectMember, ProjectTask, ProjectMilestone, ProjectInvitation

**Lifecycle:**
1. User creates project with title, description, category, technologies
2. Specifies team roles needed (looking_for)
3. Invites users to team with role assignment
4. Creates tasks within project (todo/in_progress/review/completed)
5. Marks milestones as complete
6. Manages visibility (public/private/collaborative)

**Team Roles:**
- Owner: Full control, can manage everything
- Admin: Same as owner
- Contributor: Can edit project and manage tasks
- Viewer: Read-only access

### 3. Messaging System
**Models:** Message, ChatRoom, ChatRoomMember, MessageFile, MessageReaction, MessageReadStatus

**Scalability Decision:** Separate MessageReadStatus model instead of boolean field
- Handles read tracking at scale
- Supports multiple readers in group chats
- Methods: mark_as_read_by(), is_read_by(), get_read_count()

**Features:**
- Direct messages (1-to-1)
- Group chats (ChatRoom)
- Message threading (reply_to)
- Read status indicators
- File attachments
- Emoji reactions
- Message search API
- Draft messages
- Typing indicators

### 4. Social Networking
**Models:** Connection, Follow, Activity, Notification

**Connection Flow:**
1. User sends connection request → status='pending'
2. Receiver accepts/rejects → status='accepted'/'rejected'
3. Both users can message, see profiles

**Follow System:**
- Follow users to see their activity
- Activity feed aggregates followed users' actions
- Public/private activity control

**Activity Types:**
- profile_updated, project_created, project_liked
- connection_made, message_sent, comment_added
- user_followed, task_completed, milestone_completed

### 5. Profile System
**StudentProfile Model:**
```python
- full_name, college, location, bio
- profile_photo (with image validation)
- skills (JSONField array: ['python', 'javascript', ...])
- project_interests (JSONField array)
- role_preference
- Social links: GitHub, LinkedIn, Portfolio, Behance
- profile_completed flag
- Timestamps: created_at, updated_at
```

**NLP Features:**
- Extract skills from text
- Categorize interests
- Calculate profile similarity for recommendations
- Find collaborators by matching skills

---

## Technology Stack Details

### Backend Framework
- **Django 4.2.8** - Web framework
- **DRF 3.14.0** - REST API
- **django-allauth 0.61.1** - Social authentication
- **django-cors-headers 4.3.1** - CORS support

### Database & ORM
- **PostgreSQL 14+** - Production database
- **SQLite3** - Development fallback
- **psycopg2-binary 2.9.9** - PostgreSQL driver
- **dj-database-url 2.1.0** - Connection string parsing

### Email
- **Brevo API** (Primary) - Transactional email service
- **ZeptoMail API** (Alternative) - Email service
- **Gmail SMTP** (Fallback) - Free SMTP option
- **Console Backend** (Development) - Log to console

### Real-time & Caching
- **Channels 4.0.0** - WebSocket support
- **channels-redis 4.1.0** - Redis backend
- **redis 5.0.1** - Cache/session store
- **django-redis 5.4.0** - Redis integration

### Data Processing
- **nltk 3.8.1** - Natural Language Processing
- **pandas 2.1.4** - Data manipulation
- **openpyxl 3.1.2** - Excel file handling
- **scikit-learn** - TF-IDF, similarity calculations

### File Storage
- **Pillow 10.1.0** - Image processing
- **boto3 1.34.34** - AWS S3 integration
- **django-storages 1.14.2** - Cloud storage backend

### Development & Testing
- **pytest 7.4.3** - Testing framework
- **black 23.12.1** - Code formatter
- **flake8 6.1.0** - Linter
- **mypy 1.7.1** - Type checking
- **django-debug-toolbar 4.2.0** - Debugging

### Production
- **gunicorn 21.2.0** - WSGI server
- **whitenoise 6.6.0** - Static file serving
- **sentry-sdk 1.38.0** - Error tracking

---

## Database Schema (Key Models)

### User & Profile
- **User** (Django auth.User)
- **StudentProfile** (extended profile with skills, interests, photo)
- **UserStatus** (online/offline tracking)
- **UserStats** (statistics counters)

### Projects
- **Project** (title, description, category, visibility)
- **ProjectMember** (team membership with roles)
- **ProjectTask** (todo items with status/priority)
- **ProjectMilestone** (project milestones)
- **ProjectInvitation** (team invitation management)

### Messaging
- **Message** (content, type, threading)
- **ChatRoom** (group conversations)
- **ChatRoomMember** (chat participants)
- **MessageReadStatus** (scalable read tracking)
- **MessageFile** (file attachments)
- **MessageReaction** (emoji reactions)
- **File** (uploaded file metadata)

### Social
- **Connection** (connection requests)
- **Follow** (following relationship)
- **Activity** (activity feed entries)
- **Notification** (user notifications)
- **Like** (project likes)
- **Comment** (project comments)

### Other
- **OTP** (one-time passwords)

---

## API Endpoints

### REST API Base: `/api/`

**Chat Management:**
- POST/GET `/chat-rooms/` - Create/list chat rooms
- GET/PUT `/chat-rooms/<id>/` - Get/update room details
- GET `/chat-rooms/<room_id>/members/` - Get room members

**Messaging:**
- POST/GET `/messages/` - Send/list messages
- GET `/messages/<pk>/` - Get message detail
- GET `/messages/search/` - Search messages
- GET `/messages/<message_id>/status/` - Read status
- POST `/messages/<message_id>/reactions/` - Add reaction

**Direct Messages:**
- POST `/direct-message/` - Send DM

**Utilities:**
- GET `/conversations/` - List conversations
- POST `/typing/` - Send typing indicator
- GET/POST `/drafts/` - Manage drafts

**College & User Data:**
- GET `/college-search/` - Search colleges
- POST `/validate-college/` - Validate college
- GET `/user-profile/<user_id>/` - Get user profile
- GET `/user-stats/` - User statistics
- POST `/nlp-analyze/` - NLP analysis

---

## Email System

### Backend Selection Priority
1. **Brevo** (if BREVO_API_KEY set) - Production recommended
2. **ZeptoMail** (if ZEPTO_MAIL_API_KEY set) - Alternative
3. **Gmail SMTP** (if EMAIL_HOST_USER set) - Fallback
4. **Console** - Development (prints to console)

### Uses
- OTP delivery (login, registration, password reset)
- Welcome emails
- Notifications (connection requests, project invites, messages)
- System emails

### Implementation
```python
send_mail(
    subject='Your OTP Code',
    message='Your OTP is: 123456',
    from_email=settings.DEFAULT_FROM_EMAIL,
    recipient_list=['user@example.com'],
    html_message='<strong>Your OTP is: 123456</strong>'
)
```

---

## Forms & Validation

| Form | Fields | Validation |
|------|--------|-----------|
| **RegisterForm** | username, email, password1, password2, terms_agree | Unique username/email, password strength (8+, upper, lower, digit) |
| **LoginForm** | username, password, remember_me | Basic auth validation |
| **OTPVerificationForm** | otp_code | 6 digits only, numeric |
| **StudentProfileForm** | 20+ fields | File type validation for images, checkbox for skills |
| **ProjectForm** | 8 fields (title, desc, tech, role, cat, timeline, collab, github) | Title 5-200 chars, desc 20-5000 chars, URL validation |
| **CustomSocialSignupForm** | full_name, college, interests | Saves to StudentProfile during OAuth signup |

---

## Security Considerations

### ✅ Implemented
- CSRF protection via middleware
- Password validation (8+ chars, mixed case, digit)
- Email uniqueness validation
- File extension validation for uploads
- Session-based authentication
- User permissions checking in views
- OTP single-use enforcement
- OTP expiry (5 minutes)

### ⚠️ Areas for Improvement
- Rate limiting on API endpoints (not implemented)
- Input sanitization for text fields
- SQL injection protection (Django ORM handles, but worth reviewing)
- XSS protection (use Django's template escaping)
- SECRET_KEY auto-generation in dev (fine, but ensure env var in prod)
- No API documentation (drf-spectacular installed but not used)
- WebSocket authentication (Channels installed but config unclear)

---

## Performance Considerations

### Current Implementation
- Basic pagination (10 items per page)
- Cache configuration exists but minimal usage
- No select_related/prefetch_related optimization visible
- No query caching
- Redis available but underutilized

### Recommendations
1. **N+1 Query Optimization**
   ```python
   # Instead of:
   projects = Project.objects.all()
   for p in projects:
       print(p.owner.username)  # Extra query!
   
   # Use:
   projects = Project.objects.select_related('owner')
   ```

2. **Caching Strategy**
   - Cache user profiles (1 hour)
   - Cache project listings (5 mins)
   - Cache activity feeds (2 mins)

3. **Database Indexes**
   - Add indexes on frequently searched fields
   - Index foreign keys for join performance

4. **Pagination**
   - Standardize across all list views
   - Use DRF pagination classes

---

## Deployment Checklist

### Environment Setup
- [ ] Create PostgreSQL database (Render.com recommended)
- [ ] Set all required environment variables
- [ ] Configure SECRET_KEY (use secrets module)
- [ ] Set ALLOWED_HOSTS for domain
- [ ] Configure email backend (Brevo recommended)
- [ ] Configure social OAuth apps

### Security
- [ ] Enable SECURE_SSL_REDIRECT (for HTTPS)
- [ ] Set SESSION_COOKIE_SECURE
- [ ] Set CSRF_COOKIE_SECURE
- [ ] Set secure password validators
- [ ] Configure ALLOWED_HOSTS

### Static & Media
- [ ] Configure S3 storage (optional)
- [ ] Run collectstatic
- [ ] Set correct permissions on media directory

### Monitoring
- [ ] Set up Sentry (already in requirements)
- [ ] Configure logging rotation
- [ ] Set up error alerting

### Database
- [ ] Run migrations on production
- [ ] Create superuser
- [ ] Verify database connection
- [ ] Set up backups

### Testing
- [ ] Run full test suite
- [ ] Load test key endpoints
- [ ] Test email delivery
- [ ] Verify social login

---

## Development Workflow

### Local Setup (5 steps)
```bash
1. git clone https://github.com/Goku0090/uni.git
2. python -m venv venv && source venv/bin/activate
3. pip install -r requirements.txt
4. cp .env.template .env && edit .env
5. python manage.py migrate && python manage.py runserver
```

### Making Changes
1. Create feature branch: `git checkout -b feature/xyz`
2. Make changes and test locally
3. Run tests: `python -m pytest`
4. Format code: `black accounts/`
5. Commit and push
6. Create pull request

### Common Commands
```bash
# Database
python manage.py makemigrations
python manage.py migrate

# Development
python manage.py runserver
python manage.py shell

# Testing
python -m pytest
python -m pytest accounts/tests.py -v

# Static files
python manage.py collectstatic

# Code quality
black .
flake8 .
mypy .
```

---

## Known Issues & Limitations

1. **Monolithic views.py** (3193 lines)
   - Should split into: auth, projects, messaging, social, profiles

2. **No comprehensive testing**
   - tests.py mostly empty, needs pytest fixtures and coverage

3. **Limited API documentation**
   - drf-spectacular installed but not configured for auto-docs

4. **WebSocket implementation unclear**
   - Channels installed but no routing.py visible

5. **No rate limiting**
   - API vulnerable to abuse without throttling

6. **Error handling basic**
   - Generic error messages, could be more specific

7. **Caching underutilized**
   - Redis configured but minimal usage

8. **Image optimization missing**
   - Profile photos not resized/compressed

9. **Scaling concerns**
   - Single app may need splitting for microservices
   - Task queue (Celery) installed but minimal usage

10. **Email retry logic**
    - No built-in retries for failed emails

---

## Recommendations (Priority Order)

### High Priority
1. **Split views.py** into logical modules (auth, projects, etc.)
2. **Add comprehensive tests** with pytest fixtures
3. **Implement rate limiting** on API endpoints
4. **Add API documentation** (use drf-spectacular)
5. **Fix N+1 queries** with select_related/prefetch_related

### Medium Priority
6. **Implement WebSocket messaging** for real-time delivery
7. **Add image optimization** for profile photos
8. **Implement caching strategy** for hot paths
9. **Add email retry logic** with exponential backoff
10. **Improve error handling** with specific messages

### Low Priority
11. Create CLI management commands for admin tasks
12. Add background job monitoring
13. Implement activity feed pagination
14. Add advanced search filters
15. Create mobile API optimizations

---

## Code Statistics

- **Total Models:** 20+
- **View Functions:** 50+
- **Forms:** 5
- **Serializers:** Several (API)
- **URL Patterns:** 100+
- **Template Files:** 30+
- **Test Files:** Minimal (needs expansion)
- **Dependencies:** 84 packages

---

## Conclusion

UniSync is a **well-structured Django application** with comprehensive features for collaborative project management and social networking. The architecture is sound with proper use of models, views, and REST API. Key strengths include:

✅ Multi-backend email system  
✅ Flexible authentication (OTP + OAuth)  
✅ Scalable messaging (MessageReadStatus)  
✅ Role-based project permissions  
✅ NLP-powered recommendations  
✅ Comprehensive model relationships  

Main areas for improvement:

⚠️ Code organization (split monolithic views)  
⚠️ Testing coverage  
⚠️ API documentation  
⚠️ Performance optimization  
⚠️ Real-time features  

With targeted improvements, this can become a production-grade platform for student collaboration.

---

## Additional Resources Generated

This analysis includes:
1. **CODEBASE_COMPREHENSIVE_ANALYSIS_2026.md** - Detailed technical documentation
2. **DEVELOPMENT_QUICK_REFERENCE.md** - Developer guide with examples
3. **CODE_FLOW_DIAGRAMS.md** - 10 detailed user flow diagrams
4. **Architecture & ER Diagrams** - Visual representations

---

**Analysis Version:** 1.0  
**Generated:** January 29, 2026  
**Analyzer:** Amp AI
