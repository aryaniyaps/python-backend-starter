from fastapi import Request


def get_ip_address(request: Request) -> str:
    """Get the IP address from the request."""
    return request.client.host
