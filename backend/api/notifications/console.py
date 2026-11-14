import logging

from django.conf import settings

from .base import AdminChannel

logger = logging.getLogger("api.notifications")


class ConsoleChannel(AdminChannel):
    """Development channel: prints alerts to the log when enabled."""

    name = "console"

    def is_configured(self) -> bool:
        return settings.NOTIFY_CONSOLE

    def send(self, text: str) -> None:
        logger.warning("[admin notification]\n%s", text)
