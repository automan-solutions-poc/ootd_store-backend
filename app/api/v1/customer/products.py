from typing import List
from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from app.db.session import get_db
from app.api.deps import customer_required
from app.models.models import User
from app.schemas.product import ProductOut
from app.services.product_service import ProductService

router = APIRouter(prefix="/products", dependencies=[customer_required])

@router.get("/", response_model=List[ProductOut])
async def get_products(
    skip: int = 0,
    limit: int = 100,
    db: AsyncSession = Depends(get_db)
):
    return await ProductService.get_products(db, skip=skip, limit=limit, active_only=True)
