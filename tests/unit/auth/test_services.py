import pytest
from unittest.mock import MagicMock, patch
from app.auth.services import AuthService
from app.auth.models import LoginUserInput, LoginUserResult
from app.core.errors import InvalidInputError, UnauthenticatedError


pytestmark = pytest.mark.asyncio


async def test_login_user_valid_credentials() -> None:
    """Ensure we can login a user with valid credentials."""
    with patch("app.auth.services.UserRepo.get_user_by_email") as mock_get_user:
        with patch(
            "app.auth.services.AuthRepo.create_authentication_token"
        ) as mock_create_token:
            mock_user = MagicMock()
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
        mock_user = MagicMock()
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
            mock_user = MagicMock()
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
