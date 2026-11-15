"""Forgot-password flow: SMS code, then new password."""

from django.contrib.auth.password_validation import validate_password
from django.core.exceptions import ValidationError
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_protect
from rest_framework import status
from rest_framework.response import Response

from .. import otp
from ..accounts import find_user_by_mobile
from ..sms import normalize_mobile
from .signup import AuthBase, otp_response


@method_decorator(csrf_protect, name="dispatch")
class PasswordResetOtpView(AuthBase):
    """Step 1: send a code. Same answer whether or not the number has an account."""

    def post(self, request):
        mobile = normalize_mobile(request.data.get("mobile"))
        if not mobile:
            return Response({"detail": "Enter a valid mobile number."}, status=status.HTTP_400_BAD_REQUEST)
        if not find_user_by_mobile(mobile):
            return otp_response(otp.OK)
        return otp_response(otp.request_otp(mobile, otp.RESET))


@method_decorator(csrf_protect, name="dispatch")
class PasswordResetView(AuthBase):
    """Step 2: verify the code and set the new password (existing sessions are invalidated)."""

    def post(self, request):
        mobile = normalize_mobile(request.data.get("mobile"))
        password = request.data.get("password", "")
        if not mobile or not password:
            return Response({"detail": "Mobile number and password are required."}, status=status.HTTP_400_BAD_REQUEST)
        user = find_user_by_mobile(mobile)
        try:
            if user:
                validate_password(password, user=user)
        except ValidationError as exc:
            return Response({"detail": exc.messages}, status=status.HTTP_400_BAD_REQUEST)
        if not user or not otp.verify_otp(mobile, otp.RESET, request.data.get("code", "")):
            return Response({"detail": "Invalid or expired code."}, status=status.HTTP_400_BAD_REQUEST)
        user.set_password(password)
        user.save(update_fields=["password"])
        return Response({"detail": "Password changed."})
