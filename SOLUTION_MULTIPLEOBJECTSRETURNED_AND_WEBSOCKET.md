# Solution: MultipleObjectsReturned Error + WebSocket Integration

## Problem 1: MultipleObjectsReturned on OAuth Login

### Error Traceback
```
django.core.exceptions.MultipleObjectsReturned
  File "allauth/socialaccount/adapter.py", line 299, in get_app
    raise MultipleObjectsReturned
```

### Cause
Allauth found **multiple SocialApp entries** for Google or GitHub when trying to initiate OAuth login.

### Diagnosis

Run the diagnostic tool:
```bash
cd auth_project
python diagnose_oauth_error.py
```

Expected output:
```
CHECKING SOCIALAPP SITES RELATIONSHIPS
======================================================================
Total SocialApps: 2
  - Google (ID: 1)
  - GitHub (ID: 2)

SIMULATING ALLAUTH GET_APP() LOGIC
======================================================================
Google apps on current site: 1
GitHub apps on current site: 1
```

### Solution

**Step 1:** Run the cleanup script
```bash
python fix_duplicate_oauth.py
```

This will:
- Detect duplicate SocialApp entries
- Keep the first one
- Delete all duplicates
- Verify the fix

**Step 2:** If that doesn't work, manually fix:

```bash
python manage.py shell
```

```python
from allauth.socialaccount.models import SocialApp

# Check counts
google_count = SocialApp.objects.filter(provider='google').count()
github_count = SocialApp.objects.filter(provider='github').count()

print(f"Google apps: {google_count}")
print(f"GitHub apps: {github_count}")

# Delete duplicates (keep only first)
if google_count > 1:
    # Delete all Google apps except the first one
    to_delete = SocialApp.objects.filter(provider='google')[1:]
    for app in to_delete:
        print(f"Deleting duplicate: {app.name} (ID: {app.id})")
        app.delete()

if github_count > 1:
    # Delete all GitHub apps except the first one
    to_delete = SocialApp.objects.filter(provider='github')[1:]
    for app in to_delete:
        print(f"Deleting duplicate: {app.name} (ID: {app.id})")
        app.delete()

exit()
```

**Step 3:** Verify fix

```python
from allauth.socialaccount.models import SocialApp

google = SocialApp.objects.filter(provider='google')
github = SocialApp.objects.filter(provider='github')

print(f"Google apps: {google.count()}")  # Should be 1
print(f"GitHub apps: {github.count()}")  # Should be 1

exit()
```

### Test in Browser

1. Clear cookies & cache: `Ctrl+Shift+Delete`
2. Go to: `http://localhost:8000/accounts/login/`
3. Click "Login with Google"
4. Should redirect to Google OAuth (not error)

---

## Problem 2: WebSocket Not Working

### Your Code
```javascript
let socket = new WebSocket("ws://localhost:8000/ws/project/2/");
socket.onopen = () => console.log("✅ WORKING!");
```

### Common Issues

#### Issue 1: WebSocket Server Not Running
**Symptom:** Connection refused / WebSocket not available

**Solution:**
```bash
# Terminal 1: Standard Django
python manage.py runserver

# Terminal 2: WebSocket server (Daphne)
python manage.py runworker project_update activity_feed notifications
```

Or use single-threaded ASGI server:
```bash
pip install daphne
python -m daphne -b 0.0.0.0 -p 8000 auth_project.asgi:application
```

#### Issue 2: WebSocket URL Wrong
**Check:**
```bash
# Should be ws:// not http://
# Should be full path: ws://localhost:8000/ws/project/2/
# Port must match Django server
```

#### Issue 3: ASGI Not Configured
**Fix in settings.py:**
```python
ASGI_APPLICATION = 'auth_project.asgi.application'

CHANNEL_LAYERS = {
    'default': {
        'BACKEND': 'channels_redis.core.RedisChannelLayer',
        'CONFIG': {
            'hosts': [('127.0.0.1', 6379)],
        },
    }
}
```

#### Issue 4: Redis Not Running
**Start Redis:**
```bash
# Windows (using WSL)
wsl
redis-server

# macOS
brew install redis
redis-server

# Linux
sudo apt-get install redis-server
redis-server
```

### WebSocket Testing

#### Browser Console Test
```javascript
// Open DevTools (F12)
let socket = new WebSocket("ws://localhost:8000/ws/project/2/");

socket.onopen = function(event) {
    console.log("Connected!");
    // Send test message
    socket.send(JSON.stringify({
        type: 'comment.post',
        text: 'Test comment'
    }));
};

socket.onmessage = function(event) {
    const data = JSON.parse(event.data);
    console.log("Received:", data);
};

socket.onerror = function(event) {
    console.error("WebSocket error:", event);
};

socket.onclose = function(event) {
    console.log("Disconnected");
};
```

#### Python Test
```bash
python manage.py shell
```

```python
from channels.db import database_sync_to_async
from channels.layers import get_channel_layer
import asyncio

# Test channel layer
channel_layer = get_channel_layer()

# Send message to group
asyncio.run(channel_layer.group_send(
    'project_2',  # Group name
    {
        'type': 'project.comment_posted',
        'comment_id': 1,
        'author': 'test_user',
        'text': 'Test comment',
        'timestamp': '2026-02-08T10:30:00Z',
    }
))

print("Message sent to channel group")
exit()
```

---

## Integrated Solution: Full Stack Test

### 1. Start Services
```bash
# Terminal 1: WebSocket Server
python manage.py runworker project_update activity_feed notifications

# Terminal 2: Django Server  
python manage.py runserver

# Terminal 3: Redis (separate window)
redis-server
```

### 2. Test OAuth Login
```bash
# In browser: http://localhost:8000/accounts/login/
# Click "Login with Google"
# Should work without MultipleObjectsReturned error
```

### 3. Test WebSocket
```bash
# Create a project first
# In browser console:
let socket = new WebSocket("ws://localhost:8000/ws/project/1/");
socket.onopen = () => {
    console.log("Connected!");
    socket.send(JSON.stringify({
        type: 'comment.post',
        text: 'Hello from WebSocket!'
    }));
};

socket.onmessage = (event) => {
    console.log("Message received:", event.data);
};

socket.onerror = (error) => {
    console.error("Error:", error);
};
```

### 4. Verify in Django Admin
```bash
# http://localhost:8000/admin/
# Check:
# - SocialApps: Should have 1 Google, 1 GitHub
# - Projects: Should see new project
# - Comments: Should see posted comment
```

---

## Quick Checklist

- [ ] Run `python fix_duplicate_oauth.py`
- [ ] Verify no duplicate SocialApps
- [ ] Update SocialApp credentials in admin
- [ ] Start Redis server
- [ ] Start WebSocket worker
- [ ] Start Django server
- [ ] Test OAuth login in browser
- [ ] Test WebSocket in browser console
- [ ] Check Django logs for errors

---

## Files Created

| File | Purpose |
|------|---------|
| `fix_duplicate_oauth.py` | Remove duplicate OAuth apps |
| `diagnose_oauth_error.py` | Diagnose OAuth issues |
| `reset_oauth_config.py` | Full OAuth reset |
| `deep_debug_oauth.py` | Deep database inspection |
| `FIX_OAUTH_ERROR_QUICK.md` | Quick 5-minute fix |
| `FIX_OAUTH_MULTIPLEOBJECTSRETURNED_ERROR.md` | Detailed solutions |

---

## Next Steps

1. Run fix scripts
2. Test OAuth login
3. Test WebSocket connection
4. Check browser console for errors
5. Check Django logs: `tail -100 logs/django.log`

---

**Status**: Ready to test  
**Last Updated**: 2026-02-08
