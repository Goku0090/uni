# Quick Profile Link Additions - Code Snippets

Add these profile link snippets to your templates to enable clicking on user profiles throughout the app.

---

## 1. FIND COLLABORATORS PAGE

**File**: `accounts/templates/find_collaborators.html` (or similar)

**Replace user card HTML with**:

```html
<!-- User Collaborator Card with Profile Link -->
<div class="col-md-6 col-lg-4 mb-4">
    <div class="card user-card h-100">
        <!-- Avatar Profile Link -->
        <a href="{% url 'user_profile' username=user.username %}" 
           class="card-img-top user-image-link">
            {% if user.student_profile.profile_photo %}
                <img src="{{ user.student_profile.profile_photo.url }}" 
                     alt="{{ user.username }}"
                     class="img-fluid user-avatar">
            {% else %}
                <div class="avatar-placeholder">
                    {{ user.username|first|upper }}
                </div>
            {% endif %}
        </a>
        
        <div class="card-body">
            <!-- Name Profile Link -->
            <a href="{% url 'user_profile' username=user.username %}" 
               class="card-link text-decoration-none">
                <h5 class="card-title">
                    {{ user.student_profile.full_name }}
                </h5>
            </a>
            
            <p class="card-text text-muted small">
                @{{ user.username }}
            </p>
            
            {% if user.student_profile.college %}
            <p class="card-text">
                <i class="fas fa-graduation-cap"></i> 
                {{ user.student_profile.college }}
            </p>
            {% endif %}
            
            {% if user.student_profile.bio %}
            <p class="card-text small">
                {{ user.student_profile.bio|truncatewords:15 }}
            </p>
            {% endif %}
            
            <!-- Skills -->
            {% if user.student_profile.skills %}
            <div class="mb-3">
                {% for skill in user.student_profile.skills %}
                <span class="badge bg-light text-dark">{{ skill }}</span>
                {% endfor %}
            </div>
            {% endif %}
        </div>
        
        <div class="card-footer bg-white">
            <div class="d-grid gap-2">
                <!-- View Profile Button -->
                <a href="{% url 'user_profile' username=user.username %}" 
                   class="btn btn-outline-primary btn-sm">
                    <i class="fas fa-user"></i> View Profile
                </a>
                
                <!-- Connect Button -->
                <a href="{% url 'send_connection' user.id %}" 
                   class="btn btn-primary btn-sm">
                    <i class="fas fa-user-plus"></i> Connect
                </a>
            </div>
        </div>
    </div>
</div>
```

---

## 2. EXPLORE PROJECTS PAGE

**File**: `accounts/templates/explore_project.html`

**For Project Cards - Add owner profile link**:

```html
<!-- Project Card with Owner Profile Link -->
<div class="card project-card mb-4">
    <!-- Project Owner Section -->
    <div class="card-header bg-light">
        <div class="d-flex align-items-center">
            <a href="{% url 'user_profile' username=project.owner.username %}" 
               class="text-decoration-none me-2">
                {% if project.owner.student_profile.profile_photo %}
                    <img src="{{ project.owner.student_profile.profile_photo.url }}" 
                         alt="{{ project.owner.username }}"
                         class="rounded-circle"
                         width="40" height="40">
                {% else %}
                    <div class="rounded-circle bg-primary text-white d-flex align-items-center justify-content-center"
                         style="width: 40px; height: 40px; font-weight: bold;">
                        {{ project.owner.username|first|upper }}
                    </div>
                {% endif %}
            </a>
            
            <div>
                <a href="{% url 'user_profile' username=project.owner.username %}" 
                   class="text-decoration-none">
                    <h6 class="mb-0">{{ project.owner.student_profile.full_name }}</h6>
                </a>
                <small class="text-muted">@{{ project.owner.username }}</small>
            </div>
        </div>
    </div>
    
    <div class="card-body">
        <h5 class="card-title">{{ project.title }}</h5>
        <p class="card-text">{{ project.description|truncatewords:30 }}</p>
        
        {% if project.technologies %}
        <div class="mb-3">
            <strong>Tech:</strong>
            {% for tech in project.technologies %}
            <span class="badge bg-info">{{ tech }}</span>
            {% endfor %}
        </div>
        {% endif %}
    </div>
    
    <div class="card-footer">
        <div class="d-flex justify-content-between align-items-center">
            <small class="text-muted">
                Created: {{ project.created_at|date:"M d, Y" }}
            </small>
            <div>
                <a href="{% url 'project_detail' project.id %}" 
                   class="btn btn-sm btn-outline-primary">
                    View Project
                </a>
            </div>
        </div>
    </div>
</div>
```

---

## 3. PROJECT DETAIL PAGE

**File**: `accounts/templates/project_detail.html`

**Add to project detail header**:

```html
<!-- Project Detail with Owner Profile Link -->
<div class="container mt-4">
    <div class="row">
        <div class="col-md-8">
            <div class="project-header mb-4">
                <!-- Owner Profile Section -->
                <div class="d-flex align-items-center mb-4 p-3 bg-light rounded">
                    <a href="{% url 'user_profile' username=project.owner.username %}" 
                       class="text-decoration-none">
                        {% if project.owner.student_profile.profile_photo %}
                            <img src="{{ project.owner.student_profile.profile_photo.url }}" 
                                 alt="{{ project.owner.username }}"
                                 class="rounded-circle me-3"
                                 width="60" height="60">
                        {% else %}
                            <div class="rounded-circle bg-primary text-white d-flex align-items-center justify-content-center me-3"
                                 style="width: 60px; height: 60px; font-size: 24px; font-weight: bold;">
                                {{ project.owner.username|first|upper }}
                            </div>
                        {% endif %}
                    </a>
                    
                    <div>
                        <a href="{% url 'user_profile' username=project.owner.username %}" 
                           class="text-decoration-none">
                            <h5 class="mb-0">{{ project.owner.student_profile.full_name }}</h5>
                            <small class="text-muted">@{{ project.owner.username }}</small>
                        </a>
                    </div>
                    
                    <div class="ms-auto">
                        <a href="{% url 'user_profile' username=project.owner.username %}" 
                           class="btn btn-sm btn-outline-primary">
                            View Profile
                        </a>
                    </div>
                </div>
                
                <h1>{{ project.title }}</h1>
                <p class="text-muted">
                    Created: {{ project.created_at|date:"F d, Y" }}
                </p>
            </div>
        </div>
    </div>
</div>
```

**For Project Members**:

```html
<!-- Project Members List -->
<div class="members-section mt-5">
    <h4>Project Team</h4>
    <div class="row">
        {% for member in project.members.all %}
        <div class="col-md-4 mb-3">
            <div class="card member-card">
                <a href="{% url 'user_profile' username=member.user.username %}" 
                   class="card-link">
                    {% if member.user.student_profile.profile_photo %}
                        <img src="{{ member.user.student_profile.profile_photo.url }}" 
                             alt="{{ member.user.username }}"
                             class="card-img-top">
                    {% else %}
                        <div class="card-img-top bg-secondary text-white d-flex align-items-center justify-content-center"
                             style="height: 150px; font-size: 48px; font-weight: bold;">
                            {{ member.user.username|first|upper }}
                        </div>
                    {% endif %}
                </a>
                <div class="card-body">
                    <a href="{% url 'user_profile' username=member.user.username %}" 
                       class="text-decoration-none">
                        <h6 class="card-title">
                            {{ member.user.student_profile.full_name }}
                        </h6>
                    </a>
                    <p class="card-text small">
                        <span class="badge bg-primary">{{ member.get_role_display }}</span>
                    </p>
                </div>
                <div class="card-footer">
                    <a href="{% url 'user_profile' username=member.user.username %}" 
                       class="btn btn-sm btn-outline-primary w-100">
                        View Profile
                    </a>
                </div>
            </div>
        </div>
        {% endfor %}
    </div>
</div>
```

---

## 4. MESSAGES / CHAT PAGE

**File**: `accounts/templates/chat.html`

**For Messages Display**:

```html
<!-- Chat Message with Sender Profile Link -->
<div class="message-item">
    <div class="message-sender-info">
        <a href="{% url 'user_profile' username=message.sender.username %}" 
           class="text-decoration-none d-flex align-items-center">
            {% if message.sender.student_profile.profile_photo %}
                <img src="{{ message.sender.student_profile.profile_photo.url }}" 
                     alt="{{ message.sender.username }}"
                     class="rounded-circle me-2"
                     width="32" height="32">
            {% else %}
                <div class="rounded-circle bg-secondary text-white d-flex align-items-center justify-content-center me-2"
                     style="width: 32px; height: 32px;">
                    {{ message.sender.username|first|upper }}
                </div>
            {% endif %}
            <span class="text-dark">{{ message.sender.username }}</span>
        </a>
        <small class="text-muted ms-2">
            {{ message.created_at|date:"g:i A" }}
        </small>
    </div>
    
    <div class="message-content">
        {{ message.content }}
    </div>
</div>
```

**For Conversation List**:

```html
<!-- Chat Conversation with User Profile Link -->
<div class="conversation-item">
    <a href="{% url 'chat' other_user.id %}" 
       class="text-decoration-none d-flex align-items-center">
        
        <!-- User Avatar -->
        <a href="{% url 'user_profile' username=other_user.username %}" 
           class="text-decoration-none me-3"
           onclick="event.stopPropagation();">
            {% if other_user.student_profile.profile_photo %}
                <img src="{{ other_user.student_profile.profile_photo.url }}" 
                     alt="{{ other_user.username }}"
                     class="rounded-circle"
                     width="48" height="48">
            {% else %}
                <div class="rounded-circle bg-primary text-white d-flex align-items-center justify-content-center"
                     style="width: 48px; height: 48px; font-size: 20px; font-weight: bold;">
                    {{ other_user.username|first|upper }}
                </div>
            {% endif %}
        </a>
        
        <!-- User Info -->
        <div class="flex-grow-1">
            <div class="d-flex justify-content-between align-items-center">
                <div>
                    <a href="{% url 'user_profile' username=other_user.username %}" 
                       class="text-decoration-none"
                       onclick="event.stopPropagation();">
                        <strong>{{ other_user.student_profile.full_name }}</strong>
                    </a>
                    <span class="text-muted ms-2">@{{ other_user.username }}</span>
                </div>
                <small class="text-muted">
                    {{ last_message.created_at|date:"M d" }}
                </small>
            </div>
            <p class="text-muted small mb-0">
                {{ last_message.content|truncatewords:10 }}
            </p>
        </div>
    </a>
</div>
```

---

## 5. ACTIVITY FEED

**File**: `accounts/templates/activity_feed.html` (or dashboard)

**For Activity Items**:

```html
<!-- Activity Feed Item with User Profile Link -->
<div class="activity-item p-3 border-bottom">
    <div class="d-flex align-items-start">
        <!-- User Avatar Link -->
        <a href="{% url 'user_profile' username=activity.user.username %}" 
           class="text-decoration-none me-3">
            {% if activity.user.student_profile.profile_photo %}
                <img src="{{ activity.user.student_profile.profile_photo.url }}" 
                     alt="{{ activity.user.username }}"
                     class="rounded-circle"
                     width="40" height="40">
            {% else %}
                <div class="rounded-circle bg-secondary text-white d-flex align-items-center justify-content-center"
                     style="width: 40px; height: 40px;">
                    {{ activity.user.username|first|upper }}
                </div>
            {% endif %}
        </a>
        
        <div class="flex-grow-1">
            <!-- Activity Text with User Link -->
            <p class="mb-1">
                <a href="{% url 'user_profile' username=activity.user.username %}" 
                   class="text-decoration-none">
                    <strong>{{ activity.user.student_profile.full_name }}</strong>
                </a>
                {{ activity.title }}
            </p>
            
            {% if activity.description %}
            <p class="text-muted small mb-1">
                {{ activity.description }}
            </p>
            {% endif %}
            
            <small class="text-muted">
                {{ activity.created_at|timesince }} ago
            </small>
        </div>
    </div>
</div>
```

---

## 6. NOTIFICATIONS PAGE

**File**: `accounts/templates/notifications.html` (or notification list)

**For Notification Items**:

```html
<!-- Notification with User Profile Link -->
<div class="notification-item">
    <a href="{% url 'user_profile' username=notification.from_user.username %}" 
       class="text-decoration-none d-flex align-items-center">
        
        <!-- User Avatar -->
        {% if notification.from_user.student_profile.profile_photo %}
            <img src="{{ notification.from_user.student_profile.profile_photo.url }}" 
                 alt="{{ notification.from_user.username }}"
                 class="rounded-circle me-3"
                 width="40" height="40">
        {% else %}
            <div class="rounded-circle bg-secondary text-white d-flex align-items-center justify-content-center me-3"
                 style="width: 40px; height: 40px;">
                {{ notification.from_user.username|first|upper }}
            </div>
        {% endif %}
        
        <!-- Notification Content -->
        <div class="flex-grow-1">
            <p class="mb-0">
                <strong>{{ notification.from_user.student_profile.full_name }}</strong>
                <span class="text-muted">{{ notification.message }}</span>
            </p>
            <small class="text-muted">
                {{ notification.created_at|timesince }} ago
            </small>
        </div>
    </a>
</div>
```

---

## 7. SEARCH RESULTS

**File**: `accounts/templates/search_results.html` (if exists)

**For User Search Results**:

```html
<!-- User Search Result with Profile Link -->
<a href="{% url 'user_profile' username=user.username %}" 
   class="list-group-item list-group-item-action d-flex justify-content-between align-items-center">
    
    <div class="d-flex align-items-center">
        {% if user.student_profile.profile_photo %}
            <img src="{{ user.student_profile.profile_photo.url }}" 
                 alt="{{ user.username }}"
                 class="rounded-circle me-3"
                 width="40" height="40">
        {% else %}
            <div class="rounded-circle bg-secondary text-white d-flex align-items-center justify-content-center me-3"
                 style="width: 40px; height: 40px;">
                {{ user.username|first|upper }}
            </div>
        {% endif %}
        
        <div>
            <h6 class="mb-0">{{ user.student_profile.full_name }}</h6>
            <small class="text-muted">@{{ user.username }}</small>
        </div>
    </div>
    
    <span class="badge bg-primary">
        {{ user.student_profile.college }}
    </span>
</a>
```

---

## 8. GLOBAL CSS ADDITIONS

**Add to your CSS file or `<style>` tag**:

```css
/* Profile Link Styling */
a[href*="/user/"] {
    transition: color 0.2s ease;
}

a[href*="/user/"] {
    color: #007bff;
}

a[href*="/user/"]:hover {
    color: #0056b3;
    text-decoration: underline;
}

/* Avatar Styling */
.rounded-circle {
    border: 2px solid #e0e0e0;
    object-fit: cover;
    cursor: pointer;
    transition: border-color 0.2s ease;
}

.rounded-circle:hover {
    border-color: #007bff;
}

/* User Card Hover Effect */
.user-card {
    transition: transform 0.2s, box-shadow 0.2s;
}

.user-card:hover {
    transform: translateY(-4px);
    box-shadow: 0 4px 12px rgba(0, 0, 0, 0.15);
}

/* Card Link Text */
.card-link {
    color: inherit;
    text-decoration: none;
}

.card-link:hover {
    color: #007bff;
}

.card-title {
    transition: color 0.2s ease;
}

.card-title a {
    color: inherit;
}

.card-title a:hover {
    color: #007bff;
}

/* Message Sender Link */
.message-sender-info a {
    transition: opacity 0.2s ease;
}

.message-sender-info a:hover {
    opacity: 0.8;
}

/* Activity User Link */
.activity-item a {
    text-decoration: none;
}

.activity-item a:hover {
    text-decoration: underline;
}
```

---

## 9. IMPLEMENTATION ORDER

**Recommended order to implement**:

1. ✅ **Find Collaborators** (Section 1) - Most important
2. ✅ **Explore Projects** (Section 2) - Common use case
3. ✅ **Project Detail** (Section 3) - Show team members
4. ✅ **Messages/Chat** (Section 4) - Enable easy profile viewing in conversations
5. ✅ **Activity Feed** (Section 5) - See who did what
6. ✅ **Notifications** (Section 6) - Quick links to notification sources
7. ✅ **Search Results** (Section 7) - If search exists
8. ✅ **Global CSS** (Section 8) - Apply to all pages

---

## 10. TESTING CHECKLIST

After implementing all sections:

```
[ ] Click on user names - opens profile ✓
[ ] Click on avatars - opens profile ✓
[ ] Click on "View Profile" buttons ✓
[ ] All links work correctly ✓
[ ] Mobile responsive ✓
[ ] Hover effects work ✓
[ ] Profile page shows correct user ✓
[ ] No 404 errors ✓
[ ] Page loads quickly ✓
[ ] All profile info displays ✓
```

---

## Summary

These snippets provide a complete implementation of profile linking throughout the application. Simply copy-paste the relevant sections into your templates and you're done!

**Time to implement**: 1-2 hours  
**Difficulty**: Easy  
**Testing required**: Yes (manual)

---
