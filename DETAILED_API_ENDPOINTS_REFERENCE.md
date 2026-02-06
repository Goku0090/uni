# Detailed API Endpoints Reference - UniSync

## Authentication Endpoints

### 1. Register User
```
POST /register/
Content-Type: application/x-www-form-urlencoded

Parameters:
- email (required): User email
- password (required): Password (min 8 chars)
- password_confirm (required): Password confirmation

Response: 
- 201: User created, redirect to login
- 400: Validation error (email exists, password mismatch)
- 500: Server error

Location: accounts/views.py, RegisterForm
```

### 2. Login (Email OTP)
```
POST /login/
Content-Type: application/x-www-form-urlencoded

Parameters:
- email (required): User email
- send_otp (optional): If present, send OTP
- username (alternative): Username instead of email

Response:
- 200: OTP sent (if send_otp=true)
- 200: Login form rendered
- 302: Redirect to dashboard if already authenticated
- 400: User not found or validation error

Location: accounts/views.py, LoginForm
```

### 3. Verify OTP
```
POST /verify-otp/
Content-Type: application/x-www-form-urlencoded

Parameters:
- otp_code (required): 6-digit OTP code
- email (required): User email

Response:
- 302: Redirect to dashboard (success)
- 200: Error message, re-render OTP form
- 400: Invalid or expired OTP
- 404: User not found

Location: accounts/views.py, OTPVerificationForm
```

### 4. Logout
```
GET /logout/

Response:
- 302: Redirect to login page
- Session cleared

Location: accounts/views.py
```

---

## User Profile Endpoints

### 5. View Own Profile
```
GET /profile/
Requires: Authentication

Response:
- 200: Render profile template with user data
- Data includes:
  - full_name, college, location
  - interests, skills, bio
  - profile_photo, social links
  - projects, connections count
  - activity timeline

Location: accounts/views.py, student_profile()
```

### 6. Edit Profile
```
GET /profile/edit/
POST /profile/edit/

Requires: Authentication
Content-Type: multipart/form-data

Parameters (POST):
- full_name: User's full name
- college: College name
- location: Location
- interests: JSON array of interests
- skills: JSON array of skills
- bio: User biography
- profile_photo: Image file (jpg, jpeg, png, gif)
- github: GitHub URL
- linkedin: LinkedIn URL
- portfolio: Portfolio URL
- behance: Behance URL

Response:
- 200: Form rendered (GET)
- 302: Redirect to profile view (POST, success)
- 200: Re-render form with errors (POST, validation error)

Validation:
- File extension validation (jpg, jpeg, png, gif)
- Field length limits
- URL format validation

Location: accounts/views.py, edit_profile()
```

### 7. View Other User Profile
```
GET /profile/<username>/
GET /user/<user_id>/

Requires: Authentication (optional for public profiles)

URL Parameters:
- username: Other user's username
- user_id: User's database ID

Response:
- 200: Render other user's profile
- 404: User not found
- Data includes:
  - Basic profile info
  - Projects
  - Connections/followers
  - Activity feed

Location: accounts/views.py, view_other_profile()
```

### 8. User Profile API (JSON)
```
GET /api/users/<user_id>/
GET /api/user-profile/

Requires: Authentication

Query Parameters:
- format: json (optional)

Response (JSON):
{
  "id": 1,
  "username": "john_doe",
  "email": "john@example.com",
  "full_name": "John Doe",
  "college": "MIT",
  "location": "Boston",
  "bio": "Full-stack developer",
  "interests": ["web", "AI"],
  "skills": ["Python", "Django"],
  "profile_photo": "/media/profile_photos/...",
  "github": "https://github.com/...",
  "linkedin": "https://linkedin.com/...",
  "connections_count": 42,
  "projects_count": 5,
  "profile_completed": true,
  "created_at": "2025-01-15T10:30:00Z"
}

Status Codes:
- 200: Success
- 404: User not found
- 401: Unauthorized

Location: accounts/serializers.py, UserProfileSerializer
```

---

## Project Endpoints

### 9. Create Project
```
GET /projects/create/
POST /projects/create/

Requires: Authentication
Content-Type: application/x-www-form-urlencoded (POST)

Parameters (POST):
- title (required): Project title
- description (required): Project description
- category: Project category (web, mobile, AI, etc.)
- visibility: public or private
- collaboration_needs: JSON array (roles needed)
- skills_required: JSON array (skills needed)
- project_type: collaborative, research, internship
- status: planning, active, completed

Response:
- 200: Form rendered (GET)
- 302: Redirect to project detail (POST, success)
- 200: Re-render form with errors (POST, error)

Validation:
- Title length (5-200 chars)
- Description length (10-5000 chars)
- Category must be valid choice
- Visibility must be public/private

Location: accounts/views.py, create_project(), ProjectForm
```

### 10. View Project Detail
```
GET /projects/<project_id>/

Requires: Authentication (or public access if public project)

URL Parameters:
- project_id: Project database ID

Response:
- 200: Render project detail template
- 404: Project not found or access denied
- Data includes:
  - Project info (title, description, owner)
  - Team members
  - Comments
  - Tasks & milestones
  - Files
  - Activity log
  - Like count, comment count
  - Related projects

Location: accounts/views.py, project_detail()
```

### 11. Project Feed / List
```
GET /projects/
GET /projects/feed/

Requires: Authentication

Query Parameters:
- page: Page number (default: 1)
- search: Search query
- category: Filter by category
- sort: latest, popular, trending
- visibility: Filter by visibility

Response:
- 200: Render projects page with paginated list
- Data includes:
  - Project cards (title, owner, image)
  - Pagination info
  - Filter options
  - Sorting options

Pagination:
- 10 projects per page (configurable)
- Total count and page info in template context

Location: accounts/views.py, project_feed()
```

### 12. Search Projects
```
GET /projects/search/

Requires: Authentication

Query Parameters:
- q (required): Search query
- category: Filter by category
- college: Filter by college
- sort: latest, popular

Response:
- 200: Render search results
- Data includes:
  - Matching projects
  - Result count
  - Filter options

Search Fields:
- Project title
- Project description
- Collaboration needs

Location: accounts/views.py, search_projects()
```

### 13. Edit Project
```
GET /projects/<project_id>/edit/
POST /projects/<project_id>/edit/

Requires: Authentication (owner only)

Parameters (POST):
- title: Project title
- description: Project description
- category: Category
- visibility: public/private
- collaboration_needs: JSON array
- skills_required: JSON array
- status: planning, active, completed

Response:
- 200: Form rendered (GET)
- 302: Redirect to project detail (POST, success)
- 403: Forbidden (not owner)
- 404: Project not found

Location: accounts/views.py, edit_project()
```

### 14. Delete Project
```
POST /projects/<project_id>/delete/
DELETE /api/projects/<project_id>/

Requires: Authentication (owner only)

Response:
- 302: Redirect to projects feed (success)
- 403: Forbidden (not owner)
- 404: Project not found
- 204: No content (DELETE method)

Location: accounts/views.py, delete_project()
```

### 15. Add Collaborator
```
POST /projects/<project_id>/add-collaborator/
POST /api/projects/<project_id>/members/

Requires: Authentication (owner only)

Parameters:
- user_id (required): User to add
- role: member, developer, designer, manager

Response:
- 200: Collaborator added (JSON)
- 302: Redirect to project detail
- 403: Forbidden (not owner)
- 404: Project or user not found
- 400: User already member

JSON Response:
{
  "success": true,
  "message": "Collaborator added",
  "member": {
    "id": 1,
    "username": "jane_doe",
    "role": "developer"
  }
}

Location: accounts/views.py, add_collaborator()
```

### 16. Remove Collaborator
```
POST /projects/<project_id>/remove-collaborator/<user_id>/
DELETE /api/projects/<project_id>/members/<user_id>/

Requires: Authentication (owner only)

Response:
- 200: Collaborator removed (JSON)
- 302: Redirect to project detail
- 403: Forbidden (not owner)
- 404: Project, user, or membership not found

Location: accounts/views.py, remove_collaborator()
```

---

## Collaboration & Networking Endpoints

### 17. Find Collaborators
```
GET /collaborators/find/
GET /api/collaborators/find/

Requires: Authentication

Query Parameters:
- skills: Comma-separated skills to filter
- interests: Comma-separated interests
- college: College filter
- search: Name/username search
- sort: match_score, recent, connections
- page: Page number

Response:
- 200: Render find collaborators page
- Data includes:
  - Potential collaborators (sorted by match score)
  - Filter options
  - Profile preview cards
  - Connect/Message buttons

Match Score Algorithm:
- Skill overlap: 40%
- Interest overlap: 30%
- College match: 20%
- Connection path: 10%

Location: accounts/views.py, find_collaborators(), StudentProfileNLP
```

### 18. Connect With User
```
POST /connect/<user_id>/
POST /api/users/<user_id>/connect/

Requires: Authentication

Response:
- 200: Connection created (JSON)
- 302: Redirect to referrer
- 400: Already connected
- 404: User not found

JSON Response:
{
  "success": true,
  "message": "Connected with user",
  "is_following": true
}

Location: accounts/views.py, connect_user(), Connection model
```

### 19. Disconnect From User
```
POST /disconnect/<user_id>/
DELETE /api/users/<user_id>/disconnect/

Requires: Authentication

Response:
- 200: Connection removed (JSON)
- 302: Redirect to referrer
- 404: Connection not found

Location: accounts/views.py, disconnect_user()
```

### 20. Get User Connections
```
GET /connections/
GET /api/users/<user_id>/connections/

Requires: Authentication

Query Parameters:
- user_id: User to fetch connections for (optional, default: current user)
- page: Page number
- search: Search connections

Response:
- 200: Render connections page or JSON list
- Data includes:
  - List of connected users
  - Profile cards
  - Mutual connections count

JSON Response:
{
  "count": 42,
  "next": "/api/users/1/connections/?page=2",
  "results": [
    {
      "id": 2,
      "username": "jane_doe",
      "full_name": "Jane Doe",
      "profile_photo": "/media/profile_photos/...",
      "mutual_connections": 5
    }
  ]
}

Location: accounts/views.py, get_connections()
```

---

## Messaging Endpoints

### 21. Send Message
```
POST /messages/send/
POST /api/messages/

Requires: Authentication
Content-Type: application/json or form-data

Parameters:
- to_user (required): Recipient user ID
- content (required): Message text
- files (optional): File attachments (multipart)

Response:
- 201: Message sent (JSON)
- 400: Validation error (missing required fields)
- 404: Recipient not found

JSON Response:
{
  "id": 123,
  "from_user": {
    "id": 1,
    "username": "john_doe"
  },
  "to_user": {
    "id": 2,
    "username": "jane_doe"
  },
  "content": "Hello!",
  "created_at": "2025-01-15T10:30:00Z",
  "read_at": null,
  "files": []
}

Location: accounts/views.py, send_message(), chat_api.py
```

### 22. View Messages
```
GET /messages/
GET /messages/<user_id>/
GET /api/messages/

Requires: Authentication

Query Parameters:
- user_id: Conversation with this user
- page: Page number

Response:
- 200: Render messages page or JSON list
- Data includes:
  - Message threads (list of conversations)
  - Recent messages
  - Unread count
  - Recipient info

JSON Response:
{
  "conversations": [
    {
      "user": {"id": 2, "username": "jane_doe"},
      "last_message": "See you tomorrow!",
      "last_message_time": "2025-01-15T10:30:00Z",
      "unread_count": 3
    }
  ]
}

Location: accounts/views.py, view_messages(), chat_api.py
```

### 23. Mark Message Read
```
POST /messages/<message_id>/mark-read/
POST /api/messages/<message_id>/read/

Requires: Authentication

Response:
- 200: Message marked as read (JSON)
- 404: Message not found

Location: accounts/views.py, MessageReadStatus model
```

---

## Comments Endpoints

### 24. Post Comment
```
POST /projects/<project_id>/comments/
POST /api/projects/<project_id>/comments/

Requires: Authentication
Content-Type: application/json or form-data

Parameters:
- text (required): Comment content
- parent_id (optional): Reply to comment ID

Response:
- 201: Comment created (JSON)
- 400: Validation error
- 404: Project not found

JSON Response:
{
  "id": 456,
  "project": 10,
  "user": {"id": 1, "username": "john_doe"},
  "text": "Great idea!",
  "created_at": "2025-01-15T10:30:00Z",
  "updated_at": "2025-01-15T10:30:00Z",
  "replies": [],
  "reply_count": 0
}

Location: accounts/views.py, post_comment(), comment_api.py
```

### 25. Edit Comment
```
PUT /comments/<comment_id>/
POST /api/comments/<comment_id>/edit/

Requires: Authentication (author only)

Parameters:
- text (required): Updated comment text

Response:
- 200: Comment updated (JSON)
- 403: Forbidden (not author)
- 404: Comment not found

Location: accounts/views.py, edit_comment()
```

### 26. Delete Comment
```
DELETE /comments/<comment_id>/
POST /api/comments/<comment_id>/delete/

Requires: Authentication (author only)

Response:
- 204: Comment deleted (no content)
- 302: Redirect to project
- 403: Forbidden (not author)
- 404: Comment not found

Location: accounts/views.py, delete_comment()
```

---

## Like & Interaction Endpoints

### 27. Like Project
```
POST /projects/<project_id>/like/
POST /api/projects/<project_id>/like/

Requires: Authentication

Response:
- 200: Like created/updated (JSON)
- 404: Project not found

JSON Response:
{
  "success": true,
  "liked": true,
  "likes_count": 42
}

Location: accounts/views.py, like_project(), Like model
```

### 28. Unlike Project
```
DELETE /projects/<project_id>/like/
POST /api/projects/<project_id>/unlike/

Requires: Authentication

Response:
- 200: Like removed (JSON)
- 404: Project or like not found

Location: accounts/views.py, unlike_project()
```

---

## Notifications Endpoints

### 29. Get Notifications
```
GET /notifications/
GET /api/notifications/

Requires: Authentication

Query Parameters:
- page: Page number
- unread_only: true/false (default: false)
- type: message, like, comment, connection, all

Response:
- 200: Render notifications page or JSON list
- Data includes:
  - List of notifications
  - Unread count
  - Notification details

JSON Response:
{
  "count": 15,
  "unread_count": 3,
  "results": [
    {
      "id": 1,
      "type": "comment",
      "message": "Jane commented on your project",
      "related_object": {"id": 10, "title": "Web App"},
      "is_read": false,
      "created_at": "2025-01-15T10:30:00Z"
    }
  ]
}

Location: accounts/views.py, get_notifications(), Notification model
```

### 30. Mark Notification Read
```
POST /notifications/<notification_id>/mark-read/
POST /api/notifications/<notification_id>/read/

Requires: Authentication

Response:
- 200: Notification marked as read (JSON)
- 404: Notification not found

Location: accounts/views.py, mark_notification_read()
```

### 31. Mark All Notifications Read
```
POST /notifications/mark-all-read/
POST /api/notifications/mark-all-read/

Requires: Authentication

Response:
- 200: All notifications marked as read (JSON)

Location: accounts/views.py
```

---

## Contact & Support Endpoints

### 32. Contact Form
```
POST /contact/
GET /contact/

Requires: No authentication

Parameters (POST):
- name (required): Visitor name
- email (required): Visitor email
- subject (required): Message subject
- message (required): Message content

Response:
- 200: Form rendered (GET)
- 200: Success message and re-render form (POST)
- 400: Validation error

Location: accounts/views.py, views_contact.py
```

---

## Common Response Codes

| Code | Meaning | Common Causes |
|------|---------|---------------|
| 200 | OK | Request successful |
| 201 | Created | Resource created successfully |
| 204 | No Content | Successful deletion |
| 302 | Found | Redirect response |
| 400 | Bad Request | Missing/invalid parameters |
| 401 | Unauthorized | Not authenticated |
| 403 | Forbidden | Authenticated but not authorized |
| 404 | Not Found | Resource doesn't exist |
| 500 | Server Error | Unexpected server error |

---

## Authentication Headers

For API endpoints requiring authentication:

```
Authorization: Token YOUR_TOKEN_HERE
OR
(Cookie-based for traditional views)
```

For CSRF-protected POST requests:

```
X-CSRFToken: <csrf_token_value>
Cookie: csrftoken=<csrf_token_value>
```

---

## Rate Limiting

Currently: No rate limiting implemented
Recommendation: Implement rate limiting for production
- 100 requests/minute per user
- 1000 requests/hour per IP

---

## Error Response Format (JSON)

```json
{
  "error": "Error message",
  "code": "ERROR_CODE",
  "details": {
    "field_name": ["error detail 1", "error detail 2"]
  }
}
```

---

## File Upload Specifications

### Profile Photo
- **Field**: profile_photo
- **Allowed Types**: jpg, jpeg, png, gif
- **Max Size**: 5MB
- **Dimensions**: Recommended 400x400px or higher
- **Storage**: /media/profile_photos/
- **URL Access**: /media/profile_photos/{filename}

### Message Attachments
- **Field**: files
- **Allowed Types**: pdf, doc, docx, xls, xlsx, txt, zip
- **Max Size**: 10MB per file
- **Max Files**: 5 per message
- **Storage**: /media/message_files/

---

*Last Updated: February 6, 2026*
*API Version: 1.0*
*Status: Production*
