"""Django Oscar defaults, search and checkout rules."""

import os

from .env import *  # noqa: F401,F403
from .env import BASE_DIR, env_bool, env_list  # noqa: F401
from .security import DEBUG  # noqa: F401

# ---------------------------------------------------------
# Oscar defaults
#
# Oscar has many ecommerce-specific settings.
# Importing its defaults allows us to start with sane values.
# ---------------------------------------------------------

from oscar.defaults import *  # noqa: E402,F401,F403


# We allow anonymous customers to create baskets and later
# decide whether checkout requires login.
OSCAR_ALLOW_ANON_CHECKOUT = True


# Number of products stored in the recently viewed cookie.
OSCAR_RECENTLY_VIEWED_PRODUCTS = 20

# Order workflow used by the store. The dashboard can move an order
# through these states as fulfilment progresses.
OSCAR_INITIAL_ORDER_STATUS = "Pending"
OSCAR_INITIAL_LINE_STATUS = "Pending"
OSCAR_ORDER_STATUS_PIPELINE = {
    "Pending": ("Being processed", "Cancelled"),
    "Being processed": ("Processed", "Cancelled"),
    "Processed": ("Shipped", "Cancelled"),
    "Shipped": ("Delivered",),
    "Delivered": (),
    "Cancelled": (),
}

# Used when a new stock record is created in Oscar's dashboard.
# Existing stock records retain their own configured currency.
OSCAR_DEFAULT_CURRENCY = os.getenv("OSCAR_DEFAULT_CURRENCY", "ریال")


# ---------------------------------------------------------
# Search
#
# Whoosh runs locally on this server.
# There is no external search service.
# ---------------------------------------------------------

HAYSTACK_CONNECTIONS = {
    "default": {
        "ENGINE": "haystack.backends.whoosh_backend.WhooshEngine",
        "PATH": BASE_DIR / "whoosh_index",
    },
}

HAYSTACK_SIGNAL_PROCESSOR = "haystack.signals.RealtimeSignalProcessor"



# ---------------------------------------------------------
# Checkout/payment safety
#
# Pending orders are useful while developing locally, but a
# production store must not consider an order paid until the
# payment provider has confirmed the transaction.
# ---------------------------------------------------------

CHECKOUT_ALLOW_PENDING_ORDERS = env_bool(
    "CHECKOUT_ALLOW_PENDING_ORDERS",
    DEBUG,
)
