"""Discount codes (Oscar vouchers) on the current basket."""

from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_protect
from oscar.apps.basket.signals import voucher_addition, voucher_removal
from oscar.core.loading import get_class, get_model
from rest_framework import status
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.throttling import ScopedRateThrottle
from rest_framework.views import APIView

from ..serializers import serialize_basket

Voucher = get_model("voucher", "Voucher")
Applicator = get_class("offer.applicator", "Applicator")


def _error(detail):
    return Response({"detail": detail}, status=status.HTTP_400_BAD_REQUEST)


@method_decorator(csrf_protect, name="dispatch")
class BasketVoucherView(APIView):
    """POST {"code": "VIP10"} applies a discount code to the basket."""

    permission_classes = [AllowAny]
    throttle_classes = [ScopedRateThrottle]
    throttle_scope = "coupon"

    def post(self, request):
        basket = request.basket
        code = str(request.data.get("code", "")).strip()
        if not code:
            return _error("Enter a discount code.")
        if basket.is_empty:
            return _error("Your basket is empty.")

        voucher = Voucher.objects.filter(code__iexact=code).first()
        if voucher is None or not voucher.is_active():
            return _error("Invalid or expired discount code.")
        if basket.vouchers.filter(pk=voucher.pk).exists():
            return _error("This discount code is already applied.")
        available, _message = voucher.is_available_to_user(request.user)
        if not available:
            return _error("This discount code is not available for you.")

        basket.vouchers.add(voucher)
        basket.reset_offer_applications()
        Applicator().apply(basket, request.user, request)

        # A code that gives no discount (e.g. basket too small) is not kept.
        if not basket.offer_applications.voucher_discounts:
            basket.vouchers.remove(voucher)
            basket.reset_offer_applications()
            Applicator().apply(basket, request.user, request)
            return _error("Your basket does not qualify for this discount code.")

        voucher_addition.send(sender=self, basket=basket, voucher=voucher)
        return Response(serialize_basket(basket, request))


@method_decorator(csrf_protect, name="dispatch")
class BasketVoucherRemoveView(APIView):
    permission_classes = [AllowAny]

    def delete(self, request, code):
        basket = request.basket
        voucher = basket.vouchers.filter(code__iexact=code).first()
        if voucher is None:
            return Response({"detail": "Discount code not found."}, status=status.HTTP_404_NOT_FOUND)
        basket.vouchers.remove(voucher)
        voucher_removal.send(sender=self, basket=basket, voucher=voucher)
        basket.reset_offer_applications()
        Applicator().apply(basket, request.user, request)
        return Response(serialize_basket(basket, request))
