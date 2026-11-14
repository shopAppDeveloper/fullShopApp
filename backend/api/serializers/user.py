"""Customer serialization."""

from ..accounts import real_email
from ..models import Profile


def serialize_user(user):
    """Return only customer fields the storefront is allowed to see."""

    profile = Profile.objects.filter(user_id=user.id).only("mobile", "mobile_verified").first()
    return {
        "id": user.id,
        "email": real_email(user),
        "mobile": profile.mobile if profile else None,
        "mobile_verified": bool(profile and profile.mobile_verified),
        "first_name": user.first_name,
        "last_name": user.last_name,
        "is_staff": user.is_staff,
    }
