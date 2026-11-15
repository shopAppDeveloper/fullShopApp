from unittest import mock

from django.contrib.auth import get_user_model
from django.core.cache import cache
from django.test import override_settings
from rest_framework.test import APITestCase

from .accounts import create_mobile_user
from .models import SmsLog

URL = "/api/admin/sms/send/"


class MessagingTests(APITestCase):
    def setUp(self):
        cache.clear()

    def test_anonymous_and_customer_rejected(self):
        self.assertEqual(self.client.post(URL, {"mobile": "09123456789", "text": "x"}, format="json").status_code, 403)
        self.client.force_login(create_mobile_user("09120000000", "S3cret-pass!x"))
        self.assertEqual(self.client.post(URL, {"mobile": "09123456789", "text": "x"}, format="json").status_code, 403)

    @override_settings(INTERNAL_API_KEY="k3y")
    def test_api_key(self):
        r = self.client.post(URL, {"mobile": "09123456789", "text": "سلام"}, format="json", HTTP_X_API_KEY="k3y")
        self.assertEqual(r.status_code, 200)
        self.assertEqual(SmsLog.objects.get().purpose, "custom")
        bad = self.client.post(URL, {"mobile": "09123456789", "text": "x"}, format="json", HTTP_X_API_KEY="nope")
        self.assertEqual(bad.status_code, 403)

    @override_settings(INTERNAL_API_KEY="")
    def test_empty_key_never_matches(self):
        r = self.client.post(URL, {"mobile": "09123456789", "text": "x"}, format="json", HTTP_X_API_KEY="")
        self.assertEqual(r.status_code, 403)

    def test_staff_discount_code(self):
        staff = get_user_model().objects.create_user("s", "s@x.com", "pw", is_staff=True)
        self.client.force_login(staff)
        r = self.client.post(URL, {"mobile": "۰۹۱۲۳۴۵۶۷۸۹", "discount_code": "VIP10"}, format="json")
        self.assertEqual(r.status_code, 200)
        log = SmsLog.objects.get()
        self.assertEqual((log.purpose, log.to), ("discount", "09123456789"))
        self.assertIn("VIP10", log.text)

    def test_validation(self):
        staff = get_user_model().objects.create_user("s", "s@x.com", "pw", is_staff=True)
        self.client.force_login(staff)
        self.assertEqual(self.client.post(URL, {"mobile": "1", "text": "x"}, format="json").status_code, 400)
        self.assertEqual(self.client.post(URL, {"mobile": "09123456789"}, format="json").status_code, 400)


class EventSmsTests(APITestCase):
    def test_signup_sms_after_commit(self):
        from .sms.events import signup_sms

        user = create_mobile_user("09123456789", "S3cret-pass!x")
        with self.captureOnCommitCallbacks(execute=True):
            signup_sms(user)
        log = SmsLog.objects.get()
        self.assertEqual((log.purpose, log.to), ("signup", "09123456789"))

    @override_settings(SMS_EVENTS_ENABLED=False)
    def test_disabled(self):
        from .sms.events import signup_sms

        with self.captureOnCommitCallbacks(execute=True):
            signup_sms(create_mobile_user("09123456789", "S3cret-pass!x"))
        self.assertEqual(SmsLog.objects.count(), 0)
