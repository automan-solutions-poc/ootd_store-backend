from typing import List
from uuid import UUID
from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from app.db.session import get_db
from app.api.deps import admin_required
from app.schemas.user import UserOut, UserUpdate
from app.services.admin_service import AdminService

router = APIRouter(prefix="/users", dependencies=[admin_required])

@router.get("/", response_model=List[UserOut])
async def get_users(skip: int = 0, limit: int = 100, db: AsyncSession = Depends(get_db)):
    return await AdminService.get_all_users(db, skip=skip, limit=limit)

@router.patch("/{user_id}", response_model=UserOut)
async def update_user(user_id: UUID, user_in: UserUpdate, db: AsyncSession = Depends(get_db)):
    return await AdminService.update_user(db, user_id, user_in)
