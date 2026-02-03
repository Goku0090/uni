# Live Feed Comments - Quick Reference Guide

## What Was Added

### 1. **Backend Files Created**
- `accounts/comment_api.py` - REST API endpoints for comments
- `accounts/forms.py` - Added `CommentForm` class
- `accounts/urls.py` - Added 4 new API routes
- `accounts/templates/includes/comment_section.html` - Reusable comment component

### 2. **API Endpoints**

| Method | Endpoint | Purpose |
|--------|----------|---------|
| GET | `/accounts/api/projects/<id>/comments/` | Fetch all comments |
| POST | `/accounts/api/projects/<id>/comments/add/` | Add new comment |
| DELETE | `/accounts/api/comments/<id>/delete/` | Delete comment |
| PUT | `/accounts/api/comments/<id>/edit/` | Edit comment |

### 3. **Database Model (Already Exists)**
```python
class Comment(models.Model):
    user = ForeignKey(User)
    project = ForeignKey(Project)
    content = TextField()
    created_at = DateTimeField(auto_now_add=True)
    updated_at = DateTimeField(auto_now=True)
```

---

## How to Use

### **In Any Template**

```html
{% include 'includes/comment_section.html' with project=project %}
```

### **Example Integration**

**In activity_feed.html:**
```html
{% if activity.project %}
    <!-- Project card -->
    <div class="project-card">
        <h5>{{ activity.project.title }}</h5>
        <p>{{ activity.project.description }}</p>
        
        <!-- ADD THIS LINE -->
        {% include 'includes/comment_section.html' with project=activity.project %}
    </div>
{% endif %}
```

**In project_detail.html:**
```html
<div class="project-details">
    <!-- Project info -->
    ...
    
    <!-- ADD THIS LINE -->
    {% include 'includes/comment_section.html' with project=project %}
</div>
```

---

## Features at a Glance

✅ **Users Can:**
- Comment without connecting
- Edit their own comments
- Delete their own comments
- See other users' comments

✅ **Project Owners Can:**
- Delete any comment on their project
- Receive notifications when someone comments

✅ **Built-in:**
- Real-time comment loading
- Character counter (1000 max)
- User avatars and profiles
- Timestamps
- Error handling
- Loading spinners
- Success/error messages

---

## API Response Examples

### Get Comments
```json
{
  "success": true,
  "count": 3,
  "comments": [
    {
      "id": 1,
      "content": "Great project!",
      "user": {
        "id": 5,
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

### Add Comment
```json
{
  "success": true,
  "comment": {
    "id": 4,
    "content": "Love this!",
    "user": {
      "id": 1,
      "username": "john",
      "profile_photo": "/media/profile_photos/john.jpg"
    },
    "created_at": "2024-01-15T11:00:00Z",
    "formatted_time": "Jan 15, 2024 11:00 AM"
  }
}
```

---

## Testing the Feature

### 1. **Via Browser**
1. Go to activity feed or project detail page
2. Scroll to comment section
3. Type a comment
4. Click "Post"
5. Comment appears instantly
6. Try editing and deleting

### 2. **Via API (cURL)**
```bash
# Get comments
curl http://localhost:8000/accounts/api/projects/1/comments/

# Add comment
curl -X POST http://localhost:8000/accounts/api/projects/1/comments/add/ \
  -H "Content-Type: application/json" \
  -H "X-CSRFToken: YOUR_TOKEN" \
  -d '{"content": "Amazing!"}'

# Delete comment
curl -X DELETE http://localhost:8000/accounts/api/comments/5/delete/ \
  -H "X-CSRFToken: YOUR_TOKEN"
```

---

## Styling Customization

The component uses Bootstrap 5 classes. To customize:

**In comment_section.html template:**
```html
<!-- Change the card styling -->
<div class="card border-light">  <!-- Change to border-primary, etc. -->

<!-- Change the button color -->
<button class="btn btn-primary">Post</button>  <!-- Change to btn-success, etc. -->

<!-- Modify colors in the <style> section -->
<style>
  .comment-item {
    border-left: 3px solid #007bff;  /* Change color */
    background-color: #f8f9fa;        /* Change background */
  }
</style>
```

---

## Permissions & Security

| Action | User | Project Owner | Anonymous |
|--------|------|---------------|-----------|
| View comments | ✅ | ✅ | ✅ |
| Add comment | ✅ | ✅ | ❌ |
| Edit own comment | ✅ | ✅ | - |
| Delete own comment | ✅ | ✅ | - |
| Delete any comment | - | ✅ | - |

---

## Error Handling

All errors are caught and displayed as friendly messages:

- "Comment cannot be empty"
- "Comment too long (max 1000 characters)"
- "Project not found"
- "Comment not found"
- "Permission denied"
- "Failed to add comment"
- "Failed to delete comment"
- "Failed to edit comment"

---

## Database Queries Used

**Optimized for performance:**
```python
# Get comments with related user profile
Comment.objects.filter(project=project).select_related(
    'user__student_profile'
).order_by('-created_at')
```

---

## Common Issues & Solutions

### **Issue: Comments not loading**
**Solution:** Check browser console for errors. Make sure CSRF token is in template.

### **Issue: "Permission denied" error**
**Solution:** Only comment author or project owner can delete. Check who's logged in.

### **Issue: Comment section not appearing**
**Solution:** Make sure template include line is correct:
```html
{% include 'includes/comment_section.html' with project=project %}
```

### **Issue: No profile photos showing**
**Solution:** Check StudentProfile.profile_photo file exists and is accessible.

---

## Files Modified/Created

```
✅ Created:
  - accounts/comment_api.py
  - accounts/templates/includes/comment_section.html
  - LIVE_FEED_COMMENTS_IMPLEMENTATION.md

✏️ Modified:
  - accounts/forms.py (added CommentForm)
  - accounts/urls.py (added 4 API routes)

📦 Already Existed:
  - accounts/models.py (Comment model)
```

---

## Next Steps

1. ✅ Copy `comment_section.html` template to correct location
2. ✅ Add comment_api.py to accounts app
3. ✅ Update urls.py with new routes
4. ✅ Add form import to forms.py
5. ✅ Include `{% include 'includes/comment_section.html' with project=project %}` in your feed/detail templates
6. ✅ Test locally
7. ✅ Deploy to production

---

## Performance Notes

- Queries are optimized with select_related
- Comments load asynchronously (no page reload)
- Pagination ready for future scaling
- Character counter prevents large submissions
- User avatars are cached in browser

---

## Support

For issues or improvements:
1. Check browser console for errors
2. Check Django logs for backend errors
3. Verify all files are in correct locations
4. Test API endpoints with cURL first
5. Clear browser cache if template changes don't appear

---

**Last Updated:** February 3, 2026
