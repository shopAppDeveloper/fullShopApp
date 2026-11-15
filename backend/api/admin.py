from django.contrib import admin

from .models import NewsletterSubscriber, Payment, Profile, SmsLog


@admin.register(NewsletterSubscriber)
class NewsletterSubscriberAdmin(admin.ModelAdmin):
    list_display = ("email", "is_active", "created_at")
    list_filter = ("is_active",)
    search_fields = ("email",)


@admin.register(SmsLog)
class SmsLogAdmin(admin.ModelAdmin):
    list_display = ("to", "purpose", "status", "provider", "created_at")
    list_filter = ("status", "purpose", "provider")
    search_fields = ("to",)
    readonly_fields = [f.name for f in SmsLog._meta.fields]

    def has_add_permission(self, request):
        return False


@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    list_display = ("user", "mobile", "mobile_verified", "created_at")
    search_fields = ("mobile", "user__email")


@admin.register(Payment)
class PaymentAdmin(admin.ModelAdmin):
    list_display = ("order", "amount", "status", "ref_id", "created_at")
    list_filter = ("status",)
    search_fields = ("order__number", "authority", "ref_id")
    readonly_fields = [f.name for f in Payment._meta.fields]

    def has_add_permission(self, request):
        return False
