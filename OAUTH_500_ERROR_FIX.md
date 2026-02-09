# OAuth 500 Error Fix - GET /accounts/3rdparty/signup/

## Problem
Getting HTTP 500 (Internal Server Error) on OAuth endpoints:
```
GET http://127.0.0.1:8000/accounts/3rdparty/signup/ 500 (Internal Server Error)
```

## Root Cause
**Missing SocialApp Configuration** in django-allauth database

The `django-allauth` package requires SocialApp entries (Google, GitHub) to be created in the database, linked to the current Site. Without these, all OAuth redirect attempts fail.

## Solution

### Step 1: Run OAuth Setup Script
```bash
cd auth_project
python setup_oauth_fixed.py
```

**Output:**
```
[OK] Google OAuth UPDATED
  - Client ID: your-google-client-id
  - Sites: ['example.com']
[OK] GitHub OAuth CREATED
  - Client ID: your-github-client-id
  - Sites: ['example.com']
[SUCCESS] OAuth Setup Complete!
```

### Step 2: Configure Credentials in .env
Update your `.env` file with real OAuth credentials from Google and GitHub:

```ini
# Google OAuth
GOOGLE_OAUTH_CLIENT_ID=YOUR_GOOGLE_CLIENT_ID_HERE
GOOGLE_OAUTH_SECRET_KEY=YOUR_GOOGLE_SECRET_KEY_HERE

# GitHub OAuth  
GITHUB_OAUTH_CLIENT_ID=YOUR_GITHUB_CLIENT_ID_HERE
GITHUB_OAUTH_SECRET_KEY=YOUR_GITHUB_SECRET_KEY_HERE
```

### Step 3: Update Settings for Your Domain
If you changed your domain, update the Site in Django admin:

```bash
python manage.py shell
```

```python
from django.contrib.sites.models import Site
site = Site.objects.get_or_create(id=1)[0]
site.domain = 'yourdomain.com'  # Change to your actual domain
site.name = 'UniSync'
site.save()
```

## What the Script Does

1. **Creates/Updates SocialApp for Google**
   - Provider: google
   - Client ID from GOOGLE_OAUTH_CLIENT_ID env var
   - Secret from GOOGLE_OAUTH_SECRET_KEY env var

2. **Creates/Updates SocialApp for GitHub**
   - Provider: github
   - Client ID from GITHUB_OAUTH_CLIENT_ID env var
   - Secret from GITHUB_OAUTH_SECRET_KEY env var

3. **Links Both to Site ID 1**
   - Django's Site framework requires SocialApps to be linked to Sites
   - Uses default Site (example.com) or creates new Site

## Database Check
To verify SocialApps are properly configured:

```bash
python manage.py shell
```

```python
from allauth.socialaccount.models import SocialApp

# Check all SocialApps
apps = SocialApp.objects.all()
for app in apps:
    print(f"Provider: {app.provider}")
    print(f"Name: {app.name}")
    print(f"Client ID: {app.client_id}")
    print(f"Sites: {list(app.sites.all().values_list('domain', flat=True))}")
    print()
```

**Expected Output:**
```
Provider: google
Name: Google
Client ID: YOUR_CLIENT_ID
Sites: ['example.com']

Provider: github
Name: GitHub
Client ID: YOUR_CLIENT_ID
Sites: ['example.com']
```

## Manual Setup (Alternative)
If script fails, setup manually via Django admin:

1. Go to `http://localhost:8000/admin/`
2. Navigate to **Sites** → Click Site "example.com"
   - Change domain to your actual domain
   - Click Save

3. Navigate to **Social applications** → **Add Social Application**
   - **Provider:** Google
   - **Name:** Google
   - **Client id:** Your Google Client ID
   - **Secret key:** Your Google Secret Key
   - **Sites:** Select your Site
   - Click Save

4. Repeat for GitHub provider

## Getting OAuth Credentials

### Google OAuth
1. Go to [Google Cloud Console](https://console.cloud.google.com/)
2. Create new project or select existing
3. Enable **Google+ API**
4. Create **OAuth 2.0 Client ID** (Web Application)
5. Add authorized redirect URIs:
   ```
   http://localhost:8000/accounts/google/login/callback/
   http://127.0.0.1:8000/accounts/google/login/callback/
   https://yourdomain.com/accounts/google/login/callback/
   ```
6. Copy Client ID and Secret

### GitHub OAuth
1. Go to GitHub Settings → Developer settings → OAuth Apps
2. Click "New OAuth App"
3. Fill in:
   - **Application name:** UniSync
   - **Homepage URL:** http://localhost:8000
   - **Authorization callback URL:** http://localhost:8000/accounts/github/login/callback/
4. Copy Client ID and Client Secret

## Settings Configuration
Verify these settings in `auth_project/settings.py`:

```python
# Line 175 - Must be set to 1
SITE_ID = 1

# Line 179-180 - Authentication backends
AUTHENTICATION_BACKENDS = (
    'django.contrib.auth.backends.ModelBackend',
    'allauth.account.auth_backends.AuthenticationBackend',
)

# Line 188-195 - Allauth settings
SOCIALACCOUNT_AUTO_SIGNUP = True
SOCIALACCOUNT_LOGIN_ON_GET = True
ACCOUNT_LOGIN_METHODS = {'username'}
ACCOUNT_SIGNUP_FIELDS = ['email*', 'username*', 'password1*', 'password2*']
ACCOUNT_EMAIL_VERIFICATION = 'none'
ACCOUNT_LOGOUT_REDIRECT_URL = '/login/'
ACCOUNT_EMAIL_REQUIRED = True
SOCIALACCOUNT_QUERY_EMAIL = True

# Line 198-200 - Custom social signup form
SOCIALACCOUNT_FORMS = {
    'signup': 'accounts.forms.CustomSocialSignupForm',
}
```

## URL Configuration
Verify in `auth_project/urls.py`:

```python
path('accounts/', include('accounts.urls')),           # Custom URLs first
path('accounts/', include('allauth.urls')),           # Allauth URLs second
```

## Testing OAuth Flow
1. Start server: `python manage.py runserver`
2. Click "Login with Google" button
3. You should be redirected to Google consent screen
4. After consent, redirected back to app

**Expected Flow:**
```
Login Page
    ↓ Click "Login with Google"
Google Consent Screen
    ↓ Approve
Redirect to /accounts/google/login/callback/?code=...&state=...
    ↓ Exchange code for token
Auto-login to UniSync
```

## Common Issues

### Error 1: "No SocialApp found for provider"
**Solution:** Run setup_oauth_fixed.py script

### Error 2: "Site matching query does not exist"
**Solution:** Ensure SITE_ID = 1 in settings.py, or create Site:
```bash
python manage.py shell
from django.contrib.sites.models import Site
Site.objects.get_or_create(id=1, defaults={'domain': 'localhost:8000', 'name': 'UniSync'})
```

### Error 3: "Redirect URI mismatch"
**Solution:** Ensure callback URLs match exactly in OAuth app settings

### Error 4: Invalid Client ID/Secret
**Solution:** 
- Check credentials are copied correctly from OAuth provider
- No extra spaces or quotes
- Credentials match the domain in `.env` and settings

## Production Deployment
Before deploying to production:

1. **Update Site domain:**
   ```python
   Site.objects.get_or_create(id=1, defaults={
       'domain': 'yourdomain.com',
       'name': 'UniSync'
   })
   ```

2. **Update OAuth redirect URLs** in Google/GitHub console:
   - Google: `https://yourdomain.com/accounts/google/login/callback/`
   - GitHub: `https://yourdomain.com/accounts/github/login/callback/`

3. **Update .env variables** for production credentials

4. **Restart application:**
   ```bash
   python manage.py runserver
   # or
   gunicorn auth_project.wsgi
   ```

## File Changes
The following files were modified:

1. **accounts/signals_realtime.py** (Line 271)
   - Changed emoji logging to plain text for Windows compatibility
   - `✅ → [SUCCESS]`

2. **setup_oauth_fixed.py** (New file)
   - Script to automatically setup Google & GitHub SocialApps
   - Reads credentials from .env
   - Links to Site ID 1

## Next Steps
1. Run: `python setup_oauth_fixed.py`
2. Update .env with real OAuth credentials
3. Test OAuth login flow
4. Commit changes: `git add . && git commit -m "Fix OAuth 500 error with SocialApp setup"`

---
**Status:** OAuth configuration fixed and ready for testing
**Generated:** 2026-02-07
