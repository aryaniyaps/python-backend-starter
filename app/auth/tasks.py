from urllib.parse import urlencode, urljoin

from app.config import settings
from app.core.constants import APP_URL
from app.core.emails import email_sender
from app.core.templates import (
    reset_password_html,
    reset_password_subject,
    reset_password_text,
)


def send_onboarding_email(
    receiver: str,
    username: str,
    password_reset_token: str,
    operating_system: str,
    browser_name: str,
) -> None:
    """Send an onboarding email to the given user."""
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
            operating_system=operating_system,
            browser_name=browser_name,
            username=username,
        ),
        html=reset_password_html.render(
            action_url=action_url,
            operating_system=operating_system,
            browser_name=browser_name,
            username=username,
        ),
    )


def send_new_login_location_detected_email(
    receiver: str,
    username: str,
    password_reset_token: str,
    operating_system: str,
    browser_name: str,
) -> None:
    """Send a new login location detected email to the given user."""
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
            operating_system=operating_system,
            browser_name=browser_name,
            username=username,
        ),
        html=reset_password_html.render(
            action_url=action_url,
            operating_system=operating_system,
            browser_name=browser_name,
            username=username,
        ),
    )


def send_password_reset_request_email(
    receiver: str,
    username: str,
    password_reset_token: str,
    operating_system: str,
    browser_name: str,
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
            operating_system=operating_system,
            browser_name=browser_name,
            username=username,
        ),
        html=reset_password_html.render(
            action_url=action_url,
            operating_system=operating_system,
            browser_name=browser_name,
            username=username,
        ),
    )
