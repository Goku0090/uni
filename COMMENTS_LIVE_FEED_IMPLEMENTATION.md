# Comments Section in Live Feed - Implementation Guide

## Overview
The comment section has been successfully integrated into the live feed (main_home page) where projects are displayed. Users can now comment directly on project cards without needing to visit the project detail page.

## What Was Added

### 1. **HTML Structure** (main_home.html)
Added a comments section to each project card with:

```html
<!-- Comments Section -->
<div class="border-t border-gray-600 pt-4">
    <!-- Comments Counter & Toggle -->
    <button onclick="toggleComments({{ post.id }}, this)" class="text-sm font-semibold text-accent hover:text-accent/80 mb-3 flex items-center gap-2 transition-colors">
        <svg class="w-4 h-4" fill="currentColor" viewBox="0 0 20 20">
            <path d="M2 5a2 2 0 012-2h12a2 2 0 012 2v10a2 2 0 01-2 2H4a2 2 0 01-2-2V5z"></path>
            <path d="M15 7H5"></path>
        </svg>
        💬 Comments <span class="comment-count-{{ post.id }} text-gray-400 text-xs">(0)</span>
    </button>

    <!-- Comments Container (Initially Hidden) -->
    <div class="comments-container-{{ post.id }} hidden max-h-64 overflow-y-auto space-y-3 mb-3 bg-gray-800/30 rounded-lg p-3">
        <div class="comments-list-{{ post.id }} space-y-3">
            <!-- Comments loaded here via JS -->
        </div>
    </div>

    <!-- Add Comment Form (Only for logged-in users) -->
    {% if user.is_authenticated %}
    <div class="add-comment-form-{{ post.id }} bg-gray-800/50 rounded-lg p-3">
        <div class="flex gap-2">
            <input type="text" placeholder="Add a comment..." class="flex-1 px-3 py-2 bg-gray-700 border border-gray-600 rounded-lg text-white text-sm placeholder-gray-400 focus:outline-none focus:ring-2 focus:ring-accent comment-input-{{ post.id }}" maxlength="1000">
            <button onclick="submitComment({{ post.id }}, this)" class="px-4 py-2 bg-accent hover:bg-accent/80 text-white rounded-lg font-semibold text-sm transition-colors">
                Post
            </button>
        </div>
        <div class="comment-error-{{ post.id }} text-red-400 text-xs mt-2 hidden"></div>
    </div>
    {% else %}
    <div class="bg-gray-800/50 rounded-lg p-3 text-center">
        <p class="text-gray-400 text-sm"><a href="{% url 'login' %}" class="text-accent hover:text-accent/80 font-semibold">Login</a> to comment</p>
    </div>
    {% endif %}
</div>
```

### 2. **JavaScript Functions** (in main_home.html)

#### `toggleComments(projectId, button)`
- **Purpose**: Toggle comment section visibility
- **Action**: Shows/hides the comments container and loads comments when needed

#### `loadCommentsIfNeeded(projectId)`
- **Purpose**: Fetch comments from the API (lazy loading)
- **API Call**: `GET /accounts/api/projects/<project_id>/comments/`
- **Response**: Returns array of comments with user info and timestamps

#### `createCommentElement(comment, projectId)`
- **Purpose**: Render individual comment HTML
- **Features**:
  - User profile photo or avatar
  - Username and timestamp
  - Edit button (if user owns comment)
  - Delete button (if user owns comment or is project owner)
  - HTML-escaped content for security

#### `submitComment(projectId, button)`
- **Purpose**: Post a new comment
- **Validation**: 
  - Checks if comment is not empty
  - Enforces 1000 character limit
- **API Call**: `POST /accounts/api/projects/<project_id>/comments/add/`
- **After Success**:
  - Clears input field
  - Adds new comment to the top of list
  - Updates comment count
  - Shows success notification

#### `deleteComment(commentId, projectId)`
- **Purpose**: Remove a comment
- **Confirmation**: Asks user to confirm before deleting
- **API Call**: `DELETE /accounts/api/comments/<comment_id>/delete/`
- **After Success**: Removes comment element and updates count

#### `editComment(commentId, currentContent, projectId)`
- **Purpose**: Update comment text
- **Method**: Uses browser `prompt()` for simple editing
- **API Call**: `POST /accounts/api/comments/<comment_id>/edit/`
- **Validation**: 1000 character limit

#### `escapeHtml(text)`
- **Purpose**: Prevent XSS attacks by escaping HTML characters
- **Escapes**: `& < > " '`

### 3. **API Endpoints Used**

All endpoints are already configured in `accounts/urls.py`:

```python
# Get comments
path('api/projects/<int:project_id>/comments/', get_comments, name='get-comments'),

# Add comment
path('api/projects/<int:project_id>/comments/add/', add_comment, name='add-comment'),

# Delete comment
path('api/comments/<int:comment_id>/delete/', delete_comment, name='delete-comment'),

# Edit comment
path('api/comments/<int:comment_id>/edit/', edit_comment, name='edit-comment'),
```

### 4. **Backend (comment_api.py)**

**Functions Already Implemented:**

1. **`add_comment(request, project_id)`**
   - Creates comment with user validation
   - Creates activity log entry
   - Sends notification to project owner
   - Returns comment data with user info

2. **`get_comments(request, project_id)`**
   - Fetches all comments for a project
   - Includes user profile photo data
   - Sets edit/delete permissions per comment

3. **`delete_comment(request, comment_id)`**
   - Verifies user owns comment or is project owner
   - Deletes comment from database

4. **`edit_comment(request, comment_id)`**
   - Verifies user owns comment
   - Updates comment content
   - Validates 1000 character limit

## Features

### ✅ Implemented
- [x] Toggle comments visibility on project cards
- [x] Lazy load comments when section is opened
- [x] Display comment count
- [x] Add comments without leaving the feed
- [x] Edit your own comments
- [x] Delete comments (own or if project owner)
- [x] User profile photos in comments
- [x] Timestamps on comments
- [x] Error handling and validation
- [x] XSS prevention (HTML escaping)
- [x] Login requirement for commenting
- [x] Real-time UI updates
- [x] CSRF protection
- [x] Success/error notifications

### 🎨 Design Features
- Dark theme with accent colors
- Smooth transitions and animations
- Responsive design
- Overflow scrolling for long comment lists (max-h-64)
- Visual feedback (disabled buttons, loading states)
- Comment counter badge
- Inline edit/delete buttons

## Usage Flow

### For Users (Logged In)
1. View project card in live feed
2. Click "💬 Comments" button
3. Comments load automatically
4. Type comment in input field
5. Click "Post" button
6. Comment appears at top of list
7. Can edit or delete own comments

### For Anonymous Users
- Can view comments
- Prompted to login to comment
- Login link provided in comment section

## Technical Details

### Permissions
- **Add Comment**: Any logged-in user
- **Edit Comment**: Comment owner only
- **Delete Comment**: Comment owner or project owner

### Validation
- Comment text: 1-1000 characters
- XSS prevention: HTML escaping
- CSRF protection: Token validation

### Database
- Uses existing `Comment` model
- Related to `Project` and `User`
- Tracks `created_at` and `updated_at`

### Performance
- Lazy loading (comments only fetch when opened)
- Comment count cached in UI
- Single API call per project when opened

## Testing

### Test Cases
1. **Add Comment**
   - Valid comment posts successfully
   - Empty comment shows error
   - Long comment (>1000 chars) shows error
   - Count updates correctly

2. **Load Comments**
   - Comments display with correct user info
   - Timestamps format correctly
   - Edit/delete buttons appear conditionally

3. **Edit Comment**
   - Own comment can be edited
   - Other's comment cannot be edited
   - Content updates in real-time

4. **Delete Comment**
   - Confirmation dialog appears
   - Comment removed from list
   - Count decrements

5. **Authentication**
   - Non-logged users see login link
   - Logged users see input field
   - Invalid tokens handled gracefully

## Styling Reference

### Color Scheme
- Background: `bg-gray-800/30`, `bg-gray-800/50`
- Text: `text-white`, `text-gray-200`, `text-gray-400`
- Accent: `text-accent` (cyan #3AB7BF)
- Errors: `text-red-400`
- Edit: `text-blue-400`

### Spacing
- Padding: `p-3`
- Gaps: `gap-2`
- Max height: `max-h-64` (scrollable)

### Responsive
- Full width on mobile
- Inline editing on desktop
- Touch-friendly button sizes

## Future Enhancements

1. **Nested Comments/Replies**
   - Add `reply_to` field reference
   - Indent nested comments
   - Threading UI

2. **Comment Reactions**
   - Add emoji reactions
   - Like/upvote comments
   - Show reaction counts

3. **Rich Text Editor**
   - Markdown support
   - Code blocks
   - Link previews

4. **Advanced Filtering**
   - Sort by newest/oldest/popular
   - Filter by commenter
   - Search comments

5. **Moderation**
   - Flag inappropriate comments
   - Admin review queue
   - Block users

6. **Real-time Updates**
   - WebSocket integration
   - Instant notifications
   - Live comment feeds

## Files Modified

1. **accounts/templates/main_home.html**
   - Added HTML structure for comments
   - Added JavaScript functions
   - Added event handlers

## Files Already Configured

1. **accounts/comment_api.py** - Comment API endpoints
2. **accounts/models.py** - Comment model definition
3. **accounts/urls.py** - API route configuration

## Troubleshooting

### Comments not loading
- Check browser console for errors
- Verify CSRF token in page source
- Check API response in Network tab

### Edit/Delete buttons not showing
- Verify user is logged in
- Check user ID matches comment owner
- Check if user is project owner

### Character limit validation
- Frontend: 1000 character limit on input
- Backend: Additional validation in API
- Error message displays if exceeded

## Security Considerations

1. **CSRF Protection**: All POST/DELETE requests require token
2. **XSS Prevention**: HTML escaping on all comment content
3. **Permission Checks**: Backend validates edit/delete permissions
4. **Input Validation**: 
   - Character length limit
   - Non-empty validation
   - HTML tag stripping

## Performance Metrics

- Comment fetch: One API call per project (lazy loaded)
- Comment render: O(n) where n = number of comments
- Memory: Minimal (stores loaded comments in dictionary)
- Network: ~1-2KB per comment

---

**Implementation Date**: February 2026
**Status**: ✅ Complete and Tested
**Last Updated**: 2026-02-03
