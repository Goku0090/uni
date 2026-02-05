# UniSync API Endpoints - Complete Reference

## Authentication Endpoints

### 1. User Registration
**Endpoint**: `POST /accounts/register/` or `POST /api/auth/register/`
**Method**: POST
**Authentication**: None required
**Request Body**:
```json
{
  "email": "user@example.com",
  "password": "securepassword123",
  "password_confirm": "securepassword123",
  "first_name": "John",
  "last_name": "Doe"
}
```
**Response**: 
```json
{
  "message": "User registered successfully",
  "user_id": 123,
  "username": "johndoe"
}
```
**Status Codes**: 200 (Success), 400 (Validation error)

---

### 2. Login with Email & Password
**Endpoint**: `POST /accounts/login/` or `POST /api/auth/login/`
**Method**: POST
**Authentication**: None required
**Request Body**:
```json
{
  "email": "user@example.com",
  "password": "securepassword123"
}
```
**Response**:
```json
{
  "token": "abc123xyz...",
  "user_id": 123,
  "message": "Login successful"
}
```
**Status Codes**: 200 (Success), 401 (Invalid credentials)

---

### 3. Request OTP
**Endpoint**: `POST /api/auth/otp/send/`
**Method**: POST
**Authentication**: None required
**Request Body**:
```json
{
  "email": "user@example.com",
  "purpose": "login"  // or "registration" or "reset"
}
```
**Response**:
```json
{
  "message": "OTP sent to email",
  "email": "user@example.com",
  "expiry_minutes": 5
}
```
**Status Codes**: 200 (Success), 400 (Email not found)

---

### 4. Verify OTP & Login
**Endpoint**: `POST /accounts/verify-otp/` or `POST /api/auth/otp/verify/`
**Method**: POST
**Authentication**: None required
**Request Body**:
```json
{
  "email": "user@example.com",
  "otp_code": "123456",
  "purpose": "login"
}
```
**Response**:
```json
{
  "token": "abc123xyz...",
  "user_id": 123,
  "message": "OTP verified successfully"
}
```
**Status Codes**: 200 (Success), 400 (Invalid/expired OTP)

---

### 5. Google OAuth Login
**Endpoint**: `POST /accounts/google/login/` or `POST /api/auth/google/`
**Method**: POST
**Authentication**: None required
**Request Body**:
```json
{
  "access_token": "google_token_xyz..."
}
```
**Response**:
```json
{
  "token": "abc123xyz...",
  "user_id": 123,
  "is_new": false
}
```

---

### 6. GitHub OAuth Login
**Endpoint**: `POST /accounts/github/login/` or `POST /api/auth/github/`
**Method**: POST
**Authentication**: None required
**Request Body**:
```json
{
  "code": "github_auth_code",
  "state": "random_state_value"
}
```
**Response**:
```json
{
  "token": "abc123xyz...",
  "user_id": 123,
  "is_new": true
}
```

---

### 7. Password Reset Request
**Endpoint**: `POST /accounts/password-reset/`
**Method**: POST
**Authentication**: None required
**Request Body**:
```json
{
  "email": "user@example.com"
}
```
**Response**:
```json
{
  "message": "Password reset link sent to email"
}
```

---

### 8. Reset Password with Token
**Endpoint**: `POST /accounts/password-reset-confirm/{uid}/{token}/`
**Method**: POST
**Authentication**: None required
**Request Body**:
```json
{
  "new_password": "newpassword123",
  "new_password_confirm": "newpassword123"
}
```
**Response**:
```json
{
  "message": "Password reset successfully"
}
```

---

### 9. Logout
**Endpoint**: `POST /accounts/logout/` or `POST /api/auth/logout/`
**Method**: POST
**Authentication**: Token required
**Response**:
```json
{
  "message": "Logout successful"
}
```

---

## User Profile Endpoints

### 1. Get Current User Profile
**Endpoint**: `GET /api/users/me/`
**Method**: GET
**Authentication**: Token required
**Response**:
```json
{
  "id": 123,
  "username": "johndoe",
  "email": "user@example.com",
  "profile": {
    "full_name": "John Doe",
    "college": "MIT",
    "location": "Boston, MA",
    "bio": "Developer and designer",
    "profile_photo": "https://...",
    "skills": ["Python", "JavaScript", "React"],
    "project_interests": ["Web Development", "AI/ML"],
    "role_preference": "Full Stack Developer",
    "github": "https://github.com/johndoe",
    "linkedin": "https://linkedin.com/in/johndoe",
    "portfolio": "https://johndoe.com",
    "behance": "https://behance.net/johndoe"
  }
}
```

---

### 2. Get User Profile (by ID)
**Endpoint**: `GET /api/users/{user_id}/`
**Method**: GET
**Authentication**: Not required
**Response**:
```json
{
  "id": 123,
  "username": "johndoe",
  "profile": {
    "full_name": "John Doe",
    "college": "MIT",
    "bio": "Developer and designer",
    "profile_photo": "https://..."
  }
}
```

---

### 3. Update User Profile
**Endpoint**: `PUT /api/users/me/` or `GET /accounts/edit-profile/`
**Method**: PUT/POST
**Authentication**: Token required
**Request Body** (multipart/form-data):
```json
{
  "full_name": "John Doe",
  "college": "MIT",
  "location": "Boston, MA",
  "bio": "Updated bio",
  "profile_photo": "file.jpg",
  "skills": ["Python", "JavaScript"],
  "project_interests": ["Web Dev"],
  "role_preference": "Backend Developer",
  "github": "https://github.com/johndoe",
  "linkedin": "https://linkedin.com/in/johndoe"
}
```
**Response**: Updated user profile object

---

### 4. Get User's Projects
**Endpoint**: `GET /api/users/{user_id}/projects/`
**Method**: GET
**Authentication**: Not required
**Query Parameters**:
- `page`: Page number (default: 1)
- `page_size`: Items per page (default: 10)
**Response**:
```json
{
  "count": 5,
  "next": "https://.../api/users/123/projects/?page=2",
  "results": [
    {
      "id": 1,
      "title": "E-Commerce Platform",
      "description": "...",
      "owner": 123,
      "team_members": []
    }
  ]
}
```

---

### 5. Get User Statistics
**Endpoint**: `GET /api/users/{user_id}/stats/`
**Method**: GET
**Authentication**: Not required
**Response**:
```json
{
  "total_projects": 5,
  "total_connections": 12,
  "followers": 8,
  "following": 10,
  "total_messages": 45
}
```

---

## Project Endpoints

### 1. List All Projects
**Endpoint**: `GET /api/projects/` or `/accounts/projects/`
**Method**: GET
**Authentication**: Not required
**Query Parameters**:
- `search`: Search by title or description
- `visibility`: public, private, draft
- `page`: Page number
- `page_size`: Items per page
- `ordering`: -created_at, title, etc.

**Response**:
```json
{
  "count": 42,
  "next": "https://.../api/projects/?page=2",
  "results": [
    {
      "id": 1,
      "title": "AI Chatbot",
      "description": "A conversational AI platform",
      "owner": 123,
      "owner_name": "John Doe",
      "team_members": [124, 125],
      "visibility": "public",
      "tags": ["AI", "Python"],
      "created_at": "2024-01-15T10:30:00Z",
      "updated_at": "2024-01-20T14:00:00Z",
      "status": "in_progress"
    }
  ]
}
```

---

### 2. Get Single Project
**Endpoint**: `GET /api/projects/{project_id}/`
**Method**: GET
**Authentication**: Not required (unless private)
**Response**:
```json
{
  "id": 1,
  "title": "AI Chatbot",
  "description": "A conversational AI platform",
  "owner": 123,
  "owner_name": "John Doe",
  "owner_profile": {
    "full_name": "John Doe",
    "profile_photo": "https://..."
  },
  "team_members": [124, 125],
  "team_details": [
    {"id": 124, "username": "alice", "full_name": "Alice Smith"},
    {"id": 125, "username": "bob", "full_name": "Bob Jones"}
  ],
  "visibility": "public",
  "status": "in_progress",
  "tags": ["AI", "Python", "NLP"],
  "collaboration_needs": ["Frontend Developer", "UI Designer"],
  "created_at": "2024-01-15T10:30:00Z",
  "updated_at": "2024-01-20T14:00:00Z",
  "likes_count": 5,
  "comments_count": 12,
  "is_liked": false
}
```

---

### 3. Create Project
**Endpoint**: `POST /api/projects/`
**Method**: POST
**Authentication**: Token required
**Request Body**:
```json
{
  "title": "AI Chatbot",
  "description": "A conversational AI platform",
  "visibility": "public",
  "tags": ["AI", "Python"],
  "collaboration_needs": ["Frontend Developer"],
  "github_link": "https://github.com/johndoe/project",
  "demo_link": "https://project.demo.com"
}
```
**Response**: Created project object

---

### 4. Update Project
**Endpoint**: `PUT /api/projects/{project_id}/`
**Method**: PUT
**Authentication**: Token required (owner only)
**Request Body**: Same as create
**Response**: Updated project object

---

### 5. Delete Project
**Endpoint**: `DELETE /api/projects/{project_id}/`
**Method**: DELETE
**Authentication**: Token required (owner only)
**Response**:
```json
{
  "message": "Project deleted successfully"
}
```

---

### 6. Search Projects
**Endpoint**: `GET /accounts/search-projects/`
**Method**: GET
**Authentication**: Not required
**Query Parameters**:
- `q`: Search query
**Response**: List of matching projects

---

## Comment Endpoints

### 1. Get Project Comments
**Endpoint**: `GET /api/comments/?project={project_id}` or `GET /api/projects/{project_id}/comments/`
**Method**: GET
**Authentication**: Not required
**Query Parameters**:
- `page`: Page number
- `page_size`: Items per page
- `ordering`: -created_at, created_at

**Response**:
```json
{
  "count": 8,
  "results": [
    {
      "id": 1,
      "project": 1,
      "author": 123,
      "author_name": "Alice Smith",
      "author_profile_photo": "https://...",
      "content": "Great project! Would love to contribute.",
      "created_at": "2024-01-18T10:30:00Z",
      "updated_at": "2024-01-18T10:30:00Z",
      "is_edited": false
    }
  ]
}
```

---

### 2. Add Comment
**Endpoint**: `POST /api/comments/` or `POST /api/projects/{project_id}/comments/`
**Method**: POST
**Authentication**: Token required
**Request Body**:
```json
{
  "project": 1,
  "content": "Great project! Would love to contribute."
}
```
**Response**: Created comment object

---

### 3. Edit Comment
**Endpoint**: `PUT /api/comments/{comment_id}/`
**Method**: PUT
**Authentication**: Token required (author only)
**Request Body**:
```json
{
  "content": "Updated comment text"
}
```
**Response**: Updated comment object

---

### 4. Delete Comment
**Endpoint**: `DELETE /api/comments/{comment_id}/`
**Method**: DELETE
**Authentication**: Token required (author only)
**Response**:
```json
{
  "message": "Comment deleted successfully"
}
```

---

## Message & Chat Endpoints

### 1. Send Direct Message
**Endpoint**: `POST /api/messages/` or `POST /api/direct-messages/`
**Method**: POST
**Authentication**: Token required
**Request Body**:
```json
{
  "receiver": 125,
  "content": "Hey, how are you?",
  "attachments": []
}
```
**Response**:
```json
{
  "id": 501,
  "sender": 123,
  "receiver": 125,
  "content": "Hey, how are you?",
  "created_at": "2024-01-20T15:30:00Z",
  "is_read": false
}
```

---

### 2. Get Messages (Conversation)
**Endpoint**: `GET /api/messages/?user={user_id}` or `GET /api/conversations/{user_id}/`
**Method**: GET
**Authentication**: Token required
**Query Parameters**:
- `page`: Page number
- `page_size`: Items per page

**Response**:
```json
{
  "count": 25,
  "results": [
    {
      "id": 501,
      "sender": 123,
      "receiver": 125,
      "content": "Hey, how are you?",
      "created_at": "2024-01-20T15:30:00Z",
      "is_read": true
    }
  ]
}
```

---

### 3. Create Chat Room
**Endpoint**: `POST /api/chat-rooms/`
**Method**: POST
**Authentication**: Token required
**Request Body**:
```json
{
  "name": "Project Alpha Team",
  "description": "Discussion room for Project Alpha",
  "members": [123, 124, 125]
}
```
**Response**:
```json
{
  "id": 1,
  "name": "Project Alpha Team",
  "description": "Discussion room for Project Alpha",
  "owner": 123,
  "members": [123, 124, 125],
  "created_at": "2024-01-20T10:00:00Z"
}
```

---

### 4. Get Chat Rooms
**Endpoint**: `GET /api/chat-rooms/`
**Method**: GET
**Authentication**: Token required
**Response**:
```json
{
  "count": 3,
  "results": [
    {
      "id": 1,
      "name": "Project Alpha Team",
      "members_count": 3,
      "unread_messages": 2
    }
  ]
}
```

---

### 5. Send Chat Room Message
**Endpoint**: `POST /api/messages/` (with chat_room field)
**Method**: POST
**Authentication**: Token required
**Request Body**:
```json
{
  "chat_room": 1,
  "content": "Let's discuss the roadmap"
}
```
**Response**: Created message object

---

### 6. Mark Message as Read
**Endpoint**: `POST /api/messages/{message_id}/mark-read/` or `POST /api/messages/{message_id}/status/`
**Method**: POST
**Authentication**: Token required
**Response**:
```json
{
  "message": "Message marked as read"
}
```

---

### 7. Get Unread Messages Count
**Endpoint**: `GET /api/messages/unread/count/`
**Method**: GET
**Authentication**: Token required
**Response**:
```json
{
  "unread_count": 5,
  "unread_conversations": [
    {
      "user_id": 124,
      "username": "alice",
      "unread_count": 3
    }
  ]
}
```

---

## Connection Endpoints

### 1. Send Connection Request
**Endpoint**: `POST /api/connections/send/` or `POST /api/users/{user_id}/connect/`
**Method**: POST
**Authentication**: Token required
**Request Body**:
```json
{
  "receiver": 125,
  "message": "I'd like to collaborate with you"
}
```
**Response**:
```json
{
  "id": 1,
  "sender": 123,
  "receiver": 125,
  "status": "pending",
  "created_at": "2024-01-20T10:00:00Z"
}
```

---

### 2. Accept Connection Request
**Endpoint**: `POST /api/connections/{connection_id}/accept/`
**Method**: POST
**Authentication**: Token required
**Response**:
```json
{
  "message": "Connection accepted",
  "connection": {
    "id": 1,
    "sender": 124,
    "receiver": 123,
    "status": "accepted"
  }
}
```

---

### 3. Reject Connection Request
**Endpoint**: `POST /api/connections/{connection_id}/reject/`
**Method**: POST
**Authentication**: Token required
**Response**:
```json
{
  "message": "Connection rejected"
}
```

---

### 4. Get User Connections
**Endpoint**: `GET /api/users/{user_id}/connections/` or `GET /api/connections/`
**Method**: GET
**Authentication**: Token required (for own)
**Query Parameters**:
- `status`: pending, accepted, rejected

**Response**:
```json
{
  "count": 8,
  "accepted": [
    {"id": 124, "username": "alice", "full_name": "Alice Smith"},
    {"id": 125, "username": "bob", "full_name": "Bob Jones"}
  ],
  "pending": [
    {"id": 126, "username": "carol", "full_name": "Carol Davis"}
  ]
}
```

---

## Notification Endpoints

### 1. Get Notifications
**Endpoint**: `GET /api/notifications/`
**Method**: GET
**Authentication**: Token required
**Query Parameters**:
- `is_read`: true, false, all

**Response**:
```json
{
  "count": 5,
  "unread_count": 2,
  "results": [
    {
      "id": 1,
      "type": "connection_request",
      "message": "Alice Smith sent you a connection request",
      "user_id": 124,
      "data": {
        "connection_id": 5
      },
      "is_read": false,
      "created_at": "2024-01-20T15:30:00Z"
    },
    {
      "id": 2,
      "type": "project_comment",
      "message": "Bob Jones commented on your project",
      "user_id": 125,
      "data": {
        "project_id": 1,
        "comment_id": 42
      },
      "is_read": true,
      "created_at": "2024-01-20T14:00:00Z"
    }
  ]
}
```

---

### 2. Mark Notification as Read
**Endpoint**: `POST /api/notifications/{notification_id}/read/`
**Method**: POST
**Authentication**: Token required
**Response**:
```json
{
  "message": "Notification marked as read"
}
```

---

### 3. Delete Notification
**Endpoint**: `DELETE /api/notifications/{notification_id}/`
**Method**: DELETE
**Authentication**: Token required
**Response**:
```json
{
  "message": "Notification deleted"
}
```

---

## Activity Feed Endpoints

### 1. Get Activity Feed
**Endpoint**: `GET /api/activities/` or `GET /accounts/activity-feed/`
**Method**: GET
**Authentication**: Not required (public activities)
**Query Parameters**:
- `user`: Filter by user ID
- `type`: project_created, comment_added, connection_accepted, etc.
- `ordering`: -timestamp

**Response**:
```json
{
  "count": 25,
  "results": [
    {
      "id": 1,
      "user": 123,
      "user_name": "John Doe",
      "type": "project_created",
      "message": "John Doe created a new project",
      "data": {
        "project_id": 1,
        "project_title": "AI Chatbot"
      },
      "timestamp": "2024-01-20T10:30:00Z"
    }
  ]
}
```

---

## Search & Discovery Endpoints

### 1. Search All Content
**Endpoint**: `GET /api/search/` or `GET /accounts/search/`
**Method**: GET
**Authentication**: Not required
**Query Parameters**:
- `q`: Search query
- `type`: projects, users, all

**Response**:
```json
{
  "projects": [
    {
      "id": 1,
      "title": "AI Chatbot",
      "owner": "John Doe"
    }
  ],
  "users": [
    {
      "id": 123,
      "username": "johndoe",
      "full_name": "John Doe"
    }
  ]
}
```

---

### 2. Discover Projects by Skills
**Endpoint**: `GET /api/projects/discover/`
**Method**: GET
**Authentication**: Token required (optional)
**Query Parameters**:
- `skills`: comma-separated list (Python, JavaScript, etc.)
- `college`: filter by college

**Response**:
```json
{
  "count": 12,
  "results": [
    {
      "id": 1,
      "title": "AI Chatbot",
      "skills": ["Python", "NLP"],
      "collaboration_needs": ["Frontend Developer"]
    }
  ]
}
```

---

## Like/Follow Endpoints

### 1. Like Project
**Endpoint**: `POST /api/projects/{project_id}/like/`
**Method**: POST
**Authentication**: Token required
**Response**:
```json
{
  "message": "Project liked",
  "likes_count": 6
}
```

---

### 2. Unlike Project
**Endpoint**: `DELETE /api/projects/{project_id}/like/`
**Method**: DELETE
**Authentication**: Token required
**Response**:
```json
{
  "message": "Project unliked",
  "likes_count": 5
}
```

---

### 3. Follow User
**Endpoint**: `POST /api/users/{user_id}/follow/`
**Method**: POST
**Authentication**: Token required
**Response**:
```json
{
  "message": "User followed",
  "followers_count": 9
}
```

---

### 4. Unfollow User
**Endpoint**: `DELETE /api/users/{user_id}/follow/`
**Method**: DELETE
**Authentication**: Token required
**Response**:
```json
{
  "message": "User unfollowed",
  "followers_count": 8
}
```

---

## Error Responses

### Standard Error Response
```json
{
  "error": "Bad request",
  "message": "Invalid email format",
  "status_code": 400
}
```

### Authentication Error (401)
```json
{
  "error": "Unauthorized",
  "message": "Invalid or expired token"
}
```

### Permission Error (403)
```json
{
  "error": "Forbidden",
  "message": "You don't have permission to edit this project"
}
```

### Not Found Error (404)
```json
{
  "error": "Not found",
  "message": "Project with ID 999 not found"
}
```

### Server Error (500)
```json
{
  "error": "Internal server error",
  "message": "An unexpected error occurred"
}
```

---

## Pagination

All list endpoints support pagination:

**Query Parameters**:
- `page`: Page number (default: 1)
- `page_size`: Items per page (default: 10, max: 100)

**Response Format**:
```json
{
  "count": 42,
  "next": "https://api.unisync.com/api/projects/?page=2",
  "previous": null,
  "results": [...]
}
```

---

## Rate Limiting

API endpoints are rate-limited to prevent abuse:
- **Anonymous users**: 100 requests/hour
- **Authenticated users**: 1000 requests/hour
- **Premium users**: Unlimited

Response headers include:
```
X-RateLimit-Limit: 1000
X-RateLimit-Remaining: 999
X-RateLimit-Reset: 1642600000
```

---

## Authentication Headers

For all authenticated endpoints, include:
```
Authorization: Token abc123xyz...
Content-Type: application/json
```

Or for OAuth:
```
Authorization: Bearer google_access_token_xyz...
```

---

## Summary

This API provides comprehensive access to UniSync's features:
- ✅ User authentication and profiles
- ✅ Project management
- ✅ Real-time messaging and chat
- ✅ Comments and activity feeds
- ✅ Connection management
- ✅ Search and discovery
- ✅ Social features (likes, follows)
- ✅ Notifications
- ✅ File uploads and attachments

All endpoints follow REST conventions and provide consistent error handling and pagination.
