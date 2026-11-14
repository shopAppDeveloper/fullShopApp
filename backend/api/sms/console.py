"""Development provider: prints the message instead of sending it."""

import logging

from .base import SmsProvider, SmsResult

logger = logging.getLogger("api.sms")


class ConsoleSmsProvider(SmsProvider):
    name = "console"

    def send(self, to: str, text: str) -> SmsResult:
        logger.warning("[SMS console] to=%s text=%s", to, text)
        return SmsResult(ok=True, message_id="console")
