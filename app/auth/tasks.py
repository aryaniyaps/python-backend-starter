from typing import Annotated
from urllib.parse import urlencode, urljoin

from aioinject import Inject, inject

from app.core.constants import APP_URL
from app.core.emails import EmailSender
from app.core.templates import reset_password_html, reset_password_text
from app.worker import worker


@worker.task
@inject
def send_password_reset_request_email(
    to: str,
    username: str,
    password_reset_token: str,
    operating_system: str,
    browser_name: str,
    email_sender: Annotated[EmailSender, Inject],
) -> None:
    """Sends a password reset request email to the given user."""

    # point action URL to a frontend page
    action_url = (
        urljoin(APP_URL, "/auth/reset-password")
        + "?"
        + urlencode(
            {
                "email": to,
                "reset_token": password_reset_token,
            }
        )
    )

    email_sender.send_email(
        to=to,
        subject="Password Reset Request",
        body=reset_password_text.render(
            action_url=action_url,
            operating_system=operating_system,
            browser_name=browser_name,
            username=username,
        ),
        html_body=reset_password_html.render(
            action_url=action_url,
            operating_system=operating_system,
            browser_name=browser_name,
            username=username,
        ),
    )
