"""Payment flow: create a gateway session for an order, and settle it when the customer returns."""

import logging

from django.db import transaction
from django.utils import timezone

from ..accounts import real_email
from ..models import Payment, Profile
from ..notifications import events
from ..payments import methods, zarinpal
from . import orders as order_service

logger = logging.getLogger(__name__)


def order_amount(order) -> int:
    """Whole Toman owed for the order."""
    return int(order.total_incl_tax)


def start_payment(order, *, method=None, callback_url: str) -> str:
    """Start paying `order` with the chosen method code; returns the URL to redirect the customer to."""
    chosen = methods.get_method(method)
    if chosen is None:
        raise ValueError("unknown or disabled payment method")
    return chosen.start(order, callback_url)


def start_zarinpal(order, *, callback_url: str) -> str:
    """Request a Zarinpal session for `order` and return the gateway URL."""
    amount = order_amount(order)
    profile = Profile.objects.filter(user_id=order.user_id).first() if order.user_id else None
    authority = zarinpal.request_payment(
        amount=amount,
        callback_url=callback_url,
        description=f"سفارش {order.number}",
        mobile=profile.mobile if profile else "",
        email=real_email(order.user) if order.user_id else "",
        order_number=str(order.number),
    )
    Payment.objects.create(order=order, amount=amount, authority=authority, method="zarinpal")
    return zarinpal.start_url(authority)


def verify_payment(*, authority: str, status_param: str):
    """
    Settle the payment named by `authority` (from the gateway redirect). Idempotent.
    Returns the Payment, or None if the authority is unknown. The amount always comes from our database.
    """
    with transaction.atomic():
        payment = Payment.objects.select_for_update().select_related("order").filter(authority=authority).first()
        if payment is None:
            return None
        if payment.status != Payment.PENDING:
            return payment  # already settled: a repeated callback changes nothing
        order = payment.order
        number = str(order.number)

        if status_param != "OK":
            payment.status, payment.error = Payment.FAILED, "cancelled by customer"
            payment.save(update_fields=["status", "error"])
            events.payment_failed(number, "انصراف از پرداخت")
            return payment

        try:
            result = zarinpal.verify_payment(amount=payment.amount, authority=authority)
        except zarinpal.ZarinpalError as exc:
            # Gateway hiccup: leave the payment pending so the customer can be re-verified/retried.
            logger.warning("Zarinpal verify error for order %s: %s", number, exc)
            return payment

        payment.verified_at = timezone.now()
        if result.ok:
            payment.status, payment.ref_id, payment.card_pan = Payment.PAID, result.ref_id, result.card_pan
            payment.save(update_fields=["status", "ref_id", "card_pan", "verified_at"])
            order_service.mark_order_paid(order, ref_id=result.ref_id)
            events.payment_ok(number, payment.amount, result.ref_id)
        else:
            payment.status, payment.error = Payment.FAILED, f"verify code {result.code}"
            payment.save(update_fields=["status", "error", "verified_at"])
            order_service.mark_order_payment_failed(order, reason=payment.error)
            events.payment_failed(number, payment.error)
        return payment
