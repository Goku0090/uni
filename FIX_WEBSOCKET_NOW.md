# Fix WebSocket 404 Errors - NOW

## Status
- ❌ WebSocket routes broken: `/ws/project/2/` → 404
- ✅ HTTP routes working: `/accounts/projects/2/comments/` → 200
- ⏳ **Cause:** Using Django runserver (HTTP only) instead of Daphne (HTTP + WebSocket)

---

## IMMEDIATE ACTION (Right Now)

### Step 1: Install Daphne
```bash
cd e:\login\auth_project
pip install daphne==4.0.0
```

**Verify installation:**
```bash
python -m daphne --version
# Should output: daphne, version 4.0.0
```

### Step 2: Stop Django Runserver
```
Kill any running:
  python manage.py runserver
```

### Step 3: Start Daphne Server

**Windows:**
```bash
cd e:\login
run_daphne.bat
```

**Mac/Linux:**
```bash
cd /path/to/login
bash run_daphne.sh
```

**Manual command:**
```bash
cd e:\login\auth_project
python -m daphne -b 127.0.0.1 -p 8000 auth_project.asgi:application
```

**Expected output:**
```
2026-02-06 10:30:00,123 daphne.server INFO     Listening on TCP address 127.0.0.1:8000
2026-02-06 10:30:00,124 daphne.server INFO     Accepting connections
```

### Step 4: Test WebSocket

**Open browser console on project page:**
```javascript
// F12 → Console tab
let socket = new WebSocket("ws://localhost:8000/ws/project/2/");
socket.onopen = () => console.log("✅ WORKING!");
socket.onerror = (e) => console.log("❌ Error:", e);
```

**Check DevTools Network tab:**
1. F12 → Network tab
2. Filter by "WS" or "ws"
3. Look for `/ws/project/2/`
4. Status should be: **101** (not 404)
5. Color should be: **Green** (not red)

### Step 5: Commit Changes
```bash
cd e:\login
git add requirements.txt Procfile run_daphne.bat run_daphne.sh
git commit -m "Fix WebSocket routing: use Daphne ASGI server instead of runserver"
git push origin main
```

---

## Verification Checklist

### Local Development
- [ ] Daphne installed: `pip list | grep daphne`
- [ ] Running Daphne: Check console output shows "Listening on TCP address"
- [ ] No Django runserver process running
- [ ] HTTP works: `curl http://localhost:8000/api/`
- [ ] WebSocket works: Browser console test shows "✅ WORKING!"
- [ ] DevTools status: 101 (green)
- [ ] Comments endpoint working: `/accounts/projects/2/comments/` → 200

### Files Updated
- [ ] `requirements.txt` - Has `daphne==4.0.0`
- [ ] `Procfile` - Uses `daphne ... auth_project.asgi:application`
- [ ] `run_daphne.bat` - Created (Windows users)
- [ ] `run_daphne.sh` - Created (Mac/Linux users)

### Ready to Deploy
- [ ] All tests passing locally
- [ ] WebSocket connections working
- [ ] Git commit created
- [ ] Ready to push to Render/Railway

---

## What Changed?

### Before (Broken)
```
Command:    python manage.py runserver
Server:     Django development server (HTTP only)
WebSocket:  ❌ Not supported → 404
Status:     GET /ws/project/2/ → 404 Not Found
```

### After (Fixed)
```
Command:    daphne -b 127.0.0.1 -p 8000 auth_project.asgi:application
Server:     Daphne ASGI server (HTTP + WebSocket)
WebSocket:  ✅ Fully supported → 101
Status:     ws://localhost:8000/ws/project/2/ → 101 Switching Protocols
```

---

## Why This Fixes It

**Django runserver:**
- Only handles HTTP protocol
- Doesn't know about WebSocket
- Tries to match `/ws/project/2/` as HTTP GET
- Returns 404 (route not found)

**Daphne:**
- Handles both HTTP and WebSocket
- Recognizes WebSocket upgrade request
- Routes to correct consumer
- Returns 101 (switching protocols)
- Maintains persistent connection

---

## Real-time Features Now Working

Once fixed, these will work:

✅ Project status updates (live)  
✅ Comments appear instantly  
✅ Activity feed updates  
✅ Notifications in real-time  
✅ User presence tracking  
✅ Collaborative editing  

---

## Troubleshooting

### Issue: "Command not found: daphne"
**Fix:** Reinstall with full path
```bash
python -m pip install daphne==4.0.0
```

### Issue: "Port 8000 already in use"
**Fix:** Kill existing process or use different port
```bash
# Use port 8001
daphne -b 127.0.0.1 -p 8001 auth_project.asgi:application
```

### Issue: Still getting 404
**Check:**
1. Are you still using runserver? (Stop it!)
2. Is Daphne running? (Check console output)
3. Is the URL correct? (Should be `ws://` not `http://`)

### Issue: "ModuleNotFoundError: No module named 'daphne'"
**Fix:** Install in correct environment
```bash
# If using venv:
source venv/bin/activate  # Mac/Linux
venv\Scripts\activate.bat  # Windows

pip install daphne==4.0.0
```

---

## Next Steps

1. ✅ Install Daphne (done above)
2. ✅ Run Daphne (done above)
3. ✅ Test WebSocket (done above)
4. ✅ Commit changes (done above)
5. 🚀 Deploy to production (will use updated Procfile)

---

## Files Modified

| File | Change | Status |
|------|--------|--------|
| `requirements.txt` | Added `daphne==4.0.0` | ✅ Done |
| `Procfile` | Changed to Daphne | ✅ Done |
| `run_daphne.bat` | Created (Windows) | ✅ Done |
| `run_daphne.sh` | Created (Mac/Linux) | ✅ Done |

---

## Expected Results After Fix

```
BEFORE:
[WARNING] Not Found: /ws/project/2/
[WARNING] "GET /ws/project/2/ HTTP/1.1" 404 9033

AFTER:
[INFO] WebSocket connection accepted: ws://localhost:8000/ws/project/2/
[INFO] User connected to project 2
[INFO] Broadcasting project status update to all clients
✅ Real-time updates working
```

---

## Support

- If Daphne still won't start, verify Python is 3.8+: `python --version`
- If WebSocket still 404, check that you killed runserver
- If port conflicts, use: `daphne -b 127.0.0.1 -p 9000 auth_project.asgi:application`
- For production issues, see `WEBSOCKET_DETAILED_ANALYSIS.md`

---

## Summary

**Problem:** WebSocket returns 404  
**Cause:** Wrong server (runserver vs Daphne)  
**Solution:** Install Daphne, use it instead of runserver  
**Time:** 5 minutes  
**Result:** Real-time features working ✅

---

**Status:** Ready to implement  
**Priority:** High (blocks real-time features)  
**Complexity:** Low (just change server)  
**Impact:** Enables all WebSocket features
