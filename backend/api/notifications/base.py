"""Admin notification contract and event names."""

# Events that can be sent to the shop admins.
ORDER_NEW = "order_new"
STOCK_LOW = "stock_low"
PAYMENT_OK = "payment_ok"
PAYMENT_FAILED = "payment_failed"
SIGNUP_NEW = "signup_new"

EVENTS = (ORDER_NEW, STOCK_LOW, PAYMENT_OK, PAYMENT_FAILED, SIGNUP_NEW)


class AdminChannel:
    """A destination for admin alerts (Telegram, Bale, console, ...)."""

    name = "base"

    def is_configured(self) -> bool:
        """True when the channel has everything it needs (token, chat ids)."""
        raise NotImplementedError

    def send(self, text: str) -> None:
        """Deliver `text` to every admin of this channel. May raise; the dispatcher handles it."""
        raise NotImplementedError
