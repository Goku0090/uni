# Debugging: No Collaborators Showing

## 🔍 Problem
The Find Collaborators page appears empty - no collaborators are displayed.

---

## ✅ Troubleshooting Steps

### Step 1: Check if StudentProfiles Exist

**Option A: Django Shell**
```bash
python manage.py shell
```

Then run:
```python
from accounts.models import StudentProfile
profiles = StudentProfile.objects.all()
print(f"Total profiles: {profiles.count()}")
for profile in profiles:
    print(f"  - {profile.user.username}: {profile.full_name or 'No name'}")
```

**Option B: Admin Panel**
1. Go to `/admin/`
2. Login as admin
3. Click "Student Profiles"
4. Check if any profiles exist

**Result:** If count is 0, no profiles exist yet.

---

### Step 2: Create Test Profiles

If no profiles exist, create some for testing:

**Using Script:**
```bash
python manage.py shell < create_test_profiles.py
```

**Or Manually (Django Shell):**
```python
from django.contrib.auth.models import User
from accounts.models import StudentProfile

# Create test users
user1 = User.objects.create_user(
    username='alice',
    email='alice@college.com',
    password='testpass123'
)

user2 = User.objects.create_user(
    username='bob',
    email='bob@college.com',
    password='testpass123'
)

# Create their profiles
StudentProfile.objects.create(
    user=user1,
    full_name='Alice Johnson',
    college='MIT',
    location='Boston, MA',
    bio='Passionate about web development',
    skills=['Python', 'React', 'Django'],
    interests=['Web Development', 'Open Source']
)

StudentProfile.objects.create(
    user=user2,
    full_name='Bob Smith',
    college='Stanford',
    location='San Francisco, CA',
    bio='Machine learning enthusiast',
    skills=['Python', 'TensorFlow', 'Data Science'],
    interests=['AI', 'Machine Learning']
)

print("Test profiles created!")
```

---

### Step 3: Verify Current User is Logged In

The page requires login. Check:

1. Are you logged in? 
   - Top right should show your username or "Logout" button
   - If not, go to `/accounts/login/` first

2. Does your user account have a StudentProfile?
   ```python
   from django.contrib.auth.models import User
   user = User.objects.get(username='yourname')
   profile = user.student_profile  # This should NOT error
   ```

3. If error, create a profile for yourself:
   ```python
   from accounts.models import StudentProfile
   StudentProfile.objects.create(
       user=user,
       full_name='Your Name',
       college='Your College',
       bio='Your bio'
   )
   ```

---

### Step 4: Check Database Query

**In Django Shell:**
```python
from accounts.models import StudentProfile
from django.contrib.auth.models import User

# Get current user (use your username)
current_user = User.objects.get(username='yourname')

# Query excludes current user - should see others
profiles = StudentProfile.objects.exclude(user=current_user)
print(f"Other profiles: {profiles.count()}")
for p in profiles:
    print(f"  - {p.full_name}")
```

**Result:** Should show other users' profiles (not your own).

---

### Step 5: Test the View Directly

**In Django Shell:**
```python
from django.test import RequestFactory
from accounts.views import find_collaborators
from django.contrib.auth.models import User

# Create a fake request
factory = RequestFactory()
request = factory.get('/find-collaborators/')

# Add user to request
request.user = User.objects.get(username='yourname')

# Call view
response = find_collaborators(request)

# Check context
print(response.context_data['search_results'])
```

---

## 🐛 Common Issues & Fixes

### Issue 1: No StudentProfiles Exist
**Symptom:** Count is 0 when querying StudentProfile  
**Cause:** No profiles have been created yet  
**Fix:** Create test profiles using script above

### Issue 2: Only 1 User with Profile
**Symptom:** You see empty page (your own profile is excluded)  
**Cause:** Need at least 2 users with profiles  
**Fix:** Create a second test user with profile

### Issue 3: User Not Logged In
**Symptom:** Page shows login required error  
**Cause:** Not authenticated  
**Fix:** Login first at `/accounts/login/`

### Issue 4: Current User Not in StudentProfile
**Symptom:** Page throws error  
**Cause:** User exists but profile doesn't  
**Fix:** Create profile via admin or script

### Issue 5: Skills Field is Empty
**Symptom:** Page loads but no data shows  
**Cause:** StudentProfile has blank skills/interests  
**Fix:** Add data to profiles:
```python
profile = StudentProfile.objects.get(user__username='alice')
profile.skills = ['Python', 'React', 'Django']
profile.interests = ['Web Dev', 'Open Source']
profile.save()
```

---

## 🔧 Quick Fix Script

Create `fix_no_collaborators.py`:

```python
#!/usr/bin/env python
import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'auth_project.settings')
django.setup()

from django.contrib.auth.models import User
from accounts.models import StudentProfile

# Create test users if they don't exist
users_data = [
    {
        'username': 'alice',
        'email': 'alice@test.com',
        'password': 'testpass123',
        'full_name': 'Alice Johnson',
        'college': 'MIT',
        'bio': 'Web developer interested in modern tech',
        'skills': ['Python', 'React', 'Django', 'PostgreSQL'],
        'interests': ['Web Development', 'Open Source', 'Startups']
    },
    {
        'username': 'bob',
        'email': 'bob@test.com',
        'password': 'testpass123',
        'full_name': 'Bob Smith',
        'college': 'Stanford',
        'bio': 'AI/ML enthusiast and data scientist',
        'skills': ['Python', 'TensorFlow', 'PyTorch', 'Data Science'],
        'interests': ['AI', 'Machine Learning', 'Deep Learning']
    },
    {
        'username': 'carol',
        'email': 'carol@test.com',
        'password': 'testpass123',
        'full_name': 'Carol White',
        'college': 'Berkeley',
        'bio': 'Full-stack developer with UI/UX focus',
        'skills': ['JavaScript', 'React', 'Node.js', 'CSS', 'Design'],
        'interests': ['Web Design', 'UX/UI', 'Frontend']
    },
    {
        'username': 'david',
        'email': 'david@test.com',
        'password': 'testpass123',
        'full_name': 'David Lee',
        'college': 'IIT Delhi',
        'bio': 'Mobile app developer and entrepreneur',
        'skills': ['Flutter', 'Swift', 'Java', 'Firebase'],
        'interests': ['Mobile Apps', 'Startups', 'IoT']
    }
]

count = 0
for data in users_data:
    username = data.pop('username')
    email = data.pop('email')
    password = data.pop('password')
    
    # Create user if not exists
    user, created = User.objects.get_or_create(
        username=username,
        defaults={'email': email}
    )
    
    if created:
        user.set_password(password)
        user.save()
        print(f"✓ Created user: {username}")
    
    # Create profile if not exists
    profile, created = StudentProfile.objects.get_or_create(
        user=user,
        defaults=data
    )
    
    if created:
        print(f"  ✓ Created profile for {username}")
        count += 1
    else:
        print(f"  ℹ Profile already exists for {username}")

print(f"\n✅ Done! Created {count} new profiles")
print(f"📋 Total profiles: {StudentProfile.objects.count()}")
print(f"\n🔐 Test credentials:")
for data in users_data:
    print(f"  - Username: {data['username']}, Password: testpass123")
```

**Run it:**
```bash
python fix_no_collaborators.py
```

---

## ✅ Verification Checklist

After fixes, verify:

- [ ] At least 2 StudentProfiles exist
- [ ] Current user is logged in
- [ ] Current user has a StudentProfile
- [ ] Other profiles have data (skills, interests, bio, college)
- [ ] Visit `/find-collaborators/`
- [ ] Should see collaborator cards displayed
- [ ] Search works
- [ ] Filters work
- [ ] Grid/List toggle works

---

## 📊 Expected Data Structure

Each StudentProfile should have:
```
{
    "user": <User object>,
    "full_name": "John Doe",
    "college": "MIT",
    "location": "Boston, MA",
    "bio": "Some description",
    "skills": ["Python", "React", "Django"],
    "interests": ["Web Dev", "Open Source"],
    "profile_photo": <optional>,
    "github": <optional>,
    "linkedin": <optional>
}
```

---

## 🚀 Quick Start (Copy-Paste)

**1. Check if profiles exist:**
```bash
python manage.py shell
```

```python
from accounts.models import StudentProfile
print(f"Total profiles: {StudentProfile.objects.count()}")
exit()
```

**2. If 0 profiles, run fix script:**
```bash
python fix_no_collaborators.py
```

**3. Visit the page:**
```
http://127.0.0.1:8000/find-collaborators/
```

**4. Login as test user:**
- Username: `alice` (or bob/carol/david)
- Password: `testpass123`

**5. You should now see collaborators!** ✅

---

## 🐛 Still Not Working?

### Check Django Logs
```bash
# Look for errors in console when running:
python manage.py runserver
```

### Check Template Rendering
In browser DevTools (F12):
1. Network tab - check if page loaded
2. Console tab - check for JS errors
3. Inspector - check HTML structure

### Database Check
```bash
python manage.py dbshell
sqlite> SELECT COUNT(*) FROM accounts_studentprofile;
```

### View Function Debug
Add this to `find_collaborators()` in views.py:
```python
print(f"DEBUG: Found {len(search_results)} search results")
print(f"DEBUG: Found {len(suggestions)} suggestions")
```

Then check console output when visiting page.

---

## 📞 Still Need Help?

1. Run the fix script above
2. Check all steps in verification checklist
3. Share the output from Django shell queries
4. Check console logs

**The most common cause:** No StudentProfiles exist in the database.

Running `python fix_no_collaborators.py` should solve it! ✅

---

## Summary

**If no collaborators show:**

1. **Create test data:**
   ```bash
   python fix_no_collaborators.py
   ```

2. **Login with test account:**
   - Username: alice
   - Password: testpass123

3. **Visit the page:**
   - http://127.0.0.1:8000/find-collaborators/

**Done!** You should now see collaborators. 🎉
