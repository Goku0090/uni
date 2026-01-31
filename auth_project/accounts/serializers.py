"""
Serializers for the accounts app
Provides API serialization for models
"""

from rest_framework import serializers
from .models import StudentProfile, Project, Message, Connection, Notification


class UserProfileSerializer(serializers.ModelSerializer):
    """
    Serializer for StudentProfile model
    Provides user profile information for API responses
    """
    username = serializers.CharField(source='user.username', read_only=True)
    email = serializers.EmailField(source='user.email', read_only=True)
    full_name = serializers.CharField(source='user.get_full_name', read_only=True)
    date_joined = serializers.DateTimeField(source='user.date_joined', read_only=True)
    is_online = serializers.BooleanField(read_only=True)

    class Meta:
        model = StudentProfile
        fields = [
            'id', 'username', 'email', 'full_name', 'date_joined',
            'college', 'location', 'interests', 'bio', 'profile_photo',
            'skills', 'project_interests', 'role_preference',
            'github', 'linkedin', 'portfolio', 'behance',
            'profile_completed', 'is_online'
        ]
        read_only_fields = ['id', 'profile_completed']


class ProjectSerializer(serializers.ModelSerializer):
    """
    Serializer for Project model
    """
    owner = UserProfileSerializer(read_only=True)
    likes_count = serializers.SerializerMethodField()
    comments_count = serializers.SerializerMethodField()

    class Meta:
        model = Project
        fields = [
            'id', 'title', 'description', 'technologies', 'looking_for',
            'category', 'timeline', 'collaboration_needs', 'github_link',
            'created_at', 'updated_at', 'owner', 'likes_count', 'comments_count'
        ]
        read_only_fields = ['id', 'created_at', 'updated_at']

    def get_likes_count(self, obj):
        return obj.likes.count()

    def get_comments_count(self, obj):
        return obj.comments.count()


class MessageSerializer(serializers.ModelSerializer):
    """
    Serializer for Message model
    """
    sender = UserProfileSerializer(read_only=True)
    reactions = serializers.SerializerMethodField()

    class Meta:
        model = Message
        fields = [
            'id', 'content', 'sender', 'created_at', 'is_read',
            'message_type', 'reactions'
        ]
        read_only_fields = ['id', 'created_at']

    def get_reactions(self, obj):
        reactions = obj.reactions.values('reaction').annotate(
            count=serializers.Count('reaction')
        ).order_by('reaction')
        return {r['reaction']: r['count'] for r in reactions}


class ConnectionSerializer(serializers.ModelSerializer):
    """
    Serializer for Connection model
    """
    sender = UserProfileSerializer(read_only=True)
    receiver = UserProfileSerializer(read_only=True)

    class Meta:
        model = Connection
        fields = [
            'id', 'sender', 'receiver', 'status', 'created_at'
        ]
        read_only_fields = ['id', 'created_at']


class NotificationSerializer(serializers.ModelSerializer):
    """
    Serializer for Notification model
    """
    from_user = UserProfileSerializer(read_only=True)

    class Meta:
        model = Notification
        fields = [
            'id', 'notification_type', 'title', 'message',
            'from_user', 'created_at', 'is_read'
        ]
        read_only_fields = ['id', 'created_at']
