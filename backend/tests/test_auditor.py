from __future__ import annotations
import pytest
from app.core.auditor import AdversarialAuditor, RiskLevel, FactRisk

def test_low_risk():
    auditor = AdversarialAuditor()
    risk = auditor.assess(identity_status="VERIFIED", source_type="primary", is_contradicted=False)
    assert risk == RiskLevel.LOW

def test_medium_risk():
    auditor = AdversarialAuditor()
    risk = auditor.assess(identity_status="PROBABLE", source_type="secondary", is_contradicted=False)
    assert risk == RiskLevel.MEDIUM

def test_high_risk():
    auditor = AdversarialAuditor()
    risk = auditor.assess(identity_status="VERIFIED", source_type="primary", is_contradicted=True)
    assert risk == RiskLevel.HIGH

def test_critical_risk():
    auditor = AdversarialAuditor()
    risk = auditor.assess(identity_status="AMBIGUOUS", source_type="unverified", is_contradicted=True)
    assert risk == RiskLevel.CRITICAL

def test_financial_facts():
    auditor = AdversarialAuditor()
    risk = auditor.assess(fact_type="financial", identity_status="PROBABLE")
    assert risk >= RiskLevel.HIGH

def test_publish_decision():
    auditor = AdversarialAuditor()
    assert auditor.should_publish(RiskLevel.LOW) is True
    assert auditor.should_publish(RiskLevel.CRITICAL) is False
