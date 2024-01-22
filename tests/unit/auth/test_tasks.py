from unittest.mock import MagicMock, patch
from urllib.parse import urlencode, urljoin

from app.auth.tasks import send_password_reset_request_email
from app.config import settings
from app.core.constants import APP_URL
from app.core.templates import (
    reset_password_html,
    reset_password_subject,
    reset_password_text,
)
from app.users.schemas import UserSchema
from redmail.email.sender import EmailSender


def test_send_password_reset_request_email() -> None:
    """Ensure we can send a password reset request email."""
    # Mock the required objects
    mock_user = MagicMock(
        spec=UserSchema,
        email="user@example.com",
        username="testuser",
    )

    password_reset_token = "fake_token"

    device = "Sample Device"

    browser_name = "Chrome"

    ip_address = "127.0.0.1"

    location = "Chennai, India"

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
            device=device,
            browser_name=browser_name,
            ip_address=ip_address,
            location=location,
        )

    action_url = (
        urljoin(APP_URL, "/auth/reset-password")
        + "?"
        + urlencode(
            {
                "email": mock_user.email,
                "reset_token": password_reset_token,
            },
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
            device=device,
            browser_name=browser_name,
            username=mock_user.username,
            ip_address=ip_address,
            location=location,
        ),
        html=reset_password_html.render(
            action_url=action_url,
            device=device,
            browser_name=browser_name,
            username=mock_user.username,
            ip_address=ip_address,
            location=location,
        ),
    )
