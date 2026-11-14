from django.contrib import admin

from .models import NewsletterSubscriber, SmsLog


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
