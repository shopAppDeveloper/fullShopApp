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

    def test_customer_can_register_and_get_current_user(self):
        csrf = self._csrf()

        response = self.client.post(
            "/api/auth/register/",
            {
                "email": "customer@example.com",
                "password": "A-strong-test-password-123!",
                "first_name": "Test",
                "last_name": "Customer",
            },
            format="json",
            HTTP_X_CSRFTOKEN=csrf,
        )

        self.assertEqual(response.status_code, 201)
        self.assertEqual(response.json()["user"]["email"], "customer@example.com")

        response = self.client.get("/api/auth/me/")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()["user"]["email"], "customer@example.com")


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
