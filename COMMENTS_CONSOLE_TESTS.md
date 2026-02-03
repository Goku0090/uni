# 🖥️ Console Tests for Comments Posting Issue

## How to Use This

1. **Press F12** in your browser
2. **Click Console tab**
3. **Copy & paste** each code block below
4. **Press Enter**
5. **Check output** for errors

---

## Test 1: Check CSRF Token Exists

```javascript
const token = document.querySelector('[name=csrfmiddlewaretoken]')?.value;
console.log('✅ CSRF Token found:', !!token);
console.log('Token preview:', token ? token.substring(0, 20) + '...' : 'NOT FOUND');
```

**Expected Output:**
```
✅ CSRF Token found: true
Token preview: abc123xyz...
```

**If shows "false":**
→ Reload page with Ctrl+Shift+R

---

## Test 2: Check DOM Elements Exist

```javascript
// Check if comments section elements exist
const projectId = 1; // Change to actual project ID
const input = document.querySelector(`.comment-input-${projectId}`);
const button = document.querySelector(`[onclick="submitComment(${projectId}"]`);
const container = document.querySelector(`.comments-container-${projectId}`);

console.log('✅ Input field exists:', !!input);
console.log('✅ Post button exists:', !!button);
console.log('✅ Comments container exists:', !!container);

if (input) console.log('   Input value:', input.value);
```

**Expected Output:**
```
✅ Input field exists: true
✅ Post button exists: true
✅ Comments container exists: true
   Input value: 
```

**If shows "false":**
→ Comments section might not be loaded
→ Try scrolling down on project card

---

## Test 3: Test API Connection

```javascript
// Test if API endpoint responds
const projectId = 1; // Change to actual project ID
const token = document.querySelector('[name=csrfmiddlewaretoken]')?.value;

fetch(`/accounts/api/projects/${projectId}/comments/`, {
    method: 'GET',
    headers: {
        'Content-Type': 'application/json',
    }
})
.then(response => {
    console.log('✅ API responded with status:', response.status);
    return response.json();
})
.then(data => {
    console.log('✅ API returned data:', data);
    console.log('   Comments count:', data.count || 0);
})
.catch(error => {
    console.error('❌ API Error:', error.message);
});
```

**Expected Output:**
```
✅ API responded with status: 200
✅ API returned data: {success: true, count: 0, comments: [...]}
   Comments count: 0
```

**If shows error:**
```
❌ API Error: [error message]
```
→ API endpoint not working
→ Check routes in urls.py

---

## Test 4: Test Comment Posting

```javascript
// Test posting a comment
const projectId = 1; // Change to actual project ID
const token = document.querySelector('[name=csrfmiddlewaretoken]')?.value;

console.log('Attempting to post comment...');

fetch(`/accounts/api/projects/${projectId}/comments/add/`, {
    method: 'POST',
    headers: {
        'Content-Type': 'application/json',
        'X-CSRFToken': token
    },
    body: JSON.stringify({ content: 'Test comment from console' })
})
.then(response => {
    console.log('✅ Server responded with status:', response.status);
    if (!response.ok) {
        console.error('❌ HTTP Error:', response.statusText);
    }
    return response.json();
})
.then(data => {
    if (data.success) {
        console.log('✅ SUCCESS! Comment posted');
        console.log('   Comment ID:', data.comment.id);
        console.log('   Content:', data.comment.content);
    } else {
        console.error('❌ Server error:', data.error);
    }
})
.catch(error => {
    console.error('❌ Network error:', error.message);
});
```

**Expected Output (Success):**
```
Attempting to post comment...
✅ Server responded with status: 200
✅ SUCCESS! Comment posted
   Comment ID: 123
   Content: Test comment from console
```

**If error:**
```
❌ Server responded with status: 404
❌ HTTP Error: Not Found
```
→ API endpoint not found
→ Check urls.py configuration

---

## Test 5: Check All Functions Exist

```javascript
// Check if JavaScript functions are defined
console.log('✅ toggleComments:', typeof toggleComments);
console.log('✅ submitComment:', typeof submitComment);
console.log('✅ loadCommentsIfNeeded:', typeof loadCommentsIfNeeded);
console.log('✅ createCommentElement:', typeof createCommentElement);
console.log('✅ deleteComment:', typeof deleteComment);
console.log('✅ editComment:', typeof editComment);
console.log('✅ escapeHtml:', typeof escapeHtml);
```

**Expected Output:**
```
✅ toggleComments: function
✅ submitComment: function
✅ loadCommentsIfNeeded: function
✅ createCommentElement: function
✅ deleteComment: function
✅ editComment: function
✅ escapeHtml: function
```

**If shows "undefined":**
→ JavaScript not loaded
→ Check main_home.html
→ Hard refresh (Ctrl+Shift+R)

---

## Test 6: Full Integration Test

```javascript
// Complete test from click to finish
const projectId = 1; // Change to actual project ID

console.log('=== FULL INTEGRATION TEST ===');

// Step 1: Check token
const token = document.querySelector('[name=csrfmiddlewaretoken]')?.value;
console.log('Step 1 - CSRF Token:', !!token ? '✅ Present' : '❌ Missing');

// Step 2: Check elements
const input = document.querySelector(`.comment-input-${projectId}`);
const button = document.querySelector(`[onclick="submitComment(${projectId}"]`);
console.log('Step 2 - Input field:', !!input ? '✅ Found' : '❌ Not found');
console.log('Step 3 - Button:', !!button ? '✅ Found' : '❌ Not found');

// Step 3: Check API
await fetch(`/accounts/api/projects/${projectId}/comments/`)
    .then(r => r.json())
    .then(d => console.log('Step 4 - API Accessible:', d.success ? '✅ Yes' : '❌ No'))
    .catch(() => console.log('Step 4 - API Accessible: ❌ No'));

// Step 4: Test posting
await fetch(`/accounts/api/projects/${projectId}/comments/add/`, {
    method: 'POST',
    headers: {
        'Content-Type': 'application/json',
        'X-CSRFToken': token
    },
    body: JSON.stringify({ content: 'Console test' })
})
.then(r => r.json())
.then(d => {
    if (d.success) {
        console.log('Step 5 - Post Request: ✅ Success');
        console.log('Comment ID:', d.comment.id);
    } else {
        console.log('Step 5 - Post Request: ❌ Failed');
        console.log('Error:', d.error);
    }
})
.catch(e => {
    console.log('Step 5 - Post Request: ❌ Error');
    console.log('Error:', e.message);
});

console.log('=== TEST COMPLETE ===');
```

**Expected Output:**
```
=== FULL INTEGRATION TEST ===
Step 1 - CSRF Token: ✅ Present
Step 2 - Input field: ✅ Found
Step 3 - Button: ✅ Found
Step 4 - API Accessible: ✅ Yes
Step 5 - Post Request: ✅ Success
Comment ID: 123
=== TEST COMPLETE ===
```

---

## Interpreting Results

### All ✅ Checks Pass
→ System working correctly
→ Issue might be browser-specific
→ Try: Clear cache, logout/login, use different browser

### Some ❌ Checks Fail

**CSRF Token Missing:**
→ Reload page
→ Clear cookies
→ Check login status

**API Returns 404:**
→ Endpoint not configured
→ Check urls.py
→ Check imports in urls.py

**API Returns 500:**
→ Server error
→ Check Django console for traceback
→ Check comment_api.py for syntax errors

**Elements Not Found:**
→ JavaScript not loaded
→ Comments section might be collapsed
→ Hard refresh page

---

## Quick Diagnostics Command

Copy all at once for quick diagnosis:

```javascript
const projectId = 1;
const token = document.querySelector('[name=csrfmiddlewaretoken]')?.value;
const input = document.querySelector(`.comment-input-${projectId}`);

console.log('=== QUICK DIAGNOSIS ===');
console.log('Token:', token ? '✅' : '❌');
console.log('Input:', input ? '✅' : '❌');
console.log('Functions: ', typeof toggleComments === 'function' ? '✅' : '❌');
console.log('=== END ===');
```

---

## Network Tab Debugging

Instead of console, you can check **Network tab**:

1. **Open DevTools**: F12
2. **Go to**: Network tab
3. **Try posting comment**
4. **Look for request** to `/accounts/api/projects/1/comments/add/`
5. **Check**:
   - **Status**: 200 = good, 404 = not found, 500 = error
   - **Response**: Should show `{"success": true}` or error message
   - **Headers**: Should have `X-CSRFToken` header

---

## Troubleshooting Based on Tests

| Test Result | Problem | Solution |
|-------------|---------|----------|
| CSRF Token ❌ | Token missing | Reload page |
| Input field ❌ | Comments not loaded | Scroll down / click toggle |
| Functions ❌ | JavaScript not loaded | Hard refresh page |
| API 404 | Endpoint not found | Check urls.py routes |
| API 500 | Server error | Check Django logs |
| Post 403 | Not authenticated | Login again |
| All ✅ but still fails | Unknown | Restart browser + Django |

---

## ✅ Success Indicators

When posting works, you'll see in console:

```javascript
// Function call:
submitComment(1, button)

// Console logs:
Posting comment to project: 1
CSRF Token present: true
Response status: 200
Response data: Object { success: true, comment: {...} }

// Page changes:
✅ Comment appears
✅ Counter updates
✅ Success toast shows
```

---

**Console Tests v1.0**  
**For Immediate Use**  
**Last Updated**: February 3, 2026
