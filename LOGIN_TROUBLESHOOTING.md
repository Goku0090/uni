# Login Issue - Troubleshooting Guide

## Problem Statement
The login functionality is not working properly.

## Current Code Analysis

### 1. **LoginForm** (`forms.py`, lines 99-120)
```python
class LoginForm(AuthenticationForm):
    username = forms.CharField(...)
    password = forms.CharField(...)
    remember_me = forms.BooleanField(required=False, ...)
```
- ✅ Form extends Django's `AuthenticationForm`
- ✅ Has username, password fields
- ✅ Has "remember me" checkbox
- **Status**: Form looks correct

### 2. **Login View** (`views.py`, lines 313-369)
```python
def login_view(request):
    if request.method == 'POST':
        form = LoginForm(request, request.POST)
        if form.is_valid():
            # Authenticate user
            user = authenticate(request, username=username, password=password)
            if user:
                # Direct login OR OTP login
                login(request, user)
                return redirect('main_home')
            else:
                messages.error(request, 'Invalid username or password.')
        else:
            messages.error(request, 'Please correct the errors below.')
```
- ✅ Handles POST requests
- ✅ Validates form
- ✅ Authenticates user
- ✅ Redirects on success
- **Status**: Logic appears correct

### 3. **Login Template** (`login.html`, lines 117-177)
```html
<form method="POST" action="" class="space-y-6" id="loginForm" novalidate>
    {% csrf_token %}
    <input type="text" name="username" ... />
    <input type="password" name="password" ... />
    <button type="submit">Login</button>
</form>
```
- ✅ POST method
- ✅ CSRF token included
- ✅ Username/password fields with correct names
- **Status**: Template is correct

### 4. **Settings** (`settings.py`)
- ⚠️ **CSRF Middleware is DISABLED** (Line 68):
  ```python
  # 'django.middleware.csrf.CsrfViewMiddleware',  # Temporarily disabled for login testing
  ```
- ✅ CSRF token still included in template (works without middleware)
- **Note**: While disabled for testing, shouldn't cause login to fail

### 5. **URL Routing** (`urls.py`, Line 22)
```python
path('login/', views.login_view, name='login'),
```
- ✅ Route exists and properly named
- **Status**: Routing is correct

---

## Potential Issues & Solutions

### Issue 1: **Form Validation Failure**
**Symptom**: Form appears invalid when submitted

**Check these**:
1. Is username valid format (3-150 chars)?
2. Does user exist in database?
3. Are password/username correct?

**Solution**:
```python
# Add debug logging in login_view
print(f"DEBUG: Form valid: {form.is_valid()}")
if not form.is_valid():
    print(f"DEBUG: Form errors: {form.errors}")
```

---

### Issue 2: **Username/Email Not Recognized**
**Symptom**: "Invalid username or password" even with correct credentials

**Problem**: LoginForm uses `username` field, but you might be entering email

**Current Code** (Line 318-325):
```python
form = LoginForm(request, request.POST)
if form.is_valid():
    username = form.cleaned_data['username']
    # authenticate expects username, not email
    user = authenticate(request, username=username, password=password)
```

**Solution**: Modify login_view to accept both username AND email:

```python
def login_view(request):
    if request.method == 'POST':
        form = LoginForm(request, request.POST)
        if form.is_valid():
            username_or_email = form.cleaned_data['username']
            password = form.cleaned_data['password']
            
            # Try username first, then email
            user = authenticate(request, username=username_or_email, password=password)
            
            if not user:
                # Try email login
                try:
                    user_obj = User.objects.get(email=username_or_email)
                    user = authenticate(request, username=user_obj.username, password=password)
                except User.DoesNotExist:
                    user = None
            
            if user:
                login(request, user)
                return redirect('main_home')
            else:
                messages.error(request, 'Invalid username/email or password.')
```

---

### Issue 3: **Redirect Not Working**
**Symptom**: Login button clicked but page doesn't change

**Check these**:
1. Is `main_home` URL name defined? ✅ (confirmed in urls.py)
2. Is redirect happening? (Check server logs)
3. Is JavaScript preventing form submission?

**JavaScript Check** (login.html):
```javascript
document.getElementById('loginForm').addEventListener('submit', function(e) {
    // Check if form submission is prevented
    console.log('Form submitting');
});
```

---

### Issue 4: **Session Not Set**
**Symptom**: User logs in but session doesn't persist

**Check**:
1. Is `login(request, user)` being called? ✅ (Yes, line 338)
2. Are session middleware loaded? ✅ (Yes, confirmed in settings)
3. Are session cookies enabled?

---

## Quick Debugging Steps

### Step 1: Enable Verbose Logging
Add to login_view (already has print statements):
```python
logger.info(f"Login attempt: {request.POST.get('username')}")
logger.info(f"Form valid: {form.is_valid()}")
logger.info(f"User authenticated: {user}")
```

### Step 2: Test with Test User
Create test user via shell:
```bash
python manage.py shell
>>> from django.contrib.auth.models import User
>>> User.objects.create_user(username='testuser', email='test@example.com', password='TestPass123')
```

### Step 3: Verify Database Connection
```bash
python manage.py dbshell
```

### Step 4: Check Console Errors
Open browser dev tools (F12) and check:
- Network tab (form submission)
- Console tab (JavaScript errors)
- Application tab (session/cookies)

---

## Recommended Fix: Enhanced Email/Username Login

**File**: `accounts/views.py`  
**Location**: Lines 313-369  
**Change**: Modify login_view to support both email and username

```python
def login_view(request):
    if request.method == 'POST':
        form = LoginForm(request, request.POST)
        if form.is_valid():
            username_or_email = form.cleaned_data['username']
            password = form.cleaned_data['password']
            
            # Try username first
            user = authenticate(request, username=username_or_email, password=password)
            
            # If username fails, try email
            if not user:
                try:
                    user_obj = User.objects.get(email=username_or_email)
                    user = authenticate(request, username=user_obj.username, password=password)
                except User.DoesNotExist:
                    user = None
            
            if user:
                login(request, user)
                messages.success(request, 'Login successful!')
                return redirect('main_home')
            else:
                logger.warning(f"Failed login attempt: {username_or_email}")
                messages.error(request, 'Invalid username/email or password.')
        else:
            logger.warning(f"Form validation failed: {form.errors}")
            messages.error(request, 'Please correct the errors below.')
    else:
        form = LoginForm(request)
    
    context = {
        'form': form,
        'GITHUB_CLIENT_ID': os.getenv('GITHUB_CLIENT_ID'),
        'GOOGLE_CLIENT_ID': os.getenv('GOOGLE_CLIENT_ID'),
    }
    return render(request, 'login.html', context)
```

---

## Files to Check/Modify

| File | Issue | Action |
|------|-------|--------|
| `accounts/views.py` | Email login not supported | ✏️ Modify login_view |
| `accounts/forms.py` | LoginForm basic | ✏️ Could enhance |
| `login.html` | Template OK | ✅ No change needed |
| `settings.py` | CSRF disabled | ✏️ Re-enable when ready |
| `urls.py` | Routes OK | ✅ No change needed |

---

## Testing Checklist

After implementing fix:
- [ ] Test with username
- [ ] Test with email
- [ ] Test with wrong password
- [ ] Test with non-existent user
- [ ] Verify redirect to main_home
- [ ] Check session persists
- [ ] Test logout
- [ ] Test "Remember me" checkbox

---

## Next Steps

1. **Implement email login** in views.py
2. **Test with sample user**
3. **Check browser console** for errors
4. **Enable CSRF protection** once stable
5. **Add comprehensive logging**
