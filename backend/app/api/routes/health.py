from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import text
from app.api.deps import get_db

router = APIRouter()

@router.get('/health')
async def health_check():
    return {'status': 'ok', 'service': 'NORVAULT', 'version': '1.0.0'}

@router.get('/health/db')
async def db_health(db: AsyncSession = Depends(get_db)):
    try:
        await db.execute(text("SELECT 1"))
        return {'status': 'ok', 'message': 'Database connection is healthy'}
    except Exception as e:
        return {'status': 'error', 'message': str(e)}
