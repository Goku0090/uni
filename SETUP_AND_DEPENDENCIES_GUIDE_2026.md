# Setup & Dependencies Guide 2026

## System Requirements

### Minimum Requirements
- **OS**: Windows 10+, macOS 10.15+, Ubuntu 18.04+
- **CPU**: 2 cores
- **RAM**: 4GB (8GB recommended)
- **Disk**: 5GB for development environment
- **Python**: 3.9+ (3.11+ recommended)
- **Node.js**: 16+ (18+ recommended)

### Recommended Setup
- **OS**: Ubuntu 20.04+ or macOS 12+
- **CPU**: 4+ cores
- **RAM**: 8GB+
- **Disk**: 10GB+ SSD
- **Python**: 3.11
- **Node.js**: 20 LTS

---

## Backend Dependencies

### Core Dependencies (requirements.txt)

**Web Framework & API**
```
Django==4.2.8                          # Web framework
djangorestframework==3.14.0            # REST API
drf-spectacular==0.26.5                # API documentation
```

**Database**
```
psycopg2-binary==2.9.9                # PostgreSQL adapter
dj-database-url==2.1.0                # Database URL parser
```

**Authentication & Social Login**
```
django-allauth==0.61.1                # Auth + social login
requests==2.31.0                      # HTTP library
requests-oauthlib==1.3.1              # OAuth support
```

**WebSocket & Real-time**
```
channels==4.0.0                       # WebSocket support
channels-redis==4.1.0                 # Redis channel layer
redis==5.0.1                          # Redis client
django-redis==5.4.0                   # Redis cache
```

**Utilities**
```
python-dotenv==1.0.0                  # .env file loading
django-cors-headers==4.3.1            # CORS handling
gunicorn==21.2.0                      # Production WSGI
whitenoise==6.6.0                     # Static file serving
```

**Data Processing**
```
pandas==2.0.3                         # Data manipulation
numpy==1.24.3                         # Numerical computing
```

**NLP & ML (Optional)**
```
nltk==3.8.1                           # Natural language processing
spacy==3.7.2                          # Advanced NLP
textblob==0.17.1                      # Text analysis
scikit-learn==1.3.2                   # Machine learning
```

**Image Processing**
```
pillow==10.0.0                        # Image library
```

**Security**
```
cryptography==41.0.4                  # Encryption
```

---

## Frontend Dependencies

### npm Packages (package.json)

**Core Framework**
```json
{
  "react": "^18.2.0",              // UI library
  "react-dom": "^18.2.0",          // React DOM rendering
  "react-router-dom": "^6.20.0"    // Client-side routing
}
```

**HTTP Client**
```json
{
  "axios": "^1.6.0"                // Promise-based HTTP
}
```

**Build Tools (Dev Dependencies)**
```json
{
  "vite": "^5.0.0",                // Build tool
  "@vitejs/plugin-react": "^4.2.0" // React plugin for Vite
}
```

### Optional Packages (Not Included)
```
Material-UI: UI component library
Tailwind CSS: Utility-first CSS
Redux: State management
Socket.io: WebSocket wrapper
```

---

## Installation Guide

### Prerequisites Installation

#### Windows
```bash
# Install Chocolatey (if not installed)
# https://chocolatey.org/install

# Install Python 3.11
choco install python --version 3.11

# Install Node.js LTS
choco install nodejs

# Verify installations
python --version
node --version
npm --version
```

#### macOS
```bash
# Install Homebrew (if not installed)
/bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"

# Install Python
brew install python@3.11

# Install Node.js
brew install node

# Verify
python3 --version
node --version
npm --version
```

#### Ubuntu/Debian
```bash
# Update package lists
sudo apt update

# Install Python
sudo apt install python3.11 python3.11-venv python3-pip

# Install Node.js (using NodeSource)
curl -fsSL https://deb.nodesource.com/setup_20.x | sudo -E bash -
sudo apt install nodejs

# Verify
python3.11 --version
node --version
npm --version
```

### Backend Setup

#### 1. Clone Repository
```bash
git clone https://github.com/Goku0090/uni.git
cd uni/backend
```

#### 2. Create Virtual Environment
```bash
# Windows
python -m venv venv
venv\Scripts\activate

# macOS/Linux
python3.11 -m venv venv
source venv/bin/activate
```

#### 3. Install Dependencies
```bash
pip install --upgrade pip setuptools wheel
pip install -r requirements.txt
```

#### 4. Configure Environment
```bash
# Copy example env file
cp .env.example .env

# Edit .env with your settings
# Windows: notepad .env
# macOS/Linux: nano .env
```

**Minimum .env Configuration:**
```env
# Security
DEBUG=True
SECRET_KEY=your-secret-key-here
ALLOWED_HOSTS=localhost,127.0.0.1

# Database (choose one)
# Option 1: PostgreSQL
DATABASE_URL=postgresql://user:password@localhost:5432/unisinq_db

# Option 2: SQLite (default)
# DATABASE_URL=sqlite:///db.sqlite3

# Email (at least one)
# Option 1: Brevo (Recommended)
BREVO_API_KEY=your-brevo-api-key

# Option 2: Gmail
EMAIL_HOST_USER=your-email@gmail.com
EMAIL_HOST_PASSWORD=your-app-password

# OAuth (Optional)
GOOGLE_CLIENT_ID=your-google-client-id
GOOGLE_CLIENT_SECRET=your-google-client-secret
GITHUB_CLIENT_ID=your-github-client-id
GITHUB_CLIENT_SECRET=your-github-client-secret

# CORS
CORS_ALLOWED_ORIGINS=http://localhost:3000
CSRF_TRUSTED_ORIGINS=http://localhost:3000
```

#### 5. Database Setup
```bash
# Create migrations
python manage.py makemigrations

# Apply migrations
python manage.py migrate

# Create superuser (admin)
python manage.py createsuperuser
# Enter: username, email, password

# Create test data (optional)
python manage.py loaddata sample_data.json
```

#### 6. Collect Static Files
```bash
python manage.py collectstatic --noinput
```

#### 7. Run Development Server
```bash
python manage.py runserver
# Access at http://localhost:8000
```

---

### Frontend Setup

#### 1. Navigate to Frontend Directory
```bash
cd ../frontend
```

#### 2. Install Dependencies
```bash
npm install
```

#### 3. Configure Environment (Optional)
```bash
# Create .env.local
echo "VITE_API_URL=http://localhost:8000" > .env.local
```

#### 4. Run Development Server
```bash
npm run dev
# Access at http://localhost:5173
```

---

## Database Setup

### Option 1: SQLite (Development - Easiest)
No setup required. Django will create `db.sqlite3` automatically.

### Option 2: PostgreSQL (Recommended for Production)

#### Windows
```bash
# Download PostgreSQL from https://www.postgresql.org/download/windows/
# Run installer, keep defaults
# Set password for 'postgres' user

# Add to PATH (if not auto-added):
# C:\Program Files\PostgreSQL\15\bin

# Create database and user
psql -U postgres
```

```sql
-- In psql prompt
CREATE DATABASE unisinq_db;
CREATE USER unisinq_user WITH PASSWORD 'your_password';
ALTER ROLE unisinq_user SET client_encoding TO 'utf8';
ALTER ROLE unisinq_user SET default_transaction_isolation TO 'read committed';
ALTER ROLE unisinq_user SET default_transaction_deferrable TO on;
ALTER ROLE unisinq_user SET timezone TO 'UTC';
GRANT ALL PRIVILEGES ON DATABASE unisinq_db TO unisinq_user;
\q
```

#### macOS
```bash
# Install PostgreSQL
brew install postgresql@15

# Start PostgreSQL
brew services start postgresql@15

# Create database and user
createdb unisinq_db
createuser -P unisinq_user
# Enter password twice

# Grant privileges
psql -d unisinq_db
```

```sql
ALTER USER unisinq_user CREATEDB;
GRANT ALL PRIVILEGES ON DATABASE unisinq_db TO unisinq_user;
\q
```

#### Ubuntu/Debian
```bash
# Install PostgreSQL
sudo apt install postgresql postgresql-contrib

# Start service
sudo service postgresql start

# Create database and user
sudo -u postgres psql
```

```sql
CREATE DATABASE unisinq_db;
CREATE USER unisinq_user WITH PASSWORD 'your_password';
ALTER ROLE unisinq_user SET client_encoding TO 'utf8';
ALTER ROLE unisinq_user SET default_transaction_isolation TO 'read committed';
ALTER ROLE unisinq_user SET timezone TO 'UTC';
GRANT ALL PRIVILEGES ON DATABASE unisinq_db TO unisinq_user;
\q
```

#### Update .env
```env
DATABASE_URL=postgresql://unisinq_user:your_password@localhost:5432/unisinq_db
```

#### Test Connection
```bash
cd backend
python manage.py dbshell
# If successful, you'll see psql prompt
\q
```

---

## Optional Services

### Redis Cache (For Production)

#### Windows (Docker)
```bash
docker run -d -p 6379:6379 redis:latest
```

#### macOS
```bash
brew install redis
brew services start redis
```

#### Ubuntu
```bash
sudo apt install redis-server
sudo service redis-server start
```

#### Test Redis
```bash
python manage.py shell
```

```python
from django.core.cache import cache
cache.set('test', 'hello', 60)
print(cache.get('test'))  # Should print: hello
exit()
```

### Email Service Setup

#### Brevo (Recommended)
1. Go to https://www.brevo.com/
2. Sign up for free account
3. Go to Settings → SMTP & API
4. Copy API Key
5. Add to .env: `BREVO_API_KEY=your_key`

#### Gmail
1. Go to https://myaccount.google.com/
2. Security → App passwords (requires 2FA enabled)
3. Select Mail and Windows (or Other)
4. Copy password
5. Add to .env:
   ```env
   EMAIL_HOST_USER=your-email@gmail.com
   EMAIL_HOST_PASSWORD=xxxx xxxx xxxx xxxx
   ```

### OAuth Providers

#### Google
1. Go to https://console.cloud.google.com/
2. Create new project
3. Enable Google+ API
4. Create OAuth 2.0 credentials (Web application)
5. Add authorized redirect URIs:
   - http://localhost:8000/accounts/google/login/callback/
   - http://localhost:3000 (for frontend)
6. Copy Client ID and Secret
7. Add to .env and Django admin

#### GitHub
1. Go to https://github.com/settings/developers
2. OAuth Apps → New OAuth App
3. Add Authorization callback URL:
   - http://localhost:8000/accounts/github/login/callback/
4. Copy Client ID and Secret
5. Add to .env and Django admin

---

## Production Deployment

### Railway Deployment

#### 1. Install Railway CLI
```bash
npm i -g @railway/cli
```

#### 2. Login to Railway
```bash
railway login
```

#### 3. Create Project
```bash
railway init
# Follow prompts
```

#### 4. Configure Environment
```bash
railway variables set DEBUG=False
railway variables set SECRET_KEY=your-production-key
# Add other variables...
```

#### 5. Deploy
```bash
railway up
```

### Docker Deployment

#### Build Image
```bash
docker build -t unisinq .
```

#### Run Container
```bash
docker run -p 8000:8000 \
  -e DEBUG=False \
  -e SECRET_KEY=your-key \
  -e DATABASE_URL=postgresql://... \
  unisinq
```

#### Docker Compose
```bash
docker-compose up -d
```

---

## Troubleshooting

### Python Package Issues
```bash
# Clear pip cache
pip cache purge

# Upgrade pip
pip install --upgrade pip

# Install with specific version
pip install Django==4.2.8

# List installed packages
pip list
```

### Database Connection Error
```bash
# Test PostgreSQL connection
psql -h localhost -U unisinq_user -d unisinq_db

# Check Django database settings
python manage.py dbshell

# Run migrations
python manage.py migrate --verbosity 2
```

### Static Files Not Found
```bash
# Collect static files
python manage.py collectstatic --noinput --clear

# Check STATIC_URL and STATIC_ROOT in settings.py
python manage.py findstatic css/style.css
```

### Port Already in Use
```bash
# Windows - Find process using port 8000
netstat -ano | findstr :8000

# macOS/Linux
lsof -i :8000

# Kill process
# Windows: taskkill /PID <PID> /F
# macOS/Linux: kill -9 <PID>

# Or use different port
python manage.py runserver 8001
```

### Module Not Found
```bash
# Activate virtual environment
# Windows: venv\Scripts\activate
# macOS/Linux: source venv/bin/activate

# Verify Python location
which python

# Reinstall dependencies
pip install -r requirements.txt --force-reinstall
```

### WebSocket Connection Failed
```bash
# Install Daphne for WebSocket support
pip install daphne

# Run with Daphne
daphne -b 0.0.0.0 -p 8000 auth_project.asgi:application

# Or use runserver (includes Daphne in dev)
python manage.py runserver
```

### CORS Errors
```python
# Update .env
CORS_ALLOWED_ORIGINS=http://localhost:3000,http://localhost:5173
CSRF_TRUSTED_ORIGINS=http://localhost:3000,http://localhost:5173

# Restart server
```

---

## Development Tools

### Recommended IDE/Editor
- **VS Code** (lightweight, extensions for Python/JavaScript)
- **PyCharm Community** (Python IDE)
- **WebStorm** (JavaScript IDE)

### VS Code Extensions
```
Python
Pylance
Django
JavaScript (ES6) code snippets
REST Client
Thunder Client (Postman alternative)
Docker
```

### Debug with VS Code
Create `.vscode/launch.json`:
```json
{
  "version": "0.2.0",
  "configurations": [
    {
      "name": "Django",
      "type": "python",
      "request": "launch",
      "program": "${workspaceFolder}/backend/manage.py",
      "args": ["runserver"],
      "django": true
    }
  ]
}
```

### API Testing Tools
- **Postman**: https://www.postman.com/downloads/
- **Insomnia**: https://insomnia.rest/
- **Thunder Client**: VS Code extension
- **curl**: Command line (built-in)

### Database Tools
- **DBeaver**: GUI database client
- **DB Browser for SQLite**: Lightweight SQLite tool
- **pgAdmin**: PostgreSQL management
- **psql**: Command line PostgreSQL

---

## Verification Checklist

After setup, verify everything works:

- [ ] Backend server runs: `python manage.py runserver` → http://localhost:8000
- [ ] Frontend server runs: `npm run dev` → http://localhost:5173
- [ ] Can access admin panel: http://localhost:8000/admin
- [ ] Can access API: http://localhost:8000/api/projects/
- [ ] Database migrations applied: `python manage.py showmigrations --list`
- [ ] Static files collected: `python manage.py collectstatic --noinput`
- [ ] Email configured: Check .env for email backend
- [ ] No missing environment variables: All required vars set

---

## Quick Start Commands

```bash
# Backend
cd backend
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
pip install -r requirements.txt
cp .env.example .env  # Edit with your settings
python manage.py migrate
python manage.py createsuperuser
python manage.py runserver

# Frontend (new terminal)
cd frontend
npm install
npm run dev

# Now open:
# Frontend: http://localhost:5173
# Backend: http://localhost:8000
# Admin: http://localhost:8000/admin
```

---

**Last Updated**: February 16, 2026
**Version**: 1.0
