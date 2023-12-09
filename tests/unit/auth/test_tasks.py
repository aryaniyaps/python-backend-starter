from unittest.mock import MagicMock
from urllib.parse import urlencode, urljoin

from app.auth.tasks import send_password_reset_request_email
from app.core.constants import APP_URL
from app.core.emails import EmailSender
from app.core.templates import (
    reset_password_html,
    reset_password_subject,
    reset_password_text,
)
from app.users.models import User


def test_send_password_reset_request_email() -> None:
    """Ensure we can send a password reset request email."""
    # Mock the required objects
    mock_user = MagicMock(
        spec=User,
        email="user@example.com",
        username="testuser",
    )
    password_reset_token = "fake_token"
    operating_system = "Windows"
    browser_name = "Chrome"

    mock_email_sender = MagicMock(
        spec=EmailSender,
        send_email=MagicMock(
            return_value=None,
        ),
    )

    send_password_reset_request_email(
        to=mock_user.email,
        username=mock_user.username,
        password_reset_token=password_reset_token,
        operating_system=operating_system,
        browser_name=browser_name,
        email_sender=mock_email_sender,
    )

    action_url = (
        urljoin(APP_URL, "/auth/reset-password")
        + "?"
        + urlencode(
            {
                "email": mock_user.email,
                "reset_token": password_reset_token,
            }
        )
    )

    # Perform assertions on the mocked send_email function
    mock_email_sender.send_email.assert_called_once_with(
        to=mock_user.email,
        subject=reset_password_subject.render(
            username=mock_user.username,
        ),
        body=reset_password_text.render(
            action_url=action_url,
            operating_system=operating_system,
            browser_name=browser_name,
            username=mock_user.username,
        ),
        html_body=reset_password_html.render(
            action_url=action_url,
            operating_system=operating_system,
            browser_name=browser_name,
            username=mock_user.username,
        ),
    )
