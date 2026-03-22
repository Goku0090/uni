/**
 * Comments Handler for Project Detail Page
 * Handles loading, posting, editing, and deleting comments
 */

document.addEventListener('DOMContentLoaded', function() {
    const commentSections = document.querySelectorAll('.comment-section');
    
    commentSections.forEach(section => {
        const projectId = section.dataset.projectId;
        const commentForm = section.querySelector('.comment-form');
        const commentsList = section.querySelector('.comments-list');
        const commentCount = section.querySelector('.comment-count');
        const textarea = commentForm?.querySelector('textarea');
        const charCount = commentForm?.querySelector('.char-count');
        
        // Load comments on page load
        if (commentsList && projectId) {
            loadComments(projectId);
        }
        
        // Handle character counter
        if (textarea && charCount) {
            textarea.addEventListener('input', function() {
                charCount.textContent = this.value.length + '/1000';
            });
        }
        
        // Handle comment form submission
        if (commentForm) {
            commentForm.addEventListener('submit', function(e) {
                e.preventDefault();
                submitComment(projectId, commentForm, commentsList, commentCount);
            });
        }
    });
});

/**
 * Get default avatar URL (data URI - no external requests)
 * Uses SVG with initials to avoid external API calls
 */
function getDefaultAvatarUrl(username = 'U') {
    const initial = (username && username[0] || 'U').toUpperCase();
    const colors = ['667eea', '764ba2', '4dabf7', '51cf66', 'ffd93d', 'ff6b6b'];
    const colorIndex = (initial.charCodeAt(0)) % colors.length;
    const bgColor = colors[colorIndex];
    
    // SVG data URI - no external requests needed
    const svg = `<svg xmlns="http://www.w3.org/2000/svg" width="36" height="36" viewBox="0 0 36 36">
        <rect width="36" height="36" fill="#${bgColor}"/>
        <text x="18" y="24" font-size="18" font-weight="bold" text-anchor="middle" fill="white" font-family="Arial, sans-serif">${initial}</text>
    </svg>`;
    
    return 'data:image/svg+xml;base64,' + btoa(svg);
}

/**
 * Load comments for a project
 */
function loadComments(projectId) {
    const section = document.querySelector(`[data-project-id="${projectId}"]`);
    if (!section) return;
    
    const commentsList = section.querySelector('.comments-list');
    const commentCount = section.querySelector('.comment-count');
    
    if (!commentsList) return;
    
    // Create abort controller for timeout (5 seconds)
    const controller = new AbortController();
    const timeoutId = setTimeout(() => controller.abort(), 5000);
    
    fetch(`/accounts/projects/${projectId}/comments/`, {
        signal: controller.signal
    })
        .then(response => {
            clearTimeout(timeoutId);
            if (!response.ok) throw new Error('Failed to load comments');
            return response.json();
        })
        .then(data => {
            if (data.success) {
                if (commentCount) {
                    commentCount.textContent = data.count;
                }
                
                if (data.comments.length === 0) {
                    commentsList.innerHTML = '<div class="comments-empty">No comments yet. Be the first to comment!</div>';
                } else {
                    commentsList.innerHTML = data.comments.map(comment => createCommentHTML(comment, projectId)).join('');
                    attachCommentActions(projectId);
                }
            }
        })
        .catch(error => {
            clearTimeout(timeoutId);
            console.error('Error loading comments:', error);
            if (error.name === 'AbortError') {
                commentsList.innerHTML = '<div class="alert alert-warning mb-0"><small>Comments taking too long to load. <a href="javascript:location.reload()">Refresh</a></small></div>';
            } else {
                commentsList.innerHTML = '<div class="alert alert-warning mb-0"><small>Failed to load comments. Please refresh.</small></div>';
            }
        });
}

/**
 * Submit a new comment
 */
function submitComment(projectId, form, commentsList, commentCount) {
    const textarea = form.querySelector('textarea');
    const button = form.querySelector('button');
    const spinner = button.querySelector('.spinner-border');
    const submitText = button.querySelector('.submit-text');
    const content = textarea.value.trim();
    
    if (!content) {
        alert('Please enter a comment');
        return;
    }
    
    // Disable button and show spinner
    button.disabled = true;
    if (spinner) spinner.classList.remove('d-none');
    if (submitText) submitText.classList.add('d-none');
    
    const csrfToken = form.querySelector('[name=csrfmiddlewaretoken]')?.value;
    
    fetch(`/accounts/projects/${projectId}/comments/add/`, {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
            'X-CSRFToken': csrfToken || ''
        },
        body: JSON.stringify({ content: content })
    })
        .then(response => {
            if (!response.ok) throw new Error('Failed to post comment');
            return response.json();
        })
        .then(data => {
            if (data.success) {
                // Clear textarea and reset counter
                textarea.value = '';
                form.querySelector('.char-count').textContent = '0/1000';
                
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
            if (spinner) spinner.classList.add('d-none');
            if (submitText) submitText.classList.remove('d-none');
        });
}

/**
 * Create HTML for a comment
 */
function createCommentHTML(comment, projectId) {
    // Use user's profile photo if available, otherwise use local avatar fallback
    const avatarUrl = comment.user.profile_photo || getDefaultAvatarUrl(comment.user.username);
    const canDelete = comment.can_delete;
    const canEdit = comment.can_edit;
    
    return `
        <div class="comment-item" data-comment-id="${comment.id}">
            <div class="comment-header">
                <div class="comment-author-info">
                    <img src="${avatarUrl}" alt="${comment.user.username}" class="comment-avatar" onerror="this.src='${getDefaultAvatarUrl()}'">
                    <div>
                        <div class="comment-author">${escapeHtml(comment.user.full_name || comment.user.username)}</div>
                        <div class="comment-username">@${escapeHtml(comment.user.username)}</div>
                    </div>
                </div>
                <div class="comment-time">${comment.formatted_time || 'just now'}</div>
            </div>
            
            <div class="comment-content">${escapeHtml(comment.content)}</div>
            
            ${canDelete || canEdit ? `
                <div class="comment-actions">
                    ${canEdit ? `<button class="edit-comment-btn" data-comment-id="${comment.id}" title="Edit comment"><i class="fas fa-edit me-1"></i>Edit</button>` : ''}
                    ${canDelete ? `<button class="delete-comment-btn" data-comment-id="${comment.id}" data-project-id="${projectId}" title="Delete comment"><i class="fas fa-trash me-1"></i>Delete</button>` : ''}
                </div>
            ` : ''}
        </div>
    `;
}

/**
 * Attach event handlers to comment action buttons
 */
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

/**
 * Delete a comment
 */
function deleteComment(commentId, projectId) {
    const commentElement = document.querySelector(`[data-comment-id="${commentId}"]`);
    if (commentElement) commentElement.style.opacity = '0.5';
    
    const csrfToken = document.querySelector('[name=csrfmiddlewaretoken]')?.value;
    
    fetch(`/accounts/comments/${commentId}/delete/`, {
        method: 'DELETE',
        headers: {
            'X-CSRFToken': csrfToken || ''
        }
    })
        .then(response => {
            if (!response.ok) throw new Error('Failed to delete');
            return response.json();
        })
        .then(data => {
            if (data.success) {
                loadComments(projectId);
                showMessage('Comment deleted', 'success');
            } else {
                showMessage(data.error || 'Failed to delete comment', 'error');
                if (commentElement) commentElement.style.opacity = '1';
            }
        })
        .catch(error => {
            console.error('Error:', error);
            showMessage('Failed to delete comment', 'error');
            if (commentElement) commentElement.style.opacity = '1';
        });
}

/**
 * Edit a comment
 */
function editComment(commentId, projectId) {
    const commentElement = document.querySelector(`[data-comment-id="${commentId}"]`);
    const contentElement = commentElement.querySelector('.comment-content');
    const currentContent = contentElement.textContent;
    
    const newContent = prompt('Edit your comment (max 1000 characters):', currentContent);
    if (newContent === null) return;
    
    const trimmedContent = newContent.trim();
    
    if (trimmedContent === '') {
        showMessage('Comment cannot be empty', 'error');
        return;
    }
    
    if (trimmedContent.length > 1000) {
        showMessage('Comment too long (max 1000 characters)', 'error');
        return;
    }
    
    if (trimmedContent === currentContent) {
        return; // No changes
    }
    
    commentElement.style.opacity = '0.5';
    
    const csrfToken = document.querySelector('[name=csrfmiddlewaretoken]')?.value;
    
    fetch(`/accounts/comments/${commentId}/edit/`, {
        method: 'PUT',
        headers: {
            'Content-Type': 'application/json',
            'X-CSRFToken': csrfToken || ''
        },
        body: JSON.stringify({ content: trimmedContent })
    })
        .then(response => {
            if (!response.ok) throw new Error('Failed to edit');
            return response.json();
        })
        .then(data => {
            if (data.success) {
                loadComments(projectId);
                showMessage('Comment updated', 'success');
            } else {
                showMessage(data.error || 'Failed to edit comment', 'error');
                commentElement.style.opacity = '1';
            }
        })
        .catch(error => {
            console.error('Error:', error);
            showMessage('Failed to edit comment', 'error');
            commentElement.style.opacity = '1';
        });
}

/**
 * Show a temporary message to the user
 */
function showMessage(message, type) {
    // Create alert element
    const alert = document.createElement('div');
    const alertClass = type === 'error' ? 'alert-danger' : (type === 'success' ? 'alert-success' : 'alert-info');
    alert.className = `alert ${alertClass} alert-dismissible fade show`;
    alert.role = 'alert';
    alert.innerHTML = `
        ${message}
        <button type="button" class="btn-close" data-bs-dismiss="alert" aria-label="Close"></button>
    `;
    alert.style.zIndex = '9999';
    alert.style.position = 'fixed';
    alert.style.top = '20px';
    alert.style.right = '20px';
    alert.style.minWidth = '300px';
    
    // Insert at top of page
    document.body.appendChild(alert);
    
    // Auto-dismiss after 4 seconds
    setTimeout(() => {
        alert.remove();
    }, 4000);
}

/**
 * Escape HTML special characters
 */
function escapeHtml(text) {
    const map = {
        '&': '&amp;',
        '<': '&lt;',
        '>': '&gt;',
        '"': '&quot;',
        "'": '&#039;'
    };
    return String(text || '').replace(/[&<>"']/g, m => map[m]);
}
