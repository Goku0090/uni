# Project Visibility & Filtering System Implementation

## Overview

Implemented intelligent project filtering system that shows projects to users based on profile compatibility:
- **Same College**
- **Same Technologies/Skills**
- **Same Interests/Preferences**

---

## Features Implemented

### 1. ProjectVisibilityFilter Class

**Location:** `accounts/utils.py`

A utility class with static methods for filtering and matching projects with users.

#### Methods:

##### `get_visible_projects(user, all_projects=None)`
- **Purpose:** Filter projects based on user compatibility
- **Input:**
  - `user`: Django User object
  - `all_projects`: QuerySet of projects (optional, fetches all if None)
- **Output:** Tuple of (filtered_projects, match_details_dict)
- **Algorithm:**
  1. Extracts user profile data (college, skills, interests)
  2. Normalizes all data (lowercase, strip whitespace)
  3. For each project, calculates match score:
     - College match: +30 points
     - Technology match: +40 points
     - Interest/preference match: +30 points
     - User's own projects: 100 points
  4. Sorts by match score (highest first)
  5. Returns projects and detailed match info

##### `get_project_match_badge(match_score)`
- **Purpose:** Return badge styling based on compatibility score
- **Returns:** Dictionary with color, text, and emoji
- **Scoring:**
  ```
  >= 80  → Perfect Match ⭐ (Green)
  >= 60  → Good Match 👍 (Blue)
  >= 30  → Some Match 👀 (Yellow)
  < 30   → No Match 💤 (Gray)
  ```

##### `get_compatibility_percentage(user, project)`
- **Purpose:** Calculate exact compatibility percentage
- **Returns:** Integer 0-100
- **Calculation:** (matched_criteria / total_criteria) × 100
  - Criteria: College (33%), Technologies (33%), Interests (33%)

---

## Implementation Details

### Data Normalization

Projects and user profiles use either **list** or **comma-separated string** formats:

```python
# Format 1: JSONField as List
profile.skills = ['Python', 'JavaScript', 'React']
project.technologies = ['Django', 'React', 'PostgreSQL']

# Format 2: String format
profile.skills = 'Python,JavaScript,React'
project.technologies = 'Django,React,PostgreSQL'
```

The filter handles both formats automatically:
- Convert to lowercase for comparison
- Split strings by comma
- Remove whitespace
- Deduplicate using sets

### Matching Algorithm

#### College Match (30 points)
```python
if user_college.lower() == project_college.lower():
    match_score += 30
```

#### Technology Match (40 points)
```python
user_skills = {'python', 'react', 'javascript'}
project_techs = {'react', 'django', 'nodejs'}
intersection = {'react'}  # Common technology

if intersection:
    match_score += 40
```

#### Interest/Preference Match (30 points)
```python
user_interests = {'web development', 'frontend'}
project_looking = {'full-stack developer', 'frontend'}
intersection = {'frontend'}

if intersection:
    match_score += 30
```

#### User's Own Projects (100 points)
```python
if project.user == request.user:
    match_score = 100
    match_reasons = ["Your Project"]
```

---

## View Integration

### Updated: `main_home()` View

**Location:** `accounts/views.py` (Line 742)

#### Changes:
1. Import ProjectVisibilityFilter
2. Check if user is authenticated
3. Fetch all projects
4. Apply visibility filter
5. Attach match info to each project
6. Pass to template

#### Code:
```python
@login_required
def main_home(request):
    """Main home view with project visibility filtering"""
    unread_count = 0
    visible_projects = []
    project_match_details = {}
    
    if request.user.is_authenticated:
        # Get unread notifications
        unread_count = Notification.objects.filter(
            user=request.user, 
            is_read=False
        ).count()
        
        # Get visible projects based on compatibility
        all_projects = Project.objects.all().order_by('-created_at')
        visible_projects, project_match_details = ProjectVisibilityFilter.get_visible_projects(
            request.user,
            all_projects
        )
        
        # Add match details to each project for template rendering
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
        'unread_notification_count': unread_count,
        # ... other context ...
    })
```

---

## Template Integration (Optional)

### Using Match Info in Templates

```django
{% for project in feed_posts %}
    <div class="project-card">
        <h3>{{ project.title }}</h3>
        <p>{{ project.description }}</p>
        
        <!-- Match Badge -->
        {% if project.match_badge %}
            <div class="match-badge {{ project.match_badge.color }}">
                {{ project.match_badge.emoji }}
                {{ project.match_badge.text }}
                ({{ project.match_score }}%)
            </div>
        {% endif %}
        
        <!-- Match Reasons -->
        {% if project.match_reasons %}
            <ul class="match-reasons">
                {% for reason in project.match_reasons %}
                    <li>✓ {{ reason }}</li>
                {% endfor %}
            </ul>
        {% endif %}
    </div>
{% endfor %}
```

### CSS Styling Example

```css
.match-badge {
    padding: 8px 12px;
    border-radius: 20px;
    font-size: 12px;
    font-weight: bold;
    display: inline-block;
    margin-top: 8px;
}

.match-badge.green {
    background-color: #d1fae5;
    color: #065f46;
    border: 1px solid #6ee7b7;
}

.match-badge.blue {
    background-color: #dbeafe;
    color: #0c2d6b;
    border: 1px solid #60a5fa;
}

.match-badge.yellow {
    background-color: #fef3c7;
    color: #78350f;
    border: 1px solid #fcd34d;
}

.match-badge.gray {
    background-color: #f3f4f6;
    color: #374151;
    border: 1px solid #d1d5db;
}

.match-reasons {
    list-style: none;
    padding: 8px 0;
    font-size: 12px;
    color: #6b7280;
}

.match-reasons li {
    padding: 4px 0;
}
```

---

## Data Flow

```
User visits main_home
    ↓
Django checks if user is authenticated
    ↓
Fetch user's StudentProfile (college, skills, interests)
    ↓
Fetch all projects from database
    ↓
ProjectVisibilityFilter processes each project:
    - Extract user profile data
    - Extract project data
    - Normalize all data
    - Calculate match scores
    - Generate match badges
    ↓
Sort projects by match score (descending)
    ↓
Attach match info to each project object
    ↓
Render template with filtered projects and match details
    ↓
Template displays projects with match badges
```

---

## Example Scenarios

### Scenario 1: Perfect College + Technology Match

**User Profile:**
```
College: "MIT"
Skills: ["Python", "React", "Django"]
Interests: ["Web Development", "AI/ML"]
```

**Project:**
```
Owner: Student from MIT
Technologies: ["React", "Node.js", "MongoDB"]
Looking For: ["Frontend Developer", "Full Stack"]
```

**Result:**
```
College Match: +30 (Same college: MIT)
Tech Match: +40 (Common: React)
Interest Match: +0 (No matching interests)
Total Score: 70

Badge: Good Match 👍 (Blue, 70%)
Reasons: 
  - Same College
  - Common Technologies: React
```

---

### Scenario 2: Technology + Interest Match Only

**User Profile:**
```
College: "Stanford"
Skills: ["Python", "TensorFlow", "PyTorch"]
Interests: ["AI/ML", "Data Science"]
```

**Project:**
```
Owner: Student from MIT
Technologies: ["Python", "TensorFlow", "Jupyter"]
Looking For: ["AI/ML Engineer", "Data Scientist"]
```

**Result:**
```
College Match: +0 (Different colleges)
Tech Match: +40 (Common: Python, TensorFlow)
Interest Match: +30 (Common: AI/ML, Data Science)
Total Score: 70

Badge: Good Match 👍 (Blue, 70%)
Reasons:
  - Common Technologies: Python, TensorFlow
  - Matching Interests: AI/ML, Data Science
```

---

### Scenario 3: No Match

**User Profile:**
```
College: "Harvard"
Skills: ["Java", "Spring Boot"]
Interests: ["Backend Development"]
```

**Project:**
```
Owner: Student from MIT
Technologies: ["React", "Vue", "Angular"]
Looking For: ["Frontend Developer", "UI Designer"]
```

**Result:**
```
College Match: +0 (Different colleges)
Tech Match: +0 (No common technologies)
Interest Match: +0 (No matching interests)
Total Score: 0

Badge: No Match 💤 (Gray, 0%)
Reasons:
  - No direct match
```

---

### Scenario 4: User's Own Project

**Any scenario where project owner == current user:**

```
Match Score: 100 (always)
Badge: Perfect Match ⭐ (Green, 100%)
Reasons: ["Your Project"]
```

---

## Performance Considerations

### Current Approach
- **Pros:**
  - Simple and readable
  - Flexible matching criteria
  - Handles both list and string formats
  - Sorts by relevance
  
- **Cons:**
  - O(n) complexity for each user (n = number of projects)
  - No database-level filtering
  - Recalculates on every request

### Optimization Strategies

#### Option 1: Database Query Optimization
```python
# Instead of filtering in Python
visible_projects, match_details = ProjectVisibilityFilter.get_visible_projects(request.user)

# Use Django ORM with Q objects
from django.db.models import Q

projects = Project.objects.filter(
    Q(technologies__contains=user_skill) |
    Q(looking_for__contains=user_interest) |
    Q(user__student_profile__college=user_college)
).order_by('-created_at')
```

#### Option 2: Caching
```python
from django.views.decorators.cache import cache_page

@cache_page(60)  # Cache for 60 seconds
def main_home(request):
    # ... filtering logic ...
```

#### Option 3: Pagination
```python
from django.core.paginator import Paginator

paginator = Paginator(visible_projects, 20)  # 20 per page
page_number = request.GET.get('page')
page_obj = paginator.get_page(page_number)

return render(request, 'main_home.html', {
    'page_obj': page_obj,
    # ...
})
```

---

## Testing Checklist

### Manual Testing

- [ ] User with complete profile views home page
- [ ] Same college projects appear with college match badge
- [ ] Same technology projects appear with tech match badge
- [ ] Same interests projects appear with interest match badge
- [ ] User's own projects show 100% match
- [ ] Projects with no match show "No Match" badge
- [ ] Match scores are correct
- [ ] Projects sorted by match score (highest first)
- [ ] User without profile views home page (no errors)
- [ ] Filter handles both list and string formats
- [ ] Unauthenticated users see appropriate content

### Unit Tests

```python
# Example test cases
def test_college_match():
    user = create_test_user(college="MIT")
    project = create_test_project(college="MIT")
    
    visible, details = ProjectVisibilityFilter.get_visible_projects(user, [project])
    
    assert details[project.id]['score'] >= 30
    assert "Same College" in details[project.id]['reasons']

def test_technology_match():
    user = create_test_user(skills=["Python", "React"])
    project = create_test_project(technologies=["React", "Node.js"])
    
    visible, details = ProjectVisibilityFilter.get_visible_projects(user, [project])
    
    assert details[project.id]['score'] >= 40
    assert "Common Technologies" in details[project.id]['reasons']

def test_no_match():
    user = create_test_user(college="MIT", skills=["Java"])
    project = create_test_project(college="Stanford", technologies=["Python"])
    
    visible, details = ProjectVisibilityFilter.get_visible_projects(user, [project])
    
    assert details[project.id]['score'] == 0

def test_user_own_project():
    user = create_test_user()
    project = create_test_project(owner=user)
    
    visible, details = ProjectVisibilityFilter.get_visible_projects(user, [project])
    
    assert details[project.id]['score'] == 100
    assert "Your Project" in details[project.id]['reasons']
```

---

## Future Enhancements

### 1. Advanced Matching
- Fuzzy string matching for tech names (e.g., "JS" → "JavaScript")
- Category-based matching (frontend vs backend)
- Weighted scoring (tech more important than interests)

### 2. User Preferences
- Let users control visibility settings
- Option to "hide" projects they're not interested in
- Custom filter criteria

### 3. Real-time Updates
- Notify users when matching projects are posted
- Show "New Matching Projects" badge
- WebSocket integration for live filtering

### 4. Analytics
- Track which filter criteria lead to connections
- Show users why certain projects are recommended
- A/B test different matching algorithms

### 5. Performance
- Implement background task for pre-computing matches
- Use Elasticsearch for full-text tech search
- Cache match results per user

### 6. Machine Learning
- Learn from user interactions (clicks, connections)
- Improve recommendations over time
- Collaborative filtering with similar users

---

## Configuration

### Adjust Scoring Weights

**File:** `accounts/utils.py` (ProjectVisibilityFilter class)

```python
# Current weights:
COLLEGE_WEIGHT = 30      # Percentage of total score
TECHNOLOGY_WEIGHT = 40
INTEREST_WEIGHT = 30

# To change, modify these lines in get_visible_projects():
match_score += 30  # Change 30 to desired college weight
match_score += 40  # Change 40 to desired tech weight
match_score += 30  # Change 30 to desired interest weight
```

### Adjust Badge Thresholds

**File:** `accounts/utils.py` (get_project_match_badge method)

```python
# Current thresholds:
if match_score >= 80:      # Perfect match threshold
    return {'color': 'green', 'text': 'Perfect Match', 'emoji': '⭐'}
elif match_score >= 60:    # Good match threshold
    return {'color': 'blue', 'text': 'Good Match', 'emoji': '👍'}
elif match_score >= 30:    # Some match threshold
    return {'color': 'yellow', 'text': 'Some Match', 'emoji': '👀'}
```

---

## Summary

✅ Implemented intelligent project filtering  
✅ Matches on college, technologies, and interests  
✅ Calculates and displays match scores  
✅ Shows helpful match reasons  
✅ Sorts projects by relevance  
✅ Handles different data formats  
✅ User-friendly badge system  
✅ Easy to customize and extend  

The system makes UniSync more relevant by connecting students with projects they're actually interested in and qualified for.
