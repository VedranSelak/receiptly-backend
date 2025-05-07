from datetime import datetime, timedelta, timezone
from typing import Annotated

import jwt
from fastapi import Depends
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from src.config.session import get_db_session
from src.config.settings import settings
from src.users.exceptions import InvalidCredentialsException, UserAlreadyExistsException, UserNotFoundException
from src.users.models import User
from src.users.password_hash_helper import PasswordHashHelper
from src.users.schemas import CreateUserRequestDto, CreateUserResponseDto, GetUserResponseDto, LoginResponseDto


class UserService:
    def __init__(self, session: Annotated[AsyncSession, Depends(get_db_session)]):
        self.session = session

    async def create_user(self, user_data: CreateUserRequestDto) -> CreateUserResponseDto:
        db_user = (await self.session.execute(select(User).where(User.email == user_data.email))).scalars().first()
        if db_user:
            raise UserAlreadyExistsException()

        new_user = User(
            first_name=user_data.first_name,
            last_name=user_data.last_name,
            email=user_data.email,
            password=PasswordHashHelper.get_password_hash(user_data.password),
        )
        self.session.add(new_user)
        await self.session.commit()
        await self.session.refresh(new_user)

        return CreateUserResponseDto(id=new_user.id, message="User successfuly signed up!")

    async def login_user(self, credentials: OAuth2PasswordRequestForm) -> LoginResponseDto:
        db_user = (await self.session.execute(select(User).where(User.email == credentials.username))).scalars().first()
        if not db_user:
            raise UserNotFoundException()

        if not PasswordHashHelper.verify_password(credentials.password, db_user.password):
            raise InvalidCredentialsException()

        expires = int((datetime.now(timezone.utc) + timedelta(minutes=5)).timestamp())
        payload = {"id": str(db_user.id), "sub": db_user.email, "expires": expires}

        token = jwt.encode(payload, settings.JWT_SECRET, algorithm=settings.JWT_ALGORITHM)

        return LoginResponseDto(access_token=token, token_type="bearer")

    async def get_me(self, user_id: int) -> GetUserResponseDto:
        db_user = (await self.session.execute(select(User).where(User.id == user_id))).scalars().first()

        if not db_user:
            raise UserNotFoundException()

        return GetUserResponseDto.model_validate(db_user)
