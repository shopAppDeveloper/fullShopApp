from django.test import TestCase, override_settings

from .models import SmsLog
from .sms import normalize_mobile, send_sms
from .sms.base import SmsProvider, SmsResult


class Boom(SmsProvider):
    def send(self, to, text):
        raise RuntimeError("gateway down")


class PhoneTests(TestCase):
    def test_normalize(self):
        for raw in ["09123456789", "9123456789", "+989123456789", "00989123456789", "۰۹۱۲۳۴۵۶۷۸۹", "0912 345 6789"]:
            self.assertEqual(normalize_mobile(raw), "09123456789", raw)
        for bad in ["", None, "0212345678", "0912345", "abc", "09123456789012"]:
            self.assertIsNone(normalize_mobile(bad), bad)


class SendSmsTests(TestCase):
    def test_console_provider_logs(self):
        r = send_sms("09123456789", "hello", purpose="test")
        self.assertTrue(r.ok)
        log = SmsLog.objects.get()
        self.assertEqual((log.to, log.status, log.text), ("09123456789", "sent", "hello"))

    def test_otp_text_is_hidden(self):
        send_sms("09123456789", "code 123456", purpose="otp", log_text=False)
        self.assertEqual(SmsLog.objects.get().text, "[hidden]")

    def test_invalid_number_fails_without_raising(self):
        r = send_sms("123", "x")
        self.assertFalse(r.ok)
        self.assertEqual(SmsLog.objects.get().status, "failed")

    @override_settings(SMS_PROVIDER="api.tests_sms.Boom")
    def test_provider_exception_is_swallowed(self):
        r = send_sms("09123456789", "x")
        self.assertFalse(r.ok)
        self.assertIn("gateway down", SmsLog.objects.get().error)
