# Fix: User Profile 404 Error

## Problem

When clicking on user profile, getting error:
```
[WARNING] Not Found: /accounts/api/user-profile/2/
```

## Root Cause

The frontend is fetching from the **wrong URL path**.

**Current (Wrong)**:
```javascript
fetch(`/accounts/api/user-profile/${userId}/`)
```

**Should be**:
```javascript
fetch(`/api/user-profile/${userId}/`)
```

## Files to Fix

### 1. find_collaborators.html (Line 1660)

**Current Code**:
```html
fetch(`/accounts/api/user-profile/${userId}/`, {
```

**Fixed Code**:
```html
fetch(`/api/user-profile/${userId}/`, {
```

### 2. features/messages.html (Line 1361 & 1616)

**Current Code**:
```javascript
this.baseUrl = '/accounts/api/messages/search/';
this.baseUrl = '/accounts/api/messages/';
```

**Fixed Code**:
```javascript
this.baseUrl = '/api/messages/search/';
this.baseUrl = '/api/messages/';
```

---

## Explanation

### URL Routing Configuration

In `auth_project/urls.py`:

```python
# Line 14
path('accounts/', include('accounts.urls')),  # ← accounts.urls are here

# Line 16  
path('api/', include('accounts.urls')),  # ← accounts.urls are ALSO here
```

This means accounts.urls is mounted at TWO paths:
- `/accounts/` (for page routes)
- `/api/` (for API routes)

The API routes should use `/api/` prefix, NOT `/accounts/api/`.

### Available Routes

| Route | Path |
|-------|------|
| User Profile API | `/api/user-profile/<int:user_id>/` |
| Messages API | `/api/messages/` |
| Message Search | `/api/messages/search/` |

---

## Implementation Steps

### Step 1: Edit find_collaborators.html

**Location**: `accounts/templates/find_collaborators.html`

Find line ~1660:
```javascript
fetch(`/accounts/api/user-profile/${userId}/`, {
```

Change to:
```javascript
fetch(`/api/user-profile/${userId}/`, {
```

### Step 2: Edit features/messages.html

**Location**: `accounts/templates/features/messages.html`

Find line ~1361 and ~1616:
```javascript
this.baseUrl = '/accounts/api/messages/search/';
this.baseUrl = '/accounts/api/messages/';
```

Change to:
```javascript
this.baseUrl = '/api/messages/search/';
this.baseUrl = '/api/messages/';
```

### Step 3: Test

1. Navigate to find collaborators page
2. Click on a user profile
3. Modal should load WITHOUT 404 error
4. Profile data should display correctly

---

## Verification

After making changes, verify:

1. ✅ No 404 errors in browser console
2. ✅ Profile modal loads correctly
3. ✅ Profile data displays (name, college, bio, etc.)
4. ✅ Messages page works correctly
5. ✅ No other API errors

---

## Root Cause Analysis

**Why this happened:**

The URL configuration in `auth_project/urls.py` is:

```python
urlpatterns = [
    path('accounts/', include('accounts.urls')),  # Mount at /accounts/
    path('accounts/', include('allauth.urls')),
    path('api/', include('accounts.urls')),       # Mount at /api/
    # ... other routes
]
```

So the same `accounts.urls` is included at both `/accounts/` and `/api/`.

**Frontend mistake:**
Frontend code hardcoded `/accounts/api/` instead of just `/api/`.

**Correct approach:**
- Use `/accounts/` for page routes (HTML)
- Use `/api/` for API routes (JSON)

---

## Prevention

To prevent this in the future:

1. **Use Django template tags** for URL generation:
   ```html
   <!-- Instead of hardcoding -->
   <script>
       const apiUrl = "{% url 'user_profile_api' user_id=123 %}";
   </script>
   ```

2. **Or store URL in template context**:
   ```python
   # views.py
   context = {
       'api_base_url': '/api/',
   }
   ```

3. **Or use JavaScript data attributes**:
   ```html
   <div data-api-url="{% url 'api_base' %}">
   ```

---

## Quick Fix Commands

If you prefer to find and replace across files:

### Find all instances:
```
Search: /accounts/api/
Replace: /api/
Files: All .html and .js templates
```

### Specific Files:
- `accounts/templates/find_collaborators.html`
- `accounts/templates/features/messages.html`

---

## Testing Checklist

After applying fix:

- [ ] Navigate to Find Collaborators page
- [ ] Click on any user profile
- [ ] Modal opens without 404 error
- [ ] Profile info displays correctly
- [ ] Check browser console (no errors)
- [ ] Test on mobile view
- [ ] Test with different users
- [ ] Verify messages still work
- [ ] No other API calls broken

---

## API Endpoint Reference

### Working Endpoints

After the fix, these endpoints will work:

```
GET /api/user-profile/1/
Response: JSON with user profile data

GET /api/messages/
Response: Message list

GET /api/messages/search/?q=query
Response: Search results
```

### Response Format

```json
{
  "id": 2,
  "username": "johndoe",
  "full_name": "John Doe",
  "college": "MIT",
  "location": "Boston",
  "interests": ["AI", "Web Dev"],
  "bio": "Student developer",
  "profile_photo": "https://..."
}
```

---

## Summary

| Item | Before | After |
|------|--------|-------|
| API URL | `/accounts/api/user-profile/2/` | `/api/user-profile/2/` |
| Status | ❌ 404 Error | ✅ Works |
| Files to fix | 2 files | 2 files |
| Changes | ~3 lines | ~3 lines |
| Time to fix | 5 minutes | - |

---

## Support

If you encounter other `404` errors with `/accounts/api/` paths:

1. Change to `/api/`
2. Check `accounts/urls.py` for the actual route name
3. Verify the endpoint is defined in `views.py`
4. Check browser network tab for exact error

---

**Created**: January 29, 2026  
**Status**: Ready to Apply  
**Impact**: Critical (Breaks Profile Feature)  
**Difficulty**: Very Easy (Find & Replace)  
**Time**: 5 minutes

---
