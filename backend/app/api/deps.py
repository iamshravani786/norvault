"""FastAPI dependency injection — singletons and factories."""

from __future__ import annotations

from collections.abc import AsyncGenerator
from decimal import Decimal

import httpx
from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.config import get_settings
from app.core.budget_manager import BudgetManager
from app.core.cache_manager import CacheManager
from app.database import get_db as _get_db
from app.services.pipeline import CompanyPipeline

# ---------------------------------------------------------------------------
# Module-level singletons (created once, reused across requests)
# ---------------------------------------------------------------------------
_settings = get_settings()
_budget_manager = BudgetManager(
    max_requests=_settings.max_requests,
    max_cost=_settings.max_cost,
)
_cache_manager = CacheManager(default_ttl=3600)
_http_client = httpx.AsyncClient(
    timeout=httpx.Timeout(_settings.http_timeout_sec),
    follow_redirects=True,
    limits=httpx.Limits(max_connections=50, max_keepalive_connections=20),
)


# ---------------------------------------------------------------------------
# Dependency functions
# ---------------------------------------------------------------------------


async def get_db() -> AsyncGenerator[AsyncSession, None]:
    """Yield an async database session."""
    async for session in _get_db():
        yield session


def get_budget_manager() -> BudgetManager:
    """Return the global budget manager singleton."""
    return _budget_manager


def get_cache_manager() -> CacheManager:
    """Return the global cache manager singleton."""
    return _cache_manager


def get_http_client() -> httpx.AsyncClient:
    """Return the shared HTTP client singleton."""
    return _http_client


def get_pipeline(
    db: AsyncSession = Depends(get_db),
    http_client: httpx.AsyncClient = Depends(get_http_client),
    cache_manager: CacheManager = Depends(get_cache_manager),
    budget_manager: BudgetManager = Depends(get_budget_manager),
) -> CompanyPipeline:
    """Build a CompanyPipeline with all dependencies injected."""
    return CompanyPipeline(db, http_client, cache_manager, budget_manager)
