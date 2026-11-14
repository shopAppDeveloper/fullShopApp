"""`notify_admin(event, data)`: fan an event out to every configured channel without ever raising."""

import logging
import threading

from django.conf import settings
from django.db import transaction

from . import base
from .bale import BaleChannel
from .console import ConsoleChannel
from .messages import render
from .telegram import TelegramChannel

logger = logging.getLogger("api.notifications")

CHANNELS = (TelegramChannel, BaleChannel, ConsoleChannel)


def active_channels() -> list:
    out = []
    for cls in CHANNELS:
        try:
            ch = cls()
            if ch.is_configured():
                out.append(ch)
        except Exception:
            logger.exception("Bad notification channel %s", cls.__name__)
    return out


def _deliver(text: str) -> None:
    for ch in active_channels():
        try:
            ch.send(text)
        except Exception:
            logger.exception("Channel %s failed", ch.name)


def notify_admin(event: str, data: dict | None = None) -> None:
    """
    Queue an alert. Sent after the current DB transaction commits (so a rolled-back
    order is never announced), in a background thread with a short timeout.
    """
    if event not in base.EVENTS:
        logger.warning("Unknown admin event %s", event)
        return
    try:
        text = render(event, data or {})
    except Exception:
        logger.exception("Could not render %s", event)
        return

    def run():
        if getattr(settings, "NOTIFY_ASYNC", True):
            threading.Thread(target=_deliver, args=(text,), daemon=True).start()
        else:
            _deliver(text)

    transaction.on_commit(run)
