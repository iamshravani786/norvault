from __future__ import annotations

import logging
from datetime import datetime, timezone
from typing import Any

from .base import AuthorityLevel, SourceAdapter, AdapterResult, ExtractedFact

logger = logging.getLogger(__name__)

class BrregUnderenheterAdapter(SourceAdapter):
    id = "brreg_underenheter"
    name = "Brønnøysund Underenheter"
    authority_level = AuthorityLevel.GOVERNMENT
    base_url = "https://data.brreg.no/enhetsregisteret/api/underenheter"
    
    async def fetch(self, org_number: str, **kwargs) -> AdapterResult:
        params = {"overordnetEnhet": org_number, "size": 100}
        headers = {
            "Accept": "application/json",
            "User-Agent": "NORVAULT/1.0 (competition-agent)"
        }
        
        response = await self._make_request(self.base_url, params=params, headers=headers)
        if not response:
            return AdapterResult(success=False, adapter_id=self.id, error_message="Failed to fetch data")
            
        if response.status_code != 200:
            return AdapterResult(success=False, adapter_id=self.id, status_code=response.status_code, error_message=f"HTTP {response.status_code}")
            
        data = response.json()
        facts = await self.extract_facts(data, org_number)
        
        return AdapterResult(
            success=True,
            adapter_id=self.id,
            raw_data=data,
            facts=facts,
            status_code=response.status_code
        )
        
    async def extract_facts(self, raw_data: dict[str, Any], org_number: str) -> list[ExtractedFact]:
        facts = []
        now = datetime.now(timezone.utc)
        url = f"{self.base_url}?overordnetEnhet={org_number}"
        
        items = raw_data.get("_embedded", {}).get("underenheter", [])
        for item in items:
            sub_org_number = item.get("organisasjonsnummer")
            if not sub_org_number:
                continue
                
            value = {
                "sub_org_number": sub_org_number,
                "name": item.get("navn"),
                "employees": item.get("antallAnsatte"),
                "address": item.get("beliggenhetsadresse"),
                "industry_code": item.get("naeringskode1", {}).get("kode")
            }
            
            facts.append(ExtractedFact(
                fact_type="corporate_relationship",
                subject=sub_org_number,
                predicate="BRANCH_OF",
                value=org_number,
                source_adapter_id=self.id,
                source_url=url,
                retrieved_at=now,
                confidence=1.0,
                identity_match_score=1.0,
                fact_category="OBSERVED"
            ))
            
            facts.append(ExtractedFact(
                fact_type="subunit_info",
                subject=sub_org_number,
                predicate="has_info",
                value=value,
                source_adapter_id=self.id,
                source_url=url,
                retrieved_at=now,
                confidence=1.0,
                identity_match_score=1.0,
                fact_category="OBSERVED"
            ))

        return facts
