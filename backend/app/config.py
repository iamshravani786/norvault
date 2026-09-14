"""Application configuration loaded from environment variables."""

from __future__ import annotations

from decimal import Decimal
from functools import lru_cache

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """NORVAULT application settings.

    All values are loaded from environment variables (or a .env file).
    """

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=False,
    )

    # Database
    database_url: str = "postgresql+asyncpg://norvault:norvault@localhost:5432/norvault"

    # Brønnøysundregistrene
    brreg_base_url: str = "https://data.brreg.no"
    brreg_enheter_url: str = ""  # Computed in model_post_init
    brreg_underenheter_url: str = ""
    brreg_regnskap_url: str = ""

    # Request budget
    max_requests: int = 2000
    max_cost: Decimal = Decimal("10.00")

    # Rate limiting
    brreg_rate_limit_per_sec: float = 10.0
    website_rate_limit_per_sec: float = 5.0

    # HTTP client
    http_timeout_sec: float = 30.0
    http_max_retries: int = 3

    # Logging
    log_level: str = "INFO"

    # Server
    backend_host: str = "0.0.0.0"
    backend_port: int = 8000

    def model_post_init(self, __context: object) -> None:
        """Compute derived URLs after initialization."""
        base = self.brreg_base_url.rstrip("/")
        if not self.brreg_enheter_url:
            self.brreg_enheter_url = f"{base}/enhetsregisteret/api"
        if not self.brreg_underenheter_url:
            self.brreg_underenheter_url = f"{base}/enhetsregisteret/api"
        if not self.brreg_regnskap_url:
            self.brreg_regnskap_url = f"{base}/regnskapsregisteret/regnskap"


@lru_cache
def get_settings() -> Settings:
    """Return cached application settings singleton."""
    return Settings()
