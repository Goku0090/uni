# Comments Badge Bug Fix - Activity Feed

## Problem

**Symptom**: Comment badge shows `0` initially. When user clicks on comments, the count updates and shows actual comments.

**Root Cause**: 
1. The comment count badge in HTML is hardcoded to `0`
2. The `handleCommentClick()` function toggles visibility but doesn't fetch/load the comments
3. Comment count is only loaded when comments are explicitly fetched

**Location**: 
- Template: `accounts/templates/social/activity_feed.html` (line 691)
- JavaScript: `accounts/templates/social/activity_feed.html` (lines 1029-1044)

---

## Current Behavior

### Template (Line 634 & 691)
```html
<!-- Line 634: Initial badge (button display) -->
<span class="text-sm">{{ activity.comments_count|default:0 }}</span>

<!-- Line 691: Comments section header (hidden until clicked) -->
<span class="text-xs bg-white/10 px-2 py-1 rounded-full" id="comment-count-{{ activity.id }}">0</span>
```

### JavaScript (Lines 1029-1044)
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

**Issue**: Function only toggles visibility, doesn't load comments or update count.

---

## Solution

### Step 1: Update Template to Use Dynamic Count

**File**: `accounts/templates/social/activity_feed.html`

**Line 634** - Update the badge to add ID:
```html
<!-- OLD -->
<span class="text-sm">{{ activity.comments_count|default:0 }}</span>

<!-- NEW -->
<span class="text-sm" id="comment-count-badge-{{ activity.id }}">{{ activity.comments_count|default:0 }}</span>
```

### Step 2: Update JavaScript to Load Comments on Click

**File**: `accounts/templates/social/activity_feed.html` (replace lines 1029-1044)

```javascript
function handleCommentClick(event) {
    const button = event.currentTarget;
    const activityId = button.closest('.activity-card').dataset.activityId;
    const commentsSection = document.getElementById(`comments-${activityId}`);
    
    // Toggle comments visibility
    commentsSection.classList.toggle('hidden');
    
    // If opening comments, load them
    if (!commentsSection.classList.contains('hidden')) {
        loadCommentsForActivity(activityId);
        
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
    
    // Get project ID from activity data
    const projectId = activity.dataset.projectId;
    if (!projectId) return;
    
    const commentsList = document.getElementById(`comments-list-${activityId}`);
    const commentCount = document.getElementById(`comment-count-${activityId}`);
    
    if (!commentsList) return;
    
    // Fetch comments
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
            // Update comment count
            if (commentCount) {
                commentCount.textContent = data.count;
            }
            
            // Update badge
            const badge = document.getElementById(`comment-count-badge-${activityId}`);
            if (badge) {
                badge.textContent = data.count;
            }
            
            // Clear existing comments
            commentsList.innerHTML = '';
            
            // Display comments
            if (data.comments && data.comments.length > 0) {
                data.comments.forEach(comment => {
                    const commentEl = createCommentElement(comment, projectId);
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

function createCommentElement(comment, projectId) {
    const div = document.createElement('div');
    div.className = 'flex gap-3 comment-item';
    div.innerHTML = `
        <img src="${comment.user.profile_photo || '/static/default-avatar.png'}" 
             class="w-8 h-8 rounded-full flex-shrink-0" 
             alt="${comment.user.username}">
        <div class="flex-1 min-w-0">
            <div class="flex items-center gap-2">
                <a href="/profile/${comment.user.username}" class="font-semibold text-white hover:text-blue-400">
                    ${comment.user.full_name || comment.user.username}
                </a>
                <span class="text-xs text-gray-500">${comment.formatted_time}</span>
            </div>
            <p class="text-gray-300 break-words whitespace-pre-wrap">${escapeHtml(comment.content)}</p>
            ${comment.can_delete ? `<button class="text-xs text-red-400 hover:text-red-300 mt-1" onclick="deleteComment(${comment.id}, ${projectId})">Delete</button>` : ''}
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

### Step 3: Add project_id to Activity Card Data Attribute

**File**: `accounts/templates/social/activity_feed.html` (around line 615 where activity card starts)

```html
<!-- Find this line -->
<div class="activity-card" data-activity-id="{{ activity.id }}">

<!-- Change to -->
<div class="activity-card" data-activity-id="{{ activity.id }}" data-project-id="{{ activity.project.id }}">
```

---

## Implementation Steps

1. **Open** `accounts/templates/social/activity_feed.html`

2. **Find line 615** - Activity card div:
   ```html
   <div class="activity-card" data-activity-id="{{ activity.id }}">
   ```
   Add `data-project-id="{{ activity.project.id }}"` attribute

3. **Find line 634** - Comment badge button:
   ```html
   <span class="text-sm">{{ activity.comments_count|default:0 }}</span>
   ```
   Add id: `id="comment-count-badge-{{ activity.id }}"`

4. **Find lines 1029-1044** - Replace `handleCommentClick` function with the new version above

5. **Add new functions** - Add `loadCommentsForActivity`, `createCommentElement`, `escapeHtml` functions right after `handleCommentClick`

6. **Test**:
   - Load activity feed - badges should show correct counts
   - Click on comment button - comments load and section expands
   - Add a comment - count updates
   - Delete a comment - count decreases

---

## Why This Happens

The comment badge shows 0 because:

1. Template has hardcoded `0` in the hidden comments section
2. The activity model may not have `comments_count` annotation 
3. The click handler only toggles visibility, doesn't load data
4. Comments are loaded only when needed (lazy loading), but count wasn't updated

---

## Backend (Optional Enhancement)

If you want counts on initial page load, update the view:

**File**: `accounts/views.py` (where activities are fetched)

```python
from django.db.models import Count

def get_activity_feed(request):
    activities = Activity.objects.all().select_related(
        'user', 'project'
    ).annotate(
        comments_count=Count('project__comments', distinct=True)
    ).order_by('-created_at')
    
    return render(request, 'social/activity_feed.html', {
        'activities': activities
    })
```

---

## Files to Modify

1. **accounts/templates/social/activity_feed.html**
   - Line ~615: Add `data-project-id` attribute
   - Line 634: Add `id` to comment badge
   - Lines 1029-1044: Replace `handleCommentClick` function
   - After 1044: Add new functions

---

## Testing Checklist

- [ ] Load activity feed
- [ ] Verify comment badges show correct count (or load on click)
- [ ] Click comment button
- [ ] Comments section expands
- [ ] Comments load from API
- [ ] Comment count updates
- [ ] Add a new comment
- [ ] Count increments
- [ ] Delete a comment
- [ ] Count decrements

---

## Summary

The fix enables the comment badge to:
1. Show actual count initially (from database annotation)
2. Load comments when section is opened
3. Update counts when comments are added/deleted
4. Display full comments with proper formatting

This is a clean implementation that follows lazy-loading patterns and doesn't require additional API endpoints.
