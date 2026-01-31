# Email Not Sending - Complete Diagnosis & Solution

## The Problem
✉️ OTP emails for login/registration are not being sent

## Root Cause Identified
🔍 **No email service configured** - System is using **Console Backend** (emails print to terminal, not sent)

### Why Console Backend?
Settings.py (lines 234-254) checks for:
1. ❌ `BREVO_API_KEY` - Not set
2. ❌ `ZEPTO_MAIL_API_KEY` + `ZEPTO_MAIL_TOKEN` - Not set
3. ❌ `EMAIL_HOST_USER` + `EMAIL_HOST_PASSWORD` - Not set
4. ✅ **Falls back to Console Backend** (default)

When Console Backend active:
```python
EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'
```

**Result**: 
- OTP code appears in Django console
- Email NOT sent to actual email address
- User receives nothing in inbox

---

## The Solution

### Choose Email Service (1 of 3)

#### 🟦 **OPTION A: Gmail SMTP (Easiest)**

**Pros**: Free, instant, no signup needed
**Time**: 5 minutes

**Steps**:
1. Create `.env` file (see below)
2. Enable Gmail 2-Step Verification
3. Generate App Password
4. Add to .env
5. Restart server

**Result**:
```
[SUCCESS] EMAIL BACKEND: Using Gmail SMTP
```

---

#### 🟦 **OPTION B: Brevo (Recommended)**

**Pros**: Professional, reliable, free tier (300/day)
**Time**: 5 minutes

**Steps**:
1. Sign up: https://www.brevo.com/
2. Get API Key from Settings → SMTP & API
3. Add to .env: `BREVO_API_KEY=...`
4. Restart server

**Result**:
```
[SUCCESS] EMAIL BACKEND: Using Brevo for OTP and transactional emails
```

---

#### 🟦 **OPTION C: ZeptoMail (Alternative)**

**Pros**: Good alternative to Brevo
**Time**: 5 minutes

**Steps**:
1. Sign up: https://www.zeptomail.com/
2. Get API Key and Mail Token
3. Add to .env
4. Restart server

**Result**:
```
[SUCCESS] EMAIL BACKEND: Using ZeptoMail for OTP and transactional emails
```

---

## Implementation Steps

### Step 1: Create `.env` File

**Location**: `e:\login\.env`

**For Gmail**:
```bash
EMAIL_HOST_USER=your-email@gmail.com
EMAIL_HOST_PASSWORD=your-app-password
DEFAULT_FROM_EMAIL=your-email@gmail.com
```

**For Brevo**:
```bash
BREVO_API_KEY=your-api-key-here
DEFAULT_FROM_EMAIL=noreply@unisync.app
```

**For ZeptoMail**:
```bash
ZEPTO_MAIL_API_KEY=your-api-key
ZEPTO_MAIL_TOKEN=your-mail-token
DEFAULT_FROM_EMAIL=noreply@unisync.app
```

### Step 2: Get Credentials

#### Gmail App Password
1. Go to: https://myaccount.google.com/security
2. Enable "2-Step Verification"
3. Click "App passwords"
4. Select: Mail → Windows Computer
5. Copy 16-character password
6. Paste as `EMAIL_HOST_PASSWORD`

#### Brevo API Key
1. Go to: https://www.brevo.com/
2. Sign up (free)
3. Dashboard → Settings → SMTP & API
4. Copy API Key
5. Paste as `BREVO_API_KEY`

#### ZeptoMail Credentials
1. Go to: https://www.zeptomail.com/
2. Sign up (free)
3. Dashboard → Settings
4. Copy API Key and Mail Token
5. Paste both

### Step 3: Restart Django

```bash
# Stop server: Ctrl+C
# Start server: python manage.py runserver
```

### Step 4: Verify Setup

Check console output for:
```
✅ [SUCCESS] EMAIL BACKEND: Using Gmail SMTP
✅ [SUCCESS] EMAIL BACKEND: Using Brevo...
✅ [SUCCESS] EMAIL BACKEND: Using ZeptoMail...
```

NOT:
```
❌ [WARNING] EMAIL BACKEND: Using console backend
```

---

## Test Email Sending

### Method 1: Django Shell
```bash
python manage.py shell
>>> from django.core.mail import send_mail
>>> result = send_mail(
...     'Test Email',
...     'This is a test',
...     'noreply@unisync.app',
...     ['your-email@gmail.com']
... )
>>> print(result)  # Should print: 1
1
>>> exit()
```

### Method 2: OTP Email
1. Go to: http://localhost:8000/login/
2. Enter username/email
3. Click "Login"
4. Check inbox (or spam) for OTP email
5. Email should arrive within 10 seconds

---

## Code Changes Made

### 1. **Brevo Backend Created**
**File**: `accounts/brevo_mail_backend.py`
- ✅ Created (complete implementation)
- Ready for production use
- Includes error handling

### 2. **Login View Enhanced**
**File**: `accounts/views.py` (lines 313-384)
- ✅ Already updated with email auth support
- Already has OTP email sending
- send_otp_email() function at lines 139-199

### 3. **Email Configuration**
**File**: `settings.py` (lines 214-270)
- ✅ Already configured with email backend selection
- Checks for credentials in order
- Falls back to console if none set

---

## What Happens When Email Works

### Login Flow with Email
```
User enters credentials
        ↓
Form validated
        ↓
User authenticated
        ↓
OTP generated
        ↓
send_otp_email() called
        ↓
✅ Email sent via configured backend
        ↓
User receives email with OTP code
        ↓
User enters OTP to complete login
```

### Console Flow (Current - Not Working)
```
User enters credentials
        ↓
Form validated
        ↓
User authenticated
        ↓
OTP generated
        ↓
send_otp_email() called
        ↓
⚠️ Email printed to console (NOT SENT)
        ↓
❌ User receives nothing in inbox
        ↓
User cannot complete login
```

---

## Troubleshooting

### Problem: Still Using Console Backend
**Solution**: 
- Verify .env file is in `e:\login\` (project root)
- Verify credentials are exact (no extra spaces)
- Restart server after creating .env
- Check Django startup output

### Problem: Gmail Not Sending
**Solutions**:
1. Verify 2-Step Verification is enabled
2. Use App Password (not regular password)
3. Check app password is 16 characters
4. Verify email is lowercase

### Problem: Brevo/ZeptoMail Not Sending
**Solutions**:
1. Copy API key exactly (including dashes)
2. Verify API key hasn't expired
3. Check API key is in correct .env variable
4. Verify sender email is verified in service

### Problem: "OTP email sent" but not received
**Check**:
1. Spam/junk folder
2. Email service rate limiting (restart server)
3. Check logs in `logs/django.log`
4. Verify recipient email is correct

---

## File Structure After Setup

```
e:/login/
├── .env                           ← CREATE THIS
├── manage.py
├── auth_project/
│   ├── auth_project/
│   │   └── settings.py           (already configured)
│   ├── accounts/
│   │   ├── brevo_mail_backend.py ✅ CREATED
│   │   ├── zepto_mail_backend.py ✅ EXISTS
│   │   ├── views.py              ✅ HAS send_otp_email()
│   │   └── ...
│   └── ...
└── ...
```

---

## Security Notes

✅ **Safe**:
- Email credentials in .env (not committed)
- API keys not exposed in code
- Password hashing still used
- Session-based auth maintained

⚠️ **Important**:
- Never commit .env to git
- Add `.env` to `.gitignore`
- Use environment variables in production
- Keep API keys secret

---

## Production Deployment

For production:
1. **Use Brevo** (most reliable)
2. Set `BREVO_API_KEY` via platform settings
3. Use verified sender email
4. Enable logging
5. Monitor email delivery

---

## Quick Decision Table

| Scenario | Solution | Time |
|----------|----------|------|
| Testing locally | Gmail SMTP | 5 min |
| Small production | Brevo free tier | 5 min |
| High volume | Brevo paid | 10 min |
| Already have Zoho | ZeptoMail | 5 min |

---

## Support Resources

| Topic | Resource |
|-------|----------|
| Gmail App Passwords | https://support.google.com/accounts/answer/185833 |
| Brevo Documentation | https://developers.brevo.com/ |
| ZeptoMail Documentation | https://www.zeptomail.com/developers/ |
| Django Email Backends | https://docs.djangoproject.com/en/stable/topics/email/ |

---

## Summary Checklist

- [ ] Choose email service (Gmail recommended)
- [ ] Create `.env` file in `e:\login\`
- [ ] Get credentials from service
- [ ] Add to .env file
- [ ] Restart Django server
- [ ] Verify startup output shows correct backend
- [ ] Test email sending via shell
- [ ] Test OTP email via login page
- [ ] Add .env to .gitignore
- [ ] Document setup for team

---

## Next Steps

1. **Choose email service** (Gmail recommended for quickest setup)
2. **Create .env file** with your credentials
3. **Restart Django server**
4. **Check console** for success message
5. **Test email** via login or shell
6. **Verify in inbox** (check spam folder)

Your emails should be sending within 5 minutes!
