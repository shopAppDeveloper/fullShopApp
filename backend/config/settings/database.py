"""Database and password validation."""

import os

from .env import *  # noqa: F401,F403
from .env import BASE_DIR, env_bool, env_list  # noqa: F401
from .security import DEBUG  # noqa: F401

# ---------------------------------------------------------
# Database
# ---------------------------------------------------------

DATABASE_ENGINE = os.getenv(
    "DATABASE_ENGINE",
    "django.db.backends.sqlite3",
)

if DATABASE_ENGINE == "django.db.backends.postgresql":
    DATABASES = {
        "default": {
            "ENGINE": DATABASE_ENGINE,
            "NAME": os.getenv("DATABASE_NAME", "shop"),
            "USER": os.getenv("DATABASE_USER", "shop"),
            "PASSWORD": os.getenv("DATABASE_PASSWORD", ""),
            "HOST": os.getenv("DATABASE_HOST", "127.0.0.1"),
            "PORT": os.getenv("DATABASE_PORT", "5432"),
        }
    }

else:
    # SQLite is convenient for local development.
    #
    # IMPORTANT:
    # Oscar officially recommends PostgreSQL for production.
    DATABASES = {
        "default": {
            "ENGINE": "django.db.backends.sqlite3",
            "NAME": BASE_DIR / "db.sqlite3",
        }
    }


# ---------------------------------------------------------
# Password validation
# ---------------------------------------------------------

AUTH_PASSWORD_VALIDATORS = [
    {
        "NAME": (
            "django.contrib.auth.password_validation.UserAttributeSimilarityValidator"
        ),
    },
    {
        "NAME": ("django.contrib.auth.password_validation.MinimumLengthValidator"),
        "OPTIONS": {
            "min_length": 9,
        },
    },
    {
        "NAME": ("django.contrib.auth.password_validation.CommonPasswordValidator"),
    },
    {
        "NAME": ("django.contrib.auth.password_validation.NumericPasswordValidator"),
    },
]
