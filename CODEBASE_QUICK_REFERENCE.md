# UniSync Codebase - Quick Reference Guide

## 📋 Quick Navigation

### Main Entry Points

| URL | View Function | Template | Purpose |
|-----|--------------|----------|---------|
| `/accounts/login/` | `login_view()` | `login.html` | User login |
| `/accounts/register/` | `register_view()` | `register.html` | New user signup |
| `/accounts/student-profile/` | `student_profile()` | `student_profile.html` | User profile |
| `/accounts/find-collaborators/` | `find_collaborators()` | `find_collaborators.html` | Search users |
| `/accounts/post-project/` | `post_project()` | `post_project.html` | Create project |
| `/accounts/messages/` | `message_view()` | `messages.html` | Direct messages |

### Key Files

```
auth_project/
├── accounts/
│   ├── models.py (718 lines) - Database models
│   ├── views.py (1476+ lines) - View functions
│   ├── forms.py (583 lines) - Form validation
│   ├── urls.py (120 lines) - URL routing
│   ├── templates/
│   │   └── login.html (421 lines) - Login UI
│   ├── static/
│   │   └── js/login.js (183 lines) - Login logic
│   └── services/
│       └── auth_service.py (470 lines) - Email sending
├── auth_project/
│   └── settings.py (356+ lines) - Configuration
└── requirements.txt - Dependencies
```

---

## 🔑 Core Models Quick Reference

### User (Django built-in)
```python
User.objects.create_user(
    username='john_doe',
    email='john@example.com',
    password='SecurePass123'
)
```

### StudentProfile (1:1 with User)
```python
StudentProfile.objects.create(
    user=user,
    full_name='John Doe',
    college='MIT',
    interests=['Python', 'AI'],  # JSON array
    skills=['Python', 'Django'],  # JSON array
    profile_photo=image_file
)
```

### OTP (Email verification)
```python
# Generate OTP
otp = OTP.generate_otp('john@example.com', 'login')
# Returns: 6-digit code, 5-minute expiry

# Verify OTP
is_valid, message = otp.verify_otp('123456')
```

### Project (Collaboration)
```python
Project.objects.create(
    user=request.user,
    title='AI Chat Bot',
    description='Build an AI chatbot...',
    technologies='Python, Django, TensorFlow',
    looking_for='Frontend Developer, UI Designer',
    category='ai',
    timeline='3-6 months'
)
```

### Connection (Social)
```python
Connection.objects.create(
    sender=user1,
    receiver=user2,
    status='pending'  # pending, accepted, rejected
)
```

### Message (Messaging)
```python
Message.objects.create(
    sender=user1,
    receiver=user2,
    content='Hello!',
    message_type='text'  # text, file, image, call
)

# Mark as read
message.mark_as_read_by(user2)
```

---

## 🔐 Authentication Flow

### Login (Username or Email)
```python
# Form submission
username = request.POST.get('username')  # Can be username OR email
password = request.POST.get('password')

# Django authenticate() handles both
user = authenticate(request, username=username, password=password)

if user:
    login(request, user)
    AuthService.send_welcome_back_email(user.email, user.username)
    return redirect('main_home')
```

### Registration
```python
# Validation requirements
- username: 3-150 chars, unique, alphanumeric + underscore/hyphen
- email: valid format, unique
- password: 8+ chars, uppercase, lowercase, digit

# Create user
user = User.objects.create_user(
    username=username,
    email=email,
    password=password
)

# Create profile
StudentProfile.objects.create(user=user, ...)

# Send welcome email
AuthService.send_welcome_email(email, username)
```

### OTP (5-minute validity)
```python
# Generate
otp = OTP.generate_otp(email, purpose='reset')  # 6-digit code
send_otp_email(email, otp.otp_code, 'password reset')

# Verify
otp = OTP.objects.get(email=email, purpose='reset')
is_valid, msg = otp.verify_otp(user_input_code)
```

### Password Reset
```python
# 1. User requests reset (forgot-password page)
# 2. OTP generated and sent to email
# 3. User enters OTP (verify-otp page)
# 4. If valid, user can reset password (reset-password page)
# 5. Password updated and user redirected to login
```

---

## 📧 Email System

### How Email Backend is Selected (Priority Order)

```python
1. if BREVO_API_KEY:
       Use BrevoMailBackend  # Recommended for production
   
2. elif ZEPTO_MAIL_API_KEY + ZEPTO_MAIL_TOKEN:
       Use ZeptoMailBackend  # Alternative
   
3. elif EMAIL_HOST_USER + EMAIL_HOST_PASSWORD:
       Use Gmail SMTP  # Fallback
   
4. else:
       Use ConsoleBackend  # Development (prints to console)
```

### Email Types

| Purpose | Subject | Recipient | Backend |
|---------|---------|-----------|---------|
| Welcome | "Welcome to UniSync, {user}! 🎉" | New user email | Auto-selected |
| Welcome Back | "Welcome back, {user}! 🚀" | Login user email | Auto-selected |
| OTP | "Your {purpose} OTP Code" | User email | Auto-selected |
| Password Reset | "Password Reset - UniSync" | Reset requester | Auto-selected |

### Send Custom Email
```python
from django.core.mail import EmailMultiAlternatives
from django.conf import settings

msg = EmailMultiAlternatives(
    subject="Your Subject",
    body="Plain text version",
    from_email=settings.DEFAULT_FROM_EMAIL,
    to=[recipient_email]
)
msg.attach_alternative(html_version, "text/html")
msg.send()
```

---

## 🎨 Frontend Structure (login.html)

### HTML Structure
```
<html dark>
  ├─ <head> (CSS, Tailwind, Font Awesome)
  ├─ <body class="bg-background text-text">
  │  ├─ Background Orbs (animated)
  │  ├─ Floating Particles (animated)
  │  ├─ Navbar (logo, home, signup links)
  │  ├─ Main Content
  │  │  ├─ Header (title, description)
  │  │  ├─ Messages (success/error)
  │  │  ├─ Login Form
  │  │  │  ├─ Username/Email field
  │  │  │  ├─ Password field (with toggle)
  │  │  │  ├─ Remember me checkbox
  │  │  │  ├─ Submit button
  │  │  │  └─ CSRF token
  │  │  ├─ Footer (signup link)
  │  │  └─ Feature highlights (3 columns)
  │  └─ JavaScript (login.js)
  └─ Styles (CSS animations, 3D effects)
```

### Color Scheme (Dark Mode)
```javascript
{
  background: '#1E1E2F',    // Dark navy
  primary: '#2D2D44',       // Slightly lighter
  accent: '#3AB7BF',        // Cyan blue (highlights)
  text: '#EAEAEA',          // Off-white
  softDark: '#28293E'       // Softer dark
}
```

### JavaScript Functions (login.js)
```javascript
validateEmail(email)              // Check email format
validateUsername(username)        // Check username format
showFieldError(input, message)    // Display error
hideFieldError(input)             // Clear error
togglePassword()                  // Show/hide password
Form submission handling          // Validation + submit
```

---

## 🗄️ Database Schema (Key Tables)

### users (Django built-in)
```sql
id, username, email, password, first_name, last_name,
is_active, is_staff, date_joined, last_login
```

### accounts_studentprofile (1:1 with users)
```sql
id, user_id (UNIQUE),
full_name, college, location,
interests (JSON), bio,
profile_photo (file path),
skills (JSON), project_interests (JSON),
github, linkedin, portfolio, behance (URLs),
profile_completed (bool),
created_at, updated_at
```

### accounts_otp
```sql
id, email, otp_code, purpose (enum),
is_used (bool),
created_at, expires_at
Indices: email + purpose
```

### accounts_project
```sql
id, user_id (FK),
title, description, technologies (text),
looking_for (text), category,
timeline, collaboration_needs,
github_link (URL),
created_at, updated_at
```

### accounts_connection
```sql
id, sender_id (FK), receiver_id (FK),
status (enum: pending/accepted/rejected),
created_at, updated_at
Unique: sender_id + receiver_id
```

### accounts_message
```sql
id, sender_id (FK), receiver_id (FK),
chat_room_id (FK, nullable),
content (text), message_type (enum),
reply_to_id (FK, nullable),
created_at, updated_at
```

---

## 🔧 Configuration Reference

### Environment Variables

```bash
# Security
SECRET_KEY=your-secret-key
DEBUG=True|False

# Database
DATABASE_URL=postgres://user:pass@host/db  # Production
# OR locally:
DB_NAME=unisync_db
DB_USER=unisync_user
DB_PASSWORD=your_password
DB_HOST=localhost
DB_PORT=5432

# Email
BREVO_API_KEY=your-brevo-key          # Primary
ZEPTO_MAIL_API_KEY=your-zepto-key     # Alternative
ZEPTO_MAIL_TOKEN=your-zepto-token
EMAIL_HOST_USER=your-gmail@gmail.com  # Fallback
EMAIL_HOST_PASSWORD=app-password

# Security Headers
SECURE_SSL_REDIRECT=True
SESSION_COOKIE_SECURE=True
CSRF_COOKIE_SECURE=True
```

### Installed Apps
```python
INSTALLED_APPS = [
    # Django core
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.sites',
    
    # Custom
    'accounts',
    
    # Social auth
    'allauth',
    'allauth.account',
    'allauth.socialaccount',
    'allauth.socialaccount.providers.google',
    'allauth.socialaccount.providers.github',
    
    # API
    'rest_framework',
]
```

---

## 🚀 Common Tasks

### Create a New User Programmatically
```python
from django.contrib.auth.models import User
from accounts.models import StudentProfile

user = User.objects.create_user(
    username='newuser',
    email='user@example.com',
    password='SecurePass123'
)

StudentProfile.objects.create(
    user=user,
    full_name='New User',
    college='Stanford',
    profile_completed=True
)
```

### Send Email to User
```python
from accounts.services.auth_service import AuthService

# Send welcome email
AuthService.send_welcome_email('user@example.com', 'username')

# Send password reset email
AuthService.send_password_reset_email(
    'user@example.com',
    'username',
    'https://example.com/reset/token'
)
```

### Query Projects by User
```python
from accounts.models import Project

# Get all projects by user
user_projects = Project.objects.filter(user=request.user)

# Get all projects with specific technology
projects_with_python = Project.objects.filter(
    technologies__icontains='Python'
)

# Get all projects in a category
ai_projects = Project.objects.filter(category='ai')
```

### Get User's Connections
```python
from accounts.models import Connection
from django.db.models import Q

# Get accepted connections
connections = Connection.objects.filter(
    Q(sender=request.user) | Q(receiver=request.user),
    status='accepted'
)

# Get pending requests (received by user)
pending = Connection.objects.filter(
    receiver=request.user,
    status='pending'
)
```

### Get User Messages
```python
from accounts.models import Message
from django.db.models import Q

# Get all conversations
messages = Message.objects.filter(
    Q(sender=request.user) | Q(receiver=request.user)
).order_by('-created_at')

# Get conversation with specific user
conversation = Message.objects.filter(
    Q(sender=request.user, receiver=other_user) |
    Q(sender=other_user, receiver=request.user)
).order_by('created_at')
```

### Perform Login Programmatically
```python
from django.contrib.auth import authenticate, login

user = authenticate(username='john_doe', password='SecurePass123')
if user is not None:
    login(request, user)  # Creates session
    # User is now logged in
```

---

## 🐛 Debugging Tips

### Check if Email Backend is Working
```python
from django.core.mail import send_mail

send_mail(
    subject='Test Email',
    message='This is a test',
    from_email='noreply@example.com',
    recipient_list=['test@example.com'],
)
# Check console or email service for delivery
```

### View Django Logs
```bash
# Enable logging in settings.py
LOGGING = {
    'version': 1,
    'handlers': {
        'console': {'class': 'logging.StreamHandler'},
    },
    'loggers': {
        'accounts': {'handlers': ['console'], 'level': 'DEBUG'},
    },
}
```

### Check Database Queries
```python
from django.db import connection

# Enable query logging
LOGGING = {...}  # as above

# View all queries executed
for query in connection.queries:
    print(query['sql'])
```

### Test OTP Generation
```python
from accounts.models import OTP

otp = OTP.generate_otp('test@example.com', 'login')
print(f"OTP Code: {otp.otp_code}")
print(f"Valid: {otp.is_valid()}")
print(f"Expires: {otp.expires_at}")

# Verify
is_valid, msg = otp.verify_otp('123456')
print(f"Verification: {msg}")
```

---

## 📊 Statistics

| Metric | Value |
|--------|-------|
| Total Python Lines | 3,000+ |
| Template Files | 20+ |
| Static Files | CSS, JS, Images |
| Database Models | 15+ |
| URL Patterns | 100+ |
| Email Backends | 3 (Brevo, ZeptoMail, Gmail) |
| Supported OAuth | Google, GitHub |
| Password Strength | 8+ chars, mixed case, digits |

---

## 🔒 Security Checklist

- ✅ CSRF Token on forms
- ✅ Password hashing (PBKDF2)
- ✅ Input sanitization
- ✅ SQL injection prevention (ORM)
- ✅ XSS prevention (template escaping)
- ✅ Session security
- ⚠️ No rate limiting on login (TODO)
- ⚠️ REST API uses AllowAny (should restrict)

---

## 📚 Common Patterns

### Form Handling
```python
if request.method == 'POST':
    form = MyForm(request.POST, request.FILES)
    if form.is_valid():
        instance = form.save(commit=False)
        instance.user = request.user
        instance.save()
        messages.success(request, 'Saved!')
        return redirect('success_page')
else:
    form = MyForm()
return render(request, 'template.html', {'form': form})
```

### Login Required
```python
from django.contrib.auth.decorators import login_required

@login_required(login_url='login')
def my_view(request):
    user = request.user
    profile = user.student_profile
    return render(request, 'template.html')
```

### Query with Related Objects
```python
# Avoid N+1 queries
projects = Project.objects.select_related('user').all()
for project in projects:
    print(project.user.username)  # No extra query
```

---

## 🎯 Next Steps for Development

1. **Add rate limiting** to prevent brute force attacks
2. **Improve REST API** permissions (authenticate by default)
3. **Add email confirmation** for registration
4. **Implement password reset confirmation** (via email link)
5. **Add user activity logging** for security auditing
6. **Set up monitoring** (Sentry) for production
7. **Add unit tests** for critical flows
8. **Implement caching** for frequently accessed data
