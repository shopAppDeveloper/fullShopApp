"""Paths and environment-variable helpers."""

import os
from pathlib import Path


# ---------------------------------------------------------
# Basic paths
# ---------------------------------------------------------

BASE_DIR = Path(__file__).resolve().parent.parent.parent


# ---------------------------------------------------------
# Environment helpers
# ---------------------------------------------------------


def env_bool(name: str, default: bool = False) -> bool:
    """
    Read a boolean environment variable.

    Examples:
        DEBUG=true
        DEBUG=false

    This allows us to use the same code in development
    and production without editing this file every time.
    """
    value = os.getenv(name)

    if value is None:
        return default

    return value.lower() in ("1", "true", "yes", "on")


def env_list(name: str, default: list[str] | None = None) -> list[str]:
    """
    Read a comma-separated environment variable.

    Example:

        ALLOWED_HOSTS=localhost,127.0.0.1

    becomes:

        ["localhost", "127.0.0.1"]
    """
    value = os.getenv(name)

    if not value:
        return default or []

    return [item.strip() for item in value.split(",") if item.strip()]
