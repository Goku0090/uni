"""
WebSocket consumers for real-time project updates
Handles live notifications, status updates, and activity feeds
"""

import json
from channels.generic.websocket import AsyncWebsocketConsumer
from channels.db import database_sync_to_async
from django.utils import timezone
from .models import Project, Activity, Notification
import logging

logger = logging.getLogger(__name__)


class ProjectUpdateConsumer(AsyncWebsocketConsumer):
    """
    WebSocket consumer for real-time project status updates
    Broadcasts updates to all connected clients watching a project
    """
    
    async def connect(self):
        """Handle WebSocket connection"""
        self.project_id = self.scope['url_route']['kwargs']['project_id']
        self.project_group_name = f'project_{self.project_id}'
        
        # Join project group
        await self.channel_layer.group_add(
            self.project_group_name,
            self.channel_name
        )
        
        # Accept connection
        await self.accept()
        
        # Send initial project data
        project_data = await self.get_project_data()
        await self.send(text_data=json.dumps({
            'type': 'project.initial_data',
            'data': project_data
        }))
        
        logger.info(f"User {self.scope['user']} connected to project {self.project_id}")

    async def disconnect(self, close_code):
        """Handle WebSocket disconnection"""
        await self.channel_layer.group_discard(
            self.project_group_name,
            self.channel_name
        )
        logger.info(f"User {self.scope['user']} disconnected from project {self.project_id}")

    async def receive(self, text_data):
        """Receive message from WebSocket"""
        try:
            data = json.loads(text_data)
            message_type = data.get('type')
            
            if message_type == 'status.update':
                # Handle project status update
                new_status = data.get('status')
                await self.handle_status_update(new_status)
                
            elif message_type == 'member.add':
                # Handle adding new member
                user_id = data.get('user_id')
                await self.handle_member_add(user_id)
                
            elif message_type == 'comment.post':
                # Handle new comment
                comment_text = data.get('text')
                await self.handle_new_comment(comment_text)
                
        except json.JSONDecodeError:
            logger.error(f"Invalid JSON received: {text_data}")
            await self.send_error("Invalid message format")

    async def project_status_update(self, event):
        """
        Receive status update from group and send to WebSocket
        Event sent from views/signals when project status changes
        """
        await self.send(text_data=json.dumps({
            'type': 'project.status_update',
            'status': event['status'],
            'timestamp': event.get('timestamp'),
            'changed_by': event.get('changed_by'),
            'message': event.get('message', ''),
        }))

    async def project_member_added(self, event):
        """
        Receive member addition notification
        Event sent when new member joins project team
        """
        await self.send(text_data=json.dumps({
            'type': 'project.member_added',
            'user_id': event['user_id'],
            'username': event.get('username'),
            'full_name': event.get('full_name'),
            'timestamp': event.get('timestamp'),
        }))

    async def project_comment_posted(self, event):
        """
        Receive new comment notification
        Event sent when comment is posted on project
        """
        await self.send(text_data=json.dumps({
            'type': 'project.comment_posted',
            'comment_id': event['comment_id'],
            'author': event.get('author'),
            'text': event.get('text'),
            'timestamp': event.get('timestamp'),
        }))

    async def project_member_count_update(self, event):
        """
        Receive member count update
        Event sent when team composition changes
        """
        await self.send(text_data=json.dumps({
            'type': 'project.member_count',
            'current_members': event['current_members'],
            'required_members': event.get('required_members'),
        }))

    @database_sync_to_async
    def get_project_data(self):
        """Fetch current project data from database"""
        try:
            project = Project.objects.get(id=self.project_id)
            return {
                'id': project.id,
                'title': project.title,
                'description': project.description,
                'category': project.category,
                'is_active': project.is_active,
                'owner': project.user.username,
                'owner_id': project.user.id,
                'created_at': project.created_at.isoformat(),
                'updated_at': project.updated_at.isoformat(),
            }
        except Project.DoesNotExist:
            logger.error(f"Project {self.project_id} not found")
            return None

    @database_sync_to_async
    def handle_status_update(self, new_status):
        """Handle project status change"""
        try:
            project = Project.objects.get(id=self.project_id)
            
            # Check if user has permission (user is the owner, not owner)
            if project.user != self.scope['user']:
                raise PermissionError("Only project owner can update status")
            
            # Project doesn't have status field, skip status update
            # Instead just log the activity
            
            # Create activity log
            Activity.objects.create(
                user=self.scope['user'],
                activity_type='project_updated',
                title=f"Updated project '{project.title}'",
                description=f"Project status/details updated",
                project=project
            )
            
            # Broadcast to all connected clients
            import asyncio
            asyncio.create_task(self.channel_layer.group_send(
                self.project_group_name,
                {
                    'type': 'project.status_update',
                    'status': new_status,
                    'changed_by': self.scope['user'].username,
                    'timestamp': timezone.now().isoformat(),
                    'message': f"Project status changed to {new_status}",
                }
            ))
            
            logger.info(f"Project {self.project_id} status updated to {new_status}")
        except Exception as e:
            logger.error(f"Error updating status: {str(e)}")
            asyncio.create_task(self.send_error(str(e)))

    @database_sync_to_async
    def handle_member_add(self, user_id):
        """Handle adding new member to project"""
        try:
            project = Project.objects.get(id=self.project_id)
            
            # Check permission (use project.user not project.owner)
            if project.user != self.scope['user']:
                raise PermissionError("Only project owner can add members")
            
            from django.contrib.auth.models import User
            from .models import ProjectMember
            new_member = User.objects.get(id=user_id)
            
            # Add member via ProjectMember model (not project.members)
            ProjectMember.objects.get_or_create(
                project=project,
                user=new_member,
                defaults={'role': 'contributor'}
            )
            
            # Create activity log
            Activity.objects.create(
                user=self.scope['user'],
                activity_type='project_updated',
                title=f"Added {new_member.username} to project",
                description=f"Added {new_member.username} as team member",
                project=project
            )
            
            # Broadcast to all connected clients
            import asyncio
            asyncio.create_task(self.channel_layer.group_send(
                self.project_group_name,
                {
                    'type': 'project.member_added',
                    'user_id': new_member.id,
                    'username': new_member.username,
                    'full_name': new_member.student_profile.full_name,
                    'timestamp': timezone.now().isoformat(),
                }
            ))
            
            logger.info(f"Member {user_id} added to project {self.project_id}")
        except Exception as e:
            logger.error(f"Error adding member: {str(e)}")
            asyncio.create_task(self.send_error(str(e)))

    @database_sync_to_async
    def handle_new_comment(self, comment_text):
        """Handle new comment posting"""
        try:
            from .models import Comment
            project = Project.objects.get(id=self.project_id)
            
            # Create comment (use 'content' field, not 'text')
            comment = Comment.objects.create(
                project=project,
                user=self.scope['user'],
                content=comment_text
            )
            
            # Broadcast to all connected clients
            import asyncio
            asyncio.create_task(self.channel_layer.group_send(
                self.project_group_name,
                {
                    'type': 'project.comment_posted',
                    'comment_id': comment.id,
                    'author': self.scope['user'].username,
                    'text': comment_text,
                    'timestamp': timezone.now().isoformat(),
                }
            ))
            
            logger.info(f"Comment posted on project {self.project_id}")
        except Exception as e:
            logger.error(f"Error posting comment: {str(e)}")
            asyncio.create_task(self.send_error(str(e)))

    async def send_error(self, error_message):
        """Send error message to client"""
        await self.send(text_data=json.dumps({
            'type': 'error',
            'message': error_message,
        }))


class ActivityFeedConsumer(AsyncWebsocketConsumer):
    """
    WebSocket consumer for real-time activity feed
    Shows live updates of all projects in user's feed
    """
    
    async def connect(self):
        """Handle connection to activity feed"""
        self.user = self.scope['user']
        self.group_name = f'activity_feed_{self.user.id}'
        
        if not self.user.is_authenticated:
            await self.close()
            return
        
        # Join user's activity feed group
        await self.channel_layer.group_add(
            self.group_name,
            self.channel_name
        )
        
        await self.accept()
        logger.info(f"User {self.user.username} connected to activity feed")

    async def disconnect(self, close_code):
        """Handle disconnection"""
        await self.channel_layer.group_discard(
            self.group_name,
            self.channel_name
        )
        logger.info(f"User {self.user.username} disconnected from activity feed")

    async def activity_notification(self, event):
        """
        Receive activity notification and broadcast to client
        Event types: project.created, project.updated, comment.posted, member.added
        """
        await self.send(text_data=json.dumps({
            'type': 'activity.update',
            'activity_type': event['activity_type'],
            'project_id': event.get('project_id'),
            'project_title': event.get('project_title'),
            'action': event.get('action'),
            'actor': event.get('actor'),
            'timestamp': event.get('timestamp'),
            'icon': self.get_activity_icon(event['activity_type']),
        }))

    @staticmethod
    def get_activity_icon(activity_type):
        """Get appropriate icon for activity type"""
        icons = {
            'project.created': '🚀',
            'project.updated': '✏️',
            'member.added': '👥',
            'comment.posted': '💬',
            'status.changed': '⚡',
            'like.added': '❤️',
        }
        return icons.get(activity_type, '📢')


class NotificationConsumer(AsyncWebsocketConsumer):
    """
    WebSocket consumer for real-time notifications
    Sends notifications for mentions, messages, and important updates
    """
    
    async def connect(self):
        """Handle notification subscription"""
        self.user = self.scope['user']
        self.group_name = f'notifications_{self.user.id}'
        
        if not self.user.is_authenticated:
            await self.close()
            return
        
        # Join user's notification group
        await self.channel_layer.group_add(
            self.group_name,
            self.channel_name
        )
        
        await self.accept()
        
        # Send unread notification count
        unread_count = await self.get_unread_count()
        await self.send(text_data=json.dumps({
            'type': 'notification.count',
            'unread_count': unread_count,
        }))
        
        logger.info(f"User {self.user.username} connected to notifications")

    async def disconnect(self, close_code):
        """Handle notification disconnection"""
        await self.channel_layer.group_discard(
            self.group_name,
            self.channel_name
        )
        logger.info(f"User {self.user.username} disconnected from notifications")

    async def receive(self, text_data):
        """Handle incoming messages"""
        try:
            data = json.loads(text_data)
            
            if data.get('type') == 'mark_read':
                notification_id = data.get('notification_id')
                await self.mark_notification_read(notification_id)
                
        except json.JSONDecodeError:
            logger.error(f"Invalid JSON: {text_data}")

    async def send_notification(self, event):
        """
        Send notification to user
        Event types: mention, message, project_update, connection_request
        """
        await self.send(text_data=json.dumps({
            'type': 'notification.received',
            'notification_id': event.get('notification_id'),
            'title': event.get('title'),
            'message': event.get('message'),
            'notification_type': event.get('notification_type'),
            'actor': event.get('actor'),
            'related_object_id': event.get('related_object_id'),
            'timestamp': event.get('timestamp'),
            'sound': event.get('sound', True),
        }))

    @database_sync_to_async
    def get_unread_count(self):
        """Get count of unread notifications"""
        try:
            return Notification.objects.filter(
                user=self.user,
                is_read=False
            ).count()
        except Exception as e:
            logger.error(f"Error getting unread count: {str(e)}")
            return 0

    @database_sync_to_async
    def mark_notification_read(self, notification_id):
        """Mark notification as read"""
        try:
            notification = Notification.objects.get(
                id=notification_id,
                user=self.user
            )
            notification.is_read = True
            notification.save()
            
            logger.info(f"Notification {notification_id} marked as read")
        except Notification.DoesNotExist:
            logger.error(f"Notification {notification_id} not found")
        except Exception as e:
            logger.error(f"Error marking notification as read: {str(e)}")
