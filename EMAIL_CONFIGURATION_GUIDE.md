# Email Configuration for OTP - Quick Setup Guide

## Overview

For OTP login to work, you need ONE of these email services configured:

1. **Brevo** (Recommended - Free tier available)
2. **ZeptoMail**
3. **Gmail SMTP**
4. **Console** (Development - prints to terminal)

---

## Option 1: Brevo (RECOMMENDED ⭐)

### Why Brevo?
✅ Free tier: 300 emails/day
✅ Easy setup
✅ Reliable for transactional emails
✅ Good documentation

### Setup:

**Step 1: Create Brevo Account**
1. Go to: https://www.brevo.com/
2. Sign up (free)
3. Verify email

**Step 2: Get API Key**
1. Log in to Brevo
2. Go to: Settings → API
3. Generate API key
4. Copy the key

**Step 3: Add to .env**
```
BREVO_API_KEY=your-copied-api-key-here
```

**Step 4: Test**
```bash
python manage.py shell
```

Then:
```python
from django.conf import settings
print(settings.EMAIL_BACKEND)
# Should show: accounts.brevo_mail_backend.BrevoMailBackend

# Test sending
from django.core.mail import send_mail
send_mail(
    'Test Email',
    'Testing Brevo email',
    settings.DEFAULT_FROM_EMAIL,
    ['youremail@gmail.com']
)
print("Email sent!")
exit()
```

**Step 5: Check Email**
- Wait 30 seconds
- Check your inbox (or spam folder)
- Should receive test email

✅ **Done! Brevo is configured**

---

## Option 2: ZeptoMail

### Setup:

**Step 1: Create ZeptoMail Account**
1. Go to: https://www.zeptomail.com/
2. Sign up
3. Create workspace

**Step 2: Get Credentials**
1. Go to: Settings
2. Copy API Key
3. Copy Token

**Step 3: Add to .env**
```
ZEPTO_MAIL_API_KEY=your-api-key
ZEPTO_MAIL_TOKEN=your-token
```

**Step 4: Test**
```bash
python manage.py shell
```

```python
from django.conf import settings
print(settings.EMAIL_BACKEND)
# Should show: accounts.zepto_mail_backend.ZeptoMailBackend

# Test
from django.core.mail import send_mail
send_mail('Test', 'Test message', settings.DEFAULT_FROM_EMAIL, ['test@gmail.com'])
print("Email sent!")
exit()
```

---

## Option 3: Gmail SMTP

### Setup:

**Step 1: Enable 2-Factor Authentication**
1. Go to: https://myaccount.google.com/
2. Security → 2-Step Verification
3. Enable if not already enabled

**Step 2: Create App Password**
1. Go to: https://myaccount.google.com/apppasswords
2. Select: Mail and Windows
3. Google will generate 16-character password
4. Copy this password

**Step 3: Add to .env**
```
EMAIL_HOST_USER=your-email@gmail.com
EMAIL_HOST_PASSWORD=your-16-char-app-password
```

⚠️ **Important:** Use the app password, NOT your regular Gmail password

**Step 4: Test**
```bash
python manage.py shell
```

```python
from django.conf import settings
print(settings.EMAIL_BACKEND)
# Should show: django.core.mail.backends.smtp.EmailBackend

# Test
from django.core.mail import send_mail
send_mail('Test', 'Test message', settings.DEFAULT_FROM_EMAIL, ['test@gmail.com'])
print("Email sent!")
exit()
```

---

## Option 4: Console (Development Only)

No setup needed! Emails print to Django console.

**Check OTP code in terminal:**
```
When user tries to login, you'll see something like:
[Email] OTP email sent to test@example.com
Content-Type: text/plain; charset="utf-8"
Subject: 🚀 - Your login OTP Code
...
Your OTP for login is: 123456
```

---

## Verify Email is Working

### Test 1: Check Settings

```bash
python manage.py shell
```

```python
from django.conf import settings

# Check which backend is active
print(f"EMAIL_BACKEND: {settings.EMAIL_BACKEND}")

# Check sender
print(f"DEFAULT_FROM_EMAIL: {settings.DEFAULT_FROM_EMAIL}")

# Check host (if using SMTP)
print(f"EMAIL_HOST: {settings.EMAIL_HOST}")
print(f"EMAIL_PORT: {settings.EMAIL_PORT}")
exit()
```

### Test 2: Send Test Email

```bash
python manage.py shell
```

```python
from django.core.mail import send_mail
from django.conf import settings

result = send_mail(
    subject='Test Email',
    message='This is a test email from UniSync',
    from_email=settings.DEFAULT_FROM_EMAIL,
    recipient_list=['your-real-email@gmail.com'],
    fail_silently=False
)

print(f"Email sent: {result}")  # Should print: Email sent: 1
exit()
```

### Test 3: Check Email Inbox

- Wait 30 seconds
- Check inbox
- Check spam/junk folder
- Verify you received the test email

---

## Complete Test Flow

Once email is configured:

**1. Open login page:**
```
http://127.0.0.1:8000/accounts/login/
```

**2. Enter test credentials:**
- Username: testuser
- Password: TestPassword123

**3. You should see:**
```
✅ "OTP sent to test@example.com. Please verify to complete login."
✅ Redirected to OTP page
```

**4. Check email for OTP:**
- Subject: "🚀 - Your login OTP Code"
- Look for 6-digit number

**5. Enter OTP and verify:**
- Page should redirect to dashboard
- User is logged in!

---

## Troubleshooting

### Error: "Failed to send OTP email"

**Check 1: Is backend configured?**
```bash
python manage.py shell
from django.conf import settings
print(settings.EMAIL_BACKEND)
```

Should show one of:
- accounts.brevo_mail_backend.BrevoMailBackend
- accounts.zepto_mail_backend.ZeptoMailBackend
- django.core.mail.backends.smtp.EmailBackend
- django.core.mail.backends.console.EmailBackend

**Check 2: Are .env values correct?**
```bash
cat .env | grep -E "BREVO|ZEPTO|EMAIL"
```

Verify keys/passwords are exactly as provided

**Check 3: Test email directly**
```bash
python manage.py shell
from django.core.mail import send_mail
send_mail('Test', 'Test', 'noreply@example.com', ['test@gmail.com'])
```

If this fails, email service is not working

### Error: "Invalid API Key"

**For Brevo:**
- Copy API key again
- Make sure no spaces before/after
- Verify it's not revoked in Brevo dashboard

**For ZeptoMail:**
- Check both API_KEY and TOKEN are set
- Verify tokens haven't expired

### Error: "Invalid Credentials" (Gmail)

- Make sure you're using **App Password**, not Gmail password
- App password is 16 characters
- Gmail account must have 2FA enabled

### Email arrives in spam folder

Add to email provider's allow list:
- Gmail: Mark as "Not Spam"
- Outlook: Add sender to contacts
- Other: Add to safe senders list

---

## Email Content

Users will receive emails like this:

### Subject
```
🚀 - Your login OTP Code
```

### Plain Text Version
```
Hi there!

Your OTP for login is: 123456

This OTP is valid for 5 minutes only.

If you didn't request this, please ignore this email.

Best regards,
🚀 Team
```

### HTML Version
```
[Formatted with colors and styling]
- Large OTP display (32px font)
- Expiry warning
- Professional branding
- Footer with timestamp
```

---

## Best Practices

✅ **Do:**
- Use Brevo or similar service for production
- Keep API keys in .env (not in code)
- Test email sending before deploying
- Monitor email delivery
- Set up bounce/complaint handling

❌ **Don't:**
- Use Gmail for high-volume emails (gets blocked)
- Commit .env to git
- Share API keys publicly
- Use same email for multiple purposes
- Ignore email delivery failures

---

## Production Deployment

When deploying to production:

**Step 1: Update .env on server**
```
BREVO_API_KEY=production-api-key
```

**Step 2: Verify email settings**
```bash
python manage.py check
```

**Step 3: Test email**
```bash
python manage.py shell
# Run email test
```

**Step 4: Monitor**
- Check email delivery logs
- Monitor bounce rates
- Set up alerts for failures

---

## Environment Variables Reference

```bash
# For Brevo
BREVO_API_KEY=your-brevo-api-key

# For ZeptoMail
ZEPTO_MAIL_API_KEY=your-api-key
ZEPTO_MAIL_TOKEN=your-token

# For Gmail SMTP
EMAIL_HOST_USER=your-email@gmail.com
EMAIL_HOST_PASSWORD=your-16-char-app-password

# Optional
DEFAULT_FROM_EMAIL=noreply@yourdomain.com
```

---

## Summary

| Service | Setup Time | Cost | Reliability |
|---------|-----------|------|-------------|
| Brevo | 5 min | Free (300/day) | ⭐⭐⭐⭐⭐ |
| ZeptoMail | 10 min | Free tier | ⭐⭐⭐⭐ |
| Gmail | 10 min | Free | ⭐⭐⭐ |
| Console | 0 min | Free | ⭐ (Dev only) |

**Recommended:** Use Brevo for the best balance of simplicity and reliability.

---

## Next Steps

1. Choose ONE email service above
2. Follow its setup guide
3. Test email sending
4. Test OTP login flow
5. Verify OTP emails arrive
6. Done! ✅

Status: Ready to configure email
