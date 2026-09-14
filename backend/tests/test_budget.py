from __future__ import annotations
import pytest
import asyncio
from app.core.budget_manager import BudgetManager, BudgetExhaustedException

@pytest.mark.asyncio
async def test_initial_state(mock_budget_manager):
    assert mock_budget_manager.requests_made == 0

@pytest.mark.asyncio
async def test_recording_requests(mock_budget_manager):
    await mock_budget_manager.record_request("brreg")
    assert mock_budget_manager.requests_made == 1

@pytest.mark.asyncio
async def test_budget_exhaustion():
    bm = BudgetManager(max_requests=1)
    await bm.record_request("brreg")
    with pytest.raises(BudgetExhaustedException):
        await bm.record_request("brreg")

@pytest.mark.asyncio
async def test_cache_hit_recording(mock_budget_manager):
    await mock_budget_manager.record_cache_hit("brreg")
    assert mock_budget_manager.cache_hits == 1

@pytest.mark.asyncio
async def test_per_source_breakdown(mock_budget_manager):
    await mock_budget_manager.record_request("brreg")
    await mock_budget_manager.record_request("proff")
    breakdown = mock_budget_manager.get_breakdown()
    assert breakdown["brreg"] == 1
    assert breakdown["proff"] == 1

@pytest.mark.asyncio
async def test_reset(mock_budget_manager):
    await mock_budget_manager.record_request("brreg")
    mock_budget_manager.reset()
    assert mock_budget_manager.requests_made == 0

@pytest.mark.asyncio
async def test_concurrent_access(mock_budget_manager):
    async def make_req():
        await mock_budget_manager.record_request("test")
    await asyncio.gather(*(make_req() for _ in range(10)))
    assert mock_budget_manager.requests_made == 10
