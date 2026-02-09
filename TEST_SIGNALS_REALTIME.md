# Testing Guide: signals_realtime.py Fixes

## Test Environment Setup

### Prerequisites
```bash
cd e:\login\auth_project
python manage.py migrate  # Ensure DB is up to date
python manage.py shell
```

---

## Test 1: Project Creation Signal ✅

### What Gets Tested
- Project model creation triggers signal
- Signal handler uses correct `instance.user` field
- Activity record created

### Steps
```bash
1. Open Django shell:
   python manage.py shell

2. Create test user:
   from django.contrib.auth.models import User
   user = User.objects.create_user(username='testuser', password='pass123')
   
3. Create project:
   from accounts.models import Project
   project = Project.objects.create(
       user=user,
       title="Test Project",
       description="Test Description"
   )
   
4. Verify success:
   print(f"Project created: {project.id}")
   print(f"Project user: {project.user.username}")
```

### Expected Result
```
✅ Project created successfully
✅ No AttributeError
✅ Signal handler executed
✅ Activity created
```

### What We're Testing
- **Line 22-35**: `project_status_changed` signal
- **Issue Fixed**: Project creation works without error

---

## Test 2: Team Member Addition Signal ✅

### What Gets Tested
- ProjectMember uses correct `instance.user` field (NOT `instance.member`)
- Team member addition signal triggers
- Activity created for member

### Steps
```bash
1. Using same shell from Test 1:

2. Create ProjectMember:
   from accounts.models import ProjectMember
   member = ProjectMember.objects.create(
       project=project,
       user=user,
       role='contributor'
   )
   
3. Verify:
   print(f"Member created: {member.id}")
   print(f"Member user: {member.user.username}")
   
4. Check activity:
   from accounts.models import Activity
   activities = Activity.objects.filter(activity_type='member.added')
   print(f"Activities created: {activities.count()}")
```

### Expected Result
```
✅ ProjectMember created successfully
✅ Activity created with activity_type='member.added'
✅ No AttributeError on instance.member
```

### What We're Testing
- **Line 65**: Changed `instance.member` → `instance.user`
- **Line 58-96**: `team_member_added` signal
- **Issue Fixed**: Uses correct ProjectMember field

---

## Test 3: Connection Creation Signal ✅

### What Gets Tested
- Connection signal uses correct `receiver` and `sender` fields (NOT `to_user`/`from_user`)
- Notification created for receiver
- Correct notification_type set

### Steps
```bash
1. Create second test user:
   user2 = User.objects.create_user(username='testuser2', password='pass123')
   
2. Create Connection:
   from accounts.models import Connection
   connection = Connection.objects.create(
       sender=user,
       receiver=user2,
       status='pending'
   )
   
3. Verify:
   print(f"Connection created: {connection.id}")
   print(f"Sender: {connection.sender.username}")
   print(f"Receiver: {connection.receiver.username}")
   
4. Check notification:
   from accounts.models import Notification
   notif = Notification.objects.get(user=user2)
   print(f"Notification type: {notif.notification_type}")
   print(f"Notification title: {notif.title}")
   print(f"Notification message: {notif.message}")
```

### Expected Result
```
✅ Connection created successfully
✅ Notification created with notification_type='connection_request'
✅ Notification has title and message
✅ Receiver is user2
✅ No errors referencing to_user/from_user
```

### What We're Testing
- **Line 176**: Changed `instance.to_user` → `instance.receiver`
- **Line 178**: Changed `instance.from_user` → `instance.sender`
- **Line 180**: Changed field reference
- **Line 167-181**: `connection_created` signal
- **Issue Fixed**: Uses correct Connection fields

---

## Test 4: Activity Broadcast Function ✅

### What Gets Tested
- `broadcast_activity_feed()` uses correct Connection query
- Query filters on `receiver` and `status='accepted'`
- Uses `sender_id` in values_list

### Steps
```bash
1. Accept connection to create accepted status:
   connection.status = 'accepted'
   connection.save()
   
2. Trigger activity broadcast (by creating comment):
   from accounts.models import Comment
   comment = Comment.objects.create(
       user=user2,
       project=project,
       content="Great project!"
   )
   
3. Verify no errors in logs:
   # Check console for "Error broadcasting activity" messages
   # Should see no errors
   
4. Verify followers query would work:
   from accounts.models import Connection
   followers = Connection.objects.filter(
       receiver=user2,
       status='accepted'
   ).values_list('sender_id', flat=True)
   print(f"Followers: {list(followers)}")
```

### Expected Result
```
✅ Comment created successfully
✅ Activity broadcast executes without error
✅ No FieldError on query filters
✅ Followers list populated correctly
```

### What We're Testing
- **Lines 193-196**: Changed query filters to `receiver`, `status='accepted'`, `sender_id`
- **Line 184-213**: `broadcast_activity_feed()` function
- **Issue Fixed**: Query uses correct Connection field names

---

## Test 5: Notification Creation ✅

### What Gets Tested
- Notification objects use `notification_type` (NOT `type`)
- Notification objects include `title` field
- All required fields populated

### Steps
```bash
1. Query all notifications:
   from accounts.models import Notification
   notifications = Notification.objects.all()
   
2. Verify field names:
   for notif in notifications:
       print(f"Type: {notif.notification_type}")
       print(f"Title: {notif.title}")
       print(f"Message: {notif.message}")
       print(f"User: {notif.user.username}")
       print("---")
   
3. Verify all have required fields:
   assert all(n.notification_type for n in notifications), "Missing type"
   assert all(n.title for n in notifications), "Missing title"
   assert all(n.message for n in notifications), "Missing message"
```

### Expected Result
```
✅ All notifications have notification_type
✅ All notifications have title
✅ All notifications have message
✅ No errors about unknown fields
```

### What We're Testing
- **Line 225**: Changed `type=` → `notification_type=`
- **Line 226**: Added `title=title`
- **Line 216-245**: `notify_user()` function
- **Issue Fixed**: Uses correct Notification field names

---

## Test 6: Web Request Test (Post Project) ✅

### What Gets Tested
- HTTP POST to `/post-project/` endpoint works
- No AttributeError occurs
- Project created successfully

### Steps
```bash
1. Start Django development server:
   python manage.py runserver
   
2. In browser or with curl:
   POST http://localhost:8000/post-project/
   
   Form data:
   - title: "Web Development Project"
   - description: "Building a Django REST API"
   - technologies: ["Python", "Django", "PostgreSQL"]
   - looking_for: ["Backend Developer", "DevOps Engineer"]
   
3. Check response:
   - Should redirect to /post-project/ with success message
   - No 500 Internal Server Error
   - No AttributeError in console
```

### Expected Result
```
✅ HTTP 302 (redirect) or 200 (success page)
✅ Project appears in list
✅ No error traceback
✅ No AttributeError mentioned
```

### What We're Testing
- Real-world HTTP request handling
- All signal handlers triggered correctly
- End-to-end project creation flow

---

## Test 7: Django System Check ✅

### What Gets Tested
- Django configuration is valid
- All models are properly defined
- Signal handlers registered successfully

### Steps
```bash
python manage.py check
```

### Expected Result
```
✅ System check identifies 0 errors
✅ [SUCCESS] Database: PostgreSQL via Render
✅ [SUCCESS] Email Backend: Brevo
✅ [SUCCESS] Real-time signal handlers registered successfully
```

---

## Test Checklist

### Unit Tests
- [ ] Test 1: Project creation signal passes
- [ ] Test 2: Team member addition signal passes
- [ ] Test 3: Connection creation signal passes
- [ ] Test 4: Activity broadcast function passes
- [ ] Test 5: Notification creation passes
- [ ] Test 6: Web request test passes
- [ ] Test 7: Django system check passes

### Integration Tests
- [ ] Create project via web interface
- [ ] Send connection request via web interface
- [ ] Accept connection
- [ ] Add team member to project
- [ ] Post comment on project
- [ ] Check notifications were created
- [ ] Verify WebSocket broadcasts (if applicable)

### Database Tests
- [ ] Verify Project records created
- [ ] Verify ProjectMember records created
- [ ] Verify Connection records created
- [ ] Verify Notification records created
- [ ] Verify Activity records created

---

## Troubleshooting

### If You Get: "No module named accounts"
```bash
# Make sure you're in the right directory:
cd e:\login\auth_project

# Then run shell:
python manage.py shell
```

### If You Get: Database Error
```bash
# Run migrations:
python manage.py migrate

# Then try test again
```

### If You Get: AttributeError Still
```bash
# Verify the file was saved correctly:
# Check line 65 shows: member = instance.user
# Check line 176 shows: user=instance.receiver
# Check line 194 shows: receiver=actor
# Check line 226 shows: notification_type=notification_type

# If not, re-apply fixes from FIX_SIGNALS_REALTIME_ERRORS.md
```

### If You Get: Model Error
```bash
# Verify models are imported:
python manage.py shell
>>> from accounts.models import Project, Connection, ProjectMember, Notification
>>> # Should import without error
```

---

## Success Criteria

✅ All 7 tests pass  
✅ No AttributeError at /post-project/  
✅ Django system check passes  
✅ Notifications created with correct fields  
✅ Activity records created  
✅ WebSocket broadcasts (if testing)  

---

## References

- `FIX_SIGNALS_REALTIME_ERRORS.md` - Technical details
- `BEFORE_AFTER_SIGNALS_FIX.txt` - What changed
- `ACTION_SIGNALS_FIX_COMPLETE.md` - Full summary

---

Date: February 07, 2026  
Status: Ready for Testing
