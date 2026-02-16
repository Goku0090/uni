# Frontend/Backend Separation - Quick Start

## What You'll Get

```
Before:
  e:/login/auth_project/
    ├── auth_project/  (Django settings)
    ├── accounts/      (Django app)
    ├── manage.py
    └── Procfile

After:
  e:/login/
    ├── backend/       (Django API)
    │   ├── auth_project/
    │   ├── accounts/
    │   ├── manage.py
    │   └── Procfile
    ├── frontend/      (React app)
    │   ├── src/
    │   └── package.json
    └── docker-compose.yml
```

## Benefits

✅ **Independent Deployment** - Update frontend without redeploying backend  
✅ **Better Scalability** - Scale frontend and backend separately  
✅ **Technology Flexibility** - Can replace React with Vue/Angular anytime  
✅ **Team Separation** - Frontend and backend teams work independently  
✅ **Separate CI/CD** - Different deployment pipelines  
✅ **CDN Support** - Serve frontend from CDN  

## Quickest Path (30 minutes)

### Step 1: Reorganize Folders (5 min)

```bash
# Windows PowerShell
cd e:/login/

mkdir backend
mkdir frontend

# Move Django files
Move-Item "auth_project" "backend/auth_project" -Force
Move-Item "accounts" "backend/accounts" -Force
Move-Item "manage.py" "backend/manage.py" -Force
Move-Item "requirements.txt" "backend/requirements.txt" -Force
Move-Item "Procfile" "backend/Procfile" -Force
Move-Item ".env" "backend/.env" -Force
```

### Step 2: Create Frontend (10 min)

Create minimal React app:

```bash
cd e:/login/frontend
npm create vite@latest . -- --template react
npm install axios
```

### Step 3: Update Backend for CORS (5 min)

In `backend/auth_project/settings.py`, add:

```python
# After INSTALLED_APPS
INSTALLED_APPS = [
    ...
    'corsheaders',
]

# Add to MIDDLEWARE (first)
MIDDLEWARE = [
    'corsheaders.middleware.CorsMiddleware',
    'django.middleware.security.SecurityMiddleware',
    ...
]

# Add at bottom
CORS_ALLOWED_ORIGINS = [
    'http://localhost:3000',
]

CORS_ALLOW_CREDENTIALS = True
```

Also add to requirements:
```
django-cors-headers==4.3.1
```

### Step 4: Create docker-compose.yml (5 min)

Save this as `e:/login/docker-compose.yml`:

```yaml
version: '3.9'

services:
  backend:
    build:
      context: ./backend
      dockerfile: docker/Dockerfile.backend
    ports:
      - "8000:8000"
    environment:
      - DEBUG=False
      - CORS_ALLOWED_ORIGINS=http://localhost:3000
    volumes:
      - ./backend:/app
    networks:
      - unisync

  frontend:
    build:
      context: ./frontend
    ports:
      - "3000:80"
    networks:
      - unisync

  redis:
    image: redis:7-alpine
    ports:
      - "6379:6379"
    networks:
      - unisync

networks:
  unisync:
```

### Step 5: Create Dockerfiles (5 min)

**backend/docker/Dockerfile.backend:**
```dockerfile
FROM python:3.11-slim
WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY . .
CMD ["gunicorn", "auth_project.wsgi", "--bind", "0.0.0.0:8000"]
```

**frontend/Dockerfile:**
```dockerfile
FROM node:18-alpine as build
WORKDIR /app
COPY package*.json ./
RUN npm install
COPY . .
RUN npm run build

FROM nginx:alpine
COPY --from=build /app/dist /usr/share/nginx/html
EXPOSE 80
CMD ["nginx", "-g", "daemon off;"]
```

### Step 6: Test Locally (No Docker)

**Terminal 1 - Backend:**
```bash
cd backend
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
python manage.py runserver
```

**Terminal 2 - Frontend:**
```bash
cd frontend
npm install
npm run dev
```

Access:
- Frontend: http://localhost:5173 (Vite default)
- Backend: http://localhost:8000
- Admin: http://localhost:8000/admin

### Step 7: Test with Docker

```bash
docker-compose up
```

Access:
- Frontend: http://localhost:3000
- Backend: http://localhost:8000

---

## File Structure After Migration

```
e:/login/
├── backend/
│   ├── auth_project/
│   │   ├── settings.py      ← Add CORS config
│   │   ├── urls.py
│   │   ├── wsgi.py
│   │   └── asgi.py
│   ├── accounts/
│   │   ├── models.py
│   │   ├── views.py
│   │   ├── serializers.py
│   │   └── urls.py
│   ├── docker/
│   │   └── Dockerfile.backend
│   ├── manage.py
│   ├── requirements.txt
│   ├── .env
│   └── Procfile
│
├── frontend/
│   ├── src/
│   │   ├── main.jsx
│   │   ├── App.jsx
│   │   └── api/
│   │       └── client.js    ← API calls here
│   ├── index.html
│   ├── vite.config.js
│   ├── package.json
│   ├── .env.local
│   ├── Dockerfile
│   └── nginx.conf
│
├── docker-compose.yml       ← New
├── .gitignore
└── README.md
```

---

## Environment Variables

**backend/.env:**
```env
DEBUG=False
SECRET_KEY=your-secret-key
ALLOWED_HOSTS=localhost,127.0.0.1,*.railway.app
DATABASE_URL=postgresql://...
REDIS_URL=redis://redis:6379/0
CORS_ALLOWED_ORIGINS=http://localhost:3000,https://your-frontend.vercel.app
```

**frontend/.env.local:**
```env
VITE_API_URL=http://localhost:8000/api
```

---

## Frontend API Client Example

**frontend/src/api/client.js:**
```javascript
import axios from 'axios'

const API_URL = import.meta.env.VITE_API_URL || 'http://localhost:8000/api'

const client = axios.create({
  baseURL: API_URL,
  withCredentials: true,
})

export const getProjects = () => client.get('/projects/')
export const getProfile = () => client.get('/profile/')
export const loginUser = (email, password) => client.post('/login/', { email, password })

export default client
```

**frontend/src/App.jsx:**
```javascript
import { useState, useEffect } from 'react'
import { getProjects } from './api/client'

function App() {
  const [projects, setProjects] = useState([])

  useEffect(() => {
    getProjects().then(res => setProjects(res.data))
  }, [])

  return (
    <div>
      <h1>Projects</h1>
      {projects.map(p => <div key={p.id}>{p.title}</div>)}
    </div>
  )
}

export default App
```

---

## Deployment

### Backend → Railway

1. Create Railway project
2. Connect to `backend/` folder (not root)
3. Set `PORT` variable → let Railway assign it
4. Set other env vars
5. Deploy

### Frontend → Vercel

1. Create Vercel project
2. Connect to `frontend/` folder
3. Set `VITE_API_URL=https://your-railway-url/api`
4. Deploy

### Both Together → Docker

```bash
docker-compose up -d
```

---

## Common Issues & Fixes

### CORS Error
**Error:** `Access to XMLHttpRequest blocked by CORS policy`

**Fix:** Add to `backend/auth_project/settings.py`:
```python
CORS_ALLOWED_ORIGINS = ['https://your-frontend-domain.com']
```

### API Not Found
**Error:** `404 Not Found`

**Fix:** Frontend calling wrong API URL. Check:
```javascript
// Must be /api/projects/ not /projects/
fetch('http://localhost:8000/api/projects/')
```

### CSRF Token Missing
**Error:** `CSRF token missing or incorrect`

**Fix:** Backend needs `withCredentials: true`:
```javascript
const client = axios.create({
  withCredentials: true,  // ← Add this
})
```

---

## Helpful Commands

```bash
# Docker
docker-compose up           # Start everything
docker-compose logs -f      # View logs
docker-compose down         # Stop everything

# Backend
cd backend
python manage.py migrate    # Run migrations
python manage.py createsuperuser  # Create admin

# Frontend
cd frontend
npm install                 # Install dependencies
npm run dev                 # Development server
npm run build               # Production build
```

---

## Summary

✅ **5 minutes**: Move files to backend/frontend folders  
✅ **10 minutes**: Create basic React app  
✅ **5 minutes**: Add CORS to Django  
✅ **10 minutes**: Create Docker files  
✅ **Done**: Now you have separated architecture!

Next step: Deploy backend to Railway, frontend to Vercel.

See **FRONTEND_BACKEND_SEPARATION_GUIDE.md** for detailed instructions.
