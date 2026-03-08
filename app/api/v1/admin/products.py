from typing import List, Optional
from uuid import UUID
from fastapi import APIRouter, Depends, Query
from sqlalchemy.ext.asyncio import AsyncSession
from app.db.session import get_db
from app.api.deps import admin_required
from app.schemas.product import ProductOut, ProductCreate, ProductUpdate
from app.services.product_service import ProductService

router = APIRouter(prefix="/products", dependencies=[admin_required])

@router.post("/", response_model=ProductOut)
async def create_product(product_in: ProductCreate, db: AsyncSession = Depends(get_db)):
    return await ProductService.create_product(db, product_in)

@router.get("/", response_model=List[ProductOut])
async def get_products(
    skip: int = 0,
    limit: int = 100,
    db: AsyncSession = Depends(get_db)
):
    return await ProductService.get_products(db, skip=skip, limit=limit)

@router.get("/{product_id}", response_model=ProductOut)
async def get_product(product_id: UUID, db: AsyncSession = Depends(get_db)):
    return await ProductService.get_product(db, product_id)

@router.patch("/{product_id}", response_model=ProductOut)
async def update_product(product_id: UUID, product_in: ProductUpdate, db: AsyncSession = Depends(get_db)):
    return await ProductService.update_product(db, product_id, product_in)

@router.delete("/{product_id}")
async def delete_product(product_id: UUID, db: AsyncSession = Depends(get_db)):
    await ProductService.delete_product(db, product_id)
    return {"message": "Product deleted"}

@router.post("/bulk-update-pricing")
async def bulk_update_pricing(percentage_change: float, db: AsyncSession = Depends(get_db)):
    await ProductService.bulk_update_pricing(db, percentage_change)
    return {"message": "Pricing updated successfully"}
