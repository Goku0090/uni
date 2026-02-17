# Google Analytics Setup Guide

## ✅ Implemented - Google Analytics Ready!

Your UniSinq app now supports Google Analytics tracking with a clean, environment-based approach.

---

## Quick Setup (2 minutes)

### Step 1: Add Environment Variable

**Local Development** (`backend/.env`):
```
GOOGLE_ANALYTICS_ID=G-K0PB5TRR26
```

**On Render Dashboard:**
1. Go to: https://dashboard.render.com
2. Select your service
3. Click "Environment"
4. Add variable:
   - Key: `GOOGLE_ANALYTICS_ID`
   - Value: `G-K0PB5TRR26`
5. Click "Save" (auto-redeploy)

### Step 2: Done! ✅

Google Analytics will start tracking automatically!

---

## How It Works

### Context Processor (`accounts/context_processors.py`)

Reads the `GOOGLE_ANALYTICS_ID` from environment and passes to all templates:

```python
def google_analytics(request):
    return {
        'google_analytics_id': os.getenv('GOOGLE_ANALYTICS_ID', ''),
    }
```

### Template Integration (`base.html`)

Conditionally loads Google Analytics:

```html
{% if google_analytics_id %}
    <!-- Google tag (gtag.js) -->
    <script async src="https://www.googletagmanager.com/gtag/js?id={{ google_analytics_id }}"></script>
    <script>
      window.dataLayer = window.dataLayer || [];
      function gtag(){dataLayer.push(arguments);}
      gtag('js', new Date());
      gtag('config', '{{ google_analytics_id }}');
    </script>
{% endif %}
```

### Settings Registration (`settings.py`)

Added to context processors:
```python
'accounts.context_processors.google_analytics',
'accounts.context_processors.site_config',
```

---

## Features

✅ **Environment-based** - No hardcoded IDs  
✅ **Optional** - Only loads if ID is provided  
✅ **Secure** - Uses environment variables  
✅ **Clean** - Single source of truth  
✅ **Production-ready** - Works on Render  

---

## Files Modified

1. **`backend/accounts/templates/base.html`**
   - Added Google Analytics script block
   - Conditional loading based on environment

2. **`backend/accounts/context_processors.py`** (NEW)
   - `google_analytics()` - Provides tracking ID
   - `site_config()` - Bonus: Site metadata

3. **`backend/auth_project/settings.py`**
   - Added context processors to TEMPLATES config

4. **`.env.example`** & **`backend/.env.example`**
   - Added GOOGLE_ANALYTICS_ID example

---

## Verify It's Working

### In Browser DevTools

1. Open: https://unisinq-v5ni.onrender.com
2. Right-click → Inspect → Network tab
3. Look for: `gtag.js` request
4. Should see: `200 OK` response ✅

### In Google Analytics Dashboard

1. Go to: https://analytics.google.com
2. Select your property
3. Go to: Realtime → Overview
4. Visit your app
5. Should see live visitor data ✅

---

## Google Analytics Features Available

Once tracking ID is set:

✅ **Page Views** - Track which pages users visit  
✅ **Events** - Track user interactions (clicks, signups)  
✅ **User Demographics** - Age, gender, interests  
✅ **Traffic Sources** - Where users come from  
✅ **Device Info** - Desktop, mobile, tablet  
✅ **Behavior** - User flow through your app  
✅ **Goals** - Track conversions  

---

## Tracking Custom Events

You can add custom event tracking in templates:

```html
<!-- Track button clicks -->
<button onclick="gtag('event', 'sign_up', {'method': 'email'})">
    Sign Up
</button>

<!-- Track form submissions -->
<form onsubmit="gtag('event', 'form_submit', {'form_id': 'contact'})">
    ...
</form>

<!-- Track custom actions -->
<script>
    gtag('event', 'view_project', {
        'project_id': '12345',
        'project_name': 'My Project'
    });
</script>
```

---

## Environment Variable

### What It Does

```
GOOGLE_ANALYTICS_ID=G-K0PB5TRR26
```

This 12-character ID tells Google Analytics:
- Which property to send data to
- Which account owns the tracking
- How to organize your analytics

### Where to Get It

1. Go to: https://analytics.google.com
2. Sign in with Google account
3. Create property (or use existing)
4. Get property ID: Format `G-XXXXXXXXXX`
5. Copy and use in environment variable

---

## Your Current ID

```
G-K0PB5TRR26
```

This is your tracking ID. Replace with your own if needed.

---

## Multiple Environments

### Local Development
```
GOOGLE_ANALYTICS_ID=G-K0PB5TRR26
```

### Production (Render)
```
GOOGLE_ANALYTICS_ID=G-K0PB5TRR26  (or different ID)
```

### Staging
```
GOOGLE_ANALYTICS_ID=G-XXXXXXXXXX  (different ID)
```

Each environment can have its own tracking ID!

---

## Debugging

### Analytics Not Showing Data?

**Check 1:** Environment variable is set
```bash
echo $GOOGLE_ANALYTICS_ID
```

**Check 2:** Page loads gtag.js
- Open DevTools → Network → search "gtag.js"
- Should see 200 OK response

**Check 3:** JavaScript console for errors
- Open DevTools → Console
- Should see no errors

**Check 4:** Google Analytics account
- Check property ID is correct
- Check analytics.google.com shows traffic

### Still Not Working?

1. Restart your app (Render: click Redeploy)
2. Clear browser cache (Ctrl+Shift+Delete)
3. Visit your app in new incognito window
4. Check Google Analytics in real-time view

---

## Best Practices

✅ **Track important events** - Signups, logins, conversions  
✅ **Use meaningful names** - `project_creation`, not `event1`  
✅ **Respect privacy** - Don't track sensitive data  
✅ **Monitor regularly** - Check analytics weekly  
✅ **Set goals** - Define what success means  

---

## Bonus: Site Configuration

The context processor also provides:

```python
'site_name': 'UniSinq'
'site_description': 'Connect. Collaborate. Create.'
```

Customize in environment:
```
SITE_NAME=MyApp
SITE_DESCRIPTION=My awesome app
```

Use in templates:
```html
<title>{{ site_name }} - {{ site_description }}</title>
```

---

## Files Reference

| File | Purpose | Status |
|------|---------|--------|
| `accounts/context_processors.py` | Provides analytics ID | ✅ Created |
| `base.html` | Loads tracking script | ✅ Updated |
| `settings.py` | Registers context processor | ✅ Updated |
| `.env.example` | Configuration template | ✅ Updated |
| `backend/.env.example` | Configuration template | ✅ Updated |

---

## Next Steps

1. **Set environment variable:**
   - Local: Add to `backend/.env`
   - Render: Add to Dashboard → Environment

2. **Verify it's working:**
   - Visit your app
   - Check DevTools for gtag.js
   - Check Google Analytics realtime view

3. **Add custom events:**
   - Track important user actions
   - Set up conversion goals
   - Monitor analytics regularly

---

## Status

✅ Google Analytics integrated  
✅ Environment-based configuration  
✅ Ready for Render deployment  
✅ Tracking ID set to: `G-K0PB5TRR26`  

---

**Documentation**: GOOGLE_ANALYTICS_SETUP.md  
**Implementation**: Complete & Ready!  
**Tracking ID**: G-K0PB5TRR26  

Your app is now tracking analytics! 📊
