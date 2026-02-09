# UniSync - Quick Code Reference & Patterns

## Common Code Patterns

### 1. Creating a New Project

```python
# views.py
@login_required
def post_project(request):
    if request.method == 'POST':
        form = ProjectForm(request.POST, request.FILES)
        if form.is_valid():
            project = form.save(commit=False)
            project.user = request.user
            project.save()
            
            # Auto-add creator as owner
            ProjectMember.objects.create(
                project=project,
                user=request.user,
                role='owner'
            )
            
            return redirect('project_detail', project_id=project.id)
    else:
        form = ProjectForm()
    return render(request, 'post_project.html', {'form': form})
```

### 2. Fetching Project Details with Optimization

```python
# views.py - Optimized query
from django.shortcuts import get_object_or_404
from django.db.models import Count, Prefetch

def project_detail(request, project_id):
    project = get_object_or_404(
        Project.objects
            .select_related('user__student_profile')  # Avoid N+1
            .prefetch_related(
                Prefetch('members', 
                    queryset=ProjectMember.objects
                        .select_related('user__student_profile')
                ),
                Prefetch('comments',
                    queryset=Comment.objects
                        .select_related('user')
                        .order_by('-created_at')
                ),
                'likes'
            ),
        id=project_id
    )
    
    context = {
        'project': project,
        'is_owner': project.user == request.user,
        'is_member': ProjectMember.objects.filter(
            project=project, 
            user=request.user
        ).exists(),
        'comments_count': project.comments.count(),
        'members_count': project.members.count(),
    }
    return render(request, 'project_detail.html', context)
```

### 3. API Serializer with Nested Data

```python
# serializers.py
from rest_framework import serializers
from .models import Project, ProjectMember, Comment

class ProjectMemberSerializer(serializers.ModelSerializer):
    user = UserProfileSerializer(read_only=True)
    
    class Meta:
        model = ProjectMember
        fields = ['id', 'user', 'role', 'joined_at']

class ProjectSerializer(serializers.ModelSerializer):
    owner = UserProfileSerializer(
        source='user',  # Maps 'user' field to 'owner'
        read_only=True
    )
    members = ProjectMemberSerializer(many=True, read_only=True)
    comments_count = serializers.SerializerMethodField()
    
    class Meta:
        model = Project
        fields = [
            'id', 'title', 'description', 'category',
            'owner', 'members', 'status', 'visibility',
            'created_at', 'updated_at', 'comments_count'
        ]
    
    def get_comments_count(self, obj):
        return obj.comments.count()
```

### 4. Posting a Comment

```python
# views.py or API
@login_required
def post_comment(request, project_id):
    project = get_object_or_404(Project, id=project_id)
    
    if request.method == 'POST':
        content = request.POST.get('content', '').strip()
        parent_id = request.POST.get('parent_comment')
        
        if not content:
            messages.error(request, 'Comment cannot be empty')
            return redirect('project_detail', project_id=project_id)
        
        parent = None
        if parent_id:
            parent = get_object_or_404(Comment, id=parent_id, project=project)
        
        comment = Comment.objects.create(
            project=project,
            user=request.user,
            content=content,
            parent_comment=parent
        )
        
        # Trigger real-time update via WebSocket signal
        # Signal handler in signals_realtime.py will broadcast this
        
        messages.success(request, 'Comment posted!')
        return redirect('project_detail', project_id=project_id)
```

### 5. Real-Time Update via WebSocket

```python
# signals_realtime.py
from django.db.models.signals import post_save
from django.dispatch import receiver
from channels.layers import get_channel_layer
import json

@receiver(post_save, sender=Comment)
def comment_created_signal(sender, instance, created, **kwargs):
    if created:  # Only on creation
        channel_layer = get_channel_layer()
        
        # Broadcast to project group
        group_name = f'project_{instance.project.id}'
        
        message_data = {
            'type': 'comment_added',
            'comment': {
                'id': instance.id,
                'user': instance.user.username,
                'content': instance.content,
                'created_at': str(instance.created_at),
            }
        }
        
        # Send to all consumers in this project group
        async_to_sync(channel_layer.group_send)(
            group_name,
            {
                'type': 'notify_comment',  # Maps to notify_comment method
                'data': message_data,
            }
        )
```

### 6. WebSocket Consumer

```python
# consumers.py
from channels.generic.websocket import AsyncWebsocketConsumer
import json

class ProjectUpdateConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.project_id = self.scope['url_route']['kwargs']['project_id']
        self.group_name = f'project_{self.project_id}'
        
        # Join group
        await self.channel_layer.group_add(
            self.group_name,
            self.channel_name
        )
        
        await self.accept()
        print(f"✅ Connected to {self.group_name}")
    
    async def disconnect(self, code):
        await self.channel_layer.group_discard(
            self.group_name,
            self.channel_name
        )
        print(f"❌ Disconnected from {self.group_name}")
    
    async def notify_comment(self, event):
        """
        Broadcast handler - called when group_send message arrives
        """
        data = event['data']
        
        # Send to WebSocket
        await self.send(text_data=json.dumps(data))
```

### 7. Client-Side WebSocket

```javascript
// static/js/realtime-updates.js

class ProjectWebSocket {
    constructor(projectId) {
        this.projectId = projectId;
        this.socket = null;
        this.reconnectAttempts = 0;
        this.maxReconnectAttempts = 5;
        this.reconnectDelay = 1000;
    }
    
    connect() {
        const protocol = window.location.protocol === 'https:' ? 'wss' : 'ws';
        const url = `${protocol}://${window.location.host}/ws/project/${this.projectId}/`;
        
        this.socket = new WebSocket(url);
        
        this.socket.onopen = () => {
            console.log('✅ WebSocket connected');
            this.reconnectAttempts = 0;
        };
        
        this.socket.onmessage = (e) => {
            const data = JSON.parse(e.data);
            this.handleMessage(data);
        };
        
        this.socket.onerror = (error) => {
            console.error('❌ WebSocket error:', error);
        };
        
        this.socket.onclose = () => {
            console.log('WebSocket closed. Reconnecting...');
            this.reconnect();
        };
    }
    
    handleMessage(data) {
        switch(data.type) {
            case 'comment_added':
                this.addCommentToDOM(data.comment);
                break;
            case 'member_added':
                this.addMemberToDOM(data.member);
                break;
            default:
                console.log('Unknown message type:', data.type);
        }
    }
    
    addCommentToDOM(comment) {
        const commentsContainer = document.getElementById('comments');
        const commentElement = document.createElement('div');
        commentElement.className = 'comment';
        commentElement.innerHTML = `
            <strong>${comment.user}</strong>
            <p>${comment.content}</p>
            <small>${comment.created_at}</small>
        `;
        commentsContainer.appendChild(commentElement);
    }
    
    reconnect() {
        if (this.reconnectAttempts < this.maxReconnectAttempts) {
            this.reconnectAttempts++;
            setTimeout(() => this.connect(), this.reconnectDelay);
        }
    }
}

// Initialize
document.addEventListener('DOMContentLoaded', () => {
    const projectId = document.getElementById('project-id').value;
    const ws = new ProjectWebSocket(projectId);
    ws.connect();
});
```

### 8. Handling Comments with Likes

```python
# models.py
class Comment(models.Model):
    project = models.ForeignKey(Project, on_delete=models.CASCADE, related_name='comments')
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    content = models.TextField()
    parent_comment = models.ForeignKey('self', null=True, blank=True, on_delete=models.CASCADE, related_name='replies')
    likes_count = models.PositiveIntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def like(self, user):
        """Like this comment"""
        obj, created = CommentLike.objects.get_or_create(
            comment=self,
            user=user
        )
        if created:
            self.likes_count += 1
            self.save()
        return created
    
    def unlike(self, user):
        """Unlike this comment"""
        deleted_count, _ = CommentLike.objects.filter(
            comment=self,
            user=user
        ).delete()
        
        if deleted_count > 0:
            self.likes_count = max(0, self.likes_count - 1)
            self.save()
        return deleted_count > 0

class CommentLike(models.Model):
    comment = models.ForeignKey(Comment, on_delete=models.CASCADE, related_name='comment_likes')
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        unique_together = ['comment', 'user']
```

### 9. Search & Filtering

```python
# views.py
from django.db.models import Q

def search_projects(request):
    query = request.GET.get('q', '')
    category = request.GET.get('category', '')
    visibility = request.GET.get('visibility', '')
    
    projects = Project.objects.all()
    
    # Text search
    if query:
        projects = projects.filter(
            Q(title__icontains=query) |
            Q(description__icontains=query) |
            Q(collaboration_needs__icontains=query)
        )
    
    # Category filter
    if category:
        projects = projects.filter(category=category)
    
    # Visibility filter
    if visibility in ['public', 'private', 'team-only']:
        projects = projects.filter(visibility=visibility)
    
    # Pagination
    paginator = Paginator(projects.order_by('-created_at'), 10)
    page = request.GET.get('page')
    page_obj = paginator.get_page(page)
    
    return render(request, 'search_results.html', {
        'page_obj': page_obj,
        'query': query,
        'categories': Project.CATEGORY_CHOICES,
    })
```

### 10. Sending Emails

```python
# views.py
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string

def send_welcome_email(user):
    subject = f'Welcome to UniSync, {user.username}!'
    
    # Prepare email context
    context = {
        'user': user,
        'activation_url': f'https://yoursite.com/dashboard/',
    }
    
    # Render HTML template
    html_content = render_to_string('emails/welcome.html', context)
    text_content = f'Welcome {user.username}!'
    
    # Create email
    email = EmailMultiAlternatives(
        subject=subject,
        body=text_content,
        from_email=settings.DEFAULT_FROM_EMAIL,
        to=[user.email]
    )
    
    # Attach HTML version
    email.attach_alternative(html_content, "text/html")
    
    # Send
    email.send()

# Or use the simplified send_mail
from django.core.mail import send_mail

send_mail(
    'OTP Code',
    f'Your OTP code is: {otp_code}',
    settings.DEFAULT_FROM_EMAIL,
    [user.email],
    fail_silently=False,
)
```

### 11. Generating OTP

```python
# models.py
@classmethod
def generate_otp(cls, email, purpose):
    import random
    import string
    
    # Generate 6-digit code
    otp_code = ''.join(random.choices(string.digits, k=6))
    
    # Expiry in 5 minutes
    expires_at = timezone.now() + timezone.timedelta(minutes=5)
    
    # Deactivate existing OTPs
    cls.objects.filter(email=email, purpose=purpose, is_used=False).update(is_used=True)
    
    # Create new OTP
    return cls.objects.create(
        email=email,
        otp_code=otp_code,
        purpose=purpose,
        expires_at=expires_at
    )

# Usage
otp_obj = OTP.generate_otp('user@example.com', 'login')
send_otp_email(otp_obj.email, otp_obj.otp_code)
```

### 12. Project Member Management

```python
# views.py
@login_required
def invite_to_project(request, project_id):
    project = get_object_or_404(Project, id=project_id, user=request.user)
    
    if request.method == 'POST':
        user_id = request.POST.get('user_id')
        role = request.POST.get('role', 'contributor')
        
        user = get_object_or_404(User, id=user_id)
        
        # Check if already member
        if ProjectMember.objects.filter(project=project, user=user).exists():
            messages.error(request, 'User is already a member')
            return redirect('project_detail', project_id=project_id)
        
        # Create invitation
        invitation = ProjectInvitation.objects.create(
            project=project,
            invited_user=user,
            invited_by=request.user,
            role=role,
            expires_at=timezone.now() + timezone.timedelta(days=7)
        )
        
        # Send email notification
        send_invitation_email(user.email, invitation)
        
        messages.success(request, f'Invitation sent to {user.username}')
        return redirect('project_detail', project_id=project_id)
```

### 13. Activity Feed

```python
# views.py
def activity_feed(request):
    user = request.user
    
    # Get activities from followed users
    followed_users = user.following.values_list('following_id', flat=True)
    
    activities = Activity.objects.filter(
        Q(user__in=followed_users) | Q(user=user),
        is_public=True
    ).select_related('user', 'project', 'target_user').order_by('-created_at')
    
    # Pagination
    paginator = Paginator(activities, 20)
    page = request.GET.get('page')
    page_obj = paginator.get_page(page)
    
    return render(request, 'activity_feed.html', {'page_obj': page_obj})

# Create activity on project creation
@receiver(post_save, sender=Project)
def log_project_creation(sender, instance, created, **kwargs):
    if created:
        Activity.objects.create(
            user=instance.user,
            activity_type='project_created',
            title=f'Created project: {instance.title}',
            project=instance,
            is_public=True
        )
```

### 14. Message Tracking

```python
# models.py
def mark_as_read(self, user):
    """Mark message as read by a user"""
    MessageReadStatus.objects.get_or_create(
        message=self,
        user=user,
        defaults={'read_at': timezone.now()}
    )

# views.py
def get_conversation(request, user_id):
    other_user = get_object_or_404(User, id=user_id)
    
    messages = Message.objects.filter(
        Q(sender=request.user, receiver=other_user) |
        Q(sender=other_user, receiver=request.user)
    ).select_related('sender', 'receiver').order_by('created_at')
    
    # Mark received messages as read
    for msg in messages.filter(receiver=request.user):
        msg.mark_as_read_by(request.user)
    
    return render(request, 'conversation.html', {
        'other_user': other_user,
        'messages': messages,
    })
```

### 15. Caching User Stats

```python
# views.py
from django.core.cache import cache

def dashboard(request):
    user = request.user
    
    # Try cache first
    stats = cache.get(f'user_stats_{user.id}')
    
    if stats is None:
        # Calculate if not cached
        stats = {
            'projects_created': Project.objects.filter(user=user).count(),
            'connections': Connection.objects.filter(
                Q(sender=user) | Q(receiver=user),
                status='accepted'
            ).count(),
            'followers': Follow.objects.filter(following=user).count(),
            'following': Follow.objects.filter(follower=user).count(),
        }
        
        # Cache for 5 minutes
        cache.set(f'user_stats_{user.id}', stats, 300)
    
    return render(request, 'dashboard.html', stats)

# Invalidate cache on change
@receiver(post_save, sender=ProjectMember)
def invalidate_stats_cache(sender, instance, **kwargs):
    cache.delete(f'user_stats_{instance.project.user.id}')
```

---

## Template Patterns

### Common Template Structure

```html
<!-- base.html -->
{% load static %}
<!DOCTYPE html>
<html>
<head>
    <title>{% block title %}UniSync{% endblock %}</title>
    {% csrf_token %}
    <script>
        const csrfToken = document.querySelector('[name=csrfmiddlewaretoken]').value;
    </script>
</head>
<body>
    {% include 'components/navbar.html' %}
    
    <div class="container">
        {% if messages %}
            {% for message in messages %}
                <div class="alert alert-{{ message.tags }}">
                    {{ message }}
                </div>
            {% endfor %}
        {% endif %}
        
        {% block content %}{% endblock %}
    </div>
    
    {% include 'components/footer.html' %}
    {% block js %}{% endblock %}
</body>
</html>
```

### Form Handling

```html
<!-- contact form -->
<form method="POST">
    {% csrf_token %}
    {{ form.as_p }}
    <button type="submit" class="btn btn-primary">Submit</button>
</form>
```

---

## Common Errors & Fixes

### WebSocket Connection Issues

```javascript
// Debug WebSocket
let socket = new WebSocket("ws://localhost:8000/ws/project/1/");

socket.onerror = (error) => {
    console.error("Error:", error);
    // Check: 1. Daphne running 2. URL correct 3. Auth working
};
```

### N+1 Query Problems

```python
# Bad - creates N queries
projects = Project.objects.all()
for p in projects:
    owner = p.user.username  # N queries

# Good - 1 query
projects = Project.objects.select_related('user').all()
for p in projects:
    owner = p.user.username
```

### Permission Denied

```python
@login_required
def edit_project(request, project_id):
    project = get_object_or_404(Project, id=project_id)
    
    # Check permission
    if project.user != request.user:
        messages.error(request, 'You cannot edit this project')
        return redirect('project_detail', project_id=project_id)
    
    # ... rest of view
```

---

This covers the most common patterns used throughout the UniSync codebase!
