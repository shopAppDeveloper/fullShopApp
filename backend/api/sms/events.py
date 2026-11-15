"""Customer SMS for business events (sent after the DB transaction commits; never raises)."""

import logging

from django.conf import settings
from django.db import transaction

from ..models import Profile
from .service import send_sms

logger = logging.getLogger("api.sms")

SIGNUP_TEXT = "به فروشگاه خوش آمدید! ثبت‌نام شما با موفقیت انجام شد."
ORDER_TEXT = "سفارش شما با شماره {number} ثبت شد. از خرید شما سپاسگزاریم."


def _enabled():
    return getattr(settings, "SMS_EVENTS_ENABLED", True)


def _mobile_of(user):
    p = Profile.objects.filter(user_id=user.pk).only("mobile").first() if user and user.pk else None
    return p.mobile if p else None


def _safe_send(mobile, text, purpose):
    if mobile:
        try:
            send_sms(mobile, text, purpose=purpose)
        except Exception:
            logger.exception("SMS event failed")


def signup_sms(user) -> None:
    if _enabled():
        mobile = _mobile_of(user)
        transaction.on_commit(lambda: _safe_send(mobile, SIGNUP_TEXT, "signup"))


def order_placed_sms(order) -> None:
    if _enabled():
        mobile = _mobile_of(order.user)
        if not mobile and order.shipping_address_id:
            mobile = order.shipping_address.phone_number and str(order.shipping_address.phone_number)
        text = ORDER_TEXT.format(number=order.number)
        transaction.on_commit(lambda: _safe_send(mobile, text, "order"))
