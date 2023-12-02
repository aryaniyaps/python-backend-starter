from typing import Annotated

from pydantic import AmqpDsn, Field, PostgresDsn, RedisDsn
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    debug: bool

    database_url: Annotated[
        PostgresDsn,
        Field(
            examples=[
                "postgresql+asyncpg://user:pass@localhost:5432/database",
            ],
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
        str,
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


settings = Settings()  # type: ignore
