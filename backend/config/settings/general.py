"""Locale, auth backends, static/media files, email."""

import os

from .env import *  # noqa: F401,F403
from .env import BASE_DIR, env_bool, env_list  # noqa: F401
from .security import DEBUG  # noqa: F401

# ---------------------------------------------------------
# Authentication
# ---------------------------------------------------------

LANGUAGE_CODE = os.getenv("DJANGO_LANGUAGE_CODE", "fa")
LANGUAGES = [
    ("fa", "فارسی (ایران)"),
    ("en", "English"),
]
LOCALE_PATHS = [BASE_DIR / "locale"]

TIME_ZONE = os.getenv("DJANGO_TIME_ZONE", "Asia/Tehran")

USE_I18N = True
USE_TZ = True


# Oscar provides an authentication backend that allows
# customers to authenticate using their email address.
AUTHENTICATION_BACKENDS = (
    "oscar.apps.customer.auth_backends.EmailBackend",
    "django.contrib.auth.backends.ModelBackend",
)


# ---------------------------------------------------------
# Django Sites
# ---------------------------------------------------------

SITE_ID = 1


# ---------------------------------------------------------
# Static files
# ---------------------------------------------------------

STATIC_URL = "/static/"

STATIC_ROOT = BASE_DIR / "staticfiles"
STATICFILES_DIRS = [BASE_DIR / "static"]


# ---------------------------------------------------------
# User-uploaded media
#
# Product images uploaded through Oscar will eventually
# live here.
# ---------------------------------------------------------

MEDIA_URL = "/media/"

MEDIA_ROOT = BASE_DIR / "media"


# ---------------------------------------------------------
# Default primary key
# ---------------------------------------------------------

DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"


# ---------------------------------------------------------
# Email
#
# For development we don't need an external email service.
# Django simply prints emails to the terminal.
#
# Later we can replace this with your own SMTP setup.
# ---------------------------------------------------------

EMAIL_BACKEND = "django.core.mail.backends.console.EmailBackend"
