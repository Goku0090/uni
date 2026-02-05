# UniSync Technical Stack & Dependencies Guide

---

## Overview

UniSync is a full-featured Django web application built with modern Python and JavaScript. It includes real-time messaging, social features, project management, and integrations with external services.

---

## Technology Stack

### Backend Framework
- **Django 4.2.8** - Web framework
- **Django REST Framework 3.14.0** - API development
- **Python 3.8+** - Programming language

### Database
- **PostgreSQL** (primary) - Production database
- **SQLite3** (fallback) - Development/testing
- **psycopg2-binary 2.9.9** - PostgreSQL adapter
- **dj-database-url 2.1.0** - Database URL parser

### Authentication & Authorization
- **django-allauth 0.61.1** - Social authentication (Google, GitHub)
- **Django built-in** - Session management, password hashing
- **requests-oauthlib 1.3.1** - OAuth handling

### Messaging & Real-Time
- **Channels 4.0.0** - WebSocket support for real-time features
- **Channels Redis 4.1.0** - Message broker for channels
- **Redis 5.0.1** - Caching and session storage
- **django-redis 5.4.0** - Redis integration

### Email Service Integration
- **Custom Brevo Backend** - Primary email service
- **Custom ZeptoMail Backend** - Fallback email service
- **Gmail SMTP** - Fallback email option
- **zeptomail 1.0.0** - ZeptoMail SDK

### File Storage & Processing
- **Pillow 10.1.0** - Image processing
- **boto3 1.34.34** - AWS S3 integration
- **django-storages 1.14.2** - Cloud storage backend
- **openpyxl 3.1.2** - Excel file processing
- **pandas 2.1.4** - Data manipulation

### API & External Services
- **requests 2.31.0** - HTTP client
- **rapidapi 1.0.0** - RapidAPI SDK for college search
- **drf-spectacular 0.26.5** - OpenAPI documentation

### NLP & Data Processing
- **NLTK 3.8.1** - Natural language processing
- **pandas 2.1.4** - Data analysis
- **openpyxl 3.1.2** - Excel handling

### Production Deployment
- **Gunicorn 21.2.0** - WSGI server
- **WhiteNoise 6.6.0** - Static file serving
- **Sentry SDK 1.38.0** - Error tracking

### Development Tools
- **Django Debug Toolbar 4.2.0** - Debugging
- **Django Extensions 3.2.3** - Command extensions
- **Black 23.12.1** - Code formatter
- **Flake8 6.1.0** - Code linter
- **isort 5.13.2** - Import sorter
- **mypy 1.7.1** - Type checker

### Testing
- **pytest 7.4.3** - Testing framework
- **pytest-django 4.7.0** - Django integration
- **Selenium 4.16.0** - Browser automation

### Task Processing
- **Celery 5.3.4** - Background task queue
- **Redis** - Message broker

### Frontend
- **Bootstrap 5** - CSS framework
- **jQuery** - JavaScript library (legacy)
- **Vanilla JavaScript** - Custom scripts
- **crispy-bootstrap5 0.7** - Form rendering

### Additional Libraries
- **django-cors-headers 4.3.1** - CORS support
- **django-filter 23.5** - Filtering
- **django-crispy-forms 2.1** - Form handling
- **python-dotenv 1.0.0** - Environment variables

---

## Dependency Graph

### Core Dependencies
```
Django 4.2.8
├── django-allauth 0.61.1
│   └── requests 2.31.0
│       └── requests-oauthlib 1.3.1
├── djangorestframework 3.14.0
│   └── drf-spectacular 0.26.5
├── channels 4.0.0
│   ├── channels-redis 4.1.0
│   └── redis 5.0.1
└── python-dotenv 1.0.0
```

### Database Dependencies
```
psycopg2-binary 2.9.9 (PostgreSQL)
├── libpq (external dependency)
└── dj-database-url 2.1.0
```

### Email Dependencies
```
Custom Email Backends
├── requests 2.31.0 (for Brevo API)
└── zeptomail 1.0.0 (for ZeptoMail)
```

### Storage Dependencies
```
boto3 1.34.34 (AWS S3)
├── botocore (included)
└── django-storages 1.14.2
    └── Pillow 10.1.0 (Image handling)
```

### Data Processing
```
pandas 2.1.4
├── openpyxl 3.1.2 (Excel)
├── numpy (dependency)
└── nltk 3.8.1 (NLP)
```

---

## Installation & Setup

### Prerequisites
- Python 3.8+ installed
- pip package manager
- PostgreSQL 12+ (for production)
- Redis 6+ (for caching and channels)
- Git for version control

### Installation Steps

```bash
# 1. Clone repository
git clone https://github.com/Goku0090/uni.git
cd auth_project

# 2. Create virtual environment
python -m venv venv

# 3. Activate virtual environment
# On Windows:
venv\Scripts\activate
# On macOS/Linux:
source venv/bin/activate

# 4. Install dependencies
pip install -r requirements.txt

# 5. Create .env file
cp .env.template .env
# Edit .env with your configuration

# 6. Run migrations
python manage.py migrate

# 7. Create superuser (optional)
python manage.py createsuperuser

# 8. Collect static files (production)
python manage.py collectstatic --noinput

# 9. Run development server
python manage.py runserver

# 10. Access application
# Open http://localhost:8000 in browser
```

---

## Environment Variables

### Required Variables

```bash
# Django Settings
DEBUG=True/False
SECRET_KEY=your_secret_key
ALLOWED_HOSTS=localhost,127.0.0.1,yourdomain.com

# Database
DATABASE_URL=postgresql://user:password@localhost:5432/unisync_db
# OR
DB_ENGINE=django.db.backends.postgresql
DB_NAME=unisync_db
DB_USER=unisync_user
DB_PASSWORD=your_password
DB_HOST=localhost
DB_PORT=5432

# Email Configuration
BREVO_API_KEY=your_brevo_api_key
ZEPTO_MAIL_API_KEY=your_zepto_api_key
ZEPTO_MAIL_TOKEN=your_zepto_token
EMAIL_HOST_USER=your_email@gmail.com
EMAIL_HOST_PASSWORD=your_app_password
DEFAULT_FROM_EMAIL=noreply@unisync.app

# Social Authentication
GOOGLE_CLIENT_ID=your_google_client_id
GOOGLE_CLIENT_SECRET=your_google_client_secret
GITHUB_CLIENT_ID=your_github_client_id
GITHUB_CLIENT_SECRET=your_github_client_secret

# External APIs
RAPIDAPI_KEY=your_rapidapi_key
RAPIDAPI_HOST=universities-list.p.rapidapi.com

# Redis (for caching and channels)
REDIS_URL=redis://localhost:6379/0

# AWS S3 (optional, for cloud storage)
AWS_ACCESS_KEY_ID=your_access_key
AWS_SECRET_ACCESS_KEY=your_secret_key
AWS_STORAGE_BUCKET_NAME=your_bucket_name
AWS_S3_REGION_NAME=us-east-1

# Sentry (error tracking, optional)
SENTRY_DSN=your_sentry_dsn

# Security (Production)
SECURE_SSL_REDIRECT=True
SESSION_COOKIE_SECURE=True
CSRF_COOKIE_SECURE=True
```

---

## Key Package Details

### Django Allauth (0.61.1)
**Purpose:** Social authentication and account management

**Key Features:**
- Email-based authentication
- Google OAuth 2.0
- GitHub OAuth 2.0
- Email verification
- Password reset flows

**Configuration:**
```python
INSTALLED_APPS = [
    'allauth',
    'allauth.account',
    'allauth.socialaccount',
    'allauth.socialaccount.providers.google',
    'allauth.socialaccount.providers.github',
]
```

### Django REST Framework (3.14.0)
**Purpose:** Building REST APIs

**Key Features:**
- Serialization/deserialization
- Authentication and permissions
- Pagination
- Filtering and search
- API documentation

**Used for:**
- Messaging API endpoints
- Comment API endpoints
- Project API endpoints
- User profile API endpoints

### Channels (4.0.0)
**Purpose:** WebSocket support for real-time features

**Key Features:**
- WebSocket support
- Channel layers
- Async consumer support
- Real-time messaging

**Requires:**
- Redis backend (via channels-redis)
- ASGI application configuration

### Pillow (10.1.0)
**Purpose:** Image processing

**Operations:**
- Profile photo upload validation
- Image resizing
- Format conversion
- EXIF data handling

**Supported Formats:** JPEG, PNG, GIF, WebP

### Celery (5.3.4)
**Purpose:** Background task processing

**Use Cases:**
- Sending emails asynchronously
- Processing file uploads
- Generating reports
- Scheduled cleanup tasks

**Requires:**
- Redis or RabbitMQ as message broker

### Redis (5.0.1)
**Purpose:** Caching and session storage

**Use Cases:**
- Session management
- Cache layer for database queries
- Message broker for Celery
- Channel layer for WebSockets

---

## Development Tools Setup

### Code Formatting & Linting

```bash
# Format code with Black
black .

# Sort imports
isort .

# Check code style
flake8 .

# Type checking
mypy accounts/

# Run all checks
black --check .
isort --check-only .
flake8 .
mypy accounts/
```

### Testing

```bash
# Run all tests
pytest

# Run specific test file
pytest accounts/tests.py

# Run with coverage
pytest --cov=accounts

# Run Django tests
python manage.py test accounts

# Run Selenium tests (browser automation)
pytest selenium_tests/
```

### Debugging

```bash
# Enable Django Debug Toolbar in development
DEBUG = True
INSTALLED_APPS += ['debug_toolbar']

# Access at http://localhost:8000/__debug__/
```

---

## Deployment Configuration

### Production Dependencies
- **Gunicorn** - WSGI server
- **WhiteNoise** - Static file serving
- **Sentry SDK** - Error tracking
- **django-cors-headers** - CORS headers

### Deployment Platforms

#### Render
```bash
# Requirements:
- render.yaml configuration
- DATABASE_URL environment variable
- Procfile for process definitions
```

#### Railway
```bash
# Requirements:
- railway.json configuration
- Database provisioning
- Environment variables
```

#### Docker
```dockerfile
FROM python:3.11-slim
WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY . .
CMD ["gunicorn", "auth_project.wsgi"]
```

---

## Performance Optimization

### Caching Strategy
```python
# Redis caching
CACHES = {
    'default': {
        'BACKEND': 'django_redis.cache.RedisCache',
        'LOCATION': 'redis://127.0.0.1:6379/1',
        'OPTIONS': {
            'CLIENT_CLASS': 'django_redis.client.DefaultClient',
        }
    }
}
```

### Database Optimization
- Add indexes on frequently queried fields
- Use select_related() for foreign keys
- Use prefetch_related() for reverse relations
- Implement pagination for large result sets

### Static File Optimization
- Use WhiteNoise for efficient serving
- Enable gzip compression
- Use CSS/JS minification
- Set appropriate cache headers

---

## Monitoring & Logging

### Sentry Integration
```python
import sentry_sdk
from sentry_sdk.integrations.django import DjangoIntegration

sentry_sdk.init(
    dsn=os.getenv('SENTRY_DSN'),
    integrations=[DjangoIntegration()],
    traces_sample_rate=0.1,
)
```

### Logging Configuration
```python
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'handlers': {
        'console': {'class': 'logging.StreamHandler'},
        'file': {
            'class': 'logging.handlers.RotatingFileHandler',
            'filename': 'logs/django.log',
        },
    },
}
```

---

## Security Best Practices

### Environment Variables
✅ Never commit .env file  
✅ Use `.env.template` as reference  
✅ Rotate secrets regularly  
✅ Use different keys for prod/dev/staging

### Dependencies
✅ Keep packages updated: `pip list --outdated`  
✅ Use security checklist: `python manage.py check --deploy`  
✅ Monitor CVEs: Use tools like `safety`

### Code Quality
✅ Run linters and type checkers  
✅ Use pre-commit hooks  
✅ Implement CI/CD pipeline  
✅ Regular security audits

---

## Troubleshooting

### Common Issues

**PostgreSQL Connection Error**
```bash
# Check connection parameters
python manage.py dbshell

# Install PostgreSQL client
# Windows: Download from postgresql.org
# macOS: brew install postgresql
# Linux: apt-get install postgresql-client
```

**Redis Connection Error**
```bash
# Check Redis is running
redis-cli ping

# Start Redis server
redis-server
```

**Static Files Not Loading**
```bash
# Collect static files
python manage.py collectstatic --noinput --clear

# Check STATIC_ROOT and STATIC_URL
```

**Email Not Sending**
```bash
# Check email backend configuration
python manage.py shell
from django.core.mail import send_mail
send_mail('Test', 'This is a test', 'from@example.com', ['to@example.com'])
```

---

## Version Compatibility

| Package | Version | Status |
|---------|---------|--------|
| Django | 4.2.8 | LTS, Stable |
| Python | 3.8+ | Supported |
| PostgreSQL | 12+ | Compatible |
| Redis | 6+ | Compatible |
| Node | 14+ | For frontend tools |

---

## Resources

- Django Documentation: https://docs.djangoproject.com/
- Django REST Framework: https://www.django-rest-framework.org/
- Channels Documentation: https://channels.readthedocs.io/
- PostgreSQL Documentation: https://www.postgresql.org/docs/
- Redis Documentation: https://redis.io/documentation/

---

*Last Updated: February 3, 2025*
