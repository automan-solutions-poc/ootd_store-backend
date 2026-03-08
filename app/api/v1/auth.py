from fastapi import APIRouter, Depends, BackgroundTasks
from sqlalchemy.ext.asyncio import AsyncSession
from app.db.session import get_db
from app.schemas.auth import Token, Login, PasswordReset
from app.schemas.user import UserOut, UserCreate
from app.services.auth_service import AuthService
from app.services.email_service import EmailService

router = APIRouter()

@router.post("/login", response_model=Token)
async def login(login_data: Login, db: AsyncSession = Depends(get_db)):
    return await AuthService.authenticate(db, login_data)

@router.post("/register", response_model=UserOut)
async def register(user_in: UserCreate, db: AsyncSession = Depends(get_db)):
    return await AuthService.register(db, user_in)

@router.post("/reset-password")
async def reset_password(
    reset_data: PasswordReset,
    background_tasks: BackgroundTasks,
    db: AsyncSession = Depends(get_db)
):
    user = await AuthService.reset_password(db, reset_data)
    background_tasks.add_task(EmailService.send_password_reset, user.email)
    return {"message": "Password reset successful"}
