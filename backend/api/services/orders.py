"""
Order registration and payment status.

STUB: `register_order` - the order-creation logic still lives in views/orders.py (CreateOrderView).
Move it here when convenient and keep views thin.
"""


def register_order(*, user, basket, shipping_address, shipping_method, request=None):
    """Create an order from a basket and return it. Must run inside a transaction."""
    raise NotImplementedError("Order registration is not implemented yet.")


def mark_order_paid(order, *, ref_id: str = "") -> None:
    """Move a Pending order to Paid after the gateway confirmed the payment."""
    if order.status == "Pending":
        order.set_status("Paid")
    if ref_id:
        order.notes.create(note_type="System", message=f"پرداخت موفق؛ کد پیگیری {ref_id}")


def mark_order_payment_failed(order, *, reason: str = "") -> None:
    """Keep the order Pending (the customer may retry) and leave a note for the shop."""
    order.notes.create(note_type="System", message=f"پرداخت ناموفق: {reason}")
