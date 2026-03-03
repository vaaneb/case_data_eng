from functools import lru_cache
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    # Basic app info
    APP_NAME: str = "Case Data Eng - API"
    APP_ENV: str = "dev"  # dev | staging | prod

    # Database
    DATABASE_URL: str

    # Logging
    LOG_LEVEL: str = "INFO"  # DEBUG | INFO | WARNING | ERROR | CRITICAL
    LOG_SQL_QUERIES: bool = False  # Set to False to disable SQL query logging

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore",
    )


@lru_cache
def get_settings() -> Settings:
    """
    Cached so we don't recreate Settings on every import.
    """
    return Settings()