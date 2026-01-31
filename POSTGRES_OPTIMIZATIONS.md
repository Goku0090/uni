# PostgreSQL Optimization & Configuration Guide

## Current Status
✓ PostgreSQL configured in `settings.py` (lines 99-139)
✓ `psycopg2-binary` in `requirements.txt` (line 7)
✓ `dj-database-url` in `requirements.txt` (line 8)
✓ Render deployment configured in `render.yaml`

---

## Enhanced Database Configuration

### Update settings.py with Production Optimizations

Add this to `auth_project/settings.py` after line 139:

```python
# ===== ENHANCED POSTGRESQL CONFIGURATION =====

# Connection Pooling Configuration
if DATABASE_URL and not DEBUG:
    # Production: Enable connection pooling and health checks
    DATABASES['default']['CONN_MAX_AGE'] = 600
    DATABASES['default']['OPTIONS'] = {
        'connect_timeout': 10,
        'options': '-c default_transaction_isolation=read_committed',
    }
    # Enable prepared statements for security
    DATABASES['default']['ATOMIC_REQUESTS'] = True

# Database performance settings for large datasets
DB_TIMEOUT = os.getenv('DB_TIMEOUT', '30')
DATABASES['default']['CONN_HEALTH_CHECKS'] = True
DATABASES['default']['AUTOCOMMIT'] = True

# Query logging for debugging (development only)
if DEBUG:
    LOGGING['loggers']['django.db.backends'] = {
        'handlers': ['console'],
        'level': 'DEBUG',
        'propagate': False,
    }

print(f"[DATABASE] Configured: {DATABASES['default']['ENGINE']}")
print(f"[DATABASE] Database: {DATABASES['default'].get('NAME', 'sqlite3')}")
if 'HOST' in DATABASES['default']:
    print(f"[DATABASE] Host: {DATABASES['default'].get('HOST', 'N/A')}")
```

---

## Migration Strategy

### Create & Run Migrations

```bash
# Create initial migrations
python manage.py makemigrations

# Plan migrations (view without executing)
python manage.py migrate --plan

# Run migrations
python manage.py migrate

# Check migration status
python manage.py showmigrations

# Reverse a migration if needed
python manage.py migrate accounts 0002  # Go back to specific version
```

### Migration Order (Important)

1. User & Auth migrations (Django built-in)
2. StudentProfile migrations
3. Connection/Follow migrations
4. Project & Team migrations
5. Message & ChatRoom migrations
6. Activity & Notification migrations

### Rollback Strategy

```bash
# List all migrations
python manage.py showmigrations

# Rollback to specific migration
python manage.py migrate accounts 0001

# Create rollback migration
python manage.py makemigrations accounts --empty --name undo_feature
```

---

## Database Indexes

### Add to `accounts/models.py` for Performance

```python
class StudentProfile(models.Model):
    # ... existing fields ...
    
    class Meta:
        indexes = [
            models.Index(fields=['user']),
            models.Index(fields=['college']),
            models.Index(fields=['interests']),
            models.Index(fields=['created_at']),
        ]

class Project(models.Model):
    # ... existing fields ...
    
    class Meta:
        indexes = [
            models.Index(fields=['user']),
            models.Index(fields=['created_at']),
            models.Index(fields=['category']),
            models.Index(fields=['-created_at']),  # For ordering
        ]

class Connection(models.Model):
    # ... existing fields ...
    
    class Meta:
        indexes = [
            models.Index(fields=['sender', 'status']),
            models.Index(fields=['receiver', 'status']),
            models.Index(fields=['created_at']),
        ]

class Message(models.Model):
    # ... existing fields ...
    
    class Meta:
        indexes = [
            models.Index(fields=['chat_room', 'created_at']),
            models.Index(fields=['sender', 'receiver']),
            models.Index(fields=['created_at']),
        ]

class Activity(models.Model):
    # ... existing fields ...
    
    class Meta:
        indexes = [
            models.Index(fields=['user', '-created_at']),
            models.Index(fields=['activity_type']),
            models.Index(fields=['is_public']),
        ]
```

### Create Index Migration

```bash
python manage.py makemigrations accounts --name add_database_indexes
python manage.py migrate
```

---

## Query Optimization

### Common N+1 Query Problems & Solutions

**Before (N+1):**
```python
# In find_collaborators view (line 1321)
for profile in suggestions:
    profile.user  # This causes N additional queries!
```

**After (Optimized):**
```python
base_profiles = StudentProfile.objects.filter(
    # ...
).select_related('user')  # Single query

# Or for many-to-many:
projects = Project.objects.filter(
    # ...
).select_related('user').prefetch_related('comments')
```

### Database Query Cache

Add to settings.py:
```python
# Cache Database Queries
CACHES = {
    'default': {
        'BACKEND': 'django.core.cache.backends.redis.RedisCache',
        'LOCATION': os.getenv('REDIS_URL', 'redis://127.0.0.1:6379/1'),
        'OPTIONS': {
            'CLIENT_CLASS': 'django_redis.client.DefaultClient',
            'CONNECTION_POOL_KWARGS': {'max_connections': 50, 'retry_on_timeout': True},
            'SOCKET_CONNECT_TIMEOUT': 5,
            'SOCKET_TIMEOUT': 5,
            'COMPRESSOR': 'django_redis.compressors.zlib.ZlibCompressor',
            'IGNORE_EXCEPTIONS': True,  # Graceful fallback
        }
    }
}
```

### Cache Commonly Accessed Data

```python
# In views.py
from django.views.decorators.cache import cache_page
from django.core.cache import cache

@cache_page(60 * 5)  # Cache for 5 minutes
@login_required
def find_collaborators(request):
    """Cached collaborator finder"""
    cache_key = f"collaborators_{request.user.id}"
    
    cached = cache.get(cache_key)
    if cached:
        return cached
    
    # ... fetch results ...
    
    cache.set(cache_key, results, 300)  # Cache for 5 minutes
    return results
```

---

## Monitoring & Debugging

### Enable Query Logging

Create `accounts/middleware/logging_middleware.py`:
```python
import logging
from django.utils.deprecation import MiddlewareMixin

logger = logging.getLogger('django.db.backends')

class QueryLoggingMiddleware(MiddlewareMixin):
    def process_response(self, request, response):
        if hasattr(request, 'META'):
            from django.db import connection
            queries = len(connection.queries)
            if queries > 10:
                logger.warning(f"High query count: {queries} for {request.path}")
        return response
```

Add to MIDDLEWARE:
```python
MIDDLEWARE = [
    # ... existing middleware ...
    'accounts.middleware.logging_middleware.QueryLoggingMiddleware',
]
```

### Django Debug Toolbar

Already in requirements.txt! Enable in development:

```python
# Add to settings.py
if DEBUG:
    INSTALLED_APPS += ['debug_toolbar']
    MIDDLEWARE += ['debug_toolbar.middleware.DebugToolbarMiddleware']
    INTERNAL_IPS = ['127.0.0.1']
```

Add to urls.py:
```python
if DEBUG:
    import debug_toolbar
    urlpatterns += [path('__debug__/', include(debug_toolbar.urls))]
```

---

## Backup & Restore

### Automated Backups (Render)

Render handles this automatically! Access in dashboard:
- Backups → Create Backup
- Restore from backup point

### Local Backup

```bash
# Full database dump
pg_dump -U unisync_user unisync_db > backup_$(date +%Y%m%d).sql

# Compressed backup
pg_dump -U unisync_user unisync_db | gzip > backup.sql.gz

# Specific table only
pg_dump -U unisync_user unisync_db -t accounts_project > projects_backup.sql
```

### Restore from Backup

```bash
# Restore full database
psql -U unisync_user unisync_db < backup.sql

# Restore from compressed
gunzip < backup.sql.gz | psql -U unisync_user unisync_db

# Restore specific table
psql -U unisync_user unisync_db < projects_backup.sql
```

---

## Data Cleanup

### Remove Old OTP Codes

```python
# Create management command: accounts/management/commands/cleanup_otps.py
from django.core.management.base import BaseCommand
from django.utils import timezone
from accounts.models import OTP

class Command(BaseCommand):
    help = 'Remove expired OTP codes'
    
    def handle(self, *args, **options):
        # Delete OTPs older than 1 day
        one_day_ago = timezone.now() - timezone.timedelta(days=1)
        deleted, _ = OTP.objects.filter(
            created_at__lt=one_day_ago,
            is_used=True
        ).delete()
        
        self.stdout.write(self.style.SUCCESS(f'Deleted {deleted} old OTP codes'))
```

Run:
```bash
python manage.py cleanup_otps
```

### Archive Old Activities

```python
# accounts/management/commands/archive_activities.py
from django.core.management.base import BaseCommand
from accounts.models import Activity
import datetime

class Command(BaseCommand):
    help = 'Archive activities older than 90 days'
    
    def handle(self, *args, **options):
        threshold = datetime.datetime.now() - datetime.timedelta(days=90)
        archived, _ = Activity.objects.filter(
            created_at__lt=threshold
        ).delete()
        
        self.stdout.write(self.style.SUCCESS(f'Archived {archived} old activities'))
```

---

## Monitoring in Production

### PostgreSQL Status Command

```sql
-- Check active connections
SELECT count(*) as active_connections FROM pg_stat_activity;

-- Check table sizes
SELECT schemaname, tablename, 
       pg_size_pretty(pg_total_relation_size(schemaname||'.'||tablename)) 
FROM pg_tables 
WHERE schemaname = 'public' 
ORDER BY pg_total_relation_size(schemaname||'.'||tablename) DESC;

-- Check index usage
SELECT schemaname, tablename, indexname, idx_scan 
FROM pg_stat_user_indexes 
ORDER BY idx_scan DESC;

-- Long-running queries
SELECT pid, usename, application_name, query, query_start, state
FROM pg_stat_activity 
WHERE state = 'active' AND query NOT LIKE '%pg_stat%'
ORDER BY query_start;
```

---

## Performance Tuning

### For Render Free Plan (Limited Resources)

```python
# Reduce connection pool
DATABASES['default']['CONN_MAX_AGE'] = 300  # 5 minutes

# Enable persistent connections
DATABASES['default']['AUTOCOMMIT'] = False

# Limit concurrent connections
import os
max_connections = int(os.getenv('DB_MAX_CONNECTIONS', '10'))
```

### For Production/Paid Plans

```python
# Better connection pooling
DATABASES['default']['CONN_MAX_AGE'] = 600
DATABASES['default']['CONN_HEALTH_CHECKS'] = True
DATABASES['default']['OPTIONS'] = {
    'keepalives': 1,
    'keepalives_idle': 30,
    'keepalives_interval': 10,
    'keepalives_count': 5,
}
```

---

## Troubleshooting

### "FATAL: remaining connection slots reserved for non-replication superuser connections"

**Cause:** Too many connections for free plan
**Solution:**
```python
# Reduce concurrent connections in settings
DATABASES['default']['CONN_MAX_AGE'] = 300
```

### "Disk quota exceeded"

**Cause:** Free plan limit (10GB)
**Solution:**
```bash
# Check database size
SELECT pg_size_pretty(pg_database_size('unisync_db'));

# Delete old data
DELETE FROM accounts_activity WHERE created_at < NOW() - INTERVAL '90 days';
DELETE FROM accounts_otp WHERE is_used = true AND created_at < NOW() - INTERVAL '7 days';
```

### "Connection timeout"

**Cause:** Database server overload
**Solution:** Add connection timeout to settings
```python
DATABASES['default']['CONN_MAX_AGE'] = 600
DATABASES['default']['OPTIONS'] = {
    'connect_timeout': 10,
    'statement_timeout': 30000,  # 30 seconds
}
```

---

## Checklist for Render Deployment

- [ ] `render.yaml` in repository root
- [ ] All environment variables set in Render dashboard
- [ ] `requirements.txt` includes `psycopg2-binary` and `dj-database-url`
- [ ] Migrations created: `python manage.py makemigrations`
- [ ] Settings configured for Render: Line 99-139 in settings.py
- [ ] Build script runs migrations: `build.sh`
- [ ] Database indexes added to models
- [ ] Query optimization applied to high-traffic views
- [ ] Cache configuration ready (Redis URL set)
- [ ] Monitoring/logging configured
- [ ] Backup strategy documented
- [ ] SSL mode set to `require` for production

---

## Performance Targets

| Metric | Target | Status |
|--------|--------|--------|
| Query response time | <200ms | ⏳ |
| Page load time | <2s | ⏳ |
| Database connections | <10 (free) | Configure |
| Cache hit rate | >80% | Configure |
| Backup frequency | Daily | Auto |

---

## Quick Commands Reference

```bash
# Setup
python manage.py migrate
python manage.py createsuperuser

# Optimization
python manage.py makemigrations --name add_database_indexes
python manage.py migrate

# Monitoring
python manage.py dbshell
python manage.py querycount

# Cleanup
python manage.py cleanup_otps
python manage.py cleanup_old_activities

# Testing
python manage.py test accounts
pytest --cov=accounts
```
