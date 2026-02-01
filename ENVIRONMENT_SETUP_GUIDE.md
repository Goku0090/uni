# Complete Environment Setup Guide

## Table of Contents
1. [Email Services Setup](#email-services)
2. [Social Authentication Setup](#social-authentication)
3. [External APIs Setup](#external-apis)
4. [Environment Variables](#environment-variables)

---

# EMAIL SERVICES

## Option 1: Brevo (RECOMMENDED)

### Step 1: Create Brevo Account
1. Go to https://www.brevo.com
2. Sign up (Free tier available)
3. Verify email

### Step 2: Get API Key
1. Login to Brevo
2. Go to **Settings** → **API Keys**
3. Under "SMTP & API Relay", click **"Create**
4. Copy the API Key (looks like: `xsw34a7e9d8c7f6b5a4d`)

### Step 3: Add Verified Sender Email
1. Go to **Senders List & Contacts** → **Senders List**
2. Click **"Add Sender"**
3. Enter your email (or domain email like noreply@yourdomain.com)
4. Verify via email link sent by Brevo

### Step 4: Configure Environment Variable
```
BREVO_API_KEY=xsw34a7e9d8c7f6b5a4d
```

**Advantages:**
- Free tier generous
- Reliable delivery
- Good reputation
- Built-in phone support
- Easy to use dashboard

---

## Option 2: ZeptoMail

### Step 1: Create ZeptoMail Account
1. Go to https://www.zeptomail.com
2. Sign up
3. Verify email

### Step 2: Get API Key & Token
1. Dashboard → **Account Settings**
2. Click **"API Keys"**
3. Generate new API key
4. Also get API Token from same page

### Step 3: Verify Sender
1. Go to **Senders**
2. Add new sender email
3. Verify via email link

### Step 4: Configure Environment Variables
```
ZEPTO_MAIL_API_KEY=your-api-key
ZEPTO_MAIL_TOKEN=your-token
```

---

## Option 3: Gmail SMTP (Not Recommended for Production)

### Step 1: Enable 2FA on Gmail
1. Go to https://myaccount.google.com/security
2. Enable 2-Step Verification

### Step 2: Generate App Password
1. Go to https://myaccount.google.com/apppasswords
2. Select "Mail" and "Windows Computer"
3. Generate app password
4. Copy 16-character password (ignore spaces)

### Step 3: Configure Environment Variables
```
EMAIL_HOST_USER=your-email@gmail.com
EMAIL_HOST_PASSWORD=xxxx xxxx xxxx xxxx
```

**Note:** This method is less reliable and may have rate limits.

---

## Test Email Configuration

After setting up, test in Django shell:

```bash
# For Render or Railway, use their Shell feature
python auth_project/manage.py shell
```

```python
from django.core.mail import send_mail

send_mail(
    subject='Test Email',
    message='This is a test email from UniSync',
    from_email='noreply@yourdomain.com',
    recipient_list=['your-test-email@gmail.com'],
    fail_silently=False
)

print("Email sent successfully!")
```

If successful, you'll see the email in your inbox.

---

# SOCIAL AUTHENTICATION

## Google OAuth 2.0

### Step 1: Create Google Cloud Project
1. Go to https://console.cloud.google.com
2. Click **"Select a Project"** (top left)
3. Click **"New Project"**
4. Name: `UniSync`
5. Click **"Create"**

### Step 2: Enable Google+ API
1. Search for **"Google+ API"** in search box
2. Click "Google+ API"
3. Click **"Enable"**

### Step 3: Create OAuth Credentials
1. Go to **"Credentials"** (left sidebar)
2. Click **"Create Credentials"** → **"OAuth client ID"**
3. If prompted, configure OAuth consent screen first:
   - User Type: External
   - Fill in app name, email, developer contact
   - Add scopes: email, profile, openid

### Step 4: Create OAuth Client
1. Application Type: **Web application**
2. Name: `UniSync Web`
3. **Authorized JavaScript origins:**
   ```
   http://localhost:8000
   https://yourdomain.com
   https://yourdomain.onrender.com
   https://yourdomain.up.railway.app
   ```
4. **Authorized redirect URIs:**
   ```
   http://localhost:8000/accounts/google/login/callback/
   https://yourdomain.com/accounts/google/login/callback/
   https://yourdomain.onrender.com/accounts/google/login/callback/
   https://yourdomain.up.railway.app/accounts/google/login/callback/
   ```
5. Click **"Create"**

### Step 5: Copy Credentials
```
GOOGLE_CLIENT_ID=xxxxx.apps.googleusercontent.com
GOOGLE_CLIENT_SECRET=GOCSPX-xxxxx
```

### Step 6: Add to Django Admin
After deploying:
1. Go to `/admin`
2. Login with superuser
3. Go to **Sites** → Edit domain to your domain
4. Go to **Social Applications** → **Add**
5. Provider: Google
6. Name: Google
7. Client id: (paste)
8. Secret key: (paste)
9. Sites: Select your site
10. Save

---

## GitHub OAuth

### Step 1: Create OAuth App
1. Go to GitHub → **Settings** → **Developer settings** → **OAuth Apps**
2. Click **"New OAuth App"**

### Step 2: Fill Application Details
- **Application name:** UniSync
- **Homepage URL:** `https://yourdomain.com`
- **Application description:** Student Collaboration Platform
- **Authorization callback URL:**
  ```
  https://yourdomain.com/accounts/github/login/callback/
  https://yourdomain.onrender.com/accounts/github/login/callback/
  https://yourdomain.up.railway.app/accounts/github/login/callback/
  ```

### Step 3: Copy Credentials
- **Client ID** → `GITHUB_CLIENT_ID`
- **Client Secret** → `GITHUB_CLIENT_SECRET` (Generate new if needed)

```
GITHUB_CLIENT_ID=Iv1.xxxxx
GITHUB_CLIENT_SECRET=xxxxxxxx
```

### Step 4: Add to Django Admin
1. Go to `/admin` after deploying
2. Login with superuser
3. Go to **Social Applications** → **Add**
4. Provider: GitHub
5. Name: GitHub
6. Client id: (paste)
7. Secret key: (paste)
8. Sites: Select your site
9. Save

---

# EXTERNAL APIS

## RapidAPI (Universities List)

### Step 1: Sign Up
1. Go to https://rapidapi.com
2. Sign up with GitHub/Google

### Step 2: Search Universities API
1. Search **"Universities List"** in RapidAPI
2. Select the API
3. Click **"Subscribe"** (Free plan available)

### Step 3: Get API Key
1. Go to your dashboard
2. Click on the API
3. Copy **API Key** (or X-RapidAPI-Key)

```
RAPIDAPI_KEY=xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx
```

### Step 4: Test API
```python
import requests

url = "https://universities-list.p.rapidapi.com/"
headers = {
    "X-RapidAPI-Key": "your-api-key",
    "X-RapidAPI-Host": "universities-list.p.rapidapi.com"
}
response = requests.get(url, headers=headers, params={"name": "Stanford"})
print(response.json())
```

---

# ENVIRONMENT VARIABLES

## Generation Guide

### Generate Secret Key
```bash
python -c 'from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())'
```

### All Required Variables

#### Core Django
```
DEBUG=False
SECRET_KEY=django-insecure-xxxxxxxxxxxxx
ALLOWED_HOSTS=yourdomain.com,www.yourdomain.com,yourdomain.onrender.com,yourdomain.up.railway.app
```

#### Database
```
DATABASE_URL=postgresql://user:password@host:port/dbname
# (Auto-provided by Render/Railway)
```

#### Email (Choose One)
```
# Brevo
BREVO_API_KEY=xxxxx

# OR ZeptoMail
ZEPTO_MAIL_API_KEY=xxxxx
ZEPTO_MAIL_TOKEN=xxxxx

# OR Gmail
EMAIL_HOST_USER=email@gmail.com
EMAIL_HOST_PASSWORD=xxxx xxxx xxxx xxxx

# Always set this
DEFAULT_FROM_EMAIL=noreply@yourdomain.com
```

#### Social Authentication
```
GOOGLE_CLIENT_ID=xxxxx.apps.googleusercontent.com
GOOGLE_CLIENT_SECRET=GOCSPX-xxxxx

GITHUB_CLIENT_ID=Iv1.xxxxx
GITHUB_CLIENT_SECRET=xxxxx
```

#### External Services
```
RAPIDAPI_KEY=xxxxx
```

#### Optional: Caching
```
REDIS_URL=redis://localhost:6379/0
```

#### Optional: Monitoring
```
SENTRY_DSN=https://xxxxx@sentry.io/xxxxx
```

#### Security (Production)
```
SECURE_SSL_REDIRECT=True
SESSION_COOKIE_SECURE=True
CSRF_COOKIE_SECURE=True
SECURE_HSTS_SECONDS=31536000
SECURE_HSTS_INCLUDE_SUBDOMAINS=True
SECURE_HSTS_PRELOAD=True
```

---

## Render Environment Variables Interface

1. Go to web service
2. Click **"Environment"**
3. Add each variable:
   - Key: `VARIABLE_NAME`
   - Value: `variable_value`
4. Save/Deploy

---

## Railway Environment Variables Interface

1. Click web service
2. Go to **"Variables"** tab
3. Add each variable:
   - Key: `VARIABLE_NAME`
   - Value: `variable_value`
4. Auto-redeploys

---

## Local Development

Create `.env` in `auth_project/`:

```bash
# auth_project/.env
DEBUG=True
SECRET_KEY=your-dev-secret-key
ALLOWED_HOSTS=localhost,127.0.0.1
DATABASE_URL=sqlite:///db.sqlite3

# Email - Use console for development
BREVO_API_KEY=

# Social Auth (optional for local dev)
GOOGLE_CLIENT_ID=
GOOGLE_CLIENT_SECRET=
GITHUB_CLIENT_ID=
GITHUB_CLIENT_SECRET=

DEFAULT_FROM_EMAIL=noreply@localhost:8000
```

Then load in Django:
```python
from dotenv import load_dotenv
load_dotenv()  # Already in settings.py
```

---

## Security Best Practices

1. **Never commit .env files** ✅ Already in .gitignore
2. **Use strong SECRET_KEY** - 50+ characters
3. **Use HTTPS in production** - Enabled with SECURE_SSL_REDIRECT
4. **Rotate API keys regularly**
5. **Use separate credentials for dev/staging/production**
6. **Store secrets only in environment variables**
7. **Enable 2FA on all external services**

---

## Troubleshooting

### Email Not Sending
```bash
# Test email connection
python manage.py shell
from django.core.mail import send_mail
send_mail('Test', 'Test', 'from@example.com', ['to@example.com'])
```

### OAuth Not Working
- Verify redirect URLs match exactly
- Check Client ID and Secret are correct
- Ensure domain is in ALLOWED_HOSTS
- Check Sites in Django admin

### API Key Errors
- Verify API key is set in environment
- Check API key hasn't expired
- Verify correct host/endpoint
- Check rate limits

---

## Next Steps

1. Set up Brevo (or email service)
2. Create Google OAuth credentials
3. Create GitHub OAuth credentials
4. Get RapidAPI key
5. Deploy to Render and/or Railway
6. Add environment variables
7. Test all features

---

**Complete deployment happens in these order:**
1. ✅ Code uploaded to GitHub
2. ⏳ Configure email service
3. ⏳ Configure OAuth credentials
4. ⏳ Deploy to Render (or Railway)
5. ⏳ Add environment variables
6. ⏳ Run migrations
7. ⏳ Test all features
