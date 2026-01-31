# Test Profile Fix - Verification Guide

## Quick Test (5 minutes)

### Test 1: User Profile Modal
**Time**: 2 minutes

1. **Navigate to Find Collaborators**
   - URL: `http://localhost:8000/find-collaborators/`

2. **Click on any user**
   - Should open profile modal
   - Modal should show user info without 404 error

3. **Expected Result**:
   ```
   ✅ Modal opens
   ✅ Shows user profile data
   ✅ No error messages
   ✅ No 404 in console
   ```

4. **If it fails**:
   - Check browser console (F12 → Console tab)
   - Look for 404 errors
   - Verify the API URL is `/api/user-profile/<id>/`

---

### Test 2: Message Search
**Time**: 2 minutes

1. **Navigate to Messages**
   - URL: `http://localhost:8000/messages/`

2. **Use search feature**
   - Type a search query
   - Should search messages
   - Results should appear

3. **Expected Result**:
   ```
   ✅ Search works
   ✅ Results appear
   ✅ No 404 errors
   ✅ No console errors
   ```

---

### Test 3: Browser Console
**Time**: 1 minute

1. **Open Developer Tools**
   - Press: `F12`
   - Go to: `Console` tab

2. **Check for errors**
   - Should be CLEAN
   - No 404 messages
   - No API errors

3. **Expected Result**:
   ```
   ✅ No errors
   ✅ No warnings related to API
   ✅ Network requests successful
   ```

---

## Detailed Testing (20 minutes)

### Test Suite

#### Test 1.1: Find Collaborators - Profile Modal

**Setup**:
- Open Find Collaborators page
- Have 2+ users available

**Steps**:
1. [ ] Click on first user's name
2. [ ] Modal opens
3. [ ] Profile data displays (name, college, bio)
4. [ ] Close modal (click X or outside)
5. [ ] Click on second user's name
6. [ ] Modal opens with different user data
7. [ ] Check browser console - no errors

**Expected Results**:
- [ ] Modal opens instantly (no lag)
- [ ] User data appears correctly
- [ ] No 404 errors
- [ ] No JavaScript errors
- [ ] Works on second and subsequent clicks

**Pass/Fail**: ___________

---

#### Test 1.2: Find Collaborators - Avatar Click

**Steps**:
1. [ ] Click on user avatar image
2. [ ] Should trigger profile modal
3. [ ] Same data displays as name click

**Expected Results**:
- [ ] Avatar is clickable
- [ ] Modal opens
- [ ] Correct user shows

**Pass/Fail**: ___________

---

#### Test 2.1: Messages - Search Feature

**Setup**:
- Have some messages in database
- Go to Messages page

**Steps**:
1. [ ] Click in search box
2. [ ] Type a search term
3. [ ] Results appear
4. [ ] Clear search
5. [ ] Try another search term

**Expected Results**:
- [ ] Search works instantly
- [ ] Results update correctly
- [ ] No 404 errors
- [ ] No lag or delays

**Pass/Fail**: ___________

---

#### Test 3.1: Message Status Updates

**Steps**:
1. [ ] Send a test message
2. [ ] Observe message status indicator
3. [ ] Status should update (sent, delivered, read)
4. [ ] Check console for errors

**Expected Results**:
- [ ] Status updates without errors
- [ ] No 404 messages
- [ ] Status shows correctly

**Pass/Fail**: ___________

---

## Browser Console Testing

### Check Network Requests

1. **Open F12 Developer Tools**
2. **Go to Network tab**
3. **Perform actions** (click profile, search messages)
4. **Look for requests**:
   - Should see: `GET /api/user-profile/2/` → 200 OK ✅
   - Should see: `GET /api/messages/search/?q=...` → 200 OK ✅
   - Should NOT see: `/accounts/api/...` ❌

### Check Console for Errors

1. **Go to Console tab**
2. **Should be CLEAN** - no red errors
3. **No warnings** about 404
4. **Success messages** from API calls

---

## API Response Testing

### Test API Directly

You can test the API endpoints directly in browser:

```
URL: http://localhost:8000/api/user-profile/2/

Expected Response (200 OK):
{
  "id": 2,
  "username": "johndoe",
  "full_name": "John Doe",
  "college": "MIT",
  "location": "Boston",
  "interests": ["AI", "Web Dev"],
  "bio": "Student developer",
  "profile_photo": "https://..."
}
```

### cURL Test (Optional)

```bash
curl http://localhost:8000/api/user-profile/2/

Expected: JSON with user data
Not Found: JSON error {"error": "User not found"}
404 Error: HTML error page
```

---

## Checklist

### Pre-Testing
- [ ] Changes deployed locally
- [ ] Server running
- [ ] Database has test data
- [ ] Browser DevTools ready

### Functionality Tests
- [ ] Find collaborators page loads
- [ ] User profiles show in modals
- [ ] Message search works
- [ ] Message status updates work
- [ ] No 404 errors anywhere

### Browser Tests
- [ ] Tested in Chrome
- [ ] Tested in Firefox
- [ ] Tested on mobile (if possible)
- [ ] Console is clean
- [ ] No JavaScript errors

### API Tests
- [ ] GET /api/user-profile/2/ → 200
- [ ] GET /api/messages/search/ → 200
- [ ] GET /api/messages/ → 200
- [ ] No /accounts/api/ routes used

### Documentation
- [ ] Tests documented
- [ ] Issues recorded
- [ ] Results logged
- [ ] Ready to deploy

---

## Troubleshooting

### Still seeing 404 errors?

1. **Check the URL in browser DevTools Network tab**
   - Should be: `/api/user-profile/2/`
   - Not: `/accounts/api/user-profile/2/`

2. **If still showing old path**:
   - Hard refresh browser: `Ctrl+Shift+R`
   - Clear browser cache
   - Check template file was updated correctly

3. **Verify changes were saved**:
   - Check: `find_collaborators.html` line 1660
   - Check: `features/messages.html` line 1361 & 1616

### API returns 404 for valid user?

1. **Check user exists in database**
   - Go to Django admin: `/admin/auth/user/`
   - Verify user ID matches

2. **Check StudentProfile exists**
   - Some users might not have profile created
   - Create profile if needed

### Modal doesn't open?

1. **Check browser console for JavaScript errors**
2. **Verify user ID is being passed correctly**
3. **Check modal HTML exists in template**

---

## Performance Testing

### Load Times

Expected times:
- Profile modal: **< 500ms** to load
- Message search: **< 1s** to search
- Page load: **< 2s** total

Measure with:
1. Open DevTools → Network tab
2. Look at "XHR" filter
3. Check "Time" column

---

## Security Testing

### Verify Only Public Data

Profile modal should show:
- ✅ Name
- ✅ College
- ✅ Bio
- ✅ Avatar

Should NOT show:
- ❌ Email address
- ❌ Phone number
- ❌ Password hash
- ❌ Private information

---

## Regression Testing

Test that nothing broke:

- [ ] Login still works
- [ ] Registration still works
- [ ] Other pages load
- [ ] Existing messages display
- [ ] Projects still visible

---

## Results Summary

| Test | Expected | Actual | Status |
|------|----------|--------|--------|
| Profile Modal | Opens | ___ | ___ |
| Profile Data | Loads | ___ | ___ |
| 404 Errors | None | ___ | ___ |
| Console Errors | None | ___ | ___ |
| Message Search | Works | ___ | ___ |
| API Response | 200 OK | ___ | ___ |

---

## Sign-Off

**Tested By**: ___________________________

**Date**: ___________________________

**Time Spent**: ___________________________

**Result**: ✅ PASS / ❌ FAIL

**Issues Found**: 
```
_________________________________________________________________
_________________________________________________________________
```

**Notes**:
```
_________________________________________________________________
_________________________________________________________________
```

---

## When Ready to Deploy

After all tests pass:
1. [ ] Document any issues found
2. [ ] Update any workarounds
3. [ ] Commit changes
4. [ ] Deploy to staging
5. [ ] Test in staging (repeat this guide)
6. [ ] Deploy to production
7. [ ] Monitor for 24 hours

---

**Test Guide Created**: January 29, 2026  
**Expected Test Time**: 5-20 minutes  
**Difficulty**: Easy  
**Risk**: Very Low

---
