"""Secret key, DEBUG, hosts, CSRF, cookies and security headers."""

import os

from .env import *  # noqa: F401,F403
from .env import BASE_DIR, env_bool, env_list  # noqa: F401

# ---------------------------------------------------------
# Security
# ---------------------------------------------------------

SECRET_KEY = os.getenv(
    "DJANGO_SECRET_KEY",
    "dev-only-change-this-secret-key",
)

# Secure by default: debug mode must be switched on explicitly (DJANGO_DEBUG=True).
DEBUG = env_bool("DJANGO_DEBUG", False)

if not DEBUG and SECRET_KEY == "dev-only-change-this-secret-key":
    from django.core.exceptions import ImproperlyConfigured

    raise ImproperlyConfigured(
        "Set DJANGO_SECRET_KEY to a long random value (production), or set DJANGO_DEBUG=True for local development."
    )

ALLOWED_HOSTS = env_list(
    "DJANGO_ALLOWED_HOSTS",
    [
        "localhost",
        "127.0.0.1",
    ],
)


# ---------------------------------------------------------
# CSRF
# ---------------------------------------------------------

CSRF_TRUSTED_ORIGINS = env_list(
    "DJANGO_CSRF_TRUSTED_ORIGINS",
    [
        "http://localhost:3000",
        "http://127.0.0.1:3000",
    ],
)


# The JavaScript frontend needs to be able to read the
# CSRF cookie and copy it into the X-CSRFToken header.
CSRF_COOKIE_HTTPONLY = False


# Browser cookies should not be sent cross-site.
CSRF_COOKIE_SAMESITE = "Lax"
SESSION_COOKIE_SAMESITE = "Lax"


# The actual session ID must not be readable by JavaScript.
SESSION_COOKIE_HTTPONLY = True


# Enable these automatically when DEBUG=False.
SESSION_COOKIE_SECURE = not DEBUG
CSRF_COOKIE_SECURE = not DEBUG


# ---------------------------------------------------------
# Security headers
# ---------------------------------------------------------

SECURE_CONTENT_TYPE_NOSNIFF = True

SECURE_REFERRER_POLICY = "same-origin"

X_FRAME_OPTIONS = "DENY"


# Tell Django that Nginx terminates HTTPS.
SECURE_PROXY_SSL_HEADER = (
    "HTTP_X_FORWARDED_PROTO",
    "https",
)


# We will turn these on in the production deployment.
SECURE_SSL_REDIRECT = env_bool(
    "DJANGO_SECURE_SSL_REDIRECT",
    not DEBUG,
)

SECURE_HSTS_SECONDS = int(os.getenv("DJANGO_HSTS_SECONDS", "0" if DEBUG else "2592000"))
