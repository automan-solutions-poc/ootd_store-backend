from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from app.db.session import get_db
from app.services.promo_service import PromoService

router = APIRouter()

@router.get("/validate/{code}")
async def validate_promo(code: str, db: AsyncSession = Depends(get_db)):
    return await PromoService.validate_promo(db, code)
