class BaseError(Exception):
    """Base error class."""

    def __init__(self, message: str) -> None:
        self.message = message
        super().__init__(self.message)


class InvalidInputError(BaseError):
    """Indicate that the client has issued an invalid request."""


class ResourceNotFoundError(BaseError):
    """Indicate that the requested resource doesn't exist."""


class UnauthenticatedError(BaseError):
    """Indicate that the client has not authenticated yet."""


class OauthAccountLinkingError(BaseError):
    """
    Oauth account linking error.

    Indicate that the user is trying to login with a social
    account that has not been linked yet.
    """


class OauthAccountCreateError(BaseError):
    """Indicate that the user's oauth account couldn't be created."""


class UnexpectedError(BaseError):
    """Indicate that an unexpected error has occurred."""
