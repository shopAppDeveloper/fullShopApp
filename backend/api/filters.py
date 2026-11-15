"""Storefront filters built from Oscar product attributes with the codes `color` and `size`."""

from django.db.models import Q
from oscar.core.loading import get_model

ProductAttributeValue = get_model("catalogue", "ProductAttributeValue")

COLOR_CODES = ("color", "colour")
SIZE_CODES = ("size",)

# Known colour names -> hex, so the sidebar can draw swatches. Unknown names are shown as text chips.
COLOR_HEX = {
    "black": "#000000", "white": "#ffffff", "gray": "#9ca3af", "grey": "#9ca3af", "red": "#f23030",
    "green": "#22ad5c", "blue": "#3c50e0", "lightblue": "#7dd3fc", "pink": "#f472b6", "yellow": "#fbbf24",
    "orange": "#f27430", "purple": "#8b5cf6", "brown": "#92400e",
    "مشکی": "#000000", "سفید": "#ffffff", "طوسی": "#9ca3af", "خاکستری": "#9ca3af", "قرمز": "#f23030",
    "سبز": "#22ad5c", "آبی": "#3c50e0", "آبی روشن": "#7dd3fc", "صورتی": "#f472b6", "زرد": "#fbbf24",
    "نارنجی": "#f27430", "بنفش": "#8b5cf6", "قهوه‌ای": "#92400e",
}


def _values(codes):
    """Distinct display values of public products' attributes with the given codes."""
    out = set()
    qs = ProductAttributeValue.objects.filter(attribute__code__in=codes, product__is_public=True).select_related("attribute", "value_option")
    for av in qs:
        text = (av.value_option.option if av.value_option_id else av.value_text) or ""
        text = str(text).strip()
        if text:
            out.add(text)
    return sorted(out)


def filter_options():
    colors = [{"value": v, "hex": COLOR_HEX.get(v.lower())} for v in _values(COLOR_CODES)]
    sizes = [{"value": v} for v in _values(SIZE_CODES)]
    return {"colors": colors, "sizes": sizes}


def apply_attribute_filters(queryset, query_params):
    """Filter products by `color=a,b` and `size=a,b` (a variant match also matches its parent)."""
    for param, codes in (("color", COLOR_CODES), ("size", SIZE_CODES)):
        wanted = [v.strip() for v in str(query_params.get(param, "")).split(",") if v.strip()]
        if not wanted:
            continue
        match = Q(attribute__code__in=codes) & (Q(value_text__in=wanted) | Q(value_option__option__in=wanted))
        ids = ProductAttributeValue.objects.filter(match).values("product_id")
        queryset = queryset.filter(Q(pk__in=ids) | Q(children__pk__in=ids))
    return queryset
