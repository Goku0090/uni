# Quick WebSocket Fix - Action Items

## The Problem
```
[WARNING] Not Found: /ws/project/2/
[WARNING] Not Found: /ws/activity-feed/
```

**Root Cause:** Using Django's development server instead of proper ASGI server.

---

## Quick Fix (5 minutes)

### Step 1: Install Daphne
```bash
cd e:\login\auth_project
pip install daphne==4.0.0
```

### Step 2: Test Locally
```bash
# OLD (broken):
python manage.py runserver

# NEW (fixed):
daphne -b 127.0.0.1 -p 8000 auth_project.asgi:application
```

### Step 3: Update requirements.txt
Add this line to `auth_project/requirements.txt`:
```
daphne==4.0.0
```

### Step 4: Update Procfile (if deploying)
```
web: daphne -b 0.0.0.0 -p 8000 auth_project.asgi:application
```

### Step 5: Test WebSocket Connection
Open browser console on any project page:
```javascript
let socket = new WebSocket("ws://localhost:8000/ws/project/2/");
socket.onopen = () => console.log("✅ Connected!");
socket.onerror = (e) => console.log("❌ Error:", e);
```

---

## Verification Checklist

- [ ] Daphne installed
- [ ] Running via Daphne (not runserver)
- [ ] Browser DevTools shows WS status 101
- [ ] Console shows "✅ Connected!"
- [ ] requirements.txt updated
- [ ] Procfile updated
- [ ] Ready to commit

---

## Commit Changes
```bash
git add requirements.txt Procfile
git commit -m "Fix WebSocket routing: use Daphne ASGI server"
git push origin main
```

---

## Files Already Correct
✅ `auth_project/asgi.py` - ProtocolTypeRouter configured  
✅ `accounts/routing.py` - WebSocket URL patterns defined  
✅ `accounts/consumers.py` - Consumer classes implemented  

---

## Support
See `WEBSOCKET_ROUTING_FIX_2026.md` for detailed troubleshooting
