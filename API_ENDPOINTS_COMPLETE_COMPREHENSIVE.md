# UniSync API Endpoints - Complete Reference

## Overview
This document provides complete details on all API endpoints in UniSync, including authentication, messaging, profiles, projects, and networking.

---

## Authentication Endpoints

### 1. User Login
**POST** `/accounts/login/`

**Description**: Initiate login with email, sends OTP via email.

**Request Body**:
```json
{
  "email": "student@college.com"
}
```

**Response (200 OK)**:
```json
{
  "message": "OTP sent to your email",
  "purpose": "login"
}
```

**Related View**: `login_view()` (views.py L309+)

---

### 2. Register User
**POST** `/accounts/register/`

**Description**: Create new account, sends registration OTP.

**Request Body**:
```json
{
  "email": "student@college.com",
  "password": "strongpassword123"
}
```

**Response (201 Created)**:
```json
{
  "message": "Account created. OTP sent to email.",
  "purpose": "registration"
}
```

**Related View**: `register_view()` (views.py)

---

### 3. Verify OTP
**POST** `/accounts/verify-otp/<purpose>/`

**Description**: Verify OTP code sent to email. Accepts `login`, `registration`, or `reset`.

**Parameters**:
- `purpose` (path): One of `login`, `registration`, `reset`

**Request Body**:
```json
{
  "otp": "123456",
  "email": "student@college.com"
}
```

**Response (200 OK)**:
```json
{
  "message": "OTP verified successfully",
  "user_id": 42,
  "username": "studentname"
}
```

**Related View**: `verify_otp_view()` (views.py L400+)

---

### 4. Resend OTP
**POST** `/accounts/resend-otp/<purpose>/`

**Description**: Resend OTP to email if original expires.

**Parameters**:
- `purpose` (path): `login`, `registration`, or `reset`

**Request Body**:
```json
{
  "email": "student@college.com"
}
```

**Response (200 OK)**:
```json
{
  "message": "New OTP sent to your email"
}
```

---

### 5. Forgot Password
**POST** `/accounts/forgot-password/`

**Description**: Initiate password reset flow.

**Request Body**:
```json
{
  "email": "student@college.com"
}
```

**Response (200 OK)**:
```json
{
  "message": "Password reset OTP sent to email"
}
```

---

### 6. Reset Password
**POST** `/accounts/reset-password/`

**Description**: Set new password after OTP verification.

**Request Body**:
```json
{
  "email": "student@college.com",
  "new_password": "newstrongpass123",
  "otp": "123456"
}
```

**Response (200 OK)**:
```json
{
  "message": "Password reset successfully"
}
```

---

### 7. Logout
**POST** `/accounts/logout/`

**Description**: Clear session and logout user.

**Response (200 OK)**:
```json
{
  "message": "Logged out successfully"
}
```

**Related View**: `logout_view()` (views.py)

---

## User Profile Endpoints

### 8. Get User Profile (Self)
**GET** `/accounts/profile/`

**Description**: Get current logged-in user's profile.

**Headers**:
```
Authorization: Bearer <token>  (if using token auth)
```

**Response (200 OK)**:
```json
{
  "user_id": 42,
  "username": "studentname",
  "email": "student@college.com",
  "full_name": "Student Name",
  "college": "MIT",
  "location": "Boston, MA",
  "bio": "Passionate about web development",
  "interests": ["web-dev", "ai", "mobile-apps"],
  "skills": ["Python", "Django", "React", "PostgreSQL"],
  "project_interests": ["web-projects", "data-science"],
  "role_preference": "Full Stack Developer",
  "profile_photo": "https://cdn.example.com/profile_photos/42.jpg",
  "social_links": {
    "github": "https://github.com/studentname",
    "linkedin": "https://linkedin.com/in/studentname",
    "portfolio": "https://studentname.dev",
    "behance": "https://behance.net/studentname"
  },
  "profile_completed": true,
  "created_at": "2025-01-15T10:30:00Z",
  "updated_at": "2026-02-04T08:45:00Z"
}
```

**Related View**: `UserProfileView` (views.py) - REST API

---

### 9. Get Other User's Profile
**GET** `/accounts/user/<username>/`

**Description**: Get public profile of another user.

**Parameters**:
- `username` (path): Username of the profile to view

**Response (200 OK)**:
```json
{
  "user_id": 42,
  "username": "studentname",
  "full_name": "Student Name",
  "college": "MIT",
  "location": "Boston, MA",
  "bio": "Passionate about web development",
  "interests": ["web-dev", "ai", "mobile-apps"],
  "skills": ["Python", "Django", "React"],
  "profile_photo": "https://cdn.example.com/profile_photos/42.jpg",
  "social_links": {
    "github": "https://github.com/studentname",
    "linkedin": "https://linkedin.com/in/studentname"
  },
  "stats": {
    "projects_count": 5,
    "connections_count": 23,
    "followers_count": 18
  },
  "recent_projects": [
    {
      "id": 1,
      "title": "AI Chatbot",
      "description": "Build an intelligent chatbot"
    }
  ]
}
```

**Related View**: `user_profile()` (views.py)

---

### 10. Edit User Profile
**PUT/PATCH** `/accounts/student-profile/` or `/accounts/profile/`

**Description**: Update current user's profile information.

**Headers**:
```
Content-Type: application/json
Authorization: Bearer <token>
```

**Request Body**:
```json
{
  "full_name": "Updated Name",
  "college": "Stanford",
  "location": "San Francisco, CA",
  "bio": "Updated bio text",
  "interests": ["web-dev", "machine-learning"],
  "skills": ["Python", "TensorFlow"],
  "project_interests": ["research-projects"],
  "role_preference": "ML Engineer",
  "github": "https://github.com/updated",
  "linkedin": "https://linkedin.com/in/updated"
}
```

**Response (200 OK)**:
```json
{
  "message": "Profile updated successfully",
  "profile": { /* updated profile data */ }
}
```

**Related View**: `edit_profile()` (views.py L49-61)

---

### 11. Upload Profile Photo
**POST** `/accounts/profile/photo/`

**Description**: Upload or update profile picture.

**Headers**:
```
Content-Type: multipart/form-data
Authorization: Bearer <token>
```

**Form Data**:
```
profile_photo: <image_file>  (jpg, jpeg, png, gif)
```

**Response (200 OK)**:
```json
{
  "message": "Profile photo uploaded successfully",
  "photo_url": "https://cdn.example.com/profile_photos/42_new.jpg"
}
```

---

## Project Endpoints

### 12. Create Project
**POST** `/accounts/post-project/`

**Description**: Create new project for collaboration.

**Headers**:
```
Content-Type: application/json
Authorization: Bearer <token>
```

**Request Body**:
```json
{
  "title": "AI-Powered Recommendation Engine",
  "description": "Build an AI system for personalized recommendations",
  "collaboration_needs": ["Machine Learning Engineer", "Backend Developer"],
  "required_skills": ["Python", "TensorFlow", "FastAPI"],
  "timeline": "3 months",
  "visibility": "public"
}
```

**Response (201 Created)**:
```json
{
  "id": 127,
  "title": "AI-Powered Recommendation Engine",
  "owner_id": 42,
  "owner_name": "Student Name",
  "description": "Build an AI system for personalized recommendations",
  "collaboration_needs": ["Machine Learning Engineer", "Backend Developer"],
  "created_at": "2026-02-04T10:30:00Z",
  "likes_count": 0,
  "comments_count": 0
}
```

**Related View**: `post_project()` (views.py)

---

### 13. Get Project Details
**GET** `/accounts/project-detail/<project_id>/` or `/project/<project_id>/`

**Description**: Retrieve full project details including comments and team.

**Parameters**:
- `project_id` (path): ID of the project

**Response (200 OK)**:
```json
{
  "id": 127,
  "title": "AI-Powered Recommendation Engine",
  "owner_id": 42,
  "owner": {
    "username": "studentname",
    "full_name": "Student Name",
    "profile_photo": "https://cdn.example.com/profile_photos/42.jpg"
  },
  "description": "Build an AI system for personalized recommendations",
  "collaboration_needs": ["Machine Learning Engineer", "Backend Developer"],
  "required_skills": ["Python", "TensorFlow"],
  "timeline": "3 months",
  "visibility": "public",
  "created_at": "2026-02-04T10:30:00Z",
  "updated_at": "2026-02-04T10:30:00Z",
  "likes_count": 5,
  "comments_count": 3,
  "is_liked": false,
  "team_members": [
    {
      "user_id": 42,
      "username": "studentname",
      "role": "Project Owner"
    }
  ],
  "comments": [
    {
      "id": 1,
      "author": "collaborator",
      "text": "Interested in joining!",
      "created_at": "2026-02-04T11:00:00Z"
    }
  ]
}
```

**Related View**: `project_detail()` (views.py)

---

### 14. Edit Project
**PUT/PATCH** `/accounts/edit-project/<project_id>/`

**Description**: Update project details (owner only).

**Parameters**:
- `project_id` (path): ID of the project

**Request Body**:
```json
{
  "title": "Updated Title",
  "description": "Updated description",
  "collaboration_needs": ["Updated Needs"],
  "timeline": "4 months"
}
```

**Response (200 OK)**:
```json
{
  "message": "Project updated successfully",
  "project": { /* updated project data */ }
}
```

**Related View**: `edit_project()` (views.py)

---

### 15. Delete Project
**DELETE** `/accounts/delete-project/<project_id>/`

**Description**: Remove project (owner only).

**Parameters**:
- `project_id` (path): ID of the project

**Response (204 No Content)**:
```
No content returned
```

**Related View**: `delete_project()` (views.py)

---

### 16. Search Projects
**GET** `/accounts/search-projects/?q=query`

**Description**: Search projects by title, description, or requirements.

**Query Parameters**:
- `q` (required): Search query string
- `page` (optional): Page number for pagination (default: 1)

**Response (200 OK)**:
```json
{
  "count": 15,
  "next": "https://api.example.com/accounts/search-projects/?q=web&page=2",
  "previous": null,
  "results": [
    {
      "id": 127,
      "title": "Web Development Project",
      "description": "Build a modern web app",
      "owner": "studentname"
    }
  ]
}
```

**Related View**: `search_projects()` (views.py L64-74)

---

### 17. Like Project
**POST** `/accounts/like-project/<project_id>/`

**Description**: Like or unlike a project.

**Parameters**:
- `project_id` (path): ID of the project

**Response (200 OK)**:
```json
{
  "message": "Project liked successfully",
  "likes_count": 6,
  "is_liked": true
}
```

**Related View**: `like_project()` (views.py)

---

### 18. Get My Projects
**GET** `/accounts/my-projects/`

**Description**: List current user's own projects.

**Query Parameters**:
- `page` (optional): Page number for pagination

**Response (200 OK)**:
```json
{
  "count": 3,
  "results": [
    {
      "id": 127,
      "title": "AI-Powered Recommendation Engine",
      "description": "Build an AI system...",
      "likes_count": 5,
      "created_at": "2026-02-04T10:30:00Z"
    }
  ]
}
```

**Related View**: `my_projects_view()` (views.py)

---

### 19. Explore All Projects
**GET** `/accounts/explore-projects/`

**Description**: Browse all public projects with filtering.

**Query Parameters**:
- `page` (optional): Page number
- `skill` (optional): Filter by required skill
- `college` (optional): Filter by collaborator's college

**Response (200 OK)**:
```json
{
  "count": 45,
  "results": [ /* array of project objects */ ]
}
```

**Related View**: `explore_projects_view()` (views.py)

---

## Messaging & Chat Endpoints

### 20. List All Chat Rooms
**GET** `/api/chat-rooms/`

**Description**: Get all chat rooms (DMs + groups) for current user.

**Query Parameters**:
- `page` (optional): Page number
- `search` (optional): Search by room name or username

**Response (200 OK)**:
```json
{
  "count": 5,
  "results": [
    {
      "id": 1,
      "name": "John Doe",
      "is_private": true,
      "is_group": false,
      "members": [42, 50],
      "created_at": "2026-01-20T14:30:00Z",
      "last_message": {
        "text": "Hey, how's the project going?",
        "sent_at": "2026-02-04T09:15:00Z"
      }
    }
  ]
}
```

**Related View**: `ChatRoomListCreateView` (chat_api.py)

---

### 21. Create Chat Room or DM
**POST** `/api/chat-rooms/`

**Description**: Create new group chat or initiate DM.

**Request Body** (Group):
```json
{
  "name": "Project Brainstorming",
  "is_group": true,
  "members": [42, 50, 51],
  "description": "Discussion for AI project"
}
```

**Request Body** (DM):
```json
{
  "name": null,
  "is_private": true,
  "is_group": false,
  "user_id": 50
}
```

**Response (201 Created)**:
```json
{
  "id": 2,
  "name": "Project Brainstorming",
  "is_private": false,
  "is_group": true,
  "members": [42, 50, 51],
  "created_by": 42,
  "created_at": "2026-02-04T10:00:00Z"
}
```

**Related View**: `ChatRoomListCreateView` (chat_api.py)

---

### 22. Get Chat Room Details
**GET** `/api/chat-rooms/<room_id>/`

**Description**: Get room details with member info.

**Parameters**:
- `room_id` (path): ID of the chat room

**Response (200 OK)**:
```json
{
  "id": 2,
  "name": "Project Brainstorming",
  "description": "Discussion for AI project",
  "is_group": true,
  "members_count": 3,
  "members": [
    {
      "id": 42,
      "username": "student1",
      "full_name": "Student One"
    }
  ],
  "created_by": {
    "id": 42,
    "username": "student1"
  },
  "created_at": "2026-02-04T10:00:00Z"
}
```

---

### 23. List Messages in Room
**GET** `/api/messages/?room_id=<room_id>`

**Description**: Get messages from a chat room with pagination.

**Query Parameters**:
- `room_id` (required): Chat room ID
- `page` (optional): Page number

**Response (200 OK)**:
```json
{
  "count": 15,
  "next": "https://api.example.com/api/messages/?room_id=2&page=2",
  "previous": null,
  "results": [
    {
      "id": 101,
      "room_id": 2,
      "sender": {
        "id": 42,
        "username": "student1"
      },
      "text": "Let's discuss the architecture",
      "created_at": "2026-02-03T15:00:00Z",
      "is_edited": false,
      "read_by": [42, 50],
      "reactions": [
        {
          "reaction": "👍",
          "count": 2,
          "users": [50, 51]
        }
      ]
    }
  ]
}
```

**Related View**: `MessageListCreateView` (chat_api.py)

---

### 24. Send Message
**POST** `/api/messages/`

**Description**: Send message to chat room.

**Request Body**:
```json
{
  "room_id": 2,
  "text": "Let's discuss the architecture",
  "file_ids": [1, 2]
}
```

**Response (201 Created)**:
```json
{
  "id": 101,
  "room_id": 2,
  "sender_id": 42,
  "text": "Let's discuss the architecture",
  "created_at": "2026-02-04T10:15:00Z",
  "is_edited": false,
  "files": [
    {
      "id": 1,
      "filename": "architecture.pdf"
    }
  ]
}
```

**Related View**: `MessageListCreateView` (chat_api.py)

---

### 25. Edit Message
**PATCH** `/api/messages/<message_id>/`

**Description**: Edit previously sent message.

**Parameters**:
- `message_id` (path): ID of the message

**Request Body**:
```json
{
  "text": "Updated message text"
}
```

**Response (200 OK)**:
```json
{
  "id": 101,
  "text": "Updated message text",
  "is_edited": true,
  "edited_at": "2026-02-04T10:20:00Z"
}
```

---

### 26. Delete Message
**DELETE** `/api/messages/<message_id>/`

**Description**: Delete a message.

**Parameters**:
- `message_id` (path): ID of the message

**Response (204 No Content)**:
```
No content returned
```

---

### 27. Search Messages
**GET** `/api/messages/search/?q=query&room_id=<room_id>`

**Description**: Search messages in a chat room.

**Query Parameters**:
- `q` (required): Search text
- `room_id` (optional): Limit to specific room
- `from_user` (optional): Filter by sender username

**Response (200 OK)**:
```json
{
  "count": 3,
  "results": [
    {
      "id": 101,
      "text": "Let's discuss the architecture",
      "room_id": 2,
      "sender": "student1",
      "created_at": "2026-02-03T15:00:00Z"
    }
  ]
}
```

---

### 28. Get Message Read Status
**GET** `/api/messages/<message_id>/status/`

**Description**: See who has read the message.

**Parameters**:
- `message_id` (path): ID of the message

**Response (200 OK)**:
```json
{
  "message_id": 101,
  "read_by": [
    {
      "user_id": 42,
      "username": "student1",
      "read_at": "2026-02-03T15:02:00Z"
    },
    {
      "user_id": 50,
      "username": "student2",
      "read_at": "2026-02-03T15:05:00Z"
    }
  ],
  "unread_by": [
    {
      "user_id": 51,
      "username": "student3"
    }
  ]
}
```

---

### 29. Add Reaction to Message
**POST** `/api/messages/<message_id>/reactions/`

**Description**: Add emoji reaction to message.

**Parameters**:
- `message_id` (path): ID of the message

**Request Body**:
```json
{
  "reaction": "👍"
}
```

**Response (200 OK)**:
```json
{
  "message_id": 101,
  "reaction": "👍",
  "reactions_summary": [
    {
      "reaction": "👍",
      "count": 2,
      "users": ["student1", "student2"]
    }
  ]
}
```

---

### 30. Send Typing Indicator
**POST** `/api/typing/`

**Description**: Notify others that user is typing.

**Request Body**:
```json
{
  "room_id": 2,
  "is_typing": true
}
```

**Response (200 OK)**:
```json
{
  "message": "Typing indicator sent"
}
```

---

### 31. Get Draft Messages
**GET** `/api/drafts/`

**Description**: Get all draft messages (unsent).

**Response (200 OK)**:
```json
{
  "count": 2,
  "results": [
    {
      "id": 1,
      "room_id": 2,
      "text": "Draft message content...",
      "created_at": "2026-02-04T09:30:00Z"
    }
  ]
}
```

---

## Networking & Collaboration Endpoints

### 32. Find Collaborators
**GET** `/accounts/find-collaborators/?college=MIT&skill=Python`

**Description**: Find matching collaborators based on filters.

**Query Parameters**:
- `college` (optional): Filter by college
- `skill` (optional): Filter by skill
- `interest` (optional): Filter by interest
- `role` (optional): Filter by role preference

**Response (200 OK)**:
```json
{
  "count": 8,
  "results": [
    {
      "user_id": 45,
      "username": "collaborator1",
      "full_name": "Collaborator Name",
      "college": "MIT",
      "interests": ["web-dev", "ai"],
      "skills": ["Python", "React"],
      "role_preference": "Full Stack Developer",
      "profile_photo": "https://...",
      "bio": "Looking for web projects",
      "match_score": 0.92
    }
  ]
}
```

**Related View**: `find_collaborators()` (views.py L1398+)

---

### 33. Send Connection Request
**POST** `/accounts/connect/<user_id>/` or `/accounts/send-connection/<user_id>/`

**Description**: Send connection request to another user.

**Parameters**:
- `user_id` (path): ID of user to connect with

**Response (201 Created)**:
```json
{
  "message": "Connection request sent",
  "connection_id": 5,
  "status": "pending"
}
```

**Related View**: `send_connection_request()` (views.py)

---

### 34. Accept Connection
**POST** `/accounts/accept-connection/<connection_id>/`

**Description**: Accept pending connection request.

**Parameters**:
- `connection_id` (path): ID of the connection

**Response (200 OK)**:
```json
{
  "message": "Connection accepted",
  "connection_id": 5,
  "status": "accepted",
  "connected_user": {
    "user_id": 45,
    "username": "collaborator1",
    "full_name": "Collaborator Name"
  }
}
```

**Related View**: `accept_connection()` (views.py)

---

### 35. Reject Connection
**POST** `/accounts/reject-connection/<connection_id>/`

**Description**: Reject connection request.

**Parameters**:
- `connection_id` (path): ID of the connection

**Response (200 OK)**:
```json
{
  "message": "Connection rejected",
  "connection_id": 5
}
```

**Related View**: `reject_connection()` (views.py)

---

### 36. View My Connections
**GET** `/accounts/my-connections/`

**Description**: List all user's accepted connections.

**Query Parameters**:
- `status` (optional): Filter by "pending", "accepted", or "rejected"
- `page` (optional): Page number

**Response (200 OK)**:
```json
{
  "count": 23,
  "results": [
    {
      "connection_id": 5,
      "user": {
        "user_id": 45,
        "username": "collaborator1",
        "full_name": "Collaborator Name",
        "college": "MIT"
      },
      "status": "accepted",
      "connected_at": "2026-01-20T10:00:00Z"
    }
  ]
}
```

**Related View**: `my_connections()` (views.py)

---

### 37. Follow User
**POST** `/accounts/follow/<user_id>/`

**Description**: Follow another user to see their activity.

**Parameters**:
- `user_id` (path): ID of user to follow

**Response (200 OK)**:
```json
{
  "message": "User followed",
  "is_following": true
}
```

---

## Comments Endpoints

### 38. Add Comment to Project
**POST** `/api/comments/`

**Description**: Add comment to a project.

**Request Body**:
```json
{
  "project_id": 127,
  "text": "I'm very interested in this project!"
}
```

**Response (201 Created)**:
```json
{
  "id": 1,
  "project_id": 127,
  "author": {
    "user_id": 42,
    "username": "student1",
    "profile_photo": "https://..."
  },
  "text": "I'm very interested in this project!",
  "created_at": "2026-02-04T10:30:00Z",
  "likes_count": 0
}
```

**Related View**: `add_comment()` (comment_api.py)

---

### 39. Get Project Comments
**GET** `/api/comments/<project_id>/`

**Description**: Get all comments on a project.

**Parameters**:
- `project_id` (path): ID of the project

**Query Parameters**:
- `page` (optional): Page number
- `sort` (optional): "newest", "oldest", or "popular"

**Response (200 OK)**:
```json
{
  "count": 5,
  "results": [
    {
      "id": 1,
      "author": "student1",
      "text": "Interested in joining!",
      "created_at": "2026-02-04T10:30:00Z",
      "likes_count": 2
    }
  ]
}
```

**Related View**: `get_comments()` (comment_api.py)

---

### 40. Edit Comment
**PUT/PATCH** `/api/comments/<comment_id>/`

**Description**: Edit own comment.

**Parameters**:
- `comment_id` (path): ID of the comment

**Request Body**:
```json
{
  "text": "Updated comment text"
}
```

**Response (200 OK)**:
```json
{
  "id": 1,
  "text": "Updated comment text",
  "is_edited": true,
  "edited_at": "2026-02-04T10:35:00Z"
}
```

**Related View**: `edit_comment()` (comment_api.py)

---

### 41. Delete Comment
**DELETE** `/api/comments/<comment_id>/`

**Description**: Delete own comment.

**Parameters**:
- `comment_id` (path): ID of the comment

**Response (204 No Content)**:
```
No content returned
```

**Related View**: `delete_comment()` (comment_api.py)

---

## Notification Endpoints

### 42. Get Notifications
**GET** `/accounts/notifications/`

**Description**: Get user's notification list.

**Query Parameters**:
- `page` (optional): Page number
- `unread_only` (optional): Boolean to filter unread only

**Response (200 OK)**:
```json
{
  "count": 12,
  "unread_count": 3,
  "results": [
    {
      "id": 1,
      "type": "connection_request",
      "actor": {
        "user_id": 45,
        "username": "collaborator1"
      },
      "action": "sent you a connection request",
      "is_read": false,
      "created_at": "2026-02-04T09:00:00Z",
      "link": "/accounts/accept-connection/5/"
    },
    {
      "id": 2,
      "type": "comment",
      "actor": {
        "user_id": 48,
        "username": "another_user"
      },
      "action": "commented on your project",
      "is_read": false,
      "created_at": "2026-02-04T10:15:00Z",
      "link": "/accounts/project-detail/127/#comment-3"
    }
  ]
}
```

**Related View**: `notifications_view()` (views.py)

---

### 43. Mark Notification as Read
**POST** `/accounts/mark-notification-read/<notification_id>/`

**Description**: Mark individual notification as read.

**Parameters**:
- `notification_id` (path): ID of the notification

**Response (200 OK)**:
```json
{
  "message": "Notification marked as read"
}
```

**Related View**: `mark_notification_read()` (views.py)

---

## Activity Feed Endpoints

### 44. Get Activity Feed
**GET** `/accounts/activity-feed/`

**Description**: Get timeline of activities from followed users.

**Query Parameters**:
- `page` (optional): Page number

**Response (200 OK)**:
```json
{
  "count": 20,
  "results": [
    {
      "id": 1,
      "user": {
        "user_id": 45,
        "username": "collaborator1"
      },
      "action": "posted a new project",
      "content": "AI Recommendation Engine",
      "timestamp": "2026-02-04T08:00:00Z",
      "type": "project_posted"
    },
    {
      "id": 2,
      "user": {
        "user_id": 48,
        "username": "another_user"
      },
      "action": "connected with",
      "content": "colleague_name",
      "timestamp": "2026-02-04T09:15:00Z",
      "type": "connection_made"
    }
  ]
}
```

**Related View**: `activity_feed()` (views.py)

---

## Team Management Endpoints

### 45. Invite User to Project Team
**POST** `/accounts/invite-to-team/<project_id>/`

**Description**: Send team invitation for project.

**Parameters**:
- `project_id` (path): ID of the project

**Request Body**:
```json
{
  "user_id": 45,
  "role": "Backend Developer"
}
```

**Response (201 Created)**:
```json
{
  "message": "Invitation sent",
  "invitation_id": 8
}
```

---

### 46. Respond to Team Invitation
**POST** `/accounts/respond-team-invitation/<invitation_id>/`

**Description**: Accept or reject team invitation.

**Parameters**:
- `invitation_id` (path): ID of the invitation

**Request Body**:
```json
{
  "action": "accept"
}
```

**Response (200 OK)**:
```json
{
  "message": "Invitation accepted",
  "project_id": 127
}
```

---

### 47. Remove Team Member
**DELETE** `/accounts/remove-team-member/<project_id>/<user_id>/`

**Description**: Remove member from project team (owner only).

**Parameters**:
- `project_id` (path): ID of the project
- `user_id` (path): ID of the user to remove

**Response (204 No Content)**:
```
No content returned
```

---

## Response Status Codes

| Code | Meaning | Example |
|------|---------|---------|
| 200 | OK | Successfully retrieved or updated |
| 201 | Created | New resource created |
| 204 | No Content | Successful deletion |
| 400 | Bad Request | Invalid input parameters |
| 401 | Unauthorized | Missing authentication |
| 403 | Forbidden | Permission denied |
| 404 | Not Found | Resource doesn't exist |
| 500 | Server Error | Internal server error |

---

## Error Response Format

All error responses follow this format:

```json
{
  "error": "Error type",
  "detail": "Detailed error message",
  "status_code": 400
}
```

---

## Authentication

Most endpoints require authentication. Methods include:

1. **Session Authentication** (logged-in users)
   - Automatically set after login
   - Valid for duration of session

2. **Token Authentication** (optional, for mobile apps)
   - Header: `Authorization: Bearer <token>`
   - Obtain token after OTP verification

3. **Social Auth** (Google, GitHub)
   - Handles via django-allauth
   - OAuth token included in response

---

## Rate Limiting

Current rate limits (if implemented):
- 100 requests per minute for authenticated users
- 20 requests per minute for unauthenticated users

---

## Pagination

Paginated endpoints return:
```json
{
  "count": 45,
  "next": "https://api.example.com/api/endpoint/?page=2",
  "previous": null,
  "results": [ /* items */ ]
}
```

Default page size: 10 items
Query param: `?page=2` for specific page

---

## Conclusion

This comprehensive API reference covers all endpoints in UniSync, from authentication through real-time messaging and project collaboration. Each endpoint includes:

- HTTP method and path
- Description
- Request/response examples
- Related view implementation
- Query parameters and path parameters

For more details on implementation, refer to the model definitions and view code.
