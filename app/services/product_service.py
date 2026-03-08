from typing import List, Optional
from uuid import UUID
from sqlalchemy import select, update, delete, func
from sqlalchemy.ext.asyncio import AsyncSession
from app.models.models import Product
from app.schemas.product import ProductCreate, ProductUpdate
from app.utils.exceptions import NotFoundException

class ProductService:
    @staticmethod
    async def create_product(db: AsyncSession, product_in: ProductCreate):
        db_product = Product(**product_in.model_dump())
        db.add(db_product)
        await db.commit()
        await db.refresh(db_product)
        return db_product

    @staticmethod
    async def get_product(db: AsyncSession, product_id: UUID):
        result = await db.execute(select(Product).where(Product.id == product_id))
        product = result.scalar_one_or_none()
        if not product:
            raise NotFoundException("Product not found")
        return product

    @staticmethod
    async def get_products(db: AsyncSession, skip: int = 0, limit: int = 100, active_only: bool = False):
        query = select(Product)
        if active_only:
            query = query.where(Product.is_active == True)
        result = await db.execute(query.offset(skip).limit(limit))
        return result.scalars().all()

    @staticmethod
    async def update_product(db: AsyncSession, product_id: UUID, product_in: ProductUpdate):
        db_product = await ProductService.get_product(db, product_id)
        update_data = product_in.model_dump(exclude_unset=True)
        for field, value in update_data.items():
            setattr(db_product, field, value)
        await db.commit()
        await db.refresh(db_product)
        return db_product

    @staticmethod
    async def delete_product(db: AsyncSession, product_id: UUID):
        db_product = await ProductService.get_product(db, product_id)
        await db.delete(db_product)
        await db.commit()
        return db_product

    @staticmethod
    async def bulk_update_pricing(db: AsyncSession, percentage_change: float):
        # Bonus: Bulk update pricing
        factor = 1 + (percentage_change / 100)
        await db.execute(
            update(Product).values(price=Product.price * factor)
        )
        await db.commit()
