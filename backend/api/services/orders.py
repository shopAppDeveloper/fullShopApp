"""
Order registration.

STUB: the order-creation logic still lives in views/orders.py (CreateOrderView).
Move it here when the checkout/payment flow is built, and keep views thin.
"""


def register_order(*, user, basket, shipping_address, shipping_method, request=None):
    """Create an order from a basket and return it. Must run inside a transaction."""
    raise NotImplementedError("Order registration is not implemented yet.")


def mark_order_paid(order, *, ref_id: str = "") -> None:
    """Move an order to its paid status after the payment provider confirmed it."""
    raise NotImplementedError("Order payment status handling is not implemented yet.")


def mark_order_payment_failed(order, *, reason: str = "") -> None:
    """Record a failed or cancelled payment on the order."""
    raise NotImplementedError("Order payment status handling is not implemented yet.")
