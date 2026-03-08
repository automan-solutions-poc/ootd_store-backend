from uuid import UUID
from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from app.db.session import get_db
from app.api.deps import get_current_user
from app.models.models import User
from app.services.review_service import ReviewService

router = APIRouter()

@router.post("/{product_id}/review")
async def add_review(product_id: UUID, rating: int, comment: str = None, current_user: User = Depends(get_current_user), db: AsyncSession = Depends(get_db)):
    return await ReviewService.add_review(db, current_user.id, product_id, rating, comment)

@router.get("/{product_id}/summary")
async def get_summary(product_id: UUID, db: AsyncSession = Depends(get_db)):
    return await ReviewService.get_ratings_summary(db, product_id)
