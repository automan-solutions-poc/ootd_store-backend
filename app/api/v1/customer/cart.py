from uuid import UUID
from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from app.db.session import get_db
from app.api.deps import get_current_user
from app.models.models import User
from app.services.cart_service import CartService

router = APIRouter()

@router.get("/")
async def get_cart(current_user: User = Depends(get_current_user), db: AsyncSession = Depends(get_db)):
    return await CartService.get_or_create_cart(db, current_user.id)

@router.post("/add")
async def add_to_cart(variant_id: UUID, quantity: int = 1, current_user: User = Depends(get_current_user), db: AsyncSession = Depends(get_db)):
    return await CartService.add_to_cart(db, current_user.id, variant_id, quantity)
