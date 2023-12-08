from aioinject import Container
from falcon.asgi import Request, Response


class AioInjectMiddleware:
    def __init__(self, container: Container) -> None:
        self._container = container

    async def process_request(self, req: Request, resp: Response) -> None:
        """
        Set the aioinject context manager in the request
        context and enter the context manager.
        """
        context_manager = self._container.context()
        req.context["aioinject_context_manager"] = context_manager
        await context_manager.__aenter__()

    async def process_response(self, req, resp, resource, req_succeeded) -> None:
        """
        Remove the aioinject context manager from the request
        context and exit the context manager.
        """
        context_manager = req.context.pop("aioinject_context_manager", None)
        if context_manager:
            await context_manager.__aexit__(None, None, None)
