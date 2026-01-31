"""
Improved Chat API with enhanced error handling and security
"""

from rest_framework import generics, permissions, status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework.views import APIView
from django.shortcuts import get_object_or_404
from django.contrib.auth import get_user_model
from django.db.models import Q, F, Count
from .models import ChatRoom, Message, ChatRoomMember, MessageReaction, MessageReadStatus
from .serializers import MessageSerializer
from .permissions import check_chat_room_member
import logging

logger = logging.getLogger(__name__)
User = get_user_model()


class ChatRoomListCreateView(generics.ListCreateAPIView):
    """List and create chat rooms"""
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return ChatRoom.objects.filter(
            members__user=self.request.user,
            is_active=True
        ).distinct()

    def perform_create(self, serializer):
        try:
            chat_room = serializer.save(created_by=self.request.user)
            # Add creator as owner
            ChatRoomMember.objects.create(
                chat_room=chat_room,
                user=self.request.user,
                role='owner'
            )
            logger.info(f"Chat room created: {chat_room.name}")
        except Exception as e:
            logger.error(f"Error creating chat room: {str(e)}")
            raise


class ChatRoomDetailView(generics.RetrieveUpdateDestroyAPIView):
    """Chat room details"""
    permission_classes = [permissions.IsAuthenticated]
    queryset = ChatRoom.objects.filter(is_active=True)

    def get_queryset(self):
        return self.queryset.filter(members__user=self.request.user)


class ChatRoomMembersView(generics.ListAPIView):
    """List chat room members"""
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        room_id = self.kwargs['room_id']
        return ChatRoomMember.objects.filter(
            chat_room_id=room_id,
            is_active=True
        ).select_related('user')


class DirectMessageView(APIView):
    """Create or get direct message chat room"""
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request):
        user_id = request.data.get('user_id')
        if not user_id:
            return Response({'error': 'user_id required'}, status=status.HTTP_400_BAD_REQUEST)

        try:
            other_user = User.objects.get(id=user_id)

            # Check if direct chat already exists
            existing_room = ChatRoom.objects.filter(
                chat_type='direct',
                members__user=request.user
            ).filter(
                members__user=other_user
            ).distinct()

            if existing_room.exists():
                room = existing_room.first()
            else:
                # Create new direct chat room
                room = ChatRoom.objects.create(
                    chat_type='direct',
                    created_by=request.user
                )
                # Add both users
                ChatRoomMember.objects.create(chat_room=room, user=request.user)
                ChatRoomMember.objects.create(chat_room=room, user=other_user)

            return Response({'room_id': room.id})

        except User.DoesNotExist:
            return Response({'error': 'User not found'}, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            logger.error(f"Error creating direct message: {str(e)}")
            return Response({'error': 'Internal server error'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class MessageListCreateView(generics.ListCreateAPIView):
    """List and create messages"""
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = MessageSerializer

    def get_queryset(self):
        room_id = self.request.query_params.get('room_id')
        if room_id:
            return Message.objects.filter(
                chat_room_id=room_id,
                chat_room__members__user=self.request.user,
                chat_room__members__is_active=True
            ).order_by('created_at')
        return Message.objects.none()

    def perform_create(self, serializer):
        try:
            room_id = self.request.data.get('room_id')
            if not room_id:
                raise ValueError("room_id is required")

            chat_room = get_object_or_404(
                ChatRoom,
                id=room_id,
                members__user=self.request.user,
                members__is_active=True
            )

            message = serializer.save(
                chat_room=chat_room,
                sender=self.request.user
            )

            # Mark as read for sender
            MessageReadStatus.objects.get_or_create(
                message=message,
                user=self.request.user
            )

            logger.info(f"Message created in room {room_id} by {self.request.user.username}")

        except Exception as e:
            logger.error(f"Error creating message: {str(e)}")
            raise


class MessageDetailView(generics.RetrieveUpdateDestroyAPIView):
    """Message details"""
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = MessageSerializer

    def get_queryset(self):
        return Message.objects.filter(
            chat_room__members__user=self.request.user,
            chat_room__members__is_active=True
        )


class MessageSearchView(generics.ListAPIView):
    """Search messages"""
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = MessageSerializer

    def get_queryset(self):
        query = self.request.query_params.get('q', '')
        room_id = self.request.query_params.get('room_id')

        if not query or not room_id:
            return Message.objects.none()

        return Message.objects.filter(
            chat_room_id=room_id,
            chat_room__members__user=self.request.user,
            chat_room__members__is_active=True,
            content__icontains=query
        ).order_by('-created_at')


class MessageStatusView(APIView):
    """Update message read status"""
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request, message_id):
        try:
            message = get_object_or_404(
                Message,
                id=message_id,
                chat_room__members__user=request.user,
                chat_room__members__is_active=True
            )

            MessageReadStatus.objects.get_or_create(
                message=message,
                user=request.user
            )

            return Response({'status': 'read'})

        except Exception as e:
            logger.error(f"Error updating message status: {str(e)}")
            return Response({'error': 'Internal server error'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class DraftView(APIView):
    """Handle message drafts"""
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        # Return user's drafts (simplified - could be stored in cache or database)
        return Response({'drafts': []})

    def post(self, request):
        # Save draft (simplified - could be stored in cache or database)
        return Response({'status': 'saved'})


class TypingIndicatorView(APIView):
    """Handle typing indicators"""
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request):
        room_id = request.data.get('room_id')
        is_typing = request.data.get('is_typing', False)

        # This would typically use WebSocket or caching
        # For now, just return success
        return Response({'status': 'updated'})


class MessageReactionView(APIView):
    """Handle message reactions"""
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request, message_id):
        try:
            message = get_object_or_404(
                Message,
                id=message_id,
                chat_room__members__user=request.user,
                chat_room__members__is_active=True
            )

            reaction = request.data.get('reaction')
            if not reaction:
                return Response({'error': 'reaction required'}, status=status.HTTP_400_BAD_REQUEST)

            # Check if reaction already exists
            existing = MessageReaction.objects.filter(
                message=message,
                user=request.user,
                reaction=reaction
            ).first()

            if existing:
                existing.delete()
                action = 'removed'
            else:
                MessageReaction.objects.create(
                    message=message,
                    user=request.user,
                    reaction=reaction
                )
                action = 'added'

            # Get updated reaction counts
            reactions = MessageReaction.objects.filter(message=message).values('reaction').annotate(
                count=Count('reaction')
            ).order_by('reaction')

            reaction_data = {r['reaction']: r['count'] for r in reactions}

            return Response({
                'action': action,
                'reactions': reaction_data
            })

        except Exception as e:
            logger.error(f"Error handling reaction: {str(e)}")
            return Response({'error': 'Internal server error'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class ConversationListView(generics.ListAPIView):
    """List user conversations"""
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return ChatRoom.objects.filter(
            members__user=self.request.user,
            is_active=True
        ).distinct().prefetch_related('members__user', 'messages')
