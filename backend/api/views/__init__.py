"""JSON API views for the Next.js storefront, grouped by domain."""

from .addresses import (
    AddressDetailView,
    AddressListCreateView,
)
from .auth import (
    LoginView,
    LogoutView,
    MeView,
    RegisterView,
)
from .basket import (
    BasketItemCreateView,
    BasketLineView,
    BasketView,
)
from .catalog import (
    CategoryListView,
    CountryListView,
    ProductDetailView,
    ProductListView,
)
from .orders import (
    CreateOrderView,
    OrderDetailView,
    OrderListView,
    ShippingMethodListView,
)
from .system import (
    CsrfTokenView,
    HealthCheckView,
    NewsletterSubscribeView,
)

__all__ = [
    "AddressDetailView",
    "AddressListCreateView",
    "LoginView",
    "LogoutView",
    "MeView",
    "RegisterView",
    "BasketItemCreateView",
    "BasketLineView",
    "BasketView",
    "CategoryListView",
    "CountryListView",
    "ProductDetailView",
    "ProductListView",
    "CreateOrderView",
    "OrderDetailView",
    "OrderListView",
    "ShippingMethodListView",
    "CsrfTokenView",
    "HealthCheckView",
    "NewsletterSubscribeView",
]
