from uuid import UUID
from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from app.db.session import get_db
from app.api.deps import get_current_user
from app.models.models import User
from app.services.return_service import ReturnService

router = APIRouter()

@router.post("/{order_id}/request")
async def request_return(order_id: UUID, reason: str, current_user: User = Depends(get_current_user), db: AsyncSession = Depends(get_db)):
    return await ReturnService.request_return(db, order_id, reason)
