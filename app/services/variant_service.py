from typing import List
from uuid import UUID
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from app.models.models import ProductVariant
from app.utils.exceptions import NotFoundException

class VariantService:
    @staticmethod
    async def create_variant(db: AsyncSession, product_id: UUID, sku: str, price: float, size: str = None, color: str = None, stock: int = 0):
        variant = ProductVariant(
            product_id=product_id,
            sku=sku,
            price=price,
            size=size,
            color=color,
            stock_quantity=stock
        )
        db.add(variant)
        await db.commit()
        await db.refresh(variant)
        return variant

    @staticmethod
    async def get_variants_by_product(db: AsyncSession, product_id: UUID):
        result = await db.execute(select(ProductVariant).where(ProductVariant.product_id == product_id))
        return result.scalars().all()
