"""Shipping methods offered at checkout. Add a class here (and to METHODS) to offer a new one."""

from decimal import Decimal

from django.conf import settings
from oscar.apps.shipping.methods import FixedPrice


class PostShipping(FixedPrice):
    """Delivery by Iran Post. The price (whole Toman, 0 = free) comes from POST_SHIPPING_PRICE."""

    code = "post"
    name = "ارسال با پست"
    description = "ارسال سفارش با پست پیشتاز"

    def __init__(self):
        price = Decimal(settings.POST_SHIPPING_PRICE)
        super().__init__(charge_excl_tax=price, charge_incl_tax=price)  # no tax on shipping


METHODS = {PostShipping.code: PostShipping}
DEFAULT_METHOD = PostShipping.code


def get_method(code=None):
    """Return a shipping method instance for `code`, or None if it does not exist."""
    cls = METHODS.get(code or DEFAULT_METHOD)
    return cls() if cls else None
