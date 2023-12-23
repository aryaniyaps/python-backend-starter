from uuid import uuid4

from sanic import Request


async def set_request_id(request: Request) -> None:
    """Set a unique ID for each request."""
    # Generate a unique request ID
    request_id = uuid4()

    # Add the request ID to the request context
    request.ctx["request_id"] = request_id

    # add the request ID to the response headers
    request.headers["X-Request-ID"] = request_id
