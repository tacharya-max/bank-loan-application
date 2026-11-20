
from pydantic import BaseModel, EmailStr, Field


# Signup Request Schema
class UserSignup(BaseModel):

    full_name: str = Field(
        min_length=2,
        max_length=100
    )

    email: EmailStr

    phone: str | None = Field(
        default=None,
        max_length=15
    )

    password: str = Field(
        min_length=8
    )


# User Response Schema
class UserResponse(BaseModel):

    model_config = {"from_attributes": True}

    id: int
    full_name: str
    email: EmailStr
    phone: str | None
    role: str
    is_active: bool


class UserLogin(BaseModel):
    email: EmailStr
    password: str


class TokenResponse(BaseModel):
    access_token: str
    refresh_token: str
    token_type: str = "bearer"    

class RefreshTokenRequest(BaseModel):
    refresh_token: str   

class LogoutRequest(BaseModel):
    refresh_token: str     