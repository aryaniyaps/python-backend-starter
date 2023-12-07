from aioinject import Container
from falcon.asgi import Request, Response


class AioInjectMiddleware:
    def __init__(self, container: Container) -> None:
        self.container = container

    async def process_request(
        self,
        req: Request,
        resp: Response,
    ) -> None:
        """Process the request with the container context."""
        async with self.container.context():
            pass
