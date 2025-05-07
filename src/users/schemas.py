from datetime import datetime
from uuid import UUID

from pydantic import BaseModel, ConfigDict, EmailStr, field_validator


class CreateUserRequestDto(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    first_name: str
    last_name: str
    email: EmailStr
    password: str

    @field_validator("password")
    @classmethod
    def validate_password(cls, value: str) -> str:
        if len(value) < 8 or len(value) > 32:
            raise ValueError("Password must be between 8 and 32 characters long.")
        if not any(char.isupper() for char in value):
            raise ValueError("Password must contain at least one uppercase letter.")
        if not any(char.islower() for char in value):
            raise ValueError("Password must contain at least one lowercase letter.")
        if not any(char.isdigit() for char in value):
            raise ValueError("Password must contain at least one number.")
        if not any(char in "@$!%*?&" for char in value):
            raise ValueError("Password must contain at least one special character (@$!%*?&).")
        return value


class CreateUserResponseDto(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: UUID
    message: str


class LoginRequestDto(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    email: EmailStr
    password: str


class LoginResponseDto(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    access_token: str
    token_type: str


class GetUserResponseDto(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: UUID
    first_name: str
    last_name: str
    email: EmailStr
    created_at: datetime
