from __future__ import annotations
from enum import Enum
from datetime import date, datetime
from typing import Any

class FactStatus(str, Enum):
    CURRENT = "CURRENT"
    RECENT = "RECENT"
    AGING = "AGING"
    STALE = "STALE"
    UNVERIFIED = "UNVERIFIED"

class FactFreshnessConfig:
    """Per-fact-type freshness configuration."""
    def __init__(self, fact_type: str, max_fresh_days: int, aging_days: int, stale_days: int):
        self.fact_type = fact_type
        self.max_fresh_days = max_fresh_days
        self.aging_days = aging_days
        self.stale_days = stale_days

FRESHNESS_CONFIGS = {
    'legal_name': FactFreshnessConfig('legal_name', 365, 180, 730),
    'org_form': FactFreshnessConfig('org_form', 365, 180, 730),
    'registered_address': FactFreshnessConfig('registered_address', 180, 90, 365),
    'postal_address': FactFreshnessConfig('postal_address', 180, 90, 365),
    'employee_count': FactFreshnessConfig('employee_count', 90, 45, 180),
    'industry_code': FactFreshnessConfig('industry_code', 365, 180, 730),
    'board_member': FactFreshnessConfig('board_member', 180, 90, 365),
    'ceo': FactFreshnessConfig('ceo', 180, 90, 365),
    'auditor': FactFreshnessConfig('auditor', 365, 180, 730),
    'financial_statement': FactFreshnessConfig('financial_statement', 365, 180, 730),
    'vat_status': FactFreshnessConfig('vat_status', 365, 180, 730),
    'website_content': FactFreshnessConfig('website_content', 30, 14, 90),
    'homepage_url': FactFreshnessConfig('homepage_url', 180, 90, 365),
    'company_status': FactFreshnessConfig('company_status', 365, 180, 730),
    'default': FactFreshnessConfig('default', 180, 90, 365),
}

def calculate_freshness(fact_type: str, source_date: date | None, retrieved_at: datetime) -> FactStatus:
    """Calculate the freshness status of a fact."""
    base_date = source_date if source_date else retrieved_at.date()
    
    config = FRESHNESS_CONFIGS.get(fact_type, FRESHNESS_CONFIGS['default'])
    
    age_days = (datetime.now().date() - base_date).days
    
    if age_days >= config.stale_days:
        return FactStatus.STALE
    if age_days >= config.aging_days:
        return FactStatus.AGING
    if age_days >= config.max_fresh_days:
        return FactStatus.RECENT
    
    return FactStatus.CURRENT

def get_freshness_label(status: FactStatus) -> str:
    """Human-readable freshness label."""
    labels = {
        FactStatus.CURRENT: "Current",
        FactStatus.RECENT: "Recent",
        FactStatus.AGING: "Aging",
        FactStatus.STALE: "Stale",
        FactStatus.UNVERIFIED: "Unverified"
    }
    return labels.get(status, "Unknown")

def get_freshness_color(status: FactStatus) -> str:
    """Color code for UI display."""
    colors = {
        FactStatus.CURRENT: "green",
        FactStatus.RECENT: "blue",
        FactStatus.AGING: "yellow",
        FactStatus.STALE: "red",
        FactStatus.UNVERIFIED: "gray"
    }
    return colors.get(status, "gray")
