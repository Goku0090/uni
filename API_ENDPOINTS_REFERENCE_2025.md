# UniSync API Endpoints Reference

**Complete API endpoint listing with methods, parameters, and descriptions**

---

## Authentication Endpoints

### Register
```
POST /register/
POST /accounts/register/

Parameters:
- email (string, required)
- username (string, required)
- password1 (string, required)
- password2 (string, required)
- full_name (string, optional)

Response:
{
  "success": true,
  "message": "Registration successful. OTP sent to email.",
  "otp_id": <otp_id>
}
```

### Login
```
POST /login/
POST /accounts/login/

Parameters:
- username (string, required)
- password (string, required)

Response:
{
  "success": true,
  "message": "Login successful",
  "user": { id, username, email }
}
```

### Verify OTP
```
POST /verify-otp/<purpose>/
POST /accounts/verify-otp/<purpose>/

Purpose: 'login', 'registration', 'reset'

Parameters:
- otp_code (string, required, 6 digits)
- email (string, optional)

Response:
{
  "success": true,
  "message": "OTP verified successfully",
  "user": { id, username, email }
}
```

### Resend OTP
```
POST /resend-otp/<purpose>/
POST /accounts/resend-otp/<purpose>/

Parameters:
- email (string, required)

Response:
{
  "success": true,
  "message": "OTP resent to your email"
}
```

### Forgot Password
```
POST /forgot-password/
POST /accounts/forgot-password/

Parameters:
- email (string, required)

Response:
{
  "success": true,
  "message": "OTP sent to email for password reset"
}
```

### Reset Password
```
POST /reset-password/
POST /accounts/reset-password/

Parameters:
- email (string, required)
- otp_code (string, required)
- new_password (string, required)

Response:
{
  "success": true,
  "message": "Password reset successfully"
}
```

### Logout
```
POST /logout/
POST /accounts/logout/

Response:
{
  "success": true,
  "message": "Logged out successfully"
}
```

---

## User Profile Endpoints

### Get User Profile
```
GET /api/user-profile/<user_id>/
GET /accounts/user-profile/<user_id>/

Response:
{
  "id": <user_id>,
  "username": "john_doe",
  "email": "john@example.com",
  "student_profile": {
    "full_name": "John Doe",
    "college": "MIT",
    "bio": "...",
    "profile_photo": "url",
    "skills": ["Python", "Django"],
    "interests": ["AI", "Web Dev"],
    "github": "https://github.com/johndoe",
    "linkedin": "https://linkedin.com/in/johndoe",
    "portfolio": "https://johndoe.com"
  }
}
```

### Update Student Profile
```
POST /accounts/student-details/
POST /accounts/student-profile/

Parameters:
- full_name (string)
- college (string)
- bio (string)
- profile_photo (file, jpg/jpeg/png/gif)
- skills (JSON array)
- interests (JSON array)
- github (URL)
- linkedin (URL)
- portfolio (URL)
- behance (URL)
- role_preference (string)

Response:
{
  "success": true,
  "message": "Profile updated successfully",
  "profile": { ...updated profile }
}
```

### View User Profile
```
GET /accounts/student-profile/
GET /user/<username>/
GET /accounts/user/<username>/

Response:
{
  "user": { id, username, email, first_name, last_name },
  "profile": { ...student profile },
  "connections": {
    "sent": <count>,
    "received": <count>,
    "accepted": <count>
  }
}
```

### User Stats
```
GET /api/user-stats/

Response:
{
  "projects_created": <count>,
  "connections_made": <count>,
  "likes_received": <count>,
  "comments_made": <count>,
  "followers_count": <count>,
  "following_count": <count>
}
```

---

## Project Endpoints

### List Projects (Feed)
```
GET /accounts/dashboard/
GET /accounts/project-feed/

Query Parameters:
- page (integer, default 1)
- visibility (string: 'public', 'private', 'friends_only')
- category (string)
- search (string)

Response:
{
  "count": <total_projects>,
  "next": "url_to_next_page",
  "previous": "url_to_previous_page",
  "results": [
    {
      "id": <project_id>,
      "title": "Project Name",
      "description": "...",
      "user": { id, username },
      "visibility": "public",
      "category": "...",
      "status": "ongoing",
      "likes_count": 10,
      "comments_count": 5,
      "members_count": 3,
      "created_at": "2025-02-03T10:00:00Z"
    }
  ]
}
```

### Create Project
```
POST /accounts/post-project/

Parameters:
- title (string, required, max 200)
- description (string, required)
- category (string, required)
- visibility (string: 'public', 'private', 'friends_only')
- skills_needed (JSON array)
- roles_needed (JSON array)
- timeline (string)
- github_link (URL, optional)

Response:
{
  "success": true,
  "message": "Project created successfully",
  "project": { ...project details }
}
```

### Get Project Details
```
GET /accounts/project-detail/<project_id>/
GET /project/<project_id>/

Response:
{
  "id": <project_id>,
  "title": "Project Name",
  "description": "...",
  "user": { id, username, profile },
  "visibility": "public",
  "category": "...",
  "status": "ongoing",
  "skills_needed": [...],
  "roles_needed": [...],
  "github_link": "...",
  "likes_count": 10,
  "comments_count": 5,
  "members": [
    { "user_id": 1, "username": "john", "role": "owner" },
    { "user_id": 2, "username": "jane", "role": "contributor" }
  ],
  "tasks": [
    { "id": 1, "title": "Task 1", "status": "in_progress", "assigned_to": "john" }
  ],
  "milestones": [
    { "id": 1, "title": "Phase 1", "due_date": "2025-03-01", "is_completed": false }
  ],
  "created_at": "2025-01-01T00:00:00Z",
  "updated_at": "2025-02-03T10:00:00Z"
}
```

### Update Project
```
POST /accounts/edit-project/<project_id>/
PUT /accounts/edit-project/<project_id>/

Parameters: (same as Create Project)

Response:
{
  "success": true,
  "message": "Project updated successfully",
  "project": { ...updated project }
}
```

### Delete Project
```
DELETE /accounts/delete-project/<project_id>/

Response:
{
  "success": true,
  "message": "Project deleted successfully"
}
```

### Like Project
```
POST /accounts/like-project/<project_id>/

Response:
{
  "success": true,
  "message": "Project liked",
  "likes_count": 11
}
```

### My Projects
```
GET /accounts/my-projects/

Response:
{
  "projects": [
    { ...project details },
    ...
  ]
}
```

### Explore Projects
```
GET /accounts/explore-projects/

Query Parameters:
- category (string)
- visibility (string)
- skills (array)
- page (integer)

Response:
{
  "results": [ ...projects ],
  "count": <total>,
  "next": "url"
}
```

---

## Comment Endpoints

### Get Comments
```
GET /api/projects/<project_id>/comments/

Query Parameters:
- page (integer, default 1)
- ordering (string: '-created_at', 'created_at')

Response:
{
  "count": <total_comments>,
  "results": [
    {
      "id": <comment_id>,
      "user": { id, username, profile_photo },
      "content": "Comment text",
      "created_at": "2025-02-03T10:00:00Z",
      "updated_at": "2025-02-03T10:00:00Z",
      "replies": [
        { "id": 2, "user": {...}, "content": "Reply text" }
      ]
    }
  ]
}
```

### Add Comment
```
POST /api/projects/<project_id>/comments/add/

Parameters:
- content (string, required)
- reply_to (integer, optional, comment_id to reply to)

Response:
{
  "success": true,
  "message": "Comment added successfully",
  "comment": { ...comment details }
}
```

### Edit Comment
```
POST /api/comments/<comment_id>/edit/
PUT /api/comments/<comment_id>/edit/

Parameters:
- content (string, required)

Response:
{
  "success": true,
  "message": "Comment updated successfully",
  "comment": { ...updated comment }
}
```

### Delete Comment
```
DELETE /api/comments/<comment_id>/delete/

Response:
{
  "success": true,
  "message": "Comment deleted successfully"
}
```

---

## Messaging Endpoints

### Create Chat Room
```
POST /api/chat-rooms/

Parameters:
- name (string, required)
- description (string, optional)
- members (array of user_ids)
- chat_type (string: 'direct', 'group')

Response:
{
  "id": <room_id>,
  "name": "Room Name",
  "description": "...",
  "chat_type": "group",
  "members": [
    { "user_id": 1, "username": "john" }
  ],
  "created_at": "2025-02-03T10:00:00Z"
}
```

### List Chat Rooms
```
GET /api/chat-rooms/

Query Parameters:
- page (integer)
- search (string)

Response:
{
  "count": <total>,
  "results": [ ...chat rooms ]
}
```

### Get Chat Room Details
```
GET /api/chat-rooms/<room_id>/

Response:
{
  "id": <room_id>,
  "name": "Room Name",
  "members": [...],
  "last_message": { ...message },
  "unread_count": 3,
  "created_at": "2025-02-03T10:00:00Z"
}
```

### Get Chat Room Members
```
GET /api/chat-rooms/<room_id>/members/

Response:
{
  "members": [
    { "user_id": 1, "username": "john", "is_active": true, "joined_at": "..." }
  ]
}
```

### Send Direct Message
```
POST /api/direct-message/

Parameters:
- receiver_id (integer, required)
- content (string, required)
- message_type (string: 'text', 'file', 'image', 'call')
- call_type (string: 'voice', 'video', optional for call type)

Response:
{
  "id": <message_id>,
  "sender": { id, username },
  "receiver": { id, username },
  "content": "...",
  "message_type": "text",
  "created_at": "2025-02-03T10:00:00Z"
}
```

### Send Message (to Room)
```
POST /api/messages/

Parameters:
- room_id (integer, required)
- content (string, required)
- message_type (string: 'text', 'file', 'image', 'call')
- reply_to (integer, optional, message_id to reply to)

Response:
{
  "id": <message_id>,
  "sender": { id, username },
  "room": { id, name },
  "content": "...",
  "created_at": "2025-02-03T10:00:00Z"
}
```

### List Messages
```
GET /api/messages/

Query Parameters:
- room_id (integer, required)
- page (integer)
- ordering (string: '-created_at')

Response:
{
  "count": <total>,
  "results": [ ...messages ]
}
```

### Get Message Details
```
GET /api/messages/<message_id>/

Response:
{
  "id": <message_id>,
  "sender": { ...user },
  "content": "...",
  "read_by": [ ...users ],
  "reactions": [
    { "user": "john", "reaction": "👍" }
  ],
  "created_at": "2025-02-03T10:00:00Z"
}
```

### Mark Message as Read
```
POST /api/messages/<message_id>/status/

Parameters:
- status (string: 'read', 'unread')

Response:
{
  "success": true,
  "message": "Message marked as read"
}
```

### Add Message Reaction
```
POST /api/messages/<message_id>/reactions/

Parameters:
- reaction (string, required, emoji or text)

Response:
{
  "success": true,
  "message": "Reaction added",
  "reactions": [...]
}
```

### Search Messages
```
GET /api/messages/search/

Query Parameters:
- q (string, search query)
- room_id (integer, optional)
- user_id (integer, optional)

Response:
{
  "results": [ ...matching messages ]
}
```

### Draft Messages
```
GET /api/drafts/

Response:
{
  "drafts": [
    { "id": 1, "receiver_id": 2, "content": "Draft message" }
  ]
}
```

### Typing Indicator
```
POST /api/typing/

Parameters:
- room_id (integer, required)
- is_typing (boolean)

Response:
{
  "success": true
}
```

### List Conversations
```
GET /api/conversations/

Response:
{
  "conversations": [
    {
      "room_id": 1,
      "last_message": "...",
      "last_message_at": "2025-02-03T10:00:00Z",
      "unread_count": 3
    }
  ]
}
```

---

## Connection & Social Endpoints

### Send Connection Request
```
POST /accounts/send-connection/<user_id>/
POST /accounts/send-connection-request/<user_id>/
POST /connect/<user_id>/

Response:
{
  "success": true,
  "message": "Connection request sent",
  "connection": { "id": <conn_id>, "status": "pending" }
}
```

### Accept Connection
```
POST /accounts/accept-connection/<connection_id>/

Response:
{
  "success": true,
  "message": "Connection accepted",
  "connection": { "id": <conn_id>, "status": "accepted" }
}
```

### Reject Connection
```
POST /accounts/reject-connection/<connection_id>/

Response:
{
  "success": true,
  "message": "Connection rejected"
}
```

### Cancel Connection
```
POST /accounts/cancel-connection/<connection_id>/

Response:
{
  "success": true,
  "message": "Connection request cancelled"
}
```

### My Connections
```
GET /accounts/my-connections/

Query Parameters:
- status (string: 'pending', 'accepted', 'rejected')

Response:
{
  "sent": [ ...connections ],
  "received": [ ...connections ],
  "accepted": [ ...connections ]
}
```

### Follow User
```
POST /accounts/follow/<user_id>/

Response:
{
  "success": true,
  "message": "User followed",
  "following": true
}
```

### Unfollow User
```
POST /accounts/unfollow/<user_id>/

Response:
{
  "success": true,
  "message": "User unfollowed",
  "following": false
}
```

---

## Team Management Endpoints

### Invite to Team
```
POST /accounts/invite-to-team/<project_id>/

Parameters:
- user_id (integer, required)
- role (string: 'contributor', 'admin', 'viewer')
- message (string, optional)

Response:
{
  "success": true,
  "message": "Invitation sent",
  "invitation": { "id": <inv_id>, "status": "pending" }
}
```

### Respond to Invitation
```
POST /accounts/respond-team-invitation/<invitation_id>/

Parameters:
- action (string: 'accept', 'decline')

Response:
{
  "success": true,
  "message": "Invitation accepted/declined"
}
```

### Remove Team Member
```
DELETE /accounts/remove-team-member/<project_id>/<user_id>/

Response:
{
  "success": true,
  "message": "Member removed from project"
}
```

---

## Notification Endpoints

### Get Notifications
```
GET /accounts/notifications/

Query Parameters:
- page (integer)
- unread_only (boolean, default false)

Response:
{
  "count": <total>,
  "results": [
    {
      "id": <notif_id>,
      "type": "connection_request",
      "title": "John sent you a connection request",
      "is_read": false,
      "created_at": "2025-02-03T10:00:00Z"
    }
  ]
}
```

### Mark Notification as Read
```
POST /accounts/mark-notification-read/<notification_id>/

Response:
{
  "success": true,
  "message": "Notification marked as read"
}
```

---

## Activity Feed Endpoints

### Get Activity Feed
```
GET /accounts/activity-feed/

Query Parameters:
- page (integer)
- user_id (integer, optional, for specific user)

Response:
{
  "count": <total>,
  "results": [
    {
      "id": <activity_id>,
      "user": { id, username },
      "activity_type": "project_created",
      "title": "John created a new project",
      "description": "...",
      "project": { id, title },
      "created_at": "2025-02-03T10:00:00Z"
    }
  ]
}
```

---

## Search & Discovery Endpoints

### Find Collaborators
```
GET /accounts/find-collaborators/

Query Parameters:
- college (string)
- skills (array)
- interests (array)
- role_preference (string)
- page (integer)

Response:
{
  "count": <total>,
  "results": [
    {
      "user_id": 1,
      "username": "john",
      "full_name": "John Doe",
      "college": "MIT",
      "skills": ["Python", "Django"],
      "interests": ["AI"],
      "connection_status": "not_connected"
    }
  ]
}
```

### Search Projects
```
GET /accounts/search-projects/

Query Parameters:
- q (string, search query)
- category (string)
- page (integer)

Response:
{
  "results": [ ...projects ]
}
```

### College Search
```
GET /accounts/college-search/

Query Parameters:
- q (string, college name)

Response:
{
  "colleges": [
    { "id": 1, "name": "MIT", "country": "USA" }
  ]
}
```

### Validate College
```
POST /accounts/validate-college/

Parameters:
- college_name (string)

Response:
{
  "valid": true,
  "college": { "id": 1, "name": "MIT" }
}
```

---

## Utility Endpoints

### Check Username Availability
```
GET /accounts/check-username/

Query Parameters:
- username (string)

Response:
{
  "available": true/false,
  "username": "john_doe"
}
```

### Check Email Availability
```
GET /accounts/check-email/

Query Parameters:
- email (string)

Response:
{
  "available": true/false,
  "email": "john@example.com"
}
```

### NLP Analyze
```
POST /accounts/nlp-analyze/

Parameters:
- text (string)

Response:
{
  "sentiment": "positive",
  "keywords": [...],
  "score": 0.85
}
```

### Download File
```
GET /accounts/download-file/<file_id>/

Response: File download
```

---

## API Response Format

### Success Response
```json
{
  "success": true,
  "message": "Operation completed successfully",
  "data": {}
}
```

### Error Response
```json
{
  "success": false,
  "error": "Error message",
  "status_code": 400
}
```

### Paginated Response
```json
{
  "count": 100,
  "next": "http://api.example.com/resource/?page=2",
  "previous": null,
  "results": [...]
}
```

---

## Status Codes

| Code | Meaning |
|------|---------|
| 200  | OK - Success |
| 201  | Created - Resource created |
| 204  | No Content - Successful deletion |
| 400  | Bad Request - Invalid parameters |
| 401  | Unauthorized - Not authenticated |
| 403  | Forbidden - No permission |
| 404  | Not Found - Resource doesn't exist |
| 409  | Conflict - Resource already exists |
| 500  | Server Error |

---

## Authentication

All endpoints except login/register require:
- **Session Authentication**: Django session cookie
- **Header**: `Cookie: sessionid=<sessionid>`

---

*Last updated: February 3, 2025*
