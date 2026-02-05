# CORRECT project_detail() view for your actual model structure
# Replace lines 1697-1824 in e:/login/auth_project/accounts/views.py with this

@login_required
def project_detail(request, project_id):
    """View project details - CORRECTED FOR ACTUAL MODELS"""
    
    # Load project with optimizations for actual model structure
    project = get_object_or_404(
        Project.objects.select_related(
            'user__student_profile'
        ).prefetch_related(
            'comments__user__student_profile',
            'members__user__student_profile',  # ProjectMember relation
            'invitations__invited_user__student_profile',  # ProjectInvitation relation
            'tasks',
            'milestones',
            'likes'
        ),
        id=project_id
    )

    # Handle comment submission
    if request.method == 'POST' and 'comment_content' in request.POST:
        if request.user.is_authenticated:
            comment_content = request.POST.get('comment_content', '').strip()
            if comment_content and len(comment_content) <= 1000:
                Comment.objects.create(
                    user=request.user,
                    project=project,
                    content=comment_content
                )
                messages.success(request, 'Comment added successfully!')
                return redirect('project_detail', project_id=project_id)

    # Process technologies
    tech_list = project.get_technologies_list() if hasattr(project, 'get_technologies_list') else []
    looking_list = project.get_looking_for_list() if hasattr(project, 'get_looking_for_list') else []

    # Paginate comments (20 per page instead of loading all)
    all_comments = project.comments.select_related('user__student_profile').order_by('-created_at')
    paginator = Paginator(all_comments, 20)
    comments_page_obj = paginator.get_page(request.GET.get('comment_page', 1))

    # Check connection status
    is_connected = False
    connection_status = None
    
    if request.user.is_authenticated and request.user != project.user:
        try:
            connection = Connection.objects.filter(
                Q(sender=request.user, receiver=project.user) |
                Q(sender=project.user, receiver=request.user)
            ).only('status').first()
            
            if connection:
                is_connected = connection.status == 'accepted'
                connection_status = connection.status
        except Connection.DoesNotExist:
            pass

    # Team information - USE ProjectMember (actual model), NOT ProjectTeam
    team_members = []
    user_team_role = None
    can_manage_team = False
    pending_invitations = []

    try:
        # Get all active project members
        team_members = [
            m for m in project.members.all() 
            if m.is_active
        ]

        # Find current user's role in project
        user_membership = None
        for member in team_members:
            if member.user_id == request.user.id:
                user_membership = member
                break

        if user_membership:
            user_team_role = user_membership.role
            can_manage_team = user_membership.can_manage_project
        else:
            can_manage_team = request.user == project.user

        # Get pending invitations if user can manage team
        if can_manage_team:
            pending_invitations = [
                i for i in project.invitations.all() 
                if i.status == 'pending'
            ]

    except (AttributeError, Exception) as e:
        # Fallback if anything goes wrong
        can_manage_team = request.user == project.user

    # Tasks and milestones (already prefetched)
    all_tasks = list(project.tasks.all().order_by('created_at'))
    all_milestones = list(project.milestones.all().order_by('created_at'))

    # Calculate statistics FROM LOADED DATA (no additional queries)
    completed_tasks_count = sum(1 for task in all_tasks if task.status == 'completed')
    total_tasks_count = len(all_tasks)

    # Task status breakdown
    task_status_dict = {}
    for task in all_tasks:
        status = task.status
        if status not in task_status_dict:
            task_status_dict[status] = 0
        task_status_dict[status] += 1

    task_status_counts = [
        {'status': s, 'label': l, 'count': task_status_dict.get(s, 0)}
        for s, l in ProjectTask.STATUS_CHOICES
        if s in task_status_dict
    ]

    # Milestone statistics
    completed_milestones_count = sum(1 for m in all_milestones if m.is_completed)
    total_milestones_count = len(all_milestones)

    # Get potential team members
    potential_members = []
    
    if can_manage_team and request.user.is_authenticated:
        existing_member_ids = {m.user_id for m in team_members} if team_members else set()
        existing_member_ids.add(project.user.id)

        connected_users = Connection.objects.filter(
            Q(sender=request.user, status='accepted') |
            Q(receiver=request.user, status='accepted')
        ).select_related('sender__student_profile', 'receiver__student_profile')

        seen_ids = set()
        for conn in connected_users:
            other_user = conn.receiver if conn.sender_id == request.user.id else conn.sender
            
            if other_user.id not in existing_member_ids and other_user.id not in seen_ids:
                potential_members.append(other_user)
                seen_ids.add(other_user.id)

    return render(request, 'project_detail.html', {
        'project': project,
        'tech_list': tech_list,
        'looking_list': looking_list,
        'comments': comments_page_obj,
        'is_owner': request.user == project.user if request.user.is_authenticated else False,
        'is_connected': is_connected,
        'connection_status': connection_status,
        'team_members': team_members,
        'user_team_role': user_team_role,
        'can_manage_team': can_manage_team,
        'pending_invitations': pending_invitations,
        'potential_members': potential_members,
        'tasks': all_tasks,
        'milestones': all_milestones,
        'completed_tasks_count': completed_tasks_count,
        'total_tasks_count': total_tasks_count,
        'task_status_counts': task_status_counts,
        'completed_milestones_count': completed_milestones_count,
        'total_milestones_count': total_milestones_count,
    })
