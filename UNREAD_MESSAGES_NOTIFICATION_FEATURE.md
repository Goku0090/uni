# Unread Messages Notification Feature Implementation

**Feature**: Display unread message count in navigation bar  
**Status**: Implementation Guide (Ready to implement)  
**Date**: January 29, 2026

---

## 📋 Feature Overview

When a user messages another person, the recipient should see:
1. **Unread message badge** in the navbar on the Messages link
2. **Unread count** (e.g., "5") displayed prominently
3. **Visual indicator** - Badge changes color/style
4. **Real-time update** - Count updates when messages arrive

---

## 🎯 Implementation Steps

### Step 1: Update main_home view (accounts/views.py line 742)

**Add unread message count to context:**

```python
@login_required
def main_home(request):
    """Simplified main home view for testing"""
    # Count unread messages for current user
    unread_count = Message.objects.filter(
        receiver=request.user
    ).exclude(
        read_statuses__user=request.user
    ).count()
    
    return render(request, 'main_home.html', {
        'feed_posts': [],
        'categories': ['Web Development', 'Mobile Apps', 'AI/ML', 'Data Science'],
        'available_techs': ['Python', 'JavaScript', 'React', 'Django', 'Node.js'],
        'homepage_stats': {
            'total_projects': 1250,
            'active_users': 890,
            'total_connections': 2100,
            'success_stories': 45
        },
        'active_filters': {},
        'has_filters': False,
        'unread_message_count': unread_count,  # ← ADD THIS
    })
```

### Step 2: Update navbar in main_home.html (line 68-73)

**Add badge to Messages link:**

**Current Code:**
```html
<a href="{% url 'messages' %}" class="hover:text-accent transition flex items-center gap-2" title="Inbox - Chat with Collaborators & Teams">
    <svg class="w-5 h-5" fill="currentColor" viewBox="0 0 20 20">
        <path fill-rule="evenodd" d="M18 10c0 3.866-3.582 7-8 7a8.841 8.841 0 01-4.083-.98L2 17l1.338-3.123C2.493 12.767 2 11.434 2 10c0-3.866 3.582-7 8-7s8 3.134 8 7zM7 9H5v2h2V9zm8 0h-2v2h2V9zM9 9h2v2H9V9z" clip-rule="evenodd"/>
    </svg>
    <span class="text-xs font-medium">Messages</span>
</a>
```

**Updated Code:**
```html
<a href="{% url 'messages' %}" class="hover:text-accent transition flex items-center gap-2 relative" title="Inbox - Chat with Collaborators & Teams">
    <svg class="w-5 h-5" fill="currentColor" viewBox="0 0 20 20">
        <path fill-rule="evenodd" d="M18 10c0 3.866-3.582 7-8 7a8.841 8.841 0 01-4.083-.98L2 17l1.338-3.123C2.493 12.767 2 11.434 2 10c0-3.866 3.582-7 8-7s8 3.134 8 7zM7 9H5v2h2V9zm8 0h-2v2h2V9zM9 9h2v2H9V9z" clip-rule="evenodd"/>
    </svg>
    <span class="text-xs font-medium">Messages</span>
    <!-- Unread badge -->
    {% if unread_message_count > 0 %}
    <span class="absolute -top-2 -right-2 bg-red-500 text-white text-xs font-bold rounded-full w-5 h-5 flex items-center justify-center animate-pulse">
        {% if unread_message_count > 99 %}
            99+
        {% else %}
            {{ unread_message_count }}
        {% endif %}
    </span>
    {% endif %}
</a>
```

### Step 3: Add similar logic to other views

Update these views to pass unread_count to their templates:
- `student_profile` (line ~2480)
- `find_collaborators` (line ~1365)
- `my_connections` (line ~1105)
- `post_project` (line ~1576)
- `notifications_view` (line ~1266)
- Any other view with navbar

---

## 💻 Code Implementation (Ready to Copy)

### In accounts/views.py

Add this helper function at the top (after imports):

```python
def get_unread_message_count(user):
    """Get count of unread messages for a user"""
    if not user.is_authenticated:
        return 0
    
    from accounts.models import Message, MessageReadStatus
    return Message.objects.filter(
        receiver=user
    ).exclude(
        read_statuses__user=user
    ).count()
```

Then update main_home view:

```python
@login_required
def main_home(request):
    """Simplified main home view for testing"""
    return render(request, 'main_home.html', {
        'feed_posts': [],
        'categories': ['Web Development', 'Mobile Apps', 'AI/ML', 'Data Science'],
        'available_techs': ['Python', 'JavaScript', 'React', 'Django', 'Node.js'],
        'homepage_stats': {
            'total_projects': 1250,
            'active_users': 890,
            'total_connections': 2100,
            'success_stories': 45
        },
        'active_filters': {},
        'has_filters': False,
        'unread_message_count': get_unread_message_count(request.user),
    })
```

---

## 🎨 HTML/CSS Badge Styles

### Option 1: Animated Pulse (Red Badge)
```html
{% if unread_message_count > 0 %}
<span class="absolute -top-2 -right-2 bg-red-500 text-white text-xs font-bold rounded-full w-5 h-5 flex items-center justify-center animate-pulse">
    {{ unread_message_count > 99 ? '99+' : unread_message_count }}
</span>
{% endif %}
```

**Styles**:
- Position: Absolute (top-right of icon)
- Color: Red (indicates unread)
- Animation: Pulse (draws attention)
- Size: Small (5x5 with icon numbers)

### Option 2: Static Blue Badge
```html
{% if unread_message_count > 0 %}
<span class="absolute -top-1 -right-1 bg-blue-500 text-white text-xs font-semibold rounded-full px-1.5 py-0.5">
    {{ unread_message_count }}
</span>
{% endif %}
```

### Option 3: Notification Dot
```html
{% if unread_message_count > 0 %}
<span class="absolute top-0 right-0 w-2 h-2 bg-red-500 rounded-full animate-pulse"></span>
{% endif %}
```

---

## 🔄 Add to Base Template (Optional but Recommended)

If you have a base template that all pages extend, add the unread count there:

```html
<!-- In base.html or header.html -->
<nav class="bg-primary shadow-lg sticky top-0 z-50">
    <!-- ... navbar content ... -->
    {% if request.user.is_authenticated %}
    <script>
        // Store unread count for JavaScript use
        window.unreadMessageCount = {{ unread_message_count }};
    </script>
    {% endif %}
</nav>
```

---

## 🔄 Real-time Update with WebSocket (Advanced)

### Add JavaScript for WebSocket updates:

```javascript
// In main_home.html or JavaScript file
<script>
document.addEventListener('DOMContentLoaded', function() {
    const userId = {{ user.id }};
    const protocol = window.location.protocol === 'https:' ? 'wss:' : 'ws:';
    const ws = new WebSocket(
        protocol + '//' + window.location.host + '/ws/notifications/' + userId + '/'
    );

    ws.onmessage = function(event) {
        const data = JSON.parse(event.data);
        if (data.type === 'new_message') {
            // Update unread count in navbar
            updateUnreadCount(data.unread_count);
        }
    };

    function updateUnreadCount(count) {
        const badge = document.querySelector('[data-unread-badge]');
        if (badge) {
            if (count > 0) {
                badge.textContent = count > 99 ? '99+' : count;
                badge.style.display = 'flex';
            } else {
                badge.style.display = 'none';
            }
        }
    }
});
</script>
```

---

## 📊 Database Query Optimization

### Current Query (Simple)
```python
Message.objects.filter(receiver=user).exclude(
    read_statuses__user=user
).count()
```

**Execution Time**: O(n) - Counts all unread messages  
**Use Case**: Good for small-medium apps

### Optimized Query (With Caching)
```python
from django.core.cache import cache

def get_unread_message_count(user):
    cache_key = f'unread_messages_{user.id}'
    count = cache.get(cache_key)
    
    if count is None:
        count = Message.objects.filter(
            receiver=user
        ).exclude(
            read_statuses__user=user
        ).count()
        # Cache for 5 minutes
        cache.set(cache_key, count, 300)
    
    return count

# Invalidate cache when message is sent
def send_message(sender, receiver, content):
    message = Message.objects.create(
        sender=sender,
        receiver=receiver,
        content=content
    )
    # Clear receiver's cache
    cache.delete(f'unread_messages_{receiver.id}')
    return message
```

---

## 🛠️ Implementation Checklist

- [ ] Add helper function `get_unread_message_count()`
- [ ] Update `main_home` view to include unread_count
- [ ] Update `main_home.html` navbar Messages link with badge
- [ ] Test in browser - unread count displays
- [ ] Send test message - badge appears
- [ ] Mark message as read - badge disappears
- [ ] Update other views with navbar (profile, collaborators, etc.)
- [ ] Test across all pages with navbar
- [ ] Add caching for performance (optional)
- [ ] Add WebSocket real-time updates (optional/advanced)

---

## 📱 Mobile Responsive

Ensure badge works on mobile:

```html
<a href="{% url 'messages' %}" class="hover:text-accent transition flex items-center gap-1 sm:gap-2 relative" title="Inbox">
    <svg class="w-4 sm:w-5 h-4 sm:h-5" fill="currentColor" viewBox="0 0 20 20">
        <!-- SVG path -->
    </svg>
    <span class="text-xs font-medium hidden sm:inline">Messages</span>
    
    <!-- Badge -->
    {% if unread_message_count > 0 %}
    <span class="absolute -top-2 -right-2 bg-red-500 text-white text-xs font-bold rounded-full w-4 h-4 sm:w-5 sm:h-5 flex items-center justify-center animate-pulse text-xs">
        {% if unread_message_count > 99 %}99+{% else %}{{ unread_message_count }}{% endif %}
    </span>
    {% endif %}
</a>
```

---

## 🔒 Security Considerations

- ✅ Only show unread count for authenticated users
- ✅ Use `@login_required` decorator on views
- ✅ Count only messages where `receiver=current_user`
- ✅ Use `.exclude(read_statuses__user=user)` to be accurate
- ✅ Cache is per-user, not global

---

## 🎯 User Experience Flow

1. **User A sends message to User B**
   - User B receives message
   - Badge appears on Messages link showing "1"

2. **User B receives 5 messages**
   - Badge updates to show "5"
   - Badge pulses red to draw attention

3. **User B clicks Messages**
   - Messages load
   - Messages marked as read
   - Badge disappears (count becomes 0)

4. **User B navigates away**
   - Badge still visible if more unread messages
   - Navigation bar remains consistent

---

## 📝 Alternative Notification Approaches

### Approach 1: Toast Notification (Recommended for UX)
```javascript
// When new message arrives
function showMessageNotification(senderName) {
    const toast = document.createElement('div');
    toast.innerHTML = `New message from ${senderName}`;
    toast.className = 'fixed top-20 right-4 bg-green-500 text-white px-4 py-2 rounded-lg animate-slide-in';
    document.body.appendChild(toast);
    
    setTimeout(() => toast.remove(), 5000);
}
```

### Approach 2: Browser Notification
```javascript
// Request permission
Notification.requestPermission();

// Send notification
new Notification('New Message', {
    body: `From ${senderName}`,
    tag: 'new-message'
});
```

### Approach 3: Page Title Change
```javascript
// Change browser tab title to show unread count
if (unreadCount > 0) {
    document.title = `(${unreadCount}) UniSync - Home`;
} else {
    document.title = 'UniSync - Home';
}
```

---

## 🚀 Future Enhancements

1. **Unread Messages per User**: Show unread count per conversation
2. **Message Preview**: Hover over badge to see last message
3. **Quick Reply**: Click badge to open last conversation
4. **Sound Alert**: Play notification sound
5. **Desktop Notifications**: Browser push notifications
6. **Analytics**: Track message patterns

---

## 📚 Related Code References

### Message Model
- File: `accounts/models.py` (Line 149)
- Fields: sender, receiver, content, created_at
- Method: `mark_as_read_by(user)`

### MessageReadStatus Model
- File: `accounts/models.py` (Line 275)
- Tracks: Which user read which message
- Query: `exclude(read_statuses__user=user)`

### Current Views
- `main_home`: Line 742
- `messages`: Line ~850
- `chat_view`: Line ~1930

---

## 💡 Tips & Tricks

### Query Tips
```python
# Get unread message count
unread = Message.objects.filter(receiver=user).exclude(read_statuses__user=user).count()

# Get unread conversations count (unique senders)
unread_convos = Message.objects.filter(receiver=user).exclude(
    read_statuses__user=user
).values('sender').distinct().count()

# Get latest unread message
latest_unread = Message.objects.filter(receiver=user).exclude(
    read_statuses__user=user
).order_by('-created_at').first()
```

### Styling Tips
- Use `animate-pulse` for attention
- Position badge with `absolute -top-2 -right-2`
- Use red for unread, green for action
- Keep badge size small (w-5 h-5)

### Performance Tips
- Cache for 5-10 minutes
- Invalidate cache on message send
- Use select_related for joins
- Avoid N+1 queries

---

## 🧪 Testing

### Manual Test Cases
1. Send message between two users
2. Check recipient sees badge
3. Click Messages link
4. Badge should disappear
5. Send multiple messages
6. Badge should update count
7. Refresh page
8. Badge should still be there

### Automated Tests
```python
def test_unread_message_count(self):
    user = User.objects.create_user('test', 'test@test.com', 'pass')
    sender = User.objects.create_user('sender', 'sender@test.com', 'pass')
    
    Message.objects.create(sender=sender, receiver=user, content='Hi')
    
    count = get_unread_message_count(user)
    self.assertEqual(count, 1)
    
    # Mark as read
    message = Message.objects.first()
    message.mark_as_read_by(user)
    
    count = get_unread_message_count(user)
    self.assertEqual(count, 0)
```

---

## 📖 Summary

This implementation will:
✅ Show unread message count in navbar  
✅ Update dynamically  
✅ Display badge with count  
✅ Improve user experience  
✅ Work across all pages  
✅ Scale with caching (optional)  

**Ready to implement!** Follow the steps above to add this feature.

---

For code examples and more implementation details, see the code sections above.

**Questions?** Refer to Django documentation on:
- QuerySet exclude(): https://docs.djangoproject.com/en/4.2/ref/models/querysets/#exclude
- Caching: https://docs.djangoproject.com/en/4.2/topics/cache/
- Template tags: https://docs.djangoproject.com/en/4.2/ref/templates/builtins/
