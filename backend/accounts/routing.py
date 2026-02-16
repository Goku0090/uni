"""
WebSocket routing for real-time project updates
Handles connections for live project status updates and notifications
"""

from django.urls import re_path
from . import consumers

websocket_urlpatterns = [
    # Project updates WebSocket
    # URL: ws://localhost:8000/ws/project/<project_id>/
    re_path(r'ws/project/(?P<project_id>\w+)/$', consumers.ProjectUpdateConsumer.as_asgi()),
    
    # Activity feed WebSocket
    # URL: ws://localhost:8000/ws/activity-feed/
    re_path(r'ws/activity-feed/$', consumers.ActivityFeedConsumer.as_asgi()),
    
    # Notifications WebSocket
    # URL: ws://localhost:8000/ws/notifications/
    re_path(r'ws/notifications/$', consumers.NotificationConsumer.as_asgi()),
]
