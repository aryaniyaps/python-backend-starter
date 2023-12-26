import asyncio

from app.asgi import run_app
from app.config import get_settings

from . import create_app


async def main() -> None:
    """Initialize and run the application."""
    settings = get_settings()
    app = create_app(settings=settings)

    await run_app(
        app=app,
        settings=settings,
    )


if __name__ == "__main__":
    asyncio.run(main())
