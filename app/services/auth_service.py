import secrets
import hashlib
from datetime import datetime, timedelta, timezone
from sqlalchemy import select, delete
from sqlalchemy.ext.asyncio import AsyncSession
from app.core import security
from app.models.models import User, PasswordResetToken
from app.schemas.auth import Login, PasswordReset
from app.schemas.user import UserCreate
from app.utils.exceptions import UnauthorizedException, NotFoundException, BadRequestException

class AuthService:
    @staticmethod
    async def authenticate(db: AsyncSession, login_data: Login):
        result = await db.execute(select(User).where(User.email == login_data.email))
        user = result.scalar_one_or_none()
        if not user or not security.verify_password(login_data.password, user.password_hash):
            raise UnauthorizedException("Incorrect email or password")
        if not user.is_active:
            raise UnauthorizedException("Inactive user")

        access_token = security.create_access_token(subject=user.id)
        return {"access_token": access_token, "token_type": "bearer"}

    @staticmethod
    async def register(db: AsyncSession, user_in: UserCreate):
        result = await db.execute(select(User).where(User.email == user_in.email))
        if result.scalar_one_or_none():
            raise BadRequestException("User with this email already exists")

        # Security fix: Force role to CUSTOMER for public registration
        db_user = User(
            email=user_in.email,
            password_hash=security.get_password_hash(user_in.password),
            role=User.role.type.enums[1] if hasattr(User.role.type, 'enums') else "CUSTOMER"
        )
        # Using a safer way to assign CUSTOMER role
        from app.models.models import UserRole
        db_user.role = UserRole.CUSTOMER

        db.add(db_user)
        await db.commit()
        await db.refresh(db_user)
        return db_user

    @staticmethod
    async def request_password_reset(db: AsyncSession, email: str):
        result = await db.execute(select(User).where(User.email == email))
        user = result.scalar_one_or_none()
        if not user:
            # We don't want to leak if the email exists, but we'll return the token for this implementation
            # In a real app, you might just return success regardless.
            raise NotFoundException("User not found")

        token = secrets.token_urlsafe(32)
        token_hash = hashlib.sha256(token.encode()).hexdigest()

        reset_token = PasswordResetToken(
            user_id=user.id,
            token_hash=token_hash,
            expires_at=datetime.now(timezone.utc) + timedelta(minutes=15)
        )
        db.add(reset_token)
        await db.commit()
        return token

    @staticmethod
    async def reset_password(db: AsyncSession, reset_data: PasswordReset):
        token_hash = hashlib.sha256(reset_data.token.encode()).hexdigest()

        result = await db.execute(
            select(PasswordResetToken)
            .where(PasswordResetToken.token_hash == token_hash)
            .where(PasswordResetToken.expires_at > datetime.now(timezone.utc))
        )
        token_entry = result.scalar_one_or_none()
        if not token_entry:
            raise BadRequestException("Invalid or expired reset token")

        result = await db.execute(select(User).where(User.id == token_entry.user_id))
        user = result.scalar_one_or_none()
        if not user:
            raise NotFoundException("User not found")

        user.password_hash = security.get_password_hash(reset_data.new_password)

        # Single-use: delete the token
        await db.delete(token_entry)
        await db.commit()
        return user
