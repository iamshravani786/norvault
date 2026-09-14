from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from app.api.deps import get_db

router = APIRouter(prefix='/evidence', tags=['evidence'])

@router.get('/sources')
async def list_sources(db: AsyncSession = Depends(get_db)):
    """List all registered source adapters."""
    return {"message": "Not implemented yet"}

@router.get('/documents/{document_id}')
async def get_document(document_id: int, db: AsyncSession = Depends(get_db)):
    """Get a specific source document."""
    return {"message": "Not implemented yet"}
