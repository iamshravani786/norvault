from fastapi import APIRouter, Depends, Query
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.deps import get_db, get_budget_manager
from app.core.budget_manager import BudgetManager
from app.services.bulk_import import bulk_import_companies

router = APIRouter(prefix='/admin', tags=['admin'])

@router.get('/budget')
async def get_budget_status(budget: BudgetManager = Depends(get_budget_manager)):
    """Get current request budget status."""
    return await budget.get_status()

@router.post('/budget/reset')
async def reset_budget(budget: BudgetManager = Depends(get_budget_manager)):
    """Reset budget counters."""
    await budget.reset()
    return {"status": "reset", "details": await budget.get_status()}

@router.get('/runs')
async def list_runs(db: AsyncSession = Depends(get_db)):
    """List recent retrieval runs."""
    return {"message": "Not implemented yet"}

@router.get('/runs/{run_id}')
async def get_run_detail(run_id: str, db: AsyncSession = Depends(get_db)):
    """Get details of a specific retrieval run."""
    return {"message": "Not implemented yet"}

@router.post('/import/bulk')
async def trigger_bulk_import(
    count: int = Query(1000, ge=100, le=5000),
    db: AsyncSession = Depends(get_db),
):
    """Trigger bulk import of companies from BRREG bulk data."""
    stats = await bulk_import_companies(db, count=count)
    return stats

@router.get('/stats')
async def get_system_stats(db: AsyncSession = Depends(get_db)):
    """Get system statistics (total companies, facts, etc)."""
    return {"message": "Not implemented yet"}
