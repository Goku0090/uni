# UniSync API & Endpoints Reference

## Base URL
- **Development**: `http://localhost:8000`
- **Production**: Domain-dependent

---

## Authentication Endpoints

### POST /register/
User registration with email verification.

**Request Body**:
```json
{
  "username": "john_doe",
  "email": "john@example.com",
  "password1": "SecurePassword123!",
  "password2": "SecurePassword123!",
  "full_name": "John Doe"
}
```

**Response**: `201 Created`
```json
{
  "message": "User registered successfully",
  "user_id": 1,
  "email": "john@example.com"
}
```

---

### POST /login/
Login with OTP or password.

**Request Body (OTP)**:
```json
{
  "email": "john@example.com",
  "method": "otp"
}
```

**Response**: `200 OK`
```json
{
  "message": "OTP sent to email",
  "session_id": "abc123"
}
```

**Request Body (Password)**:
```json
{
  "username": "john_doe",
  "password": "SecurePassword123!",
  "method": "password"
}
```

**Response**: `200 OK`
```json
{
  "message": "Login successful",
  "user_id": 1,
  "session_id": "abc123"
}
```

---

### POST /verify-otp/{purpose}/
Verify OTP code.

**URL Parameters**:
- `purpose`: `login` | `registration` | `reset`

**Request Body**:
```json
{
  "email": "john@example.com",
  "otp_code": "123456"
}
```

**Response**: `200 OK`
```json
{
  "message": "OTP verified successfully",
  "user_id": 1
}
```

---

### GET /logout/
User logout (clears session).

**Response**: `302 Redirect` to `/login/`

---

### POST /forgot-password/
Initiate password reset.

**Request Body**:
```json
{
  "email": "john@example.com"
}
```

**Response**: `200 OK`
```json
{
  "message": "Password reset OTP sent to email"
}
```

---

### POST /reset-password/
Complete password reset.

**Request Body**:
```json
{
  "email": "john@example.com",
  "otp_code": "123456",
  "new_password": "NewPassword123!"
}
```

**Response**: `200 OK`
```json
{
  "message": "Password reset successfully"
}
```

---

## Profile Management

### GET /student-profile/
Get current user's profile (HTML page).

**Response**: HTML page with profile information

---

### POST /student-details/
Update student profile.

**Request Body** (multipart/form-data):
```json
{
  "full_name": "John Doe",
  "college": "MIT",
  "location": "Cambridge, MA",
  "bio": "Passionate developer",
  "interests": ["AI", "Web Development"],
  "skills": ["Python", "JavaScript", "Django"],
  "project_interests": ["Data Science", "Startups"],
  "role_preference": "Backend Developer",
  "github": "https://github.com/johndoe",
  "linkedin": "https://linkedin.com/in/johndoe",
  "portfolio": "https://johndoe.dev",
  "behance": "https://behance.net/johndoe",
  "profile_photo": <file>
}
```

**Response**: `200 OK`
```json
{
  "message": "Profile updated successfully",
  "profile": {
    "user_id": 1,
    "full_name": "John Doe",
    "college": "MIT",
    "skills": ["Python", "JavaScript", "Django"],
    "profile_photo": "/media/profile_photos/user1.jpg"
  }
}
```

---

### GET /user-profile/{user_id}/
Get user profile (API).

**Response**: `200 OK`
```json
{
  "user_id": 1,
  "username": "john_doe",
  "email": "john@example.com",
  "full_name": "John Doe",
  "college": "MIT",
  "bio": "Passionate developer",
  "profile_photo": "/media/profile_photos/user1.jpg",
  "skills": ["Python", "JavaScript"],
  "interests": ["AI", "Web Development"],
  "project_interests": ["Data Science"],
  "github": "https://github.com/johndoe",
  "linkedin": "https://linkedin.com/in/johndoe",
  "followers": 42,
  "following": 15,
  "projects_count": 5,
  "profile_completed": true
}
```

---

### GET /user/{username}/
View user profile (HTML page).

**Response**: HTML profile page

---

### POST /edit-profile/
Edit profile (HTML form).

**Response**: HTML form page

---

## Project Management

### POST /post-project/
Create new project.

**Request Body**:
```json
{
  "title": "AI Chat Application",
  "description": "Building an AI-powered chat application",
  "collaboration_needs": ["Backend Developer", "Frontend Developer"],
  "technologies": ["Python", "Django", "React", "PostgreSQL"],
  "status": "active",
  "visibility": "public",
  "images": [<file1>, <file2>]
}
```

**Response**: `201 Created`
```json
{
  "project_id": 1,
  "title": "AI Chat Application",
  "owner": {
    "user_id": 1,
    "username": "john_doe"
  },
  "status": "active",
  "visibility": "public",
  "created_at": "2024-01-15T10:30:00Z",
  "likes": 0,
  "comments": 0
}
```

---

### GET /project-detail/{project_id}/
Get project details.

**Response**: `200 OK`
```json
{
  "project_id": 1,
  "title": "AI Chat Application",
  "description": "Building an AI-powered chat application",
  "owner": {
    "user_id": 1,
    "username": "john_doe",
    "full_name": "John Doe",
    "profile_photo": "/media/profile_photos/user1.jpg"
  },
  "collaboration_needs": ["Backend Developer"],
  "technologies": ["Python", "Django"],
  "status": "active",
  "visibility": "public",
  "team": [
    {
      "user_id": 2,
      "username": "jane_smith",
      "role": "Frontend Developer"
    }
  ],
  "likes": 5,
  "comments": 3,
  "comments_list": [
    {
      "comment_id": 1,
      "author": {
        "username": "user1",
        "profile_photo": "/media/profile_photos/user1.jpg"
      },
      "content": "Great project!",
      "created_at": "2024-01-15T11:00:00Z",
      "likes": 2
    }
  ],
  "created_at": "2024-01-15T10:30:00Z",
  "updated_at": "2024-01-15T10:30:00Z"
}
```

---

### PUT /edit-project/{project_id}/
Edit project.

**Request Body**:
```json
{
  "title": "AI Chat Application v2",
  "description": "Updated description",
  "collaboration_needs": ["Backend Developer", "DevOps"],
  "technologies": ["Python", "Django", "React", "PostgreSQL", "Docker"],
  "status": "active",
  "visibility": "public"
}
```

**Response**: `200 OK`

---

### DELETE /delete-project/{project_id}/
Delete project.

**Response**: `204 No Content`

---

### GET /project-detail/{project_id}/?page={page}
List projects with pagination.

**Query Parameters**:
- `page`: Page number (default: 1)
- `search`: Search query
- `visibility`: Filter by visibility

**Response**: `200 OK`
```json
{
  "count": 100,
  "next": "/project-detail/?page=2",
  "previous": null,
  "results": [
    {
      "project_id": 1,
      "title": "Project 1",
      "owner": "user1",
      "likes": 5
    }
  ]
}
```

---

## Social Features

### POST /find-collaborators/
Search and filter users.

**Query Parameters**:
- `skill`: Filter by skill
- `interest`: Filter by interest
- `college`: Filter by college
- `search`: Search by name/username

**Response**: `200 OK`
```json
{
  "results": [
    {
      "user_id": 2,
      "username": "jane_smith",
      "full_name": "Jane Smith",
      "college": "Stanford",
      "bio": "Full-stack developer",
      "skills": ["JavaScript", "React", "Node.js"],
      "interests": ["Web Development", "AI"],
      "profile_photo": "/media/profile_photos/user2.jpg",
      "connection_status": "not_connected"
    }
  ],
  "count": 50
}
```

---

### POST /send-connection-request/{user_id}/
Send connection request.

**Response**: `201 Created`
```json
{
  "message": "Connection request sent",
  "connection_id": 1,
  "status": "pending"
}
```

---

### POST /accept-connection/{connection_id}/
Accept connection request.

**Response**: `200 OK`
```json
{
  "message": "Connection accepted",
  "connection_id": 1,
  "status": "accepted"
}
```

---

### POST /reject-connection/{connection_id}/
Reject connection request.

**Response**: `200 OK`
```json
{
  "message": "Connection rejected",
  "connection_id": 1,
  "status": "rejected"
}
```

---

### GET /my-connections/
Get user's connections.

**Query Parameters**:
- `status`: `pending` | `accepted` | `rejected`

**Response**: `200 OK`
```json
{
  "connections": [
    {
      "connection_id": 1,
      "user": {
        "user_id": 2,
        "username": "jane_smith",
        "full_name": "Jane Smith",
        "profile_photo": "/media/profile_photos/user2.jpg"
      },
      "status": "accepted",
      "created_at": "2024-01-15T10:00:00Z"
    }
  ],
  "total": 10
}
```

---

### POST /follow/{user_id}/
Follow user.

**Response**: `201 Created`
```json
{
  "message": "Now following user",
  "follow_id": 1
}
```

---

### POST /like-project/{project_id}/
Like project.

**Response**: `200 OK`
```json
{
  "message": "Project liked",
  "likes": 6
}
```

---

## Messaging & Chat

### POST /chat-rooms/
Create chat room.

**Request Body**:
```json
{
  "name": "AI Project Team",
  "description": "Chat room for AI project collaboration",
  "is_group": true,
  "members": [1, 2, 3]
}
```

**Response**: `201 Created`
```json
{
  "room_id": 1,
  "name": "AI Project Team",
  "owner": 1,
  "is_group": true,
  "members": [1, 2, 3],
  "created_at": "2024-01-15T10:30:00Z"
}
```

---

### GET /chat-rooms/
List chat rooms.

**Response**: `200 OK`
```json
{
  "results": [
    {
      "room_id": 1,
      "name": "AI Project Team",
      "owner": "john_doe",
      "is_group": true,
      "members_count": 3,
      "last_activity": "2024-01-15T15:30:00Z"
    }
  ]
}
```

---

### GET /chat-rooms/{id}/
Get chat room details.

**Response**: `200 OK`
```json
{
  "room_id": 1,
  "name": "AI Project Team",
  "description": "Chat room for AI project collaboration",
  "owner": {
    "user_id": 1,
    "username": "john_doe"
  },
  "is_group": true,
  "members": [
    {
      "user_id": 1,
      "username": "john_doe",
      "profile_photo": "/media/profile_photos/user1.jpg"
    },
    {
      "user_id": 2,
      "username": "jane_smith",
      "profile_photo": "/media/profile_photos/user2.jpg"
    }
  ],
  "created_at": "2024-01-15T10:30:00Z"
}
```

---

### POST /messages/
Create message.

**Request Body**:
```json
{
  "room_id": 1,
  "content": "Let's discuss the project architecture",
  "files": [<file1>, <file2>]
}
```

**Response**: `201 Created`
```json
{
  "message_id": 1,
  "sender": {
    "user_id": 1,
    "username": "john_doe"
  },
  "room_id": 1,
  "content": "Let's discuss the project architecture",
  "created_at": "2024-01-15T15:30:00Z",
  "is_read": false
}
```

---

### GET /messages/?room_id={room_id}
List messages.

**Query Parameters**:
- `room_id`: Chat room ID
- `page`: Page number
- `ordering`: `created_at` | `-created_at`

**Response**: `200 OK`
```json
{
  "count": 150,
  "next": "/messages/?room_id=1&page=2",
  "results": [
    {
      "message_id": 1,
      "sender": {
        "user_id": 1,
        "username": "john_doe"
      },
      "content": "Let's discuss the project architecture",
      "created_at": "2024-01-15T15:30:00Z",
      "is_read": true
    }
  ]
}
```

---

### POST /messages/{message_id}/status/
Update message status.

**Request Body**:
```json
{
  "is_read": true
}
```

**Response**: `200 OK`

---

### POST /messages/search/
Search messages.

**Query Parameters**:
- `query`: Search term
- `room_id`: Filter by room

**Response**: `200 OK`
```json
{
  "results": [
    {
      "message_id": 1,
      "content": "Let's discuss the project architecture",
      "sender": "john_doe",
      "created_at": "2024-01-15T15:30:00Z"
    }
  ]
}
```

---

### POST /messages/{message_id}/reactions/
Add emoji reaction to message.

**Request Body**:
```json
{
  "emoji": "👍"
}
```

**Response**: `201 Created`
```json
{
  "reaction_id": 1,
  "message_id": 1,
  "user": "john_doe",
  "emoji": "👍",
  "created_at": "2024-01-15T15:35:00Z"
}
```

---

### POST /typing/
Send typing indicator.

**Request Body**:
```json
{
  "room_id": 1,
  "is_typing": true
}
```

**Response**: `200 OK`

---

### POST /drafts/
Save draft message.

**Request Body**:
```json
{
  "room_id": 1,
  "content": "Draft message content"
}
```

**Response**: `201 Created`
```json
{
  "draft_id": 1,
  "room_id": 1,
  "content": "Draft message content",
  "created_at": "2024-01-15T15:30:00Z"
}
```

---

## Comments System

### POST /projects/{project_id}/comments/add/
Add comment to project.

**Request Body**:
```json
{
  "content": "Great project idea! I'd love to join."
}
```

**Response**: `201 Created`
```json
{
  "comment_id": 1,
  "project_id": 1,
  "author": {
    "user_id": 2,
    "username": "jane_smith",
    "profile_photo": "/media/profile_photos/user2.jpg"
  },
  "content": "Great project idea! I'd love to join.",
  "created_at": "2024-01-15T15:30:00Z",
  "likes": 0
}
```

---

### GET /projects/{project_id}/comments/
Get all comments for project.

**Query Parameters**:
- `page`: Page number
- `ordering`: `-created_at` (default)

**Response**: `200 OK`
```json
{
  "count": 5,
  "results": [
    {
      "comment_id": 1,
      "author": {
        "user_id": 2,
        "username": "jane_smith",
        "profile_photo": "/media/profile_photos/user2.jpg"
      },
      "content": "Great project idea!",
      "created_at": "2024-01-15T15:30:00Z",
      "likes": 2,
      "is_edited": false
    }
  ]
}
```

---

### DELETE /comments/{comment_id}/delete/
Delete comment (owner only).

**Response**: `204 No Content`

---

### PUT /comments/{comment_id}/edit/
Edit comment (owner only).

**Request Body**:
```json
{
  "content": "Updated comment content"
}
```

**Response**: `200 OK`
```json
{
  "comment_id": 1,
  "content": "Updated comment content",
  "is_edited": true,
  "edited_at": "2024-01-15T16:00:00Z"
}
```

---

## Notifications

### GET /notifications/
Get user notifications.

**Query Parameters**:
- `page`: Page number
- `is_read`: Filter by read status

**Response**: `200 OK`
```json
{
  "count": 15,
  "results": [
    {
      "notification_id": 1,
      "actor": {
        "user_id": 2,
        "username": "jane_smith"
      },
      "action_type": "like",
      "content": "jane_smith liked your project",
      "project_id": 1,
      "created_at": "2024-01-15T15:30:00Z",
      "is_read": false
    }
  ]
}
```

---

### POST /mark-notification-read/{notification_id}/
Mark notification as read.

**Response**: `200 OK`
```json
{
  "notification_id": 1,
  "is_read": true
}
```

---

## Activity Feed

### GET /activity-feed/
Get activity feed.

**Query Parameters**:
- `page`: Page number
- `ordering`: `-timestamp` (default)

**Response**: `200 OK`
```json
{
  "count": 100,
  "results": [
    {
      "activity_id": 1,
      "user": {
        "user_id": 1,
        "username": "john_doe"
      },
      "action_type": "project_posted",
      "description": "Posted new project: AI Chat Application",
      "project_id": 1,
      "timestamp": "2024-01-15T10:30:00Z"
    },
    {
      "activity_id": 2,
      "user": {
        "user_id": 2,
        "username": "jane_smith"
      },
      "action_type": "comment_added",
      "description": "Commented on AI Chat Application",
      "timestamp": "2024-01-15T15:30:00Z"
    }
  ]
}
```

---

## Utility Endpoints

### GET /check-username/?username={username}
Check username availability.

**Response**: `200 OK`
```json
{
  "available": true,
  "message": "Username is available"
}
```

---

### GET /check-email/?email={email}
Check email availability.

**Response**: `200 OK`
```json
{
  "available": true,
  "message": "Email is available"
}
```

---

### GET /college-search/?query={query}
Search colleges (RapidAPI).

**Response**: `200 OK`
```json
{
  "results": [
    {
      "name": "Massachusetts Institute of Technology",
      "location": "Cambridge, MA",
      "country": "USA"
    },
    {
      "name": "Stanford University",
      "location": "Stanford, CA",
      "country": "USA"
    }
  ]
}
```

---

### POST /validate-college/
Validate college name.

**Request Body**:
```json
{
  "college": "MIT"
}
```

**Response**: `200 OK`
```json
{
  "valid": true,
  "college": "Massachusetts Institute of Technology",
  "location": "Cambridge, MA"
}
```

---

### GET /user-stats/?user_id={user_id}
Get user statistics.

**Response**: `200 OK`
```json
{
  "user_id": 1,
  "username": "john_doe",
  "projects_created": 5,
  "projects_joined": 8,
  "connections": 42,
  "followers": 120,
  "following": 85,
  "comments_count": 35,
  "likes_received": 150
}
```

---

### POST /nlp-analyze/
Analyze project for NLP features.

**Request Body**:
```json
{
  "title": "AI Chat Application",
  "description": "Building an AI-powered chat application",
  "collaboration_needs": ["Backend Developer"]
}
```

**Response**: `200 OK`
```json
{
  "technologies": ["Python", "Django", "React"],
  "skills_required": ["Backend Development", "API Design"],
  "recommended_collaborators": [2, 5, 8],
  "project_complexity": "medium"
}
```

---

## Error Responses

### 400 Bad Request
```json
{
  "error": "Invalid input",
  "details": {
    "field": ["Error message"]
  }
}
```

### 401 Unauthorized
```json
{
  "error": "Authentication required"
}
```

### 403 Forbidden
```json
{
  "error": "You don't have permission to perform this action"
}
```

### 404 Not Found
```json
{
  "error": "Resource not found"
}
```

### 500 Internal Server Error
```json
{
  "error": "Internal server error",
  "request_id": "abc123"
}
```

---

## Response Headers

All API responses include:
```
Content-Type: application/json
X-Request-ID: <unique-id>
Cache-Control: no-cache
```

---

## Authentication

All endpoints except login/register/forgot-password require:
- Session authentication via `sessionid` cookie
- OR
- JWT token in `Authorization: Bearer <token>` header

---

## Rate Limiting

Coming soon (configured in settings).

---

## Webhooks

Coming soon (real-time event notifications).

---

## Pagination

Default pagination: 10 items per page

**Query Parameters**:
- `page`: Page number (default: 1)
- `page_size`: Items per page (default: 10, max: 100)

**Response**:
```json
{
  "count": 100,
  "next": "/api/endpoint/?page=2",
  "previous": null,
  "results": [...]
}
```

---

## Filtering & Search

Most list endpoints support:
- `search`: Search query
- `ordering`: Sort field (prefix with `-` for descending)
- `page`: Page number

Example:
```
GET /find-collaborators/?search=python&ordering=-created_at&page=2
```

---

## Last Updated
January 15, 2024

---

## Support

For API issues, refer to:
- Django REST Framework docs: https://www.django-rest-framework.org/
- Django Allauth docs: https://django-allauth.readthedocs.io/
- UniSync GitHub: (link here)
