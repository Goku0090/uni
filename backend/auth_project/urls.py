from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from accounts import views
from accounts.views import (
    register_view, login_view, logout_view,
    dashboard_view, home_view, student_details_view,
    main, verify_otp_view, forgot_password_view, reset_password_view
)

urlpatterns = [
    path('admin/', admin.site.urls),
    path('accounts/', include('accounts.urls')),  # Custom accounts URLs first
    path('accounts/', include('allauth.urls')),  # Allauth URLs second
    path('api/', include('accounts.urls')),  # API routes - include only ONCE
    path('dashboard/', views.dashboard_view, name='dashboard'),
    path('home/', views.home_view, name='home'),
    path('register/', views.register_view, name='register'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('student-details/', student_details_view, name='student_details'),
    path('verify-otp/<str:purpose>/', verify_otp_view, name='verify_otp'),
    path('forgot-password/', forgot_password_view, name='forgot_password'),
    path('reset-password/', reset_password_view, name='reset_password'),
    path('resend-otp/<str:purpose>/', views.resend_otp_view, name='resend_otp'),
    path('main_home/', views.main_home, name='main_home'),

    path('post-project/', views.post_project, name='post_project'),
    path('project/<int:project_id>/', views.project_detail, name='project_detail'),
    path('edit-project/<int:project_id>/', views.edit_project, name='edit_project'),
    path('delete-project/<int:project_id>/', views.delete_project, name='delete_project'),
    path('my-projects/', views.my_projects_view, name='my_projects'),
    path('explore-projects/', views.explore_projects_view, name='explore_projects'),
    path('messages/', views.message_view, name='messages'),
    path('chat/<int:user_id>/', views.chat_view, name='chat'),
    path('notifications/', views.notifications_view, name='notifications'),
    path('notification/<int:notification_id>/read/', views.mark_notification_read, name='mark_notification_read'),
    path('profile/', views.profile_view, name='profile'),
    path('premium/', views.premium_view, name='premium'),
    path('upgrade/', views.upgrade_view, name='upgrade'),
    path('investor-dashboard/', views.investor_dashboard, name='investor_dashboard'),
    path('accounts/profile/', views.social_login_redirect, name='social_login_redirect'),
    # other routes like register, login, etc.
    path('student-profile/', views.student_profile, name='student_profile'),
    path('find-collaborators/', views.find_collaborators, name='find_collaborators'),
    path('about/', views.about_view, name='about'),

    # Connection routes
    path('connect/<int:user_id>/', views.send_connection_request, name='send_connection'),
    path('accept-connection/<int:connection_id>/', views.accept_connection, name='accept_connection'),
    path('reject-connection/<int:connection_id>/', views.reject_connection, name='reject_connection'),
    path('my-connections/', views.my_connections, name='my_connections'),

    # File download route
    path('download-file/<int:file_id>/', views.download_file, name='download_file'),

    # Catch-all route for homepage - must be last
    path('', views.main, name='main'),
]

if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
