"""auth views."""

from django.contrib.auth import authenticate, get_user_model, login, logout
from django.contrib.auth.password_validation import validate_password
from django.core.exceptions import ValidationError
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_protect
from rest_framework import status
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework.throttling import ScopedRateThrottle
from rest_framework.views import APIView

from ..serializers import serialize_user


class LoginView(APIView):
    permission_classes = [AllowAny]
    authentication_classes = []
    throttle_classes = [ScopedRateThrottle]
    throttle_scope = "auth"

    def post(self, request):
        email = str(request.data.get("email", "")).strip().lower()
        password = request.data.get("password", "")

        if not email or not password:
            return Response(
                {"detail": "Email and password are required."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        user = authenticate(
            request=request,
            username=email,
            password=password,
        )

        if user is None:
            return Response(
                {"detail": "Invalid email or password."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        if not user.is_active:
            return Response(
                {"detail": "This account is not active."},
                status=status.HTTP_403_FORBIDDEN,
            )

        login(request, user)
        return Response({"user": serialize_user(user)})


@method_decorator(csrf_protect, name="dispatch")
class RegisterView(APIView):
    permission_classes = [AllowAny]
    authentication_classes = []
    throttle_classes = [ScopedRateThrottle]
    throttle_scope = "auth"

    def post(self, request):
        email = str(request.data.get("email", "")).strip().lower()
        password = request.data.get("password", "")
        first_name = str(request.data.get("first_name", "")).strip()
        last_name = str(request.data.get("last_name", "")).strip()

        if not email or not password:
            return Response(
                {"detail": "Email and password are required."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        User = get_user_model()

        if User.objects.filter(email__iexact=email).exists():
            return Response(
                {"detail": "An account with this email already exists."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        user = User(
            username=email,
            email=email,
            first_name=first_name,
            last_name=last_name,
            is_active=True,
        )

        try:
            validate_password(password, user=user)
        except ValidationError as exc:
            return Response(
                {"detail": exc.messages},
                status=status.HTTP_400_BAD_REQUEST,
            )

        user.set_password(password)
        user.save()
        login(
            request,
            user,
            backend="django.contrib.auth.backends.ModelBackend",
        )

        return Response(
            {"user": serialize_user(user)},
            status=status.HTTP_201_CREATED,
        )


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
