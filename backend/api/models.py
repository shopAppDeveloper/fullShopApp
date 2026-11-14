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
