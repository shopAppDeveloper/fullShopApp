"""Order serialization."""

from .common import currency_code, money


def serialize_order(order):
    """Return an order belonging to the current customer."""

    lines = []

    for line in order.lines.select_related("product"):
        lines.append(
            {
                "id": line.id,
                "product_id": line.product_id,
                "title": line.title,
                "quantity": line.quantity,
                "unit_price": money(line.unit_price_incl_tax),
                "line_total": money(line.line_price_incl_tax),
            }
        )

    shipping_address = order.shipping_address

    address = None
    if shipping_address:
        address = {
            "first_name": shipping_address.first_name,
            "last_name": shipping_address.last_name,
            "line1": shipping_address.line1,
            "line2": shipping_address.line2,
            "state": shipping_address.state,
            "postcode": shipping_address.postcode,
            "country": shipping_address.country.iso_3166_1_a2,
            "phone_number": shipping_address.phone_number,
            "notes": shipping_address.notes,
        }

    return {
        "id": order.id,
        "number": order.number,
        "status": order.status,
        "date_placed": order.date_placed,
        "currency": currency_code(order.currency),
        "total_incl_tax": money(order.total_incl_tax),
        "total_excl_tax": money(order.total_excl_tax),
        "shipping_charge": money(order.shipping_incl_tax),
        "lines": lines,
        "shipping_address": address,
    }
