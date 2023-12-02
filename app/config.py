from typing import Annotated

from pydantic import AmqpDsn, EmailStr, Field, PostgresDsn, RedisDsn, SecretStr
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
        set[str],
        Field(
            examples=[
                {
                    "example.com",
                },
            ],
            default={
                "*",
            },
        ),
    ]

    smtp_server: str

    smtp_port: Annotated[
        int,
        Field(
            examples=[587],
        ),
    ]

    email_username: EmailStr

    email_password: SecretStr

    class Config:
        env_file = ".env"


settings = Settings()  # type: ignore
