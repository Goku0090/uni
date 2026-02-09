# Team Chat Channels for UniSinq - Complete Implementation Guide

## Overview
Implement organized team communication with **project-specific chat channels**, **thread-based discussions**, **file sharing**, and **@mention notifications**.

---

## 1. Data Models (accounts/models.py - Add These)

### 1.1 Channel Model
```python
from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone

class Channel(models.Model):
    """Project-specific chat channels"""
    
    CHANNEL_TYPES = [
        ('general', 'General Discussion'),
        ('technical', 'Technical Discussion'),
        ('management', 'Project Management'),
        ('announcements', 'Announcements'),
        ('resources', 'Resources & Files'),
        ('custom', 'Custom Channel'),
    ]
    
    project = models.ForeignKey('Project', on_delete=models.CASCADE, related_name='channels')
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True, null=True)
    channel_type = models.CharField(max_length=20, choices=CHANNEL_TYPES, default='general')
    
    # Channel settings
    is_archived = models.BooleanField(default=False)
    is_private = models.BooleanField(default=False)  # Private channels are invite-only
    created_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name='channels_created')
    
    # Metadata
    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(auto_now=True)
    last_message_at = models.DateTimeField(null=True, blank=True)
    
    class Meta:
        unique_together = ['project', 'name']
        ordering = ['channel_type', 'name']
    
    def __str__(self):
        return f"#{self.name} ({self.project.title})"
    
    @property
    def member_count(self):
        return self.members.filter(is_active=True).count()
    
    @property
    def unread_count(self, user):
        """Get unread message count for a user"""
        return self.messages.filter(
            created_at__gt=self.members.get(user=user).last_read_at
        ).count() if self.members.filter(user=user).exists() else 0


class ChannelMember(models.Model):
    """Channel membership with roles"""
    
    ROLES = [
        ('owner', 'Owner'),
        ('moderator', 'Moderator'),
        ('member', 'Member'),
    ]
    
    channel = models.ForeignKey(Channel, on_delete=models.CASCADE, related_name='members')
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    role = models.CharField(max_length=15, choices=ROLES, default='member')
    
    # Notification settings
    mute_notifications = models.BooleanField(default=False)
    last_read_at = models.DateTimeField(default=timezone.now)
    
    is_active = models.BooleanField(default=True)
    joined_at = models.DateTimeField(default=timezone.now)
    
    class Meta:
        unique_together = ['channel', 'user']
        ordering = ['joined_at']
    
    def __str__(self):
        return f"{self.user.username} in #{self.channel.name}"
    
    @property
    def can_delete_messages(self):
        return self.role in ['owner', 'moderator']
    
    @property
    def can_manage_channel(self):
        return self.role in ['owner', 'moderator']


class ChannelMessage(models.Model):
    """Messages in channels with thread support"""
    
    channel = models.ForeignKey(Channel, on_delete=models.CASCADE, related_name='messages')
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    content = models.TextField()
    
    # Thread support
    thread_root = models.ForeignKey(
        'self',
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        related_name='thread_replies'
    )
    
    # Mentions
    mentions = models.ManyToManyField(User, related_name='mentioned_in_messages', blank=True)
    
    # Metadata
    is_edited = models.BooleanField(default=False)
    edited_at = models.DateTimeField(null=True, blank=True)
    is_pinned = models.BooleanField(default=False)
    pinned_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name='pinned_messages')
    
    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['created_at']
        indexes = [
            models.Index(fields=['channel', 'created_at']),
            models.Index(fields=['author']),
            models.Index(fields=['thread_root']),
        ]
    
    def __str__(self):
        preview = self.content[:50] + '...' if len(self.content) > 50 else self.content
        return f"{self.author.username}: {preview}"
    
    @property
    def is_thread_reply(self):
        return self.thread_root is not None
    
    @property
    def reply_count(self):
        if self.thread_root is None:
            return self.thread_replies.count()
        return 0
    
    def save(self, *args, **kwargs):
        if self.pk:  # If updating existing message
            self.is_edited = True
            self.edited_at = timezone.now()
        super().save(*args, **kwargs)
        
        # Update channel's last_message_at
        self.channel.last_message_at = timezone.now()
        self.channel.save(update_fields=['last_message_at'])


class ChannelMessageFile(models.Model):
    """Files attached to channel messages"""
    
    message = models.ForeignKey(ChannelMessage, on_delete=models.CASCADE, related_name='files')
    file = models.FileField(upload_to='channel_files/%Y/%m/%d/')
    filename = models.CharField(max_length=255)
    file_size = models.PositiveIntegerField()  # in bytes
    file_type = models.CharField(max_length=100)  # MIME type
    
    uploaded_at = models.DateTimeField(default=timezone.now)
    
    class Meta:
        ordering = ['-uploaded_at']
    
    def __str__(self):
        return f"{self.filename} in message {self.message.id}"
    
    @property
    def is_image(self):
        return self.file_type.startswith('image/')
    
    @property
    def is_document(self):
        return self.file_type in [
            'application/pdf',
            'application/msword',
            'application/vnd.openxmlformats-officedocument.wordprocessingml.document',
        ]
    
    @property
    def is_code(self):
        code_types = [
            'text/plain',
            'text/javascript',
            'text/python',
            'application/json',
            'application/xml',
        ]
        return self.file_type in code_types


class ChannelMention(models.Model):
    """Track mentions for notifications"""
    
    message = models.ForeignKey(ChannelMessage, on_delete=models.CASCADE, related_name='mention_records')
    mentioned_user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='channel_mentions')
    
    is_notified = models.BooleanField(default=False)
    notified_at = models.DateTimeField(null=True, blank=True)
    
    created_at = models.DateTimeField(default=timezone.now)
    
    class Meta:
        unique_together = ['message', 'mentioned_user']
    
    def __str__(self):
        return f"{self.mentioned_user.username} mentioned in channel"
```

---

## 2. Serializers (accounts/serializers.py - Add These)

```python
from rest_framework import serializers
from .models import Channel, ChannelMember, ChannelMessage, ChannelMessageFile, ChannelMention

class ChannelSerializer(serializers.ModelSerializer):
    member_count = serializers.ReadOnlyField()
    created_by_username = serializers.CharField(source='created_by.username', read_only=True)
    
    class Meta:
        model = Channel
        fields = [
            'id', 'project', 'name', 'description', 'channel_type',
            'is_archived', 'is_private', 'created_by', 'created_by_username',
            'member_count', 'created_at', 'updated_at', 'last_message_at'
        ]
        read_only_fields = ['created_at', 'updated_at', 'last_message_at']


class ChannelMemberSerializer(serializers.ModelSerializer):
    username = serializers.CharField(source='user.username', read_only=True)
    avatar = serializers.SerializerMethodField()
    
    class Meta:
        model = ChannelMember
        fields = ['id', 'channel', 'user', 'username', 'avatar', 'role', 'mute_notifications', 'joined_at']
    
    def get_avatar(self, obj):
        if hasattr(obj.user, 'student_profile') and obj.user.student_profile.profile_photo:
            return obj.user.student_profile.profile_photo.url
        return None


class ChannelMessageFileSerializer(serializers.ModelSerializer):
    download_url = serializers.SerializerMethodField()
    
    class Meta:
        model = ChannelMessageFile
        fields = ['id', 'filename', 'file_size', 'file_type', 'is_image', 'is_document', 'is_code', 'download_url', 'uploaded_at']
    
    def get_download_url(self, obj):
        request = self.context.get('request')
        if request and obj.file:
            return request.build_absolute_uri(obj.file.url)
        return None


class ChannelMessageSerializer(serializers.ModelSerializer):
    author_username = serializers.CharField(source='author.username', read_only=True)
    author_avatar = serializers.SerializerMethodField()
    files = ChannelMessageFileSerializer(many=True, read_only=True)
    reply_count = serializers.ReadOnlyField()
    is_thread_reply = serializers.ReadOnlyField()
    mentioned_usernames = serializers.SerializerMethodField()
    
    class Meta:
        model = ChannelMessage
        fields = [
            'id', 'channel', 'author', 'author_username', 'author_avatar',
            'content', 'thread_root', 'mentions', 'mentioned_usernames',
            'files', 'is_edited', 'edited_at', 'is_pinned', 'pinned_by',
            'reply_count', 'is_thread_reply', 'created_at', 'updated_at'
        ]
        read_only_fields = ['created_at', 'updated_at', 'is_edited', 'edited_at']
    
    def get_author_avatar(self, obj):
        if hasattr(obj.author, 'student_profile') and obj.author.student_profile.profile_photo:
            return obj.author.student_profile.profile_photo.url
        return None
    
    def get_mentioned_usernames(self, obj):
        return [user.username for user in obj.mentions.all()]


class ChannelMessageDetailSerializer(ChannelMessageSerializer):
    """Detailed serializer for single message view (includes thread replies)"""
    thread_replies = ChannelMessageSerializer(many=True, read_only=True)
    
    class Meta(ChannelMessageSerializer.Meta):
        fields = ChannelMessageSerializer.Meta.fields + ['thread_replies']
```

---

## 3. Views & ViewSets (accounts/views.py - Add These)

```python
from rest_framework import viewsets, generics, status, permissions
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.parsers import MultiPartParser, FormParser
from django.shortcuts import get_object_or_404
from django.db.models import Q, Count
from django.utils import timezone
from .models import Channel, ChannelMember, ChannelMessage, ChannelMessageFile, ChannelMention, Project
from .serializers import (
    ChannelSerializer, ChannelMemberSerializer, ChannelMessageSerializer,
    ChannelMessageDetailSerializer, ChannelMessageFileSerializer
)


class IsChannelMember(permissions.BasePermission):
    """Check if user is a member of the channel"""
    
    def has_object_permission(self, request, view, obj):
        return ChannelMember.objects.filter(channel=obj, user=request.user).exists()


class IsChannelAdmin(permissions.BasePermission):
    """Check if user is admin/owner of the channel"""
    
    def has_object_permission(self, request, view, obj):
        return ChannelMember.objects.filter(
            channel=obj,
            user=request.user,
            role__in=['owner', 'moderator']
        ).exists()


class ChannelViewSet(viewsets.ModelViewSet):
    """CRUD operations for channels"""
    
    serializer_class = ChannelSerializer
    permission_classes = [permissions.IsAuthenticated]
    
    def get_queryset(self):
        # Get channels for projects the user is a member of
        user_projects = Project.objects.filter(
            Q(user=self.request.user) |
            Q(members__user=self.request.user)
        ).distinct()
        
        return Channel.objects.filter(
            Q(project__in=user_projects) |
            Q(members__user=self.request.user)
        ).distinct().prefetch_related('members', 'messages')
    
    def create(self, request, *args, **kwargs):
        """Create a new channel in a project"""
        project_id = request.data.get('project')
        project = get_object_or_404(Project, id=project_id)
        
        # Check if user is project owner/member
        if project.user != request.user and not project.members.filter(user=request.user).exists():
            return Response(
                {'detail': 'You must be a project member to create channels.'},
                status=status.HTTP_403_FORBIDDEN
            )
        
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        channel = serializer.save(created_by=request.user)
        
        # Add creator as owner
        ChannelMember.objects.create(channel=channel, user=request.user, role='owner')
        
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    
    @action(detail=True, methods=['post'])
    def add_member(self, request, pk=None):
        """Add a user to a channel"""
        channel = self.get_object()
        self.check_object_permissions(request, channel)
        
        # Check if requester is admin
        member = get_object_or_404(ChannelMember, channel=channel, user=request.user)
        if member.role not in ['owner', 'moderator']:
            return Response(
                {'detail': 'Only admins can add members.'},
                status=status.HTTP_403_FORBIDDEN
            )
        
        user_id = request.data.get('user_id')
        user = get_object_or_404(User, id=user_id)
        
        channel_member, created = ChannelMember.objects.get_or_create(
            channel=channel,
            user=user,
            defaults={'role': 'member'}
        )
        
        if not created:
            return Response({'detail': 'User is already a member.'}, status=status.HTTP_400_BAD_REQUEST)
        
        return Response(
            ChannelMemberSerializer(channel_member, context={'request': request}).data,
            status=status.HTTP_201_CREATED
        )
    
    @action(detail=True, methods=['post'])
    def remove_member(self, request, pk=None):
        """Remove a user from a channel"""
        channel = self.get_object()
        member = get_object_or_404(ChannelMember, channel=channel, user=request.user)
        
        if member.role not in ['owner', 'moderator']:
            return Response(
                {'detail': 'Only admins can remove members.'},
                status=status.HTTP_403_FORBIDDEN
            )
        
        user_id = request.data.get('user_id')
        target_member = get_object_or_404(ChannelMember, channel=channel, user_id=user_id)
        target_member.delete()
        
        return Response({'detail': 'Member removed.'}, status=status.HTTP_204_NO_CONTENT)
    
    @action(detail=True, methods=['get'])
    def members(self, request, pk=None):
        """List all channel members"""
        channel = self.get_object()
        members = channel.members.all()
        serializer = ChannelMemberSerializer(members, many=True, context={'request': request})
        return Response(serializer.data)
    
    @action(detail=True, methods=['post'])
    def leave(self, request, pk=None):
        """Leave a channel"""
        channel = self.get_object()
        member = get_object_or_404(ChannelMember, channel=channel, user=request.user)
        
        # Prevent owner from leaving if they're the only owner
        if member.role == 'owner':
            owner_count = channel.members.filter(role='owner').count()
            if owner_count == 1:
                return Response(
                    {'detail': 'Cannot leave. Transfer ownership first.'},
                    status=status.HTTP_400_BAD_REQUEST
                )
        
        member.delete()
        return Response({'detail': 'Left channel.'}, status=status.HTTP_204_NO_CONTENT)
    
    @action(detail=True, methods=['post'])
    def mute(self, request, pk=None):
        """Mute/unmute notifications for a channel"""
        channel = self.get_object()
        member = get_object_or_404(ChannelMember, channel=channel, user=request.user)
        
        mute = request.data.get('mute', True)
        member.mute_notifications = mute
        member.save()
        
        status_text = 'muted' if mute else 'unmuted'
        return Response({'detail': f'Channel {status_text}.'})


class ChannelMessageViewSet(viewsets.ModelViewSet):
    """CRUD operations for channel messages"""
    
    serializer_class = ChannelMessageSerializer
    permission_classes = [permissions.IsAuthenticated]
    parser_classes = (MultiPartParser, FormParser)
    
    def get_queryset(self):
        channel_id = self.kwargs.get('channel_id')
        
        if channel_id:
            # Filter by specific channel
            thread_root = self.request.query_params.get('thread_root')
            
            queryset = ChannelMessage.objects.filter(channel_id=channel_id)
            
            if thread_root:
                queryset = queryset.filter(thread_root_id=thread_root)
            else:
                queryset = queryset.filter(thread_root__isnull=True)
            
            return queryset.select_related('author', 'thread_root').prefetch_related('mentions', 'files')
        
        return ChannelMessage.objects.none()
    
    def get_object(self):
        message_id = self.kwargs.get('message_id')
        return get_object_or_404(ChannelMessage, id=message_id)
    
    def create(self, request, *args, **kwargs):
        """Create a new message in a channel"""
        channel_id = self.kwargs.get('channel_id')
        channel = get_object_or_404(Channel, id=channel_id)
        
        # Check if user is a channel member
        member = get_object_or_404(ChannelMember, channel=channel, user=request.user)
        
        # Parse mentions from content (@username)
        import re
        content = request.data.get('content', '')
        mention_pattern = r'@(\w+)'
        mentioned_usernames = re.findall(mention_pattern, content)
        
        # Create message
        message = ChannelMessage.objects.create(
            channel=channel,
            author=request.user,
            content=content,
            thread_root_id=request.data.get('thread_root')
        )
        
        # Add mentions
        mentioned_users = User.objects.filter(username__in=mentioned_usernames)
        message.mentions.set(mentioned_users)
        
        # Create mention records and notifications
        for user in mentioned_users:
            ChannelMention.objects.create(message=message, mentioned_user=user)
            
            # Create notification
            Notification.objects.create(
                user=user,
                notification_type='channel_mention',
                title=f'{request.user.username} mentioned you',
                message=f'You were mentioned by {request.user.username} in #{channel.name}',
                from_user=request.user
            )
        
        # Handle file uploads
        files = request.FILES.getlist('files')
        for uploaded_file in files:
            ChannelMessageFile.objects.create(
                message=message,
                file=uploaded_file,
                filename=uploaded_file.name,
                file_size=uploaded_file.size,
                file_type=uploaded_file.content_type
            )
        
        serializer = self.get_serializer(message)
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    
    def update(self, request, *args, **kwargs):
        """Edit a message"""
        message = self.get_object()
        
        # Only author can edit
        if message.author != request.user:
            return Response(
                {'detail': 'You can only edit your own messages.'},
                status=status.HTTP_403_FORBIDDEN
            )
        
        message.content = request.data.get('content', message.content)
        message.save()
        
        serializer = self.get_serializer(message)
        return Response(serializer.data)
    
    def destroy(self, request, *args, **kwargs):
        """Delete a message"""
        message = self.get_object()
        channel = message.channel
        
        # Check permissions
        member = get_object_or_404(ChannelMember, channel=channel, user=request.user)
        if message.author != request.user and member.role not in ['owner', 'moderator']:
            return Response(
                {'detail': 'You can only delete your own messages.'},
                status=status.HTTP_403_FORBIDDEN
            )
        
        message.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
    
    @action(detail=True, methods=['post'])
    def pin(self, request, *args, **kwargs):
        """Pin a message"""
        message = self.get_object()
        channel = message.channel
        
        member = get_object_or_404(ChannelMember, channel=channel, user=request.user)
        if member.role not in ['owner', 'moderator']:
            return Response(
                {'detail': 'Only admins can pin messages.'},
                status=status.HTTP_403_FORBIDDEN
            )
        
        message.is_pinned = True
        message.pinned_by = request.user
        message.save()
        
        return Response(self.get_serializer(message).data)
    
    @action(detail=True, methods=['post'])
    def unpin(self, request, *args, **kwargs):
        """Unpin a message"""
        message = self.get_object()
        
        message.is_pinned = False
        message.save()
        
        return Response(self.get_serializer(message).data)
    
    @action(detail=True, methods=['get'])
    def replies(self, request, *args, **kwargs):
        """Get all replies to a message (thread)"""
        message = self.get_object()
        
        if message.thread_root:
            return Response({'detail': 'This is a reply, not a root message.'}, status=status.HTTP_400_BAD_REQUEST)
        
        replies = message.thread_replies.all()
        serializer = self.get_serializer(replies, many=True)
        return Response({
            'root': self.get_serializer(message).data,
            'replies': serializer.data,
            'count': replies.count()
        })
    
    @action(detail=False, methods=['get'])
    def search(self, request):
        """Search messages in a channel"""
        channel_id = self.kwargs.get('channel_id')
        query = request.query_params.get('q', '')
        
        messages = ChannelMessage.objects.filter(
            channel_id=channel_id,
            content__icontains=query,
            thread_root__isnull=True
        ).select_related('author').order_by('-created_at')
        
        serializer = self.get_serializer(messages, many=True)
        return Response({
            'query': query,
            'count': messages.count(),
            'results': serializer.data
        })
```

---

## 4. URL Configuration (accounts/urls.py - Add These)

```python
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views

router = DefaultRouter()
router.register(r'channels', views.ChannelViewSet, basename='channel')

urlpatterns = [
    # Channels
    path('api/', include(router.urls)),
    
    # Channel messages
    path('api/channels/<int:channel_id>/messages/', 
         views.ChannelMessageViewSet.as_view({
             'get': 'list',
             'post': 'create'
         }), name='channel-messages'),
    
    path('api/channels/<int:channel_id>/messages/<int:message_id>/',
         views.ChannelMessageViewSet.as_view({
             'get': 'retrieve',
             'patch': 'update',
             'delete': 'destroy'
         }), name='channel-message-detail'),
    
    path('api/channels/<int:channel_id>/messages/<int:message_id>/pin/',
         views.ChannelMessageViewSet.as_view({'post': 'pin'}), name='message-pin'),
    
    path('api/channels/<int:channel_id>/messages/<int:message_id>/unpin/',
         views.ChannelMessageViewSet.as_view({'post': 'unpin'}), name='message-unpin'),
    
    path('api/channels/<int:channel_id>/messages/<int:message_id>/replies/',
         views.ChannelMessageViewSet.as_view({'get': 'replies'}), name='message-replies'),
    
    path('api/channels/<int:channel_id>/messages/search/',
         views.ChannelMessageViewSet.as_view({'get': 'search'}), name='message-search'),
]
```

---

## 5. WebSocket Consumer (accounts/consumers.py - Add This)

```python
import json
import asyncio
from channels.generic.websocket import AsyncWebsocketConsumer
from channels.db import database_sync_to_async
from django.utils import timezone
from .models import ChannelMessage, ChannelMember, Channel, ChannelMention, Notification
import logging

logger = logging.getLogger(__name__)


class ChannelChatConsumer(AsyncWebsocketConsumer):
    """WebSocket consumer for real-time channel communication"""
    
    async def connect(self):
        self.channel_id = self.scope['url_route']['kwargs']['channel_id']
        self.channel_name_group = f'channel_{self.channel_id}'
        self.user = self.scope['user']
        
        # Check if user is a channel member
        is_member = await self.check_channel_membership()
        if not is_member:
            await self.close()
            return
        
        # Join the channel group
        await self.channel_layer.group_add(
            self.channel_name_group,
            self.channel_name
        )
        
        await self.accept()
        
        # Notify others that user is online
        await self.channel_layer.group_send(
            self.channel_name_group,
            {
                'type': 'user_online',
                'username': self.user.username,
                'user_id': self.user.id
            }
        )
        
        logger.info(f"User {self.user.username} connected to channel {self.channel_id}")
    
    async def disconnect(self, close_code):
        # Leave the channel group
        await self.channel_layer.group_discard(
            self.channel_name_group,
            self.channel_name
        )
        
        # Notify others that user is offline
        await self.channel_layer.group_send(
            self.channel_name_group,
            {
                'type': 'user_offline',
                'username': self.user.username,
                'user_id': self.user.id
            }
        )
        
        logger.info(f"User {self.user.username} disconnected from channel {self.channel_id}")
    
    async def receive(self, text_data):
        """Receive message from WebSocket"""
        try:
            data = json.loads(text_data)
            message_type = data.get('type')
            
            if message_type == 'message':
                await self.handle_new_message(data)
            elif message_type == 'typing':
                await self.handle_typing(data)
            elif message_type == 'read_message':
                await self.handle_read_message(data)
        
        except json.JSONDecodeError:
            await self.send_error("Invalid JSON")
        except Exception as e:
            logger.error(f"Error in WebSocket receive: {e}")
            await self.send_error(str(e))
    
    async def handle_new_message(self, data):
        """Handle incoming message"""
        content = data.get('content', '').strip()
        thread_root_id = data.get('thread_root_id')
        
        if not content:
            await self.send_error("Message cannot be empty")
            return
        
        # Save message to database
        message = await self.save_message(content, thread_root_id)
        
        if not message:
            await self.send_error("Failed to save message")
            return
        
        # Broadcast message to all members of the channel
        await self.channel_layer.group_send(
            self.channel_name_group,
            {
                'type': 'message_send',
                'message_id': message['id'],
                'author': message['author'],
                'author_id': message['author_id'],
                'content': message['content'],
                'mentions': message['mentions'],
                'is_thread': message['is_thread'],
                'thread_root_id': message['thread_root_id'],
                'created_at': message['created_at']
            }
        )
    
    async def handle_typing(self, data):
        """Notify others when user is typing"""
        is_typing = data.get('is_typing', False)
        
        await self.channel_layer.group_send(
            self.channel_name_group,
            {
                'type': 'typing_indicator',
                'user_id': self.user.id,
                'username': self.user.username,
                'is_typing': is_typing
            }
        )
    
    async def handle_read_message(self, data):
        """Mark message as read"""
        message_id = data.get('message_id')
        
        await self.update_last_read(message_id)
    
    # Receive from group
    async def message_send(self, event):
        """Send message to WebSocket"""
        await self.send(text_data=json.dumps({
            'type': 'message',
            'data': event
        }))
    
    async def typing_indicator(self, event):
        """Send typing indicator to WebSocket"""
        # Don't send to self
        if event['user_id'] != self.user.id:
            await self.send(text_data=json.dumps({
                'type': 'typing',
                'data': event
            }))
    
    async def user_online(self, event):
        """Send user online status"""
        if event['user_id'] != self.user.id:
            await self.send(text_data=json.dumps({
                'type': 'user_status',
                'status': 'online',
                'username': event['username'],
                'user_id': event['user_id']
            }))
    
    async def user_offline(self, event):
        """Send user offline status"""
        await self.send(text_data=json.dumps({
            'type': 'user_status',
            'status': 'offline',
            'username': event['username'],
            'user_id': event['user_id']
        }))
    
    async def mention_notification(self, event):
        """Send mention notification"""
        if event['mentioned_user_id'] == self.user.id:
            await self.send(text_data=json.dumps({
                'type': 'mention',
                'data': event
            }))
    
    # Database operations
    @database_sync_to_async
    def check_channel_membership(self):
        """Check if user is a member of the channel"""
        return ChannelMember.objects.filter(
            channel_id=self.channel_id,
            user=self.user,
            is_active=True
        ).exists()
    
    @database_sync_to_async
    def save_message(self, content, thread_root_id=None):
        """Save message to database"""
        try:
            import re
            
            # Extract mentions
            mention_pattern = r'@(\w+)'
            mentioned_usernames = re.findall(mention_pattern, content)
            
            # Create message
            message = ChannelMessage.objects.create(
                channel_id=self.channel_id,
                author=self.user,
                content=content,
                thread_root_id=thread_root_id
            )
            
            # Add mentions
            from django.contrib.auth.models import User
            mentioned_users = User.objects.filter(username__in=mentioned_usernames)
            message.mentions.set(mentioned_users)
            
            # Create mention records and notifications
            for user in mentioned_users:
                ChannelMention.objects.create(message=message, mentioned_user=user)
                
                # Create notification
                Notification.objects.create(
                    user=user,
                    notification_type='channel_mention',
                    title=f'{self.user.username} mentioned you',
                    message=f'@{user.username} in #{ChannelMessage.objects.get(id=message.id).channel.name}',
                    from_user=self.user
                )
            
            return {
                'id': message.id,
                'author': self.user.username,
                'author_id': self.user.id,
                'content': message.content,
                'mentions': [u.username for u in mentioned_users],
                'is_thread': thread_root_id is not None,
                'thread_root_id': thread_root_id,
                'created_at': message.created_at.isoformat()
            }
        except Exception as e:
            logger.error(f"Error saving message: {e}")
            return None
    
    @database_sync_to_async
    def update_last_read(self, message_id):
        """Update user's last read message time"""
        try:
            member = ChannelMember.objects.get(
                channel_id=self.channel_id,
                user=self.user
            )
            member.last_read_at = timezone.now()
            member.save()
        except ChannelMember.DoesNotExist:
            pass
    
    async def send_error(self, error_message):
        """Send error message to client"""
        await self.send(text_data=json.dumps({
            'type': 'error',
            'message': error_message
        }))
```

---

## 6. WebSocket Routing (accounts/routing.py - Add This)

```python
from django.urls import path
from . import consumers

websocket_urlpatterns = [
    # Channel chat
    path('ws/channel/<int:channel_id>/', consumers.ChannelChatConsumer.as_asgi()),
]
```

---

## 7. Frontend - Channel List Template

```html
<!-- accounts/templates/channels/channel_list.html -->
{% extends 'base.html' %}
{% load static %}

{% block title %}{{ project.title }} - Channels{% endblock %}

{% block content %}
<div class="container mx-auto py-6">
    <div class="grid grid-cols-12 gap-6">
        <!-- Sidebar - Channel List -->
        <div class="col-span-3 bg-gray-900 rounded-lg p-4">
            <div class="mb-6">
                <h2 class="text-xl font-bold mb-4">{{ project.title }}</h2>
                {% if is_project_owner %}
                <button onclick="showCreateChannelModal()" class="w-full bg-blue-600 hover:bg-blue-700 text-white py-2 px-4 rounded-lg flex items-center justify-center gap-2">
                    <i data-lucide="plus" class="w-4 h-4"></i>
                    New Channel
                </button>
                {% endif %}
            </div>
            
            <!-- Channel List -->
            <div id="channel-list" class="space-y-2">
                {% for channel in channels %}
                <div class="channel-item p-3 rounded-lg cursor-pointer hover:bg-gray-800 transition" 
                     onclick="selectChannel({{ channel.id }}, '{{ channel.name }}')">
                    <div class="font-medium">#{{ channel.name }}</div>
                    <div class="text-xs text-gray-400">
                        {% if channel.unread_count %}
                        <span class="bg-red-600 text-white px-2 py-1 rounded">{{ channel.unread_count }}</span>
                        {% endif %}
                    </div>
                </div>
                {% empty %}
                <p class="text-gray-400 text-sm">No channels yet</p>
                {% endfor %}
            </div>
        </div>
        
        <!-- Main Chat Area -->
        <div class="col-span-9">
            <div id="chat-container" class="bg-gray-900 rounded-lg h-full flex flex-col">
                <!-- Header -->
                <div id="chat-header" class="border-b border-gray-800 p-4">
                    <div class="flex justify-between items-center">
                        <div>
                            <h3 id="channel-title" class="text-xl font-bold">#general</h3>
                            <p id="channel-description" class="text-sm text-gray-400"></p>
                        </div>
                        <div class="flex gap-2">
                            <button class="px-4 py-2 bg-gray-800 hover:bg-gray-700 rounded-lg">
                                <i data-lucide="search" class="w-4 h-4"></i>
                            </button>
                            <button class="px-4 py-2 bg-gray-800 hover:bg-gray-700 rounded-lg" onclick="toggleMemberList()">
                                <i data-lucide="users" class="w-4 h-4"></i> Members
                            </button>
                        </div>
                    </div>
                </div>
                
                <!-- Messages -->
                <div id="message-list" class="flex-1 overflow-y-auto p-4 space-y-4">
                    <!-- Messages will be loaded here -->
                </div>
                
                <!-- Message Input -->
                <div class="border-t border-gray-800 p-4">
                    <!-- Typing Indicators -->
                    <div id="typing-indicators" class="text-sm text-gray-400 mb-2 h-4"></div>
                    
                    <!-- File Preview -->
                    <div id="file-preview" class="mb-3 flex gap-2 flex-wrap"></div>
                    
                    <!-- Input Form -->
                    <form id="message-form" class="flex gap-2">
                        <input 
                            type="text" 
                            id="message-input" 
                            class="flex-1 bg-gray-800 text-white border border-gray-700 rounded-lg px-4 py-2 focus:outline-none focus:border-blue-500"
                            placeholder="Message #general... (Type @username to mention)"
                            autocomplete="off"
                        >
                        <label class="cursor-pointer bg-gray-800 hover:bg-gray-700 text-white px-4 py-2 rounded-lg">
                            <i data-lucide="paperclip" class="w-4 h-4"></i>
                            <input type="file" id="file-input" multiple class="hidden" accept="*/*">
                        </label>
                        <button type="submit" class="bg-blue-600 hover:bg-blue-700 text-white px-6 py-2 rounded-lg font-semibold">
                            Send
                        </button>
                    </form>
                </div>
            </div>
        </div>
    </div>
</div>

<!-- Create Channel Modal -->
<div id="create-channel-modal" class="hidden fixed inset-0 bg-black/50 flex items-center justify-center z-50">
    <div class="bg-gray-900 rounded-lg p-6 w-full max-w-md">
        <h3 class="text-xl font-bold mb-4">Create Channel</h3>
        <form id="create-channel-form" onsubmit="createChannel(event)">
            <input type="hidden" id="project-id" value="{{ project.id }}">
            
            <div class="mb-4">
                <label class="block text-sm font-medium mb-2">Channel Name</label>
                <input type="text" name="name" required class="w-full bg-gray-800 border border-gray-700 rounded-lg px-3 py-2">
            </div>
            
            <div class="mb-4">
                <label class="block text-sm font-medium mb-2">Type</label>
                <select name="channel_type" class="w-full bg-gray-800 border border-gray-700 rounded-lg px-3 py-2">
                    <option value="general">General</option>
                    <option value="technical">Technical</option>
                    <option value="management">Management</option>
                    <option value="announcements">Announcements</option>
                    <option value="resources">Resources</option>
                </select>
            </div>
            
            <div class="mb-4">
                <label class="block text-sm font-medium mb-2">Description</label>
                <textarea name="description" rows="3" class="w-full bg-gray-800 border border-gray-700 rounded-lg px-3 py-2"></textarea>
            </div>
            
            <div class="flex gap-2">
                <button type="button" onclick="closeModal('create-channel-modal')" class="flex-1 bg-gray-700 text-white py-2 rounded-lg">Cancel</button>
                <button type="submit" class="flex-1 bg-blue-600 hover:bg-blue-700 text-white py-2 rounded-lg font-semibold">Create</button>
            </div>
        </form>
    </div>
</div>

{% block scripts %}
<script>
const API_BASE = '/api';
let currentChannelId = null;
let socket = null;
let selectedFiles = [];

// Initialize
document.addEventListener('DOMContentLoaded', () => {
    // Select first channel by default
    const firstChannel = document.querySelector('.channel-item');
    if (firstChannel) {
        firstChannel.click();
    }
});

// Select channel
function selectChannel(channelId, channelName) {
    currentChannelId = channelId;
    document.getElementById('channel-title').textContent = `#${channelName}`;
    
    // Update active state
    document.querySelectorAll('.channel-item').forEach(el => el.classList.remove('bg-blue-600'));
    event.target.closest('.channel-item').classList.add('bg-blue-600');
    
    // Connect to WebSocket
    connectToChannel(channelId);
    
    // Load messages
    loadMessages(channelId);
}

// Connect to WebSocket
function connectToChannel(channelId) {
    const protocol = window.location.protocol === 'https:' ? 'wss:' : 'ws:';
    socket = new WebSocket(`${protocol}//${window.location.host}/ws/channel/${channelId}/`);
    
    socket.onopen = () => {
        console.log('✅ Connected to channel', channelId);
    };
    
    socket.onmessage = (event) => {
        const data = JSON.parse(event.data);
        
        if (data.type === 'message') {
            appendMessage(data.data);
        } else if (data.type === 'typing') {
            updateTypingIndicator(data.data);
        } else if (data.type === 'user_status') {
            updateUserStatus(data.data);
        } else if (data.type === 'mention') {
            showMentionNotification(data.data);
        }
    };
    
    socket.onerror = (error) => {
        console.error('❌ WebSocket error:', error);
    };
    
    socket.onclose = () => {
        console.log('🔌 WebSocket closed');
    };
}

// Load messages
async function loadMessages(channelId) {
    const response = await fetch(`${API_BASE}/channels/${channelId}/messages/`);
    const messages = await response.json();
    
    const messageList = document.getElementById('message-list');
    messageList.innerHTML = '';
    
    messages.forEach(msg => appendMessage(msg, false));
    
    // Scroll to bottom
    messageList.scrollTop = messageList.scrollHeight;
}

// Append message
function appendMessage(message, animate = true) {
    const messageList = document.getElementById('message-list');
    
    // Check if message already exists
    if (document.getElementById(`message-${message.id}`)) return;
    
    const msgEl = document.createElement('div');
    msgEl.id = `message-${message.id}`;
    msgEl.className = 'message p-3 rounded-lg bg-gray-800 hover:bg-gray-750 transition';
    msgEl.innerHTML = `
        <div class="flex gap-3">
            <img src="${message.author_avatar || '/static/images/default-avatar.png'}" class="w-8 h-8 rounded-full">
            <div class="flex-1">
                <div class="flex items-center gap-2">
                    <strong>${message.author_username}</strong>
                    <span class="text-xs text-gray-400">${new Date(message.created_at).toLocaleTimeString()}</span>
                    ${message.is_edited ? '<span class="text-xs text-gray-500">(edited)</span>' : ''}
                </div>
                <div class="text-sm mt-1 break-words">${formatMentions(message.content)}</div>
                
                ${message.files.length > 0 ? `
                    <div class="mt-2 space-y-1">
                        ${message.files.map(f => `
                            <a href="${f.download_url}" class="block text-blue-400 hover:underline text-sm">
                                <i data-lucide="file"></i> ${f.filename}
                            </a>
                        `).join('')}
                    </div>
                ` : ''}
                
                ${message.reply_count > 0 ? `
                    <div class="mt-2 text-xs text-blue-400 cursor-pointer hover:underline" onclick="loadThread(${message.id})">
                        ${message.reply_count} replies
                    </div>
                ` : ''}
            </div>
        </div>
    `;
    
    if (animate) {
        msgEl.style.opacity = '0';
        messageList.appendChild(msgEl);
        msgEl.animate([{ opacity: 0 }, { opacity: 1 }], { duration: 300 });
    } else {
        messageList.appendChild(msgEl);
    }
    
    messageList.scrollTop = messageList.scrollHeight;
}

// Format mentions
function formatMentions(content) {
    return content.replace(/@(\w+)/g, '<span class="bg-blue-600/30 text-blue-300 px-1 rounded">@$1</span>');
}

// Send message
document.getElementById('message-form')?.addEventListener('submit', async (e) => {
    e.preventDefault();
    
    if (!currentChannelId) return;
    
    const input = document.getElementById('message-input');
    const content = input.value.trim();
    
    if (!content && selectedFiles.length === 0) return;
    
    const formData = new FormData();
    formData.append('content', content);
    formData.append('channel', currentChannelId);
    
    selectedFiles.forEach(file => {
        formData.append('files', file);
    });
    
    try {
        const response = await fetch(`${API_BASE}/channels/${currentChannelId}/messages/`, {
            method: 'POST',
            body: formData,
            headers: { 'X-CSRFToken': getCookie('csrftoken') }
        });
        
        if (response.ok) {
            input.value = '';
            selectedFiles = [];
            document.getElementById('file-preview').innerHTML = '';
        }
    } catch (error) {
        console.error('Error sending message:', error);
    }
});

// Typing indicator
document.getElementById('message-input')?.addEventListener('input', () => {
    if (socket && socket.readyState === WebSocket.OPEN) {
        socket.send(JSON.stringify({
            type: 'typing',
            is_typing: document.getElementById('message-input').value.length > 0
        }));
    }
});

// File handling
document.getElementById('file-input')?.addEventListener('change', (e) => {
    selectedFiles = [...e.target.files];
    
    const preview = document.getElementById('file-preview');
    preview.innerHTML = selectedFiles.map(f => `
        <div class="bg-gray-800 p-2 rounded text-sm flex items-center gap-2">
            <i data-lucide="file"></i> ${f.name}
            <button type="button" onclick="removeFile('${f.name}')" class="text-red-400">✕</button>
        </div>
    `).join('');
});

// Modal functions
function showCreateChannelModal() {
    document.getElementById('create-channel-modal').classList.remove('hidden');
}

function closeModal(modalId) {
    document.getElementById(modalId).classList.add('hidden');
}

async function createChannel(e) {
    e.preventDefault();
    
    const formData = new FormData(e.target);
    const data = {
        project: document.getElementById('project-id').value,
        name: formData.get('name'),
        channel_type: formData.get('channel_type'),
        description: formData.get('description')
    };
    
    const response = await fetch(`${API_BASE}/channels/`, {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
            'X-CSRFToken': getCookie('csrftoken')
        },
        body: JSON.stringify(data)
    });
    
    if (response.ok) {
        closeModal('create-channel-modal');
        // Reload channels
        location.reload();
    }
}

// Utility functions
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

function updateTypingIndicator(data) {
    const indicator = document.getElementById('typing-indicators');
    const typingUsers = [];
    
    if (data.is_typing && data.user_id !== {{ user.id }}) {
        typingUsers.push(data.username);
    }
    
    indicator.textContent = typingUsers.length > 0 ? `${typingUsers.join(', ')} ${typingUsers.length === 1 ? 'is' : 'are'} typing...` : '';
}

function showMentionNotification(data) {
    const notification = document.createElement('div');
    notification.className = 'fixed top-4 right-4 bg-blue-600 text-white p-4 rounded-lg shadow-lg';
    notification.innerHTML = `
        <strong>${data.author} mentioned you</strong><br>
        ${data.message.substring(0, 100)}...
    `;
    document.body.appendChild(notification);
    
    setTimeout(() => notification.remove(), 5000);
}
</script>
{% endblock %}
```

---

## 8. Implementation Checklist

- [ ] Add all models to `accounts/models.py`
- [ ] Create migrations: `python manage.py makemigrations accounts`
- [ ] Apply migrations: `python manage.py migrate`
- [ ] Add serializers to `accounts/serializers.py`
- [ ] Add viewsets to `accounts/views.py`
- [ ] Update URL routing in `accounts/urls.py`
- [ ] Add WebSocket consumer to `accounts/consumers.py`
- [ ] Update WebSocket routing in `accounts/routing.py`
- [ ] Create channel templates
- [ ] Test WebSocket connection
- [ ] Deploy to production

---

## 9. Key Features Summary

| Feature | Status | Details |
|---------|--------|---------|
| **Channel Creation** | ✅ | Create project-specific channels |
| **Channel Types** | ✅ | General, Technical, Management, Announcements, Resources |
| **Thread-based Discussions** | ✅ | Reply to messages in threads |
| **File Sharing** | ✅ | Upload files with messages (images, documents, code) |
| **@Mentions** | ✅ | Mention users with notifications |
| **Real-time Updates** | ✅ | WebSocket for instant message delivery |
| **Typing Indicators** | ✅ | Show when users are typing |
| **Message Editing** | ✅ | Edit your own messages |
| **Message Pinning** | ✅ | Pin important messages |
| **Search** | ✅ | Search messages in channels |
| **Member Management** | ✅ | Add/remove channel members |
| **Read Status** | ✅ | Track unread messages |
| **Notifications** | ✅ | Mention notifications in activity feed |

---

## 10. Testing WebSocket Connection

```javascript
// Test in browser console
const channelId = 2;
const protocol = window.location.protocol === 'https:' ? 'wss:' : 'ws:';
const socket = new WebSocket(`${protocol}//${window.location.host}/ws/channel/${channelId}/`);

socket.onopen = () => console.log('✅ Connected');
socket.onmessage = (e) => console.log('📨', JSON.parse(e.data));
socket.onerror = (e) => console.error('❌ Error', e);

// Send a message
socket.send(JSON.stringify({
    type: 'message',
    content: 'Hello team! @john please check this',
    thread_root_id: null
}));
```

---

This implementation provides **professional-grade team communication** with all requested features: organized channels, threads, file sharing, and @mentions with real-time notifications.
