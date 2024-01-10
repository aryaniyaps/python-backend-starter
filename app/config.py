from typing import Annotated

from pydantic import AnyUrl, Field, PostgresDsn, RedisDsn, UrlConstraints
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    debug: bool

    host: Annotated[
        str,
        Field(
            examples=[
                "127.0.0.1",
            ],
            default="127.0.0.1",
        ),
    ]

    port: Annotated[
        int,
        Field(
            examples=[
                8000,
            ],
            default=8000,
        ),
    ]

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
            default=20,
            gt=0,
        ),
    ]

    redis_url: Annotated[
        RedisDsn,
        Field(
            examples=[
                "redis://user:pass@localhost:6379/1",
            ],
        ),
    ]

    celery_broker_url: Annotated[
        RedisDsn,
        Field(
            examples=[
                "redis://user:pass@localhost:6379/1",
            ],
        ),
    ]

    cors_allow_origins: Annotated[
        set[str] | str,
        Field(
            examples=[
                {
                    "example.com",
                },
                "*",
            ],
            default="*",
        ),
    ]

    email_port: Annotated[
        int,
        Field(
            default=587,
            examples=[
                587,
            ],
        ),
    ]

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

    model_config = SettingsConfigDict(
        env_file=".env",
    )


settings = Settings()  # type: ignore
