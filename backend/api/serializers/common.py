"""Shared serialization helpers."""

from decimal import Decimal


def money(value):
    """Serialize Decimal-like values without floating point loss."""

    if value is None:
        return None
    return str(Decimal(value))
