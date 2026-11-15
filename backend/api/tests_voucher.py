from django.core.cache import cache
from oscar.core.loading import get_model
from rest_framework.test import APIClient, APITestCase

Product = get_model("catalogue", "Product")
ProductClass = get_model("catalogue", "ProductClass")
Partner = get_model("partner", "Partner")
StockRecord = get_model("partner", "StockRecord")
Voucher = get_model("voucher", "Voucher")
Range = get_model("offer", "Range")
Benefit = get_model("offer", "Benefit")
Condition = get_model("offer", "Condition")
ConditionalOffer = get_model("offer", "ConditionalOffer")


def make_voucher(code="VIP10", percent=10, min_value=0):
    now = __import__("django.utils.timezone", fromlist=["now"]).now()
    voucher = Voucher.objects.create(
        name=code, code=code, usage="Multi-use",
        start_datetime=now - __import__("datetime").timedelta(days=1),
        end_datetime=now + __import__("datetime").timedelta(days=30),
    )
    rng = Range.objects.create(name="all", includes_all_products=True)
    benefit = Benefit.objects.create(range=rng, type="Percentage", value=percent)
    condition = Condition.objects.create(range=rng, type="Value", value=min_value) if min_value else Condition.objects.create(range=rng, type="Count", value=1)
    offer = ConditionalOffer.objects.create(
        name=code, offer_type="Voucher", benefit=benefit, condition=condition,
        start_datetime=now - __import__("datetime").timedelta(days=1),
    )
    voucher.offers.add(offer)
    return voucher


class VoucherApiTests(APITestCase):
    def setUp(self):
        cache.clear()
        self.client = APIClient(enforce_csrf_checks=True)
        self.csrf = self.client.get("/api/auth/csrf/").json()["csrfToken"]
        pc = ProductClass.objects.create(name="c", track_stock=False)
        self.product = Product.objects.create(title="کالا", product_class=pc, is_public=True)
        StockRecord.objects.create(product=self.product, partner=Partner.objects.create(name="p"),
                                   partner_sku="s", price=100000, num_in_stock=10)

    def call(self, method, url, data=None):
        return getattr(self.client, method)(url, data, format="json", HTTP_X_CSRFTOKEN=self.csrf)

    def add_item(self):
        r = self.call("post", "/api/basket/items/", {"product_id": self.product.id, "quantity": 2})
        self.assertEqual(r.status_code, 201, r.content)

    def test_apply_and_remove(self):
        make_voucher("VIP10", 10)
        self.add_item()
        r = self.call("post", "/api/basket/voucher/", {"code": "vip10"})
        self.assertEqual(r.status_code, 200, r.content)
        b = r.json()
        self.assertEqual((b["subtotal"], b["discount"], b["total"], b["vouchers"]), ("200000", "20000", "180000", ["VIP10"]))
        self.assertEqual(self.call("post", "/api/basket/voucher/", {"code": "VIP10"}).status_code, 400)  # duplicate
        r = self.call("delete", "/api/basket/voucher/VIP10/")
        self.assertEqual((r.json()["discount"], r.json()["total"], r.json()["vouchers"]), ("0", "200000", []))

    def test_invalid_empty_and_unqualified(self):
        make_voucher("BIG", 10, min_value=1_000_000)
        self.assertEqual(self.call("post", "/api/basket/voucher/", {"code": "BIG"}).status_code, 400)  # empty basket
        self.add_item()
        self.assertEqual(self.call("post", "/api/basket/voucher/", {"code": "NOPE"}).status_code, 400)
        r = self.call("post", "/api/basket/voucher/", {"code": "BIG"})
        self.assertEqual(r.status_code, 400)
        self.assertEqual(self.client.get("/api/basket/").json()["vouchers"], [])  # not kept


class VoucherOrderTests(VoucherApiTests):
    def test_order_total_includes_discount_and_voucher_usage(self):
        from oscar.apps.address.models import Country

        from .accounts import create_mobile_user

        Country.objects.create(iso_3166_1_a2="IR", iso_3166_1_a3="IRN", iso_3166_1_numeric="364",
                               printable_name="Iran", name="Iran", is_shipping_country=True)
        voucher = make_voucher("VIP10", 10)
        self.client.force_login(create_mobile_user("09123456789", "S3cret-pass!x"))
        self.csrf = self.client.get("/api/auth/csrf/").json()["csrfToken"]
        self.add_item()
        self.assertEqual(self.call("post", "/api/basket/voucher/", {"code": "VIP10"}).status_code, 200)
        r = self.call("post", "/api/checkout/orders/", {"first_name": "a", "last_name": "b", "line1": "x", "postcode": "1234567891", "country": "IR"})
        self.assertEqual(r.status_code, 201, r.content)
        self.assertEqual(r.json()["order"]["total_incl_tax"], "180000")
        voucher.refresh_from_db()
        self.assertEqual(voucher.num_orders, 1)
