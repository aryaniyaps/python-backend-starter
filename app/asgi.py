import asyncio

from fastapi import FastAPI
from uvicorn import Config, Server

from app import create_app
from app.config import settings


async def run_app(app: FastAPI) -> None:
    """Run the ASGI app instance."""
    server = Server(
        config=Config(
            app=app,
            host=settings.host,
            port=settings.port,
            server_header=settings.debug,
            reload=settings.debug,
        ),
    )

    await server.serve()


async def main() -> None:
    """Initialize and run the application."""
    await run_app(
        app=create_app(),
    )


if __name__ == "__main__":
    asyncio.run(main())
