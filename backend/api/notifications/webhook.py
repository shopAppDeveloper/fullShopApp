"""Stub for future bot commands (e.g. "report today"). Incoming updates are accepted and ignored."""

from django.conf import settings
from django.http import Http404
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView


class BotWebhookView(APIView):
    permission_classes = [AllowAny]
    authentication_classes = []

    def post(self, request, secret):
        expected = getattr(settings, "BOT_WEBHOOK_SECRET", "")
        if not expected or secret != expected:
            raise Http404
        # TODO: parse update, verify sender chat id is an admin, dispatch command.
        return Response({"ok": True})
