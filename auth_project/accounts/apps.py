from django.apps import AppConfig


class AccountsConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'accounts'
    
    def ready(self):
        """
        Import signal handlers when app is ready
        This ensures real-time updates are active
        """
        try:
            import accounts.signals_realtime
            accounts.signals_realtime.ready()
        except Exception as e:
            import logging
            logger = logging.getLogger(__name__)
            logger.error(f"Error loading signals_realtime: {str(e)}")
