from typing import List, Optional
from uuid import UUID
from fastapi import APIRouter, Depends, Query
from sqlalchemy.ext.asyncio import AsyncSession
from app.db.session import get_db
from app.api.deps import admin_required
from app.schemas.order import OrderOut, OrderUpdateStatus
from app.services.order_service import OrderService
from app.models.models import OrderStatus

router = APIRouter(prefix="/orders", dependencies=[admin_required])

@router.get("/", response_model=List[OrderOut])
async def get_orders(
    status: Optional[OrderStatus] = None,
    skip: int = 0,
    limit: int = 100,
    db: AsyncSession = Depends(get_db)
):
    return await OrderService.get_all_orders(db, status=status, skip=skip, limit=limit)

@router.get("/{order_id}", response_model=OrderOut)
async def get_order_details(order_id: UUID, db: AsyncSession = Depends(get_db)):
    return await OrderService.get_order(db, order_id)

@router.patch("/{order_id}/status", response_model=OrderOut)
async def update_order_status(order_id: UUID, status_in: OrderUpdateStatus, db: AsyncSession = Depends(get_db)):
    return await OrderService.update_order_status(db, order_id, status_in.status)

@router.post("/{order_id}/cancel", response_model=OrderOut)
async def cancel_order(order_id: UUID, db: AsyncSession = Depends(get_db)):
    return await OrderService.cancel_order(db, order_id)
