# UniSync - Detailed Feature Breakdown

## 1. Authentication & Authorization System

### 1.1 Registration Process
**File**: `accounts/views.py` (lines 209-300+)

```python
def register_view(request):
    # Step 1: Collect user data
    - username, email, password, confirm_password
    - full_name, college, location, interests, bio
    
    # Step 2: Validation
    - Check required fields
    - Verify password strength (8+ chars, uppercase, digit)
    - Confirm password match
    - Check username/email uniqueness
    
    # Step 3: Create user
    - Create User object
    - Create StudentProfile
    - Generate OTP for email verification
    
    # Step 4: Send OTP email
    - Use configured email backend
    - HTML + Plain text email
    - 5-minute expiry
```

**Email Template** (HTML):
```html
Subject: 🚀 Your Registration OTP Code
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Hi there!
Your OTP: [6-DIGIT CODE]
Valid for: 5 minutes only
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
```

### 1.2 OTP Authentication
**Model**: `OTP` (models.py, lines 55-123)

```python
class OTP(models.Model):
    email: EmailField
    otp_code: CharField(6 digits)
    purpose: CharField (login/registration/reset)
    is_used: BooleanField
    created_at: DateTimeField
    expires_at: DateTimeField (created_at + 5 minutes)
    
    Methods:
    - is_valid()           # Check expiry & used status
    - verify_otp()         # Verify against provided code
    - generate_otp()       # Create new OTP, deactivate old ones
    - hash_otp()           # SHA-256 hashing (optional)
```

**Verification Flow**:
```
1. User enters email
2. Generate random 6-digit OTP
3. Set expires_at = now + 5 minutes
4. Deactivate any existing OTPs for this email/purpose
5. Send via email backend
6. User submits OTP
7. Verify: not expired, not used, matches code
8. Mark as used, activate account
```

### 1.3 Social Login (OAuth)
**Configuration** (settings.py, lines 273-291):

```python
SOCIALACCOUNT_PROVIDERS = {
    'google': {
        'SCOPE': ['profile', 'email'],
        'AUTH_PARAMS': {'access_type': 'online'},
    },
    'github': {
        'SCOPE': ['user:email', 'read:user'],
    }
}
```

**Features**:
- Auto signup on first login
- Email extraction
- Custom signup form: `CustomSocialSignupForm`
- Profile auto-fill from OAuth data

### 1.4 Password Management
**Functions** (views.py):
```python
def password_reset():
    # 1. User enters email
    # 2. Generate OTP (purpose='reset')
    # 3. Send reset OTP email
    # 4. Verify OTP
    # 5. Allow new password entry
    # 6. Hash & save new password

def change_password():
    # For logged-in users
    # 1. Verify current password
    # 2. Validate new password strength
    # 3. Update password
```

### 1.5 Session Management
**Middleware** (settings.py, line 66):
```python
MIDDLEWARE = [
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'allauth.account.middleware.AccountMiddleware',
]

Session timeout: Django default (2 weeks)
Secure cookies: Configurable via environment
```

---

## 2. Project Management System

### 2.1 Project Model
**File**: `accounts/models.py` (lines 251-300+)

```python
class Project(models.Model):
    # Basic Info
    user: ForeignKey(User)              # Project owner
    title: CharField(200)
    description: TextField
    category: CharField                  # Web App, Mobile, Data Science, etc.
    
    # Technical Details
    technologies: CharField             # Comma-separated
    github_link: URLField
    project_link: URLField
    
    # Collaboration
    looking_for: CharField              # Skills/roles needed
    collaboration_needs: TextField
    timeline: CharField                 # Expected duration
    
    # Status & Visibility
    is_active: BooleanField(default=True)
    visibility: CharField (public/private/hidden)
    
    # Metadata
    created_at: DateTimeField
    updated_at: DateTimeField
    
    # Relations
    members: ProjectMember (through)
    tasks: ProjectTask (many)
    milestones: ProjectMilestone (many)
    comments: Comment (many)
    likes: Like (many)
```

### 2.2 Project Lifecycle

#### Creation Flow
```
User Input (form)
    ↓
Validate (title, description required)
    ↓
Create Project object
    ↓
Auto-add creator as owner in ProjectMember
    ↓
Create Activity entry (project_created)
    ↓
Redirect to project list
    ↓
Visible in feeds/search
```

#### Update Flow
```
Get project (verify ownership)
    ↓
Validate new data
    ↓
Update fields
    ↓
Auto-update: updated_at timestamp
    ↓
NO activity created (just updates)
```

#### Delete Flow
```
Get project (verify ownership)
    ↓
Delete ProjectMembers
    ↓
Delete ProjectTasks
    ↓
Delete ProjectMilestones
    ↓
Delete Comments
    ↓
Delete Likes
    ↓
Delete Project
    ↓
Activity not recorded (cascade)
```

### 2.3 Project Visibility & Filtering
**Function**: `ProjectVisibilityFilter` (utils.py)

```python
class ProjectVisibilityFilter:
    Filter types:
    
    1. By visibility setting
       - public    → All users see
       - private   → Only members see
       - hidden    → Only owner sees (not even in search)
    
    2. By category
       - Web App, Mobile App, Data Science, AI/ML, etc.
    
    3. By technology
       - Python, JavaScript, React, Django, etc.
    
    4. By timeline
       - Short-term, Medium-term, Long-term
    
    5. By collaboration needs
       - Frontend, Backend, Full-stack, Designer, etc.
    
    6. By member count
       - Solo, Small (2-3), Medium (4-6), Large (7+)
    
    7. By creation date
       - Latest, This week, This month
    
    8. By engagement
       - Most liked, Most commented, Most joined
```

**Example Query**:
```python
projects = Project.objects.filter(
    visibility='public',
    category='Web App',
    technologies__icontains='React'
)
```

### 2.4 Team Management
**Models**: `ProjectMember`, `ProjectInvitation`, `ProjectTeam`

```python
class ProjectMember(models.Model):
    project: ForeignKey(Project)
    user: ForeignKey(User)
    role: CharField (owner/admin/contributor/viewer)
    is_active: BooleanField
    joined_at: DateTimeField
    
    Permissions by role:
    - owner      → Can manage everything, invite, delete
    - admin      → Can manage members, tasks, edit project
    - contributor → Can edit tasks, comment, upload files
    - viewer     → Can view only, comment

class ProjectInvitation(models.Model):
    project: ForeignKey(Project)
    invited_user: ForeignKey(User)
    invited_by: ForeignKey(User)
    role: CharField
    message: TextField (optional)
    status: CharField (pending/accepted/declined/expired)
    created_at: DateTimeField
    expires_at: DateTimeField (14 days from creation)
    
    Methods:
    - accept()   → Create ProjectMember, mark accepted
    - decline()  → Mark declined
```

**Invitation Flow**:
```
1. Project owner invites user
2. Create ProjectInvitation (status=pending)
3. Send notification to invited user
4. User clicks "Accept"
5. Create ProjectMember
6. Set status=accepted, responded_at=now
7. User added to team
8. Notification sent to inviter
9. Auto-expire after 14 days
```

### 2.5 Tasks & Milestones

#### Tasks
```python
class ProjectTask(models.Model):
    project: ForeignKey(Project)
    title: CharField(200)
    description: TextField
    assigned_to: ForeignKey(User, nullable)
    assigned_by: ForeignKey(User)
    
    status: CharField (todo/in_progress/review/completed/cancelled)
    priority: CharField (low/medium/high/urgent)
    
    due_date: DateField
    completed_at: DateTimeField
    created_at: DateTimeField
    
    Methods:
    - mark_completed()  → Set status=completed, set completed_at
```

#### Milestones
```python
class ProjectMilestone(models.Model):
    project: ForeignKey(Project)
    title: CharField(200)
    description: TextField
    due_date: DateField
    is_completed: BooleanField
    completed_at: DateTimeField
    completed_by: ForeignKey(User, nullable)
    
    Methods:
    - mark_completed(user)  → Set is_completed=True, record user
```

---

## 3. Collaboration & Social Features

### 3.1 Connection System
**Model**: `Connection` (models.py, lines 126-146)

```python
class Connection(models.Model):
    sender: ForeignKey(User)
    receiver: ForeignKey(User)
    status: CharField (pending/accepted/rejected)
    created_at: DateTimeField
    updated_at: DateTimeField
    
    Constraint: unique_together=['sender', 'receiver']
    (one connection per pair, directional)
```

**Flow**:
```
Step 1: Send Request
    User A clicks "Connect" on User B's profile
    → Connection(sender=A, receiver=B, status='pending')
    → Notification sent to B
    
Step 2: User B Reviews
    B sees pending connection in notifications
    
Step 3: Accept/Reject
    Accept:  status='accepted'  → Can message each other
    Reject:  status='rejected'  → Cannot resend for 30 days
    
Step 4: Message
    Once accepted, can send direct messages
```

### 3.2 Follow System
**Model**: `Follow` (models.py, lines 456-472)

```python
class Follow(models.Model):
    follower: ForeignKey(User)
    following: ForeignKey(User)
    created_at: DateTimeField
    
    Constraint: unique_together=['follower', 'following']
    
Purpose:
    - See user's activities in feed
    - Get updates on their projects
    - No reciprocal follow required
```

### 3.3 Find Collaborators Feature
**Function**: `find_collaborators_view()` (views.py, lines 1370-1585)

**Features**:
1. **Search Query**
   - Full-text search across:
     - Profile full_name
     - College name
     - Bio text
     - Skills (JSON array)
   - Case-insensitive matching

2. **Filters**
   ```python
   Filters available:
   - college           (dropdown list)
   - skills            (multi-select)
   - interests         (multi-select)
   - role_preference   (frontend/backend/fullstack/designer/etc)
   - location          (text search)
   ```

3. **Match Scoring**
   ```python
   Matching algorithm:
   
   for each user_profile:
       matching_interests = user_interests ∩ profile_interests
       match_score = (len(matching_interests) / len(user_interests)) * 100
       
   # Sort by match_score descending
   suggestions.sort(key=lambda x: x.match_score, reverse=True)
   
   # Show top 20 matches
   ```

4. **Result Types**
   - Search results (if query provided)
   - Suggestions (based on filters)
   - All users (fallback)

5. **Display Info**
   ```python
   For each user:
   - Full name or username
   - College
   - Bio
   - Profile photo
   - Interests/Skills (tagged)
   - Connection status (connected/pending/none)
   - Match score (if applicable)
   ```

### 3.4 Activity Feed
**Model**: `Activity` (models.py, lines 475-507)

```python
class Activity(models.Model):
    user: ForeignKey(User)
    activity_type: CharField (
        profile_updated,
        project_created,
        project_liked,
        connection_made,
        message_sent,
        comment_added,
        user_followed,
        task_completed,
        milestone_completed
    )
    title: CharField(200)
    description: TextField
    project: ForeignKey(Project, nullable)
    target_user: ForeignKey(User, nullable)
    connection: ForeignKey(Connection, nullable)
    is_public: BooleanField(default=True)
    created_at: DateTimeField
    
    Visible to:
    - User themselves (always)
    - Followers (if is_public=True)
    - Team members (projects, tasks)
```

**Activity Creation Triggers**:
```python
# Automatic
- Post project             → create_activity(type='project_created')
- Like project             → create_activity(type='project_liked')
- Comment on project       → create_activity(type='comment_added')
- Accept connection        → create_activity(type='connection_made')
- Follow user              → create_activity(type='user_followed')
- Update profile           → create_activity(type='profile_updated')
- Complete task            → create_activity(type='task_completed')
- Complete milestone       → create_activity(type='milestone_completed')
```

---

## 4. Messaging & Communication

### 4.1 Direct Messaging
**Models**: `Message`, `ChatRoom`, `ChatRoomMember`, `MessageReadStatus`

```python
class Message(models.Model):
    # Direct message fields
    sender: ForeignKey(User)
    receiver: ForeignKey(User, nullable)      # Null for group
    content: TextField
    message_type: CharField (text/file/image/call)
    
    # Group chat fields
    chat_room: ForeignKey(ChatRoom, nullable)
    
    # Threading support
    reply_to: ForeignKey(Message, nullable)   # For message threads
    
    # Metadata
    created_at: DateTimeField
    updated_at: DateTimeField
    
    Methods:
    - mark_as_read_by(user)    → Create MessageReadStatus
    - is_read_by(user)         → Check if read
    - get_read_by_users()      → All who read
    - get_read_count()         → Count readers
    - get_unread_users()       → For group chats
```

**Read Status**:
```python
class MessageReadStatus(models.Model):
    message: ForeignKey(Message)
    user: ForeignKey(User)
    read_at: DateTimeField
    
    # Many-to-many relationship between Message and User
    # Allows tracking multiple readers for group messages
```

### 4.2 Group Chat
```python
class ChatRoom(models.Model):
    name: CharField(200)
    chat_type: CharField (direct/group)
    members: ManyToManyField(User, through=ChatRoomMember)
    created_at: DateTimeField
    updated_at: DateTimeField
    
    # Example: Project Discussion Room
    # ChatRoom.objects.create(
    #     name="MyProject - General",
    #     chat_type='group'
    # )
    # Add members to room
```

### 4.3 Message Features
1. **File Attachments**
   ```python
   class MessageFile(models.Model):
       message: ForeignKey(Message)
       file: ForeignKey(File)
       uploaded_at: DateTimeField
   ```

2. **Reactions**
   ```python
   class MessageReaction(models.Model):
       message: ForeignKey(Message)
       user: ForeignKey(User)
       reaction: CharField  # Emoji or text (👍, ❤️, etc)
       created_at: DateTimeField
   ```

3. **Call Support**
   ```python
   Message.call_type = CharField (voice/video)
   # Used for initiating calls within chat
   ```

### 4.4 Comments on Projects
**Model**: `Comment` (models.py, lines 291-320+)

```python
class Comment(models.Model):
    user: ForeignKey(User)
    project: ForeignKey(Project)
    content: TextField
    parent: ForeignKey(Comment, nullable)      # Threading
    
    # Approval workflow (optional)
    is_approved: BooleanField(default=True)
    
    created_at: DateTimeField
    updated_at: DateTimeField
    
    Methods:
    - get_replies()         → Get child comments
    - edit_comment()        → Update content
    - delete_comment()      → Mark deleted (soft delete)
```

**Comment Flow on Project Detail**:
```
1. User views project detail
2. Load project + comments (paginated)
3. Comments sorted by created_at (latest first)
4. Show 5-10 comments per page
5. User submits new comment
6. Create Comment object
7. Create Activity (comment_added)
8. Send notification to project owner
9. Comment appears immediately (if approved=True)
10. Reload comment section
```

---

## 5. Notifications System

### 5.1 Notification Model
**File**: `accounts/models.py`

```python
class Notification(models.Model):
    NOTIFICATION_TYPES = [
        ('connection_request', 'Connection Request'),
        ('connection_accepted', 'Connection Accepted'),
        ('project_comment', 'Project Comment'),
        ('project_like', 'Project Like'),
        ('message', 'New Message'),
        ('project_invite', 'Project Invitation'),
        ('user_follow', 'User Followed You'),
        ('milestone_completed', 'Milestone Completed'),
        ('task_assigned', 'Task Assigned'),
    ]
    
    user: ForeignKey(User)               # Recipient
    related_user: ForeignKey(User)       # Who triggered? (nullable)
    notification_type: CharField
    title: CharField(200)
    description: TextField
    
    # Optional relations to related objects
    project: ForeignKey(Project, nullable)
    connection: ForeignKey(Connection, nullable)
    message: ForeignKey(Message, nullable)
    
    # Status
    is_read: BooleanField(default=False)
    action_url: CharField (where to go when clicked)
    
    # Metadata
    created_at: DateTimeField
    
    Methods:
    - mark_as_read()
    - get_notification_badge_count()
```

### 5.2 Notification Triggers
**Service**: `accounts/services/notification_service.py`

```python
def notify_connection_request(sender, receiver):
    # When connection request sent
    Notification.objects.create(
        user=receiver,
        related_user=sender,
        notification_type='connection_request',
        title=f"{sender.username} sent you a connection request",
        action_url=f'/find-collaborators/?username={sender.username}'
    )

def notify_project_comment(commenter, project):
    # When someone comments on your project
    if project.user != commenter:
        Notification.objects.create(
            user=project.user,
            related_user=commenter,
            notification_type='project_comment',
            title=f"{commenter.username} commented on your project",
            project=project,
            action_url=f'/projects/{project.id}/'
        )

def notify_message(sender, receiver):
    # When new message received
    Notification.objects.create(
        user=receiver,
        related_user=sender,
        notification_type='message',
        message=message_obj,
        action_url=f'/messages/{sender.username}/'
    )
```

### 5.3 Notification Display
```python
# In dashboard/navbar
unread_count = Notification.objects.filter(
    user=request.user,
    is_read=False
).count()

# Show badge with count
# Click to open notification panel
# Mark all as read on view
```

---

## 6. Email System

### 6.1 Email Backend Selection (settings.py, lines 219-257)

```python
Priority order:

1. BREVO (Production - Recommended)
   EMAIL_BACKEND = 'accounts.brevo_mail_backend.BrevoMailBackend'
   BREVO_API_KEY = os.getenv('BREVO_API_KEY')
   ✓ Reliable transactional emails
   ✓ Good deliverability
   ✓ Detailed analytics

2. ZEPTOMAIL (Alternative)
   EMAIL_BACKEND = 'accounts.zepto_mail_backend.ZeptoMailBackend'
   ZEPTO_MAIL_API_KEY = os.getenv('ZEPTO_MAIL_API_KEY')
   ZEPTO_MAIL_TOKEN = os.getenv('ZEPTO_MAIL_TOKEN')

3. GMAIL SMTP (Fallback)
   EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
   EMAIL_HOST = 'smtp.gmail.com'
   EMAIL_PORT = 587
   EMAIL_USE_TLS = True
   EMAIL_HOST_USER = os.getenv('EMAIL_HOST_USER')
   EMAIL_HOST_PASSWORD = os.getenv('EMAIL_HOST_PASSWORD')

4. CONSOLE (Development)
   EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'
   # Prints to terminal
```

### 6.2 Email Types Sent

#### OTP Email
```
Subject: 🚀 Your {purpose} OTP Code
From: noreply@unisync.app

Content:
- Your OTP: [6-DIGIT-CODE]
- Valid for: 5 minutes
- Purpose: Login/Registration/Reset
- Warning: Don't share this code

Format: HTML + Plain text (EmailMultiAlternatives)
```

#### Project Invitation
```
Subject: Invitation to join project: {project.title}
From: {inviter.email}

Content:
- Project name & description
- Role offered: owner/admin/contributor/viewer
- Message from inviter
- Accept/Decline buttons
```

#### Comment Notification
```
Subject: {user.username} commented on {project.title}
From: noreply@unisync.app

Content:
- "User X commented: {comment text}"
- View project link
- Reply directly link
```

#### Connection Request
```
Subject: {user.username} wants to connect with you
From: noreply@unisync.app

Content:
- User profile snippet
- Accept/Reject buttons
- View profile link
```

### 6.3 Email Sending
**Function**: `send_otp_email()` (views.py, lines 135-196)

```python
def send_otp_email(email, otp_code, purpose):
    subject = f"🚀 Your {purpose.title()} OTP Code"
    from_email = settings.DEFAULT_FROM_EMAIL
    to = [email]
    
    # Plain text version
    text_message = f"""
    Hi there!
    Your OTP for {purpose} is: {otp_code}
    This OTP is valid for 5 minutes only.
    ...
    """
    
    # HTML version
    html_message = f"""
    <!DOCTYPE html>
    <html>
    ...
    """
    
    try:
        msg = EmailMultiAlternatives(subject, text_message, from_email, to)
        msg.attach_alternative(html_message, "text/html")
        msg.send()
        logger.info(f"OTP email sent to {email}")
    except Exception as e:
        logger.error(f"Failed to send OTP email: {str(e)}")
        # Notify admins
        mail_admins(..., fail_silently=True)
```

---

## 7. User Profile & Statistics

### 7.1 StudentProfile Model
```python
class StudentProfile(models.Model):
    user: OneToOneField(User)
    
    # Personal Info
    full_name: CharField
    bio: TextField
    college: CharField
    location: CharField
    
    # Professional
    skills: JSONField (array)          # ["Python", "JavaScript", "Django"]
    interests: JSONField (array)       # ["Web Dev", "ML", "Mobile"]
    project_interests: JSONField (array)
    role_preference: CharField         # "Backend Developer"
    
    # Social
    profile_photo: ImageField
    github: URLField
    linkedin: URLField
    portfolio: URLField
    behance: URLField
    
    # Status
    profile_completed: BooleanField
    created_at: DateTimeField
    updated_at: DateTimeField
    
    Methods:
    - get_display_name() → Returns full_name or username
```

### 7.2 UserStats Model
```python
class UserStats(models.Model):
    user: OneToOneField(User)
    
    projects_created: PositiveIntegerField
    connections_made: PositiveIntegerField
    likes_received: PositiveIntegerField
    comments_made: PositiveIntegerField
    projects_joined: PositiveIntegerField
    tasks_completed: PositiveIntegerField
    followers_count: PositiveIntegerField
    following_count: PositiveIntegerField
    last_updated: DateTimeField
    
    Methods:
    - update_stats() → Recalculate all counts from DB
```

### 7.3 Public Profile View
**Function**: `student_profile_view()` or similar

```
Display for User A viewing User B:

[Profile Header]
- Avatar (profile_photo)
- Name (full_name)
- College
- Location
- Match score (if applicable)

[About Section]
- Bio
- Skills (tags)
- Interests (tags)
- Role preference

[Social Links]
- GitHub, LinkedIn, Portfolio, Behance

[Stats Box]
- Projects created
- Connections made
- Skills count
- Interests count

[Action Buttons]
- Connect (if not connected)
- Message (if connected)
- View projects
- Follow/Unfollow

[User's Projects]
- List of public projects
```

---

## 8. Security & Validation

### 8.1 Input Sanitization
**Function**: `sanitize_input()` (views.py, lines 107-133)

```python
def sanitize_input(text, max_length=None):
    # Remove HTML tags
    text = strip_tags(text)
    
    # Remove dangerous characters
    text = re.sub(r'[<>]', '', text)
    
    # Trim whitespace
    text = text.strip()
    
    # Apply length limit
    if max_length:
        text = text[:max_length]
    
    return text
```

**Applied to**:
- Comment content
- Project descriptions
- User bios
- Chat messages
- Profile fields

### 8.2 Password Validation
**Settings**: settings.py, lines 141-146

```python
AUTH_PASSWORD_VALIDATORS = [
    UserAttributeSimilarityValidator(),    # Not similar to username
    MinimumLengthValidator(),              # Min 8 characters
    CommonPasswordValidator(),             # Not in common passwords list
    NumericPasswordValidator(),            # Not all numbers
]

Additional checks in register_view:
    - At least 1 uppercase letter
    - At least 1 digit
    - Password != confirm_password check
```

### 8.3 CSRF Protection
```python
MIDDLEWARE includes:
- 'django.middleware.csrf.CsrfViewMiddleware'

All POST forms:
- {% csrf_token %} in templates
- Automatically validated

CSRF_COOKIE_SECURE: Can be enabled for HTTPS
```

### 8.4 Authentication Decorators
```python
@login_required
def protected_view(request):
    # Redirect to login if not authenticated
    pass

@user_passes_test(lambda u: u.is_staff)
def admin_view(request):
    # Redirect if not admin
    pass
```

### 8.5 Permission Checks
```python
# Project ownership
project = get_object_or_404(Project, id=id, user=request.user)

# Team role validation
ProjectMember.can_manage_project  # Boolean property by role
ProjectMember.can_edit_project    # Boolean property by role

# Connection status
if not Connection.objects.filter(..., status='accepted').exists():
    return HttpResponseForbidden()
```

---

## 9. Performance Optimizations

### 9.1 Database Query Optimization
```python
# Use select_related for foreign keys
projects = Project.objects.select_related(
    'user__student_profile'
).all()

# Use prefetch_related for reverse relations
comments = Comment.objects.prefetch_related(
    'user__student_profile'
).filter(project=project)

# Filter early to reduce result set
projects = Project.objects.filter(
    visibility='public'
).select_related('user__student_profile')[:20]
```

### 9.2 Caching Strategy
```python
from django.views.decorators.cache import cache_page

@cache_page(60 * 5)  # Cache for 5 minutes
def get_projects_feed(request):
    # Expensive query
    pass

# Cache individual objects
from django.core.cache import cache
cache.set('user_profile_' + str(user_id), profile, 60*30)
profile = cache.get('user_profile_' + str(user_id))
```

### 9.3 Pagination
```python
# In views
from django.core.paginator import Paginator

paginator = Paginator(projects, 10)  # 10 per page
page_number = request.GET.get('page')
page_obj = paginator.get_page(page_number)

# In template
{% for project in page_obj %}
    ...
{% endfor %}

{% if page_obj.has_next %}
    <a href="?page={{ page_obj.next_page_number }}">Next</a>
{% endif %}
```

### 9.4 API Response Optimization
```python
# Only return needed fields
class ProjectSerializer(serializers.ModelSerializer):
    class Meta:
        model = Project
        fields = ['id', 'title', 'description', 'user']
        # Don't include heavy fields like markdown descriptions

# Limit nested relations
# Use depth=1 cautiously (can cause N+1 queries)
```

---

## 10. Testing & Quality Assurance

### 10.1 Test Files Present
- test_login.py
- test_email.py
- test_profile_view.py
- test_filter.py
- test_comments_api.py
- test_zeptomail.py

### 10.2 Recommended Test Coverage
```python
# Model tests
- OTP generation & verification
- Connection accept/reject logic
- Project member permissions
- Comment threading

# View tests
- Login with valid/invalid OTP
- Project creation authorization
- Comment posting restrictions
- Profile update validation

# Form tests
- Password strength validation
- Email uniqueness
- Username validation

# Integration tests
- Complete registration flow
- Project creation → Comment → Notification flow
- Connection request → Message flow
```

### 10.3 Manual Testing Checklist
```
Authentication:
☐ Register with email
☐ Verify OTP
☐ Login with password
☐ Google OAuth login
☐ GitHub OAuth login
☐ Password reset
☐ Logout

Projects:
☐ Create project
☐ Edit project
☐ Delete project
☐ Like project
☐ Comment on project
☐ Filter projects
☐ Search projects

Collaboration:
☐ Send connection request
☐ Accept connection
☐ Send message to connection
☐ Send group message
☐ Invite to project
☐ Accept project invite

Profile:
☐ Edit profile photo
☐ Update bio/skills
☐ View public profile
☐ Follow user
☐ View statistics
```

---

## Summary

UniSync implements a **production-grade collaboration platform** with:

✅ **Robust Authentication**: OTP, OAuth, password management  
✅ **Project Management**: CRUD, teams, tasks, milestones  
✅ **Social Features**: Connections, follows, activities  
✅ **Communication**: Direct messaging, comments, groups  
✅ **Notifications**: Real-time alerts across features  
✅ **Security**: Input validation, CSRF protection, permission checks  
✅ **Performance**: Query optimization, pagination, caching  

The architecture is **scalable**, **maintainable**, and **extensible** for future enhancements.
