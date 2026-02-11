# Railway Environment Variables Setup

## Quick Setup on Railway Dashboard

Go to: **Your Project → Variables**

### Required Variables

Copy-paste these exactly:

```
DEBUG=False
ALLOWED_HOSTS=*.up.railway.app
SECRET_KEY=django-insecure-change-this-to-random-string
DATABASE_URL=<Railway will auto-fill after adding PostgreSQL>
BREVO_API_KEY=<get-from-brevo-dashboard>
DEFAULT_FROM_EMAIL=noreply@yourdomain.com
```

## Step-by-Step

### 1. Generate Django Secret Key

Run this on your computer:
```bash
python -c "from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())"
```

Copy the output (long string).

### 2. Get Brevo API Key

1. Go to https://www.brevo.com
2. Log in
3. Click **Settings → SMTP & API**
4. Copy **API v3 Key**

### 3. Set Variables on Railway

1. Go to your Railway project
2. Click **Variables** tab
3. Add each variable:
   - Key: `DEBUG` → Value: `False`
   - Key: `ALLOWED_HOSTS` → Value: `*.up.railway.app`
   - Key: `SECRET_KEY` → Value: `<paste-generated-key>`
   - Key: `BREVO_API_KEY` → Value: `<paste-brevo-key>`
   - Key: `DEFAULT_FROM_EMAIL` → Value: `noreply@yourdomain.com`

4. Click **Add Service → PostgreSQL**
   - Railway auto-fills `DATABASE_URL` ✓

### 4. Redeploy

Click **Redeploy** button

Should succeed in 2-3 minutes with no PORT errors.

## Verify

After deployment:

1. Visit your Railway app URL (look in Railway dashboard)
2. Should see login page
3. Try OTP email
4. Check logs for errors

## If Still Getting PORT Error

This means the container is starting but can't bind to port. Try:

1. **Delete the project completely** in Railway
2. **Reconnect** the repo
3. **Fresh deploy**

Or try **simple Procfile** instead of Docker:

Create `Procfile`:
```
web: cd auth_project && python manage.py migrate && gunicorn auth_project.wsgi:application --workers 3
```

Delete `Dockerfile` and `start.sh`.

Railway will auto-detect Procfile and use simpler deployment.

## If Procfile Doesn't Work

Go back to Dockerfile but simpler version - remove start.sh entirely:

`Dockerfile`:
```dockerfile
FROM python:3.11-slim

WORKDIR /app
COPY . .

RUN apt-get update && apt-get install -y libpq-dev gcc && rm -rf /var/lib/apt/lists/*
RUN pip install --no-cache-dir -r auth_project/requirements.txt

EXPOSE 8000
CMD ["sh", "-c", "cd auth_project && python manage.py migrate && gunicorn auth_project.wsgi:application --workers 3 --bind 0.0.0.0:8000"]
```

---

Try the **Procfile approach first** - it's simpler and less likely to have environment variable issues.
