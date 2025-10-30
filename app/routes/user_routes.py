from fastapi import APIRouter, Depends

from app.repositories.user_repository import UserRepository
from app.schemas.user import LoginUserSchema, RegisterUserSchema, UserListResponse
from app.services.user_service import UserService

router = APIRouter(prefix="/users", tags=["Users"])


@router.post("/")
async def register_user(
    user: RegisterUserSchema, service: UserService = Depends(UserService)
):
    return await service.register_user(user)


@router.get("/")
async def get_users(service: UserService = Depends(UserService)) -> UserListResponse:
    return await service.get_users()


@router.post("/login/")
async def login_user(
    user: LoginUserSchema, service: UserService = Depends(UserService)
):
    return await service.login_user(user)
