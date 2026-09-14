from __future__ import annotations
from datetime import datetime
from decimal import Decimal
from pydantic import BaseModel

class SourceBudget(BaseModel):
    source_name: str
    requests_used: int
    requests_saved_by_cache: int
    cost_estimate: Decimal

class BudgetStatus(BaseModel):
    requests_used: int
    requests_remaining: int
    requests_saved_by_cache: int
    cache_hit_rate: float
    external_cost_estimate: Decimal
    cost_remaining: Decimal
    budget_utilization_pct: float
    per_source_breakdown: list[SourceBudget]

class RunStats(BaseModel):
    run_id: str
    started_at: datetime
    completed_at: datetime | None = None
    duration_sec: float | None = None
    requests_made: int
    cache_hits: int
    facts_found: int
    facts_rejected: int
    facts_published: int
    conflicts_detected: int
    audit_failures: int
    status: str
