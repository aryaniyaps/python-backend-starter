class BaseError(Exception):
    """
    Base error class.
    """

    def __init__(self, message: str) -> None:
        self.message = message


class InvalidInputError(BaseError):
    """
    Indicate that the client has
    issued an invalid request.
    """

    pass


class ResourceNotFoundError(BaseError):
    """
    Indicate that the requested
    resource doesn't exist.
    """

    pass


class UnauthenticatedError(BaseError):
    """
    Indicate that the client has not
    authenticated yet.
    """

    pass


class UnexpectedError(BaseError):
    """
    Indicate that an unexpected
    error has occurred.
    """

    pass
