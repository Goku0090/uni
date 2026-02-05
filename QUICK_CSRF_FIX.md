# Quick CSRF Token Fix - Implementation Steps

## The Problem
```
[WARNING] Forbidden (CSRF token missing.): /connect/3/
[WARNING] "POST /connect/3/ HTTP/1.1" 403 2491
```

## The Fix (5 Minutes)

### 1. Add CSRF Token Utility Function

Add this to your main JavaScript or at the top of templates that need it:

```javascript
function getCsrfToken() {
    // Try meta tag first (best practice)
    let token = document.querySelector('meta[name="csrf-token"]')?.getAttribute('content');
    if (token) return token;
    
    // Fallback: try to find in cookies
    const name = 'csrftoken';
    if (document.cookie) {
        for (let cookie of document.cookie.split(';')) {
            cookie = cookie.trim();
            if (cookie.startsWith(name + '=')) {
                return decodeURIComponent(cookie.substring(name.length + 1));
            }
        }
    }
    
    // Fallback: try form field
    return document.querySelector('[name=csrfmiddlewaretoken]')?.value || null;
}
```

### 2. Add CSRF Token to Meta Tags in Base Template

In `base.html` (in `<head>`):

```html
<head>
    {% csrf_token %}
    <meta name="csrf-token" content="{{ csrf_token }}">
</head>
```

### 3. Fix All POST Requests

**Template:** `find_collaborators.html`  
**Function:** `sendConnectionRequest` (line ~1782)

Change this:
```javascript
fetch(`/accounts/send-connection-request/${userId}/`, {
    method: 'POST',
    headers: {
        'Content-Type': 'application/json',
        // MISSING: 'X-CSRFToken': csrftoken,
    },
    body: JSON.stringify({})
})
```

To this:
```javascript
const csrfToken = getCsrfToken();

fetch(`/accounts/send-connection-request/${userId}/`, {
    method: 'POST',
    headers: {
        'Content-Type': 'application/json',
        'X-CSRFToken': csrfToken,  // ← ADD THIS LINE
        'X-Requested-With': 'XMLHttpRequest'
    },
    body: JSON.stringify({})
})
```

### 4. Check CSRF Token is Being Sent

Open Browser DevTools (F12):
- Go to **Network** tab
- Make a connection request
- Click the POST request to `/connect/` or `/send-connection-request/`
- Check **Request Headers** section
- Look for: `x-csrftoken: ...` (should have a long value)

**If missing:** CSRF token is not being sent → need to fix JavaScript  
**If present:** Server should accept the request

---

## One-Line Test

In browser console (F12 → Console tab):
```javascript
getCsrfToken()  // Should return a long token string
```

If it returns `null` → CSRF token not in meta tag

---

## Files That Need Fixing

Based on the grep results, update these templates:

1. **find_collaborators.html** - `sendConnectionRequest()` at line 1782
2. **main_home.html** - Connection fetch calls around line 1843
3. **activity_feed.html** - `sendConnectionRequest()` at line 2252
4. **project_detail.html** - `quickConnect()` function
5. **messages.html** - Any POST requests to `/connect/`

---

## Minimal Fix Template

Use this pattern for ANY POST/PUT/DELETE request:

```javascript
const csrfToken = document.querySelector('meta[name="csrf-token"]')?.getAttribute('content');

fetch('/your-endpoint/', {
    method: 'POST',
    headers: {
        'Content-Type': 'application/json',
        'X-CSRFToken': csrfToken,  // ← Always include this
    },
    body: JSON.stringify({...})
})
```

---

## Verify the Fix Works

After making changes:

1. Restart Django: `python manage.py runserver`
2. Open browser: `http://localhost:8000`
3. Clear cache: Ctrl+Shift+Delete
4. Try to send connection request
5. Check server logs - should see `200` not `403`

Expected:
```
[INFO] "POST /connect/3/ HTTP/1.1" 200
```

Not:
```
[WARNING] Forbidden (CSRF token missing.): /connect/3/
```

---

## Why This Happens

Django has CSRF protection enabled by default. It requires:
1. A CSRF token to exist on the page
2. That token to be sent with POST/PUT/DELETE requests
3. The token to be in the `X-CSRFToken` header (or form data)

When the header is missing → 403 Forbidden error

---

**Time to Fix:** 5-10 minutes  
**Difficulty:** Easy  
**Risk:** None - this is how Django is meant to work

