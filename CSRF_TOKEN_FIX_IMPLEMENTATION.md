# CSRF Token Missing Error - Fix Implementation

## Problem
```
[WARNING] Forbidden (CSRF token missing.): /connect/3/
[WARNING] "POST /connect/3/ HTTP/1.1" 403 2491
```

The `/connect/3/` endpoint is returning **403 Forbidden** because the CSRF token is missing from the request headers.

---

## Root Cause

The CSRF token is not being included in the fetch request to `/connect/<user_id>/` endpoint.

### Issue Location
- **Endpoint:** `/accounts/urls.py` line 52
  ```python
  path('connect/<int:user_id>/', views.connect_view, name='connect'),
  ```

- **View:** `connect_view()` in `views.py` (line 2134)
  - Requires POST method
  - Lacks CSRF token in requests
  
- **Templates:** Multiple templates may be calling this endpoint without CSRF token

---

## Solution

### Step 1: Fix the `getCsrfToken()` Function

Add this utility function to your JavaScript (if not already present):

```javascript
function getCsrfToken() {
    // Method 1: From meta tag (preferred)
    let token = document.querySelector('meta[name="csrf-token"]')?.getAttribute('content');
    
    if (token) return token;
    
    // Method 2: From cookies (fallback)
    const name = 'csrftoken';
    if (document.cookie && document.cookie !== '') {
        const cookies = document.cookie.split(';');
        for (let i = 0; i < cookies.length; i++) {
            const cookie = cookies[i].trim();
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                token = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    
    // Method 3: From form field (fallback)
    if (!token) {
        token = document.querySelector('[name=csrfmiddlewaretoken]')?.value;
    }
    
    console.log('CSRF Token retrieved:', !!token);
    return token;
}
```

---

### Step 2: Update All Connect Requests

**For `/connect/<user_id>/` endpoint:**

```javascript
async function sendConnectRequest(userId) {
    const csrfToken = getCsrfToken();
    
    if (!csrfToken) {
        console.error('CSRF token not found!');
        showNotification('Security error: CSRF token missing', 'error');
        return;
    }
    
    try {
        const response = await fetch(`/accounts/connect/${userId}/`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'X-CSRFToken': csrfToken,      // ← CRITICAL
                'X-Requested-With': 'XMLHttpRequest'
            },
            body: JSON.stringify({})
        });
        
        const data = await response.json();
        
        if (!response.ok) {
            throw new Error(data.message || 'Failed to send connection request');
        }
        
        showNotification(data.message, 'success');
        return data;
        
    } catch (error) {
        console.error('Connection request error:', error);
        showNotification(error.message, 'error');
    }
}
```

---

### Step 3: Ensure CSRF Token in Meta Tag

**In your base template (e.g., `base.html`):**

```html
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    {% csrf_token %}  <!-- ← This creates the token -->
    <meta name="csrf-token" content="{{ csrf_token }}">  <!-- ← Explicit meta tag -->
    ...
</head>
```

---

### Step 4: Update Find Collaborators Template

**File:** `find_collaborators.html`

**Current (Broken):**
```javascript
function sendConnectionRequest(userId, event) {
    if (event) event.stopPropagation();
    const button = event && event.target ? event.target.closest('button') : null;
    const csrftoken = getCsrfToken();
    
    fetch(`/accounts/send-connection-request/${userId}/`, {  // ← Wrong endpoint or missing token
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
            'X-CSRFToken': csrftoken,
            'X-Requested-With': 'XMLHttpRequest'
        },
        body: JSON.stringify({})
    });
}
```

**Fixed:**
```javascript
function sendConnectionRequest(userId, event) {
    if (event) event.stopPropagation();
    
    const button = event && event.target ? event.target.closest('button') : null;
    const csrftoken = getCsrfToken();
    
    if (!csrftoken) {
        console.error('CSRF token not found');
        showNotification('Security error: CSRF token missing', 'error');
        return;
    }
    
    if (button) {
        button.disabled = true;
        button.innerHTML = '<i data-lucide="loader" class="w-4 h-4 animate-spin mr-2"></i>Sending...';
    }
    
    fetch(`/accounts/send-connection-request/${userId}/`, {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
            'X-CSRFToken': csrftoken,  // ← CRITICAL: Must include
            'X-Requested-With': 'XMLHttpRequest'
        },
        body: JSON.stringify({})
    })
    .then(response => response.json())
    .then(data => {
        if (data.success) {
            showNotification(data.message || 'Connection request sent!', 'success');
            if (button) {
                button.disabled = true;
                button.innerHTML = '<i data-lucide="clock" class="w-4 h-4 mr-2"></i><span>Pending</span>';
                button.className = 'flex-1 connect-button text-sm bg-yellow-600/20 text-yellow-800 cursor-not-allowed opacity-75';
            }
        } else {
            showNotification(data.message || 'Failed to send request', 'error');
            if (button) {
                button.disabled = false;
                button.innerHTML = 'Connect';
            }
        }
    })
    .catch(error => {
        console.error('Error:', error);
        showNotification('Network error: ' + error.message, 'error');
        if (button) {
            button.disabled = false;
            button.innerHTML = 'Connect';
        }
    });
}
```

---

### Step 5: For `/connect/` Endpoint

If you're calling the direct `/connect/<user_id>/` endpoint:

```javascript
async function connectUser(userId) {
    const csrfToken = getCsrfToken();
    
    if (!csrfToken) {
        console.error('CSRF token not available');
        showNotification('Security error: CSRF token missing', 'error');
        return;
    }
    
    try {
        const response = await fetch(`/accounts/connect/${userId}/`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'X-CSRFToken': csrfToken,  // ← Include this header
                'X-Requested-With': 'XMLHttpRequest'
            },
            body: JSON.stringify({})
        });
        
        if (response.status === 403) {
            throw new Error('CSRF token missing or invalid');
        }
        
        const data = await response.json();
        
        if (data.success) {
            showNotification(data.message, 'success');
        } else {
            showNotification(data.message, 'warning');
        }
        
        return data;
        
    } catch (error) {
        console.error('Connection error:', error);
        showNotification(error.message, 'error');
    }
}
```

---

## Implementation Checklist

- [ ] **Ensure CSRF token in meta tag:**
  ```html
  <meta name="csrf-token" content="{{ csrf_token }}">
  ```

- [ ] **Define `getCsrfToken()` function** in your main JavaScript file

- [ ] **Include `X-CSRFToken` header** in all POST/PUT/DELETE fetch requests:
  ```javascript
  headers: {
      'X-CSRFToken': getCsrfToken(),
      ...
  }
  ```

- [ ] **Test each endpoint:**
  - `/accounts/connect/<user_id>/`
  - `/accounts/send-connection-request/<user_id>/`
  - `/accounts/send-connection/<user_id>/`
  - All POST endpoints

- [ ] **Check browser console** for CSRF token errors

- [ ] **Verify `getCsrfToken()` returns value** before making requests

---

## Testing

### Quick Test in Browser Console

```javascript
// Check if CSRF token is available
console.log('CSRF Token:', getCsrfToken());

// Test a connection request
sendConnectRequest(3);  // Replace 3 with actual user ID
```

### Expected Behavior

**Before Fix:**
```
WARNING] Forbidden (CSRF token missing.): /connect/3/
[WARNING] "POST /connect/3/ HTTP/1.1" 403 2491
```

**After Fix:**
```
[INFO] "POST /connect/3/ HTTP/1.1" 200
{"success": true, "message": "Connection request sent to username!"}
```

---

## Files to Update

1. **find_collaborators.html** - `sendConnectionRequest()` function
2. **main_home.html** - Any connect/connection calls
3. **activity_feed.html** - `sendConnectionRequest()` function
4. **project_detail.html** - `quickConnect()` function
5. **messages.html** - Any connection-related calls
6. **base.html** - Ensure CSRF token in meta tags

---

## Common Mistakes to Avoid

❌ **Wrong:**
```javascript
fetch(`/accounts/connect/${userId}/`, {
    method: 'POST',
    body: JSON.stringify({})
    // Missing headers!
});
```

✅ **Correct:**
```javascript
fetch(`/accounts/connect/${userId}/`, {
    method: 'POST',
    headers: {
        'Content-Type': 'application/json',
        'X-CSRFToken': getCsrfToken(),  // ← Must have this
        'X-Requested-With': 'XMLHttpRequest'
    },
    body: JSON.stringify({})
});
```

---

## Debug Checklist

If you still get 403 errors:

1. ✅ Check CSRF token exists: `document.querySelector('meta[name="csrf-token"]')`
2. ✅ Check it has a value: `console.log(getCsrfToken())`
3. ✅ Check header is sent: Browser DevTools → Network tab → Request Headers
4. ✅ Check endpoint allows POST: `views.py` line 2134
5. ✅ Check middleware: `CSRF_COOKIE_SECURE` not set to True in dev mode
6. ✅ Clear browser cache and cookies
7. ✅ Check Django settings: `CsrfViewMiddleware` is enabled

---

**Status:** Ready to implement  
**Priority:** HIGH - Security issue  
**Affected Endpoints:** `/connect/`, `/send-connection-request/`, and all POST endpoints

