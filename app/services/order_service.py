from typing import List, Optional
from uuid import UUID
from sqlalchemy import select, func
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import BackgroundTasks

from app.models.models import Order, OrderItem, OrderStatus, User, Product, ProductVariant
from app.schemas.order import OrderCreate
from app.services.fulfillment_service import FulfillmentService
from app.services.email_service import EmailService
from app.utils.exceptions import NotFoundException, BadRequestException

class OrderService:
    @staticmethod
    async def create_order(db: AsyncSession, user: User, order_in: OrderCreate, background_tasks: BackgroundTasks):
        # 1) Fetch variants to get verified prices (Security fix: avoid client-controlled pricing)
        skus = [item.sku for item in order_in.items]
        result = await db.execute(select(ProductVariant).where(ProductVariant.sku.in_(skus)))
        variants = {v.sku: v for v in result.scalars().all()}

        if len(variants) != len(set(skus)):
            missing = set(skus) - set(variants.keys())
            raise BadRequestException(f"Some products not found: {missing}")

        total_amount = 0
        order_items_to_create = []

        for item in order_in.items:
            variant = variants[item.sku]
            if not variant.is_active:
                raise BadRequestException(f"Product variant {variant.sku} is not active")

            item_total = variant.price * item.quantity
            total_amount += item_total

            order_items_to_create.append(
                OrderItem(
                    sku=item.sku,
                    quantity=item.quantity,
                    price=variant.price
                )
            )

        # 2) Insert order with status = PENDING
        db_order = Order(
            user_id=user.id,
            total_amount=total_amount,
            status=OrderStatus.PENDING
        )
        db.add(db_order)
        # We need the ID, so flush
        await db.flush()

        # 3) Insert order items
        for db_item in order_items_to_create:
            db_item.order_id = db_order.id
            db.add(db_item)

        # 4) Commit transaction
        await db.commit()
        await db.refresh(db_order)

        # 5) Process fulfillment (outside DB transaction)
        fulfillment_id = await FulfillmentService.process_fulfillment({
            "external_order_id": str(db_order.id),
            "items": [{"sku": i.sku, "quantity": i.quantity} for i in order_in.items]
        })

        # 6) If success → CONFIRMED, 7) If failure → FAILED
        if fulfillment_id:
            db_order.status = OrderStatus.CONFIRMED
            db_order.fulfillment_id = fulfillment_id
            background_tasks.add_task(EmailService.send_order_confirmation, user.email, str(db_order.id))
        else:
            db_order.status = OrderStatus.FAILED
            background_tasks.add_task(EmailService.send_order_failure, user.email, str(db_order.id))

        await db.commit()
        await db.refresh(db_order)
        return db_order

    @staticmethod
    async def get_order(db: AsyncSession, order_id: UUID, user_id: Optional[UUID] = None):
        query = select(Order).where(Order.id == order_id)
        if user_id:
            query = query.where(Order.user_id == user_id)

        result = await db.execute(query)
        order = result.scalar_one_or_none()
        if not order:
            raise NotFoundException("Order not found")
        return order

    @staticmethod
    async def get_user_orders(db: AsyncSession, user_id: UUID, skip: int = 0, limit: int = 100):
        result = await db.execute(
            select(Order)
            .where(Order.user_id == user_id)
            .offset(skip)
            .limit(limit)
            .order_by(Order.created_at.desc())
        )
        return result.scalars().all()

    @staticmethod
    async def get_all_orders(db: AsyncSession, status: Optional[OrderStatus] = None, skip: int = 0, limit: int = 100):
        query = select(Order)
        if status:
            query = query.where(Order.status == status)
        result = await db.execute(query.offset(skip).limit(limit).order_by(Order.created_at.desc()))
        return result.scalars().all()

    @staticmethod
    async def update_order_status(db: AsyncSession, order_id: UUID, status: OrderStatus):
        db_order = await OrderService.get_order(db, order_id)
        db_order.status = status
        await db.commit()
        await db.refresh(db_order)
        return db_order

    @staticmethod
    async def cancel_order(db: AsyncSession, order_id: UUID):
        db_order = await OrderService.get_order(db, order_id)
        if db_order.status == OrderStatus.CANCELLED:
            raise BadRequestException("Order is already cancelled")
        db_order.status = OrderStatus.CANCELLED
        await db.commit()
        await db.refresh(db_order)
        return db_order
