from urllib.parse import urlencode, urljoin

from app.config import settings
from app.core.constants import APP_URL
from app.core.emails import email_sender
from app.core.templates import (
    new_login_location_html,
    new_login_location_subject,
    new_login_location_text,
    onboarding_html,
    onboarding_subject,
    onboarding_text,
    reset_password_html,
    reset_password_subject,
    reset_password_text,
)


def send_onboarding_email(
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


def send_new_login_location_detected_email(
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
    receiver: str,
    username: str,
    password_reset_token: str,
    device: str,
    browser_name: str,
    ip_address: str,
    location: str,
) -> None:
    """Send a password reset request email to the given user."""
    # point action URL to a frontend page
    action_url = (
        urljoin(APP_URL, "/auth/reset-password")
        + "?"
        + urlencode(
            {
                "email": receiver,
                "reset_token": password_reset_token,
            },
        )
    )

    email_sender.send(
        sender=settings.email_from,
        receivers=[receiver],
        subject=reset_password_subject.render(
            username=username,
        ),
        text=reset_password_text.render(
            action_url=action_url,
            device=device,
            browser_name=browser_name,
            username=username,
            ip_address=ip_address,
            location=location,
        ),
        html=reset_password_html.render(
            action_url=action_url,
            device=device,
            browser_name=browser_name,
            username=username,
            ip_address=ip_address,
            location=location,
        ),
    )
