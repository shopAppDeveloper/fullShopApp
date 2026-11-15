import re
from unittest import mock

from django.contrib.auth import get_user_model
from rest_framework.test import APIClient, APITestCase

from .accounts import create_mobile_user

OLD, NEW = "Old-strong-pass-123!", "New-strong-pass-456!"


def code(m):
    return re.search(r"\d{6}", m.call_args.args[1]).group()


class LoginAndResetTests(APITestCase):
    def setUp(self):
        from django.core.cache import cache

        cache.clear()  # the "auth" throttle counter is shared across tests
        self.client = APIClient(enforce_csrf_checks=True)
        self.csrf = self.client.get("/api/auth/csrf/").json()["csrfToken"]
        self.user = create_mobile_user("09123456789", OLD)
        self.email_user = get_user_model().objects.create_user("a@b.com", "a@b.com", OLD)

    def post(self, url, data):
        return self.client.post(url, data, format="json", HTTP_X_CSRFTOKEN=self.csrf)

    def test_login_by_mobile_in_any_format(self):
        for ident in ["09123456789", "+989123456789", "۰۹۱۲۳۴۵۶۷۸۹"]:
            self.assertEqual(self.post("/api/auth/login/", {"identifier": ident, "password": OLD}).status_code, 200, ident)

    def test_login_by_email_legacy_field_and_wrong_password(self):
        self.assertEqual(self.post("/api/auth/login/", {"email": "A@b.com", "password": OLD}).status_code, 200)
        self.assertEqual(self.post("/api/auth/login/", {"identifier": "a@b.com", "password": "x"}).status_code, 400)
        self.assertEqual(self.post("/api/auth/login/", {"identifier": "09000000000", "password": OLD}).status_code, 400)

    def test_password_reset_flow(self):
        with mock.patch("api.otp.send_sms") as m:
            self.assertEqual(self.post("/api/auth/password/otp/", {"mobile": "09123456789"}).status_code, 200)
            c = code(m)
        self.assertEqual(self.post("/api/auth/password/reset/", {"mobile": "09123456789", "code": "x", "password": NEW}).status_code, 400)
        self.assertEqual(self.post("/api/auth/password/reset/", {"mobile": "09123456789", "code": c, "password": "123"}).status_code, 400)
        self.assertEqual(self.post("/api/auth/password/reset/", {"mobile": "09123456789", "code": c, "password": NEW}).status_code, 200)
        self.assertEqual(self.post("/api/auth/login/", {"identifier": "09123456789", "password": OLD}).status_code, 400)
        self.assertEqual(self.post("/api/auth/login/", {"identifier": "09123456789", "password": NEW}).status_code, 200)
        # the code is single-use (login rotated the CSRF token)
        self.csrf = self.client.get("/api/auth/csrf/").json()["csrfToken"]
        self.assertEqual(self.post("/api/auth/password/reset/", {"mobile": "09123456789", "code": c, "password": OLD}).status_code, 400)

    def test_unknown_number_gets_same_answer_and_no_sms(self):
        with mock.patch("api.otp.send_sms") as m:
            r = self.post("/api/auth/password/otp/", {"mobile": "09999999999"})
        self.assertEqual(r.status_code, 200)
        m.assert_not_called()

    def test_reset_code_is_not_valid_for_signup(self):
        with mock.patch("api.otp.send_sms") as m:
            self.post("/api/auth/password/otp/", {"mobile": "09123456789"})
            c = code(m)
        r = self.post("/api/auth/signup/", {"mobile": "09123456789", "code": c, "password": NEW})
        self.assertEqual(r.status_code, 400)
