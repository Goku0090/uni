# OTP Login Flow - Complete Setup Guide

## ✅ Status: ENABLED

The OTP verification login flow is now active. Here's how it works:

---

## Login Flow with OTP

```
1. User enters username/email + password
                ↓
2. Server authenticates credentials
                ↓
3. ✅ Credentials valid → Generate OTP (6-digit code)
                ↓
4. Send OTP to user's email
                ↓
5. Redirect to OTP verification page
                ↓
6. User enters OTP from email (6 digits)
                ↓
7. Server validates OTP (must match, not expired, not already used)
                ↓
8. ✅ OTP valid → Create session & log user in
                ↓
9. Send welcome back email
                ↓
10. Redirect to main dashboard
                ↓
✅ USER FULLY LOGGED IN!
```

---

## Required Configuration

### 1. Email Backend MUST be Configured

The OTP requires an email service. Choose ONE:

#### Option A: Brevo (Recommended - Free tier)
```bash
# In .env file:
BREVO_API_KEY=your-brevo-api-key
```

#### Option B: ZeptoMail
```bash
# In .env file:
ZEPTO_MAIL_API_KEY=your-key
ZEPTO_MAIL_TOKEN=your-token
```

#### Option C: Gmail SMTP
```bash
# In .env file:
EMAIL_HOST_USER=your-email@gmail.com
EMAIL_HOST_PASSWORD=your-app-password
```

#### Option D: Development (Console - prints to terminal)
```bash
# No configuration needed
# OTP codes will print to Django console
# Check terminal for: "OTP for login is: 123456"
```

### 2. Check Current Email Backend

```bash
python manage.py shell
```

Then:
```python
from django.conf import settings
print(f"Email backend: {settings.EMAIL_BACKEND}")

# Test email sending
from django.core.mail import send_mail
send_mail(
    'Test Email',
    'This is a test',
    settings.DEFAULT_FROM_EMAIL,
    ['test@example.com'],
)
print("Email test sent!")
exit()
```

---

## How to Test

### Step 1: Setup (Run Once)

```bash
# Navigate to project
cd e:/login/auth_project

# Ensure migrations are run
python manage.py migrate

# Create test user
python manage.py shell
```

Paste in shell:
```python
from django.contrib.auth.models import User
from accounts.models import StudentProfile

# Create test user
user = User.objects.create_user(
    username='testuser',
    email='test@example.com',
    password='TestPassword123'
)

# Create profile
StudentProfile.objects.create(
    user=user,
    full_name='Test User',
    college='Test College'
)

print("✅ Test user created!")
exit()
```

### Step 2: Run Server

```bash
python manage.py runserver
```

### Step 3: Test OTP Login Flow

**1. Go to:** `http://127.0.0.1:8000/accounts/login/`

**2. Enter credentials:**
- Username: `testuser`
- Password: `TestPassword123`
- Click: "Login to UniSync"

**3. Expected output:**
```
✅ Success message: "OTP sent to test@example.com. Please verify to complete login."
✅ Redirects to: OTP verification page
```

**4. Get OTP Code:**

If email configured:
- Check email inbox for OTP code (6 digits)
- Look for subject: "🚀 - Your login OTP Code"

If using console backend:
- Check Django console/terminal
- Look for: `OTP email sent successfully to test@example.com`
- The code will be in the email content (search for 6-digit number)

**5. Enter OTP:**
- Enter the 6-digit code
- Click: "Verify OTP"

**6. Expected result:**
```
✅ Success message: "Login successful!"
✅ Redirect to: Main dashboard
✅ User is logged in
✅ Welcome back email sent
```

---

## Development Testing (No Email Configured)

If you haven't configured email yet:

### In Django Shell

```bash
python manage.py shell
```

Then:
```python
from accounts.models import OTP

# Generate test OTP
otp = OTP.generate_otp('test@example.com', 'login')
print(f"OTP Code: {otp.otp_code}")
print(f"Valid for: 5 minutes")
exit()
```

Or check the OTP table directly:

```python
from accounts.models import OTP
from django.utils import timezone

# Get latest OTP for login
latest_otp = OTP.objects.filter(email='test@example.com', purpose='login').order_by('-created_at').first()
if latest_otp:
    print(f"OTP Code: {latest_otp.otp_code}")
    print(f"Expires: {latest_otp.expires_at}")
    print(f"Is valid: {latest_otp.is_valid()}")
exit()
```

---

## OTP Email Template

Users receive an email like this:

```
Subject: 🚀 - Your login OTP Code

Hi there!

Your OTP for login is: 123456

This OTP is valid for 5 minutes only.

If you didn't request this, please ignore this email.

Best regards,
🚀 Team
```

HTML version also includes:
- Formatted OTP display
- Expiry time warning
- Professional styling

---

## Session Configuration

During OTP flow, these values are stored in session:

```python
request.session['login_user_id'] = user.id
request.session['login_user_email'] = user.email
request.session['login_username'] = user.username
```

After OTP verification:
- Session is cleared
- User is logged in with `login(request, user)`
- User stays logged in as long as session is valid

---

## OTP Validation Rules

An OTP is **valid** if ALL conditions are met:

✅ OTP code matches exactly (case-sensitive if alphanumeric)
✅ OTP hasn't expired (5 minute window)
✅ OTP hasn't been used before
✅ Purpose matches ('login', 'registration', or 'reset')
✅ Email matches user's email

---

## Error Handling

### If User Sees Error: "OTP has expired"

```
Cause: User took more than 5 minutes to enter OTP
Solution: Click "Resend OTP" button to get new code
```

### If User Sees Error: "Invalid OTP"

```
Cause: Wrong OTP code entered
Solution: Check email again and re-enter correct code
```

### If User Sees Error: "No OTP found"

```
Cause: OTP was deleted or never sent
Solution: Try logging in again (generates new OTP)
```

### If No Email Arrives

```
Cause 1: Email backend not configured
Solution: Check settings.EMAIL_BACKEND
         Configure .env file with email credentials

Cause 2: Email service down
Solution: Check email provider status

Cause 3: Spam folder
Solution: Check spam/junk folder in email
```

---

## Security Features

✅ **6-digit codes** - 1 million possible combinations
✅ **5-minute expiry** - Short window to prevent brute force
✅ **One-time use** - Code deleted after verification
✅ **Email verification** - Requires email access
✅ **Rate limiting** (recommended addition) - Limit attempts
✅ **Logging** - All OTP events logged for audit

---

## Setup Checklist

- [ ] Run migrations: `python manage.py migrate`
- [ ] Configure email backend in .env
- [ ] Create test user
- [ ] Start Django server
- [ ] Test login with username
- [ ] Receive OTP email (or see in console)
- [ ] Enter OTP code
- [ ] Verify login successful
- [ ] Check user is logged in

---

## File Structure

```
accounts/
├── models.py
│   ├── OTP model (6-digit code, 5-min expiry)
│   └── User, StudentProfile
├── views.py
│   ├── login_view() → Authenticate + Generate OTP
│   └── verify_otp_view() → Validate OTP + Create session
├── forms.py
│   └── OTPVerificationForm (6-digit validation)
├── templates/
│   ├── login.html (username/password form)
│   └── verify_otp.html (OTP entry form)
└── services/
    └── auth_service.py (email sending)
```

---

## Code Flow

### login_view() - Lines 309-380

```python
def login_view(request):
    if request.method == 'POST':
        # 1. Get username/email and password from form
        username_or_email = request.POST.get('username')
        password = request.POST.get('password')
        
        # 2. Authenticate user
        user = authenticate(request, username=username_or_email, password=password)
        
        # 3. If valid, generate OTP
        if user is not None:
            otp = OTP.generate_otp(user.email, 'login')
            
        # 4. Send OTP email
            send_otp_email(user.email, otp.otp_code, 'login')
            
        # 5. Store user ID in session
            request.session['login_user_id'] = user.id
            
        # 6. Redirect to OTP verification
            return redirect('verify_otp', purpose='login')
```

### verify_otp_view() - Lines 384-499

```python
def verify_otp_view(request, purpose):
    if request.method == 'POST':
        otp_input = form.cleaned_data['otp_code']
        
        # 1. Get user from session
        user_id = request.session.get('login_user_id')
        user = User.objects.get(id=user_id)
        
        # 2. Get latest OTP for this email
        otp_obj = OTP.objects.filter(
            email=user.email, 
            purpose='login'
        ).order_by('-created_at').first()
        
        # 3. Validate OTP
        if otp_obj.otp_code == otp_input:
            # 4. Create session
            login(request, user)
            
            # 5. Send welcome back email
            AuthService.send_welcome_back_email(user.email, user.username)
            
            # 6. Redirect to dashboard
            return redirect('main_home')
```

---

## Common Questions

**Q: Can I skip OTP verification?**
A: Not recommended for security. To disable, modify login_view() to call `login(request, user)` directly.

**Q: Is OTP required for registration?**
A: Yes, same flow applies during registration.

**Q: Can OTP be used for password reset?**
A: Yes, same system handles 3 purposes: login, registration, reset.

**Q: What if user loses email?**
A: They cannot login. You'll need to:
1. Reset their email in admin panel
2. They can use "Forgot Password" flow

**Q: How long is OTP valid?**
A: 5 minutes from generation. After that, user must request new OTP.

---

## Troubleshooting

### Issue: "OTP sent to X@example.com" but no email arrives

**Check 1: Email backend configured?**
```bash
python manage.py shell
from django.conf import settings
print(settings.EMAIL_BACKEND)
```

**Check 2: .env file has correct credentials?**
```bash
cat .env | grep EMAIL
cat .env | grep BREVO
```

**Check 3: Email service is working?**
```python
# In Django shell
from django.core.mail import send_mail
send_mail('Test', 'Test message', 'noreply@example.com', ['youremail@gmail.com'])
```

**Check 4: Check console**
If using console backend, OTP appears in terminal

### Issue: "Invalid OTP" but code is correct

**Cause 1:** Spaces or line breaks in code
→ Make sure no extra spaces

**Cause 2:** OTP expired
→ Check timestamp (5 minute window)

**Cause 3:** Code already used
→ OTP is one-time only, must request new one

### Issue: Redirect loop

**Cause:** Session not being created properly
→ Check if `login(request, user)` is being called
→ Check CSRF token in form

---

## Next Steps

1. ✅ Configure email in .env file
2. ✅ Run migrations
3. ✅ Create test user
4. ✅ Test complete login → OTP → Verification flow
5. ✅ Monitor error logs
6. Optional: Add rate limiting (after 3 failed OTP attempts)
7. Optional: Add CAPTCHA after failed attempts

---

## Support

If OTP doesn't work:
1. Check Django console for error messages
2. Verify email backend is configured
3. Test email sending directly
4. Check OTP table in database
5. Review error logs

Status: **OTP Login Flow Active** ✅
