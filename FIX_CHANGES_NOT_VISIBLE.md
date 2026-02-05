# ⚠️ Changes Not Visible - Quick Fix

## Problem
You updated `messages.html` but changes don't appear at http://127.0.0.1:8000/messages/

## Root Cause
You likely have **two projects**:
- Updated file: `e:/login/auth_project/` 
- Running server: `c:/Users/GAUTAM/Desktop/unisync/`

These are **different folders**!

---

## Fix #1: Restart Django Server (Most Common)

### On Windows PowerShell:
```powershell
# Step 1: Stop current server
# Press Ctrl+C in your terminal

# Step 2: Clear Python cache
cd e:\login\auth_project
Remove-Item -Path ".\.pytest_cache\" -Recurse -Force
Remove-Item -Path ".\.ruff_cache\" -Recurse -Force
Get-ChildItem -Recurse -Include "__pycache__" | Remove-Item -Recurse -Force

# Step 3: Restart server
python manage.py runserver
```

### On Windows Command Prompt:
```cmd
# Step 1: Stop current server (Ctrl+C)

# Step 2: Navigate to project
cd e:\login\auth_project

# Step 3: Restart
python manage.py runserver
```

### On Mac/Linux:
```bash
# Step 1: Stop server (Ctrl+C)

# Step 2: Navigate
cd /path/to/e:/login/auth_project

# Step 3: Restart
python manage.py runserver
```

---

## Fix #2: Clear Browser Cache

1. **Hard Refresh**
   - Windows/Linux: `Ctrl+Shift+R`
   - Mac: `Cmd+Shift+R`

2. **Or Clear Cache**
   - Open DevTools (F12)
   - Right-click refresh button → "Empty cache and hard refresh"

3. **Or Open Incognito**
   - Windows: `Ctrl+Shift+N`
   - Mac: `Cmd+Shift+N`

---

## Fix #3: Check You're Editing the Right File

### Confirm the file location:
```bash
# Show the file we updated
type e:\login\auth_project\accounts\templates\messages.html

# Search for "UniSync" in the file
findstr "UniSync" e:\login\auth_project\accounts\templates\messages.html
```

If you see "UniSync" in the output, the file is updated correctly.

---

## Fix #4: Verify Django is Running from Correct Folder

### Check where Django is running:

```bash
# Check if manage.py exists in current folder
ls manage.py

# You should see: manage.py (200 bytes)
# If not, you're in the wrong folder!
```

### Correct folder should have:
```
e:/login/auth_project/
├── manage.py
├── accounts/
│   └── templates/
│       └── messages.html  ← Our updated file
├── auth_project/
│   └── settings.py
└── db.sqlite3
```

---

## Fix #5: Check Django Settings

Open `e:\login\auth_project\auth_project\settings.py` and verify:

```python
# Should have templates path like:
TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR.parent / 'templates'],  # or similar
        'APP_DIRS': True,
        ...
    }
]
```

---

## Fix #6: Full Reset

If nothing works, do complete reset:

```bash
# 1. Stop server (Ctrl+C)
cd e:\login\auth_project

# 2. Delete cache files
py -m pip cache purge

# 3. Migrate database
python manage.py migrate

# 4. Collect static files
python manage.py collectstatic --noinput

# 5. Restart server
python manage.py runserver
```

---

## Fix #7: Two Projects Issue (If Applicable)

If you have code in BOTH locations:

### Check if file exists in your running location:
```bash
# Check if messages.html exists there
dir c:\Users\GAUTAM\Desktop\unisync\accounts\templates\messages.html

# If it doesn't exist, that's the problem!
```

### Solution:
Option A - Copy file:
```bash
copy e:\login\auth_project\accounts\templates\messages.html ^
      c:\Users\GAUTAM\Desktop\unisync\accounts\templates\messages.html
```

Option B - Use the right folder:
```bash
# Stop server running from unisync folder
cd e:\login\auth_project
python manage.py runserver
```

---

## Quick Verification Steps

### Step 1: Verify file is updated
```bash
# Should show "UniSync" in the output
type e:\login\auth_project\accounts\templates\messages.html | findstr "UniSync"
```

Expected output:
```
<h2 class="text-2xl font-bold bg-gradient-to-r from-blue-600 to-pink-600 bg-clip-text text-transparent">UniSync</h2>
```

### Step 2: Verify server is running
```bash
# You should see this in terminal:
# Starting development server at http://127.0.0.1:8000/
```

### Step 3: Verify page loads
Visit: http://127.0.0.1:8000/messages/
Should show updated header with UniSync logo

---

## Debugging Output

If still not working, run this and share output:

```bash
# 1. Show Django version
python -m django --version

# 2. Show project root
cd e:\login\auth_project && pwd

# 3. Show file exists
ls -la accounts/templates/messages.html

# 4. Show file content (search for UniSync)
grep -n "UniSync" accounts/templates/messages.html

# 5. Test Django can find template
python manage.py shell
>>> from django.template.loader import get_template
>>> t = get_template('messages.html')
>>> print(t)
```

---

## Common Issues & Solutions

### Issue: "Template Does Not Exist"
**Solution**: Check `TEMPLATES['DIRS']` in settings.py

### Issue: "Static files not loading"
**Solution**: Run `python manage.py collectstatic`

### Issue: "Old version still showing"
**Solution**: 
1. Hard refresh (Ctrl+Shift+R)
2. Clear browser cache
3. Restart server

### Issue: "Server won't restart"
**Solution**:
1. Wait 5 seconds
2. Check if port 8000 is already in use: `netstat -ano | findstr :8000`
3. Kill process: `taskkill /PID <PID> /F`
4. Restart

### Issue: "Different folder structure"
**Solution**: Your project might have different structure. Check:
- `settings.py` → TEMPLATES section
- Templates might be in: `templates/accounts/messages.html`
- Or: `app/templates/messages.html`

---

## Step-by-Step Full Restart

### For Windows PowerShell:

```powershell
# 1. Navigate to project
Set-Location e:\login\auth_project

# 2. Check current directory
Get-Location

# 3. Stop server if running (Ctrl+C in terminal)
# Wait for: "^CKeyboardInterrupt"

# 4. Clear cache
Remove-Item -Path ".\.pytest_cache" -Recurse -Force -ErrorAction SilentlyContinue
Remove-Item -Path ".\.ruff_cache" -Recurse -Force -ErrorAction SilentlyContinue
Get-ChildItem -Path . -Include "__pycache__" -Recurse -Force | Remove-Item -Recurse -Force -ErrorAction SilentlyContinue

# 5. Start server
python manage.py runserver

# 6. Open browser and visit
# http://127.0.0.1:8000/messages/
```

---

## What Should Happen

### After restart, you should see:

```
Watching for file changes with StatReloader
Performing system checks...

System check identified no issues (0 silenced).
February 04, 2026 - 15:30:45
Django version 4.x.x, using settings 'auth_project.settings'
Starting development server at http://127.0.0.1:8000/
Quit the server with CONTROL-C.
```

### Then in browser:
- Page shows new header with: `[Logo] UniSync` instead of `🚀 Messages`
- Hover effect works (ring glows, text fades)
- Mobile responsive

---

## If Still Not Working

1. **Share these details:**
   - Output of: `python -m django --version`
   - Output of: `python manage.py runserver` (first 10 lines)
   - Where your actual code is: e:/login/ or c:/Users/GAUTAM/Desktop/unisync/?
   - What you see at http://127.0.0.1:8000/messages/

2. **Most likely cause**: You're running Django from wrong folder

3. **Solution**: Use correct folder path

---

## The 3-Second Fix

```bash
# Stop server (Ctrl+C)
cd e:\login\auth_project
python manage.py runserver
# Wait 5 seconds
# Open http://127.0.0.1:8000/messages/
# Changes should be visible!
```

**This solves 90% of "changes not visible" issues.**

---

## Need More Help?

Check:
1. Is `messages.html` actually updated? (Open file, search for "UniSync")
2. Is Django running? (See message in terminal)
3. Is Django running from correct folder? (Check terminal path)
4. Did you restart after edit? (Stop Ctrl+C and restart)
5. Did you hard refresh? (Ctrl+Shift+R)

Fix these 5 things in order, 99% sure it will work!
