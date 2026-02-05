# Quick Fix: Connect Button 403 Error

## Problem
```
POST http://127.0.0.1:8000/connect/3/ 403 (Forbidden)
```
The "Connect" button on collaborator cards was throwing a 403 Forbidden error.

## Root Cause
Missing CSRF token in the template.

## Solution (One Line!)
Add this to `find_collaborators_enhanced.html` before the `<script>` tag:

```html
{% csrf_token %}
```

## Where to Add
**File:** `auth_project/accounts/templates/find_collaborators_enhanced.html`  
**Before:** Line 723 (before `<script>` tag)  
**After:** Line 721 (after `</section>`)

## What It Looks Like
```html
     </section>

     <!-- CSRF Token -->
     {% csrf_token %}

     <script>
         let currentViewMode = 'grid';
```

## Testing (30 seconds)
1. Go to the Find Collaborators page
2. Click "Connect" on any collaborator
3. ✅ Should work without error
4. ✅ No 403 error in console

## Why It Works
- `{% csrf_token %}` creates: `<input type="hidden" name="csrfmiddlewaretoken" value="...">`
- JavaScript looks for this token: `document.querySelector('[name=csrfmiddlewaretoken]')`
- Token is included in form submission
- Django accepts the request ✅

## Status
✅ **FIXED**

---

**Full Documentation:** [FIX_CSRF_403_CONNECT_ERROR.md](./FIX_CSRF_403_CONNECT_ERROR.md)
