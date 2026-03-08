from uuid import UUID
from sqlalchemy import select, delete
from sqlalchemy.ext.asyncio import AsyncSession
from app.models.models import Cart, CartItem
from app.utils.exceptions import NotFoundException

class CartService:
    @staticmethod
    async def get_or_create_cart(db: AsyncSession, user_id: UUID):
        result = await db.execute(select(Cart).where(Cart.user_id == user_id))
        cart = result.scalar_one_or_none()
        if not cart:
            cart = Cart(user_id=user_id)
            db.add(cart)
            await db.commit()
            await db.refresh(cart)
        return cart

    @staticmethod
    async def add_to_cart(db: AsyncSession, user_id: UUID, variant_id: UUID, quantity: int):
        cart = await CartService.get_or_create_cart(db, user_id)
        result = await db.execute(
            select(CartItem)
            .where(CartItem.cart_id == cart.id)
            .where(CartItem.variant_id == variant_id)
        )
        item = result.scalar_one_or_none()
        if item:
            item.quantity += quantity
        else:
            item = CartItem(cart_id=cart.id, variant_id=variant_id, quantity=quantity)
            db.add(item)
        await db.commit()
        return cart
