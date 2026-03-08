from datetime import datetime
from decimal import Decimal
from typing import Optional, List
from uuid import UUID
from pydantic import BaseModel, ConfigDict, Field

class ProductVariantBase(BaseModel):
    sku: str
    size: Optional[str] = None
    color: Optional[str] = None
    price: Decimal = Field(gt=0)
    stock_quantity: int = Field(0, ge=0)
    is_active: bool = True

class ProductVariantCreate(ProductVariantBase):
    pass

class ProductVariantOut(ProductVariantBase):
    id: UUID

    model_config = ConfigDict(from_attributes=True)

class ProductBase(BaseModel):
    name: str
    description: Optional[str] = None
    category_id: Optional[UUID] = None
    is_active: bool = True

class ProductCreate(ProductBase):
    variants: List[ProductVariantCreate] = []

class ProductUpdate(BaseModel):
    name: Optional[str] = None
    description: Optional[str] = None
    category_id: Optional[UUID] = None
    is_active: Optional[bool] = None
    variants: Optional[List[ProductVariantCreate]] = None

class ProductOut(ProductBase):
    id: UUID
    created_at: datetime
    variants: List[ProductVariantOut] = []

    model_config = ConfigDict(from_attributes=True)
