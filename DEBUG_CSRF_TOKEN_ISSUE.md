# Debug CSRF Token Issue - Step by Step

## The Problem

You're still getting:
```
POST http://127.0.0.1:8000/connect/3/ 403 (Forbidden)
```

Even though the code calls `/accounts/send-connection-request/3/`

## Debug Steps

### Step 1: Check if Function is Being Called

Open DevTools (F12) → Console tab

Paste this code:

```javascript
// Override the function to log when it's called
const originalSendConnection = sendConnectionRequest;
sendConnectionRequest = function(userId, event) {
    console.log('sendConnectionRequest called with userId:', userId);
    return originalSendConnection(userId, event);
};
```

Then click Connect button and check console.

**What to look for:**
- ✅ See log message: "sendConnectionRequest called with userId: 3"
- ❌ No log message = Function not being called

---

### Step 2: Check if getCsrfToken() Works

In console, run:

```javascript
console.log('CSRF Token:', getCsrfToken());
console.log('Token type:', typeof getCsrfToken());
```

**Expected:**
- Token should be a string like "j7d9K8x3m2L..."
- Type should be "function"

**If returns null:**
```javascript
// Check if hidden input exists
console.log('Hidden input:', document.querySelector('[name=csrfmiddlewaretoken]'));
console.log('Its value:', document.querySelector('[name=csrfmiddlewaretoken]')?.value);
```

---

### Step 3: Check if Fetch is Happening

In DevTools → Console:

```javascript
// Monkey-patch fetch to log all requests
const originalFetch = window.fetch;
window.fetch = function(...args) {
    console.log('FETCH:', args[0], args[1]);
    return originalFetch.apply(this, args);
};
```

Then click Connect button.

**What to look for:**
- ✅ Console shows: `FETCH: /accounts/send-connection-request/3/ {method: 'POST', ...}`
- ❌ Shows `/connect/3/` instead = Wrong endpoint
- ❌ No fetch log = fetch not being called

---

### Step 4: Network Tab Details

Open DevTools (F12) → Network tab

Click Connect button

Find the request. Click it.

**Check:**

1. **URL:**
   ```
   POST http://127.0.0.1:8000/accounts/send-connection-request/3/
   ```
   (Should say `/accounts/send-connection-request/`)

2. **Request Headers:**
   Look for:
   ```
   x-csrftoken: j7d9K8x3m2L...
   ```
   
   **If missing:** Token not being sent
   **If present:** Token is being sent correctly

3. **Response Status:**
   ```
   200 OK  ← Good
   403 Forbidden ← Bad
   ```

4. **Response Body:**
   ```json
   {"success": true, "message": "..."}
   ```

---

## What the Output Tells You

### Scenario 1: Function Called, Token Present, 200 OK ✅

```
Console: sendConnectionRequest called with userId: 3
Console: CSRF Token: j7d9K8x3m2L...
Network: URL: /accounts/send-connection-request/3/
Network: Headers: x-csrftoken: j7d9K8x3m2L...
Network: Status: 200 OK
```

**Result:** FIX IS WORKING! ✅

---

### Scenario 2: Function Called, No Token, 403 ❌

```
Console: sendConnectionRequest called with userId: 3
Console: CSRF Token: null
Network: URL: /accounts/send-connection-request/3/
Network: Headers: (no x-csrftoken)
Network: Status: 403 Forbidden
```

**Result:** Token not being found or sent
**Fix:** Check CSRF meta tag in HTML

---

### Scenario 3: Different URL Being Called ❌

```
Network: URL: /connect/3/
Network: Status: 403 Forbidden
```

**Result:** Wrong endpoint being called
**Fix:** Check what function the button calls

---

### Scenario 4: Function Not Called ❌

```
Console: (no "sendConnectionRequest called" log)
Network: (request to /connect/3/)
```

**Result:** Button not calling JavaScript function
**Fix:** Button might be submitting a form instead

---

## If You Find the Problem

### Problem: getCsrfToken() returns null

**Solution:**
1. Check HTML has: `{% csrf_token %}`
2. Check function can find hidden input:
   ```javascript
   document.querySelector('[name=csrfmiddlewaretoken]')
   ```
3. If not found, CSRF token not in page

### Problem: Calling /connect/3/ instead of /send-connection-request/

**Check:**
1. Is button calling `sendConnectionRequest()`?
2. Is `sendConnectionRequest()` function defined?
3. Are there multiple buttons? Maybe clicking wrong one?

### Problem: CSRF token not in headers

**Check:**
1. `getCsrfToken()` returns a value?
2. Header key is exactly: `'X-CSRFToken'` (case matters!)
3. Token is being set in request

### Problem: 403 Forbidden on /send-connection-request/

This means:
1. CSRF token not being sent, OR
2. CSRF token doesn't match Django's expected token
3. Django CSRF middleware rejecting request

**Solutions:**
1. Make sure `{% csrf_token %}` is in template
2. Make sure token is in request headers
3. Restart Django
4. Clear browser cache again

---

## Quick Diagnostic Command

Paste this in console - it will tell you everything:

```javascript
console.log('=== CSRF DEBUG ===');
console.log('1. getCsrfToken() returns:', getCsrfToken());
console.log('2. Hidden input exists:', !!document.querySelector('[name=csrfmiddlewaretoken]'));
console.log('3. Hidden input value:', document.querySelector('[name=csrfmiddlewaretoken]')?.value);
console.log('4. sendConnectionRequest function exists:', typeof sendConnectionRequest);
console.log('5. Meta tag exists:', !!document.querySelector('meta[name="csrf-token"]'));
console.log('6. Meta tag value:', document.querySelector('meta[name="csrf-token"]')?.getAttribute('content'));
```

Run this and tell me what each line returns.

---

## What I Need From You

1. Run the diagnostic command above ↑
2. Tell me the results
3. Tell me: When you click Connect, does the Network tab show:
   - `/accounts/send-connection-request/3/` OR `/connect/3/`?
4. Tell me: What status code does it return?

Then I can tell you exactly how to fix it.

