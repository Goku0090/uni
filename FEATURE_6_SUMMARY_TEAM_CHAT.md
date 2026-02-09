# Feature 6: Team Chat Channels ⭐⭐⭐⭐

## Executive Summary

**Team Chat Channels** enable organized, real-time team communication with **project-specific channels**, **threaded discussions**, **file sharing**, and **@mention notifications**. This feature transforms collaboration from project-level to conversation-level organization.

---

## Problem Statement

**Current Issues:**
- No organized team communication structure
- Messages scattered across DMs and comments
- Difficult to track important discussions
- No way to mention specific team members
- File sharing is not centralized
- No threading for related discussions

**Impact:**
- Teams struggle with information organization
- Important updates get lost in message chains
- Onboarding new team members is difficult
- No audit trail of project decisions

---

## Solution Overview

### Architecture: Project → Channels → Messages → Threads

```
Project (UniSinq App)
    ├── #general (General Discussion)
    │   ├── Message 1
    │   ├── Message 2 (Root of Thread)
    │   │   ├── Reply 1
    │   │   ├── Reply 2 (@john check this)
    │   │   └── Reply 3 (with 2 files)
    │   └── Message 3
    │
    ├── #technical (Technical Discussion)
    │   ├── Message 1 (Pinned by @admin)
    │   ├── Message 2 (@mentions @sarah @mike)
    │   └── Message 3 (with code snippet file)
    │
    ├── #management (Project Management)
    │   ├── Milestone Updates
    │   ├── Deadline Reminders
    │   └── Team Decisions
    │
    ├── #announcements (Announcements)
    │   └── Important Updates (Read-only for non-admins)
    │
    └── #resources (Resources & Files)
        ├── Design Files
        ├── Documentation
        └── Code Snippets
```

---

## Key Features

### 1. Channel Management

| Feature | Details |
|---------|---------|
| **Channel Types** | General, Technical, Management, Announcements, Resources, Custom |
| **Channel Privacy** | Public (anyone in project can see) or Private (invite-only) |
| **Channel Archiving** | Archive inactive channels without deleting |
| **Channel Metadata** | Description, creation date, last activity |
| **Member Roles** | Owner, Moderator, Member with granular permissions |

**Database:**
```python
class Channel(models.Model):
    project = ForeignKey(Project)
    name = CharField(max_length=100, unique_together=['project', 'name'])
    channel_type = CharField(choices=[...])
    is_private = BooleanField()
    is_archived = BooleanField()
    created_by = ForeignKey(User)
    last_message_at = DateTimeField()
```

### 2. Real-time Messaging

| Feature | Implementation |
|---------|-----------------|
| **WebSocket Integration** | Instant message delivery using Django Channels + Redis |
| **Typing Indicators** | Show when users are typing messages |
| **Read Status** | Track which messages users have read |
| **Online Status** | See who's currently in the channel |
| **Message Editing** | Edit messages after posting (with "edited" indicator) |
| **Message Deletion** | Delete messages (owner or moderator only) |

**WebSocket Flow:**
```
User Types & Sends
    ↓
WebSocket Consumer Receives
    ↓
Parse Mentions (@username)
    ↓
Save to Database
    ↓
Broadcast to Channel Group
    ↓
All Connected Users Receive Instantly
    ↓
Append to DOM + Scroll to Bottom
```

### 3. Thread-based Discussions

Organize related messages into conversation threads without cluttering the main channel.

**Structure:**
```
Message (thread_root = NULL)
├── Reply 1 (thread_root = Message)
├── Reply 2 (thread_root = Message)
│   └── Can have nested replies
└── Reply 3 (thread_root = Message)
```

**Use Cases:**
- Keep related discussions together
- Reduce main channel clutter
- Easy to follow conversation context
- Reply counter shows discussion activity

**Database:**
```python
class ChannelMessage(models.Model):
    channel = ForeignKey(Channel)
    author = ForeignKey(User)
    content = TextField()
    thread_root = ForeignKey('self', null=True, blank=True)  # Key for threading
    created_at = DateTimeField()
```

### 4. @Mention System with Notifications

Notify specific users when mentioned in messages.

**Features:**
- Parse mentions automatically (@username)
- Create notification records
- Send to activity feed
- Email notification option (future)
- Mention history in user profile

**Notification Flow:**
```
User Types "@john"
    ↓
Message Saved
    ↓
Extract Mentioned Users
    ↓
Create ChannelMention Record
    ↓
Create Notification
    ↓
Broadcast to User's Notification WebSocket
    ↓
Show Badge/Alert in UI
```

**Database:**
```python
class ChannelMention(models.Model):
    message = ForeignKey(ChannelMessage)
    mentioned_user = ForeignKey(User)
    is_notified = BooleanField()
    created_at = DateTimeField()
```

### 5. File Sharing

Share documents, images, code snippets, and resources.

**Supported Types:**
- **Images**: PNG, JPG, GIF (show thumbnails)
- **Documents**: PDF, DOCX, XLSX
- **Code**: Python, JS, JSON, SQL
- **Archives**: ZIP, RAR
- **Media**: MP4, MP3

**Features:**
- Drag & drop upload
- Multiple file support
- File size validation
- MIME type checking
- Direct download links
- Preview for images/code

**Database:**
```python
class ChannelMessageFile(models.Model):
    message = ForeignKey(ChannelMessage)
    file = FileField(upload_to='channel_files/%Y/%m/%d/')
    filename = CharField(max_length=255)
    file_size = PositiveIntegerField()
    file_type = CharField(max_length=100)  # MIME type
    uploaded_at = DateTimeField()
```

### 6. Advanced Features

#### Message Pinning
Pin important messages to channel header for quick access.

```python
# Admin pins critical message
message.is_pinned = True
message.pinned_by = request.user
message.save()

# Show pinned messages in channel header
pinned = Channel.objects.get(id=channel_id).messages.filter(is_pinned=True)
```

#### Message Search
Search messages across channels by content.

```python
# Search within channel
messages = ChannelMessage.objects.filter(
    channel=channel,
    content__icontains="search_term"
)

# API Endpoint
GET /api/channels/{channel_id}/messages/search/?q=python
```

#### Channel Search
Find channels by name/description.

```python
channels = Channel.objects.filter(
    Q(name__icontains="query") | Q(description__icontains="query")
)
```

#### Unread Message Tracking
Show unread count per channel.

```python
# Get unread count
member = ChannelMember.objects.get(channel=channel, user=user)
unread = channel.messages.filter(
    created_at__gt=member.last_read_at,
    thread_root__isnull=True  # Only count root messages
).count()
```

#### Notification Muting
Allow users to mute channel notifications.

```python
member.mute_notifications = True
member.save()

# Check before sending notification
if not member.mute_notifications:
    Notification.objects.create(...)
```

---

## API Endpoints

### Channel Management
```
POST   /api/channels/                  Create channel
GET    /api/channels/                  List channels
GET    /api/channels/{id}/             Get channel details
PATCH  /api/channels/{id}/             Update channel
DELETE /api/channels/{id}/             Delete channel

POST   /api/channels/{id}/add_member/        Add member
POST   /api/channels/{id}/remove_member/     Remove member
GET    /api/channels/{id}/members/           List members
POST   /api/channels/{id}/leave/             Leave channel
POST   /api/channels/{id}/mute/              Mute notifications
```

### Messages
```
GET    /api/channels/{id}/messages/                List messages
POST   /api/channels/{id}/messages/                Create message
GET    /api/channels/{id}/messages/{msg_id}/      Get message
PATCH  /api/channels/{id}/messages/{msg_id}/      Edit message
DELETE /api/channels/{id}/messages/{msg_id}/      Delete message

POST   /api/channels/{id}/messages/{msg_id}/pin/         Pin message
POST   /api/channels/{id}/messages/{msg_id}/unpin/       Unpin message
GET    /api/channels/{id}/messages/{msg_id}/replies/     Get thread replies
GET    /api/channels/{id}/messages/search/?q=term        Search messages
```

### WebSocket
```
ws://localhost:8000/ws/channel/{channel_id}/

Message Types:
- type: 'message' → New message sent
- type: 'typing' → User is typing
- type: 'user_status' → User online/offline
- type: 'mention' → User was mentioned
```

---

## Implementation Timeline

### Phase 1: Core Infrastructure (Week 1)
- [ ] Add database models
- [ ] Create migrations
- [ ] Build API endpoints
- [ ] Implement WebSocket consumer
- [ ] Test basic messaging

### Phase 2: Advanced Features (Week 2)
- [ ] @mention system
- [ ] File sharing
- [ ] Thread discussions
- [ ] Search functionality
- [ ] Read status tracking

### Phase 3: UI/UX (Week 3)
- [ ] Channel list UI
- [ ] Message display component
- [ ] Thread reply UI
- [ ] File upload widget
- [ ] Mention autocomplete

### Phase 4: Polish (Week 4)
- [ ] Notifications integration
- [ ] Keyboard shortcuts
- [ ] Message reactions
- [ ] Performance optimization
- [ ] Mobile responsiveness

---

## Frontend Components

### 1. Channel Sidebar
```html
<div class="channel-list">
    {% for channel in channels %}
    <div class="channel-item" onclick="selectChannel({{ channel.id }})">
        #{{ channel.name }}
        {% if channel.unread_count %}
        <span class="badge">{{ channel.unread_count }}</span>
        {% endif %}
    </div>
    {% endfor %}
</div>
```

### 2. Message Area
```html
<div id="messages" class="message-list">
    <!-- Messages dynamically loaded -->
</div>
```

### 3. Input Area
```html
<form id="message-form">
    <textarea id="message-input" 
              placeholder="Type message... Use @name to mention"
              data-channel="{{ channel.id }}">
    </textarea>
    <button type="submit">Send</button>
    <input type="file" id="file-input" multiple>
</form>
```

### 4. JavaScript Integration
```javascript
// Connect to WebSocket
const socket = new WebSocket(`ws://.../ws/channel/${channelId}/`);

// Listen for messages
socket.onmessage = (event) => {
    const data = JSON.parse(event.data);
    if (data.type === 'message') {
        appendMessage(data.message);
    }
};

// Send message
document.getElementById('message-form').addEventListener('submit', (e) => {
    e.preventDefault();
    socket.send(JSON.stringify({
        type: 'message',
        content: document.getElementById('message-input').value
    }));
});
```

---

## Performance Considerations

### Database Optimization
```python
# Use select_related for foreign keys
ChannelMessage.objects.select_related('author', 'channel')

# Use prefetch_related for many-to-many
message.prefetch_related('mentions', 'files')

# Add database indexes
class ChannelMessage(models.Model):
    class Meta:
        indexes = [
            models.Index(fields=['channel', 'created_at']),
            models.Index(fields=['thread_root']),
            models.Index(fields=['author']),
        ]
```

### Caching
```python
# Cache channel list per project
cache.set(f'project_{project_id}_channels', channels, timeout=3600)

# Cache unread counts
cache.set(f'channel_{channel_id}_unread', unread_count, timeout=300)
```

### Pagination
```python
# Paginate messages (load 20 at a time)
from rest_framework.pagination import PageNumberPagination

class MessagePagination(PageNumberPagination):
    page_size = 20
    page_size_query_param = 'page_size'
    max_page_size = 100
```

### WebSocket Groups
```python
# Use channel groups to reduce broadcasting
await self.channel_layer.group_add(
    f'channel_{channel_id}',  # Group name
    self.channel_name          # This connection
)

# Only broadcast to relevant group
await self.channel_layer.group_send(
    f'channel_{channel_id}',   # Only subscribers
    {'type': 'message.send', 'data': {...}}
)
```

---

## Security & Permissions

### Access Control
```python
class IsChannelMember(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        return ChannelMember.objects.filter(
            channel=obj,
            user=request.user
        ).exists()

class IsChannelAdmin(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        return ChannelMember.objects.filter(
            channel=obj,
            user=request.user,
            role__in=['owner', 'moderator']
        ).exists()
```

### Message Validation
```python
# Prevent empty messages
if not content.strip():
    raise ValidationError("Message cannot be empty")

# File size limit (10MB)
if file.size > 10 * 1024 * 1024:
    raise ValidationError("File too large")

# Rate limiting
from django.core.cache import cache
if cache.get(f'rate_limit_{user_id}'):
    raise RateLimited("Too many messages")
```

### CSRF Protection
```python
# All POST requests require CSRF token
@csrf_protect
def create_message(request):
    # Handle request
```

---

## Testing

### Unit Tests
```python
from django.test import TestCase

class ChannelTestCase(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='john')
        self.project = Project.objects.create(user=self.user, title='App')
        self.channel = Channel.objects.create(
            project=self.project,
            name='general',
            created_by=self.user
        )
    
    def test_channel_creation(self):
        self.assertEqual(self.channel.name, 'general')
        self.assertTrue(self.channel.project.id)
    
    def test_add_member(self):
        user2 = User.objects.create_user(username='jane')
        ChannelMember.objects.create(channel=self.channel, user=user2)
        self.assertTrue(self.channel.members.filter(user=user2).exists())
    
    def test_create_message(self):
        message = ChannelMessage.objects.create(
            channel=self.channel,
            author=self.user,
            content='Hello'
        )
        self.assertEqual(message.content, 'Hello')
        self.assertEqual(message.author.username, 'john')
```

### WebSocket Tests
```python
from channels.testing import WebsocketCommunicator
import asyncio

class ChannelChatTestCase(TestCase):
    async def test_websocket_connection(self):
        communicator = WebsocketCommunicator(
            ChannelChatConsumer.as_asgi(),
            "/ws/channel/1/"
        )
        connected, _ = await communicator.connect()
        self.assertTrue(connected)
        await communicator.disconnect()
```

---

## Deployment Checklist

- [ ] Run migrations: `python manage.py migrate`
- [ ] Collect static files: `python manage.py collectstatic`
- [ ] Test WebSocket with Daphne
- [ ] Configure Redis for channel layer
- [ ] Set up SSL/TLS for WSS
- [ ] Configure ALLOWED_HOSTS
- [ ] Enable CSRF protection
- [ ] Set up email notifications
- [ ] Test file uploads
- [ ] Monitor WebSocket connections
- [ ] Set up logging for errors
- [ ] Performance test with load

---

## Related Features

This feature integrates with:
- **Project Management** (chat in projects)
- **Activity Feed** (mention notifications)
- **User Profiles** (@mention autocomplete)
- **File Management** (file sharing)
- **Notifications** (@mention alerts)

---

## Success Metrics

| Metric | Target |
|--------|--------|
| **Channel Adoption** | 80% of projects have channels |
| **Message Throughput** | 1000 msgs/sec per channel |
| **WebSocket Latency** | <100ms message delivery |
| **User Engagement** | 70% weekly active in channels |
| **File Upload Success** | 99% uptime |
| **Search Performance** | <500ms for large channels |

---

## Documentation Files

1. **TEAM_CHAT_CHANNELS_IMPLEMENTATION.md** - Full technical guide
2. **TEAM_CHAT_QUICK_START.md** - 15-minute quick start
3. **FEATURE_6_SUMMARY_TEAM_CHAT.md** - This file

---

## Next Steps

1. Review full implementation guide
2. Follow quick start (15 mins)
3. Test locally with Daphne
4. Deploy to staging
5. Load test with multiple users
6. Deploy to production

**Estimated Implementation: 2-3 weeks for complete feature with Polish**

---

This completes the **Team Chat Channels** feature specification. Ready to implement! 🚀
