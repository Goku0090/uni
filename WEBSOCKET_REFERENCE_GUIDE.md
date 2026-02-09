# WebSocket Implementation Reference Guide
**Complete guide for UniSync WebSocket architecture**

---

## Quick Reference

### Current Status
```
Error:      /ws/project/2/ → 404 Not Found
Cause:      Using Django runserver (HTTP only) instead of Daphne (ASGI)
Fix:        3-step implementation
Time:       5 minutes
Impact:     Medium (breaks real-time features)
```

### File Locations
```
Configuration:     auth_project/asgi.py
Routing:          accounts/routing.py  
Consumers:        accounts/consumers.py
Settings:         auth_project/settings.py
Procfile:         ./Procfile
Requirements:     auth_project/requirements.txt
```

---

## 1. Architecture Overview

### What is WebSocket?

**WebSocket** = Persistent two-way connection over single TCP socket

```
Traditional HTTP:
Client → Request → Server
Client ← Response ← Server
(Connection closes after response)

WebSocket:
Client ←→ Connection ←→ Server
(Connection stays open, bidirectional messages)
```

### Why WebSocket for UniSync?

1. **Real-time Project Updates** - Changes appear instantly
2. **Live Comments** - See comments as they're posted
3. **Notifications** - Immediate alerts to users
4. **Activity Feed** - Live activity stream
5. **Messaging** - Real-time chat

### WebSocket Flow

```
1. Browser initiates:
   GET /ws/project/2/ HTTP/1.1
   Upgrade: websocket

2. Server responds:
   HTTP/1.1 101 Switching Protocols
   Upgrade: websocket

3. Persistent connection:
   Client ←→ Server
   (JSON messages both ways)

4. Consumer handles:
   - connect() → Accept
   - receive() → Process message
   - send() → Send response
   - disconnect() → Cleanup
```

---

## 2. WebSocket in UniSync

### Configured Routes

```
Path                          Consumer                  Purpose
────────────────────────────────────────────────────────────────
/ws/project/<project_id>/    ProjectUpdateConsumer    Project status
/ws/activity-feed/           ActivityFeedConsumer     Activity stream
/ws/notifications/           NotificationConsumer     Real-time alerts
```

### Message Types

**Project Updates:**
```json
{
  "type": "project.status_update",
  "status": "active",
  "changed_by": "john_doe",
  "timestamp": "2026-02-06T10:30:00Z"
}
```

**Comments:**
```json
{
  "type": "project.comment_posted",
  "comment_id": 123,
  "username": "jane_doe",
  "content": "Great project!",
  "created_at": "2026-02-06T10:30:00Z"
}
```

**Notifications:**
```json
{
  "type": "notification.new",
  "notification_type": "project_comment",
  "title": "Jane commented on your project",
  "message": "Great project!"
}
```

---

## 3. Implementation Guide

### Step 1: Install Daphne (Immediate)

```bash
# Terminal
pip install daphne==4.0.0

# Or add to requirements.txt
echo "daphne==4.0.0" >> auth_project/requirements.txt
pip install -r auth_project/requirements.txt
```

### Step 2: Update requirements.txt

```txt
# auth_project/requirements.txt
...
daphne==4.0.0
channels==4.0.0
channels-redis==4.1.0
...
```

### Step 3: Start Daphne (Local Development)

```bash
# Stop this:
python manage.py runserver

# Start this:
cd auth_project
daphne -b 127.0.0.1 -p 8000 auth_project.asgi:application
```

### Step 4: Test in Browser

```javascript
// Open browser console (F12)
// On any project page, run:

let socket = new WebSocket("ws://localhost:8000/ws/project/2/");
socket.onopen = () => console.log("✅ WebSocket connected!");
socket.onmessage = (e) => console.log("📬", JSON.parse(e.data));
socket.onerror = (e) => console.error("❌", e);
```

### Step 5: Update Procfile (Deployment)

```makefile
# Procfile
web: daphne -b 0.0.0.0 -p 8000 auth_project.asgi:application
```

---

## 4. Detailed Component Reference

### ASGI Configuration

**File:** `auth_project/asgi.py`

```python
from channels.auth import AuthMiddlewareStack
from channels.routing import ProtocolTypeRouter, URLRouter
from django.core.asgi import get_asgi_application
import accounts.routing

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'auth_project.settings')

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

**Breakdown:**
- `ProtocolTypeRouter` - Routes by protocol (http/websocket)
- `AuthMiddlewareStack` - Adds user auth to scope
- `URLRouter` - Matches URL patterns to consumers

### WebSocket Routes

**File:** `accounts/routing.py`

```python
from django.urls import re_path
from . import consumers

websocket_urlpatterns = [
    # Pattern format: re_path(regex, consumer)
    re_path(r'ws/project/(?P<project_id>\w+)/$', 
            consumers.ProjectUpdateConsumer.as_asgi()),
    
    re_path(r'ws/activity-feed/$', 
            consumers.ActivityFeedConsumer.as_asgi()),
    
    re_path(r'ws/notifications/$', 
            consumers.NotificationConsumer.as_asgi()),
]
```

**Pattern Matching:**
```
Pattern:  r'ws/project/(?P<project_id>\w+)/$'
URL:      ws://localhost:8000/ws/project/2/
Match:    ✅ (project_id='2')

URL:      ws://localhost:8000/ws/project/abc123/
Match:    ✅ (project_id='abc123')

URL:      ws://localhost:8000/ws/project/
Match:    ❌ (missing trailing slash)
```

### Consumer Implementation

**File:** `accounts/consumers.py`

```python
from channels.generic.websocket import AsyncWebsocketConsumer
from channels.db import database_sync_to_async
import json

class ProjectUpdateConsumer(AsyncWebsocketConsumer):
    """Handles real-time project updates"""
    
    async def connect(self):
        """Called when WebSocket connects"""
        # Extract URL parameters
        self.project_id = self.scope['url_route']['kwargs']['project_id']
        self.project_group_name = f'project_{self.project_id}'
        
        # Join group for broadcasting
        await self.channel_layer.group_add(
            self.project_group_name,
            self.channel_name
        )
        
        # Accept connection
        await self.accept()
        
        # Send initial data
        project_data = await self.get_project_data()
        await self.send(text_data=json.dumps({
            'type': 'project.initial_data',
            'data': project_data
        }))
    
    async def receive(self, text_data):
        """Called when message received from client"""
        data = json.loads(text_data)
        message_type = data.get('type')
        
        if message_type == 'status.update':
            await self.handle_status_update(data.get('status'))
        elif message_type == 'comment.post':
            await self.handle_new_comment(data.get('text'))
    
    async def disconnect(self, close_code):
        """Called when WebSocket closes"""
        await self.channel_layer.group_discard(
            self.project_group_name,
            self.channel_name
        )
    
    # Handler for group messages
    async def project_status_update(self, event):
        """Broadcast status update to all clients in group"""
        await self.send(text_data=json.dumps({
            'type': 'project.status_update',
            'status': event['status'],
            'changed_by': event.get('changed_by'),
            'timestamp': event.get('timestamp'),
        }))
    
    # Helper methods
    @database_sync_to_async
    def get_project_data(self):
        """Fetch project from database"""
        from .models import Project
        try:
            project = Project.objects.get(id=self.project_id)
            return {
                'id': project.id,
                'title': project.title,
                'status': project.status,
                'members': project.members.count(),
            }
        except Project.DoesNotExist:
            return None
    
    async def send_error(self, message):
        """Send error message to client"""
        await self.send(text_data=json.dumps({
            'type': 'error',
            'message': message
        }))
```

**Key Methods:**
- `connect()` - WebSocket connects
- `receive(text_data)` - Message from client
- `send(text_data)` - Message to client
- `disconnect(close_code)` - WebSocket closes
- Group handlers - Receive group broadcasts

---

## 5. Broadcasting to Multiple Clients

### How Group Broadcasting Works

```
View/Signal
    │
    └─→ group_send('project_123', {
        'type': 'project.status_update',
        'status': 'active'
    })
        │
        └─→ All consumers in group
            │
            ├─→ Consumer A (User A)
            ├─→ Consumer B (User B)
            ├─→ Consumer C (User C)
            │
            └─→ Call: async def project_status_update(self, event)
                │
                └─→ await self.send(...)  (send to each client)
```

### Example: Broadcasting from View

```python
# In views.py
from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync

def update_project_status(request, project_id):
    """Update project status and notify all viewers"""
    
    project = Project.objects.get(id=project_id)
    project.status = request.POST.get('status')
    project.save()
    
    # Notify all users watching this project
    channel_layer = get_channel_layer()
    async_to_sync(channel_layer.group_send)(
        f'project_{project_id}',
        {
            'type': 'project.status_update',
            'status': project.status,
            'changed_by': request.user.username,
            'timestamp': timezone.now().isoformat(),
        }
    )
    
    return JsonResponse({'success': True})
```

### Example: Broadcasting from Signal

```python
# In signals.py
from django.db.models.signals import post_save
from django.dispatch import receiver
from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync

@receiver(post_save, sender=Project)
def project_saved(sender, instance, created, **kwargs):
    """When project is saved, notify viewers"""
    
    if created:
        activity_type = 'project_created'
    else:
        activity_type = 'project_updated'
    
    channel_layer = get_channel_layer()
    async_to_sync(channel_layer.group_send)(
        f'project_{instance.id}',
        {
            'type': 'project.updated',
            'activity': activity_type,
            'project_id': instance.id,
            'timestamp': timezone.now().isoformat(),
        }
    )
```

---

## 6. Client-Side Implementation

### Simple WebSocket Client

```html
<!-- In template -->
<script>
const projectId = {{ project.id }};
const wsUrl = `ws://${window.location.host}/ws/project/${projectId}/`;
const socket = new WebSocket(wsUrl);

// Connection opened
socket.onopen = function(event) {
    console.log('WebSocket connected');
    // Can now send/receive messages
};

// Message received from server
socket.onmessage = function(event) {
    const data = JSON.parse(event.data);
    console.log('Received:', data);
    
    if (data.type === 'project.status_update') {
        console.log('Status:', data.status);
        // Update UI with new status
    }
    else if (data.type === 'project.comment_posted') {
        // Add comment to UI
        addCommentToUI(data);
    }
};

// Error occurred
socket.onerror = function(error) {
    console.error('WebSocket error:', error);
};

// Connection closed
socket.onclose = function(event) {
    console.log('WebSocket closed');
};

// Send message to server
function updateProjectStatus(status) {
    socket.send(JSON.stringify({
        'type': 'status.update',
        'status': status
    }));
}

function postComment(text) {
    socket.send(JSON.stringify({
        'type': 'comment.post',
        'text': text
    }));
}
</script>
```

### React Component Example

```jsx
import { useEffect, useState } from 'react';

export default function ProjectDetail({ projectId }) {
    const [socket, setSocket] = useState(null);
    const [status, setStatus] = useState(null);
    
    useEffect(() => {
        const ws = new WebSocket(
            `ws://${window.location.host}/ws/project/${projectId}/`
        );
        
        ws.onopen = () => {
            console.log('Connected');
            setSocket(ws);
        };
        
        ws.onmessage = (event) => {
            const data = JSON.parse(event.data);
            if (data.type === 'project.status_update') {
                setStatus(data.status);
            }
        };
        
        return () => ws.close();
    }, [projectId]);
    
    return (
        <div>
            <h1>Project {projectId}</h1>
            <p>Status: {status}</p>
        </div>
    );
}
```

---

## 7. Channel Layers Configuration

### Development (In-Memory)

```python
# settings.py
CHANNEL_LAYERS = {
    'default': {
        'BACKEND': 'channels.layers.InMemoryChannelLayer'
    }
}
```

**Use case:** Single process, testing

### Production (Redis)

```python
# settings.py
CHANNEL_LAYERS = {
    'default': {
        'BACKEND': 'channels_redis.core.RedisChannelLayer',
        'CONFIG': {
            'hosts': [('127.0.0.1', 6379)],
            'capacity': 1500,
            'expiry': 10,
        },
    },
}
```

**Use case:** Multiple Daphne processes, horizontal scaling

### Render.com (Redis)

```python
# settings.py
import redis
import os

CHANNEL_LAYERS = {
    'default': {
        'BACKEND': 'channels_redis.core.RedisChannelLayer',
        'CONFIG': {
            'hosts': [os.getenv('REDIS_URL', 'redis://localhost:6379')],
        },
    },
}
```

---

## 8. Troubleshooting Guide

### Problem: 404 on /ws/project/2/

**Cause:** Using Django runserver

**Solution:**
```bash
# Wrong:
python manage.py runserver

# Right:
daphne -b 127.0.0.1 -p 8000 auth_project.asgi:application
```

### Problem: Connection Accepted But No Messages

**Cause:** Redis not running or misconfigured

**Solution:**
```bash
# Start Redis
redis-server

# Or verify in settings.py
CHANNEL_LAYERS = {
    'CONFIG': {
        'hosts': [('127.0.0.1', 6379)],  # Verify address
    }
}
```

### Problem: "No module named 'channels'"

**Cause:** Package not installed

**Solution:**
```bash
pip install channels==4.0.0 channels-redis==4.1.0
```

### Problem: WebSocket Connection Hangs

**Cause:** Blocking operation in consumer

**Solution:**
```python
# Wrong (blocking):
async def receive(self, text_data):
    # Synchronous database query
    user = User.objects.get(id=1)  # ❌ Blocks event loop

# Right (non-blocking):
async def receive(self, text_data):
    # Async database query
    user = await database_sync_to_async(User.objects.get)(id=1)  # ✅
```

---

## 9. Performance Tips

### Optimize Consumers

```python
# Bad: N+1 queries
async def receive(self, text_data):
    data = json.loads(text_data)
    project = await self.get_project()  # Query 1
    members = await self.get_members()  # Query 2
    tasks = await self.get_tasks()      # Query 3

# Good: Prefetch relations
@database_sync_to_async
def get_project_with_relations(self):
    return Project.objects.prefetch_related(
        'members', 'tasks'
    ).get(id=self.project_id)
```

### Limit Connection Count

```python
CHANNEL_LAYERS = {
    'CONFIG': {
        'capacity': 1500,  # Max connections
        'expiry': 10,      # Cleanup timeout
    }
}
```

### Batch Messages

```python
# Bad: Too many messages
for i in range(1000):
    socket.send(json.dumps({'data': i}))

# Good: Batch updates
updates = []
for i in range(1000):
    updates.append({'data': i})
socket.send(json.dumps({'type': 'batch_update', 'data': updates}))
```

---

## 10. Deployment Checklist

- [ ] Install Daphne: `pip install daphne==4.0.0`
- [ ] Add to requirements.txt
- [ ] Update Procfile to use daphne
- [ ] Update render.yaml if applicable
- [ ] Configure CHANNEL_LAYERS in settings.py
- [ ] Test WebSocket locally
- [ ] Test in browser DevTools (should be status 101)
- [ ] Deploy to production
- [ ] Verify WebSocket works in production
- [ ] Monitor for errors in logs

---

## 11. File Checklist

```
Required Files:
✅ auth_project/asgi.py             (ProtocolTypeRouter setup)
✅ accounts/routing.py               (WebSocket URL patterns)
✅ accounts/consumers.py             (Consumer classes)
✅ auth_project/settings.py          (CHANNEL_LAYERS config)
✅ auth_project/requirements.txt     (daphne, channels)
✅ Procfile                          (daphne startup)

Templates (for client side):
✅ templates/project_detail.html     (WebSocket client code)
✅ templates/activity_feed.html      (Activity feed)
✅ templates/notifications.html      (Notifications)
```

---

## 12. Command Reference

### Development

```bash
# Install dependencies
pip install daphne==4.0.0 channels==4.0.0 channels-redis==4.1.0

# Run Daphne
daphne -b 127.0.0.1 -p 8000 auth_project.asgi:application

# Test WebSocket
wscat -c ws://localhost:8000/ws/project/1/

# Run Django migrations
python manage.py migrate

# Create test user
python manage.py shell
>>> from django.contrib.auth.models import User
>>> User.objects.create_user('testuser', 'test@test.com', 'password')
```

### Production

```bash
# Render deployment
git push origin main

# Check logs
render logs --tail 100

# SSH into container
render ssh

# Monitor WebSocket
curl http://localhost:8000/api/health/
```

---

## Summary

| Component | Location | Status |
|-----------|----------|--------|
| ASGI Config | auth_project/asgi.py | ✅ Configured |
| Routes | accounts/routing.py | ✅ Configured |
| Consumers | accounts/consumers.py | ✅ Implemented |
| Daphne | requirements.txt | ⏳ Install |
| Procfile | Procfile | ⏳ Update |
| Settings | auth_project/settings.py | ✅ Configured |

---

**Status:** Ready to Deploy  
**Next Step:** Follow Quick Fix or Detailed Implementation guide
