from uuid import UUID
from sqlalchemy import update
from sqlalchemy.ext.asyncio import AsyncSession
from app.models.models import ProductVariant
from app.utils.exceptions import NotFoundException

class InventoryService:
    @staticmethod
    async def update_stock(db: AsyncSession, variant_id: UUID, quantity: int):
        result = await db.execute(
            update(ProductVariant)
            .where(ProductVariant.id == variant_id)
            .values(stock_quantity=ProductVariant.stock_quantity + quantity)
        )
        await db.commit()
        if result.rowcount == 0:
            raise NotFoundException("Variant not found")
