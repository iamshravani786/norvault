from __future__ import annotations

import logging
from typing import Dict, Type

import httpx

from app.core.cache_manager import CacheManager
from app.core.budget_manager import BudgetManager

from .base import SourceAdapter
from .brreg_enheter import BrregEnheterAdapter
from .brreg_roller import BrregRollerAdapter
from .brreg_regnskap import BrregRegnskapAdapter
from .brreg_underenheter import BrregUnderenheterAdapter
from .website import WebsiteAdapter

logger = logging.getLogger(__name__)

ADAPTER_CLASSES: Dict[str, Type[SourceAdapter]] = {
    "brreg_enheter": BrregEnheterAdapter,
    "brreg_roller": BrregRollerAdapter,
    "brreg_regnskap": BrregRegnskapAdapter,
    "brreg_underenheter": BrregUnderenheterAdapter,
    "company_website": WebsiteAdapter,
}

async def seed_default_sources() -> None:
    """Seed the database with default source adapter entries."""
    # In a real implementation, this would insert/update source records in the database.
    logger.info("Seeding default sources...")
    sources = [
        {"id": "brreg_enheter", "name": "Brønnøysund Enhetsregisteret", "authority_level": 1},
        {"id": "brreg_roller", "name": "Brønnøysund Roller", "authority_level": 1},
        {"id": "brreg_regnskap", "name": "Brønnøysund Regnskap", "authority_level": 1},
        {"id": "brreg_underenheter", "name": "Brønnøysund Underenheter", "authority_level": 1},
        {"id": "company_website", "name": "Company Website", "authority_level": 2},
    ]
    for s in sources:
        logger.debug(f"Seeded source: {s['id']}")
    logger.info("Finished seeding sources.")

def get_adapter(
    adapter_id: str, 
    http_client: httpx.AsyncClient, 
    cache_manager: CacheManager, 
    budget_manager: BudgetManager
) -> SourceAdapter:
    """Factory function to get an adapter by ID."""
    adapter_cls = ADAPTER_CLASSES.get(adapter_id)
    if not adapter_cls:
        raise ValueError(f"Adapter not found: {adapter_id}")
    return adapter_cls(http_client, cache_manager, budget_manager)

def get_all_adapters(
    http_client: httpx.AsyncClient, 
    cache_manager: CacheManager, 
    budget_manager: BudgetManager
) -> list[SourceAdapter]:
    """Get all allowed adapters."""
    adapters = []
    for adapter_id in ADAPTER_CLASSES:
        adapter = get_adapter(adapter_id, http_client, cache_manager, budget_manager)
        if adapter.allowed:
            adapters.append(adapter)
    return adapters
