"""
Comment API endpoints for live feed commenting system
Allows users to comment on projects without needing to connect
"""

from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from django.utils import timezone
from .models import Comment, Project, Activity
from .views import create_notification
import logging

logger = logging.getLogger(__name__)


@login_required
def add_comment(request, project_id):
    """
    Add a comment to a project
    POST /accounts/api/projects/<project_id>/comments/
    Body: {'content': 'Great project!'}
    """
    if request.method != 'POST':
        return JsonResponse({'error': 'Method not allowed'}, status=405)
    
    try:
        project = Project.objects.get(id=project_id)
        
        # Get comment content from JSON or POST data
        content = None
        if request.content_type == 'application/json':
            import json
            try:
                data = json.loads(request.body)
                content = data.get('content', '').strip()
            except:
                pass
        
        if not content:
            content = request.POST.get('content', '').strip()
        
        if not content:
            return JsonResponse({'error': 'Comment cannot be empty'}, status=400)
        
        if len(content) > 1000:
            return JsonResponse({'error': 'Comment too long (max 1000 characters)'}, status=400)
        
        # Create comment
        comment = Comment.objects.create(
            user=request.user,
            project=project,
            content=content
        )
        
        # Create activity log
        Activity.objects.create(
            user=request.user,
            activity_type='comment_added',
            title=f'Commented on "{project.title}"',
            description=content[:100],
            project=project,
            is_public=True
        )
        
        # Create notification for project owner if not the same user
        if project.user != request.user:
            try:
                create_notification(
                    user=project.user,
                    notification_type='project_comment',
                    title=f'{request.user.username} commented on your project',
                    message=f'"{project.title}": {content[:100]}...',
                    from_user=request.user
                )
            except Exception as e:
                logger.warning(f"Failed to create notification: {e}")
        
        # Prepare response with user profile photo
        profile_photo = ''
        try:
            if hasattr(request.user, 'student_profile') and request.user.student_profile.profile_photo:
                profile_photo = request.user.student_profile.profile_photo.url
        except:
            pass
        
        return JsonResponse({
            'success': True,
            'comment': {
                'id': comment.id,
                'content': comment.content,
                'user': {
                    'id': request.user.id,
                    'username': request.user.username,
                    'profile_photo': profile_photo
                },
                'created_at': comment.created_at.isoformat(),
                'formatted_time': comment.created_at.strftime('%b %d, %Y %I:%M %p')
            }
        })
    
    except Project.DoesNotExist:
        return JsonResponse({'error': 'Project not found'}, status=404)
    except Exception as e:
        logger.error(f"Error adding comment: {str(e)}")
        return JsonResponse({'error': 'Failed to add comment'}, status=500)


@login_required
def get_comments(request, project_id):
    """
    Get all comments for a project
    GET /accounts/api/projects/<project_id>/comments/
    """
    try:
        project = Project.objects.get(id=project_id)
        
        # Get all comments with user profile data
        comments = Comment.objects.filter(project=project).select_related(
            'user__student_profile'
        ).order_by('-created_at')
        
        comments_data = []
        for comment in comments:
            profile_photo = ''
            full_name = comment.user.username
            
            try:
                if comment.user.student_profile:
                    if comment.user.student_profile.profile_photo:
                        profile_photo = comment.user.student_profile.profile_photo.url
                    if comment.user.student_profile.full_name:
                        full_name = comment.user.student_profile.full_name
            except:
                pass
            
            comments_data.append({
                'id': comment.id,
                'content': comment.content,
                'user': {
                    'id': comment.user.id,
                    'username': comment.user.username,
                    'full_name': full_name,
                    'profile_photo': profile_photo
                },
                'created_at': comment.created_at.isoformat(),
                'formatted_time': comment.created_at.strftime('%b %d, %Y %I:%M %p'),
                'can_delete': request.user == comment.user or request.user == project.user,
                'can_edit': request.user == comment.user
            })
        
        return JsonResponse({
            'success': True,
            'count': len(comments_data),
            'comments': comments_data
        })
    
    except Project.DoesNotExist:
        return JsonResponse({'error': 'Project not found'}, status=404)
    except Exception as e:
        logger.error(f"Error fetching comments: {str(e)}")
        return JsonResponse({'error': 'Failed to fetch comments'}, status=500)


@login_required
def delete_comment(request, comment_id):
    """
    Delete a comment
    DELETE /accounts/api/comments/<comment_id>/
    """
    if request.method not in ['DELETE', 'POST']:
        return JsonResponse({'error': 'Method not allowed'}, status=405)
    
    try:
        comment = Comment.objects.get(id=comment_id)
        project = comment.project
        
        # Check permissions
        if request.user != comment.user and request.user != project.user:
            return JsonResponse({'error': 'Permission denied'}, status=403)
        
        comment.delete()
        return JsonResponse({'success': True, 'message': 'Comment deleted'})
    
    except Comment.DoesNotExist:
        return JsonResponse({'error': 'Comment not found'}, status=404)
    except Exception as e:
        logger.error(f"Error deleting comment: {str(e)}")
        return JsonResponse({'error': 'Failed to delete comment'}, status=500)


@login_required
def edit_comment(request, comment_id):
    """
    Edit a comment
    PUT/POST /accounts/api/comments/<comment_id>/
    Body: {'content': 'Updated comment'}
    """
    if request.method not in ['PUT', 'POST']:
        return JsonResponse({'error': 'Method not allowed'}, status=405)
    
    try:
        comment = Comment.objects.get(id=comment_id)
        
        # Check if user can edit
        if request.user != comment.user:
            return JsonResponse({'error': 'Permission denied'}, status=403)
        
        # Get new content
        content = None
        if request.content_type == 'application/json':
            import json
            try:
                data = json.loads(request.body)
                content = data.get('content', '').strip()
            except:
                pass
        
        if not content:
            content = request.POST.get('content', '').strip()
        
        if not content:
            return JsonResponse({'error': 'Comment cannot be empty'}, status=400)
        
        if len(content) > 1000:
            return JsonResponse({'error': 'Comment too long (max 1000 characters)'}, status=400)
        
        comment.content = content
        comment.save(update_fields=['content'])
        
        return JsonResponse({
            'success': True,
            'comment': {
                'id': comment.id,
                'content': comment.content,
                'updated_at': comment.updated_at.isoformat()
            }
        })
    
    except Comment.DoesNotExist:
        return JsonResponse({'error': 'Comment not found'}, status=404)
    except Exception as e:
        logger.error(f"Error editing comment: {str(e)}")
        return JsonResponse({'error': 'Failed to edit comment'}, status=500)
