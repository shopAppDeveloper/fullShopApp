"""Minimal Zarinpal v4 client (request / verify). Pure HTTP; no Django models."""

import json
import urllib.request
from dataclasses import dataclass

from django.conf import settings


class ZarinpalError(Exception):
    """Gateway unreachable, misconfigured, or it rejected the call."""


@dataclass(frozen=True)
class VerifyResult:
    ok: bool
    ref_id: str = ""
    card_pan: str = ""
    code: int | None = None


def _post(path: str, payload: dict) -> dict:
    if not settings.ZARINPAL_MERCHANT_ID:
        raise ZarinpalError("ZARINPAL_MERCHANT_ID is not configured")
    payload = {"merchant_id": settings.ZARINPAL_MERCHANT_ID, **payload}
    req = urllib.request.Request(
        f"{settings.ZARINPAL_API_BASE}/pg/v4/payment/{path}.json",
        json.dumps(payload).encode(),
        {"Content-Type": "application/json", "Accept": "application/json"},
    )
    try:
        with urllib.request.urlopen(req, timeout=settings.ZARINPAL_TIMEOUT) as resp:  # noqa: S310
            return json.loads(resp.read().decode())
    except Exception as exc:  # network, TLS, bad JSON, HTTP error body
        raise ZarinpalError(f"gateway call failed: {type(exc).__name__}") from exc


def _data(body: dict) -> dict:
    data = body.get("data")
    return data if isinstance(data, dict) else {}


def request_payment(*, amount: int, callback_url: str, description: str, mobile: str = "", email: str = "", order_number: str = "") -> str:
    """Ask the gateway for a payment session; returns the `authority` token."""
    metadata = {k: v for k, v in {"mobile": mobile, "email": email, "order_id": order_number}.items() if v}
    body = _post("request", {
        "amount": amount,
        "currency": settings.ZARINPAL_CURRENCY,
        "callback_url": callback_url,
        "description": description,
        "metadata": metadata,
    })
    data = _data(body)
    if data.get("code") != 100 or not data.get("authority"):
        raise ZarinpalError(f"request rejected (code {data.get('code') or body.get('errors')})")
    return data["authority"]


def verify_payment(*, amount: int, authority: str) -> VerifyResult:
    """Confirm a payment. Code 100 = verified now, 101 = already verified earlier."""
    body = _post("verify", {"amount": amount, "authority": authority})
    data = _data(body)
    code = data.get("code")
    if code in (100, 101):
        return VerifyResult(True, str(data.get("ref_id", "")), str(data.get("card_pan", "")), code)
    return VerifyResult(False, code=code)


def start_url(authority: str) -> str:
    return f"{settings.ZARINPAL_PAY_BASE}/{authority}"
