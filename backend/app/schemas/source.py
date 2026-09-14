from __future__ import annotations
from datetime import datetime
from enum import Enum
from pydantic import BaseModel
from .evidence import ExtractedFact
from .identity import IdentityMatchResult

class AuthorityLevel(int, Enum):
    GOVERNMENT = 1
    COMPANY_OWNED = 2
    REPUTABLE_PUBLIC = 3
    DISCOVERY_ONLY = 4

class AdapterResult(BaseModel):
    success: bool
    adapter_id: str
    url: str
    http_status: int | None = None
    content_hash: str | None = None
    etag: str | None = None
    last_modified: str | None = None
    retrieved_at: datetime
    raw_data: dict | None = None
    error: str | None = None
    from_cache: bool = False
    facts: list[ExtractedFact] = []
    identity_match: IdentityMatchResult | None = None

class SourceInfo(BaseModel):
    adapter_id: str
    name: str
    authority_level: AuthorityLevel
    is_allowed: bool
    capabilities: list[str]
    rate_limit_per_sec: float | None = None
