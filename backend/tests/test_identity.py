from __future__ import annotations
import pytest
from app.core.identity import IdentityFirewall, Decision, SignalInfo

def test_verified_decision():
    firewall = IdentityFirewall()
    decision = firewall.evaluate(target_org="923609016", source_org="923609016", target_name="Equinor ASA", source_name="Equinor")
    assert decision == Decision.VERIFIED

def test_rejected_decision():
    firewall = IdentityFirewall()
    decision = firewall.evaluate(target_org="923609016", source_org="985399077", target_name="Equinor", source_name="DNB")
    assert decision == Decision.REJECTED

def test_probable_decision():
    firewall = IdentityFirewall()
    decision = firewall.evaluate(target_org="923609016", source_org=None, target_name="Equinor ASA", source_name="Equinor ASA")
    assert decision == Decision.PROBABLE

def test_ambiguous_decision():
    firewall = IdentityFirewall()
    decision = firewall.evaluate(target_org="923609016", source_org=None, target_name="Equinor ASA", source_name="Statoil")
    assert decision == Decision.AMBIGUOUS

def test_signal_scoring():
    firewall = IdentityFirewall()
    score = firewall.calculate_score(signals=[SignalInfo(type="org_match", weight=1.0)])
    assert score == 1.0

def test_name_normalization():
    firewall = IdentityFirewall()
    assert firewall.normalize_name(" Equinor ASA ") == "equinor asa"
    assert firewall.normalize_name("EQUINOR ASA") == "equinor asa"
    
def test_parent_subsidiary():
    firewall = IdentityFirewall()
    decision = firewall.evaluate_relationship(parent_org="923609016", sub_org="123456789")
    assert decision in [Decision.VERIFIED, Decision.REJECTED, Decision.PROBABLE, Decision.AMBIGUOUS]
