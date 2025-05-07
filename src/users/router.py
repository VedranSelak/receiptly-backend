from typing import Annotated

from fastapi import APIRouter, Depends
from fastapi.security import OAuth2PasswordRequestForm

from src.common.dependencies import get_current_user
from src.common.schemas import TokenData
from src.users.schemas import CreateUserRequestDto, CreateUserResponseDto, LoginResponseDto
from src.users.service import UserService

router = APIRouter(
    prefix="/users",
    tags=["users"],
    responses={404: {"description": "Not found"}},
)


@router.post("/sign-up", status_code=201, response_model=CreateUserResponseDto)
async def create_user(new_user: CreateUserRequestDto, service: Annotated[UserService, Depends()]):
    return await service.create_user(new_user)


@router.post("/login", status_code=201, response_model=LoginResponseDto)
async def login_user(
    credentials: Annotated[OAuth2PasswordRequestForm, Depends()], service: Annotated[UserService, Depends()]
):
    return await service.login_user(credentials)


@router.get("/me", status_code=200)
async def get_me(
    current_user: Annotated[TokenData, Depends(get_current_user)], service: Annotated[UserService, Depends()]
):
    return await service.get_me(current_user.id)
