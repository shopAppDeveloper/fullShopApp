from django.conf import settings

from .bot_api import BotApiChannel


class BaleChannel(BotApiChannel):
    """Bale's bot API mirrors Telegram's (same method names), only the host differs."""

    name = "bale"

    def __init__(self):
        super().__init__(
            settings.BALE_BOT_TOKEN,
            settings.BALE_ADMIN_CHAT_IDS,
            settings.BALE_API_BASE,
            settings.NOTIFY_TIMEOUT,
        )
