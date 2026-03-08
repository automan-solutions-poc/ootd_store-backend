from uuid import UUID
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from app.models.models import User, Address
from app.utils.exceptions import NotFoundException

class UserService:
    @staticmethod
    async def get_profile(db: AsyncSession, user_id: UUID):
        result = await db.execute(select(User).where(User.id == user_id))
        user = result.scalar_one_or_none()
        if not user:
            raise NotFoundException("User not found")
        return user

    @staticmethod
    async def add_address(db: AsyncSession, user_id: UUID, address_data: dict):
        address = Address(user_id=user_id, **address_data)
        db.add(address)
        await db.commit()
        await db.refresh(address)
        return address
