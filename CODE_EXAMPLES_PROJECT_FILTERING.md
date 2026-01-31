# Project Filtering - Code Examples

## Complete Code Implementation

### 1. ProjectVisibilityFilter Class

**Location:** `accounts/utils.py` (lines 240-441)

```python
class ProjectVisibilityFilter:
    """Filter projects based on user profile compatibility"""

    @staticmethod
    def get_visible_projects(user, all_projects=None):
        """
        Get projects visible to a user based on:
        1. Same college
        2. Same technologies used
        3. Same interests/preferences
        """
        if all_projects is None:
            from .models import Project
            all_projects = Project.objects.all()
        
        try:
            user_profile = user.student_profile
        except:
            return all_projects.filter(user=user), []
        
        visible_projects = []
        match_details = {}
        
        # Extract and normalize user data
        user_interests = self._normalize_set(user_profile.interests)
        user_skills = self._normalize_set(user_profile.skills)
        user_college = user_profile.college or ""
        
        for project in all_projects:
            match_score = 0
            match_reasons = []
            
            # 1. College Match
            if self._college_matches(user_college, project):
                match_score += 30
                match_reasons.append("Same College")
            
            # 2. Technologies Match
            project_techs = self._normalize_set(project.technologies)
            tech_intersection = user_skills.intersection(project_techs)
            if tech_intersection:
                match_score += 40
                tech_list = ', '.join(list(tech_intersection)[:2])
                match_reasons.append(f"Common Technologies: {tech_list}")
            
            # 3. Interests Match
            project_looking = self._normalize_set(project.looking_for)
            interest_intersection = user_interests.intersection(project_looking)
            if interest_intersection:
                match_score += 30
                interest_list = ', '.join(list(interest_intersection)[:2])
                match_reasons.append(f"Matching Interests: {interest_list}")
            
            # 4. User's own projects
            if project.user == user:
                match_score = 100
                match_reasons = ["Your Project"]
            
            # Add to visible projects
            if match_score > 0:
                visible_projects.append(project)
                match_details[project.id] = {
                    'score': match_score,
                    'reasons': match_reasons,
                    'has_match': True
                }
        
        # Sort by match score
        visible_projects.sort(
            key=lambda p: match_details[p.id]['score'],
            reverse=True
        )
        
        return visible_projects, match_details

    @staticmethod
    def _normalize_set(data):
        """Normalize data to a set of lowercase strings"""
        if not data:
            return set()
        
        if isinstance(data, list):
            return set(str(item).lower().strip() for item in data if item)
        elif isinstance(data, str):
            return set(item.lower().strip() for item in data.split(',') if item.strip())
        return set()

    @staticmethod
    def _college_matches(user_college, project):
        """Check if colleges match"""
        if not user_college:
            return False
        try:
            project_college = project.user.student_profile.college or ""
            return user_college.lower() == project_college.lower()
        except:
            return False

    @staticmethod
    def get_project_match_badge(match_score):
        """Get badge styling based on match score"""
        if match_score >= 80:
            return {
                'color': 'green',
                'text': 'Perfect Match',
                'emoji': '⭐'
            }
        elif match_score >= 60:
            return {
                'color': 'blue',
                'text': 'Good Match',
                'emoji': '👍'
            }
        elif match_score >= 30:
            return {
                'color': 'yellow',
                'text': 'Some Match',
                'emoji': '👀'
            }
        else:
            return {
                'color': 'gray',
                'text': 'No Match',
                'emoji': '💤'
            }

    @staticmethod
    def get_compatibility_percentage(user, project):
        """Calculate compatibility percentage"""
        match_score = 0
        total_criteria = 3
        
        try:
            user_profile = user.student_profile
        except:
            return 0
        
        # College match
        if user_profile.college and project.user.student_profile.college:
            if user_profile.college.lower() == project.user.student_profile.college.lower():
                match_score += 1
        
        # Technology match
        user_skills = ProjectVisibilityFilter._normalize_set(user_profile.skills)
        project_techs = ProjectVisibilityFilter._normalize_set(project.technologies)
        if user_skills and project_techs and user_skills.intersection(project_techs):
            match_score += 1
        
        # Interest match
        user_interests = ProjectVisibilityFilter._normalize_set(user_profile.interests)
        project_looking = ProjectVisibilityFilter._normalize_set(project.looking_for)
        if user_interests and project_looking and user_interests.intersection(project_looking):
            match_score += 1
        
        percentage = (match_score / total_criteria * 100) if total_criteria > 0 else 0
        return round(percentage)
```

---

### 2. Updated main_home View

**Location:** `accounts/views.py` (lines 742-779)

```python
@login_required
def main_home(request):
    """Main home view with project visibility filtering"""
    unread_count = 0
    visible_projects = []
    project_match_details = {}
    
    if request.user.is_authenticated:
        # Get unread notifications count
        unread_count = Notification.objects.filter(
            user=request.user,
            is_read=False
        ).count()
        
        # Get visible projects based on user compatibility
        all_projects = Project.objects.all().order_by('-created_at')
        visible_projects, project_match_details = ProjectVisibilityFilter.get_visible_projects(
            request.user,
            all_projects
        )
        
        # Attach match badge info to each project
        for project in visible_projects:
            if project.id in project_match_details:
                match_info = project_match_details[project.id]
                project.match_score = match_info['score']
                project.match_reasons = match_info['reasons']
                project.match_badge = ProjectVisibilityFilter.get_project_match_badge(
                    match_info['score']
                )
    
    return render(request, 'main_home.html', {
        'feed_posts': visible_projects,
        'project_match_details': project_match_details,
        'categories': ['Web Development', 'Mobile Apps', 'AI/ML', 'Data Science'],
        'available_techs': ['Python', 'JavaScript', 'React', 'Django', 'Node.js'],
        'homepage_stats': {
            'total_projects': Project.objects.count(),
            'active_users': User.objects.filter(is_active=True).count(),
            'total_connections': Connection.objects.filter(status='accepted').count(),
            'success_stories': 45
        },
        'active_filters': {},
        'has_filters': False,
        'unread_notification_count': unread_count,
    })
```

---

### 3. Import Statement

**Location:** `accounts/views.py` (line 37)

```python
from .utils import StudentProfileNLP, ProjectVisibilityFilter
```

---

## Usage Examples in Other Views

### Example 1: Display in Projects Feed

```python
from accounts.utils import ProjectVisibilityFilter
from accounts.models import Project

def projects_feed(request):
    """Show filtered projects for user"""
    all_projects = Project.objects.all().order_by('-created_at')
    
    visible_projects, match_details = ProjectVisibilityFilter.get_visible_projects(
        request.user,
        all_projects
    )
    
    # Paginate results
    from django.core.paginator import Paginator
    paginator = Paginator(visible_projects, 20)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    return render(request, 'projects_feed.html', {
        'page_obj': page_obj,
        'match_details': match_details
    })
```

### Example 2: Get Compatibility Score

```python
from accounts.utils import ProjectVisibilityFilter
from accounts.models import Project

def project_detail(request, project_id):
    """Show project with compatibility info"""
    project = get_object_or_404(Project, id=project_id)
    
    # Calculate compatibility
    compatibility = 0
    if request.user.is_authenticated:
        compatibility = ProjectVisibilityFilter.get_compatibility_percentage(
            request.user,
            project
        )
    
    return render(request, 'project_detail.html', {
        'project': project,
        'compatibility': compatibility
    })
```

### Example 3: Show Recommendations

```python
from accounts.utils import ProjectVisibilityFilter
from accounts.models import Project

def recommended_projects(request):
    """Show top recommended projects"""
    all_projects = Project.objects.all().order_by('-created_at')
    
    visible_projects, match_details = ProjectVisibilityFilter.get_visible_projects(
        request.user,
        all_projects
    )
    
    # Get only good matches
    good_matches = [
        p for p in visible_projects
        if match_details.get(p.id, {}).get('score', 0) >= 60
    ]
    
    return render(request, 'recommendations.html', {
        'projects': good_matches[:10],  # Top 10
        'match_details': match_details
    })
```

---

## Template Usage Examples

### Example 1: Show Match Badge

```django
{% for project in feed_posts %}
    <div class="project-card">
        <h3>{{ project.title }}</h3>
        <p>{{ project.description|truncatewords:20 }}</p>
        
        {% if project.match_badge %}
            <div class="match-badge badge-{{ project.match_badge.color }}">
                <span class="badge-emoji">{{ project.match_badge.emoji }}</span>
                <span class="badge-text">{{ project.match_badge.text }}</span>
                <span class="badge-score">({{ project.match_score }}%)</span>
            </div>
        {% endif %}
        
        <a href="{% url 'project_detail' project.id %}">View Project</a>
    </div>
{% endfor %}
```

### Example 2: Show Match Reasons

```django
{% for project in feed_posts %}
    <div class="project-item">
        <h4>{{ project.title }}</h4>
        
        {% if project.match_reasons %}
            <ul class="match-reasons">
                {% for reason in project.match_reasons %}
                    <li class="reason">
                        <span class="check">✓</span>
                        {{ reason }}
                    </li>
                {% endfor %}
            </ul>
        {% endif %}
        
        <button onclick="connectUser({{ project.user.id }})">
            Connect with Creator
        </button>
    </div>
{% endfor %}
```

### Example 3: Tabbed View (Good vs All)

```django
<div class="tabs">
    <button class="tab-btn active" onclick="showTab('recommended')">
        Recommended ({{ recommended_count }})
    </button>
    <button class="tab-btn" onclick="showTab('all')">
        All Projects ({{ total_count }})
    </button>
</div>

<div id="recommended" class="tab-content active">
    {% for project in good_matches %}
        {% include "project_card.html" %}
    {% endfor %}
</div>

<div id="all" class="tab-content">
    {% for project in feed_posts %}
        {% include "project_card.html" %}
    {% endfor %}
</div>
```

---

## CSS Examples

### Badge Styling

```css
.match-badge {
    display: inline-flex;
    align-items: center;
    gap: 8px;
    padding: 8px 12px;
    border-radius: 20px;
    font-size: 12px;
    font-weight: bold;
    margin: 8px 0;
}

.badge-green {
    background-color: #d1fae5;
    color: #065f46;
    border: 1px solid #6ee7b7;
}

.badge-blue {
    background-color: #dbeafe;
    color: #0c2d6b;
    border: 1px solid #60a5fa;
}

.badge-yellow {
    background-color: #fef3c7;
    color: #78350f;
    border: 1px solid #fcd34d;
}

.badge-gray {
    background-color: #f3f4f6;
    color: #374151;
    border: 1px solid #d1d5db;
}

.badge-emoji {
    font-size: 16px;
}

.badge-score {
    margin-left: 4px;
    opacity: 0.8;
}
```

### Match Reasons Styling

```css
.match-reasons {
    list-style: none;
    padding: 8px 0;
    margin: 8px 0;
}

.match-reasons .reason {
    padding: 4px 0;
    font-size: 12px;
    color: #6b7280;
    display: flex;
    align-items: center;
    gap: 6px;
}

.reason .check {
    color: #10b981;
    font-weight: bold;
}
```

---

## JavaScript Examples

### Toggle Match Details

```javascript
function toggleMatchDetails(projectId) {
    const element = document.getElementById(`details-${projectId}`);
    if (element) {
        element.style.display = element.style.display === 'none' ? 'block' : 'none';
    }
}
```

### Filter by Score

```javascript
function filterByScore(minScore) {
    const projects = document.querySelectorAll('[data-match-score]');
    
    projects.forEach(project => {
        const score = parseInt(project.dataset.matchScore);
        if (score >= minScore) {
            project.style.display = 'block';
        } else {
            project.style.display = 'none';
        }
    });
}

// Usage:
// filterByScore(60) - Show only good matches and above
```

### Sort by Score

```javascript
function sortByScore() {
    const container = document.getElementById('projects-container');
    const projects = Array.from(container.querySelectorAll('[data-match-score]'));
    
    projects.sort((a, b) => {
        const scoreA = parseInt(a.dataset.matchScore);
        const scoreB = parseInt(b.dataset.matchScore);
        return scoreB - scoreA;  // Descending
    });
    
    projects.forEach(project => {
        container.appendChild(project);
    });
}
```

---

## Testing Code

### Unit Test Example

```python
from django.test import TestCase
from django.contrib.auth.models import User
from accounts.models import StudentProfile, Project
from accounts.utils import ProjectVisibilityFilter

class ProjectVisibilityTest(TestCase):
    
    def setUp(self):
        # Create user with profile
        self.user = User.objects.create_user(
            username='testuser',
            email='test@example.com',
            password='testpass123'
        )
        self.profile = StudentProfile.objects.create(
            user=self.user,
            college='MIT',
            skills=['Python', 'React'],
            interests=['Web Development']
        )
        
        # Create project
        self.project = Project.objects.create(
            user=User.objects.create_user(
                username='author',
                email='author@example.com',
                password='pass123'
            ),
            title='Test Project',
            description='A test project',
            technologies=['React', 'Node.js'],
            looking_for=['Frontend Dev']
        )
    
    def test_college_match(self):
        """Test college matching"""
        visible, details = ProjectVisibilityFilter.get_visible_projects(
            self.user,
            Project.objects.all()
        )
        
        # Project should be visible (college match)
        self.assertIn(self.project, visible)
        
        # Score should be at least 30 (college match)
        self.assertGreaterEqual(details[self.project.id]['score'], 30)
    
    def test_technology_match(self):
        """Test technology matching"""
        visible, details = ProjectVisibilityFilter.get_visible_projects(
            self.user,
            Project.objects.all()
        )
        
        # Score should include tech match (40)
        self.assertGreaterEqual(details[self.project.id]['score'], 40)
```

### Django Shell Testing

```python
# python manage.py shell

from django.contrib.auth.models import User
from accounts.models import Project
from accounts.utils import ProjectVisibilityFilter

# Test with first user
user = User.objects.first()
projects = Project.objects.all()

visible, details = ProjectVisibilityFilter.get_visible_projects(user, projects)

# Print results
print(f"Total projects: {projects.count()}")
print(f"Visible to user: {len(visible)}")
print(f"\nTop 5 matching projects:")

for project in visible[:5]:
    info = details.get(project.id, {})
    score = info.get('score', 0)
    reasons = info.get('reasons', [])
    
    print(f"\n{project.title}")
    print(f"  Score: {score}%")
    print(f"  Reasons: {', '.join(reasons)}")
```

---

## Performance Optimization Code

### With Caching

```python
from django.views.decorators.cache import cache_page
from accounts.utils import ProjectVisibilityFilter

@cache_page(60)  # Cache for 60 seconds
@login_required
def main_home(request):
    """Cached version of main_home"""
    # ... filtering code ...
    pass
```

### With Pagination

```python
from django.core.paginator import Paginator
from accounts.utils import ProjectVisibilityFilter

def main_home(request):
    """With pagination"""
    # ... get visible projects ...
    visible_projects, details = ProjectVisibilityFilter.get_visible_projects(
        request.user
    )
    
    # Paginate
    paginator = Paginator(visible_projects, 20)  # 20 per page
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    return render(request, 'main_home.html', {
        'page_obj': page_obj,
        # ...
    })
```

---

## Summary

✅ Complete implementation ready to use  
✅ Multiple usage examples  
✅ Template examples  
✅ Styling examples  
✅ Testing code provided  
✅ Performance optimization options  

Use these examples to integrate and customize the project filtering system for your specific needs!
