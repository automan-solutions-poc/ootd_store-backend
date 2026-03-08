from uuid import UUID
from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from app.db.session import get_db
from app.api.deps import get_current_user
from app.models.models import User
from app.services.wishlist_service import WishlistService

router = APIRouter()

@router.get("/")
async def get_wishlist(current_user: User = Depends(get_current_user), db: AsyncSession = Depends(get_db)):
    return await WishlistService.get_or_create_wishlist(db, current_user.id)

@router.post("/add")
async def add_to_wishlist(product_id: UUID, current_user: User = Depends(get_current_user), db: AsyncSession = Depends(get_db)):
    return await WishlistService.add_to_wishlist(db, current_user.id, product_id)
