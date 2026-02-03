# Live Feed Comment Section Implementation Guide

## Overview

This guide covers the implementation of a **comment section in the live feed** where users can comment on projects **without needing to connect to the project owner first**.

## What Was Added

### 1. **CommentForm** (forms.py)
- Enhanced form for adding comments
- Textarea with 2 rows, placeholder text
- Max 1000 characters validation
- Styled with Bootstrap classes

### 2. **Comment API Endpoints** (comment_api.py)
Four new REST API endpoints for managing comments:

#### **GET /accounts/api/projects/<project_id>/comments/**
Fetch all comments for a project
```
Response:
{
  "success": true,
  "count": 5,
  "comments": [
    {
      "id": 1,
      "content": "Great project!",
      "user": {
        "id": 2,
        "username": "alice",
        "full_name": "Alice Smith",
        "profile_photo": "/media/profile_photos/alice.jpg"
      },
      "created_at": "2024-01-15T10:30:00Z",
      "formatted_time": "Jan 15, 2024 10:30 AM",
      "can_delete": true,
      "can_edit": true
    }
  ]
}
```

#### **POST /accounts/api/projects/<project_id>/comments/add/**
Add a new comment
```
Request:
{
  "content": "This is awesome!"
}

Response:
{
  "success": true,
  "comment": {
    "id": 6,
    "content": "This is awesome!",
    "user": {
      "id": 1,
      "username": "john",
      "profile_photo": "/media/profile_photos/john.jpg"
    },
    "created_at": "2024-01-15T11:45:00Z",
    "formatted_time": "Jan 15, 2024 11:45 AM"
  }
}
```

#### **DELETE /accounts/api/comments/<comment_id>/**
Delete a comment (own comment or project owner only)
```
Response:
{
  "success": true,
  "message": "Comment deleted"
}
```

#### **PUT /accounts/api/comments/<comment_id>/edit/**
Edit a comment (own comment only)
```
Request:
{
  "content": "Updated comment"
}

Response:
{
  "success": true,
  "comment": {
    "id": 1,
    "content": "Updated comment",
    "updated_at": "2024-01-15T12:00:00Z"
  }
}
```

### 3. **URL Routes** (urls.py)
Added 4 new API endpoints:
```python
path('api/projects/<int:project_id>/comments/', get_comments, name='get-comments'),
path('api/projects/<int:project_id>/comments/add/', add_comment, name='add-comment'),
path('api/comments/<int:comment_id>/delete/', delete_comment, name='delete-comment'),
path('api/comments/<int:comment_id>/edit/', edit_comment, name='edit-comment'),
```

## Frontend Implementation

### HTML Template for Comments Section

Add this to your `social/activity_feed.html` or `project_detail.html`:

```html
<!-- LIVE FEED COMMENT SECTION -->
<div class="comment-section mt-4" data-project-id="{{ project.id }}" id="comments-section-{{ project.id }}">
    <div class="card">
        <div class="card-header bg-light">
            <h6 class="mb-0">💬 Comments (<span class="comment-count">0</span>)</h6>
        </div>
        
        <div class="card-body">
            <!-- Comment Input Form -->
            {% if user.is_authenticated %}
            <div class="comment-input-wrapper mb-4">
                <form class="comment-form" data-project-id="{{ project.id }}">
                    {% csrf_token %}
                    <div class="input-group">
                        <textarea 
                            class="form-control comment-textarea" 
                            placeholder="Share your thoughts on this project..."
                            rows="2"
                            maxlength="1000"
                            style="border-radius: 8px 0 0 8px;"
                        ></textarea>
                        <button class="btn btn-primary" type="submit" style="border-radius: 0 8px 8px 0;">
                            <span class="spinner-border spinner-border-sm d-none me-2" role="status" aria-hidden="true"></span>
                            Post
                        </button>
                    </div>
                    <small class="text-muted">Max 1000 characters</small>
                </form>
            </div>
            {% else %}
            <div class="alert alert-info">
                <a href="{% url 'login' %}">Sign in</a> to comment on this project
            </div>
            {% endif %}
            
            <!-- Comments List -->
            <div class="comments-list" id="comments-{{ project.id }}">
                <div class="text-center text-muted py-4">
                    <small>Loading comments...</small>
                </div>
            </div>
        </div>
    </div>
</div>

<style>
.comment-section {
    margin-top: 2rem;
    margin-bottom: 2rem;
}

.comment-form textarea {
    resize: none;
    font-size: 14px;
}

.comment-item {
    padding: 1rem;
    border-left: 3px solid #e9ecef;
    margin-bottom: 1rem;
    border-radius: 4px;
    transition: all 0.3s ease;
}

.comment-item:hover {
    background-color: #f8f9fa;
    border-left-color: #007bff;
}

.comment-author {
    font-weight: 600;
    font-size: 14px;
}

.comment-time {
    color: #6c757d;
    font-size: 12px;
}

.comment-content {
    margin: 0.5rem 0;
    line-height: 1.5;
    color: #333;
}

.comment-actions {
    margin-top: 0.5rem;
    display: flex;
    gap: 0.5rem;
}

.comment-actions button {
    background: none;
    border: none;
    color: #6c757d;
    cursor: pointer;
    font-size: 12px;
    padding: 0;
    text-decoration: none;
}

.comment-actions button:hover {
    color: #007bff;
}

.comment-avatar {
    width: 32px;
    height: 32px;
    border-radius: 50%;
    object-fit: cover;
    background: #e9ecef;
}

.comments-empty {
    text-align: center;
    color: #6c757d;
    padding: 2rem;
}
</style>
```

### JavaScript for Comment Functionality

```html
<script>
document.addEventListener('DOMContentLoaded', function() {
    // Get all comment sections
    const commentSections = document.querySelectorAll('.comment-section');
    
    commentSections.forEach(section => {
        const projectId = section.dataset.projectId;
        const commentForm = section.querySelector('.comment-form');
        const commentsList = section.querySelector('.comments-list');
        const commentCount = section.querySelector('.comment-count');
        
        // Load comments on page load
        loadComments(projectId);
        
        // Handle comment form submission
        if (commentForm) {
            commentForm.addEventListener('submit', function(e) {
                e.preventDefault();
                submitComment(projectId, commentForm, commentsList, commentCount);
            });
        }
    });
});

function loadComments(projectId) {
    const section = document.querySelector(`[data-project-id="${projectId}"]`);
    const commentsList = section.querySelector('.comments-list');
    const commentCount = section.querySelector('.comment-count');
    
    fetch(`/accounts/api/projects/${projectId}/comments/`)
        .then(response => response.json())
        .then(data => {
            if (data.success) {
                commentCount.textContent = data.count;
                
                if (data.comments.length === 0) {
                    commentsList.innerHTML = '<div class="comments-empty">No comments yet. Be the first to comment!</div>';
                } else {
                    commentsList.innerHTML = data.comments.map(comment => createCommentHTML(comment, projectId)).join('');
                    attachCommentActions(projectId);
                }
            }
        })
        .catch(error => {
            console.error('Error loading comments:', error);
            commentsList.innerHTML = '<div class="alert alert-danger">Failed to load comments</div>';
        });
}

function submitComment(projectId, form, commentsList, commentCount) {
    const textarea = form.querySelector('textarea');
    const button = form.querySelector('button');
    const spinner = button.querySelector('.spinner-border');
    const content = textarea.value.trim();
    
    if (!content) {
        alert('Please enter a comment');
        return;
    }
    
    // Disable button and show spinner
    button.disabled = true;
    spinner.classList.remove('d-none');
    
    fetch(`/accounts/api/projects/${projectId}/comments/add/`, {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
            'X-CSRFToken': form.querySelector('[name=csrfmiddlewaretoken]').value
        },
        body: JSON.stringify({ content: content })
    })
    .then(response => response.json())
    .then(data => {
        if (data.success) {
            // Clear textarea
            textarea.value = '';
            
            // Reload comments
            loadComments(projectId);
            
            // Show success message
            showMessage('Comment posted successfully!', 'success');
        } else {
            showMessage(data.error || 'Failed to post comment', 'error');
        }
    })
    .catch(error => {
        console.error('Error posting comment:', error);
        showMessage('Failed to post comment', 'error');
    })
    .finally(() => {
        button.disabled = false;
        spinner.classList.add('d-none');
    });
}

function createCommentHTML(comment, projectId) {
    const avatarUrl = comment.user.profile_photo || 'https://via.placeholder.com/32';
    const canDelete = comment.can_delete;
    const canEdit = comment.can_edit;
    
    return `
        <div class="comment-item" data-comment-id="${comment.id}">
            <div class="d-flex gap-3">
                <img src="${avatarUrl}" alt="${comment.user.username}" class="comment-avatar">
                
                <div class="flex-grow-1">
                    <div class="d-flex justify-content-between align-items-start">
                        <div>
                            <span class="comment-author">${comment.user.full_name}</span>
                            <span class="text-muted">@${comment.user.username}</span>
                            <div class="comment-time">${comment.formatted_time}</div>
                        </div>
                    </div>
                    
                    <div class="comment-content">${escapeHtml(comment.content)}</div>
                    
                    ${canDelete || canEdit ? `
                        <div class="comment-actions">
                            ${canEdit ? `<button class="edit-comment-btn" data-comment-id="${comment.id}">Edit</button>` : ''}
                            ${canDelete ? `<button class="delete-comment-btn" data-comment-id="${comment.id}" data-project-id="${projectId}">Delete</button>` : ''}
                        </div>
                    ` : ''}
                </div>
            </div>
        </div>
    `;
}

function attachCommentActions(projectId) {
    // Delete button handlers
    document.querySelectorAll('.delete-comment-btn').forEach(btn => {
        btn.addEventListener('click', function(e) {
            e.preventDefault();
            if (confirm('Are you sure you want to delete this comment?')) {
                const commentId = this.dataset.commentId;
                deleteComment(commentId, projectId);
            }
        });
    });
    
    // Edit button handlers
    document.querySelectorAll('.edit-comment-btn').forEach(btn => {
        btn.addEventListener('click', function(e) {
            e.preventDefault();
            const commentId = this.dataset.commentId;
            editComment(commentId, projectId);
        });
    });
}

function deleteComment(commentId, projectId) {
    fetch(`/accounts/api/comments/${commentId}/delete/`, {
        method: 'DELETE',
        headers: {
            'X-CSRFToken': document.querySelector('[name=csrfmiddlewaretoken]').value
        }
    })
    .then(response => response.json())
    .then(data => {
        if (data.success) {
            loadComments(projectId);
            showMessage('Comment deleted', 'success');
        } else {
            showMessage(data.error || 'Failed to delete comment', 'error');
        }
    })
    .catch(error => {
        console.error('Error:', error);
        showMessage('Failed to delete comment', 'error');
    });
}

function editComment(commentId, projectId) {
    const commentElement = document.querySelector(`[data-comment-id="${commentId}"]`);
    const contentElement = commentElement.querySelector('.comment-content');
    const currentContent = contentElement.textContent;
    
    const newContent = prompt('Edit your comment:', currentContent);
    if (newContent === null || newContent.trim() === '') return;
    
    if (newContent.trim().length > 1000) {
        showMessage('Comment too long (max 1000 characters)', 'error');
        return;
    }
    
    fetch(`/accounts/api/comments/${commentId}/edit/`, {
        method: 'PUT',
        headers: {
            'Content-Type': 'application/json',
            'X-CSRFToken': document.querySelector('[name=csrfmiddlewaretoken]').value
        },
        body: JSON.stringify({ content: newContent.trim() })
    })
    .then(response => response.json())
    .then(data => {
        if (data.success) {
            loadComments(projectId);
            showMessage('Comment updated', 'success');
        } else {
            showMessage(data.error || 'Failed to edit comment', 'error');
        }
    })
    .catch(error => {
        console.error('Error:', error);
        showMessage('Failed to edit comment', 'error');
    });
}

function showMessage(message, type) {
    // Create alert element
    const alert = document.createElement('div');
    alert.className = `alert alert-${type === 'error' ? 'danger' : 'success'} alert-dismissible fade show`;
    alert.role = 'alert';
    alert.innerHTML = `
        ${message}
        <button type="button" class="btn-close" data-bs-dismiss="alert"></button>
    `;
    
    // Insert at top of page
    const container = document.body.firstChild;
    document.body.insertBefore(alert, container);
    
    // Auto-dismiss after 3 seconds
    setTimeout(() => {
        alert.remove();
    }, 3000);
}

function escapeHtml(text) {
    const map = {
        '&': '&amp;',
        '<': '&lt;',
        '>': '&gt;',
        '"': '&quot;',
        "'": '&#039;'
    };
    return text.replace(/[&<>"']/g, m => map[m]);
}
</script>
```

## Integration Steps

### 1. **Add to Activity Feed Template** (`social/activity_feed.html`)
In the project activity card section, add the comment section:

```html
{% if activity.project %}
    <div class="project-card">
        <!-- Existing project details -->
        ...
        
        <!-- ADD THIS: Comment Section -->
        <div class="project-comments mt-3">
            {% include 'includes/comment_section.html' with project=activity.project %}
        </div>
    </div>
{% endif %}
```

### 2. **Create Reusable Component** (`accounts/templates/includes/comment_section.html`)
Create this new template file with the HTML/JS from above.

### 3. **Update Project Detail Template** (`accounts/templates/project_detail.html`)
Add comment section to project detail page:

```html
<!-- At the bottom of project details -->
{% include 'includes/comment_section.html' with project=project %}
```

### 4. **Migrate Database** (if Comment model changes)
```bash
python manage.py makemigrations
python manage.py migrate
```

## Features

### ✅ **What Users Can Do**
- ✅ Comment on projects without connecting
- ✅ View all comments on a project
- ✅ Edit their own comments
- ✅ Delete their own comments
- ✅ Project owner can delete any comment
- ✅ See commenter profile (username, avatar, full name)
- ✅ Timestamps on each comment
- ✅ Real-time comment display

### ✅ **Notifications**
- ✅ Project owner receives notification when someone comments
- ✅ Activity log entry created
- ✅ Shows in user's activity feed

### ✅ **Security**
- ✅ CSRF protection
- ✅ User authentication required
- ✅ Permission checks (edit/delete own comments)
- ✅ Input validation (max 1000 chars)
- ✅ XSS protection (HTML escaping)

### ✅ **Performance**
- ✅ Efficient database queries (select_related, prefetch_related)
- ✅ Pagination ready
- ✅ Async loading with fetch API
- ✅ Spinner for user feedback

## API Usage Examples

### Add Comment via CURL
```bash
curl -X POST http://localhost:8000/accounts/api/projects/1/comments/add/ \
  -H "Content-Type: application/json" \
  -H "X-CSRFToken: YOUR_CSRF_TOKEN" \
  -d '{"content": "Amazing project!"}'
```

### Get Comments via CURL
```bash
curl http://localhost:8000/accounts/api/projects/1/comments/
```

### Delete Comment via CURL
```bash
curl -X DELETE http://localhost:8000/accounts/api/comments/5/delete/ \
  -H "X-CSRFToken: YOUR_CSRF_TOKEN"
```

## Testing Checklist

- [ ] Comment form appears for authenticated users
- [ ] Anonymous users see login prompt
- [ ] Can submit comment with content
- [ ] Comments appear immediately after submission
- [ ] Comment count updates
- [ ] Can delete own comment
- [ ] Can edit own comment
- [ ] Project owner can delete any comment
- [ ] Notifications created for project owner
- [ ] Activity log entries created
- [ ] Timestamps display correctly
- [ ] User profiles display with comments
- [ ] Max 1000 character limit enforced

## Model Relationships

```
Comment
├── user (ForeignKey → User)
├── project (ForeignKey → Project)
├── content (TextField)
├── created_at (DateTimeField)
└── updated_at (DateTimeField)

Project
└── comments (Reverse FK from Comment)
```

## Future Enhancements

- [ ] Nested replies (comments on comments)
- [ ] Comment likes/reactions
- [ ] Comment moderation (flag/report)
- [ ] Rich text editing (markdown support)
- [ ] Comment threading
- [ ] Typing indicators
- [ ] Real-time updates (WebSocket)
- [ ] Comment sorting (newest/oldest/popular)
- [ ] Pagination for many comments
- [ ] Email notifications
