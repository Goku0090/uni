# WebSocket 404 Error - Detailed Technical Analysis

**Issue Date:** February 6, 2026  
**Error Pattern:** 404 on `/ws/project/2/` and `/ws/activity-feed/`  
**Severity:** Medium (WebSocket functionality broken, HTTP API still works)  
**Resolution Time:** 5-15 minutes

---

## 1. Error Analysis

### What's Happening

```
[WARNING] Not Found: /ws/project/2/
[WARNING] "GET /ws/project/2/ HTTP/1.1" 404 9033

[WARNING] Not Found: /ws/activity-feed/
[WARNING] "GET /ws/activity-feed/ HTTP/1.1" 404 9045
```

### Why It's 404

The browser is **treating WebSocket requests as HTTP GET requests** instead of upgrading them to WebSocket protocol (ws://).

**Key indicator:** `"GET /ws/project/2/ HTTP/1.1"` ← HTTP, not WS

### Root Cause

**Django's development server (`python manage.py runserver`) only handles HTTP protocol.**

When a WebSocket request comes in:
```
GET /ws/project/2/ HTTP/1.1
Upgrade: websocket
Connection: Upgrade
```

Django's HTTP router tries to match this against Django URL patterns (in `urls.py`), finds nothing, and returns 404.

The ASGI layer (which handles WebSocket) is never reached.

---

## 2. Current Architecture Review

### What's Configured Correctly ✅

#### ASGI Application (`auth_project/asgi.py`)
```python
application = ProtocolTypeRouter({
    "http": get_asgi_application(),
    "websocket": AuthMiddlewareStack(
        URLRouter(
            accounts.routing.websocket_urlpatterns
        )
    ),
})
```

**Status:** ✅ Correct  
**Purpose:** Routes HTTP and WebSocket to different handlers

#### WebSocket URL Patterns (`accounts/routing.py`)
```python
websocket_urlpatterns = [
    re_path(r'ws/project/(?P<project_id>\w+)/$', consumers.ProjectUpdateConsumer.as_asgi()),
    re_path(r'ws/activity-feed/$', consumers.ActivityFeedConsumer.as_asgi()),
    re_path(r'ws/notifications/$', consumers.NotificationConsumer.as_asgi()),
]
```

**Status:** ✅ Correct  
**Purpose:** Maps WebSocket URLs to consumer classes

#### Consumer Classes (`accounts/consumers.py`)
```python
class ProjectUpdateConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        # Handle WebSocket connection
        self.project_id = self.scope['url_route']['kwargs']['project_id']
        await self.accept()
        # ...
    
    async def receive(self, text_data):
        # Handle incoming messages
        data = json.loads(text_data)
        # ...
```

**Status:** ✅ Correct  
**Purpose:** Handles WebSocket lifecycle (connect, receive, disconnect)

### What's Missing ❌

**An ASGI-compatible server to handle protocol routing**

The application is configured to use ASGI, but it's being run via:
```bash
python manage.py runserver  # ← HTTP only!
```

Instead of:
```bash
daphne -b 127.0.0.1 -p 8000 auth_project.asgi:application  # ← HTTP + WebSocket
```

---

## 3. Server Comparison

### Django Development Server
```
python manage.py runserver
├─ Handles: HTTP only
├─ Protocol: HTTP/1.1
├─ WSGI: ✅ Yes
├─ ASGI: ❌ No
├─ WebSocket: ❌ Not supported
└─ Use case: HTTP development only
```

### Daphne ASGI Server
```
daphne -b 127.0.0.1 -p 8000 auth_project.asgi:application
├─ Handles: HTTP + WebSocket (HTTP/1.1 and WS)
├─ Protocol: HTTP/1.1, WebSocket, HTTP/2
├─ WSGI: ❌ No (ASGI instead)
├─ ASGI: ✅ Yes
├─ WebSocket: ✅ Yes
└─ Use case: Full protocol support (dev + prod)
```

### Gunicorn + Uvicorn
```
gunicorn --workers 4 --worker-class uvicorn.workers.UvicornWorker auth_project.asgi:application
├─ Handles: HTTP + WebSocket (production)
├─ ASGI: ✅ Yes
├─ WebSocket: ✅ Yes
├─ Performance: High
└─ Use case: Production servers
```

---

## 4. Request Flow Comparison

### Current (Broken) Flow
```
Client Browser
    │
    │ ws://localhost:8000/ws/project/2/
    │
    ▼
Django runserver (HTTP only)
    │
    │ ❌ Can't upgrade to WebSocket
    │ Treats as GET /ws/project/2/ HTTP/1.1
    │
    ▼
Django URL Router (urls.py)
    │
    │ ❌ No match found
    │ (WebSocket routes are in accounts/routing.py, not urls.py)
    │
    ▼
404 Not Found
    │
Error to Client: GET /ws/project/2/ HTTP/1.1 → 404
```

### Correct Flow (Fixed)
```
Client Browser
    │
    │ ws://localhost:8000/ws/project/2/
    │
    ▼
Daphne ASGI Server
    │
    ├─ Protocol: WebSocket detected ✅
    ├─ Handler: ASGI (not WSGI)
    │
    ▼
ProtocolTypeRouter (asgi.py)
    │
    ├─ "websocket" protocol detected
    ├─ Route to accounts.routing.websocket_urlpatterns
    │
    ▼
URLRouter (accounts/routing.py)
    │
    ├─ Pattern: r'ws/project/(?P<project_id>\w+)/$'
    ├─ Match found! ✅
    │
    ▼
ProjectUpdateConsumer.as_asgi()
    │
    ├─ connect() → Accept connection
    ├─ Initialize project group
    ├─ Send initial data
    │
    ▼
WebSocket Connection Established ✅
```

---

## 5. Technical Deep-Dive

### How WebSocket Upgrade Works

**Step 1: Initial HTTP GET with Upgrade Header**
```http
GET /ws/project/2/ HTTP/1.1
Host: localhost:8000
Upgrade: websocket
Connection: Upgrade
Sec-WebSocket-Key: dGhlIHNhbXBsZSBub25jZQ==
Sec-WebSocket-Version: 13
```

**Step 2: Server Response (if successful)**
```http
HTTP/1.1 101 Switching Protocols
Upgrade: websocket
Connection: Upgrade
Sec-WebSocket-Accept: s3pPLMBiTxaQ9kYGzzhZRbK+xOo=
```

**Status 101** = Protocol switch to WebSocket

**Step 3: Bidirectional Communication**
```
Client ↔ Server (over WebSocket, not HTTP)
```

### Why Django runserver Fails

Django's runserver uses WSGI (Web Server Gateway Interface):
- WSGI is **synchronous** and **request-response** only
- Can't handle persistent connections
- Can't upgrade HTTP to WebSocket
- Designed for CGI-style request handling

### Why Daphne Works

Daphne uses ASGI (Asynchronous Server Gateway Interface):
- ASGI is **asynchronous** and **supports multiple protocols**
- Can maintain persistent connections
- Can upgrade HTTP to WebSocket
- Can handle concurrent connections
- Supports WebSocket, HTTP/2, etc.

---

## 6. Configuration Details

### ASGI Application Structure

**File:** `auth_project/asgi.py`

```python
from channels.routing import ProtocolTypeRouter, URLRouter
from channels.auth import AuthMiddlewareStack

application = ProtocolTypeRouter({
    # HTTP requests
    "http": get_asgi_application(),
    
    # WebSocket requests
    "websocket": AuthMiddlewareStack(
        URLRouter(
            accounts.routing.websocket_urlpatterns
        )
    ),
})
```

**Breaking it down:**

1. **ProtocolTypeRouter** - Dispatches by protocol type
   - `"http"` → Django HTTP handler
   - `"websocket"` → WebSocket handler

2. **AuthMiddlewareStack** - Adds user authentication to WebSocket
   - Reads user from session/cookies
   - Sets `scope['user']`

3. **URLRouter** - Routes WebSocket to correct consumer
   - Reads from `accounts.routing.websocket_urlpatterns`
   - Matches URL patterns

4. **Consumer Handler** - Processes WebSocket lifecycle
   - `connect()` - Accept or reject connection
   - `receive()` - Handle incoming messages
   - `disconnect()` - Clean up

---

## 7. Consumer Implementation

### ProjectUpdateConsumer

**Purpose:** Handle real-time project status updates

**Methods:**

```python
async def connect(self):
    """
    Called when WebSocket connects
    - Extract project_id from URL
    - Join group: f'project_{project_id}'
    - Accept connection
    - Send initial data
    """
    self.project_id = self.scope['url_route']['kwargs']['project_id']
    self.project_group_name = f'project_{self.project_id}'
    
    await self.channel_layer.group_add(
        self.project_group_name,
        self.channel_name
    )
    await self.accept()
    
    project_data = await self.get_project_data()
    await self.send(text_data=json.dumps({
        'type': 'project.initial_data',
        'data': project_data
    }))
```

```python
async def receive(self, text_data):
    """
    Called when WebSocket receives message
    - Parse JSON
    - Route by message type
    - Broadcast to group or respond
    """
    data = json.loads(text_data)
    message_type = data.get('type')
    
    if message_type == 'status.update':
        await self.handle_status_update(data.get('status'))
    elif message_type == 'comment.post':
        await self.handle_new_comment(data.get('text'))
    # ... more handlers
```

```python
async def disconnect(self, close_code):
    """
    Called when WebSocket closes
    - Leave group
    - Clean up resources
    """
    await self.channel_layer.group_discard(
        self.project_group_name,
        self.channel_name
    )
```

### Group Broadcasting

**Sending to all clients in group:**
```python
# From views.py or signals
await channel_layer.group_send(
    f'project_{project_id}',
    {
        'type': 'project.status_update',  # ← method name in consumer
        'status': 'active',
        'timestamp': timezone.now().isoformat(),
        'changed_by': user.username
    }
)
```

**Receiving in consumer:**
```python
async def project_status_update(self, event):
    """
    Receive group message
    Called when group_send() is used
    """
    await self.send(text_data=json.dumps({
        'type': 'project.status_update',
        'status': event['status'],
        'timestamp': event.get('timestamp'),
        'changed_by': event.get('changed_by'),
    }))
```

---

## 8. Setting Up Daphne

### Installation

```bash
# Option 1: Direct install
pip install daphne==4.0.0

# Option 2: Add to requirements.txt
echo "daphne==4.0.0" >> requirements.txt
pip install -r requirements.txt
```

### Local Development

```bash
# Start Daphne on localhost:8000
daphne -b 127.0.0.1 -p 8000 auth_project.asgi:application

# With debug output
daphne -b 127.0.0.1 -p 8000 -v 2 auth_project.asgi:application

# With auto-reload (if available)
daphne -b 127.0.0.1 -p 8000 auth_project.asgi:application --reload
```

### Production Deployment

#### render.yaml (Render.com)
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
```

#### Procfile (Railway/Heroku)
```
web: daphne -b 0.0.0.0 -p $PORT auth_project.asgi:application
```

---

## 9. Channel Layers Setup

### For Production (Redis)

**In settings.py:**
```python
CHANNEL_LAYERS = {
    'default': {
        'BACKEND': 'channels_redis.core.RedisChannelLayer',
        'CONFIG': {
            "hosts": [os.getenv('REDIS_URL', 'redis://localhost:6379')],
            "capacity": 1500,
            "expiry": 10,
        },
    },
}
```

**Why:** Multiple Daphne instances need to communicate via Redis

### For Development (In-Memory)

**In settings.py:**
```python
if DEBUG:
    CHANNEL_LAYERS = {
        'default': {
            'BACKEND': 'channels.layers.InMemoryChannelLayer',
        }
    }
```

**Why:** Single process, no need for Redis

---

## 10. Testing WebSocket Connections

### Test 1: Browser Console

```javascript
// Open any project page
// Press F12 → Console tab
// Paste:

let socket = new WebSocket("ws://localhost:8000/ws/project/2/");

socket.onopen = function(e) {
    console.log("✅ Connected!", e);
    console.log("Ready state:", socket.readyState); // 1 = OPEN
};

socket.onmessage = function(event) {
    console.log("📬 Message:", JSON.parse(event.data));
};

socket.onerror = function(error) {
    console.error("❌ Error:", error);
};

socket.onclose = function(e) {
    console.log("❌ Closed:", e.code, e.reason);
};

// Send a message
socket.send(JSON.stringify({
    'type': 'status.update',
    'status': 'active'
}));
```

### Test 2: DevTools Network Tab

1. Open DevTools (F12)
2. Go to **Network** tab
3. **Filter:** Type "WS" or "ws"
4. Check for connections:
   - **Name:** `/ws/project/2/`
   - **Status:** `101` (should be green)
   - **Type:** `websocket`

### Test 3: CLI Tool

```bash
# Install wscat
npm install -g wscat

# Connect
wscat -c ws://localhost:8000/ws/project/2/

# Send message
> {"type":"status.update","status":"active"}

# Receive message
< {"type":"project.status_update","status":"active",...}
```

---

## 11. Troubleshooting

### 404 Still Appears

**Check 1:** Verify Daphne is running
```bash
# If using runserver:
python manage.py runserver
# ❌ Wrong - WebSocket won't work

# If using Daphne:
daphne -b 127.0.0.1 -p 8000 auth_project.asgi:application
# ✅ Correct
```

**Check 2:** Verify port is correct
```bash
# Browser should connect to same port
ws://localhost:8000/ws/project/2/  # ✅
ws://localhost:8001/ws/project/2/  # ❌ (different port)
```

**Check 3:** Verify URL pattern matches
```python
# In accounts/routing.py
re_path(r'ws/project/(?P<project_id>\w+)/$', ...)
#       ↑ No slash before 'ws'
#       Should match: /ws/project/2/
```

### Connection Accepted But No Messages

**Check 1:** Redis not running
```bash
# In production, Redis is required for group_send()
redis-server
```

**Check 2:** Channel layer misconfigured
```python
# Should be in settings.py
CHANNEL_LAYERS = {
    'default': {
        'BACKEND': 'channels_redis.core.RedisChannelLayer',
        'CONFIG': { "hosts": [('127.0.0.1', 6379)] },
    },
}
```

**Check 3:** Consumer group_send() not called
```python
# In views.py or signals, need to explicitly send
await channel_layer.group_send(
    f'project_{project_id}',
    {'type': 'project.status_update', ...}
)
```

### Memory Leak / High CPU

**Check 1:** Too many open connections
```python
# Add connection limit
CHANNEL_LAYERS = {
    'CONFIG': {
        'capacity': 1500,  # Max connections
        'expiry': 10,      # Clean up timeout
    }
}
```

**Check 2:** Infinite loop in receive()
```python
# Make sure receive() has proper error handling
async def receive(self, text_data):
    try:
        # ... process message
    except Exception as e:
        logger.error(f"Error: {e}")
        await self.send_error(str(e))
```

---

## 12. Performance Considerations

### Connection Limits

```python
# settings.py
CHANNEL_LAYERS = {
    'CONFIG': {
        'capacity': 1500,      # Max concurrent connections
        'expiry': 10,          # Seconds before cleanup
        'group_expiry': 86400, # Group expiry (24h)
    }
}
```

### Scalability

**Single Server:**
- Daphne can handle ~1000 concurrent connections per process
- Use 4-8 worker processes for production

**Multi-Server:**
- Redis channel layer enables communication across servers
- Allows horizontal scaling

### Optimization Tips

1. **Use select_related()** - Avoid N+1 queries in consumers
2. **Batch messages** - Send updates every 100ms, not every 1ms
3. **Compress JSON** - Reduce message size
4. **Auth caching** - Cache user permissions in consumer

---

## 13. Complete Implementation Checklist

- [ ] Install daphne: `pip install daphne==4.0.0`
- [ ] Add to requirements.txt
- [ ] Stop using `python manage.py runserver`
- [ ] Start using `daphne -b 127.0.0.1 -p 8000 auth_project.asgi:application`
- [ ] Test WebSocket in browser console
- [ ] Check DevTools for status 101
- [ ] Verify no 404 errors
- [ ] Test group broadcasting
- [ ] Test multiple clients
- [ ] Update Procfile for production
- [ ] Deploy and verify

---

## 14. Comparison: Before vs After

### Before (Broken)
```
Server: python manage.py runserver
Result: /ws/project/2/ → 404
Status:  ❌ WebSocket not supported
```

### After (Fixed)
```
Server: daphne -b 127.0.0.1 -p 8000 auth_project.asgi:application
Result: /ws/project/2/ → 101 Switching Protocols
Status:  ✅ WebSocket working
```

---

## Summary Table

| Component | Current | Fixed |
|-----------|---------|-------|
| **Server** | Django runserver | Daphne ASGI |
| **Protocol Support** | HTTP only | HTTP + WebSocket |
| **ASGI** | ❌ | ✅ |
| **WebSocket** | ❌ | ✅ |
| **Status Code** | 404 | 101 |
| **Connection** | Fails | Works |

---

**Resolution:** Follow Quick Fix steps or detailed WEBSOCKET_ROUTING_FIX_2026.md

**Next:** Deploy to Render/Railway with updated Procfile
