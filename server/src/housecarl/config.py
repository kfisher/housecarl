# Copyright 2026 Kevin Fisher. All rights reserved.
# SPDX-License-Identifier: AGPL-3.0-only

"""
Application settings.

"""

from pathlib import Path

from pydantic import computed_field
from pydantic_settings import BaseSettings, SettingsConfigDict

# Only set when running as a container with Docker/Swarm secrets mounted, so
# that local, non-container use doesn't warn about a missing directory.
_SECRETS_DIR = Path("/run/secrets") if Path("/run/secrets").is_dir() else None


class Settings(BaseSettings):
    """
    Specifies the application settings.

    These settings are set using environment variables, a Docker secrets
    file (for `postgres_password`), or from a file named `.env`.
    """

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        secrets_dir=_SECRETS_DIR,
    )

    postgres_user: str = "housecarl"
    postgres_password: str
    postgres_host: str = "db"
    postgres_db: str = "housecarl"

    @computed_field  # type: ignore[prop-decorator]
    @property
    def database_url(self) -> str:
        return (
            f"postgresql+psycopg://{self.postgres_user}:{self.postgres_password}"
            f"@{self.postgres_host}/{self.postgres_db}"
        )


settings = Settings()
