# Fix: Project Detail View Not Opening (Loading Forever)

## Problem Summary
When clicking "View Full Project" on a project card in the live feed, the page loads indefinitely and never displays the project details.

## Root Cause
The `project_detail.html` template has an **undefined attribute error** that causes the page rendering to fail silently.

### Issue Details:
- **Location**: `accounts/templates/project_detail.html`, Line 39
- **Problem**: Template references `project.user.username|first|upper`
- **But the model field is**: `user` (not `owner`)
- **What goes wrong**: The template tries to access the user's name but encounters an error during template rendering, which hangs the loading state

### Code that causes the issue:
```html
<!-- Line 38-40 in project_detail.html -->
<div class="w-10 h-10 rounded-full bg-gradient-to-br from-purple-500 to-pink-500 flex items-center justify-center text-lg font-bold">
    {{ project.user.username|first|upper }}
</div>
```

The problem is likely one of these:
1. Missing `.student_profile` access for displaying user name
2. Null user reference
3. Missing related_name in query

---

## Solution

### Option 1: Fix the Template (RECOMMENDED)
Replace all occurrences of `project.user` with proper access patterns in `project_detail.html`:

**Line 39**: Change from:
```html
{{ project.user.username|first|upper }}
```

To:
```html
{{ project.user.get_full_name|first|upper }}
```

**Line 42**: Change from:
```html
<p class="text-sm text-white font-semibold">{{ project.user.username }}</p>
```

To:
```html
<p class="text-sm text-white font-semibold">{{ project.user.student_profile.full_name|default:project.user.username }}</p>
```

**Line 43**: Verify it's correct:
```html
<p class="text-xs text-gray-500">Posted {{ project.created_at|timesince }} ago</p>
```

**Line 150**: Change from:
```html
<h2 class="text-2xl font-bold mb-4">💬 Interested? Connect with {{ project.user.username }}</h2>
```

To:
```html
<h2 class="text-2xl font-bold mb-4">💬 Interested? Connect with {{ project.user.student_profile.full_name|default:project.user.username }}</h2>
```

**Line 154**: Change from:
```html
<p class="text-green-300">✓ You are connected with {{ project.user.username }}</p>
```

To:
```html
<p class="text-green-300">✓ You are connected with {{ project.user.student_profile.full_name|default:project.user.username }}</p>
```

**Line 175**: Change from:
```html
<h2 class="text-2xl font-bold mb-4">🔥 More Projects from {{ project.user.username }}</h2>
```

To:
```html
<h2 class="text-2xl font-bold mb-4">🔥 More Projects from {{ project.user.student_profile.full_name|default:project.user.username }}</h2>
```

---

### Option 2: Fix in the View (ALTERNATIVE)
If the issue is related to missing user data, update the view in `views.py` line 1805 to optimize queries:

```python
def project_detail(request, project_id):
    """View project details"""
    # Add select_related for user optimization
    project = get_object_or_404(
        Project.objects.select_related('user__student_profile'),
        id=project_id
    )
    
    # ... rest of the code ...
```

This ensures the user and student profile are loaded efficiently without causing N+1 queries.

---

## Implementation Steps

### Step 1: Fix the Template
Edit `/e:/login/auth_project/accounts/templates/project_detail.html`

Replace these sections:

**Around Line 38-43:**
```diff
- <div class="w-10 h-10 rounded-full bg-gradient-to-br from-purple-500 to-pink-500 flex items-center justify-center text-lg font-bold">
-     {{ project.user.username|first|upper }}
+ <div class="w-10 h-10 rounded-full bg-gradient-to-br from-purple-500 to-pink-500 flex items-center justify-center text-lg font-bold">
+     {% if project.user.student_profile.profile_photo %}
+         <img src="{{ project.user.student_profile.profile_photo.url }}" alt="Avatar" class="w-full h-full rounded-full object-cover">
+     {% else %}
+         {{ project.user.username|first|upper }}
+     {% endif %}
</div>
<div>
-     <p class="text-sm text-white font-semibold">{{ project.user.username }}</p>
+     <p class="text-sm text-white font-semibold">{{ project.user.student_profile.full_name|default:project.user.username }}</p>
```

**Around Line 150:**
```diff
- <h2 class="text-2xl font-bold mb-4">💬 Interested? Connect with {{ project.user.username }}</h2>
+ <h2 class="text-2xl font-bold mb-4">💬 Interested? Connect with {{ project.user.student_profile.full_name|default:project.user.username }}</h2>
```

**Around Line 154:**
```diff
- <p class="text-green-300">✓ You are connected with {{ project.user.username }}</p>
+ <p class="text-green-300">✓ You are connected with {{ project.user.student_profile.full_name|default:project.user.username }}</p>
```

**Around Line 175:**
```diff
- <h2 class="text-2xl font-bold mb-4">🔥 More Projects from {{ project.user.username }}</h2>
+ <h2 class="text-2xl font-bold mb-4">🔥 More Projects from {{ project.user.student_profile.full_name|default:project.user.username }}</h2>
```

### Step 2: Optimize the View
Edit `/e:/login/auth_project/accounts/views.py` line 1705:

```python
def project_detail(request, project_id):
    """View project details"""
    project = get_object_or_404(
        Project.objects.select_related('user__student_profile'),
        id=project_id
    )
    
    # ... rest remains the same ...
```

### Step 3: Test
1. Go to the project feed
2. Click "View Full Project" on any project card
3. The page should now load without hanging

---

## Additional Template Issues to Check

Also verify there are no other missing attribute accesses in the template. Check the browser console (F12 → Console) for JavaScript errors:

```javascript
// Common issues to look for:
- Template syntax errors
- Missing form fields
- Undefined variables in JavaScript
```

---

## Expected Result
✅ Project detail page loads successfully
✅ Project title, description, and metadata display
✅ Connection button appears (if not owner)
✅ Comments section loads
✅ User information displays properly

---

## Related Files
- **Template**: `accounts/templates/project_detail.html`
- **View**: `accounts/views.py` (project_detail function, line 1705)
- **Model**: `accounts/models.py` (Project model, line 403)
- **Feed Template**: `accounts/templates/accounts/project_feed.html`

---

## Testing Checklist
- [ ] Click "View Full Project" from feed - page loads
- [ ] Project title displays correctly
- [ ] Project owner's name/avatar displays
- [ ] Connection status shows correctly
- [ ] Comments section appears
- [ ] Back to Home button works
- [ ] Edit/Delete buttons appear if owner
- [ ] No console errors in browser dev tools

---

## Quick Implementation Command
After making changes, restart Django:
```bash
python manage.py runserver
```

Then clear browser cache (Ctrl+Shift+Delete) and test again.
