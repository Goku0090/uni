# Logo Fix: Activity Feed Page

## Issue
Logo not visible on activity feed page: `http://127.0.0.1:8000/api/activity-feed/`

## Root Cause
The activity feed template was referencing a non-existent file:
```html
<!-- BROKEN -->
<img src="{% static 'images/unisinq-logo.jpg' %}" alt="UniSinq Logo">
```

The actual logo file in the system is:
- `static/images/logo.jpg` ✅ (exists)
- `static/images/logo.svg` ✅ (exists)

But templates were looking for:
- `unisinq-logo.jpg` ❌ (doesn't exist)
- `unisync-logo.jpg` ❌ (doesn't exist)

## Solution Applied
Fixed the logo path in:
- **accounts/templates/social/activity_feed.html** (line 286)

Changed from:
```html
<img src="{% static 'images/unisinq-logo.jpg' %}" alt="UniSinq Logo" class="h-10 w-10 rounded-lg">
```

To:
```html
<img src="{% static 'images/logo.jpg' %}" alt="UniSinq Logo" class="h-10 w-10 rounded-lg object-cover">
```

## What to Do Now

### 1. Clear Static Files Cache
```bash
python manage.py collectstatic --clear --noinput
```

### 2. Restart Django Server
```bash
# Restart your Django development server
```

### 3. Clear Browser Cache
- Windows/Linux: `Ctrl+Shift+Delete`
- Mac: `Cmd+Shift+Delete`

### 4. Test the Page
Navigate to: `http://127.0.0.1:8000/activity-feed/`

You should now see the logo in the navbar!

## Logo Files Available

| File | Location | Format | Status |
|------|----------|--------|--------|
| logo.jpg | static/images/logo.jpg | JPG | ✅ Used |
| logo.svg | static/images/logo.svg | SVG | ✅ Available |
| unisync-logo.jpg | static/images/unisync-logo.jpg | JPG | Old naming |
| unisync_logo.jpg | static/images/unisync_logo.jpg | JPG | Old naming |

## Verification

After fixes, the navbar should display:
- ✅ Logo image (rounded square)
- ✅ "UniSinq" text
- ✅ Navigation links

---

**Status**: ✅ FIXED
**File Modified**: accounts/templates/social/activity_feed.html
**Change**: Line 286 logo path corrected
