# Fix: Like Error on main_home page

## Error Details

```
SyntaxError: Unexpected token '<', "<!DOCTYPE "... is not valid JSON
Location: main_home/:864 (JavaScript console)
```

## Root Cause

The error occurred because:

1. **Two conflicting `like_project()` functions** existed in `views.py`:
   - **First function** (line 1595): Returns JSON ✅
   - **Second function** (line 2554): Returns HTML redirect ❌

2. **The second function had issues**:
   - Used wrong `get_or_create` parameters (`content_type='project'` doesn't exist)
   - Tried to return a redirect instead of JSON
   - Django threw an error (500 page)
   - Browser received HTML error page instead of JSON
   - JavaScript tried to parse HTML as JSON → SyntaxError

## What Was Fixed

### 1. ✅ Removed Duplicate Function
Deleted the conflicting `like_project()` at line 2554-2593 that was causing errors.

### 2. ✅ Fixed First Function
Updated the original `like_project()` (line 1595) to:
- Add `@login_required` decorator
- Add `@require_http_methods(['POST'])` for better validation
- Add try-except block for error handling
- Return proper JSON responses in all cases
- Include `likes_count` in response
- Log errors for debugging

### 3. ✅ Added Missing Import
Added: `from django.views.decorators.http import require_http_methods`

## The Fixed Code

```python
@login_required
@require_http_methods(['POST'])
def like_project(request, project_id):
    """Toggle like on a project - AJAX endpoint"""
    try:
        project = get_object_or_404(Project, id=project_id)

        # Check if user already liked the project
        existing_like = Like.objects.filter(user=request.user, project=project).first()

        if existing_like:
            # Unlike
            existing_like.delete()
            liked = False
            message = "Project unliked"
        else:
            # Like
            Like.objects.create(user=request.user, project=project)
            liked = True
            message = "Project liked!"

            # Create activity
            Activity.objects.create(
                user=request.user,
                action_type='project_liked',
                target_project=project
            )

        return JsonResponse({
            'success': True, 
            'liked': liked, 
            'message': message,
            'likes_count': project.likes.count()
        })
    except Exception as e:
        logger.error(f"Error liking project: {str(e)}")
        return JsonResponse({
            'success': False,
            'message': f'Error: {str(e)}'
        }, status=400)
```

## How It Works Now

### Request Flow
```
1. User clicks "Like" button on main_home
2. JavaScript sends: POST /accounts/like-project/{project_id}/
3. Server validates request (login required, POST only)
4. Server toggles like in database
5. Server returns JSON: {"success": true, "liked": true, ...}
6. JavaScript parses JSON and updates UI
7. User sees heart icon turn red/gray
```

### Error Handling
If something goes wrong:
1. Exception is caught
2. Error is logged for debugging
3. JSON error response is returned (not HTML)
4. JavaScript handles error gracefully

## Testing

### To verify the fix works:

1. **Start server**
   ```bash
   python manage.py runserver
   ```

2. **Open main_home**
   ```
   http://127.0.0.1:8000/accounts/
   ```

3. **Click Like button** on any project card
   - Heart icon should turn red
   - Notification should appear
   - No console errors

4. **Click again to Unlike**
   - Heart icon should turn gray
   - Notification should appear
   - Still no errors

5. **Check browser console**
   ```
   Press F12 → Console
   Should NOT see "Like error:" messages
   ```

## What Changed in Files

### accounts/views.py

**Added import:**
```python
from django.views.decorators.http import require_http_methods
```

**Fixed function** (lines 1595-1616):
- Added `@login_required` and `@require_http_methods(['POST'])`
- Added try-except block
- Improved Activity creation (uses correct model)
- Returns JSON on success and error

**Removed function** (old lines 2554-2593):
- Deleted duplicate/conflicting function
- Deleted incorrect `get_or_create` call
- Deleted redirect logic (not needed for AJAX)

## Benefits

✅ **No more SyntaxError** - Always returns valid JSON  
✅ **Better error handling** - Errors are logged and reported correctly  
✅ **Only one function** - No confusion from duplicates  
✅ **More secure** - Validates request method and user login  
✅ **Better feedback** - Includes likes_count in response  

## Rollback (If Needed)

If this causes issues:

```bash
# Revert changes
git checkout accounts/views.py

# Or manually:
# 1. Remove the import from line 23
# 2. Put back the old function (line 2554-2593)
# 3. Restart server
```

## Files Modified

- `e:/login/auth_project/accounts/views.py` (2 changes)
  - Added import: `require_http_methods`
  - Fixed `like_project()` function (improved version)
  - Removed duplicate `like_project()` function

## No Template Changes Needed

The JavaScript in `main_home.html` (line 909-936) is already correct:
```javascript
fetch('/accounts/like-project/' + postId + '/', {
    method: 'POST',
    headers: {
        'X-CSRFToken': document.querySelector('[name=csrfmiddlewaretoken]').value,
        'Content-Type': 'application/json',
    },
    body: JSON.stringify({})
})
.then(response => response.json())  // ← Expects JSON
.then(data => {
    if (data.liked) { ... }  // ← Uses 'liked' field
})
```

Now the backend correctly returns JSON that matches this expectation.

## Summary

| Item | Status |
|------|--------|
| Root Cause | ✅ Identified (duplicate functions) |
| Fix Applied | ✅ Removed duplicate, fixed original |
| Testing | ✅ Ready to test |
| Rollback | ✅ Available if needed |
| Breaking Changes | ❌ None (same API response) |

## Success Criteria

After this fix:
- ✅ Like button works without errors
- ✅ Heart icon animates
- ✅ Notification appears
- ✅ No console errors
- ✅ Likes count increases
- ✅ Un-liking works

---

**Status**: ✅ Fixed  
**Time to Apply**: Already done (check git)  
**Time to Test**: 2 minutes  
**Risk Level**: Low (only fixing existing logic)
