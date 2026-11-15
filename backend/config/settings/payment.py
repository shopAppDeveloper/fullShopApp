"""Zarinpal payment gateway. Credentials come from .env; amounts are whole Toman (currency IRT)."""

import os

from .env import env_bool

ZARINPAL_MERCHANT_ID = os.getenv("ZARINPAL_MERCHANT_ID", "")
ZARINPAL_SANDBOX = env_bool("ZARINPAL_SANDBOX", True)
ZARINPAL_CURRENCY = "IRT"
ZARINPAL_TIMEOUT = float(os.getenv("ZARINPAL_TIMEOUT", "10"))

_host = "sandbox.zarinpal.com" if ZARINPAL_SANDBOX else "payment.zarinpal.com"
ZARINPAL_API_BASE = os.getenv("ZARINPAL_API_BASE", f"https://{_host}")
ZARINPAL_PAY_BASE = os.getenv("ZARINPAL_PAY_BASE", f"https://{_host}/pg/StartPay")

# Public origin of the shop (nginx / Next.js). Zarinpal redirects the customer's browser to
# {SITE_URL}/api/payments/callback/, which then sends them on to the storefront result page.
SITE_URL = os.getenv("SITE_URL", "http://localhost:3000").rstrip("/")
