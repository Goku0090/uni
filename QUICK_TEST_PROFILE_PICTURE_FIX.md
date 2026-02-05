# Quick Test: Profile Picture Fix

## What Was Fixed
Added `profile.refresh_from_db()` to refresh profile data after form save, ensuring the uploaded profile picture appears.

**File Changed**: `accounts/views.py` (Line 1356-1359)
**Line Added**: `profile.refresh_from_db()` after `form.save()`

---

## 3-Minute Test

### Step 1: Start Server
```bash
cd e:/login/auth_project
python manage.py runserver
```

### Step 2: Navigate to Profile
1. Login: `http://localhost:8000/student-profile/`
2. Or click "Profile" in navbar

### Step 3: Upload Picture
1. Click "Edit Profile" button
2. Click on the profile photo area
3. Select a JPG or PNG image from your computer
4. **Should show preview**
5. Click "Save Profile"

### Step 4: Verify
After page reload:
- ✅ Profile picture should appear
- ✅ Image should be visible in the circular frame
- ✅ No 404 errors in console (F12)
- ✅ Image should remain after refresh

---

## Troubleshooting

### Image still not showing?
1. **Check media directory exists**:
   ```bash
   # In Windows
   dir e:\login\auth_project\media\profile_photos\
   
   # Should show your image file
   ```

2. **Clear browser cache**:
   - Press: `Ctrl+Shift+Delete`
   - Select "All time"
   - Click "Clear data"

3. **Hard refresh**:
   - Press: `Ctrl+Shift+R` (or `Cmd+Shift+R` on Mac)

4. **Check server console**:
   - Should NOT show any errors about saving profile

5. **Verify file saved**:
   ```bash
   python manage.py shell
   >>> from accounts.models import StudentProfile
   >>> p = StudentProfile.objects.get(user__username='your_username')
   >>> p.profile_photo
   # Should show the file path, like: <ImageFieldFile: profile_photos/image.jpg>
   >>> p.profile_photo.url
   # Should show: /media/profile_photos/image.jpg
   >>> exit()
   ```

---

## What to Check

### 1. Template Shows URL
If you see a broken image icon, check the URL:
1. Right-click on broken image
2. "Copy image link"
3. Paste in address bar
4. Should show: `/media/profile_photos/yourimage.jpg`

### 2. Django Serves the File
1. Visit: `http://localhost:8000/media/profile_photos/` in browser
2. Should see the uploaded files
3. If 404, media serving is not configured

### 3. File Exists on Disk
```bash
# Check if file exists
dir e:\login\auth_project\media\profile_photos\

# If empty, file didn't save properly
```

---

## Expected Behavior

### Before Fix ❌
1. Upload image
2. Save profile
3. Page refreshes
4. **Profile picture doesn't appear**
5. Placeholder shows instead

### After Fix ✅
1. Upload image
2. Save profile
3. Page refreshes
4. **Profile picture appears immediately**
5. Image is persistent

---

## Code Verification

Check that the fix was applied:

```bash
# Search for the fix
grep -n "refresh_from_db" e:/login/auth_project/accounts/views.py

# Should show:
# 1360:            profile.refresh_from_db()
```

Or look at the file:
```python
# Line ~1356-1363 should have:
form.save()
messages.success(request, 'Profile updated successfully!')
logger.info(f"Student profile updated for user {request.user.username}")

# Refresh profile from database to ensure updated data (especially for profile_photo)
profile.refresh_from_db()

return redirect('student_profile')
```

---

## Tests for Different Scenarios

### Test 1: New User, First Upload
1. Create new user
2. Go to profile
3. Upload image
4. Save
5. ✅ Should appear

### Test 2: Change Existing Image
1. Login with user who has image
2. Edit profile
3. Upload different image
4. Save
5. ✅ New image should appear (old one deleted)

### Test 3: Remove Image
1. Login with user who has image
2. Leave image field blank
3. Save
4. ✅ Placeholder should show

### Test 4: Large Image
1. Use image > 1MB
2. Upload
3. ✅ Should work (limit is 5MB)

### Test 5: Multiple Users
1. Login as User A, upload image
2. Logout
3. Login as User B, upload different image
4. ✅ Each user should see their own image

---

## Performance Impact
- Minimal (one extra database query)
- Query is simple (just refresh one row)
- No noticeable impact on performance

---

## Browser Console Check

Open DevTools (F12) while testing:

### Good Signs
- No 404 errors
- No error messages
- Console shows: Profile photo uploaded logs
- Image file loads successfully

### Bad Signs
- 404 for `/media/profile_photos/...`
- JavaScript errors
- CSRF token errors
- Database errors

---

## Database Check

```bash
python manage.py shell

# Check profile exists
>>> from accounts.models import StudentProfile
>>> from django.contrib.auth.models import User
>>> user = User.objects.get(username='testuser')
>>> profile = StudentProfile.objects.get(user=user)

# Check image field
>>> profile.profile_photo
<ImageFieldFile: profile_photos/example.jpg>  # ✅ Good

>>> profile.profile_photo.url
'/media/profile_photos/example.jpg'  # ✅ Good

# Check if file physically exists
>>> import os
>>> os.path.exists(profile.profile_photo.path)
True  # ✅ File exists

>>> exit()
```

---

## Complete Verification Checklist

- [ ] Server started with `python manage.py runserver`
- [ ] Logged into profile page
- [ ] Uploaded test image
- [ ] Clicked "Save Profile"
- [ ] Page refreshed
- [ ] Image appears in profile ✅
- [ ] No 404 errors in console
- [ ] File exists in `auth_project/media/profile_photos/`
- [ ] Image URL works: `/media/profile_photos/yourimage.jpg`
- [ ] Multiple users can upload different images

---

## Ready for Production?

After passing above tests:
- ✅ Works in development
- ✅ Ready for staging test
- ✅ Ready for production deployment

---

## Time Estimates

- Local testing: 3 minutes
- Troubleshooting (if needed): 5-10 minutes
- Total verification: ~10 minutes

---

**Fix Status**: ✅ Applied
**Testing**: Ready
**Production Ready**: Yes (after testing)
