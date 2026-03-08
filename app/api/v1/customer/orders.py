from typing import List
from uuid import UUID
from fastapi import APIRouter, Depends, BackgroundTasks
from sqlalchemy.ext.asyncio import AsyncSession
from app.db.session import get_db
from app.api.deps import get_current_user, customer_required
from app.models.models import User
from app.schemas.order import OrderOut, OrderCreate
from app.services.order_service import OrderService

router = APIRouter(prefix="/orders", dependencies=[customer_required])

@router.post("/", response_model=OrderOut)
async def create_order(
    order_in: OrderCreate,
    background_tasks: BackgroundTasks,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    return await OrderService.create_order(db, current_user, order_in, background_tasks)

@router.get("/", response_model=List[OrderOut])
async def get_my_orders(
    skip: int = 0,
    limit: int = 100,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    return await OrderService.get_user_orders(db, current_user.id, skip=skip, limit=limit)

@router.get("/{order_id}", response_model=OrderOut)
async def get_order_details(
    order_id: UUID,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    return await OrderService.get_order(db, order_id, user_id=current_user.id)
