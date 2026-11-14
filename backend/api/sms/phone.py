"""Iranian mobile number normalisation."""

import re

_DIGITS = str.maketrans("۰۱۲۳۴۵۶۷۸۹٠١٢٣٤٥٦٧٨٩", "01234567890123456789")
_MOBILE = re.compile(r"^09\d{9}$")


def normalize_mobile(value) -> str | None:
    """
    Return the number as 09XXXXXXXXX, or None if it is not a valid Iranian mobile.
    Accepts Persian/Arabic digits and the forms 09.., 9.., 989.., +989.., 00989...
    """
    if value is None:
        return None
    s = re.sub(r"[\s\-()]", "", str(value).translate(_DIGITS))
    if s.startswith("+"):
        s = s[1:]
    if s.startswith("0098"):
        s = s[4:]
    elif s.startswith("98"):
        s = s[2:]
    if s.startswith("9") and len(s) == 10:
        s = "0" + s
    return s if _MOBILE.match(s) else None
