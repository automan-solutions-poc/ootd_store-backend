from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from app.db.session import get_db
from app.api.deps import admin_required
from app.services.inventory_service import InventoryService
from app.services.category_service import CategoryService
from uuid import UUID

router = APIRouter()

@router.post("/categories")
async def create_category(name: str, slug: str, parent_id: UUID = None, db: AsyncSession = Depends(get_db)):
    return await CategoryService.create_category(db, name, slug, parent_id)

@router.patch("/inventory/{variant_id}")
async def update_stock(variant_id: UUID, quantity: int, db: AsyncSession = Depends(get_db)):
    await InventoryService.update_stock(db, variant_id, quantity)
    return {"message": "Stock updated"}
