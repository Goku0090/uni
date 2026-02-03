# Social Login Quick Start Guide

## ✅ What's Ready

Social login buttons have been added to:
- ✅ Login page (`/login/`)
- ✅ Registration page (`/register/`)

Both pages now feature:
- Google OAuth button
- GitHub OAuth button
- Professional styling with hover effects
- Mobile responsive design

## 🚀 Get Started in 5 Minutes

### 1. Create Google OAuth Credentials

```bash
# Step-by-step:
1. Visit: https://console.cloud.google.com/
2. Create new project → name it "UniSync"
3. Enable Google+ API
4. Credentials → Create OAuth 2.0 Client ID → Web Application
5. Authorized Redirect URIs:
   - http://localhost:8000/accounts/google/login/callback/
   - https://yourdomain.com/accounts/google/login/callback/
6. Copy: Client ID and Client Secret
```

### 2. Create GitHub OAuth Credentials

```bash
# Step-by-step:
1. Visit: https://github.com/settings/developers
2. OAuth Apps → New OAuth App
3. Fill form:
   - App name: UniSync
   - Homepage URL: http://localhost:8000
   - Authorization callback: http://localhost:8000/accounts/github/login/callback/
4. Copy: Client ID and Client Secret
```

### 3. Add to Django Admin

```bash
# In your terminal:
python manage.py runserver

# In browser:
1. Go to: http://localhost:8000/admin/
2. Login with admin account
3. Navigate to: Social Applications
4. Click: Add Social Application
```

#### Google Setup in Admin
```
Provider:    Google
Name:        Google
Client id:   [Your Google Client ID]
Secret key:  [Your Google Client Secret]
Sites:       [Your Site]
Click:       Save
```

#### GitHub Setup in Admin
```
Provider:    GitHub
Name:        GitHub
Client id:   [Your GitHub Client ID]
Secret key:  [Your GitHub Client Secret]
Sites:       [Your Site]
Click:       Save
```

## 🧪 Test Locally

```bash
# 1. Start development server
python manage.py runserver

# 2. Open in browser
http://localhost:8000/login/

# 3. Click "Google" or "GitHub" button

# 4. You should be redirected to OAuth provider

# 5. After authorization, redirected back to UniSync

# ✅ If successful, you're logged in!
```

## 📱 UI Preview

### Login Page
```
┌─────────────────────────────────┐
│   UniSync Login                 │
├─────────────────────────────────┤
│ [Username/Email input]          │
│ [Password input]                │
│ [Remember me] [Forgot pwd?]     │
│ [Login Button]                  │
│                                 │
│  ─── or continue with ───       │
│                                 │
│ [Google] [GitHub]               │
│                                 │
│ New to UniSync? Sign up ↗       │
└─────────────────────────────────┘
```

### Register Page
```
┌─────────────────────────────────┐
│   UniSync Sign Up               │
├─────────────────────────────────┤
│ Step 1: Account Credentials     │
│ [Form fields...]                │
│ [Next Button]                   │
│                                 │
│  ─── or sign up with ───        │
│                                 │
│ [Google] [GitHub]               │
│                                 │
│ Already have account? Sign in ↗ │
└─────────────────────────────────┘
```

## 🎨 Button Features

```html
✨ Design Elements
├── SVG Icons (Google & GitHub)
├── Gradient Backgrounds
├── Magnetic Hover Effects
├── Smooth Transitions
├── Responsive Layout
└── Dark Theme Compatible

🔒 Security
├── CSRF Protection
├── Secure Sessions
├── SSL/TLS Ready
└── Secure Cookies
```

## 📋 Checklist

```
Local Setup
☐ Google OAuth credentials created
☐ GitHub OAuth credentials created
☐ Social Apps added in Django admin
☐ Sites app configured correctly
☐ Tested Google login locally
☐ Tested GitHub login locally

Production Deployment
☐ Update allowed domains
☐ Set SECURE_SSL_REDIRECT=True
☐ Set SESSION_COOKIE_SECURE=True
☐ Set CSRF_COOKIE_SECURE=True
☐ Update OAuth redirect URIs for production domain
☐ Test social login on production
☐ Monitor login errors
☐ Collect user feedback
```

## 🔗 Useful Links

| Resource | URL |
|----------|-----|
| Google Cloud Console | https://console.cloud.google.com/ |
| GitHub OAuth Apps | https://github.com/settings/developers |
| django-allauth Docs | https://django-allauth.readthedocs.io/ |
| Django Security | https://docs.djangoproject.com/en/4.2/topics/security/ |

## ⚡ Common Issues & Fixes

### "Redirect URI mismatch"
```
Fix: Make sure redirect URI in OAuth app exactly matches your Django callback URL
Example: http://localhost:8000/accounts/google/login/callback/
         ↑ Must be exact (including trailing slash)
```

### "Social app not found"
```
Fix: Go to Django admin → Social Applications → Verify entry exists
     Check that Site is selected and matches SITE_ID
```

### "Site matching query does not exist"
```
Fix: Django admin → Sites → Check domain matches
     Default: example.com → Change to localhost:8000 for development
```

## 🎯 What Happens When User Clicks

```
User clicks "Sign in with Google"
        ↓
Django redirects to Google OAuth
        ↓
User logs in with Google (or authorizes if already logged in)
        ↓
Google redirects back to Django with auth code
        ↓
Django exchanges code for access token
        ↓
django-allauth creates/finds user and logs them in
        ↓
User redirected to dashboard
        ↓
✅ User is authenticated!
```

## 📝 Code Changes Summary

```
Modified Files:
1. accounts/templates/login.html
   - Added Google OAuth button
   - Added GitHub OAuth button
   - Professional divider section

2. accounts/templates/register.html
   - Updated social login buttons
   - Replaced icon buttons with SVG
   - Added proper OAuth links
   - Help text for users

Configuration Files (Already Set):
- auth_project/settings.py → allauth installed & configured
- auth_project/urls.py → OAuth URLs included
```

## 🚀 Performance Impact

- **Page Load**: Minimal (buttons are HTML, no SDK loading)
- **Redirect**: Fast (redirects to OAuth provider)
- **User Creation**: ~1 second (django-allauth optimized)
- **Database**: Adds 1 SocialAccount row per OAuth user

## 🔐 Security Notes

```
✅ Implemented:
- CSRF tokens on forms
- Secure session cookies
- django-allauth validation
- OAuth provider trust

⚠️ Remember:
- Never hardcode client secrets
- Use environment variables
- Keep secrets out of git
- Regularly rotate credentials
```

## 📞 Support

If you encounter issues:

1. **Check Django logs**
   ```bash
   tail -f logs/debug.log
   ```

2. **Check browser console**
   ```
   F12 → Console tab → Look for errors
   ```

3. **Verify credentials**
   ```
   Django admin → Social Applications → Check credentials
   ```

4. **Test manually**
   ```bash
   python manage.py shell
   >>> from allauth.socialaccount.models import SocialApp
   >>> SocialApp.objects.all()
   ```

---

## 🎉 You're All Set!

Once you've set up the OAuth credentials and added them to Django admin:

1. ✅ Visit your login page
2. ✅ Click social login button
3. ✅ You're ready to use social authentication!

**Estimated Time**: 10-15 minutes setup per provider

**Questions?** Check the full guide: `SOCIAL_LOGIN_SETUP_GUIDE.md`
