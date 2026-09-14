from __future__ import annotations
import pytest
from datetime import datetime, timedelta, timezone
from app.core.temporal import TemporalTruthEngine, TemporalStatus, Fact

def test_current_status():
    engine = TemporalTruthEngine()
    fact = Fact(retrieved_at=datetime.now(timezone.utc), source_date=datetime.now(timezone.utc))
    assert engine.evaluate(fact) == TemporalStatus.CURRENT

def test_aging_status():
    engine = TemporalTruthEngine()
    fact = Fact(retrieved_at=datetime.now(timezone.utc) - timedelta(days=180), source_date=datetime.now(timezone.utc) - timedelta(days=180))
    assert engine.evaluate(fact) == TemporalStatus.AGING

def test_stale_status():
    engine = TemporalTruthEngine()
    fact = Fact(retrieved_at=datetime.now(timezone.utc) - timedelta(days=500), source_date=datetime.now(timezone.utc) - timedelta(days=500))
    assert engine.evaluate(fact) == TemporalStatus.STALE

def test_fact_type_thresholds():
    engine = TemporalTruthEngine()
    financial_fact = Fact(type="financial", source_date=datetime.now(timezone.utc) - timedelta(days=400))
    basic_fact = Fact(type="basic_info", source_date=datetime.now(timezone.utc) - timedelta(days=400))
    assert engine.evaluate(financial_fact) == TemporalStatus.STALE
    assert engine.evaluate(basic_fact) == TemporalStatus.AGING

def test_source_date_vs_retrieved_at():
    engine = TemporalTruthEngine()
    fact = Fact(retrieved_at=datetime.now(timezone.utc), source_date=datetime.now(timezone.utc) - timedelta(days=500))
    assert engine.evaluate(fact) == TemporalStatus.STALE

def test_none_dates():
    engine = TemporalTruthEngine()
    fact = Fact(retrieved_at=None, source_date=None)
    assert engine.evaluate(fact) == TemporalStatus.STALE
