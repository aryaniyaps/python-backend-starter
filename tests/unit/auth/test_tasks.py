from unittest.mock import MagicMock, patch
from urllib.parse import urlencode, urljoin

from app.auth.tasks import send_password_reset_request_email
from app.core.constants import APP_URL
from app.core.emails import EmailSender
from app.core.templates import reset_password_html, reset_password_text
from app.users.models import User


def test_send_password_reset_request_email() -> None:
    """Ensure we can send a password reset request email."""
    # Mock the required objects
    user = MagicMock(
        spec=User,
        email="user@example.com",
        username="testuser",
    )
    password_reset_token = "fake_token"
    operating_system = "Windows"
    browser_name = "Chrome"

    # Mock the email_sender.send_email function
    # FIXME: this patch isn't working because we are using the context to get
    # the email sender.
    with patch.object(EmailSender, "send_email") as mock_send_email:
        # Call the Celery task directly
        send_password_reset_request_email.apply_async(
            args=[
                user.email,
                user.username,
                password_reset_token,
                operating_system,
                browser_name,
            ]
        )

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

    # Perform assertions on the mocked send_email function
    mock_send_email.assert_called_once_with(
        to=user.email,
        subject="Password Reset Request",
        body=reset_password_text.render(
            action_url=action_url,
            operating_system=operating_system,
            browser_name=browser_name,
            username=user.username,
        ),
        html_body=reset_password_html.render(
            action_url=action_url,
            operating_system=operating_system,
            browser_name=browser_name,
            username=user.username,
        ),  # You may want to use more specific assertions here
    )
