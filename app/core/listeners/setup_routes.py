from di import Container, ScopeState
from di.dependent import Dependent
from di.executors import AsyncExecutor
from sanic import Request, Sanic

from app.core.containers import DIScope


def _wrap_with_container(
    handler,
    container: Container,
    app_state: ScopeState,
):
    # TODO: cache solved dependent
    solved = container.solve(
        Dependent(handler, scope=DIScope.REQUEST),
        scopes=[
            DIScope.REQUEST,
            DIScope.APP,
        ],
    )

    async def wrapped_handler(request: Request, *args, **kwargs):
        async with container.enter_scope(DIScope.REQUEST, app_state) as request_state:
            # FIXME: path params are not passed to the handlers here
            return await solved.execute_async(
                executor=AsyncExecutor(),
                state=request_state,
                values={
                    Request: request,
                },
            )

    return wrapped_handler


def setup_routes(app_state: ScopeState, container: Container):
    def _setup_routes(app: Sanic) -> None:
        app.router.reset()
        routes = app.router.routes_all
        for route in routes.values():
            route.handler = _wrap_with_container(
                handler=route.handler,
                container=container,
                app_state=app_state,
            )

        app.router.finalize()

    return _setup_routes
