from fastapi import APIRouter, Depends, Query
from sqlalchemy.ext.asyncio import AsyncSession
from app.db.session import get_db
from app.api.deps import admin_required
from app.schemas.analytics import AnalyticsOut, AnalyticsRevenueOut
from app.services.admin_service import AdminService

router = APIRouter(prefix="/analytics", dependencies=[admin_required])

@router.get("/", response_model=AnalyticsOut)
async def get_analytics(db: AsyncSession = Depends(get_db)):
    return await AdminService.get_analytics(db)

@router.get("/revenue", response_model=AnalyticsRevenueOut)
async def get_revenue_by_date(
    start_date: str,
    end_date: str,
    db: AsyncSession = Depends(get_db)
):
    revenue_data = await AdminService.get_revenue_by_date(db, start_date, end_date)
    return {"revenue_by_date": revenue_data}
