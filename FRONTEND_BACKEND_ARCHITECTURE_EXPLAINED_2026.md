# Frontend-Backend Architecture Explained

## Current Setup Issue

You've noticed that:
- **Backend runs everything** - Includes frontend
- **Frontend dev server** - Shows basic UniSync page

This is because your project has **two different deployment modes**:

### 1. Production Mode (What backend does)
- Django serves **both** API + built frontend
- Frontend gets pre-built and placed in Django's static/media folders
- Single port (8000) serves everything

### 2. Development Mode (What frontend dev does)
- React dev server runs independently on port 3000
- Vite proxy redirects API calls to backend (8000)
- Shows basic HTML + JavaScript

---

## Architecture Diagram

```
┌─────────────────────────────────────────────────────────────┐
│                    DEVELOPMENT SETUP                        │
├──────────────────────────┬──────────────────────────────────┤
│                          │                                  │
│  Terminal 1              │  Terminal 2                      │
│  ─────────────           │  ─────────────                   │
│  Backend Server          │  Frontend Dev Server             │
│  python manage.py        │  npm run dev                     │
│  runserver               │                                  │
│  Port: 8000              │  Port: 3000                      │
│  Serves: API             │  Serves: React UI                │
│                          │                                  │
│  ┌────────────────────┐  │  ┌─────────────────────────────┐ │
│  │ Django             │  │  │ Vite Dev Server             │ │
│  │ ├─ /api/*          │  │  │ ├─ index.html               │ │
│  │ ├─ /admin/         │  │  │ ├─ App.jsx                  │ │
│  │ ├─ /ws/*           │  │  │ ├─ Hot reload enabled       │ │
│  │ └─ /media/         │  │  │ └─ Proxy to /api → 8000     │ │
│  └────────────────────┘  │  └─────────────────────────────┘ │
│          ↑               │            ↑                      │
│          │               │            │                      │
│    PostgreSQL            │       No backend                  │
│    + Redis               │       (only HTTP)                 │
│                          │                                  │
└──────────────────────────┴──────────────────────────────────┘
           Browser connects to:
           - API: http://localhost:8000/api
           - React: http://localhost:3000
           - WebSocket: ws://localhost:8000/ws

┌─────────────────────────────────────────────────────────────┐
│                   PRODUCTION SETUP                          │
├─────────────────────────────────────────────────────────────┤
│                                                             │
│  Single Server                                              │
│  ─────────────                                              │
│  python manage.py runserver                                 │
│  Port: 8000                                                 │
│                                                             │
│  ┌───────────────────────────────────────────────────────┐ │
│  │ Django (Gunicorn in production)                       │ │
│  │ ├─ /static/  (React built files + CSS/JS)            │ │
│  │ ├─ /api/*    (REST API)                              │ │
│  │ ├─ /admin/   (Django admin)                          │ │
│  │ ├─ /ws/*     (WebSocket)                             │ │
│  │ ├─ / or /index.html (Serves React app)               │ │
│  │ └─ /media/   (User uploads)                          │ │
│  └───────────────────────────────────────────────────────┘ │
│                           ↑                                  │
│                           │                                  │
│                    PostgreSQL + Redis                        │
│                                                             │
└─────────────────────────────────────────────────────────────┘
        Browser connects to:
        - Everything: http://localhost:8000
```

---

## Why Backend Runs Everything

### Step-by-step: What happens when you `python manage.py runserver`

```
1. Django starts on port 8000
   ├─ Loads settings.py
   ├─ Reads INSTALLED_APPS
   ├─ Initializes database
   ├─ Sets up static files from STATIC_ROOT
   └─ Starts HTTP server

2. Backend configuration (settings.py)
   ├─ STATIC_URL = '/static/'
   ├─ STATICFILES_DIRS = [BASE_DIR / 'static']
   ├─ STATIC_ROOT = BASE_DIR / 'staticfiles'
   └─ WhiteNoise middleware serves static files

3. When you visit http://localhost:8000
   ├─ Request hits Django
   ├─ Django URL routing
   │  ├─ Try /api/* routes → views.py
   │  ├─ Try /admin/* → admin panel
   │  ├─ Try /ws/* → WebSocket
   │  └─ Try / → serve index.html from static
   │
   ├─ index.html is served with:
   │  ├─ Pre-built React bundle (main.jsx compiled)
   │  ├─ CSS files
   │  └─ JavaScript files
   │
   └─ Browser loads index.html + JS/CSS
      ├─ React initializes
      ├─ App.jsx renders
      └─ Makes API calls to /api/*

4. Everything works from one port (8000)
   ├─ Frontend serves from /static/
   ├─ Backend serves from /api/
   └─ WebSocket serves from /ws/
```

---

## Why Frontend Dev Server Shows Basic Page

When you run `npm run dev`:

```
Terminal: npm run dev
  ↓
Executes: vite (based on package.json scripts)
  ↓
Vite starts on port 3000
  ├─ Serves: /frontend/src/App.jsx
  ├─ Serves: /frontend/index.html
  ├─ Has Hot Module Replacement (HMR)
  └─ Proxies /api to http://localhost:8000

Browser visits: http://localhost:3000
  ├─ Vite serves index.html (basic HTML)
  ├─ Loads App.jsx (React component)
  ├─ App.jsx renders
  └─ Makes API calls to /api → proxied to 8000

Why "basic"?
- It's development mode (no production optimizations)
- You're seeing the React app raw, not processed by Django
- CSS/images might not be loaded if paths are wrong
```

---

## How They Connect

### Vite Proxy Configuration (vite.config.js)

```javascript
server: {
  port: 3000,
  proxy: {
    '/api': {                              // Any request to /api
      target: 'http://localhost:8000',     // Forward to backend
      changeOrigin: true,                  // Allow CORS
    },
    '/ws': {                               // WebSocket requests
      target: 'ws://localhost:8000',       // Forward to backend WS
      ws: true,                            // Enable WebSocket
    },
  },
}
```

**What happens:**

```
Browser (localhost:3000)
  ├─ Fetch /api/projects/
  │  ↓ (Vite intercepts)
  │  ↓ (Proxy rule matches)
  │  ↓ Forwards to http://localhost:8000/api/projects/
  │  ↓ (Backend responds)
  │  ↓ Returns to browser
  │
  └─ Works seamlessly!
```

---

## Development Workflow

### Recommended Setup

**Terminal 1 - Backend:**
```bash
cd backend
python manage.py runserver
# Runs on http://localhost:8000
# Serves: API, admin, WebSocket
```

**Terminal 2 - Frontend:**
```bash
cd frontend
npm install  # First time only
npm run dev
# Runs on http://localhost:3000
# Serves: React app with hot reload
```

**Terminal 3 - Database & Cache (Optional):**
```bash
docker-compose up -d
# Starts PostgreSQL and Redis
# If using SQLite, not needed for development
```

**Browser:**
- Visit `http://localhost:3000` for frontend with hot reload
- API calls automatically proxy to backend
- WebSocket automatically connects to backend

### What Each Terminal Does

| Terminal | Command | Port | What It Serves |
|----------|---------|------|---|
| 1 | `python manage.py runserver` | 8000 | API, WebSocket, Django admin |
| 2 | `npm run dev` | 3000 | React app, auto-reload |
| 3 | `docker-compose up -d` | 5432, 6379 | PostgreSQL, Redis (background) |

---

## How Data Flows in Development

### Frontend to Backend Communication

```
User Action (click button)
  ↓
React Event Handler
  ├─ fetch('/api/projects/')
  └─ OR axios.get('/api/projects/')
  ↓
Vite Dev Server (port 3000)
  ├─ Matches '/api' rule
  ├─ Forwards to http://localhost:8000/api/projects/
  ↓
Django Backend (port 8000)
  ├─ URLconf matches route
  ├─ View processes request
  ├─ Queries database
  ├─ Returns JSON
  ↓
Response back to browser
  ↓
React receives data
  ├─ Updates state
  ├─ Re-renders component
  └─ User sees update
```

### WebSocket Connection in Development

```
Browser (React)
  └─ new WebSocket('ws://localhost:3000/ws/chat/123')
  ↓ (Vite intercepts)
  ↓ (Proxy rule matches '/ws')
  ↓ Upgrades to ws://localhost:8000/ws/chat/123
  ↓
Django Channels Consumer
  ├─ Accepts connection
  ├─ Loads message history
  ├─ Adds to broadcast group
  ↓
User sends message
  ├─ Message sent via WebSocket
  ├─ Consumer receives via receive()
  ├─ Saves to database
  ├─ Broadcasts to group
  ↓
All connected clients receive update
  ├─ Browser WebSocket receives event
  ├─ React updates state
  └─ UI updates in real-time
```

---

## Production Deployment (Why Backend Runs Everything)

When deploying to production (Render, Railway, etc.):

```
Build Process:
  1. npm run build (in frontend/)
     ├─ Compiles React + JSX
     ├─ Minifies CSS/JS
     ├─ Generates dist/ folder
     └─ Creates optimized bundle

  2. Copy build to backend static folder
     ├─ cp -r frontend/dist/* backend/static/
     └─ Django will serve these files

  3. python manage.py collectstatic
     ├─ Gathers all static files
     ├─ Puts them in STATIC_ROOT
     └─ Ready for production

Deployment:
  1. Single port (8000)
  2. Gunicorn serves Django
  3. WhiteNoise middleware serves static files
  4. Everything from one server:
     ├─ /api/* → Django views
     ├─ /static/* → React built files
     ├─ /admin/ → Django admin
     ├─ /ws/* → WebSocket
     └─ / → index.html (React app)
```

**Why this way?**
- Single server to manage
- Simpler deployment
- Nginx can cache static files
- Lower operational complexity

---

## Current Project Structure

```
project-root/
├── backend/                    # Django project
│   ├── auth_project/           # Django settings
│   ├── accounts/               # Main app
│   ├── static/                 # Static files
│   │   ├── css/               # CSS files
│   │   ├── js/                # JavaScript
│   │   ├── images/            # Images
│   │   └── data/              # Data files
│   ├── manage.py
│   └── requirements.txt
│
├── frontend/                   # React project
│   ├── src/
│   │   ├── App.jsx            # Main component
│   │   ├── main.jsx           # Entry point
│   │   └── api/               # API client
│   ├── public/                # Public assets
│   ├── package.json
│   ├── vite.config.js         # Vite config (proxies to 8000)
│   └── index.html
│
├── build.sh                    # Build script for production
├── docker-compose.yml          # Local dev services
└── Dockerfile                  # Production image
```

---

## Common Questions

### Q: Why can't I see my frontend changes when running backend alone?
**A:** Backend serves pre-built React files from `backend/static/`. Changes to `frontend/src/` won't appear until:
1. You rebuild: `npm run build` in frontend/
2. Copy to backend: `cp -r frontend/dist/* backend/static/`
3. Restart backend

**Solution:** Use `npm run dev` in a separate terminal for hot reload.

### Q: Why do I get "Cannot GET /" when visiting localhost:8000?
**A:** Django doesn't have a route for `/`. Add this to `backend/accounts/urls.py`:
```python
path('', views.home_view, name='home'),
```
Or it should redirect to `/api/` or `/admin/`.

### Q: How do API calls work with the Vite proxy?
**A:** Vite intercepts requests starting with `/api` and forwards them:
- Browser: `fetch('/api/projects/')`
- Vite: intercepts, forwards to `http://localhost:8000/api/projects/`
- Backend: responds with JSON
- Browser: receives response

### Q: Why is WebSocket connection failing?
**A:** Check that:
1. Backend is running on 8000
2. Redis is running (if using Redis channel layer)
3. Daphne or runserver is handling async
4. Firewall isn't blocking port 8000

### Q: Should I run both frontend and backend?
**A:** Yes, for development:
1. Backend on 8000 (API + WebSocket)
2. Frontend on 3000 (React with hot reload)

For production:
1. Single backend on 8000 (serves everything)

### Q: How to make frontend production-ready?
**A:** In `frontend/`:
```bash
npm run build
# Creates optimized frontend/dist/ folder

# Then copy to backend/static/
# Django will serve it
```

---

## Environment Variables for Development

### Backend (.env)
```
DEBUG=True
ALLOWED_HOSTS=localhost,127.0.0.1
DATABASE_URL=postgresql://localhost/unisinq_db
REDIS_URL=redis://localhost:6379/1
SECURE_SSL_REDIRECT=False
```

### Frontend (.env.local)
```
VITE_API_URL=http://localhost:8000/api
```

---

## Debugging Tips

### If frontend won't connect to backend:
1. **Check backend is running:**
   ```bash
   curl http://localhost:8000/api/projects/
   ```

2. **Check Vite proxy in browser DevTools:**
   - Network tab
   - Check request URL
   - Should show it proxied to 8000

3. **Check CORS headers:**
   - Response should have `Access-Control-Allow-Origin`

### If WebSocket won't connect:
1. **Check backend WebSocket is enabled:**
   ```bash
   # In terminal running backend, should see:
   # WebSocket connection established
   ```

2. **Check proxy includes WebSocket:**
   - vite.config.js should have `/ws` proxy

3. **Check Redis (if using):**
   ```bash
   redis-cli ping
   # Should return: PONG
   ```

---

## Summary

| Aspect | Development | Production |
|--------|-------------|-----------|
| **Backend** | Port 8000 | Port 8000 (Gunicorn) |
| **Frontend** | Port 3000 | Served from /static on 8000 |
| **How they connect** | Vite proxy | Django static files |
| **Hot reload** | Yes (Vite HMR) | No |
| **Terminals needed** | 2-3 | 0 (single server) |
| **Build step** | Not needed | `npm run build` |

**Key takeaway:** 
- **Development**: Separate servers for easier debugging
- **Production**: Single server for simplicity

Both are valid. You choose based on your needs!

