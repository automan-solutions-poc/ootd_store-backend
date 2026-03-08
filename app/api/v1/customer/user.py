from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from app.db.session import get_db
from app.api.deps import get_current_user
from app.models.models import User
from app.services.user_service import UserService
from app.schemas.user import UserOut

router = APIRouter()

@router.get("/profile", response_model=UserOut)
async def get_profile(current_user: User = Depends(get_current_user), db: AsyncSession = Depends(get_db)):
    return await UserService.get_profile(db, current_user.id)

@router.post("/address")
async def add_address(address_data: dict, current_user: User = Depends(get_current_user), db: AsyncSession = Depends(get_db)):
    return await UserService.add_address(db, current_user.id, address_data)
