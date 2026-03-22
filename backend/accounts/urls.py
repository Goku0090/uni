from django.urls import path
from . import views
from .views import UserProfileView
from .views_contact import privacy_policy_view, terms_of_service_view, contact_us_view, contact_submit
from .chat_api import (
    ChatRoomListCreateView, ChatRoomDetailView, ChatRoomMembersView,
    DirectMessageView, MessageListCreateView, MessageDetailView,
    MessageSearchView, MessageStatusView, DraftView, TypingIndicatorView,
    MessageReactionView, ConversationListView
)
from .comment_api import add_comment, get_comments, delete_comment, edit_comment
# Template functionality temporarily disabled
# from .template_api import (
#     templates_list_view, template_detail_view, use_template_view,
#     quick_create_from_template, rate_template, get_user_template_rating,
#     ProjectTemplateListView, ProjectTemplateDetailView,
#     api_create_from_template, api_rate_template, get_template_json
# )

urlpatterns = [
    # Main pages
    path('dashboard/', views.dashboard_view, name='dashboard'),
    path('', views.main, name='main'),
    path('privacy/', privacy_policy_view, name='privacy'),
    path('terms/', terms_of_service_view, name='terms'),
    path('contact/', contact_us_view, name='contact'),
    path('contact/submit/', contact_submit, name='contact_submit'),

    # Authentication
    path('login/', views.login_view, name='login'),
    path('register/', views.register_view, name='register'),
    path('logout/', views.logout_view, name='logout'),
    path('forgot-password/', views.forgot_password_view, name='forgot_password'),
    path('reset-password/', views.reset_password_view, name='reset_password'),
    path('verify-otp/<str:purpose>/', views.verify_otp_view, name='verify_otp'),
    path('resend-otp/<str:purpose>/', views.resend_otp_view, name='resend_otp'),

    # Profile
    path('student-details/', views.student_details_view, name='student_details'),
    path('student-profile/', views.student_profile, name='student_profile'),
    path('profile/', UserProfileView.as_view(), name='user-profile'),

    # Main app
    path('help/', views.help_center_view, name='help'),
    path('find-collaborators/', views.find_collaborators, name='find_collaborators'),
    path('post-project/', views.post_project, name='post_project'),
    path('edit-project/<int:project_id>/', views.edit_project, name='edit_project'),
    path('delete-project/<int:project_id>/', views.delete_project, name='delete_project'),
    path('project-detail/<int:project_id>/', views.project_detail, name='project_detail'),
    path('like-project/<int:project_id>/', views.like_project, name='like_project'),

    # Social features
    path('notifications/', views.notifications_view, name='notifications'),
    path('mark-notification-read/<int:notification_id>/', views.mark_notification_read, name='mark_notification_read'),
    path('activity-feed/', views.activity_feed, name='activity_feed'),
    path('user/<str:username>/', views.user_profile, name='user_profile'),
    path('follow/<int:user_id>/', views.follow_user, name='follow_user'),
    path('my-connections/', views.my_connections, name='my_connections'),
    path('connect/<int:user_id>/', views.connect_view, name='connect'),
    path('send-connection/<int:user_id>/', views.connect_view, name='send_connection'),
    path('send-connection-request/<int:user_id>/', views.send_connection_request, name='send_connection_request'),
    path('accept-connection/<int:connection_id>/', views.accept_connection, name='accept_connection'),
    path('reject-connection/<int:connection_id>/', views.reject_connection, name='reject_connection'),
    path('cancel-connection/<int:connection_id>/', views.cancel_connection_request, name='cancel_connection'),

    # Team management
    path('invite-to-team/<int:project_id>/', views.invite_to_team, name='invite_to_team'),
    path('respond-team-invitation/<int:invitation_id>/', views.respond_to_team_invitation, name='respond_team_invitation'),
    path('remove-team-member/<int:project_id>/<int:user_id>/', views.remove_team_member, name='remove_team_member'),

    # Messaging
    path('messages/', views.message_view, name='messages'),
    path('chat/<int:user_id>/', views.chat_view, name='chat'),

    # Enhanced Messaging
    path('enhanced-messages/', views.enhanced_messages_view, name='enhanced_messages'),
    path('enhanced-chat/<int:room_id>/', views.enhanced_chat_view, name='enhanced_chat'),
    path('create-group-chat/', views.create_group_chat, name='create_group_chat'),
    path('add-reaction/<int:message_id>/', views.add_reaction, name='add_reaction'),

    # File handling
    path('download-file/<int:file_id>/', views.download_file, name='download_file'),

    # =============================================
    # REST API ENDPOINTS FOR MESSAGING
    # =============================================

    # Chat Room Management
    path('chat-rooms/', ChatRoomListCreateView.as_view(), name='chat-rooms-list'),
    path('chat-rooms/<int:id>/', ChatRoomDetailView.as_view(), name='chat-room-detail'),
    path('chat-rooms/<int:room_id>/members/', ChatRoomMembersView.as_view(), name='chat-room-members'),
    path('direct-message/', DirectMessageView.as_view(), name='direct-message'),

    # Messages
    path('messages/', MessageListCreateView.as_view(), name='messages-list'),
    path('messages/<int:pk>/', MessageDetailView.as_view(), name='message-detail'),
    path('messages/search/', MessageSearchView.as_view(), name='message-search'),
    path('messages/<int:message_id>/status/', MessageStatusView.as_view(), name='message-status'),
    path('messages/<int:message_id>/reactions/', MessageReactionView.as_view(), name='message-reactions'),

    # Drafts
    path('drafts/', DraftView.as_view(), name='drafts'),

    # Typing Indicators
    path('typing/', TypingIndicatorView.as_view(), name='typing'),

    # Conversations List
    path('conversations/', ConversationListView.as_view(), name='conversations'),

    # =============================================
    # COLLEGE MANAGEMENT APIs
    # =============================================
    path('college-search/', views.college_search_api, name='college_search_api'),
    path('validate-college/', views.validate_college_api, name='validate_college_api'),

    # =============================================
    # LEGACY API ENDPOINTS
    # =============================================

    path('', views.api_root, name='api_root'),
    path('home/', views.home_api, name='home_api'),
    path('check-username/', views.check_username_availability, name='check_username'),
    path('check-email/', views.check_email_availability, name='check_email'),
    path('user-stats/', views.user_stats_api, name='user_stats_api'),
    path('user-profile/<int:user_id>/', views.user_profile_api, name='user_profile_api'),
    path('nlp-analyze/', views.nlp_analyze_api, name='nlp_analyze_api'),
    
    # =============================================
    # COMMENT SYSTEM - LIVE FEED API
    # =============================================
    path('projects/<int:project_id>/comments/', get_comments, name='get-comments'),
    path('projects/<int:project_id>/comments/add/', add_comment, name='add-comment'),
    path('comments/<int:comment_id>/delete/', delete_comment, name='delete-comment'),
    path('comments/<int:comment_id>/edit/', edit_comment, name='edit-comment'),

    # =============================================
    # TEMPLATE ROUTES TEMPORARILY DISABLED
    # =============================================
    # All template routes removed for now
    # To re-enable, uncomment template_api imports and re-add these routes
    
    # Newsletter subscription
    path('newsletter/subscribe/', views.newsletter_subscribe, name='newsletter_subscribe'),
]
