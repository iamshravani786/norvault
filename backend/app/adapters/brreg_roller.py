from __future__ import annotations

import logging
from datetime import datetime, timezone
from typing import Any

from .base import AuthorityLevel, SourceAdapter, AdapterResult, ExtractedFact

logger = logging.getLogger(__name__)

class BrregRollerAdapter(SourceAdapter):
    id = "brreg_roller"
    name = "Brønnøysund Roller"
    authority_level = AuthorityLevel.GOVERNMENT
    base_url = "https://data.brreg.no/enhetsregisteret/api/enheter"
    
    async def fetch(self, org_number: str, **kwargs) -> AdapterResult:
        url = f"{self.base_url}/{org_number}/roller"
        headers = {
            "Accept": "application/json",
            "User-Agent": "NORVAULT/1.0 (competition-agent)"
        }
        
        response = await self._make_request(url, headers=headers)
        if not response:
            return AdapterResult(success=False, adapter_id=self.id, error_message="Failed to fetch data")
            
        if response.status_code == 404:
            return AdapterResult(success=True, adapter_id=self.id, status_code=404, error_message="Roles not found")
            
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
        url = f"{self.base_url}/{org_number}/roller"
        
        rollegrupper = raw_data.get("rollegrupper", [])
        for gruppe in rollegrupper:
            sist_endret = gruppe.get("sistEndret")
            roller = gruppe.get("roller", [])
            for rolle in roller:
                type_kode = rolle.get("type", {}).get("kode")
                
                person = rolle.get("person")
                enhet = rolle.get("enhet")
                
                value = {
                    "role_type": type_kode,
                    "last_changed": sist_endret
                }
                
                if person:
                    navn = person.get("navn", {})
                    full_name = " ".join(filter(None, [navn.get("fornavn"), navn.get("mellomnavn"), navn.get("etternavn")]))
                    value["person_name"] = full_name
                elif enhet:
                    value["entity_org_number"] = enhet.get("organisasjonsnummer")
                    value["entity_name"] = enhet.get("navn")
                    
                facts.append(ExtractedFact(
                    fact_type="role",
                    subject=org_number,
                    predicate="has_role",
                    value=value,
                    source_adapter_id=self.id,
                    source_url=url,
                    source_date=sist_endret,
                    retrieved_at=now,
                    confidence=1.0,
                    identity_match_score=1.0,
                    fact_category="OBSERVED"
                ))

        return facts
