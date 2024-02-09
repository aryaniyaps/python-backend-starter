from http import HTTPStatus

from fastapi import HTTPException, Request


def get_ip_address(request: Request) -> str:
    """Get the IP address from the request."""
    if request.client is None:
        raise HTTPException(
            status_code=HTTPStatus.UNPROCESSABLE_ENTITY,
            detail="Client IP not available.",
        )
    return request.client.host
