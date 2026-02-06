# Django Template Recursion Error - Fix Report

**Error:** `RecursionError: maximum recursion depth exceeded` on `/project/2/` endpoint

**Root Cause:** The `project_detail.html` template is including `comment_section.html` which executes JavaScript that may be causing template re-rendering loops during the template inheritance chain.

---

## Diagnosis

The error stack trace shows infinite recursion in Django's template rendering system:
```
File "django/template/base.py", line 173, in render
File "django/template/loader_tags.py", line 210, in render
... (repeated 500+ times)
File "django/template/context.py", line 60, in push
RecursionError: maximum recursion depth exceeded
```

### Issues Found:

1. **project_detail.html (Line 289):**
   ```html
   {% include 'includes/comment_section.html' with project=project %}
   ```
   - This include is at the very end of the template
   - The comment_section contains Bootstrap CSS that may conflict

2. **Template Structure:**
   - `project_detail.html` is a standalone HTML file (not extending base.html)
   - Uses Tailwind CSS directly
   - Includes Bootstrap-based comment section
   - This CSS framework mismatch may cause rendering issues

3. **Comment Section Script (Lines 201-234):**
   - Executes JavaScript on page load
   - Calls `loadComments()` which makes AJAX requests
   - May trigger infinite loops if AJAX response triggers template re-render

---

## Solutions

### Solution 1: Fix Template Structure (RECOMMENDED)

Create a proper base template and fix the inheritance chain:

**File: `auth_project/accounts/templates/base.html`**
```html
<!DOCTYPE html>
<html lang="en" class="dark">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{% block title %}UniSync{% endblock %}</title>
    
    <!-- Tailwind CSS -->
    <script src="https://cdn.tailwindcss.com"></script>
    
    <!-- Google Fonts -->
    <link href="https://fonts.googleapis.com/css2?family=Poppins:wght@300;400;600;700&display=swap" rel="stylesheet">
    
    <!-- Bootstrap (for comments component) -->
    <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/css/bootstrap.min.css" rel="stylesheet">
    
    <style>
        body { font-family: 'Poppins', sans-serif; }
    </style>
    
    {% block extra_css %}{% endblock %}
</head>
<body class="bg-gradient-to-br from-gray-900 via-purple-900 to-gray-900 min-h-screen text-white">
    {% csrf_token %}
    
    {% block content %}{% endblock %}
    
    <script src="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/js/bootstrap.bundle.min.js"></script>
    <script src="https://kit.fontawesome.com/your-key.js" crossorigin="anonymous"></script>
    
    {% block extra_js %}{% endblock %}
</body>
</html>
```

**Updated: `auth_project/accounts/templates/project_detail.html`**
```html
{% extends "base.html" %}

{% block title %}{{ project.title }} | UniSync{% endblock %}

{% block content %}
    <!-- Navbar -->
    <nav class="bg-black/30 backdrop-blur-lg shadow-2xl sticky top-0 z-50">
        <div class="max-w-7xl mx-auto px-6 py-4 flex justify-between items-center">
            <div class="flex items-center space-x-3">
                <a href="{% url 'main_home' %}" class="text-2xl font-bold bg-gradient-to-r from-purple-400 to-pink-400 bg-clip-text text-transparent hover:opacity-80 transition">🚀</a>
            </div>
            <div class="flex gap-4">
                <a href="{% url 'main_home' %}" class="px-6 py-2 bg-purple-600 hover:bg-purple-700 rounded-full transition font-semibold">⬅ Back to Home</a>
            </div>
        </div>
    </nav>

    <div class="max-w-5xl mx-auto px-6 py-12">
        <!-- Project Header Content (keep existing code) -->
        <div class="bg-white/5 backdrop-blur-lg border border-white/10 rounded-3xl p-8 mb-6">
            <!-- ... all your existing project display code ... -->
        </div>
        
        <!-- Contact Section (keep existing code) -->
        {% if not is_owner %}
        <div class="bg-white/5 backdrop-blur-lg border border-white/10 rounded-3xl p-8">
            <!-- ... existing contact code ... -->
        </div>
        {% endif %}
        
        <!-- Related Projects (keep existing code) -->
        <div class="mt-8">
            <!-- ... existing related projects code ... -->
        </div>
    </div>

    <!-- Comments Section - Now separated from main template -->
    <div class="max-w-5xl mx-auto px-6 py-12">
        {% include 'includes/comment_section.html' with project=project %}
    </div>

    <!-- Footer -->
    <footer class="bg-black/50 backdrop-blur-lg py-8 mt-12">
        <div class="max-w-7xl mx-auto px-6 text-center text-gray-400">
            <p>&copy; 2025 UniSync. Bringing ideas to life. 🚀</p>
        </div>
    </footer>

    <script>
        <!-- Keep all your existing JavaScript -->
    </script>
{% endblock %}
```

---

### Solution 2: Disable Comment Section Temporarily (QUICK FIX)

**File: `auth_project/accounts/templates/project_detail.html`**

Comment out line 289 temporarily:
```html
<!-- COMMENTED OUT DUE TO RECURSION ERROR -->
<!-- {% include 'includes/comment_section.html' with project=project %} -->

<!-- Fallback message -->
<div class="mt-8 text-center text-gray-400">
    <p>Comments section temporarily disabled. We're fixing a rendering issue.</p>
</div>
```

---

### Solution 3: Fix Comment Section Template

**File: `auth_project/accounts/templates/includes/comment_section.html`**

**Problem:** The template may be causing nested rendering issues due to JavaScript executing during template render.

**Fix - Add error handling:**
```html
<!-- Check for circular includes -->
{% if not comment_section_included %}
    <!-- Comment Section Code -->
    {% include 'includes/comment_section_content.html' with project=project %}
    
    {# Set flag to prevent re-inclusion #}
    {% set comment_section_included = True %}
{% endif %}
```

However, Django doesn't support `{% set %}`. Better approach:

**Separate the script from the template:**

Create `auth_project/accounts/templates/includes/comment_section_safe.html`:
```html
<!-- Safe Comment Section Without Inline Script -->
<div class="comment-section mt-4" data-project-id="{{ project.id }}" id="comments-section-{{ project.id }}">
    <div class="card border-light">
        <div class="card-header bg-light border-bottom">
            <h6 class="mb-0">
                <i class="fas fa-comments me-2" style="color: #007bff;"></i>
                Comments (<span class="comment-count">0</span>)
            </h6>
        </div>
        
        <div class="card-body">
            <!-- Comment Input Form -->
            {% if user.is_authenticated %}
            <div class="comment-input-wrapper mb-4">
                <form class="comment-form" data-project-id="{{ project.id }}">
                    {% csrf_token %}
                    <div class="input-group">
                        <textarea 
                            class="form-control comment-textarea" 
                            placeholder="Share your thoughts on this project..."
                            rows="2"
                            maxlength="1000"
                            required
                        ></textarea>
                        <button 
                            class="btn btn-primary" 
                            type="submit"
                        >
                            Post
                        </button>
                    </div>
                </form>
            </div>
            {% else %}
            <div class="alert alert-info mb-4">
                <a href="{% url 'login' %}">Sign in</a> to comment
            </div>
            {% endif %}
            
            <!-- Comments List -->
            <div class="comments-list" id="comments-{{ project.id }}">
                <div class="text-center text-muted py-5">Loading comments...</div>
            </div>
        </div>
    </div>
</div>

<!-- Load script from static file or separate block -->
<script src="{% static 'js/comments.js' %}"></script>
```

---

## Implementation Steps

### Step 1: Create base template
```bash
cp auth_project/accounts/templates/project_detail.html auth_project/accounts/templates/project_detail_backup.html
# Then edit project_detail.html to extend base.html
```

### Step 2: Test for recursion
```bash
# Restart Django server
python manage.py runserver

# Access project detail page
# Check if recursion error is gone
curl http://localhost:8000/accounts/project-detail/1/
```

### Step 3: Fix comment section if still broken
- Move JavaScript to separate static file: `accounts/static/js/comments.js`
- Update include to reference safe version

### Step 4: Add error handling in views.py
```python
from django.template.loader import render_to_string

@login_required
def project_detail(request, project_id):
    try:
        project = get_object_or_404(Project, id=project_id)
        context = {'project': project, 'is_owner': project.user == request.user}
        
        # Render template safely with timeout
        template = render_to_string(
            'project_detail.html',
            context,
            request=request
        )
        return HttpResponse(template)
    except RecursionError:
        return HttpResponse("Template rendering error. Please try again later.", status=500)
    except Exception as e:
        logger.error(f"Error rendering project detail: {str(e)}")
        raise
```

---

## Prevention

1. **Avoid deeply nested includes:** Keep include depth < 5 levels
2. **Don't include templates in loops:** Can cause exponential nesting
3. **Use template tags instead of includes:** For complex logic
4. **Test with DEBUG=False:** Recursion errors are masked in production
5. **Use template caching:** Cache rendered templates to prevent re-renders

---

## Quick Workaround

Until fully fixed, disable comments:

**File: `auth_project/accounts/templates/project_detail.html` (line 289)**
```html
<!-- Commented out to fix recursion error -->
<!-- {% include 'includes/comment_section.html' with project=project %} -->
```

Then navigate to `/project/2/` - should load without error.

---

## Status

- **Error:** Confirmed - Template recursion in project detail view
- **Impact:** Project detail pages cannot be rendered
- **Severity:** CRITICAL - Blocks project viewing
- **Fix Time:** 15 minutes (Solution 2) to 1 hour (Solution 1)

Apply Solution 2 immediately, then implement Solution 1 properly.
