from typing import List
from uuid import UUID
from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from app.db.session import get_db
from app.api.deps import customer_required
from app.models.models import User
from app.schemas.product import ProductOut
from app.services.product_service import ProductService

router = APIRouter(prefix="/products")

@router.get("/", response_model=List[ProductOut])
async def get_products(
    skip: int = 0,
    limit: int = 100,
    db: AsyncSession = Depends(get_db)
):
    return await ProductService.get_products(db, skip=skip, limit=limit, active_only=True)

@router.get("/{product_id}", response_model=ProductOut)
async def get_product(
    product_id: UUID,
    db: AsyncSession = Depends(get_db)
):
    product = await ProductService.get_product(db, product_id)
    if not product.is_active:
        from app.utils.exceptions import NotFoundException
        raise NotFoundException("Product not found")
    return product
