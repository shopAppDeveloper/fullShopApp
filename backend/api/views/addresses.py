"""addresses views."""

from django.core.exceptions import ValidationError
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_protect
from oscar.apps.address.models import Country, UserAddress
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from ..utils import parse_bool, normalize_postcode


class AddressListCreateView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        addresses = request.user.addresses.all().select_related("country")
        return Response(
            [
                {
                    "id": address.id,
                    "first_name": address.first_name,
                    "last_name": address.last_name,
                    "line1": address.line1,
                    "line2": address.line2,
                    "line3": address.line3,
                    "line4": address.line4,
                    "state": address.state,
                    "postcode": address.postcode,
                    "country": address.country.iso_3166_1_a2,
                    "country_name": address.country.printable_name,
                    "phone_number": address.phone_number,
                    "is_default_for_shipping": address.is_default_for_shipping,
                    "is_default_for_billing": address.is_default_for_billing,
                }
                for address in addresses
            ]
        )

    @method_decorator(csrf_protect)
    def post(self, request):
        data = request.data

        try:
            country = Country.objects.get(
                iso_3166_1_a2__iexact=str(data.get("country", "")).strip()
            )
        except Country.DoesNotExist:
            return Response(
                {"detail": "Invalid country."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        address = UserAddress(
            user=request.user,
            first_name=str(data.get("first_name", "")).strip(),
            last_name=str(data.get("last_name", "")).strip(),
            line1=str(data.get("line1", "")).strip(),
            line2=str(data.get("line2", "")).strip(),
            line3=str(data.get("line3", "")).strip(),
            line4=str(data.get("line4", "")).strip(),
            state=str(data.get("state", "")).strip(),
            postcode=normalize_postcode(data.get("postcode", "")),
            country=country,
            phone_number=str(data.get("phone_number", "")).strip(),
            is_default_for_shipping=parse_bool(
                data.get("is_default_for_shipping"), False
            ),
            is_default_for_billing=parse_bool(
                data.get("is_default_for_billing"), False
            ),
        )

        try:
            address.full_clean()
            address.save()
        except ValidationError as exc:
            return Response(
                {"detail": exc.message_dict},
                status=status.HTTP_400_BAD_REQUEST,
            )

        return Response(
            {
                "id": address.id,
                "detail": "Address saved.",
            },
            status=status.HTTP_201_CREATED,
        )


@method_decorator(csrf_protect, name="dispatch")
class AddressDetailView(APIView):
    permission_classes = [IsAuthenticated]

    def delete(self, request, address_id):
        try:
            address = request.user.addresses.get(id=address_id)
        except UserAddress.DoesNotExist:
            return Response(
                {"detail": "Address not found."},
                status=status.HTTP_404_NOT_FOUND,
            )

        address.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
