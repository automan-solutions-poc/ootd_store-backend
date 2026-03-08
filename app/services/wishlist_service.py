from uuid import UUID
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from app.models.models import Wishlist, WishlistItem
from app.utils.exceptions import NotFoundException

class WishlistService:
    @staticmethod
    async def get_or_create_wishlist(db: AsyncSession, user_id: UUID):
        result = await db.execute(select(Wishlist).where(Wishlist.user_id == user_id))
        wishlist = result.scalar_one_or_none()
        if not wishlist:
            wishlist = Wishlist(user_id=user_id)
            db.add(wishlist)
            await db.commit()
            await db.refresh(wishlist)
        return wishlist

    @staticmethod
    async def add_to_wishlist(db: AsyncSession, user_id: UUID, product_id: UUID):
        wishlist = await WishlistService.get_or_create_wishlist(db, user_id)
        item = WishlistItem(wishlist_id=wishlist.id, product_id=product_id)
        db.add(item)
        await db.commit()
        return wishlist
