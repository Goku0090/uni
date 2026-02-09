# Run This Now - Fix WebSocket 404

**Problem:** `/ws/project/2/` returns 404  
**Solution:** Use Daphne instead of runserver  
**Time:** 5 minutes  

---

## STEP 1: Copy & Paste Commands

Open Command Prompt / Terminal and run these commands:

### Windows Command Prompt
```cmd
cd e:\login\auth_project
pip install daphne==4.0.0
```

**Wait for it to finish.** You'll see:
```
Successfully installed daphne-4.0.0
```

### Mac/Linux Terminal
```bash
cd /path/to/login/auth_project
pip install daphne==4.0.0
```

---

## STEP 2: Stop Runserver

If you have `python manage.py runserver` running:
- **Press Ctrl+C** to stop it
- Or close that terminal window

---

## STEP 3: Start Daphne

### Windows (EASIEST)
```cmd
cd e:\login
run_daphne.bat
```

You should see:
```
========================================
Starting Daphne ASGI Server
========================================

Listening on TCP address 127.0.0.1:8000
Accepting connections
```

### Mac/Linux
```bash
cd /path/to/login
bash run_daphne.sh
```

You should see:
```
========================================
Starting Daphne ASGI Server
========================================

Listening on TCP address 127.0.0.1:8000
Accepting connections
```

### OR Run Manually
If scripts don't work:
```bash
cd auth_project
python -m daphne -b 127.0.0.1 -p 8000 auth_project.asgi:application
```

---

## STEP 4: Test It Works

**Open your browser to:** http://localhost:8000

**Open browser console (F12)** and paste this:
```javascript
let socket = new WebSocket("ws://localhost:8000/ws/project/2/");
socket.onopen = () => console.log("✅ WEBSOCKET WORKING!");
socket.onerror = (e) => console.log("❌ Error:", e);
socket.onclose = () => console.log("Closed");
```

### Expected Result
You should see in console:
```
✅ WEBSOCKET WORKING!
```

**If you see that, you're done!** ✅

### Check DevTools Network
1. Press F12
2. Go to **Network** tab
3. Filter for "ws" or "WS"
4. You should see `/ws/project/2/` with **Status: 101** (green)

---

## STEP 5: Save Changes to Git

Open a **NEW** terminal/command prompt and run:

```bash
cd e:\login

git add requirements.txt
git add Procfile
git add run_daphne.bat
git add run_daphne.sh

git commit -m "Fix WebSocket: use Daphne ASGI server"

git push origin main
```

---

## That's It!

The WebSocket 404 errors are now fixed. ✅

### Real-time Features Now Working:
- ✅ Project updates
- ✅ Comments appear instantly
- ✅ Activity feed updates
- ✅ Notifications in real-time

---

## Troubleshooting

### "daphne: command not found"
```bash
python -m pip install daphne==4.0.0
```

### "Port 8000 already in use"
Option 1: Kill existing process
```bash
# Windows:
netstat -ano | findstr :8000
taskkill /PID <PID> /F

# Mac/Linux:
lsof -ti:8000 | xargs kill -9
```

Option 2: Use different port
```bash
daphne -b 127.0.0.1 -p 8001 auth_project.asgi:application
```

### "ModuleNotFoundError: No module named 'daphne'"
Make sure you're in the right Python environment:
```bash
# If using virtual environment (venv):
# Windows:
venv\Scripts\activate.bat

# Mac/Linux:
source venv/bin/activate

# Then:
pip install daphne==4.0.0
```

### Still getting 404
1. **Are you still running runserver?** (Stop it!)
2. **Is Daphne running?** (Should see "Listening on TCP" in console)
3. **Using correct URL?** (Should be `ws://` not `http://`)

---

## Keep Daphne Running

**During development, keep the Daphne terminal window open.**

When you want to stop it:
- Press **Ctrl+C**

To restart:
- Run the same command again

---

## What Was Changed

**requirements.txt:** Added `daphne==4.0.0`  
**Procfile:** Changed to use Daphne  
**run_daphne.bat:** Created (Windows script)  
**run_daphne.sh:** Created (Mac/Linux script)  

---

## Next: Deploy to Render/Railway

Once working locally:

```bash
git push origin main
```

Render/Railway will automatically use the updated Procfile with Daphne. WebSocket will work there too!

---

## Summary

| Step | Command | Status |
|------|---------|--------|
| 1 | `pip install daphne==4.0.0` | ✅ Run this |
| 2 | Kill runserver | ✅ Do this |
| 3 | `run_daphne.bat` (or manual) | ✅ Run this |
| 4 | Browser test | ✅ Should see "✅ WORKING" |
| 5 | `git push origin main` | ✅ Do this |

---

**Total time: ~5 minutes**  
**Difficulty: LOW**  
**Result: WebSocket 404 FIXED ✅**

---

Questions? See `FIX_WEBSOCKET_NOW.md` for more detail.
