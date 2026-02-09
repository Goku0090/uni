# --- PAGINATION FOR PROJECT LISTS & SEARCH ---
from django.core.paginator import Paginator

# Example usage in a project feed or search view:
def project_feed(request):
    projects = Project.objects.all().order_by('-created_at')
    paginator = Paginator(projects, 10)  # 10 projects per page
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    return render(request, 'accounts/project_feed.html', {'page_obj': page_obj})

# --- DJANGO MESSAGES FOR FEEDBACK (already partially used, ensure everywhere) ---
# Example: messages.success(request, 'Action completed successfully!')

# --- AVATAR DISPLAY IN DASHBOARD & FEEDS ---
# In dashboard and project feed templates, use:
# <img src="{{ project.owner.student_profile.profile_photo.url }}" alt="Avatar" class="avatar">
# --- DOCSTRINGS ADDED FOR MAJOR FUNCTIONS/CLASSES ---
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods
from django.contrib.auth.models import User
from django.contrib import messages
from django.core.mail import EmailMultiAlternatives
from django.conf import settings
from django.utils import timezone
from django.http import JsonResponse, HttpResponse, HttpResponseForbidden, Http404
from django.db import models
from django.db.models import Q
from django.core.cache import cache
from django.views.decorators.cache import cache_page
from rest_framework import generics, permissions
from .serializers import UserProfileSerializer
from .forms import RegisterForm, LoginForm, OTPVerificationForm, StudentProfileForm, ProjectForm
from .models import StudentProfile, OTP, Connection, Message, Notification, Comment, UserStatus, File, MessageFile, MessageReaction, ProjectTeam, ProjectTeamMember, ProjectTeamInvitation, ProjectTask, ProjectMilestone, Activity, Follow, Like, UserStats, ChatRoom, ChatRoomMember, MessageReadStatus, Project
from .utils import StudentProfileNLP, ProjectVisibilityFilter
import random
import logging

# Set up logging
logger = logging.getLogger(__name__)

# Import for contact form
from django.core.mail import send_mail


# --- USER PROFILE EDITING & AVATAR UPLOAD ---
@login_required
def edit_profile(request):
    """Allow users to edit their profile and upload avatar."""
    profile = StudentProfile.objects.get(user=request.user)
    if request.method == 'POST':
        form = StudentProfileForm(request.POST, request.FILES, instance=profile)
        if form.is_valid():
            form.save()
            messages.success(request, 'Profile updated successfully!')
            return redirect('student_profile')
    else:
        form = StudentProfileForm(instance=profile)
    return render(request, 'accounts/edit_profile.html', {'form': form})

# --- PROJECT SEARCH & FILTERING ---
def search_projects(request):
    """Allow users to search and filter projects."""
    query = request.GET.get('q', '')
    projects = Project.objects.all()
    if query:
        projects = projects.filter(
            Q(title__icontains=query) |
            Q(description__icontains=query) |
            Q(collaboration_needs__icontains=query)
        )
    return render(request, 'accounts/search_projects.html', {'projects': projects, 'query': query})

# --- IMPROVED DASHBOARD ---
@login_required
def dashboard_view(request):
    """Show project/activity summary on dashboard."""
    profile = StudentProfile.objects.get(user=request.user)
    user_projects = Project.objects.filter(owner=request.user)
    recent_activities = Activity.objects.filter(user=request.user).order_by('-timestamp')[:10]
    return render(request, 'accounts/dashboard.html', {
        'profile': profile,
        'user_projects': user_projects,
        'recent_activities': recent_activities
    })

# Error handling decorator - Fixed to avoid redirect loops
def handle_view_errors(view_func):
    """
    Decorator to handle exceptions in views and provide user-friendly error messages
    """
    def wrapper(request, *args, **kwargs):
        try:
            return view_func(request, *args, **kwargs)
        except Exception as e:
            logger.error(f"Error in {view_func.__name__}: {str(e)}", exc_info=True)
            messages.error(request, "An unexpected error occurred. Please try again.")
            # Avoid redirect loops - redirect to dashboard instead of main_home
            if request.method == 'POST':
                return redirect(request.META.get('HTTP_REFERER', '/'))
            return redirect('/')
    return wrapper

# Input sanitization function
def sanitize_input(text, max_length=None):
    """
    Sanitize user input to prevent XSS and other attacks
    """
    from django.utils.html import strip_tags
    import re

    if not text:
        return text

    # Convert to string if not already
    text = str(text)

    # Remove HTML tags
    text = strip_tags(text)

    # Remove potentially dangerous characters
    text = re.sub(r'[<>]', '', text)

    # Trim whitespace
    text = text.strip()

    # Apply length limit if specified
    if max_length and len(text) > max_length:
        text = text[:max_length]

    return text

# Send OTP Email (HTML + Plaintext)
def send_otp_email(email, otp_code, purpose):
    subject = f"🚀 - Your {purpose.title()} OTP Code"
    from_email = settings.DEFAULT_FROM_EMAIL
    to = [email]

    text_message = f"""
Hi there!

Your OTP for {purpose} is: {otp_code}

This OTP is valid for 5 minutes only.

If you didn't request this, please ignore this email.

Best regards,
🚀 Team
"""

    html_message = f"""
<!DOCTYPE html>
<html>
<head>
<style>
    body {{ font-family: Arial, sans-serif; background: #f4f4f4; padding: 20px; }}
    .container {{ background: white; padding: 30px; border-radius: 10px; box-shadow: 0 0 10px rgba(0,0,0,0.1); }}
    .otp-box {{ background: #007bff; color: white; padding: 20px; text-align: center; border-radius: 8px; margin: 20px 0; }}
    .otp-code {{ font-size: 32px; font-weight: bold; letter-spacing: 8px; }}
</style>
</head>
<body>
<div class="container">
    <h2>🔐 🚀 Verification</h2>
    <p>Hi there!</p>
    <p>Your OTP for <b>{purpose}</b> is:</p>
    <div class="otp-box"><div class="otp-code">{otp_code}</div></div>
    <p>This OTP is valid for <strong>5 minutes</strong>. Do not share it with anyone.</p>
    <p>Ignore if you did not request this.</p>
    <p>– 🚀 Team</p>
</div>
</body>
</html>
"""

    try:
        msg = EmailMultiAlternatives(subject, text_message, from_email, to)
        msg.attach_alternative(html_message, "text/html")
        msg.send()
        logger.info(f"OTP email sent successfully to {email} for {purpose}")
    except Exception as e:
        logger.error(f"Failed to send OTP email to {email}: {str(e)}")
        # Notify admin but don't expose OTP in logs
        try:
            from django.core.mail import mail_admins
            mail_admins(
                f'OTP Email Sending Failed - {purpose}',
                f'Failed to send {purpose} OTP to {email}\n\nError: {str(e)}\n\nPlease check email configuration.',
                fail_silently=True
            )
        except:
            pass
        # Note: OTP is still created, user can use retry or contact support


# Dashboard - Simplified to avoid redirect loops
@login_required
def dashboard_view(request):
    return redirect('main_home')





# Registration
def register_view(request):
    if request.method == 'POST':
        logger.debug("POST request received for registration")

        # Get form data
        username = request.POST.get('username', '').strip()
        email = request.POST.get('email', '').strip().lower()
        password = request.POST.get('password', '')
        confirm_password = request.POST.get('confirm_password', '')

        # Additional profile data from multi-step form
        full_name = request.POST.get('full_name', '').strip()
        college = request.POST.get('college', '').strip()
        location = request.POST.get('location', '').strip()
        interests = request.POST.get('interests', '').strip()
        bio = request.POST.get('bio', '').strip()

        logger.debug(f"Registration attempt for username: {username}, email: {email}")

        # Basic validation
        if not username or not email or not password:
            messages.error(request, 'Username, email, and password are required.')
            logger.warning(f"Registration failed: missing required fields")
            return redirect('register')

        # Password confirmation check
        if password != confirm_password:
            messages.error(request, 'Passwords do not match.')
            logger.warning(f"Registration failed: password mismatch for {username}")
            return redirect('register')

        # Password strength validation (matching the form requirements)
        if len(password) < 8:
            messages.error(request, 'Password must be at least 8 characters long.')
            return redirect('register')

        if not any(c.isupper() for c in password):
            messages.error(request, 'Password must contain at least one uppercase letter.')
            return redirect('register')

        if not any(c.isdigit() for c in password):
            messages.error(request, 'Password must contain at least one digit.')
            return redirect('register')

        # Username validation
        if len(username) < 3:
            messages.error(request, 'Username must be at least 3 characters long.')
            return redirect('register')

        if User.objects.filter(username=username).exists():
            messages.error(request, 'This username is already taken.')
            logger.warning(f"Registration failed: username already taken {username}")
            return redirect('register')

        # Email validation
        if User.objects.filter(email=email).exists():
            messages.error(request, 'An account with this email already exists.')
            logger.warning(f"Registration failed: email already exists {email}")
            return redirect('register')

        # Terms agreement check
        if not request.POST.get('terms_agree'):
            messages.error(request, 'You must agree to the Terms of Service and Privacy Policy.')
            return redirect('register')

        try:
            logger.info(f"Creating new user: {username}")

            # Create user
            user = User.objects.create_user(username=username, email=email, password=password)
            user.backend = settings.AUTHENTICATION_BACKENDS[0]

            # Create student profile with additional data
            StudentProfile.objects.create(
                user=user,
                full_name=full_name,
                college=college,
                location=location,
                interests=interests,
                bio=bio,
                profile_completed=bool(full_name and college)
            )

            # Log the user in
            login(request, user)
            messages.success(request, 'Registration successful! Welcome to UniSinq!')
            logger.info(f"User registered successfully: {username}")

            # Redirect to main dashboard after successful registration
            return redirect('main_home')

        except Exception as e:
            logger.error(f"Registration failed with exception: {str(e)}")
            messages.error(request, 'Registration failed. Please try again.')
            return redirect('register')

    return render(request, 'register.html', {'form': RegisterForm()})


# Login
def login_view(request):
    """Handle user login with username or email support + OTP verification"""
    if request.method == 'POST':
        username_or_email = request.POST.get('username', '').strip()
        password = request.POST.get('password', '').strip()
        
        # Validation
        if not username_or_email or not password:
            messages.error(request, 'Username/Email and password are required.')
            return redirect('login')
        
        try:
            # Try authentication with username first
            user = authenticate(request, username=username_or_email, password=password)
            
            # If failed, try with email (user might have entered email instead of username)
            if not user:
                try:
                    user_obj = User.objects.get(email=username_or_email)
                    user = authenticate(request, username=user_obj.username, password=password)
                except User.DoesNotExist:
                    user = None
            
            # If authentication successful
            if user is not None:
                # Check if user has email
                if not user.email:
                    messages.error(request, 'Your account does not have an email address. Please contact support.')
                    logger.warning(f"Login attempt for user {user.username} with no email")
                    return redirect('login')
                
                # Generate and send OTP
                try:
                    otp = OTP.generate_otp(user.email, 'login')
                    send_otp_email(user.email, otp.otp_code, 'login')
                    
                    # Store user ID in session for OTP verification
                    request.session['login_user_id'] = user.id
                    request.session['login_user_email'] = user.email
                    request.session['login_username'] = user.username
                    
                    messages.success(request, f'OTP sent to {user.email}. Please verify to complete login.')
                    logger.info(f"OTP generated and sent to {user.email} for user {user.username}")
                    
                    return redirect('verify_otp', purpose='login')
                
                except Exception as e:
                    logger.error(f"Failed to send OTP email: {str(e)}")
                    messages.error(request, 'Failed to send OTP email. Please try again.')
                    return redirect('login')
            else:
                # Authentication failed
                messages.error(request, 'Invalid username/email or password.')
                logger.warning(f"Failed login attempt with: {username_or_email}")
                return redirect('login')
        
        except Exception as e:
            logger.error(f"Login error: {str(e)}")
            messages.error(request, 'An error occurred during login. Please try again.')
            return redirect('login')
    
    else:
        form = LoginForm()
    
    import os
    # Get OAuth credentials and handle potential MultipleObjectsReturned errors
    try:
        from allauth.socialaccount.models import SocialApp
        
        # Check for duplicate social apps (common issue)
        google_apps = SocialApp.objects.filter(provider='google')
        github_apps = SocialApp.objects.filter(provider='github')
        
        # OAuth is only enabled if:
        # 1. Exactly 1 SocialApp of that provider exists
        # 2. The credential env var is set (not placeholder)
        google_client_id = os.getenv('GOOGLE_CLIENT_ID', '').strip()
        github_client_id = os.getenv('GITHUB_CLIENT_ID', '').strip()
        
        has_google = (
            google_apps.count() == 1 
            and google_client_id 
            and not google_client_id.startswith('your-')
            and 'example' not in google_client_id
        )
        has_github = (
            github_apps.count() == 1 
            and github_client_id 
            and not github_client_id.startswith('your-')
            and 'example' not in github_client_id
        )
        
        if google_apps.count() > 1:
            logger.warning(f"Multiple Google SocialApp entries found ({google_apps.count()}). OAuth may not work.")
        if github_apps.count() > 1:
            logger.warning(f"Multiple GitHub SocialApp entries found ({github_apps.count()}). OAuth may not work.")
            
    except Exception as e:
        logger.error(f"Error checking social apps: {e}")
        has_google = False
        has_github = False
    
    context = {
        'form': form,
        'GITHUB_CLIENT_ID': github_client_id if has_github else None,
        'GOOGLE_CLIENT_ID': google_client_id if has_google else None,
    }
    return render(request, 'login.html', context)


# OTP Verification
def verify_otp_view(request, purpose):
    if request.method == 'POST':
        form = OTPVerificationForm(request.POST)
        if form.is_valid():
            try:
                otp_input = form.cleaned_data['otp_code']
                email = None
                user = None

                if purpose == 'registration':
                    data = request.session.get('registration_data')
                    if not data:
                        messages.error(request, 'Session expired. Please register again.')
                        return redirect('register')
                    email = data.get('email')
                    if not email:
                        messages.error(request, 'Invalid registration data.')
                        return redirect('register')
                        
                elif purpose == 'login':
                    user_id = request.session.get('login_user_id')
                    if not user_id:
                        messages.error(request, 'Session expired. Please login again.')
                        return redirect('login')
                    try:
                        user = User.objects.get(id=user_id)
                        email = user.email
                    except User.DoesNotExist:
                        messages.error(request, 'User not found. Please login again.')
                        return redirect('login')
                elif purpose == 'reset':
                    email = request.session.get('reset_email')
                    if not email:
                        messages.error(request, 'Session expired. Please request password reset again.')
                        return redirect('forgot_password')
                else:
                    messages.error(request, 'Invalid OTP purpose.')
                    return redirect('login')

                # Verify OTP
                otp_obj = OTP.objects.filter(email=email, purpose=purpose).order_by('-created_at').first()
                
                if not otp_obj:
                    messages.error(request, 'No OTP found. Please request a new OTP.')
                    logger.warning(f"No OTP found for {email} - {purpose}")
                    return redirect(f'resend_otp', purpose=purpose)
                    
                if not otp_obj.is_valid():
                    messages.error(request, 'OTP has expired. Please request a new one.')
                    logger.warning(f"Expired OTP for {email} - {purpose}")
                    return redirect(f'resend_otp', purpose=purpose)
                    
                if otp_obj.otp_code != otp_input:
                    messages.error(request, 'Invalid OTP. Please try again.')
                    logger.warning(f"Invalid OTP code for {email} - {purpose}")
                    return render(request, 'verify_otp.html', {'form': form, 'purpose': purpose})

                # OTP is valid - process based on purpose
                otp_obj.delete()
                
                if purpose == 'registration':
                    data = request.session.pop('registration_data', {})
                    if not data:
                        messages.error(request, 'Session expired. Please register again.')
                        return redirect('register')
                        
                    try:
                        user = User.objects.create_user(
                            username=data['username'], 
                            email=data['email'], 
                            password=data['password']
                        )
                        user.backend = settings.AUTHENTICATION_BACKENDS[0]
                        login(request, user)
                        messages.success(request, 'Registration successful!')
                        logger.info(f"User registered successfully: {data['username']}")
                        return redirect('student_details')
                    except Exception as e:
                        logger.error(f"Error creating user during OTP verification: {str(e)}")
                        messages.error(request, 'Error creating account. Please try again.')
                        return redirect('register')
                        
                elif purpose == 'login':
                    request.session.pop('login_user_id', None)
                    user.backend = settings.AUTHENTICATION_BACKENDS[0]
                    login(request, user)

                    # Send welcome back email (non-blocking)
                    try:
                        from .services.auth_service import AuthService
                        AuthService.send_welcome_back_email(user.email, user.username)
                    except Exception as e:
                        logger.warning(f"Failed to send welcome back email to {user.email}: {str(e)}")

                    messages.success(request, 'Login successful!')
                    logger.info(f"User logged in successfully: {user.username}")
                    return redirect('main_home')
                    
                elif purpose == 'reset':
                    # Redirect to password reset form
                    request.session['reset_verified'] = True
                    messages.success(request, 'OTP verified. Please set your new password.')
                    return redirect('reset_password')
                    
            except Exception as e:
                logger.error(f"Error in verify_otp_view: {str(e)}", exc_info=True)
                messages.error(request, 'An error occurred. Please try again.')
                return render(request, 'verify_otp.html', {'form': form, 'purpose': purpose})
        else:
            # Form is invalid
            for error in form.errors.values():
                messages.error(request, f"Form error: {error}")
    else:
        form = OTPVerificationForm()
        
    return render(request, 'verify_otp.html', {'form': form, 'purpose': purpose})


# Logout
def logout_view(request):
    logout(request)
    return redirect('main')


# Home / Dashboard Redirect
@login_required
def home_view(request):
    try:
        if not request.user.profile.profile_completed:
            return redirect('student_details')
    except StudentProfile.DoesNotExist:
        return redirect('student_details')
    return render(request, 'home.html')


# Profile Completion
@login_required
@csrf_exempt
def student_details_view(request):
    if request.method == 'POST':
        # Get all form data
        profile_photo = request.FILES.get('profile_photo')
        full_name = request.POST.get('full_name', '').strip()
        college = request.POST.get('college', '').strip()
        other_college = request.POST.get('other_college', '').strip()
        location = request.POST.get('location', '').strip()
        interests = request.POST.get('interests', '').strip()
        bio = request.POST.get('bio', '').strip()

        # Validate required fields
        if not full_name:
            messages.error(request, 'Full name is required.')
            return redirect('student_details')
        
        if not college:
            messages.error(request, 'College/University is required.')
            return redirect('student_details')
        
        if len(college) < 3:
            messages.error(request, 'Please enter a valid college name (at least 3 characters).')
            return redirect('student_details')

        # New fields
        skills = request.POST.getlist('skills[]') or []
        project_interests = request.POST.getlist('project_interests[]') or []
        role_preference = request.POST.get('role_preference', '')
        github = request.POST.get('github', '').strip()
        linkedin = request.POST.get('linkedin', '').strip()
        portfolio = request.POST.get('portfolio', '').strip()
        behance = request.POST.get('behance', '').strip()

        final_college = other_college if college.lower() == 'others' else college

        # Get or create profile
        profile, created = StudentProfile.objects.get_or_create(user=request.user)

        # Update all fields
        profile.full_name = full_name
        profile.college = final_college
        profile.other_college = other_college if college.lower() == 'others' else None
        profile.location = location
        profile.interests = interests
        profile.bio = bio
        profile.skills = skills
        profile.project_interests = project_interests
        profile.role_preference = role_preference
        profile.github = github
        profile.linkedin = linkedin
        profile.portfolio = portfolio
        profile.behance = behance
        profile.profile_completed = True
        
        # Only update photo if a new one was uploaded
        if profile_photo:
            # Delete old photo if it exists
            if profile.profile_photo:
                profile.profile_photo.delete()
            profile.profile_photo = profile_photo
            logger.info(f"Profile photo uploaded for user {request.user.username}: {profile_photo.name}")
        
        # Save the profile
        profile.save()

        # Create activity record for profile completion
        Activity.objects.create(
            user=request.user,
            activity_type='profile_updated',
            title='Completed profile',
            description=f'{request.user.username} completed their profile',
            is_public=False
        )

        messages.success(request, 'Profile saved successfully!')
        logger.info(f"Student profile completed for user {request.user.username}")
        return redirect('main_home')

    return render(request, 'account/student_details.html')


@login_required
def nlp_analyze_api(request):
    """API endpoint for NLP analysis of text"""
    if request.method == 'POST':
        text = request.POST.get('text', '')

        if not text:
            return JsonResponse({'error': 'No text provided'}, status=400)

        analysis = {
            'skills': StudentProfileNLP.extract_skills(text),
            'interests': StudentProfileNLP.analyze_interests(text),
            'keywords': StudentProfileNLP.extract_keywords(text),
            'sentiment': StudentProfileNLP.analyze_sentiment(text)
        }

        return JsonResponse(analysis)

    return JsonResponse({'error': 'Method not allowed'}, status=405)


# Landing Page
def main(request):

        return render(request, 'main.html')

# About Us Page
def about_view(request):
    """About Us page showcasing UniSinq and its creator"""
    context = {
        'page_title': 'About UniSinq',
        'meta_description': 'Learn about UniSinq - a student collaboration platform created by Gautam Nair to connect talented students worldwide for innovative projects.',
    }
    return render(request, 'about.html', context)

# Help Center Page
def help_center_view(request):
    """Help Center page with FAQs and support resources"""
    context = {
        'page_title': 'Help Center - UniSinq',
        'meta_description': 'Get help and support for UniSinq. Find answers to frequently asked questions and learn how to make the most of our student collaboration platform.',
    }
    return render(request, 'help_center.html', context)


# Forgot Password - Request OTP
def forgot_password_view(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        user = User.objects.filter(email=email).first()
        if not user:
            messages.error(request, "No account found with this email")
            return render(request, 'forgot_password.html')
        otp = OTP.generate_otp(email, 'reset')
        send_otp_email(email, otp.otp_code, 'password reset')
        request.session['reset_email'] = email
        messages.success(request, 'OTP sent to your email. Please verify to reset your password.')
        return redirect('reset_password')
    return render(request, 'forgot_password.html')


# Reset Password After OTP
def reset_password_view(request):
    if request.method == 'POST':
        otp_input = request.POST.get('otp_code')
        new_password = request.POST.get('new_password')
        confirm_password = request.POST.get('confirm_password')
        email = request.session.get('reset_email')

        if not email:
            messages.error(request, 'Session expired. Please try again.')
            return redirect('forgot_password')

        if new_password != confirm_password:
            messages.error(request, 'Passwords do not match.')
            return redirect('reset_password')

        otp_obj = OTP.objects.filter(email=email, purpose='reset').order_by('-created_at').first()
        if otp_obj and otp_obj.otp_code == otp_input and otp_obj.is_valid():
            user = User.objects.filter(email=email).first()
            if not user:
                messages.error(request, 'No account found with this email.')
                return render(request, 'reset_password.html')
            user.set_password(new_password)
            user.save()
            from django.contrib.sessions.models import Session
            sessions = Session.objects.all()
            for session in sessions:
                data = session.get_decoded()
                if data.get('_auth_user_id') == str(user.id):
                    session.delete()

            
            otp_obj.delete()
            del request.session['reset_email']
            messages.success(request, 'Password reset successful! Please login.')
            return redirect('login')
        else:
            messages.error(request, 'Invalid or expired OTP.')

    return render(request, 'reset_password.html')

from django.contrib.auth import get_user_model, get_user

def resend_otp_view(request, purpose):
    email = None
    if purpose == 'registration':
        data = request.session.get('registration_data')
        if not data:
            messages.error(request, 'Session expired. Please register again.')
            return redirect('register')
        email = data['email']
    elif purpose == 'login':
        user_id = request.session.get('login_user_id')
        if not user_id:
            messages.error(request, 'Session expired. Please login again.')
            return redirect('login')
        user = get_user_model().objects.filter(id=user_id).first()
        email = user.email if user else None
    elif purpose == 'reset':
        email = request.session.get('reset_email')
        if not email:
            messages.error(request, 'Session expired. Please try again.')
            return redirect('forgot_password')
    else:
        messages.error(request, 'Invalid OTP purpose.')
        return redirect('main')

    otp = OTP.generate_otp(email, purpose)
    send_otp_email(email, otp.otp_code, purpose)
    messages.success(request, f'OTP resent to {email}.')
    if purpose == 'registration':
        return redirect('verify_otp', purpose='registration')
    elif purpose == 'login':
        return redirect('verify_otp', purpose='login')
    elif purpose == 'reset':
        return redirect('reset_password')
    
@login_required
def main_home(request):
    """Simplified main home view for testing"""
    from django.db.models import Q
    
    # Get unread notifications count for badge
    unread_count = 0
    visible_projects = []
    project_match_details = {}
    connection_status = {}
    liked_project_ids = set()
    
    if request.user.is_authenticated:
        unread_count = Notification.objects.filter(user=request.user, is_read=False).count()
        
        # Get visible projects based on user profile compatibility
        all_projects = Project.objects.all().order_by('-created_at')
        visible_projects, project_match_details = ProjectVisibilityFilter.get_visible_projects(
            request.user,
            all_projects
        )
        
        # Get projects liked by current user
        liked_project_ids = set(
            Like.objects.filter(user=request.user).values_list('project_id', flat=True)
        )
        
        # Get connection status for all project owners in the feed
        project_owner_ids = [project.user.id for project in visible_projects if project.user.id != request.user.id]
        
        if project_owner_ids:
            connections = Connection.objects.filter(
                Q(sender=request.user, receiver_id__in=project_owner_ids) |
                Q(sender_id__in=project_owner_ids, receiver=request.user)
            ).values('sender_id', 'receiver_id', 'status')
            
            for conn in connections:
                other_user_id = conn['receiver_id'] if conn['sender_id'] == request.user.id else conn['sender_id']
                connection_status[other_user_id] = conn['status']
        
        # Add match badge info and comments to each project
        for project in visible_projects:
            if project.id in project_match_details:
                match_info = project_match_details[project.id]
                project.match_score = match_info['score']
                project.match_reasons = match_info['reasons']
                project.match_badge = ProjectVisibilityFilter.get_project_match_badge(match_info['score'])
            
            # Fetch comments for the project to display on load
            project.comments_list = Comment.objects.filter(project=project).select_related('user').order_by('-created_at')[:5]
            project.comments_count = Comment.objects.filter(project=project).count()
    
    return render(request, 'main_home.html', {
        'feed_posts': visible_projects,
        'project_match_details': project_match_details,
        'connection_status': connection_status,
        'liked_project_ids': liked_project_ids,
        'categories': ['Web Development', 'Mobile Apps', 'AI/ML', 'Data Science'],
        'available_techs': ['Python', 'JavaScript', 'React', 'Django', 'Node.js'],
        'homepage_stats': {
            'total_projects': Project.objects.count(),
            'active_users': User.objects.filter(is_active=True).count(),
            'total_connections': Connection.objects.filter(status='accepted').count(),
            'success_stories': 45
        },
        'active_filters': {},
        'has_filters': False,
        'unread_notification_count': unread_count,
    })





@login_required
def my_projects_view(request):
    """Show current user's projects"""
    projects = Project.objects.filter(user=request.user).order_by('-created_at')

    return render(request, 'post_project.html', {
        'projects': projects,
    })

@login_required
def explore_projects_view(request):
    """Explore all projects"""
    projects = Project.objects.all().order_by('-created_at')

    return render(request, 'post_project.html', {
        'projects': projects,
        'explore_mode': True,
    })

# Helper function to create notifications
def create_notification(user, notification_type, title, message, from_user=None, connection=None, message_obj=None):
    """Create a notification for a user"""
    notification = Notification.objects.create(
        user=user,
        notification_type=notification_type,
        title=title,
        message=message,
        from_user=from_user,
        connection=connection,
        message_obj=message_obj
    )

    # Send real-time notification via WebSocket (if configured)
    try:
        from channels.layers import get_channel_layer
        from asgiref.sync import async_to_sync

        channel_layer = get_channel_layer()
        if channel_layer:
            async_to_sync(channel_layer.group_send)(
                f'notifications_{user.id}',
                {
                    'type': 'notification_message',
                    'notification': {
                        'id': notification.id,
                        'type': notification_type,
                        'title': title,
                        'message': message,
                        'created_at': notification.created_at.isoformat(),
                        'from_user_id': from_user.id if from_user else None,
                        'from_user_username': from_user.username if from_user else None,
                    }
                }
            )
    except (ImportError, RuntimeError, AttributeError):
        # Channels not configured or not available - notification still saved to database
        pass

    return notification



    """Chat with a specific user"""
    other_user = get_object_or_404(User, id=user_id)

    # Check if users are connected
    connection = Connection.objects.filter(
        Q(sender=request.user, receiver=other_user) |
        Q(sender=other_user, receiver=request.user)
    ).first()

    is_connected = connection and connection.status == 'accepted'

    if request.method == 'POST':
        content = request.POST.get('content', '').strip()
        uploaded_file = request.FILES.get('file')

        # Handle file upload
        if uploaded_file:
            # Validate file size (max 10MB)
            if uploaded_file.size > 10 * 1024 * 1024:
                messages.error(request, 'File size cannot exceed 10MB.')
                return redirect('chat', user_id=user_id)

            # Create File instance
            file_obj = File.objects.create(
                user=request.user,
                file=uploaded_file,
                filename=uploaded_file.name,
                file_size=uploaded_file.size,
                file_type=uploaded_file.content_type
            )

            # Create message with file attachment
            message = Message.objects.create(
                sender=request.user,
                receiver=other_user,
                content=content or f"📎 {uploaded_file.name}"
            )

            # Attach file to message
            MessageFile.objects.create(message=message, file=file_obj)

        elif content:
            # Create regular text message
            message = Message.objects.create(
                sender=request.user,
                receiver=other_user,
                content=content
            )
        else:
            messages.error(request, 'Please enter a message or upload a file.')
            return redirect('chat', user_id=user_id)

        # Create notification for receiver (only if there's content or it's a file)
        if content or uploaded_file:
            notification_message = content[:50] if content else f"📎 {uploaded_file.name}"
            create_notification(
                user=other_user,
                notification_type='message',
                title=f'New message from {request.user.username}',
                message=f'{request.user.username}: {notification_message}...',
                from_user=request.user,
                message_obj=message
            )

        # Mark messages from this user as read (when replying)
        unread_msgs = Message.objects.filter(
            sender=other_user,
            receiver=request.user
        ).exclude(
            read_statuses__user=request.user
        )
        for msg in unread_msgs:
            msg.mark_as_read_by(request.user)

        return redirect('chat', user_id=user_id)

    # Get all messages between users with reaction counts
    messages = Message.objects.filter(
    Q(sender=request.user, receiver=other_user) |
    Q(sender=other_user, receiver=request.user)
    ).order_by('created_at').prefetch_related('files__file', 'reactions')

    # Add reaction counts to each message
    for message in messages:
        reactions = MessageReaction.objects.filter(message=message).values('reaction').annotate(
            count=models.Count('reaction')
        ).order_by('reaction')
        message.reaction_counts = {r['reaction']: r['count'] for r in reactions}

    # Mark received messages as read
    unread_messages = Message.objects.filter(
        sender=other_user,
        receiver=request.user
    ).exclude(
        read_statuses__user=request.user
    )
    for message in unread_messages:
        message.mark_as_read_by(request.user)

    # Generate consistent room name for WebSocket
    room_name = f'user_{min(request.user.id, other_user.id)}_{max(request.user.id, other_user.id)}'

    return render(request, 'features/chat.html', {
        'other_user': other_user,
        'messages': messages,
        'is_connected': is_connected,
        'connection': connection,
        'room_name': room_name
    })


# -------------------------
# Enhanced Messaging Views
# -------------------------

@login_required
def enhanced_messages_view(request):
    """Enhanced messages view with group chats and project chats"""
    # Get user's chat rooms
    chat_rooms = ChatRoom.objects.filter(
        members__user=request.user,
        members__is_active=True,
        is_active=True
    ).distinct().prefetch_related('members__user', 'project')

    # Get conversations data
    conversations = []
    for room in chat_rooms:
        # Get last message
        last_message = room.messages.order_by('-created_at').first()

        # Count unread messages (exclude messages from current user)
        unread_count = MessageReadStatus.objects.filter(
            message__chat_room=room,
            user=request.user
        ).exclude(
            message__sender=request.user
        ).count()

        # For direct chats, get the other user
        other_user = None
        if room.chat_type == 'direct':
            other_member = room.members.exclude(user=request.user).first()
            if other_member:
                other_user = other_member.user

        conversations.append({
            'room': room,
            'last_message': last_message,
            'unread_count': unread_count,
            'other_user': other_user,
        })

    # Sort by most recent message
    conversations.sort(key=lambda x: x['last_message'].created_at if x['last_message'] else room.created_at, reverse=True)

    return render(request, 'features/enhanced_messages.html', {
        'conversations': conversations
    })


@login_required
def enhanced_chat_view(request, room_id):
    """Enhanced chat view supporting group chats, threading, and reactions"""
    chat_room = get_object_or_404(ChatRoom, id=room_id, is_active=True)

    # Check if user is a member of this chat room
    membership = ChatRoomMember.objects.filter(
        chat_room=chat_room,
        user=request.user,
        is_active=True
    ).first()

    if not membership:
        messages.error(request, "You don't have access to this chat.")
        return redirect('enhanced_messages')

    if request.method == 'POST':
        content = request.POST.get('content', '').strip()
        reply_to_id = request.POST.get('reply_to')
        uploaded_file = request.FILES.get('file')

        reply_to = None
        if reply_to_id:
            try:
                reply_to = Message.objects.get(id=reply_to_id, chat_room=chat_room)
            except Message.DoesNotExist:
                pass

        # Handle file upload
        if uploaded_file:
            if uploaded_file.size > 10 * 1024 * 1024:
                messages.error(request, 'File size cannot exceed 10MB.')
                return redirect('enhanced_chat', room_id=room_id)

            file_obj = File.objects.create(
                user=request.user,
                file=uploaded_file,
                filename=uploaded_file.name,
                file_size=uploaded_file.size,
                file_type=uploaded_file.content_type
            )

            message = Message.objects.create(
                chat_room=chat_room,
                sender=request.user,
                content=content or f"📎 {uploaded_file.name}",
                message_type='file' if file_obj.is_image else 'file',
                reply_to=reply_to
            )

            MessageFile.objects.create(message=message, file=file_obj)

        elif content:
            message = Message.objects.create(
                chat_room=chat_room,
                sender=request.user,
                content=content,
                reply_to=reply_to
            )
        else:
            messages.error(request, 'Please enter a message or upload a file.')
            return redirect('enhanced_chat', room_id=room_id)

        # Create read status for all members except sender
        for member in chat_room.members.filter(is_active=True).exclude(user=request.user):
            MessageReadStatus.objects.get_or_create(
                message=message,
                user=member.user
            )

        # Create notifications for other members
        for member in chat_room.members.filter(is_active=True).exclude(user=request.user):
            notification_message = content[:50] if content else f"📎 {uploaded_file.name if uploaded_file else 'File'}"
            create_notification(
                user=member.user,
                notification_type='message',
                title=f'New message in {chat_room.display_name}',
                message=f'{request.user.username}: {notification_message}...',
                from_user=request.user,
                message_obj=message
            )

        return redirect('enhanced_chat', room_id=room_id)

    # Get messages with reactions and threading info
    messages_list = chat_room.messages.select_related('sender', 'reply_to').prefetch_related(
        'files__file', 'reactions', 'replies'
    ).order_by('created_at')

    # Add reaction counts to each message
    for message in messages_list:
        reactions = MessageReaction.objects.filter(message=message).values('reaction').annotate(
            count=models.Count('reaction')
        ).order_by('reaction')
        message.reaction_counts = {r['reaction']: r['count'] for r in reactions}

        # Mark message as read for current user
        MessageReadStatus.objects.get_or_create(
            message=message,
            user=request.user
        )

    # Get room members
    members = chat_room.members.filter(is_active=True).select_related('user')

    # Generate room name for WebSocket (for real-time features)
    room_name = f'chat_{chat_room.id}'

    return render(request, 'features/enhanced_chat.html', {
        'chat_room': chat_room,
        'messages': messages_list,
        'members': members,
        'current_membership': membership,
        'room_name': room_name
    })


@login_required
def create_group_chat(request):
    """Create a new group chat"""
    if request.method == 'POST':
        name = request.POST.get('name', '').strip()
        member_ids = request.POST.getlist('members')

        if not name:
            messages.error(request, 'Group name is required.')
            return redirect('enhanced_messages')

        if len(member_ids) < 2:
            messages.error(request, 'Group chat must have at least 2 members.')
            return redirect('enhanced_messages')

        # Create chat room
        chat_room = ChatRoom.objects.create(
            name=name,
            chat_type='group'
        )

        # Add creator as owner
        ChatRoomMember.objects.create(
            chat_room=chat_room,
            user=request.user,
            role='owner'
        )

        # Add other members
        for member_id in member_ids:
            try:
                user = User.objects.get(id=member_id)
                if user != request.user:
                    ChatRoomMember.objects.create(
                        chat_room=chat_room,
                        user=user,
                        role='member'
                    )
            except User.DoesNotExist:
                continue

        messages.success(request, f'Group "{name}" created successfully!')
        return redirect('enhanced_chat', room_id=chat_room.id)

    # Get potential members (connected users)
    connected_users = Connection.objects.filter(
        Q(sender=request.user, status='accepted') |
        Q(receiver=request.user, status='accepted')
    ).select_related('sender', 'receiver')

    potential_members = []
    seen_users = set()
    for conn in connected_users:
        other_user = conn.receiver if conn.sender == request.user else conn.sender
        if other_user.id not in seen_users:
            potential_members.append(other_user)
            seen_users.add(other_user.id)

    return render(request, 'features/create_group_chat.html', {
        'potential_members': potential_members
    })


@login_required
def add_reaction(request, message_id):
    """Add or remove a reaction to/from a message"""
    if request.method == 'POST':
        reaction_type = request.POST.get('reaction')
        if not reaction_type:
            return JsonResponse({'error': 'Reaction type required'}, status=400)

        try:
            message = Message.objects.get(id=message_id)

            # Check if user can react to this message (must be in the same chat room)
            if not ChatRoomMember.objects.filter(
                chat_room=message.chat_room,
                user=request.user,
                is_active=True
            ).exists():
                return JsonResponse({'error': 'Permission denied'}, status=403)

            # Check if reaction already exists
            existing_reaction = MessageReaction.objects.filter(
                message=message,
                user=request.user,
                reaction=reaction_type
            ).first()

            if existing_reaction:
                # Remove reaction
                existing_reaction.delete()
                action = 'removed'
            else:
                # Add reaction
                MessageReaction.objects.create(
                    message=message,
                    user=request.user,
                    reaction=reaction_type
                )
                action = 'added'

            # Get updated reaction counts
            reactions = MessageReaction.objects.filter(message=message).values('reaction').annotate(
                count=models.Count('reaction')
            ).order_by('reaction')

            reaction_data = {r['reaction']: r['count'] for r in reactions}

            return JsonResponse({
                'action': action,
                'reactions': reaction_data
            })

        except Message.DoesNotExist:
            return JsonResponse({'error': 'Message not found'}, status=404)

    return JsonResponse({'error': 'Method not allowed'}, status=405)


@login_required
def start_call(request, room_id):
    """Start a voice/video call in a chat room"""
    chat_room = get_object_or_404(ChatRoom, id=room_id)

    # Check membership
    if not ChatRoomMember.objects.filter(
        chat_room=chat_room,
        user=request.user,
        is_active=True
    ).exists():
        return JsonResponse({'error': 'Not a member of this chat'}, status=403)

    call_type = request.POST.get('call_type', 'voice')
    if call_type not in ['voice', 'video']:
        return JsonResponse({'error': 'Invalid call type'}, status=400)

    # Create call message
    message = Message.objects.create(
        chat_room=chat_room,
        sender=request.user,
        content=f"📞 Started a {call_type} call",
        message_type='call',
        call_type=call_type
    )

    # Notify other members
    for member in chat_room.members.filter(is_active=True).exclude(user=request.user):
        create_notification(
            user=member.user,
            notification_type='message',
            title=f'{call_type.title()} call in {chat_room.display_name}',
            message=f'{request.user.username} started a {call_type} call',
            from_user=request.user,
            message_obj=message
        )

    return JsonResponse({
        'success': True,
        'call_id': f"call_{message.id}",
        'call_type': call_type,
        'room_name': f'call_{chat_room.id}_{message.id}'
    })

@login_required
def notifications_view(request):
    """View all notifications"""
    notifications = Notification.objects.filter(user=request.user).order_by('-created_at')

    # Mark all as read when viewing
    if request.method == 'POST' and request.POST.get('mark_read'):
        notifications.filter(is_read=False).update(is_read=True)
        messages.success(request, 'All notifications marked as read!')
        return redirect('notifications')

    return render(request, 'features/notifications.html', {
        'notifications': notifications,
        'unread_count': notifications.filter(is_read=False).count()
    })


@login_required
def mark_notification_read(request, notification_id):
    """Mark a specific notification as read"""
    notification = get_object_or_404(Notification, id=notification_id, user=request.user)
    notification.is_read = True
    notification.save()

    # Redirect based on notification type
    if notification.notification_type == 'message' and notification.message_obj:
        return redirect('chat', user_id=notification.from_user.id)
    elif notification.notification_type in ['connection_request', 'connection_accepted']:
        return redirect('my_connections')
    else:
        return redirect('notifications')

def profile_view(request):
    return render(request, 'features/profile.html')

def premium_view(request):
    return render(request, 'features/premium.html')

def upgrade_view(request):
    return render(request, 'upgrade.html')



def investor_dashboard(request):
    return render(request, 'investor_dashboard.html')




@login_required
def student_profile(request):
    profile, created = StudentProfile.objects.get_or_create(
        user=request.user,
        defaults={'full_name': request.user.get_full_name() or request.user.username}
    )

    if request.method == 'POST':
        form = StudentProfileForm(request.POST, request.FILES, instance=profile)
        if form.is_valid():
            # Handle profile photo update
            if 'profile_photo' in request.FILES:
                # Delete old photo if it exists
                if profile.profile_photo:
                    profile.profile_photo.delete()
                logger.info(f"Profile photo uploaded for user {request.user.username}")
            
            form.save()
            messages.success(request, 'Profile updated successfully!')
            logger.info(f"Student profile updated for user {request.user.username}")
            
            # Refresh profile from database to ensure updated data (especially for profile_photo)
            profile.refresh_from_db()
            
            return redirect('student_profile')
    else:
        form = StudentProfileForm(instance=profile)

    return render(request, 'account/student_profile.html', {
        'form': form,
        'profile': profile,
        'user_obj': request.user,
        'interest_suggestions': [
            'Artificial Intelligence', 'Machine Learning', 'Web Development',
            'Data Science', 'Blockchain', 'Cybersecurity', 'Sports', 'Music'
        ],
        'school_suggestions': [
            'Harvard University', 'MIT', 'Stanford University',
            'IIT Bombay', 'IIT Delhi', 'NIT Trichy', 'BITS Pilani'
        ]
    })

@login_required
def social_login_redirect(request):
    try:
        profile = StudentProfile.objects.get(user=request.user)
        if not profile.profile_completed:
            return redirect('student_details')
        else:
            return redirect('main')  # or dashboard
    except StudentProfile.DoesNotExist:
        return redirect('student_details')

class UserProfileView(generics.RetrieveAPIView):
    queryset = StudentProfile.objects.all()
    serializer_class = UserProfileSerializer
    permission_classes = [permissions.IsAuthenticated]

@login_required
def find_collaborators(request):
    # Get current user's interests if they have a profile
    try:
        user_profile = request.user.student_profile
        user_interests = user_profile.interests.lower().split(",") if user_profile.interests else []
    except StudentProfile.DoesNotExist:
        user_interests = []
        user_profile = None

    # --- Get filter parameters ---
    query = request.GET.get("q", "").strip()
    skills_filter = request.GET.getlist("skills")  # Multiple skills
    college_filter = request.GET.get("college", "").strip()
    location_filter = request.GET.get("location", "").strip()

    # Build active filters dict for template
    active_filters = {}
    if skills_filter:
        active_filters['skills'] = skills_filter
    if college_filter:
        active_filters['college'] = college_filter
    if location_filter:
        active_filters['location'] = location_filter

    # --- Apply filters to base queryset ---
    base_profiles = StudentProfile.objects.exclude(user=request.user).select_related('user')

    # Apply skills filter
    if skills_filter:
        skills_query = Q()
        for skill in skills_filter:
            skills_query |= Q(interests__icontains=skill.lower())
        base_profiles = base_profiles.filter(skills_query)

    # Apply college filter
    if college_filter:
        # Filter by exact college name (case-insensitive)
        base_profiles = base_profiles.filter(college__iexact=college_filter)

    # Apply location filter
    if location_filter:
        if location_filter == 'remote':
            # For remote, we might want to show all or filter by specific remote-friendly locations
            pass  # Keep all for now
        else:
            base_profiles = base_profiles.filter(location__icontains=location_filter)

    # --- Search functionality ---
    query = request.GET.get("q", "").strip()
    search_results = []

    if query:
        # Search within filtered results
        search_queryset = base_profiles.filter(
            Q(full_name__icontains=query) |
            Q(college__icontains=query) |
            Q(location__icontains=query) |
            Q(interests__icontains=query) |
            Q(user__username__icontains=query)
        )

        # Limit results and create search results
        search_results = list(search_queryset[:20])
    elif active_filters:
        # If no search query but filters are applied, show filtered results
        search_results = list(base_profiles[:20])

    # --- Suggested collaborators ---
    # Get all users except current user
    all_users = User.objects.exclude(id=request.user.id)

    # Get users with profiles
    users_with_profiles = base_profiles
    users_without_profiles = all_users.exclude(student_profile__isnull=False)

    # Create suggestions list
    suggestions = []

    # First, add users with profiles (prioritize those with matching interests if user has interests)
    if user_interests:
        # Find profiles with matching interests
        query_filter = Q()
        for interest in user_interests:
            interest = interest.strip()
            if interest:
                query_filter |= Q(interests__icontains=interest)

        matching_profiles = users_with_profiles.filter(query_filter).distinct()

        # Add match scores and sort by relevance
        for profile in matching_profiles:
            profile_interests = profile.interests.lower().split(",") if profile.interests else []
            matching_interests = set(user_interests) & set([i.strip() for i in profile_interests])
            profile.match_score = int((len(matching_interests) / len(user_interests)) * 100) if user_interests else 0
            suggestions.append(profile)

        # Sort by match score (highest first)
        suggestions.sort(key=lambda x: x.match_score, reverse=True)

    # If we don't have enough suggestions, add more profiles
    if len(suggestions) < 20:
        remaining_profiles = users_with_profiles.exclude(id__in=[getattr(p, 'id', None) for p in suggestions])
        for profile in remaining_profiles[:20-len(suggestions)]:
            profile.match_score = 0  # No match score for non-matching suggestions
            suggestions.append(profile)

    # If still not enough, add users without profiles
    if len(suggestions) < 20:
        for user in users_without_profiles[:20-len(suggestions)]:
            class PseudoProfile:
                def __init__(self, user):
                    self.user = user
                    self.full_name = user.get_full_name() or user.username
                    self.college = "Profile not completed"
                    self.location = ""
                    self.interests = ""
                    self.bio = "This user hasn't completed their profile yet."
                    self.profile_photo = None
                    self.match_score = 0

            suggestions.append(PseudoProfile(user))

    # Limit suggestions to 20
    suggestions = suggestions[:20]

    # Get connection statuses for all users
    all_user_ids = []
    if search_results:
        for result in search_results:
            all_user_ids.append(result.user.id)
    for suggestion in suggestions:
        all_user_ids.append(suggestion.user.id)

    connections = Connection.objects.filter(
        Q(sender=request.user, receiver__id__in=all_user_ids) |
        Q(receiver=request.user, sender__id__in=all_user_ids)
    )

    # Create a connection status map
    connection_status = {}
    for conn in connections:
        other_user_id = conn.receiver.id if conn.sender == request.user else conn.sender.id
        connection_status[other_user_id] = conn.status

    # Get statistics for the template
    total_users = User.objects.count()
    active_projects = Project.objects.filter(created_at__gte=timezone.now() - timezone.timedelta(days=30)).count()
    connections_today = Connection.objects.filter(created_at__date=timezone.now().date()).count()

    # Get all unique skills/interests for skills count
    all_interests = set()
    all_colleges = set()
    for profile in StudentProfile.objects.all():
        if profile.interests:
            interests = [interest.strip() for interest in profile.interests.split(',')]
            all_interests.update(interests)
        if profile.college:
            all_colleges.add(profile.college)
    skills_count = len(all_interests)
    colleges_list = sorted(list(all_colleges))

    # Determine which template to use (enhanced or original)
    template_name = "find_collaborators_enhanced.html"

    return render(request, template_name, {
        "query": query,
        "search_results": search_results,
        "suggestions": suggestions,
        "user_interests": user_interests,
        "connection_status": connection_status,
        "active_filters": active_filters,
        "total_users": total_users,
        "active_projects": active_projects,
        "connections_today": connections_today,
        "skills_count": skills_count,
        "colleges": colleges_list,
    })


@login_required
@require_http_methods(["POST"])
def like_project(request, project_id):
    """Toggle like on a project - AJAX endpoint"""
    try:
        project = get_object_or_404(Project, id=project_id)

        # Check if user already liked the project
        existing_like = Like.objects.filter(user=request.user, project=project).first()

        if existing_like:
            # Unlike
            existing_like.delete()
            liked = False
            message = "Project unliked"
        else:
            # Like
            Like.objects.create(user=request.user, project=project)
            liked = True
            message = "Project liked!"

            # Create activity
            Activity.objects.create(
                user=request.user,
                activity_type='project_liked',
                title=f"Liked '{project.title}'",
                description=f"{request.user.username} liked the project '{project.title}'",
                project=project
            )

        return JsonResponse({
            'success': True, 
            'liked': liked, 
            'message': message,
            'likes_count': project.likes.count()
        })
    except Exception as e:
        logger.error(f"Error liking project: {str(e)}")
        return JsonResponse({
            'success': False,
            'message': f'Error: {str(e)}'
        }, status=400)

@login_required
def post_project(request):
    if request.method == "POST":
        title = request.POST.get('title')
        description = request.POST.get('description')
        techs = request.POST.getlist('technologies')
        looking = request.POST.getlist('looking_for')
        category = request.POST.get('category', 'Other')
        
        timeline = request.POST.get('timeline', '')
        collaboration = request.POST.get('collaboration_needs', '')
        github_link = request.POST.get('github_link', '')

        if title and description:
            project = Project.objects.create(
                user=request.user,
                title=title,
                description=description,
                technologies=", ".join(techs) if techs else "",
                looking_for=", ".join(looking) if looking else "",
                category=category
                , timeline=timeline if timeline else None,
                collaboration_needs=collaboration if collaboration else None,
                github_link=github_link if github_link else None
            )

            # Create activity
            create_activity(
                user=request.user,
                activity_type='project_created',
                title=f"Created project '{title}'",
                description=f"{request.user.username} created a new project titled '{title}'",
                project=project
            )

            messages.success(request, 'Project posted successfully!')
            return redirect('post_project')
    
    projects = Project.objects.filter(user=request.user).order_by('-created_at')
    
    return render(request, 'post_project.html', {
        'projects': projects,
    })


@login_required
def edit_project(request, project_id):
    """Edit a project"""
    project = get_object_or_404(Project, id=project_id, user=request.user)
    
    if request.method == 'POST':
        title = request.POST.get('title')
        description = request.POST.get('description')
        techs = request.POST.getlist('technologies')
        looking = request.POST.getlist('looking_for')
        
        if title and description:
            project.title = title
            project.description = description
            project.technologies = ", ".join(techs) if techs else ""
            project.looking_for = ", ".join(looking) if looking else ""
            project.save()
            
            messages.success(request, 'Project updated successfully!')
            return redirect('post_project')
    
    # Process technologies for display
    tech_list = [tech.strip() for tech in project.technologies.split(',')] if project.technologies else []
    looking_list = [item.strip() for item in project.looking_for.split(',')] if project.looking_for else []
    
    return render(request, 'edit_project.html', {
        'project': project,
        'tech_list': tech_list,
        'looking_list': looking_list,
    })


@login_required
def delete_project(request, project_id):
    """Delete a project"""
    project = get_object_or_404(Project, id=project_id, user=request.user)
    project.delete()
    messages.success(request, 'Project deleted successfully!')
    return redirect('post_project')


@login_required
def project_detail(request, project_id):
    """View project details - ULTRA-OPTIMIZED for performance"""
    from django.db.models import Count, Q, Prefetch
    from django.views.decorators.http import condition
    
    # ULTRA-OPTIMIZATION: Single prefetch query for all project data
    project = get_object_or_404(
        Project.objects.select_related(
            'user__student_profile'
        ).prefetch_related(
            'comments__user__student_profile',
            'tasks',
            'milestones'
        ),
        id=project_id
    )

    # Handle comment submission
    if request.method == 'POST' and 'comment_content' in request.POST:
        comment_content = request.POST.get('comment_content', '').strip()
        if comment_content:
            Comment.objects.create(
                user=request.user,
                project=project,
                content=comment_content
            )
            messages.success(request, 'Comment added successfully!')
            return redirect('project_detail', project_id=project_id)

    # Process technologies for display (using cached split)
    tech_list = [tech.strip() for tech in project.technologies.split(',')] if project.technologies else []
    looking_list = [item.strip() for item in project.looking_for.split(',')] if project.looking_for else []

    # ULTRA-OPTIMIZATION: Use prefetched comments (already loaded above)
    comments = sorted(
        project.comments.all(),
        key=lambda x: x.created_at,
        reverse=True
    )[:50]

    # Check if user already connected with project owner (cached query)
    is_connected = False
    connection_status = None
    if request.user.is_authenticated and request.user != project.user:
        connection = Connection.objects.filter(
            Q(sender=request.user, receiver=project.user) |
            Q(sender=project.user, receiver=request.user)
        ).only('status').first()
        if connection:
            is_connected = connection.status == 'accepted'
            connection_status = connection.status

    # Team information - ONLY fetch if needed
    team = None
    team_members = []
    user_team_role = None
    can_manage_team = request.user == project.user if request.user.is_authenticated else False
    pending_invitations = []

    # Skip team queries if not project owner and not authenticated
    if can_manage_team or request.user.is_authenticated:
        try:
            team = ProjectTeam.objects.only('id', 'project_id').get(project=project)
            
            # Only fetch team members if project owner or team member
            if can_manage_team:
                team_members = list(
                    ProjectTeamMember.objects.filter(
                        team=team, 
                        is_active=True
                    ).select_related('user__student_profile')[:50]
                )
                pending_invitations = list(
                    ProjectTeamInvitation.objects.filter(
                        project=project,
                        status='pending'
                    ).select_related('invited_user__student_profile')[:20]
                )
            else:
                # Check user's role in team
                try:
                    user_membership = ProjectTeamMember.objects.filter(
                        team=team, 
                        user=request.user, 
                        is_active=True
                    ).only('role', 'id').first()
                    if user_membership:
                        user_team_role = user_membership.role
                        team_members = list(
                            ProjectTeamMember.objects.filter(
                                team=team, 
                                is_active=True
                            ).select_related('user__student_profile')[:50]
                        )
                except ProjectTeamMember.DoesNotExist:
                    pass

        except ProjectTeam.DoesNotExist:
            pass

    # ULTRA-OPTIMIZATION: Use prefetched tasks and milestones (already loaded)
    tasks = list(project.tasks.all()[:50])
    milestones = list(project.milestones.all()[:30])

    # Calculate task statistics (from prefetched data)
    completed_tasks = sum(1 for t in tasks if t.status == 'completed')
    total_tasks = len(tasks)
    
    # Task status breakdown (computed from prefetched data)
    task_status_dict = {}
    status_dict = {status: label for status, label in ProjectTask.STATUS_CHOICES}
    for task in tasks:
        if task.status not in task_status_dict:
            task_status_dict[task.status] = 0
        task_status_dict[task.status] += 1
    
    task_status_counts = [
        {
            'status': status,
            'label': status_dict.get(status, status),
            'count': count
        }
        for status, count in task_status_dict.items()
    ]

    # Milestone statistics (computed from prefetched data)
    completed_milestones = sum(1 for m in milestones if m.is_completed)
    total_milestones = len(milestones)

    # ULTRA-OPTIMIZATION: Only fetch potential members if absolutely needed
    potential_members = []
    if can_manage_team:
        connected_users = Connection.objects.filter(
            Q(sender=request.user, status='accepted') |
            Q(receiver=request.user, status='accepted')
        ).select_related('sender__student_profile', 'receiver__student_profile').only(
            'sender__id', 'sender__student_profile__full_name',
            'receiver__id', 'receiver__student_profile__full_name'
        )[:30]

        existing_member_ids = {project.user.id}
        if team:
            existing_ids = ProjectTeamMember.objects.filter(
                team=team, 
                is_active=True
            ).values_list('user_id', flat=True)
            existing_member_ids.update(existing_ids)

        for conn in connected_users:
            other_user = conn.receiver if conn.sender_id == request.user.id else conn.sender
            if other_user.id not in existing_member_ids:
                potential_members.append(other_user)

    return render(request, 'project_detail.html', {
        'project': project,
        'tech_list': tech_list,
        'looking_list': looking_list,
        'comments': comments,
        'is_owner': request.user == project.user,
        'is_connected': is_connected,
        'connection_status': connection_status,

        # Team information
        'team': team,
        'team_members': team_members,
        'user_team_role': user_team_role,
        'can_manage_team': can_manage_team,
        'pending_invitations': pending_invitations,
        'potential_members': potential_members,

        # Tasks and milestones
        'tasks': tasks,
        'milestones': milestones,

        # Task statistics
        'completed_tasks_count': completed_milestones,
        'total_tasks_count': total_tasks,
        'task_status_counts': task_status_counts,
        'completed_milestones_count': completed_milestones,
        'total_milestones_count': total_milestones,
    })


@login_required
def user_profile_api(request, user_id):
    """
    API endpoint to get comprehensive user profile data including projects
    GET /api/user-profile/<user_id>/
    Returns: User profile, projects, connections, stats, and social info
    """
    try:
        user = User.objects.get(id=user_id)
        profile = StudentProfile.objects.get(user=user)
        
        # Get user statistics
        try:
            stats = UserStats.objects.get(user=user)
        except UserStats.DoesNotExist:
            stats = None
        
        # Get user's projects
        projects = Project.objects.filter(user=user).values(
            'id', 'title', 'description', 'category', 'is_active',
            'created_at', 'updated_at'
        ).annotate(
            likes_count=models.Count('likes'),
            comments_count=models.Count('comments'),
            team_members_count=models.Count('members')
        ).order_by('-created_at')
        
        # Get connection status with current user
        connection_status = None
        if request.user.is_authenticated and request.user.id != user_id:
            try:
                connection = Connection.objects.filter(
                    models.Q(sender=request.user, receiver=user) |
                    models.Q(sender=user, receiver=request.user)
                ).first()
                if connection:
                    connection_status = connection.status
            except Connection.DoesNotExist:
                connection_status = None
        
        # Check if current user follows this user
        is_followed = False
        if request.user.is_authenticated and request.user.id != user_id:
            is_followed = Follow.objects.filter(
                follower=request.user,
                following=user
            ).exists()
        
        # Build response data
        data = {
            # Basic Profile Info
            'id': user.id,
            'username': user.username,
            'email': user.email if request.user.id == user.id else None,  # Only show own email
            'full_name': profile.full_name or user.username,
            'college': profile.college,
            'location': profile.location,
            'bio': profile.bio,
            'profile_photo': profile.profile_photo.url if profile.profile_photo else None,
            'profile_completed': profile.profile_completed,
            'created_at': user.date_joined.isoformat(),
            
            # Skills & Interests
            'skills': profile.skills or [],
            'interests': profile.interests or [],
            'project_interests': profile.project_interests or [],
            'role_preference': profile.role_preference,
            
            # Social Links
            'github': profile.github,
            'linkedin': profile.linkedin,
            'portfolio': profile.portfolio,
            'behance': profile.behance,
            
            # Statistics
            'stats': {
                'projects_created': stats.projects_created if stats else 0,
                'connections': stats.connections_made if stats else 0,
                'likes_received': stats.likes_received if stats else 0,
                'comments_made': stats.comments_made if stats else 0,
                'followers': stats.followers_count if stats else 0,
                'following': stats.following_count if stats else 0,
            } if stats else {
                'projects_created': 0,
                'connections': 0,
                'likes_received': 0,
                'comments_made': 0,
                'followers': 0,
                'following': 0,
            },
            
            # Projects
            'projects': list(projects),
            'projects_count': projects.count(),
            
            # Connection Status (for current user)
            'connection_status': connection_status,  # pending/accepted/rejected or null
            'is_followed': is_followed,
            
            # Online Status
            'is_online': hasattr(profile, 'is_online') and profile.is_online,
        }
        
        return JsonResponse(data, safe=False)
    except User.DoesNotExist:
        return JsonResponse({'error': 'User not found'}, status=404)
    except StudentProfile.DoesNotExist:
        return JsonResponse({'error': 'User profile not found'}, status=404)
    except Exception as e:
        logger.error(f"Error fetching user profile {user_id}: {str(e)}", exc_info=True)
        return JsonResponse({'error': 'Error fetching user profile'}, status=500)


@login_required
def message_view(request):
    """Main messaging page - show conversations (direct messages and group chats)"""
    # Get all users the current user has messaged with or is connected to
    connected_users = Connection.objects.filter(
        Q(sender=request.user, status='accepted') |
        Q(receiver=request.user, status='accepted')
    ).select_related('sender', 'receiver')

    # Extract the other users
    conversation_users = set()
    for conn in connected_users:
        if conn.sender == request.user:
            conversation_users.add(conn.receiver)
        else:
            conversation_users.add(conn.sender)

    # Also include users we've sent messages to (even if not connected)
    sent_messages = Message.objects.filter(sender=request.user).values_list('receiver', flat=True).distinct()
    received_messages = Message.objects.filter(receiver=request.user).values_list('sender', flat=True).distinct()

    for user_id in sent_messages:
        if user_id:  # Skip None values
            try:
                conversation_users.add(User.objects.get(id=user_id))
            except User.DoesNotExist:
                pass  # User was deleted, skip
    for user_id in received_messages:
        if user_id:  # Skip None values
            try:
                conversation_users.add(User.objects.get(id=user_id))
            except User.DoesNotExist:
                pass  # User was deleted, skip

    # Get all group chat rooms where user is a member (ADDED)
    group_chat_rooms = ChatRoom.objects.filter(
        members__user=request.user,
        is_active=True
    ).distinct()

    # Convert to list and sort by most recent message
    conversations = []
    
    # Add direct message conversations
    for user in conversation_users:
        last_message = Message.objects.filter(
            Q(sender=request.user, receiver=user) |
            Q(sender=user, receiver=request.user)
        ).order_by('-created_at').first()

        # Count unread messages from this user
        # A message is unread if there's no MessageReadStatus for the receiver
        all_messages = Message.objects.filter(
            sender=user,
            receiver=request.user
        ).values_list('id', flat=True)
        
        read_message_ids = MessageReadStatus.objects.filter(
            message_id__in=all_messages,
            user=request.user
        ).values_list('message_id', flat=True)
        
        unread_count = len(set(all_messages) - set(read_message_ids))

        conversations.append({
            'type': 'direct',
            'user': user,
            'chat_room': None,
            'last_message': last_message,
            'unread_count': unread_count
        })
    
    # Add group chat conversations (ADDED)
    for room in group_chat_rooms:
        last_message = room.messages.order_by('-created_at').first()
        
        # Count unread messages in group chat
        all_room_messages = room.messages.values_list('id', flat=True)
        read_room_message_ids = MessageReadStatus.objects.filter(
            message_id__in=all_room_messages,
            user=request.user
        ).values_list('message_id', flat=True)
        
        unread_count = len(set(all_room_messages) - set(read_room_message_ids))
        
        conversations.append({
            'type': 'group',
            'user': None,
            'chat_room': room,
            'last_message': last_message,
            'unread_count': unread_count
        })

    # Sort by most recent message
    conversations.sort(key=lambda x: x['last_message'].created_at if x['last_message'] else timezone.now(), reverse=True)

    # Get unread notifications count for badge
    unread_notification_count = Notification.objects.filter(user=request.user, is_read=False).count()

    return render(request, 'features/messages.html', {
        'conversations': conversations,
        'unread_notification_count': unread_notification_count
    })


@login_required
def chat_view(request, user_id):
    """Chat with a specific user"""
    other_user = get_object_or_404(User, id=user_id)

    # Check if users are connected
    connection = Connection.objects.filter(
        Q(sender=request.user, receiver=other_user) |
        Q(sender=other_user, receiver=request.user)
    ).first()

    is_connected = connection and connection.status == 'accepted'

    if request.method == 'POST':
        content = request.POST.get('content', '').strip()
        uploaded_file = request.FILES.get('file')

        # Handle file upload
        if uploaded_file:
            # Validate file size (max 10MB)
            if uploaded_file.size > 10 * 1024 * 1024:
                messages.error(request, 'File size cannot exceed 10MB.')
                return redirect('chat', user_id=user_id)

            # Create File instance
            file_obj = File.objects.create(
                user=request.user,
                file=uploaded_file,
                filename=uploaded_file.name,
                file_size=uploaded_file.size,
                file_type=uploaded_file.content_type
            )

            # Create message with file attachment
            message = Message.objects.create(
                sender=request.user,
                receiver=other_user,
                content=content or f"📎 {uploaded_file.name}"
            )

            # Attach file to message
            MessageFile.objects.create(message=message, file=file_obj)

        elif content:
            # Create regular text message
            message = Message.objects.create(
                sender=request.user,
                receiver=other_user,
                content=content
            )
        else:
            messages.error(request, 'Please enter a message or upload a file.')
            return redirect('chat', user_id=user_id)

        # Create notification for receiver (only if there's content or it's a file)
        if content or uploaded_file:
            notification_message = content[:50] if content else f"📎 {uploaded_file.name}"
            create_notification(
                user=other_user,
                notification_type='message',
                title=f'New message from {request.user.username}',
                message=f'{request.user.username}: {notification_message}...',
                from_user=request.user,
                message_obj=message
            )

        # Mark messages from this user as read (when replying)
        unread_msgs = Message.objects.filter(
            sender=other_user,
            receiver=request.user
        ).exclude(
            read_statuses__user=request.user
        )
        for msg in unread_msgs:
            msg.mark_as_read_by(request.user)

        return redirect('chat', user_id=user_id)

    # Get all messages between users with reaction counts
    messages = Message.objects.filter(
    Q(sender=request.user, receiver=other_user) |
    Q(sender=other_user, receiver=request.user)
    ).order_by('created_at').prefetch_related('files__file', 'reactions')

    # Add reaction counts to each message
    for message in messages:
        reactions = MessageReaction.objects.filter(message=message).values('reaction').annotate(
            count=models.Count('reaction')
        ).order_by('reaction')
        message.reaction_counts = {r['reaction']: r['count'] for r in reactions}

    # Mark received messages as read
    unread_messages = Message.objects.filter(
        sender=other_user,
        receiver=request.user
    ).exclude(
        read_statuses__user=request.user
    )
    for message in unread_messages:
        message.mark_as_read_by(request.user)

    # Generate consistent room name for WebSocket
    room_name = f'user_{min(request.user.id, other_user.id)}_{max(request.user.id, other_user.id)}'

    return render(request, 'features/chat.html', {
        'other_user': other_user,
        'messages': messages,
        'is_connected': is_connected,
        'connection': connection,
        'room_name': room_name
    })


# -------------------------
# Connection Views
# -------------------------
@login_required
def connect_view(request, user_id):
    """AJAX endpoint to send connection request"""
    print(f"DEBUG connect_view: Request method: {request.method}, User: {request.user}")
    if request.method != 'POST':
        print(f"DEBUG connect_view: Method not POST, returning 405")
        return JsonResponse({'success': False, 'message': 'Method not allowed'}, status=405)

    receiver = get_object_or_404(User, id=user_id)

    if receiver == request.user:
        return JsonResponse({'success': False, 'message': 'You cannot connect with yourself!'})

    # Check if connection already exists
    existing = Connection.objects.filter(
        Q(sender=request.user, receiver=receiver) |
        Q(sender=receiver, receiver=request.user)
    ).first()

    if existing:
        if existing.status == 'pending':
            message = f"Connection request already pending with {receiver.username}"
            return JsonResponse({'success': False, 'message': message})
        elif existing.status == 'accepted':
            message = f"You are already connected with {receiver.username}"
            return JsonResponse({'success': False, 'message': message})
        else:
            message = "Connection request was previously rejected"
            return JsonResponse({'success': False, 'message': message})
    else:
        connection = Connection.objects.create(sender=request.user, receiver=receiver)

        # Create notification for receiver
        create_notification(
            user=receiver,
            notification_type='connection_request',
            title=f'Connection request from {request.user.username}',
            message=f'{request.user.username} wants to connect with you.',
            from_user=request.user,
            connection=connection
        )

        message = f"Connection request sent to {receiver.username}!"
        return JsonResponse({'success': True, 'message': message})


def send_connection_request(request, user_id):
    """AJAX endpoint to send connection request (for activity feed)"""
    print(f"DEBUG: Request method: {request.method}, User: {request.user}, Authenticated: {request.user.is_authenticated}")
    
    if not request.user.is_authenticated:
        return JsonResponse({'success': False, 'message': 'You must be logged in'}, status=401)
    
    if request.method != 'POST':
        print(f"DEBUG: Method not POST, returning 405")
        return JsonResponse({'success': False, 'message': 'Method not allowed'}, status=405)

    receiver = get_object_or_404(User, id=user_id)

    if receiver == request.user:
        return JsonResponse({'success': False, 'message': 'You cannot connect with yourself!'})

    # Check if connection already exists
    existing = Connection.objects.filter(
        Q(sender=request.user, receiver=receiver) |
        Q(sender=receiver, receiver=request.user)
    ).first()

    if existing:
        if existing.status == 'pending':
            return JsonResponse({'success': False, 'message': f"Connection request already pending with {receiver.username}"})
        elif existing.status == 'accepted':
            return JsonResponse({'success': False, 'message': f"You are already connected with {receiver.username}"})
        else:
            return JsonResponse({'success': False, 'message': "Connection request was previously rejected"})
    else:
        connection = Connection.objects.create(sender=request.user, receiver=receiver)

        # Create notification for receiver
        create_notification(
            user=receiver,
            notification_type='connection_request',
            title=f'Connection request from {request.user.username}',
            message=f'{request.user.username} wants to connect with you.',
            from_user=request.user,
            connection=connection
        )

        # Create activity
        create_activity(
            user=request.user,
            activity_type='connection_request_sent',
            title=f'Sent connection request to {receiver.username}',
            connection=connection
        )

        return JsonResponse({'success': True, 'message': f"Connection request sent to {receiver.username}!"})


@login_required
def accept_connection(request, connection_id):
    """Accept a connection request"""
    connection = get_object_or_404(Connection, id=connection_id, receiver=request.user)
    connection.status = 'accepted'
    connection.save()

    # Create notification for sender
    create_notification(
        user=connection.sender,
        notification_type='connection_accepted',
        title=f'{request.user.username} accepted your connection request',
        message=f'You are now connected with {request.user.username}!',
        from_user=request.user,
        connection=connection
    )

    messages.success(request, f"You are now connected with {connection.sender.username}!")
    return redirect('my_connections')


@login_required
def reject_connection(request, connection_id):
    """Reject a connection request"""
    connection = get_object_or_404(Connection, id=connection_id, receiver=request.user)
    connection.status = 'rejected'
    connection.save()
    messages.info(request, f"Connection request from {connection.sender.username} rejected")
    return redirect('my_connections')


@login_required
def cancel_connection_request(request, connection_id):
    """Cancel a sent connection request"""
    connection = get_object_or_404(Connection, id=connection_id, sender=request.user, status='pending')
    receiver_name = connection.receiver.username
    connection.delete()
    messages.success(request, f"Connection request to {receiver_name} cancelled")
    return redirect('my_connections')


@login_required
def my_connections(request):
    """View all connections and pending requests"""
    # Pending requests received
    pending_requests = Connection.objects.filter(
        receiver=request.user,
        status='pending'
    ).select_related('sender__student_profile')

    # Accepted connections (both sent and received)
    accepted_connections = Connection.objects.filter(
        Q(sender=request.user, status='accepted') |
        Q(receiver=request.user, status='accepted')
    ).select_related('sender__student_profile', 'receiver__student_profile')

    # Ensure UserStatus exists for connected users
    connected_user_ids = set()
    for conn in accepted_connections:
        connected_user_ids.add(conn.sender.id)
        connected_user_ids.add(conn.receiver.id)
    for user_id in connected_user_ids:
        if user_id != request.user.id:
            UserStatus.objects.get_or_create(user_id=user_id)

    # Sent pending requests
    sent_requests = Connection.objects.filter(
        sender=request.user,
        status='pending'
    ).select_related('receiver__student_profile')
    
    return render(request, 'my_connections.html', {
        'pending_requests': pending_requests,
        'accepted_connections': accepted_connections,
        'sent_requests': sent_requests,
    })


@login_required
def add_reaction(request, message_id):
    """Add or remove a reaction to/from a message via AJAX"""
    if request.method == 'POST':
        reaction_type = request.POST.get('reaction')
        if not reaction_type:
            return JsonResponse({'error': 'Reaction type required'}, status=400)

        try:
            message = Message.objects.get(id=message_id)
            # Check if user can react to this message (must be sender or receiver)
            if request.user not in [message.sender, message.receiver]:
                return JsonResponse({'error': 'Permission denied'}, status=403)

            # Check if reaction already exists
            existing_reaction = MessageReaction.objects.filter(
                message=message,
                user=request.user,
                reaction=reaction_type
            ).first()

            if existing_reaction:
                # Remove reaction
                existing_reaction.delete()
                action = 'removed'
            else:
                # Add reaction
                MessageReaction.objects.create(
                    message=message,
                    user=request.user,
                    reaction=reaction_type
                )
                action = 'added'

            # Get updated reaction counts
            reactions = MessageReaction.objects.filter(message=message).values('reaction').annotate(
                count=models.Count('reaction')
            ).order_by('reaction')

            reaction_data = {r['reaction']: r['count'] for r in reactions}

            return JsonResponse({
                'action': action,
                'reactions': reaction_data
            })

        except Message.DoesNotExist:
            return JsonResponse({'error': 'Message not found'}, status=404)

    return JsonResponse({'error': 'Method not allowed'}, status=405)


@login_required
def download_file(request, file_id):
    """Download a shared file"""
    try:
        file_obj = File.objects.get(id=file_id)
        # Check if user can download this file (must be sender or receiver of the message)
        message_file = MessageFile.objects.filter(file=file_obj).first()
        if not message_file:
            return HttpResponseForbidden("File not accessible")

        message = message_file.message
        if request.user not in [message.sender, message.receiver]:
            return HttpResponseForbidden("Permission denied")

        # Serve the file
        response = HttpResponse(file_obj.file.read(), content_type=file_obj.file_type)
        response['Content-Disposition'] = f'attachment; filename="{file_obj.filename}"'
        return response

    except File.DoesNotExist:
        raise Http404("File not found")


@login_required
def search_messages(request, user_id):
    """Search messages in a chat conversation"""
    other_user = get_object_or_404(User, id=user_id)

    # Check if users are connected
    connection = Connection.objects.filter(
        Q(sender=request.user, receiver=other_user) |
        Q(sender=other_user, receiver=request.user)
    ).first()

    if not connection or connection.status != 'accepted':
        return JsonResponse({'error': 'Not connected with this user'}, status=403)

    query = request.GET.get('q', '').strip()
    if not query:
        return JsonResponse({'results': []})

    # Search messages
    messages = Message.objects.filter(
        Q(sender=request.user, receiver=other_user) |
        Q(sender=other_user, receiver=request.user)
    ).filter(
        Q(content__icontains=query)
    ).select_related('sender', 'receiver').order_by('-created_at')[:20]  # Limit to 20 results

    results = []
    for message in messages:
        # Get reactions for this message
        reactions = MessageReaction.objects.filter(message=message).values('reaction').annotate(
            count=models.Count('reaction')
        ).order_by('reaction')

        results.append({
            'id': message.id,
            'content': message.content,
            'sender': message.sender.username,
            'timestamp': message.created_at.isoformat(),
            'reactions': {r['reaction']: r['count'] for r in reactions}
        })

    return JsonResponse({'results': results})


@login_required
def toggle_theme(request):
    """Toggle between dark and light theme"""
    if request.method == 'POST':
        current_theme = request.POST.get('theme', 'dark')
        new_theme = 'light' if current_theme == 'dark' else 'dark'
        # In a real app, you'd save this to user preferences
        # For now, we'll just return the new theme
        return JsonResponse({'theme': new_theme})

    return JsonResponse({'error': 'Method not allowed'}, status=405)


# -------------------------
# Social Engagement Views
# -------------------------

@login_required
def follow_user(request, user_id):
    """Follow or unfollow a user"""
    target_user = get_object_or_404(User, id=user_id)

    if target_user == request.user:
        messages.error(request, "You cannot follow yourself.")
        return redirect('find_collaborators')

    follow, created = Follow.objects.get_or_create(
        follower=request.user,
        following=target_user,
        defaults={}
    )

    if not created:
        # User was already following, so unfollow
        follow.delete()

        # Remove the follow activity
        Activity.objects.filter(
            user=request.user,
            activity_type='user_followed',
            target_user=target_user
        ).delete()

        messages.success(request, f"You unfollowed {target_user.username}.")
    else:
        # User is now following
        create_notification(
            user=target_user,
            notification_type='user_followed',
            title=f'{request.user.username} started following you',
            message=f'{request.user.username} is now following you',
            from_user=request.user
        )
        messages.success(request, f"You are now following {target_user.username}!")

    # Update user stats
    UserStats.objects.get_or_create(user=request.user, defaults={})[0].update_stats()
    UserStats.objects.get_or_create(user=target_user, defaults={})[0].update_stats()

    return redirect(request.META.get('HTTP_REFERER', 'find_collaborators'))


@login_required
def activity_feed(request):
    """Show activity feed for the current user"""
    # Get users that current user follows
    following_users = Follow.objects.filter(follower=request.user).values_list('following', flat=True)

    # Get activities from followed users and own activities
    activities = Activity.objects.filter(
        Q(user__in=following_users) | Q(user=request.user),
        is_public=True
    ).select_related(
        'user', 'project', 'target_user', 'connection'
    ).order_by('-created_at')[:50]  # Limit to 50 most recent activities

    # Add additional data to activities for template
    for activity in activities:
        # Add activity type for filtering
        if activity.project:
            activity.activity_type = 'project'
            activity.activity_icon = '🚀'
        elif activity.connection:
            activity.activity_type = 'connection'
            activity.activity_icon = '🤝'
        elif activity.comment:
            activity.activity_type = 'comment'
            activity.activity_icon = '💬'
        elif activity.target_user:
            activity.activity_type = 'follow'
            activity.activity_icon = '👥'
        else:
            activity.activity_type = 'general'
            activity.activity_icon = '📱'

        # Add engagement counts (simplified - in real app these would be cached)
        activity.likes_count = 0  # Placeholder
        activity.comments_count = 0  # Placeholder
        
        # Add connection status for the activity user
        if activity.user != request.user:
            try:
                connection = Connection.objects.get(
                    Q(requester=request.user, receiver=activity.user) |
                    Q(requester=activity.user, receiver=request.user)
                )
                if connection.status == 'pending':
                    activity.user.connection_status = 'pending'
                elif connection.status == 'accepted':
                    activity.user.connection_status = 'connected'
                else:
                    activity.user.connection_status = 'none'
            except Connection.DoesNotExist:
                activity.user.connection_status = 'none'
        else:
            activity.user.connection_status = 'self'

    # Get user stats
    user_stats, created = UserStats.objects.get_or_create(user=request.user, defaults={})
    if created or (timezone.now() - user_stats.last_updated).seconds > 300:  # Update every 5 minutes
        user_stats.update_stats()

    # Add followers count to user stats
    user_stats.followers_count = Follow.objects.filter(following=request.user).count()
    user_stats.following_count = following_users.count()

    context = {
        'activities': activities,
        'user_stats': user_stats,
        'following_count': following_users.count(),
    }

    return render(request, 'social/activity_feed.html', context)


@login_required
def user_profile(request, username):
    """View a user's public profile with their activities"""
    try:
        profile_user = get_object_or_404(User, username=username)
    except Http404:
        messages.error(request, "User profile not found.")
        return redirect('main_home')

    try:
        # Get user stats - handle gracefully if not found
        try:
            user_stats = UserStats.objects.get(user=profile_user)
            # Update stats if needed
            if (timezone.now() - user_stats.last_updated).total_seconds() > 300:
                user_stats.update_stats()
        except UserStats.DoesNotExist:
            # Create new stats if doesn't exist
            user_stats = UserStats.objects.create(user=profile_user)
            user_stats.update_stats()

        # Check if current user follows this user (only if user is authenticated)
        is_following = False
        is_own_profile = False
        
        if request.user.is_authenticated:
            is_following = Follow.objects.filter(follower=request.user, following=profile_user).exists()
            is_own_profile = request.user == profile_user

        # Get user's public activities - handle if Activity model doesn't have is_public field
        try:
            activities = Activity.objects.filter(
                user=profile_user,
                is_public=True
            ).select_related(
                'user', 'project', 'target_user', 'connection'
            ).order_by('-created_at')[:20]
        except Exception:
            # If filtering by is_public fails, just get all activities
            activities = Activity.objects.filter(
                user=profile_user
            ).select_related(
                'user', 'project', 'target_user', 'connection'
            ).order_by('-created_at')[:20]

        # Get user's projects (active projects only)
        if is_own_profile:
            projects = Project.objects.filter(user=profile_user).order_by('-created_at')[:6]
        else:
            # For non-owner, show active projects only
            projects = Project.objects.filter(
                user=profile_user,
                is_active=True
            ).order_by('-created_at')[:6]

        # Get user's connections count
        connections_count = Connection.objects.filter(
            Q(sender=profile_user, status='accepted') | Q(receiver=profile_user, status='accepted')
        ).count()

        # Get student profile with error handling
        try:
            student_profile = profile_user.student_profile
        except StudentProfile.DoesNotExist:
            student_profile = None

        context = {
            'profile_user': profile_user,
            'user_stats': user_stats,
            'is_following': is_following,
            'is_own_profile': is_own_profile,
            'activities': activities,
            'projects': projects,
            'connections_count': connections_count,
            'student_profile': student_profile,
        }

        return render(request, 'social/user_profile.html', context)

    except Exception as e:
        logger.error(f"Error loading user profile for {username}: {str(e)}", exc_info=True)
        # Return a simpler profile page if full profile fails
        try:
            student_profile = profile_user.student_profile
        except StudentProfile.DoesNotExist:
            student_profile = None
        
        context = {
            'profile_user': profile_user,
            'student_profile': student_profile,
            'activities': [],
            'projects': [],
            'connections_count': 0,
        }
        return render(request, 'social/user_profile.html', context)


# -------------------------
# Helper Functions for Activities
# -------------------------

def create_activity(user, activity_type, title, description=None, **kwargs):
    """Helper function to create activity records"""
    Activity.objects.create(
        user=user,
        activity_type=activity_type,
        title=title,
        description=description,
        **kwargs
    )


# -------------------------
# Project Team Views
# -------------------------

@login_required
def invite_to_team(request, project_id):
    """Invite a user to join a project team"""
    project = get_object_or_404(Project, id=project_id)

    # Check if user can invite (must be project owner or team owner)
    if project.user != request.user:
        # Check if user is team owner
        try:
            team_member = ProjectTeamMember.objects.get(team__project=project, user=request.user)
            if not team_member.can_invite_members:
                messages.error(request, "You don't have permission to invite team members.")
                return redirect('project_detail', project_id=project_id)
        except ProjectTeamMember.DoesNotExist:
            messages.error(request, "You don't have permission to manage this project.")
            return redirect('project_detail', project_id=project_id)

    if request.method == 'POST':
        user_id = request.POST.get('user_id')
        role = request.POST.get('role', 'contributor')
        message = request.POST.get('message', '').strip()

        try:
            invited_user = User.objects.get(id=user_id)

            # Check if already a team member
            if ProjectTeamMember.objects.filter(team__project=project, user=invited_user, is_active=True).exists():
                messages.error(request, f"{invited_user.username} is already a team member.")
                return redirect('project_detail', project_id=project_id)

            # Check if invitation already exists
            existing_invitation = ProjectTeamInvitation.objects.filter(
                team__project=project, invited_user=invited_user, status='pending'
            ).first()

            if existing_invitation:
                messages.info(request, f"An invitation is already pending for {invited_user.username}.")
                return redirect('project_detail', project_id=project_id)

            # Get or create team
            team, created = ProjectTeam.objects.get_or_create(
                project=project,
                defaults={'name': f"{project.title} Team"}
            )

            # Create invitation (expires in 7 days)
            from django.utils import timezone
            expires_at = timezone.now() + timezone.timedelta(days=7)

            invitation = ProjectTeamInvitation.objects.create(
                team=team,
                invited_user=invited_user,
                invited_by=request.user,
                role=role,
                message=message,
                expires_at=expires_at
            )

            # Create notification
            create_notification(
                user=invited_user,
                notification_type='team_invitation',
                title=f'Team invitation to {project.title}',
                message=f'{request.user.username} invited you to join the team for "{project.title}"',
                from_user=request.user
            )

            messages.success(request, f"Invitation sent to {invited_user.username}!")
            return redirect('project_detail', project_id=project_id)

        except User.DoesNotExist:
            messages.error(request, "User not found.")
            return redirect('project_detail', project_id=project_id)

    # For GET requests, redirect to project detail
    return redirect('project_detail', project_id=project_id)


@login_required
def respond_to_team_invitation(request, invitation_id):
    """Accept or decline a team invitation"""
    invitation = get_object_or_404(ProjectTeamInvitation, id=invitation_id, invited_user=request.user)

    if request.method == 'POST':
        action = request.POST.get('action')

        if action == 'accept':
            if invitation.accept():
                messages.success(request, f"Welcome to the {invitation.team.project.title} team!")
            else:
                messages.error(request, "Could not accept invitation. It may have expired.")
        elif action == 'decline':
            if invitation.decline():
                messages.info(request, "Invitation declined.")
            else:
                messages.error(request, "Could not decline invitation.")

        return redirect('notifications')

    return redirect('notifications')


@login_required
def remove_team_member(request, project_id, user_id):
    """Remove a member from a project team"""
    project = get_object_or_404(Project, id=project_id)

    # Check permissions
    if project.user != request.user:
        try:
            team_member = ProjectTeamMember.objects.get(team__project=project, user=request.user)
            if not team_member.can_invite_members:
                messages.error(request, "You don't have permission to remove team members.")
                return redirect('project_detail', project_id=project_id)
        except ProjectTeamMember.DoesNotExist:
            messages.error(request, "You don't have permission to manage this team.")
            return redirect('project_detail', project_id=project_id)

    try:
        member_to_remove = ProjectTeamMember.objects.get(team__project=project, user_id=user_id, is_active=True)

        # Can't remove the project owner
        if member_to_remove.user == project.user:
            messages.error(request, "Cannot remove the project owner from the team.")
            return redirect('project_detail', project_id=project_id)

        member_to_remove.is_active = False
        member_to_remove.save()

        messages.success(request, f"Removed {member_to_remove.user.username} from the team.")
        return redirect('project_detail', project_id=project_id)

    except ProjectTeamMember.DoesNotExist:
        messages.error(request, "Team member not found.")
        return redirect('project_detail', project_id=project_id)


@login_required
def create_project_task(request, project_id):
    """Create a new task for a project"""
    project = get_object_or_404(Project, id=project_id)

    # Check permissions
    if project.user != request.user:
        try:
            team_member = ProjectTeamMember.objects.get(team__project=project, user=request.user, is_active=True)
            if not team_member.can_manage_tasks:
                messages.error(request, "You don't have permission to create tasks.")
                return redirect('project_detail', project_id=project_id)
        except ProjectTeamMember.DoesNotExist:
            messages.error(request, "You don't have permission to manage this project.")
            return redirect('project_detail', project_id=project_id)

    if request.method == 'POST':
        title = request.POST.get('title', '').strip()
        description = request.POST.get('description', '').strip()
        assigned_to_id = request.POST.get('assigned_to')
        priority = request.POST.get('priority', 'medium')
        due_date = request.POST.get('due_date')

        if not title:
            messages.error(request, "Task title is required.")
            return redirect('project_detail', project_id=project_id)

        # Validate assigned user is team member
        assigned_to = None
        if assigned_to_id:
            try:
                assigned_user = User.objects.get(id=assigned_to_id)
                # Check if assigned user is a team member or project owner
                if (assigned_user != project.user and
                    not ProjectTeamMember.objects.filter(team__project=project, user=assigned_user, is_active=True).exists()):
                    messages.error(request, "Can only assign tasks to team members.")
                    return redirect('project_detail', project_id=project_id)
                assigned_to = assigned_user
            except User.DoesNotExist:
                messages.error(request, "Assigned user not found.")
                return redirect('project_detail', project_id=project_id)

        task = ProjectTask.objects.create(
            project=project,
            title=title,
            description=description,
            assigned_to=assigned_to,
            assigned_by=request.user,
            priority=priority,
            due_date=due_date if due_date else None
        )

        messages.success(request, f"Task '{title}' created successfully!")
        return redirect('project_detail', project_id=project_id)

    return redirect('project_detail', project_id=project_id)


@login_required
def update_task_status(request, task_id):
    """Update the status of a project task"""
    task = get_object_or_404(ProjectTask, id=task_id)

    # Check permissions
    if task.project.user != request.user:
        try:
            team_member = ProjectTeamMember.objects.get(team__project=task.project, user=request.user, is_active=True)
            if not team_member.can_manage_tasks and task.assigned_to != request.user:
                messages.error(request, "You don't have permission to update this task.")
                return JsonResponse({'error': 'Permission denied'}, status=403)
        except ProjectTeamMember.DoesNotExist:
            messages.error(request, "You don't have permission to manage this task.")
            return JsonResponse({'error': 'Permission denied'}, status=403)

    if request.method == 'POST':
        new_status = request.POST.get('status')
        if new_status in dict(ProjectTask.STATUS_CHOICES):
            old_status = task.status
            task.status = new_status
            if new_status == 'completed' and old_status != 'completed':
                task.mark_completed()

                # Create activity for task completion
                create_activity(
                    user=request.user,
                    activity_type='task_completed',
                    title=f"Completed task '{task.title}'",
                    description=f"{request.user.username} completed the task '{task.title}' in project '{task.project.title}'",
                    task=task,
                    project=task.project
                )

            task.save()
            return JsonResponse({'success': True, 'status': new_status})
        else:
            return JsonResponse({'error': 'Invalid status'}, status=400)

    return JsonResponse({'error': 'Method not allowed'}, status=405)


@login_required
def create_project_milestone(request, project_id):
    """Create a milestone for a project"""
    project = get_object_or_404(Project, id=project_id)

    # Check permissions (only project owner and team owners can create milestones)
    if project.user != request.user:
        try:
            team_member = ProjectTeamMember.objects.get(team__project=project, user=request.user, is_active=True)
            if team_member.role != 'owner':
                messages.error(request, "Only team owners can create milestones.")
                return redirect('project_detail', project_id=project_id)
        except ProjectTeamMember.DoesNotExist:
            messages.error(request, "You don't have permission to manage this project.")
            return redirect('project_detail', project_id=project_id)

    if request.method == 'POST':
        title = request.POST.get('title', '').strip()
        description = request.POST.get('description', '').strip()
        due_date = request.POST.get('due_date')

        if not title:
            messages.error(request, "Milestone title is required.")
            return redirect('project_detail', project_id=project_id)

        ProjectMilestone.objects.create(
            project=project,
            title=title,
            description=description,
            due_date=due_date if due_date else None
        )

        messages.success(request, f"Milestone '{title}' created successfully!")
        return redirect('project_detail', project_id=project_id)


@login_required
def mark_milestone_complete(request, milestone_id):
    """Mark a milestone as completed"""
    milestone = get_object_or_404(ProjectMilestone, id=milestone_id)

    # Check permissions (only project owner or team owners can complete milestones)
    if milestone.project.user != request.user:
        try:
            team_member = ProjectTeamMember.objects.get(team__project=milestone.project, user=request.user, is_active=True)
            if team_member.role != 'owner':
                messages.error(request, "Only team owners can complete milestones.")
                return redirect('project_detail', project_id=milestone.project.id)
        except ProjectTeamMember.DoesNotExist:
            messages.error(request, "You don't have permission to complete this milestone.")
            return redirect('project_detail', project_id=milestone.project.id)

    if not milestone.is_completed:
        milestone.mark_completed(user=request.user)
        messages.success(request, f"Milestone '{milestone.title}' marked as completed!")
    else:
        messages.info(request, "Milestone is already completed.")

    return redirect('project_detail', project_id=milestone.project.id)


# -------------------------
# API Views for Profile Statistics
# -------------------------

@login_required
def user_stats_api(request):
    """API endpoint to get user statistics for profile page"""
    try:
        user_stats, created = UserStats.objects.get_or_create(user=request.user, defaults={})
        if created or (timezone.now() - user_stats.last_updated).seconds > 300:  # Update every 5 minutes
            user_stats.update_stats()

        data = {
            'projects_created': user_stats.projects_created,
            'connections_made': user_stats.connections_made,
            'likes_received': user_stats.likes_received,
            'comments_made': user_stats.comments_made,
            'projects_joined': user_stats.projects_joined,
            'tasks_completed': user_stats.tasks_completed,
        }
        return JsonResponse(data)
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)


def check_username_availability(request):
    """API endpoint to check if username is available"""
    username = request.GET.get('username', '').strip()

    if not username:
        return JsonResponse({'available': False, 'message': 'Username is required'})

    if len(username) < 3:
        return JsonResponse({'available': False, 'message': 'Username must be at least 3 characters'})

    # Check if username matches pattern
    import re
    if not re.match(r'^[\w.@+-]{1,150}$', username):
        return JsonResponse({'available': False, 'message': 'Invalid username format'})

    # Check if username exists
    available = not User.objects.filter(username__iexact=username).exists()

    return JsonResponse({
        'available': available,
        'message': 'Username available' if available else 'Username already taken'
    })


def check_email_availability(request):
    """API endpoint to check if email is available"""
    email = request.GET.get('email', '').strip()

    if not email:
        return JsonResponse({'available': False, 'message': 'Email is required'})

    # Basic email validation
    import re
    if not re.match(r'^[^\s@]+@[^\s@]+\.[^\s@]+$', email):
        return JsonResponse({'available': False, 'message': 'Invalid email format'})

    # Check if email exists
    available = not User.objects.filter(email__iexact=email).exists()

    return JsonResponse({
        'available': available,
        'message': 'Email available' if available else 'Email already registered'
    })


def home_api(request):
    """SIMPLE PUBLIC API - No authentication required"""
    return JsonResponse({
        'success': True,
        'message': 'API is working!',
        'data': {
            'total_projects': 1250,
            'active_users': 890,
            'total_connections': 2100,
            'success_stories': 45
        },
        'timestamp': timezone.now().isoformat()
    })


def api_root(request):
    """Enhanced API root page with documentation and examples"""
    api_endpoints = {
        'home': {
            'url': '/api/home/',
            'method': 'GET',
            'description': 'Get home page data including statistics and project feed',
            'auth_required': True,
            'example': '/api/home/',
            'response': {
                'success': True,
                'user': {'id': 1, 'username': 'johndoe', 'full_name': 'John Doe'},
                'statistics': {
                    'total_projects': 1250,
                    'active_users': 890,
                    'total_connections': 2100,
                    'success_stories': 45
                },
                'feed': [{'id': 1, 'title': 'Project Title', 'description': '...'}],
                'timestamp': '2025-11-03T16:00:00Z'
            }
        },
        'check_username': {
            'url': '/api/check-username/?username={username}',
            'method': 'GET',
            'description': 'Check if a username is available for registration',
            'auth_required': True,
            'example': '/api/check-username/?username=johndoe',
            'response': {
                'available': True,
                'message': 'Username available'
            }
        },
        'check_email': {
            'url': '/api/check-email/?email={email}',
            'method': 'GET',
            'description': 'Check if an email is available for registration',
            'auth_required': True,
            'example': '/api/check-email/?email=johndoe@example.com',
            'response': {
                'available': True,
                'message': 'Email available'
            }
        },
        'user_profile': {
            'url': '/api/user-profile/{user_id}/',
            'method': 'GET',
            'description': 'Get detailed user profile information including college, interests, and bio',
            'auth_required': True,
            'example': '/api/user-profile/1/',
            'response': {
                'id': 1,
                'username': 'johndoe',
                'full_name': 'John Doe',
                'college': 'MIT',
                'location': 'Boston, MA',
                'interests': 'python, javascript, ai',
                'bio': 'Computer Science student passionate about AI and web development',
                'profile_photo': '/media/profile_photos/john.jpg'
            }
        },
        'user_stats': {
            'url': '/api/user-stats/',
            'method': 'GET',
            'description': 'Get comprehensive user statistics and activity metrics',
            'auth_required': True,
            'example': '/api/user-stats/',
            'response': {
                'projects_created': 5,
                'connections_made': 23,
                'likes_received': 45,
                'comments_made': 12,
                'projects_joined': 3,
                'tasks_completed': 28
            }
        },
        'projects_list': {
            'url': '/api/projects/',
            'method': 'GET',
            'description': 'List all projects with filtering and pagination support',
            'auth_required': False,
            'example': '/api/projects/?category=web&skills=react',
            'response': {
                'count': 25,
                'next': '/api/projects/?page=2',
                'previous': None,
                'results': [
                    {
                        'id': 1,
                        'title': 'E-commerce Platform',
                        'description': 'Full-stack e-commerce solution',
                        'technologies': 'React, Node.js, MongoDB',
                        'user': 'johndoe',
                        'created_at': '2025-11-03T10:00:00Z'
                    }
                ]
            }
        },
        'connections': {
            'url': '/api/connections/',
            'method': 'GET',
            'description': 'Get user connections and pending requests',
            'auth_required': True,
            'example': '/api/connections/',
            'response': {
                'accepted': [
                    {
                        'id': 1,
                        'user': 'johndoe',
                        'full_name': 'John Doe',
                        'college': 'MIT',
                        'connected_at': '2025-10-15T14:30:00Z'
                    }
                ],
                'pending': [
                    {
                        'id': 2,
                        'user': 'janedoe',
                        'full_name': 'Jane Doe',
                        'college': 'Stanford'
                    }
                ]
            }
        },
        'messages': {
            'url': '/api/messages/{user_id}/',
            'method': 'GET',
            'description': 'Get message history with a specific user',
            'auth_required': True,
            'example': '/api/messages/2/',
            'response': {
                'messages': [
                    {
                        'id': 1,
                        'sender': 'johndoe',
                        'content': 'Hey, interested in collaborating?',
                        'timestamp': '2025-11-03T15:30:00Z',
                        'is_read': True
                    }
                ],
                'unread_count': 0
            }
        },
        'notifications': {
            'url': '/api/notifications/',
            'method': 'GET',
            'description': 'Get user notifications and activity feed',
            'auth_required': True,
            'example': '/api/notifications/',
            'response': {
                'notifications': [
                    {
                        'id': 1,
                        'type': 'connection_request',
                        'title': 'New connection request',
                        'message': 'johndoe wants to connect',
                        'created_at': '2025-11-03T16:00:00Z',
                        'is_read': False
                    }
                ],
                'unread_count': 3
            }
        }
    }

    context = {
        'api_endpoints': api_endpoints,
        'api_base_url': request.build_absolute_uri('/api/'),
        'auth_methods': [
            'Session Authentication (for web app)',
            'Token Authentication (for mobile/external apps)',
            'Basic Authentication (for testing)'
        ],
        'response_formats': ['JSON', 'XML (via Accept header)'],
        'rate_limits': '1000 requests/hour per user',
        'contact_info': 'API Support: support@unisinq.com'
    }

    return render(request, 'api_root.html', context)


# =============================================
# College Management APIs
# =============================================

def college_search_api(request):
    """
    API endpoint for college autocomplete search
    GET /api/college-search/?q=IIT
    """
    from .college_utils import CollegeManager
    
    query = request.GET.get('q', '').strip()
    
    if not query or len(query) < 1:
        return JsonResponse({'results': []})
    
    try:
        results = CollegeManager.search_colleges(query, max_results=10)
        return JsonResponse({
            'success': True,
            'results': results,
            'count': len(results)
        })
    except Exception as e:
        print(f"❌ College search error: {e}")
        return JsonResponse({
            'success': False,
            'error': str(e)
        }, status=500)


@login_required
def validate_college_api(request):
    """
    API endpoint to validate if a college exists
    POST /api/validate-college/
    Body: {'college': 'IIT Bombay'}
    """
    from .college_utils import CollegeManager
    
    if request.method != 'POST':
        return JsonResponse({'error': 'Method not allowed'}, status=405)
    
    try:
        import json
        data = json.loads(request.body)
        college_name = data.get('college', '').strip()
        
        if not college_name:
            return JsonResponse({
                'valid': False,
                'message': 'College name is required'
            })
        
        # Check if college exists or is custom
        is_valid = CollegeManager.validate_college(college_name) or len(college_name) >= 3
        
        return JsonResponse({
            'valid': is_valid,
            'college': college_name,
            'message': 'Valid college' if is_valid else 'Please enter a valid college name'
        })
    except Exception as e:
         print(f"❌ College validation error: {e}")
         return JsonResponse({
             'error': str(e)
         }, status=500)
