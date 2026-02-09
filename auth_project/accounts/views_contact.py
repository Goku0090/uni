# =============================================
# PRIVACY POLICY & CONTACT US VIEWS
# =============================================

from django.shortcuts import render
from django.http import JsonResponse
from django.core.mail import send_mail
from django.conf import settings
from django.utils import timezone
import logging

logger = logging.getLogger(__name__)


def privacy_policy_view(request):
    """Display the privacy policy page."""
    return render(request, 'privacy_policy.html')


def terms_of_service_view(request):
    """Display the terms of service page."""
    return render(request, 'terms_of_service.html')


def contact_us_view(request):
    """Display the contact us page with form."""
    return render(request, 'contact_us.html')


def contact_submit(request):
    """Handle contact form submission and send email."""
    if request.method == 'POST':
        try:
            name = request.POST.get('name', '').strip()
            email = request.POST.get('email', '').strip()
            subject = request.POST.get('subject', '').strip()
            category = request.POST.get('category', '').strip()
            message = request.POST.get('message', '').strip()

            # Validation
            if not all([name, email, subject, message]):
                return JsonResponse({
                    'success': False,
                    'message': 'Please fill in all required fields.'
                }, status=400)

            # Validate email format
            if '@' not in email or '.' not in email.split('@')[1]:
                return JsonResponse({
                    'success': False,
                    'message': 'Please enter a valid email address.'
                }, status=400)

            # Prevent spam - max message length
            if len(message) > 5000:
                return JsonResponse({
                    'success': False,
                    'message': 'Message is too long. Maximum 5000 characters.'
                }, status=400)

            # Send email to support
            email_subject = f"UniSinq Contact Form: {subject}"
            email_body = f"""
New Contact Form Submission:

Name: {name}
Email: {email}
Category: {category if category else 'Not specified'}
Subject: {subject}

Message:
{message}

---
User IP: {get_client_ip(request)}
Timestamp: {timezone.now()}
            """

            # Send to support email
            send_mail(
                email_subject,
                email_body,
                settings.DEFAULT_FROM_EMAIL,
                ['support@unisinq.com'],
                fail_silently=False,
            )

            # Send confirmation email to user
            confirmation_body = f"""
Hi {name},

Thank you for reaching out to UniSinq! We've received your message and will get back to you within 24 hours.

Message Details:
- Subject: {subject}
- Category: {category if category else 'General'}

If you need immediate assistance, please reply to this email or visit our support page.

Best regards,
UniSinq Team
            """

            send_mail(
                'We received your message - UniSinq Support',
                confirmation_body,
                settings.DEFAULT_FROM_EMAIL,
                [email],
                fail_silently=False,
            )

            logger.info(f"Contact form submission received from {email}")

            return JsonResponse({
                'success': True,
                'message': 'Thank you! Your message has been sent successfully.'
            })

        except Exception as e:
            logger.error(f"Error processing contact form: {str(e)}")
            return JsonResponse({
                'success': False,
                'message': 'An error occurred while sending your message. Please try again later.'
            }, status=500)

    return JsonResponse({'success': False}, status=405)


def get_client_ip(request):
    """Get client IP address from request."""
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[0]
    else:
        ip = request.META.get('REMOTE_ADDR')
    return ip
