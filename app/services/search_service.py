from sqlalchemy import select, or_
from sqlalchemy.ext.asyncio import AsyncSession
from app.models.models import Product, Category

class SearchService:
    @staticmethod
    async def search_products(db: AsyncSession, query: str = None, category_slug: str = None, min_price: float = None, max_price: float = None, sort_by: str = "created_at"):
        # This is a conceptual search, usually would use Elasticsearch/PostgreSQL TSVector
        stmt = select(Product).where(Product.is_active == True)

        if query:
            stmt = stmt.where(or_(
                Product.name.ilike(f"%{query}%"),
                Product.description.ilike(f"%{query}%")
            ))

        if category_slug:
            stmt = stmt.join(Category).where(Category.slug == category_slug)

        # Pricing filtering would join Variants
        #stmt = stmt.join(ProductVariant)

        if sort_by == "price_asc":
            #stmt = stmt.order_by(ProductVariant.price.asc())
            pass
        else:
            stmt = stmt.order_by(Product.created_at.desc())

        result = await db.execute(stmt)
        return result.scalars().all()
