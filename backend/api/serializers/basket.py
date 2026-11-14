"""Basket serialization."""

from .catalog import product_image_url
from .common import money


def serialize_basket_line(line, request):
    """Serialize one Oscar basket line."""

    product = line.product
    purchase_info = line.purchase_info

    if purchase_info.price.is_tax_known:
        unit_price = purchase_info.price.incl_tax
    else:
        unit_price = purchase_info.price.excl_tax

    # Oscar calculates line totals and offer discounts on the basket line.
    line_total = line.line_price_incl_tax_incl_discounts

    return {
        "id": line.id,
        "product_id": product.id,
        "title": product.title,
        "slug": product.slug,
        "quantity": line.quantity,
        "unit_price": money(unit_price),
        "line_total": money(line_total),
        "currency": purchase_info.price.currency,
        "sku": purchase_info.stockrecord.partner_sku
        if purchase_info.stockrecord
        else None,
        "image": product_image_url(product),
        "availability": {
            "available": purchase_info.availability.is_available_to_buy,
            "message": purchase_info.availability.message,
        },
    }


def serialize_basket(basket, request):
    """Return the current server-side Oscar basket."""

    lines = [serialize_basket_line(line, request) for line in basket.all_lines()]

    if basket.is_tax_known:
        total = basket.total_incl_tax
        total_excl_tax = basket.total_excl_tax
    else:
        total = basket.total_excl_tax
        total_excl_tax = basket.total_excl_tax

    return {
        "id": basket.id,
        "status": basket.status,
        "num_items": basket.num_items,
        "num_lines": basket.num_lines,
        "is_empty": basket.is_empty,
        "is_shipping_required": basket.is_shipping_required(),
        "currency": basket.currency,
        "total": money(total),
        "total_excl_tax": money(total_excl_tax),
        "lines": lines,
    }
