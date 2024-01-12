from unittest.mock import MagicMock, patch
from urllib.parse import urlencode, urljoin

from redmail.email.sender import EmailSender

from app.auth.tasks import send_password_reset_request_email
from app.config import settings
from app.core.constants import APP_URL
from app.core.templates import (
    reset_password_html,
    reset_password_subject,
    reset_password_text,
)
from app.users.schemas import UserSchema
from tests.unit.mock_smtp import MockSMTP


def test_send_password_reset_request_email() -> None:
    """Ensure we can send a password reset request email."""
    # Mock the required objects
    mock_user = MagicMock(
        spec=UserSchema,
        email="user@example.com",
        username="testuser",
    )
    password_reset_token = "fake_token"
    operating_system = "Windows"
    browser_name = "Chrome"

    mock_email_sender = EmailSender(
        host=settings.email_host,
        port=settings.email_port,
        use_starttls=False,
        cls_smtp=MockSMTP,  # type: ignore
    )

    mock_email_sender = MagicMock(
        spec=EmailSender,
        send=MagicMock(
            return_value=None,
        ),
    )

    with patch(
        "app.auth.tasks.email_sender",
        mock_email_sender,
    ):
        send_password_reset_request_email(
            receiver=mock_user.email,
            username=mock_user.username,
            password_reset_token=password_reset_token,
            operating_system=operating_system,
            browser_name=browser_name,
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

    mock_email_sender.send.assert_called_with(
        sender=settings.email_from,
        receivers=[mock_user.email],
        subject=reset_password_subject.render(
            username=mock_user.username,
        ),
        text=reset_password_text.render(
            action_url=action_url,
            operating_system=operating_system,
            browser_name=browser_name,
            username=mock_user.username,
        ),
        html=reset_password_html.render(
            action_url=action_url,
            operating_system=operating_system,
            browser_name=browser_name,
            username=mock_user.username,
        ),
    )
