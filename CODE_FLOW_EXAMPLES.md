# UniSync Code Flow Examples

## 1. User Registration Flow

### Request Path: POST `/register/` → `register_view()`

```
User submits registration form
          ↓
register_view() receives POST
          ↓
Validate inputs:
  - username not empty ✓
  - email not empty & valid ✓
  - password == confirm_password ✓
  - password length >= 8 ✓
  - password contains uppercase ✓
  - password contains digit ✓
  - username not already taken ✓
  - email not already taken ✓
          ↓
Create Django User object
  user = User.objects.create_user(
      username=username,
      email=email,
      password=password
  )
          ↓
Create StudentProfile
  profile = StudentProfile.objects.create(
      user=user,
      full_name=full_name,
      college=college,
      location=location,
      interests=interests,
      bio=bio
  )
          ↓
Send welcome email
  AuthService.send_welcome_email(email, username)
          ↓
Generate OTP
  otp = OTP.generate_otp(email, 'registration')
  - Generates random 6-digit code
  - Sets expires_at = now + 5 minutes
  - Deactivates previous OTPs
          ↓
Send OTP email
  send_otp_email(email, otp_code, 'registration')
          ↓
Redirect to verify OTP page
  redirect('verify_otp', purpose='registration')
```

**Key Models Involved:**
- `User` (Django built-in)
- `StudentProfile` (custom)
- `OTP` (custom)

**Key Functions:**
- `register_view()` - Main handler
- `AuthService.send_welcome_email()` - Welcome message
- `OTP.generate_otp()` - OTP creation
- `send_otp_email()` - Email dispatch

---

## 2. Login with OTP Flow

### Request Path: POST `/login/` → `login_view()`

```
User enters email/username on login form
          ↓
login_view() receives POST
          ↓
Get email from POST data
  email_or_username = request.POST.get('email')
          ↓
Find user by email OR username
  if '@' in email_or_username:
      user = User.objects.get(email=email_or_username)
  else:
      user = User.objects.get(username=email_or_username)
          ↓
User exists?
  ├─ Yes → Continue
  └─ No  → Show error, return to login
          ↓
Generate OTP for login purpose
  otp = OTP.generate_otp(user.email, 'login')
          ↓
Send OTP email
  send_otp_email(user.email, otp.otp_code, 'login')
          ↓
Store email in session
  request.session['login_email'] = user.email
          ↓
Redirect to OTP verification
  redirect('verify_otp', purpose='login')
```

**Session Storage:**
```python
request.session['login_email'] = user.email  # Persists across requests
```

**Key Security:**
- No password transmitted
- OTP expires in 5 minutes
- Email verified
- Rate limiting (not implemented - missing)

---

## 3. OTP Verification Flow

### Request Path: POST `/verify-otp/login/` → `verify_otp_view(request, 'login')`

```
User receives OTP in email, enters code
          ↓
verify_otp_view() receives POST with otp_code
          ↓
Get email from session
  email = request.session.get('login_email')
          ↓
Query OTP from database
  otp_obj = OTP.objects.filter(
      email=email,
      purpose='login',
      is_used=False
  ).latest('-created_at')
          ↓
Verify OTP
  is_valid, message = otp_obj.verify_otp(user_code)
          ├─ Check: not expired (timezone.now() < expires_at)
          ├─ Check: not is_used (is_used == False)
          └─ Check: code matches exactly
          ↓
OTP Valid?
  ├─ Yes → Continue
  └─ No  → Show error message, return to verify page
          ↓
Get user by email
  user = User.objects.get(email=email)
          ↓
Authenticate user
  login(request, user, backend='django.contrib.auth.backends.ModelBackend')
          ↓
Send welcome back email (optional)
  AuthService.send_welcome_back_email(email, user.username)
          ↓
Clear session
  del request.session['login_email']
          ↓
Redirect to dashboard
  redirect('main_home')
```

**Key Method:**
```python
def verify_otp(self, otp_code):
    if not self.is_valid():
        return False, "OTP has expired or is invalid."
    if otp_code == self.otp_code:
        self.is_used = True
        self.save()
        return True, "OTP verified successfully."
    return False, "Invalid OTP code."
```

**Security Notes:**
- Plain text comparison (could use hashing)
- OTP marked used after successful verification
- User fully authenticated with Django login()

---

## 4. Project Creation Flow

### Request Path: POST `/post-project/` → `post_project()`

```
Authenticated user fills project form
          ↓
post_project() receives POST
          ↓
Extract form data
  title = request.POST.get('title')
  description = request.POST.get('description')
  techs = request.POST.getlist('technologies')  # Array
  looking = request.POST.getlist('looking_for')  # Array
  category = request.POST.get('category', 'Other')
  timeline = request.POST.get('timeline', '')
  collaboration = request.POST.get('collaboration_needs', '')
  github_link = request.POST.get('github_link', '')
          ↓
Validate required fields
  if not title or not description:
      Show error, redirect back
          ↓
Create Project model instance
  project = Project.objects.create(
      user=request.user,                    # Set owner
      title=title,
      description=description,
      technologies=", ".join(techs),        # Convert array to CSV
      looking_for=", ".join(looking),       # Convert array to CSV
      category=category,
      timeline=timeline,
      collaboration_needs=collaboration,
      github_link=github_link
  )
          ↓
Create Activity record
  create_activity(
      user=request.user,
      activity_type='project_created',
      title=f"Created project '{title}'",
      description=f"{user.username} created '{title}'",
      project=project
  )
          ↓
Broadcast notification (if notification system active)
  # Notify followers or connected users
          ↓
Display success message
  messages.success(request, 'Project posted successfully!')
          ↓
Redirect to projects list
  redirect('post_project')
```

**Data Format Note:**
```python
# Array input
techs = ['Python', 'Django', 'PostgreSQL']

# Stored as CSV string
project.technologies = "Python, Django, PostgreSQL"

# Displayed by splitting
tech_list = [tech.strip() for tech in project.technologies.split(',')]
```

**Key Model Relations:**
- `Project.user` → Owner (User)
- `Project.tasks` → ProjectTask (reverse relation)
- `Project.members` → ProjectMember (reverse relation)
- `Project.activities` → Activity (reverse relation)

---

## 5. Find Collaborators Flow

### Request Path: GET `/find-collaborators/?q=python&college=MIT` → `find_collaborators()`

```
User visits find_collaborators page
          ↓
find_collaborators() handles GET
          ↓
Get current user profile
  user_profile = StudentProfile.objects.get(user=request.user)
  user_interests = user_profile.interests.lower().split(',')
          ↓
Extract query parameters
  query = request.GET.get('q', '')           # Search term
  college = request.GET.get('college', '')
  location = request.GET.get('location', '')
  skills = request.GET.get('skills', '')
  interests = request.GET.get('interests', '')
  role = request.GET.get('role', '')
          ↓
Build base queryset
  base_profiles = StudentProfile.objects.filter(
      user__is_active=True
  ).exclude(user=request.user)
          ↓
Apply filters (if any)
  active_filters = False
  
  if query:
      search_profiles = base_profiles.filter(
          Q(full_name__icontains=query) |
          Q(bio__icontains=query) |
          Q(interests__icontains=query) |
          Q(skills__icontains=query)
      )
      active_filters = True
  
  if college:
      base_profiles = base_profiles.filter(college=college)
      active_filters = True
  
  if location:
      base_profiles = base_profiles.filter(location__icontains=location)
      active_filters = True
  
  if skills:
      base_profiles = base_profiles.filter(skills__icontains=skills)
      active_filters = True
  
  if role:
      base_profiles = base_profiles.filter(role_preference=role)
      active_filters = True
          ↓
Generate suggestions with NLP matching
  suggestions = []
  
  if user_interests:
      # NLP-based interest matching
      for profile in base_profiles:
          profile_interests = profile.interests.lower().split(',')
          matching_interests = set(user_interests) & set(profile_interests)
          profile.match_score = (
              len(matching_interests) / len(user_interests) * 100
          )
          suggestions.append(profile)
      
      suggestions.sort(key=lambda x: x.match_score, reverse=True)
          ↓
Get connection statuses
  all_user_ids = [p.user.id for p in suggestions]
  
  connections = Connection.objects.filter(
      Q(sender=request.user, receiver__id__in=all_user_ids) |
      Q(receiver=request.user, sender__id__in=all_user_ids)
  )
  
  connection_status = {}
  for conn in connections:
      other_user_id = (
          conn.receiver.id if conn.sender == request.user
          else conn.sender.id
      )
      connection_status[other_user_id] = conn.status
          ↓
Calculate statistics
  total_users = User.objects.count()
  active_projects = Project.objects.filter(
      created_at__gte=timezone.now() - timedelta(days=30)
  ).count()
  connections_today = Connection.objects.filter(
      created_at__date=timezone.now().date()
  ).count()
          ↓
Render template with context
  return render(request, 'find_collaborators.html', {
      'query': query,
      'search_results': search_results,
      'suggestions': suggestions,
      'user_interests': user_interests,
      'connection_status': connection_status,
      'active_filters': active_filters,
      'total_users': total_users,
      'active_projects': active_projects,
      'connections_today': connections_today,
  })
```

**NLP Matching Algorithm:**
```python
user_interests = ['python', 'django', 'machine-learning']

for profile in profiles:
    profile_interests = ['python', 'web-dev', 'django']
    
    # Find common interests
    matching = set(user_interests) & set(profile_interests)
    # Result: {'python', 'django'}
    
    # Calculate score
    score = (len(matching) / len(user_interests)) * 100
    # Result: (2 / 3) * 100 = 66.67%
    
    profile.match_score = score
```

**Connection Status Map:**
```python
connection_status = {
    5: 'pending',     # User 5: request sent/received
    10: 'accepted',   # User 10: connected
    15: 'rejected',   # User 15: rejected
    # No key = not connected
}
```

---

## 6. Send Connection Request Flow

### Request Path: POST `/send-connection/<user_id>/` → `send_connection_request()`

```
User clicks "Connect" button on profile
          ↓
send_connection_request() receives POST
          ↓
Get target user
  target_user = get_object_or_404(User, id=user_id)
          ↓
Check if connection already exists
  existing = Connection.objects.filter(
      Q(sender=request.user, receiver=target_user) |
      Q(sender=target_user, receiver=request.user)
  ).exists()
  
  if existing:
      Show error "Already connected or pending"
          ↓
Create Connection request
  connection = Connection.objects.create(
      sender=request.user,
      receiver=target_user,
      status='pending'
  )
          ↓
Create Notification for receiver
  Notification.objects.create(
      user=target_user,
      from_user=request.user,
      notification_type='connection_request',
      title=f'{request.user.username} sent you a connection request',
      message='Click to view and respond'
  )
          ↓
Create Activity record
  create_activity(
      user=request.user,
      activity_type='connection_made',
      title=f'Sent connection request to {target_user.username}',
      description=f'{request.user.username} sent a connection request'
  )
          ↓
Send notification email (if enabled)
  # Could send email via Brevo/ZeptoMail
          ↓
Return response
  if AJAX:
      return JsonResponse({'success': True})
  else:
      messages.success(request, 'Connection request sent!')
      redirect('find_collaborators')
```

**Database State After:**
```
Connection {
    id: 1,
    sender: request.user,
    receiver: target_user,
    status: 'pending',
    created_at: now,
    updated_at: now
}

Notification {
    id: 1,
    user: target_user,
    from_user: request.user,
    notification_type: 'connection_request',
    is_read: False,
    created_at: now
}
```

**Unique Constraint:**
```python
# In Connection model
class Meta:
    unique_together = ['sender', 'receiver']
```
Prevents duplicate connections in same direction.

---

## 7. Message Sending & Read Status Flow

### Request Path: POST `/messages/` (DRF API) → Message created

```
User sends message via chat interface
          ↓
Frontend makes AJAX POST to /messages/
  {
      "content": "Hello!",
      "receiver": 5,
      "message_type": "text"
  }
          ↓
MessageListCreateView handles POST
          ↓
MessageSerializer validates data
  - content: required, non-empty
  - receiver: valid user ID
  - message_type: in choices
          ↓
Create Message instance
  message = Message.objects.create(
      sender=request.user,
      receiver=receiver_user,
      content=content,
      message_type='text',
      created_at=now()
  )
          ↓
Create Notification
  Notification.objects.create(
      user=receiver_user,
      from_user=request.user,
      notification_type='new_message',
      title='New message from ' + request.user.username,
      message=content[:50] + '...'
  )
          ↓
Broadcast via WebSocket (if Channels enabled)
  # Real-time delivery to receiver if online
          ↓
Return JSON response
  {
      "id": 1,
      "content": "Hello!",
      "sender": {...},
      "created_at": "2024-01-29T10:00:00Z",
      "is_read": False
  }
```

### Message Read Status Flow

```
Receiver opens conversation with sender
          ↓
Frontend loads message history
  GET /messages/?receiver=sender_id
          ↓
Display all messages in chat
          ↓
For each unread message, frontend calls mark read
  POST /messages/<message_id>/status/
  {
      "read": true
  }
          ↓
mark_read_by() method executes
  MessageReadStatus.objects.get_or_create(
      message=message,
      user=request.user,
      defaults={'read_at': timezone.now()}
  )
          ↓
Database state updated
  MessageReadStatus {
      id: 1,
      message: message,
      user: receiver_user,
      read_at: now()
  }
          ↓
Return JSON response
  {
      "success": True,
      "read_by_count": 1
  }
```

**Read Status Queries:**

```python
# Check if user read message
is_read = message.is_read_by(user)
# → Checks MessageReadStatus.objects.filter(message=msg, user=user).exists()

# Get all readers
readers = message.get_read_by_users()
# → All users in MessageReadStatus for this message

# Get unread count
unread = message.get_read_count()
# → message.read_statuses.count()

# For group chats, get who hasn't read
unread_users = message.get_unread_users()
# → Complex logic checking ChatRoomMembers vs MessageReadStatus
```

---

## 8. Email Sending with Multiple Backends

### send_otp_email() Function Flow

```
Called from login_view() or register_view()
          ↓
Email backend selected from settings.py
  if BREVO_API_KEY:
      backend = 'accounts.brevo_mail_backend.BrevoMailBackend'
  elif ZEPTO_MAIL_API_KEY:
      backend = 'accounts.zepto_mail_backend.ZeptoMailBackend'
  elif EMAIL_HOST_USER:
      backend = 'django.core.mail.backends.smtp.EmailBackend'
  else:
      backend = 'django.core.mail.backends.console.EmailBackend'
          ↓
Build email message
  subject = f"Your {purpose.title()} OTP Code"
  
  text_message = f"""
  Hi there!
  Your OTP for {purpose} is: {otp_code}
  ...
  """
  
  html_message = f"""
  <html>
  <style>...</style>
  <body>
  <div class="container">
      <h2>OTP Code</h2>
      <div class="otp-box">{otp_code}</div>
  </body>
  </html>
  """
          ↓
Create EmailMultiAlternatives object
  msg = EmailMultiAlternatives(
      subject=subject,
      body=text_message,
      from_email=DEFAULT_FROM_EMAIL,
      to=[email]
  )
  msg.attach_alternative(html_message, "text/html")
          ↓
Send via backend
  msg.send()
          ↓
Result handling
  try:
      msg.send()
      logger.info(f"OTP email sent to {email}")
      return True
  except Exception as e:
      logger.error(f"Failed to send OTP: {e}")
      # Notify admins
      mail_admins(
          f'OTP Email Failed - {purpose}',
          f'Error: {str(e)}'
      )
      return False
```

**Brevo Backend (BrevoMailBackend):**
```python
class BrevoMailBackend(BaseEmailBackend):
    def send_messages(self, email_messages):
        # Uses BREVO_API_KEY from environment
        # Makes HTTP POST to Brevo API
        # Returns number of successfully sent emails
        pass
```

**Console Backend (for testing):**
```python
# In Django settings
EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'

# Output:
# ----Message-----
# Subject: Your Login OTP Code
# From: noreply@unisync.app
# To: user@example.com
# 
# Your OTP for login is: 123456
# ----End Message-----
```

---

## 9. Project Visibility Filtering Flow

### explore_projects_view() Filtering

```
User visits /explore-projects/
          ↓
Query all projects initially
  projects = Project.objects.all()
          ↓
Apply ProjectVisibilityFilter
  filter = ProjectVisibilityFilter(projects, user=request.user)
  filtered_projects = filter.filter()
          ↓
Filter logic (likely in ProjectVisibilityFilter):
  for project in projects:
      if project.visibility == 'public':
          include  # Public to everyone
      elif project.visibility == 'private':
          if project.owner == request.user or user in project.members:
              include  # Owner or member
          else:
              exclude  # Not visible to others
      elif project.visibility == 'draft':
          if project.owner == request.user:
              include  # Only owner
          else:
              exclude  # Hidden from others
          ↓
Paginate results
  paginator = Paginator(filtered_projects, 10)
  page = paginator.get_page(page_number)
          ↓
Add context data
  for project in page:
      project.likes_count = project.likes.count()
      project.comments_count = project.comments.count()
      project.members_count = project.members.count()
          ↓
Render template
  return render(request, 'explore_projects.html', {
      'projects': page,
      'total_count': filtered_projects.count()
  })
```

---

## 10. User Statistics Update Flow

### update_stats() Method in UserStats Model

```
Called after significant user action
          ↓
Count all projects
  projects_created = Project.objects.filter(
      user=self.user
  ).count()
          ↓
Count connections
  connections_made = Connection.objects.filter(
      Q(sender=self.user) | Q(receiver=self.user),
      status='accepted'
  ).count()
          ↓
Count likes received
  likes_received = Like.objects.filter(
      project__user=self.user
  ).count()
          ↓
Count comments made
  comments_made = Comment.objects.filter(
      user=self.user
  ).count()
          ↓
Count followers
  followers_count = Follow.objects.filter(
      following=self.user
  ).count()
          ↓
Count following
  following_count = Follow.objects.filter(
      follower=self.user
  ).count()
          ↓
Update all fields
  self.projects_created = projects_created
  self.connections_made = connections_made
  self.likes_received = likes_received
  self.comments_made = comments_made
  self.followers_count = followers_count
  self.following_count = following_count
  self.last_updated = timezone.now()
  self.save()
          ↓
Result stored in database
  UserStats {
      user: user_obj,
      projects_created: 5,
      connections_made: 12,
      likes_received: 23,
      comments_made: 8,
      followers_count: 15,
      following_count: 18,
      last_updated: now()
  }
```

---

## Summary of Key Data Flows

| Flow | Entry Point | Key Models | Database Writes |
|------|-------------|-----------|-----------------|
| Registration | POST `/register/` | User, StudentProfile, OTP | 3 new records |
| Login OTP | POST `/login/` → `/verify-otp/` | User, OTP | 1 update (OTP.is_used) |
| Project Creation | POST `/post-project/` | Project, Activity | 2 new records |
| Connection Request | POST `/send-connection/` | Connection, Notification, Activity | 3 new records |
| Message Send | POST `/messages/` | Message, Notification | 2 new records |
| Message Read | POST `/messages/status/` | MessageReadStatus | 1 new record |
| Find Collaborators | GET `/find-collaborators/` | StudentProfile, Connection | 0 writes (read-only) |
| Email Send | Various endpoints | None (external API) | 0 database writes |

