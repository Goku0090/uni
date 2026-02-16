"""
Custom permissions for the accounts app
"""

from rest_framework import permissions
from django.shortcuts import get_object_or_404
from .models import ChatRoom, ChatRoomMember, Project, ProjectTeamMember


class IsChatRoomMember(permissions.BasePermission):
    """
    Custom permission to only allow members of a chat room to access it.
    """

    def has_object_permission(self, request, view, obj):
        # Check if user is a member of the chat room
        return ChatRoomMember.objects.filter(
            chat_room=obj,
            user=request.user,
            is_active=True
        ).exists()


class IsProjectOwnerOrTeamMember(permissions.BasePermission):
    """
    Custom permission to only allow project owners or team members to access project.
    """

    def has_object_permission(self, request, view, obj):
        # Check if user is project owner
        if obj.user == request.user:
            return True

        # Check if user is a team member
        return ProjectTeamMember.objects.filter(
            team__project=obj,
            user=request.user,
            is_active=True
        ).exists()


def check_chat_room_member(view_func):
    """
    Decorator to check if user is a member of the chat room
    """
    def wrapper(request, room_id, *args, **kwargs):
        chat_room = get_object_or_404(ChatRoom, id=room_id)

        # Check if user is a member of this chat room
        if not ChatRoomMember.objects.filter(
            chat_room=chat_room,
            user=request.user,
            is_active=True
        ).exists():
            from django.http import HttpResponseForbidden
            return HttpResponseForbidden("You don't have access to this chat room.")

        return view_func(request, room_id, *args, **kwargs)
    return wrapper


def check_project_owner(view_func):
    """
    Decorator to check if user owns the project
    """
    def wrapper(request, project_id, *args, **kwargs):
        project = get_object_or_404(Project, id=project_id)

        if project.user != request.user:
            from django.http import HttpResponseForbidden
            return HttpResponseForbidden("You don't have permission to access this project.")

        return view_func(request, project_id, *args, **kwargs)
    return wrapper


def check_team_owner(view_func):
    """
    Decorator to check if user is a team owner/admin
    """
    def wrapper(request, project_id, *args, **kwargs):
        project = get_object_or_404(Project, id=project_id)

        # Check if user is project owner
        if project.user == request.user:
            return view_func(request, project_id, *args, **kwargs)

        # Check if user is team owner/admin
        try:
            team_member = ProjectTeamMember.objects.get(
                team__project=project,
                user=request.user,
                is_active=True
            )
            if team_member.role in ['owner', 'admin']:
                return view_func(request, project_id, *args, **kwargs)
        except ProjectTeamMember.DoesNotExist:
            pass

        from django.http import HttpResponseForbidden
        return HttpResponseForbidden("You don't have permission to manage this team.")
    return wrapper


def check_chat_membership(user, chat_room):
    """
    Utility function to check if user is member of chat room
    """
    return ChatRoomMember.objects.filter(
        chat_room=chat_room,
        user=user,
        is_active=True
    ).exists()


def check_project_ownership(user, project):
    """
    Utility function to check if user owns the project
    """
    return project.user == user


def check_team_membership(user, project):
    """
    Utility function to check if user is a team member
    """
    return ProjectTeamMember.objects.filter(
        team__project=project,
        user=user,
        is_active=True
    ).exists()


def check_can_edit_project(user, project):
    """
    Utility function to check if user can edit the project
    """
    # Project owner can edit
    if project.user == user:
        return True

    # Team owners/admins can edit
    try:
        team_member = ProjectTeamMember.objects.get(
            team__project=project,
            user=user,
            is_active=True
        )
        return team_member.role in ['owner', 'admin']
    except ProjectTeamMember.DoesNotExist:
        return False


def verify_project_ownership(request, project_id):
    """
    Verify user owns the project, return project if valid
    """
    from django.shortcuts import get_object_or_404

    project = get_object_or_404(Project, id=project_id)

    if project.user != request.user:
        from django.http import HttpResponseForbidden
        raise HttpResponseForbidden("You don't own this project.")

    return project


def verify_team_membership(request, project_id):
    """
    Verify user is a team member, return team member if valid
    """
    from django.shortcuts import get_object_or_404

    project = get_object_or_404(Project, id=project_id)

    try:
        team_member = ProjectTeamMember.objects.get(
            team__project=project,
            user=request.user,
            is_active=True
        )
        return team_member
    except ProjectTeamMember.DoesNotExist:
        from django.http import HttpResponseForbidden
        raise HttpResponseForbidden("You are not a member of this project team.")


def verify_chat_membership(request, room_id):
    """
    Verify user is a chat room member, return membership if valid
    """
    from django.shortcuts import get_object_or_404

    chat_room = get_object_or_404(ChatRoom, id=room_id)

    try:
        membership = ChatRoomMember.objects.get(
            chat_room=chat_room,
            user=request.user,
            is_active=True
        )
        return membership
    except ChatRoomMember.DoesNotExist:
        from django.http import HttpResponseForbidden
        raise HttpResponseForbidden("You are not a member of this chat room.")
