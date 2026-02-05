# Notification Click Redirect Implementation

## 📋 Current Problem

When a user clicks on a notification, it should redirect them to the relevant content:
- **Connection Request** → User's profile
- **Message** → Message chat
- **Project Like** → Project details
- **Project Comment** → Project with comments section
- **Team Invitation** → Project or team management page
- **User Follow** → User's profile

**Current Issue**: Notifications are just static text with no clickable functionality.

---

## 🚀 SOLUTION: 3 APPROACHES

### Approach 1: Simple & Fast (1-2 hours) ⭐ RECOMMENDED
Add notification type field to model + view functions to generate URLs

### Approach 2: Medium Effort (2-3 hours)
GenericForeignKey to link notifications to any model

### Approach 3: Full Featured (3-4 hours)
Complete refactor with URL generation, tracking, and analytics

---

## 🔧 IMPLEMENTATION: APPROACH 1 (RECOMMENDED)

### STEP 1: Update Notification Model (15 min)

**File**: `accounts/models.py`

**Find**: The Notification class (around line 337)

**Add these fields** to the Notification model:

```python
class Notification(models.Model):
    """User notifications"""

    NOTIFICATION_TYPES = [
        ('connection_request', 'Connection Request'),
        ('connection_accepted', 'Connection Accepted'),
        ('message', 'New Message'),
        ('project_like', 'Project Liked'),
        ('project_comment', 'Project Comment'),
        ('team_invitation', 'Team Invitation'),
        ('follow', 'User Follow'),
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='notifications')
    notification_type = models.CharField(max_length=20, choices=NOTIFICATION_TYPES)
    title = models.CharField(max_length=200)
    message = models.TextField()

    # Related objects
    from_user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name='sent_notifications')
    connection = models.ForeignKey(Connection, on_delete=models.SET_NULL, null=True, blank=True)
    message_obj = models.ForeignKey(Message, on_delete=models.SET_NULL, null=True, blank=True)
    
    # ADD THESE TWO FIELDS:
    project = models.ForeignKey(Project, on_delete=models.SET_NULL, null=True, blank=True)  # For project-related notifications
    redirect_url = models.CharField(max_length=500, blank=True, null=True)  # Custom redirect URL

    is_read = models.BooleanField(default=False)
    read_at = models.DateTimeField(null=True, blank=True)
    created_at = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return f"{self.user.username}: {self.title}"
    
    # ADD THIS METHOD:
    def get_redirect_url(self):
        """Get the URL to redirect to when notification is clicked"""
        from django.urls import reverse
        
        if self.redirect_url:
            return self.redirect_url
        
        # Generate URL based on notification type
        if self.notification_type == 'connection_request':
            return reverse('user_profile', args=[self.from_user.username])
        
        elif self.notification_type == 'connection_accepted':
            return reverse('user_profile', args=[self.from_user.username])
        
        elif self.notification_type == 'message':
            if self.message_obj:
                # Redirect to chat with the user
                if self.message_obj.sender == self.user:
                    return reverse('chat', args=[self.message_obj.receiver.id])
                else:
                    return reverse('chat', args=[self.message_obj.sender.id])
            return reverse('messages')
        
        elif self.notification_type == 'project_like':
            if self.project:
                return reverse('project_detail', args=[self.project.id])
            return reverse('main_home')
        
        elif self.notification_type == 'project_comment':
            if self.project:
                return reverse('project_detail', args=[self.project.id]) + '#comments'
            return reverse('main_home')
        
        elif self.notification_type == 'team_invitation':
            if self.project:
                return reverse('project_detail', args=[self.project.id]) + '#team'
            return reverse('main_home')
        
        elif self.notification_type == 'follow':
            if self.from_user:
                return reverse('user_profile', args=[self.from_user.username])
            return reverse('main_home')
        
        return reverse('main_home')

    class Meta:
        ordering = ['-created_at']
```

**Migration**:
```bash
python manage.py makemigrations
python manage.py migrate
```

---

### STEP 2: Update create_notification() Helper (15 min)

**File**: `accounts/views.py`

**Find**: The `create_notification()` function (around line 807)

**Replace it with**:

```python
def create_notification(user, notification_type, title, message, from_user=None, connection=None, message_obj=None, project=None):
    """Create a notification for a user with redirect URL"""
    from django.urls import reverse
    
    # Generate redirect URL based on notification type
    redirect_url = None
    
    if notification_type == 'connection_request':
        redirect_url = reverse('user_profile', args=[from_user.username]) if from_user else None
    
    elif notification_type == 'message':
        if message_obj:
            if message_obj.sender == user:
                redirect_url = reverse('chat', args=[message_obj.receiver.id])
            else:
                redirect_url = reverse('chat', args=[message_obj.sender.id])
    
    elif notification_type == 'project_like':
        if project:
            redirect_url = reverse('project_detail', args=[project.id])
    
    elif notification_type == 'project_comment':
        if project:
            redirect_url = reverse('project_detail', args=[project.id]) + '#comments'
    
    elif notification_type == 'team_invitation':
        if project:
            redirect_url = reverse('project_detail', args=[project.id]) + '#team'
    
    elif notification_type == 'follow':
        redirect_url = reverse('user_profile', args=[from_user.username]) if from_user else None
    
    # Create notification
    notification = Notification.objects.create(
        user=user,
        notification_type=notification_type,
        title=title,
        message=message,
        from_user=from_user,
        connection=connection,
        message_obj=message_obj,
        project=project,
        redirect_url=redirect_url
    )
    
    # Send real-time notification via WebSocket (if configured)
    try:
        from channels.layers import get_channel_layer
        from asgiref.sync import async_to_sync
        channel_layer = get_channel_layer()
        async_to_sync(channel_layer.group_send)(
            f'notification_{user.id}',
            {
                'type': 'notification_message',
                'notification': {
                    'id': notification.id,
                    'title': notification.title,
                    'message': notification.message,
                    'type': notification.notification_type,
                }
            }
        )
    except Exception as e:
        pass  # WebSocket not configured, that's fine
    
    return notification
```

---

### STEP 3: Create Notification Click Handler View (20 min)

**File**: `accounts/views.py`

**Add this function**:

```python
@login_required
def notification_click(request, notification_id):
    """Handle notification click and redirect"""
    try:
        notification = Notification.objects.get(id=notification_id, user=request.user)
        
        # Mark as read
        if not notification.is_read:
            notification.is_read = True
            notification.read_at = timezone.now()
            notification.save()
        
        # Get redirect URL
        redirect_url = notification.get_redirect_url()
        
        # Log the notification click (optional - for analytics)
        logger.info(f"User {request.user.username} clicked notification {notification_id}")
        
        return redirect(redirect_url)
    
    except Notification.DoesNotExist:
        messages.error(request, "Notification not found")
        return redirect('notifications')
    except Exception as e:
        logger.error(f"Error handling notification click: {str(e)}")
        messages.error(request, "Error processing notification")
        return redirect('notifications')
```

---

### STEP 4: Update URLs (10 min)

**File**: `accounts/urls.py`

**Add this route**:

```python
path('notification/<int:notification_id>/', views.notification_click, name='notification_click'),
```

---

### STEP 5: Update Notifications Template (20 min)

**File**: `templates/notifications.html`

**Find**: The notification-item div (around line 148)

**Replace the entire notification loop** with:

```html
{% if notifications %}
    {% for notification in notifications %}
        <!-- Make notification clickable -->
        <a href="{% url 'notification_click' notification.id %}" 
           class="block no-underline">
            <div class="notification-item {% if not notification.is_read %}unread{% endif %} 
                        hover:shadow-lg transition-all duration-300 cursor-pointer">
                <div class="flex items-start gap-4">
                    <!-- User Avatar -->
                    {% if notification.from_user %}
                        <img src="{{ notification.from_user.student_profile.profile_photo.url|default:'/static/default-avatar.png' }}" 
                             alt="{{ notification.from_user.username }}" 
                             class="w-12 h-12 rounded-full object-cover border-2 border-blue-200">
                    {% else %}
                        <div class="notification-icon bg-blue-100">
                            {% if notification.notification_type == 'connection_request' %}
                                👤
                            {% elif notification.notification_type == 'message' %}
                                💬
                            {% elif notification.notification_type == 'project_like' %}
                                ❤️
                            {% elif notification.notification_type == 'project_comment' %}
                                💭
                            {% elif notification.notification_type == 'team_invitation' %}
                                👥
                            {% elif notification.notification_type == 'follow' %}
                                👁️
                            {% else %}
                                📢
                            {% endif %}
                        </div>
                    {% endif %}
                    
                    <!-- Notification Content -->
                    <div class="flex-1 min-w-0">
                        <div class="flex items-start justify-between gap-2">
                            <div>
                                <h3 class="font-semibold text-gray-900 text-sm">
                                    {{ notification.title }}
                                </h3>
                                <p class="text-sm text-gray-600 mt-1 leading-relaxed">
                                    {{ notification.message }}
                                </p>
                                <span class="text-xs text-gray-500 mt-2 block">
                                    🕐 {{ notification.created_at|timesince }} ago
                                </span>
                            </div>
                            
                            <!-- Unread Indicator -->
                            {% if not notification.is_read %}
                                <span class="w-3 h-3 bg-blue-600 rounded-full flex-shrink-0 mt-1.5 animate-pulse"></span>
                            {% endif %}
                        </div>
                    </div>
                    
                    <!-- Arrow Icon (shows it's clickable) -->
                    <svg class="w-5 h-5 text-gray-400 flex-shrink-0 mt-1 group-hover:text-blue-600 transition" 
                         fill="none" stroke="currentColor" viewBox="0 0 24 24">
                        <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 5l7 7-7 7"></path>
                    </svg>
                </div>
            </div>
        </a>
    {% endfor %}
{% else %}
    <div class="empty-state">
        <div class="empty-state-icon">📭</div>
        <h3 class="text-xl font-semibold text-gray-900 mb-2">No notifications yet</h3>
        <p class="text-gray-600 mb-6">You're all caught up! Check back later for updates.</p>
        <div class="flex gap-3 justify-center">
            <a href="{% url 'find_collaborators' %}" class="px-6 py-3 bg-blue-600 text-white rounded-lg hover:bg-blue-700 transition font-medium">
                Find Collaborators
            </a>
            <a href="{% url 'main_home' %}" class="px-6 py-3 bg-gray-200 text-gray-800 rounded-lg hover:bg-gray-300 transition font-medium">
                Back to Home
            </a>
        </div>
    </div>
{% endif %}
```

---

### STEP 6: Update Notification Creation Calls (15 min)

**Throughout `views.py`**, update all `create_notification()` calls to include the project parameter:

**Example 1: When someone comments on a project**
```python
# OLD:
create_notification(
    user=project.user,
    notification_type='project_comment',
    title=f'{request.user.username} commented on your project',
    message=f'"{project.title}": {comment_text[:100]}...',
    from_user=request.user
)

# NEW:
create_notification(
    user=project.user,
    notification_type='project_comment',
    title=f'{request.user.username} commented on your project',
    message=f'"{project.title}": {comment_text[:100]}...',
    from_user=request.user,
    project=project  # ADD THIS
)
```

**Example 2: When someone likes a project**
```python
# OLD:
create_notification(
    user=project.user,
    notification_type='project_like',
    title=f'{request.user.username} liked your project',
    message=f'"{project.title}" got a like',
    from_user=request.user
)

# NEW:
create_notification(
    user=project.user,
    notification_type='project_like',
    title=f'{request.user.username} liked your project',
    message=f'"{project.title}" got a like',
    from_user=request.user,
    project=project  # ADD THIS
)
```

**Example 3: When connection request**
```python
# OLD:
create_notification(
    user=receiver,
    notification_type='connection_request',
    title=f'{request.user.username} wants to connect',
    message=f'Accept or reject the connection request',
    from_user=request.user,
    connection=connection
)

# NEW - Already has from_user, which is sufficient
# (Will redirect to from_user's profile automatically)
```

---

## 🎨 STEP 7: Enhanced Notification Display (Optional - 10 min)

**Add better styling** to `notifications.html` (replace the old notification-item styles):

```html
<style>
    .notification-item {
        background: white;
        border: 1px solid #e2e8f0;
        border-radius: 12px;
        padding: 16px;
        margin-bottom: 12px;
        transition: all 0.3s ease;
        cursor: pointer;
    }

    .notification-item:hover {
        box-shadow: 0 10px 25px rgba(37, 99, 235, 0.15);
        transform: translateY(-2px);
        border-color: #2563eb;
        background: #f0f9ff;
    }

    .notification-item.unread {
        background: linear-gradient(135deg, rgba(37, 99, 235, 0.05), rgba(59, 130, 246, 0.05));
        border-color: #2563eb;
        border-width: 2px;
    }

    .notification-item.unread:hover {
        background: linear-gradient(135deg, rgba(37, 99, 235, 0.1), rgba(59, 130, 246, 0.1));
    }

    .notification-icon {
        width: 48px;
        height: 48px;
        border-radius: 50%;
        display: flex;
        align-items: center;
        justify-content: center;
        font-size: 24px;
        flex-shrink: 0;
        background: linear-gradient(135deg, #dbeafe, #bfdbfe);
    }

    /* Pulse animation for unread indicator */
    @keyframes pulse {
        0%, 100% {
            opacity: 1;
        }
        50% {
            opacity: 0.5;
        }
    }

    .animate-pulse {
        animation: pulse 2s cubic-bezier(0.4, 0, 0.6, 1) infinite;
    }

    /* Arrow icon animation */
    a:hover .group-hover\:text-blue-600 {
        color: #2563eb !important;
    }
</style>
```

---

## ✅ Testing Checklist

- [ ] Create a test notification (manually in Django admin)
- [ ] Click the notification
- [ ] Verify it redirects to correct page
- [ ] Verify notification is marked as read
- [ ] Test each notification type:
  - [ ] Connection request → User profile
  - [ ] Message → Chat
  - [ ] Project like → Project details
  - [ ] Project comment → Project + scroll to comments
  - [ ] Team invitation → Project details
  - [ ] Follow → User profile
- [ ] Test on mobile
- [ ] Check for console errors

---

## 📊 Summary of Changes

| File | Changes | Time |
|------|---------|------|
| models.py | Add project + redirect_url fields, get_redirect_url() method | 15 min |
| views.py | Update create_notification(), add notification_click() | 20 min |
| urls.py | Add notification_click route | 5 min |
| notifications.html | Make notifications clickable, add styling | 20 min |
| views.py (all calls) | Add project parameter to notification creation | 15 min |
| **Total** | | **1.5 hours** |

---

## 🚀 Advanced: Add Mark All as Read (Optional - 10 min)

**File**: `accounts/views.py`

```python
@login_required
def mark_all_notifications_read(request):
    """Mark all notifications as read"""
    Notification.objects.filter(
        user=request.user,
        is_read=False
    ).update(
        is_read=True,
        read_at=timezone.now()
    )
    messages.success(request, 'All notifications marked as read')
    return redirect('notifications')
```

**Add to `urls.py`**:
```python
path('notifications/mark-all-read/', views.mark_all_notifications_read, name='mark_all_notifications_read'),
```

**Add button to template** (before `</main>`):
```html
{% if notifications %}
    <div class="mt-8 text-center">
        <a href="{% url 'mark_all_notifications_read' %}" 
           class="inline-block px-6 py-2 text-sm font-medium text-blue-600 hover:text-blue-700 
                  hover:bg-blue-50 rounded-lg transition">
            ✓ Mark all as read
        </a>
    </div>
{% endif %}
```

---

## 🎁 Bonus: Real-time Notification Popup

**Optional**: Add JavaScript to show a toast notification when new notification arrives (WebSocket):

```javascript
// In notifications.html, before </body>:
<script>
    // Listen for new notifications (if WebSocket is configured)
    const ws = new WebSocket('ws://localhost:8000/ws/notifications/');
    
    ws.onmessage = function(e) {
        const data = JSON.parse(e.data);
        if (data.type === 'notification_message') {
            showNotificationToast(data.notification);
            // Optionally reload the page to show new notification
            // location.reload();
        }
    };
    
    function showNotificationToast(notification) {
        const toast = document.createElement('div');
        toast.className = 'fixed top-4 right-4 bg-blue-600 text-white px-6 py-3 rounded-lg shadow-lg z-50 animate-bounce';
        toast.textContent = `🔔 ${notification.title}`;
        document.body.appendChild(toast);
        
        setTimeout(() => toast.remove(), 5000);
    }
</script>
```

---

## 📁 Files Modified Summary

```
✓ accounts/models.py           - Add fields + get_redirect_url() method
✓ accounts/views.py            - Update create_notification(), add notification_click()
✓ accounts/urls.py             - Add notification_click route
✓ templates/notifications.html - Make notifications clickable
✓ views.py (all calls)         - Update notification creation calls
```

---

## 🎉 Result

✅ Clicking a notification redirects to relevant content  
✅ Notifications are marked as read automatically  
✅ Better UX with visual feedback  
✅ Works for all notification types  
✅ Mobile responsive  
✅ Easy to extend for more notification types  

Total implementation time: **1.5 hours**  
Impact: **Huge** - Users can act directly from notifications!

