"""Catalogue (product/category/price) serialization."""

from oscar.core.loading import get_model

from .common import currency_code, money
from ..utils import get_strategy
from ..sanitize import sanitize_html

Product = get_model("catalogue", "Product")


def get_price_information(product, request):
    """
    Resolve price, availability and stock through Oscar.

    The browser never calculates authoritative ecommerce prices.
    """

    strategy = get_strategy(request)

    # Oscar exposes a separate parent strategy because a parent product
    # can represent several purchasable child products.
    if product.is_parent:
        purchase_info = strategy.fetch_for_parent(product)
    else:
        purchase_info = strategy.fetch_for_product(product)

    price = purchase_info.price
    availability = purchase_info.availability
    stockrecord = purchase_info.stockrecord

    result = {
        "available": bool(availability.is_available_to_buy),
        "availability_message": availability.message,
        "currency": currency_code(price.currency),
        "price": None,
        "price_excl_tax": None,
        "tax": None,
        "tax_included": False,
        "stock": None,
        "sku": None,
    }

    if stockrecord is not None:
        result["sku"] = stockrecord.partner_sku
        result["stock"] = stockrecord.num_in_stock

    if not price.exists:
        return result

    result["price_excl_tax"] = money(price.excl_tax)
    result["tax"] = money(price.tax)

    if price.is_tax_known:
        result["price"] = money(price.incl_tax)
        result["tax_included"] = True
    else:
        result["price"] = money(price.excl_tax)

    return result


def serialize_image(image):
    """Convert an Oscar product image to a small frontend DTO."""

    return {
        "url": image.original.url,
        "caption": image.caption or "",
        "is_primary": image.is_primary(),
    }


def serialize_variant(product, request):
    """Serialize one purchasable Oscar child product."""

    attributes = {
        value.attribute.code: value.value_as_text
        for value in product.get_attribute_values()
    }

    images = [serialize_image(image) for image in product.get_all_images()]

    return {
        "id": product.id,
        "title": product.title,
        "slug": product.slug,
        "attributes": attributes,
        "images": images,
        "price": get_price_information(product, request),
    }


def serialize_product(product, request):
    """Convert an Oscar product to the public storefront representation."""

    categories = [
        {
            "id": category.id,
            "name": category.name,
            "slug": category.slug,
        }
        for category in product.categories.all()
    ]

    images = [serialize_image(image) for image in product.get_all_images()]

    attributes = {
        value.attribute.code: value.value_as_text
        for value in product.get_attribute_values()
    }

    children = []

    if product.is_parent:
        children = [
            serialize_variant(child, request)
            for child in product.children.all()
            if child.is_public
        ]

    return {
        "id": product.id,
        "title": product.title,
        "slug": product.slug,
        "description": sanitize_html(product.description),
        "rating": float(product.rating or 0),
        "images": images,
        "attributes": attributes,
        "categories": categories,
        "structure": product.structure,
        "price": get_price_information(product, request),
        "children": children,
    }


def serialize_category(category):
    """Return a category plus its storefront metadata."""

    # Count products assigned to this category or one of its descendants.
    # Oscar stores the tree path on the category model, so this avoids
    # issuing a separate descendant traversal for every category.
    product_count = (
        Product.objects.filter(
            is_public=True,
            categories__path__startswith=category.path,
        )
        .exclude(structure=Product.CHILD)
        .distinct()
        .count()
    )

    image_url = None
    if getattr(category, "image", None):
        try:
            image_url = category.image.url
        except ValueError:
            image_url = None

    return {
        "id": category.id,
        "name": category.name,
        "slug": category.slug,
        "product_count": product_count,
        "depth": category.depth,
        "image": image_url,
    }


def product_image_url(product):
    """Return the first available image URL for basket/order summaries."""

    images = product.get_all_images()
    if not images:
        return None
    return images[0].original.url
