"""Public entry point for sending SMS. Never raises: failures are logged and returned."""

import logging

from django.conf import settings
from django.utils.module_loading import import_string

from .base import SmsProvider, SmsResult
from .phone import normalize_mobile

logger = logging.getLogger("api.sms")

PROVIDERS = {"console": "api.sms.console.ConsoleSmsProvider"}


def get_provider() -> SmsProvider:
    """Resolve SMS_PROVIDER: a short name in PROVIDERS or a dotted path to a SmsProvider subclass."""
    name = getattr(settings, "SMS_PROVIDER", "console")
    return import_string(PROVIDERS.get(name, name))()


def send_sms(to, text: str, purpose: str = "", log_text: bool = True) -> SmsResult:
    """
    Send one SMS and record it in SmsLog.
    `purpose` e.g. "otp", "signup", "order", "discount". Pass log_text=False for secrets (OTP codes).
    """
    from ..models import SmsLog

    number = normalize_mobile(to)
    provider_name = getattr(settings, "SMS_PROVIDER", "console")
    if not number:
        result = SmsResult(ok=False, error="invalid mobile number")
    else:
        try:
            result = get_provider().send(number, text)
        except Exception as exc:  # a gateway outage must never break the caller
            logger.exception("SMS provider failed")
            result = SmsResult(ok=False, error=str(exc)[:200])
    try:
        SmsLog.objects.create(
            to=number or str(to)[:20],
            text=text if log_text else "[hidden]",
            purpose=purpose,
            provider=provider_name,
            status=SmsLog.SENT if result.ok else SmsLog.FAILED,
            provider_message_id=result.message_id,
            error=result.error,
        )
    except Exception:
        logger.exception("Could not write SmsLog")
    return result
