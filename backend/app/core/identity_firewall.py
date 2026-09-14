from __future__ import annotations
import re
from typing import Any

class IdentitySignal:
    def __init__(self, field: str, match_score: float, status: str):
        self.field = field
        self.match_score = match_score
        self.status = status

class IdentityMatchResult:
    def __init__(self, requested_org_number: str, decision: str, confidence: float, signals: list[IdentitySignal]):
        self.requested_org_number = requested_org_number
        self.decision = decision
        self.confidence = confidence
        self.signals = signals

class IdentityFirewall:
    def resolve(
        self,
        requested_org_number: str,
        source_data: dict[str, Any],
        source_adapter_id: str,
        canonical_company: dict[str, Any] | None = None,
    ) -> IdentityMatchResult:
        """
        Determine if source_data describes the requested company.
        
        Decision logic:
        - If source_data contains org_number and it matches → VERIFIED (1.0)
        - If source_data contains org_number and it differs → REJECTED (0.0)
        - If no org_number in source but name matches canonical → PROBABLE (0.7-0.9)
        - If no org_number and no name match → AMBIGUOUS (0.3-0.5)
        - If explicit conflict (different org_number) → REJECTED (0.0)
        """
        signals = []
        
        # Org Number Signal
        found_org = str(source_data.get('org_number')) if source_data.get('org_number') else None
        org_signal = self._check_org_number_signal(requested_org_number, found_org)
        signals.append(org_signal)
        
        # Name Signal
        if canonical_company and canonical_company.get('name') and source_data.get('name'):
            name_signal = self._check_name_signal(canonical_company['name'], source_data['name'])
            signals.append(name_signal)
            
        # Address Signal
        if canonical_company and canonical_company.get('address') and source_data.get('address'):
            addr_signal = self._check_address_signal(canonical_company['address'], source_data['address'])
            signals.append(addr_signal)
            
        decision, confidence, reason = self._compute_decision(signals)
        
        return IdentityMatchResult(
            requested_org_number=requested_org_number,
            decision=decision,
            confidence=confidence,
            signals=signals
        )
        
    def _check_org_number_signal(self, requested: str, found: str | None) -> IdentitySignal:
        if not found:
            return IdentitySignal('org_number', 0.0, 'MISSING')
            
        clean_requested = re.sub(r'\D', '', requested)
        clean_found = re.sub(r'\D', '', found)
        
        if clean_requested == clean_found:
            return IdentitySignal('org_number', 1.0, 'MATCH')
        return IdentitySignal('org_number', 0.0, 'MISMATCH')
        
    def _check_name_signal(self, canonical_name: str, candidate_name: str) -> IdentitySignal:
        c1 = re.sub(r'[^a-z0-9]', '', canonical_name.lower())
        c2 = re.sub(r'[^a-z0-9]', '', candidate_name.lower())
        
        if not c1 or not c2:
            return IdentitySignal('name', 0.0, 'MISSING')
            
        if c1 == c2:
            return IdentitySignal('name', 1.0, 'EXACT_MATCH')
            
        if c1 in c2 or c2 in c1:
            return IdentitySignal('name', 0.8, 'PARTIAL_MATCH')
            
        return IdentitySignal('name', 0.0, 'NO_MATCH')
        
    def _check_address_signal(self, canonical_addr: dict[str, Any] | None, candidate_addr: dict[str, Any] | None) -> IdentitySignal:
        if not canonical_addr or not candidate_addr:
            return IdentitySignal('address', 0.0, 'MISSING')
            
        c_zip = canonical_addr.get('zipcode', '')
        cand_zip = candidate_addr.get('zipcode', '')
        
        if c_zip and cand_zip and c_zip == cand_zip:
            return IdentitySignal('address', 0.7, 'ZIP_MATCH')
            
        return IdentitySignal('address', 0.0, 'NO_MATCH')
        
    def _compute_decision(self, signals: list[IdentitySignal]) -> tuple[str, float, str]:
        org_signal = next((s for s in signals if s.field == 'org_number'), None)
        
        if org_signal and org_signal.status == 'MATCH':
            return 'VERIFIED', 1.0, 'Exact org number match'
            
        if org_signal and org_signal.status == 'MISMATCH':
            return 'REJECTED', 0.0, 'Org number mismatch'
            
        name_signal = next((s for s in signals if s.field == 'name'), None)
        
        if name_signal and name_signal.match_score >= 0.8:
            return 'PROBABLE', name_signal.match_score, 'Name match without org number'
            
        return 'AMBIGUOUS', 0.4, 'Insufficient signals to verify identity'
