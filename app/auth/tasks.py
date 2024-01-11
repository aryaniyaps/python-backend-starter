from urllib.parse import urlencode, urljoin

from app.core.constants import APP_URL
from app.core.emails import mailer
from app.core.templates import (
    reset_password_html,
    reset_password_subject,
    reset_password_text,
)
from app.worker import worker


@worker.task
def send_password_reset_request_email(
    receiver: str,
    username: str,
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
                "email": receiver,
                "reset_token": password_reset_token,
            }
        )
    )

    message = mailer.new(
        to=receiver,
        subject=reset_password_subject.render(
            username=username,
        ),
        plain=reset_password_text.render(
            action_url=action_url,
            operating_system=operating_system,
            browser_name=browser_name,
            username=username,
        ),
        rich=reset_password_html.render(
            action_url=action_url,
            operating_system=operating_system,
            browser_name=browser_name,
            username=username,
        ),
    )

    mailer.send(message)
