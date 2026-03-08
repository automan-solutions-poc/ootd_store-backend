from uuid import UUID
from sqlalchemy import select, func
from sqlalchemy.ext.asyncio import AsyncSession
from app.models.models import Review
from app.utils.exceptions import NotFoundException

class ReviewService:
    @staticmethod
    async def add_review(db: AsyncSession, user_id: UUID, product_id: UUID, rating: int, comment: str = None):
        review = Review(user_id=user_id, product_id=product_id, rating=rating, comment=comment)
        db.add(review)
        await db.commit()
        await db.refresh(review)
        return review

    @staticmethod
    async def get_product_reviews(db: AsyncSession, product_id: UUID):
        result = await db.execute(select(Review).where(Review.product_id == product_id))
        return result.scalars().all()

    @staticmethod
    async def get_ratings_summary(db: AsyncSession, product_id: UUID):
        result = await db.execute(
            select(func.avg(Review.rating), func.count(Review.id))
            .where(Review.product_id == product_id)
        )
        avg_rating, count = result.one()
        return {"average_rating": float(avg_rating or 0), "review_count": count}
