from saq.types import Context

from app.config import settings
from app.core.emails import email_sender
from app.core.templates import (
    email_verification_request_html,
    email_verification_request_subject,
    email_verification_request_text,
    new_login_location_html,
    new_login_location_subject,
    new_login_location_text,
    onboarding_html,
    onboarding_subject,
    onboarding_text,
    reset_password_html,
    reset_password_request_html,
    reset_password_request_subject,
    reset_password_request_text,
    reset_password_subject,
    reset_password_text,
)


def send_onboarding_email(
    _ctx: Context,
    *,
    receiver: str,
    username: str,
) -> None:
    """Send an onboarding email to the given user."""
    email_sender.send(
        sender=settings.email_from,
        receivers=[receiver],
        subject=onboarding_subject.render(
            username=username,
        ),
        text=onboarding_text.render(
            username=username,
        ),
        html=onboarding_html.render(
            username=username,
        ),
    )


def send_email_verification_request_email(
    _ctx: Context,
    *,
    receiver: str,
    verification_token: str,
    device: str,
    browser_name: str,
    ip_address: str,
    location: str,
) -> None:
    """Send an email verification request to the given email."""
    email_sender.send(
        sender=settings.email_from,
        receivers=[receiver],
        subject=email_verification_request_subject.render(),
        text=email_verification_request_text.render(
            verification_token=verification_token,
            device=device,
            browser_name=browser_name,
            ip_address=ip_address,
            location=location,
        ),
        html=email_verification_request_html.render(
            verification_token=verification_token,
            device=device,
            browser_name=browser_name,
            ip_address=ip_address,
            location=location,
        ),
    )


def send_new_login_location_detected_email(
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
    """Send a new login location detected email to the given user."""
    email_sender.send(
        sender=settings.email_from,
        receivers=[receiver],
        subject=new_login_location_subject.render(
            device=device,
        ),
        text=new_login_location_text.render(
            username=username,
            login_timestamp=login_timestamp,
            device=device,
            browser_name=browser_name,
            ip_address=ip_address,
            location=location,
        ),
        html=new_login_location_html.render(
            username=username,
            login_timestamp=login_timestamp,
            device=device,
            browser_name=browser_name,
            ip_address=ip_address,
            location=location,
        ),
    )


def send_password_reset_request_email(
    _ctx: Context,
    *,
    receiver: str,
    username: str,
    password_reset_token: str,
    device: str,
    browser_name: str,
    ip_address: str,
    location: str,
) -> None:
    """Send a password reset request email to the given user."""
    email_sender.send(
        sender=settings.email_from,
        receivers=[receiver],
        subject=reset_password_request_subject.render(
            username=username,
        ),
        text=reset_password_request_text.render(
            password_reset_token=password_reset_token,
            device=device,
            browser_name=browser_name,
            username=username,
            ip_address=ip_address,
            location=location,
        ),
        html=reset_password_request_html.render(
            password_reset_token=password_reset_token,
            device=device,
            browser_name=browser_name,
            username=username,
            ip_address=ip_address,
            location=location,
        ),
    )


def send_password_reset_email(
    _ctx: Context,
    *,
    receiver: str,
    username: str,
    device: str,
    browser_name: str,
    ip_address: str,
    location: str,
) -> None:
    """Send a password reset email to the given user."""
    email_sender.send(
        sender=settings.email_from,
        receivers=[receiver],
        subject=reset_password_subject.render(),
        text=reset_password_text.render(
            device=device,
            browser_name=browser_name,
            username=username,
            ip_address=ip_address,
            location=location,
        ),
        html=reset_password_html.render(
            device=device,
            browser_name=browser_name,
            username=username,
            ip_address=ip_address,
            location=location,
        ),
    )
