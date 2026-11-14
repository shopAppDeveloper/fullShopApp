"""SMS one-time codes: issue (with cooldown + hourly cap) and verify (limited attempts, single use)."""

import secrets
from datetime import timedelta

from django.conf import settings
from django.utils import timezone
from django.utils.crypto import constant_time_compare, salted_hmac

from .models import OtpCode
from .sms import send_sms

SIGNUP, RESET = "signup", "reset"

OK, TOO_SOON, LIMIT = "ok", "too_soon", "limit"


def _hash(mobile, purpose, code):
    return salted_hmac("otp", f"{mobile}:{purpose}:{code}").hexdigest()


def request_otp(mobile: str, purpose: str) -> str:
    """Create and SMS a code. Returns OK, TOO_SOON (resend cooldown) or LIMIT (hourly cap)."""
    now = timezone.now()
    recent = OtpCode.objects.filter(mobile=mobile, purpose=purpose, created_at__gte=now - timedelta(hours=1))
    last = recent.first()
    if last and (now - last.created_at).total_seconds() < settings.OTP_RESEND_SECONDS:
        return TOO_SOON
    if recent.count() >= settings.OTP_HOURLY_LIMIT:
        return LIMIT
    code = f"{secrets.randbelow(10**6):06d}"
    OtpCode.objects.filter(mobile=mobile, purpose=purpose, used=False).update(used=True)
    OtpCode.objects.create(
        mobile=mobile, purpose=purpose, code_hash=_hash(mobile, purpose, code),
        expires_at=now + timedelta(seconds=settings.OTP_TTL_SECONDS),
    )
    send_sms(mobile, f"کد تأیید شما: {code}", purpose="otp", log_text=False)
    return OK


def verify_otp(mobile: str, purpose: str, code: str) -> bool:
    """True once for a correct, unexpired code; wrong guesses are counted and lock the code."""
    otp = OtpCode.objects.filter(mobile=mobile, purpose=purpose, used=False).first()
    if not otp or otp.expires_at < timezone.now() or otp.attempts >= settings.OTP_MAX_ATTEMPTS:
        return False
    otp.attempts += 1
    ok = constant_time_compare(otp.code_hash, _hash(mobile, purpose, str(code).strip()))
    if ok:
        otp.used = True
    otp.save(update_fields=["attempts", "used"])
    return ok
