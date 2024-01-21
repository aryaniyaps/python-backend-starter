from fastapi import HTTPException, Request, status


def get_ip_address(request: Request) -> str:
    """Get the IP address from the request."""
    if request.client is None:
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail="Client IP not available",
        )
    return request.client.host
