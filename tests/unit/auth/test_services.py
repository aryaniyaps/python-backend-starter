from unittest.mock import MagicMock, patch

import pytest
from argon2.exceptions import HashingError
from user_agents.parsers import UserAgent

from app.auth.models import (
    CreateUserInput,
    CreateUserResult,
    LoginUserInput,
    LoginUserResult,
    PasswordResetInput,
    PasswordResetRequestInput,
    PasswordResetToken,
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
        return_value=MagicMock(spec=User),
    ), patch.object(
        AuthRepo,
        "create_authentication_token",
        return_value="fake_token",
    ):
        result = await AuthService.register_user(
            CreateUserInput(
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
                CreateUserInput(
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
                CreateUserInput(
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
                CreateUserInput(
                    username="new_user",
                    email="new_user@example.com",
                    password="password",
                ),
            )


async def test_login_user_valid_credentials() -> None:
    """Ensure we can login a user with valid credentials."""
    with patch("app.auth.services.UserRepo.get_user_by_email") as mock_get_user:
        with patch(
            "app.auth.services.AuthRepo.create_authentication_token"
        ) as mock_create_token:
            mock_user = MagicMock(spec=User)
            mock_user.id = 1
            mock_user.password = "hashed_password"
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
    with patch("app.auth.services.UserRepo.get_user_by_email") as mock_get_user:
        mock_user = MagicMock(spec=User)
        mock_user.id = 1
        mock_user.password = "hashed_password"
        mock_get_user.return_value = mock_user

        with patch("app.auth.services.password_hasher.verify") as mock_verify:
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
    """Ensure the user's password gets rehashed if the old
    password needs rehashing."""
    with patch("app.auth.services.UserRepo.get_user_by_email") as mock_get_user:
        with patch(
            "app.auth.services.AuthRepo.create_authentication_token"
        ) as mock_create_token:
            mock_user = MagicMock(spec=User)
            mock_user.id = 1
            mock_user.password = "old_hashed_password"
            mock_get_user.return_value = mock_user
            mock_create_token.return_value = "fake_token"

            # Perform the login
            result = await AuthService.login_user(
                LoginUserInput(
                    login="user@example.com",
                    password="new_password",
                )
            )

    assert isinstance(result, LoginUserResult)
    assert result.authentication_token == "fake_token"
    assert result.user == mock_user


async def test_verify_authentication_token_valid_token() -> None:
    """Ensure we can verify a valid authentication token."""
    with patch(
        "app.auth.services.AuthRepo.verify_authentication_token"
    ) as mock_verify_token:
        mock_verify_token.return_value = 1

        # Perform token verification
        user_id = await AuthService.verify_authentication_token("valid_token")

    assert user_id == 1


async def test_verify_authentication_token_invalid_token() -> None:
    """Ensure we cannot verify an invalid authentication token."""
    with patch(
        "app.auth.services.AuthRepo.verify_authentication_token"
    ) as mock_verify_token:
        mock_verify_token.return_value = None

        # Perform token verification
        with pytest.raises(UnauthenticatedError):
            await AuthService.verify_authentication_token("invalid_token")


async def test_remove_authentication_token() -> None:
    """Ensure we can remove an authentication token."""
    with patch(
        "app.auth.services.AuthRepo.remove_authentication_token"
    ) as mock_remove_token:
        # Perform token removal
        await AuthService.remove_authentication_token("token_to_remove")

    mock_remove_token.assert_called_once_with("token_to_remove")


async def test_send_password_reset_request_success() -> None:
    """Ensure we can send a password reset request successfully."""
    password_reset_request_input = PasswordResetRequestInput(email="user@example.com")
    user_agent = MagicMock(
        spec=UserAgent,
        get_os=MagicMock(return_value="Windows"),
        get_browser=MagicMock(return_value="Chrome"),
    )

    with patch.object(UserRepo, "get_user_by_email", return_value=MagicMock(spec=User)):
        with patch.object(
            AuthRepo, "create_password_reset_token", return_value="reset_token"
        ):
            with patch.object(
                AuthService,
                "send_password_reset_request_email",
                return_value=None,
            ) as mock_send_email:
                await AuthService.send_password_reset_request(
                    password_reset_request_input, user_agent
                )

    mock_send_email.assert_called_once_with(
        user=MagicMock(spec=User),
        password_reset_token="reset_token",
        operating_system=user_agent.get_os(),
        browser_name=user_agent.get_browser(),
    )


async def test_send_password_reset_request_user_not_found() -> None:
    """Ensure we cannot send a password reset request for a non-existing user."""
    password_reset_request_input = PasswordResetRequestInput(
        email="nonexistent@example.com"
    )
    user_agent = MagicMock(
        spec=UserAgent,
        get_os=MagicMock(return_value="Windows"),
        get_browser=MagicMock(return_value="Chrome"),
    )

    with patch.object(UserRepo, "get_user_by_email", return_value=None):
        with pytest.raises(
            InvalidInputError, match="User with that email does not exist."
        ):
            await AuthService.send_password_reset_request(
                password_reset_request_input, user_agent
            )


async def test_reset_password_success() -> None:
    """Ensure we can reset a user's password successfully."""
    password_reset_input = PasswordResetInput(
        email="user@example.com",
        reset_token="fake_token",
        new_password="new_password",
    )

    with patch.object(UserRepo, "get_user_by_email", return_value=MagicMock(spec=User)):
        with patch.object(
            AuthRepo,
            "get_password_reset_token",
            return_value=MagicMock(
                spec=PasswordResetToken,
            ),
        ):
            with patch.object(
                UserRepo, "update_user_password", return_value=None
            ) as mock_update_password:
                await AuthService.reset_password(password_reset_input)

    mock_update_password.assert_called_once_with(
        user_id=MagicMock(spec=User).id,
        password_hash=password_hasher.hash(
            password=password_reset_input.new_password,
        ),  # You may want to use a more specific assertion here
    )


async def test_reset_password_invalid_token() -> None:
    """Ensure we cannot reset a user's password with an invalid token."""
    with patch.object(UserRepo, "get_user_by_email", return_value=MagicMock(spec=User)):
        with patch.object(AuthRepo, "get_password_reset_token", return_value=None):
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
