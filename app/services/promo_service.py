from datetime import datetime, timezone
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from app.models.models import PromoCode
from app.utils.exceptions import BadRequestException

class PromoService:
    @staticmethod
    async def validate_promo(db: AsyncSession, code: str):
        result = await db.execute(
            select(PromoCode)
            .where(PromoCode.code == code)
            .where(PromoCode.is_active == True)
            .where(PromoCode.expiry_date > datetime.now(timezone.utc))
        )
        promo = result.scalar_one_or_none()
        if not promo:
            raise BadRequestException("Invalid or expired promo code")
        return promo
