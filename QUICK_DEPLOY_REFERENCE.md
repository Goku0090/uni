# Quick Deploy Reference Card

## Deploy in 18 Minutes ⚡

### Essential Info
- **Platform**: Render.com (free tier)
- **Time**: ~18 minutes
- **Cost**: Free (with paid upgrade option)
- **Result**: Live app on `https://unisync.onrender.com`

---

## 7 Steps

### 1️⃣ Sign Up (2 min)
```
→ https://render.com
→ Click Sign Up
→ GitHub login
```

### 2️⃣ Create Service (3 min)
```
→ New → Web Service
→ Select: Goku0090/uni
→ Connect
```

### 3️⃣ Configure (2 min)
```
Name:     unisync
Runtime:  Python 3
Build:    bash build.sh
Start:    cd backend && gunicorn auth_project.wsgi:application --workers 3 --worker-class sync --bind 0.0.0.0:$PORT --timeout 120
```

### 4️⃣ Environment (2 min)
```
DEBUG=False
SECRET_KEY=(generate)
PYTHONUNBUFFERED=1
PYTHONDONTWRITEBYTECODE=1
EMAIL_BACKEND=django.core.mail.backends.console.EmailBackend
```

### 5️⃣ Database (1 min)
```
→ New → PostgreSQL
→ Name: unisync-db
→ Copy CONNECTION_STRING
```

### 6️⃣ Link (1 min)
```
→ Add DATABASE_URL
→ Set to CONNECTION_STRING
→ Add ALLOWED_HOSTS=localhost,127.0.0.1
```

### 7️⃣ Deploy! (10 min)
```
→ Create Web Service
→ Wait for build
→ Status: Live ✅
```

---

## Generate SECRET_KEY

```python
import secrets
print(secrets.token_urlsafe(50))
```
Copy output and paste in Render.

---

## After Deploy

1. Get URL: `https://unisync-xxxx.onrender.com`
2. Update ALLOWED_HOSTS with your domain
3. Create admin via Shell:
   ```bash
   cd backend
   python manage.py createsuperuser
   ```
4. Test: Visit your URL

---

## URLs After Deploy

| Resource | URL |
|----------|-----|
| App | `https://unisync-xxxx.onrender.com` |
| Admin | `https://unisync-xxxx.onrender.com/admin/` |
| Dashboard | `https://dashboard.render.com` |

---

## Quick Troubleshooting

| Problem | Solution |
|---------|----------|
| Build fails | Check logs → Check requirements.txt |
| 500 error | Add ALLOWED_HOSTS → Add SECRET_KEY |
| Won't start | Add DATABASE_URL → Migrate DB |
| Slow | Free tier is slow → Upgrade if needed |

---

## Docs

- **Quick Start**: `00_DEPLOYMENT_START_HERE.md`
- **Detailed**: `DEPLOYMENT_STEPS_FINAL_2026.md`
- **Checklist**: `DEPLOY_NOW_FINAL_CHECKLIST.md`

---

## Status

✅ Code ready  
✅ GitHub pushed  
✅ Config complete  

**→ Ready to deploy!**

---

**Start here**: https://render.com

**Time to live**: 18 minutes 🚀
