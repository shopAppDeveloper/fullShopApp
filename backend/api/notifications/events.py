"""Business events -> admin alerts. Views call these helpers; stock alerts hook into Oscar signals."""

import logging

from django.conf import settings
from django.db.models.signals import post_save, pre_save
from oscar.core.loading import get_model

from . import base
from .dispatcher import notify_admin

logger = logging.getLogger("api.notifications")
StockRecord = get_model("partner", "StockRecord")


def _customer(user, fallback=""):
    if user is None or not getattr(user, "pk", None):
        return fallback or "مهمان"
    return user.get_full_name() or user.email or user.get_username()


def order_placed(order) -> None:
    notify_admin(base.ORDER_NEW, {
        "number": order.number,
        "total": str(order.total_incl_tax),
        "customer": _customer(order.user, order.guest_email),
    })


def signup(user) -> None:
    notify_admin(base.SIGNUP_NEW, {"customer": _customer(user)})


def payment_ok(order_number, amount, ref_id="") -> None:
    notify_admin(base.PAYMENT_OK, {"number": order_number, "amount": amount, "ref_id": ref_id})


def payment_failed(order_number, reason="") -> None:
    notify_admin(base.PAYMENT_FAILED, {"number": order_number, "reason": reason})


# ---- low stock: alert once each time stock crosses the threshold downwards ----

def _remember_old_level(sender, instance, **kwargs):
    old = None
    if instance.pk:
        old = (StockRecord.objects.filter(pk=instance.pk)
               .values_list("num_in_stock", "num_allocated").first())
    instance._old_net = None if not old or old[0] is None else old[0] - (old[1] or 0)


def _alert_if_low(sender, instance, created, **kwargs):
    if not instance.product.get_product_class().track_stock or instance.num_in_stock is None:
        return
    threshold = settings.LOW_STOCK_THRESHOLD
    net = instance.num_in_stock - (instance.num_allocated or 0)
    old = getattr(instance, "_old_net", None)
    if net <= threshold and (old is None or old > threshold):
        notify_admin(base.STOCK_LOW, {"title": instance.product.get_title(), "stock": max(net, 0)})


def connect_signals() -> None:
    pre_save.connect(_remember_old_level, sender=StockRecord, dispatch_uid="stock_old")
    post_save.connect(_alert_if_low, sender=StockRecord, dispatch_uid="stock_low")
