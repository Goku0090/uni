# UniSync - Data Flow & System Interactions

## User Registration Flow

```
1. User submits registration form
   ├─ Username, Email, Password → /register/
   │
2. Backend validation
   ├─ Check username availability
   ├─ Check email availability
   ├─ Validate password strength
   └─ Sanitize input
   │
3. Create User & StudentProfile
   ├─ Create Django User object
   ├─ Create StudentProfile (empty/basic)
   ├─ Set profile_completed = False
   └─ Create UserStatus = offline
   │
4. Send welcome email
   ├─ Choose email backend (Brevo/ZeptoMail/Gmail/Console)
   ├─ Render HTML email template
   ├─ Send welcome email
   └─ Log email sent
   │
5. Create session
   ├─ Generate session ID
   ├─ Store in Redis/database
   └─ Return session cookie
   │
6. Redirect to OTP verification
   └─ /verify-otp/registration/?email=user@example.com
```

---

## OTP Authentication Flow

```
Login Request
├─ User submits email → /login/
│
Generate OTP
├─ Create 6-digit random code
├─ Set expiry (5 minutes)
├─ Deactivate previous OTPs for this email
├─ Store in OTP model
└─ Send via email
│
Verify OTP
├─ User submits code → /verify-otp/login/
├─ Check if OTP is valid (not expired, not used)
├─ Check if code matches
├─ Mark OTP as used
├─ Create Django session
└─ Log user in
│
Post-Login
├─ Update UserStatus = online
├─ Create Activity record = "user_login"
├─ Redirect to dashboard
└─ Set session expiry
```

---

## Project Creation Flow

```
User creates project
├─ POST /post-project/
├─ Submit form with:
│  ├─ Title, Description
│  ├─ Collaboration needs (array)
│  ├─ Technologies (array)
│  ├─ Visibility (public/private/college)
│  └─ Images/files
│
Database insert
├─ Create Project record
│  ├─ owner = current_user
│  ├─ created_at = now
│  ├─ likes_count = 0
│  ├─ comments_count = 0
│  └─ visibility = public (default)
│
File handling
├─ For each uploaded image
│  ├─ Validate file type (image only)
│  ├─ Save to media/projects/
│  ├─ Create ProjectImage record
│  └─ Return file URL
│
NLP Analysis (async)
├─ Extract technologies from description
├─ Identify required skills
├─ Generate recommendations
└─ Store in cache
│
Notifications
├─ Create Activity record = "project_posted"
├─ Notify followers of project owner
├─ Update user stats
└─ Add to activity feed
│
Response
├─ Return project details
├─ Redirect to project detail page
└─ Display success message
```

---

## Project Discovery & Collaboration

```
User searches for collaborators
├─ GET /find-collaborators/?skill=python&college=MIT
│
Filter users
├─ Query StudentProfile
│  ├─ Filter by skills (JSON array match)
│  ├─ Filter by college (exact/fuzzy match)
│  ├─ Filter by interests
│  └─ Exclude:
│     ├─ Current user
│     ├─ Blocked users
│     └─ Users with pending/existing connections
│
Enrich results
├─ For each user:
│  ├─ Load profile picture
│  ├─ Load connection status
│  ├─ Load follow status
│  ├─ Calculate skill match percentage
│  └─ Load recent projects
│
Sort results
├─ By skill match (descending)
├─ By profile completion
├─ By activity timestamp
└─ Apply pagination (10/page)
│
Return results
├─ User data
├─ Connection status
├─ Skill match percentage
└─ Recent activity
```

---

## Connection Request Flow

```
User sends connection request
├─ POST /send-connection-request/{user_id}/
│  └─ Check if user exists
│
Create Connection record
├─ Connection
│  ├─ sender = current_user
│  ├─ receiver = target_user
│  ├─ status = "pending"
│  ├─ created_at = now
│  └─ unique_together constraint
│
Send notification
├─ Create Notification
│  ├─ user = receiver
│  ├─ actor = sender
│  ├─ action_type = "connect_request"
│  ├─ content = "{sender} sent you a connection request"
│  ├─ is_read = False
│  └─ created_at = now
│
Send email notification
├─ Choose email backend
├─ Render notification email template
├─ Send to receiver
└─ Log email sent
│
Update user stats
├─ receiver.pending_connections += 1
└─ Increment connection count
│
WebSocket notification (real-time)
├─ Connect to user's WebSocket channel
└─ Send notification in real-time
│
Response
├─ Return connection_id
├─ Return status = "pending"
└─ Redirect to connections page
```

Connection Acceptance
├─ POST /accept-connection/{connection_id}/
│
Update Connection
├─ connection.status = "accepted"
├─ connection.updated_at = now
└─ Save
│
Create reciprocal connection
├─ Create Connection (reverse)
│  ├─ sender = receiver
│  ├─ receiver = sender
│  └─ status = "accepted"
│
Update statistics
├─ sender.connections += 1
├─ receiver.connections += 1
└─ Add to "My Connections"
│
Notifications
├─ Notify sender of acceptance
├─ Update Activity feed
└─ WebSocket real-time update
```

---

## Messaging Flow

```
User sends direct message
├─ POST /messages/
├─ sender = current_user
├─ room_id = chat_room
├─ content = message text
└─ files = [attachments]
│
Create Message record
├─ Message
│  ├─ room_id = chat_room
│  ├─ sender = current_user
│  ├─ content = message
│  ├─ is_read = False
│  ├─ created_at = now
│  └─ has_files = bool
│
Handle file attachments
├─ For each file:
│  ├─ Validate file (type, size)
│  ├─ Save to media/files/
│  ├─ Create MessageFile record
│  └─ Store metadata
│
Update chat room
├─ ChatRoom.last_activity = now
├─ ChatRoom.last_message_content = message
└─ Increment message count
│
Notifications
├─ For each room member:
│  ├─ If not sender:
│  │  ├─ Create Notification
│  │  ├─ Is_read = False
│  │  └─ Send WebSocket event
│  └─ If offline:
│     └─ Queue email notification
│
Update user status
├─ Set typing_indicator = False
├─ Update last_activity = now
└─ Persist to Redis
│
WebSocket broadcast
├─ Connect to room channel
├─ Broadcast message to all members
├─ Include sender info, timestamps
└─ Trigger client UI updates
│
Response
├─ Return message_id
├─ Return created_at timestamp
└─ Return is_read status
```

---

## Comment System Flow

```
User adds comment on project
├─ POST /projects/{project_id}/comments/add/
├─ content = comment text
└─ Sanitize input
│
Create Comment record
├─ Comment
│  ├─ project = project
│  ├─ author = current_user
│  ├─ content = sanitized content
│  ├─ likes_count = 0
│  ├─ is_edited = False
│  ├─ created_at = now
│  └─ edited_at = None
│
Update project
├─ Project.comments_count += 1
├─ Project.updated_at = now
└─ Update in cache
│
Create Activity
├─ Activity
│  ├─ user = comment_author
│  ├─ action_type = "comment_added"
│  ├─ description = "Commented on {project}"
│  └─ timestamp = now
│
Send notifications
├─ Notify project owner
│  ├─ Create Notification
│  ├─ action_type = "comment_added"
│  └─ Send email
├─ Notify previous commenters
│  ├─ Create Notification
│  └─ Send WebSocket event
└─ Increment user stats
   └─ comments_count += 1
│
Update live feed
├─ WebSocket broadcast to project watchers
├─ Include comment data
├─ Update comment count badge
└─ Refresh UI in real-time
│
Response
├─ Return comment_id
├─ Return author info (with profile picture)
├─ Return created_at
└─ Return likes count
```

---

## Like System Flow

```
User likes a project
├─ POST /like-project/{project_id}/
│
Check if already liked
├─ Query Like model
├─ Like.project = project AND Like.user = user
│
If not liked:
├─ Create Like record
│  ├─ user = current_user
│  ├─ project = project
│  ├─ created_at = now
│  └─ Save
│
If already liked:
├─ Delete Like record
└─ Decrement count
│
Update project
├─ Project.likes_count = count(Like)
├─ Project.updated_at = now
└─ Cache updated count
│
Create notification (if new like)
├─ Notification
│  ├─ user = project_owner
│  ├─ actor = current_user
│  ├─ action_type = "like"
│  ├─ content = "{actor} liked your project"
│  └─ is_read = False
│
Send email (optional, configurable)
├─ Queue email to project owner
├─ Include project title
└─ Include link to project
│
Update statistics
├─ User.likes_received += 1
└─ Project.engagement_score += 1
│
WebSocket update
├─ Broadcast like count update
├─ Update like button state
└─ Real-time UI refresh
│
Response
├─ Return likes_count
├─ Return is_liked status
└─ Return new UI state
```

---

## Notification Flow

```
Activity occurs
├─ Project liked
├─ Comment added
├─ Connection request
├─ Message received
├─ User followed
└─ Team invited

Create Notification record
├─ Notification
│  ├─ user = affected_user
│  ├─ actor = action_performer
│  ├─ action_type = event_type
│  ├─ description = human_readable
│  ├─ content_type = related_model
│  ├─ object_id = related_object_id
│  ├─ is_read = False
│  └─ created_at = now

Store notification
├─ Save to database
├─ Cache in Redis for quick access
└─ Index by user_id

Deliver notification
├─ WebSocket (real-time if online)
│  ├─ Connect to user channel
│  ├─ Broadcast notification
│  └─ Update notification badge
├─ Email (if configured)
│  ├─ Choose email backend
│  ├─ Render template
│  ├─ Send email
│  └─ Log sent
└─ Push notification (mobile)
   ├─ Send to mobile device
   └─ Display system notification

User views notifications
├─ GET /notifications/
├─ Fetch all unread notifications
├─ Group by action_type
├─ Sort by created_at (newest first)
└─ Return paginated results

Mark as read
├─ POST /mark-notification-read/{notification_id}/
├─ notification.is_read = True
├─ notification.updated_at = now
├─ Broadcast WebSocket update
└─ Update notification badge count

Response
├─ Notification list
├─ Unread count
├─ Grouped by type
└─ Related data (profile pics, etc.)
```

---

## Authentication State Management

```
Session Lifecycle
├─ User logs in
│  ├─ Create session in database
│  ├─ Store in Redis with TTL
│  ├─ Set session cookie (HTTP-only, secure)
│  ├─ Mark UserStatus = online
│  └─ Create Activity record
│
Active session
├─ Request includes sessionid cookie
├─ Middleware validates session
│  ├─ Check session exists
│  ├─ Check not expired
│  ├─ Check user is active
│  └─ Populate request.user
├─ Update last_activity timestamp
└─ Renew session TTL
│
User logout
├─ POST /logout/
├─ Delete session from database
├─ Clear session cookie
├─ Mark UserStatus = offline
├─ Create Activity record = "logout"
└─ Redirect to login page
│
Session timeout
├─ Session expires in Redis
├─ User auto-logged out
├─ Next request redirects to login
└─ Create Activity record = "session_timeout"
```

---

## Real-time Features (WebSockets)

```
WebSocket Connection
├─ Client connects to /ws/notifications/
├─ Authenticate user via session
├─ Add to user's channel group
├─ Broadcast online status
└─ Store connection in Redis

Typing Indicator
├─ POST /typing/ with is_typing=true
├─ Broadcast to room members
├─ Other users see "User is typing..."
├─ Timeout if no heartbeat (5 seconds)
└─ Display "User stopped typing"

Message broadcast
├─ Message sent → /messages/
├─ Save to database
├─ Broadcast via WebSocket
├─ All room members receive in real-time
├─ Update message count
└─ Play notification sound

Notification delivery
├─ Activity occurs
├─ Create Notification record
├─ Check if user online
├─ If online:
│  ├─ Send via WebSocket
│  ├─ Display in real-time
│  └─ Update badge count
└─ If offline:
   ├─ Store for later delivery
   └─ Send email notification

Presence update
├─ User comes online
├─ Broadcast presence to connections
├─ Show "online" status
├─ Store in Redis with TTL
└─ Update last_activity
```

---

## Caching Strategy

```
Cache layers
├─ Redis (primary)
│  ├─ User sessions
│  ├─ Notification badges
│  ├─ User status (online/offline)
│  ├─ Chat room member lists
│  ├─ Project like counts
│  └─ User profile pictures
│
├─ Database query cache
│  ├─ Frequently accessed profiles
│  ├─ Popular projects
│  ├─ Recent comments
│  └─ Activity feed items
│
└─ Page cache
   ├─ User profiles (15 min)
   ├─ Project listings (10 min)
   ├─ Home feed (5 min)
   └─ Static pages (1 hour)

Invalidation
├─ Profile updated
│  ├─ Clear user cache
│  ├─ Clear profile picture cache
│  └─ Broadcast update via WebSocket
│
├─ Project updated
│  ├─ Clear project cache
│  ├─ Clear listing cache
│  └─ Notify followers
│
└─ Comment added
   ├─ Invalidate project cache
   ├─ Update comment count
   └─ Broadcast to viewers
```

---

## Data Synchronization

```
Cross-device sync
├─ User logs in on device A
├─ Session created with unique ID
├─ User logs in on device B
├─ Both sessions remain active
└─ Actions sync across devices

Message sync
├─ Message sent on device A
├─ Stored in database
├─ Broadcast via WebSocket
├─ Device B receives in real-time
└─ Marked as read when viewed

Notification sync
├─ Notification created
├─ Pushed to database
├─ Delivered via all channels
├─ Device A receives via WebSocket
├─ Device B receives via email
└─ Marked read on device A
   └─ Syncs to device B via WebSocket

Online status
├─ User comes online on device A
├─ Update UserStatus = online
├─ Broadcast to connections
├─ Device B sees user online
└─ Update activity timestamp
```

---

## Error Handling & Recovery

```
Database errors
├─ Connection fails
│  ├─ Fallback to local cache
│  ├─ Queue operations
│  └─ Retry with exponential backoff
├─ Transaction fails
│  ├─ Rollback changes
│  ├─ Log error
│  └─ Return user-friendly message
└─ Timeout
   ├─ Limit query time
   ├─ Cache results
   └─ Return cached data

Email errors
├─ Brevo fails
│  ├─ Fallback to ZeptoMail
│  ├─ Fallback to Gmail
│  └─ Fallback to console
├─ Rate limit
│  ├─ Queue email
│  ├─ Retry after delay
│  └─ Log attempt
└─ Invalid email
   ├─ Validate format
   ├─ Log error
   └─ Skip sending

WebSocket errors
├─ Connection drops
│  ├─ Attempt reconnect
│  ├─ Queue updates locally
│  └─ Sync when reconnected
├─ Message fails
│  ├─ Save to draft
│  ├─ Queue for retry
│  └─ Notify user
└─ Broadcast error
   ├─ Log error
   ├─ Retry to individual connections
   └─ Fallback to polling
```

---

## Performance Optimization

```
Database optimization
├─ Indexed fields
│  ├─ Foreign keys
│  ├─ User searches (skills, interests)
│  ├─ Timestamps (sorting, filtering)
│  └─ Status fields
│
├─ Query optimization
│  ├─ select_related() for ForeignKeys
│  ├─ prefetch_related() for M2M
│  ├─ Pagination (default 10/page)
│  └─ Lazy loading for large datasets
│
└─ Statistics caching
   ├─ Denormalized counters
   ├─ Async aggregation
   └─ Periodic updates

API optimization
├─ Response compression (gzip)
├─ JSON pagination
├─ Selective field loading
├─ Cache-Control headers
└─ Last-Modified headers

Frontend optimization
├─ Static file compression
├─ Image lazy loading
├─ JavaScript bundling
├─ CSS minification
└─ CDN caching (S3)
```

---

## End-to-End Example: User Post to Collaboration

```
1. Alice registers on UniSync
   └─ Creates profile with skills: [Python, Django, React]

2. Alice creates a project
   ├─ Title: "AI Chat Application"
   ├─ Tech stack: [Python, Django, React]
   ├─ Needs: [Frontend Developer, DevOps]
   └─ Project.visibility = public

3. Alice's followers see activity in feed
   ├─ Activity.action_type = "project_posted"
   ├─ Notifications sent to followers
   └─ Broadcast via WebSocket

4. Bob searches for collaborators
   ├─ /find-collaborators/?skill=react
   ├─ Bob's connection status checked
   └─ Alice appears in results

5. Bob views Alice's profile
   ├─ Sees projects, skills, interests
   └─ Sees "Connect" button

6. Bob sends connection request
   ├─ POST /send-connection-request/
   ├─ Notification created & sent to Alice
   ├─ Email sent: "{Bob} wants to connect"
   └─ Alice sees notification in real-time

7. Alice accepts connection
   ├─ Connection.status = "accepted"
   ├─ Notification sent to Bob
   ├─ Both see each other's profiles
   └─ Can now message directly

8. Alice finds Bob's project
   ├─ Bob had posted "Web Scraper Project"
   ├─ Alice comments: "I'd love to contribute!"
   ├─ Comment saved & notification sent to Bob
   └─ Real-time update in live feed

9. Bob invites Alice to project team
   ├─ POST /invite-to-team/
   ├─ TeamInvitation created
   ├─ Email sent to Alice
   └─ Notification in app

10. Alice accepts team invitation
    ├─ TeamInvitation.status = "accepted"
    ├─ Alice added to Project.team
    ├─ Notification sent to Bob
    └─ Both can now collaborate

11. Alice and Bob message about project
    ├─ Create ChatRoom
    ├─ Send messages
    ├─ Real-time WebSocket delivery
    ├─ File attachments
    └─ Read status tracking

12. Project completed
    ├─ Project.status = "completed"
    ├─ Activity posted
    ├─ Notifications to team & followers
    └─ Stored in portfolio
```

---

## Summary

UniSync's data flow is designed for:
- ✅ Real-time user interactions
- ✅ Scalable message delivery
- ✅ Efficient notification system
- ✅ Cached performance optimization
- ✅ Graceful error handling
- ✅ Cross-device synchronization
- ✅ WebSocket real-time updates
- ✅ Email fallback for offline users

The architecture supports millions of simultaneous connections while maintaining data consistency and reliability.
