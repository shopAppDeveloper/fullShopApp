from unittest import mock

from django.db import transaction
from django.test import TestCase, TransactionTestCase, override_settings

from .notifications import ORDER_NEW, notify_admin
from .notifications import dispatcher
from .notifications.bale import BaleChannel
from .notifications.messages import render
from .notifications.telegram import TelegramChannel

SYNC = dict(NOTIFY_ASYNC=False, NOTIFY_CONSOLE=False)


@override_settings(TELEGRAM_BOT_TOKEN="T", TELEGRAM_ADMIN_CHAT_IDS=["1", "2"], BALE_BOT_TOKEN="B", BALE_ADMIN_CHAT_IDS=["9"], **SYNC)
class ChannelTests(TransactionTestCase):
    def test_sends_to_all_configured_channels(self):
        with mock.patch("urllib.request.urlopen") as up:
            notify_admin(ORDER_NEW, {"number": "100", "total": "1500000", "customer": "x"})
        urls = [c.args[0].full_url for c in up.call_args_list]
        self.assertEqual(len(urls), 3)
        self.assertIn("https://api.telegram.org/botT/sendMessage", urls)
        self.assertIn("https://tapi.bale.ai/botB/sendMessage", urls)

    def test_failure_never_raises(self):
        with mock.patch("urllib.request.urlopen", side_effect=OSError("down")):
            notify_admin(ORDER_NEW, {"number": "1"})  # must not raise

    def test_unknown_event_ignored(self):
        with mock.patch("urllib.request.urlopen") as up:
            notify_admin("nope", {})
        up.assert_not_called()


class ConfigTests(TestCase):
    @override_settings(TELEGRAM_BOT_TOKEN="", TELEGRAM_ADMIN_CHAT_IDS=[], BALE_BOT_TOKEN="B", BALE_ADMIN_CHAT_IDS=[])
    def test_needs_token_and_chat_ids(self):
        self.assertFalse(TelegramChannel().is_configured())
        self.assertFalse(BaleChannel().is_configured())

    def test_no_channel_by_default(self):
        self.assertEqual(dispatcher.active_channels(), [])

    def test_persian_message(self):
        self.assertIn("سفارش جدید #5", render(ORDER_NEW, {"number": 5, "total": "1500000"}))
        self.assertIn("1,500,000", render(ORDER_NEW, {"number": 5, "total": "1500000"}))

    @override_settings(BOT_WEBHOOK_SECRET="")
    def test_webhook_disabled_without_secret(self):
        self.assertEqual(self.client.post("/api/bot/webhook/x/", {}).status_code, 404)

    @override_settings(BOT_WEBHOOK_SECRET="s3")
    def test_webhook_secret(self):
        self.assertEqual(self.client.post("/api/bot/webhook/bad/", {}).status_code, 404)
        self.assertEqual(self.client.post("/api/bot/webhook/s3/", {}).status_code, 200)


class OnCommitTests(TestCase):
    @override_settings(TELEGRAM_BOT_TOKEN="T", TELEGRAM_ADMIN_CHAT_IDS=["1"], **SYNC)
    def test_deferred_until_commit(self):
        with mock.patch("urllib.request.urlopen") as up:
            with self.captureOnCommitCallbacks(execute=False) as cbs:
                notify_admin(ORDER_NEW, {"number": "1"})
            up.assert_not_called()
            cbs[0]()
            up.assert_called_once()
