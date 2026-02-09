# Project Templates - Quick Reference Card

## ⚡ 3-Step Setup

```bash
# 1. Migrate database
python manage.py migrate

# 2. Create 10 templates
python manage.py create_templates

# 3. Add to navbar
<a href="{% url 'templates_list' %}">📋 Templates</a>
```

---

## 🎯 Core Components

### 3 Models
```python
ProjectTemplate     # Template definitions + ratings
TemplateRating      # User ratings (1-5 stars)
TemplateUsageLog    # Track template usage
```

### 11 Endpoints
```
GET    /templates/                     # List
GET    /templates/<id>/               # Details
GET    /templates/<id>/use/            # Use form
POST   /templates/<id>/rate/           # Rate (AJAX)
GET    /api/templates/                # List (JSON)
POST   /api/templates/<id>/create-project/  # Create
... (5 more)
```

### 10 Templates
```
🛍️ E-Commerce  💪 Fitness   🤖 AI
📊 Analytics   ⛓️ Blockchain 🏠 IoT
🎮 Game        ☁️ SaaS      👥 Social
➕ Custom
```

---

## 📊 Key Features

| Feature | Status |
|---------|--------|
| One-click creation | ✅ |
| Auto-filled forms | ✅ |
| 1-5 star rating | ✅ |
| Usage tracking | ✅ |
| Learning resources | ✅ |
| Smart filtering | ✅ |
| REST API | ✅ |
| Admin interface | ✅ |

---

## 🔗 URLs

### User Pages
```
/templates/              # List templates
/templates/1/            # Template details
/templates/1/use/        # Create from template
/templates/1/rate/       # Rate template
```

### API
```
/api/templates/                    # List (JSON)
/api/templates/1/                 # Details (JSON)
/api/templates/1/create-project/  # Create project
/api/templates/1/rate/            # Rate template
```

---

## 💾 Database Fields

### ProjectTemplate
```
id, name, category, description, icon
template_title, template_description
template_technologies, template_looking_for
suggested_timeline, suggested_team_size
difficulty_level, example_projects, learning_resources
rating, rating_count, usage_count
is_active, is_featured, created_at, updated_at
```

### TemplateRating
```
id, template_id, user_id
rating (1-5), review (optional)
helpful_count, created_at, updated_at
```

### TemplateUsageLog
```
id, template_id, user_id, project_id
created_at
```

---

## 🚀 Quick Test

```bash
# 1. Test in Django shell
python manage.py shell

# 2. Check templates created
from accounts.models import ProjectTemplate
print(ProjectTemplate.objects.count())  # Should be 10

# 3. Test web view
# Visit http://localhost:8000/templates/

# 4. Test API
# Visit http://localhost:8000/api/templates/
```

---

## 📈 Analytics Queries

```python
# Most popular templates
ProjectTemplate.objects.order_by('-usage_count')[:5]

# Highest rated
ProjectTemplate.objects.order_by('-rating')[:5]

# Template usage by user
TemplateUsageLog.objects.filter(user=request.user)

# Template ratings by user
TemplateRating.objects.filter(user=request.user)
```

---

## 🎨 Frontend Integration

### Add Link
```html
<a href="{% url 'templates_list' %}">📋 Templates</a>
```

### Display Templates
```html
{% for template in templates %}
  <div class="template">
    <span>{{ template.icon }}</span>
    <h3>{{ template.name }}</h3>
    <p>{{ template.description|truncatewords:15 }}</p>
    <div>⭐ {{ template.rating }}/5</div>
    <a href="{% url 'use_template' template.id %}">Use →</a>
  </div>
{% endfor %}
```

---

## 🔧 Common Tasks

### Add New Template
```python
from accounts.models import ProjectTemplate

ProjectTemplate.objects.create(
    name="My Template",
    category="web",
    description="Description",
    icon="🎨",
    template_title="Title",
    template_description="Description",
    template_technologies=["Tech1", "Tech2"],
    template_looking_for=["Role1", "Role2"]
)
```

### Feature Template
```python
template = ProjectTemplate.objects.get(id=1)
template.is_featured = True
template.save()
```

### Archive Template
```python
template.is_active = False
template.save()
```

### Get User Rating
```python
from accounts.models import TemplateRating

rating = TemplateRating.objects.get(
    template_id=1,
    user=request.user
)
print(rating.rating)  # 1-5
```

---

## 🐛 Troubleshooting

### Templates not showing
```bash
python manage.py create_templates
```

### URL not found
```bash
python manage.py shell
from django.urls import reverse
reverse('templates_list')  # Should return '/templates/'
```

### Rating not saving
Check if user is authenticated:
```python
if request.user.is_authenticated:
    # Can rate
```

---

## 📚 Documentation Files

| File | Content |
|------|---------|
| PROJECT_TEMPLATES_QUICK_START.md | Setup in 3 steps |
| PROJECT_TEMPLATES_IMPLEMENTATION_GUIDE.md | Complete guide |
| PROJECT_TEMPLATES_SUMMARY.md | Feature summary |
| PROJECT_TEMPLATES_DEPLOYMENT_CHECKLIST.md | Deploy guide |

---

## ✅ Checklist

- [ ] Run migrations
- [ ] Create templates
- [ ] Add navigation link
- [ ] Test /templates/ page
- [ ] Test /api/templates/
- [ ] Test create project
- [ ] Test rating system
- [ ] Deploy to production

---

## 📞 Support

**Quick Question?** → Check QUICK_START file
**Need Details?** → Check IMPLEMENTATION_GUIDE file
**Deploying?** → Check DEPLOYMENT_CHECKLIST file
**Code Issue?** → Check model/view docstrings

---

## 🎁 What You Get

✅ 10 pre-made templates
✅ 11 API endpoints
✅ One-click project creation
✅ 1-5 star rating system
✅ Usage tracking
✅ Learning resources
✅ 2000+ lines documentation
✅ Production ready

**Status: COMPLETE ✅**
