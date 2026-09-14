from fastapi import APIRouter, Depends, Body
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List

from app.api.deps import get_db, get_pipeline
from app.services.benchmark import BenchmarkRunner
from app.services.pipeline import CompanyPipeline

router = APIRouter(prefix='/benchmark', tags=['benchmark'])

@router.post('/run')
async def run_benchmark(
    org_numbers: List[str] = Body(...),
    db: AsyncSession = Depends(get_db),
    pipeline: CompanyPipeline = Depends(get_pipeline),
):
    """Run benchmark on a list of org numbers. Returns benchmark results."""
    runner = BenchmarkRunner()
    result = await runner.run(org_numbers, db, pipeline)
    return result

@router.get('/results/{run_id}')
async def get_benchmark_results(run_id: str, db: AsyncSession = Depends(get_db)):
    """Get results of a benchmark run."""
    return {"message": "Not implemented yet"}
