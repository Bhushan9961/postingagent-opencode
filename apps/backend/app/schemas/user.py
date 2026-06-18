from datetime import datetime

from pydantic import BaseModel, EmailStr


class UserCreate(BaseModel):
    email: EmailStr
    password: str
    full_name: str
    role: str = "viewer"


class UserRead(BaseModel):
    id: int
    email: str
    full_name: str
    role: str
    is_active: bool
    created_at: datetime

    model_config = {"from_attributes": True}


class UserUpdate(BaseModel):
    full_name: str | None = None
    role: str | None = None
    is_active: bool | None = None


class TokenResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"


class LoginRequest(BaseModel):
    email: EmailStr
    password: str
