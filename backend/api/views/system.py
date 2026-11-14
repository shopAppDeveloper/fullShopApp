"""system views."""

from django.core.exceptions import ValidationError
from django.core.validators import validate_email
from django.middleware.csrf import get_token
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import ensure_csrf_cookie
from rest_framework import status
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.throttling import ScopedRateThrottle
from rest_framework.views import APIView

from ..models import NewsletterSubscriber


class HealthCheckView(APIView):
    permission_classes = [AllowAny]
    authentication_classes = []

    def get(self, request):
        return Response({"status": "ok", "service": "django"})


class CsrfTokenView(APIView):
    permission_classes = [AllowAny]
    authentication_classes = []

    @method_decorator(ensure_csrf_cookie)
    def get(self, request):
        return Response({"csrfToken": get_token(request)})


class NewsletterSubscribeView(APIView):
    permission_classes = [AllowAny]
    authentication_classes = []
    throttle_classes = [ScopedRateThrottle]
    throttle_scope = "newsletter"

    def post(self, request):
        email = str(request.data.get("email", "")).strip().lower()
        try:
            validate_email(email)
        except ValidationError:
            return Response(
                {"detail": "Enter a valid email address."},
                status=status.HTTP_400_BAD_REQUEST,
            )
        # Same answer for new and existing addresses: never reveal who is subscribed.
        NewsletterSubscriber.objects.get_or_create(email=email)
        return Response({"detail": "Subscribed."}, status=status.HTTP_201_CREATED)
