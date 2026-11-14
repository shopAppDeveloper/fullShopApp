from django.core.management.base import BaseCommand

from api.notifications.dispatcher import active_channels
from api.notifications import base, notify_admin

SAMPLES = {
    base.ORDER_NEW: {"number": "100001", "total": "1500000", "customer": "مشتری آزمایشی"},
    base.STOCK_LOW: {"title": "محصول آزمایشی", "stock": 2},
    base.PAYMENT_OK: {"number": "100001", "amount": "1500000", "ref_id": "123456"},
    base.PAYMENT_FAILED: {"number": "100001", "reason": "انصراف کاربر"},
    base.SIGNUP_NEW: {"customer": "کاربر آزمایشی"},
}


class Command(BaseCommand):
    help = "Send a sample admin notification to every configured channel (Telegram/Bale/console)."

    def add_arguments(self, parser):
        parser.add_argument("event", nargs="?", default=base.ORDER_NEW, choices=base.EVENTS)

    def handle(self, *args, **opts):
        chans = [c.name for c in active_channels()]
        if not chans:
            self.stderr.write("No channel configured (set TELEGRAM_*/BALE_* or NOTIFY_CONSOLE=True).")
            return
        notify_admin(opts["event"], SAMPLES[opts["event"]])
        self.stdout.write(f"Queued '{opts['event']}' to: {', '.join(chans)}")
