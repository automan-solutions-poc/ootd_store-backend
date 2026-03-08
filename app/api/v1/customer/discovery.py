from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from app.db.session import get_db
from app.services.category_service import CategoryService
from app.services.search_service import SearchService

router = APIRouter()

@router.get("/categories")
async def list_categories(db: AsyncSession = Depends(get_db)):
    return await CategoryService.get_categories(db)

@router.get("/search")
async def search(q: str = None, category: str = None, db: AsyncSession = Depends(get_db)):
    return await SearchService.search_products(db, query=q, category_slug=category)
