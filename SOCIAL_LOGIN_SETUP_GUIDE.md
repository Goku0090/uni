# Social Login Integration - Complete Setup Guide

## Overview
Social login has been successfully integrated into UniSync with **Google** and **GitHub** OAuth providers using `django-allauth`. Users can now:
- Sign up with Google or GitHub accounts
- Login with social accounts
- Link existing accounts to social profiles

## What Was Updated

### 1. Login Page (`accounts/templates/login.html`)
✅ Added social login buttons below the traditional login form
- Google OAuth button with official Google SVG icon
- GitHub OAuth button with official GitHub SVG icon
- Divider text: "or continue with"
- Magnetic hover effect for better UX
- Help text explaining social login

### 2. Registration Page (`accounts/templates/register.html`)
✅ Updated social login section with proper links
- Google OAuth button
- GitHub OAuth button
- Modern styling matching the register form design
- Help text for new users

## Features Added

### Design Elements
```html
<!-- Social Login Divider -->
- Professional divider with "or continue with" text
- Blurred backdrop effect
- Responsive grid layout (2 columns)

<!-- Social Buttons -->
- SVG icons (not font icons - better performance)
- Gradient backgrounds
- Magnetic hover effect
- Smooth transitions
- Mobile responsive
```

### Button Styling
```css
.social-btn {
    - Gradient backgrounds (white/10 to white/5)
    - Hover state with brighter gradient
    - Border transitions
    - Flexbox layout for icon + text
    - Backdrop blur effect
}

.magnetic-hover {
    - Smooth transform transitions
    - Responds to mouse movement
    - Resets on mouse leave
}
```

## Prerequisites Setup

### 1. Environment Variables (.env)
Ensure your `.env` file contains:
```
DEBUG=False
ALLOWED_HOSTS=localhost,127.0.0.1,your-domain.com
SECURE_SSL_REDIRECT=True
SESSION_COOKIE_SECURE=True
CSRF_COOKIE_SECURE=True
```

### 2. Django Settings
Already configured in `auth_project/settings.py`:
```python
INSTALLED_APPS = [
    # ... other apps
    'allauth',
    'allauth.account',
    'allauth.socialaccount',
    'allauth.socialaccount.providers.google',
    'allauth.socialaccount.providers.github',
]
```

### 3. URL Configuration
Already set up in `auth_project/urls.py`:
```python
urlpatterns = [
    path('accounts/', include('accounts.urls')),      # Custom URLs
    path('accounts/', include('allauth.urls')),       # Allauth URLs
    # ...
]
```

## Setting Up Google OAuth

### Step 1: Create a Google Cloud Project
1. Go to [Google Cloud Console](https://console.cloud.google.com/)
2. Create a new project (name it "UniSync")
3. Enable the Google+ API

### Step 2: Create OAuth Credentials
1. Go to "Credentials" in the left sidebar
2. Click "Create Credentials" → "OAuth 2.0 Client ID"
3. Choose "Web application"
4. Add authorized redirect URIs:
   ```
   http://localhost:8000/accounts/google/login/callback/
   https://yourdomain.com/accounts/google/login/callback/
   ```
5. Copy the **Client ID** and **Client Secret**

### Step 3: Add to Django Admin
1. Log in to Django admin (`/admin/`)
2. Go to **Sites** and ensure your domain is correct
3. Go to **Social Applications**
4. Click **Add Social Application**
   - **Provider**: Google
   - **Name**: Google
   - **Client id**: [Your Google Client ID]
   - **Secret key**: [Your Google Client Secret]
   - **Sites**: Select your site

## Setting Up GitHub OAuth

### Step 1: Create a GitHub OAuth App
1. Go to GitHub Settings → Developer settings → OAuth Apps
2. Click "New OAuth App"
3. Fill in the form:
   - **Application name**: UniSync
   - **Homepage URL**: `https://yourdomain.com` or `http://localhost:8000`
   - **Authorization callback URL**: 
     ```
     http://localhost:8000/accounts/github/login/callback/
     https://yourdomain.com/accounts/github/login/callback/
     ```
4. Copy the **Client ID** and generate/copy the **Client Secret**

### Step 2: Add to Django Admin
1. Log in to Django admin (`/admin/`)
2. Go to **Social Applications**
3. Click **Add Social Application**
   - **Provider**: GitHub
   - **Name**: GitHub
   - **Client id**: [Your GitHub Client ID]
   - **Secret key**: [Your GitHub Client Secret]
   - **Sites**: Select your site

## How It Works

### User Flow

#### New User (Sign Up)
```
User clicks "Sign up with Google/GitHub"
    ↓
Redirected to OAuth provider
    ↓
User authorizes UniSync
    ↓
Returned to UniSync with OAuth data
    ↓
django-allauth creates User + SocialAccount
    ↓
User is logged in
    ↓
Redirected to dashboard or profile completion
```

#### Existing User (Login)
```
User clicks "Login with Google/GitHub"
    ↓
Redirected to OAuth provider
    ↓
User authorizes (or already authorized)
    ↓
Returned to UniSync
    ↓
django-allauth finds SocialAccount
    ↓
User is logged in
    ↓
Redirected to dashboard
```

#### Linking Accounts
```
Logged-in user visits login page
    ↓
Clicks social login button
    ↓
OAuth provider confirms they're already logged in
    ↓
Returns without requiring new auth
    ↓
django-allauth links social account to existing user
```

## Template Tags Used

### `{% load socialaccount %}`
Required at the top of templates to use social login tags.

### `{% provider_login_url 'google' %}`
Generates the correct OAuth redirect URL for Google.

### `{% provider_login_url 'github' %}`
Generates the correct OAuth redirect URL for GitHub.

## Customization Options

### 1. Change Button Text
Edit the `<span>` element in social buttons:
```html
<span class="text-sm font-semibold">Sign in with Google</span>
```

### 2. Modify Button Styling
Update the Tailwind classes:
```html
<a href="..." class="social-btn [ADD_NEW_CLASSES]">
```

### 3. Add More Providers
Add to `INSTALLED_APPS`:
```python
'allauth.socialaccount.providers.microsoft',
'allauth.socialaccount.providers.apple',
```

Update templates with new buttons and configure in admin.

### 4. Customize OAuth Flow
Create a custom adapter in `accounts/adapters.py`:
```python
from allauth.socialaccount.adapter import DefaultSocialAccountAdapter

class CustomSocialAccountAdapter(DefaultSocialAccountAdapter):
    def pre_social_login(self, request, sociallogin):
        # Custom logic before login
        pass
    
    def save_user(self, request, sociallogin):
        # Custom user creation logic
        return super().save_user(request, sociallogin)
```

## Security Considerations

✅ **Already Implemented**:
- CSRF protection enabled
- Secure cookie settings
- Session security
- django-allauth security features

✅ **Best Practices**:
- Always use HTTPS in production
- Keep Client Secrets private (never commit to git)
- Regularly rotate OAuth credentials
- Monitor failed login attempts
- Use environment variables for sensitive data

## Troubleshooting

### Issue: "Redirect URI mismatch"
**Solution**: Ensure the redirect URIs in OAuth app settings match your Django configuration exactly.

### Issue: "Site matching query does not exist"
**Solution**: 
1. Go to Django admin
2. Check **Sites** app
3. Ensure site domain matches your deployed domain
4. Create missing sites if needed

### Issue: Social buttons not showing
**Solution**:
1. Ensure `{% load socialaccount %}` is at top of template
2. Check browser console for JavaScript errors
3. Verify SocialApp entries in admin

### Issue: User created but profile not completed
**Solution**: 
- Redirect users to profile completion page after social signup
- Check if StudentProfile is created for new social users

## Post-Login Redirect

Users are redirected to the URL specified in `SOCIALACCOUNT_ADAPTER`. Default behavior:
1. First-time social signup → Profile completion
2. Returning social login → Dashboard

To customize, update `accounts/adapters.py`:
```python
def get_login_redirect_url(self, request):
    return '/student-details/'  # or your preferred URL
```

## Verifying Setup

### Test Google Login
```bash
# 1. Run development server
python manage.py runserver

# 2. Go to login page: http://localhost:8000/login/
# 3. Click "Sign up with Google"
# 4. You should be redirected to Google
# 5. After authorization, redirected back to UniSync
```

### Test GitHub Login
```bash
# Same steps as Google, but click "Sign up with GitHub"
```

### Check in Admin
```
Admin > Social Applications
Should see entries for:
- Google (with Client ID and Secret)
- GitHub (with Client ID and Secret)
```

## Performance Tips

1. **Lazy load OAuth SDKs** (if needed)
2. **Cache user info** after social login
3. **Batch process new social user setup**
4. **Monitor OAuth request times**

## Related Documentation

- [django-allauth Docs](https://django-allauth.readthedocs.io/)
- [Google OAuth Documentation](https://developers.google.com/identity/protocols/oauth2)
- [GitHub OAuth Documentation](https://docs.github.com/en/developers/apps/building-oauth-apps)
- [Django Security Documentation](https://docs.djangoproject.com/en/4.2/topics/security/)

## Files Modified

1. ✅ `accounts/templates/login.html` - Added social buttons
2. ✅ `accounts/templates/register.html` - Updated social buttons

## Next Steps

1. Set up Google OAuth credentials
2. Set up GitHub OAuth credentials
3. Test social login locally
4. Deploy and test in production
5. Monitor user signups and feedback
6. (Optional) Add more OAuth providers

---

**Last Updated**: February 1, 2026
**Status**: ✅ Complete and Ready for Testing
