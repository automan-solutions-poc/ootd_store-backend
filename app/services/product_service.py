from datetime import datetime, timezone
from typing import List, Optional
from uuid import UUID
from sqlalchemy import select, update, delete, func
from sqlalchemy.ext.asyncio import AsyncSession
from app.models.models import Product
from app.schemas.product import ProductCreate, ProductUpdate
from app.utils.exceptions import NotFoundException, BadRequestException

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
        # Soft delete logic
        db_product = await ProductService.get_product(db, product_id)
        db_product.is_active = False
        await db.commit()
        return db_product

    @staticmethod
    async def bulk_update_pricing(db: AsyncSession, percentage_change: float, admin_id: UUID):
        # Safety range check
        if not (-50 <= percentage_change <= 50):
            raise BadRequestException("percentage_change must be between -50 and 50")

        # 1) Calculate old average price
        avg_old_res = await db.execute(select(func.avg(Product.price)))
        old_avg = avg_old_res.scalar() or 0.0

        # 2) Perform update in transaction
        factor = 1 + (percentage_change / 100)
        await db.execute(
            update(Product).values(price=Product.price * factor)
        )
        await db.commit()

        # 3) Calculate new average price
        avg_new_res = await db.execute(select(func.avg(Product.price)))
        new_avg = avg_new_res.scalar() or 0.0

        # 4) Log action
        from app.core.logging import logger
        logger.info(
            "bulk_pricing_updated",
            admin_id=str(admin_id),
            percentage_change=percentage_change,
            timestamp=datetime.now(timezone.utc).isoformat()
        )

        # 5) Return stats
        # Counting updated products is tricky with bulk update result in some DBs,
        # but we can get it from rowcount if supported
        res = await db.execute(select(func.count(Product.id)))
        count = res.scalar() or 0

        return {
            "number_of_products_updated": count,
            "old_average_price": float(old_avg),
            "new_average_price": float(new_avg)
        }
