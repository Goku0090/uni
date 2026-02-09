# UniSinq Code Implementation Reference Guide

## Quick Reference - Key Code Examples

### 1. OTP Authentication Flow

#### Backend: Generate OTP
```python
# accounts/views.py
from .models import OTP
from django.core.mail import send_mail

@csrf_exempt
def send_otp(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        purpose = request.POST.get('purpose')  # 'login', 'registration', 'reset'
        
        # Generate OTP
        otp_obj = OTP.generate_otp(email, purpose)
        
        # Send email
        subject = f"Your {purpose.title()} OTP: {otp_obj.otp_code}"
        message = f"Your OTP is {otp_obj.otp_code}. Valid for 5 minutes."
        send_mail(subject, message, 'noreply@unisinq.com', [email])
        
        return JsonResponse({'message': 'OTP sent to email', 'otp_id': otp_obj.id})
```

#### Backend: Verify OTP
```python
@csrf_exempt
def verify_otp(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        otp_code = request.POST.get('otp_code')
        purpose = request.POST.get('purpose')
        
        # Get OTP
        otp = OTP.objects.filter(email=email, purpose=purpose).latest('created_at')
        
        # Verify
        is_valid, message = otp.verify_otp(otp_code)
        
        if is_valid:
            if purpose == 'registration':
                # Create new user
                user = User.objects.create_user(
                    username=email,
                    email=email,
                    password=request.POST.get('password')
                )
                StudentProfile.objects.create(user=user)
            elif purpose == 'login':
                user = User.objects.get(email=email)
            
            # Create JWT token
            token = generate_jwt_token(user)
            return JsonResponse({'token': token, 'user': UserSerializer(user).data})
        else:
            return JsonResponse({'error': message}, status=400)
```

#### Frontend: Send OTP
```javascript
// staticfiles/js/login.js
async function sendOTP(email, purpose) {
    const response = await fetch('/auth/send-otp/', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
            'X-CSRFToken': getCookie('csrftoken'),
        },
        body: JSON.stringify({ email, purpose })
    });
    return await response.json();
}

// Display OTP input
document.getElementById('send-otp-btn').onclick = async () => {
    const email = document.getElementById('email').value;
    const result = await sendOTP(email, 'login');
    if (result.message) {
        alert('OTP sent! Check your email.');
        document.getElementById('otp-input-section').style.display = 'block';
    }
};
```

#### Frontend: Verify OTP
```javascript
async function verifyOTP(email, otpCode, purpose) {
    const response = await fetch('/auth/verify-otp/', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
            'X-CSRFToken': getCookie('csrftoken'),
        },
        body: JSON.stringify({ email, otp_code: otpCode, purpose })
    });
    const data = await response.json();
    if (data.token) {
        localStorage.setItem('token', data.token);
        window.location.href = '/dashboard/';
    } else {
        alert(data.error);
    }
}

document.getElementById('verify-otp-btn').onclick = () => {
    const email = document.getElementById('email').value;
    const otpCode = document.getElementById('otp-code').value;
    verifyOTP(email, otpCode, 'login');
};
```

---

### 2. Project Creation with Real-Time Updates

#### Backend: Create Project
```python
# accounts/views.py
from django.views.decorators.http import require_http_methods
from .models import Project, ProjectMember, Activity
from .serializers import ProjectSerializer
import json

@require_http_methods(['POST'])
@login_required
def create_project(request):
    data = json.loads(request.body)
    
    # Create project
    project = Project.objects.create(
        user=request.user,
        title=data.get('title'),
        description=data.get('description'),
        category=data.get('category'),
        technologies=data.get('technologies', []),
        looking_for=data.get('looking_for', []),
        github_link=data.get('github_link'),
    )
    
    # Auto-add creator as owner
    ProjectMember.objects.create(
        project=project,
        user=request.user,
        role='owner'
    )
    
    # Create activity
    Activity.objects.create(
        user=request.user,
        activity_type='project_created',
        title=f"Created project '{project.title}'",
        description=project.description,
        project=project,
        is_public=True
    )
    
    # Broadcast to activity feed via WebSocket
    from channels.layers import get_channel_layer
    import asyncio
    channel_layer = get_channel_layer()
    asyncio.create_task(channel_layer.group_send(
        f'activity_feed_{request.user.id}',
        {
            'type': 'activity.notification',
            'activity_type': 'project.created',
            'project_id': project.id,
            'project_title': project.title,
            'actor': request.user.username,
            'timestamp': timezone.now().isoformat(),
        }
    ))
    
    return JsonResponse({
        'message': 'Project created successfully',
        'project': ProjectSerializer(project).data
    })
```

#### Frontend: Project Creation with Form
```html
<!-- accounts/templates/create_project.html -->
<form id="project-form">
    <input type="text" id="title" placeholder="Project Title" required>
    <textarea id="description" placeholder="Description" required></textarea>
    
    <select id="category">
        <option value="web">Web Development</option>
        <option value="mobile">Mobile Apps</option>
        <option value="ai">AI/ML</option>
        <!-- ... -->
    </select>
    
    <div id="technologies-input">
        <input type="text" placeholder="Add technology (e.g., React, Node.js)">
        <button type="button" onclick="addTechnology()">Add</button>
        <div id="technologies-list"></div>
    </div>
    
    <button type="submit">Create Project</button>
</form>

<script>
let technologies = [];

function addTechnology() {
    const input = document.querySelector('#technologies-input input');
    const tech = input.value.trim();
    if (tech) {
        technologies.push(tech);
        updateTechList();
        input.value = '';
    }
}

function updateTechList() {
    const list = document.getElementById('technologies-list');
    list.innerHTML = technologies
        .map(t => `<span class="tech-tag">${t} <button type="button" onclick="removeTech('${t}')">×</button></span>`)
        .join('');
}

document.getElementById('project-form').onsubmit = async (e) => {
    e.preventDefault();
    
    const projectData = {
        title: document.getElementById('title').value,
        description: document.getElementById('description').value,
        category: document.getElementById('category').value,
        technologies: technologies,
        looking_for: [],
    };
    
    const response = await fetch('/api/projects/', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
            'X-CSRFToken': getCookie('csrftoken'),
        },
        body: JSON.stringify(projectData)
    });
    
    if (response.ok) {
        alert('Project created!');
        window.location.href = '/dashboard/';
    }
};
</script>
```

---

### 3. WebSocket Real-Time Comments

#### Backend: ProjectUpdateConsumer
```python
# accounts/consumers.py
from channels.generic.websocket import AsyncWebsocketConsumer
from channels.db import database_sync_to_async
import json

class ProjectUpdateConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        # Extract project_id from URL: ws://localhost/ws/project/2/
        self.project_id = self.scope['url_route']['kwargs']['project_id']
        self.project_group_name = f'project_{self.project_id}'
        
        # Join group
        await self.channel_layer.group_add(
            self.project_group_name,
            self.channel_name
        )
        
        await self.accept()
        
        # Send initial project data
        project_data = await self.get_project_data()
        await self.send(text_data=json.dumps({
            'type': 'project.initial_data',
            'data': project_data
        }))

    async def disconnect(self, close_code):
        await self.channel_layer.group_discard(
            self.project_group_name,
            self.channel_name
        )

    async def receive(self, text_data):
        data = json.loads(text_data)
        message_type = data.get('type')
        
        if message_type == 'comment.post':
            comment_text = data.get('text')
            await self.handle_new_comment(comment_text)

    async def project_comment_posted(self, event):
        """Receive comment notification from group"""
        await self.send(text_data=json.dumps({
            'type': 'project.comment_posted',
            'comment_id': event['comment_id'],
            'author': event.get('author'),
            'text': event.get('text'),
            'timestamp': event.get('timestamp'),
        }))

    @database_sync_to_async
    def handle_new_comment(self, comment_text):
        from .models import Comment, Project
        
        project = Project.objects.get(id=self.project_id)
        comment = Comment.objects.create(
            project=project,
            user=self.scope['user'],
            content=comment_text
        )
        
        # Broadcast to all connected clients
        import asyncio
        asyncio.create_task(self.channel_layer.group_send(
            self.project_group_name,
            {
                'type': 'project.comment_posted',
                'comment_id': comment.id,
                'author': self.scope['user'].username,
                'text': comment_text,
                'timestamp': timezone.now().isoformat(),
            }
        ))
```

#### Routing: Connect WebSocket
```python
# accounts/routing.py
from django.urls import re_path
from . import consumers

websocket_urlpatterns = [
    re_path(r'ws/project/(?P<project_id>\w+)/$', consumers.ProjectUpdateConsumer.as_asgi()),
    re_path(r'ws/activity/$', consumers.ActivityFeedConsumer.as_asgi()),
    re_path(r'ws/notifications/$', consumers.NotificationConsumer.as_asgi()),
]
```

#### Frontend: WebSocket Connection
```javascript
// staticfiles/js/realtime-updates.js
class ProjectWebSocket {
    constructor(projectId) {
        this.projectId = projectId;
        this.socket = null;
        this.connect();
    }
    
    connect() {
        const protocol = window.location.protocol === 'https:' ? 'wss' : 'ws';
        const wsUrl = `${protocol}://${window.location.host}/ws/project/${this.projectId}/`;
        
        this.socket = new WebSocket(wsUrl);
        
        this.socket.onopen = (e) => {
            console.log('✅ WebSocket connected to project');
        };
        
        this.socket.onmessage = (e) => {
            const data = JSON.parse(e.data);
            this.handleMessage(data);
        };
        
        this.socket.onerror = (e) => {
            console.error('❌ WebSocket error:', e);
        };
        
        this.socket.onclose = (e) => {
            console.log('WebSocket closed, reconnecting in 3s...');
            setTimeout(() => this.connect(), 3000);
        };
    }
    
    handleMessage(data) {
        if (data.type === 'project.comment_posted') {
            this.addCommentToUI(data);
        } else if (data.type === 'project.member_added') {
            this.addMemberToUI(data);
        }
    }
    
    addCommentToUI(data) {
        const comment = document.createElement('div');
        comment.className = 'comment';
        comment.innerHTML = `
            <strong>${data.author}</strong>
            <p>${data.text}</p>
            <small>${new Date(data.timestamp).toLocaleTimeString()}</small>
        `;
        document.getElementById('comments-list').appendChild(comment);
    }
    
    postComment(text) {
        this.socket.send(JSON.stringify({
            type: 'comment.post',
            text: text
        }));
    }
}

// Usage
const ws = new ProjectWebSocket(projectId);

document.getElementById('comment-form').onsubmit = (e) => {
    e.preventDefault();
    const text = document.getElementById('comment-input').value;
    ws.postComment(text);
    document.getElementById('comment-input').value = '';
};
```

#### Template: Display Comments with WebSocket
```html
<!-- accounts/templates/project_detail.html -->
<div class="comments-section">
    <h3>Comments</h3>
    <div id="comments-list">
        {% for comment in project.comments.all %}
        <div class="comment">
            <strong>{{ comment.user.username }}</strong>
            <p>{{ comment.content }}</p>
            <small>{{ comment.created_at|date:"Y-m-d H:i" }}</small>
        </div>
        {% endfor %}
    </div>
    
    <form id="comment-form">
        {% csrf_token %}
        <textarea id="comment-input" placeholder="Add a comment..." required></textarea>
        <button type="submit">Post Comment</button>
    </form>
</div>

<script>
const projectId = {{ project.id }};
const ws = new ProjectWebSocket(projectId);
</script>
```

---

### 4. Messaging with Read Receipts

#### Backend: Create Message
```python
# accounts/chat_api_improved.py
from rest_framework import viewsets
from rest_framework.decorators import action
from .models import ChatRoom, Message, MessageReadStatus
from .serializers import MessageSerializer

class MessageViewSet(viewsets.ModelViewSet):
    queryset = Message.objects.all()
    serializer_class = MessageSerializer

    @action(detail=False, methods=['post'])
    def create_message(self, request):
        chat_room_id = request.data.get('chat_room_id')
        content = request.data.get('content')
        
        chat_room = ChatRoom.objects.get(id=chat_room_id)
        message = Message.objects.create(
            sender=request.user,
            chat_room=chat_room,
            content=content,
            message_type='text'
        )
        
        # Mark as read by sender
        message.mark_as_read_by(request.user)
        
        # Broadcast via WebSocket
        from channels.layers import get_channel_layer
        import asyncio
        
        channel_layer = get_channel_layer()
        asyncio.create_task(channel_layer.group_send(
            f'chat_room_{chat_room_id}',
            {
                'type': 'message.new',
                'message_id': message.id,
                'sender': request.user.username,
                'content': content,
                'timestamp': message.created_at.isoformat(),
            }
        ))
        
        return JsonResponse({
            'message': 'Message sent',
            'data': MessageSerializer(message).data
        })

    @action(detail=True, methods=['put'])
    def mark_as_read(self, request, pk=None):
        message = self.get_object()
        message.mark_as_read_by(request.user)
        
        return JsonResponse({
            'message': 'Marked as read',
            'read_count': message.get_read_count()
        })

    @action(detail=True, methods=['get'])
    def read_by(self, request, pk=None):
        message = self.get_object()
        users = message.get_read_by_users()
        
        return JsonResponse({
            'read_by': [
                {'id': u.id, 'username': u.username}
                for u in users
            ],
            'read_count': message.get_read_count()
        })
```

#### Frontend: Message UI with Read Status
```javascript
// staticfiles/js/messages-handlers.js
class ChatHandler {
    constructor(chatRoomId) {
        this.chatRoomId = chatRoomId;
        this.connectWebSocket();
    }
    
    connectWebSocket() {
        const protocol = window.location.protocol === 'https:' ? 'wss' : 'ws';
        this.socket = new WebSocket(
            `${protocol}://${window.location.host}/ws/chat/${this.chatRoomId}/`
        );
        
        this.socket.onmessage = (e) => {
            const data = JSON.parse(e.data);
            if (data.type === 'message.new') {
                this.displayMessage(data);
            } else if (data.type === 'message.read') {
                this.updateReadStatus(data);
            }
        };
    }
    
    displayMessage(data) {
        const messageDiv = document.createElement('div');
        messageDiv.className = 'message';
        messageDiv.id = `message-${data.message_id}`;
        messageDiv.innerHTML = `
            <div class="message-header">
                <strong>${data.sender}</strong>
                <small>${new Date(data.timestamp).toLocaleTimeString()}</small>
            </div>
            <div class="message-content">
                ${data.content}
            </div>
            <div class="message-status">
                <span class="read-status" data-msg-id="${data.message_id}">1 read</span>
            </div>
        `;
        
        const container = document.getElementById('messages-container');
        container.appendChild(messageDiv);
        
        // Auto-mark as read
        setTimeout(() => this.markMessageAsRead(data.message_id), 500);
    }
    
    markMessageAsRead(messageId) {
        fetch(`/api/chat/messages/${messageId}/read/`, {
            method: 'PUT',
            headers: {
                'X-CSRFToken': getCookie('csrftoken'),
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({})
        }).then(r => r.json()).then(data => {
            console.log(`Message ${messageId} marked as read (${data.read_count} users)`);
        });
    }
    
    updateReadStatus(data) {
        const el = document.querySelector(`[data-msg-id="${data.message_id}"]`);
        if (el) {
            el.textContent = `${data.read_count} read`;
        }
    }
    
    sendMessage(content) {
        fetch('/api/chat/rooms/' + this.chatRoomId + '/messages/', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'X-CSRFToken': getCookie('csrftoken'),
            },
            body: JSON.stringify({ content })
        });
    }
}

// Usage
const chat = new ChatHandler(roomId);

document.getElementById('send-btn').onclick = () => {
    const input = document.getElementById('message-input');
    chat.sendMessage(input.value);
    input.value = '';
};
```

---

### 5. User Profile with Photo Upload

#### Backend: Profile Upload
```python
# accounts/views.py
from django.shortcuts import get_object_or_404
from django.http import JsonResponse
from PIL import Image
import os

@login_required
def upload_profile_photo(request):
    if request.method == 'POST' and request.FILES:
        file = request.FILES['profile_photo']
        
        # Validate
        valid_extensions = ['jpg', 'jpeg', 'png', 'gif']
        ext = file.name.split('.')[-1].lower()
        
        if ext not in valid_extensions:
            return JsonResponse({'error': 'Invalid file type'}, status=400)
        
        if file.size > 5 * 1024 * 1024:  # 5MB
            return JsonResponse({'error': 'File too large'}, status=400)
        
        # Save to profile
        profile = request.user.student_profile
        profile.profile_photo = file
        profile.save()
        
        # Optimize image
        try:
            img = Image.open(profile.profile_photo.path)
            img.thumbnail((200, 200))
            img.save(profile.profile_photo.path, 'PNG', quality=85)
        except Exception as e:
            print(f"Image optimization error: {e}")
        
        return JsonResponse({
            'message': 'Photo uploaded successfully',
            'photo_url': profile.profile_photo.url
        })
```

#### Frontend: Profile Photo Upload
```html
<!-- accounts/templates/profile.html -->
<div class="profile-section">
    <div class="profile-photo">
        <img id="profile-img" src="{{ user.student_profile.profile_photo.url }}" alt="Profile">
        <input type="file" id="photo-input" accept="image/*" style="display:none;">
        <button onclick="document.getElementById('photo-input').click()">Change Photo</button>
    </div>
    
    <form id="profile-form">
        {% csrf_token %}
        <input type="text" name="full_name" value="{{ user.student_profile.full_name }}" placeholder="Full Name">
        <input type="text" name="college" value="{{ user.student_profile.college }}" placeholder="College">
        <textarea name="bio">{{ user.student_profile.bio }}</textarea>
        <button type="submit">Save Profile</button>
    </form>
</div>

<script>
document.getElementById('photo-input').onchange = async (e) => {
    const file = e.target.files[0];
    const formData = new FormData();
    formData.append('profile_photo', file);
    
    const response = await fetch('/user/profile/upload-photo/', {
        method: 'POST',
        headers: { 'X-CSRFToken': getCookie('csrftoken') },
        body: formData
    });
    
    if (response.ok) {
        const data = await response.json();
        document.getElementById('profile-img').src = data.photo_url;
        alert('Photo uploaded!');
    }
};

document.getElementById('profile-form').onsubmit = async (e) => {
    e.preventDefault();
    const formData = new FormData(e.target);
    
    const response = await fetch('/user/profile/', {
        method: 'PATCH',
        headers: { 'X-CSRFToken': getCookie('csrftoken') },
        body: formData
    });
    
    if (response.ok) {
        alert('Profile updated!');
    }
};
</script>
```

---

### 6. Search & Filter Collaborators

#### Backend: Collaborator Search
```python
# accounts/views.py
from django.db.models import Q
from .models import StudentProfile

@require_http_methods(['GET'])
def search_collaborators(request):
    query = request.GET.get('q', '').strip()
    college = request.GET.get('college', '').strip()
    interests = request.GET.get('interests', '').strip()
    skills = request.GET.get('skills', '').strip()
    
    # Start with all profiles
    profiles = StudentProfile.objects.filter(user__is_active=True)
    
    # Apply filters
    if query:
        profiles = profiles.filter(
            Q(full_name__icontains=query) |
            Q(user__username__icontains=query) |
            Q(bio__icontains=query)
        )
    
    if college:
        profiles = profiles.filter(
            Q(college__icontains=college) |
            Q(other_college__icontains=college)
        )
    
    if interests:
        profiles = profiles.filter(interests__contains=[interests])
    
    if skills:
        profiles = profiles.filter(skills__contains=[skills])
    
    # Exclude current user
    profiles = profiles.exclude(user=request.user)
    
    # Serialize
    from .serializers import StudentProfileSerializer
    serializer = StudentProfileSerializer(profiles, many=True)
    
    return JsonResponse({
        'count': profiles.count(),
        'results': serializer.data
    })
```

#### Frontend: Search UI
```html
<!-- accounts/templates/find_collaborators.html -->
<div class="search-section">
    <input type="text" id="search-input" placeholder="Search by name or skills...">
    
    <div class="filters">
        <input type="text" id="college-filter" placeholder="College">
        
        <select id="interests-filter" multiple>
            <option value="ai">AI/ML</option>
            <option value="web">Web Dev</option>
            <option value="mobile">Mobile</option>
            <!-- ... -->
        </select>
        
        <button onclick="performSearch()">Search</button>
    </div>
    
    <div id="results-container"></div>
</div>

<script>
async function performSearch() {
    const query = document.getElementById('search-input').value;
    const college = document.getElementById('college-filter').value;
    const interests = document.getElementById('interests-filter').value;
    
    const url = `/search/collaborators/?q=${query}&college=${college}&interests=${interests}`;
    const response = await fetch(url);
    const data = await response.json();
    
    displayResults(data.results);
}

function displayResults(profiles) {
    const container = document.getElementById('results-container');
    container.innerHTML = profiles.map(p => `
        <div class="collaborator-card">
            <img src="${p.profile_photo}" alt="Profile">
            <h3>${p.full_name || p.username}</h3>
            <p>${p.bio}</p>
            <p>College: ${p.college}</p>
            <p>Skills: ${p.skills.join(', ')}</p>
            <button onclick="connectWith('${p.user_id}')">Connect</button>
        </div>
    `).join('');
}
</script>
```

---

## Common Error Handling Patterns

### OTP Errors
```python
if not otp.is_valid():
    return JsonResponse({'error': 'OTP has expired or is invalid.'}, status=400)

if otp_code != otp.otp_code:
    return JsonResponse({'error': 'Invalid OTP code.'}, status=400)
```

### Permission Errors
```python
if project.user != request.user:
    return JsonResponse({'error': 'Only project owner can do this.'}, status=403)

if not ProjectMember.objects.filter(project=project, user=request.user, role__in=['owner', 'admin']).exists():
    return JsonResponse({'error': 'Insufficient permissions.'}, status=403)
```

### Model Not Found
```python
try:
    project = Project.objects.get(id=project_id)
except Project.DoesNotExist:
    return JsonResponse({'error': 'Project not found.'}, status=404)
```

### WebSocket Error Handling
```python
async def send_error(self, error_message):
    await self.send(text_data=json.dumps({
        'type': 'error',
        'message': error_message,
    }))
```

---

## CSRF Token Helper

```javascript
// staticfiles/js/api-utils.js
function getCookie(name) {
    let cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        const cookies = document.cookie.split(';');
        for (let i = 0; i < cookies.length; i++) {
            const cookie = cookies[i].trim();
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}

// Usage in all API calls
headers: {
    'X-CSRFToken': getCookie('csrftoken'),
    'Content-Type': 'application/json'
}
```

---

## Database Query Optimization Tips

### Use `select_related()` for ForeignKey
```python
# Instead of:
comments = Comment.objects.all()  # N+1 query problem

# Use:
comments = Comment.objects.select_related('user', 'project')
```

### Use `prefetch_related()` for M2M
```python
# Instead of:
projects = Project.objects.all()
for p in projects:
    print(p.members.all())  # N+1 query

# Use:
projects = Project.objects.prefetch_related('members')
```

### Use `only()` and `defer()` to limit fields
```python
# Get only specific fields
profiles = StudentProfile.objects.only('full_name', 'college')

# Defer expensive fields
projects = Project.objects.defer('description')
```

---

## Deployment Checklist

- [ ] Set `DEBUG = False`
- [ ] Generate new `SECRET_KEY`
- [ ] Configure `ALLOWED_HOSTS`
- [ ] Set up PostgreSQL database
- [ ] Configure Redis for channels
- [ ] Set up email service (Brevo/ZeptoMail)
- [ ] Configure social auth (Google/GitHub)
- [ ] Run `python manage.py migrate`
- [ ] Run `python manage.py collectstatic`
- [ ] Start Daphne: `daphne -b 0.0.0.0 -p 8000 auth_project.asgi:application`
- [ ] Configure Nginx reverse proxy
- [ ] Set up SSL certificate
- [ ] Enable CSRF protection
- [ ] Configure CORS if needed

---

## Testing Tips

### Test OTP
```python
# test_otp.py
from django.test import TestCase
from .models import OTP

class OTPTestCase(TestCase):
    def test_otp_generation(self):
        otp = OTP.generate_otp('test@example.com', 'login')
        self.assertEqual(len(otp.otp_code), 6)
        self.assertTrue(otp.is_valid())
    
    def test_otp_expiry(self):
        otp = OTP.generate_otp('test@example.com', 'login')
        otp.expires_at = timezone.now() - timedelta(minutes=1)
        otp.save()
        self.assertFalse(otp.is_valid())
```

### Test Project Creation
```python
def test_create_project(self):
    user = User.objects.create_user('test', 'test@example.com', 'password')
    project = Project.objects.create(
        user=user,
        title='Test Project',
        description='Test'
    )
    self.assertEqual(project.user, user)
```

---

This reference guide covers the most important code patterns in UniSinq. Use it as a template for understanding the architecture and implementing similar features.
