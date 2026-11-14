"""orders views."""

import logging

from django.conf import settings
from django.core.exceptions import ValidationError
from django.db import transaction
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_protect
from oscar.apps.address.models import Country
from oscar.apps.checkout.calculators import OrderTotalCalculator
from oscar.apps.order.models import Order, ShippingAddress
from oscar.apps.order.utils import OrderCreator
from oscar.apps.shipping.methods import Free
from rest_framework import status
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from ..notifications import events as order_events
from ..serializers import currency_code, money, serialize_order

logger = logging.getLogger(__name__)


class ShippingMethodListView(APIView):
    permission_classes = [AllowAny]

    def get(self, request):
        basket = request.basket
        method = Free()
        charge = method.calculate(basket)

        return Response(
            [
                {
                    "code": "free",
                    "name": "Standard shipping",
                    "description": "Standard delivery",
                    "price": money(
                        charge.incl_tax if charge.is_tax_known else charge.excl_tax
                    ),
                    "currency": currency_code(charge.currency),
                }
            ]
        )


class OrderListView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        orders = (
            Order.objects.filter(user=request.user)
            .prefetch_related("lines", "shipping_address")
            .order_by("-date_placed")
        )

        return Response([serialize_order(order) for order in orders])


class OrderDetailView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, number):
        try:
            order = (
                Order.objects.filter(user=request.user)
                .prefetch_related("lines", "shipping_address")
                .get(number=number)
            )
        except Order.DoesNotExist:
            return Response(
                {"detail": "Order not found."},
                status=status.HTTP_404_NOT_FOUND,
            )

        return Response(serialize_order(order))


@method_decorator(csrf_protect, name="dispatch")
class CreateOrderView(APIView):
    """
    Create a pending Oscar order from the current basket.

    Payment is intentionally NOT marked as successful here.
    A payment provider must later verify payment before the order
    moves beyond its pending state.
    """

    permission_classes = [IsAuthenticated]

    @transaction.atomic
    def post(self, request):
        basket = request.basket
        basket.strategy = request.strategy

        if basket.is_empty:
            return Response(
                {"detail": "Your basket is empty."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        data = request.data

        required_fields = [
            "first_name",
            "last_name",
            "line1",
            "postcode",
            "country",
        ]

        missing = [
            field for field in required_fields if not str(data.get(field, "")).strip()
        ]

        if missing:
            return Response(
                {
                    "detail": "Required shipping fields are missing.",
                    "fields": missing,
                },
                status=status.HTTP_400_BAD_REQUEST,
            )

        try:
            country = Country.objects.get(
                iso_3166_1_a2__iexact=str(data["country"]).strip(),
                is_shipping_country=True,
            )
        except Country.DoesNotExist:
            return Response(
                {
                    "detail": "Invalid country. Configure countries in Oscar before checkout."
                },
                status=status.HTTP_400_BAD_REQUEST,
            )

        shipping_address = ShippingAddress(
            first_name=str(data.get("first_name", "")).strip(),
            last_name=str(data.get("last_name", "")).strip(),
            line1=str(data.get("line1", "")).strip(),
            line2=str(data.get("line2", "")).strip(),
            line3=str(data.get("line3", "")).strip(),
            line4=str(data.get("city", data.get("line4", ""))).strip(),
            state=str(data.get("state", "")).strip(),
            postcode=str(data.get("postcode", "")).strip(),
            country=country,
            phone_number=str(data.get("phone_number", "")).strip(),
            notes=str(data.get("notes", "")).strip(),
        )

        try:
            shipping_address.full_clean()
        except ValidationError as exc:
            return Response(
                {"detail": exc.message_dict},
                status=status.HTTP_400_BAD_REQUEST,
            )

        shipping_method = Free()
        shipping_charge = shipping_method.calculate(basket)
        order_total = OrderTotalCalculator().calculate(
            basket,
            shipping_charge,
        )

        # The order starts as Pending. It must not be represented as
        # paid until the payment provider has confirmed the transaction.
        order_status = getattr(Order, "PENDING", "Pending")

        if not settings.CHECKOUT_ALLOW_PENDING_ORDERS:
            return Response(
                {
                    "detail": (
                        "A payment provider is not configured for this store. "
                        "Checkout order creation is disabled until payment is connected."
                    )
                },
                status=status.HTTP_503_SERVICE_UNAVAILABLE,
            )

        try:
            order = OrderCreator().place_order(
                basket=basket,
                total=order_total,
                shipping_method=shipping_method,
                shipping_charge=shipping_charge,
                user=request.user,
                shipping_address=shipping_address,
                billing_address=None,
                status=order_status,
                request=request,
            )
        except Exception:
            logger.exception(
                "Unable to create order for user %s.",
                request.user.pk,
            )
            return Response(
                {"detail": "The order could not be created."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        # Oscar's checkout flow marks the basket submitted after the order
        # has been placed. This also prevents the same basket from being reused.
        basket.submit()
        order_events.order_placed(order)

        return Response(
            {
                "order": serialize_order(order),
                "payment": {
                    "status": "pending",
                    "required": True,
                    "message": "Connect the production payment provider before treating this order as paid.",
                },
            },
            status=status.HTTP_201_CREATED,
        )
