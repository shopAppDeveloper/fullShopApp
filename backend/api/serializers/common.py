"""Shared serialization helpers."""

from decimal import ROUND_HALF_UP, Decimal

from django.conf import settings


def money(value):
    """Serialize a price as a whole-Toman string (e.g. "1250000"), without float loss."""

    if value is None:
        return None
    return str(Decimal(value).quantize(Decimal(1), rounding=ROUND_HALF_UP))


def currency_code(_value=None):
    """
    The store sells in Toman only. Legacy stock records or orders created with
    another label (e.g. "ریال") are still presented as Toman.
    """

    return settings.STORE_CURRENCY
