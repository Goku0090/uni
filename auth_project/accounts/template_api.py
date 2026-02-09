"""
Project Templates API
Handles listing, selecting, and rating project templates
"""

from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.views.decorators.http import require_http_methods
from rest_framework import generics, permissions
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes

from .models import (
    ProjectTemplate, TemplateRating, TemplateUsageLog, Project
)
from .serializers import ProjectTemplateSerializer
import json
import logging

logger = logging.getLogger(__name__)


# ============================================================================
# TEMPLATE LISTING & BROWSING
# ============================================================================

@login_required
def templates_list_view(request):
    """Display all project templates"""
    templates = ProjectTemplate.objects.filter(is_active=True)
    
    # Filter by category
    category = request.GET.get('category')
    if category:
        templates = templates.filter(category=category)
    
    # Sort options
    sort = request.GET.get('sort', '-rating')  # Default: highest rated
    if sort in ['-rating', 'usage_count', '-usage_count', 'difficulty_level', 'name']:
        templates = templates.order_by(sort)
    
    # Get user's ratings for templates (for UI display)
    user_ratings = {}
    if request.user.is_authenticated:
        ratings = TemplateRating.objects.filter(
            user=request.user
        ).values('template_id', 'rating')
        user_ratings = {r['template_id']: r['rating'] for r in ratings}
    
    categories = ProjectTemplate.TEMPLATE_CATEGORIES
    
    context = {
        'templates': templates,
        'categories': categories,
        'selected_category': category,
        'selected_sort': sort,
        'user_ratings': user_ratings,
    }
    
    return render(request, 'accounts/templates_list.html', context)


@login_required  # Web view requires login to see all template details
def template_detail_view(request, template_id):
    """View template details and related example projects"""
    template = get_object_or_404(ProjectTemplate, id=template_id, is_active=True)
    
    # Get user's rating if they have one
    user_rating = None
    if request.user.is_authenticated:
        user_rating = TemplateRating.objects.filter(
            template=template,
            user=request.user
        ).first()
    
    # Get recent usage
    recent_usages = TemplateUsageLog.objects.filter(
        template=template
    ).select_related('user')[:5]
    
    # Get all ratings
    ratings = template.user_ratings.all().order_by('-created_at')
    
    context = {
        'template': template,
        'user_rating': user_rating,
        'ratings': ratings,
        'recent_usages': recent_usages,
        'rating_distribution': get_rating_distribution(template),
    }
    
    return render(request, 'accounts/template_detail.html', context)


def get_rating_distribution(template):
    """Get distribution of ratings (1-5 stars) with percentages"""
    distribution = {i: {'count': 0, 'percentage': 0} for i in range(1, 6)}
    
    ratings = TemplateRating.objects.filter(template=template)
    total_ratings = ratings.count()
    
    if total_ratings == 0:
        return distribution
    
    # Count ratings by star level
    for rating in ratings:
        distribution[rating.rating]['count'] += 1
    
    # Calculate percentages
    for stars in distribution:
        distribution[stars]['percentage'] = (distribution[stars]['count'] / total_ratings) * 100
    
    return distribution


# ============================================================================
# USING TEMPLATES TO CREATE PROJECTS
# ============================================================================

@login_required
def use_template_view(request, template_id):
    """Use a template to start creating a project"""
    template = get_object_or_404(ProjectTemplate, id=template_id, is_active=True)
    
    if request.method == 'POST':
        try:
            # Create project from template
            project = Project.objects.create(
                user=request.user,
                title=request.POST.get('title', template.template_title),
                description=request.POST.get('description', template.template_description),
                category=request.POST.get('category', template.category),
                technologies=json.loads(request.POST.get(
                    'technologies', 
                    json.dumps(template.template_technologies)
                )),
                looking_for=json.loads(request.POST.get(
                    'looking_for',
                    json.dumps(template.template_looking_for)
                )),
                collaboration_needs=request.POST.get(
                    'collaboration_needs',
                    template.template_collaboration_needs or ''
                ),
                timeline=request.POST.get('timeline', template.suggested_timeline or ''),
            )
            
            # Log template usage
            TemplateUsageLog.objects.create(
                template=template,
                user=request.user,
                project=project
            )
            
            # Increment template usage count
            template.increment_usage()
            
            # Redirect to edit project
            from django.urls import reverse
            return redirect('edit_project', project_id=project.id)
        
        except Exception as e:
            logger.error(f"Error creating project from template: {str(e)}")
            return JsonResponse({
                'error': f'Failed to create project: {str(e)}'
            }, status=400)
    
    # GET request - show template preview with form
    context = {
        'template': template,
    }
    
    return render(request, 'accounts/use_template.html', context)


# ============================================================================
# TEMPLATE QUICK START (AJAX)
# ============================================================================

@login_required
@require_http_methods(["POST"])
def quick_create_from_template(request, template_id):
    """Quick create a project from template (AJAX)"""
    try:
        template = ProjectTemplate.objects.get(id=template_id, is_active=True)
        
        # Get form data
        data = json.loads(request.body)
        
        # Create project
        project = Project.objects.create(
            user=request.user,
            title=data.get('title', template.template_title),
            description=data.get('description', template.template_description),
            category=data.get('category', template.category),
            technologies=data.get('technologies', template.template_technologies),
            looking_for=data.get('looking_for', template.template_looking_for),
            collaboration_needs=data.get('collaboration_needs', ''),
            timeline=data.get('timeline', template.suggested_timeline or ''),
        )
        
        # Log usage
        TemplateUsageLog.objects.create(
            template=template,
            user=request.user,
            project=project
        )
        
        template.increment_usage()
        
        return JsonResponse({
            'success': True,
            'project_id': project.id,
            'message': 'Project created successfully!',
            'redirect_url': f'/edit-project/{project.id}/'
        })
    
    except ProjectTemplate.DoesNotExist:
        return JsonResponse({'error': 'Template not found'}, status=404)
    except Exception as e:
        logger.error(f"Error in quick_create_from_template: {str(e)}")
        return JsonResponse({'error': str(e)}, status=400)


# ============================================================================
# TEMPLATE RATINGS
# ============================================================================

@login_required
@require_http_methods(["POST"])
def rate_template(request, template_id):
    """Rate a project template"""
    try:
        template = ProjectTemplate.objects.get(id=template_id, is_active=True)
        data = json.loads(request.body)
        
        rating = int(data.get('rating', 0))
        review = data.get('review', '')
        
        # Validate rating
        if rating < 1 or rating > 5:
            return JsonResponse({'error': 'Rating must be between 1 and 5'}, status=400)
        
        # Create or update rating
        user_rating, created = TemplateRating.objects.update_or_create(
            template=template,
            user=request.user,
            defaults={
                'rating': rating,
                'review': review
            }
        )
        
        # Update template rating
        if created:
            template.update_rating(rating)
        else:
            # Recalculate rating
            all_ratings = TemplateRating.objects.filter(template=template)
            if all_ratings.exists():
                avg_rating = sum(r.rating for r in all_ratings) / len(all_ratings)
                template.rating = avg_rating
                template.save(update_fields=['rating'])
        
        return JsonResponse({
            'success': True,
            'message': 'Rating saved successfully!',
            'new_rating': float(template.rating),
            'rating_count': template.rating_count
        })
    
    except ProjectTemplate.DoesNotExist:
        return JsonResponse({'error': 'Template not found'}, status=404)
    except Exception as e:
        logger.error(f"Error rating template: {str(e)}")
        return JsonResponse({'error': str(e)}, status=400)


@login_required
def get_user_template_rating(request, template_id):
    """Get current user's rating for a template (AJAX)"""
    try:
        template = get_object_or_404(ProjectTemplate, id=template_id)
        rating = TemplateRating.objects.filter(
            template=template,
            user=request.user
        ).first()
        
        if rating:
            return JsonResponse({
                'rating': rating.rating,
                'review': rating.review,
                'created_at': rating.created_at.isoformat()
            })
        else:
            return JsonResponse({'rating': None})
    
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=400)


# ============================================================================
# REST API ENDPOINTS
# ============================================================================

class ProjectTemplateListView(generics.ListAPIView):
    """REST API: List all active templates"""
    queryset = ProjectTemplate.objects.filter(is_active=True).order_by(
        '-is_featured', '-rating', '-usage_count'
    )
    serializer_class = ProjectTemplateSerializer
    permission_classes = [permissions.AllowAny]
    
    def get_queryset(self):
        queryset = super().get_queryset()
        
        # Filter by category
        category = self.request.query_params.get('category')
        if category:
            queryset = queryset.filter(category=category)
        
        # Filter by difficulty
        difficulty = self.request.query_params.get('difficulty')
        if difficulty:
            queryset = queryset.filter(difficulty_level=difficulty)
        
        # Search
        search = self.request.query_params.get('search')
        if search:
            queryset = queryset.filter(
                name__icontains=search
            ) | queryset.filter(
                description__icontains=search
            )
        
        return queryset


class ProjectTemplateDetailView(generics.RetrieveAPIView):
    """REST API: Get template details - Returns JSON"""
    queryset = ProjectTemplate.objects.filter(is_active=True)
    serializer_class = ProjectTemplateSerializer
    permission_classes = [permissions.AllowAny]
    lookup_field = 'id'  # Look up by 'id' not 'pk'
    lookup_url_kwarg = 'pk'  # But URL parameter is 'pk'


# Ultra-simple JSON endpoint (pure Django, no DRF)
from django.views.decorators.csrf import csrf_exempt

@csrf_exempt
def get_template_json(request, template_id):
    """Ultra-simple JSON endpoint - guaranteed to return JSON"""
    try:
        template = ProjectTemplate.objects.get(id=template_id, is_active=True)
        data = {
            'id': template.id,
            'template_title': template.template_title,
            'template_description': template.template_description,
            'category': template.category,
            'difficulty_level': template.difficulty_level,
            'rating': float(template.rating) if template.rating else 0,
            'rating_count': template.rating_count or 0,
            'usage_count': template.usage_count or 0,
            'template_technologies': template.template_technologies or [],
            'template_looking_for': template.template_looking_for or [],
            'suggested_timeline': template.suggested_timeline or '',
            'is_featured': template.is_featured or False,
            'is_active': template.is_active,
        }
        return JsonResponse(data)
    except ProjectTemplate.DoesNotExist:
        return JsonResponse({'error': 'Template not found'}, status=404)
    except Exception as e:
        logger.error(f"Error fetching template: {str(e)}")
        return JsonResponse({'error': str(e)}, status=500)


@api_view(['POST'])
@permission_classes([permissions.IsAuthenticated])
def api_create_from_template(request, template_id):
    """REST API: Create project from template"""
    try:
        template = ProjectTemplate.objects.get(id=template_id, is_active=True)
        
        # Create project
        project = Project.objects.create(
            user=request.user,
            title=request.data.get('title', template.template_title),
            description=request.data.get('description', template.template_description),
            category=request.data.get('category', template.category),
            technologies=request.data.get('technologies', template.template_technologies),
            looking_for=request.data.get('looking_for', template.template_looking_for),
            collaboration_needs=request.data.get('collaboration_needs', ''),
            timeline=request.data.get('timeline', template.suggested_timeline or ''),
        )
        
        # Log usage
        TemplateUsageLog.objects.create(
            template=template,
            user=request.user,
            project=project
        )
        
        template.increment_usage()
        
        return Response({
            'success': True,
            'project_id': project.id,
            'message': 'Project created successfully!'
        })
    
    except ProjectTemplate.DoesNotExist:
        return Response({'error': 'Template not found'}, status=404)
    except Exception as e:
        logger.error(f"Error in API create: {str(e)}")
        return Response({'error': str(e)}, status=400)


@api_view(['POST'])
@permission_classes([permissions.IsAuthenticated])
def api_rate_template(request, template_id):
    """REST API: Rate a template"""
    try:
        template = ProjectTemplate.objects.get(id=template_id, is_active=True)
        
        rating = int(request.data.get('rating', 0))
        review = request.data.get('review', '')
        
        if rating < 1 or rating > 5:
            return Response({'error': 'Rating must be between 1 and 5'}, status=400)
        
        user_rating, created = TemplateRating.objects.update_or_create(
            template=template,
            user=request.user,
            defaults={'rating': rating, 'review': review}
        )
        
        # Update template rating
        if created:
            template.update_rating(rating)
        else:
            all_ratings = TemplateRating.objects.filter(template=template)
            if all_ratings.exists():
                avg_rating = sum(r.rating for r in all_ratings) / len(all_ratings)
                template.rating = avg_rating
                template.save(update_fields=['rating'])
        
        return Response({
            'success': True,
            'new_rating': float(template.rating),
            'rating_count': template.rating_count
        })
    
    except ProjectTemplate.DoesNotExist:
        return Response({'error': 'Template not found'}, status=404)
    except Exception as e:
        return Response({'error': str(e)}, status=400)
