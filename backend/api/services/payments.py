"""
Payment gateway (Zarinpal) operations.

STUB: implemented in the Zarinpal task. Amounts are whole Toman (Zarinpal currency "IRT").
"""


def start_payment(order, *, callback_url: str) -> str:
    """Request a payment from the gateway and return the URL to redirect the customer to."""
    raise NotImplementedError("Payment is not implemented yet.")


def verify_payment(order, *, authority: str) -> bool:
    """Verify the gateway callback. Return True only when the payment is confirmed."""
    raise NotImplementedError("Payment is not implemented yet.")
