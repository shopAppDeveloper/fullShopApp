import re
from unittest import mock

from django.test import override_settings
from rest_framework.test import APITestCase, APIClient

from .models import OtpCode
from .otp import OK, SIGNUP, TOO_SOON, request_otp, verify_otp

PW = "A-strong-test-password-123!"


def sent_code(m):
    return re.search(r"\d{6}", m.call_args.args[1]).group()


class OtpTests(APITestCase):
    def test_roundtrip_single_use(self):
        with mock.patch("api.otp.send_sms") as m:
            self.assertEqual(request_otp("09123456789", SIGNUP), OK)
            code = sent_code(m)
        self.assertEqual(m.call_args.kwargs["log_text"], False)
        self.assertFalse(verify_otp("09123456789", SIGNUP, "000000" if code != "000000" else "111111"))
        self.assertTrue(verify_otp("09123456789", SIGNUP, code))
        self.assertFalse(verify_otp("09123456789", SIGNUP, code))

    def test_cooldown_and_hash_storage(self):
        with mock.patch("api.otp.send_sms") as m:
            request_otp("09123456789", SIGNUP)
            self.assertEqual(request_otp("09123456789", SIGNUP), TOO_SOON)
        self.assertNotIn(sent_code(m), OtpCode.objects.get().code_hash)

    @override_settings(OTP_MAX_ATTEMPTS=3)
    def test_attempt_lockout(self):
        with mock.patch("api.otp.send_sms") as m:
            request_otp("09123456789", SIGNUP)
            code = sent_code(m)
        wrong = "000000" if code != "000000" else "111111"
        for _ in range(3):
            verify_otp("09123456789", SIGNUP, wrong)
        self.assertFalse(verify_otp("09123456789", SIGNUP, code))


class SignupApiTests(APITestCase):
    def setUp(self):
        self.client = APIClient(enforce_csrf_checks=True)
        self.csrf = self.client.get("/api/auth/csrf/").json()["csrfToken"]

    def post(self, url, data):
        return self.client.post(url, data, format="json", HTTP_X_CSRFTOKEN=self.csrf)

    def test_full_signup(self):
        with mock.patch("api.otp.send_sms") as m:
            r = self.post("/api/auth/signup/otp/", {"mobile": "۰۹۱۲۳۴۵۶۷۸۹"})
            code = sent_code(m)
        self.assertEqual(r.status_code, 200)
        bad = self.post("/api/auth/signup/", {"mobile": "09123456789", "code": "x", "password": PW})
        self.assertEqual(bad.status_code, 400)
        r = self.post("/api/auth/signup/", {"mobile": "09123456789", "code": code, "password": PW, "first_name": "علی"})
        self.assertEqual(r.status_code, 201)
        me = self.client.get("/api/auth/me/").json()["user"]
        self.assertEqual((me["mobile"], me["email"], me["first_name"]), ("09123456789", "", "علی"))

    def test_registered_number_gets_no_code(self):
        from .accounts import create_mobile_user
        create_mobile_user("09123456789", PW)
        with mock.patch("api.otp.send_sms") as m:
            r = self.post("/api/auth/signup/otp/", {"mobile": "09123456789"})
        self.assertEqual(r.status_code, 200)
        m.assert_not_called()

    def test_invalid_mobile_and_weak_password(self):
        self.assertEqual(self.post("/api/auth/signup/otp/", {"mobile": "123"}).status_code, 400)
        self.assertEqual(self.post("/api/auth/signup/", {"mobile": "09123456789", "code": "1", "password": "123"}).status_code, 400)
