from typing import Annotated

from pydantic import AmqpDsn, Field, PostgresDsn, RedisDsn, UrlConstraints
from pydantic_core import Url
from pydantic_settings import BaseSettings


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
        AmqpDsn,
        Field(
            examples=[
                "amqp://user:pass@localhost:5672//",
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

    email_server: Annotated[
        Url,
        UrlConstraints(
            allowed_schemes=[
                "smtp",
            ],
            default_port=587,
        ),
        Field(
            examples=[
                "smtp://user:pass@host:587",
            ],
        ),
    ]

    email_from: Annotated[
        str,
        Field(
            examples=[
                "aryaniyaps@example.com",
            ],
        ),
    ]

    class Config:
        env_file = ".env"
