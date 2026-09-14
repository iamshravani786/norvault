from __future__ import annotations
from pydantic import BaseModel
from typing import Literal, Any
from .contradiction_engine import ExtractedFact, Conflict
from .identity_firewall import IdentityMatchResult

class AuditResult(BaseModel):
    publish: bool
    risk_level: Literal['LOW', 'MEDIUM', 'HIGH', 'CRITICAL']
    reasons: list[str]
    rejected_claims: list[dict[str, Any]]
    checks_performed: list[dict[str, Any]]

class AdversarialAuditor:
    def audit_fact(
        self,
        fact: ExtractedFact,
        identity_match: IdentityMatchResult,
        source_authority_level: int,
        conflicts: list[Conflict],
        existing_facts: list[ExtractedFact] | None = None,
    ) -> AuditResult:
        """
        Run adversarial verification checks on a fact before publishing.
        """
        reasons = []
        checks = []
        risk_scores = []
        
        # 1. Identity Check
        identity_passed = identity_match.decision in ('VERIFIED', 'PROBABLE')
        checks.append({'check_name': 'IDENTITY_CHECK', 'passed': identity_passed, 'detail': f"Identity: {identity_match.decision}"})
        if identity_match.decision == 'AMBIGUOUS':
            risk_scores.append(4) # CRITICAL
            reasons.append("Identity is ambiguous.")
        elif identity_match.decision == 'PROBABLE':
            risk_scores.append(3) # HIGH
            reasons.append("Identity is only probable.")
        elif identity_match.decision == 'REJECTED':
            risk_scores.append(4)
            reasons.append("Identity rejected.")
            
        # 4. Source Authority Check
        auth_passed = source_authority_level in (1, 2)
        checks.append({'check_name': 'SOURCE_AUTHORITY_CHECK', 'passed': auth_passed, 'detail': f"Authority Level: {source_authority_level}"})
        if not auth_passed:
            risk_scores.append(2) # MEDIUM
            reasons.append(f"Secondary source used (Level {source_authority_level}).")
            
        # 5. Contradiction Check
        is_contradicted = any(c.fact_type == fact.fact_type and c.predicate == fact.predicate for c in conflicts)
        checks.append({'check_name': 'CONTRADICTION_CHECK', 'passed': not is_contradicted, 'detail': f"Contradicted: {is_contradicted}"})
        if is_contradicted:
            risk_scores.append(3) # HIGH
            reasons.append("Fact is contradicted by another source.")
            
        # Overall Risk
        max_risk = max(risk_scores) if risk_scores else 1
        
        risk_level_map: dict[int, Literal['LOW', 'MEDIUM', 'HIGH', 'CRITICAL']] = {
            1: 'LOW',
            2: 'MEDIUM',
            3: 'HIGH',
            4: 'CRITICAL'
        }
        
        risk_level = risk_level_map[max_risk]
        
        # 8. Financial Safety Check
        is_financial = fact.fact_type in ('financial_statement', 'revenue', 'profit')
        if is_financial and max_risk > 2:
            publish = False
            reasons.append("Financial fact failed safety constraints (risk too high).")
        elif risk_level == 'CRITICAL':
            publish = False
        else:
            publish = True
            
        return AuditResult(
            publish=publish,
            risk_level=risk_level,
            reasons=reasons,
            rejected_claims=[fact.model_dump()] if not publish else [],
            checks_performed=checks
        )
    
    def audit_company(
        self,
        org_number: str,
        all_facts: list[ExtractedFact],
        identity_match: IdentityMatchResult,
        conflicts: list[Conflict],
    ) -> AuditResult:
        """Audit all facts for a company and produce aggregate result."""
        agg_reasons = []
        agg_rejected = []
        agg_checks = []
        max_risk_val = 1
        
        risk_val_map = {'LOW': 1, 'MEDIUM': 2, 'HIGH': 3, 'CRITICAL': 4}
        
        for fact in all_facts:
            res = self.audit_fact(fact, identity_match, fact.authority_level, conflicts)
            if not res.publish:
                agg_rejected.extend(res.rejected_claims)
            
            agg_reasons.extend(res.reasons)
            agg_checks.extend(res.checks_performed)
            max_risk_val = max(max_risk_val, risk_val_map[res.risk_level])
            
        risk_level_map: dict[int, Literal['LOW', 'MEDIUM', 'HIGH', 'CRITICAL']] = {
            1: 'LOW',
            2: 'MEDIUM',
            3: 'HIGH',
            4: 'CRITICAL'
        }
        
        final_risk = risk_level_map[max_risk_val]
        publish = final_risk != 'CRITICAL'
        
        return AuditResult(
            publish=publish,
            risk_level=final_risk,
            reasons=list(set(agg_reasons)),
            rejected_claims=agg_rejected,
            checks_performed=agg_checks
        )
