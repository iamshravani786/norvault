from __future__ import annotations
import pytest
from app.core.contradictions import ContradictionEngine, Resolution, FactInfo

def test_no_contradiction():
    engine = ContradictionEngine()
    f1 = FactInfo(value="A", authority=1, period="2023")
    f2 = FactInfo(value="A", authority=1, period="2023")
    assert engine.detect(f1, f2) is None

def test_contradiction_detected():
    engine = ContradictionEngine()
    f1 = FactInfo(value="A", authority=1, period="2023")
    f2 = FactInfo(value="B", authority=1, period="2023")
    assert engine.detect(f1, f2) is not None

def test_different_reporting_period():
    engine = ContradictionEngine()
    f1 = FactInfo(value="100", authority=1, period="2022")
    f2 = FactInfo(value="200", authority=1, period="2023")
    assert engine.resolve(f1, f2) == Resolution.DIFFERENT_REPORTING_PERIOD

def test_latest_authoritative():
    engine = ContradictionEngine()
    f1 = FactInfo(value="100", authority=1, period="2023")
    f2 = FactInfo(value="200", authority=2, period="2023")
    assert engine.resolve(f1, f2) == Resolution.LATEST_AUTHORITATIVE

def test_unresolved():
    engine = ContradictionEngine()
    f1 = FactInfo(value="100", authority=1, period="2023")
    f2 = FactInfo(value="200", authority=1, period="2023")
    assert engine.resolve(f1, f2) == Resolution.UNRESOLVED

def test_different_entity():
    engine = ContradictionEngine()
    f1 = FactInfo(value="100", authority=1, period="2023", entity_id="1")
    f2 = FactInfo(value="200", authority=1, period="2023", entity_id="2")
    assert engine.resolve(f1, f2) == Resolution.DIFFERENT_ENTITY
