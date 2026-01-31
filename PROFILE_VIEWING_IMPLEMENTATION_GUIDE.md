# Profile Viewing Feature - Implementation & Setup Guide

**Date**: January 29, 2026  
**Feature**: Click on any user profile to view their public profile  
**Status**: Partially Implemented - Needs Frontend Links

---

## 1. CURRENT STATE

### ✅ What's Already Implemented

**Backend View** (`accounts/views.py` - Line 2501):
```python
def user_profile(request, username):
    """View a user's public profile with their activities"""
    profile_user = get_object_or_404(User, username=username)
    
    # Get user stats (projects, connections, likes, etc.)
    user_stats, created = UserStats.objects.get_or_create(user=profile_user, defaults={})
    if created or (timezone.now() - user_stats.last_updated).seconds > 300:
        user_stats.update_stats()
    
    # Check if current user follows this user
    is_following = Follow.objects.filter(follower=request.user, following=profile_user).exists()
    is_own_profile = request.user == profile_user
    
    # Get user's public activities (20 most recent)
    activities = Activity.objects.filter(
        user=profile_user,
        is_public=True
    ).order_by('-created_at')[:20]
    
    # Get user's public projects (6 most recent)
    projects = Project.objects.filter(user=profile_user).order_by('-created_at')[:6]
    
    # Get connection count
    connections_count = Connection.objects.filter(
        Q(sender=profile_user, status='accepted') | Q(receiver=profile_user, status='accepted')
    ).count()
    
    context = {
        'profile_user': profile_user,
        'user_stats': user_stats,
        'is_following': is_following,
        'is_own_profile': is_own_profile,
        'activities': activities,
        'projects': projects,
        'connections_count': connections_count,
        'student_profile': getattr(profile_user, 'student_profile', None),
    }
    
    return render(request, 'social/user_profile.html', context)
```

**URL Route** (`accounts/urls.py` - Line 48):
```python
path('user/<str:username>/', views.user_profile, name='user_profile'),
```

**Template**: `accounts/templates/social/user_profile.html` (13,851 bytes)

**Data Displayed**:
- Profile photo
- Full name
- College/location
- Bio
- Skills and interests
- Social links (GitHub, LinkedIn, etc.)
- User statistics (projects, connections, likes, comments)
- Recent projects
- Recent activities
- Follow button (if applicable)

---

## 2. HOW TO IMPLEMENT PROFILE LINKS

### 2.1 Add Links in User List/Cards

**For Find Collaborators Page**:
```html
<!-- In find_collaborators.html template -->
<a href="{% url 'user_profile' username=user.username %}" 
   class="user-link btn btn-sm btn-outline-primary">
    View Profile
</a>
```

**For User Cards**:
```html
<!-- Generic user card component -->
<div class="user-card">
    <a href="{% url 'user_profile' username=user.username %}" 
       class="user-name-link">
        <h5>{{ user.student_profile.full_name }}</h5>
    </a>
    <img src="{{ user.student_profile.profile_photo.url }}" 
         alt="Profile" class="profile-photo">
    <p class="college">{{ user.student_profile.college }}</p>
</div>
```

### 2.2 Add Links in Project Details

```html
<!-- In project_detail.html -->
<div class="project-owner">
    <a href="{% url 'user_profile' username=project.owner.username %}" 
       class="owner-link">
        <img src="{{ project.owner.student_profile.profile_photo.url }}" 
             alt="Owner">
        <h6>{{ project.owner.student_profile.full_name }}</h6>
    </a>
</div>
```

### 2.3 Add Links in Messages/Comments

```html
<!-- In message display -->
<div class="message">
    <a href="{% url 'user_profile' username=message.sender.username %}" 
       class="sender-link">
        <img src="{{ message.sender.student_profile.profile_photo.url }}" 
             alt="Sender">
        {{ message.sender.username }}
    </a>
    <p>{{ message.content }}</p>
</div>
```

### 2.4 Add Links in Activity Feed

```html
<!-- In activity_feed.html or dashboard -->
<div class="activity-item">
    <a href="{% url 'user_profile' username=activity.user.username %}" 
       class="activity-user-link">
        {{ activity.user.student_profile.full_name }}
    </a>
    <span>{{ activity.title }}</span>
</div>
```

---

## 3. USAGE FLOW

```
User1 clicks on User2's name/avatar
    ↓
URL: /user/<username>/
    ↓
views.user_profile(request, username)
    ↓
Fetch User, StudentProfile, UserStats, Activities, Projects
    ↓
Check if follower, connection status
    ↓
Render social/user_profile.html
    ↓
Display full profile with:
    ├─ Profile info
    ├─ Avatar & social links
    ├─ Stats (projects, connections, followers)
    ├─ Recent projects
    ├─ Recent activities
    ├─ Connection request button (if not connected)
    └─ Follow/Unfollow button
```

---

## 4. FEATURES AVAILABLE ON USER PROFILE PAGE

### 4.1 Profile Information Display
```
├─ Profile Photo
├─ Full Name
├─ Username
├─ College/University
├─ Location
├─ Bio
├─ Skills (as tags)
├─ Project Interests (as tags)
├─ Social Links:
│  ├─ GitHub
│  ├─ LinkedIn
│  ├─ Portfolio
│  └─ Behance
└─ Account created date
```

### 4.2 User Statistics
```
├─ Projects created
├─ Connections made
├─ Likes received
├─ Comments made
├─ Followers count
└─ Following count
```

### 4.3 User's Recent Projects (6 latest)
- Project title
- Description snippet
- Technologies used
- Looking for roles
- Like/Comment count

### 4.4 User's Recent Activities (20 latest)
- Activity type icons
- Activity description
- Timestamp

### 4.5 Interactive Features
- **Follow/Unfollow button** (if not own profile)
- **Send Connection Request** (if not connected)
- **View projects** (clickable project cards)
- **View activities** (full activity feed)

---

## 5. TEMPLATE CHANGES NEEDED

### 5.1 Find Collaborators Template
**File**: `accounts/templates/find_collaborators.html` or similar

**Add**:
```html
{% for user in users %}
<div class="collaborator-card">
    <div class="card-header">
        <a href="{% url 'user_profile' username=user.username %}" class="user-profile-link">
            {% if user.student_profile.profile_photo %}
                <img src="{{ user.student_profile.profile_photo.url }}" 
                     alt="{{ user.username }}" class="avatar">
            {% else %}
                <div class="avatar-placeholder">{{ user.username|first|upper }}</div>
            {% endif %}
        </a>
    </div>
    <div class="card-body">
        <a href="{% url 'user_profile' username=user.username %}" class="user-link">
            <h5>{{ user.student_profile.full_name }}</h5>
        </a>
        <p class="college">{{ user.student_profile.college }}</p>
        <p class="bio">{{ user.student_profile.bio }}</p>
        <div class="actions">
            <a href="{% url 'user_profile' username=user.username %}" 
               class="btn btn-sm btn-outline-primary">
                View Profile
            </a>
            <a href="{% url 'send_connection' user.id %}" 
               class="btn btn-sm btn-primary">
                Connect
            </a>
        </div>
    </div>
</div>
{% endfor %}
```

### 5.2 Explore Projects Template
**File**: `accounts/templates/explore_project.html`

**Add**:
```html
{% for project in projects %}
<div class="project-card">
    <div class="project-owner">
        <a href="{% url 'user_profile' username=project.owner.username %}">
            <img src="{{ project.owner.student_profile.profile_photo.url }}" 
                 alt="Owner" class="owner-avatar">
            <span>{{ project.owner.student_profile.full_name }}</span>
        </a>
    </div>
    <!-- Rest of project card -->
</div>
{% endfor %}
```

### 5.3 Messages/Chat Template
**File**: `accounts/templates/chat.html`

**Add**:
```html
{% for message in messages %}
<div class="message">
    <div class="message-sender">
        <a href="{% url 'user_profile' username=message.sender.username %}">
            <img src="{{ message.sender.student_profile.profile_photo.url }}" 
                 alt="Sender">
            <span>{{ message.sender.username }}</span>
        </a>
    </div>
    <div class="message-content">
        {{ message.content }}
    </div>
</div>
{% endfor %}
```

---

## 6. CSS STYLING RECOMMENDATIONS

```css
/* Profile link styling */
.user-profile-link {
    text-decoration: none;
    color: inherit;
    transition: opacity 0.2s ease;
}

.user-profile-link:hover {
    opacity: 0.8;
}

/* User name links */
.user-link, .user-name-link {
    color: #007bff;
    text-decoration: none;
    font-weight: 500;
}

.user-link:hover, .user-name-link:hover {
    text-decoration: underline;
    color: #0056b3;
}

/* Avatar styling */
.avatar {
    width: 40px;
    height: 40px;
    border-radius: 50%;
    object-fit: cover;
    border: 2px solid #e0e0e0;
    cursor: pointer;
    transition: border-color 0.2s ease;
}

.avatar:hover {
    border-color: #007bff;
}

/* User cards */
.user-card {
    border: 1px solid #e0e0e0;
    border-radius: 8px;
    padding: 15px;
    text-align: center;
    transition: box-shadow 0.3s ease;
}

.user-card:hover {
    box-shadow: 0 4px 12px rgba(0, 0, 0, 0.1);
}

.profile-photo {
    width: 100%;
    height: 150px;
    object-fit: cover;
    border-radius: 8px;
    margin: 10px 0;
}
```

---

## 7. DJANGO URL TAGS REFERENCE

### Basic Usage
```html
<!-- Simple profile link by username -->
<a href="{% url 'user_profile' username=user.username %}">
    {{ user.get_full_name }}
</a>

<!-- With custom text -->
<a href="{% url 'user_profile' user.username %}">
    View {{ user.username }}'s profile
</a>

<!-- In template variables -->
{% url 'user_profile' username=profile_user.username as profile_url %}
<a href="{{ profile_url }}">Profile</a>
```

---

## 8. TESTING THE FEATURE

### 8.1 Manual Testing Checklist

```
[ ] Navigate to /user/testuser1/
[ ] Verify profile page loads correctly
[ ] Verify all profile info displays:
    [ ] Avatar
    [ ] Full name
    [ ] College
    [ ] Bio
    [ ] Skills
    [ ] Social links
[ ] Verify stats display correctly
[ ] Verify recent projects show (max 6)
[ ] Verify recent activities show (max 20)
[ ] Check connection status button
[ ] Check follow/unfollow button
[ ] Test with invalid username (should 404)
[ ] Test mobile responsiveness
```

### 8.2 Test Cases

**Test 1**: View own profile
```
User: testuser1
Click: testuser1's profile
Expected: View own profile, see "Edit Profile" button
```

**Test 2**: View another user's profile
```
User: testuser1
Click: testuser2's profile
Expected: View testuser2's profile, see "Connect" button
```

**Test 3**: Invalid username
```
URL: /user/nonexistentuser/
Expected: 404 error page
```

**Test 4**: Profile with no photo
```
User: userwithouphoto
Expected: Show avatar placeholder or default image
```

---

## 9. SECURITY CONSIDERATIONS

### 9.1 Current Security Features

✅ **Only public data displayed**:
- Email address: NOT shown
- Password: Never displayed
- Private activities: Filtered out (is_public=True only)
- Private projects: Not shown in profile

✅ **Access control**:
- No authentication required to view profiles
- Users can control what activities are public
- Profile completion is optional

### 9.2 Recommended Enhancements

1. **Privacy settings**:
```python
# Add to StudentProfile model
class StudentProfile:
    PRIVACY_CHOICES = [
        ('public', 'Everyone can see'),
        ('friends', 'Only connections'),
        ('private', 'Only me'),
    ]
    privacy_level = models.CharField(
        max_length=10, 
        choices=PRIVACY_CHOICES, 
        default='public'
    )
```

2. **Block/Report user**:
```python
# Prevent blocked users from viewing profile
if BlockedUser.objects.filter(
    blocker=profile_user, 
    blocked=request.user
).exists():
    return HttpResponseForbidden("You cannot view this profile")
```

3. **Rate limiting** on profile views to prevent scraping

---

## 10. PERFORMANCE OPTIMIZATION

### 10.1 Current Query Optimization

```python
# The view already uses:
activities = Activity.objects.filter(...).select_related(
    'user', 'project', 'target_user', 'connection'
)  # Reduces N+1 queries

projects = Project.objects.filter(
    user=profile_user
).order_by('-created_at')[:6]  # Limits to 6, sorted by date
```

### 10.2 Further Optimizations

```python
# Add caching for profile views (5 min TTL)
from django.views.decorators.cache import cache_page

@cache_page(60 * 5)  # Cache for 5 minutes
def user_profile(request, username):
    # ... view code ...
```

### 10.3 Database Indexes

Ensure indexes on frequently queried fields:
```python
class Meta:
    indexes = [
        models.Index(fields=['user', '-created_at']),  # For Activity
        models.Index(fields=['user', '-created_at']),  # For Project
        models.Index(fields=['username']),  # For User lookup
    ]
```

---

## 11. IMPLEMENTATION CHECKLIST

### Phase 1: Verify Backend (DONE ✅)
- [x] `user_profile` view exists
- [x] URL route configured
- [x] Template file exists
- [x] Context data prepared

### Phase 2: Add Frontend Links (TODO)
- [ ] Find collaborators page: Add "View Profile" button
- [ ] Explore projects page: Add owner profile link
- [ ] Messages/chat: Add sender profile link
- [ ] Activity feed: Add user profile link
- [ ] Project detail: Add owner/member profile links
- [ ] Notifications: Add source user profile link
- [ ] Search results: Add user profile links

### Phase 3: Styling (TODO)
- [ ] Add CSS for profile links
- [ ] Add avatar hover effects
- [ ] Mobile responsive styling
- [ ] Ensure consistent styling across all pages

### Phase 4: Testing (TODO)
- [ ] Manual testing of all profile links
- [ ] Test 404 handling
- [ ] Test with users without photos
- [ ] Test on mobile devices
- [ ] Performance testing

### Phase 5: Documentation (TODO)
- [ ] Update user documentation
- [ ] Add help center article
- [ ] Create video tutorial (optional)

---

## 12. EXAMPLE COMPLETE IMPLEMENTATION

### Find Collaborators Template (Complete Example)

```html
{% extends "base.html" %}
{% load static %}

{% block title %}Find Collaborators{% endblock %}

{% block content %}
<div class="container mt-5">
    <h2>Find Collaborators</h2>
    
    <div class="filters mb-4">
        <!-- Filter form here -->
    </div>
    
    <div class="collaborators-grid row">
        {% for user in users %}
        <div class="col-md-6 col-lg-4 mb-4">
            <div class="card user-card">
                <!-- Profile Link -->
                <a href="{% url 'user_profile' username=user.username %}" 
                   class="card-link">
                    <div class="card-img-top user-image">
                        {% if user.student_profile.profile_photo %}
                            <img src="{{ user.student_profile.profile_photo.url }}" 
                                 alt="{{ user.username }}"
                                 class="user-avatar">
                        {% else %}
                            <div class="avatar-placeholder">
                                {{ user.username|first|upper }}
                            </div>
                        {% endif %}
                    </div>
                </a>
                
                <div class="card-body">
                    <!-- Name Link -->
                    <a href="{% url 'user_profile' username=user.username %}" 
                       class="card-title">
                        <h5>{{ user.student_profile.full_name }}</h5>
                    </a>
                    
                    <p class="card-text college">
                        {{ user.student_profile.college }}
                    </p>
                    
                    <p class="card-text bio">
                        {{ user.student_profile.bio|truncatewords:15 }}
                    </p>
                    
                    <!-- Skills -->
                    <div class="skills mb-3">
                        {% for skill in user.student_profile.skills %}
                        <span class="badge badge-secondary">{{ skill }}</span>
                        {% endfor %}
                    </div>
                    
                    <!-- Action Buttons -->
                    <div class="btn-group w-100" role="group">
                        <a href="{% url 'user_profile' username=user.username %}" 
                           class="btn btn-outline-primary">
                            View Profile
                        </a>
                        <a href="{% url 'send_connection' user.id %}" 
                           class="btn btn-primary">
                            Connect
                        </a>
                    </div>
                </div>
            </div>
        </div>
        {% empty %}
        <div class="col-12">
            <p class="text-muted">No collaborators found matching your criteria.</p>
        </div>
        {% endfor %}
    </div>
</div>

<style>
.user-card {
    transition: transform 0.2s, box-shadow 0.2s;
    border: 1px solid #e0e0e0;
}

.user-card:hover {
    transform: translateY(-5px);
    box-shadow: 0 4px 12px rgba(0, 0, 0, 0.15);
}

.user-image {
    height: 200px;
    overflow: hidden;
    background-color: #f0f0f0;
}

.user-avatar {
    width: 100%;
    height: 100%;
    object-fit: cover;
}

.avatar-placeholder {
    display: flex;
    align-items: center;
    justify-content: center;
    height: 100%;
    font-size: 48px;
    background-color: #007bff;
    color: white;
    font-weight: bold;
}

.card-title a {
    text-decoration: none;
    color: inherit;
}

.card-title a:hover {
    color: #007bff;
}

.skills {
    display: flex;
    flex-wrap: wrap;
    gap: 5px;
}

.badge {
    font-size: 12px;
}

.btn-group {
    gap: 5px;
}

.btn-group .btn {
    flex: 1;
    font-size: 14px;
}
</style>
{% endblock %}
```

---

## 13. NEXT STEPS

1. **Run the test suite**:
```bash
python manage.py test accounts.tests.ProfileTests
```

2. **Add profile links** to all user-facing pages:
   - Find collaborators
   - Explore projects
   - Messages/chat
   - Activity feed
   - Search results

3. **Update CSS** for consistent styling across links

4. **Test thoroughly** on desktop and mobile

5. **Gather user feedback** on usability

---

## 14. REFERENCE DOCUMENTATION

### URL Reverse Lookup
```python
# In Python code
from django.urls import reverse
profile_url = reverse('user_profile', kwargs={'username': 'johndoe'})

# In templates
{% url 'user_profile' username=user.username %}
```

### Context Variables Available
```python
{
    'profile_user': User,              # The user being viewed
    'student_profile': StudentProfile, # Extended profile data
    'user_stats': UserStats,           # Stats model
    'is_following': bool,              # Current user follows
    'is_own_profile': bool,            # Is current user's profile
    'activities': QuerySet,            # Recent public activities
    'projects': QuerySet,              # Recent projects
    'connections_count': int,          # Total connections
}
```

---

## Summary

The profile viewing feature is **fully implemented on the backend**. All that's needed is to:

1. ✅ Backend: Already done (view + URL + template)
2. ⏳ Frontend: Add profile links throughout the application
3. ⏳ Styling: Ensure consistent styling
4. ⏳ Testing: Verify all links work

**Estimated Time to Complete**: 2-4 hours

**Difficulty Level**: Easy (mostly template updates)

---

**End of Implementation Guide**
