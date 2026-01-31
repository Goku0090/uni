# Quick Implementation - Unread Messages Notification

**Time to implement**: 15-20 minutes  
**Difficulty**: Easy  
**No database changes needed**

---

## Step 1: Update views.py (1 minute)

Add this function after the imports in `accounts/views.py`:

```python
def get_unread_message_count(user):
    """Get count of unread messages for a user"""
    if not user.is_authenticated:
        return 0
    
    from accounts.models import Message
    return Message.objects.filter(
        receiver=user
    ).exclude(
        read_statuses__user=user
    ).count()
```

---

## Step 2: Update main_home view (1 minute)

Find this in `accounts/views.py` line 742:

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
        'unread_message_count': get_unread_message_count(request.user),  # ← ADD THIS LINE
    })
```

---

## Step 3: Update HTML template (5 minutes)

Open `accounts/templates/main_home.html` line 68-73.

**Find this:**
```html
<a href="{% url 'messages' %}" class="hover:text-accent transition flex items-center gap-2" title="Inbox - Chat with Collaborators & Teams">
    <svg class="w-5 h-5" fill="currentColor" viewBox="0 0 20 20">
        <path fill-rule="evenodd" d="M18 10c0 3.866-3.582 7-8 7a8.841 8.841 0 01-4.083-.98L2 17l1.338-3.123C2.493 12.767 2 11.434 2 10c0-3.866 3.582-7 8-7s8 3.134 8 7zM7 9H5v2h2V9zm8 0h-2v2h2V9zM9 9h2v2H9V9z" clip-rule="evenodd"/>
    </svg>
    <span class="text-xs font-medium">Messages</span>
</a>
```

**Replace with:**
```html
<a href="{% url 'messages' %}" class="hover:text-accent transition flex items-center gap-2 relative" title="Inbox - Chat with Collaborators & Teams">
    <svg class="w-5 h-5" fill="currentColor" viewBox="0 0 20 20">
        <path fill-rule="evenodd" d="M18 10c0 3.866-3.582 7-8 7a8.841 8.841 0 01-4.083-.98L2 17l1.338-3.123C2.493 12.767 2 11.434 2 10c0-3.866 3.582-7 8-7s8 3.134 8 7zM7 9H5v2h2V9zm8 0h-2v2h2V9zM9 9h2v2H9V9z" clip-rule="evenodd"/>
    </svg>
    <span class="text-xs font-medium">Messages</span>
    {% if unread_message_count > 0 %}
    <span class="absolute -top-2 -right-2 bg-red-500 text-white text-xs font-bold rounded-full w-5 h-5 flex items-center justify-center animate-pulse">
        {% if unread_message_count > 99 %}99+{% else %}{{ unread_message_count }}{% endif %}
    </span>
    {% endif %}
</a>
```

---

## Step 4: Restart and Test (1 minute)

```bash
# Restart Django
python manage.py runserver

# Test:
# 1. Log in as User A
# 2. Open new browser tab, log in as User B
# 3. User B goes to /chat/
# 4. User A sends a message to User B
# 5. User B's navbar should show badge with "1"
# 6. User B clicks Messages
# 7. Badge disappears (message marked as read)
```

---

## Step 5: (Optional) Update Other Views

Repeat Step 2 and 3 for these views to have consistent navbar:

- **student_profile** (line ~2480)
- **find_collaborators** (line ~1365)
- **my_connections** (line ~1105)
- **post_project** (line ~1576)
- **notifications_view** (line ~1266)
- **chat_view** (line ~1930)
- **message_view** (line ~850)

Each one needs:
1. Add `'unread_message_count': get_unread_message_count(request.user),` to context
2. Add the HTML badge to their navbar if they have one

---

## Visual Result

**Before**: Messages link just shows icon and text
```
🗨️ Messages
```

**After**: Messages link shows icon, text, AND red badge with count
```
🗨️ Messages [5]  ← Red pulsing badge showing 5 unread messages
```

---

## Colors & Styling Options

### Red Pulsing (Recommended - Default)
```html
<span class="absolute -top-2 -right-2 bg-red-500 text-white text-xs font-bold rounded-full w-5 h-5 flex items-center justify-center animate-pulse">
```

### Blue Static
```html
<span class="absolute -top-2 -right-2 bg-blue-500 text-white text-xs font-bold rounded-full w-5 h-5 flex items-center justify-center">
```

### Green with Bell Icon
```html
<span class="absolute -top-2 -right-2 bg-green-500 text-white text-xs font-bold rounded-full w-5 h-5 flex items-center justify-center">
    🔔
</span>
```

---

## Troubleshooting

### Badge not showing?
1. Check unread_message_count is passed to template
2. Check you're logged in (badge only shows for auth users)
3. Check message is sent to you (receiver must be current user)
4. Restart Django server

### Badge shows but count wrong?
1. Check if message is actually unread
2. Go to `/admin/` → MessageReadStatus
3. Verify no read_statuses entry for your message
4. Try refreshing page

### Badge stays even after reading?
1. Check the `mark_as_read_by()` method is called
2. Check MessageReadStatus is created in database
3. Try clearing browser cache
4. Restart Django

---

## Performance Optimization (Optional)

Add caching to avoid querying every page load:

```python
from django.core.cache import cache

def get_unread_message_count(user):
    """Get count of unread messages for a user (with caching)"""
    if not user.is_authenticated:
        return 0
    
    cache_key = f'unread_messages_{user.id}'
    count = cache.get(cache_key)
    
    if count is None:
        from accounts.models import Message
        count = Message.objects.filter(
            receiver=user
        ).exclude(
            read_statuses__user=user
        ).count()
        cache.set(cache_key, count, 300)  # Cache 5 minutes
    
    return count
```

Then update where messages are sent to clear cache:

```python
# In send_message function
cache.delete(f'unread_messages_{receiver.id}')
```

---

## Done! 🎉

Your navbar now shows unread message count!

**Next level enhancements** (optional):
- Add WebSocket for real-time updates
- Add sound notification
- Add browser notification
- Add per-conversation unread counts
- Add message preview on hover

See `UNREAD_MESSAGES_NOTIFICATION_FEATURE.md` for advanced options.
