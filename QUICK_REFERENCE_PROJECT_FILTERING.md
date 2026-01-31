# Quick Reference: Project Visibility Filtering

## What Changed

Projects posted by users are now **only visible to other users** if they match on:
1. ✅ **Same College**
2. ✅ **Same Technologies/Skills**
3. ✅ **Same Interests/Preferences**

---

## How It Works

### Before
- All projects visible to everyone
- No filtering or recommendations

### After
```
User A has skills: Python, React, Django
User A has college: MIT
User A has interests: Web Development, AI/ML

↓

When User A views home page:
- Sees projects from MIT developers ✅
- Sees projects using Python/React/Django ✅
- Sees projects for Web Dev / AI/ML roles ✅
- Doesn't see unrelated projects ❌
```

---

## Match Score System

| Score Range | Badge | Meaning | Color |
|-----------|-------|---------|-------|
| 80-100 | ⭐ Perfect Match | All/most criteria match | 🟢 Green |
| 60-79 | 👍 Good Match | Some criteria match | 🔵 Blue |
| 30-59 | 👀 Some Match | Partial match | 🟡 Yellow |
| 0-29 | 💤 No Match | No matches | ⚪ Gray |

---

## Scoring Breakdown

```
College Match        = +30 points
Technology Match     = +40 points
Interest Match       = +30 points
User's Own Project   = 100 points (fixed)
```

---

## Example

### User Profile
```
College: MIT
Skills: Python, React, JavaScript
Interests: Web Development, Frontend
```

### Project 1
```
Owner: MIT student
Technologies: React, Node.js
Looking for: Frontend Developer

Matches:
✅ College (MIT)     = +30
✅ Tech (React)      = +40
✅ Interest (Frontend) = +30
TOTAL = 100% (Perfect Match ⭐)
```

### Project 2
```
Owner: Stanford student
Technologies: Java, Spring Boot
Looking for: Backend Developer

Matches:
❌ College (Stanford) = +0
❌ Tech (no match)    = +0
❌ Interest (Backend) = +0
TOTAL = 0% (No Match 💤)
```

---

## Files Modified

### 1. `accounts/utils.py`
**Added:** `ProjectVisibilityFilter` class
- `get_visible_projects()` - Main filtering function
- `get_project_match_badge()` - Badge styling
- `get_compatibility_percentage()` - Score calculation

### 2. `accounts/views.py`
**Modified:** `main_home()` function
- Import `ProjectVisibilityFilter`
- Filter projects before rendering
- Attach match info to each project

---

## How to Use

### In Views
```python
from .utils import ProjectVisibilityFilter

# Get filtered projects for current user
visible_projects, match_details = ProjectVisibilityFilter.get_visible_projects(
    request.user
)

# Or with custom project list
visible_projects, match_details = ProjectVisibilityFilter.get_visible_projects(
    request.user,
    all_projects=custom_queryset
)

# Each project now has:
# - project.match_score (0-100)
# - project.match_reasons (list of reasons)
# - project.match_badge (dict with color, text, emoji)
```

### In Templates (Optional)
```django
{% for project in feed_posts %}
    <div class="project-card">
        <h2>{{ project.title }}</h2>
        
        {% if project.match_badge %}
            <span class="badge {{ project.match_badge.color }}">
                {{ project.match_badge.emoji }}
                {{ project.match_badge.text }}
            </span>
        {% endif %}
        
        {% if project.match_reasons %}
            <ul>
            {% for reason in project.match_reasons %}
                <li>{{ reason }}</li>
            {% endfor %}
            </ul>
        {% endif %}
    </div>
{% endfor %}
```

---

## Key Benefits

✅ **Better Recommendations** - Users see relevant projects  
✅ **Higher Quality Matches** - More likely to connect successfully  
✅ **Reduced Noise** - Don't see unrelated projects  
✅ **Easy to Extend** - Add more matching criteria anytime  
✅ **Flexible** - Works with list or string data formats  

---

## Common Issues & Solutions

### Issue: Projects not showing up
**Solution:** Check user profile has college/skills/interests filled

### Issue: Wrong match score
**Solution:** Verify data format (list or string), ensure data is normalized

### Issue: Performance slow with many projects
**Solution:** Add pagination, implement caching, optimize database

---

## Testing

```python
# Quick test in Django shell
from django.contrib.auth.models import User
from accounts.utils import ProjectVisibilityFilter
from accounts.models import Project

user = User.objects.first()
projects = Project.objects.all()
visible, details = ProjectVisibilityFilter.get_visible_projects(user, projects)

print(f"Total projects: {projects.count()}")
print(f"Visible to user: {len(visible)}")
print(f"Match details: {details}")
```

---

## Data Format Support

Both formats are automatically handled:

```python
# Format 1: List (JSONField)
profile.skills = ['Python', 'React', 'Django']
project.technologies = ['Django', 'React']

# Format 2: String (comma-separated)
profile.skills = 'Python,React,Django'
project.technologies = 'Django,React'

# Both work! Filter normalizes automatically.
```

---

## Customization Examples

### Adjust Scoring Weights

```python
# In ProjectVisibilityFilter.get_visible_projects():

# Make technology more important
if tech_intersection:
    match_score += 50  # Was 40

# Make college less important
if college_match:
    match_score += 20  # Was 30
```

### Change Badge Thresholds

```python
# In ProjectVisibilityFilter.get_project_match_badge():

if match_score >= 70:      # Was 80
    return {'color': 'green', 'text': 'Perfect Match', ...}
```

### Add New Matching Criteria

```python
# In get_visible_projects(), after interest match:

# 4. Category Match (new!)
project_category = project.category or ""
user_categories = ['web', 'ai']  # From user preferences

if user_categories and project_category in user_categories:
    match_score += 20  # New weight
    match_reasons.append("Matching Category")
```

---

## Performance Tips

1. **Use pagination** to limit projects per page
2. **Cache results** for 60 seconds if many projects
3. **Add database indexes** on college, technologies fields
4. **Monitor query count** with Django Debug Toolbar

---

## Next Steps

### To Display Match Info in Template:
1. Update `main_home.html` to show badges
2. Add CSS styling for match badges
3. Test with different user profiles

### To Add More Matching Criteria:
1. Edit `ProjectVisibilityFilter.get_visible_projects()`
2. Add new matching logic
3. Update scoring weights
4. Test thoroughly

### To Optimize Performance:
1. Implement caching decorator
2. Add database-level filtering with Q objects
3. Use pagination
4. Profile with Django Debug Toolbar

---

## Summary

✅ Projects now intelligently filtered  
✅ Match college, technologies, interests  
✅ Show match scores and reasons  
✅ Easy to customize  
✅ Better user experience  

The filtering happens automatically in the `main_home()` view. Projects are sorted by match score, so the most relevant ones appear first!
