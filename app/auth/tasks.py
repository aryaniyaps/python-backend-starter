from urllib.parse import urlencode, urljoin

from app.core.constants import APP_URL
from app.core.emails import email_sender
from app.core.templates import reset_password_html, reset_password_text
from app.users.models import User
from app.worker import worker


@worker.task
def send_password_reset_request_email(
    user: User,
    password_reset_token: str,
    operating_system: str,
    browser_name: str,
) -> None:
    """Sends a password reset request email to the given user."""

    # point action URL to a frontend page
    action_url = (
        urljoin(APP_URL, "/auth/reset-password")
        + "?"
        + urlencode(
            {
                "email": user.email,
                "reset_token": password_reset_token,
            }
        )
    )

    email_sender.send_email(
        to=user.email,
        subject="Password Reset Request",
        body=reset_password_text.render(),
        html_body=reset_password_html.render(
            action_url=action_url,
            operating_system=operating_system,
            browser_name=browser_name,
        ),
    )
