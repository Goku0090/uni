# WebSocket 404 Fix - START HERE

**Date:** February 6, 2026  
**Issue:** WebSocket routes return 404 errors  
**Status:** ✅ **SOLUTION READY - Follow steps below**

---

## Current Problem

```
[WARNING] Not Found: /ws/project/2/
[WARNING] "GET /ws/project/2/ HTTP/1.1" 404 9033
[WARNING] Not Found: /ws/activity-feed/
[WARNING] Not Found: /ws/notifications/
```

Comments API works (HTTP):
```
[INFO] "GET /accounts/projects/2/comments/ HTTP/1.1" 200 789
```

---

## The Fix (3 Steps)

### 1️⃣ Install Daphne (2 minutes)
```bash
cd e:\login\auth_project
pip install daphne==4.0.0
```

### 2️⃣ Run Daphne (1 minute)
```bash
# Windows:
cd e:\login
run_daphne.bat

# Mac/Linux:
bash run_daphne.sh
```

### 3️⃣ Test (1 minute)
Browser console (F12):
```javascript
let socket = new WebSocket("ws://localhost:8000/ws/project/2/");
socket.onopen = () => console.log("✅ WORKING!");
```

**Expected:** Console shows `✅ WORKING!`

---

## What Changed (Auto-Applied)

✅ **requirements.txt** - Added `daphne==4.0.0`  
✅ **Procfile** - Changed to use Daphne  
✅ **run_daphne.bat** - Windows startup script  
✅ **run_daphne.sh** - Mac/Linux startup script  

---

## Why This Works

| Aspect | Before | After |
|--------|--------|-------|
| **Server** | `python manage.py runserver` | `daphne ... auth_project.asgi:application` |
| **Protocol** | HTTP only | HTTP + WebSocket |
| **WebSocket** | ❌ 404 error | ✅ 101 success |
| **Real-time** | ❌ Disabled | ✅ Enabled |

---

## Detailed Documents

### Quick Start (5 minutes)
📄 **RUN_THIS_NOW.md** - Copy-paste commands

### Implementation (30 minutes)
📄 **FIX_WEBSOCKET_NOW.md** - Complete checklist  
📄 **WEBSOCKET_FIX_SUMMARY.txt** - Overview

### Technical Details (1 hour)
📄 **WEBSOCKET_ROUTING_FIX_2026.md** - Full implementation guide  
📄 **WEBSOCKET_DETAILED_ANALYSIS.md** - Deep-dive technical  
📄 **WEBSOCKET_REFERENCE_GUIDE.md** - Complete reference

### Codebase Analysis
📄 **COMPREHENSIVE_CODE_ANALYSIS_2026_FINAL.md** - All code documented  
📄 **CODE_ANALYSIS_SUMMARY_2026.md** - Quick overview

---

## Step-by-Step Instructions

### **[RECOMMENDED] Use startup scripts**

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

### OR Manual command

```bash
cd e:\login\auth_project
python -m daphne -b 127.0.0.1 -p 8000 auth_project.asgi:application
```

### You should see:
```
========================================
Starting Daphne ASGI Server
========================================

Listening on TCP address 127.0.0.1:8000
Accepting connections
```

---

## Test WebSocket Works

### Browser Console Test
1. Open http://localhost:8000
2. Press **F12** (DevTools)
3. Go to **Console** tab
4. Paste:
```javascript
let socket = new WebSocket("ws://localhost:8000/ws/project/2/");
socket.onopen = () => console.log("✅ WEBSOCKET WORKING!");
socket.onerror = (e) => console.error("❌ Error:", e);
```

### Expected: Console shows
```
✅ WEBSOCKET WORKING!
```

### DevTools Network Check
1. **F12** → **Network** tab
2. Filter: Type "ws"
3. Look for `/ws/project/2/`
4. **Status:** Should be **101** (green, not red)

---

## Commit & Deploy

### Save to Git
```bash
cd e:\login

git add requirements.txt Procfile run_daphne.bat run_daphne.sh
git commit -m "Fix WebSocket routing: use Daphne ASGI server"
git push origin main
```

### Deploy to Production
Once pushed, Render/Railway will:
1. Read updated Procfile
2. Use Daphne instead of gunicorn
3. Support both HTTP and WebSocket
4. All real-time features work

---

## Verification Checklist

- [ ] Installed daphne: `pip install daphne==4.0.0`
- [ ] Stopped any running runserver
- [ ] Running Daphne (check console)
- [ ] Browser test shows ✅ WORKING
- [ ] DevTools shows status 101
- [ ] HTTP endpoints still work
- [ ] Comments API works
- [ ] Changes committed
- [ ] Pushed to main

---

## What Now Works

Once fixed:

✅ **Project Updates** - Status changes appear instantly  
✅ **Live Comments** - See comments as they're posted  
✅ **Activity Feed** - Live activity stream  
✅ **Notifications** - Real-time alerts  
✅ **Presence** - User online status  
✅ **Collaboration** - Real-time updates  

---

## Troubleshooting

### Problem: `pip: command not found`
```bash
python -m pip install daphne==4.0.0
```

### Problem: `Port 8000 already in use`
```bash
daphne -b 127.0.0.1 -p 9000 auth_project.asgi:application
```

### Problem: Still getting 404
- ✓ Kill runserver (Ctrl+C in its terminal)
- ✓ Is Daphne running? (Check console output)
- ✓ Using correct URL? (Should be `ws://` not `http://`)

### Problem: `ModuleNotFoundError: daphne`
```bash
# Activate virtual environment first
venv\Scripts\activate.bat  # Windows
source venv/bin/activate   # Mac/Linux

# Then install
pip install daphne==4.0.0
```

---

## Architecture Overview

```
BEFORE (Broken):
  Browser → /ws/project/2/ → Django runserver (HTTP only) → 404 ❌

AFTER (Fixed):
  Browser → /ws/project/2/ → Daphne (HTTP + WebSocket) → 101 ✅
              (WebSocket upgrade)    (ASGI routing)        (established)
```

---

## Files Overview

| File | What Changed |
|------|--------------|
| requirements.txt | Added `daphne==4.0.0` |
| Procfile | Changed to `daphne ... auth_project.asgi:application` |
| run_daphne.bat | NEW - Windows startup script |
| run_daphne.sh | NEW - Mac/Linux startup script |
| auth_project/asgi.py | ✅ Already correct |
| accounts/routing.py | ✅ Already correct |
| accounts/consumers.py | ✅ Already correct |

---

## Time Estimate

| Task | Time |
|------|------|
| Install Daphne | 2 min |
| Run Daphne | 1 min |
| Test WebSocket | 1 min |
| Commit & Push | 1 min |
| **TOTAL** | **5 min** |

---

## Next Actions

### Immediate (now)
1. Open **RUN_THIS_NOW.md**
2. Copy commands
3. Run them
4. Test in browser

### Short-term (today)
1. Verify all tests pass
2. Commit changes
3. Push to main

### Long-term (production)
1. Deploy to Render/Railway
2. Verify WebSocket works there
3. Monitor for any issues

---

## Support Resources

| Document | Purpose |
|----------|---------|
| RUN_THIS_NOW.md | Copy-paste commands |
| FIX_WEBSOCKET_NOW.md | Detailed checklist |
| WEBSOCKET_ROUTING_FIX_2026.md | Full implementation |
| WEBSOCKET_DETAILED_ANALYSIS.md | Technical details |
| WEBSOCKET_REFERENCE_GUIDE.md | Complete reference |

---

## Summary

**Problem:** WebSocket returns 404  
**Cause:** Using Django runserver (HTTP only)  
**Solution:** Use Daphne (HTTP + WebSocket)  
**Time:** 5 minutes  
**Difficulty:** LOW  
**Impact:** HIGH (enables real-time features)  

---

## Start Now

→ Open **RUN_THIS_NOW.md** and follow the steps

Or read **FIX_WEBSOCKET_NOW.md** for more detail

---

**Status:** ✅ Ready to implement  
**Blocking:** No (HTTP still works, WebSocket broken)  
**Priority:** High (blocks real-time features)  
**Risk:** Very low (easily reversible)

---

**Time to fix: 5 minutes**  
**Time to benefit: Immediate (all real-time features work)**

Get started now! 🚀
