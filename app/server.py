import uvicorn

from app.config import settings

if __name__ == "__main__":
    # TODO: instead of setting up logging within create_app,
    # we can pass the log config directly to uvicorn
    uvicorn.run(
        app="app:create_app",
        factory=True,
        host=settings.host,
        port=settings.port,
        server_header=settings.debug,
        reload=settings.debug,
        access_log=settings.debug,
        log_config=None,
    )
