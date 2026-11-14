"""Provider-agnostic SMS contract. A concrete gateway only has to implement `SmsProvider.send`."""

from dataclasses import dataclass


@dataclass(frozen=True)
class SmsResult:
    ok: bool
    message_id: str = ""
    error: str = ""


class SmsProvider:
    """Base class for SMS gateways (Kavenegar, Melipayamak, SMS.ir, ...)."""

    name = "base"

    def send(self, to: str, text: str) -> SmsResult:
        """Send `text` to `to` (normalized, e.g. 09123456789). Must return a result, not raise."""
        raise NotImplementedError
