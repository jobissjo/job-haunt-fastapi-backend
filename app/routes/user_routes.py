from fastapi import APIRouter, Depends

from app.repositories.user_repository import UserRepository
from app.schemas.user import (
    LoginUserSchema,
    RegisterUserSchema,
    UserListResponse,
    UserTokenDecodedData,
    UpdateUserProfileSchema,
    UpdateUserPasswordSchema,
    TokenResponseSchema,
)
from app.services.user_service import UserService
from app.services.common import CommonService
from fastapi import File, UploadFile
from app.schemas.common import BaseResponseSchema


router = APIRouter(prefix="/users", tags=["Users"])


@router.post("/")
async def register_user(
    user: RegisterUserSchema, service: UserService = Depends(UserService)
)->BaseResponseSchema:
    return await service.register_user(user)


@router.get("/")
async def get_users(service: UserService = Depends(UserService)) -> UserListResponse:
    return await service.get_users()


@router.post("/login/")
async def login_user(
    user: LoginUserSchema, service: UserService = Depends(UserService)
)->TokenResponseSchema:
    return await service.login_user(user)

@router.get("/me/")
async def get_me(
    service: UserService = Depends(UserService),
    user_data: UserTokenDecodedData = Depends(CommonService.verify_token_get_user),
    ):
    return await service.get_user_by_id(user_data.id)

@router.put("/update-profile/")
async def update_user_profile(
    update_data: UpdateUserProfileSchema,
    service: UserService = Depends(UserService),
    user_data: UserTokenDecodedData = Depends(CommonService.verify_token_get_user),
    ):
    return await service.update_user(user_data.id, update_data)


@router.post("/change-password/")
async def update_user_password(
    update_data: UpdateUserPasswordSchema,
    service: UserService = Depends(UserService),
    user_data: UserTokenDecodedData = Depends(CommonService.verify_token_get_user),
    ):
    return await service.update_user_password(user_data, update_data)


@router.put("/upload-resume/")
async def update_user_resume(
    resume: UploadFile = File(...),
    service: UserService = Depends(UserService),
    user_data: UserTokenDecodedData = Depends(CommonService.verify_token_get_user),
    ):
    return await service.update_user_resume(user_data.id, resume)

@router.put("/upload-profile-picture/")
async def update_user_profile_picture(
    profile_picture: UploadFile = File(...),
    service: UserService = Depends(UserService),
    user_data: UserTokenDecodedData = Depends(CommonService.verify_token_get_user),
    ):
    return await service.update_user_profile_picture(user_data.id, profile_picture)

@router.put("/upload-cover-picture/")
async def update_user_cover_picture(
    cover_picture: UploadFile = File(...),
    service: UserService = Depends(UserService),
    user_data: UserTokenDecodedData = Depends(CommonService.verify_token_get_user),
    ):
    return await service.update_user_cover_picture(user_data.id, cover_picture)


