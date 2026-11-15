"""JSON API views for the Next.js storefront, grouped by domain."""

from .addresses import (
    AddressDetailView,
    AddressListCreateView,
)
from .auth import (
    LoginView,
    LogoutView,
    MeView,
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
from .password import (
    PasswordResetOtpView,
    PasswordResetView,
)
from .signup import (
    SignupOtpView,
    SignupView,
)
from .system import (
    CsrfTokenView,
    HealthCheckView,
    NewsletterSubscribeView,
)

__all__ = [
    "PasswordResetOtpView",
    "PasswordResetView",
    "SignupOtpView",
    "SignupView",
    "AddressDetailView",
    "AddressListCreateView",
    "LoginView",
    "LogoutView",
    "MeView",
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
