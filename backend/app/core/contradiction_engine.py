from __future__ import annotations
from typing import Any
from collections import defaultdict
from pydantic import BaseModel
from datetime import datetime

class ExtractedFact(BaseModel):
    id: str
    company_id: str
    fact_type: str
    predicate: str
    value: str
    source_id: str
    authority_level: int
    reporting_period: str | None = None
    entity_scope: str | None = None
    source_date: datetime | None = None
    retrieved_at: datetime
    
class Conflict(BaseModel):
    conflict_id: str
    company_id: str
    fact_type: str
    predicate: str
    facts: list[Any]
    resolution_strategy: str | None = None
    resolved_fact_id: str | None = None

class ContradictionEngine:
    def detect_contradictions(
        self,
        facts: list[Any],
    ) -> list[Conflict]:
        """
        Group facts by (company, fact_type, predicate) and check for value disagreements.
        """
        groups: dict[tuple[str, str, str], list[ExtractedFact]] = defaultdict(list)
        
        for fact in facts:
            groups[(fact.subject, fact.fact_type, fact.predicate)].append(fact)
            
        conflicts = []
        conflict_counter = 1
        
        for key, group in groups.items():
            if len(group) <= 1:
                continue
                
            unique_values = set()
            for f in group:
                try:
                    unique_values.add(f.value)
                except TypeError:
                    unique_values.add(str(f.value))
                    
            if len(unique_values) > 1:
                conflicts.append(
                    Conflict(
                        conflict_id=f"conflict_{conflict_counter}",
                        company_id=key[0],
                        fact_type=key[1],
                        predicate=key[2],
                        facts=group
                    )
                )
                conflict_counter += 1
                
        return conflicts
    
    def resolve_conflict(self, conflict: Conflict) -> Conflict:
        """
        Attempt to resolve a conflict.
        """
        facts = conflict.facts
        
        periods = set(f.reporting_period for f in facts if f.reporting_period)
        if len(periods) > 1:
            conflict.resolution_strategy = 'DIFFERENT_REPORTING_PERIOD'
            return conflict
            
        scopes = set(f.entity_scope for f in facts if f.entity_scope)
        if len(scopes) > 1:
            conflict.resolution_strategy = 'DIFFERENT_ENTITY'
            return conflict
            
        max_auth = max(f.authority_level for f in facts)
        top_auth_facts = [f for f in facts if f.authority_level == max_auth]
        
        if len(top_auth_facts) == 1:
            conflict.resolution_strategy = 'LATEST_AUTHORITATIVE'
            conflict.resolved_fact_id = top_auth_facts[0].id
            return conflict
            
        def get_date(f: ExtractedFact) -> datetime:
            return f.source_date if f.source_date else f.retrieved_at
            
        top_auth_facts.sort(key=get_date, reverse=True)
        newest_date = get_date(top_auth_facts[0])
        newest_facts = [f for f in top_auth_facts if get_date(f) == newest_date]
        
        if len(newest_facts) == 1:
            conflict.resolution_strategy = 'LATEST_AUTHORITATIVE'
            conflict.resolved_fact_id = newest_facts[0].id
            return conflict
            
        conflict.resolution_strategy = 'UNRESOLVED'
        return conflict
