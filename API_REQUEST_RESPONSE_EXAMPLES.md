# UniSync API - Request & Response Examples

## 📋 Table of Contents
1. [Authentication APIs](#authentication-apis)
2. [User Profile APIs](#user-profile-apis)
3. [Project APIs](#project-apis)
4. [Messaging APIs](#messaging-apis)
5. [Social APIs](#social-apis)
6. [Error Responses](#error-responses)

---

## Authentication APIs

### 1. Register User
**Endpoint**: `POST /register/`

**Request**:
```json
{
  "username": "johndoe",
  "email": "john@example.com",
  "password1": "SecurePass123",
  "password2": "SecurePass123",
  "terms_agree": true
}
```

**Response** (Success - 201):
```json
{
  "id": 1,
  "username": "johndoe",
  "email": "john@example.com",
  "message": "Registration successful! OTP sent to your email.",
  "redirect": "/verify-otp/registration/"
}
```

**Response** (Error - 400):
```json
{
  "username": ["This username is already taken."],
  "email": ["An account with this email already exists."],
  "password1": ["Password must contain at least one uppercase letter."]
}
```

---

### 2. Login with Credentials
**Endpoint**: `POST /login/`

**Request**:
```json
{
  "username": "johndoe",
  "password": "SecurePass123",
  "login_method": "password"
}
```

**Response** (Success - 200):
```json
{
  "user_id": 1,
  "username": "johndoe",
  "email": "john@example.com",
  "message": "Login successful!",
  "redirect": "/dashboard/",
  "session_id": "abc123xyz"
}
```

**Response** (Requires OTP - 200):
```json
{
  "message": "OTP sent to your email",
  "purpose": "login",
  "redirect": "/verify-otp/login/",
  "email_masked": "jo**@example.com"
}
```

---

### 3. Login with OTP
**Endpoint**: `POST /login/`

**Request**:
```json
{
  "email": "john@example.com",
  "login_method": "otp"
}
```

**Response** (OTP Sent - 200):
```json
{
  "message": "OTP sent to your email",
  "purpose": "login",
  "expires_in": 300,
  "redirect": "/verify-otp/login/"
}
```

---

### 4. Verify OTP
**Endpoint**: `POST /verify-otp/login/`

**Request**:
```json
{
  "email": "john@example.com",
  "otp_code": "123456",
  "purpose": "login"
}
```

**Response** (Success - 200):
```json
{
  "user_id": 1,
  "username": "johndoe",
  "email": "john@example.com",
  "message": "OTP verified! Logged in successfully.",
  "redirect": "/dashboard/",
  "token": "abc123xyz789"
}
```

**Response** (Invalid OTP - 400):
```json
{
  "error": "Invalid OTP code.",
  "remaining_attempts": 2
}
```

---

### 5. Resend OTP
**Endpoint**: `POST /resend-otp/login/`

**Request**:
```json
{
  "email": "john@example.com",
  "purpose": "login"
}
```

**Response** (Success - 200):
```json
{
  "message": "OTP resent to your email",
  "expires_in": 300
}
```

---

### 6. Forgot Password
**Endpoint**: `POST /forgot-password/`

**Request**:
```json
{
  "email": "john@example.com"
}
```

**Response** (Success - 200):
```json
{
  "message": "Password reset OTP sent to your email",
  "purpose": "reset",
  "expires_in": 300,
  "redirect": "/reset-password/"
}
```

---

### 7. Reset Password
**Endpoint**: `POST /reset-password/`

**Request**:
```json
{
  "email": "john@example.com",
  "otp_code": "123456",
  "new_password": "NewSecurePass456",
  "confirm_password": "NewSecurePass456"
}
```

**Response** (Success - 200):
```json
{
  "message": "Password reset successfully!",
  "redirect": "/login/"
}
```

---

### 8. Logout
**Endpoint**: `GET /logout/`

**Response** (Success - 200):
```json
{
  "message": "Logged out successfully",
  "redirect": "/login/"
}
```

---

## User Profile APIs

### 1. Get User Profile
**Endpoint**: `GET /user-profile/<user_id>/`

**Response** (Success - 200):
```json
{
  "id": 1,
  "user": {
    "id": 1,
    "username": "johndoe",
    "email": "john@example.com",
    "first_name": "John",
    "last_name": "Doe"
  },
  "full_name": "John Doe",
  "college": "MIT",
  "location": "Boston, MA",
  "bio": "Computer Science student interested in AI",
  "profile_photo": "https://cdn.example.com/photos/johndoe.jpg",
  "skills": ["Python", "JavaScript", "React"],
  "project_interests": ["AI/ML", "Web Development"],
  "role_preference": "Backend Developer",
  "github": "https://github.com/johndoe",
  "linkedin": "https://linkedin.com/in/johndoe",
  "portfolio": "https://johndoe.dev",
  "profile_completed": true,
  "created_at": "2024-01-15T10:30:00Z",
  "updated_at": "2025-02-01T14:20:00Z",
  "followers_count": 45,
  "following_count": 32,
  "projects_count": 8
}
```

---

### 2. Update User Profile
**Endpoint**: `POST /student-details/`

**Request**:
```json
{
  "full_name": "John Doe",
  "college": "MIT",
  "location": "Boston, MA",
  "bio": "CS student interested in AI & ML",
  "skills": ["Python", "JavaScript", "React", "Django"],
  "project_interests": ["AI/ML", "Web Development", "Cloud"],
  "role_preference": "Full Stack Developer",
  "github": "https://github.com/johndoe",
  "linkedin": "https://linkedin.com/in/johndoe"
}
```

**Response** (Success - 200):
```json
{
  "message": "Profile updated successfully!",
  "profile": {
    "full_name": "John Doe",
    "college": "MIT",
    "skills": ["Python", "JavaScript", "React", "Django"],
    "profile_completed": true
  }
}
```

---

### 3. Upload Profile Photo
**Endpoint**: `POST /edit-profile/`

**Request** (multipart/form-data):
```
Content-Type: multipart/form-data; boundary=----WebKitFormBoundary

------WebKitFormBoundary
Content-Disposition: form-data; name="profile_photo"; filename="photo.jpg"
Content-Type: image/jpeg

[binary image data]
------WebKitFormBoundary
```

**Response** (Success - 200):
```json
{
  "message": "Profile updated successfully!",
  "profile_photo": "https://cdn.example.com/photos/johndoe.jpg"
}
```

---

### 4. View Other User's Profile
**Endpoint**: `GET /user/<username>/`

**Response** (Success - 200):
```json
{
  "user": {
    "username": "johndoe",
    "email": "john@example.com"
  },
  "profile": {
    "full_name": "John Doe",
    "college": "MIT",
    "bio": "CS student interested in AI",
    "profile_photo": "https://cdn.example.com/photos/johndoe.jpg",
    "skills": ["Python", "JavaScript"],
    "followers_count": 45,
    "following_count": 32
  },
  "stats": {
    "projects_created": 8,
    "connections": 12,
    "followers": 45
  },
  "is_following": false,
  "connection_status": "pending"
}
```

---

### 5. Get User Statistics
**Endpoint**: `GET /user-stats/`

**Response** (Success - 200):
```json
{
  "user_id": 1,
  "username": "johndoe",
  "stats": {
    "projects_created": 8,
    "connections_made": 12,
    "likes_received": 34,
    "comments_made": 21,
    "projects_joined": 5,
    "tasks_completed": 18,
    "followers_count": 45,
    "following_count": 32
  },
  "last_updated": "2025-02-01T14:20:00Z"
}
```

---

## Project APIs

### 1. Create Project
**Endpoint**: `POST /post-project/`

**Request**:
```json
{
  "title": "AI Chat Application",
  "description": "Building an AI-powered chatbot using GPT-4 and Django",
  "category": "AI/ML",
  "visibility": "public",
  "skills_required": ["Python", "Machine Learning", "NLP"],
  "members_needed": 3,
  "collaboration_needs": "Looking for ML engineers and frontend developers"
}
```

**Response** (Success - 201):
```json
{
  "id": 42,
  "title": "AI Chat Application",
  "description": "Building an AI-powered chatbot using GPT-4 and Django",
  "owner": {
    "id": 1,
    "username": "johndoe"
  },
  "visibility": "public",
  "status": "active",
  "created_at": "2025-02-01T14:20:00Z",
  "redirect": "/project/42/",
  "message": "Project created successfully!"
}
```

---

### 2. Get Project Details
**Endpoint**: `GET /project/<project_id>/`

**Response** (Success - 200):
```json
{
  "id": 42,
  "title": "AI Chat Application",
  "description": "Building an AI-powered chatbot using GPT-4 and Django",
  "owner": {
    "id": 1,
    "username": "johndoe",
    "profile_photo": "https://cdn.example.com/photos/johndoe.jpg"
  },
  "category": "AI/ML",
  "visibility": "public",
  "skills_required": ["Python", "Machine Learning", "NLP"],
  "members_needed": 3,
  "members_current": 2,
  "status": "active",
  "likes_count": 15,
  "comments_count": 8,
  "created_at": "2025-02-01T14:20:00Z",
  "updated_at": "2025-02-01T14:20:00Z",
  "team": [
    {
      "id": 1,
      "username": "johndoe",
      "role": "owner"
    },
    {
      "id": 5,
      "username": "janedoe",
      "role": "contributor"
    }
  ],
  "is_liked_by_user": false,
  "is_member": false,
  "can_edit": false
}
```

---

### 3. Update Project
**Endpoint**: `PUT /edit-project/<project_id>/`

**Request**:
```json
{
  "title": "AI Chat Application v2",
  "description": "Improved version with voice support",
  "members_needed": 2,
  "visibility": "private"
}
```

**Response** (Success - 200):
```json
{
  "id": 42,
  "message": "Project updated successfully!",
  "project": {
    "title": "AI Chat Application v2",
    "description": "Improved version with voice support",
    "members_needed": 2,
    "visibility": "private"
  }
}
```

---

### 4. Delete Project
**Endpoint**: `DELETE /delete-project/<project_id>/`

**Response** (Success - 200):
```json
{
  "message": "Project deleted successfully!",
  "redirect": "/my-projects/"
}
```

---

### 5. Like Project
**Endpoint**: `POST /like-project/<project_id>/`

**Request**:
```json
{
  "action": "like"
}
```

**Response** (Success - 200):
```json
{
  "status": "liked",
  "likes_count": 16,
  "message": "Project liked!"
}
```

---

### 6. Explore Projects
**Endpoint**: `GET /explore-projects/?page=1&search=AI&sort=-created_at`

**Response** (Success - 200):
```json
{
  "count": 127,
  "next": "https://api.example.com/explore-projects/?page=2",
  "previous": null,
  "results": [
    {
      "id": 42,
      "title": "AI Chat Application",
      "description": "Building an AI-powered chatbot...",
      "owner": {"id": 1, "username": "johndoe"},
      "likes_count": 16,
      "members_count": 2,
      "created_at": "2025-02-01T14:20:00Z"
    }
  ]
}
```

---

### 7. Search Projects
**Endpoint**: `GET /search_projects/?q=python&category=web`

**Response** (Success - 200):
```json
{
  "count": 23,
  "results": [
    {
      "id": 42,
      "title": "AI Chat Application",
      "category": "AI/ML",
      "skills_required": ["Python", "ML"],
      "match_score": 0.95
    }
  ]
}
```

---

## Messaging APIs

### 1. Send Message
**Endpoint**: `POST /messages/`

**Request**:
```json
{
  "receiver_id": 5,
  "content": "Hey, want to collaborate on a project?",
  "message_type": "text"
}
```

**Response** (Success - 201):
```json
{
  "id": 1023,
  "sender": {
    "id": 1,
    "username": "johndoe"
  },
  "receiver": {
    "id": 5,
    "username": "janedoe"
  },
  "content": "Hey, want to collaborate on a project?",
  "message_type": "text",
  "created_at": "2025-02-01T15:30:00Z",
  "is_read": false
}
```

---

### 2. Get Messages
**Endpoint**: `GET /messages/?page=1&receiver_id=5`

**Response** (Success - 200):
```json
{
  "count": 45,
  "next": "https://api.example.com/messages/?page=2",
  "previous": null,
  "results": [
    {
      "id": 1023,
      "sender": {"id": 1, "username": "johndoe"},
      "receiver": {"id": 5, "username": "janedoe"},
      "content": "Hey, want to collaborate?",
      "created_at": "2025-02-01T15:30:00Z",
      "is_read": false,
      "read_by_count": 0
    }
  ]
}
```

---

### 3. Mark Message as Read
**Endpoint**: `POST /messages/<message_id>/status/`

**Request**:
```json
{
  "status": "read"
}
```

**Response** (Success - 200):
```json
{
  "message_id": 1023,
  "status": "read",
  "read_at": "2025-02-01T15:35:00Z",
  "read_by_count": 1
}
```

---

### 4. Add Reaction to Message
**Endpoint**: `POST /messages/<message_id>/reactions/`

**Request**:
```json
{
  "reaction": "👍"
}
```

**Response** (Success - 201):
```json
{
  "message_id": 1023,
  "reaction": "👍",
  "user": {"id": 1, "username": "johndoe"},
  "created_at": "2025-02-01T15:35:00Z",
  "reaction_count": 3
}
```

---

### 5. Create Group Chat
**Endpoint**: `POST /chat-rooms/`

**Request**:
```json
{
  "name": "Project Team",
  "chat_type": "group",
  "description": "Chat for AI Chat Application project",
  "members": [1, 5, 8]
}
```

**Response** (Success - 201):
```json
{
  "id": 7,
  "name": "Project Team",
  "chat_type": "group",
  "description": "Chat for AI Chat Application project",
  "created_at": "2025-02-01T16:00:00Z",
  "members_count": 3,
  "members": [
    {"id": 1, "username": "johndoe"},
    {"id": 5, "username": "janedoe"},
    {"id": 8, "username": "alicejones"}
  ]
}
```

---

### 6. Get Conversations List
**Endpoint**: `GET /conversations/`

**Response** (Success - 200):
```json
{
  "count": 8,
  "results": [
    {
      "id": 7,
      "name": "Project Team",
      "type": "group",
      "last_message": "Sounds good! Let's start coding.",
      "last_message_time": "2025-02-01T16:15:00Z",
      "unread_count": 0,
      "members_count": 3
    }
  ]
}
```

---

## Social APIs

### 1. Send Connection Request
**Endpoint**: `POST /connect/<user_id>/`

**Request**:
```json
{
  "message": "Let's collaborate on AI projects!"
}
```

**Response** (Success - 201):
```json
{
  "connection_id": 42,
  "status": "pending",
  "target_user": {
    "id": 5,
    "username": "janedoe"
  },
  "message": "Connection request sent!",
  "created_at": "2025-02-01T16:30:00Z"
}
```

---

### 2. Accept Connection
**Endpoint**: `POST /accept-connection/<connection_id>/`

**Response** (Success - 200):
```json
{
  "connection_id": 42,
  "status": "accepted",
  "message": "Connection accepted!",
  "accepted_at": "2025-02-01T16:35:00Z"
}
```

---

### 3. Get My Connections
**Endpoint**: `GET /my-connections/?status=accepted&page=1`

**Response** (Success - 200):
```json
{
  "count": 12,
  "results": [
    {
      "id": 5,
      "username": "janedoe",
      "full_name": "Jane Doe",
      "profile_photo": "https://cdn.example.com/photos/janedoe.jpg",
      "college": "Stanford",
      "status": "accepted",
      "connected_at": "2025-02-01T16:35:00Z"
    }
  ]
}
```

---

### 4. Follow User
**Endpoint**: `POST /follow/<user_id>/`

**Response** (Success - 200):
```json
{
  "user_id": 5,
  "status": "following",
  "followers_count": 46,
  "message": "You are now following janedoe"
}
```

---

### 5. Get Activity Feed
**Endpoint**: `GET /activity-feed/?page=1`

**Response** (Success - 200):
```json
{
  "count": 34,
  "results": [
    {
      "id": 203,
      "user": {"id": 5, "username": "janedoe"},
      "activity_type": "project_created",
      "title": "janedoe created a new project",
      "description": "AI Chat Application",
      "related_project": {
        "id": 42,
        "title": "AI Chat Application"
      },
      "created_at": "2025-02-01T16:40:00Z",
      "is_public": true
    }
  ]
}
```

---

### 6. Get Notifications
**Endpoint**: `GET /notifications/?unread=true`

**Response** (Success - 200):
```json
{
  "count": 3,
  "unread_count": 3,
  "results": [
    {
      "id": 15,
      "title": "New Connection Request",
      "description": "Alice Jones sent you a connection request",
      "related_user": {"id": 8, "username": "alicejones"},
      "is_read": false,
      "created_at": "2025-02-01T17:00:00Z"
    }
  ]
}
```

---

### 7. Find Collaborators
**Endpoint**: `GET /find-collaborators/?skills=Python,React&college=MIT`

**Response** (Success - 200):
```json
{
  "count": 8,
  "results": [
    {
      "id": 5,
      "username": "janedoe",
      "full_name": "Jane Doe",
      "college": "MIT",
      "skills": ["Python", "React", "JavaScript"],
      "project_interests": ["Web Development", "AI/ML"],
      "match_score": 0.92,
      "profile_photo": "https://cdn.example.com/photos/janedoe.jpg"
    }
  ]
}
```

---

## Error Responses

### 400 Bad Request
```json
{
  "error": "Bad Request",
  "message": "Invalid input parameters",
  "details": {
    "email": ["Invalid email format"]
  }
}
```

---

### 401 Unauthorized
```json
{
  "error": "Unauthorized",
  "message": "Authentication required",
  "redirect": "/login/"
}
```

---

### 403 Forbidden
```json
{
  "error": "Forbidden",
  "message": "You don't have permission to perform this action"
}
```

---

### 404 Not Found
```json
{
  "error": "Not Found",
  "message": "The requested resource was not found"
}
```

---

### 429 Too Many Requests
```json
{
  "error": "Rate Limited",
  "message": "Too many requests. Please try again later.",
  "retry_after": 60
}
```

---

### 500 Server Error
```json
{
  "error": "Internal Server Error",
  "message": "An unexpected error occurred",
  "request_id": "abc123xyz"
}
```

---

## Headers

### Common Request Headers
```
Content-Type: application/json
Authorization: Bearer {token}
Accept: application/json
User-Agent: MyApp/1.0
```

### Common Response Headers
```
Content-Type: application/json
Content-Length: 1234
Date: Mon, 02 Feb 2025 14:20:00 GMT
X-RateLimit-Limit: 1000
X-RateLimit-Remaining: 999
X-RateLimit-Reset: 1738520400
Cache-Control: no-cache
ETag: "abc123"
```

---

## Pagination

### Paginated Response Format
```json
{
  "count": 127,
  "next": "https://api.example.com/endpoint/?page=2",
  "previous": null,
  "page_size": 10,
  "total_pages": 13,
  "current_page": 1,
  "results": [...]
}
```

### Pagination Parameters
```
?page=1           - Get specific page
?page_size=20     - Custom page size (max 100)
?ordering=-created_at  - Sort results
?search=query     - Search results
```

---

**Last Updated**: February 02, 2025  
**API Version**: v1.0  
**Status**: Production Ready
