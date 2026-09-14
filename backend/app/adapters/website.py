from __future__ import annotations

import logging
from datetime import datetime, timezone
from typing import Any

from bs4 import BeautifulSoup
import httpx

from .base import AuthorityLevel, SourceAdapter, AdapterResult, ExtractedFact

logger = logging.getLogger(__name__)

class WebsiteAdapter(SourceAdapter):
    id = "company_website"
    name = "Company Website"
    authority_level = AuthorityLevel.COMPANY_OWNED
    
    async def fetch(self, org_number: str, **kwargs) -> AdapterResult:
        website_url = kwargs.get("homepage_url")
        if not website_url or not (website_url.startswith("http://") or website_url.startswith("https://")):
            return AdapterResult(success=False, adapter_id=self.id, error_message="Invalid or missing homepage_url")
            
        headers = {
            "User-Agent": "NORVAULT/1.0 (competition-agent)"
        }
        
        try:
            # Bypass base `_make_request` caching/budget for website maybe, or use a custom client call
            # with strict timeouts and size limits as requested.
            async with httpx.AsyncClient(timeout=10.0) as client:
                response = await client.get(website_url, headers=headers)
                
            if response.status_code != 200:
                return AdapterResult(success=False, adapter_id=self.id, status_code=response.status_code, error_message=f"HTTP {response.status_code}")
                
            content = response.content
            if len(content) > 1024 * 1024:
                content = content[:1024 * 1024]
                
            raw_data = {"html": content.decode("utf-8", errors="ignore"), "url": website_url}
            facts = await self.extract_facts(raw_data, org_number)
            
            return AdapterResult(
                success=True,
                adapter_id=self.id,
                raw_data=raw_data,
                facts=facts,
                status_code=response.status_code
            )
            
        except Exception as e:
            logger.error(f"Failed to fetch website {website_url}: {e}")
            return AdapterResult(success=False, adapter_id=self.id, error_message=str(e))
        
    async def extract_facts(self, raw_data: dict[str, Any], org_number: str) -> list[ExtractedFact]:
        facts = []
        now = datetime.now(timezone.utc)
        html = raw_data.get("html", "")
        url = raw_data.get("url", "")
        
        if not html:
            return facts
            
        soup = BeautifulSoup(html, "html.parser")
        
        title = soup.title.string.strip() if soup.title and soup.title.string else None
        
        description = None
        meta_desc = soup.find("meta", attrs={"name": "description"})
        if meta_desc and meta_desc.get("content"):
            description = meta_desc["content"].strip()
            
        # Extract and sanitize content
        for script in soup(["script", "style", "noscript", "meta"]):
            script.decompose()
            
        text = soup.get_text(separator=" ", strip=True)
        content_summary = text[:500] if text else None
        
        if title:
            facts.append(ExtractedFact(
                fact_type="website_metadata",
                subject=org_number,
                predicate="website_title",
                value=title,
                source_adapter_id=self.id,
                source_url=url,
                retrieved_at=now,
                confidence=0.8,
                identity_match_score=0.9,
                fact_category="OBSERVED"
            ))
            
        if description:
            facts.append(ExtractedFact(
                fact_type="website_metadata",
                subject=org_number,
                predicate="website_description",
                value=description,
                source_adapter_id=self.id,
                source_url=url,
                retrieved_at=now,
                confidence=0.8,
                identity_match_score=0.9,
                fact_category="OBSERVED"
            ))
            
        if content_summary:
            facts.append(ExtractedFact(
                fact_type="website_content",
                subject=org_number,
                predicate="website_content",
                value=content_summary,
                source_adapter_id=self.id,
                source_url=url,
                retrieved_at=now,
                confidence=0.8,
                identity_match_score=0.9,
                fact_category="OBSERVED"
            ))

        return facts
