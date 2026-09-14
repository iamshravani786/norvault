from __future__ import annotations
from datetime import date, datetime
from decimal import Decimal
from enum import Enum
from pydantic import BaseModel, ConfigDict

class FactStatus(str, Enum):
    CURRENT = 'CURRENT'
    RECENT = 'RECENT'
    AGING = 'AGING'
    STALE = 'STALE'
    SUPERSEDED = 'SUPERSEDED'
    CONFLICTED = 'CONFLICTED'
    UNVERIFIED = 'UNVERIFIED'

class FactCategory(str, Enum):
    OBSERVED = 'observed'
    DERIVED = 'derived'
    INFERRED = 'inferred'

class ExtractedFact(BaseModel):
    """A fact extracted from a source, before auditing."""
    fact_type: str
    subject: str  # The org number
    predicate: str  # e.g. 'has_employee_count'
    value_text: str | None = None
    value_numeric: Decimal | None = None
    value_json: dict | None = None
    source_adapter_id: str
    source_url: str
    source_date: date | None = None
    retrieved_at: datetime
    confidence: float = 1.0
    identity_match_score: float = 1.0
    fact_category: FactCategory = FactCategory.OBSERVED
    extraction_method: str = 'api_field'
    raw_extracted_value: str | None = None

class PublishedFact(BaseModel):
    """A fact that has passed auditing and is ready for display."""
    model_config = ConfigDict(from_attributes=True)
    id: int
    fact_type: str
    subject: str
    predicate: str
    display_value: str
    value_numeric: Decimal | None = None
    source_name: str
    source_url: str
    source_date: date | None = None
    retrieved_at: datetime
    freshness_status: FactStatus
    confidence: float
    identity_match_score: float
    fact_category: FactCategory
    why_this_company: str  # Identity match explanation

class EvidenceChain(BaseModel):
    """Full evidence chain from source to claim."""
    fact: PublishedFact
    source_requested: str
    timestamp: datetime
    source_url: str
    content_hash: str | None = None
    extracted_value: str | None = None
    normalized_value: str | None = None
    identity_match_reasoning: str
    final_claim: str

class EvidenceGraphNode(BaseModel):
    id: str
    node_type: str  # 'company', 'fact', 'source', 'document', 'person', etc.
    label: str
    data: dict = {}

class EvidenceGraphEdge(BaseModel):
    source: str  # node id
    target: str  # node id
    edge_type: str  # 'HAS_FACT', 'SUPPORTED_BY', etc.
    label: str = ''

class EvidenceGraph(BaseModel):
    nodes: list[EvidenceGraphNode]
    edges: list[EvidenceGraphEdge]
