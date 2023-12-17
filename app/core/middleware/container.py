from di import Container, ScopeState
from di.dependent import Dependent
from di.executors import AsyncExecutor
from falcon.asgi import Request, Response

from app.core.containers import DIScope


class ContainerMiddleware:
    def __init__(
        self,
        container: Container,
        app_state: ScopeState,
    ) -> None:
        self._container = container
        self._app_state = app_state
        self._handler_cache = {}

    async def process_request(self, req: Request, resp: Response) -> None:
        """Process the request before routing it.

        Note:
            Because Falcon routes each request based on req.path, a
            request can be effectively re-routed by setting that
            attribute to a new value from within process_request().

        Args:
            req: Request object that will eventually be
                routed to an on_* responder method.
            resp: Response object that will be routed to
                the on_* responder.
        """

    async def process_resource(self, req, resp, resource, params) -> None:
        """Process the request after routing.

        Note:
            This method is only called when the request matches
            a route to a resource.

        Args:
            req: Request object that will be passed to the
                routed responder.
            resp: Response object that will be passed to the
                responder.
            resource: Resource object to which the request was
                routed.
            params: A dict-like object representing any additional
                params derived from the route's URI template fields,
                that will be passed to the resource's responder
                method as keyword arguments.
        """
        solved = self._container.solve(
            Dependent(resource, scope=DIScope.REQUEST),
            scopes=[
                DIScope.REQUEST,
            ],
        )

        context_manager = self._container.enter_scope(
            DIScope.REQUEST,
            self._app_state,
        )
        req.context["di_context_manager"] = context_manager
        request_state = await context_manager.__aenter__()

        # TODO: pass the params to the responder
        await solved.execute_async(
            executor=AsyncExecutor(),
            state=request_state,
            values={
                Request: req,
                Response: resp,
            },
        )

        # prevent falcon from calling the resource directly
        resp.complete = True

    async def process_response(
        self,
        req: Request,
        resp: Response,
        resource,
        req_succeeded: bool,
    ) -> None:
        """Post-processing of the response (after routing).

        Args:
            req: Request object.
            resp: Response object.
            resource: Resource object to which the request was
                routed. May be None if no route was found
                for the request.
            req_succeeded: True if no exceptions were raised while
                the framework processed and routed the request;
                otherwise False.
        """
        context_manager = req.context.pop("di_context_manager", None)
        if context_manager is not None:
            await context_manager.__aexit__(None, None, None)
