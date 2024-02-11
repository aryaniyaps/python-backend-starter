from collections.abc import Sequence
from typing import Annotated

from pydantic import Field, PostgresDsn, RedisDsn
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    debug: bool

    host: Annotated[
        str,
        Field(
            examples=[
                "127.0.0.1",
            ],
        ),
    ] = "127.0.0.1"

    port: Annotated[
        int,
        Field(
            examples=[
                8000,
            ],
        ),
    ] = 8000

    log_level: Annotated[
        str,
        Field(
            examples=[
                "INFO",
                "NOTSET",
                "DEBUG",
            ],
        ),
    ] = "DEBUG"

    openapi_url: str | None = "/openapi.json"

    server_url: str = "http://localhost:8000"

    database_url: Annotated[
        PostgresDsn,
        Field(
            examples=[
                "postgresql+asyncpg://user:pass@localhost:5432/database",
            ],
        ),
    ]

    database_pool_size: Annotated[
        int,
        Field(
            examples=[
                20,
            ],
            gt=0,
        ),
    ] = 20

    redis_url: Annotated[
        RedisDsn,
        Field(
            examples=[
                "redis://user:pass@localhost:6379/1",
            ],
        ),
    ]

    saq_broker_url: Annotated[
        RedisDsn,
        Field(
            examples=[
                "redis://user:pass@localhost:6379/1",
            ],
        ),
    ]

    saq_concurrency: Annotated[
        int,
        Field(
            examples=[
                100,
            ],
        ),
    ] = 100

    cors_allow_origins: Annotated[
        Sequence[str],
        Field(
            examples=[
                {
                    "example.com",
                },
            ],
        ),
    ] = ("*",)

    email_port: Annotated[
        int,
        Field(
            examples=[
                587,
            ],
        ),
    ] = 587

    email_host: Annotated[
        str,
        Field(
            examples=[
                "localhost",
            ],
        ),
    ]

    email_username: str | None = None

    email_password: str | None = None

    email_from: Annotated[
        str,
        Field(
            examples=[
                "aryaniyaps@example.com",
            ],
        ),
    ]

    geolite2_database_path: Annotated[
        str,
        Field(
            examples=[
                "/path/to/GeoLite2-City.mmdb",
            ],
        ),
    ]

    google_client_id: str

    google_client_secret: str

    model_config = SettingsConfigDict(
        env_file=".env",
        env_prefix="server_",
    )


settings = Settings()
