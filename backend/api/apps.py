"""
Configuration for our API Django application.
"""

from django.apps import AppConfig


class ApiConfig(AppConfig):
    """
    Registers the API application with Django.
    """

    default_auto_field = "django.db.models.BigAutoField"

    name = "api"

    def ready(self):
        from .notifications.events import connect_signals

        connect_signals()
