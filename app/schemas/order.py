from datetime import datetime
from decimal import Decimal
from typing import List, Optional
from uuid import UUID
from pydantic import BaseModel, ConfigDict, Field
from app.models.models import OrderStatus

class OrderItemBase(BaseModel):
    sku: str
    quantity: int = Field(gt=0)
    price: Decimal = Field(gt=0)

class OrderItemCreate(BaseModel):
    sku: str
    quantity: int = Field(gt=0)

class OrderItemOut(OrderItemBase):
    id: UUID

    model_config = ConfigDict(from_attributes=True)

class OrderBase(BaseModel):
    total_amount: Decimal
    status: OrderStatus = OrderStatus.PENDING

class OrderCreate(BaseModel):
    items: List[OrderItemCreate]

class OrderUpdateStatus(BaseModel):
    status: OrderStatus

class OrderOut(OrderBase):
    id: UUID
    user_id: UUID
    fulfillment_id: Optional[str] = None
    created_at: datetime
    items: List[OrderItemOut]

    model_config = ConfigDict(from_attributes=True)
