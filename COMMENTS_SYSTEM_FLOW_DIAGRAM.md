# Comments System - Flow Diagrams

## Complete Comments System Architecture

```
┌─────────────────────────────────────────────────────────────────────┐
│                          WEB BROWSER                                 │
├─────────────────────────────────────────────────────────────────────┤
│                                                                       │
│  ┌──────────────────────────────────────────────────────────────┐   │
│  │  project_detail.html                                         │   │
│  ├──────────────────────────────────────────────────────────────┤   │
│  │  - Project title, description, tags, etc.                    │   │
│  │                                                              │   │
│  │  {% include 'includes/comment_section.html' %}              │   │
│  │           ↓                                                  │   │
│  │  ┌────────────────────────────────────────────────────────┐ │   │
│  │  │  comment_section.html                                 │ │   │
│  │  ├────────────────────────────────────────────────────────┤ │   │
│  │  │  Comment Form                                          │ │   │
│  │  │  [Textarea] [Post Button]                              │ │   │
│  │  │                                                         │ │   │
│  │  │  Comments List                                         │ │   │
│  │  │  [Comment 1] [Comment 2] [Comment 3]                   │ │   │
│  │  │                                                         │ │   │
│  │  │  JavaScript Handlers:                                  │ │   │
│  │  │  - loadComments()                                      │ │   │
│  │  │  - submitComment()                                     │ │   │
│  │  │  - deleteComment()                                     │ │   │
│  │  │  - editComment()                                       │ │   │
│  │  └────────────────────────────────────────────────────────┘ │   │
│  │                                                              │   │
│  └──────────────────────────────────────────────────────────────┘   │
│                                                                       │
└─────────────────────────────────────────────────────────────────────┘
```

---

## Request Flow Diagram

### 1️⃣ Load Comments (GET)

```
Browser                        Django
  │                              │
  │  DOMContentLoaded            │
  ├─────────────────────────────→│
  │  loadComments(projectId)     │
  │                              │
  │  fetch('/accounts/projects/  │
  │         1/comments/')        │
  ├─────────────────────────────→│
  │                     accounts/urls.py (line 125)
  │                     ↓
  │              path('projects/<id>/comments/',
  │                    get_comments)
  │                     ↓
  │         comment_api.py :: get_comments()
  │              {
  │                Query database
  │                Fetch all comments for project
  │                Include user profile data
  │              }
  │                     ↓
  │         ← 200 OK + JSON
  │    [
  │      {
  │        id: 1,
  │        content: "Great project!",
  │        user: { username, full_name, profile_photo },
  │        created_at: "2026-02-04T10:30:00Z"
  │      }
  │    ]
  │←─────────────────────────────┤
  │                              │
  │  Display comments on page    │
  │  ✓ Comments now visible      │
  │                              │
```

### 2️⃣ Add Comment (POST)

```
Browser                        Django
  │                              │
  │  User types comment          │
  │  Clicks "Post" button        │
  │                              │
  │  submitComment()             │
  │                              │
  │  fetch('/accounts/projects/  │
  │         1/comments/add/',    │
  │         {                    │
  │           method: 'POST',    │
  │           body: {            │
  │             content: "Nice!" │
  │           }                  │
  │         })                   │
  │                              │
  ├─────────────────────────────→│
  │                     accounts/urls.py (line 126)
  │                     ↓
  │              path('projects/<id>/comments/add/',
  │                    add_comment)
  │                     ↓
  │         comment_api.py :: add_comment()
  │              {
  │                Create Comment object
  │                Set user, project, content
  │                Save to database
  │                Create Activity log
  │                Send notification to owner
  │              }
  │                     ↓
  │         ← 200 OK + JSON
  │    {
  │      success: true,
  │      comment: {
  │        id: 2,
  │        content: "Nice!",
  │        created_at: "..."
  │      }
  │    }
  │←─────────────────────────────┤
  │                              │
  │  Clear textarea              │
  │  Reload all comments         │
  │  ✓ New comment visible       │
  │                              │
```

### 3️⃣ Edit Comment (PUT)

```
Browser                        Django
  │                              │
  │  User clicks Edit button     │
  │  Shows prompt dialog         │
  │                              │
  │  editComment(commentId)      │
  │                              │
  │  fetch('/accounts/comments/  │
  │         5/edit/',            │
  │         {                    │
  │           method: 'PUT',     │
  │           body: {            │
  │             content: "New text" │
  │           }                  │
  │         })                   │
  │                              │
  ├─────────────────────────────→│
  │                     accounts/urls.py (line 128)
  │                     ↓
  │              path('comments/<id>/edit/',
  │                    edit_comment)
  │                     ↓
  │         comment_api.py :: edit_comment()
  │              {
  │                Check: user == comment.user
  │                Update content
  │                Save to database
  │              }
  │                     ↓
  │         ← 200 OK + JSON
  │    {
  │      success: true,
  │      comment: {
  │        id: 5,
  │        content: "New text",
  │        updated_at: "..."
  │      }
  │    }
  │←─────────────────────────────┤
  │                              │
  │  Reload comments             │
  │  ✓ Updated comment visible   │
  │                              │
```

### 4️⃣ Delete Comment (DELETE)

```
Browser                        Django
  │                              │
  │  User clicks Delete button   │
  │  Shows confirmation dialog   │
  │                              │
  │  deleteComment(commentId)    │
  │                              │
  │  fetch('/accounts/comments/  │
  │         5/delete/',          │
  │         {                    │
  │           method: 'DELETE'   │
  │         })                   │
  │                              │
  ├─────────────────────────────→│
  │                     accounts/urls.py (line 127)
  │                     ↓
  │              path('comments/<id>/delete/',
  │                    delete_comment)
  │                     ↓
  │         comment_api.py :: delete_comment()
  │              {
  │                Check permissions:
  │                - user == comment.user OR
  │                - user == project.user
  │                Delete from database
  │              }
  │                     ↓
  │         ← 200 OK + JSON
  │    {
  │      success: true,
  │      message: "Comment deleted"
  │    }
  │←─────────────────────────────┤
  │                              │
  │  Reload comments             │
  │  ✓ Comment removed           │
  │                              │
```

---

## Data Flow Diagram

```
                            USER ACTION
                                 │
                    ┌────────────┴────────────┐
                    │                         │
              Load Page                  View Project
                    │                         │
                    └────────────┬────────────┘
                                 │
                        ┌────────▼────────┐
                        │ Browser Loads   │
                        │ project_detail  │
                        │ .html           │
                        └────────┬────────┘
                                 │
                    ┌────────────▼────────────┐
                    │ Include comment_section │
                    │ .html                   │
                    └────────┬────────────────┘
                             │
           ┌─────────────────┼─────────────────┐
           │                 │                 │
      ┌────▼────┐     ┌─────▼─────┐    ┌─────▼────┐
      │ Comment │     │ Form HTML │    │JavaScript│
      │ List    │     │ Textarea  │    │Handlers  │
      └────┬────┘     └─────┬─────┘    └─────┬────┘
           │                │                 │
           │                │      ┌──────────▼──────────┐
           │                │      │ DOMContentLoaded    │
           │                │      │ event fires         │
           │                │      └──────────┬──────────┘
           │                │                 │
           │                │      ┌──────────▼──────────┐
           │                │      │ loadComments()      │
           │                │      │ called              │
           │                │      └──────────┬──────────┘
           │                │                 │
           │  ┌─────────────┴─────────────────▼──────────┐
           │  │ fetch('/accounts/projects/1/comments/')  │
           │  └─────────────┬─────────────────────────┬──┘
           │                │                         │
      ┌────▼────────┐   ┌───▼─────────────────────┐
      │ Server:     │   │ Server Response:        │
      │ GET request │   │ [                       │
      │ from        │   │   {comment data},       │
      │ /accounts/  │   │   {comment data}        │
      │ projects/1/ │   │ ]                       │
      │ comments/   │   └───┬─────────────────────┘
      └────┬────────┘       │
           │         ┌───────▼────────┐
           │         │ Display        │
           │         │ comments       │
           │         │ on page        │
           │         └────────────────┘
           │
      ┌────▼───────────────────────────┐
      │ User sees:                      │
      │ ✓ Existing comments             │
      │ ✓ Comment form                  │
      │ ✓ Can post new comment          │
      │ ✓ Can edit own comment          │
      │ ✓ Can delete own comment        │
      └────────────────────────────────┘
```

---

## Database Schema (Comments Related)

```
┌──────────────────────────────────────┐
│          auth_user                   │
├──────────────────────────────────────┤
│ id (PK)                              │
│ username                             │
│ email                                │
│ first_name                           │
│ last_name                            │
└──────────────────────────────────────┘
           │
           │ (user → comment.user)
           │
┌──────────────────────────────────────┐
│      accounts_comment                │
├──────────────────────────────────────┤
│ id (PK)                              │
│ user_id (FK → auth_user)             │
│ project_id (FK → accounts_project)   │
│ content (TextField)                  │
│ created_at (DateTime)                │
│ updated_at (DateTime)                │
└──────────────────────────────────────┘
           │
           │ (project → comment.project)
           │
┌──────────────────────────────────────┐
│      accounts_project                │
├──────────────────────────────────────┤
│ id (PK)                              │
│ user_id (FK → auth_user)             │
│ title (CharField)                    │
│ description (TextField)              │
│ visibility (CharField)               │
│ created_at (DateTime)                │
└──────────────────────────────────────┘
```

---

## Multi-User Comment Visibility

```
┌─────────────────────────────────────────────────────────┐
│                   Project ID: 1                          │
│            "Build a Mobile App"                          │
├─────────────────────────────────────────────────────────┤
│                                                          │
│  Owner: User A                                           │
│                                                          │
│  ┌──────────────────────────────────────────────────┐   │
│  │  Comments Section                                │   │
│  ├──────────────────────────────────────────────────┤   │
│  │  Comments (3)                                    │   │
│  │                                                  │   │
│  │  [User B] "Interested in design!" ✅ Visible    │   │
│  │           Can edit? NO                           │   │
│  │           Can delete? YES (am owner)             │   │
│  │                                                  │   │
│  │  [User C] "Let's build it!" ✅ Visible           │   │
│  │           Can edit? NO                           │   │
│  │           Can delete? YES (am owner)             │   │
│  │                                                  │   │
│  │  [User A] "Let's start!" ✅ Visible              │   │
│  │           Can edit? YES                          │   │
│  │           Can delete? YES                        │   │
│  │                                                  │   │
│  │  Post Comment: [Textarea] [Post]                 │   │
│  └──────────────────────────────────────────────────┘   │
│                                                          │
└─────────────────────────────────────────────────────────┘

Same comments visible to ALL users viewing this project:
✓ User A (owner)
✓ User B (connected)
✓ User C (connected)
✓ Any authenticated user (if project is public)
```

---

## Error Handling Flow

```
┌─────────────────────┐
│ User posts comment  │
└────────────┬────────┘
             │
      ┌──────▼──────┐
      │ Send POST   │
      │ request     │
      └──────┬──────┘
             │
        ┌────▼────────────────────┐
        │ Server receives request │
        └────┬────────────────────┘
             │
      ┌──────▼──────────────────────────────┐
      │ Check: Is user authenticated?       │
      └──────┬───────────────┬──────────────┘
             │               │
         YES │               │ NO
             │               │
        ┌────▼────┐      ┌───▼─────────────┐
        │ Continue │      │ Return 401      │
        └────┬────┘      │ Unauthorized    │
             │           └─────────────────┘
        ┌────▼──────────────────────────────┐
        │ Check: Is comment content empty?  │
        └────┬──────────┬──────────────────┘
             │          │
         NO  │          │ YES
             │          │
        ┌────▼────┐  ┌──▼──────────────────┐
        │ Continue │  │ Return 400          │
        └────┬────┘  │ Bad Request         │
             │       └─────────────────────┘
        ┌────▼──────────────────────────────┐
        │ Check: Is content < 1000 chars?   │
        └────┬──────────┬──────────────────┘
             │          │
         YES │          │ NO
             │          │
        ┌────▼────┐  ┌──▼──────────────────┐
        │ Continue │  │ Return 400          │
        └────┬────┘  │ Bad Request         │
             │       └─────────────────────┘
        ┌────▼───────────────────┐
        │ Save to database       │
        └────┬───────────────────┘
             │
        ┌────▼────────────────────┐
        │ Create Activity log     │
        └────┬────────────────────┘
             │
        ┌────▼──────────────────────────────┐
        │ Send notification to owner        │
        │ (if not the same user)            │
        └────┬──────────────────────────────┘
             │
        ┌────▼──────────────────────────┐
        │ Return 200 OK + comment data  │
        └────┬──────────────────────────┘
             │
        ┌────▼──────────────────────────┐
        │ Browser: Clear textarea       │
        │ Browser: Reload all comments  │
        │ Browser: Show comment posted  │
        │ Browser: User sees new comment│
        └───────────────────────────────┘
```

---

## Authentication & Authorization Flow

```
┌────────────────────────────────────┐
│ User visits project detail page    │
└────────────────┬───────────────────┘
                 │
        ┌────────▼────────┐
        │ Is user logged  │
        │ in?             │
        └────┬────────────┘
             │
      ┌──────┴──────┐
      │             │
   YES│             │NO
      │             │
  ┌───▼───────┐  ┌─▼──────────────┐
  │ Show form │  │ Show message:  │
  │ to post   │  │ "Sign in to    │
  │ comments  │  │  comment"      │
  └───┬───────┘  └────────────────┘
      │
  ┌───▼─────────────────────────────┐
  │ User submits comment            │
  └───┬─────────────────────────────┘
      │
  ┌───▼─────────────────────────────┐
  │ Server checks:                  │
  │ - Is user authenticated? (YES)  │
  │ - Is comment valid? (checks)    │
  └───┬─────────────────────────────┘
      │
  ┌───▼──────────────────────────────┐
  │ Save comment                     │
  │ Display to all users             │
  └──────────────────────────────────┘

DELETE: Only if:
  - User == comment.user OR
  - User == project.user (owner)

EDIT: Only if:
  - User == comment.user
```

---

## Summary

The comments system works through a series of coordinated JavaScript fetch calls to Django REST endpoints. The fix simply corrected the endpoint paths from `/api/` to `/accounts/`, enabling proper communication between the frontend and backend.

**Result**: Comments are now visible to all users viewing a project ✅
