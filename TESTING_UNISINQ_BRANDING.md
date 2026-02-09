# Testing Guide - UniSinq Branding Update

## Quick Test Checklist

### Visual Tests (Manual)
- [ ] Login page displays logo correctly
- [ ] Home page shows new "UniSinq" branding
- [ ] Logo doesn't appear broken/missing
- [ ] All page titles show "UniSinq"
- [ ] Navigation text shows "UniSinq"
- [ ] Mobile view displays logo properly

### Functional Tests
- [ ] Click logo → redirects to home
- [ ] Page titles correct in browser tab
- [ ] Meta descriptions show new branding
- [ ] Notification badges use correct logo
- [ ] Real-time updates work (WebSocket)

### Text Content Tests
- [ ] Search for "UniSync" - should find only in comments/old docs
- [ ] All headings show "UniSinq"
- [ ] Email addresses show "unisinq.com"
- [ ] Social media handles show "@unisinq"

---

## Automated Test Commands

### 1. **Search for Remaining Old References**

#### Find in HTML Templates
```bash
cd auth_project
grep -r "UniSync" accounts/templates/ | grep -v ".pyc"
```
Expected: Should return 0 results (or only in base templates not updated)

#### Find in JavaScript
```bash
grep -r "unisync" static/js/
grep -r "UniSync" static/js/
```
Expected: Should return 0 results

#### Find in Python
```bash
grep -r "unisync" accounts/*.py
```
Expected: Only in test files or comments

### 2. **Check Logo File References**

```bash
# Find broken logo references
grep -r "unisync_logo" accounts/templates/
grep -r "unisync-logo" accounts/templates/
```
Expected: Should return 0 results

### 3. **Verify New References**

```bash
# Count new branding references
grep -r "UniSinq" accounts/templates/ | wc -l
grep -r "unisinq" static/js/ | wc -l
```
Expected: Both should have positive counts

---

## Browser Testing Steps

### Step 1: Clear Cache
```
Windows: Ctrl + Shift + Delete
Mac: Cmd + Shift + Delete
Linux: Ctrl + Shift + Delete

Then:
- Select "Images and files"
- Select "All time"
- Click "Clear data"
```

### Step 2: Test Login Page
```
1. Go to http://localhost:8000/login/
2. Verify:
   - Logo displays (not broken)
   - Page title shows "Login - UniSinq"
   - All text shows "UniSinq" (not "UniSync")
   - Logo image is visible and not 404
```

### Step 3: Test Home Page
```
1. Login or go to http://localhost:8000/
2. Verify:
   - Logo in navbar displays correctly
   - Page title shows "UniSinq"
   - All headings show "UniSinq"
   - No broken image icons
```

### Step 4: Test Find Collaborators
```
1. Go to http://localhost:8000/find-collaborators/
2. Verify:
   - Logo displays
   - Page title shows "UniSinq"
   - Navigation shows "UniSinq"
```

### Step 5: Test Contact Page
```
1. Go to http://localhost:8000/contact/
2. Verify:
   - Email shows "support@unisinq.com"
   - Logo displays correctly
   - Page title shows "UniSinq"
```

### Step 6: Test Notifications
```
1. Open DevTools (F12)
2. Check Console for:
   - WebSocket connection successful
   - Notification badges use correct logo
   - No 404 errors for logo
```

---

## Console Commands (DevTools)

### Check LocalStorage Keys
```javascript
// Open DevTools Console (F12)

// Check for new key
localStorage.getItem('unisinq_recent_searches')
// Should return data or null (not error)

// Check old key is gone or being replaced
localStorage.getItem('unisync_recent_searches')
// Should return null

// List all localStorage keys
Object.keys(localStorage)
// Should NOT contain 'unisync_recent_searches'
```

### Check WebSocket Connection
```javascript
// In Console:
console.log('WebSocket test:')

// Should see connection status in console
// Look for:
// "Connected to project X updates"
// "Connected to activity feed"
// "Connected to notifications"
```

### Check Logo Path
```javascript
// In Console:
document.querySelector('img[alt*="UniSinq"]')
// Should return the image element

document.querySelector('img[alt*="UniSync"]')
// Should return null (no old references)
```

---

## Network Testing

### Check Logo Download
1. Open DevTools → Network tab
2. Reload page
3. Filter by images
4. Look for `/static/images/logo.jpg`
   - Status should be 200 (not 404)
   - Size should be > 0 KB

### Check Requests
```
Network Tab → Filter:
✅ GET /static/images/logo.jpg → 200 OK
✅ GET /static/js/realtime-updates.js → 200 OK
❌ Should NOT see: /static/images/unisync_logo.jpg → 404
```

---

## Response Headers Testing

```bash
# Check if pages return correct meta tags
curl -I http://localhost:8000/
# Look for: "UniSinq" in headers if applicable

curl http://localhost:8000/ | grep -i "unisinq"
# Should show multiple matches
```

---

## Performance Testing

### Bundle Size Check
```bash
# Check if collectstatic works properly
python manage.py collectstatic --noinput

# Verify staticfiles directory
ls -la auth_project/staticfiles/images/
# Should show: logo.jpg (and not broken unisync files)
```

### Asset Loading
1. Open DevTools → Application → Cache Storage
2. Clear site data
3. Reload page
4. Check Network tab for asset load times
5. Verify logo loads in < 500ms

---

## Mobile Testing

### Responsive Design
```
DevTools → Toggle device toolbar (Ctrl+Shift+M)

Test sizes:
✅ Mobile (375px)
✅ Tablet (768px)
✅ Desktop (1024px+)

Verify:
- Logo displays at correct size
- No text truncation
- Navigation works
```

---

## Accessibility Testing

### Screen Reader Test
```bash
# Using NVDA or JAWS:
1. Navigate to logo
2. Should read: "UniSinq Logo"
   (not "UniSync Logo" or broken image)

# Check alt text
inspect logo element → alt="UniSinq Logo" ✓
```

### Color Contrast
1. Logo should have sufficient contrast
2. Text should be readable
3. Use: https://webaim.org/resources/contrastchecker/

---

## Email Testing

### Test Email Branding
```bash
cd auth_project

# Send test email
python manage.py shell

from django.core.mail import send_mail
send_mail(
    'Test Email from UniSinq',
    'This is a test',
    'from@example.com',
    ['to@example.com'],
)
```

Verify in email:
- Any logo images load correctly
- Any links reference new domain
- No old branding in template

---

## SEO Testing

### Meta Tags
```bash
# Check page meta tags
curl http://localhost:8000/ | grep -E "<title|og:|meta name"

# Should show:
# <title>UniSinq - ...</title>
# og:title content="UniSinq"
# etc.
```

---

## Final Sign-Off Checklist

### Before Deploying
- [ ] All pages tested in Chrome
- [ ] All pages tested in Firefox
- [ ] Mobile tested on iPhone simulator
- [ ] Mobile tested on Android simulator
- [ ] Logo loads without 404 errors
- [ ] No console JavaScript errors
- [ ] Static files collected successfully
- [ ] Cache cleared and fresh load works
- [ ] Email templates verified (if applicable)
- [ ] Social share buttons work correctly

### Production Deployment
- [ ] Backup current static files
- [ ] Run `collectstatic --noinput`
- [ ] Verify staging environment first
- [ ] Monitor error logs post-deployment
- [ ] Check Google Analytics
- [ ] Monitor user reports
- [ ] Prepare rollback plan

---

## Common Issues & Solutions

### Issue: Logo Still Shows As "unisync_logo.jpg"
**Solution:**
```bash
# Hard refresh browser
Ctrl+Shift+R (or Cmd+Shift+R on Mac)

# Clear browser cache completely
Settings → Clear browsing data → All time

# On server:
python manage.py collectstatic --noinput --clear
```

### Issue: LocalStorage Still Has Old Key
**Solution:**
```javascript
// In Console:
localStorage.removeItem('unisync_recent_searches');
location.reload();
```

### Issue: 404 for Logo
**Verify:**
```bash
ls -la auth_project/static/images/logo.jpg
# File should exist and be readable

python manage.py collectstatic --noinput
# Verify it copies to staticfiles/
```

### Issue: CSS Class Not Applied
**Check:**
```bash
grep -n "unisinq-logo\|unisync-logo" auth_project/accounts/templates/*.html
# All should use "unisinq-logo"

python manage.py collectstatic --noinput
# Rebuild CSS if using Sass
```

---

## Performance Baseline

### Expected Load Times
- Logo: 0-100ms
- Page load: < 2000ms
- First contentful paint: < 1000ms

### Monitor with DevTools
1. Open DevTools → Performance tab
2. Click reload and record
3. Check timeline for:
   - Logo load time
   - Rendering time
   - Script execution time

---

## Rollback Testing

### Test Rollback Works
```bash
# Stash current changes
git stash

# Verify old branding works
python manage.py runserver

# Test old version
# Then restore new changes
git stash pop
```

---

## Success Criteria

✅ **All** of these must pass:
1. [ ] Logo displays on all pages (not 404)
2. [ ] All page titles show "UniSinq"
3. [ ] No console errors related to images
4. [ ] LocalStorage uses new keys
5. [ ] Email addresses updated
6. [ ] Social handles updated (@unisinq)
7. [ ] Mobile responsive
8. [ ] No broken links
9. [ ] WebSocket working
10. [ ] Performance acceptable

---

## Testing Report Template

```markdown
## UniSinq Branding Testing Report

**Date**: [Date]
**Tester**: [Name]
**Environment**: [Dev/Staging/Prod]

### Results
- Logo Display: [✅/❌]
- Branding Text: [✅/❌]
- Mobile Responsive: [✅/❌]
- Performance: [✅/❌]
- Accessibility: [✅/❌]

### Issues Found
[List any issues]

### Sign-Off
[Name] - [Date]
```

---

*Use this guide to thoroughly test all branding changes before deployment.*
