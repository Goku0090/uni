"""
Django signals for real-time project updates
Triggers WebSocket events when models change
"""

from django.db.models.signals import post_save, pre_save
from django.dispatch import receiver
from django.utils import timezone
from asgiref.sync import async_to_sync
from channels.layers import get_channel_layer
import json
import logging

logger = logging.getLogger(__name__)

# Import models (avoid circular imports by importing in functions)

# Store original receivers to prevent duplicate signal registration
_signal_handlers_registered = False


@receiver(post_save, sender='accounts.Project')
def project_status_changed(sender, instance, created, **kwargs):
    """
    Signal handler for project status changes
    Broadcasts to all users watching this project
    """
    if created:
        # New project created
        broadcast_activity_feed(
            actor=instance.user,
            activity_type='project.created',
            project=instance,
            action=f"Created project '{instance.title}'",
        )
    else:
        # Project updated (status, description, etc)
        broadcast_activity_feed(
            actor=instance.user,
            activity_type='project.updated',
            project=instance,
            action=f"Updated project '{instance.title}'",
        )
        
        # Broadcast to specific project group
        channel_layer = get_channel_layer()
        async_to_sync(channel_layer.group_send)(
            f'project_{instance.id}',
            {
                'type': 'project.member_count_update',
                'current_members': instance.members.count(),
                'required_members': getattr(instance, 'team_size', None),
            }
        )


@receiver(post_save, sender='accounts.ProjectMember')
def team_member_added(sender, instance, created, **kwargs):
    """
    Signal handler for new team members
    Broadcasts member addition to project group
    """
    if created:
        project = instance.project
        member = instance.user
        
        # Broadcast to project group
        channel_layer = get_channel_layer()
        async_to_sync(channel_layer.group_send)(
            f'project_{project.id}',
            {
                'type': 'project.member_added',
                'user_id': member.id,
                'username': member.username,
                'full_name': member.student_profile.full_name if hasattr(member, 'student_profile') else member.get_full_name(),
                'timestamp': timezone.now().isoformat(),
            }
        )
        
        # Broadcast to activity feed
        broadcast_activity_feed(
            actor=member,
            activity_type='member.added',
            project=project,
            action=f"Joined '{project.title}' team",
        )
        
        # Send notification to project owner
        notify_user(
            user=project.user,
            title='New Team Member',
            message=f'{member.get_full_name()} joined your project',
            notification_type='member_added',
            related_object_id=project.id,
        )


@receiver(post_save, sender='accounts.Comment')
def comment_posted(sender, instance, created, **kwargs):
    """
    Signal handler for new comments
    Broadcasts comment to project group
    """
    if created:
        project = instance.project
        
        # Broadcast to project group
        channel_layer = get_channel_layer()
        async_to_sync(channel_layer.group_send)(
            f'project_{project.id}',
            {
                'type': 'project.comment_posted',
                'comment_id': instance.id,
                'author': instance.user.username,
                'text': instance.text[:100],  # First 100 chars
                'timestamp': timezone.now().isoformat(),
            }
        )
        
        # Broadcast to activity feed
        broadcast_activity_feed(
            actor=instance.user,
            activity_type='comment.posted',
            project=project,
            action=f"Commented on '{project.title}'",
        )
        
        # Notify project owner
        if instance.user != project.user:
            notify_user(
                user=project.user,
                title='New Comment',
                message=f'{instance.user.username} commented on your project',
                notification_type='comment_posted',
                related_object_id=project.id,
            )


@receiver(post_save, sender='accounts.Like')
def like_added(sender, instance, created, **kwargs):
    """
    Signal handler for project likes
    Notifies project owner
    """
    if created:
        project = instance.project
        
        # Broadcast to activity feed
        broadcast_activity_feed(
            actor=instance.user,
            activity_type='like.added',
            project=project,
            action=f"Liked '{project.title}'",
        )
        
        # Notify project owner
        if instance.user != project.user:
            notify_user(
                user=project.user,
                title='Project Liked',
                message=f'{instance.user.username} liked your project',
                notification_type='like_added',
                related_object_id=project.id,
            )


@receiver(post_save, sender='accounts.Connection')
def connection_created(sender, instance, created, **kwargs):
    """
    Signal handler for new connections
    Notifies when users connect
    """
    if created:
        # Notify the user receiving the connection request
        notify_user(
            user=instance.receiver,
            title='New Connection Request',
            message=f'{instance.sender.username} sent you a connection request',
            notification_type='connection_request',
            related_object_id=instance.sender.id,
        )


def broadcast_activity_feed(actor, activity_type, project, action):
    """
    Broadcast activity to all users following the project or actor
    """
    try:
        channel_layer = get_channel_layer()
        
        # Get all connections of the actor (followers)
        from .models import Connection
        followers = Connection.objects.filter(
            receiver=actor,
            status='accepted'
        ).values_list('sender_id', flat=True)
        
        # Broadcast to each follower
        for user_id in followers:
            async_to_sync(channel_layer.group_send)(
                f'activity_feed_{user_id}',
                {
                    'type': 'activity.notification',
                    'activity_type': activity_type,
                    'project_id': project.id,
                    'project_title': project.title,
                    'action': action,
                    'actor': actor.username,
                    'timestamp': timezone.now().isoformat(),
                }
            )
    except Exception as e:
        logger.error(f"Error broadcasting activity: {str(e)}")


def notify_user(user, title, message, notification_type, related_object_id=None):
    """
    Send notification to user via WebSocket
    """
    try:
        # Create notification in database
        from .models import Notification
        notification = Notification.objects.create(
            user=user,
            notification_type=notification_type,
            title=title,
            message=message,
        )
        
        # Send via WebSocket
        channel_layer = get_channel_layer()
        async_to_sync(channel_layer.group_send)(
            f'notifications_{user.id}',
            {
                'type': 'send.notification',
                'notification_id': notification.id,
                'title': title,
                'message': message,
                'notification_type': notification_type,
                'related_object_id': related_object_id,
                'timestamp': timezone.now().isoformat(),
            }
        )
    except Exception as e:
        logger.error(f"Error sending notification: {str(e)}")


def ready():
    """
    Register signal handlers
    Called from apps.py
    """
    global _signal_handlers_registered
    
    if _signal_handlers_registered:
        logger.debug("Signal handlers already registered, skipping")
        return
    
    try:
        from django.apps import apps
        from .models import Project, ProjectMember, Comment, Like, Connection
        
        # Connect signals without decorator
        post_save.connect(project_status_changed, sender=Project)
        post_save.connect(team_member_added, sender=ProjectMember)
        post_save.connect(comment_posted, sender=Comment)
        post_save.connect(like_added, sender=Like)
        post_save.connect(connection_created, sender=Connection)
        
        _signal_handlers_registered = True
        logger.info("[SUCCESS] Real-time signal handlers registered successfully")
    except Exception as e:
        logger.error(f"❌ Error registering signal handlers: {str(e)}")
        import traceback
        logger.error(traceback.format_exc())
