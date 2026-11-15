"""auth views."""

from django.contrib.auth import login, logout
from django.contrib.auth.hashers import make_password
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_protect
from rest_framework import status
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework.throttling import ScopedRateThrottle
from rest_framework.views import APIView

from ..accounts import find_user_by_login
from ..serializers import serialize_user


class LoginView(APIView):
    """Log in with a mobile number or an e-mail address (`identifier`; legacy `email` also accepted)."""

    permission_classes = [AllowAny]
    authentication_classes = []
    throttle_classes = [ScopedRateThrottle]
    throttle_scope = "auth"

    def post(self, request):
        identifier = request.data.get("identifier") or request.data.get("email") or request.data.get("mobile")
        password = request.data.get("password", "")

        if not identifier or not password:
            return Response(
                {"detail": "Email or mobile number and password are required."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        user = find_user_by_login(identifier)
        if user is None:
            make_password(password)  # keep timing similar to a real check
        if user is None or not user.check_password(password):
            return Response(
                {"detail": "Invalid email or password."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        if not user.is_active:
            return Response(
                {"detail": "This account is not active."},
                status=status.HTTP_403_FORBIDDEN,
            )

        login(request, user, backend="django.contrib.auth.backends.ModelBackend")
        return Response({"user": serialize_user(user)})


class MeView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        return Response({"user": serialize_user(request.user)})


@method_decorator(csrf_protect, name="dispatch")
class LogoutView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        logout(request)
        return Response({"detail": "Logged out successfully."})
