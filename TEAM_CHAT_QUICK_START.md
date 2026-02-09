# Team Chat Channels - Quick Start Guide (15 mins)

## Step 1: Add Models (5 mins)

Copy this into `auth_project/accounts/models.py`:

```python
from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone

class Channel(models.Model):
    CHANNEL_TYPES = [
        ('general', 'General'),
        ('technical', 'Technical'),
        ('management', 'Management'),
        ('announcements', 'Announcements'),
        ('resources', 'Resources'),
        ('custom', 'Custom'),
    ]
    
    project = models.ForeignKey('Project', on_delete=models.CASCADE, related_name='channels')
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True, null=True)
    channel_type = models.CharField(max_length=20, choices=CHANNEL_TYPES, default='general')
    is_archived = models.BooleanField(default=False)
    is_private = models.BooleanField(default=False)
    created_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name='channels_created')
    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(auto_now=True)
    last_message_at = models.DateTimeField(null=True, blank=True)
    
    class Meta:
        unique_together = ['project', 'name']
        ordering = ['channel_type', 'name']
    
    def __str__(self):
        return f"#{self.name} ({self.project.title})"


class ChannelMember(models.Model):
    ROLES = [('owner', 'Owner'), ('moderator', 'Moderator'), ('member', 'Member')]
    
    channel = models.ForeignKey(Channel, on_delete=models.CASCADE, related_name='members')
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    role = models.CharField(max_length=15, choices=ROLES, default='member')
    mute_notifications = models.BooleanField(default=False)
    last_read_at = models.DateTimeField(default=timezone.now)
    is_active = models.BooleanField(default=True)
    joined_at = models.DateTimeField(default=timezone.now)
    
    class Meta:
        unique_together = ['channel', 'user']


class ChannelMessage(models.Model):
    channel = models.ForeignKey(Channel, on_delete=models.CASCADE, related_name='messages')
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    content = models.TextField()
    thread_root = models.ForeignKey('self', on_delete=models.CASCADE, null=True, blank=True, related_name='thread_replies')
    mentions = models.ManyToManyField(User, related_name='mentioned_in_messages', blank=True)
    is_edited = models.BooleanField(default=False)
    edited_at = models.DateTimeField(null=True, blank=True)
    is_pinned = models.BooleanField(default=False)
    pinned_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name='pinned_messages')
    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['created_at']
        indexes = [models.Index(fields=['channel', 'created_at'])]


class ChannelMessageFile(models.Model):
    message = models.ForeignKey(ChannelMessage, on_delete=models.CASCADE, related_name='files')
    file = models.FileField(upload_to='channel_files/%Y/%m/%d/')
    filename = models.CharField(max_length=255)
    file_size = models.PositiveIntegerField()
    file_type = models.CharField(max_length=100)
    uploaded_at = models.DateTimeField(default=timezone.now)


class ChannelMention(models.Model):
    message = models.ForeignKey(ChannelMessage, on_delete=models.CASCADE, related_name='mention_records')
    mentioned_user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='channel_mentions')
    is_notified = models.BooleanField(default=False)
    notified_at = models.DateTimeField(null=True, blank=True)
    created_at = models.DateTimeField(default=timezone.now)
    
    class Meta:
        unique_together = ['message', 'mentioned_user']
```

---

## Step 2: Create & Run Migrations (2 mins)

```bash
cd auth_project

# Create migrations
python manage.py makemigrations accounts

# Apply migrations
python manage.py migrate

# Verify
python manage.py shell
>>> from accounts.models import Channel
>>> print("✅ Models loaded successfully")
```

---

## Step 3: Add Serializers (3 mins)

Add to `auth_project/accounts/serializers.py`:

```python
from rest_framework import serializers
from .models import Channel, ChannelMember, ChannelMessage, ChannelMessageFile

class ChannelSerializer(serializers.ModelSerializer):
    member_count = serializers.SerializerMethodField()
    created_by_username = serializers.CharField(source='created_by.username', read_only=True)
    
    class Meta:
        model = Channel
        fields = ['id', 'project', 'name', 'description', 'channel_type', 'is_archived', 'is_private', 'created_by_username', 'member_count', 'created_at']
    
    def get_member_count(self, obj):
        return obj.members.filter(is_active=True).count()


class ChannelMessageSerializer(serializers.ModelSerializer):
    author_username = serializers.CharField(source='author.username', read_only=True)
    files = serializers.SerializerMethodField()
    
    class Meta:
        model = ChannelMessage
        fields = ['id', 'channel', 'author_username', 'content', 'thread_root', 'is_pinned', 'reply_count', 'created_at']
    
    def get_files(self, obj):
        return [
            {'id': f.id, 'filename': f.filename, 'url': f.file.url}
            for f in obj.files.all()
        ]
```

---

## Step 4: Add Basic Views (3 mins)

Add to `auth_project/accounts/views.py`:

```python
from rest_framework import viewsets, permissions
from rest_framework.decorators import action
from rest_framework.response import Response
from .models import Channel, ChannelMember, ChannelMessage
from .serializers import ChannelSerializer, ChannelMessageSerializer

class ChannelViewSet(viewsets.ModelViewSet):
    serializer_class = ChannelSerializer
    permission_classes = [permissions.IsAuthenticated]
    
    def get_queryset(self):
        user_projects = Project.objects.filter(user=self.request.user)
        return Channel.objects.filter(project__in=user_projects).prefetch_related('members')
    
    def create(self, request, *args, **kwargs):
        project_id = request.data.get('project')
        channel = Channel.objects.create(
            project_id=project_id,
            name=request.data.get('name'),
            channel_type=request.data.get('channel_type', 'general'),
            description=request.data.get('description'),
            created_by=request.user
        )
        # Add creator as owner
        ChannelMember.objects.create(channel=channel, user=request.user, role='owner')
        return Response(ChannelSerializer(channel).data, status=201)
    
    @action(detail=True, methods=['post'])
    def add_member(self, request, pk=None):
        channel = self.get_object()
        user_id = request.data.get('user_id')
        ChannelMember.objects.get_or_create(channel=channel, user_id=user_id)
        return Response({'status': 'member added'})


class ChannelMessageViewSet(viewsets.ModelViewSet):
    serializer_class = ChannelMessageSerializer
    permission_classes = [permissions.IsAuthenticated]
    
    def get_queryset(self):
        channel_id = self.kwargs.get('channel_id')
        return ChannelMessage.objects.filter(channel_id=channel_id, thread_root__isnull=True)
    
    def create(self, request, *args, **kwargs):
        channel_id = self.kwargs.get('channel_id')
        
        import re
        content = request.data.get('content')
        mentions = re.findall(r'@(\w+)', content)
        
        message = ChannelMessage.objects.create(
            channel_id=channel_id,
            author=request.user,
            content=content
        )
        
        # Add mentions
        mentioned_users = User.objects.filter(username__in=mentions)
        message.mentions.set(mentioned_users)
        
        return Response(ChannelMessageSerializer(message).data, status=201)
```

---

## Step 5: Register URLs (2 mins)

Add to `auth_project/accounts/urls.py`:

```python
from rest_framework.routers import DefaultRouter
from . import views

router = DefaultRouter()
router.register(r'channels', views.ChannelViewSet, basename='channel')

urlpatterns = [
    path('api/', include(router.urls)),
    
    path('api/channels/<int:channel_id>/messages/',
         views.ChannelMessageViewSet.as_view({'get': 'list', 'post': 'create'}),
         name='channel-messages'),
]
```

---

## Step 6: WebSocket Consumer (2 mins)

Add to `auth_project/accounts/consumers.py`:

```python
import json
from channels.generic.websocket import AsyncWebsocketConsumer
from channels.db import database_sync_to_async
from .models import ChannelMessage, ChannelMember, ChannelMention, Notification

class ChannelChatConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.channel_id = self.scope['url_route']['kwargs']['channel_id']
        self.channel_group_name = f'channel_{self.channel_id}'
        self.user = self.scope['user']
        
        # Check membership
        is_member = await self.check_membership()
        if not is_member:
            await self.close()
            return
        
        # Join group
        await self.channel_layer.group_add(self.channel_group_name, self.channel_name)
        await self.accept()
    
    async def disconnect(self, close_code):
        await self.channel_layer.group_discard(self.channel_group_name, self.channel_name)
    
    async def receive(self, text_data):
        data = json.loads(text_data)
        
        if data['type'] == 'message':
            message = await self.save_message(data.get('content'))
            
            await self.channel_layer.group_send(self.channel_group_name, {
                'type': 'chat.message',
                'message_id': message['id'],
                'author': message['author'],
                'content': message['content'],
                'created_at': message['created_at']
            })
    
    async def chat_message(self, event):
        await self.send(text_data=json.dumps({
            'type': 'message',
            'data': event
        }))
    
    @database_sync_to_async
    def check_membership(self):
        return ChannelMember.objects.filter(
            channel_id=self.channel_id,
            user=self.user
        ).exists()
    
    @database_sync_to_async
    def save_message(self, content):
        import re
        
        message = ChannelMessage.objects.create(
            channel_id=self.channel_id,
            author=self.user,
            content=content
        )
        
        # Process mentions
        mentions = re.findall(r'@(\w+)', content)
        mentioned_users = User.objects.filter(username__in=mentions)
        message.mentions.set(mentioned_users)
        
        # Create notifications
        for user in mentioned_users:
            Notification.objects.create(
                user=user,
                notification_type='channel_mention',
                title=f'{self.user.username} mentioned you',
                from_user=self.user
            )
        
        return {
            'id': message.id,
            'author': self.user.username,
            'content': message.content,
            'created_at': message.created_at.isoformat()
        }
```

Add to `auth_project/accounts/routing.py`:

```python
from django.urls import path
from . import consumers

websocket_urlpatterns = [
    path('ws/channel/<int:channel_id>/', consumers.ChannelChatConsumer.as_asgi()),
]
```

---

## Step 7: Test It! (1 min)

```bash
# Start server
python manage.py runserver

# In another terminal, start Daphne (for WebSocket)
daphne -b 0.0.0.0 -p 8000 auth_project.asgi:application
```

Test in browser console:

```javascript
// Create a channel
fetch('/api/channels/', {
    method: 'POST',
    headers: {'Content-Type': 'application/json', 'X-CSRFToken': getCookie('csrftoken')},
    body: JSON.stringify({
        project: 1,
        name: 'general',
        channel_type: 'general',
        description: 'General discussion'
    })
}).then(r => r.json()).then(data => console.log('✅ Channel created:', data));

// Connect to WebSocket
const socket = new WebSocket('ws://localhost:8000/ws/channel/1/');
socket.onopen = () => console.log('✅ Connected');
socket.onmessage = (e) => console.log('📨', JSON.parse(e.data));

// Send message
socket.send(JSON.stringify({
    type: 'message',
    content: 'Hello team! @john please review'
}));
```

---

## Step 8: Frontend Integration

Create `accounts/templates/channels.html`:

```html
{% extends 'base.html' %}

{% block content %}
<div class="container mx-auto py-6">
    <h1 class="text-3xl font-bold mb-6">{{ project.title }} - Team Chat</h1>
    
    <div class="grid grid-cols-12 gap-6">
        <!-- Channels Sidebar -->
        <div class="col-span-3 bg-gray-900 rounded-lg p-4">
            <div id="channels-list"></div>
        </div>
        
        <!-- Messages Area -->
        <div class="col-span-9 bg-gray-900 rounded-lg flex flex-col h-screen">
            <div id="messages" class="flex-1 overflow-y-auto p-4 space-y-4"></div>
            
            <form id="message-form" class="p-4 border-t border-gray-800">
                <textarea id="message-input" placeholder="Message... (@mention to notify)" class="w-full bg-gray-800 text-white p-2 rounded mb-2"></textarea>
                <button type="submit" class="bg-blue-600 text-white px-4 py-2 rounded">Send</button>
            </form>
        </div>
    </div>
</div>

<script>
const API_BASE = '/api';
let socket = null;

async function loadChannels(projectId) {
    const channels = await fetch(`${API_BASE}/channels/?project=${projectId}`).then(r => r.json());
    document.getElementById('channels-list').innerHTML = channels.map(c => `
        <button onclick="selectChannel(${c.id}, '${c.name}')" class="w-full text-left p-2 hover:bg-gray-800 rounded">
            #${c.name} (${c.member_count})
        </button>
    `).join('');
}

function selectChannel(channelId, name) {
    document.querySelector('.channel-title').textContent = `#${name}`;
    
    // Connect WebSocket
    const protocol = window.location.protocol === 'https:' ? 'wss:' : 'ws:';
    socket = new WebSocket(`${protocol}//${window.location.host}/ws/channel/${channelId}/`);
    socket.onmessage = (e) => {
        const data = JSON.parse(e.data);
        if (data.type === 'message') {
            const msg = data.data;
            document.getElementById('messages').innerHTML += `
                <div class="p-3 bg-gray-800 rounded">
                    <strong>${msg.author}</strong>
                    <p>${msg.content}</p>
                    <small class="text-gray-400">${msg.created_at}</small>
                </div>
            `;
        }
    };
    
    // Load messages
    fetch(`${API_BASE}/channels/${channelId}/messages/`)
        .then(r => r.json())
        .then(msgs => {
            document.getElementById('messages').innerHTML = msgs.map(m => `
                <div class="p-3 bg-gray-800 rounded">
                    <strong>${m.author_username}</strong>
                    <p>${m.content}</p>
                </div>
            `).join('');
        });
}

document.getElementById('message-form').addEventListener('submit', (e) => {
    e.preventDefault();
    const content = document.getElementById('message-input').value;
    socket.send(JSON.stringify({type: 'message', content: content}));
    document.getElementById('message-input').value = '';
});
</script>
{% endblock %}
```

---

## Done! 🎉

Your team chat channels are now live with:
- ✅ Project-specific channels
- ✅ Real-time WebSocket messaging
- ✅ @mention notifications
- ✅ Thread-based discussions (via thread_root)
- ✅ File sharing (ready to implement)

**Next Steps:**
1. Add file upload handling
2. Customize channel templates
3. Add thread UI
4. Deploy to production

See full implementation in: **TEAM_CHAT_CHANNELS_IMPLEMENTATION.md**
