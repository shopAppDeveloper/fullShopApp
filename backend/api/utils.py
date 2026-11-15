"""Request-level helpers shared by API views."""

from oscar.apps.partner.strategy import Selector


def get_strategy(request):
    """Return Oscar's pricing/availability strategy for this request."""

    return Selector().strategy(
        request=request,
        user=request.user,
    )


def parse_bool(value, default=False):
    """Parse a JSON/form-like boolean value safely."""
    if value is None:
        return default

    if isinstance(value, bool):
        return value

    if isinstance(value, (int, float)):
        return bool(value)

    return str(value).strip().lower() in {"1", "true", "yes", "on"}


def parse_positive_int(value, default=1, maximum=99):
    """Validate quantity-like integer input received from the browser."""

    try:
        result = int(value)
    except (TypeError, ValueError):
        return None

    if result < 1 or result > maximum:
        return None

    return result


def normalize_postcode(value):
    """Iranian postcodes: accept Persian digits and 10 digits without the dash (Oscar expects 12345-67890)."""
    digits = str(value).strip().translate(str.maketrans("۰۱۲۳۴۵۶۷۸۹٠١٢٣٤٥٦٧٨٩", "01234567890123456789"))
    if len(digits) == 10 and digits.isdigit():
        return f"{digits[:5]}-{digits[5:]}"
    return digits
