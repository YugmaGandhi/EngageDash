"""Application configuration.

All settings are read from environment variables (or a local `.env` file when running
outside Docker). Access the singleton via `get_settings()`.
"""

from functools import lru_cache

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """Typed application settings sourced from the environment."""

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=False,
        # The root .env also holds vars for other services (Postgres, frontend);
        # ignore anything this model doesn't declare.
        extra="ignore",
    )

    # ---------- App ----------
    environment: str = "development"
    log_level: str = "INFO"
    # Comma-separated list of allowed CORS origins (parsed via `cors_origins`).
    backend_cors_origins: str = "http://localhost:3000"

    # ---------- Database ----------
    database_url: str = "postgresql+psycopg://engagedash:change-me@localhost:5432/engagedash"

    # ---------- Redis ----------
    redis_url: str = "redis://localhost:6379/0"

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
