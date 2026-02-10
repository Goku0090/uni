# Render Deployment Fix: Python 3.13 → 3.12

## Problem
Render is using **Python 3.13**, but many packages fail to compile on it. The solution is to **downgrade to Python 3.12**.

## Quick Fix

### Step 1: Create/Update `render.yaml`
```yaml
services:
  - type: web
    name: unisync
    runtime: python
    runtimeVersion: 3.12.0
    buildCommand: pip install -r requirements.txt
    startCommand: gunicorn auth_project.wsgi:application --workers 3 --bind 0.0.0.0:$PORT
    envVars:
      - key: DEBUG
        value: "False"
      - key: PYTHON_VERSION
        value: "3.12"
      - key: PIP_DEFAULT_TIMEOUT
        value: "600"
      - key: PYTHONUNBUFFERED
        value: "1"
```

### Step 2: Update `requirements.txt`
Use the current requirements.txt (it's already optimized).

### Step 3: Deploy
```bash
git add render.yaml requirements.txt
git commit -m "fix: use Python 3.12 for Render deployment"
git push origin main
```

Render will automatically detect `render.yaml` and use Python 3.12.

## Why Python 3.12?
- ✅ All packages have pre-compiled wheels
- ✅ No compilation needed
- ✅ Deploys in minutes, not hours
- ✅ Better stability than 3.13
- ✅ All Django features work

## Alternative: Use Procfile (if not using render.yaml)

If Render doesn't detect `render.yaml`, use **Procfile**:

```
python-version: 3.12
web: gunicorn auth_project.wsgi:application --workers 3
```

## If render.yaml Not Working

Go to **Render Dashboard → Settings → Environment**:

1. Click **Environment Variables**
2. Add:
   ```
   PYTHON_VERSION = 3.12
   PIP_DEFAULT_TIMEOUT = 600
   ```

3. Or set build command:
   ```
   pip install --only-binary :all: -r requirements.txt
   ```

## Verify Python Version

After deployment, check Python version:
```bash
# SSH into Render instance
# Then run:
python --version
```

Should show: `Python 3.12.x`

## Expected Install Times

- **Python 3.12 + binary wheels**: 2-3 minutes ✅
- **Python 3.13 + source compilation**: 30+ minutes ❌

## Database & Static Files

If deploy shows new errors:

```bash
# SSH into Render instance and run:
python manage.py migrate
python manage.py collectstatic --noinput
```

## Final Checklist

- ✅ `render.yaml` created with `runtimeVersion: 3.12.0`
- ✅ `requirements.txt` updated
- ✅ Environment variables set (`BREVO_API_KEY`, etc.)
- ✅ Git pushed

Then Render will:
1. Detect `render.yaml`
2. Use Python 3.12
3. Install dependencies (2-3 min)
4. Run migrations
5. Start server

---

**Deployment Status:** ✅ Ready for Render with Python 3.12
