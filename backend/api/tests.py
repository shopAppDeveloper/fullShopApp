from django.test import TestCase
from rest_framework.test import APIClient


class PublicApiTests(TestCase):
    def setUp(self):
        self.client = APIClient()

    def test_health_endpoint(self):
        response = self.client.get("/api/health/")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()["status"], "ok")

    def test_product_list_is_public(self):
        response = self.client.get("/api/products/")
        self.assertEqual(response.status_code, 200)
        self.assertIn("results", response.json())

    def test_category_list_is_public(self):
        response = self.client.get("/api/categories/")
        self.assertEqual(response.status_code, 200)
        self.assertIsInstance(response.json(), list)

    def test_unknown_product_returns_404(self):
        response = self.client.get("/api/products/does-not-exist/")
        self.assertEqual(response.status_code, 404)


class AuthenticationApiTests(TestCase):
    def setUp(self):
        self.client = APIClient(enforce_csrf_checks=True)

    def _csrf(self):
        response = self.client.get("/api/auth/csrf/")
        self.assertEqual(response.status_code, 200)
        return response.json()["csrfToken"]



class SecurityTests(TestCase):
    """Authorization and abuse-protection checks."""

    def setUp(self):
        from django.core.cache import cache

        cache.clear()
        self.client = APIClient()

    def test_private_endpoints_require_login(self):
        for url in ("/api/orders/", "/api/addresses/", "/api/auth/me/"):
            self.assertIn(self.client.get(url).status_code, (401, 403), url)

    def test_order_lookup_is_scoped_to_the_logged_in_user(self):
        from django.contrib.auth import get_user_model

        User = get_user_model()
        other = User.objects.create_user(username="b", email="b@example.com", password="x-Strong-pass-123")
        self.client.force_authenticate(user=other)
        self.assertEqual(self.client.get("/api/orders/100001/").status_code, 404)

    def test_login_is_rate_limited(self):
        statuses = [
            self.client.post(
                "/api/auth/login/", {"email": "x@example.com", "password": "wrong"}, format="json"
            ).status_code
            for _ in range(12)
        ]
        self.assertEqual(statuses[0], 400)
        self.assertIn(429, statuses)


class SanitizeHtmlTests(TestCase):
    def test_dangerous_markup_is_removed_and_formatting_kept(self):
        from .sanitize import sanitize_html

        dirty = (
            '<p onclick="x()">سلام <strong>دنیا</strong></p>'
            '<script>alert(1)</script><img src=x onerror=alert(1)>'
            '<a href="javascript:alert(1)">bad</a><a href="https://example.com">ok</a>'
            '<iframe src="https://evil"></iframe>'
        )
        clean = sanitize_html(dirty)
        self.assertIn("<strong>دنیا</strong>", clean)
        self.assertIn('href="https://example.com"', clean)
        for bad in ("<script", "onclick", "onerror", "javascript:", "<iframe", "<img"):
            self.assertNotIn(bad, clean)


class TomanTests(TestCase):
    def test_money_is_whole_toman(self):
        from api.serializers import currency_code, money

        self.assertEqual(money("1250000.00"), "1250000")
        self.assertEqual(money("99.5"), "100")
        self.assertIsNone(money(None))
        self.assertEqual(currency_code("ریال"), "IRT")
        self.assertEqual(currency_code(None), "IRT")


class CatalogFilterTests(TestCase):
    def test_price_and_bestselling_params_are_accepted(self):
        for qs in ["min_price=1000&max_price=5000", "sort=bestselling", "min_price=abc"]:
            self.assertEqual(self.client.get(f"/api/products/?{qs}").status_code, 200, qs)
