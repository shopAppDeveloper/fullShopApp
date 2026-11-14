"""Customer serialization."""


def serialize_user(user):
    """Return only customer fields the storefront is allowed to see."""

    return {
        "id": user.id,
        "email": user.email,
        "first_name": user.first_name,
        "last_name": user.last_name,
        "is_staff": user.is_staff,
    }
