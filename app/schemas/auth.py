from enum import Enum

from pydantic import BaseModel, ConfigDict, EmailStr, Field


class UserRole(str, Enum):
    BUSINESS_OWNER = "BUSINESS_OWNER"
    SUPER_ADMIN = "SUPER_ADMIN"
    MANAGER = "MANAGER"
    CUSTOMER = "CUSTOMER"
    CONTENT_CREATOR = "CONTENT_CREATOR"


class RegisterRequest(BaseModel):
    full_name: str = Field(..., min_length=2, max_length=120)
    email: EmailStr
    phone: str | None = None
    password: str = Field(..., min_length=8, max_length=128)
    role: UserRole


class LoginRequest(BaseModel):
    email: EmailStr
    password: str


class TokenResponse(BaseModel):
    access_token: str
    refresh_token: str
    token_type: str = "bearer"


class RefreshRequest(BaseModel):
    refresh_token: str


class UserResponse(BaseModel):
    id: int
    full_name: str
    email: EmailStr
    phone: str | None = None
    role: str
    is_active: bool

    model_config = ConfigDict(from_attributes=True)
