# START HERE - "Error Loading Comments" Fix

**You're seeing:** ⚠️ Failed to load comments  
**Time to fix:** 2-5 minutes  
**Difficulty:** Easy

---

## THE FASTEST FIX (Do This RIGHT NOW)

### 1️⃣ Restart the Server
In your terminal:
```bash
Ctrl+C
python manage.py runserver
```

### 2️⃣ Clear Browser Cache
```
Ctrl+Shift+Delete → "All time" → Delete data → Done
```

### 3️⃣ Reload Page
```
F5  (or Ctrl+R)
```

---

## Is It Fixed?

Go to a project page and look at the comments section.

**If you see:**
- ✅ "No comments yet" message → **FIXED!** 🎉
- ✅ A list of comments → **FIXED!** 🎉
- ❌ "Failed to load comments" → Continue below

---

## If Still Broken (Run Diagnostic)

```bash
cd auth_project
python test_comments_api.py
```

This will tell you exactly what's wrong.

---

## Common Issues

### Issue 1: Server Not Fully Restarted
**Symptom:** Restarted but still shows error  
**Fix:** Look in terminal for: `Starting development server at http://127.0.0.1:8000/`
If missing, kill and restart: `pkill -f "python manage.py"` then `python manage.py runserver`

### Issue 2: Browser Cache
**Symptom:** Clear cache but still see error  
**Fix:** Use Incognito/Private mode (Ctrl+Shift+N)

### Issue 3: Fix Not Applied
**Symptom:** Test script shows `/api/api/` in URL  
**Fix:** See "Apply Fix Manually" below

---

## Apply Fix Manually (If Needed)

**File:** `auth_project/accounts/urls.py`  
**Lines:** 125-128

Change from:
```python
path('api/projects/<int:project_id>/comments/', get_comments, name='get-comments'),
```

To:
```python
path('projects/<int:project_id>/comments/', get_comments, name='get-comments'),
```

Do same for all 4 lines. Then restart server.

---

## Help Documents

| File | Use When |
|------|----------|
| **QUICK_FIX_STEPS.md** | Need step-by-step instructions |
| **DEBUG_ERROR_LOADING_COMMENTS.md** | Need detailed troubleshooting |
| **VISUAL_TROUBLESHOOTING_GUIDE.md** | Need diagrams and flowcharts |
| **test_comments_api.py** | Need to diagnose the problem |

---

## TL;DR

```bash
Ctrl+C
python manage.py runserver
Ctrl+Shift+Delete (clear cache)
F5 (reload)
```

**99% of the time this fixes it!**

---

*February 3, 2025*
