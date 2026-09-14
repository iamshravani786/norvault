from __future__ import annotations

import logging
from datetime import datetime, timezone
from typing import Any

from .base import AuthorityLevel, SourceAdapter, AdapterResult, ExtractedFact

logger = logging.getLogger(__name__)

class BrregEnheterAdapter(SourceAdapter):
    id = "brreg_enheter"
    name = "Brønnøysund Enhetsregisteret"
    authority_level = AuthorityLevel.GOVERNMENT
    base_url = "https://data.brreg.no/enhetsregisteret/api/enheter"
    
    async def fetch(self, org_number: str, **kwargs) -> AdapterResult:
        url = f"{self.base_url}/{org_number}"
        headers = {
            "Accept": "application/json",
            "User-Agent": "NORVAULT/1.0 (competition-agent)"
        }
        
        response = await self._make_request(url, headers=headers)
        if not response:
            return AdapterResult(success=False, adapter_id=self.id, error_message="Failed to fetch data")
            
        if response.status_code == 404:
            return AdapterResult(success=True, adapter_id=self.id, status_code=404, error_message="Company not found")
            
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
        url = f"{self.base_url}/{org_number}"
        source_date = raw_data.get("registreringsdatoEnhetsregisteret")
        
        def add_fact(predicate: str, value: Any, f_type: str = "entity_attribute"):
            if value is not None:
                facts.append(ExtractedFact(
                    fact_type=f_type,
                    subject=org_number,
                    predicate=predicate,
                    value=value,
                    source_adapter_id=self.id,
                    source_url=url,
                    source_date=source_date,
                    retrieved_at=now,
                    confidence=1.0,
                    identity_match_score=1.0,
                    fact_category="OBSERVED"
                ))

        add_fact("legal_name", raw_data.get("navn"))
        
        org_form = raw_data.get("organisasjonsform")
        if org_form:
            add_fact("org_form", org_form.get("kode"))
            
        add_fact("registered_address", raw_data.get("forretningsadresse"))
        add_fact("postal_address", raw_data.get("postadresse"))
        
        for i in range(1, 4):
            nkode = raw_data.get(f"naeringskode{i}")
            if nkode:
                add_fact(f"industry_code_{i}", nkode.get("kode"))
                
        add_fact("employee_count", raw_data.get("antallAnsatte"))
        add_fact("registration_date", raw_data.get("registreringsdatoEnhetsregisteret"))
        add_fact("foundation_date", raw_data.get("stiftelsesdato"))
        
        status = "active"
        if raw_data.get("konkurs"):
            status = "bankrupt"
        elif raw_data.get("underAvvikling") or raw_data.get("underTvangsavviklingEllerTvangsopplosning"):
            status = "dissolved"
        add_fact("company_status", status)
        
        add_fact("vat_status", raw_data.get("registrertIMvaregisteret"))
        add_fact("business_register_status", raw_data.get("registrertIForetaksregisteret"))
        add_fact("latest_accounts_year", raw_data.get("sisteInnsendteAarsregnskap"))
        add_fact("homepage_url", raw_data.get("hjemmeside"))

        return facts
