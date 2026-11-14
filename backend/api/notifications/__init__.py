"""Admin alerts (Telegram / Bale / console). Use `from api.notifications import notify_admin`."""

from .base import ORDER_NEW, PAYMENT_FAILED, PAYMENT_OK, SIGNUP_NEW, STOCK_LOW
from .dispatcher import notify_admin

__all__ = ["notify_admin", "ORDER_NEW", "STOCK_LOW", "PAYMENT_OK", "PAYMENT_FAILED", "SIGNUP_NEW"]
