# Django Cache Clear & Template Recursion Fix

## Issue Resolved ✓

**Problem:** Django template recursion error when loading project detail page
**Root Cause:** Comment section template line 2 had a template tag inside an HTML comment that was being parsed by Django
**Status:** FIXED

---

## What Was Wrong

File: `auth_project/accounts/templates/includes/comment_section.html` Line 2

### BEFORE (BROKEN):
```html
<!-- Live Feed Comment Section Component -->
<!-- Usage: {% include 'includes/comment_section.html' with project=project %} -->
```

The `{% include ... %}` inside the HTML comment was being parsed by Django's template engine, causing:
- The template to try to include itself
- Infinite recursion loop
- Maximum recursion depth exceeded error

### AFTER (FIXED):
```html
<!-- Live Feed Comment Section Component -->
<!-- To use this component, add the following to your template: -->
<!-- include 'includes/comment_section.html' with project=project -->
```

The Django template tag syntax `{% %}` was removed from the comment, so Django doesn't try to parse it.

---

## How to Clear Django's Template Cache

### Option 1: Clear Python Cache Files (Windows)

```bash
cd e:\login\auth_project

# Remove all __pycache__ directories
for /r %x in (__pycache__) do @if exist "%x" rd /s /q "%x"

# Remove .pyc files
for /r %x in (*.pyc) do @if exist "%x" del "%x"
```

### Option 2: Django Cache Clear Command

```bash
cd e:\login\auth_project
python manage.py clear_cache
```

### Option 3: Manual Cache Location

Django template cache is typically stored in:
```
C:\Users\GAUTAM\AppData\Local\Programs\Python\Python313\Lib\site-packages\django\
```

The cache might be in:
- `django\views\cache` (deprecated in newer Django)
- Memory cache (RAM - cleared on server restart)
- `django\core\cache\backends\`

### Option 4: Most Reliable - Restart Python

Simply restart the Django development server:

```bash
# Stop current server (Ctrl+C)
# Then restart:
cd e:\login\auth_project
python manage.py runserver
```

---

## Complete Fix Steps

### Step 1: Verify the Fix Was Applied ✓
```bash
# Check that the template tag is removed from comment
type e:\login\auth_project\accounts\templates\includes\comment_section.html | findstr "Usage:"
```

Should NOT show a line with `{% include`. If it does, the fix wasn't applied.

### Step 2: Clear All Caches
```bash
cd e:\login\auth_project

# Option A: Using Django command
python manage.py clear_cache

# Option B: Delete Python cache
powershell -Command "Get-ChildItem -Path . -Filter '__pycache__' -Recurse -Force | Remove-Item -Recurse -Force"

# Option C: Both together
python manage.py clear_cache && powershell -Command "Get-ChildItem -Path . -Filter '__pycache__' -Recurse -Force | Remove-Item -Recurse -Force"
```

### Step 3: Restart Django Server
```bash
# Kill current server
# Ctrl+C

# Start fresh
python manage.py runserver
```

### Step 4: Test the Fix
```bash
# Navigate to:
http://localhost:8000/accounts/project-detail/1/

# Or curl test:
curl http://localhost:8000/accounts/project-detail/1/
```

---

## Expected Results

After applying the fix and clearing cache:

✓ Project detail page loads without 500 error  
✓ No "RecursionError: maximum recursion depth exceeded" message  
✓ Project title displays  
✓ Project information shows  
✓ Comments section shows "Comments feature is temporarily disabled..." message  

---

## What Was Changed

| File | Line | Change |
|------|------|--------|
| `comment_section.html` | 2 | Removed `{% include %}` from HTML comment |
| `project_detail.html` | 290 | Kept the include commented out (temporary) |

---

## Technical Details

### Why Django Parses Template Tags in Comments

Django's template engine processes all `{% ... %}` and `{{ ... }}` tags before rendering, regardless of whether they're in HTML comments. This is by design because:

1. **Template compilation happens first** - Before any HTML is generated
2. **Template tags must be valid** - Even in comments, Django tries to parse them
3. **Context matters** - The template engine needs to resolve all template tags

### Safe Way to Comment Out Template Tags

❌ **DON'T DO THIS:**
```html
<!-- {% include 'something.html' %} -->
```

✓ **DO THIS INSTEAD:**
```html
<!-- To use, add: include 'something.html' -->
```

Or use Django's template comment tag:
```html
{% comment %}
{% include 'something.html' %}
{% endcomment %}
```

---

## Permanent Fix (Coming Soon)

This is a temporary fix. The permanent solution will:
1. Move JavaScript to a separate static file
2. Create a safe template without inline scripts
3. Re-enable comments with proper separation of concerns

See `CRITICAL_BUG_FIX_ACTION_PLAN.md` for full details.

---

## Troubleshooting

### Still Getting RecursionError?

1. **Verify the fix:**
   ```bash
   type e:\login\auth_project\accounts\templates\includes\comment_section.html
   ```
   Look for line 2 - should NOT have `{% include %}`

2. **Check for other instances:**
   ```bash
   findstr /r "{% include.*comment_section" e:\login\auth_project\accounts\templates\*.html
   ```

3. **Clear cache more aggressively:**
   ```bash
   # Delete all .pyc files
   for /r %x in (*.pyc) do @if exist "%x" del "%x"
   
   # Delete all __pycache__ folders
   for /r %x in (__pycache__) do @if exist "%x" rd /s /q "%x"
   
   # Restart Python
   python manage.py runserver --no-reload
   ```

4. **Check Django version:**
   ```bash
   python -c "import django; print(django.VERSION)"
   ```

### Getting Different Error?

If you see a different error after the fix, it might be:
- **TemplateNotFound:** Template file is missing or in wrong directory
- **SyntaxError:** Template syntax error elsewhere in the file
- **VariableDoesNotExist:** Context variable not passed to template

---

## Summary

✓ **Fixed:** Removed Django template tag from HTML comment  
✓ **Applied:** Changed line 2 of comment_section.html  
✓ **Cache:** Instructions provided for clearing template cache  
✓ **Testing:** Steps to verify the fix  

**Action Required:** Clear Django cache and restart server

