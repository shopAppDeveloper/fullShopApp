"""basket views."""

import logging
from oscar.core.loading import get_model

from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_protect
from rest_framework import status
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView

from ..utils import get_strategy, parse_positive_int
from ..serializers import serialize_basket

Product = get_model("catalogue", "Product")
logger = logging.getLogger(__name__)


class BasketView(APIView):
    """Return the current anonymous or authenticated Oscar basket."""

    permission_classes = [AllowAny]

    def get(self, request):
        return Response(serialize_basket(request.basket, request))

    @method_decorator(csrf_protect)
    def delete(self, request):
        basket = request.basket
        if not basket.is_empty:
            basket.flush()
        return Response(serialize_basket(basket, request))


@method_decorator(csrf_protect, name="dispatch")
class BasketItemCreateView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        product_id = request.data.get("product_id")
        quantity = parse_positive_int(request.data.get("quantity"), default=1)

        if quantity is None:
            return Response(
                {"detail": "Quantity must be between 1 and 99."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        try:
            product = Product.objects.get(id=product_id, is_public=True)
        except (Product.DoesNotExist, TypeError, ValueError):
            return Response(
                {"detail": "Product not found."},
                status=status.HTTP_404_NOT_FOUND,
            )

        if product.is_parent:
            return Response(
                {"detail": "Select a product variant before adding it to the basket."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        basket = request.basket

        try:
            basket.strategy = get_strategy(request)
            line, _created = basket.add_product(product, quantity=quantity)
        except Exception as exc:
            # Oscar performs the actual availability/quantity checks.
            # We log the exception server-side and return a safe message
            # instead of exposing Python/Oscar internals to customers.
            logger.exception("Unable to add product %s to basket.", product.id)
            return Response(
                {"detail": "The product could not be added to the basket."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        return Response(
            {
                "basket": serialize_basket(basket, request),
                "line_id": line.id,
            },
            status=status.HTTP_201_CREATED,
        )


@method_decorator(csrf_protect, name="dispatch")
class BasketLineView(APIView):
    permission_classes = [AllowAny]

    def put(self, request, line_id):
        basket = request.basket
        basket.strategy = get_strategy(request)
        quantity = parse_positive_int(request.data.get("quantity"), default=1)

        if quantity is None:
            return Response(
                {"detail": "Quantity must be between 1 and 99."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        try:
            line = basket.lines.get(id=line_id)
        except basket.lines.model.DoesNotExist:
            return Response(
                {"detail": "Basket line not found."},
                status=status.HTTP_404_NOT_FOUND,
            )

        allowed, reason = line.purchase_info.availability.is_purchase_permitted(
            quantity
        )
        if not allowed:
            return Response(
                {"detail": reason},
                status=status.HTTP_400_BAD_REQUEST,
            )

        line.quantity = quantity
        line.save()
        basket.reset_offer_applications()

        return Response(serialize_basket(basket, request))

    def delete(self, request, line_id):
        basket = request.basket

        try:
            line = basket.lines.get(id=line_id)
        except basket.lines.model.DoesNotExist:
            return Response(
                {"detail": "Basket line not found."},
                status=status.HTTP_404_NOT_FOUND,
            )

        line.delete()
        basket.reset_offer_applications()

        return Response(serialize_basket(basket, request))
