from allauth.socialaccount.adapter import DefaultSocialAccountAdapter
from allauth.socialaccount.models import SocialApp
from django.contrib.auth.models import User


class CustomSocialAccountAdapter(DefaultSocialAccountAdapter):
    def get_app(self, request, provider, client_id=None):
        """Override get_app to handle MultipleObjectsReturned gracefully"""
        try:
            return super().get_app(request, provider, client_id)
        except:
            # If super fails, try to get the first matching app
            app = SocialApp.objects.filter(provider=provider).first()
            if app:
                return app
            raise
    
    def pre_social_login(self, request, sociallogin):
        """Auto-link social account to existing user with same email"""
        if sociallogin.is_existing:
            return
        
        try:
            # Check if email already exists
            email = sociallogin.account.extra_data.get('email', '')
            if email:
                existing_user = User.objects.get(email=email)
                # Link the social account to existing user
                sociallogin.connect(request, existing_user)
        except User.DoesNotExist:
            pass
        except User.MultipleObjectsReturned:
            pass
