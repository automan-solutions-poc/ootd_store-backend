from venv import logger

from fastapi import APIRouter, Depends, BackgroundTasks
from sqlalchemy.ext.asyncio import AsyncSession
from app.db.session import get_db
from app.schemas.auth import Token, Login, PasswordReset, PasswordResetRequest
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

@router.post("/request-password-reset")
async def request_password_reset(
    request_data: PasswordResetRequest,
    background_tasks: BackgroundTasks,
    db: AsyncSession = Depends(get_db)
):
    token = await AuthService.request_password_reset(db, request_data.email)
    # Security fix: Do NOT return the token in the API response.
    # Only send it via background task (e.g., email).
    background_tasks.add_task(EmailService.send_password_reset_token, request_data.email, token)
    # For testing, we can log it on the server side instead.
    logger.info("password_reset_requested", email=request_data.email, token=token)
    return {"message": "If an account with this email exists, a reset token has been sent."}

@router.post("/reset-password")
async def reset_password(
    reset_data: PasswordReset,
    background_tasks: BackgroundTasks,
    db: AsyncSession = Depends(get_db)
):
    user = await AuthService.reset_password(db, reset_data)
    background_tasks.add_task(EmailService.send_password_reset, user.email)
    return {"message": "Password reset successful"}
