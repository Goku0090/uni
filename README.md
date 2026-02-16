# UniSync - Student Collaboration Platform

Separated Frontend/Backend Architecture with React + Django REST + WebSockets.

## 🚀 Quick Start

### Prerequisites
- Docker & Docker Compose
- OR Python 3.11+ and Node.js 18+ (for manual setup)

### With Docker (Recommended)

```bash
# Start all services
docker-compose up

# Access:
# Frontend:  http://localhost:3000
# Backend:   http://localhost:8000
# Admin:     http://localhost:8000/admin
```

### Manual Setup

#### Backend
```bash
cd backend
python -m venv venv

# Windows
venv\Scripts\activate
# Mac/Linux
source venv/bin/activate

pip install -r requirements.txt
python manage.py migrate
python manage.py runserver
```

#### Frontend (in new terminal)
```bash
cd frontend
npm install
npm run dev
```

Access:
- Frontend: http://localhost:5173 (Vite)
- Backend: http://localhost:8000

## 📁 Project Structure

```
unisync/
├── backend/              # Django REST API
│   ├── auth_project/     # Django settings
│   ├── accounts/         # Main Django app
│   ├── docker/
│   │   └── Dockerfile.backend
│   ├── manage.py
│   ├── requirements.txt
│   ├── .env
│   └── Procfile
├── frontend/             # React SPA
│   ├── src/
│   │   ├── App.jsx
│   │   ├── main.jsx
│   │   ├── api/
│   │   │   └── client.js
│   │   └── index.css
│   ├── Dockerfile
│   ├── nginx.conf
│   ├── vite.config.js
│   ├── package.json
│   └── .env.local
└── docker-compose.yml
```

## 🔧 Configuration

### Backend Environment Variables

Create `backend/.env`:
```env
DEBUG=False
SECRET_KEY=your-secret-key-here
ALLOWED_HOSTS=localhost,127.0.0.1,*.railway.app,your-domain.com
DATABASE_URL=postgresql://user:password@host/db
REDIS_URL=redis://redis:6379/0
CORS_ALLOWED_ORIGINS=http://localhost:3000,https://your-frontend-domain.com
BREVO_API_KEY=your-brevo-key
GOOGLE_OAUTH_CLIENT_ID=your-google-id
GOOGLE_OAUTH_SECRET=your-google-secret
```

### Frontend Environment Variables

`frontend/.env.local`:
```env
VITE_API_URL=http://localhost:8000/api
VITE_WS_URL=ws://localhost:8000/ws
```

## 📝 API Endpoints

Backend provides REST API at `http://localhost:8000/api/`:

### Authentication
- `POST /login/` - User login
- `POST /register/` - User registration
- `GET /logout/` - User logout

### Projects
- `GET /projects/` - List projects
- `POST /projects/` - Create project
- `GET /projects/{id}/` - Get project details
- `PUT /projects/{id}/` - Update project
- `DELETE /projects/{id}/` - Delete project

### Messaging
- `GET /chat-rooms/` - List chat rooms
- `POST /messages/` - Send message
- `WebSocket /ws/chat/{room_id}/` - Real-time messaging

For full API reference, see `COMPREHENSIVE_CODE_ANALYSIS_2026_FINAL.md`.

## 🐳 Docker Commands

```bash
# Start services
docker-compose up

# Stop services
docker-compose down

# View logs
docker-compose logs -f backend
docker-compose logs -f frontend

# Rebuild images
docker-compose up --build

# Run migrations
docker-compose exec backend python manage.py migrate

# Create superuser
docker-compose exec backend python manage.py createsuperuser
```

## 🚢 Deployment

### Backend → Railway

1. Create Railway account
2. Connect GitHub repository
3. Select `backend/` directory
4. Set environment variables
5. Deploy

### Frontend → Vercel

1. Create Vercel account
2. Connect GitHub repository
3. Select `frontend/` directory
4. Set `VITE_API_URL` to your Railway backend URL
5. Deploy

## 📚 Documentation

- `COMPREHENSIVE_CODE_ANALYSIS_2026_FINAL.md` - Complete codebase analysis
- `FRONTEND_BACKEND_SEPARATION_GUIDE.md` - Detailed separation guide
- `FRONTEND_BACKEND_QUICK_START.md` - Quick setup guide

## 🛠️ Development

### Backend Development
```bash
cd backend
python manage.py runserver          # Start dev server
python manage.py makemigrations     # Create migrations
python manage.py migrate            # Apply migrations
python manage.py test               # Run tests
```

### Frontend Development
```bash
cd frontend
npm run dev                         # Start dev server
npm run build                       # Production build
npm run preview                     # Preview build
```

## 🔐 Security

- ✅ CSRF token protection
- ✅ CORS configuration
- ✅ Environment-based secrets
- ✅ Password hashing (PBKDF2)
- ✅ XSS prevention
- ✅ SQL injection prevention

## 📊 Key Features

- 🔐 User authentication (Email OTP + OAuth)
- 🎯 Project management & discovery
- 👥 Team collaboration
- 💬 Real-time messaging (WebSocket)
- 🔔 Live notifications
- 🌐 API-first architecture
- 📱 Mobile-ready SPA

## 🐛 Troubleshooting

### API Connection Error
```javascript
// Check CORS in backend/auth_project/settings.py
CORS_ALLOWED_ORIGINS = ['http://localhost:3000']
```

### Static Files Not Loading
```bash
docker-compose exec backend python manage.py collectstatic --noinput
```

### Database Issues
```bash
docker-compose exec backend python manage.py migrate
docker-compose exec backend python manage.py createsuperuser
```

## 📞 Support

For detailed documentation and analysis, see:
- `START_FRONTEND_BACKEND_SEPARATION.md`
- `REORGANIZE_PROJECT.md`
- `ANALYSIS_COMPLETE_2026_FINAL.md`

## 📄 License

MIT License

---

**Status:** ✅ Production Ready

**Last Updated:** February 16, 2026
