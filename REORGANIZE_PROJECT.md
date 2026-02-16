# Quick Migration: Reorganize into Frontend/Backend

## Current Structure vs New Structure

### Current (Monolithic)
```
e:/login/auth_project/
├── auth_project/
├── accounts/
├── manage.py
├── requirements.txt
└── Procfile
```

### New (Separated)
```
e:/login/
├── backend/
│   ├── auth_project/
│   ├── accounts/
│   ├── manage.py
│   ├── requirements.txt
│   ├── Procfile
│   └── docker/
│       └── Dockerfile.backend
├── frontend/
│   ├── src/
│   ├── package.json
│   └── Dockerfile
└── docker-compose.yml
```

---

## Migration Steps (Windows PowerShell)

### 1. Create Backend Folder

```powershell
# From e:/login/
cd e:/login/
mkdir backend
mkdir frontend
```

### 2. Move Django Files to Backend

```powershell
# Move Django project directory
Move-Item "e:/login/auth_project" "e:/login/backend/auth_project" -Force
Move-Item "e:/login/accounts" "e:/login/backend/accounts" -Force

# Move manage.py
Move-Item "e:/login/manage.py" "e:/login/backend/manage.py" -Force

# Move requirements
Move-Item "e:/login/requirements.txt" "e:/login/backend/requirements.txt" -Force
Move-Item "e:/login/requirements-*.txt" "e:/login/backend/" -Force

# Move configuration files
Move-Item "e:/login/.env" "e:/login/backend/.env" -Force
Move-Item "e:/login/Procfile" "e:/login/backend/Procfile" -Force

# Move migrations
Move-Item "e:/login/migrations" "e:/login/backend/migrations" -Force -ErrorAction SilentlyContinue

# Move media and static
Move-Item "e:/login/media" "e:/login/backend/media" -Force -ErrorAction SilentlyContinue
Move-Item "e:/login/static" "e:/login/backend/static" -Force -ErrorAction SilentlyContinue
Move-Item "e:/login/staticfiles" "e:/login/backend/staticfiles" -Force -ErrorAction SilentlyContinue

# Move database
Move-Item "e:/login/db.sqlite3" "e:/login/backend/db.sqlite3" -Force -ErrorAction SilentlyContinue
```

### 3. Create Backend Dockerfile

Create file: `e:/login/backend/docker/Dockerfile.backend`

```dockerfile
FROM python:3.11-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

RUN python manage.py collectstatic --noinput

CMD ["gunicorn", "auth_project.wsgi", "--bind", "0.0.0.0:8000", "--workers", "4"]
```

### 4. Create Frontend Structure (React with Vite)

```powershell
cd e:/login/frontend

# Create basic structure
mkdir src
mkdir public
mkdir src/components
mkdir src/pages
mkdir src/api

# Create package.json
```

Create file: `e:/login/frontend/package.json`

```json
{
  "name": "unisync-frontend",
  "version": "1.0.0",
  "type": "module",
  "scripts": {
    "dev": "vite",
    "build": "vite build",
    "preview": "vite preview"
  },
  "dependencies": {
    "react": "^18.2.0",
    "react-dom": "^18.2.0",
    "axios": "^1.6.0",
    "react-router-dom": "^6.20.0"
  },
  "devDependencies": {
    "@vitejs/plugin-react": "^4.2.0",
    "vite": "^5.0.0"
  }
}
```

### 5. Create Frontend Files

**e:/login/frontend/src/main.jsx**
```javascript
import React from 'react'
import ReactDOM from 'react-dom/client'
import App from './App.jsx'

ReactDOM.createRoot(document.getElementById('root')).render(
  <React.StrictMode>
    <App />
  </React.StrictMode>,
)
```

**e:/login/frontend/src/App.jsx**
```javascript
import { useState, useEffect } from 'react'
import client from './api/client'
import './App.css'

function App() {
  const [projects, setProjects] = useState([])
  const [loading, setLoading] = useState(true)

  useEffect(() => {
    fetchProjects()
  }, [])

  const fetchProjects = async () => {
    try {
      const response = await client.get('/projects/')
      setProjects(response.data)
    } catch (error) {
      console.error('Error fetching projects:', error)
    } finally {
      setLoading(false)
    }
  }

  return (
    <div className="App">
      <h1>UniSync Projects</h1>
      {loading ? (
        <p>Loading...</p>
      ) : (
        <div className="projects">
          {projects.map(project => (
            <div key={project.id} className="project-card">
              <h2>{project.title}</h2>
              <p>{project.description}</p>
            </div>
          ))}
        </div>
      )}
    </div>
  )
}

export default App
```

**e:/login/frontend/src/api/client.js**
```javascript
import axios from 'axios'

const API_URL = import.meta.env.VITE_API_URL || 'http://localhost:8000/api'

const client = axios.create({
  baseURL: API_URL,
  withCredentials: true,
})

export default client
```

**e:/login/frontend/index.html**
```html
<!DOCTYPE html>
<html lang="en">
  <head>
    <meta charset="UTF-8" />
    <meta name="viewport" content="width=device-width, initial-scale=1.0" />
    <title>UniSync</title>
  </head>
  <body>
    <div id="root"></div>
    <script type="module" src="/src/main.jsx"></script>
  </body>
</html>
```

**e:/login/frontend/vite.config.js**
```javascript
import { defineConfig } from 'vite'
import react from '@vitejs/plugin-react'

export default defineConfig({
  plugins: [react()],
  server: {
    port: 3000,
    proxy: {
      '/api': {
        target: 'http://localhost:8000',
        changeOrigin: true,
      },
    },
  },
})
```

**e:/login/frontend/.env.local**
```env
VITE_API_URL=http://localhost:8000/api
VITE_WS_URL=ws://localhost:8000/ws
```

### 6. Create Frontend Dockerfile

Create file: `e:/login/frontend/Dockerfile`

```dockerfile
# Build stage
FROM node:18-alpine AS build

WORKDIR /app

COPY package*.json ./
RUN npm install

COPY . .
RUN npm run build

# Serve stage
FROM nginx:alpine

COPY --from=build /app/dist /usr/share/nginx/html
COPY nginx.conf /etc/nginx/conf.d/default.conf

EXPOSE 80

CMD ["nginx", "-g", "daemon off;"]
```

### 7. Create Frontend nginx.conf

Create file: `e:/login/frontend/nginx.conf`

```nginx
server {
    listen 80;
    server_name _;
    root /usr/share/nginx/html;

    location / {
        try_files $uri $uri/ /index.html;
    }
}
```

### 8. Create Root docker-compose.yml

Create file: `e:/login/docker-compose.yml`

```yaml
version: '3.9'

services:
  backend:
    build:
      context: ./backend
      dockerfile: docker/Dockerfile.backend
    container_name: unisync-backend
    ports:
      - "8000:8000"
    environment:
      - DEBUG=False
      - DATABASE_URL=sqlite:///db.sqlite3
      - REDIS_URL=redis://redis:6379/0
      - CORS_ALLOWED_ORIGINS=http://localhost:3000
    depends_on:
      - redis
    volumes:
      - ./backend:/app
    networks:
      - unisync-network

  frontend:
    build:
      context: ./frontend
    container_name: unisync-frontend
    ports:
      - "3000:80"
    depends_on:
      - backend
    networks:
      - unisync-network

  redis:
    image: redis:7-alpine
    container_name: unisync-redis
    ports:
      - "6379:6379"
    volumes:
      - redis_data:/data
    networks:
      - unisync-network

volumes:
  redis_data:

networks:
  unisync-network:
    driver: bridge
```

### 9. Update backend/auth_project/settings.py

Add CORS configuration:

```python
# Add to INSTALLED_APPS
'corsheaders',

# Add to MIDDLEWARE (at top)
'corsheaders.middleware.CorsMiddleware',

# Add at end
CORS_ALLOWED_ORIGINS = [
    'http://localhost:3000',
    'http://localhost',
]

CORS_ALLOW_CREDENTIALS = True
```

### 10. Create Root .gitignore

Create file: `e:/login/.gitignore`

```
# Backend
backend/.env
backend/*.log
backend/db.sqlite3
backend/__pycache__/
backend/.venv/
backend/venv/
backend/node_modules/

# Frontend
frontend/node_modules/
frontend/.env.local
frontend/dist/
frontend/.DS_Store

# IDE
.vscode/
.idea/
*.swp
*.swo

# OS
.DS_Store
Thumbs.db
```

### 11. Create Root README.md

Create file: `e:/login/README.md`

```markdown
# UniSync - Student Collaboration Platform

## Quick Start

### Docker (Recommended)

```bash
docker-compose up
```

Access:
- Frontend: http://localhost:3000
- Backend: http://localhost:8000
- Admin: http://localhost:8000/admin

### Manual

**Backend:**
```bash
cd backend
python -m venv venv
venv\Scripts\activate  # Windows
source venv/bin/activate  # Mac/Linux
pip install -r requirements.txt
python manage.py migrate
python manage.py runserver
```

**Frontend:**
```bash
cd frontend
npm install
npm run dev
```

## Project Structure

```
├── backend/     - Django REST API
├── frontend/    - React SPA
└── docker-compose.yml
```

## Deployment

- **Backend**: Railway
- **Frontend**: Vercel

See FRONTEND_BACKEND_SEPARATION_GUIDE.md for detailed instructions.
```

---

## Verification Steps

```powershell
# Check backend structure
Get-ChildItem "e:/login/backend"
# Should show: auth_project, accounts, manage.py, requirements.txt, Procfile

# Check frontend structure
Get-ChildItem "e:/login/frontend"
# Should show: src, public, package.json, vite.config.js

# Test Docker
cd e:/login
docker-compose up
# Should start backend on 8000, frontend on 3000
```

---

## Update Django Settings

After moving, update any hardcoded paths in `backend/auth_project/settings.py`:

```python
# Make sure BASE_DIR points correctly
BASE_DIR = Path(__file__).resolve().parent.parent

# Should be: e:/login/backend
```

---

## Next Steps

1. ✅ Reorganize files as above
2. ✅ Create Dockerfiles
3. ✅ Update CORS in Django
4. ✅ Test locally with `docker-compose up`
5. ✅ Deploy backend to Railway
6. ✅ Deploy frontend to Vercel
7. ✅ Update API URLs in frontend

---

Let me know when ready and I'll help with deployment!
