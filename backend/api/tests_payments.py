from unittest import mock

from django.core.cache import cache
from django.test import override_settings
from oscar.core.loading import get_model
from rest_framework.test import APIClient, APITestCase

from .accounts import create_mobile_user
from .models import Payment
from .payments import zarinpal

Order = get_model("order", "Order")


def make_order(user, total=150000, number="100001"):
    return Order.objects.create(
        number=number, user=user, currency="IRT", total_incl_tax=total, total_excl_tax=total, status="Pending",
    )


def gateway(responses):
    """Replace the HTTP call; `responses` maps path -> response body."""
    return mock.patch.object(zarinpal, "_post", side_effect=lambda path, payload: responses[path])


@override_settings(ZARINPAL_MERCHANT_ID="m" * 36, **{"NOTIFY_ASYNC": False})
class PaymentFlowTests(APITestCase):
    def setUp(self):
        cache.clear()
        self.client = APIClient(enforce_csrf_checks=True)
        self.user = create_mobile_user("09123456789", "S3cret-pass!x")
        self.client.force_login(self.user)
        self.csrf = self.client.get("/api/auth/csrf/").json()["csrfToken"]
        self.order = make_order(self.user)

    def start(self, number="100001"):
        return self.client.post("/api/payments/start/", {"order_number": number}, format="json", HTTP_X_CSRFTOKEN=self.csrf)

    def test_start_sends_toman_amount_and_returns_redirect(self):
        with gateway({"request": {"data": {"code": 100, "authority": "A" * 36}}}) as g:
            r = self.start()
        self.assertEqual(r.status_code, 200)
        self.assertTrue(r.json()["redirect_url"].endswith("/StartPay/" + "A" * 36))
        sent = g.call_args.args[1]
        self.assertEqual((sent["amount"], sent["currency"]), (150000, "IRT"))
        self.assertEqual(Payment.objects.get().status, "pending")

    def test_cannot_pay_someone_elses_or_unknown_order(self):
        other = create_mobile_user("09120000000", "S3cret-pass!x")
        make_order(other, number="100002")
        self.assertEqual(self.start("100002").status_code, 404)
        self.assertEqual(self.start("nope").status_code, 404)

    def test_callback_success_marks_paid_once(self):
        Payment.objects.create(order=self.order, amount=150000, authority="AUTH1")
        ok = {"verify": {"data": {"code": 100, "ref_id": 777, "card_pan": "6037****1234"}}}
        with gateway(ok) as g:
            r = self.client.get("/api/payments/callback/?Authority=AUTH1&Status=OK")
            self.assertEqual(g.call_args.args[1], {"amount": 150000, "authority": "AUTH1"})
            self.assertEqual(r.status_code, 302)
            self.assertIn("status=ok&order=100001", r["Location"])
            self.client.get("/api/payments/callback/?Authority=AUTH1&Status=OK")  # replay
            self.assertEqual(g.call_count, 1)
        self.order.refresh_from_db()
        self.assertEqual(self.order.status, "Paid")
        p = Payment.objects.get()
        self.assertEqual((p.status, p.ref_id), ("paid", "777"))
        self.assertEqual(self.start().status_code, 400)  # already paid

    def test_callback_cancelled_and_failed(self):
        Payment.objects.create(order=self.order, amount=150000, authority="AUTH2")
        with gateway({}) as g:
            r = self.client.get("/api/payments/callback/?Authority=AUTH2&Status=NOK")
            g.assert_not_called()
        self.assertIn("status=failed", r["Location"])
        self.order.refresh_from_db()
        self.assertEqual(self.order.status, "Pending")
        Payment.objects.create(order=self.order, amount=150000, authority="AUTH3")
        with gateway({"verify": {"data": {"code": -51}}}):
            r = self.client.get("/api/payments/callback/?Authority=AUTH3&Status=OK")
        self.assertIn("status=failed", r["Location"])
        self.order.refresh_from_db()
        self.assertEqual(self.order.status, "Pending")

    def test_unknown_authority(self):
        r = self.client.get("/api/payments/callback/?Authority=zzz&Status=OK")
        self.assertIn("status=failed", r["Location"])

    def test_gateway_down_on_start_and_verify(self):
        with mock.patch.object(zarinpal, "_post", side_effect=zarinpal.ZarinpalError("x")):
            self.assertEqual(self.start().status_code, 502)
            Payment.objects.create(order=self.order, amount=150000, authority="AUTH4")
            r = self.client.get("/api/payments/callback/?Authority=AUTH4&Status=OK")
        self.assertIn("status=pending", r["Location"])
        self.assertEqual(Payment.objects.get(authority="AUTH4").status, "pending")


class NotConfiguredTests(APITestCase):
    @override_settings(ZARINPAL_MERCHANT_ID="")
    def test_missing_merchant_id(self):
        with self.assertRaises(zarinpal.ZarinpalError):
            zarinpal.request_payment(amount=1, callback_url="x", description="d")


@override_settings(ZARINPAL_MERCHANT_ID="m" * 36)
class MethodsTests(APITestCase):
    def test_lists_enabled_methods_and_shipping(self):
        r = self.client.get("/api/checkout/payment-methods/").json()
        self.assertEqual([m["code"] for m in r], ["zarinpal"])
        s = self.client.get("/api/shipping/methods/").json()
        self.assertEqual([(m["code"], m["price"]) for m in s], [("post", "0")])

    @override_settings(ZARINPAL_MERCHANT_ID="", DEBUG=False)
    def test_zarinpal_hidden_without_credentials_in_production(self):
        self.assertEqual(self.client.get("/api/checkout/payment-methods/").json(), [])

    @override_settings(POST_SHIPPING_PRICE=45000)
    def test_post_price_from_settings(self):
        self.assertEqual(self.client.get("/api/shipping/methods/").json()[0]["price"], "45000")

    def test_unknown_payment_method_rejected(self):
        cache.clear()
        user = create_mobile_user("09123456789", "S3cret-pass!x")
        make_order(user)
        c = APIClient(enforce_csrf_checks=True)
        c.force_login(user)
        csrf = c.get("/api/auth/csrf/").json()["csrfToken"]
        r = c.post("/api/payments/start/", {"order_number": "100001", "method": "paypal"}, format="json", HTTP_X_CSRFTOKEN=csrf)
        self.assertEqual(r.status_code, 400)
