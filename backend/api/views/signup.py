"""Sign-up with a mobile number verified by an SMS code."""

from django.contrib.auth import get_user_model, login
from django.contrib.auth.password_validation import validate_password
from django.core.exceptions import ValidationError
from django.core.validators import validate_email
from django.db import IntegrityError, transaction
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_protect
from rest_framework import status
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.throttling import ScopedRateThrottle
from rest_framework.views import APIView

from .. import otp
from ..accounts import create_mobile_user, find_user_by_mobile
from ..notifications.events import signup as signup_event
from ..serializers import serialize_user
from ..sms import normalize_mobile
from ..sms.events import signup_sms

OTP_ERRORS = {
    otp.TOO_SOON: ("Please wait before requesting another code.", status.HTTP_429_TOO_MANY_REQUESTS),
    otp.LIMIT: ("Too many codes requested. Try again later.", status.HTTP_429_TOO_MANY_REQUESTS),
}


class AuthBase(APIView):
    permission_classes = [AllowAny]
    authentication_classes = []
    throttle_classes = [ScopedRateThrottle]
    throttle_scope = "auth"


def otp_response(result):
    if result in OTP_ERRORS:
        detail, code = OTP_ERRORS[result]
        return Response({"detail": detail}, status=code)
    return Response({"detail": "If the number is valid, a code has been sent."})


@method_decorator(csrf_protect, name="dispatch")
class SignupOtpView(AuthBase):
    """Step 1: send a code. The answer is identical for registered numbers (no enumeration)."""

    def post(self, request):
        mobile = normalize_mobile(request.data.get("mobile"))
        if not mobile:
            return Response({"detail": "Enter a valid mobile number."}, status=status.HTTP_400_BAD_REQUEST)
        if find_user_by_mobile(mobile):
            return otp_response(otp.OK)
        return otp_response(otp.request_otp(mobile, otp.SIGNUP))


@method_decorator(csrf_protect, name="dispatch")
class SignupView(AuthBase):
    """Step 2: verify the code and create the account."""

    def post(self, request):
        d = request.data
        mobile = normalize_mobile(d.get("mobile"))
        password = d.get("password", "")
        email = str(d.get("email", "")).strip().lower()
        if not mobile or not password:
            return Response({"detail": "Mobile number and password are required."}, status=status.HTTP_400_BAD_REQUEST)
        if email:
            try:
                validate_email(email)
            except ValidationError:
                return Response({"detail": "Enter a valid email address."}, status=status.HTTP_400_BAD_REQUEST)
            if get_user_model().objects.filter(email__iexact=email).exists():
                return Response({"detail": "Registration failed."}, status=status.HTTP_400_BAD_REQUEST)
        try:
            validate_password(password)
        except ValidationError as exc:
            return Response({"detail": exc.messages}, status=status.HTTP_400_BAD_REQUEST)
        if find_user_by_mobile(mobile) or not otp.verify_otp(mobile, otp.SIGNUP, d.get("code", "")):
            return Response({"detail": "Invalid or expired code."}, status=status.HTTP_400_BAD_REQUEST)
        try:
            with transaction.atomic():
                user = create_mobile_user(
                    mobile, password,
                    first_name=str(d.get("first_name", "")).strip(),
                    last_name=str(d.get("last_name", "")).strip(),
                    email=email,
                )
        except IntegrityError:
            return Response({"detail": "Registration failed."}, status=status.HTTP_400_BAD_REQUEST)
        login(request, user, backend="django.contrib.auth.backends.ModelBackend")
        signup_event(user)
        signup_sms(user)
        return Response({"user": serialize_user(user)}, status=status.HTTP_201_CREATED)
