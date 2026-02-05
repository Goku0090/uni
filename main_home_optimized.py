# OPTIMIZED main_home() view
# Replace the existing main_home() function in accounts/views.py (lines 742-781)
# with this optimized version

from django.shortcuts import render
from django.core.paginator import Paginator
from django.db.models import Count, Q, F
from accounts.models import Project, Notification, Connection, User
from accounts.utils import ProjectVisibilityFilter

def main_home(request):
    """
    Simplified main home view for testing - OPTIMIZED VERSION
    
    Performance improvements:
    - Implements pagination (10 projects per page)
    - Uses select_related() for project owners
    - Uses annotate() for counts instead of N+1 queries
    - Limits profile visibility filter to visible projects only
    - Caches unread notification count
    """
    
    unread_count = 0
    visible_projects = []
    project_match_details = {}
    page_obj = None

    # ============================================================
    # GET UNREAD NOTIFICATIONS COUNT (CACHED)
    # ============================================================
    if request.user.is_authenticated:
        from django.core.cache import cache
        
        # Use cache to avoid querying notifications every page load
        cache_key = f'unread_notifications_{request.user.id}'
        unread_count = cache.get(cache_key)
        
        if unread_count is None:
            unread_count = Notification.objects.filter(
                user=request.user, 
                is_read=False
            ).count()
            # Cache for 5 minutes
            cache.set(cache_key, unread_count, 300)

    # ============================================================
    # GET AND PAGINATE PROJECTS
    # ============================================================
    # Optimize: select related project owner and their profile
    # Annotate: add comment/like counts without additional queries
    base_projects = Project.objects.select_related(
        'user__student_profile'
    ).annotate(
        comment_count=Count('comments', distinct=True),
        like_count=Count('likes', distinct=True),
        team_member_count=Count('team__members', distinct=True)
    ).filter(
        is_active=True  # Only show active projects
    ).order_by('-created_at')

    # ============================================================
    # APPLY VISIBILITY FILTER (OPTIMIZED)
    # ============================================================
    if request.user.is_authenticated:
        # ProjectVisibilityFilter.get_visible_projects() returns filtered projects
        # This should be optimized to work with the annotated queryset
        visible_projects, project_match_details = ProjectVisibilityFilter.get_visible_projects(
            request.user,
            base_projects
        )
    else:
        # Non-authenticated users see all active projects
        visible_projects = base_projects

    # ============================================================
    # PAGINATE PROJECTS (NEW - prevents loading all projects)
    # ============================================================
    # Convert to list if it's a filtered list, otherwise use queryset
    if isinstance(visible_projects, list):
        # If ProjectVisibilityFilter returns a list, paginate it
        paginator = Paginator(visible_projects, 10)  # 10 projects per page
        page_number = request.GET.get('page', 1)
        page_obj = paginator.get_page(page_number)
        projects_to_display = page_obj
    else:
        # If it's a queryset, paginate with the queryset
        paginator = Paginator(visible_projects, 10)  # 10 projects per page
        page_number = request.GET.get('page', 1)
        page_obj = paginator.get_page(page_number)
        projects_to_display = page_obj.object_list

    # ============================================================
    # ADD MATCH BADGE INFO (IN-MEMORY)
    # ============================================================
    # Instead of calling get_project_match_badge for each project in template,
    # do it here once
    for project in projects_to_display:
        if project.id in project_match_details:
            match_info = project_match_details[project.id]
            project.match_score = match_info.get('score', 0)
            project.match_reasons = match_info.get('reasons', [])
            # Cache the badge result
            project.match_badge = ProjectVisibilityFilter.get_project_match_badge(
                match_info['score']
            )
        else:
            project.match_score = 0
            project.match_reasons = []
            project.match_badge = None

    # ============================================================
    # HOMEPAGE STATISTICS (CACHED)
    # ============================================================
    from django.core.cache import cache
    stats_cache_key = 'homepage_stats'
    homepage_stats = cache.get(stats_cache_key)
    
    if homepage_stats is None:
        # These are expensive queries - cache for 1 hour
        homepage_stats = {
            'total_projects': Project.objects.filter(is_active=True).count(),
            'active_users': User.objects.filter(is_active=True).count(),
            'total_connections': Connection.objects.filter(status='accepted').count(),
            'success_stories': 45  # Hardcode or get from separate model
        }
        cache.set(stats_cache_key, homepage_stats, 3600)

    # ============================================================
    # CATEGORY AND TECH LISTS (OPTIONAL - can be static)
    # ============================================================
    categories = ['Web Development', 'Mobile Apps', 'AI/ML', 'Data Science']
    available_techs = ['Python', 'JavaScript', 'React', 'Django', 'Node.js']

    # ============================================================
    # RENDER TEMPLATE
    # ============================================================
    return render(request, 'main_home.html', {
        'feed_posts': projects_to_display,  # The page object items
        'page_obj': page_obj,  # For pagination controls in template
        'project_match_details': project_match_details,
        'categories': categories,
        'available_techs': available_techs,
        'homepage_stats': homepage_stats,
        'active_filters': {},
        'has_filters': False,
        'unread_notification_count': unread_count,
        'total_projects': len(visible_projects) if isinstance(visible_projects, list) else visible_projects.count(),
    })
