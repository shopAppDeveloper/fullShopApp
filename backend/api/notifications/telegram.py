from django.conf import settings

from .bot_api import BotApiChannel


class TelegramChannel(BotApiChannel):
    name = "telegram"

    def __init__(self):
        super().__init__(
            settings.TELEGRAM_BOT_TOKEN,
            settings.TELEGRAM_ADMIN_CHAT_IDS,
            settings.TELEGRAM_API_BASE,
            settings.NOTIFY_TIMEOUT,
        )
