"""Internal API: send a custom SMS or a special discount code to a customer."""

from django.conf import settings
from django.utils.crypto import constant_time_compare
from rest_framework import status
from rest_framework.permissions import BasePermission
from rest_framework.response import Response
from rest_framework.throttling import ScopedRateThrottle
from rest_framework.views import APIView

from ..accounts import find_user_by_mobile
from ..sms import normalize_mobile, send_sms

DISCOUNT_TEXT = "کد تخفیف ویژه‌ی شما: {code}"


class IsStaffOrApiKey(BasePermission):
    """Logged-in staff (session) or a caller presenting the INTERNAL_API_KEY in `X-API-Key`."""

    def has_permission(self, request, view):
        key = getattr(settings, "INTERNAL_API_KEY", "")
        sent = request.headers.get("X-API-Key", "")
        if key and sent and constant_time_compare(sent, key):
            return True
        user = request.user
        return bool(user and user.is_authenticated and user.is_staff)


class SendCustomerSmsView(APIView):
    """
    POST {"mobile": "09...", "text": "..."}           -> custom message
    POST {"mobile": "09...", "discount_code": "ABC"}  -> discount-code message (optional "text" with {code})
    """

    permission_classes = [IsStaffOrApiKey]
    throttle_classes = [ScopedRateThrottle]
    throttle_scope = "admin_sms"

    def post(self, request):
        d = request.data
        mobile = normalize_mobile(d.get("mobile"))
        if not mobile:
            return Response({"detail": "Enter a valid mobile number."}, status=status.HTTP_400_BAD_REQUEST)
        code = str(d.get("discount_code", "")).strip()
        text = str(d.get("text", "")).strip()
        if code:
            text = (text or DISCOUNT_TEXT).replace("{code}", code)
            purpose = "discount"
        else:
            purpose = "custom"
        if not text or len(text) > 500:
            return Response({"detail": "Message text is required (max 500 characters)."}, status=status.HTTP_400_BAD_REQUEST)
        result = send_sms(mobile, text, purpose=purpose)
        if not result.ok:
            return Response({"detail": "The SMS could not be sent."}, status=status.HTTP_502_BAD_GATEWAY)
        return Response({"detail": "SMS sent.", "registered_customer": bool(find_user_by_mobile(mobile))})
