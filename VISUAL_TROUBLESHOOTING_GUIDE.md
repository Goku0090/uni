# 📊 Visual Troubleshooting Guide - Comments Error

**For: "Failed to load comments" error**

---

## What You See (The Problem)

```
┌─────────────────────────────────────────────────────┐
│  Project Details: My Awesome Project                │
├─────────────────────────────────────────────────────┤
│                                                     │
│  [Project Description...]                           │
│                                                     │
│  ┌────────────────────────────────────────────────┐ │
│  │ 💬 Comments (0)                                │ │
│  ├────────────────────────────────────────────────┤ │
│  │ [Comment Input Field]                         │ │
│  │                                                │ │
│  │ ⚠️  Failed to load comments                    │ │ ← THIS IS THE ERROR
│  │                                                │ │
│  └────────────────────────────────────────────────┘ │
│                                                     │
└─────────────────────────────────────────────────────┘
```

---

## Decision Tree - How to Fix

```
                    Error: "Failed to load comments"
                              │
                              ▼
                    ┌─────────────────┐
                    │ Restart server? │
                    │   (Ctrl+C)      │
                    └────────┬────────┘
                             │
                    ┌────────▼────────┐
                    │  python manage  │
                    │  .py runserver  │
                    └────────┬────────┘
                             │
                    ┌────────▼────────┐
                    │ Clear browser   │
                    │ cache?          │
                    │(Ctrl+Shift+Del) │
                    └────────┬────────┘
                             │
                    ┌────────▼────────┐
                    │ Reload page?    │
                    │     (F5)        │
                    └────────┬────────┘
                             │
                    ┌────────▼────────────┐
                    │ Comments loading?   │
                    └────────┬────────┬───┘
                             │        │
                          YES│        │NO
                             │        │
                    ✅ FIXED! │        │
                             │        ▼
                             │   ┌──────────────┐
                             │   │ Run: python  │
                             │   │ test_        │
                             │   │ comments_    │
                             │   │ api.py       │
                             │   └──────────────┘
                             │
                             ▼
                        Does test pass?
                        ┌───────┬─────┐
                     YES│       │NO   │
                        │       │     │
                    ✅ FIX│       │    ▼
                        │       │ Check accounts/
                        │       │ urls.py line 125
                        │       │
                        │       │ Has /api/projects/?
                        │       │ ┌────────┬────────┐
                        │       │ │YES     │NO     │
                        │       │ │        │       │
                        │       │ │Apply   │Browser│
                        │       │ │fix     │error  │
                        │       │ │        │(404)  │
```

---

## Flowchart - "Is It Fixed?"

```
START
  │
  ▼
See "Failed to load comments"?
  ├─ NO  ► ✅ SKIP THIS GUIDE
  │
  └─ YES ▼
    Restart server?
      ├─ Done ▼
      │  Clear cache?
      │    ├─ Done ▼
      │    │  Reload page?
      │    │    ├─ Done ▼
      │    │    │  Comments loading?
      │    │    │    ├─ YES ► ✅ FIXED!
      │    │    │    │
      │    │    │    └─ NO ▼
      │    │    │       Run test script
      │    │    │       (python test_comments_api.py)
      │    │    │           │
      │    │    │           ├─ PASS ► ✅ Fixed!
      │    │    │           │
      │    │    │           └─ FAIL ▼
      │    │    │              Check accounts/urls.py
      │    │    │              Lines 125-128
      │    │    │              Has path('api/projects...')?
      │    │    │              ├─ YES ► Apply fix
      │    │    │              │         (remove 'api/')
      │    │    │              │         Restart server
      │    │    │              │         ✅ Should work now!
      │    │    │              │
      │    │    │              └─ NO ► Check DevTools
      │    │    │                       (F12 → Network)
      │    │    │                       ├─ 404 ► URL wrong
      │    │    │                       ├─ 500 ► Server error
      │    │    │                       └─ 200 ► Check response
      │    │    │
      │    │    └─ Skip ► Do it now! (Ctrl+Shift+Del)
      │    │
      │    └─ Skip ► Do it now! (Ctrl+Shift+Delete)
      │
      └─ Skip ► Do it now! (Ctrl+C)
  
END
```

---

## Status Code Reference

```
┌─────────────────────────────────────────────────┐
│  Network Tab Status Codes                       │
├─────────────────────────────────────────────────┤
│                                                 │
│  ✅ 200 OK                                       │
│     Request succeeded, check response data      │
│                                                 │
│  ❌ 404 NOT FOUND                                │
│     URL is wrong (fix not applied)              │
│     Solution: Edit accounts/urls.py             │
│                                                 │
│  ❌ 500 INTERNAL SERVER ERROR                    │
│     Server crashed or has a bug                │
│     Solution: Check Django logs (tail logs/...) │
│                                                 │
│  ❌ 403 FORBIDDEN                                │
│     Not authenticated (not logged in)           │
│     Solution: Login first                       │
│                                                 │
│  ⏳ (No request at all)                          │
│     Server not responding                       │
│     Solution: Restart server (Ctrl+C)           │
│                                                 │
└─────────────────────────────────────────────────┘
```

---

## Fix Application Visual

```
BEFORE (WRONG):
├─ auth_project/urls.py
│  └─ path('api/', include('accounts.urls'))
│     └─ accounts/urls.py
│        └─ path('api/projects/<id>/comments/', ...)
│           └─ Result: /api/api/projects/... ❌

AFTER (CORRECT):
├─ auth_project/urls.py
│  └─ path('api/', include('accounts.urls'))
│     └─ accounts/urls.py
│        └─ path('projects/<id>/comments/', ...)
│           └─ Result: /api/projects/... ✅
```

---

## Step-by-Step Visual

### Step 1: Restart Server
```
Terminal:
$ python manage.py runserver
Watching for file changes with StatReloader
Starting development server at http://127.0.0.1:8000/
(press Ctrl+C to quit)
```

### Step 2: Clear Cache
```
Browser:
[Ctrl+Shift+Delete]
  ┌──────────────────────────────┐
  │ Clear Browsing Data          │
  │ ☐ Cookies and other site data│
  │ ☑ Cached images and files    │
  │ Time range: [All time ▼]     │
  │ [CLEAR DATA]                 │
  └──────────────────────────────┘
```

### Step 3: Reload Page
```
Browser:
[F5] or [Ctrl+R]
```

### Step 4: Check Network Tab
```
DevTools (F12):
┌─────────────────────────────────────┐
│ Network    Console  Elements         │
├─────────────────────────────────────┤
│ Filter: all         Preserve Log     │
├──────────┬──────────┬────────────────┤
│ Name     │ Status   │ Type           │
├──────────┼──────────┼────────────────┤
│ projects │ 200 ✅   │ document       │
│ api/...  │ 200 ✅   │ xhr            │
│ comments │ 200 ✅   │ xhr            │
└──────────┴──────────┴────────────────┘

All 200 = ✅ Working!
Any 404 = ❌ URL wrong
Any 500 = ❌ Server error
```

---

## Test Script Output

```bash
$ python test_comments_api.py

================================================================================
COMMENT API TEST SCRIPT
================================================================================

[TEST 1] URL Routing Check
────────────────────────────────────────────────────────────────────────────
✅ GET /api/projects/1/comments/ → get_comments
✅ POST /api/projects/1/comments/add/ → add_comment
✅ DELETE /api/comments/1/delete/ → delete_comment
✅ PUT /api/comments/1/edit/ → edit_comment

[TEST 2] Database Check
────────────────────────────────────────────────────────────────────────────
Users in database: 5
Projects in database: 3
Comments in database: 12

[TEST 3] Create Test Data
────────────────────────────────────────────────────────────────────────────
✅ Test user already exists: testuser
✅ StudentProfile already exists for testuser
✅ Test project already exists: 1

[TEST 4] API Endpoint Test
────────────────────────────────────────────────────────────────────────────
GET /api/projects/1/comments/
✅ Status: 200
   Success: true
   Comment count: 2
   Comments: [...]

SUMMARY
================================================================================
✅ If all tests above are GREEN, comments API is working correctly!
```

---

## Browser Console Error Messages

```javascript
✅ No errors:
   (empty console, no red messages)

❌ 404 Error:
   Failed to load resource: the server responded with a 
   status of 404 (Not Found)
   └─ Fix: Check accounts/urls.py line 125

❌ 500 Error:
   Failed to load resource: the server responded with a 
   status of 500 (Internal Server Error)
   └─ Fix: Check Django logs or server terminal

❌ Parse Error:
   Uncaught SyntaxError: Unexpected token < in JSON at position 0
   └─ Fix: Server is returning HTML instead of JSON (500 error)
```

---

## Success State (After Fix)

```
✅ BEFORE FIX:
┌─────────────────────────────────────────────────────┐
│  Comments (0)                                       │
├─────────────────────────────────────────────────────┤
│  [Input field]                                      │
│  ⚠️  Failed to load comments  ← ERROR              │
└─────────────────────────────────────────────────────┘

✅ AFTER FIX:
┌─────────────────────────────────────────────────────┐
│  Comments (2)                                       │
├─────────────────────────────────────────────────────┤
│  [Input field] [Post]                               │
│                                                     │
│  User A: "Great project!"                           │
│  3 hours ago                                        │
│                                                     │
│  User B: "I want to join!"                          │
│  2 hours ago                                        │
└─────────────────────────────────────────────────────┘
```

---

## Quick Reference Card

```
┌──────────────────────────────────────────────────────┐
│  QUICK FIX CARD                                      │
├──────────────────────────────────────────────────────┤
│  Problem: "Failed to load comments"                  │
│                                                      │
│  1. Ctrl+C        (stop server)                      │
│  2. Enter         (restart server)                   │
│  3. Ctrl+Shift+Del (clear cache)                     │
│  4. F5             (reload page)                     │
│                                                      │
│  ✅ Works? Done!                                     │
│  ❌ Doesn't work? Run: python test_comments_api.py   │
├──────────────────────────────────────────────────────┤
│  Files to check:                                     │
│  • accounts/urls.py (line 125)                       │
│  • Django logs (tail -f logs/django.log)             │
│  • Browser DevTools (F12 → Network)                  │
└──────────────────────────────────────────────────────┘
```

---

*Visual guide created: February 3, 2025*
