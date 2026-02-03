# UniSync Code Patterns & Quick Reference

---

## Authentication Patterns

### Standard Login Flow
```python
# In views.py
def login_view(request):
    if request.method == 'POST':
        form = LoginForm(data=request.POST)
        if form.is_valid():
            user = authenticate(
                username=form.cleaned_data['username'],
                password=form.cleaned_data['password']
            )
            if user:
                login(request, user)
                return redirect('dashboard')
    else:
        form = LoginForm()
    return render(request, 'login.html', {'form': form})
```

### OTP Generation & Verification
```python
# Generate OTP
otp_obj = OTP.generate_otp(email='user@example.com', purpose='login')
# otp_code is automatically 6 digits, expires in 5 minutes

# Verify OTP
is_valid, message = otp_obj.verify_otp(user_input_code)
if is_valid:
    # Process login
    user = User.objects.get(email=otp_obj.email)
    login(request, user)
```

### Social Login via django-allauth
```python
# In settings.py
AUTHENTICATION_BACKENDS = (
    'django.contrib.auth.backends.ModelBackend',
    'allauth.account.auth_backends.AuthenticationBackend',
)

SOCIALACCOUNT_PROVIDERS = {
    'google': {
        'SCOPE': ['profile', 'email'],
        'APP': {
            'client_id': os.getenv('GOOGLE_CLIENT_ID'),
            'secret': os.getenv('GOOGLE_CLIENT_SECRET'),
        }
    },
}

# In template
<a href="{% provider_login_url 'google' %}">Login with Google</a>
```

---

## Model Usage Patterns

### Creating Related Objects
```python
# User Registration - creates StudentProfile automatically
user = User.objects.create_user(
    username='john_doe',
    email='john@example.com',
    password='SecurePass123'
)

# Create or get StudentProfile
profile, created = StudentProfile.objects.get_or_create(
    user=user,
    defaults={
        'full_name': 'John Doe',
        'college': 'MIT',
        'bio': 'Full-stack developer'
    }
)

# Update stats
stats, created = UserStats.objects.get_or_create(user=user)
stats.update_stats()
```

### Project CRUD
```python
# Create
project = Project.objects.create(
    owner=request.user,
    title='AI Chatbot',
    description='Real-time chatbot using GPT',
    category='AI/ML',
    technologies=['Python', 'FastAPI', 'OpenAI'],
    looking_for=['Backend Dev', 'Frontend Dev'],
    visibility='public',
    status='active'
)

# Create owner member relationship
ProjectMember.objects.create(
    project=project,
    user=request.user,
    role='owner'
)

# Read
project = Project.objects.get(id=project_id)
members = project.members.all()
tasks = project.tasks.filter(status='todo')

# Update
project.title = 'Updated Title'
project.save()

# Delete
project.delete()  # Cascades to members, tasks, etc.
```

### Working with Messages & Read Status
```python
# Send direct message
message = Message.objects.create(
    sender=request.user,
    receiver=recipient_user,
    content='Hello!',
    message_type='text'
)

# Mark as read
message.mark_as_read_by(request.user)

# Check if read by specific user
is_read = message.is_read_by(request.user)

# Get read count
read_count = message.get_read_count()

# Get users who haven't read (for group chat)
unread_users = message.get_unread_users()
```

### Connection Requests
```python
# Send connection request
connection = Connection.objects.create(
    sender=request.user,
    receiver=target_user,
    status='pending'
)

# Accept connection
connection.status = 'accepted'
connection.save()

# Get all connections
my_connections = Connection.objects.filter(
    models.Q(sender=request.user) | models.Q(receiver=request.user),
    status='accepted'
)
```

---

## View Patterns

### @login_required Decorator
```python
@login_required(login_url='login')
def dashboard_view(request):
    """Only authenticated users can access"""
    profile = StudentProfile.objects.get(user=request.user)
    projects = Project.objects.filter(owner=request.user)
    return render(request, 'dashboard.html', {
        'profile': profile,
        'projects': projects
    })
```

### Error Handling Decorator
```python
def handle_view_errors(view_func):
    """Wrap views to handle exceptions gracefully"""
    def wrapper(request, *args, **kwargs):
        try:
            return view_func(request, *args, **kwargs)
        except Project.DoesNotExist:
            messages.error(request, "Project not found.")
            return redirect('explore_projects')
        except Exception as e:
            logger.error(f"Error: {str(e)}", exc_info=True)
            messages.error(request, "An error occurred.")
            return redirect('dashboard')
    return wrapper

@handle_view_errors
def project_detail(request, project_id):
    project = Project.objects.get(id=project_id)
    return render(request, 'project_detail.html', {'project': project})
```

### CSRF-Exempt for APIs
```python
@csrf_exempt  # Only for public APIs, not for forms
def college_search_api(request):
    """Search colleges via RapidAPI"""
    if request.method == 'POST':
        data = json.loads(request.body)
        query = data.get('query')
        # Search logic
        return JsonResponse({'results': results})
```

### Pagination Pattern
```python
from django.core.paginator import Paginator

def explore_projects_view(request):
    projects = Project.objects.filter(visibility='public').order_by('-created_at')
    
    paginator = Paginator(projects, 10)  # 10 per page
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    return render(request, 'project_feed.html', {'page_obj': page_obj})

# In template:
{% for project in page_obj %}
    ...
{% endfor %}

{% if page_obj.has_other_pages %}
    {% if page_obj.has_previous %}
        <a href="?page={{ page_obj.previous_page_number }}">Previous</a>
    {% endif %}
    
    {% for num in page_obj.paginator.page_range %}
        <a href="?page={{ num }}">{{ num }}</a>
    {% endfor %}
    
    {% if page_obj.has_next %}
        <a href="?page={{ page_obj.next_page_number }}">Next</a>
    {% endif %}
{% endif %}
```

### Filtering with Q Objects
```python
from django.db.models import Q

def search_projects(request):
    query = request.GET.get('q', '')
    category = request.GET.get('category', '')
    
    projects = Project.objects.filter(visibility='public')
    
    if query:
        projects = projects.filter(
            Q(title__icontains=query) |
            Q(description__icontains=query) |
            Q(collaboration_needs__icontains=query)
        )
    
    if category:
        projects = projects.filter(category=category)
    
    return render(request, 'search.html', {'projects': projects})
```

---

## Form Patterns

### Custom Form Validation
```python
class StudentProfileForm(forms.ModelForm):
    class Meta:
        model = StudentProfile
        fields = ['full_name', 'college', 'bio', 'skills', 'profile_photo']
    
    def clean_full_name(self):
        full_name = self.cleaned_data.get('full_name')
        if len(full_name) < 3:
            raise ValidationError("Full name must be at least 3 characters.")
        return full_name
    
    def clean_skills(self):
        skills = self.cleaned_data.get('skills')
        if len(skills) > 10:
            raise ValidationError("Maximum 10 skills allowed.")
        return skills
    
    def clean(self):
        cleaned_data = super().clean()
        # Cross-field validation
        return cleaned_data
```

### Form in Template
```html
<form method="post" enctype="multipart/form-data">
    {% csrf_token %}
    
    {{ form.as_p }}
    <!-- OR -->
    
    <div class="form-group">
        {{ form.full_name }}
        {% if form.full_name.errors %}
            <div class="alert alert-danger">
                {{ form.full_name.errors }}
            </div>
        {% endif %}
    </div>
    
    <button type="submit" class="btn btn-primary">Save</button>
</form>
```

---

## Serializer Patterns

### Basic Serializer
```python
class ProjectSerializer(serializers.ModelSerializer):
    owner = UserProfileSerializer(read_only=True)
    likes_count = serializers.SerializerMethodField()
    
    class Meta:
        model = Project
        fields = [
            'id', 'title', 'description', 'technologies',
            'owner', 'likes_count', 'created_at'
        ]
        read_only_fields = ['id', 'created_at', 'owner']
    
    def get_likes_count(self, obj):
        return obj.likes.count()
```

### Nested Serializer
```python
class ProjectDetailSerializer(serializers.ModelSerializer):
    owner = UserProfileSerializer(read_only=True)
    members = ProjectMemberSerializer(many=True, read_only=True)
    comments = CommentSerializer(many=True, read_only=True)
    
    class Meta:
        model = Project
        fields = ['id', 'title', 'owner', 'members', 'comments']
```

### Using Serializers in Views
```python
class ProjectDetailView(APIView):
    def get(self, request, project_id):
        project = Project.objects.get(id=project_id)
        serializer = ProjectDetailSerializer(project)
        return Response(serializer.data)
    
    def post(self, request):
        serializer = ProjectSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(owner=request.user)
            return Response(serializer.data, status=201)
        return Response(serializer.errors, status=400)
```

---

## Email Patterns

### Sending Email via Backend
```python
from django.core.mail import send_mail, EmailMultiAlternatives
from django.conf import settings

# Simple email
send_mail(
    subject='Your OTP Code',
    message='Your OTP is: 123456',
    from_email=settings.DEFAULT_FROM_EMAIL,
    recipient_list=['user@example.com'],
)

# HTML email
msg = EmailMultiAlternatives(
    subject='Your OTP Code',
    body='Your OTP is: 123456',
    from_email=settings.DEFAULT_FROM_EMAIL,
    to=['user@example.com']
)

html_content = '''
<html>
    <body>
        <p>Your OTP Code: <strong>123456</strong></p>
        <p>This expires in 5 minutes.</p>
    </body>
</html>
'''

msg.attach_alternative(html_content, 'text/html')
msg.send()
```

### Custom Email Backend
```python
# In accounts/custom_mail_backend.py
from django.core.mail.backends.base import BaseEmailBackend

class CustomEmailBackend(BaseEmailBackend):
    def send_messages(self, email_messages):
        for message in email_messages:
            # Custom logic (API call, logging, etc.)
            print(f"Sending to: {message.to}")
        return len(email_messages)

# In settings.py
EMAIL_BACKEND = 'accounts.custom_mail_backend.CustomEmailBackend'
```

---

## NLP & Utility Patterns

### Extract Skills from Text
```python
from accounts.utils import StudentProfileNLP

bio = "I'm a Python developer with experience in Django and React"
skills = StudentProfileNLP.extract_skills(bio)
# Returns: ['python', 'django', 'react']

# Extract interests
interests = StudentProfileNLP.analyze_interests(bio)
# Returns: {'web_dev': 2, 'backend': 1}

# Find similar profiles
profile = StudentProfile.objects.get(id=1)
similar = StudentProfileNLP.find_similar_profiles(profile, top_k=5)
# Returns list of similar ProfileIDs
```

### Project Visibility Filter
```python
from accounts.utils import ProjectVisibilityFilter

# Get visible projects for user
user = request.user
visible_projects = ProjectVisibilityFilter.get_visible_projects(user)

# Rules:
# - Owner sees all (including draft)
# - Public visible to everyone
# - Private visible to members only
# - Draft visible to owner only
```

---

## Template Patterns

### Base Template with Navbar
```html
<!-- base.html -->
<!DOCTYPE html>
<html>
<head>
    <title>{% block title %}UniSync{% endblock %}</title>
    <link rel="stylesheet" href="{% static 'css/bootstrap.css' %}">
</head>
<body>
    <nav class="navbar">
        <a href="{% url 'main' %}">UniSync</a>
        {% if user.is_authenticated %}
            <a href="{% url 'dashboard' %}">Dashboard</a>
            <a href="{% url 'messages' %}">Messages</a>
            <a href="{% url 'logout' %}">Logout</a>
        {% else %}
            <a href="{% url 'login' %}">Login</a>
            <a href="{% url 'register' %}">Register</a>
        {% endif %}
    </nav>

    {% if messages %}
        {% for message in messages %}
            <div class="alert alert-{{ message.tags }}">
                {{ message }}
            </div>
        {% endfor %}
    {% endif %}

    {% block content %}{% endblock %}

    <script src="{% static 'js/bootstrap.js' %}"></script>
</body>
</html>
```

### Using Base Template
```html
{% extends 'base.html' %}
{% load static %}

{% block title %}Dashboard - UniSync{% endblock %}

{% block content %}
<div class="container">
    <h1>Welcome, {{ user.first_name }}!</h1>
    
    {% if profile.profile_photo %}
        <img src="{{ profile.profile_photo.url }}" alt="Profile">
    {% endif %}
    
    <!-- Content here -->
</div>
{% endblock %}
```

### Conditional Display
```html
{% if user.is_authenticated %}
    <p>Welcome back, {{ user.username }}!</p>
    
    {% if profile.profile_completed %}
        <a href="{% url 'explore_projects' %}">Find Collaborators</a>
    {% else %}
        <a href="{% url 'student_details' %}">Complete Your Profile</a>
    {% endif %}
{% else %}
    <p>Please <a href="{% url 'login' %}">login</a> to continue</p>
{% endif %}
```

### Loop with Pagination
```html
{% for project in page_obj %}
    <div class="project-card">
        <h3>{{ project.title }}</h3>
        <p>{{ project.description }}</p>
        <p>By {{ project.owner.student_profile.full_name }}</p>
        <a href="{% url 'project_detail' project.id %}">View</a>
    </div>
{% empty %}
    <p>No projects found.</p>
{% endfor %}

{% if page_obj.has_other_pages %}
    <nav>
        {% if page_obj.has_previous %}
            <a href="?page=1">First</a>
            <a href="?page={{ page_obj.previous_page_number }}">Previous</a>
        {% endif %}
        
        Page {{ page_obj.number }} of {{ page_obj.paginator.num_pages }}
        
        {% if page_obj.has_next %}
            <a href="?page={{ page_obj.next_page_number }}">Next</a>
            <a href="?page={{ page_obj.paginator.num_pages }}">Last</a>
        {% endif %}
    </nav>
{% endif %}
```

---

## URL Routing Patterns

### Basic Routes
```python
# urls.py
urlpatterns = [
    path('login/', views.login_view, name='login'),
    path('register/', views.register_view, name='register'),
    path('project/<int:project_id>/', views.project_detail, name='project_detail'),
    path('api/projects/', views.ProjectListView.as_view(), name='projects-list'),
]

# In template: {% url 'login' %}
# In view: redirect('login')
# In code: reverse('login')
```

### URL Parameters
```python
# urls.py
path('user/<str:username>/', views.user_profile, name='user_profile'),
path('chat/<int:room_id>/', views.chat_view, name='chat'),

# view function
def user_profile(request, username):
    user = User.objects.get(username=username)
    return render(request, 'profile.html', {'user': user})

# In template
<a href="{% url 'user_profile' username=user.username %}">
    {{ user.username }}
</a>
```

### Include Other URLConfs
```python
# Main urls.py
from django.urls import path, include

urlpatterns = [
    path('api/', include('accounts.urls')),
    path('accounts/', include('allauth.urls')),
]

# accounts/urls.py
urlpatterns = [
    path('projects/', views.ProjectListView.as_view()),
    path('messages/', views.MessageListView.as_view()),
]
```

---

## REST API Patterns

### GET - Retrieve List
```python
# urls.py
path('api/projects/', views.ProjectListView.as_view(), name='projects-list'),

# views.py
class ProjectListView(generics.ListCreateAPIView):
    queryset = Project.objects.all()
    serializer_class = ProjectSerializer
    permission_classes = [permissions.AllowAny]
    pagination_class = pagination.PageNumberPagination
    filter_backends = [filters.SearchFilter]
    search_fields = ['title', 'description']

# Request: GET /api/projects/?search=python&page=1
# Response: {"count": 50, "next": "...", "results": [...]}
```

### POST - Create
```python
# Request: POST /api/projects/
# Body: {
#   "title": "AI Chatbot",
#   "description": "...",
#   "technologies": ["Python", "FastAPI"]
# }

class ProjectCreateView(generics.CreateAPIView):
    serializer_class = ProjectSerializer
    permission_classes = [permissions.IsAuthenticated]
    
    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)

# Response: 201 Created
```

### GET - Retrieve Detail
```python
# urls.py
path('api/projects/<int:pk>/', views.ProjectDetailView.as_view()),

# views.py
class ProjectDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Project.objects.all()
    serializer_class = ProjectSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

# PUT - Update: {title: "Updated"}
# DELETE - Destroy
```

### JSON Response
```python
from django.http import JsonResponse
from django.views.decorators.http import require_http_methods

@require_http_methods(['POST'])
def like_project(request, project_id):
    project = Project.objects.get(id=project_id)
    like, created = Like.objects.get_or_create(
        user=request.user,
        project=project
    )
    
    if not created:
        like.delete()
        return JsonResponse({'liked': False, 'count': project.likes.count()})
    
    return JsonResponse({'liked': True, 'count': project.likes.count()})
```

---

## Debug & Logging Patterns

### Logging Setup
```python
# In settings.py
LOGGING = {
    'version': 1,
    'handlers': {
        'console': {'class': 'logging.StreamHandler'},
        'file': {
            'class': 'logging.FileHandler',
            'filename': 'logs/django.log',
        }
    },
    'loggers': {
        'django': {'handlers': ['console', 'file'], 'level': 'INFO'},
        'accounts': {'handlers': ['console', 'file'], 'level': 'DEBUG'},
    }
}

# In views.py
import logging
logger = logging.getLogger(__name__)

logger.info(f"User {request.user.id} created project")
logger.warning(f"Invalid OTP attempt from {request.POST.get('email')}")
logger.error(f"Email sending failed: {str(e)}", exc_info=True)
```

### Debugging in Development
```python
# In settings.py
DEBUG = True

# In template
{{ object }}  <!-- Shows object repr -->

# Use Django Debug Toolbar
# INSTALLED_APPS += ['debug_toolbar']
# MIDDLEWARE += ['debug_toolbar.middleware.DebugToolbarMiddleware']
# INTERNAL_IPS = ['127.0.0.1']
```

---

## Performance Patterns

### Query Optimization
```python
# Bad: N+1 queries
for project in Project.objects.all():
    print(project.owner.username)  # Separate query per project

# Good: select_related (ForeignKey)
projects = Project.objects.select_related('owner')
for project in projects:
    print(project.owner.username)  # 1 query total

# Good: prefetch_related (M2M/Reverse FK)
projects = Project.objects.prefetch_related('members')
for project in projects:
    for member in project.members.all():  # Cached
        print(member.user.username)

# Using only() and defer()
projects = Project.objects.only('id', 'title')  # Exclude others
projects = Project.objects.defer('description')  # Defer heavy field
```

### Caching
```python
from django.views.decorators.cache import cache_page
from django.core.cache import cache

# Cache entire view for 60 seconds
@cache_page(60)
def explore_projects_view(request):
    projects = Project.objects.filter(visibility='public')
    return render(request, 'explore.html', {'projects': projects})

# Cache specific data
from django.views.decorators.cache import cache_page
cache_key = f'user_{request.user.id}_stats'
stats = cache.get(cache_key)
if not stats:
    stats = request.user.userstats
    cache.set(cache_key, stats, 60*5)  # 5 minutes
```

---

## Common Command Patterns

```bash
# Create superuser
python manage.py createsuperuser

# Run migrations
python manage.py makemigrations
python manage.py migrate

# Create app
python manage.py startapp appname

# Collect static files
python manage.py collectstatic --noinput

# Run development server
python manage.py runserver 0.0.0.0:8000

# Run tests
python manage.py test
pytest

# Shell
python manage.py shell
>>> from accounts.models import Project
>>> Project.objects.all()

# Create fixtures
python manage.py dumpdata > data.json
python manage.py loaddata data.json
```

---

**End of Quick Reference**
