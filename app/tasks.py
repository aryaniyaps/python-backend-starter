from datetime import timedelta

from humanize import naturaldelta
from saq.types import Context

from app.config import settings
from app.lib.constants import (
    EMAIL_VERIFICATION_CODE_EXPIRES_IN,
)
from app.lib.emails import send_template_email
from app.repositories.email_verification_code import EmailVerificationCodeRepo


async def delete_expired_email_verification_codes(ctx: Context) -> None:
    """Delete expired email verification codes."""
    await EmailVerificationCodeRepo(session=ctx["session"]).delete_expired()


async def send_onboarding_email(
    _ctx: Context,
    *,
    receiver: str,
    email: str,
) -> None:
    """Send an onboarding email to the given user."""
    await send_template_email(
        sender=settings.email_from,
        receiver=receiver,
        template="onboarding",
        context={
            "email": email,
        },
    )


async def send_email_verification_request_email(
    _ctx: Context,
    *,
    receiver: str,
    verification_code: str,
    device: str,
    browser_name: str,
    ip_address: str,
    location: str,
) -> None:
    """Send an email verification request to the given email."""
    await send_template_email(
        sender=settings.email_from,
        receiver=receiver,
        template="email-verification-request",
        context={
            "verification_code": verification_code,
            "code_expires_in": naturaldelta(
                timedelta(
                    seconds=EMAIL_VERIFICATION_CODE_EXPIRES_IN,
                ),
            ),
            "device": device,
            "browser_name": browser_name,
            "ip_address": ip_address,
            "location": location,
        },
    )


async def send_new_login_device_detected_email(
    _ctx: Context,
    *,
    receiver: str,
    username: str,
    login_timestamp: str,
    device: str,
    browser_name: str,
    ip_address: str,
    location: str,
) -> None:
    """Send a new login device detected email to the given user."""
    await send_template_email(
        sender=settings.email_from,
        receiver=receiver,
        template="new-login-device",
        context={
            "username": username,
            "login_timestamp": login_timestamp,
            "device": device,
            "browser_name": browser_name,
            "ip_address": ip_address,
            "location": location,
        },
    )
