from typing import List, Optional
from uuid import UUID
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from app.models.models import Category
from app.utils.exceptions import NotFoundException

class CategoryService:
    @staticmethod
    async def create_category(db: AsyncSession, name: str, slug: str, parent_id: Optional[UUID] = None):
        category = Category(name=name, slug=slug, parent_id=parent_id)
        db.add(category)
        await db.commit()
        await db.refresh(category)
        return category

    @staticmethod
    async def get_categories(db: AsyncSession, active_only: bool = True):
        query = select(Category)
        if active_only:
            query = query.where(Category.is_active == True)
        result = await db.execute(query)
        return result.scalars().all()

    @staticmethod
    async def get_category(db: AsyncSession, category_id: UUID):
        result = await db.execute(select(Category).where(Category.id == category_id))
        category = result.scalar_one_or_none()
        if not category:
            raise NotFoundException("Category not found")
        return category
