from datetime import datetime, timedelta
from unittest.mock import MagicMock, patch
from uuid import uuid4

import pytest
from argon2.exceptions import HashingError
from user_agents.parsers import UserAgent

from app.auth.models import (
    CreateUserResult,
    LoginUserInput,
    LoginUserResult,
    PasswordResetInput,
    PasswordResetRequestInput,
    PasswordResetToken,
    RegisterUserInput,
)
from app.auth.repos import AuthRepo
from app.auth.services import AuthService
from app.core.errors import InvalidInputError, UnauthenticatedError, UnexpectedError
from app.core.security import password_hasher
from app.users.models import User
from app.users.repos import UserRepo

pytestmark = pytest.mark.asyncio


async def test_register_user_success() -> None:
    """Ensure we can register a user successfully."""
    with patch.object(
        UserRepo,
        "get_user_by_email",
        return_value=None,
    ), patch.object(
        UserRepo,
        "get_user_by_username",
        return_value=None,
    ), patch.object(
        UserRepo,
        "create_user",
        return_value=MagicMock(spec=User, id=uuid4()),
    ), patch.object(
        AuthRepo,
        "create_authentication_token",
        return_value="fake_token",
    ):
        result = await AuthService.register_user(
            RegisterUserInput(
                username="new_user",
                email="new_user@example.com",
                password="password",
            ),
        )

    assert isinstance(result, CreateUserResult)
    assert result.authentication_token == "fake_token"
    assert result.user is not None


async def test_register_user_existing_email() -> None:
    """Ensure we cannot create an user with an existing email."""
    with patch.object(UserRepo, "get_user_by_email", return_value=MagicMock(spec=User)):
        with pytest.raises(
            InvalidInputError, match="User with that email already exists."
        ):
            await AuthService.register_user(
                RegisterUserInput(
                    username="new_user",
                    email="new_user@example.com",
                    password="password",
                ),
            )


async def test_register_user_existing_username() -> None:
    """Ensure we cannot create an user with an existing username."""
    with patch.object(UserRepo, "get_user_by_email", return_value=None), patch.object(
        UserRepo,
        "get_user_by_username",
        return_value=MagicMock(spec=User),
    ):
        with pytest.raises(
            InvalidInputError, match="User with that username already exists."
        ):
            await AuthService.register_user(
                RegisterUserInput(
                    username="new_user",
                    email="new_user@example.com",
                    password="password",
                ),
            )


async def test_register_user_hashing_error() -> None:
    """Ensure we cannot create an user when there is a password hashing error."""
    with patch.object(
        UserRepo,
        "get_user_by_email",
        return_value=None,
    ), patch.object(
        UserRepo,
        "get_user_by_username",
        return_value=None,
    ), patch.object(
        UserRepo,
        "create_user",
        side_effect=HashingError,
    ), patch.object(
        AuthRepo,
        "create_authentication_token",
        return_value="fake_token",
    ):
        with pytest.raises(
            UnexpectedError, match="Could not create user. Please try again."
        ):
            await AuthService.register_user(
                RegisterUserInput(
                    username="new_user",
                    email="new_user@example.com",
                    password="password",
                ),
            )


async def test_login_user_valid_credentials() -> None:
    """Ensure we can login a user with valid credentials."""
    with patch("app.auth.services.UserRepo.get_user_by_email") as mock_get_user, patch(
        "app.auth.services.AuthRepo.create_authentication_token"
    ) as mock_create_token:
        mock_user = MagicMock(spec=User)
        mock_user.id = uuid4()
        mock_user.password_hash = password_hasher.hash("password")
        mock_get_user.return_value = mock_user
        mock_create_token.return_value = "fake_token"

        # Perform the login
        result = await AuthService.login_user(
            LoginUserInput(
                login="user@example.com",
                password="password",
            )
        )

    assert isinstance(result, LoginUserResult)
    assert result.authentication_token == "fake_token"
    assert result.user == mock_user


async def test_login_user_invalid_credentials() -> None:
    """Ensure we cannot login an user with invalid credentials."""
    with patch("app.auth.services.UserRepo.get_user_by_email") as mock_get_user:
        mock_get_user.return_value = None

        # Perform the login
        with pytest.raises(InvalidInputError):
            await AuthService.login_user(
                LoginUserInput(
                    login="invalid_user@example.com",
                    password="invalid_password",
                )
            )


async def test_login_user_password_mismatch() -> None:
    """Ensure we cannot login an existing user with the wrong password."""
    with patch("app.auth.services.UserRepo.get_user_by_email") as mock_get_user, patch(
        "app.core.security.password_hasher.verify"
    ) as mock_verify:
        mock_user = MagicMock(spec=User)
        mock_user.id = uuid4()
        mock_user.password_hash = password_hasher.hash("password")
        mock_get_user.return_value = mock_user

        mock_verify.side_effect = Exception("Password mismatch")

        # Perform the login
        with pytest.raises(InvalidInputError):
            await AuthService.login_user(
                LoginUserInput(
                    login="user@example.com",
                    password="wrong_password",
                )
            )


async def test_login_user_password_rehash() -> None:
    """
    Ensure the user's password gets rehashed if the old
    password needs rehashing.
    """
    with patch("app.auth.services.UserRepo.get_user_by_email") as mock_get_user, patch(
        "app.auth.services.AuthRepo.create_authentication_token"
    ) as mock_create_token:
        mock_user = MagicMock(spec=User)
        mock_user.id = uuid4()
        mock_user.password_hash = password_hasher.hash("password")
        mock_get_user.return_value = mock_user
        mock_create_token.return_value = "fake_token"

        # Perform the login
        result = await AuthService.login_user(
            LoginUserInput(
                login="user@example.com",
                password="password",
            )
        )

    assert isinstance(result, LoginUserResult)
    assert result.authentication_token == "fake_token"
    assert result.user == mock_user

    # TODO: add more checks to see if password was rehashed


async def test_verify_authentication_token_valid_token() -> None:
    """Ensure we can verify a valid authentication token."""
    with patch(
        "app.auth.services.AuthRepo.get_user_id_from_authentication_token"
    ) as mock_get_user_id_from_token:
        mock_get_user_id_from_token.return_value = 1

        # Perform token verification
        user_id = await AuthService.verify_authentication_token("valid_token")

    assert user_id == 1


async def test_verify_authentication_token_invalid_token() -> None:
    """Ensure we cannot verify an invalid authentication token."""
    with patch(
        "app.auth.services.AuthRepo.get_user_id_from_authentication_token"
    ) as mock_get_user_id_from_token:
        mock_get_user_id_from_token.return_value = None

        # Perform token verification
        with pytest.raises(UnauthenticatedError):
            await AuthService.verify_authentication_token("invalid_token")


async def test_remove_authentication_token() -> None:
    """Ensure we can remove an authentication token."""
    mock_user = MagicMock(spec=User, id=uuid4())
    with patch(
        "app.auth.services.AuthRepo.remove_authentication_token"
    ) as mock_remove_token:
        # Perform token removal
        await AuthService.remove_authentication_token(
            authentication_token="token_to_remove",
            user_id=mock_user.id,
        )

    mock_remove_token.assert_called_once_with(
        authentication_token="token_to_remove",
        user_id=mock_user.id,
    )


async def test_send_password_reset_request_success() -> None:
    """Ensure we can send a password reset request successfully."""
    user_agent = MagicMock(
        spec=UserAgent,
        get_os=MagicMock(return_value="Windows"),
        get_browser=MagicMock(return_value="Chrome"),
    )

    mock_user = MagicMock(
        spec=User,
        id=uuid4(),
        email="user@example.com",
        username="username",
        last_login_at=datetime.now(),
    )

    with patch.object(
        UserRepo,
        "get_user_by_email",
        return_value=mock_user,
    ), patch.object(
        AuthRepo, "create_password_reset_token", return_value="reset_token"
    ), patch(
        "app.auth.tasks.send_password_reset_request_email"
    ) as mock_send_email:
        mock_send_email.return_value = None
        await AuthService.send_password_reset_request(
            PasswordResetRequestInput(
                email=mock_user.email,
            ),
            user_agent,
        )

    mock_send_email.assert_called_once_with(
        to=mock_user.email,
        username=mock_user.username,
        password_reset_token="reset_token",
        operating_system=user_agent.get_os(),
        browser_name=user_agent.get_browser(),
    )


async def test_send_password_reset_request_user_not_found() -> None:
    """Ensure we cannot send a password reset request for a non-existing user."""
    user_agent = MagicMock(
        spec=UserAgent,
        get_os=MagicMock(return_value="Windows"),
        get_browser=MagicMock(return_value="Chrome"),
    )

    with patch.object(UserRepo, "get_user_by_email", return_value=None):
        await AuthService.send_password_reset_request(
            PasswordResetRequestInput(email="nonexistent@example.com"), user_agent
        )
        # TODO: assert password reset email was not sent
        # and password reset token was not created


async def test_reset_password_success() -> None:
    """Ensure we can reset a user's password successfully."""
    password_reset_input = PasswordResetInput(
        email="user@example.com",
        reset_token="fake_token",
        new_password="new_password",
    )

    user_id = uuid4()
    with patch.object(
        UserRepo,
        "get_user_by_email",
        return_value=MagicMock(
            spec=User,
            email="user@example.com",
            id=user_id,
            # user has logged in before requesting password reset token
            last_login_at=datetime.now() - timedelta(minutes=5),
        ),
    ), patch.object(
        AuthRepo,
        "get_password_reset_token",
        return_value=MagicMock(
            spec=PasswordResetToken,
            user_id=user_id,
            last_login_at=datetime.now(),
        ),
    ), patch.object(
        UserRepo, "update_user_password", return_value=None
    ) as mock_update_password, patch.object(
        AuthRepo, "remove_all_authentication_tokens", return_value=None
    ) as mock_remove_all_authentication_tokens:
        await AuthService.reset_password(password_reset_input)

    # FIXME: this assertion will always fail as no two
    # argon2 hashes are the same
    mock_update_password.assert_called_once_with(
        user_id=user_id,
        password_hash=password_hasher.hash(
            password=password_reset_input.new_password,
        ),  # You may want to use a more specific assertion here
    )

    mock_remove_all_authentication_tokens.assert_called_once_with(
        user_id=user_id,
    )


async def test_reset_password_invalid_token() -> None:
    """Ensure we cannot reset a user's password with an invalid token."""
    with patch.object(
        UserRepo,
        "get_user_by_email",
        return_value=MagicMock(spec=User),
    ), patch.object(
        AuthRepo,
        "get_password_reset_token",
        return_value=None,
    ):
        with pytest.raises(
            InvalidInputError, match="Invalid password reset token or email."
        ):
            await AuthService.reset_password(
                PasswordResetInput(
                    email="user@example.com",
                    reset_token="invalid_token",
                    new_password="new_password",
                ),
            )


async def test_reset_password_user_not_found() -> None:
    """Ensure we cannot reset a password for a non-existing user."""

    with patch.object(UserRepo, "get_user_by_email", return_value=None):
        with pytest.raises(
            InvalidInputError, match="Invalid password reset token or email."
        ):
            await AuthService.reset_password(
                PasswordResetInput(
                    email="nonexistent@example.com",
                    reset_token="fake_token",
                    new_password="new_password",
                ),
            )


async def test_reset_password_invalid_email() -> None:
    """Ensure we cannot reset a password for an invalid email."""
    with patch.object(UserRepo, "get_user_by_email", return_value=None):
        with pytest.raises(
            InvalidInputError, match="Invalid password reset token or email."
        ):
            await AuthService.reset_password(
                PasswordResetInput(
                    email="invalid_email@example.com",
                    reset_token="fake_token",
                    new_password="new_password",
                ),
            )
