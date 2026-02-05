# Comments Badge Fix - Quick Implementation (5 minutes)

## The Issue in 1 Sentence
Comment badge shows 0 because comments aren't loaded until you click, but the badge isn't updated when you click.

## The Fix in 3 Steps

### Step 1: Find and Edit Line 615
**File**: `accounts/templates/social/activity_feed.html`

**Find**:
```html
<div class="activity-card" data-activity-id="{{ activity.id }}">
```

**Replace with**:
```html
<div class="activity-card" data-activity-id="{{ activity.id }}" data-project-id="{{ activity.project.id }}">
```

---

### Step 2: Find and Edit Line 634
**File**: `accounts/templates/social/activity_feed.html`

**Find**:
```html
<span class="text-sm">{{ activity.comments_count|default:0 }}</span>
```

**Replace with**:
```html
<span class="text-sm" id="comment-count-badge-{{ activity.id }}">{{ activity.comments_count|default:0 }}</span>
```

---

### Step 3: Find and Replace Lines 1029-1044
**File**: `accounts/templates/social/activity_feed.html`

**Find this entire function**:
```javascript
function handleCommentClick(event) {
    const button = event.currentTarget;
    const activityId = button.closest('.activity-card').dataset.activityId;
    const commentsSection = document.getElementById(`comments-${activityId}`);

    // Toggle comments visibility
    commentsSection.classList.toggle('hidden');

    // Focus on comment input if opening
    if (!commentsSection.classList.contains('hidden')) {
        const commentInput = commentsSection.querySelector('input[type="text"]');
        if (commentInput) {
            setTimeout(() => commentInput.focus(), 300);
        }
    }
}
```

**Replace with this**:
```javascript
let loadedActivityComments = {};

function handleCommentClick(event) {
    const button = event.currentTarget;
    const activityId = button.closest('.activity-card').dataset.activityId;
    const commentsSection = document.getElementById(`comments-${activityId}`);

    // Toggle comments visibility
    commentsSection.classList.toggle('hidden');

    // If opening comments, load them if not already loaded
    if (!commentsSection.classList.contains('hidden')) {
        if (!loadedActivityComments[activityId]) {
            loadCommentsForActivity(activityId);
        }
        
        // Focus on comment input
        const commentInput = commentsSection.querySelector('input[type="text"]');
        if (commentInput) {
            setTimeout(() => commentInput.focus(), 300);
        }
    }
}

function loadCommentsForActivity(activityId) {
    const activity = document.querySelector(`[data-activity-id="${activityId}"]`);
    if (!activity) return;
    
    const projectId = activity.dataset.projectId;
    if (!projectId) return;
    
    const commentsList = document.getElementById(`comments-list-${activityId}`);
    const commentCount = document.getElementById(`comment-count-${activityId}`);
    
    if (!commentsList) return;
    
    // Fetch comments from API
    fetch(`/accounts/projects/${projectId}/comments/`, {
        method: 'GET',
        headers: {
            'X-Requested-With': 'XMLHttpRequest',
            'Accept': 'application/json'
        }
    })
    .then(response => response.json())
    .then(data => {
        if (data.success) {
            loadedActivityComments[activityId] = true;
            
            // Update comment counts
            if (commentCount) {
                commentCount.textContent = data.count;
            }
            
            const badge = document.getElementById(`comment-count-badge-${activityId}`);
            if (badge) {
                badge.textContent = data.count;
            }
            
            // Clear and populate comments list
            commentsList.innerHTML = '';
            
            if (data.comments && data.comments.length > 0) {
                data.comments.forEach(comment => {
                    const commentEl = createCommentElement(comment);
                    commentsList.appendChild(commentEl);
                });
            } else {
                commentsList.innerHTML = '<div class="text-gray-400 text-center py-4">No comments yet</div>';
            }
        }
    })
    .catch(error => {
        console.error('Error loading comments:', error);
        commentsList.innerHTML = '<div class="text-red-400 text-center py-4">Failed to load comments</div>';
    });
}

function createCommentElement(comment) {
    const div = document.createElement('div');
    div.className = 'flex gap-3 comment-item';
    div.innerHTML = `
        <img src="${comment.user.profile_photo || '/static/default-avatar.png'}" 
             class="w-8 h-8 rounded-full flex-shrink-0" 
             alt="${comment.user.username}">
        <div class="flex-1 min-w-0">
            <div class="flex items-center gap-2">
                <span class="font-semibold text-white">${comment.user.full_name || comment.user.username}</span>
                <span class="text-xs text-gray-500">${comment.formatted_time}</span>
            </div>
            <p class="text-gray-300 break-words whitespace-pre-wrap mt-1">${escapeHtml(comment.content)}</p>
            ${comment.can_delete ? `<button class="text-xs text-red-400 hover:text-red-300 mt-2" onclick="deleteComment(${comment.id}, event)">Delete</button>` : ''}
        </div>
    `;
    return div;
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
```

---

## That's It!

After these 3 edits:
- Comment badge will show correct count
- Clicking will load actual comments
- Count will update when you add/delete comments

## Quick Test

1. Refresh page
2. Check comment badges (should show real numbers)
3. Click a comment button
4. Comments should load
5. Add a comment and see count update

---

## If It Doesn't Work

**Check these**:
1. Is `data-project-id` on the activity-card div?
2. Is the API endpoint `/accounts/projects/{id}/comments/` working?
3. Are there any browser console errors? (F12 → Console)
4. Is the file saved? Refresh browser.

---

## Common Issues

| Issue | Solution |
|-------|----------|
| Comments still show 0 | Check `data-project-id` attribute was added |
| Comments don't load | Check browser console for error, verify API endpoint |
| Nothing changes | Hard refresh (Ctrl+Shift+R) to clear cache |
| Comments show but not updated | Check if `comment.formatted_time` exists in API response |

---

## Done! 🎉

The badge now shows the real count and loads comments when clicked.
