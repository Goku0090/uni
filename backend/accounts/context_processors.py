"""
Custom context processors for templates
"""
import os


def google_analytics(request):
    """
    Add Google Analytics tracking ID to template context
    
    Usage in template:
        {% if google_analytics_id %}
            <!-- Google Analytics script -->
        {% endif %}
    
    Set via environment variable:
        GOOGLE_ANALYTICS_ID=G-K0PB5TRR26
    """
    return {
        'google_analytics_id': os.getenv('GOOGLE_ANALYTICS_ID', ''),
    }


def site_config(request):
    """
    Add general site configuration to context
    """
    return {
        'site_name': os.getenv('SITE_NAME', 'UniSinq'),
        'site_description': os.getenv('SITE_DESCRIPTION', 'Connect. Collaborate. Create.'),
    }
