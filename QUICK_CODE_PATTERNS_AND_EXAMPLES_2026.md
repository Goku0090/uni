# UniSync - Code Patterns & Examples (2026)

## Quick Reference for Common Tasks

---

## 1. Authentication Flow

### Login with OTP
```python
# views.py - Login View
def login_view(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')
        
        # Validate user exists
        try:
            user = User.objects.get(email=email)
        except User.DoesNotExist:
            messages.error(request, 'User not found')
            return redirect('login')
        
        # Generate OTP
        otp = OTP.generate_otp(email, purpose='login')
        
        # Send OTP via email
        send_mail(
            'Login OTP',
            f'Your OTP is: {otp.otp_code}',
            settings.DEFAULT_FROM_EMAIL,
            [email]
        )
        
        request.session['login_email'] = email
        return redirect('verify_otp', purpose='login')
    
    return render(request, 'login.html')
```

### Verify OTP
```python
def verify_otp_view(request, purpose):
    if request.method == 'POST':
        email = request.session.get('login_email')
        otp_code = request.POST.get('otp_code')
        
        # Retrieve and verify OTP
        try:
            otp = OTP.objects.get(email=email, purpose=purpose)
            is_valid, message = otp.verify_otp(otp_code)
            
            if is_valid:
                # Get or create user
                user, created = User.objects.get_or_create(email=email)
                
                if created:
                    # New user - redirect to profile setup
                    login(request, user)
                    return redirect('student_details')
                else:
                    # Existing user - login
                    login(request, user)
                    return redirect('dashboard')
            else:
                messages.error(request, message)
        except OTP.DoesNotExist:
            messages.error(request, 'Invalid OTP or expired')
    
    return render(request, 'verify_otp.html', {'purpose': purpose})
```

---

## 2. Profile Management

### Get User Profile
```python
# views.py
@login_required
def student_profile(request):
    profile = StudentProfile.objects.get(user=request.user)
    context = {
        'profile': profile,
        'skills': profile.skills,
        'interests': profile.interests,
    }
    return render(request, 'student_profile.html', context)
```

### Update User Profile
```python
@login_required
def edit_profile(request):
    profile = StudentProfile.objects.get(user=request.user)
    
    if request.method == 'POST':
        form = StudentProfileForm(request.POST, request.FILES, instance=profile)
        if form.is_valid():
            profile = form.save()
            profile.profile_completed = True
            profile.save()
            messages.success(request, 'Profile updated!')
            return redirect('student_profile')
    else:
        form = StudentProfileForm(instance=profile)
    
    return render(request, 'edit_profile.html', {'form': form})
```

### Serializer Pattern
```python
# serializers.py
class UserProfileSerializer(serializers.ModelSerializer):
    username = serializers.CharField(source='user.username', read_only=True)
    email = serializers.EmailField(source='user.email', read_only=True)
    
    class Meta:
        model = StudentProfile
        fields = ['id', 'username', 'email', 'full_name', 'college', 
                  'skills', 'interests', 'profile_photo', 'github', 'linkedin']

# views.py - REST API
class UserProfileView(generics.RetrieveUpdateAPIView):
    serializer_class = UserProfileSerializer
    permission_classes = [permissions.IsAuthenticated]
    
    def get_object(self):
        return self.request.user.student_profile
```

---

## 3. Project Management

### Create Project
```python
# views.py
@login_required
def post_project(request):
    if request.method == 'POST':
        form = ProjectForm(request.POST)
        if form.is_valid():
            project = form.save(commit=False)
            project.owner = request.user
            project.save()
            
            # Create notification for followers
            followers = Follow.objects.filter(following=request.user)
            for follow in followers:
                Notification.objects.create(
                    user=follow.follower,
                    actor=request.user,
                    action_type='new_project',
                    target_project=project,
                    content=f'{request.user.username} posted a new project'
                )
            
            messages.success(request, 'Project posted successfully!')
            return redirect('project_detail', project_id=project.id)
    else:
        form = ProjectForm()
    
    return render(request, 'post_project.html', {'form': form})
```

### Fetch Project with Comments
```python
# views.py
def project_detail(request, project_id):
    project = get_object_or_404(Project, id=project_id)
    
    # Apply visibility filter
    if not ProjectVisibilityFilter.can_view(project, request.user):
        raise Http404('Project not found')
    
    # Get comments with pagination
    paginator = Paginator(
        project.comments.all().order_by('-created_at'), 
        10
    )
    page_number = request.GET.get('page')
    comments = paginator.get_page(page_number)
    
    context = {
        'project': project,
        'comments': comments,
        'likes_count': project.likes.count(),
        'is_owner': project.owner == request.user,
    }
    return render(request, 'project_detail.html', context)
```

### Update Project
```python
@login_required
def edit_project(request, project_id):
    project = get_object_or_404(Project, id=project_id, owner=request.user)
    
    if request.method == 'POST':
        form = ProjectForm(request.POST, instance=project)
        if form.is_valid():
            form.save()
            # Log activity
            Activity.objects.create(
                user=request.user,
                action_type='edit_project',
                target_project=project
            )
            messages.success(request, 'Project updated!')
            return redirect('project_detail', project_id=project.id)
    else:
        form = ProjectForm(instance=project)
    
    return render(request, 'edit_project.html', {'form': form, 'project': project})
```

### Delete Project
```python
@login_required
def delete_project(request, project_id):
    project = get_object_or_404(Project, id=project_id, owner=request.user)
    
    if request.method == 'POST':
        project.delete()
        messages.success(request, 'Project deleted!')
        return redirect('dashboard')
    
    return render(request, 'confirm_delete.html', {'project': project})
```

---

## 4. Comments System

### Add Comment
```python
# comment_api.py
@login_required
@require_http_methods(['POST'])
def add_comment(request, project_id):
    project = get_object_or_404(Project, id=project_id)
    content = request.POST.get('content', '').strip()
    
    if not content:
        return JsonResponse({'error': 'Comment cannot be empty'}, status=400)
    
    # Create comment
    comment = Comment.objects.create(
        project=project,
        author=request.user,
        content=content
    )
    
    # Notify project owner
    if project.owner != request.user:
        Notification.objects.create(
            user=project.owner,
            actor=request.user,
            action_type='comment_project',
            target_project=project,
            content=f'{request.user.username} commented on your project'
        )
    
    return JsonResponse({
        'status': 'success',
        'comment': {
            'id': comment.id,
            'author': request.user.username,
            'content': comment.content,
            'created_at': comment.created_at.isoformat()
        }
    }, status=201)
```

### Get Comments (with pagination)
```python
@require_http_methods(['GET'])
def get_comments(request, project_id):
    project = get_object_or_404(Project, id=project_id)
    page = request.GET.get('page', 1)
    limit = request.GET.get('limit', 10)
    
    # Get paginated comments
    paginator = Paginator(
        project.comments.all().order_by('-created_at'), 
        int(limit)
    )
    page_obj = paginator.get_page(page)
    
    comments = [
        {
            'id': c.id,
            'author': c.author.username,
            'author_id': c.author.id,
            'profile_photo': c.author.student_profile.profile_photo.url,
            'content': c.content,
            'created_at': c.created_at.isoformat(),
            'can_edit': c.author == request.user
        }
        for c in page_obj
    ]
    
    return JsonResponse({
        'status': 'success',
        'data': comments,
        'pagination': {
            'page': page_obj.number,
            'total_pages': page_obj.paginator.num_pages,
            'total_count': page_obj.paginator.count
        }
    })
```

### Edit Comment
```python
@login_required
@require_http_methods(['POST'])
def edit_comment(request, comment_id):
    comment = get_object_or_404(Comment, id=comment_id, author=request.user)
    content = request.POST.get('content', '').strip()
    
    if not content:
        return JsonResponse({'error': 'Comment cannot be empty'}, status=400)
    
    comment.content = content
    comment.save()
    
    return JsonResponse({
        'status': 'success',
        'comment': {
            'id': comment.id,
            'content': comment.content,
            'updated_at': comment.updated_at.isoformat()
        }
    })
```

### Delete Comment
```python
@login_required
@require_http_methods(['DELETE'])
def delete_comment(request, comment_id):
    comment = get_object_or_404(Comment, id=comment_id, author=request.user)
    comment.delete()
    
    return JsonResponse({'status': 'success', 'message': 'Comment deleted'})
```

---

## 5. Social Features

### Send Connection Request
```python
# views.py
@login_required
@require_http_methods(['POST'])
def send_connection_request(request, user_id):
    target_user = get_object_or_404(User, id=user_id)
    
    if target_user == request.user:
        return JsonResponse({'error': 'Cannot connect with yourself'}, status=400)
    
    # Check if already connected
    existing = Connection.objects.filter(
        Q(from_user=request.user, to_user=target_user) |
        Q(from_user=target_user, to_user=request.user)
    ).first()
    
    if existing:
        if existing.status == 'accepted':
            return JsonResponse({'error': 'Already connected'}, status=400)
        else:
            return JsonResponse({'error': 'Connection request pending'}, status=400)
    
    # Create connection request
    connection = Connection.objects.create(
        from_user=request.user,
        to_user=target_user,
        status='pending'
    )
    
    # Create notification
    Notification.objects.create(
        user=target_user,
        actor=request.user,
        action_type='connection_request',
        content=f'{request.user.username} sent you a connection request'
    )
    
    return JsonResponse({
        'status': 'success',
        'message': 'Connection request sent'
    }, status=201)
```

### Accept Connection
```python
@login_required
@require_http_methods(['POST'])
def accept_connection(request, connection_id):
    connection = get_object_or_404(
        Connection, 
        id=connection_id, 
        to_user=request.user,
        status='pending'
    )
    
    connection.status = 'accepted'
    connection.save()
    
    # Notify the requester
    Notification.objects.create(
        user=connection.from_user,
        actor=request.user,
        action_type='connection_accepted',
        content=f'{request.user.username} accepted your connection request'
    )
    
    return JsonResponse({
        'status': 'success',
        'message': 'Connection accepted'
    })
```

### Find Collaborators with Matching
```python
# views.py
@login_required
def find_collaborators(request):
    # Get filter parameters
    interests = request.GET.get('interests', '').split(',')
    skills = request.GET.get('skills', '').split(',')
    role = request.GET.get('role', '')
    page = request.GET.get('page', 1)
    
    # Build query
    query = StudentProfile.objects.exclude(user=request.user)
    
    if interests[0]:
        query = query.filter(interests__overlap=interests)
    
    if skills[0]:
        query = query.filter(skills__overlap=skills)
    
    if role:
        query = query.filter(role_preference__icontains=role)
    
    # Apply NLP matching for ranking
    profiles = list(query)
    
    # Use StudentProfileNLP for intelligent matching
    nlp = StudentProfileNLP()
    ranked_profiles = nlp.match_profiles(
        request.user.student_profile,
        {
            'interests': interests,
            'skills': skills,
            'role': role
        }
    )
    
    # Paginate
    paginator = Paginator(ranked_profiles, 10)
    page_obj = paginator.get_page(page)
    
    return render(request, 'find_collaborators.html', {
        'profiles': page_obj,
        'page_obj': page_obj
    })
```

---

## 6. Messaging System

### Create or Get Direct Chat Room
```python
# views.py
@login_required
def chat_view(request, user_id):
    recipient = get_object_or_404(User, id=user_id)
    
    if recipient == request.user:
        raise Http404('Cannot chat with yourself')
    
    # Get or create chat room
    room = ChatRoom.objects.filter(
        is_group=False,
        members=request.user
    ).filter(members=recipient).first()
    
    if not room:
        room = ChatRoom.objects.create(
            name=f'{request.user.username}-{recipient.username}',
            is_group=False
        )
        room.members.add(request.user, recipient)
    
    # Get messages
    messages = Message.objects.filter(room=room).order_by('-created_at')[:50]
    messages = list(reversed(messages))
    
    # Mark as read
    MessageReadStatus.objects.filter(
        message__room=room,
        user=request.user
    ).update(read_at=timezone.now())
    
    context = {
        'room': room,
        'messages': messages,
        'recipient': recipient
    }
    return render(request, 'chat.html', context)
```

### Send Message (REST API)
```python
# chat_api.py
class MessageListCreateView(generics.ListCreateAPIView):
    serializer_class = MessageSerializer
    permission_classes = [permissions.IsAuthenticated]
    pagination_class = None
    
    def get_queryset(self):
        room_id = self.request.query_params.get('room_id')
        if room_id:
            return Message.objects.filter(room_id=room_id).order_by('-created_at')
        return Message.objects.none()
    
    def perform_create(self, serializer):
        room_id = self.request.data.get('room_id')
        room = get_object_or_404(ChatRoom, id=room_id)
        
        # Verify user is member
        if self.request.user not in room.members.all():
            raise PermissionDenied('Not a member of this room')
        
        # Create message
        message = serializer.save(
            sender=self.request.user,
            room=room
        )
        
        # Create read status for all members except sender
        for member in room.members.exclude(id=self.request.user.id):
            MessageReadStatus.objects.create(
                message=message,
                user=member
            )
```

### Get Messages with Read Status
```python
class MessageDetailView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = MessageSerializer
    permission_classes = [permissions.IsAuthenticated]
    queryset = Message.objects.all()
    
    def get_object(self):
        message = super().get_object()
        # Mark as read for current user
        MessageReadStatus.objects.update_or_create(
            message=message,
            user=self.request.user,
            defaults={'read_at': timezone.now()}
        )
        return message
```

---

## 7. Notifications

### Create Notification
```python
# In any view or signal
Notification.objects.create(
    user=target_user,                    # Who receives
    actor=request.user,                  # Who triggered
    action_type='comment_project',       # Type of action
    target_project=project,              # Related object (optional)
    content=f'{request.user.username} commented on your project'
)
```

### Get User Notifications
```python
@login_required
def notifications_view(request):
    notifications = Notification.objects.filter(
        user=request.user
    ).order_by('-created_at')
    
    # Paginate
    paginator = Paginator(notifications, 20)
    page = request.GET.get('page')
    page_obj = paginator.get_page(page)
    
    # Mark all as read
    unread = page_obj.filter(is_read=False)
    unread.update(is_read=True)
    
    return render(request, 'notifications.html', {
        'page_obj': page_obj
    })
```

---

## 8. Database Queries Optimization

### Select Related (Foreign Key)
```python
# Bad - N+1 queries
projects = Project.objects.all()
for project in projects:
    print(project.owner.username)  # Extra query per project

# Good - 1 query with join
projects = Project.objects.select_related('owner')
for project in projects:
    print(project.owner.username)  # No extra queries
```

### Prefetch Related (Reverse FK & M2M)
```python
# Bad - N+1 queries
rooms = ChatRoom.objects.all()
for room in rooms:
    members = room.members.all()  # Extra query per room

# Good - 2 queries total
from django.db.models import Prefetch
rooms = ChatRoom.objects.prefetch_related('members')
for room in rooms:
    members = room.members.all()  # No extra queries
```

### Efficient Counting
```python
# Bad - Loads all objects into memory
comments = project.comments.all()
count = len(comments)

# Good - Single count query
count = project.comments.count()

# Aggregation
from django.db.models import Count
projects_stats = Project.objects.annotate(
    comment_count=Count('comments'),
    like_count=Count('likes')
)
```

### Batch Operations
```python
# Bad - Multiple queries
for user_id in user_ids:
    Follow.objects.create(follower_id=user_id, following_id=me.id)

# Good - Single bulk create
follows = [
    Follow(follower_id=uid, following_id=me.id) 
    for uid in user_ids
]
Follow.objects.bulk_create(follows)
```

---

## 9. Caching Patterns

### Cache Function Results
```python
from django.core.cache import cache

@login_required
def get_user_stats(request):
    cache_key = f'user_stats_{request.user.id}'
    stats = cache.get(cache_key)
    
    if stats is None:
        # Expensive calculation
        stats = {
            'projects': request.user.project_set.count(),
            'connections': Connection.objects.filter(
                Q(from_user=request.user) | Q(to_user=request.user),
                status='accepted'
            ).count()
        }
        # Cache for 1 hour
        cache.set(cache_key, stats, 3600)
    
    return JsonResponse(stats)
```

### Cache Page
```python
from django.views.decorators.cache import cache_page

@cache_page(60 * 5)  # 5 minutes
def project_list(request):
    projects = Project.objects.all()
    return render(request, 'projects_list.html', {'projects': projects})
```

---

## 10. Error Handling

### Custom Error Handler
```python
# views.py
def handle_view_errors(view_func):
    def wrapper(request, *args, **kwargs):
        try:
            return view_func(request, *args, **kwargs)
        except Http404:
            raise
        except Exception as e:
            logger.error(f"Error in {view_func.__name__}: {str(e)}")
            messages.error(request, "An unexpected error occurred")
            return redirect('dashboard')
    return wrapper

@handle_view_errors
def my_view(request):
    # View code
    pass
```

### API Error Response
```python
from rest_framework.response import Response
from rest_framework import status

class CommentViewSet(viewsets.ModelViewSet):
    def create(self, request, *args, **kwargs):
        try:
            # Create logic
            pass
        except ValueError as e:
            return Response(
                {'error': str(e)},
                status=status.HTTP_400_BAD_REQUEST
            )
        except PermissionError:
            return Response(
                {'error': 'Permission denied'},
                status=status.HTTP_403_FORBIDDEN
            )
```

---

## 11. Form Validation

### Model Form Validation
```python
# forms.py
class ProjectForm(forms.ModelForm):
    class Meta:
        model = Project
        fields = ['title', 'description', 'category', 'technologies']
    
    def clean_title(self):
        title = self.cleaned_data.get('title')
        if len(title) < 5:
            raise forms.ValidationError('Title must be at least 5 characters')
        return title
    
    def clean_technologies(self):
        techs = self.cleaned_data.get('technologies')
        if len(techs) == 0:
            raise forms.ValidationError('Select at least one technology')
        return techs

# views.py
@login_required
def post_project(request):
    if request.method == 'POST':
        form = ProjectForm(request.POST)
        if form.is_valid():
            project = form.save(commit=False)
            project.owner = request.user
            project.save()
            messages.success(request, 'Project posted!')
            return redirect('project_detail', project_id=project.id)
        else:
            for field, errors in form.errors.items():
                messages.error(request, f'{field}: {errors}')
    else:
        form = ProjectForm()
    return render(request, 'post_project.html', {'form': form})
```

---

## 12. Email Integration

### Send OTP Email
```python
# utils.py or views.py
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string

def send_otp_email(email, otp_code, purpose):
    subject = f'{purpose.capitalize()} OTP'
    html_message = render_to_string('emails/otp.html', {
        'otp_code': otp_code,
        'purpose': purpose
    })
    
    email_msg = EmailMultiAlternatives(
        subject,
        f'Your OTP is {otp_code}',
        settings.DEFAULT_FROM_EMAIL,
        [email]
    )
    email_msg.attach_alternative(html_message, 'text/html')
    email_msg.send(fail_silently=False)
```

### Send Notification Email
```python
def notify_project_comment(project, commenter):
    subject = f'{commenter.username} commented on your project'
    context = {
        'project': project,
        'commenter': commenter,
        'project_url': f'https://unisync.in/project-detail/{project.id}/'
    }
    html_message = render_to_string('emails/project_comment.html', context)
    
    EmailMultiAlternatives(
        subject,
        strip_tags(html_message),
        settings.DEFAULT_FROM_EMAIL,
        [project.owner.email]
    ).attach_alternative(html_message, 'text/html').send()
```

---

## 13. Signals for Automatic Actions

### Auto-create StudentProfile on User Creation
```python
# signals.py
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth.models import User
from .models import StudentProfile

@receiver(post_save, sender=User)
def create_student_profile(sender, instance, created, **kwargs):
    if created:
        StudentProfile.objects.create(user=instance)

post_save.connect(create_student_profile, sender=User)
```

### Create Activity Log on Project Creation
```python
@receiver(post_save, sender=Project)
def log_project_creation(sender, instance, created, **kwargs):
    if created:
        Activity.objects.create(
            user=instance.owner,
            action_type='created_project',
            target_project=instance
        )
```

---

## 14. Permissions

### Custom Permission Classes
```python
# permissions.py
from rest_framework import permissions

class IsProjectOwner(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        return obj.owner == request.user

class CanViewProject(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        if obj.visibility == 'public':
            return True
        if obj.owner == request.user:
            return True
        if obj.visibility == 'friends-only':
            connection = Connection.objects.filter(
                Q(from_user=request.user, to_user=obj.owner) |
                Q(from_user=obj.owner, to_user=request.user),
                status='accepted'
            ).exists()
            return connection
        return False

# In views
class ProjectDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Project.objects.all()
    serializer_class = ProjectSerializer
    permission_classes = [CanViewProject, IsProjectOwner]
```

---

## 15. Middleware & Decorators

### Login Required Decorator
```python
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse

@login_required(login_url='login')
def dashboard(request):
    # User is logged in
    return render(request, 'dashboard.html')
```

### Custom Decorator for Admin Only
```python
from django.contrib.admin.decorators import is_staff

def admin_only(view_func):
    def wrapper(request, *args, **kwargs):
        if not request.user.is_staff:
            raise PermissionDenied('Admin access required')
        return view_func(request, *args, **kwargs)
    return wrapper

@admin_only
def admin_dashboard(request):
    pass
```

---

## Summary of Patterns

| Pattern | Use Case | Example |
|---------|----------|---------|
| **select_related()** | Foreign keys (1-to-1, ForeignKey) | Project.objects.select_related('owner') |
| **prefetch_related()** | Reverse ForeignKey, M2M | ChatRoom.objects.prefetch_related('members') |
| **annotate()** | Aggregations | Project.objects.annotate(comment_count=Count('comments')) |
| **bulk_create()** | Batch inserts | Model.objects.bulk_create([obj1, obj2]) |
| **cache.set()** | Cache computation results | cache.set(key, value, timeout) |
| **signals** | Auto-triggered actions | post_save.connect(handler, sender=Model) |
| **serializers** | API data transformation | ModelSerializer with nested relations |
| **permissions** | API access control | IsAuthenticated, IsOwner, etc. |
| **paginator** | Large datasets | Paginator(queryset, per_page) |
| **filters** | Complex queries | Q objects with OR/AND logic |

---

**Last Updated**: February 6, 2026
