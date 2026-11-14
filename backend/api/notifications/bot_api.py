"""Shared sender for Telegram-style bot APIs (`POST {base}/bot{token}/sendMessage`)."""

import json
import logging
import urllib.request

from .base import AdminChannel

logger = logging.getLogger("api.notifications")


class BotApiChannel(AdminChannel):
    """Telegram and Bale expose the same sendMessage call; subclasses only set the settings."""

    def __init__(self, token: str, chat_ids: list[str], api_base: str, timeout: float = 5):
        self.token = token
        self.chat_ids = chat_ids
        self.api_base = api_base.rstrip("/")
        self.timeout = timeout

    def is_configured(self) -> bool:
        return bool(self.token and self.chat_ids)

    def _post(self, chat_id: str, text: str) -> None:
        url = f"{self.api_base}/bot{self.token}/sendMessage"
        body = json.dumps({"chat_id": chat_id, "text": text}).encode()
        req = urllib.request.Request(url, body, {"Content-Type": "application/json"})
        with urllib.request.urlopen(req, timeout=self.timeout) as resp:  # noqa: S310 (fixed https base)
            resp.read()

    def send(self, text: str) -> None:
        for chat_id in self.chat_ids:
            try:
                self._post(chat_id, text)
            except Exception:
                # Never log the URL: it contains the bot token.
                logger.exception("%s: could not notify chat %s", self.name, chat_id)
