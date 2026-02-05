# UniSync API Endpoints Reference (2026)

## Base URL
```
Development: http://localhost:8000/api/
Production: https://unisync.in/api/
```

---

## Authentication Endpoints

### 1. User Login
```http
POST /api/login/
```
**Request Body:**
```json
{
  "email": "user@example.com",
  "password": "password123"
}
```

**Response (200):**
```json
{
  "status": "success",
  "message": "OTP sent to your email",
  "purpose": "login"
}
```

**Next Step:** Verify OTP at `/verify-otp/login/`

---

### 2. User Registration
```http
POST /api/register/
```
**Request Body:**
```json
{
  "email": "newuser@example.com",
  "username": "newuser",
  "password": "securepass123",
  "password_confirm": "securepass123"
}
```

**Response (201):**
```json
{
  "status": "success",
  "message": "Registration successful. OTP sent to email.",
  "purpose": "registration"
}
```

---

### 3. Verify OTP
```http
POST /api/verify-otp/<purpose>/
```
**URL Parameters:**
- `purpose`: `login` | `registration` | `reset`

**Request Body:**
```json
{
  "email": "user@example.com",
  "otp_code": "123456"
}
```

**Response (200):**
```json
{
  "status": "success",
  "message": "OTP verified successfully",
  "user_id": 42,
  "username": "john_doe"
}
```

---

### 4. Resend OTP
```http
POST /api/resend-otp/<purpose>/
```
**Request Body:**
```json
{
  "email": "user@example.com"
}
```

**Response (200):**
```json
{
  "status": "success",
  "message": "OTP resent to your email"
}
```

---

### 5. Forgot Password
```http
POST /api/forgot-password/
```
**Request Body:**
```json
{
  "email": "user@example.com"
}
```

**Response (200):**
```json
{
  "status": "success",
  "message": "Password reset OTP sent to your email"
}
```

---

### 6. Reset Password
```http
POST /api/reset-password/
```
**Request Body:**
```json
{
  "email": "user@example.com",
  "otp_code": "123456",
  "new_password": "newsecurepass123",
  "confirm_password": "newsecurepass123"
}
```

**Response (200):**
```json
{
  "status": "success",
  "message": "Password reset successfully"
}
```

---

### 7. Logout
```http
POST /api/logout/
```
**Headers:**
```
Authorization: Bearer <token>
```

**Response (200):**
```json
{
  "status": "success",
  "message": "Logged out successfully"
}
```

---

## User Profile Endpoints

### 8. Get Current User Profile
```http
GET /api/profile/
```
**Headers:**
```
Authorization: Bearer <token>
```

**Response (200):**
```json
{
  "id": 1,
  "username": "john_doe",
  "email": "john@example.com",
  "full_name": "John Doe",
  "college": "MIT",
  "location": "Boston, MA",
  "interests": ["AI", "Web Development"],
  "skills": ["Python", "JavaScript", "Django"],
  "bio": "Passionate about building great software",
  "profile_photo": "https://cdn.example.com/profile_photos/1.jpg",
  "github": "https://github.com/johndoe",
  "linkedin": "https://linkedin.com/in/johndoe",
  "portfolio": "https://johndoe.com",
  "profile_completed": true,
  "is_online": true,
  "date_joined": "2024-01-15T10:30:00Z"
}
```

---

### 9. Get User Profile by ID
```http
GET /api/user-profile/<user_id>/
```
**URL Parameters:**
- `user_id`: Integer (User ID)

**Response (200):**
```json
{
  "id": 1,
  "username": "john_doe",
  "email": "john@example.com",
  "full_name": "John Doe",
  "college": "MIT",
  "location": "Boston, MA",
  "interests": ["AI", "Web Development"],
  "skills": ["Python", "JavaScript", "Django"],
  "bio": "Passionate about building great software",
  "profile_photo": "https://cdn.example.com/profile_photos/1.jpg",
  "profile_completed": true,
  "is_online": true
}
```

---

### 10. Update User Profile
```http
POST /api/student-details/
```
**Headers:**
```
Authorization: Bearer <token>
```

**Request Body:**
```json
{
  "full_name": "John Doe",
  "college": "MIT",
  "location": "Boston, MA",
  "bio": "Updated bio",
  "interests": ["AI", "Web Development", "Blockchain"],
  "skills": ["Python", "JavaScript", "Django", "React"],
  "role_preference": "Backend Developer",
  "github": "https://github.com/johndoe",
  "linkedin": "https://linkedin.com/in/johndoe",
  "portfolio": "https://johndoe.com"
}
```

**Response (200):**
```json
{
  "status": "success",
  "message": "Profile updated successfully",
  "profile": { ... }
}
```

---

## Project Endpoints

### 11. Create Project
```http
POST /api/post-project/
```
**Headers:**
```
Authorization: Bearer <token>
Content-Type: multipart/form-data
```

**Request Body:**
```json
{
  "title": "AI-Powered Chat Application",
  "description": "Building an intelligent chatbot using NLP",
  "category": "AI/ML",
  "technologies": ["Python", "TensorFlow", "Django"],
  "looking_for": "Frontend Developer, UI/UX Designer",
  "collaboration_needs": "Need 2-3 developers for frontend",
  "timeline": "3 months",
  "github_link": "https://github.com/johndoe/chat-ai",
  "visibility": "public"
}
```

**Response (201):**
```json
{
  "status": "success",
  "message": "Project created successfully",
  "project": {
    "id": 1,
    "title": "AI-Powered Chat Application",
    "owner": { ... },
    "created_at": "2026-02-05T10:30:00Z"
  }
}
```

---

### 12. Get Project Details
```http
GET /api/project-detail/<project_id>/
```
**URL Parameters:**
- `project_id`: Integer (Project ID)

**Response (200):**
```json
{
  "id": 1,
  "title": "AI-Powered Chat Application",
  "description": "Building an intelligent chatbot using NLP",
  "category": "AI/ML",
  "technologies": ["Python", "TensorFlow", "Django"],
  "looking_for": "Frontend Developer, UI/UX Designer",
  "collaboration_needs": "Need 2-3 developers for frontend",
  "timeline": "3 months",
  "github_link": "https://github.com/johndoe/chat-ai",
  "owner": {
    "id": 1,
    "username": "john_doe",
    "full_name": "John Doe",
    "profile_photo": "..."
  },
  "likes_count": 15,
  "comments_count": 8,
  "members": [
    { "id": 1, "username": "john_doe", "role": "owner" },
    { "id": 2, "username": "jane_smith", "role": "developer" }
  ],
  "created_at": "2026-02-05T10:30:00Z",
  "updated_at": "2026-02-06T14:20:00Z"
}
```

---

### 13. Update Project
```http
POST /api/edit-project/<project_id>/
```
**Headers:**
```
Authorization: Bearer <token>
```

**Request Body:**
```json
{
  "title": "Updated Title",
  "description": "Updated description",
  "technologies": ["Python", "TensorFlow", "Django", "React"],
  "visibility": "friends-only"
}
```

**Response (200):**
```json
{
  "status": "success",
  "message": "Project updated successfully"
}
```

---

### 14. Delete Project
```http
POST /api/delete-project/<project_id>/
```
**Headers:**
```
Authorization: Bearer <token>
```

**Response (200):**
```json
{
  "status": "success",
  "message": "Project deleted successfully"
}
```

---

### 15. Like/Unlike Project
```http
POST /api/like-project/<project_id>/
```
**Headers:**
```
Authorization: Bearer <token>
```

**Response (200):**
```json
{
  "status": "success",
  "message": "Project liked",
  "likes_count": 16
}
```

**Response (for unlike):**
```json
{
  "status": "success",
  "message": "Project unliked",
  "likes_count": 15
}
```

---

## Comments Endpoints

### 16. Get Comments for Project
```http
GET /api/projects/<project_id>/comments/
```
**Query Parameters:**
- `page`: Integer (default: 1)
- `limit`: Integer (default: 10)

**Response (200):**
```json
{
  "status": "success",
  "data": [
    {
      "id": 1,
      "content": "Great project idea!",
      "author": {
        "id": 1,
        "username": "jane_smith",
        "profile_photo": "..."
      },
      "created_at": "2026-02-05T11:00:00Z",
      "updated_at": "2026-02-05T11:00:00Z"
    },
    ...
  ],
  "pagination": {
    "page": 1,
    "limit": 10,
    "total": 8
  }
}
```

---

### 17. Add Comment to Project
```http
POST /api/projects/<project_id>/comments/add/
```
**Headers:**
```
Authorization: Bearer <token>
Content-Type: application/json
```

**Request Body:**
```json
{
  "content": "Great project idea! I'd love to contribute."
}
```

**Response (201):**
```json
{
  "status": "success",
  "message": "Comment added successfully",
  "comment": {
    "id": 9,
    "content": "Great project idea! I'd love to contribute.",
    "author": { ... },
    "created_at": "2026-02-06T15:30:00Z"
  }
}
```

---

### 18. Edit Comment
```http
POST /api/comments/<comment_id>/edit/
```
**Headers:**
```
Authorization: Bearer <token>
```

**Request Body:**
```json
{
  "content": "Updated comment text"
}
```

**Response (200):**
```json
{
  "status": "success",
  "message": "Comment updated successfully"
}
```

---

### 19. Delete Comment
```http
DELETE /api/comments/<comment_id>/delete/
```
**Headers:**
```
Authorization: Bearer <token>
```

**Response (200):**
```json
{
  "status": "success",
  "message": "Comment deleted successfully"
}
```

---

## Social/Connection Endpoints

### 20. Find Collaborators
```http
GET /api/find-collaborators/
```
**Query Parameters:**
- `interests`: Comma-separated (e.g., "AI,Web Development")
- `skills`: Comma-separated (e.g., "Python,JavaScript")
- `role`: String (e.g., "Backend Developer")
- `page`: Integer (default: 1)

**Response (200):**
```json
{
  "status": "success",
  "data": [
    {
      "id": 2,
      "username": "jane_smith",
      "full_name": "Jane Smith",
      "college": "Stanford",
      "skills": ["Python", "React", "AWS"],
      "interests": ["AI", "Web Development"],
      "profile_photo": "...",
      "connection_status": "not_connected"
    },
    ...
  ],
  "pagination": {
    "page": 1,
    "limit": 10,
    "total": 25
  }
}
```

---

### 21. Send Connection Request
```http
POST /api/connect/<user_id>/
```
**Headers:**
```
Authorization: Bearer <token>
```

**Response (201):**
```json
{
  "status": "success",
  "message": "Connection request sent",
  "connection": {
    "id": 1,
    "from_user": 1,
    "to_user": 2,
    "status": "pending",
    "created_at": "2026-02-06T15:30:00Z"
  }
}
```

---

### 22. Accept Connection Request
```http
POST /api/accept-connection/<connection_id>/
```
**Headers:**
```
Authorization: Bearer <token>
```

**Response (200):**
```json
{
  "status": "success",
  "message": "Connection request accepted",
  "connection": {
    "id": 1,
    "from_user": 1,
    "to_user": 2,
    "status": "accepted",
    "updated_at": "2026-02-06T16:00:00Z"
  }
}
```

---

### 23. Reject Connection Request
```http
POST /api/reject-connection/<connection_id>/
```
**Headers:**
```
Authorization: Bearer <token>
```

**Response (200):**
```json
{
  "status": "success",
  "message": "Connection request rejected"
}
```

---

### 24. Cancel Connection Request
```http
POST /api/cancel-connection/<connection_id>/
```
**Headers:**
```
Authorization: Bearer <token>
```

**Response (200):**
```json
{
  "status": "success",
  "message": "Connection request cancelled"
}
```

---

### 25. Get My Connections
```http
GET /api/my-connections/
```
**Headers:**
```
Authorization: Bearer <token>
```

**Query Parameters:**
- `status`: `accepted` | `pending` | `all` (default: all)
- `page`: Integer (default: 1)

**Response (200):**
```json
{
  "status": "success",
  "data": [
    {
      "id": 1,
      "from_user": {
        "id": 1,
        "username": "john_doe",
        "full_name": "John Doe"
      },
      "to_user": {
        "id": 2,
        "username": "jane_smith",
        "full_name": "Jane Smith"
      },
      "status": "accepted",
      "created_at": "2026-02-05T10:30:00Z"
    },
    ...
  ]
}
```

---

### 26. Follow User
```http
POST /api/follow/<user_id>/
```
**Headers:**
```
Authorization: Bearer <token>
```

**Response (201):**
```json
{
  "status": "success",
  "message": "Now following user"
}
```

---

## Chat/Messaging Endpoints

### 27. List Chat Rooms
```http
GET /api/chat-rooms/
```
**Headers:**
```
Authorization: Bearer <token>
```

**Query Parameters:**
- `type`: `all` | `direct` | `group` (default: all)
- `page`: Integer (default: 1)

**Response (200):**
```json
{
  "status": "success",
  "data": [
    {
      "id": 1,
      "name": "John Doe",
      "is_group": false,
      "members": [
        { "id": 1, "username": "john_doe" },
        { "id": 2, "username": "jane_smith" }
      ],
      "last_message": {
        "id": 100,
        "content": "See you later!",
        "sender": 1,
        "created_at": "2026-02-06T15:30:00Z"
      },
      "unread_count": 2,
      "created_at": "2026-02-05T10:30:00Z"
    },
    ...
  ]
}
```

---

### 28. Create Chat Room
```http
POST /api/chat-rooms/
```
**Headers:**
```
Authorization: Bearer <token>
```

**Request Body:**
```json
{
  "name": "Project Discussion Group",
  "is_group": true,
  "member_ids": [1, 2, 3]
}
```

**Response (201):**
```json
{
  "status": "success",
  "message": "Chat room created",
  "room": {
    "id": 2,
    "name": "Project Discussion Group",
    "is_group": true,
    "created_at": "2026-02-06T16:00:00Z"
  }
}
```

---

### 29. Get Chat Room Details
```http
GET /api/chat-rooms/<room_id>/
```
**Headers:**
```
Authorization: Bearer <token>
```

**Response (200):**
```json
{
  "id": 1,
  "name": "John Doe",
  "is_group": false,
  "members": [
    { "id": 1, "username": "john_doe", "joined_at": "2026-02-05T10:30:00Z" },
    { "id": 2, "username": "jane_smith", "joined_at": "2026-02-05T10:30:00Z" }
  ],
  "created_at": "2026-02-05T10:30:00Z"
}
```

---

### 30. Get Chat Room Members
```http
GET /api/chat-rooms/<room_id>/members/
```
**Headers:**
```
Authorization: Bearer <token>
```

**Response (200):**
```json
{
  "status": "success",
  "data": [
    {
      "id": 1,
      "username": "john_doe",
      "full_name": "John Doe",
      "profile_photo": "...",
      "joined_at": "2026-02-05T10:30:00Z"
    },
    ...
  ]
}
```

---

### 31. Send Direct Message
```http
POST /api/direct-message/
```
**Headers:**
```
Authorization: Bearer <token>
```

**Request Body:**
```json
{
  "recipient_id": 2,
  "content": "Hey, how are you?"
}
```

**Response (201):**
```json
{
  "status": "success",
  "message": "Message sent",
  "room_id": 1,
  "message": {
    "id": 101,
    "content": "Hey, how are you?",
    "sender": 1,
    "created_at": "2026-02-06T16:30:00Z"
  }
}
```

---

### 32. Send Message in Room
```http
POST /api/messages/
```
**Headers:**
```
Authorization: Bearer <token>
Content-Type: application/json
```

**Request Body:**
```json
{
  "room_id": 1,
  "content": "Hello everyone!",
  "message_type": "text"
}
```

**Response (201):**
```json
{
  "status": "success",
  "message": "Message sent",
  "data": {
    "id": 102,
    "room_id": 1,
    "sender": { ... },
    "content": "Hello everyone!",
    "message_type": "text",
    "created_at": "2026-02-06T16:35:00Z"
  }
}
```

---

### 33. Get Messages from Room
```http
GET /api/messages/?room_id=<room_id>
```
**Headers:**
```
Authorization: Bearer <token>
```

**Query Parameters:**
- `room_id`: Integer (required)
- `page`: Integer (default: 1)
- `limit`: Integer (default: 50)

**Response (200):**
```json
{
  "status": "success",
  "data": [
    {
      "id": 100,
      "content": "Hello!",
      "sender": { ... },
      "message_type": "text",
      "created_at": "2026-02-06T15:30:00Z",
      "is_read": true,
      "reactions": {
        "👍": 2,
        "❤️": 1
      }
    },
    ...
  ],
  "pagination": {
    "page": 1,
    "limit": 50,
    "total": 150
  }
}
```

---

### 34. Mark Message as Read
```http
POST /api/messages/<message_id>/status/
```
**Headers:**
```
Authorization: Bearer <token>
```

**Request Body:**
```json
{
  "is_read": true
}
```

**Response (200):**
```json
{
  "status": "success",
  "message": "Message marked as read"
}
```

---

### 35. Add Reaction to Message
```http
POST /api/messages/<message_id>/reactions/
```
**Headers:**
```
Authorization: Bearer <token>
```

**Request Body:**
```json
{
  "reaction": "👍"
}
```

**Response (201):**
```json
{
  "status": "success",
  "message": "Reaction added",
  "reactions": {
    "👍": 3,
    "❤️": 1
  }
}
```

---

### 36. Search Messages
```http
GET /api/messages/search/?q=<query>
```
**Headers:**
```
Authorization: Bearer <token>
```

**Query Parameters:**
- `q`: Search query (required)
- `room_id`: Integer (optional, filter by room)
- `page`: Integer (default: 1)

**Response (200):**
```json
{
  "status": "success",
  "data": [
    {
      "id": 50,
      "content": "Let's meet up to discuss the project",
      "sender": { ... },
      "room_id": 1,
      "created_at": "2026-02-06T10:00:00Z"
    },
    ...
  ],
  "pagination": {
    "page": 1,
    "total": 5
  }
}
```

---

### 37. List Conversations
```http
GET /api/conversations/
```
**Headers:**
```
Authorization: Bearer <token>
```

**Response (200):**
```json
{
  "status": "success",
  "data": [
    {
      "room_id": 1,
      "name": "Jane Smith",
      "is_group": false,
      "last_message": "See you later!",
      "last_message_time": "2026-02-06T15:30:00Z",
      "unread_count": 2
    },
    {
      "room_id": 2,
      "name": "Project Team",
      "is_group": true,
      "last_message": "Meeting scheduled for tomorrow",
      "last_message_time": "2026-02-06T14:00:00Z",
      "unread_count": 0
    }
  ]
}
```

---

## Notification Endpoints

### 38. Get Notifications
```http
GET /api/notifications/
```
**Headers:**
```
Authorization: Bearer <token>
```

**Query Parameters:**
- `page`: Integer (default: 1)
- `unread_only`: Boolean (default: false)

**Response (200):**
```json
{
  "status": "success",
  "data": [
    {
      "id": 1,
      "actor": { "id": 2, "username": "jane_smith" },
      "action_type": "connection_request",
      "content": "Jane Smith sent you a connection request",
      "target_project": null,
      "is_read": false,
      "created_at": "2026-02-06T16:00:00Z"
    },
    {
      "id": 2,
      "actor": { "id": 3, "username": "bob_wilson" },
      "action_type": "project_comment",
      "content": "Bob Wilson commented on your project",
      "target_project": { "id": 1, "title": "AI Chat App" },
      "is_read": false,
      "created_at": "2026-02-06T15:30:00Z"
    }
  ]
}
```

---

### 39. Mark Notification as Read
```http
POST /api/mark-notification-read/<notification_id>/
```
**Headers:**
```
Authorization: Bearer <token>
```

**Response (200):**
```json
{
  "status": "success",
  "message": "Notification marked as read"
}
```

---

## Statistics Endpoints

### 40. Get User Statistics
```http
GET /api/user-stats/
```
**Headers:**
```
Authorization: Bearer <token>
```

**Response (200):**
```json
{
  "status": "success",
  "data": {
    "user_id": 1,
    "username": "john_doe",
    "projects_created": 5,
    "projects_participated": 8,
    "connections_count": 12,
    "followers_count": 25,
    "total_likes": 45,
    "total_comments": 23,
    "last_active": "2026-02-06T16:30:00Z"
  }
}
```

---

## Error Responses

### 400 Bad Request
```json
{
  "status": "error",
  "message": "Invalid input",
  "errors": {
    "email": "Email is required",
    "password": "Password must be at least 8 characters"
  }
}
```

### 401 Unauthorized
```json
{
  "status": "error",
  "message": "Authentication required",
  "code": 401
}
```

### 403 Forbidden
```json
{
  "status": "error",
  "message": "You don't have permission to perform this action",
  "code": 403
}
```

### 404 Not Found
```json
{
  "status": "error",
  "message": "Resource not found",
  "code": 404
}
```

### 500 Server Error
```json
{
  "status": "error",
  "message": "Internal server error",
  "code": 500
}
```

---

## Request Headers

### Required Headers
```
Authorization: Bearer <jwt_token>  (for protected endpoints)
Content-Type: application/json      (for POST/PUT requests)
```

### Optional Headers
```
X-Request-ID: <unique-id>          (for tracking requests)
X-Platform: web|mobile|desktop     (client platform)
```

---

## Rate Limiting

**Default Rate Limits:**
- **Authenticated Users**: 1000 requests/hour
- **Anonymous Users**: 100 requests/hour
- **Login Endpoint**: 5 attempts/minute

**Rate Limit Headers:**
```
X-RateLimit-Limit: 1000
X-RateLimit-Remaining: 999
X-RateLimit-Reset: 1644151200
```

---

## Pagination

All list endpoints support pagination:

**Query Parameters:**
- `page`: Page number (default: 1)
- `limit`: Items per page (default: 10, max: 100)

**Response Format:**
```json
{
  "status": "success",
  "data": [ ... ],
  "pagination": {
    "page": 1,
    "limit": 10,
    "total": 250,
    "pages": 25,
    "has_next": true,
    "has_previous": false
  }
}
```

---

## Filters & Search

### Filter Syntax
```
GET /api/projects/?category=AI&visibility=public&technologies=Python
```

### Search Syntax
```
GET /api/projects/search/?q=chatbot
GET /api/users/search/?q=john&interests=AI
```

---

## Sorting

### Sort Parameters
```
GET /api/projects/?sort=-created_at       # Newest first
GET /api/projects/?sort=title             # Alphabetical
GET /api/messages/?sort=-created_at&limit=50  # Recent messages
```

---

**Last Updated**: February 6, 2026
**API Version**: 1.0
**Status**: Production Ready
