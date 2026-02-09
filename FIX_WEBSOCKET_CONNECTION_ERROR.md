# Fix: WebSocket Connection Error

**Error:** `WebSocket connection to 'ws://127.0.0.1:8000/ws/project/2/' failed`  
**Cause:** Not using Daphne ASGI server (using Django development server instead)  
**Solution:** Start server with Daphne instead of `runserver`  
**Time to Fix:** 2 minutes

---

## The Problem

Your WebSocket client tries to connect:
```javascript
let socket = new WebSocket("ws://127.0.0.1:8000/ws/project/2/");
```

But Django's development server (`python manage.py runserver`) **only handles HTTP**, not WebSocket.

**Current Status:**
```
❌ HTTP:      Works (8000)
❌ WebSocket: Fails (ws://)
```

**Needed:**
```
✅ HTTP:      Works (8000)  
✅ WebSocket: Works (ws://)
```

---

## The Fix

### Option 1: Use Daphne (Recommended for Development)

**Step 1: Install Daphne**
```bash
pip install daphne==4.0.0
```

**Step 2: Run Daphne**

**Windows:**
```bash
cd e:\login\auth_project
daphne -b 0.0.0.0 -p 8000 auth_project.asgi:application
```

**Mac/Linux:**
```bash
cd /path/to/auth_project
daphne -b 0.0.0.0 -p 8000 auth_project.asgi:application
```

**Step 3: Test WebSocket**

Open browser console (F12):
```javascript
let socket = new WebSocket("ws://127.0.0.1:8000/ws/project/2/");
socket.onopen = () => console.log("✅ CONNECTED!");
```

**Expected Result:**
- Console shows: `✅ CONNECTED!`
- No WebSocket error in console

---

### Option 2: Use Provided Scripts

**Windows users:**
```bash
cd e:\login
run_daphne.bat
```

**Mac/Linux users:**
```bash
cd /path/to/auth_project
bash run_daphne.sh
```

---

## What These Scripts Do

### run_daphne.bat (Windows)
```batch
@echo off
cd auth_project
python -m pip install daphne==4.0.0
daphne -b 0.0.0.0 -p 8000 auth_project.asgi:application
```

### run_daphne.sh (Mac/Linux)
```bash
#!/bin/bash
cd auth_project
pip install daphne==4.0.0
daphne -b 0.0.0.0 -p 8000 auth_project.asgi:application
```

---

## Verify Configuration

Your ASGI setup is **already correct**:

**File:** `auth_project/asgi.py`
```python
from channels.auth import AuthMiddlewareStack
from channels.routing import ProtocolTypeRouter, URLRouter
import accounts.routing

application = ProtocolTypeRouter({
    "http": get_asgi_application(),      # ✅ HTTP
    "websocket": AuthMiddlewareStack(    # ✅ WebSocket
        URLRouter(
            accounts.routing.websocket_urlpatterns
        )
    ),
})
```

**WebSocket Routes:** `accounts/routing.py`
```python
websocket_urlpatterns = [
    re_path(r'ws/project/(?P<project_id>\w+)/$', consumers.ProjectUpdateConsumer.as_asgi()),
    re_path(r'ws/activity-feed/$', consumers.ActivityFeedConsumer.as_asgi()),
    re_path(r'ws/notifications/$', consumers.NotificationConsumer.as_asgi()),
]
```

✅ All configured correctly. Just need to run with Daphne.

---

## Common Issues & Fixes

### Issue: "Daphne not found"
```bash
pip install daphne==4.0.0
```

### Issue: "Port 8000 already in use"
```bash
# Windows - Find and kill process on port 8000
netstat -ano | findstr :8000
taskkill /PID <PID> /F

# Mac/Linux
lsof -i :8000
kill -9 <PID>
```

### Issue: "WebSocket still fails after Daphne starts"
1. Hard refresh browser (Ctrl+F5 or Cmd+Shift+R)
2. Check browser console for errors
3. Check Daphne console for error messages

### Issue: "Can't import channels"
```bash
pip install -r requirements.txt
```

---

## Troubleshooting Checklist

- [ ] Daphne installed: `pip list | grep daphne`
- [ ] Daphne running: See output starting with "Starting......"
- [ ] Port 8000 available: No errors about port in use
- [ ] Browser refreshed: Ctrl+F5 or Cmd+Shift+R
- [ ] Console shows connection message: `Connected to project 2 updates`
- [ ] No red errors in browser console

---

## What Happens When Fixed

**Browser Console:**
```
[realtime-updates.js] Initializing real-time updates...
[realtime-updates.js] Connected to project 2 updates
[realtime-updates.js] Connected to activity feed
[realtime-updates.js] Connected to notifications
✅ CONNECTED!
```

**Server Console (Daphne):**
```
HTTP GET /project/2/ 200 [...]
WebSocket CONNECT ws://127.0.0.1:8000/ws/project/2/ [user: your_username]
WebSocket ACCEPT ws://127.0.0.1:8000/ws/project/2/
```

---

## Next Steps

### 1. Start Daphne
```bash
daphne -b 0.0.0.0 -p 8000 auth_project.asgi:application
```

### 2. Test WebSocket
Open browser to `http://127.0.0.1:8000/project/2/` and open console (F12)

### 3. Verify Connection
Should see in console:
- ✅ `Connected to project 2 updates`
- ✅ `Connected to activity feed`
- ✅ `Connected to notifications`

### 4. Test Functionality
- Create a comment on the project
- Like the project
- Check if notifications appear in real-time

---

## Daphne Commands Reference

**Start Daphne:**
```bash
daphne -b 0.0.0.0 -p 8000 auth_project.asgi:application
```

**Daphne with verbose logging:**
```bash
daphne -b 0.0.0.0 -p 8000 -v 2 auth_project.asgi:application
```

**Daphne with custom worker count:**
```bash
daphne --workers 4 -b 0.0.0.0 -p 8000 auth_project.asgi:application
```

**Stop Daphne:**
- Press `Ctrl+C` in the terminal where it's running

---

## Important Notes

⚠️ **Development Only:**
- Daphne in this way is for development testing
- For production, use: `gunicorn + channels` or similar

✅ **Channels Already Configured:**
- `django-channels` is in requirements
- ASGI application is set up
- WebSocket routing is defined
- Everything is ready to work

✅ **Real-time Features Will Work:**
- Project comments (live)
- Notifications (instant)
- Activity feed (real-time)
- Member updates (live)

---

## Production Deployment

When deploying to production (Render/Railway):

**Add to Procfile:**
```
web: daphne -b 0.0.0.0 -p $PORT auth_project.asgi:application
```

**Or use Gunicorn with Channels:**
```
web: gunicorn --workers 4 --worker-class geventwebsocket.gunicorn.workers.GeventWebSocketWorker auth_project.wsgi
```

---

## Summary

| Step | Command | Time |
|------|---------|------|
| 1 | `pip install daphne==4.0.0` | 30 sec |
| 2 | `daphne -b 0.0.0.0 -p 8000 auth_project.asgi:application` | 5 sec |
| 3 | Refresh browser (F5) | 2 sec |
| 4 | Open console (F12) | 1 sec |
| 5 | Check for ✅ Connected messages | 10 sec |

**Total Time: ~2 minutes**

---

## Quick Command

```bash
cd e:\login\auth_project && pip install daphne==4.0.0 && daphne -b 0.0.0.0 -p 8000 auth_project.asgi:application
```

---

Once Daphne is running and WebSocket connects, you can test:
- Real-time project comments ✅
- Live notifications ✅
- Instant activity feed ✅
- Real-time member updates ✅

**Let me know when you've started Daphne!**
