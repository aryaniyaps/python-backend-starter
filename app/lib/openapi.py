from fastapi.routing import APIRoute


def generate_operation_id(route: APIRoute) -> str:
    """Generate a unique ID for each path operation."""
    return f"{route.tags[0]}-{route.name}"
