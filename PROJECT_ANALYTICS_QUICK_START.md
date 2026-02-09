# Project Analytics Dashboard - Quick Start Guide

## ⚡ 5-Step Implementation

### Step 1: Add Models (30 min)
```bash
# 1. Open: auth_project/accounts/models.py
# 2. Add three models at the end:
#    - ProjectView
#    - ProjectEngagement  
#    - ProjectTeamMetrics
# 3. Run: python manage.py makemigrations
# 4. Run: python manage.py migrate
```

**File:** `accounts/models.py` (add at end)

```python
class ProjectView(models.Model):
    project = models.ForeignKey(Project, on_delete=models.CASCADE, related_name='views')
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    ip_address = models.GenericIPAddressField(null=True, blank=True)
    user_agent = models.TextField(blank=True)
    viewed_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ['-viewed_at']
        indexes = [models.Index(fields=['project', '-viewed_at'])]
    
    def __str__(self):
        return f"{self.project.title} - view"

class ProjectEngagement(models.Model):
    TYPES = [('view', 'View'), ('like', 'Like'), ('comment', 'Comment'), 
             ('share', 'Share'), ('connection', 'Connection'), ('apply', 'Apply')]
    
    project = models.ForeignKey(Project, on_delete=models.CASCADE, related_name='engagements')
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    engagement_type = models.CharField(max_length=20, choices=TYPES)
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ['-created_at']
        indexes = [models.Index(fields=['project', '-created_at'])]
    
    def __str__(self):
        return f"{self.project.title} - {self.engagement_type}"

class ProjectTeamMetrics(models.Model):
    project = models.OneToOneField(Project, on_delete=models.CASCADE, related_name='team_metrics')
    created_at = models.DateTimeField(auto_now_add=True)
    first_member_added = models.DateTimeField(null=True, blank=True)
    team_complete_date = models.DateTimeField(null=True, blank=True)
    
    target_team_size = models.IntegerField(default=0)
    current_team_size = models.IntegerField(default=0)
    
    required_skills = models.JSONField(default=list, blank=True)
    filled_skills = models.JSONField(default=list, blank=True)
    unfilled_skills = models.JSONField(default=list, blank=True)
    
    total_applications = models.IntegerField(default=0)
    accepted_members = models.IntegerField(default=0)
    rejected_members = models.IntegerField(default=0)
    success_rate = models.FloatField(default=0.0)
    
    updated_at = models.DateTimeField(auto_now=True)
    
    def calculate_success_rate(self):
        return round((self.accepted_members / max(1, self.total_applications)) * 100, 2)
    
    def days_to_complete(self):
        if self.team_complete_date:
            return (self.team_complete_date - self.created_at).days
        return None
    
    def __str__(self):
        return f"{self.project.title} metrics"
```

---

### Step 2: Create API Views (1 hour)
**File:** `accounts/views.py` (add at end)

```python
from django.db.models import Count
from django.utils import timezone
from datetime import timedelta
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
from rest_framework import permissions

def track_project_view(project_id, user=None, ip=None, ua=None):
    try:
        project = Project.objects.get(id=project_id)
        ProjectView.objects.create(project=project, user=user, ip_address=ip, user_agent=ua)
    except: pass

def track_engagement(project_id, user, engagement_type):
    try:
        project = Project.objects.get(id=project_id)
        ProjectEngagement.objects.create(project=project, user=user, engagement_type=engagement_type)
    except: pass

@api_view(['GET'])
@permission_classes([permissions.IsAuthenticated])
def analytics_dashboard(request):
    """Dashboard overview"""
    projects = Project.objects.filter(owner=request.user)
    data = []
    for p in projects:
        metrics, _ = ProjectTeamMetrics.objects.get_or_create(project=p)
        data.append({
            'id': p.id,
            'title': p.title,
            'views': p.views.count(),
            'engagements': p.engagements.count(),
            'team_size': metrics.current_team_size,
            'success_rate': metrics.success_rate,
        })
    return Response({'projects': data, 'total': len(data)})

@api_view(['GET'])
@permission_classes([permissions.IsAuthenticated])
def project_analytics(request, project_id):
    """Project detail analytics"""
    try:
        project = Project.objects.get(id=project_id)
    except:
        return Response({'error': 'Not found'}, status=404)
    
    if project.owner != request.user:
        return Response({'error': 'Unauthorized'}, status=403)
    
    metrics, _ = ProjectTeamMetrics.objects.get_or_create(project=project)
    
    thirty_days = timezone.now() - timedelta(days=30)
    
    return Response({
        'total_views': project.views.count(),
        'views_7d': project.views.filter(viewed_at__gte=timezone.now()-timedelta(days=7)).count(),
        'views_30d': project.views.filter(viewed_at__gte=thirty_days).count(),
        'unique_views': project.views.values('user', 'ip_address').distinct().count(),
        'total_engagements': project.engagements.count(),
        'engagement_types': dict(project.engagements.values('engagement_type').annotate(count=Count('id')).values_list('engagement_type', 'count')),
        'team': {
            'target': metrics.target_team_size,
            'current': metrics.current_team_size,
            'applications': metrics.total_applications,
            'success_rate': metrics.success_rate,
            'days_to_fill': metrics.days_to_complete(),
        },
        'skills': {
            'required': metrics.required_skills,
            'filled': metrics.filled_skills,
            'fill_rate': len(metrics.filled_skills) / max(1, len(metrics.required_skills)) * 100
        }
    })

@api_view(['GET'])
@permission_classes([permissions.IsAuthenticated])
def analytics_timeline(request, project_id):
    """Views timeline for chart"""
    try:
        project = Project.objects.get(id=project_id)
    except:
        return Response({'error': 'Not found'}, status=404)
    
    if project.owner != request.user:
        return Response({'error': 'Unauthorized'}, status=403)
    
    thirty_days = timezone.now() - timedelta(days=30)
    views = project.views.filter(viewed_at__gte=thirty_days)
    
    by_date = {}
    for v in views:
        date = str(v.viewed_at.date())
        by_date[date] = by_date.get(date, 0) + 1
    
    dates = sorted(by_date.keys())
    return Response({
        'labels': dates,
        'data': [by_date[d] for d in dates],
        'total': len(views),
        'average': len(views) / 30
    })
```

---

### Step 3: Update URLs (10 min)
**File:** `accounts/urls.py`

Add these lines to the `urlpatterns` list:

```python
# Analytics endpoints
path('api/analytics/dashboard/', views.analytics_dashboard, name='analytics_dashboard'),
path('api/analytics/<int:project_id>/', views.project_analytics, name='project_analytics'),
path('api/analytics/<int:project_id>/timeline/', views.analytics_timeline, name='analytics_timeline'),
```

---

### Step 4: Update Existing Views (30 min)

**Add to `project_detail` view:**
```python
# Get IP address
x_forwarded = request.META.get('HTTP_X_FORWARDED_FOR')
ip = x_forwarded.split(',')[0] if x_forwarded else request.META.get('REMOTE_ADDR')

# Track view
track_project_view(
    project_id=project.id,
    user=request.user if request.user.is_authenticated else None,
    ip=ip,
    ua=request.META.get('HTTP_USER_AGENT', '')
)
```

**Add to like_project, post_comment, etc.:**
```python
track_engagement(project_id, request.user, 'like')  # or 'comment', 'share', etc.
```

---

### Step 5: Create HTML Template (1 hour)

**Create file:** `accounts/templates/analytics.html`

```html
{% extends 'base.html' %}
{% load static %}

{% block title %}Analytics Dashboard{% endblock %}

{% block extra_css %}
<script src="https://cdn.jsdelivr.net/npm/chart.js@3.9.1/dist/chart.min.js"></script>
<style>
    .analytics { padding: 20px; background: #f8f9fa; min-height: 100vh; }
    .metric-card { background: white; border-radius: 8px; padding: 20px; 
                   margin-bottom: 20px; box-shadow: 0 2px 4px rgba(0,0,0,0.1); }
    .metric-value { font-size: 32px; font-weight: bold; color: #3498db; margin: 10px 0; }
    .metric-label { font-size: 12px; color: #7f8c8d; text-transform: uppercase; }
    .metric-row { display: grid; grid-template-columns: repeat(auto-fit, minmax(250px, 1fr)); gap: 20px; }
    .chart-box { background: white; border-radius: 8px; padding: 20px; margin-bottom: 20px; }
</style>
{% endblock %}

{% block content %}
<div class="analytics">
    <h1>📊 Analytics Dashboard</h1>
    
    <!-- Projects Overview -->
    <div id="projects-list"></div>
    
    <!-- Detail View -->
    <div id="detail-view" style="display:none;">
        <button class="btn btn-secondary mb-3" onclick="showList()">← Back</button>
        
        <div class="metric-row" id="metrics"></div>
        
        <div class="chart-box">
            <h3>Views (Last 30 Days)</h3>
            <canvas id="chart"></canvas>
        </div>
    </div>
</div>

<script>
    function getCookie(name) {
        const value = `; ${document.cookie}`;
        const parts = value.split(`; ${name}=`);
        if (parts.length === 2) return parts.pop().split(';').shift();
    }
    
    async function loadProjects() {
        const res = await fetch('/accounts/api/analytics/dashboard/', {
            headers: { 'X-CSRFToken': getCookie('csrftoken') }
        });
        const data = await res.json();
        
        let html = '<div class="metric-row">';
        data.projects.forEach(p => {
            html += `<div class="metric-card" onclick="showProject(${p.id})">
                <h3>${p.title}</h3>
                <div class="metric-label">Views</div>
                <div class="metric-value">${p.views}</div>
                <div class="metric-label" style="margin-top:15px;">Engagements</div>
                <div class="metric-value">${p.engagements}</div>
            </div>`;
        });
        html += '</div>';
        document.getElementById('projects-list').innerHTML = html;
    }
    
    async function showProject(id) {
        const res = await fetch(`/accounts/api/analytics/${id}/`, {
            headers: { 'X-CSRFToken': getCookie('csrftoken') }
        });
        const data = await res.json();
        
        const res2 = await fetch(`/accounts/api/analytics/${id}/timeline/`, {
            headers: { 'X-CSRFToken': getCookie('csrftoken') }
        });
        const timeline = await res2.json();
        
        // Show metrics
        let html = `
            <div class="metric-card">
                <div class="metric-label">Total Views</div>
                <div class="metric-value">${data.total_views}</div>
            </div>
            <div class="metric-card">
                <div class="metric-label">Views (7d)</div>
                <div class="metric-value">${data.views_7d}</div>
            </div>
            <div class="metric-card">
                <div class="metric-label">Unique Visitors</div>
                <div class="metric-value">${data.unique_views}</div>
            </div>
            <div class="metric-card">
                <div class="metric-label">Team Size</div>
                <div class="metric-value">${data.team.current}/${data.team.target}</div>
            </div>
            <div class="metric-card">
                <div class="metric-label">Success Rate</div>
                <div class="metric-value">${data.team.success_rate}%</div>
            </div>
        `;
        document.getElementById('metrics').innerHTML = html;
        
        // Show chart
        const ctx = document.getElementById('chart').getContext('2d');
        new Chart(ctx, {
            type: 'line',
            data: {
                labels: timeline.labels,
                datasets: [{
                    label: 'Views',
                    data: timeline.data,
                    borderColor: '#3498db',
                    backgroundColor: 'rgba(52,152,219,0.1)',
                    tension: 0.4
                }]
            },
            options: {
                responsive: true,
                scales: { y: { beginAtZero: true } }
            }
        });
        
        document.getElementById('projects-list').style.display = 'none';
        document.getElementById('detail-view').style.display = 'block';
    }
    
    function showList() {
        document.getElementById('projects-list').style.display = 'block';
        document.getElementById('detail-view').style.display = 'none';
        loadProjects();
    }
    
    loadProjects();
</script>
{% endblock %}
```

---

## Testing Checklist

```bash
# 1. Create migrations
python manage.py makemigrations

# 2. Apply migrations
python manage.py migrate

# 3. Test tracking
# - View a project
# - Like a project
# - Post a comment

# 4. Check dashboard
# Visit: /accounts/analytics/

# 5. Test API
# curl http://localhost:8000/accounts/api/analytics/dashboard/

# 6. Check admin
# Visit: /admin/accounts/projectview/
```

---

## API Quick Reference

```bash
# Get dashboard
curl http://localhost:8000/accounts/api/analytics/dashboard/

# Get project analytics
curl http://localhost:8000/accounts/api/analytics/1/

# Get views timeline
curl http://localhost:8000/accounts/api/analytics/1/timeline/
```

---

## Files Modified

1. ✅ `accounts/models.py` - Add 3 models
2. ✅ `accounts/views.py` - Add 4 API functions + 2 tracking helpers
3. ✅ `accounts/urls.py` - Add 3 routes
4. ✅ `accounts/templates/analytics.html` - New template
5. ✅ Update tracking in existing views

---

## Next Steps

1. Copy Step 1-5 code above
2. Paste into respective files
3. Run migrations
4. Test locally
5. Deploy

**Estimated time: 3-4 hours**

---

## Troubleshooting

**Models not created?**
```bash
python manage.py makemigrations accounts
python manage.py migrate
```

**API returning 404?**
```bash
# Check urls.py has the routes
# Check views.py has the functions
```

**Chart not showing?**
- Check Chart.js CDN is loaded
- Check API is returning data
- Check browser console for errors

**Tracking not working?**
- Make sure `track_project_view()` is called in `project_detail`
- Make sure `track_engagement()` is called in other views
- Check database has ProjectView records

---

For detailed information, see: **FEATURE_PROJECT_ANALYTICS_DASHBOARD.md**
