import asyncio

from app.asgi import run_app
from app.config import Settings
from app.core.containers import DIScope, create_container

from . import create_app


async def main() -> None:
    """Initialize and run the application."""
    settings = Settings()  # type:ignore
    container = create_container()
    async with container.enter_scope(DIScope.APP) as app_state:
        app = create_app(
            settings=settings,
            container=container,
            app_state=app_state,
        )

        await run_app(
            app=app,
            settings=settings,
        )


if __name__ == "__main__":
    asyncio.run(main())
