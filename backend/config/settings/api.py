"""Django REST Framework configuration."""

import os

from .env import *  # noqa: F401,F403
from .env import BASE_DIR, env_bool, env_list  # noqa: F401
from .security import DEBUG  # noqa: F401

# ---------------------------------------------------------
# Django REST Framework
# ---------------------------------------------------------

REST_FRAMEWORK = {
    # We use Django sessions instead of JWT initially.
    #
    # This is especially useful because Next.js and Django
    # will eventually be served under the same website.
    "DEFAULT_AUTHENTICATION_CLASSES": [
        "rest_framework.authentication.SessionAuthentication",
    ],
    # Public API endpoints are explicitly protected with
    # IsAuthenticated where necessary.
    "DEFAULT_PERMISSION_CLASSES": [
        "rest_framework.permissions.AllowAny",
    ],
    # Our frontend only needs JSON.
    "DEFAULT_RENDERER_CLASSES": [
        "rest_framework.renderers.JSONRenderer",
    ],
    "DEFAULT_PAGINATION_CLASS": ("rest_framework.pagination.PageNumberPagination"),
    "PAGE_SIZE": 24,
    # Rate limiting (brute-force / abuse protection). Scoped rates are used by
    # login, registration and the newsletter form.
    # NOTE: the default cache is per-process; use Redis/Memcached in production
    # (CACHES) so limits are shared between workers.
    "DEFAULT_THROTTLE_CLASSES": [
        "rest_framework.throttling.AnonRateThrottle",
        "rest_framework.throttling.UserRateThrottle",
    ],
    "DEFAULT_THROTTLE_RATES": {
        "anon": "300/min",
        "user": "600/min",
        "auth": "10/min",
        "newsletter": "10/hour",
    },
    # Number of reverse proxies in front of Django (nginx = 1). Needed so the
    # client IP, not the proxy IP, is used for throttling.
    "NUM_PROXIES": int(os.getenv("DJANGO_NUM_PROXIES", "0")) or None,
}
