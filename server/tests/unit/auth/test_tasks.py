from unittest.mock import MagicMock, patch
from urllib.parse import urlencode, urljoin

from app.auth.tasks import (
    send_new_login_location_detected_email,
    send_onboarding_email,
    send_password_reset_request_email,
)
from app.config import settings
from app.lib.constants import APP_URL
from app.lib.templates import (
    new_login_device_html,
    new_login_device_subject,
    new_login_device_text,
    onboarding_html,
    onboarding_subject,
    onboarding_text,
    password_reset_html,
    password_reset_text,
    reset_password_request_subject,
)
from app.users.schemas import UserSchema
from redmail.email.sender import EmailSender


def test_send_onboarding_email() -> None:
    """Ensure we can send an onboarding email."""
    # Mock the required objects
    mock_user = MagicMock(
        spec=UserSchema,
        email="user@example.com",
        username="testuser",
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
        send_onboarding_email(
            receiver=mock_user.email,
            username=mock_user.username,
        )

    mock_email_sender.send.assert_called_with(
        sender=settings.email_from,
        receivers=[mock_user.email],
        subject=onboarding_subject.render(
            username=mock_user.username,
        ),
        text=onboarding_text.render(
            username=mock_user.username,
        ),
        html=onboarding_html.render(
            username=mock_user.username,
        ),
    )


def test_send_new_login_location_detected_email() -> None:
    """Ensure we can send a new login location detected email."""
    # Mock the required objects
    mock_user = MagicMock(
        spec=UserSchema,
        email="user@example.com",
        username="testuser",
    )

    login_timestamp = "12:10 PM, Monday, 22nd of January 2024"

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
        send_new_login_location_detected_email(
            receiver=mock_user.email,
            username=mock_user.username,
            login_timestamp=login_timestamp,
            device=device,
            browser_name=browser_name,
            ip_address=ip_address,
            location=location,
        )

    mock_email_sender.send.assert_called_with(
        sender=settings.email_from,
        receivers=[mock_user.email],
        subject=new_login_device_subject.render(
            username=mock_user.username,
            device=device,
        ),
        text=new_login_device_text.render(
            username=mock_user.username,
            login_timestamp=login_timestamp,
            device=device,
            browser_name=browser_name,
            ip_address=ip_address,
            location=location,
        ),
        html=new_login_device_html.render(
            username=mock_user.username,
            login_timestamp=login_timestamp,
            device=device,
            browser_name=browser_name,
            ip_address=ip_address,
            location=location,
        ),
    )


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
        subject=reset_password_request_subject.render(
            username=mock_user.username,
        ),
        text=password_reset_text.render(
            action_url=action_url,
            device=device,
            browser_name=browser_name,
            username=mock_user.username,
            ip_address=ip_address,
            location=location,
        ),
        html=password_reset_html.render(
            action_url=action_url,
            device=device,
            browser_name=browser_name,
            username=mock_user.username,
            ip_address=ip_address,
            location=location,
        ),
    )
