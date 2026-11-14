"""Customer lookup helpers (mobile or e-mail identity)."""

from django.contrib.auth import get_user_model

from .models import Profile
from .sms import normalize_mobile

PLACEHOLDER_DOMAIN = "mobile.invalid"


def placeholder_email(mobile: str) -> str:
    """Oscar and Django expect an e-mail; mobile-only customers get an internal, never-shown one."""
    return f"{mobile}@{PLACEHOLDER_DOMAIN}"


def real_email(user) -> str:
    return "" if user.email.endswith("@" + PLACEHOLDER_DOMAIN) else user.email


def find_user_by_mobile(value):
    mobile = normalize_mobile(value)
    if not mobile:
        return None
    profile = Profile.objects.select_related("user").filter(mobile=mobile).first()
    return profile.user if profile else None


def find_user_by_login(identifier):
    """Resolve what the customer typed in the login box: a mobile number or an e-mail address."""
    ident = str(identifier or "").strip()
    if "@" in ident:
        return get_user_model().objects.filter(email__iexact=ident).first()
    return find_user_by_mobile(ident)


def create_mobile_user(mobile, password, first_name="", last_name="", email=""):
    """Create an active, mobile-verified customer. `mobile` must already be normalised and unused."""
    User = get_user_model()
    user = User(
        username=mobile,
        email=email.lower() if email else placeholder_email(mobile),
        first_name=first_name,
        last_name=last_name,
        is_active=True,
    )
    user.set_password(password)
    user.save()
    Profile.objects.create(user=user, mobile=mobile, mobile_verified=True)
    return user
