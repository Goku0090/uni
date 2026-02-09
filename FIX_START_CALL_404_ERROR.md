# Fix for Start Call 404 Error

## Problem
When clicking the video/voice call button, getting:
```
POST http://127.0.0.1:8000/start-call/1/ 404 (Not Found)
Error starting call: SyntaxError: Unexpected token '<'
```

## Root Causes

1. **ChatRoom doesn't exist**: The code references `chat_room.id` in template, but no ChatRoom with that ID exists
2. **User not a member**: Even if the room exists, user might not be a ChatRoomMember
3. **Direct message context**: When using direct messages, there might not be a ChatRoom at all
4. **Template context issue**: `{{ chat_room.id }}` might be undefined, sending `1` as fallback

## Solution

### Step 1: Check Current Setup

First, verify what templates are being used:

```bash
# Check which template is active
python manage.py shell
>>> from accounts.models import ChatRoom
>>> ChatRoom.objects.all()  # Should show existing rooms
```

### Step 2: Fix the View to Handle Missing Rooms

**File**: `auth_project/accounts/views.py`

Update the `start_call` view (around line 1313):

```python
@login_required
def start_call(request, room_id):
    """Start a voice/video call in a chat room"""
    
    # Try to get ChatRoom, but also allow direct messages
    try:
        chat_room = ChatRoom.objects.get(id=room_id)
    except ChatRoom.DoesNotExist:
        # For direct messages, create a temporary room or return error
        return JsonResponse({
            'error': 'Chat room not found. Please start from an active conversation.',
            'code': 'ROOM_NOT_FOUND'
        }, status=404)
    
    # Check membership
    if not ChatRoomMember.objects.filter(
        chat_room=chat_room,
        user=request.user,
        is_active=True
    ).exists():
        return JsonResponse({
            'error': 'You are not a member of this chat room',
            'code': 'NOT_MEMBER'
        }, status=403)
    
    # Validate call type
    call_type = request.POST.get('call_type', 'voice')
    if call_type not in ['voice', 'video']:
        return JsonResponse({
            'error': 'Invalid call type. Must be "voice" or "video"',
            'code': 'INVALID_CALL_TYPE'
        }, status=400)
    
    # Create call message
    message = Message.objects.create(
        chat_room=chat_room,
        sender=request.user,
        content=f"📞 Started a {call_type} call",
        message_type='call',
        call_type=call_type
    )
    
    # Notify other members
    for member in chat_room.members.filter(is_active=True).exclude(user=request.user):
        create_notification(
            user=member.user,
            notification_type='message',
            title=f'{call_type.title()} call in {chat_room.display_name}',
            message=f'{request.user.username} started a {call_type} call',
            from_user=request.user,
            message_obj=message
        )
    
    return JsonResponse({
        'success': True,
        'call_id': message.id,
        'call_type': call_type,
        'room_id': chat_room.id,
        'message': 'Call started successfully'
    })
```

### Step 3: Fix JavaScript Error Handling

**File**: `auth_project/accounts/templates/features/enhanced_chat.html`

Update the `startCall` function (around line 1083):

```javascript
async function startCall(callType) {
    try {
        // Get room ID from template variable
        const roomId = '{{ chat_room.id }}';
        
        // Validate room ID exists
        if (!roomId || roomId === '' || roomId === 'None') {
            showErrorNotification('Chat room not found. Please select a conversation first.');
            console.error('Invalid room ID:', roomId);
            return;
        }
        
        console.log('Starting call:', { callType, roomId });
        
        const response = await fetch(`/start-call/${roomId}/`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/x-www-form-urlencoded',
                'X-CSRFToken': document.querySelector('[name=csrfmiddlewaretoken]').value
            },
            body: `call_type=${callType}`
        });
        
        // Check if response is OK before parsing JSON
        if (!response.ok) {
            const contentType = response.headers.get('content-type');
            
            if (contentType && contentType.includes('application/json')) {
                const data = await response.json();
                showErrorNotification(`Call failed: ${data.error || 'Unknown error'}`);
            } else {
                // Got HTML error page (404, 500, etc.)
                showErrorNotification(`Server error (${response.status}): ${response.statusText}`);
                console.error('Server returned HTML:', await response.text());
            }
            return;
        }
        
        const data = await response.json();
        
        if (data.success) {
            // Show call interface
            showCallInterface(callType, data.call_id);
            
            // Here you would integrate with WebRTC for actual calling
            showSuccessNotification(
                `${callType.charAt(0).toUpperCase() + callType.slice(1)} call started!`
            );
            
            // Broadcast call to other members via WebSocket
            if (window.chatSocket && window.chatSocket.readyState === WebSocket.OPEN) {
                window.chatSocket.send(JSON.stringify({
                    'type': 'call_started',
                    'call_type': callType,
                    'call_id': data.call_id,
                    'started_by': '{{ request.user.username }}'
                }));
            }
        } else {
            showErrorNotification(data.error || `Failed to start ${callType} call`);
        }
    } catch (error) {
        console.error('Error starting call:', error);
        showErrorNotification(`Error: ${error.message}`);
    }
}
```

### Step 4: Ensure ChatRoom Exists in Template Context

**File**: `auth_project/accounts/views.py`

Check the `enhanced_chat_view` function and ensure it passes `chat_room`:

```python
@login_required
def enhanced_chat_view(request, room_id):
    """Enhanced chat room view"""
    try:
        chat_room = get_object_or_404(ChatRoom, id=room_id)
        
        # Verify user is a member
        if not ChatRoomMember.objects.filter(
            chat_room=chat_room,
            user=request.user,
            is_active=True
        ).exists():
            return redirect('enhanced_messages')
        
        # Get messages for this room
        messages = Message.objects.filter(
            chat_room=chat_room
        ).select_related('sender').order_by('created_at')[:50]
        
        # Get room members
        members = chat_room.members.filter(is_active=True)
        
        context = {
            'chat_room': chat_room,  # IMPORTANT: Pass the room
            'messages': messages,
            'members': members,
            'room_id': room_id  # Also pass as separate variable
        }
        
        return render(request, 'features/enhanced_chat.html', context)
    
    except Exception as e:
        logger.error(f"Error in enhanced_chat_view: {str(e)}", exc_info=True)
        messages.error(request, "Failed to load chat room")
        return redirect('enhanced_messages')
```

### Step 5: Alternative Fix for Direct Messages

If you want to support calls in direct messages too, modify the view:

```python
@login_required
def start_call(request, room_id):
    """Start a voice/video call in a chat room or direct message"""
    
    # Try ChatRoom first
    chat_room = None
    try:
        chat_room = ChatRoom.objects.get(id=room_id)
        is_group_chat = True
    except ChatRoom.DoesNotExist:
        # Could be a direct message context
        # For now, return error
        is_group_chat = False
        return JsonResponse({
            'error': 'Chat room not found. Direct message calls coming soon.',
            'code': 'ROOM_NOT_FOUND'
        }, status=404)
    
    # Rest of the code...
```

### Step 6: Test the Fix

1. **Verify ChatRoom exists**:
   ```bash
   python manage.py shell
   >>> from accounts.models import ChatRoom, ChatRoomMember
   >>> room = ChatRoom.objects.first()
   >>> print(f"Room ID: {room.id}, Members: {room.members.count()}")
   ```

2. **Check browser console**:
   - Look for the room ID being sent
   - Verify CSRF token is present
   - Check Network tab for response

3. **Test the call**:
   - Navigate to a group chat
   - Click video call button
   - Should see success notification

## Quick Debug Checklist

- [ ] ChatRoom exists in database (`ChatRoom.objects.all()`)
- [ ] User is a ChatRoomMember
- [ ] Template has `{{ chat_room.id }}` defined
- [ ] CSRF token is in the form
- [ ] JavaScript is getting correct room ID
- [ ] Endpoint URL matches URL pattern in urls.py
- [ ] View function handles the request

## Files to Modify

1. `accounts/views.py` - Update `start_call()` view with better error handling
2. `accounts/templates/features/enhanced_chat.html` - Update JS with error handling
3. Test by creating a ChatRoom and calling the endpoint

## Expected Success Response

```json
{
    "success": true,
    "call_id": 123,
    "call_type": "video",
    "room_id": 1,
    "message": "Call started successfully"
}
```

## Error Responses

**Room not found (404)**:
```json
{
    "error": "Chat room not found. Please start from an active conversation.",
    "code": "ROOM_NOT_FOUND"
}
```

**Not a member (403)**:
```json
{
    "error": "You are not a member of this chat room",
    "code": "NOT_MEMBER"
}
```

**Invalid call type (400)**:
```json
{
    "error": "Invalid call type. Must be \"voice\" or \"video\"",
    "code": "INVALID_CALL_TYPE"
}
```
