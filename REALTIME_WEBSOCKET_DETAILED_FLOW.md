# UniSync Real-Time WebSocket System - Detailed Flow

## Overview

UniSync uses **Django Channels** with **WebSockets** for real-time updates. When a user posts a comment, it instantly appears on all viewers' screens without refresh.

---

## Architecture Diagram

```
┌────────────────────────────────────────────────────────────────┐
│                    Client Browser                             │
│  ┌─────────────────────────────────────────────────────────┐ │
│  │ Project Detail Page (project_detail.html)               │ │
│  │ - WebSocket connection established                       │ │
│  │ - Listening for: comment_added, member_added events    │ │
│  │ - Comment form (POST to /api/comments/)                │ │
│  └────────────────────────────────────────────────────────┘ │
│         │                              ▲                     │
│         │ 1. POST /api/comments/       │                     │
│         │ {project: 2, content: "..."}│ 4. WebSocket.send()│
│         │                              │                     │
└─────────┼──────────────────────────────┼─────────────────────┘
          │                              │
          ▼                              │
┌────────────────────────────────────────────────────────────────┐
│                  Django Backend (Daphne)                      │
│  ┌─────────────────────────────────────────────────────────┐ │
│  │ 2. View: comment_api.py → PostCommentView              │ │
│  │    - Validate request                                   │ │
│  │    - Create Comment object in database                 │ │
│  │    - Trigger signal: post_save                         │ │
│  │    - Return JSON response                              │ │
│  └─────────────────────────────────────────────────────────┘ │
│         ▼                                                     │
│  ┌─────────────────────────────────────────────────────────┐ │
│  │ 3. Signal Handler: signals_realtime.py                 │ │
│  │    @receiver(post_save, sender=Comment)                │ │
│  │    def comment_created_signal():                       │ │
│  │      - Get channel_layer                               │ │
│  │      - Prepare broadcast message                       │ │
│  │      - group_send('project_<id>', message)            │ │
│  └─────────────────────────────────────────────────────────┘ │
│         ▼                                                     │
│  ┌─────────────────────────────────────────────────────────┐ │
│  │ Channel Layer (InMemory or Redis)                       │ │
│  │ - Broadcasts message to all members in 'project_2'   │ │
│  └─────────────────────────────────────────────────────────┘ │
│         ▼                                                     │
│  ┌─────────────────────────────────────────────────────────┐ │
│  │ WebSocket Consumer: consumers.py                        │ │
│  │ ProjectUpdateConsumer                                   │ │
│  │ - receive() method receives broadcast                  │ │
│  │ - Calls notify_comment() method                        │ │
│  │ - Sends data to WebSocket channel                      │ │
│  └─────────────────────────────────────────────────────────┘ │
│         ▼                                                     │
│  ┌─────────────────────────────────────────────────────────┐ │
│  │ WebSocket Channel                                       │ │
│  │ Sends JSON message through WebSocket tunnel            │ │
│  └─────────────────────────────────────────────────────────┘ │
└─────────────────────────────────────────────────────────────────┘
          ▲
          │ 4. WebSocket message:
          │    {type: 'comment_added', comment: {...}}
          │
          ▼
┌────────────────────────────────────────────────────────────────┐
│              JavaScript Client (project_detail.html)           │
│  ┌─────────────────────────────────────────────────────────┐ │
│  │ socket.onmessage = (e) => {                            │ │
│  │     let data = JSON.parse(e.data);                     │ │
│  │     if (data.type === 'comment_added') {              │ │
│  │         addCommentToDOM(data.comment);  // Update UI  │ │
│  │     }                                                   │ │
│  │ }                                                       │ │
│  └─────────────────────────────────────────────────────────┘ │
│         ▲                                                     │
│         │ 5. DOM Updated Instantly                           │
│         │ All connected users see new comment               │
│         │ No page refresh needed                            │
│         │ Smooth real-time collaboration                    │
└─────────────────────────────────────────────────────────────────┘
```

---

## Step-by-Step Flow

### Step 1: Client Posts Comment

**File**: `project_detail.html` (JavaScript)

```html
<form id="comment-form">
    <textarea id="comment-content" placeholder="Add a comment..."></textarea>
    <button type="submit">Post</button>
</form>

<script>
document.getElementById('comment-form').addEventListener('submit', async (e) => {
    e.preventDefault();
    
    const content = document.getElementById('comment-content').value;
    const projectId = document.getElementById('project-id').value;
    
    // Send comment via API
    const response = await fetch(`/api/projects/${projectId}/comments/`, {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
            'X-CSRFToken': csrfToken,
        },
        body: JSON.stringify({
            content: content,
            parent_comment: null,  // For nested comments
        })
    });
    
    if (response.ok) {
        document.getElementById('comment-content').value = '';
        // Don't manually add to DOM - wait for WebSocket update
        console.log('Comment posted, waiting for WebSocket update...');
    }
});
</script>
```

---

### Step 2: Backend Creates Comment

**File**: `comment_api.py` (Django API View)

```python
from rest_framework import generics
from rest_framework.permissions import IsAuthenticated
from .models import Comment, Project
from .serializers import CommentSerializer

class PostCommentView(generics.CreateAPIView):
    """
    Handle comment creation
    POST /api/projects/<project_id>/comments/
    """
    serializer_class = CommentSerializer
    permission_classes = [IsAuthenticated]
    
    def perform_create(self, serializer):
        project_id = self.kwargs['project_id']
        project = get_object_or_404(Project, id=project_id)
        
        # Create comment (triggers post_save signal)
        serializer.save(
            user=self.request.user,
            project=project
        )
```

---

### Step 3: Signal Handler Triggered

**File**: `accounts/signals_realtime.py`

```python
from django.db.models.signals import post_save
from django.dispatch import receiver
from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync
import json

@receiver(post_save, sender=Comment)
def comment_created_signal(sender, instance, created, **kwargs):
    """
    Called automatically when Comment is saved.
    Broadcasts the new comment to all WebSocket consumers
    connected to this project.
    """
    
    if not created:  # Only on creation, not updates
        return
    
    # Get the channel layer
    channel_layer = get_channel_layer()
    
    # Group name matches the project ID
    group_name = f'project_{instance.project.id}'
    
    # Prepare the message to broadcast
    message = {
        'type': 'notify_comment',  # Maps to notify_comment() in consumer
        'data': {
            'type': 'comment_added',
            'comment': {
                'id': instance.id,
                'user': instance.user.username,
                'user_avatar': instance.user.student_profile.profile_photo.url if instance.user.student_profile.profile_photo else '/static/default-avatar.jpg',
                'content': instance.content,
                'created_at': instance.created_at.isoformat(),
            }
        }
    }
    
    # Send message to all consumers in the group
    # This doesn't wait for response (async)
    async_to_sync(channel_layer.group_send)(
        group_name,
        message
    )
    
    print(f"[SIGNAL] Broadcasting comment to {group_name}")
```

**Key Points:**
- Signal fires **automatically** when Comment is saved
- `group_name = f'project_{instance.project.id}'` determines which clients receive it
- `group_send()` broadcasts to all connected WebSocket consumers in that group

---

### Step 4: WebSocket Consumer Receives & Sends

**File**: `accounts/consumers.py`

```python
from channels.generic.websocket import AsyncWebsocketConsumer
from channels.db import database_sync_to_async
import json

class ProjectUpdateConsumer(AsyncWebsocketConsumer):
    """
    WebSocket consumer for real-time project updates.
    Handles comments, members, tasks, etc.
    """
    
    async def connect(self):
        """Called when WebSocket connection is established"""
        
        # Get project ID from URL route
        self.project_id = self.scope['url_route']['kwargs']['project_id']
        self.group_name = f'project_{self.project_id}'
        
        # Join the group (makes this consumer part of the broadcast)
        await self.channel_layer.group_add(
            self.group_name,
            self.channel_name
        )
        
        await self.accept()  # Accept the WebSocket connection
        
        print(f"✅ WebSocket connected: {self.group_name}")
    
    async def disconnect(self, close_code):
        """Called when WebSocket connection closes"""
        
        # Leave the group
        await self.channel_layer.group_discard(
            self.group_name,
            self.channel_name
        )
        
        print(f"❌ WebSocket disconnected: {self.group_name}")
    
    async def notify_comment(self, event):
        """
        Handler for 'notify_comment' message type.
        Called when signal broadcasts message with type='notify_comment'
        """
        
        # Extract the data from the event
        data = event['data']
        
        # Send the JSON message to the WebSocket client
        await self.send(
            text_data=json.dumps(data)
        )
        
        print(f"[CONSUMER] Sent comment update: {data['comment']['id']}")
    
    async def receive(self, text_data):
        """
        Called when client sends message to server.
        Can be used for typing indicators, read receipts, etc.
        """
        
        data = json.loads(text_data)
        message_type = data.get('type')
        
        if message_type == 'typing':
            # Broadcast typing indicator
            await self.channel_layer.group_send(
                self.group_name,
                {
                    'type': 'typing_indicator',
                    'user': self.scope['user'].username,
                }
            )
        elif message_type == 'read_comment':
            # Mark comment as read
            await self.mark_comment_read(data['comment_id'])
```

**Key Points:**
- `connect()` - Joins the WebSocket group when client connects
- `notify_comment()` - Receives broadcast from signal handler
- `send()` - Sends JSON to client through WebSocket
- Consumer is **async** (non-blocking) - can handle many concurrent clients

---

### Step 5: Client Receives & Updates UI

**File**: `static/js/realtime-updates.js`

```javascript
class ProjectWebSocket {
    constructor(projectId) {
        this.projectId = projectId;
        this.socket = null;
        this.reconnectAttempts = 0;
        this.maxReconnectAttempts = 5;
        this.reconnectDelay = 1000;
    }
    
    connect() {
        // Determine protocol (ws or wss)
        const protocol = window.location.protocol === 'https:' ? 'wss' : 'ws';
        const host = window.location.host;
        
        // WebSocket URL matches the route in routing.py
        const url = `${protocol}://${host}/ws/project/${this.projectId}/`;
        
        console.log(`[WS] Connecting to ${url}`);
        
        this.socket = new WebSocket(url);
        
        // Connection opened
        this.socket.onopen = () => {
            console.log('✅ WebSocket connected to project ' + this.projectId);
            this.reconnectAttempts = 0;
        };
        
        // Message received from server
        this.socket.onmessage = (event) => {
            const data = JSON.parse(event.data);
            console.log('[WS] Received:', data);
            
            // Route based on message type
            this.handleMessage(data);
        };
        
        // Error occurred
        this.socket.onerror = (error) => {
            console.error('❌ WebSocket error:', error);
        };
        
        // Connection closed
        this.socket.onclose = (event) => {
            console.log('WebSocket closed. Code:', event.code);
            this.reconnect();
        };
    }
    
    handleMessage(data) {
        const { type } = data;
        
        switch(type) {
            case 'comment_added':
                this.onCommentAdded(data.comment);
                break;
                
            case 'comment_deleted':
                this.onCommentDeleted(data.comment_id);
                break;
                
            case 'member_added':
                this.onMemberAdded(data.member);
                break;
                
            case 'typing_indicator':
                this.onTypingIndicator(data.user);
                break;
                
            default:
                console.warn('Unknown message type:', type);
        }
    }
    
    onCommentAdded(comment) {
        // Create DOM element for new comment
        const commentsContainer = document.getElementById('comments-list');
        const commentEl = document.createElement('div');
        commentEl.className = 'comment';
        commentEl.id = `comment-${comment.id}`;
        commentEl.innerHTML = `
            <div class="comment-header">
                <img src="${comment.user_avatar}" class="avatar-sm" alt="${comment.user}">
                <strong>${comment.user}</strong>
                <small>${this.formatTime(comment.created_at)}</small>
            </div>
            <div class="comment-content">
                <p>${escapeHtml(comment.content)}</p>
            </div>
            <div class="comment-actions">
                <button class="btn-like" data-comment-id="${comment.id}">👍 Like</button>
                <button class="btn-reply" data-comment-id="${comment.id}">💬 Reply</button>
            </div>
        `;
        
        // Add to DOM
        commentsContainer.appendChild(commentEl);
        
        // Scroll to new comment
        commentEl.scrollIntoView({ behavior: 'smooth' });
        
        // Update comments count
        this.updateCommentCount();
    }
    
    onCommentDeleted(commentId) {
        const el = document.getElementById(`comment-${commentId}`);
        if (el) {
            el.remove();
            this.updateCommentCount();
        }
    }
    
    onMemberAdded(member) {
        const membersContainer = document.getElementById('members-list');
        const memberEl = document.createElement('div');
        memberEl.className = 'member';
        memberEl.innerHTML = `
            <img src="${member.avatar}" alt="${member.username}">
            <div>
                <strong>${member.username}</strong>
                <small>${member.role}</small>
            </div>
        `;
        membersContainer.appendChild(memberEl);
    }
    
    onTypingIndicator(user) {
        // Show "User is typing..."
        console.log(`${user} is typing...`);
    }
    
    updateCommentCount() {
        const count = document.querySelectorAll('#comments-list .comment').length;
        document.getElementById('comment-count').textContent = count;
    }
    
    formatTime(isoString) {
        const date = new Date(isoString);
        return date.toLocaleTimeString();
    }
    
    reconnect() {
        if (this.reconnectAttempts < this.maxReconnectAttempts) {
            this.reconnectAttempts++;
            const delay = this.reconnectDelay * Math.pow(2, this.reconnectAttempts - 1);
            console.log(`Reconnecting in ${delay}ms...`);
            setTimeout(() => this.connect(), delay);
        } else {
            console.error('Max reconnection attempts reached');
        }
    }
}

// Initialize on page load
document.addEventListener('DOMContentLoaded', () => {
    const projectId = document.getElementById('project-id').value;
    const ws = new ProjectWebSocket(projectId);
    ws.connect();
});

// Helper to escape HTML
function escapeHtml(text) {
    const map = {
        '&': '&amp;',
        '<': '&lt;',
        '>': '&gt;',
        '"': '&quot;',
        "'": '&#039;'
    };
    return text.replace(/[&<>"']/g, (m) => map[m]);
}
```

**Key Points:**
- WebSocket URL: `ws://host/ws/project/2/`
- `onmessage` event fires when server sends data
- Message is JSON: `{type: 'comment_added', comment: {...}}`
- Update DOM instantly without page refresh
- Auto-reconnect with exponential backoff

---

## Routing Configuration

### File: `accounts/routing.py`

```python
from django.urls import re_path
from . import consumers

websocket_urlpatterns = [
    # Project updates WebSocket
    re_path(
        r'ws/project/(?P<project_id>\w+)/$',
        consumers.ProjectUpdateConsumer.as_asgi(),
        name='ws-project-updates'
    ),
    
    # Activity feed WebSocket
    re_path(
        r'ws/activity/$',
        consumers.ActivityFeedConsumer.as_asgi(),
        name='ws-activity-feed'
    ),
    
    # Notifications WebSocket
    re_path(
        r'ws/notifications/$',
        consumers.NotificationConsumer.as_asgi(),
        name='ws-notifications'
    ),
]
```

### File: `auth_project/asgi.py`

```python
import os
from django.core.asgi import get_asgi_application
from channels.routing import ProtocolTypeRouter, URLRouter
from channels.auth import AuthMiddlewareStack
from accounts.routing import websocket_urlpatterns

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'auth_project.settings')

# ASGI application that routes between HTTP and WebSocket
application = ProtocolTypeRouter({
    # HTTP requests
    'http': get_asgi_application(),
    
    # WebSocket connections
    'websocket': AuthMiddlewareStack(
        URLRouter(
            websocket_urlpatterns
        )
    ),
})
```

---

## Complete Event Flow Summary

| Step | Actor | Action | Data |
|------|-------|--------|------|
| 1 | Client JS | POST comment via API | `{project: 2, content: "Great!"}` |
| 2 | Django View | Create Comment in DB | `Comment(project=2, user=john, content="Great!")` |
| 3 | Signal Handler | Broadcast via channel layer | `group_send('project_2', {...})` |
| 4 | Consumer | Receive message in group | `notify_comment({type: 'comment_added', ...})` |
| 5 | Consumer | Send to WebSocket client | `send({type: 'comment_added', comment: {...}})` |
| 6 | Client JS | Receive via onmessage | JSON parsed and validated |
| 7 | Client JS | Update DOM | New comment appears on page |
| 8 | Browser | Display | User sees comment instantly |

---

## Performance Considerations

### Channel Layers

```python
# settings.py

# Development (In-Memory - single process only)
CHANNEL_LAYERS = {
    'default': {
        'BACKEND': 'channels.layers.InMemoryChannelLayer'
    }
}

# Production (Redis - multiple processes)
CHANNEL_LAYERS = {
    'default': {
        'BACKEND': 'channels_redis.core.RedisChannelLayer',
        'CONFIG': {
            'hosts': [('redis-url', 6379)],
        },
    },
}
```

### Scaling Considerations

1. **Single Server**: InMemoryChannelLayer works
2. **Multiple Servers**: Need Redis for shared channel layer
3. **High Load**: Use separate Daphne instances with load balancer

---

## Debugging WebSocket Issues

### Check WebSocket Connection

```javascript
// Browser console
// 1. Check connection
console.log(socket.readyState);  // 0=CONNECTING, 1=OPEN, 2=CLOSING, 3=CLOSED

// 2. Check URL
console.log(socket.url);  // Should be wss:// on production

// 3. Monitor messages
socket.onmessage = (e) => {
    console.log('[DEBUG] Message received:', e.data);
};

socket.onerror = (e) => {
    console.error('[DEBUG] Error:', e);
};
```

### Check Server Logs

```bash
# Watch Django logs
tail -f logs/django.log

# Watch Daphne server output
# Should see: "✅ WebSocket connected: project_2"
# Should see: "[SIGNAL] Broadcasting comment to project_2"
# Should see: "[CONSUMER] Sent comment update: 123"
```

### Common Issues

| Issue | Cause | Fix |
|-------|-------|-----|
| WebSocket connects but no data | Consumer not receiving signal | Check signals_realtime.py decorated |
| 403 Forbidden | Auth middleware failing | Ensure user is logged in |
| 404 Not Found | URL pattern mismatch | Check routing.py patterns |
| Message not sent | Consumer not in group | Check group_add in connect() |
| Slow updates | Redis not configured | Use Redis for production |

---

## Real-Time Features Using This System

1. **Live Comments** - Comments appear instantly
2. **Member Notifications** - When someone joins project
3. **Task Updates** - Task status changes broadcast
4. **Typing Indicators** - Show who's typing
5. **Activity Feed** - Real-time activity stream
6. **Notifications** - Instant notification delivery
7. **Read Receipts** - Show who read message
8. **Online Status** - Show user availability

All use the same WebSocket infrastructure!

---

This is the complete real-time system powering UniSync's collaborative features.
