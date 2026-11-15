"""Payment endpoints: start a Zarinpal payment, and handle the customer's return from the gateway."""

from django.conf import settings
from django.http import HttpResponseRedirect
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_protect
from oscar.core.loading import get_model
from rest_framework import status
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework.throttling import ScopedRateThrottle
from rest_framework.views import APIView

from ..models import Payment
from ..payments.zarinpal import ZarinpalError
from ..services import payments as payment_service

Order = get_model("order", "Order")


@method_decorator(csrf_protect, name="dispatch")
class StartPaymentView(APIView):
    """POST {"order_number": "..."} -> {"redirect_url": "<gateway page>"} for the customer's own unpaid order."""

    permission_classes = [IsAuthenticated]
    throttle_classes = [ScopedRateThrottle]
    throttle_scope = "payment"

    def post(self, request):
        order = Order.objects.filter(user=request.user, number=str(request.data.get("order_number", ""))).first()
        if order is None:
            return Response({"detail": "Order not found."}, status=status.HTTP_404_NOT_FOUND)
        if order.status != "Pending" or order.payments.filter(status=Payment.PAID).exists():
            return Response({"detail": "This order cannot be paid."}, status=status.HTTP_400_BAD_REQUEST)
        try:
            url = payment_service.start_payment(order, callback_url=f"{settings.SITE_URL}/api/payments/callback/")
        except ZarinpalError:
            return Response({"detail": "The payment gateway is unavailable. Try again later."}, status=status.HTTP_502_BAD_GATEWAY)
        return Response({"redirect_url": url})


class PaymentCallbackView(APIView):
    """The gateway sends the browser here (GET ?Authority=..&Status=OK|NOK); we verify and redirect to the storefront."""

    permission_classes = [AllowAny]
    authentication_classes = []

    def get(self, request):
        payment = payment_service.verify_payment(
            authority=request.query_params.get("Authority", ""),
            status_param=request.query_params.get("Status", ""),
        )
        if payment is None:
            return HttpResponseRedirect("/payment/result?status=failed")
        state = {Payment.PAID: "ok", Payment.FAILED: "failed"}.get(payment.status, "pending")
        return HttpResponseRedirect(f"/payment/result?status={state}&order={payment.order.number}")
