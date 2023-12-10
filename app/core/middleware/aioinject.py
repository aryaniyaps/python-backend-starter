from aioinject import Container, InjectionContext
from falcon.asgi import Request, Response


class AioInjectMiddleware:
    def __init__(self, container: Container) -> None:
        self._container = container

    async def process_request(
        self,
        req: Request,
        _resp: Response,
    ) -> None:
        """
        Set the aioinject context manager in the request
        context and enter the context manager.
        """
        context_manager = self._container.context()
        req.context["aioinject_context_manager"] = context_manager
        await context_manager.__aenter__()

    async def process_response(
        self,
        req: Request,
        _resp: Response,
        _resource,
        _req_succeeded: bool,
    ) -> None:
        """
        Remove the aioinject context manager from the request
        context and exit the context manager.
        """
        context_manager: InjectionContext = req.context.pop(
            "aioinject_context_manager", None
        )
        if context_manager is not None:
            await context_manager.__aexit__(None, None, None)
