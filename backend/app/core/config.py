"""Application configuration.

All settings come from `backend/.env` (or the real environment). We build the
database and Redis URLs from their parts (host, port, user, ...) so that running
in Docker vs locally only needs a different *host* — no duplicated URLs or
secrets. In Docker, compose overrides `POSTGRES_HOST`/`REDIS_HOST` with the
service names; locally they stay `localhost`.

Access the settings singleton via `get_settings()`.
"""

from functools import lru_cache

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """Typed application settings sourced from the environment."""

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=False,
        extra="ignore",
    )

    # ---------- App ----------
    environment: str = "development"
    log_level: str = "INFO"
    # Comma-separated list of allowed CORS origins (parsed via `cors_origins`).
    backend_cors_origins: str = "http://localhost:3000"

    # ---------- Database (URL built from these parts) ----------
    postgres_user: str = "engagedash"
    postgres_password: str = "change-me"
    postgres_db: str = "engagedash"
    postgres_host: str = "localhost"
    postgres_port: int = 5432

    # ---------- Redis ----------
    redis_host: str = "localhost"
    redis_port: int = 6379
    # Empty locally; managed Redis (e.g. Railway) requires a password.
    redis_password: str = ""

    # ---------- JWT / Auth ----------
    jwt_secret_key: str = "change-me-to-a-long-random-string"
    jwt_algorithm: str = "HS256"
    access_token_expire_minutes: int = 30
    refresh_token_expire_days: int = 7

    # ---------- AI (DeepSeek via NVIDIA, OpenAI-compatible) ----------
    ai_base_url: str = "https://integrate.api.nvidia.com/v1"
    ai_api_key: str = ""
    ai_model: str = "deepseek-ai/deepseek-v4-flash"

    # ---------- Cache ----------
    dashboard_cache_ttl_seconds: int = 120

    @property
    def database_url(self) -> str:
        """Full SQLAlchemy database URL, built from the parts above."""
        return (
            f"postgresql+psycopg://{self.postgres_user}:{self.postgres_password}"
            f"@{self.postgres_host}:{self.postgres_port}/{self.postgres_db}"
        )

    @property
    def redis_url(self) -> str:
        """Full Redis URL, built from the parts above (with a password if set)."""
        auth = f":{self.redis_password}@" if self.redis_password else ""
        return f"redis://{auth}{self.redis_host}:{self.redis_port}/0"

    @property
    def cors_origins(self) -> list[str]:
        """Turn the comma-separated CORS string into a list of origins."""
        return [origin.strip() for origin in self.backend_cors_origins.split(",") if origin.strip()]

    @property
    def is_production(self) -> bool:
        """True when running in the production environment."""
        return self.environment.lower() == "production"


@lru_cache
def get_settings() -> Settings:
    """Return the cached `Settings` singleton."""
    return Settings()
