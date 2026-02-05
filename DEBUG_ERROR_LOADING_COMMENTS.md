# 🔧 DEBUG: "Error Loading Comments" - Solutions

**Status:** Debugging Guide  
**Date:** February 3, 2025

---

## The Error Message

When viewing a project, users see:
```
⚠️ Failed to load comments
```

The comment section appears but shows an error instead of comments.

---

## Common Causes (In Order of Likelihood)

### Cause #1: Server Not Restarted ⭐ MOST COMMON

**Symptom:** Fix was applied but comments still show error

**Solution:**
```bash
# Stop the server (Ctrl+C in terminal)

# Wait 2 seconds

# Restart the server
python manage.py runserver

# OR if using different server:
# pkill -f "python manage.py"
# python manage.py runserver
```

**Why:** Django caches URL routing. The old routes are still in memory until restart.

---

### Cause #2: Browser Cache

**Symptom:** Comments worked, then error started, or error won't go away

**Solution:**

**Option A - Clear Cache:**
1. Press `Ctrl+Shift+Delete` (Windows) or `Cmd+Shift+Delete` (Mac)
2. Select "All time"
3. Check "Cookies and other site data" and "Cached images and files"
4. Click "Delete data"
5. Reload page

**Option B - Use Incognito/Private Mode:**
1. Press `Ctrl+Shift+N` (Chrome) or `Ctrl+Shift+P` (Firefox)
2. Navigate to the project
3. Check if comments work

**Option C - Hard Refresh:**
1. Press `Ctrl+Shift+R` (Windows) or `Cmd+Shift+R` (Mac)
2. This forces browser to get fresh version

---

### Cause #3: 404 Error (Wrong URL)

**Symptom:** Network tab shows 404 on comment requests

**Solution - Check the URL:**

1. **Open DevTools:** F12
2. **Go to Network tab**
3. **Load the project page**
4. **Look for requests** containing "comments"
5. **Check the URL:**

**Should be:** `http://localhost:8000/api/projects/1/comments/`  
**NOT:** `http://localhost:8000/api/api/projects/1/comments/`  
**NOT:** `http://localhost:8000/accounts/api/projects/1/comments/`

**If URL is wrong:**
- The template might be hardcoding wrong URL
- OR the fix wasn't properly applied
- Check: `e:/login/auth_project/accounts/urls.py` line 125
- Should have: `path('projects/<int:project_id>/comments/', ...)`
- NOT: `path('api/projects/<int:project_id>/comments/', ...)`

---

### Cause #4: CSRF Token Error

**Symptom:** 403 Forbidden error in Network tab

**Solution:**

The template includes CSRF token, so this is unlikely but check:

```html
<!-- In comment_section.html -->
{% csrf_token %}
```

Should be in the form. If missing, add it:

```html
<form class="comment-form" data-project-id="{{ project.id }}">
    {% csrf_token %}  <!-- MUST BE HERE -->
    <textarea ...></textarea>
    ...
</form>
```

---

### Cause #5: Not Authenticated

**Symptom:** Comments form doesn't show for unauthenticated users

**Solution:**
1. Make sure you're **logged in**
2. Check that your session cookie exists:
   - DevTools → Application → Cookies
   - Look for `sessionid` cookie
   - If missing, you're not logged in

---

### Cause #6: Project Doesn't Exist

**Symptom:** 404 error for specific projects

**Solution:**
```bash
python manage.py shell
>>> from accounts.models import Project
>>> Project.objects.all().count()
>>> Project.objects.filter(id=1)  # Check if project exists
```

---

### Cause #7: Permission Denied (403)

**Symptom:** 403 error in Network tab when fetching comments

**Solution:**

This shouldn't happen since `get_comments()` doesn't have permission checks. But if it does:

Check `comment_api.py` line 109:
```python
@login_required  # Must be logged in
def get_comments(request, project_id):
```

Make sure you're logged in.

---

### Cause #8: Server Error (500)

**Symptom:** 500 error in Network tab

**Solution:**

Check the server terminal for error messages:
```
Internal Server Error: /api/projects/1/comments/
Traceback (most recent call last):
  File "...", line XXX, in get_comments
    ...
```

**Common 500 errors:**

**Error: Project matching query does not exist**
```python
project = Project.objects.get(id=project_id)  # Line 115
```

Solution: Project with that ID doesn't exist. Use valid project ID.

**Error: Exception accessing student_profile**
```python
if comment.user.student_profile.profile_photo:  # Line 129
```

Solution: User doesn't have a StudentProfile. Usually auto-created, but if not:
```bash
python manage.py shell
>>> from accounts.models import StudentProfile
>>> from django.contrib.auth.models import User
>>> user = User.objects.first()
>>> StudentProfile.objects.get_or_create(user=user)
```

---

## Step-by-Step Debugging

### Step 1: Verify Fix Was Applied

```bash
grep "path('projects/<int:project_id>/comments/" e:/login/auth_project/accounts/urls.py
```

Should show lines WITHOUT `/api/` prefix in path definition.

If it shows `/api/projects/<int:project_id>/comments/`, the fix wasn't applied!

### Step 2: Restart Server

```bash
# In terminal running Django
Ctrl+C  # Stop server

# Wait 2 seconds

python manage.py runserver  # Restart
```

### Step 3: Clear Browser Cache

- Ctrl+Shift+Delete (Windows)
- Clear all
- Reload page

### Step 4: Open DevTools and Check Network

1. **Press F12** to open DevTools
2. **Click "Network" tab**
3. **Reload the page**
4. **Look for requests** to `/api/projects/X/comments/`
5. **Check the response:**
   - **200 OK** = ✅ Success
   - **404** = ❌ URL wrong or endpoint doesn't exist
   - **403** = ❌ Not authenticated
   - **500** = ❌ Server error

### Step 5: Check Response Data

If request succeeds (200), click on it and check the response:

**Should look like:**
```json
{
  "success": true,
  "count": 2,
  "comments": [
    {
      "id": 1,
      "content": "Great project!",
      "user": {
        "id": 1,
        "username": "user1",
        "full_name": "User One",
        "profile_photo": "..."
      },
      "created_at": "2025-02-03T...",
      ...
    }
  ]
}
```

### Step 6: Check Browser Console

1. **DevTools → Console tab**
2. Look for errors like:
   - `Failed to load comments`
   - `404 Not Found`
   - Any red error messages
3. Check what the actual error says

### Step 7: Check Server Logs

If you see errors in browser, check the Django server terminal for stack traces.

---

## Quick Fix Checklist

- [ ] **Restart server** (Ctrl+C then run again)
- [ ] **Clear browser cache** (Ctrl+Shift+Delete)
- [ ] **Use incognito window** (Ctrl+Shift+N)
- [ ] **Check Network tab** for 404 or 500 errors
- [ ] **Verify fix applied** (grep for correct path)
- [ ] **Check logged in** (look for sessionid cookie)
- [ ] **Try different project** (in case that project has issues)
- [ ] **Try different browser** (Firefox/Chrome/Edge)

---

## Common Error Messages & Fixes

### Error: "Failed to load comments"

**Check:**
1. Network tab shows 404? → Check URL format (Cause #3)
2. Network tab shows 500? → Check server logs (Cause #8)
3. Network tab shows 403? → Log in (Cause #5)
4. Network request succeeds but still error? → Browser cache (Cause #2)

### Error: "Cannot read property 'comments' of undefined"

**Cause:** API response is not JSON  
**Fix:** Check if response is actually JSON in Network tab

### Error: "TypeError: comments is not iterable"

**Cause:** API returned error object instead of array  
**Fix:** Check API response format in Network tab

---

## Testing Template

Use this to systematically test:

```html
<!-- Manual test in browser console -->
<script>
// Test the API endpoint directly
fetch('/api/projects/1/comments/')
  .then(r => r.json())
  .then(data => {
    console.log('Success!', data);
    console.log('Comment count:', data.count);
    console.log('Comments:', data.comments);
  })
  .catch(err => {
    console.error('Error:', err);
  });
</script>
```

Run this in browser console (F12 → Console tab → Paste → Enter)

Should show:
- `Success! {success: true, count: X, comments: [...]}`

If error:
- `Error: ...` → Check what the error says

---

## Permanent Solution Checklist

After fixing the error, verify:

- [ ] Comments appear for the user who posted them
- [ ] Other users (incognito/different browser) see the comment
- [ ] Comment count updates correctly
- [ ] Refresh doesn't lose comments
- [ ] Delete button works
- [ ] Edit button works
- [ ] Works on different projects
- [ ] No console errors in DevTools
- [ ] Network tab shows all requests as 200

---

## If Still Not Working

### Escalation Path

1. **Check Django logs:**
   ```bash
   tail -f e:/login/auth_project/logs/django.log
   ```

2. **Run Django check:**
   ```bash
   python manage.py check
   ```

3. **Check database:**
   ```bash
   python manage.py shell
   >>> from accounts.models import Comment, Project
   >>> Project.objects.all().count()
   >>> Comment.objects.all().count()
   ```

4. **Test API directly:**
   ```bash
   curl -X GET "http://localhost:8000/api/projects/1/comments/"
   ```

5. **Check URL resolution:**
   ```bash
   python manage.py shell
   >>> from django.urls import resolve
   >>> resolve('/api/projects/1/comments/')
   ```

---

## Most Likely Solution

**99% of the time, the solution is:**

```bash
# Stop server
Ctrl+C

# Clear browser cache
# Ctrl+Shift+Delete

# Restart server
python manage.py runserver
```

**Try this first before checking anything else!**

---

*Debugging guide created: February 3, 2025*
