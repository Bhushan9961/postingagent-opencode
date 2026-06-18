from datetime import UTC, datetime, timedelta
from typing import Annotated

import bcrypt as _bcrypt
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError, jwt
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.config.config import settings
from app.core.database import get_db
from app.models.user import User

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/login", auto_error=False)


class Role:
    ADMIN = "admin"
    MANAGER = "manager"
    REVIEWER = "content_reviewer"
    VIEWER = "viewer"


ROLE_HIERARCHY = {
    Role.ADMIN: 100,
    Role.MANAGER: 80,
    Role.REVIEWER: 60,
    Role.VIEWER: 40,
}


def verify_password(plain_password: str, hashed_password: str) -> bool:
    return _bcrypt.checkpw(plain_password.encode(), hashed_password.encode())


def hash_password(password: str) -> str:
    return _bcrypt.hashpw(password.encode(), _bcrypt.gensalt()).decode()


def create_access_token(user_id: int, role: str) -> str:
    expire = datetime.now(UTC) + timedelta(
        minutes=settings.access_token_expire_minutes
    )
    payload = {
        "sub": str(user_id),
        "role": role,
        "exp": expire,
    }
    return jwt.encode(payload, settings.jwt_secret, algorithm=settings.jwt_algorithm)


def decode_access_token(token: str) -> dict:
    try:
        payload = jwt.decode(
            token, settings.jwt_secret, algorithms=[settings.jwt_algorithm]
        )
        return payload
    except JWTError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid token",
        )


async def get_current_user(
    token: Annotated[str, Depends(oauth2_scheme)],
    db: Annotated[AsyncSession, Depends(get_db)],
) -> User:
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
    )
    if token is None:
        raise credentials_exception
    payload = decode_access_token(token)
    user_id = payload.get("sub")
    if user_id is None:
        raise credentials_exception
    result = await db.execute(select(User).where(User.id == int(user_id)))
    user = result.scalar_one_or_none()
    if user is None or not user.is_active:
        raise credentials_exception
    return user


def require_role(min_role: str):
    async def role_checker(current_user: User = Depends(get_current_user)):
        if ROLE_HIERARCHY.get(current_user.role, 0) < ROLE_HIERARCHY.get(min_role, 0):
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Insufficient permissions",
            )
        return current_user

    return role_checker
