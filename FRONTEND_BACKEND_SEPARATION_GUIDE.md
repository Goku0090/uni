# Frontend/Backend Separation Guide

## New Project Structure

```
unisync/
├── backend/                    # Django API Server
│   ├── auth_project/
│   │   ├── settings.py
│   │   ├── urls.py
│   │   ├── wsgi.py
│   │   └── asgi.py
│   ├── accounts/
│   │   ├── models.py
│   │   ├── views.py
│   │   ├── urls.py
│   │   ├── serializers.py
│   │   ├── chat_api.py
│   │   └── ...
│   ├── manage.py
│   ├── requirements.txt
│   ├── .env
│   ├── Procfile
│   ├── db.sqlite3
│   └── docker/
│       └── Dockerfile.backend
│
├── frontend/                   # React/Vue/Angular Frontend
│   ├── src/
│   │   ├── components/
│   │   ├── pages/
│   │   ├── api/
│   │   ├── App.jsx
│   │   └── index.jsx
│   ├── public/
│   ├── package.json
│   ├── .env.local
│   ├── vite.config.js          # or webpack.config.js
│   ├── docker/
│   │   └── Dockerfile.frontend
│   └── README.md
│
├── docker-compose.yml          # Orchestrate both services
├── .gitignore
└── README.md
```

---

## Step 1: Organize Backend

### Move Django project to backend/

```bash
# From project root
mkdir backend
mv auth_project backend/
mv accounts backend/
mv manage.py backend/
mv requirements.txt backend/
mv Procfile backend/
mv .env backend/
```

### Create backend/Dockerfile

```dockerfile
FROM python:3.11-slim

WORKDIR /app

# Install dependencies
COPY requirements.txt .
RUN pip install -r requirements.txt

# Copy Django project
COPY . .

# Collect static files
RUN python manage.py collectstatic --noinput

# Start Gunicorn
CMD ["gunicorn", "auth_project.wsgi", "--bind", "0.0.0.0:8000", "--workers", "4"]
```

### Update backend/.env

```env
DEBUG=False
SECRET_KEY=your-secret-key
ALLOWED_HOSTS=localhost,127.0.0.1,*.railway.app,your-domain.com
DATABASE_URL=postgresql://...
REDIS_URL=redis://redis:6379/0
CORS_ALLOWED_ORIGINS=http://localhost:3000,https://your-frontend-domain.com
```

### Update backend/auth_project/settings.py

```python
# Add CORS support
CORS_ALLOWED_ORIGINS = os.getenv('CORS_ALLOWED_ORIGINS', '').split(',')

# API is now separate from frontend
REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': [
        'rest_framework.authentication.SessionAuthentication',
        'rest_framework.authentication.TokenAuthentication',
    ],
}

# Static files (for API docs)
STATIC_URL = '/static/'
STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')

# CSRF trusted origins for CORS requests
CSRF_TRUSTED_ORIGINS = os.getenv('CSRF_TRUSTED_ORIGINS', '').split(',')
```

### Create backend/Procfile

```
web: gunicorn auth_project.wsgi --bind 0.0.0.0:$PORT --workers 4
worker: python manage.py runworker -v 3
```

---

## Step 2: Create Frontend

### Option A: React with Vite (Recommended)

```bash
cd frontend
npm create vite@latest . -- --template react
npm install
npm install axios react-router-dom
```

### Create frontend/.env.local

```env
VITE_API_URL=http://localhost:8000/api
VITE_WS_URL=ws://localhost:8000/ws
```

### Create frontend/src/api/client.js

```javascript
import axios from 'axios';

const API_URL = import.meta.env.VITE_API_URL;

const client = axios.create({
  baseURL: API_URL,
  withCredentials: true, // For cookies/sessions
});

export const login = (email, password) => 
  client.post('/login/', { email, password });

export const getProfile = () => 
  client.get('/profile/');

export const getProjects = () => 
  client.get('/projects/');

export const createProject = (data) => 
  client.post('/projects/', data);

export const getMessages = (roomId) => 
  client.get(`/chat-rooms/${roomId}/messages/`);

export const sendMessage = (roomId, content) => 
  client.post('/messages/', { room: roomId, content });

export default client;
```

### Create frontend/Dockerfile

```dockerfile
FROM node:18-alpine

WORKDIR /app

# Install dependencies
COPY package*.json ./
RUN npm install

# Copy source
COPY . .

# Build
RUN npm run build

# Serve with nginx
FROM nginx:alpine
COPY --from=0 /app/dist /usr/share/nginx/html
COPY nginx.conf /etc/nginx/conf.d/default.conf

EXPOSE 80
CMD ["nginx", "-g", "daemon off;"]
```

### Create frontend/nginx.conf

```nginx
server {
    listen 80;
    server_name _;
    root /usr/share/nginx/html;

    location / {
        try_files $uri $uri/ /index.html;
    }

    location /api {
        proxy_pass http://backend:8000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }

    location /ws {
        proxy_pass http://backend:8000;
        proxy_http_version 1.1;
        proxy_set_header Upgrade $http_upgrade;
        proxy_set_header Connection "upgrade";
        proxy_set_header Host $host;
    }
}
```

### Create frontend/package.json

```json
{
  "name": "unisync-frontend",
  "version": "1.0.0",
  "type": "module",
  "scripts": {
    "dev": "vite",
    "build": "vite build",
    "preview": "vite preview",
    "lint": "eslint src"
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

---

## Step 3: Docker Compose Setup

### Create docker-compose.yml

```yaml
version: '3.9'

services:
  # Backend API
  backend:
    build:
      context: ./backend
      dockerfile: docker/Dockerfile.backend
    container_name: unisync-backend
    ports:
      - "8000:8000"
    environment:
      - DEBUG=False
      - DATABASE_URL=postgresql://postgres:password@postgres:5432/unisync
      - REDIS_URL=redis://redis:6379/0
      - CORS_ALLOWED_ORIGINS=http://localhost:3000
    depends_on:
      - postgres
      - redis
    volumes:
      - ./backend:/app
    networks:
      - unisync-network
    command: >
      sh -c "python manage.py migrate &&
             gunicorn auth_project.wsgi --bind 0.0.0.0:8000 --workers 4"

  # Frontend
  frontend:
    build:
      context: ./frontend
      dockerfile: Dockerfile
    container_name: unisync-frontend
    ports:
      - "3000:80"
    depends_on:
      - backend
    networks:
      - unisync-network
    environment:
      - VITE_API_URL=http://backend:8000/api

  # PostgreSQL Database
  postgres:
    image: postgres:15
    container_name: unisync-postgres
    environment:
      - POSTGRES_USER=postgres
      - POSTGRES_PASSWORD=password
      - POSTGRES_DB=unisync
    volumes:
      - postgres_data:/var/lib/postgresql/data
    ports:
      - "5432:5432"
    networks:
      - unisync-network
    healthcheck:
      test: ["CMD-SHELL", "pg_isready -U postgres"]
      interval: 10s
      timeout: 5s
      retries: 5

  # Redis Cache & Message Broker
  redis:
    image: redis:7-alpine
    container_name: unisync-redis
    ports:
      - "6379:6379"
    volumes:
      - redis_data:/data
    networks:
      - unisync-network
    healthcheck:
      test: ["CMD", "redis-cli", "ping"]
      interval: 10s
      timeout: 5s
      retries: 5

volumes:
  postgres_data:
  redis_data:

networks:
  unisync-network:
    driver: bridge
```

---

## Step 4: Environment Files

### backend/.env

```env
# Django
DEBUG=False
SECRET_KEY=your-secret-key-here
ALLOWED_HOSTS=localhost,127.0.0.1,*.railway.app,your-domain.com

# Database
DATABASE_URL=postgresql://postgres:password@postgres:5432/unisync

# Redis
REDIS_URL=redis://redis:6379/0

# CORS
CORS_ALLOWED_ORIGINS=http://localhost:3000,https://your-frontend-domain.com
CSRF_TRUSTED_ORIGINS=http://localhost:3000,https://your-frontend-domain.com

# Email
BREVO_API_KEY=your-brevo-key
EMAIL_FROM=noreply@unisync.com

# OAuth
GOOGLE_OAUTH_CLIENT_ID=your-google-id
GOOGLE_OAUTH_SECRET=your-google-secret
GITHUB_OAUTH_CLIENT_ID=your-github-id
GITHUB_OAUTH_SECRET=your-github-secret
```

### frontend/.env.local

```env
VITE_API_URL=http://localhost:8000/api
VITE_WS_URL=ws://localhost:8000/ws
```

---

## Step 5: Update Django Settings for CORS

### backend/auth_project/settings.py

```python
# Add django-cors-headers
INSTALLED_APPS = [
    ...
    'corsheaders',
    ...
]

MIDDLEWARE = [
    'corsheaders.middleware.CorsMiddleware',
    'django.middleware.security.SecurityMiddleware',
    ...
]

# CORS Configuration
CORS_ALLOWED_ORIGINS = os.getenv('CORS_ALLOWED_ORIGINS', '').split(',')
CORS_ALLOW_CREDENTIALS = True

# CSRF Configuration for separate frontend
CSRF_TRUSTED_ORIGINS = os.getenv('CSRF_TRUSTED_ORIGINS', '').split(',')
```

---

## Step 6: Create Root .gitignore

```
# Backend
backend/.env
backend/*.log
backend/db.sqlite3
backend/__pycache__/
backend/.venv/
backend/venv/

# Frontend
frontend/node_modules/
frontend/.env.local
frontend/dist/
frontend/.DS_Store

# General
.DS_Store
*.pyc
.env
node_modules/
```

---

## Step 7: Create Root README.md

```markdown
# UniSync - Student Collaboration Platform

## Project Structure

```
unisync/
├── backend/    - Django REST API
├── frontend/   - React SPA
└── docker-compose.yml
```

## Local Development

### Option 1: Docker (Recommended)

```bash
docker-compose up
```

Access:
- Frontend: http://localhost:3000
- Backend API: http://localhost:8000
- Django Admin: http://localhost:8000/admin

### Option 2: Local (Manual)

**Backend:**
```bash
cd backend
python -m venv venv
source venv/bin/activate
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

## Deployment

### Railway: Deploy Backend

1. Create new Railway project
2. Add GitHub repo
3. Set environment variables
4. Deploy

### Vercel: Deploy Frontend

1. Create Vercel project
2. Connect GitHub
3. Set `VITE_API_URL` to your Railway backend URL
4. Deploy

### Docker Compose (Self-hosted)

```bash
docker-compose up -d
```
```

---

## Step 8: Update API URLs in Django

### backend/auth_project/urls.py

```python
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include('accounts.urls')),  # All APIs under /api/
    path('api-auth/', include('rest_framework.urls')),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
```

---

## Step 9: Deployment on Railway

### Backend on Railway

1. Create new Railway project
2. Add Variables:
```
DATABASE_URL=postgresql://...
REDIS_URL=redis://...
CORS_ALLOWED_ORIGINS=https://your-frontend-domain.com
```

3. Set Procfile with Gunicorn command

### Frontend on Vercel/Netlify

1. Create new project
2. Set environment variable:
```
VITE_API_URL=https://your-backend-railway-url/api
VITE_WS_URL=wss://your-backend-railway-url/ws
```

3. Deploy

---

## Migration Checklist

- [ ] Move Django files to `backend/`
- [ ] Create `frontend/` directory with React
- [ ] Create `docker-compose.yml`
- [ ] Update Django settings for CORS
- [ ] Create environment files
- [ ] Test locally with Docker
- [ ] Deploy backend to Railway
- [ ] Deploy frontend to Vercel
- [ ] Update CORS origins in Railway
- [ ] Test frontend-backend communication

---

## Benefits of Separation

✅ **Independent Deployment** - Update frontend/backend separately
✅ **Scalability** - Scale each tier independently
✅ **Technology Flexibility** - Replace frontend with any framework
✅ **Team Organization** - Frontend & backend teams work independently
✅ **CI/CD** - Separate pipelines for frontend/backend
✅ **Performance** - Frontend served from CDN
✅ **Maintenance** - Clearer code organization

---

## Local Development Commands

```bash
# Start everything
docker-compose up

# Start specific service
docker-compose up backend
docker-compose up frontend

# View logs
docker-compose logs -f backend
docker-compose logs -f frontend

# Stop everything
docker-compose down

# Remove volumes
docker-compose down -v
```

---

## Next Steps

1. Reorganize files as shown above
2. Test locally with Docker
3. Deploy backend to Railway
4. Deploy frontend to Vercel
5. Update environment variables
6. Test end-to-end
