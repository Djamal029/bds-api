"""Application settings, loaded once from environment variables / `.env`.

WORKED EXAMPLE — fully implemented, read this one closely.

WHY a `Settings` class instead of `os.environ.get(...)` scattered across
the codebase: every setting is declared once, with its type and default,
so a typo in an env var name fails loudly at startup (Pydantic validates
it) instead of silently returning `None` deep inside some unrelated
function at request time. It also makes settings trivially mockable in
tests (override `get_settings` as a FastAPI dependency).

WHY `lru_cache` on `get_settings()`: reading and validating environment
variables is cheap but not free, and settings never change while the
process is running, so we do it once and reuse the same object
everywhere. Every layer that needs config calls `get_settings()`, never
reads `os.environ` directly — that keeps "where do settings come from"
answerable by one file.
"""

from functools import lru_cache

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", extra="ignore")

    environment: str = "development"

    # SQLite by default: no database server required to run this locally.
    # See db/session.py for how this same setting also drives the SQLAlchemy
    # connection-pool configuration (SQLite doesn't need one, MySQL does).
    database_url: str = "sqlite:///./dev.db"

    # In a real deployment this MUST be a long random value kept out of
    # version control (see .env.example and .gitignore) — anyone with this
    # value can forge valid access tokens. Never commit a real one.
    secret_key: str = "change-me-generate-a-long-random-value"
    access_token_expire_minutes: int = 15
    refresh_token_expire_minutes: int = 10080  # 7 days

    failed_login_max_attempts: int = 5
    failed_login_lockout_minutes: int = 15

    cors_origins: list[str] = ["*"]


@lru_cache
def get_settings() -> Settings:
    return Settings()
