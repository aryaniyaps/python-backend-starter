from collections.abc import Sequence
from enum import Enum
from typing import Annotated

from pydantic import Field, PostgresDsn, RedisDsn
from pydantic_settings import BaseSettings, SettingsConfigDict


class Environment(str, Enum):
    development = "development"
    testing = "testing"
    production = "production"


class Settings(BaseSettings):
    debug: bool

    environment: Environment = Environment.development

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

    openapi_url: str | None = "/openapi.json"

    server_url: str = "http://localhost:8000"

    # database config

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

    # redis config

    redis_url: Annotated[
        RedisDsn,
        Field(
            examples=[
                "redis://user:pass@localhost:6379/1",
            ],
        ),
    ]

    # SAQ config

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

    # email config

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

    # GeoIP config

    geolite2_database_path: Annotated[
        str,
        Field(
            examples=[
                "/path/to/GeoLite2-City.mmdb",
            ],
        ),
    ]

    # oauth2 config

    google_client_id: str

    google_client_secret: str

    # sentry config

    sentry_dsn: Annotated[
        str,
        Field(
            examples=[
                "https://public@sentry.example.com/1",
            ],
        ),
    ]

    sentry_sample_rate: Annotated[
        float,
        Field(
            gt=0.0,
            le=1.0,
            examples=[
                0.1,
                1.0,
            ],
        ),
    ] = 1.0

    model_config = SettingsConfigDict(
        env_file=".env",
        env_prefix="server_",
    )

    def _is_environment(self, environment: Environment) -> bool:
        """Check whether the current environment is the given environment."""
        return self.environment == environment

    def is_development(self) -> bool:
        """Check whether the current environment is development."""
        return self._is_environment(Environment.development)

    def is_testing(self) -> bool:
        """Check whether the current environment is testing."""
        return self._is_environment(Environment.testing)

    def is_production(self) -> bool:
        """Check whether the current environment is production."""
        return self._is_environment(Environment.production)


settings = Settings()
