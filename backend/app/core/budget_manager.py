from __future__ import annotations
import asyncio
from decimal import Decimal
from typing import Any
from pydantic import BaseModel

class BudgetStatus(BaseModel):
    max_requests: int
    max_cost: Decimal
    requests_used: int
    requests_saved_by_cache: int
    cost_estimate: Decimal
    remaining_requests: int
    remaining_budget: Decimal
    per_source: dict[str, dict[str, Any]]

class BudgetManager:
    """Thread-safe request budget manager."""
    
    def __init__(self, max_requests: int = 2000, max_cost: Decimal = Decimal('10.00')):
        self._max_requests = max_requests
        self._max_cost = max_cost
        self._requests_used = 0
        self._requests_saved_by_cache = 0
        self._cost_estimate = Decimal('0.00')
        self._per_source: dict[str, dict[str, Any]] = {}
        self._lock = asyncio.Lock()
    
    async def can_request(self, source_id: str, cost: Decimal = Decimal('0.00')) -> bool:
        """Check if we have budget for another request."""
        async with self._lock:
            if self._requests_used >= self._max_requests:
                return False
            if self._cost_estimate + cost > self._max_cost:
                return False
            return True
    
    async def record_request(self, source_id: str, cached: bool = False, cost: Decimal = Decimal('0.00')) -> None:
        """Record a request (or cache hit)."""
        async with self._lock:
            if source_id not in self._per_source:
                self._per_source[source_id] = {'used': 0, 'cached': 0, 'cost': Decimal('0.00')}
                
            if cached:
                self._requests_saved_by_cache += 1
                self._per_source[source_id]['cached'] += 1
            else:
                self._requests_used += 1
                self._cost_estimate += cost
                self._per_source[source_id]['used'] += 1
                self._per_source[source_id]['cost'] += cost
    
    async def get_status(self) -> BudgetStatus:
        """Return current budget status."""
        async with self._lock:
            return BudgetStatus(
                max_requests=self._max_requests,
                max_cost=self._max_cost,
                requests_used=self._requests_used,
                requests_saved_by_cache=self._requests_saved_by_cache,
                cost_estimate=self._cost_estimate,
                remaining_requests=self._max_requests - self._requests_used,
                remaining_budget=self._max_cost - self._cost_estimate,
                per_source=self._per_source.copy()
            )
    
    async def reset(self) -> None:
        """Reset all counters."""
        async with self._lock:
            self._requests_used = 0
            self._requests_saved_by_cache = 0
            self._cost_estimate = Decimal('0.00')
            self._per_source = {}
