from __future__ import annotations
from datetime import datetime
from pydantic import BaseModel, ConfigDict
from .company import CompanyBrief, CompanyRoleRead, CompanyAddressRead, CompanyIndustryRead, CompanyEventRead
from .evidence import PublishedFact, EvidenceGraph
from .financial import FinancialSummary
from .identity import IdentityMatchResult

class ConflictRead(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    fact_type: str
    values: list[dict]
    resolution: str | None = None
    resolution_reasoning: str | None = None

class SourceConsulted(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    source_name: str
    source_url: str
    authority_level: int
    retrieved_at: datetime
    http_status: int | None = None
    facts_extracted: int
    content_hash: str | None = None

class ChangeDetected(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    change_type: str  # 'IDENTITY', 'LEGAL', 'PEOPLE', 'LOCATION', etc.
    field: str
    old_value: str | None = None
    new_value: str | None = None
    source: str
    confidence: float
    detected_at: datetime

class ProofPassport(BaseModel):
    """The complete company intelligence passport."""
    model_config = ConfigDict(from_attributes=True)
    # Header
    company_name: str
    organization_number: str
    organization_type: str | None = None
    status: str
    identity_confidence: float
    last_verified: datetime
    proof_score: float  # Overall evidence coverage score
    
    # Key Facts
    facts: list[PublishedFact]
    
    # Financial
    financial_summary: FinancialSummary | None = None
    
    # Roles
    roles: list[CompanyRoleRead]
    
    # Addresses
    addresses: list[CompanyAddressRead]
    
    # Industries
    industries: list[CompanyIndustryRead]
    
    # Corporate structure
    parent: CompanyBrief | None = None
    subsidiaries: list[CompanyBrief]
    
    # Identity
    identity_match: IdentityMatchResult
    
    # Conflicts
    conflicts: list[ConflictRead]
    
    # Timeline
    timeline: list[CompanyEventRead]
    
    # Evidence graph
    evidence_graph: EvidenceGraph
    
    # Source ledger
    sources_consulted: list[SourceConsulted]
    
    # Change radar
    changes_detected: list[ChangeDetected]
    
    # Run metadata
    run_id: str
    retrieval_time_sec: float
    requests_made: int
    cache_hits: int
