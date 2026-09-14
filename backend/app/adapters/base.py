from __future__ import annotations

import asyncio
import logging
from abc import ABC, abstractmethod
from datetime import datetime, timezone
from enum import IntEnum
from typing import Any

import httpx
from pydantic import BaseModel, Field

from app.core.cache_manager import CacheManager
from app.core.budget_manager import BudgetManager

logger = logging.getLogger(__name__)


class AuthorityLevel(IntEnum):
    GOVERNMENT = 1
    COMPANY_OWNED = 2
    REPUTABLE_PUBLIC = 3
    DISCOVERY_ONLY = 4


class ExtractedFact(BaseModel):
    """A fact extracted from a source, before auditing."""

    fact_type: str
    subject: str
    predicate: str
    value: Any
    source_adapter_id: str
    source_url: str
    source_date: str | None = None
    retrieved_at: datetime
    confidence: float = 1.0
    identity_match_score: float = 1.0
    fact_category: str = "OBSERVED"
    extraction_method: str = "api_field"
    raw_extracted_value: str | None = None


class AdapterResult(BaseModel):
    """Result of a source adapter fetch operation."""

    success: bool
    adapter_id: str
    raw_data: dict[str, Any] | None = None
    facts: list[ExtractedFact] = Field(default_factory=list)
    error_message: str | None = None
    status_code: int | None = None
    url: str | None = None
    content_hash: str | None = None
    retrieved_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    from_cache: bool = False


class SourceAdapter(ABC):
    """Abstract base class for all source adapters.

    Provides built-in budget checking, caching, rate limiting,
    and exponential-backoff retries for subclasses.
    """

    id: str = ""
    name: str = ""
    authority_level: AuthorityLevel = AuthorityLevel.GOVERNMENT
    allowed: bool = True
    capabilities: list[str] = []
    rate_limit_per_sec: float = 10.0
    base_url: str = ""

    def __init__(
        self,
        http_client: httpx.AsyncClient,
        cache_manager: CacheManager,
        budget_manager: BudgetManager,
    ):
        self._client = http_client
        self._cache = cache_manager
        self._budget = budget_manager

    @abstractmethod
    async def fetch(self, org_number: str, **kwargs: Any) -> AdapterResult:
        """Fetch raw data from the source."""

    @abstractmethod
    async def extract_facts(
        self, raw_data: dict[str, Any], org_number: str
    ) -> list[ExtractedFact]:
        """Extract structured facts from raw source data."""

    async def _make_request(
        self,
        url: str,
        params: dict[str, Any] | None = None,
        headers: dict[str, Any] | None = None,
    ) -> httpx.Response | None:
        """Make an HTTP request with budget checking, caching, and retries."""
        logger.debug("[%s] Preparing request to %s", self.id, url)

        # 1. Check budget
        if not await self._budget.can_request(self.id):
            logger.warning("[%s] Budget exceeded, skipping %s", self.id, url)
            return None

        # 2. Check result cache
        cache_key = self._cache.make_key(self.id, url, **(params or {}))
        cached = self._cache.get(cache_key)
        
        if cached and cached.is_negative:
            logger.debug("[%s] Negative cache hit for %s", self.id, url)
            await self._budget.record_request(self.id, cached=True)
            return httpx.Response(404, request=httpx.Request("GET", url))
            
        if cached and cached.value is not None:
            logger.debug("[%s] Cache hit for %s", self.id, url)
            await self._budget.record_request(self.id, cached=True)
            return httpx.Response(200, json=cached.value, request=httpx.Request("GET", url))

        # 3. Prepare conditional request headers
        request_headers = dict(headers or {})
        stored_etag = self._cache.get_etag(cache_key)
        if stored_etag:
            request_headers["If-None-Match"] = stored_etag
        stored_lm = self._cache.get_last_modified(cache_key)
        if stored_lm:
            request_headers["If-Modified-Since"] = stored_lm

        # 4. Make request with exponential backoff
        max_retries = 3
        base_delay = 1.0

        for attempt in range(max_retries):
            try:
                logger.debug("[%s] Attempt %d for %s", self.id, attempt + 1, url)
                response = await self._client.get(
                    url,
                    params=params,
                    headers=request_headers,
                    timeout=30.0,
                )
                
                if response.status_code == 304 and cached and cached.value is not None:
                    await self._budget.record_request(self.id, cached=True)
                    return httpx.Response(200, json=cached.value, request=response.request)

                if response.status_code in (429, 500, 502, 503, 504):
                    logger.warning(
                        "[%s] HTTP %d for %s — retrying",
                        self.id,
                        response.status_code,
                        url,
                    )
                    await asyncio.sleep(base_delay * (2**attempt))
                    continue

                # Record in budget manager
                await self._budget.record_request(self.id, cached=False)

                # Cache successful responses
                if response.status_code == 200:
                    try:
                        data = response.json()
                        self._cache.put(
                            cache_key,
                            data,
                            etag=response.headers.get("etag"),
                            last_modified=response.headers.get("last-modified"),
                        )
                    except Exception:
                        pass  # Non-JSON responses are not cached

                # Negative cache for 404s
                if response.status_code == 404:
                    self._cache.put(cache_key, None, is_negative=True, ttl=600)

                return response

            except httpx.RequestError as exc:
                logger.error("[%s] Request error: %s", self.id, exc)
                if attempt == max_retries - 1:
                    return None
                await asyncio.sleep(base_delay * (2**attempt))

        return None
