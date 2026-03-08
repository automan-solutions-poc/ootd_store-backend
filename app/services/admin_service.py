from typing import List, Optional
from uuid import UUID
from sqlalchemy import select, func, desc
from sqlalchemy.ext.asyncio import AsyncSession
from app.models.models import User, Order, OrderItem, Product, UserRole
from app.schemas.user import UserUpdate
from app.utils.exceptions import NotFoundException

class AdminService:
    @staticmethod
    async def get_all_users(db: AsyncSession, skip: int = 0, limit: int = 100):
        result = await db.execute(select(User).offset(skip).limit(limit))
        return result.scalars().all()

    @staticmethod
    async def update_user(db: AsyncSession, user_id: UUID, user_in: UserUpdate):
        result = await db.execute(select(User).where(User.id == user_id))
        user = result.scalar_one_or_none()
        if not user:
            raise NotFoundException("User not found")

        update_data = user_in.model_dump(exclude_unset=True)
        for field, value in update_data.items():
            setattr(user, field, value)

        await db.commit()
        await db.refresh(user)
        return user

    @staticmethod
    async def get_analytics(db: AsyncSession):
        # Total Revenue (Logic fix: only confirmed orders)
        rev_result = await db.execute(
            select(func.sum(Order.total_amount))
            .where(Order.status == OrderStatus.CONFIRMED)
        )
        total_revenue = rev_result.scalar() or 0.0

        # Orders Count
        count_result = await db.execute(select(func.count(Order.id)))
        orders_count = count_result.scalar() or 0

        # Top Selling SKUs
        sku_result = await db.execute(
            select(OrderItem.sku, func.sum(OrderItem.quantity).label("total_sold"))
            .group_by(OrderItem.sku)
            .order_by(desc("total_sold"))
            .limit(10)
        )
        top_selling_skus = [{"sku": r[0], "total_sold": r[1]} for r in sku_result.all()]

        # Customer Order Frequency
        freq_result = await db.execute(
            select(User.email, func.count(Order.id).label("order_count"))
            .join(Order, User.id == Order.user_id)
            .group_by(User.email)
            .order_by(desc("order_count"))
            .limit(10)
        )
        customer_order_frequency = [{"email": r[0], "order_count": r[1]} for r in freq_result.all()]

        return {
            "total_revenue": float(total_revenue),
            "orders_count": orders_count,
            "top_selling_skus": top_selling_skus,
            "customer_order_frequency": customer_order_frequency
        }

    @staticmethod
    async def get_revenue_by_date(db: AsyncSession, start_date: str, end_date: str):
        # simplified date range query
        result = await db.execute(
            select(func.date(Order.created_at).label("date"), func.sum(Order.total_amount))
            .where(Order.created_at >= start_date)
            .where(Order.created_at <= end_date)
            .group_by(func.date(Order.created_at))
            .order_by("date")
        )
        return [{"date": str(r[0]), "revenue": float(r[1])} for r in result.all()]
