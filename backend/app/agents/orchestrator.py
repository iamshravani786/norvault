from __future__ import annotations

import logging
from typing import List

from app.services.pipeline import CompanyPipeline
from app.schemas.passport import ProofPassport

logger = logging.getLogger(__name__)

class AgentOrchestrator:
    """Coordinates specialized agents for company intelligence gathering."""
    
    def __init__(self, db, http_client, cache_manager, budget_manager):
        self.pipeline = CompanyPipeline(db, http_client, cache_manager, budget_manager)
    
    async def investigate_company(self, org_number: str, force_refresh: bool = False) -> ProofPassport:
        """Run full investigation pipeline."""
        logger.info(f"Agent orchestrating investigation for {org_number}")
        return await self.pipeline.run(org_number, force_refresh)
    
    async def batch_investigate(self, org_numbers: list[str]) -> list[ProofPassport]:
        """Investigate multiple companies sequentially (to manage budget)."""
        logger.info(f"Agent orchestrating batch investigation for {len(org_numbers)} companies")
        results = []
        for org in org_numbers:
            try:
                res = await self.investigate_company(org)
                if res:
                    results.append(res)
            except Exception as e:
                logger.error(f"Failed to investigate {org}: {e}")
        return results
