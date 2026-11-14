"""Admin notification channels (Telegram / Bale). A channel is active once its token and chat ids are set."""

import os

from .env import env_bool


def _ids(name):
    return [i.strip() for i in os.getenv(name, "").split(",") if i.strip()]


TELEGRAM_BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN", "")
TELEGRAM_ADMIN_CHAT_IDS = _ids("TELEGRAM_ADMIN_CHAT_IDS")
TELEGRAM_API_BASE = os.getenv("TELEGRAM_API_BASE", "https://api.telegram.org")

BALE_BOT_TOKEN = os.getenv("BALE_BOT_TOKEN", "")
BALE_ADMIN_CHAT_IDS = _ids("BALE_ADMIN_CHAT_IDS")
BALE_API_BASE = os.getenv("BALE_API_BASE", "https://tapi.bale.ai")

NOTIFY_CONSOLE = env_bool("NOTIFY_CONSOLE", False)
NOTIFY_ASYNC = env_bool("NOTIFY_ASYNC", True)
NOTIFY_TIMEOUT = float(os.getenv("NOTIFY_TIMEOUT", "5"))
LOW_STOCK_THRESHOLD = int(os.getenv("LOW_STOCK_THRESHOLD", "5"))
BOT_WEBHOOK_SECRET = os.getenv("BOT_WEBHOOK_SECRET", "")  # empty = webhook disabled
