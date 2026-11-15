from django.conf import settings
from django.db import models


class NewsletterSubscriber(models.Model):
    """E-mail addresses collected by the storefront newsletter form."""

    email = models.EmailField(unique=True)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-created_at"]

    def __str__(self):
        return self.email


class SmsLog(models.Model):
    """Audit trail of every SMS handed to the gateway (OTP codes are never stored)."""

    SENT, FAILED = "sent", "failed"
    STATUS_CHOICES = [(SENT, "sent"), (FAILED, "failed")]

    to = models.CharField(max_length=20, db_index=True)
    text = models.TextField()
    purpose = models.CharField(max_length=30, blank=True, db_index=True)
    provider = models.CharField(max_length=30)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES)
    provider_message_id = models.CharField(max_length=100, blank=True)
    error = models.CharField(max_length=200, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-created_at"]

    def __str__(self):
        return f"{self.to} [{self.status}] {self.purpose}"


class Profile(models.Model):
    """Extra customer data. The mobile number (09XXXXXXXXX) is the primary identity for sign-up and password reset."""

    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="profile")
    mobile = models.CharField(max_length=11, unique=True, null=True, blank=True)
    mobile_verified = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user_id}: {self.mobile or '-'}"


class OtpCode(models.Model):
    """One-time SMS code. Only a salted hash of the code is stored."""

    mobile = models.CharField(max_length=11, db_index=True)
    purpose = models.CharField(max_length=20)  # "signup" | "reset"
    code_hash = models.CharField(max_length=64)
    expires_at = models.DateTimeField()
    attempts = models.PositiveSmallIntegerField(default=0)
    used = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-created_at"]


class Payment(models.Model):
    """One attempt to pay an order through the gateway. `amount` is whole Toman, taken from the order, never from the browser."""

    PENDING, PAID, FAILED = "pending", "paid", "failed"
    STATUS_CHOICES = [(PENDING, "pending"), (PAID, "paid"), (FAILED, "failed")]

    order = models.ForeignKey("order.Order", on_delete=models.PROTECT, related_name="payments")
    amount = models.PositiveBigIntegerField()
    authority = models.CharField(max_length=64, unique=True)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default=PENDING)
    ref_id = models.CharField(max_length=40, blank=True)
    card_pan = models.CharField(max_length=30, blank=True)
    error = models.CharField(max_length=200, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    verified_at = models.DateTimeField(null=True, blank=True)

    class Meta:
        ordering = ["-created_at"]

    def __str__(self):
        return f"{self.order_id} {self.status} {self.authority}"
