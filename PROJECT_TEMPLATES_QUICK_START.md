# Project Templates - Quick Start Guide

## What's New ⭐

Your app now has a complete **Project Templates** system to help new users quickly create projects!

---

## 3-Step Setup

### 1️⃣ Run Migrations

```bash
python manage.py migrate
```

This creates 3 new database tables:
- `ProjectTemplate` - Stores template definitions
- `TemplateRating` - User ratings for templates
- `TemplateUsageLog` - Tracks when templates are used

### 2️⃣ Load Default Templates

```bash
python manage.py create_templates
```

This adds 10 pre-made templates:
- 🛍️ E-Commerce Web App
- 💪 Mobile Fitness App
- 🤖 AI Chatbot
- 📊 Data Analytics Dashboard
- ⛓️ Blockchain Wallet
- 🏠 IoT Smart Home
- 🎮 2D Game Development
- ☁️ SaaS Platform
- 👥 Social Network
- + More!

### 3️⃣ Add Link to Navigation

Add to your navbar/main template:
```html
<a href="{% url 'templates_list' %}" class="nav-link">
    📋 Templates
</a>
```

---

## Features at a Glance

### 🎯 One-Click Project Creation
```
User clicks Template → Pre-filled form appears → Project created instantly
```

### ⭐ User Rating System
```
Browse templates → See ratings and reviews → Rate templates → Share feedback
```

### 📊 Usage Tracking
```
Track which templates are most popular
See how many projects each template created
Analytics-ready data
```

### 🏷️ Smart Organization
```
Filter by category (Web, Mobile, AI, Data, Blockchain, IoT, Game)
Filter by difficulty (Beginner, Intermediate, Advanced)
Sort by rating, popularity, or name
```

### 📚 Learning Resources
```
Each template includes:
- Example projects on GitHub
- Links to tutorials and documentation
- Technology recommendations
- Team size and timeline estimates
```

---

## User Experience Flow

### New User Journey

1. **Discovers Templates**
   ```
   Visit /templates/
   See 10 featured templates with icons
   Browse by category or difficulty
   ```

2. **Explores Template**
   ```
   Click on template (e.g., "E-Commerce Web App")
   See full details:
   - What the project does
   - Technologies recommended
   - Roles needed (Frontend, Backend, etc.)
   - Timeline and team size
   - Learning resources
   - Average rating
   ```

3. **Creates Project**
   ```
   Click "Use This Template"
   Form auto-fills with:
   - Title: "E-Commerce Platform"
   - Description: Complete with features
   - Technologies: [React, Node.js, MongoDB, ...]
   - Roles: [Full Stack, Frontend, Backend]
   - Category: Web Development
   - Timeline: 3-4 months
   ```

4. **Customizes Project**
   ```
   Edit any field as needed
   Add GitHub link or other details
   Submit to create project
   ```

5. **Rates Template**
   ```
   After creating project from template
   Visit template page
   Rate 1-5 stars
   Optionally write review
   ```

---

## Available Endpoints

### Web Pages
- `GET /templates/` - Browse all templates
- `GET /templates/<id>/` - View template details
- `GET /templates/<id>/use/` - Use template to create project
- `POST /templates/<id>/rate/` - Rate a template

### REST API
- `GET /api/templates/` - List templates (JSON)
- `GET /api/templates/<id>/` - Get template (JSON)
- `POST /api/templates/<id>/create-project/` - Create project via API
- `POST /api/templates/<id>/rate/` - Rate via API

### Query Parameters
```
# List templates with filters
GET /templates/?category=web&sort=-rating

# API with filtering
GET /api/templates/?category=mobile&difficulty=beginner&search=app
```

---

## How to Customize

### Add a New Template (Admin)

In Django admin or shell:
```python
from accounts.models import ProjectTemplate

ProjectTemplate.objects.create(
    name="My Template",
    category="web",
    description="Template description",
    icon="🎨",
    template_title="Project Title",
    template_description="Project description with details",
    template_technologies=["React", "Node.js", "MongoDB"],
    template_looking_for=["Frontend Developer", "Backend Developer"],
    suggested_timeline="2 months",
    difficulty_level="intermediate",
    is_featured=True  # Show at top
)
```

### Feature a Template
```python
template = ProjectTemplate.objects.get(id=1)
template.is_featured = True
template.save()
```

### Archive Template
```python
template = ProjectTemplate.objects.get(id=1)
template.is_active = False
template.save()
```

---

## Database Schema

### ProjectTemplate
```
- id: Primary Key
- name: Unique template name
- category: web, mobile, ai, data, blockchain, iot, game, other
- description: What template is for
- icon: Emoji (🛍️, 💪, etc.)
- template_title: Pre-filled project title
- template_description: Pre-filled description
- template_technologies: JSON array
- template_looking_for: JSON array of roles
- suggested_timeline: "2-3 months"
- suggested_team_size: "2-4 people"
- difficulty_level: beginner, intermediate, advanced
- example_projects: URL links
- learning_resources: URL links
- rating: Float 0-5 (average)
- rating_count: Number of ratings
- usage_count: Times used
- is_active: Boolean
- is_featured: Boolean
- created_at, updated_at: Timestamps
```

### TemplateRating
```
- id: Primary Key
- template: ForeignKey
- user: ForeignKey
- rating: 1-5 (Integer)
- review: Optional text
- helpful_count: Integer
- created_at, updated_at: Timestamps
- unique_together: (template, user)
```

### TemplateUsageLog
```
- id: Primary Key
- template: ForeignKey
- user: ForeignKey
- project: ForeignKey (can be null)
- created_at: Timestamp
```

---

## Example Templates Included

| Icon | Name | Category | Difficulty | Team | Timeline |
|------|------|----------|-----------|------|----------|
| 🛍️ | E-Commerce Web App | Web | Intermediate | 3-5 | 3-4 mo |
| 💪 | Mobile Fitness App | Mobile | Intermediate | 2-4 | 2-3 mo |
| 🤖 | AI Chatbot | AI | Advanced | 2-3 | 2-3 mo |
| 📊 | Data Analytics Dashboard | Data | Intermediate | 2-4 | 2-3 mo |
| ⛓️ | Blockchain Wallet | Blockchain | Advanced | 3-4 | 3-4 mo |
| 🏠 | IoT Smart Home | IoT | Advanced | 2-3 | 2-3 mo |
| 🎮 | 2D Game Development | Game | Intermediate | 3-5 | 2-3 mo |
| ☁️ | SaaS Platform | Web | Advanced | 3-5 | 3-4 mo |
| 👥 | Social Network | Web | Intermediate | 3-5 | 3-4 mo |
| ➕ | Add your own! | Any | Any | Any | Any |

---

## Analytics You Can Track

### View Most Popular Templates
```python
from accounts.models import ProjectTemplate

# Top templates by usage
ProjectTemplate.objects.order_by('-usage_count')[:5]

# Top templates by rating
ProjectTemplate.objects.order_by('-rating')[:5]

# Most rated templates (with enough ratings)
ProjectTemplate.objects.filter(rating_count__gte=5).order_by('-rating')
```

### Track User Activity
```python
# Templates user has rated
from accounts.models import TemplateRating
TemplateRating.objects.filter(user=request.user)

# Projects user created from templates
from accounts.models import TemplateUsageLog
TemplateUsageLog.objects.filter(user=request.user)
```

### Dashboard Stats
```python
from django.db.models import Count, Avg

# Total projects created from templates
TemplateUsageLog.objects.count()

# Average rating across all templates
ProjectTemplate.objects.aggregate(Avg('rating'))

# Templates by category
ProjectTemplate.objects.values('category').annotate(Count('id'))
```

---

## Common Use Cases

### Case 1: New User Needs Project Ideas
```
1. Visit /templates/
2. Browse 10 featured templates
3. Click interesting one
4. Read description and resources
5. Click "Use This Template"
6. Gets pre-filled project form
7. Customizes and creates project
```

### Case 2: User Wants to Learn
```
1. Visit /templates/
2. Find template for skill they want to learn
3. View template details
4. Find learning resources links
5. Click tutorial/docs links
6. Study examples
7. Create project using template to practice
```

### Case 3: User Wants Recommendations
```
1. Visit /templates/
2. Filter by difficulty "Beginner"
3. Filter by category "Mobile"
4. See highest-rated templates first
5. Read reviews from other users
6. Pick one with best ratings
7. Use template to start project
```

### Case 4: Admin Wants Analytics
```
1. Go to Django admin
2. View ProjectTemplate list
3. Sort by usage_count
4. See most popular templates
5. See which categories are popular
6. Feature new templates based on demand
```

---

## API Examples

### JavaScript: List Templates
```javascript
fetch('/api/templates/?category=web&difficulty=beginner')
  .then(r => r.json())
  .then(data => {
    console.log(data.results)
    // Display templates on page
  })
```

### JavaScript: Create Project from Template
```javascript
fetch('/api/templates/1/create-project/', {
  method: 'POST',
  headers: {
    'Content-Type': 'application/json',
    'X-CSRFToken': getCookie('csrftoken')
  },
  body: JSON.stringify({
    title: 'My Custom E-Commerce',
    technologies: ['React', 'Node.js'],
    looking_for: ['Frontend Developer']
  })
})
.then(r => r.json())
.then(data => {
  if (data.success) {
    window.location.href = `/edit-project/${data.project_id}/`
  }
})
```

### JavaScript: Rate Template
```javascript
fetch('/api/templates/1/rate/', {
  method: 'POST',
  headers: {
    'Content-Type': 'application/json',
    'X-CSRFToken': getCookie('csrftoken')
  },
  body: JSON.stringify({
    rating: 5,
    review: 'Excellent template!'
  })
})
.then(r => r.json())
.then(data => {
  console.log(`New average: ${data.new_rating}⭐`)
})
```

---

## Troubleshooting

### Templates not showing
```bash
# Check if templates exist
python manage.py shell
>>> from accounts.models import ProjectTemplate
>>> ProjectTemplate.objects.count()  # Should be 10+

# If 0, run:
python manage.py create_templates
```

### User rating not saving
```bash
# Check if TemplateRating table exists
python manage.py dbshell
> SELECT * FROM accounts_templaterating;

# If empty, user needs to POST to /templates/<id>/rate/
```

### URL not found
```bash
# Check URLs are registered
python manage.py shell
>>> from django.urls import reverse
>>> reverse('templates_list')  # Should return '/templates/'
>>> reverse('template_detail', args=[1])  # Should return '/templates/1/'
```

---

## Next Steps

1. **Run migrations** ✅
2. **Create templates** ✅
3. **Add navigation link** ✅
4. **Test the feature** ✅
5. **Gather user feedback** 📊
6. **Add/customize templates** 🎨
7. **Track analytics** 📈
8. **Promote templates** 📣

---

## Files Added

```
accounts/
├── models.py                    # Added 3 models
├── template_api.py              # NEW - All template views
├── serializers.py               # Added 2 serializers
├── urls.py                      # Added 11 URL patterns
└── management/commands/
    └── create_templates.py      # NEW - Management command
```

## Key Classes

```python
ProjectTemplate      # Template definition
TemplateRating       # User ratings
TemplateUsageLog     # Usage tracking

# Views
templates_list_view()
template_detail_view()
use_template_view()
rate_template()

# APIs
ProjectTemplateListView
ProjectTemplateDetailView
api_create_from_template()
api_rate_template()
```

---

## Support

For questions or issues:
1. Check the detailed guide: `PROJECT_TEMPLATES_IMPLEMENTATION_GUIDE.md`
2. View API docs in urls.py
3. Check model definitions in models.py
4. Review view implementations in template_api.py

Enjoy the new templates feature! 🎉
