from __future__ import annotations

import logging
from datetime import datetime, timezone
from typing import Any

from .base import AuthorityLevel, SourceAdapter, AdapterResult, ExtractedFact

logger = logging.getLogger(__name__)

class BrregRegnskapAdapter(SourceAdapter):
    id = "brreg_regnskap"
    name = "Brønnøysund Regnskap"
    authority_level = AuthorityLevel.GOVERNMENT
    base_url = "https://data.brreg.no/regnskapsregisteret/regnskap"
    
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
            return AdapterResult(success=True, adapter_id=self.id, status_code=404, error_message="Accounts not found")
            
        if response.status_code != 200:
            return AdapterResult(success=False, adapter_id=self.id, status_code=response.status_code, error_message=f"HTTP {response.status_code}")
            
        data = response.json()
        facts = await self.extract_facts({"accounts": data}, org_number)
        
        return AdapterResult(
            success=True,
            adapter_id=self.id,
            raw_data={"accounts": data},
            facts=facts,
            status_code=response.status_code
        )
        
    async def extract_facts(self, raw_data: dict[str, Any], org_number: str) -> list[ExtractedFact]:
        facts = []
        now = datetime.now(timezone.utc)
        url = f"{self.base_url}/{org_number}"
        
        accounts = raw_data.get("accounts", [])
        for account in accounts:
            year = account.get("regnskapsaar")
            if not year:
                continue
                
            res = account.get("resultatregnskap", {})
            dr = res.get("driftsresultat", {})
            dk = dr.get("driftskostnader", {})
            
            eiendeler = account.get("eiendeler", {})
            om = eiendeler.get("omloepsmidler", {})
            
            ekg = account.get("egenkapitalGjeld", {})
            ek = ekg.get("egenkapital", {})
            gjeld = ekg.get("gjeld", {})
            
            financials = {
                "Revenue": dr.get("driftsinntekter", {}).get("sumDriftsinntekter"),
                "Operating profit": dr.get("driftsresultat"),
                "Net income": res.get("aarsresultat"),
                "Total assets": eiendeler.get("sumEiendeler"),
                "Equity": ek.get("sumEgenkapital"),
                "Total debt": gjeld.get("sumGjeld"),
                "Cash": om.get("bankinnskuddKontanterOgLignende"),
                "Salary costs": dk.get("lonnskostnad"),
                "Tax": res.get("skattekostnadPaaOrdinaertResultat"),
                "EBT": res.get("ordinaertResultatFoerSkattekostnad"),
            }
            
            # Extract combined fact
            facts.append(ExtractedFact(
                fact_type="financial_statement",
                subject=org_number,
                predicate="has_financial_statement",
                value={"year": year, "financials": financials},
                source_adapter_id=self.id,
                source_url=url,
                retrieved_at=now,
                confidence=1.0,
                identity_match_score=1.0,
                fact_category="OBSERVED"
            ))
            
            # Extract individual facts
            for k, v in financials.items():
                if v is not None:
                    facts.append(ExtractedFact(
                        fact_type="financial_metric",
                        subject=org_number,
                        predicate=k.lower().replace(" ", "_"),
                        value={"year": year, "amount": v},
                        source_adapter_id=self.id,
                        source_url=url,
                        retrieved_at=now,
                        confidence=1.0,
                        identity_match_score=1.0,
                        fact_category="OBSERVED"
                    ))

        return facts
