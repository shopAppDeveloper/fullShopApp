"""Persian message text for each admin event."""

from . import base


def _n(v):
    return f"{int(float(v)):,}" if v not in (None, "") else "-"


def render(event: str, data: dict) -> str:
    d = data or {}
    if event == base.ORDER_NEW:
        return f"🛒 سفارش جدید #{d.get('number', '?')}\nمبلغ: {_n(d.get('total'))} تومان\nمشتری: {d.get('customer', '-')}"
    if event == base.STOCK_LOW:
        return f"⚠️ موجودی کم\nمحصول: {d.get('title', '?')}\nباقی‌مانده: {d.get('stock', '?')} عدد"
    if event == base.PAYMENT_OK:
        return f"✅ پرداخت موفق\nسفارش #{d.get('number', '?')}\nمبلغ: {_n(d.get('amount'))} تومان\nکد پیگیری: {d.get('ref_id', '-')}"
    if event == base.PAYMENT_FAILED:
        return f"❌ پرداخت ناموفق\nسفارش #{d.get('number', '?')}\nعلت: {d.get('reason', '-')}"
    if event == base.SIGNUP_NEW:
        return f"👤 ثبت‌نام جدید\n{d.get('customer', '-')}"
    return f"{event}: {d}"
