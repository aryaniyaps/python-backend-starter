from uuid import uuid4

from fastapi import Request


async def set_request_id(request: Request, call_next):
    """Set a unique ID for each request."""
    # Generate a unique request ID
    request_id = uuid4()

    # Add the request ID to the request context
    request.state.request_id = request_id

    response = await call_next(request)

    # add the request ID to the response headers
    response.headers["X-Request-ID"] = request_id
    return response
