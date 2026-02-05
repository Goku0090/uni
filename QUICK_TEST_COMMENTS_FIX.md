# Quick Test Guide: Comments Visibility Fix

## What Was Fixed
The comment system wasn't visible to other users because the frontend was calling the wrong API endpoints. All fetch requests have been updated from `/api/projects/...` to `/accounts/projects/...`

## Quick Test (5 minutes)

### Test Setup
1. Start Django server: `python manage.py runserver`
2. Open two browser windows/tabs (or use incognito for 2nd account)

### Test Procedure

**Window 1 (User A)**
- Login as first user (e.g., user@example.com)
- Go to any project: `http://localhost:8000/accounts/project-detail/1/`
- Scroll to Comments section
- Post a comment: "Test from User A"
- Verify it appears immediately

**Window 2 (User B)**
- Login as second user (e.g., user2@example.com)  
- Visit the same project URL
- Comments section should load
- You should see "Test from User A" comment
- Post a reply: "Response from User B"

**Back to Window 1**
- Refresh the page or wait for auto-load
- Both comments should be visible

---

## Troubleshooting

### Comments Not Loading?
1. Open Browser DevTools (F12)
2. Go to Network tab
3. Look for requests to `/accounts/projects/{id}/comments/`
4. Check response status (should be 200)

### 404 Error?
This means the URL is still wrong. Make sure you edited the file:
- `accounts/templates/includes/comment_section.html`

### CSRF Token Error?
- Make sure project_detail.html includes `{% csrf_token %}`
- It does (line 13)

### Comments Show But Can't Post?
1. Verify user is logged in
2. Check browser console for errors
3. Try refreshing the page

---

## What Changed

### File Modified
`accounts/templates/includes/comment_section.html`

### 4 Lines Changed
| Line | Before | After |
|------|--------|-------|
| 241 | `/api/projects/` | `/accounts/projects/` |
| 281 | `/api/projects/` | `/accounts/projects/` |
| 375 | `/api/comments/` | `/accounts/comments/` |
| 427 | `/api/comments/` | `/accounts/comments/` |

---

## Expected Behavior After Fix

✅ Comments load on page load
✅ Comments visible to all users (public projects)
✅ New comments appear immediately
✅ Users can edit own comments
✅ Users can delete own comments
✅ Project owner can delete any comment
✅ No 404 errors in console
✅ User avatars display correctly

---

## Production Deployment

After testing locally:

```bash
# 1. Commit changes
git add -A
git commit -m "Fix: Update comment API endpoints to use correct paths"

# 2. Push to production
git push

# 3. Restart server
# (depends on your deployment platform)
```

---

## Verification Commands

### Django Shell Check
```bash
python manage.py shell
>>> from accounts.models import Comment
>>> Comment.objects.count()  # Should show number of comments
>>> Comment.objects.first()  # Should show a comment object
```

### Database Query
```bash
# If using SQLite
sqlite3 db.sqlite3
SELECT COUNT(*) FROM accounts_comment;

# If using PostgreSQL
psql -U username -d database_name
SELECT COUNT(*) FROM accounts_comment;
```

---

## Notes

- No database changes needed
- No model changes needed
- No settings.py changes needed
- Only template/JavaScript fix
- Backwards compatible
- Can be deployed safely

---

## Files Changed Summary

### Modified Files
- `accounts/templates/includes/comment_section.html` ✅

### Files Verified (No changes needed)
- `accounts/comment_api.py` ✓
- `accounts/models.py` ✓
- `accounts/urls.py` ✓
- `accounts/views.py` ✓

---

## Support

If issues persist:
1. Check browser console (F12)
2. Look for 404/403 errors
3. Verify user is authenticated
4. Verify project exists
5. Check file was edited correctly
