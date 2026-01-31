"""
Models for the accounts app
"""

from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
from django.core.validators import FileExtensionValidator
import uuid


class StudentProfile(models.Model):
    """Extended user profile for students"""

    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='student_profile')
    full_name = models.CharField(max_length=100, blank=True, null=True)
    college = models.CharField(max_length=200, blank=True, null=True)
    other_college = models.CharField(max_length=200, blank=True, null=True)
    location = models.CharField(max_length=100, blank=True, null=True)
    interests = models.JSONField(default=list, blank=True)  # JSON array of interests
    bio = models.TextField(blank=True, null=True)
    profile_photo = models.ImageField(
        upload_to='profile_photos/',
        blank=True,
        null=True,
        validators=[FileExtensionValidator(['jpg', 'jpeg', 'png', 'gif'])]
    )

    # Skills and project interests as arrays
    skills = models.JSONField(default=list, blank=True)
    project_interests = models.JSONField(default=list, blank=True)
    role_preference = models.CharField(max_length=50, blank=True, null=True)

    # Social links
    github = models.URLField(blank=True, null=True)
    linkedin = models.URLField(blank=True, null=True)
    portfolio = models.URLField(blank=True, null=True)
    behance = models.URLField(blank=True, null=True)

    # Profile completion
    profile_completed = models.BooleanField(default=False)
    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.user.username}'s profile"

    def get_display_name(self):
        return self.full_name or self.user.username

    class Meta:
        ordering = ['-created_at']


class OTP(models.Model):
    """One-time password for authentication"""

    PURPOSE_CHOICES = [
        ('login', 'Login'),
        ('registration', 'Registration'),
        ('reset', 'Password Reset'),
    ]

    email = models.EmailField()
    otp_code = models.CharField(max_length=6)  # 6-digit OTP code
    purpose = models.CharField(max_length=20, choices=PURPOSE_CHOICES)
    is_used = models.BooleanField(default=False)
    created_at = models.DateTimeField(default=timezone.now)
    expires_at = models.DateTimeField()

    def is_valid(self):
        """Check if OTP is valid and not expired"""
        return not self.is_used and timezone.now() < self.expires_at

    @staticmethod
    def hash_otp(otp_code):
        """Hash OTP code using SHA-256"""
        import hashlib
        return hashlib.sha256(otp_code.encode()).hexdigest()

    def verify_otp(self, otp_code):
        """Verify OTP code against stored code"""
        if not self.is_valid():
            return False, "OTP has expired or is invalid."

        # Check if provided OTP matches the code
        if otp_code == self.otp_code:
            self.is_used = True
            self.save()
            return True, "OTP verified successfully."
        else:
            return False, "Invalid OTP code."

    @classmethod
    def generate_otp(cls, email, purpose):
        """Generate a new OTP for the given email and purpose"""
        import random
        import string

        # Generate 6-digit OTP
        otp_code = ''.join(random.choices(string.digits, k=6))

        # Set expiry time (5 minutes from now)
        expires_at = timezone.now() + timezone.timedelta(minutes=5)

        # Deactivate any existing OTPs for this email and purpose
        cls.objects.filter(email=email, purpose=purpose, is_used=False).update(is_used=True)

        # Create new OTP
        otp_obj = cls.objects.create(
            email=email,
            otp_code=otp_code,
            purpose=purpose,
            expires_at=expires_at
        )

        return otp_obj

    def __str__(self):
        return f"OTP for {self.email} ({self.purpose})"

    class Meta:
        ordering = ['-created_at']


class Connection(models.Model):
    """Connection requests between users"""

    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('accepted', 'Accepted'),
        ('rejected', 'Rejected'),
    ]

    sender = models.ForeignKey(User, on_delete=models.CASCADE, related_name='sent_connections')
    receiver = models.ForeignKey(User, on_delete=models.CASCADE, related_name='received_connections')
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='pending')
    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.sender.username} -> {self.receiver.username} ({self.status})"

    class Meta:
        unique_together = ['sender', 'receiver']
        ordering = ['-created_at']


class Message(models.Model):
    """Direct messages between users"""

    MESSAGE_TYPES = [
        ('text', 'Text'),
        ('file', 'File'),
        ('image', 'Image'),
        ('call', 'Call'),
    ]

    sender = models.ForeignKey(User, on_delete=models.CASCADE, related_name='sent_messages')
    receiver = models.ForeignKey(User, on_delete=models.CASCADE, related_name='received_messages', null=True, blank=True)

    # For enhanced messaging (group chats)
    chat_room = models.ForeignKey('ChatRoom', on_delete=models.CASCADE, null=True, blank=True, related_name='messages')

    content = models.TextField()
    message_type = models.CharField(max_length=10, choices=MESSAGE_TYPES, default='text')
    call_type = models.CharField(max_length=10, choices=[('voice', 'Voice'), ('video', 'Video')], null=True, blank=True)

    # Threading support
    reply_to = models.ForeignKey('self', on_delete=models.SET_NULL, null=True, blank=True, related_name='replies')

    # Read status now handled by MessageReadStatus model for scalability
    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(auto_now=True)

    def mark_as_read_by(self, user):
        """Mark this message as read by a specific user"""
        MessageReadStatus.objects.get_or_create(
            message=self,
            user=user,
            defaults={'read_at': timezone.now()}
        )

    def is_read_by(self, user):
        """Check if this message has been read by a specific user"""
        return MessageReadStatus.objects.filter(message=self, user=user).exists()

    def get_read_by_users(self):
        """Get all users who have read this message"""
        return User.objects.filter(
            id__in=MessageReadStatus.objects.filter(message=self).values('user')
        )

    def get_read_count(self):
        """Get the number of users who have read this message"""
        return self.read_statuses.count()

    def get_unread_users(self):
        """Get users who haven't read this message (for group chats)"""
        if self.chat_room and self.chat_room.chat_type != 'direct':
            # For group chats, get all active members except sender
            read_user_ids = set(self.read_statuses.values_list('user_id', flat=True))
            return self.chat_room.members.filter(
                is_active=True,
                user_id__in=[member.user_id for member in self.chat_room.members.all() if member.user_id != self.sender_id]
            ).exclude(user_id__in=read_user_ids)
        elif self.receiver and self.receiver != self.sender:
            # For direct messages, check if receiver has read it
            return [self.receiver] if not self.is_read_by(self.receiver) else []
        return []

    def __str__(self):
        return f"Message from {self.sender.username}: {self.content[:50]}..."

    class Meta:
        ordering = ['created_at']


class MessageFile(models.Model):
    """Files attached to messages"""

    message = models.ForeignKey(Message, on_delete=models.CASCADE, related_name='files')
    file = models.ForeignKey('File', on_delete=models.CASCADE)
    uploaded_at = models.DateTimeField(default=timezone.now)

    class Meta:
        unique_together = ['message', 'file']


class MessageReaction(models.Model):
    """Reactions to messages"""

    message = models.ForeignKey(Message, on_delete=models.CASCADE, related_name='reactions')
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    reaction = models.CharField(max_length=50)  # emoji or text
    created_at = models.DateTimeField(default=timezone.now)

    class Meta:
        unique_together = ['message', 'user', 'reaction']
        ordering = ['created_at']


class File(models.Model):
    """File uploads"""

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    file = models.FileField(upload_to='chat_files/')
    filename = models.CharField(max_length=255)
    file_size = models.PositiveIntegerField()
    file_type = models.CharField(max_length=100)
    uploaded_at = models.DateTimeField(default=timezone.now)

    @property
    def is_image(self):
        return self.file_type.startswith('image/')

    def __str__(self):
        return self.filename

    class Meta:
        ordering = ['-uploaded_at']


class MessageReadStatus(models.Model):
    """Tracks which users have read which messages"""

    message = models.ForeignKey(Message, on_delete=models.CASCADE, related_name='read_statuses')
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    read_at = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return f"{self.user.username} read message {self.message.id}"

    class Meta:
        unique_together = ['message', 'user']
        ordering = ['read_at']


class ChatRoom(models.Model):
    """Chat rooms for group chats and enhanced messaging"""

    CHAT_TYPES = [
        ('direct', 'Direct Message'),
        ('group', 'Group Chat'),
        ('project', 'Project Chat'),
    ]

    name = models.CharField(max_length=100, null=True, blank=True)
    chat_type = models.CharField(max_length=10, choices=CHAT_TYPES, default='direct')
    project = models.ForeignKey('Project', on_delete=models.CASCADE, null=True, blank=True, related_name='chat_rooms')
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(default=timezone.now)
    created_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)

    @property
    def display_name(self):
        if self.chat_type == 'direct':
            # For direct chats, get the other user's name
            return "Direct Chat"
        return self.name or f"{self.chat_type.title()} Chat"

    def __str__(self):
        return self.display_name

    class Meta:
        ordering = ['-created_at']


class ChatRoomMember(models.Model):
    """Members of chat rooms"""

    ROLES = [
        ('owner', 'Owner'),
        ('admin', 'Admin'),
        ('member', 'Member'),
    ]

    chat_room = models.ForeignKey(ChatRoom, on_delete=models.CASCADE, related_name='members')
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    role = models.CharField(max_length=10, choices=ROLES, default='member')
    is_active = models.BooleanField(default=True)
    joined_at = models.DateTimeField(default=timezone.now)

    @property
    def can_invite_members(self):
        return self.role in ['owner', 'admin']

    @property
    def can_manage_room(self):
        return self.role in ['owner', 'admin']

    class Meta:
        unique_together = ['chat_room', 'user']
        ordering = ['joined_at']


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

    is_read = models.BooleanField(default=False)
    read_at = models.DateTimeField(null=True, blank=True)
    created_at = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return f"{self.user.username}: {self.title}"

    class Meta:
        ordering = ['-created_at']


class Comment(models.Model):
    """Comments on projects"""

    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='comments')
    project = models.ForeignKey('Project', on_delete=models.CASCADE, related_name='comments')
    content = models.TextField()
    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Comment by {self.user.username} on {self.project.title}"

    class Meta:
        ordering = ['created_at']


class UserStatus(models.Model):
    """User online/offline status"""

    user = models.OneToOneField(User, on_delete=models.CASCADE)
    is_online = models.BooleanField(default=False)
    last_seen = models.DateTimeField(default=timezone.now)
    current_room = models.CharField(max_length=100, null=True, blank=True)  # WebSocket room

    def __str__(self):
        status = "online" if self.is_online else "offline"
        return f"{self.user.username} is {status}"

    class Meta:
        ordering = ['-last_seen']


class Project(models.Model):
    """Project listings"""

    CATEGORIES = [
        ('web', 'Web Development'),
        ('mobile', 'Mobile Apps'),
        ('ai', 'AI/ML'),
        ('data', 'Data Science'),
        ('blockchain', 'Blockchain'),
        ('iot', 'IoT'),
        ('game', 'Game Development'),
        ('other', 'Other'),
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='projects')
    title = models.CharField(max_length=200)
    description = models.TextField()

    # Technologies and skills
    technologies = models.JSONField(default=list, blank=True)  # JSON array of technologies
    looking_for = models.JSONField(default=list, blank=True)  # JSON array of required roles/skills

    # Project details
    category = models.CharField(max_length=20, choices=CATEGORIES, default='other')
    timeline = models.CharField(max_length=100, blank=True, null=True)
    collaboration_needs = models.TextField(blank=True, null=True)
    github_link = models.URLField(blank=True, null=True)

    # Status and metadata
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title

    def get_technologies_list(self):
        """Get technologies as a list (for backward compatibility)"""
        return self.technologies if isinstance(self.technologies, list) else []

    def get_looking_for_list(self):
        """Get looking_for as a list (for backward compatibility)"""
        return self.looking_for if isinstance(self.looking_for, list) else []

    class Meta:
        ordering = ['-created_at']


class Like(models.Model):
    """Likes on projects"""

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    project = models.ForeignKey(Project, on_delete=models.CASCADE, related_name='likes')
    created_at = models.DateTimeField(default=timezone.now)

    class Meta:
        unique_together = ['user', 'project']
        ordering = ['-created_at']


class Follow(models.Model):
    """User following relationships"""

    follower = models.ForeignKey(User, on_delete=models.CASCADE, related_name='following_relations')
    following = models.ForeignKey(User, on_delete=models.CASCADE, related_name='follower_relations')
    created_at = models.DateTimeField(default=timezone.now)

    class Meta:
        unique_together = ['follower', 'following']
        ordering = ['-created_at']


class Activity(models.Model):
    """User activity feed"""

    ACTIVITY_TYPES = [
        ('profile_updated', 'Profile Updated'),
        ('project_created', 'Project Created'),
        ('project_liked', 'Project Liked'),
        ('connection_made', 'Connection Made'),
        ('message_sent', 'Message Sent'),
        ('comment_added', 'Comment Added'),
        ('user_followed', 'User Followed'),
        ('task_completed', 'Task Completed'),
        ('milestone_completed', 'Milestone Completed'),
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='activities')
    activity_type = models.CharField(max_length=30, choices=ACTIVITY_TYPES)
    title = models.CharField(max_length=200)
    description = models.TextField(blank=True, null=True)

    # Related objects (optional)
    project = models.ForeignKey(Project, on_delete=models.SET_NULL, null=True, blank=True)
    target_user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name='target_activities')
    connection = models.ForeignKey(Connection, on_delete=models.SET_NULL, null=True, blank=True)

    is_public = models.BooleanField(default=True)
    created_at = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return f"{self.user.username}: {self.title}"

    class Meta:
        ordering = ['-created_at']


class UserStats(models.Model):
    """User statistics for dashboard"""

    user = models.OneToOneField(User, on_delete=models.CASCADE)
    projects_created = models.PositiveIntegerField(default=0)
    connections_made = models.PositiveIntegerField(default=0)
    likes_received = models.PositiveIntegerField(default=0)
    comments_made = models.PositiveIntegerField(default=0)
    projects_joined = models.PositiveIntegerField(default=0)
    tasks_completed = models.PositiveIntegerField(default=0)
    followers_count = models.PositiveIntegerField(default=0)
    following_count = models.PositiveIntegerField(default=0)
    last_updated = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return f"{self.user.username}'s stats"

    def update_stats(self):
        """Update all statistics"""
        self.projects_created = Project.objects.filter(user=self.user).count()
        self.connections_made = Connection.objects.filter(
            models.Q(sender=self.user) | models.Q(receiver=self.user),
            status='accepted'
        ).count()
        self.likes_received = Like.objects.filter(project__user=self.user).count()
        self.comments_made = Comment.objects.filter(user=self.user).count()
        self.followers_count = Follow.objects.filter(following=self.user).count()
        self.following_count = Follow.objects.filter(follower=self.user).count()
        self.last_updated = timezone.now()
        self.save()


class ProjectMember(models.Model):
    """Project members with roles"""

    ROLES = [
        ('owner', 'Owner'),
        ('admin', 'Admin'),
        ('contributor', 'Contributor'),
        ('viewer', 'Viewer'),
    ]

    project = models.ForeignKey(Project, on_delete=models.CASCADE, related_name='members')
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    role = models.CharField(max_length=15, choices=ROLES, default='contributor')
    is_active = models.BooleanField(default=True)
    joined_at = models.DateTimeField(default=timezone.now)

    @property
    def can_manage_project(self):
        return self.role in ['owner', 'admin']

    @property
    def can_invite_members(self):
        return self.role in ['owner', 'admin']

    @property
    def can_manage_tasks(self):
        return self.role in ['owner', 'admin', 'contributor']

    @property
    def can_edit_project(self):
        return self.role in ['owner', 'admin', 'contributor']

    def __str__(self):
        return f"{self.user.username} ({self.role}) on {self.project.title}"

    class Meta:
        unique_together = ['project', 'user']
        ordering = ['joined_at']


class ProjectInvitation(models.Model):
    """Invitations to join projects"""

    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('accepted', 'Accepted'),
        ('declined', 'Declined'),
        ('expired', 'Expired'),
    ]

    project = models.ForeignKey(Project, on_delete=models.CASCADE, related_name='invitations')
    invited_user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='project_invitations')
    invited_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name='sent_project_invitations')
    role = models.CharField(max_length=15, choices=ProjectMember.ROLES, default='contributor')
    message = models.TextField(blank=True, null=True)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='pending')
    created_at = models.DateTimeField(default=timezone.now)
    expires_at = models.DateTimeField()
    responded_at = models.DateTimeField(null=True, blank=True)

    def accept(self):
        """Accept the invitation"""
        if self.status != 'pending' or timezone.now() > self.expires_at:
            return False

        # Add user to project
        ProjectMember.objects.create(
            project=self.project,
            user=self.invited_user,
            role=self.role
        )

        self.status = 'accepted'
        self.responded_at = timezone.now()
        self.save()
        return True

    def decline(self):
        """Decline the invitation"""
        if self.status != 'pending':
            return False

        self.status = 'declined'
        self.responded_at = timezone.now()
        self.save()
        return True

    def __str__(self):
        return f"Invitation for {self.invited_user.username} to join {self.project.title}"

    class Meta:
        ordering = ['-created_at']


class ProjectTask(models.Model):
    """Tasks within projects"""

    STATUS_CHOICES = [
        ('todo', 'To Do'),
        ('in_progress', 'In Progress'),
        ('review', 'In Review'),
        ('completed', 'Completed'),
        ('cancelled', 'Cancelled'),
    ]

    PRIORITY_CHOICES = [
        ('low', 'Low'),
        ('medium', 'Medium'),
        ('high', 'High'),
        ('urgent', 'Urgent'),
    ]

    project = models.ForeignKey(Project, on_delete=models.CASCADE, related_name='tasks')
    title = models.CharField(max_length=200)
    description = models.TextField(blank=True, null=True)
    assigned_to = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name='assigned_tasks')
    assigned_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name='created_tasks')
    status = models.CharField(max_length=15, choices=STATUS_CHOICES, default='todo')
    priority = models.CharField(max_length=10, choices=PRIORITY_CHOICES, default='medium')
    due_date = models.DateField(null=True, blank=True)
    completed_at = models.DateTimeField(null=True, blank=True)
    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(auto_now=True)

    def mark_completed(self):
        """Mark task as completed"""
        if self.status != 'completed':
            self.status = 'completed'
            self.completed_at = timezone.now()
            self.save()

    def __str__(self):
        return f"{self.title} ({self.status})"

    class Meta:
        ordering = ['-created_at']


class ProjectMilestone(models.Model):
    """Milestones for projects"""

    project = models.ForeignKey(Project, on_delete=models.CASCADE, related_name='milestones')
    title = models.CharField(max_length=200)
    description = models.TextField(blank=True, null=True)
    due_date = models.DateField(null=True, blank=True)
    is_completed = models.BooleanField(default=False)
    completed_at = models.DateTimeField(null=True, blank=True)
    completed_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name='completed_milestones')
    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(auto_now=True)

    def mark_completed(self, user=None):
        """Mark milestone as completed"""
        if not self.is_completed:
            self.is_completed = True
            self.completed_at = timezone.now()
            if user:
                self.completed_by = user
            self.save()

    def __str__(self):
        status = "✓" if self.is_completed else "○"
        return f"{status} {self.title}"

    class Meta:
        ordering = ['due_date', 'created_at']


# ============================================================================
# Model Aliases for Backward Compatibility
# ============================================================================
# Some views.py code references old model names
# Create aliases to support both naming conventions

ProjectTeam = ProjectMember
ProjectTeamMember = ProjectMember
ProjectTeamInvitation = ProjectInvitation
