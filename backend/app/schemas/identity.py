from __future__ import annotations
from pydantic import BaseModel
from typing import Literal

class IdentitySignal(BaseModel):
    signal_type: str  # 'org_number', 'legal_name', 'address', 'municipality', 'website_domain'
    expected_value: str | None = None
    found_value: str | None = None
    matches: bool
    confidence: float  # 0.0 to 1.0

class IdentityMatchResult(BaseModel):
    organization_number: str
    canonical_name: str
    candidate_name: str | None = None
    match_score: float  # 0.0 to 1.0
    matched_signals: list[IdentitySignal]
    conflicting_signals: list[IdentitySignal]
    decision: Literal['VERIFIED', 'PROBABLE', 'AMBIGUOUS', 'REJECTED']
    reasoning: str
