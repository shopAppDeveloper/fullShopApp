"""
Payment method registry. To add a provider: implement `start(order, callback_url) -> redirect URL`,
a callback/verify endpoint, and register a PaymentMethod below. The checkout lists whatever is enabled.
"""

from dataclasses import dataclass
from typing import Callable

from django.conf import settings


@dataclass(frozen=True)
class PaymentMethod:
    code: str
    name: str
    description: str
    logo: str  # path under the storefront's /public
    is_enabled: Callable[[], bool]
    start: Callable  # (order, callback_url) -> redirect URL


def _zarinpal_start(order, callback_url):
    from ..services import payments

    return payments.start_zarinpal(order, callback_url=callback_url)


ZARINPAL = PaymentMethod(
    code="zarinpal",
    name="پرداخت آنلاین (زرین‌پال)",
    description="پرداخت امن با کارت‌های عضو شتاب",
    logo="/images/checkout/zarinpal.svg",
    # In development the radio is always shown so the checkout can be tried without credentials.
    is_enabled=lambda: bool(settings.ZARINPAL_MERCHANT_ID) or settings.DEBUG,
    start=_zarinpal_start,
)

METHODS = {m.code: m for m in (ZARINPAL,)}


def enabled_methods():
    return [m for m in METHODS.values() if m.is_enabled()]


def get_method(code=None):
    """The enabled method named `code` (or the first enabled one), else None."""
    available = enabled_methods()
    if not code:
        return available[0] if available else None
    return next((m for m in available if m.code == code), None)
