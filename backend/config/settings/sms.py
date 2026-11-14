"""SMS gateway settings (provider chosen via .env)."""

import os

# "console" prints messages (development). Set a dotted path to a SmsProvider
# subclass (see api/sms/base.py) once a gateway is chosen.
SMS_PROVIDER = os.getenv("SMS_PROVIDER", "console")
SMS_API_KEY = os.getenv("SMS_API_KEY", "")
SMS_SENDER = os.getenv("SMS_SENDER", "")
SMS_TIMEOUT = float(os.getenv("SMS_TIMEOUT", "5"))

# One-time codes
OTP_TTL_SECONDS = int(os.getenv("OTP_TTL_SECONDS", "300"))
OTP_RESEND_SECONDS = int(os.getenv("OTP_RESEND_SECONDS", "60"))
OTP_MAX_ATTEMPTS = int(os.getenv("OTP_MAX_ATTEMPTS", "5"))
OTP_HOURLY_LIMIT = int(os.getenv("OTP_HOURLY_LIMIT", "5"))
