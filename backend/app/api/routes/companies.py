"""Companies API routes."""

from __future__ import annotations

import logging
from typing import Any

from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.deps import get_db, get_pipeline
from app.core.org_number import validate_org_number
from app.schemas.passport import ProofPassport
from app.services.pipeline import CompanyPipeline

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/companies", tags=["companies"])


@router.get("/{org_number}", response_model=ProofPassport, response_model_exclude_none=True)
async def get_company_passport(
    org_number: str,
    mode: str = Query("executive", enum=["executive", "evidence", "timeline", "graph", "audit"]),
    force_refresh: bool = Query(False),
    db: AsyncSession = Depends(get_db),
    pipeline: CompanyPipeline = Depends(get_pipeline),
) -> Any:
    """Retrieve the Proof Passport for a Norwegian company."""
    if not validate_org_number(org_number):
        raise HTTPException(status_code=422, detail="Invalid organization number. Must be a 9-digit Norwegian MOD-11 number.")

    try:
        passport_dict = await pipeline.run(org_number, force_refresh)
        if not passport_dict:
            raise HTTPException(status_code=404, detail="Company not found in Enhetsregisteret.")
            
        if "error" in passport_dict:
            if passport_dict["error"] == "not_found":
                raise HTTPException(status_code=404, detail=passport_dict.get("message", "Company not found."))
            raise HTTPException(status_code=400, detail=passport_dict.get("message", "Error retrieving company."))
            
        return passport_dict
    except HTTPException:
        raise
    except Exception as e:
        logger.exception("Error in get_company_passport")
        raise HTTPException(status_code=500, detail="An internal server error occurred.")


@router.get("/{org_number}/facts")
async def get_company_facts(org_number: str, db: AsyncSession = Depends(get_db)):
    """Get all published facts for a company."""
    if not validate_org_number(org_number):
        raise HTTPException(status_code=422, detail="Invalid organization number.")
    return {"message": "Use the main passport endpoint for now."}
