"""SMS infrastructure. Use `from api.sms import send_sms`."""

from .phone import normalize_mobile
from .service import send_sms

__all__ = ["normalize_mobile", "send_sms"]
