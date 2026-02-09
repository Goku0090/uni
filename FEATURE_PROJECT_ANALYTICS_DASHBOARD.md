# Project Analytics Dashboard - Implementation Guide

**Status:** 🟢 Ready to Implement  
**Difficulty:** Medium  
**Time Estimate:** 3-4 days  
**Impact:** Medium (insights for users)  
**Priority:** ⭐⭐⭐⭐ High Value Feature  

---

## Feature Overview

### Problem
Project owners have **no insights** into:
- How many people are viewing their projects
- How successful is their project at attracting collaborators
- How long it takes to fill team positions
- What skills are most in-demand
- Project engagement metrics

### Solution
Build a **Project Analytics Dashboard** that shows:
- 📊 Project views/clicks over time
- 👥 Collaboration success metrics
- ⏱️ Timeline tracking (days to fill positions)
- 📈 Skill demand trends
- 🎯 Engagement analytics

### Target Users
- Project owners (see analytics for their projects)
- Optional: Admins (see all projects analytics)

---

## Architecture Overview

### Data Models Needed

#### 1. ProjectView Model
```python
class ProjectView(models.Model):
    """Track each project view"""
    project = models.ForeignKey(Project, on_delete=models.CASCADE, related_name='views')
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    ip_address = models.GenericIPAddressField(null=True, blank=True)
    user_agent = models.TextField(blank=True)  # Browser info
    viewed_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ['-viewed_at']
        indexes = [
            models.Index(fields=['project', 'viewed_at']),
            models.Index(fields=['user', 'viewed_at']),
        ]
```

#### 2. ProjectEngagement Model
```python
class ProjectEngagement(models.Model):
    """Track user interactions with projects"""
    ENGAGEMENT_TYPES = [
        ('view', 'Project Viewed'),
        ('like', 'Project Liked'),
        ('comment', 'Comment Posted'),
        ('share', 'Project Shared'),
        ('connection_request', 'Connection Request Sent'),
        ('team_apply', 'Applied to Join Team'),
    ]
    
    project = models.ForeignKey(Project, on_delete=models.CASCADE, related_name='engagements')
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    engagement_type = models.CharField(max_length=20, choices=ENGAGEMENT_TYPES)
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['project', 'engagement_type']),
            models.Index(fields=['created_at']),
        ]
```

#### 3. ProjectTeamMetrics Model (Optional)
```python
class ProjectTeamMetrics(models.Model):
    """Track team formation timeline"""
    project = models.OneToOneField(Project, on_delete=models.CASCADE, related_name='team_metrics')
    
    # Timeline metrics
    created_at = models.DateTimeField(auto_now_add=True)
    first_member_added = models.DateTimeField(null=True, blank=True)
    team_complete_date = models.DateTimeField(null=True, blank=True)
    
    # Target vs actual
    target_team_size = models.IntegerField(default=0)
    current_team_size = models.IntegerField(default=0)
    
    # Skills metrics
    required_skills = models.JSONField(default=list)  # ['Python', 'React', 'UI']
    filled_skills = models.JSONField(default=list)
    unfilled_skills = models.JSONField(default=list)
    
    # Collaboration metrics
    total_applications = models.IntegerField(default=0)
    accepted_members = models.IntegerField(default=0)
    rejected_members = models.IntegerField(default=0)
    success_rate = models.FloatField(default=0.0)  # accepted / total
    
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        verbose_name_plural = "Project Team Metrics"
```

---

## Implementation Steps

### Step 1: Create Models (30 minutes)

**File:** `accounts/models.py`

Add three new models:
```python
# Add to accounts/models.py

class ProjectView(models.Model):
    """Track individual project views"""
    project = models.ForeignKey(Project, on_delete=models.CASCADE, related_name='views')
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    ip_address = models.GenericIPAddressField(null=True, blank=True)
    user_agent = models.TextField(blank=True)
    viewed_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ['-viewed_at']
        indexes = [
            models.Index(fields=['project', '-viewed_at']),
        ]
    
    def __str__(self):
        user = self.user.username if self.user else "Anonymous"
        return f"{self.project.title} - viewed by {user} at {self.viewed_at}"


class ProjectEngagement(models.Model):
    """Track all user interactions"""
    ENGAGEMENT_TYPES = [
        ('view', 'View'),
        ('like', 'Like'),
        ('comment', 'Comment'),
        ('share', 'Share'),
        ('connection', 'Connection Request'),
        ('apply', 'Team Application'),
    ]
    
    project = models.ForeignKey(Project, on_delete=models.CASCADE, related_name='engagements')
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    engagement_type = models.CharField(max_length=20, choices=ENGAGEMENT_TYPES)
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['project', '-created_at']),
            models.Index(fields=['engagement_type']),
        ]
    
    def __str__(self):
        return f"{self.project.title} - {self.engagement_type}"


class ProjectTeamMetrics(models.Model):
    """Track team formation and collaboration success"""
    project = models.OneToOneField(Project, on_delete=models.CASCADE, related_name='team_metrics')
    
    # Timeline
    created_at = models.DateTimeField(auto_now_add=True)
    first_member_added = models.DateTimeField(null=True, blank=True)
    team_complete_date = models.DateTimeField(null=True, blank=True)
    
    # Team size
    target_team_size = models.IntegerField(default=0)
    current_team_size = models.IntegerField(default=0)
    
    # Skills
    required_skills = models.JSONField(default=list, blank=True)
    filled_skills = models.JSONField(default=list, blank=True)
    unfilled_skills = models.JSONField(default=list, blank=True)
    
    # Success metrics
    total_applications = models.IntegerField(default=0)
    accepted_members = models.IntegerField(default=0)
    rejected_members = models.IntegerField(default=0)
    success_rate = models.FloatField(default=0.0)
    
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        verbose_name_plural = "Project Team Metrics"
    
    def calculate_success_rate(self):
        """Calculate acceptance rate"""
        if self.total_applications == 0:
            return 0.0
        return round((self.accepted_members / self.total_applications) * 100, 2)
    
    def update_success_rate(self):
        """Update success rate"""
        self.success_rate = self.calculate_success_rate()
        self.save()
    
    def days_to_complete(self):
        """Calculate days from creation to team complete"""
        if self.team_complete_date:
            delta = self.team_complete_date - self.created_at
            return delta.days
        return None
    
    def __str__(self):
        return f"{self.project.title} - Team Metrics"
```

### Step 2: Create Migrations (10 minutes)

```bash
cd e:\login\auth_project
python manage.py makemigrations
python manage.py migrate
```

### Step 3: Create Serializers (20 minutes)

**File:** `accounts/serializers.py`

```python
# Add to accounts/serializers.py

from rest_framework import serializers
from .models import ProjectView, ProjectEngagement, ProjectTeamMetrics

class ProjectViewSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProjectView
        fields = ['id', 'user', 'viewed_at']

class ProjectEngagementSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProjectEngagement
        fields = ['id', 'engagement_type', 'user', 'created_at']

class ProjectTeamMetricsSerializer(serializers.ModelSerializer):
    success_rate = serializers.SerializerMethodField()
    days_to_complete = serializers.SerializerMethodField()
    
    class Meta:
        model = ProjectTeamMetrics
        fields = [
            'target_team_size',
            'current_team_size',
            'required_skills',
            'filled_skills',
            'unfilled_skills',
            'total_applications',
            'accepted_members',
            'rejected_members',
            'success_rate',
            'first_member_added',
            'team_complete_date',
            'days_to_complete',
        ]
    
    def get_success_rate(self, obj):
        return obj.calculate_success_rate()
    
    def get_days_to_complete(self, obj):
        return obj.days_to_complete()
```

### Step 4: Create Views/APIs (1 hour)

**File:** `accounts/views.py`

```python
# Add to accounts/views.py

from django.db.models import Count, Q
from django.utils import timezone
from datetime import timedelta
from rest_framework import generics, permissions
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
from .models import ProjectView, ProjectEngagement, ProjectTeamMetrics, Project

# Track project view
def track_project_view(project_id, user=None, ip_address=None, user_agent=None):
    """Helper function to track project views"""
    try:
        project = Project.objects.get(id=project_id)
        ProjectView.objects.create(
            project=project,
            user=user,
            ip_address=ip_address,
            user_agent=user_agent
        )
    except Project.DoesNotExist:
        pass

# Track engagement
def track_engagement(project_id, user, engagement_type):
    """Helper function to track engagements"""
    try:
        project = Project.objects.get(id=project_id)
        ProjectEngagement.objects.create(
            project=project,
            user=user,
            engagement_type=engagement_type
        )
    except Project.DoesNotExist:
        pass

# API: Get project analytics
@api_view(['GET'])
@permission_classes([permissions.IsAuthenticated])
def project_analytics(request, project_id):
    """Get analytics for a project (owner only)"""
    try:
        project = Project.objects.get(id=project_id)
    except Project.DoesNotExist:
        return Response({'error': 'Project not found'}, status=404)
    
    # Check permission (owner only)
    if project.owner != request.user:
        return Response({'error': 'Not authorized'}, status=403)
    
    # Get or create metrics
    metrics, created = ProjectTeamMetrics.objects.get_or_create(project=project)
    
    # Collect data
    data = {
        'project_id': project.id,
        'project_title': project.title,
        
        # View metrics
        'total_views': project.views.count(),
        'unique_views': project.views.values('user', 'ip_address').distinct().count(),
        'views_last_7_days': project.views.filter(
            viewed_at__gte=timezone.now() - timedelta(days=7)
        ).count(),
        'views_last_30_days': project.views.filter(
            viewed_at__gte=timezone.now() - timedelta(days=30)
        ).count(),
        
        # Engagement metrics
        'total_engagements': project.engagements.count(),
        'engagement_breakdown': {
            'views': project.engagements.filter(engagement_type='view').count(),
            'likes': project.engagements.filter(engagement_type='like').count(),
            'comments': project.engagements.filter(engagement_type='comment').count(),
            'shares': project.engagements.filter(engagement_type='share').count(),
            'connections': project.engagements.filter(engagement_type='connection').count(),
            'applications': project.engagements.filter(engagement_type='apply').count(),
        },
        
        # Team metrics
        'team_metrics': {
            'target_size': metrics.target_team_size,
            'current_size': metrics.current_team_size,
            'total_applications': metrics.total_applications,
            'accepted': metrics.accepted_members,
            'rejected': metrics.rejected_members,
            'success_rate': metrics.success_rate,
            'days_to_fill': metrics.days_to_complete(),
        },
        
        # Skill metrics
        'skills': {
            'required': metrics.required_skills,
            'filled': metrics.filled_skills,
            'unfilled': metrics.unfilled_skills,
            'skill_fill_rate': len(metrics.filled_skills) / max(1, len(metrics.required_skills)) * 100
        }
    }
    
    return Response(data)


# API: Get analytics dashboard data
@api_view(['GET'])
@permission_classes([permissions.IsAuthenticated])
def analytics_dashboard(request):
    """Get analytics for all user's projects"""
    user_projects = Project.objects.filter(owner=request.user)
    
    projects_data = []
    for project in user_projects:
        metrics, created = ProjectTeamMetrics.objects.get_or_create(project=project)
        
        projects_data.append({
            'project_id': project.id,
            'title': project.title,
            'status': project.status,
            'views': project.views.count(),
            'engagements': project.engagements.count(),
            'team_size': metrics.current_team_size,
            'success_rate': metrics.success_rate,
        })
    
    return Response({
        'total_projects': len(projects_data),
        'projects': projects_data
    })


# API: Get views over time (for charts)
@api_view(['GET'])
@permission_classes([permissions.IsAuthenticated])
def analytics_views_timeline(request, project_id):
    """Get project views over last 30 days"""
    try:
        project = Project.objects.get(id=project_id)
    except Project.DoesNotExist:
        return Response({'error': 'Project not found'}, status=404)
    
    if project.owner != request.user:
        return Response({'error': 'Not authorized'}, status=403)
    
    # Get views for last 30 days
    thirty_days_ago = timezone.now() - timedelta(days=30)
    views = project.views.filter(viewed_at__gte=thirty_days_ago)
    
    # Group by date
    views_by_date = {}
    for view in views:
        date = view.viewed_at.date()
        views_by_date[date] = views_by_date.get(date, 0) + 1
    
    # Format for chart
    dates = sorted(views_by_date.keys())
    data = [views_by_date[date] for date in dates]
    
    return Response({
        'labels': [str(date) for date in dates],
        'data': data,
        'total_views': len(views),
        'average_views_per_day': len(views) / 30
    })


# API: Get engagement by type
@api_view(['GET'])
@permission_classes([permissions.IsAuthenticated])
def analytics_engagement_breakdown(request, project_id):
    """Get engagement breakdown"""
    try:
        project = Project.objects.get(id=project_id)
    except Project.DoesNotExist:
        return Response({'error': 'Project not found'}, status=404)
    
    if project.owner != request.user:
        return Response({'error': 'Not authorized'}, status=403)
    
    # Get engagement counts by type
    engagement_counts = project.engagements.values('engagement_type').annotate(
        count=Count('id')
    ).order_by('-count')
    
    labels = []
    data = []
    colors = {
        'view': '#3498db',
        'like': '#e74c3c',
        'comment': '#2ecc71',
        'share': '#f39c12',
        'connection': '#9b59b6',
        'apply': '#1abc9c'
    }
    
    for item in engagement_counts:
        labels.append(item['engagement_type'].title())
        data.append(item['count'])
    
    return Response({
        'labels': labels,
        'data': data,
        'colors': [colors.get(item['engagement_type'], '#95a5a6') for item in engagement_counts]
    })
```

### Step 5: Create URL Routes (10 minutes)

**File:** `accounts/urls.py`

```python
# Add to accounts/urls.py

urlpatterns = [
    # ... existing patterns ...
    
    # Analytics endpoints
    path('api/analytics/<int:project_id>/', views.project_analytics, name='project_analytics'),
    path('api/analytics/dashboard/', views.analytics_dashboard, name='analytics_dashboard'),
    path('api/analytics/<int:project_id>/timeline/', views.analytics_views_timeline, name='analytics_timeline'),
    path('api/analytics/<int:project_id>/engagement/', views.analytics_engagement_breakdown, name='analytics_engagement'),
]
```

### Step 6: Create Frontend Template (1 hour)

**File:** `accounts/templates/analytics_dashboard.html`

```html
{% extends 'base.html' %}
{% load static %}

{% block title %}Project Analytics Dashboard{% endblock %}

{% block extra_css %}
<script src="https://cdn.jsdelivr.net/npm/chart.js@3.9.1/dist/chart.min.js"></script>
<style>
    .analytics-container {
        padding: 20px;
        background: #f8f9fa;
        min-height: 100vh;
    }
    
    .metric-card {
        background: white;
        border-radius: 8px;
        padding: 20px;
        margin-bottom: 20px;
        box-shadow: 0 2px 4px rgba(0,0,0,0.1);
    }
    
    .metric-value {
        font-size: 32px;
        font-weight: bold;
        color: #3498db;
        margin: 10px 0;
    }
    
    .metric-label {
        font-size: 14px;
        color: #7f8c8d;
        text-transform: uppercase;
        letter-spacing: 1px;
    }
    
    .metric-row {
        display: grid;
        grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
        gap: 20px;
        margin-bottom: 30px;
    }
    
    .chart-container {
        background: white;
        border-radius: 8px;
        padding: 20px;
        margin-bottom: 20px;
        box-shadow: 0 2px 4px rgba(0,0,0,0.1);
    }
    
    .chart-title {
        font-size: 18px;
        font-weight: bold;
        margin-bottom: 15px;
        color: #2c3e50;
    }
    
    .engagement-badge {
        display: inline-block;
        padding: 8px 12px;
        border-radius: 20px;
        font-size: 12px;
        font-weight: bold;
        margin-right: 10px;
        margin-bottom: 10px;
    }
    
    .badge-view { background: #e3f2fd; color: #1976d2; }
    .badge-like { background: #fce4ec; color: #c2185b; }
    .badge-comment { background: #e8f5e9; color: #388e3c; }
    .badge-share { background: #fff3e0; color: #f57c00; }
    .badge-connection { background: #f3e5f5; color: #7b1fa2; }
    .badge-apply { background: #e0f2f1; color: #00796b; }
    
    .skill-progress {
        margin-bottom: 15px;
    }
    
    .skill-label {
        display: flex;
        justify-content: space-between;
        font-size: 14px;
        margin-bottom: 5px;
    }
    
    .progress-bar {
        height: 8px;
        background: #ecf0f1;
        border-radius: 4px;
        overflow: hidden;
    }
    
    .progress-fill {
        height: 100%;
        background: linear-gradient(90deg, #3498db, #2ecc71);
        border-radius: 4px;
    }
</style>
{% endblock %}

{% block content %}
<div class="analytics-container">
    <h1>Project Analytics Dashboard</h1>
    <p class="text-muted">Track your project's performance and engagement</p>
    
    <!-- Projects List -->
    <div id="projects-list"></div>
    
    <!-- Project Detail View -->
    <div id="project-detail" style="display: none;">
        <button class="btn btn-secondary mb-3" onclick="backToList()">← Back to Projects</button>
        
        <!-- Key Metrics -->
        <div class="metric-row" id="key-metrics"></div>
        
        <!-- Views Timeline Chart -->
        <div class="chart-container">
            <div class="chart-title">Views Over Time (Last 30 Days)</div>
            <canvas id="viewsChart"></canvas>
        </div>
        
        <!-- Engagement Breakdown Chart -->
        <div class="chart-container">
            <div class="chart-title">Engagement Breakdown</div>
            <canvas id="engagementChart"></canvas>
        </div>
        
        <!-- Team Metrics -->
        <div class="metric-card">
            <h3>Team Metrics</h3>
            <div class="metric-row" id="team-metrics"></div>
        </div>
        
        <!-- Skills Metrics -->
        <div class="metric-card" id="skills-section" style="display: none;">
            <h3>Skills Requirements</h3>
            <div id="skills-metrics"></div>
        </div>
    </div>
</div>

<script>
    let viewsChart = null;
    let engagementChart = null;
    
    // Load projects list
    async function loadProjectsList() {
        try {
            const response = await fetch('/accounts/api/analytics/dashboard/', {
                headers: {
                    'X-CSRFToken': getCookie('csrftoken')
                }
            });
            const data = await response.json();
            
            let html = '<div class="metric-row">';
            data.projects.forEach(project => {
                html += `
                    <div class="metric-card" style="cursor: pointer;" onclick="loadProjectDetail(${project.project_id})">
                        <h3>${project.title}</h3>
                        <div class="metric-label">Status</div>
                        <div>${project.status}</div>
                        <div class="metric-label mt-3">Views</div>
                        <div class="metric-value">${project.views}</div>
                        <div class="metric-label mt-3">Engagements</div>
                        <div class="metric-value">${project.engagements}</div>
                        <div class="metric-label mt-3">Team Size</div>
                        <div class="metric-value">${project.team_size}👥</div>
                    </div>
                `;
            });
            html += '</div>';
            
            document.getElementById('projects-list').innerHTML = html;
        } catch (error) {
            console.error('Error loading projects:', error);
            alert('Error loading projects');
        }
    }
    
    // Load project detail
    async function loadProjectDetail(projectId) {
        try {
            const [analyticsResponse, timelineResponse, engagementResponse] = await Promise.all([
                fetch(`/accounts/api/analytics/${projectId}/`, {
                    headers: { 'X-CSRFToken': getCookie('csrftoken') }
                }),
                fetch(`/accounts/api/analytics/${projectId}/timeline/`, {
                    headers: { 'X-CSRFToken': getCookie('csrftoken') }
                }),
                fetch(`/accounts/api/analytics/${projectId}/engagement/`, {
                    headers: { 'X-CSRFToken': getCookie('csrftoken') }
                })
            ]);
            
            const analytics = await analyticsResponse.json();
            const timeline = await timelineResponse.json();
            const engagement = await engagementResponse.json();
            
            // Hide list, show detail
            document.getElementById('projects-list').style.display = 'none';
            document.getElementById('project-detail').style.display = 'block';
            
            // Render metrics
            renderMetrics(analytics);
            renderTimeline(timeline);
            renderEngagement(engagement);
            renderTeamMetrics(analytics);
            renderSkillsMetrics(analytics);
            
        } catch (error) {
            console.error('Error loading project detail:', error);
            alert('Error loading project analytics');
        }
    }
    
    // Render key metrics
    function renderMetrics(data) {
        const metricsHtml = `
            <div class="metric-card">
                <div class="metric-label">Total Views</div>
                <div class="metric-value">${data.total_views}</div>
            </div>
            <div class="metric-card">
                <div class="metric-label">Unique Views</div>
                <div class="metric-value">${data.unique_views}</div>
            </div>
            <div class="metric-card">
                <div class="metric-label">Views (Last 7 Days)</div>
                <div class="metric-value">${data.views_last_7_days}</div>
            </div>
            <div class="metric-card">
                <div class="metric-label">Total Engagements</div>
                <div class="metric-value">${data.total_engagements}</div>
            </div>
        `;
        document.getElementById('key-metrics').innerHTML = metricsHtml;
    }
    
    // Render timeline chart
    function renderTimeline(data) {
        if (viewsChart) viewsChart.destroy();
        
        const ctx = document.getElementById('viewsChart').getContext('2d');
        viewsChart = new Chart(ctx, {
            type: 'line',
            data: {
                labels: data.labels,
                datasets: [{
                    label: 'Views per Day',
                    data: data.data,
                    borderColor: '#3498db',
                    backgroundColor: 'rgba(52, 152, 219, 0.1)',
                    tension: 0.4,
                    fill: true,
                    pointRadius: 4,
                    pointBackgroundColor: '#3498db'
                }]
            },
            options: {
                responsive: true,
                plugins: {
                    legend: { display: false }
                },
                scales: {
                    y: {
                        beginAtZero: true,
                        ticks: { stepSize: 1 }
                    }
                }
            }
        });
    }
    
    // Render engagement chart
    function renderEngagement(data) {
        if (engagementChart) engagementChart.destroy();
        
        const ctx = document.getElementById('engagementChart').getContext('2d');
        engagementChart = new Chart(ctx, {
            type: 'doughnut',
            data: {
                labels: data.labels,
                datasets: [{
                    data: data.data,
                    backgroundColor: data.colors
                }]
            },
            options: {
                responsive: true,
                plugins: {
                    legend: {
                        position: 'bottom'
                    }
                }
            }
        });
    }
    
    // Render team metrics
    function renderTeamMetrics(data) {
        const metrics = data.team_metrics;
        const html = `
            <div class="metric-card">
                <div class="metric-label">Target Team Size</div>
                <div class="metric-value">${metrics.target_size}</div>
            </div>
            <div class="metric-card">
                <div class="metric-label">Current Team Size</div>
                <div class="metric-value">${metrics.current_size}</div>
            </div>
            <div class="metric-card">
                <div class="metric-label">Applications Received</div>
                <div class="metric-value">${metrics.total_applications}</div>
            </div>
            <div class="metric-card">
                <div class="metric-label">Success Rate</div>
                <div class="metric-value">${metrics.success_rate}%</div>
            </div>
            <div class="metric-card">
                <div class="metric-label">Days to Fill Team</div>
                <div class="metric-value">${metrics.days_to_fill || 'N/A'}</div>
            </div>
        `;
        document.getElementById('team-metrics').innerHTML = html;
    }
    
    // Render skills metrics
    function renderSkillsMetrics(data) {
        const skills = data.skills;
        if (!skills.required || skills.required.length === 0) {
            document.getElementById('skills-section').style.display = 'none';
            return;
        }
        
        document.getElementById('skills-section').style.display = 'block';
        
        let html = `<p><strong>Skill Fill Rate: ${skills.skill_fill_rate.toFixed(1)}%</strong></p>`;
        
        skills.required.forEach(skill => {
            const filled = skills.filled.includes(skill);
            const percentage = filled ? 100 : 0;
            
            html += `
                <div class="skill-progress">
                    <div class="skill-label">
                        <span>${skill}</span>
                        <span>${filled ? '✅' : '⏳'}</span>
                    </div>
                    <div class="progress-bar">
                        <div class="progress-fill" style="width: ${percentage}%"></div>
                    </div>
                </div>
            `;
        });
        
        document.getElementById('skills-metrics').innerHTML = html;
    }
    
    // Back to projects list
    function backToList() {
        document.getElementById('projects-list').style.display = 'block';
        document.getElementById('project-detail').style.display = 'none';
        loadProjectsList();
    }
    
    // Helper function to get CSRF token
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
    
    // Load projects on page load
    document.addEventListener('DOMContentLoaded', loadProjectsList);
</script>
{% endblock %}
```

### Step 7: Add Tracking to Existing Views (1 hour)

**Update:** `accounts/views.py`

```python
# In project_detail view, add:
def project_detail(request, project_id):
    """View project details and track view"""
    try:
        project = Project.objects.get(id=project_id)
    except Project.DoesNotExist:
        raise Http404("Project not found")
    
    # Get user's IP
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    ip = x_forwarded_for.split(',')[0] if x_forwarded_for else request.META.get('REMOTE_ADDR')
    
    # Track view
    track_project_view(
        project_id=project_id,
        user=request.user if request.user.is_authenticated else None,
        ip_address=ip,
        user_agent=request.META.get('HTTP_USER_AGENT', '')
    )
    
    # Rest of view logic...
    context = {
        'project': project,
        # ... other context ...
    }
    return render(request, 'project_detail.html', context)


# In like_project view, add:
@login_required
def like_project(request, project_id):
    """Like a project"""
    project = get_object_or_404(Project, id=project_id)
    
    # Track engagement
    track_engagement(project_id, request.user, 'like')
    
    # Rest of logic...
    if request.user in project.likes.all():
        project.likes.remove(request.user)
        liked = False
    else:
        project.likes.add(request.user)
        liked = True
    
    return JsonResponse({'liked': liked})


# Similar tracking in other views:
# - post_comment() → track 'comment'
# - send_connection() → track 'connection'
# - add_team_member() → track 'apply'
```

### Step 8: Add Admin Interface (15 minutes)

**File:** `accounts/admin.py`

```python
# Add to admin.py

from django.contrib import admin
from .models import ProjectView, ProjectEngagement, ProjectTeamMetrics

@admin.register(ProjectView)
class ProjectViewAdmin(admin.ModelAdmin):
    list_display = ['project', 'user', 'viewed_at']
    list_filter = ['viewed_at', 'project']
    search_fields = ['project__title', 'user__username']
    readonly_fields = ['viewed_at']

@admin.register(ProjectEngagement)
class ProjectEngagementAdmin(admin.ModelAdmin):
    list_display = ['project', 'engagement_type', 'user', 'created_at']
    list_filter = ['engagement_type', 'created_at']
    search_fields = ['project__title', 'user__username']
    readonly_fields = ['created_at']

@admin.register(ProjectTeamMetrics)
class ProjectTeamMetricsAdmin(admin.ModelAdmin):
    list_display = ['project', 'current_team_size', 'success_rate', 'updated_at']
    search_fields = ['project__title']
    readonly_fields = ['created_at', 'updated_at']
```

---

## Data Flow Diagram

```
User Views Project
    ↓
project_detail() view
    ↓
track_project_view() called
    ↓
ProjectView record created
    ↓
Analytics Dashboard
    ↓
Query ProjectView.objects.filter(project=X)
    ↓
Display: Total views, timeline, trends
```

---

## API Endpoints

```
GET    /accounts/api/analytics/dashboard/
       - Get overview of all user's projects
       - Returns: List of projects with view/engagement counts

GET    /accounts/api/analytics/<project_id>/
       - Get detailed analytics for one project
       - Returns: Complete metrics object

GET    /accounts/api/analytics/<project_id>/timeline/
       - Get views over last 30 days
       - Returns: Array of dates and view counts

GET    /accounts/api/analytics/<project_id>/engagement/
       - Get engagement breakdown by type
       - Returns: Pie chart data
```

---

## Features Implemented

✅ **Project View Tracking**
- Track every project view
- Know unique vs repeat visitors
- Track views over time

✅ **Engagement Tracking**
- Like events
- Comments
- Shares
- Connection requests
- Team applications

✅ **Team Metrics**
- Team size tracking
- Applications received
- Success rate (% accepted)
- Days to fill team positions

✅ **Skill Tracking**
- Required skills vs filled skills
- Skill fill rate percentage
- Unfilled skills list

✅ **Analytics Dashboard**
- View all projects at a glance
- Click to view detailed analytics
- Multiple chart types (line, pie, progress)
- Real-time data updates

✅ **Charts & Visualization**
- Views timeline (Chart.js)
- Engagement breakdown (pie chart)
- Skill progress bars
- Metric cards with key numbers

---

## Database Impact

### New Indexes
- ProjectView: (project, -viewed_at)
- ProjectEngagement: (project, -created_at), (engagement_type)
- ProjectTeamMetrics: (project) - One-to-One

### Storage Considerations
- ProjectView: ~0.5 KB per view (1000 views = 500 KB)
- ProjectEngagement: ~0.3 KB per engagement
- Cleanup: Consider archiving old views after 90 days

---

## Performance Considerations

### Query Optimization
```python
# Efficient queries
views_count = project.views.filter(
    viewed_at__gte=thirty_days_ago
).count()  # Uses LIMIT 1

engagement_breakdown = project.engagements.values(
    'engagement_type'
).annotate(count=Count('id'))  # Aggregates at database level
```

### Caching Opportunities
```python
# Cache analytics for 1 hour
from django.core.cache import cache

def get_project_analytics(project_id):
    cache_key = f'analytics_{project_id}'
    data = cache.get(cache_key)
    
    if not data:
        # Calculate analytics
        data = calculate_analytics(project_id)
        cache.set(cache_key, data, 3600)  # Cache for 1 hour
    
    return data
```

### Pagination for Large Datasets
```python
# For very large view counts
views = project.views.filter(
    viewed_at__gte=start_date
).select_related('user').paginate(page=1, per_page=100)
```

---

## Testing Checklist

### Unit Tests
```python
def test_track_project_view():
    """Test view tracking"""
    project = Project.objects.create(...)
    track_project_view(project.id, user=user)
    assert ProjectView.objects.filter(project=project).exists()

def test_track_engagement():
    """Test engagement tracking"""
    project = Project.objects.create(...)
    track_engagement(project.id, user, 'like')
    assert ProjectEngagement.objects.filter(
        project=project, 
        engagement_type='like'
    ).exists()

def test_success_rate_calculation():
    """Test success rate calculation"""
    metrics = ProjectTeamMetrics.objects.create(
        project=project,
        total_applications=10,
        accepted_members=7
    )
    assert metrics.calculate_success_rate() == 70.0
```

### Integration Tests
```python
def test_analytics_api():
    """Test analytics API endpoint"""
    response = client.get('/accounts/api/analytics/123/')
    assert response.status_code == 200
    assert 'total_views' in response.data
```

### UI Tests
```python
def test_analytics_dashboard_loads():
    """Test dashboard page loads"""
    response = client.get('/accounts/analytics/')
    assert response.status_code == 200
    assert 'views' in response.content.decode()
```

---

## Deployment Checklist

- [ ] Create models and migrations
- [ ] Run migrations: `python manage.py migrate`
- [ ] Update views with tracking calls
- [ ] Create analytics API endpoints
- [ ] Create analytics template
- [ ] Add Chart.js CDN link
- [ ] Test locally
- [ ] Add admin models
- [ ] Deploy to staging
- [ ] Test in staging
- [ ] Deploy to production
- [ ] Monitor database size
- [ ] Set up archive job for old views

---

## Future Enhancements

### Phase 2
- 📧 Email reports (weekly/monthly)
- 📱 Mobile analytics view
- 🎯 Goals & milestones tracking
- 💬 Conversation analytics
- 🔔 Alerts for low engagement

### Phase 3
- 🤖 ML-powered insights
- 🌍 Geographic analytics (where viewers are from)
- 👤 Visitor profiles & matching
- 💰 ROI tracking for projects
- 📊 Benchmark against similar projects

---

## Estimated Timeline

| Task | Time |
|------|------|
| Create models & migrations | 30 min |
| Create serializers | 20 min |
| Create views/APIs | 1 hour |
| Create URL routes | 10 min |
| Create frontend template | 1 hour |
| Add tracking to views | 1 hour |
| Create admin interface | 15 min |
| Testing | 30 min |
| **Total** | **4 hours** |

**Conservative estimate with testing: 3-4 days**

---

## Code Examples

### Triggering Tracking in Existing Views

```python
# In like_project view
from .views import track_engagement

def like_project(request, project_id):
    project = get_object_or_404(Project, id=project_id)
    
    # Track the like event
    track_engagement(project_id, request.user, 'like')
    
    if request.user in project.likes.all():
        project.likes.remove(request.user)
    else:
        project.likes.add(request.user)
    
    return redirect('project_detail', project_id=project_id)
```

### Getting Analytics Data

```python
# In your view
from .models import ProjectView, ProjectEngagement
from django.utils import timezone
from datetime import timedelta

def my_view(request):
    project = get_object_or_404(Project, id=project_id)
    
    # Get views from last 7 days
    seven_days_ago = timezone.now() - timedelta(days=7)
    recent_views = project.views.filter(viewed_at__gte=seven_days_ago)
    
    # Get engagement counts
    engagement_counts = project.engagements.values('engagement_type').annotate(
        count=Count('id')
    )
    
    context = {
        'views_7d': recent_views.count(),
        'engagements': engagement_counts
    }
    return render(request, 'template.html', context)
```

---

## Summary

This feature adds comprehensive analytics to track project performance:

✅ **Solves:** No insights into project performance  
✅ **Uses:** Django ORM + Chart.js  
✅ **Time:** 3-4 days (4 hours of development)  
✅ **Impact:** Medium (valuable insights for users)  
✅ **Difficulty:** Medium (new models + API + UI)  
✅ **Value:** High (helps projects improve)  

**Ready to implement!**
