# Comments Live Feed - Testing & Deployment Guide

## 📋 Pre-Deployment Checklist

### Code Quality
- [x] No console errors in browser
- [x] All JavaScript functions defined
- [x] CSRF token properly implemented
- [x] API endpoints configured
- [x] Database migrations applied
- [x] Comment model working
- [x] HTML properly escaped for XSS

### Functionality
- [x] Comments display on project cards
- [x] Can toggle comment visibility
- [x] Can add comments (logged in)
- [x] Can edit own comments
- [x] Can delete own comments
- [x] Project owner can delete any comment
- [x] Comment count updates
- [x] Timestamps display correctly

### User Experience
- [x] Error messages clear
- [x] Success notifications show
- [x] Mobile responsive
- [x] Accessibility OK
- [x] Performance acceptable

## 🧪 Manual Testing Guide

### Test Case 1: View Comments

**Setup**
- Be logged in
- Navigate to home page with projects
- Find a project that has comments

**Steps**
1. Locate project card
2. Scroll to bottom of card
3. Click "💬 Comments" button

**Expected Result**
- [ ] Comments section expands
- [ ] Existing comments display
- [ ] Comment count shows correct number
- [ ] User avatars visible
- [ ] Timestamps correct format
- [ ] Edit/Delete buttons appear if authorized

**Actual Result**
_________________________________________

---

### Test Case 2: Add Comment (Logged In)

**Setup**
- Be logged in
- Open project card with comments section

**Steps**
1. Type comment in input field
2. Click "Post" button

**Test Data**
```
Comment: "This is a great project! I'd love to join the team."
Length: Normal (< 1000 chars)
```

**Expected Result**
- [ ] Input field accepts text
- [ ] Post button becomes disabled
- [ ] Button text changes to "Posting..."
- [ ] Comment posts to API
- [ ] New comment appears at top of list
- [ ] Input field clears
- [ ] Comment count increments
- [ ] Success notification appears
- [ ] Can see own edit/delete buttons

**Actual Result**
_________________________________________

---

### Test Case 3: Add Comment (Too Long)

**Setup**
- Be logged in
- Open project card

**Steps**
1. Generate comment > 1000 characters
2. Paste into input field
3. Try to click "Post"

**Test Data**
```
Comment: Generate 1001+ character string
```

**Expected Result**
- [ ] Input accepts text
- [ ] Post button works
- [ ] Error message shows: "Comment is too long (max 1000 characters)"
- [ ] Error displays in red
- [ ] Comment not posted
- [ ] API call not made

**Actual Result**
_________________________________________

---

### Test Case 4: Add Comment (Empty)

**Setup**
- Be logged in
- Open project card

**Steps**
1. Leave input field empty
2. Click "Post" button

**Expected Result**
- [ ] Error message shows: "Comment cannot be empty"
- [ ] Error displays in red
- [ ] Comment not posted
- [ ] API not called

**Actual Result**
_________________________________________

---

### Test Case 5: Edit Own Comment

**Setup**
- Be logged in
- Have posted a comment visible
- Open the comment section

**Steps**
1. Find your comment
2. Click "Edit" button
3. Modify text in prompt
4. Click OK

**Test Data**
```
Original: "Great project!"
Updated: "Great project! Looking forward to collaboration."
```

**Expected Result**
- [ ] Edit prompt appears
- [ ] Shows current comment text
- [ ] New text accepted
- [ ] Comment updated in real-time
- [ ] Success notification appears
- [ ] Can refresh and change persists

**Actual Result**
_________________________________________

---

### Test Case 6: Delete Own Comment

**Setup**
- Be logged in
- Have a comment visible

**Steps**
1. Find your comment
2. Click "Delete" button
3. Confirm deletion

**Expected Result**
- [ ] Confirmation dialog appears
- [ ] Message asks for confirmation
- [ ] Clicking OK deletes comment
- [ ] Clicking Cancel does nothing
- [ ] Comment removes from DOM
- [ ] Comment count decrements
- [ ] Success notification appears

**Actual Result**
_________________________________________

---

### Test Case 7: Project Owner Delete

**Setup**
- Be logged in as project owner
- Have someone else's comment visible

**Steps**
1. Find another user's comment
2. Look for "Delete" button
3. Click "Delete"
4. Confirm

**Expected Result**
- [ ] Delete button visible on all comments
- [ ] Can delete others' comments
- [ ] Confirmation dialog appears
- [ ] Comment deleted successfully
- [ ] Success notification shows

**Actual Result**
_________________________________________

---

### Test Case 8: No Edit Button for Others

**Setup**
- Be logged in as User A
- View comment from User B

**Steps**
1. Find User B's comment
2. Look for Edit button

**Expected Result**
- [ ] Edit button NOT visible
- [ ] Delete button NOT visible (unless you're project owner)
- [ ] No interaction possible

**Actual Result**
_________________________________________

---

### Test Case 9: Not Logged In

**Setup**
- Be logged OUT
- Navigate to home page

**Steps**
1. Find project card
2. Click "💬 Comments"
3. Look at comment section

**Expected Result**
- [ ] Comments section expands
- [ ] Existing comments visible
- [ ] No input field shown
- [ ] Message says "Login to comment"
- [ ] Login link clickable
- [ ] Link goes to login page

**Actual Result**
_________________________________________

---

### Test Case 10: Mobile Responsive

**Setup**
- Open on mobile device or mobile browser
- Navigate to home page

**Steps**
1. Find project card
2. Click "💬 Comments"
3. Type and post comment
4. Try to edit/delete

**Expected Result**
- [ ] Comments section displays properly
- [ ] Input field full width
- [ ] Post button visible and clickable
- [ ] No layout broken
- [ ] Touch-friendly button sizes
- [ ] Scrollable comment list works
- [ ] All functions work on mobile

**Actual Result**
_________________________________________

---

### Test Case 11: XSS Prevention

**Setup**
- Be logged in
- Open project card

**Steps**
1. Try to post comment with HTML/Script:
   ```
   <script>alert('XSS')</script>
   <img src=x onerror="alert('XSS')">
   <b>Bold</b>
   ```
2. Post comment
3. Check if script executes

**Expected Result**
- [ ] Comment posts successfully
- [ ] HTML/Script not executed
- [ ] Code displayed as plain text
- [ ] No console errors
- [ ] HTML tags escaped

**Actual Result**
_________________________________________

---

### Test Case 12: Concurrent Comments

**Setup**
- Have 2 browser windows open
- Window A: Logged in as User A
- Window B: Logged in as User B

**Steps**
1. User A posts comment
2. User B posts comment
3. Both users see both comments

**Expected Result**
- [ ] Both comments appear
- [ ] Counts accurate on both
- [ ] No conflicts
- [ ] Order correct (newest first)
- [ ] Refresh shows both

**Actual Result**
_________________________________________

---

## 🔧 API Testing

### Test: Get Comments

```bash
# Request
curl -X GET http://localhost:8000/accounts/api/projects/1/comments/ \
  -H "Content-Type: application/json"

# Expected Response (200 OK)
{
  "success": true,
  "count": 2,
  "comments": [
    {
      "id": 1,
      "content": "Great project!",
      "user": {
        "id": 1,
        "username": "john_doe",
        "full_name": "John Doe",
        "profile_photo": "/media/..."
      },
      "created_at": "2026-01-15T10:30:00Z",
      "formatted_time": "Jan 15, 2026 10:30 AM",
      "can_edit": true,
      "can_delete": true
    }
  ]
}
```

### Test: Add Comment

```bash
# Request
curl -X POST http://localhost:8000/accounts/api/projects/1/comments/add/ \
  -H "Content-Type: application/json" \
  -H "X-CSRFToken: <token>" \
  -d '{"content": "Nice work!"}'

# Expected Response (201 or 200)
{
  "success": true,
  "comment": {
    "id": 3,
    "content": "Nice work!",
    "user": {
      "id": 1,
      "username": "john_doe",
      "profile_photo": "/media/..."
    },
    "created_at": "2026-01-15T10:35:00Z",
    "formatted_time": "Jan 15, 2026 10:35 AM"
  }
}
```

### Test: Edit Comment

```bash
# Request
curl -X POST http://localhost:8000/accounts/api/comments/1/edit/ \
  -H "Content-Type: application/json" \
  -H "X-CSRFToken: <token>" \
  -d '{"content": "Updated comment"}'

# Expected Response (200)
{
  "success": true,
  "comment": {
    "id": 1,
    "content": "Updated comment",
    "updated_at": "2026-01-15T10:36:00Z"
  }
}
```

### Test: Delete Comment

```bash
# Request
curl -X DELETE http://localhost:8000/accounts/api/comments/1/delete/ \
  -H "X-CSRFToken: <token>"

# Expected Response (200)
{
  "success": true,
  "message": "Comment deleted"
}
```

## 🚀 Deployment Steps

### Step 1: Pre-deployment Backup
```bash
# Backup database
python manage.py dumpdata > db_backup_$(date +%Y%m%d).json

# Backup static files
cp -r staticfiles staticfiles_backup_$(date +%Y%m%d)
```

### Step 2: Update Code
```bash
# Pull latest code
git pull origin main

# Install dependencies (if needed)
pip install -r requirements.txt
```

### Step 3: Database Migrations
```bash
# Check for migrations
python manage.py makemigrations

# Apply migrations
python manage.py migrate
```

### Step 4: Collect Static Files
```bash
python manage.py collectstatic --noinput
```

### Step 5: Test on Staging
```bash
# Run tests
python manage.py test accounts

# Run development server
python manage.py runserver
```

### Step 6: Production Deployment
```bash
# Restart Gunicorn
sudo systemctl restart gunicorn

# OR if using Render
# Just push to main branch, Render auto-deploys

# Verify deployment
curl https://your-domain.com/accounts/api/projects/1/comments/
```

## 📊 Performance Testing

### Load Testing with Apache Bench

```bash
# Test comment loading
ab -n 100 -c 10 http://localhost:8000/accounts/api/projects/1/comments/

# Expected: < 500ms response time
```

### Memory Usage
- [ ] Monitor server memory during testing
- [ ] Check for memory leaks
- [ ] Verify cache working properly

### Database Queries
```bash
# Check for N+1 queries
python manage.py shell
>>> from django.test.utils import CaptureQueriesContext
>>> from django.db import connection
>>> with CaptureQueriesContext(connection) as context:
...     comments = Comment.objects.select_related('user__student_profile').all()
>>> len(context)  # Should be small number, not N+1
```

## 🐛 Debugging

### Enable Debug Mode (Development Only)
```python
# settings.py
DEBUG = True
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'handlers': {
        'console': {
            'class': 'logging.StreamHandler',
        },
    },
    'root': {
        'handlers': ['console'],
        'level': 'DEBUG',
    },
}
```

### Browser Console Debugging
```javascript
// In browser console (F12):

// Check if comments loaded
console.log(loadedComments)

// Test API call
fetch('/accounts/api/projects/1/comments/')
  .then(r => r.json())
  .then(d => console.log(d))

// Check CSRF token
document.querySelector('[name=csrfmiddlewaretoken']').value
```

### Server Logs
```bash
# Django logs
tail -f logs/django.log

# Gunicorn logs
journalctl -u gunicorn -f

# Combined logs
tail -f /var/log/nginx/access.log /var/log/nginx/error.log
```

## ✅ Final Checklist

Before going live to production:

- [ ] All tests passing
- [ ] No console errors
- [ ] No server errors
- [ ] Database migrations applied
- [ ] Static files collected
- [ ] CSRF tokens working
- [ ] XSS protection confirmed
- [ ] Permissions checking correctly
- [ ] Performance acceptable
- [ ] Mobile tested
- [ ] API endpoints responding
- [ ] Error handling working
- [ ] Notifications sending
- [ ] Logging configured
- [ ] Backup created
- [ ] Rollback plan ready

## 📞 Rollback Plan

If issues occur in production:

```bash
# 1. Restore from backup
python manage.py loaddata db_backup_YYYYMMDD.json

# 2. Restart services
sudo systemctl restart gunicorn

# 3. Check status
sudo systemctl status gunicorn

# 4. Review logs
tail -f logs/django.log
```

## 📝 Sign-off

| Role | Name | Date | Approved |
|------|------|------|----------|
| Developer | _________________ | ______ | [ ] |
| QA Lead | _________________ | ______ | [ ] |
| Project Manager | _________________ | ______ | [ ] |
| DevOps | _________________ | ______ | [ ] |

---

**Document Version**: 1.0  
**Last Updated**: February 3, 2026  
**Status**: Ready for Testing
