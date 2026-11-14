"""catalog views."""
from oscar.core.loading import get_model

from django.db.models import Q
from oscar.apps.address.models import Country
from rest_framework import status
from rest_framework.generics import ListAPIView
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView

from ..serializers import serialize_category, serialize_product

Product = get_model("catalogue", "Product")
Category = get_model("catalogue", "Category")


class ProductListView(ListAPIView):
    permission_classes = [AllowAny]
    authentication_classes = []

    def get_queryset(self):
        queryset = (
            Product.objects.filter(is_public=True)
            .exclude(structure=Product.CHILD)
            .prefetch_related(
                "images",
                "categories",
                "attribute_values__attribute",
                "children__images",
                "children__attribute_values__attribute",
            )
        )

        search = str(self.request.query_params.get("search", "")).strip()
        category = str(self.request.query_params.get("category", "")).strip()
        sort = str(self.request.query_params.get("sort", "latest")).strip()

        if search:
            queryset = queryset.filter(
                Q(title__icontains=search) | Q(description__icontains=search)
            )

        if category:
            queryset = queryset.filter(categories__slug=category)

        if sort == "oldest":
            queryset = queryset.order_by("date_created")
        elif sort == "priority":
            queryset = queryset.order_by("-priority", "-date_created")
        elif sort == "price_asc":
            # The exact customer price is strategy-driven. This DB ordering
            # is only a best-effort catalogue order and must not be used for
            # checkout calculations.
            queryset = queryset.order_by("stockrecords__price", "title")
        elif sort == "price_desc":
            queryset = queryset.order_by("-stockrecords__price", "title")
        else:
            queryset = queryset.order_by("-date_created", "-priority")

        return queryset.distinct()

    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())
        page = self.paginate_queryset(queryset)

        data_source = page if page is not None else queryset
        data = [serialize_product(product, request) for product in data_source]

        if page is not None:
            return self.get_paginated_response(data)

        return Response(data)


class ProductDetailView(APIView):
    permission_classes = [AllowAny]
    authentication_classes = []

    def get(self, request, slug):
        try:
            product = Product.objects.prefetch_related(
                "images",
                "children__images",
                "children__attribute_values__attribute",
                "attribute_values__attribute",
                "categories",
            ).get(slug=slug, is_public=True)
        except Product.DoesNotExist:
            return Response(
                {"detail": "Product not found."},
                status=status.HTTP_404_NOT_FOUND,
            )

        if product.is_child:
            return Response(
                {"detail": "Product not found."},
                status=status.HTTP_404_NOT_FOUND,
            )

        return Response(serialize_product(product, request))


class CategoryListView(APIView):
    permission_classes = [AllowAny]
    authentication_classes = []

    def get(self, request):
        categories = Category.objects.filter(
            is_public=True, ancestors_are_public=True
        ).order_by("path")
        return Response([serialize_category(category) for category in categories])


class CountryListView(APIView):
    permission_classes = [AllowAny]
    authentication_classes = []

    def get(self, request):
        countries = Country.objects.filter(
            printable_name__isnull=False, is_shipping_country=True
        ).order_by("printable_name")
        return Response(
            [
                {
                    "code": country.iso_3166_1_a2,
                    "name": country.printable_name or country.name,
                }
                for country in countries
            ]
        )
