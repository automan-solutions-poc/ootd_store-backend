from datetime import datetime
from decimal import Decimal
from typing import Optional
from uuid import UUID
from pydantic import BaseModel, ConfigDict, Field

class ProductBase(BaseModel):
    name: str
    description: Optional[str] = None
    sku: str
    price: Decimal = Field(gt=0)
    print_type_id: Optional[str] = None
    is_active: bool = True

class ProductCreate(ProductBase):
    pass

class ProductUpdate(BaseModel):
    name: Optional[str] = None
    description: Optional[str] = None
    sku: Optional[str] = None
    price: Optional[float] = Field(None, gt=0)
    print_type_id: Optional[str] = None
    is_active: Optional[bool] = None

class ProductOut(ProductBase):
    id: UUID
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)
