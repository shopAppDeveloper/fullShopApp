from django.contrib.auth import get_user_model
from django.db import IntegrityError, transaction
from django.test import TestCase

from .accounts import create_mobile_user, find_user_by_login, find_user_by_mobile, real_email
from .serializers import serialize_user


class AccountTests(TestCase):
    def test_mobile_user(self):
        u = create_mobile_user("09123456789", "S3cret-pass!x", first_name="علی")
        self.assertEqual(find_user_by_mobile("۰۹۱۲۳۴۵۶۷۸۹"), u)
        self.assertEqual(find_user_by_login("+98 912 345 6789"), u)
        self.assertEqual(real_email(u), "")
        data = serialize_user(u)
        self.assertEqual((data["email"], data["mobile"], data["mobile_verified"]), ("", "09123456789", True))

    def test_mobile_is_unique(self):
        create_mobile_user("09123456789", "S3cret-pass!x")
        with self.assertRaises(IntegrityError), transaction.atomic():
            create_mobile_user("09123456789", "S3cret-pass!x")

    def test_email_user_still_found_and_has_no_mobile(self):
        u = get_user_model().objects.create_user("a@b.com", "a@b.com", "pw")
        self.assertEqual(find_user_by_login("A@B.com"), u)
        self.assertIsNone(serialize_user(u)["mobile"])
        self.assertIsNone(find_user_by_login("09999999999"))
