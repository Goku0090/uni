# UniSync Code Flow Diagrams

## 1. User Registration Flow

```
┌─────────────────────────────────────────────────────────────────┐
│                    USER REGISTRATION FLOW                       │
└─────────────────────────────────────────────────────────────────┘

User visits /register/
         │
         ▼
┌──────────────────────────────┐
│  register_view()             │
│  - GET: Display form         │
│  - POST: Validate input      │
└──────────────────────────────┘
         │
         ▼
    RegisterForm
    - Validate username uniqueness
    - Validate email uniqueness
    - Validate password strength (8+ chars, uppercase, lowercase, digit)
    - Check terms agreement
         │
         ├─── VALID ───────────┬──────── INVALID ────────┐
         │                      │                        │
         ▼                      ▼                        ▼
    Create User          Show errors        User sees form again
    (from Django auth)    on page            with error messages
         │
         ▼
    Create StudentProfile
    - Initialize with empty values
    - Set profile_completed=False
         │
         ▼
    Generate OTP
    - Create OTP model instance
    - Set purpose='registration'
    - Set 5-minute expiry
         │
         ▼
    Send OTP Email
    - Use configured email backend
    - Include OTP code in message
         │
         ▼
    Redirect to /verify-otp/registration/
    (User checks email for OTP)
         │
         ▼
    User Enters OTP Code
         │
         ▼
    verify_otp_view()
    - Fetch OTP record
    - Check expiry & used status
    - Compare provided code
         │
         ├─── VALID ───────┐     ├─── INVALID/EXPIRED ───┐
         │                 │     │                       │
         ▼                 ▼     ▼                       ▼
    Mark as used    Redirect    Show error      Redirect to register
    Set session     to login    message
    Log user in     page
         │
         ▼
    Registration Complete
    User can now login
```

---

## 2. OTP-Based Login Flow

```
┌─────────────────────────────────────────────────────────────────┐
│                    OTP-BASED LOGIN FLOW                         │
└─────────────────────────────────────────────────────────────────┘

User visits /login/
         │
         ▼
┌──────────────────────────────┐
│  login_view()                │
│  - GET: Display form         │
│  - POST: Handle login        │
└──────────────────────────────┘
         │
         ▼
    Try Standard Login (optional)
    - Authenticate with username + password
    ├─── SUCCESS ───────► Set session ──► Redirect to dashboard
    │
    └─── FAILED ───────────┐
                           │
                           ▼
                Check if OTP login enabled
                           │
                           ▼
                    Generate OTP
                    - Purpose='login'
                    - 5-minute expiry
                           │
                           ▼
                    Send OTP Email
                           │
                           ▼
                Redirect to /verify-otp/login/
                           │
                User checks email for OTP code
                           │
                           ▼
                User enters OTP
                           │
                           ▼
                verify_otp_view()
                - Check OTP validity
                - Verify against stored code
                           │
                    ┌──────┴──────┐
                    │             │
                   VALID        INVALID
                    │             │
                    ▼             ▼
            Mark as used      Increment
            Set session       attempts
            Login user        Show error
            │
            ▼
        Redirect to
        /dashboard/
```

---

## 3. Project Creation & Team Management Flow

```
┌─────────────────────────────────────────────────────────────────┐
│              PROJECT CREATION & TEAM MANAGEMENT FLOW            │
└─────────────────────────────────────────────────────────────────┘

User clicks "Post Project"
         │
         ▼
┌──────────────────────────────┐
│  post_project()              │
│  - GET: Display form         │
│  - POST: Create project      │
└──────────────────────────────┘
         │
         ▼
    ProjectForm Validation
    - Title (5-200 chars)
    - Description (20-5000 chars)
    - Category
    - Technologies (checkboxes)
    - Looking for roles
    - Timeline
    - GitHub link (if provided)
         │
         ├─── VALID ────────────────┐     ├─── INVALID ───┐
         │                          │     │               │
         ▼                          ▼     ▼               ▼
    Create Project         Set owner   Show errors    User re-enters
    instance               to current  on form        data
    - user = current_user      user
    - visibility='public'
    - save to DB
         │
         ▼
    Redirect to /my-projects/
    User sees new project
         │
         ▼
    ╔════════════════════════════════════════════════════╗
    ║ USER INVITES TEAM MEMBERS (From project detail)  ║
    ╚════════════════════════════════════════════════════╝
         │
         ▼
    User clicks "Invite Team Member"
         │
         ▼
    invite_to_team()
    - Display list of connections/users
    - Select role (contributor/viewer)
    - Send invitation
         │
         ▼
    Create ProjectInvitation
    - invited_user (selected)
    - invited_by = current_user
    - role = selected_role
    - status='pending'
    - expires_at = now + 7 days
         │
         ▼
    Send Notification Email
    (Optional: async with Celery)
         │
         ▼
    ╔════════════════════════════════════════════════════╗
    ║ INVITED USER RECEIVES INVITATION                  ║
    ╚════════════════════════════════════════════════════╝
         │
         ▼
    respond_to_team_invitation()
    - GET: Show invitation details
    - POST: Accept/Decline
         │
         ├─── ACCEPT ───────────────┐     ├─── DECLINE ───┐
         │                          │     │               │
         ▼                          ▼     ▼               ▼
    Call invitation       Create          Set status    User removed
    .accept()         ProjectMember      to 'declined'  from team
              │         - project        Update
         ├────┘         - user           responded_at
         │              - role
         ▼              - joined_at
    Set status to
    'accepted'
         │
         ▼
    User now appears on
    project team page
```

---

## 4. Messaging & Chat Flow

```
┌─────────────────────────────────────────────────────────────────┐
│                 DIRECT MESSAGE & CHAT FLOW                      │
└─────────────────────────────────────────────────────────────────┘

┌──────────────────────────────────────────────────────┐
│ DIRECT MESSAGE (1-to-1)                              │
└──────────────────────────────────────────────────────┘

User clicks "Chat" with another user
         │
         ▼
┌────────────────────────────────────────────┐
│  chat_view(user_id)                        │
│  - Fetch conversation history              │
│  - Load MessageReadStatus for read tracking│
│  - Display UI                              │
└────────────────────────────────────────────┘
         │
         ▼
    Retrieve Messages
    - Filter by (sender=A, receiver=B) OR (sender=B, receiver=A)
    - Order by created_at
    - Prefetch read status
         │
         ▼
    Display conversation
    Unread messages highlighted
         │
         ▼
    User types message
    Clicks Send
         │
         ▼
    POST to /api/messages/
         │
         ▼
    MessageListCreateView (DRF API)
    - Validate input
    - Create Message
         │
         ▼
    Create Message object
    - sender = current_user
    - receiver = target_user
    - content = text
    - message_type='text'
    - created_at = now
         │
         ▼
    (Optional) Create MessageReadStatus
    For tracking reads (scalable approach)
         │
         ▼
    WebSocket/Signal notification
    (if implemented) Real-time delivery
         │
         ▼
    Message displayed in chat
         │
         ▼
    User reads message
         │
         ▼
    mark_as_read_by(receiver)
    - Get or create MessageReadStatus
    - Set read_at = now
         │
         ▼
    Sender sees "read" indicator


┌──────────────────────────────────────────────────────┐
│ GROUP CHAT (Chat Room)                               │
└──────────────────────────────────────────────────────┘

User clicks "Create Group Chat"
         │
         ▼
    create_group_chat()
    - Display form with member selection
         │
         ▼
    User selects members
    Enters chat name & description
         │
         ▼
    Create ChatRoom
    - created_by = current_user
    - name = input_name
    - chat_type='group'
         │
         ▼
    Add creator + selected users
    to ChatRoomMember
         │
         ▼
    Redirect to enhanced_chat_view(room_id)
         │
         ▼
    Display chat room
    - Message history
    - Member list
    - Member activity status
         │
         ▼
    User sends message
         │
         ▼
    Create Message
    - chat_room = this room (not receiver)
    - sender = current_user
    - content = text
         │
         ▼
    Notify all room members
    Create MessageReadStatus entries
         │
         ▼
    get_unread_users()
    - Find users who haven't read
    - Highlight in UI
```

---

## 5. Project Filtering & Discovery Flow

```
┌─────────────────────────────────────────────────────────────────┐
│              PROJECT FILTERING & DISCOVERY FLOW                 │
└─────────────────────────────────────────────────────────────────┘

User visits /explore-projects/
         │
         ▼
┌──────────────────────────────────────────────┐
│  explore_projects_view()                     │
│  - GET projects based on user visibility     │
│  - Apply ProjectVisibilityFilter             │
└──────────────────────────────────────────────┘
         │
         ▼
┌──────────────────────────────────────────────┐
│  ProjectVisibilityFilter(user)               │
│  - Get all public projects                   │
│  - Get user's own projects                   │
│  - Get collaborative projects user is in     │
│  - Get shared private projects               │
└──────────────────────────────────────────────┘
         │
         ▼
    ┌─────────────────────────────────────┐
    │ Filtering Applied                   │
    └─────────────────────────────────────┘
    Filters to apply:
         │
         ├─── By Category ──────────┐
         │   (filter_by_category)   │
         │   - web, mobile, ai, etc │
         │
         ├─── By Technology ────────┐
         │   (filter_by_technology) │
         │   - python, django, etc  │
         │
         ├─── By Role ──────────────┐
         │   (filter_by_role)       │
         │   - backend_dev, etc     │
         │
         ├─── By Timeline ──────────┐
         │   (filter_by_timeline)   │
         │   - 1-2 weeks, 2-3 mo..  │
         │
         └─── Search ───────────────┐
             (search)
             - Title, description, skills
         │
         ▼
    Build QuerySet
    Q(category='web') & Q(technologies__contains='python')
         │
         ▼
    Execute DB Query
    Projects matching all filters
         │
         ▼
    Pagination
    - 10 projects per page
    - Page indicators
         │
         ▼
    Display Results
    - Project card (title, owner, tech stack)
    - Like button
    - View details link
         │
         ▼
    User clicks project
         │
         ▼
┌──────────────────────────────────────────────┐
│  project_detail(project_id)                  │
│  - Load full project data                    │
│  - Load team members                         │
│  - Load tasks & milestones                   │
│  - Load comments & likes                     │
└──────────────────────────────────────────────┘
         │
         ▼
    Display:
    - Project description
    - Team members (with roles)
    - Looking for roles (unfilled)
    - Tasks & Milestones
    - Comments
    - View/Like count
         │
         ▼
    User can:
    - Like project (if not owner)
    - Comment
    - Request to join
    - (If admin) Edit/Delete
    - (If not member) Request join
```

---

## 6. Connection & Networking Flow

```
┌─────────────────────────────────────────────────────────────────┐
│              CONNECTION & NETWORKING FLOW                       │
└─────────────────────────────────────────────────────────────────┘

User visits /find-collaborators/
         │
         ▼
    find_collaborators()
    - Display list of users
    - Filterable by skills, interests
         │
         ▼
    User can see:
    - User profiles
    - Skills & interests
    - Projects they're in
    - Connection status
         │
         ▼
    User clicks "Connect"
         │
         ▼
┌──────────────────────────────────────┐
│  send_connection_request(user_id)    │
│  - Check if already connected        │
└──────────────────────────────────────┘
         │
         ▼
    Create Connection record
    - sender = current_user
    - receiver = target_user
    - status='pending'
    - created_at = now
         │
         ▼
    (Optional) Send notification
    Target user notified of request
         │
         ▼
    ╔════════════════════════════════════════╗
    ║ TARGET USER SEES CONNECTION REQUEST    ║
    ╚════════════════════════════════════════╝
         │
         ▼
    /my-connections/ page
    Shows pending requests in separate tab
         │
         ├─────────────────────────────────┐
         │                                 │
         ▼                                 ▼
    accept_connection()             reject_connection()
    - Change status to              - Change status to
      'accepted'                      'rejected'
    - Users now connected           - Connection removed
    - Can message each other
         │
         ▼
    Both users see each other
    in connections list
         │
         ▼
    Can send direct messages
    (chat_view redirects based on connection)


┌────────────────────────────────────────────┐
│ FOLLOW SYSTEM                              │
└────────────────────────────────────────────┘

User visits other user's profile
         │
         ▼
    Click "Follow"
         │
         ▼
    follow_user(user_id)
    - Create Follow record
    - follower = current_user
    - following = target_user
         │
         ▼
    Button changes to "Following"
         │
         ▼
    Target user's activities appear
    in follower's activity feed
```

---

## 7. Activity Feed & Notifications Flow

```
┌─────────────────────────────────────────────────────────────────┐
│                ACTIVITY FEED & NOTIFICATIONS FLOW               │
└─────────────────────────────────────────────────────────────────┘

Any action in the platform triggers activity creation:
         │
    ┌────┼────┬────┬────┬────────┐
    │    │    │    │    │        │
    ▼    ▼    ▼    ▼    ▼        ▼
 Project Like Comment Connection Message Project
 created   on   added to  request  sent    updated
 project  project project  sent

    └────┬────┬────┬────┬────────┘
         │    │    │    │        │
         └────┼────┴────┴────────┘
              │
              ▼
         Create Activity record
         - user = actor
         - activity_type = one of above
         - title = descriptive title
         - related objects (project, target_user, etc)
         - is_public = True
         - created_at = now
              │
              ▼
         Create Notification
         (for relevant users)
         - user = recipient
         - notification_type = activity type
         - sender = actor
         - is_read = False
              │
              ▼
    ┌────────────────────────────────┐
    │ ACTIVITY FEED                  │
    └────────────────────────────────┘
         │
         ▼
    activity_feed()
    - Get users that current_user follows
    - Get activities from those users
    - Order by created_at DESC
    - Filter is_public=True
         │
         ▼
    Display:
    - "John created project XYZ"
    - "Sarah liked your project"
    - "Mike commented on project XYZ"
    - Timestamp (e.g., "2 hours ago")
         │
         ▼
    User can click to view full context


    ┌────────────────────────────────┐
    │ NOTIFICATIONS                  │
    └────────────────────────────────┘
         │
         ▼
    notifications_view()
    - Get all notifications for current_user
    - Group by type
    - Mark as read on interaction
         │
         ▼
    Mark notification as read
    - mark_notification_read(notification_id)
    - Update is_read = True
    - Update read_at timestamp
         │
         ▼
    Notification badge
    Unread count = Notification.objects.filter(
                     user=current_user,
                     is_read=False
                   ).count()
```

---

## 8. Email Backend Selection Flow

```
┌─────────────────────────────────────────────────────────────────┐
│                EMAIL BACKEND SELECTION FLOW                     │
└─────────────────────────────────────────────────────────────────┘

App startup (settings.py loaded)
         │
         ▼
Check environment variables:
         │
    ┌────┴────────────────────────────────┐
    │                                      │
    ▼                                      ▼
Is BREVO_API_KEY          Is ZEPTO_MAIL_API_KEY &
set?                      ZEPTO_MAIL_TOKEN set?
    │                                      │
    │ YES                                  │ YES
    ▼                                      ▼
Use Brevo          Use ZeptoMail
Backend            Backend
└────┬──────────────┬──────────────┘
     │              │
     └──────┬───────┘
            │
            ▼
    Is EMAIL_HOST_USER &
    EMAIL_HOST_PASSWORD set?
            │
            │ YES
            ▼
        Use Gmail SMTP
        Backend
            │
            └─────────┬─────────┘
                      │
                      ▼
                Use Console Backend
                (Development only)
                Print to console/logs


┌──────────────────────────────────────┐
│ EMAIL SENDING PROCESS                │
└──────────────────────────────────────┘

When send_mail() called:
         │
         ▼
Selected email backend processes:
         │
    ┌────┴────────────┐
    │                 │
    ▼                 ▼
Brevo API        Gmail SMTP
call             SMTP connection
│                │
├─ API request   ├─ SMTP auth
├─ Rate limits   ├─ Message compose
├─ Response      ├─ Send
└─ Handle err    └─ Close connection
    │                 │
    └────┬────────────┘
         │
         ▼
    Success?
    │
    ├─ YES: Log success
    │       OTP delivered
    │
    └─ NO:  Log error
            Retry logic (if implemented)
            Show user error message
```

---

## 9. View Authorization & Permission Flow

```
┌─────────────────────────────────────────────────────────────────┐
│              VIEW AUTHORIZATION & PERMISSION FLOW               │
└─────────────────────────────────────────────────────────────────┘

Protected View Request
         │
         ▼
@login_required decorator
         │
    ├─ User logged in? 
    │
    ├─ YES → Continue to view
    │
    └─ NO  → Redirect to /login/
         │
         ▼
View Function Executes
         │
         ▼
Check Object-Level Permissions
         │
    For edit_project():
         │
    ├─ Project owner?
    │  (project.owner == request.user)
    │  ├─ YES → Allow edit
    │  └─ NO  → Check if project member
    │
    └─ Project member with edit role?
       (ProjectMember.objects.filter(
          project=project,
          user=request.user,
          role__in=['owner', 'admin', 'contributor']
       ))
       ├─ YES → Allow edit
       └─ NO  → 403 Forbidden


┌──────────────────────────────────────┐
│ PROJECT MEMBER ROLE PERMISSIONS      │
└──────────────────────────────────────┘

Roles:
├─ Owner
│  ├─ can_manage_project = True
│  ├─ can_edit_project = True
│  ├─ can_manage_tasks = True
│  └─ can_invite_members = True
│
├─ Admin
│  ├─ can_manage_project = True
│  ├─ can_edit_project = True
│  ├─ can_manage_tasks = True
│  └─ can_invite_members = True
│
├─ Contributor
│  ├─ can_manage_project = False
│  ├─ can_edit_project = True
│  ├─ can_manage_tasks = True
│  └─ can_invite_members = False
│
└─ Viewer
   ├─ can_manage_project = False
   ├─ can_edit_project = False
   ├─ can_manage_tasks = False
   └─ can_invite_members = False


┌──────────────────────────────────────┐
│ MESSAGE PERMISSION CHECKING          │
└──────────────────────────────────────┘

Get message:
         │
         ▼
Is sender, receiver, or room member?
         │
    ├─ YES → Allow read
    └─ NO  → 403 Forbidden

Mark as read:
         │
         ▼
Is receiver or room member?
         │
    ├─ YES → Allow mark as read
    └─ NO  → 403 Forbidden
```

---

## 10. User Profile NLP Analysis Flow

```
┌─────────────────────────────────────────────────────────────────┐
│              USER PROFILE NLP ANALYSIS FLOW                     │
└─────────────────────────────────────────────────────────────────┘

User submits profile with skills & interests text:
         │
         ▼
StudentProfileNLP.preprocess_text(text)
         │
    ├─ Convert to lowercase
    ├─ Remove special characters
    ├─ Tokenize
    ├─ Remove stopwords
    └─ Lemmatize
         │
         ▼
Clean text ready for analysis
         │
         ▼
Extract Skills:
StudentProfileNLP.extract_skills(text)
         │
    ├─ Check against TECH_SKILLS list
    │  ├─ Programming languages
    │  ├─ Frameworks
    │  └─ Tools
    │
    └─ Return matched skills array
         │
         ▼
Categorize Interests:
StudentProfileNLP.categorize_interests(text)
         │
    ├─ Check against INTEREST_CATEGORIES
    │  ├─ ai_ml
    │  ├─ web_dev
    │  ├─ mobile_dev
    │  ├─ blockchain
    │  ├─ cybersecurity
    │  ├─ game_dev
    │  ├─ iot
    │  └─ design
    │
    └─ Return interest categories
         │
         ▼
Save to StudentProfile:
         │
    ├─ skills = ['python', 'javascript', ...]
    └─ project_interests = ['web_dev', 'ai_ml', ...]
         │
         ▼
Enable Features:
         │
    ├─ Better project recommendations
    ├─ Collaborator matching
    ├─ Skill-based filtering
    └─ Interest-based activity feed


┌──────────────────────────────────────┐
│ COLLABORATOR MATCHING                │
└──────────────────────────────────────┘

find_collaborators():
         │
         ▼
For each potential collaborator:
         │
    ├─ Calculate profile similarity
    │  (StudentProfileNLP.calculate_profile_similarity)
    │  - Compare skills
    │  - Compare interests
    │  - TF-IDF vectorization
    │  - Cosine similarity
    │
    └─ Generate similarity score (0-1)
         │
         ▼
Rank by similarity
Top matches shown first
         │
         ▼
Display:
├─ Collaborator profile
├─ Matching skills
├─ Matching interests
└─ Connection button
```

---

This comprehensive flow documentation covers all major user journeys and data flows in the UniSync application.

**Last Updated:** 2026-01-29
