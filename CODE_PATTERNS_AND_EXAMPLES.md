# Code Patterns & Examples - UniSync

## 1. AUTHENTICATION PATTERNS

### Pattern 1.1: OTP-Based Login Flow
```python
# models.py
class OTP(models.Model):
    email = models.EmailField()
    otp_code = models.CharField(max_length=6)
    expires_at = models.DateTimeField()
    is_used = models.BooleanField(default=False)
    
    def is_valid(self):
        return not self.is_used and timezone.now() < self.expires_at
    
    @classmethod
    def generate_otp(cls, email, purpose):
        otp_code = ''.join([str(random.randint(0, 9)) for _ in range(6)])
        expires_at = timezone.now() + timedelta(minutes=5)
        otp = cls.objects.create(
            email=email,
            otp_code=otp_code,
            purpose=purpose,
            expires_at=expires_at
        )
        return otp_code
```

### Pattern 1.2: View-Based Login Handler
```python
# views.py
def login_view(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data['email']
            
            # Generate and send OTP
            otp_code = OTP.generate_otp(email, 'login')
            send_otp_email(email, otp_code, 'login')
            
            # Store email in session for verification
            request.session['login_email'] = email
            return redirect('verify_otp')
    else:
        form = LoginForm()
    
    return render(request, 'accounts/login.html', {'form': form})
```

### Pattern 1.3: OTP Verification
```python
def verify_otp(request):
    if request.method == 'POST':
        email = request.session.get('login_email')
        otp_code = request.POST.get('otp_code')
        
        try:
            otp = OTP.objects.filter(email=email).latest('created_at')
            is_valid, message = otp.verify_otp(otp_code)
            
            if is_valid:
                user = User.objects.get(email=email)
                login(request, user)
                return redirect('dashboard')
            else:
                messages.error(request, message)
        except OTP.DoesNotExist:
            messages.error(request, "OTP not found")
    
    return render(request, 'accounts/verify_otp.html')
```

---

## 2. MODEL PATTERNS

### Pattern 2.1: Extended User Profile with Signals
```python
# models.py
from django.db.models.signals import post_save
from django.dispatch import receiver

class StudentProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    full_name = models.CharField(max_length=100, blank=True)
    college = models.CharField(max_length=200, blank=True)
    interests = models.JSONField(default=list)
    skills = models.JSONField(default=list)
    profile_completed = models.BooleanField(default=False)
    created_at = models.DateTimeField(default=timezone.now)

# Auto-create profile when user is created
@receiver(post_save, sender=User)
def create_student_profile(sender, instance, created, **kwargs):
    if created:
        StudentProfile.objects.create(user=instance)

post_save.connect(create_student_profile, sender=User)
```

### Pattern 2.2: JSON Array Fields for Flexible Data
```python
# models.py
class Project(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField()
    
    # Flexible storage of arrays
    collaboration_needs = models.JSONField(default=list)  # ['backend', 'frontend', 'ui']
    skills_required = models.JSONField(default=list)      # ['Python', 'React', 'PostgreSQL']
    team_size = models.JSONField(default=list)            # [2, 3, 4] for min/max/ideal
    
    def add_skill_required(self, skill):
        if skill not in self.skills_required:
            self.skills_required.append(skill)
            self.save()
    
    def get_collaboration_string(self):
        return ', '.join(self.collaboration_needs)
```

### Pattern 2.3: Timestamp Tracking
```python
# models.py - Abstract Base Model Pattern
class TimestampModel(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        abstract = True

# Usage
class Message(TimestampModel):
    content = models.TextField()
    from_user = models.ForeignKey(User, related_name='sent_messages')
    to_user = models.ForeignKey(User, related_name='received_messages')
    read_at = models.DateTimeField(null=True, blank=True)
```

---

## 3. QUERY PATTERNS

### Pattern 3.1: Optimized Profile Query
```python
# views.py - GOOD (with select_related/prefetch_related)
def view_profile(request, username):
    user = User.objects.select_related(
        'student_profile'
    ).prefetch_related(
        'project_set',
        'connection_set'
    ).get(username=username)
    
    return render(request, 'profile.html', {'user': user})
```

### Pattern 3.2: Project List with Count Aggregation
```python
# views.py
from django.db.models import Count, Q

def project_feed(request):
    projects = Project.objects.annotate(
        comment_count=Count('comment', distinct=True),
        like_count=Count('like', distinct=True),
        member_count=Count('members', distinct=True)
    ).filter(
        visibility='public'
    ).order_by(
        '-created_at'
    )[:20]  # Get only last 20
    
    return render(request, 'project_feed.html', {'projects': projects})
```

### Pattern 3.3: Search with Multiple Field Filters
```python
# views.py
def search_projects(request):
    query = request.GET.get('q', '')
    category = request.GET.get('category', '')
    college = request.GET.get('college', '')
    
    projects = Project.objects.filter(visibility='public')
    
    if query:
        projects = projects.filter(
            Q(title__icontains=query) |
            Q(description__icontains=query) |
            Q(collaboration_needs__icontains=query)
        )
    
    if category:
        projects = projects.filter(category=category)
    
    if college:
        projects = projects.filter(owner__student_profile__college=college)
    
    return render(request, 'search.html', {'projects': projects})
```

---

## 4. FORM PATTERNS

### Pattern 4.1: Custom Form Validation
```python
# forms.py
from django import forms
from .models import StudentProfile, Project

class ProjectForm(forms.ModelForm):
    collaboration_needs = forms.CharField(
        widget=forms.Textarea,
        help_text="Enter comma-separated roles needed (e.g., Backend, Frontend, UI)"
    )
    
    class Meta:
        model = Project
        fields = ['title', 'description', 'category', 'visibility']
    
    def clean_title(self):
        title = self.cleaned_data.get('title')
        if len(title) < 5:
            raise forms.ValidationError("Title must be at least 5 characters")
        return title
    
    def clean_collaboration_needs(self):
        needs = self.cleaned_data.get('collaboration_needs')
        # Convert comma-separated string to list
        return [n.strip() for n in needs.split(',') if n.strip()]
    
    def save(self, commit=True):
        instance = super().save(commit=False)
        instance.collaboration_needs = self.cleaned_data['collaboration_needs']
        if commit:
            instance.save()
        return instance
```

### Pattern 4.2: Bootstrap Form Rendering
```html
<!-- templates/form_field.html -->
<div class="mb-3">
    {{ form.field_name.label_tag }}
    {% if form.field_name.field.widget.input_type == 'checkbox' %}
        <div class="form-check">
            {{ form.field_name }}
            <label class="form-check-label">
                {{ form.field_name.label }}
            </label>
        </div>
    {% else %}
        {{ form.field_name }}
    {% endif %}
    {% if form.field_name.errors %}
        <div class="invalid-feedback d-block">
            {{ form.field_name.errors }}
        </div>
    {% endif %}
</div>
```

---

## 5. VIEW PATTERNS

### Pattern 5.1: Login Required Decorator
```python
# views.py
from django.contrib.auth.decorators import login_required

@login_required(login_url='login')
def dashboard(request):
    """View protected by authentication"""
    profile = StudentProfile.objects.get(user=request.user)
    projects = Project.objects.filter(owner=request.user)
    return render(request, 'dashboard.html', {
        'profile': profile,
        'projects': projects
    })
```

### Pattern 5.2: Permission Check in View
```python
# views.py
@login_required
def edit_project(request, project_id):
    project = get_object_or_404(Project, id=project_id)
    
    # Check if user is owner
    if project.owner != request.user:
        return HttpResponseForbidden("You don't have permission to edit this project")
    
    if request.method == 'POST':
        form = ProjectForm(request.POST, instance=project)
        if form.is_valid():
            form.save()
            messages.success(request, 'Project updated!')
            return redirect('project_detail', project_id=project.id)
    else:
        form = ProjectForm(instance=project)
    
    return render(request, 'edit_project.html', {'form': form})
```

### Pattern 5.3: AJAX Response Pattern
```python
# views.py
from django.http import JsonResponse

@login_required
def like_project(request, project_id):
    """AJAX endpoint for liking projects"""
    if not request.is_ajax():
        return JsonResponse({'error': 'Invalid request'}, status=400)
    
    project = get_object_or_404(Project, id=project_id)
    
    like, created = Like.objects.get_or_create(
        user=request.user,
        project=project
    )
    
    if not created:
        like.delete()
        liked = False
    else:
        liked = True
    
    return JsonResponse({
        'success': True,
        'liked': liked,
        'likes_count': project.like_set.count()
    })
```

---

## 6. SERIALIZER PATTERNS (DRF)

### Pattern 6.1: User Profile Serializer
```python
# serializers.py
from rest_framework import serializers
from .models import StudentProfile, User

class StudentProfileSerializer(serializers.ModelSerializer):
    username = serializers.CharField(source='user.username', read_only=True)
    email = serializers.CharField(source='user.email', read_only=True)
    
    class Meta:
        model = StudentProfile
        fields = [
            'id', 'username', 'email', 'full_name', 'college',
            'interests', 'skills', 'bio', 'profile_photo',
            'github', 'linkedin', 'portfolio'
        ]

class UserProfileSerializer(serializers.ModelSerializer):
    profile = StudentProfileSerializer(
        source='student_profile',
        read_only=True
    )
    
    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'first_name', 'last_name', 'profile']
```

### Pattern 6.2: Nested Serializer with Context
```python
# serializers.py
class CommentSerializer(serializers.ModelSerializer):
    user = StudentProfileSerializer(read_only=True)
    replies = serializers.SerializerMethodField()
    
    class Meta:
        model = Comment
        fields = ['id', 'user', 'text', 'created_at', 'replies']
    
    def get_replies(self, obj):
        replies = obj.replies.all()
        return CommentSerializer(replies, many=True).data
```

---

## 7. UTILITY PATTERNS

### Pattern 7.1: Profile Matching Algorithm
```python
# utils.py
from django.db.models import Count, Q

class StudentProfileNLP:
    @staticmethod
    def calculate_profile_similarity(user1, user2):
        """
        Calculate similarity score between two user profiles
        Returns score 0-100
        """
        profile1 = user1.student_profile
        profile2 = user2.student_profile
        
        score = 0
        
        # Skill overlap (40 points max)
        skills1 = set(profile1.skills)
        skills2 = set(profile2.skills)
        if skills1 and skills2:
            overlap = len(skills1 & skills2) / max(len(skills1), len(skills2))
            score += overlap * 40
        
        # Interest overlap (30 points max)
        interests1 = set(profile1.interests)
        interests2 = set(profile2.interests)
        if interests1 and interests2:
            overlap = len(interests1 & interests2) / max(len(interests1), len(interests2))
            score += overlap * 30
        
        # College match (20 points max)
        if profile1.college == profile2.college:
            score += 20
        
        # Connection path (10 points max)
        mutual_connections = Connection.objects.filter(
            Q(from_user=user1, to_user=user2) |
            Q(from_user=user2, to_user=user1)
        ).count()
        if mutual_connections > 0:
            score += 10
        
        return min(score, 100)
    
    @staticmethod
    def find_collaborators(user, skills=None, interests=None, limit=10):
        """Find similar users for collaboration"""
        candidates = User.objects.exclude(id=user.id)
        
        results = []
        for candidate in candidates:
            match_score = StudentProfileNLP.calculate_profile_similarity(user, candidate)
            if match_score > 20:  # Minimum threshold
                results.append((candidate, match_score))
        
        # Sort by match score
        results.sort(key=lambda x: x[1], reverse=True)
        return [(user, score) for user, score in results[:limit]]
```

### Pattern 7.2: Project Visibility Filter
```python
# utils.py
class ProjectVisibilityFilter:
    @staticmethod
    def get_visible_projects(user):
        """Get all projects visible to the given user"""
        from .models import Project
        
        return Project.objects.filter(
            Q(visibility='public') |  # All public projects
            Q(owner=user) |           # User's own projects
            Q(members=user)           # Projects user is member of
        ).distinct()
    
    @staticmethod
    def is_project_visible(project, user):
        """Check if specific project is visible to user"""
        if project.visibility == 'public':
            return True
        if project.owner == user:
            return True
        if user in project.members.all():
            return True
        return False
```

---

## 8. TEMPLATE PATTERNS

### Pattern 8.1: Base Template Inheritance
```html
<!-- templates/base.html -->
<!DOCTYPE html>
<html>
<head>
    <meta charset="utf-8">
    <meta name="viewport" content="width=device-width, initial-scale=1">
    <title>{% block title %}UniSync{% endblock %}</title>
    <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.1.3/dist/css/bootstrap.min.css" rel="stylesheet">
    {% block extra_css %}{% endblock %}
</head>
<body>
    {% include 'navbar.html' %}
    
    <main class="container mt-4">
        {% if messages %}
            {% for message in messages %}
                <div class="alert alert-{{ message.tags }}">
                    {{ message }}
                </div>
            {% endfor %}
        {% endif %}
        
        {% block content %}{% endblock %}
    </main>
    
    {% include 'footer.html' %}
    
    <script src="https://cdn.jsdelivr.net/npm/bootstrap@5.1.3/dist/js/bootstrap.bundle.min.js"></script>
    {% block extra_js %}{% endblock %}
</body>
</html>
```

### Pattern 8.2: Form Rendering with Error Display
```html
<!-- templates/form.html -->
{% extends 'base.html' %}

{% block content %}
<div class="row">
    <div class="col-md-6 offset-md-3">
        <h2>{{ form_title }}</h2>
        
        <form method="POST" enctype="multipart/form-data">
            {% csrf_token %}
            
            {% for field in form %}
                <div class="mb-3">
                    {{ field.label_tag }}
                    
                    {% if field.field.widget.input_type == 'checkbox' %}
                        <div class="form-check">
                            {{ field }}
                        </div>
                    {% else %}
                        {{ field }}
                    {% endif %}
                    
                    {% if field.errors %}
                        <div class="invalid-feedback d-block">
                            {% for error in field.errors %}
                                <p>{{ error }}</p>
                            {% endfor %}
                        </div>
                    {% endif %}
                </div>
            {% endfor %}
            
            <button type="submit" class="btn btn-primary">{{ button_text }}</button>
        </form>
    </div>
</div>
{% endblock %}
```

### Pattern 8.3: Project Card Component
```html
<!-- templates/components/project_card.html -->
<div class="card h-100">
    <div class="card-body">
        <h5 class="card-title">{{ project.title }}</h5>
        <p class="card-text text-muted">{{ project.description|truncatewords:20 }}</p>
        
        <div class="mb-2">
            <span class="badge bg-secondary">{{ project.category }}</span>
            {% if project.visibility == 'private' %}
                <span class="badge bg-warning">Private</span>
            {% endif %}
        </div>
        
        <div class="d-flex justify-content-between align-items-center">
            <small class="text-muted">
                By <a href="{% url 'view_profile' project.owner.username %}">
                    {{ project.owner.student_profile.full_name }}
                </a>
            </small>
            <small class="text-muted">
                <i class="fas fa-comment"></i> {{ project.comment_count }}
                <i class="fas fa-heart"></i> {{ project.like_count }}
            </small>
        </div>
    </div>
    
    <div class="card-footer bg-white">
        <a href="{% url 'project_detail' project.id %}" class="btn btn-sm btn-outline-primary">
            View Details
        </a>
    </div>
</div>
```

---

## 9. JAVASCRIPT PATTERNS

### Pattern 9.1: AJAX Form Submission
```javascript
// static/js/projects.js

// Like/Unlike Project
document.addEventListener('DOMContentLoaded', function() {
    const likeButtons = document.querySelectorAll('.like-btn');
    
    likeButtons.forEach(btn => {
        btn.addEventListener('click', function(e) {
            e.preventDefault();
            
            const projectId = this.dataset.projectId;
            const url = `/projects/${projectId}/like/`;
            
            fetch(url, {
                method: 'POST',
                headers: {
                    'X-CSRFToken': getCookie('csrftoken'),
                    'Content-Type': 'application/json'
                }
            })
            .then(response => response.json())
            .then(data => {
                if (data.success) {
                    this.classList.toggle('active');
                    this.querySelector('.like-count').textContent = data.likes_count;
                }
            })
            .catch(error => console.error('Error:', error));
        });
    });
});

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
```

### Pattern 9.2: Real-time Search with Debounce
```javascript
// static/js/search.js

function debounce(func, wait) {
    let timeout;
    return function executedFunction(...args) {
        const later = () => {
            clearTimeout(timeout);
            func(...args);
        };
        clearTimeout(timeout);
        timeout = setTimeout(later, wait);
    };
}

const searchInput = document.getElementById('search-input');
const searchResults = document.getElementById('search-results');

const performSearch = debounce(function(query) {
    if (query.length < 2) {
        searchResults.innerHTML = '';
        return;
    }
    
    fetch(`/projects/search/?q=${encodeURIComponent(query)}`)
        .then(response => response.text())
        .then(html => {
            searchResults.innerHTML = html;
        });
}, 300);  // Wait 300ms after user stops typing

searchInput.addEventListener('input', function() {
    performSearch(this.value);
});
```

---

## 10. COMMON PITFALLS & SOLUTIONS

### Pitfall 1: N+1 Query Problem
```python
# BAD
projects = Project.objects.all()
for project in projects:
    print(project.owner.username)  # Makes database query for each project

# GOOD
projects = Project.objects.select_related('owner')
for project in projects:
    print(project.owner.username)  # Only 2 queries total
```

### Pitfall 2: Missing CSRF Token
```html
<!-- BAD -->
<form method="POST" action="/projects/create/">
    <input type="text" name="title">
    <button type="submit">Create</button>
</form>

<!-- GOOD -->
<form method="POST" action="/projects/create/">
    {% csrf_token %}
    <input type="text" name="title">
    <button type="submit">Create</button>
</form>
```

### Pitfall 3: Unsanitized User Input
```python
# BAD
comment = request.POST.get('text')
Comment.objects.create(user=request.user, text=comment)  # XSS vulnerability

# GOOD
from django.utils.html import escape
comment = escape(request.POST.get('text'))
Comment.objects.create(user=request.user, text=comment)
```

### Pitfall 4: Unprotected Views
```python
# BAD
def delete_project(request, project_id):
    Project.objects.get(id=project_id).delete()  # Anyone can delete!
    return redirect('projects')

# GOOD
@login_required
def delete_project(request, project_id):
    project = get_object_or_404(Project, id=project_id)
    if project.owner != request.user:
        return HttpResponseForbidden()
    project.delete()
    return redirect('projects')
```

---

*Last Updated: February 6, 2026*
*Collection of production-tested patterns from UniSync project*
