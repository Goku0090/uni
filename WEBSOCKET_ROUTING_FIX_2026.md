# WebSocket Routing Fix - 404 Errors Resolution
**Date:** February 6, 2026  
**Issue:** WebSocket routes returning 404 errors

---

## Problem Statement

Two WebSocket routes are returning 404 errors:
```
[WARNING] Not Found: /ws/project/2/
[WARNING] Not Found: /ws/activity-feed/
```

### Root Cause Analysis

The WebSocket routing is **properly configured** in:
- ✅ `accounts/routing.py` - WebSocket URL patterns defined
- ✅ `auth_project/asgi.py` - ASGI application configured
- ✅ `accounts/consumers.py` - Consumer classes implemented

**But the Django HTTP routing is intercepting WebSocket requests before they reach the ASGI layer.**

---

## Current Configuration

### ASGI Configuration (auth_project/asgi.py)
```python
from channels.routing import ProtocolTypeRouter, URLRouter
from channels.auth import AuthMiddlewareStack

application = ProtocolTypeRouter({
    "http": get_asgi_application(),
    "websocket": AuthMiddlewareStack(
        URLRouter(
            accounts.routing.websocket_urlpatterns
        )
    ),
})
```
✅ **Status:** Correct

### WebSocket Routing (accounts/routing.py)
```python
websocket_urlpatterns = [
    re_path(r'ws/project/(?P<project_id>\w+)/$', consumers.ProjectUpdateConsumer.as_asgi()),
    re_path(r'ws/activity-feed/$', consumers.ActivityFeedConsumer.as_asgi()),
    re_path(r'ws/notifications/$', consumers.NotificationConsumer.as_asgi()),
]
```
✅ **Status:** Correct

### Problem: Django HTTP Routes

**File:** `auth_project/urls.py`

The issue is that Django's HTTP router doesn't know about WebSocket routes, and the application might be using a development server (Django's runserver) instead of the proper ASGI server.

---

## Solutions

### Solution 1: Use Proper ASGI Server (RECOMMENDED FOR PRODUCTION)

#### Install daphne
```bash
pip install daphne
```

#### Update Procfile
```
web: daphne -b 0.0.0.0 -p 8000 auth_project.asgi:application
```

#### Update requirements.txt
```
daphne==4.0.0
```

#### For Local Development
Instead of:
```bash
python manage.py runserver
```

Use:
```bash
daphne -b 0.0.0.0 -p 8000 auth_project.asgi:application
```

**Why:** Django's `runserver` only handles HTTP. Daphne properly routes WebSocket (ws://) requests to the ASGI layer.

---

### Solution 2: Use Django Channels Development Server

#### Alternative command
```bash
# For development with auto-reload
DJANGO_ALLOW_ASYNC_UNSAFE=true python manage.py runserver
```

But this still doesn't properly handle WebSocket. Better to use Daphne.

---

### Solution 3: Update ASGI Configuration (Additional Safeguard)

Even with Daphne, ensure your ASGI has proper error handling:

**File:** `auth_project/asgi.py`

```python
"""
ASGI config for auth_project project.
Handles both HTTP and WebSocket connections.
"""

import os
from channels.auth import AuthMiddlewareStack
from channels.routing import ProtocolTypeRouter, URLRouter
from channels.exceptions import InvalidChannelLayerError
from django.core.asgi import get_asgi_application
import accounts.routing
import logging

logger = logging.getLogger(__name__)

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'auth_project.settings')

# Get Django ASGI application
django_asgi_app = get_asgi_application()

application = ProtocolTypeRouter({
    "http": django_asgi_app,
    
    "websocket": AuthMiddlewareStack(
        URLRouter(
            accounts.routing.websocket_urlpatterns
        )
    ),
    
    # Support for lifespan protocol
    "lifespan": lambda scope: None,
})

logger.info("ASGI application initialized with WebSocket support")
```

---

## Testing WebSocket Routes

### Test 1: Check ASGI is Running Correctly
```bash
curl -i http://localhost:8000/api/
# Should return 200 OK (HTTP works)

wscat -c ws://localhost:8000/ws/project/1/
# Should connect successfully (WebSocket works)
```

### Test 2: Browser Console Test
```javascript
// Open browser console on a project detail page
let socket = new WebSocket("ws://localhost:8000/ws/project/2/");

socket.onopen = function(e) {
    console.log("✅ WebSocket connected!");
    console.log(e);
};

socket.onmessage = function(event) {
    console.log("📬 Message received:", event.data);
};

socket.onerror = function(error) {
    console.error("❌ WebSocket error:", error);
};

socket.onclose = function(e) {
    console.log("❌ WebSocket closed:", e.code);
};
```

### Test 3: Send Test Message
```javascript
socket.send(JSON.stringify({
    'type': 'status.update',
    'status': 'active'
}));
```

---

## Deployment Checklist

### For Render.com (Production)

**File:** `render.yaml`

```yaml
services:
  - type: web
    name: unisync
    env: python
    buildCommand: pip install -r requirements.txt && python manage.py migrate
    startCommand: daphne -b 0.0.0.0 -p 8000 auth_project.asgi:application
    
    envVars:
      - key: DJANGO_SETTINGS_MODULE
        value: auth_project.settings
      - key: DATABASE_URL
        fromDatabase:
          name: unisync_db
          property: connectionString
      - key: DISABLE_COLLECTSTATIC
        value: 'false'
    
    # Enable WebSocket support
    healthCheckPath: /api/
    preDeployCommand: python manage.py migrate
```

### For Railway (Production)

**File:** `Procfile`

```
web: daphne -b 0.0.0.0 -p $PORT auth_project.asgi:application
```

### Settings Update for Production

**File:** `auth_project/settings.py` (add to end)

```python
# ============================================================================
# ASGI & WebSocket Configuration
# ============================================================================

# Enable WebSocket support
ASGI_APPLICATION = 'auth_project.asgi.application'

# If using separate ASGI server
if not DEBUG:
    # Production WebSocket settings
    CHANNEL_LAYERS = {
        'default': {
            'BACKEND': 'channels_redis.core.RedisChannelLayer',
            'CONFIG': {
                "hosts": [('redis://localhost', 6379)],
                "capacity": 1500,
                "expiry": 10,
            },
        },
    }
    logger.info("[SUCCESS] WebSocket: Using Redis channel layer for production")
else:
    # Development in-memory
    CHANNEL_LAYERS = {
        'default': {
            'BACKEND': 'channels.layers.InMemoryChannelLayer'
        }
    }
    logger.info("[INFO] WebSocket: Using in-memory channel layer for development")
```

---

## Step-by-Step Fix Implementation

### Step 1: Install Daphne
```bash
pip install daphne==4.0.0
```

### Step 2: Update requirements.txt
```bash
# Add to requirements.txt
daphne==4.0.0
```

Commit:
```bash
git add requirements.txt
git commit -m "Add daphne for ASGI server support"
```

### Step 3: Update Local Development Script

**Create:** `run_dev.sh` (Linux/Mac)
```bash
#!/bin/bash
export DJANGO_SETTINGS_MODULE=auth_project.settings
export DJANGO_ALLOW_ASYNC_UNSAFE=true
daphne -b 127.0.0.1 -p 8000 auth_project.asgi:application
```

**Create:** `run_dev.bat` (Windows)
```batch
@echo off
set DJANGO_SETTINGS_MODULE=auth_project.settings
set DJANGO_ALLOW_ASYNC_UNSAFE=true
python -m daphne -b 127.0.0.1 -p 8000 auth_project.asgi:application
```

### Step 4: Update Procfile for Render
```
web: daphne -b 0.0.0.0 -p 8000 auth_project.asgi:application
```

### Step 5: Test Locally
```bash
# Terminal 1: Start Redis (if using production settings)
# redis-server

# Terminal 2: Start Daphne
./run_dev.sh  # Linux/Mac
# or
run_dev.bat  # Windows

# Terminal 3: Test in browser
# Open http://localhost:8000
# Check browser console for WebSocket connections
```

### Step 6: Deploy to Render
```bash
git add Procfile requirements.txt
git commit -m "Configure ASGI server for WebSocket support"
git push origin main
```

---

## Verify WebSocket Connections

### Check in Browser DevTools

1. Open any project detail page
2. Open **DevTools** (F12)
3. Go to **Network** tab
4. Filter by **WS** (WebSocket)
5. Should see connections like:
   - `ws://localhost:8000/ws/project/2/` ← **Status: 101**
   - `ws://localhost:8000/ws/notifications/` ← **Status: 101**

**Status 101** = Switching Protocols (WebSocket established)  
**Status 404** = Route not found (broken routing)

### Check Console for Messages

```javascript
// If working correctly:
console.log("📡 Project updates:", {
  type: 'project.initial_data',
  data: { id: 2, title: '...', ... }
});

console.log("💬 Member joined:", {
  type: 'project.member_added',
  username: 'john_doe'
});
```

---

## Common WebSocket 404 Issues & Fixes

### Issue 1: Using Django Runserver
**Problem:** `python manage.py runserver` doesn't handle WebSocket
**Fix:** Use Daphne or channels development server

### Issue 2: Wrong URL Pattern
**Problem:** WebSocket URL doesn't match routing pattern
**Fix:** Verify regex in `accounts/routing.py`
```python
# ✓ Correct: Matches ws://localhost:8000/ws/project/2/
re_path(r'ws/project/(?P<project_id>\w+)/$', consumers.ProjectUpdateConsumer.as_asgi())

# ✗ Wrong: Missing ^ and $
re_path(r'ws/project/(?P<project_id>\w+)/', consumers.ProjectUpdateConsumer.as_asgi())
```

### Issue 3: ASGI Not Configured
**Problem:** ASGI file missing or broken
**Fix:** Verify `asgi.py` has ProtocolTypeRouter configured

### Issue 4: Missing Channel Layers
**Problem:** Can't broadcast to groups
**Fix:** Configure CHANNEL_LAYERS in settings.py

### Issue 5: Redis Not Running
**Problem:** Production deployments fail
**Fix:** Ensure Redis is running and configured
```python
CHANNEL_LAYERS = {
    'default': {
        'BACKEND': 'channels_redis.core.RedisChannelLayer',
        'CONFIG': {
            "hosts": [('127.0.0.1', 6379)],
        },
    },
}
```

---

## Development vs Production Setup

### Development (Local)

```bash
# Install
pip install daphne channels channels-redis redis

# Run
daphne -b 127.0.0.1 -p 8000 auth_project.asgi:application

# In settings.py
CHANNEL_LAYERS = {
    'default': {
        'BACKEND': 'channels.layers.InMemoryChannelLayer'
    }
}
```

### Production (Render/Railway)

```bash
# Install (in requirements.txt)
daphne==4.0.0
channels==4.0.0
channels-redis==4.1.0

# Procfile
web: daphne -b 0.0.0.0 -p 8000 auth_project.asgi:application

# In settings.py
CHANNEL_LAYERS = {
    'default': {
        'BACKEND': 'channels_redis.core.RedisChannelLayer',
        'CONFIG': {
            "hosts": [os.getenv('REDIS_URL', 'redis://localhost:6379')],
        },
    },
}
```

---

## Monitoring WebSocket Health

### Add Health Check Endpoint

**File:** `accounts/views.py`

```python
@csrf_exempt
@require_http_methods(['GET'])
def health_check(request):
    """Health check endpoint for monitoring"""
    return JsonResponse({
        'status': 'ok',
        'service': 'unisync',
        'websocket': 'enabled',
        'timestamp': timezone.now().isoformat()
    })
```

**File:** `accounts/urls.py`

```python
path('health/', views.health_check, name='health_check'),
```

### Test Health Check
```bash
curl http://localhost:8000/api/health/
# Response:
# {
#   "status": "ok",
#   "service": "unisync",
#   "websocket": "enabled",
#   "timestamp": "2026-02-06T10:30:00Z"
# }
```

---

## Summary

### The Issue
Django's HTTP server (runserver) doesn't route WebSocket requests to the ASGI layer.

### The Solution
Use **Daphne** - an ASGI server that properly handles WebSocket connections.

### Implementation Steps
1. ✅ Install: `pip install daphne`
2. ✅ Update: `requirements.txt`
3. ✅ Update: `Procfile` → `daphne ... auth_project.asgi:application`
4. ✅ Run: `daphne -b 0.0.0.0 -p 8000 auth_project.asgi:application`
5. ✅ Test: Open project page, check DevTools Network tab for WS connections

### Expected Results
```
✅ ws://localhost:8000/ws/project/2/        → Status 101
✅ ws://localhost:8000/ws/activity-feed/    → Status 101
✅ ws://localhost:8000/ws/notifications/    → Status 101
```

---

**Status:** Ready to Implement  
**Difficulty:** Low (just change ASGI server)  
**Deployment Impact:** None (same port, same routes, just different server)
