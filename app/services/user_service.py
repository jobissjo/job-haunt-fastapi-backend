from fastapi import UploadFile
from fastapi.exceptions import HTTPException

from app.repositories.user_repository import UserRepository
from app.schemas.user import (
    LoginUserSchema,
    RegisterUserSchema,
    UpdateUserPasswordSchema,
    UpdateUserProfileSchema,
    UserDetailResponse,
    UserListResponse,
    UserTokenDecodedData,
)
from app.services.cloudinary import CloudinaryService
from app.services.common import CommonService


class UserService:
    def __init__(self):
        self.repository = UserRepository()

    async def register_user(self, user: RegisterUserSchema):
        username_exists = await self.repository.get_user_by_username(user.username)
        if username_exists:
            raise HTTPException(status_code=400, detail="Username already exists")
        email_exists = await self.repository.get_user_by_email(user.email)
        if email_exists:
            raise HTTPException(status_code=400, detail="Email already exists")
        phone_number_exists = await self.repository.get_user_by_phone_number(
            user.phone_number
        )
        if phone_number_exists:
            raise HTTPException(status_code=400, detail="Phone number already exists")
        hashed_password = await CommonService.hash_password(user.password)
        user.password = hashed_password
        user = await self.repository.create_user(user)
        return {"success": True, "message": "User registered successfully"}

    async def login_user(self, user_data: LoginUserSchema):
        username, email, phone_number = await CommonService.decide_email_username_phone(
            user_data.username
        )
        user = await self.repository.get_user_by_username_email_phone(
            username, email, phone_number
        )
        if not user:
            raise HTTPException(status_code=404, detail="User not found")
        if not await CommonService.verify_password(
            user_data.password, user["password"]
        ):
            raise HTTPException(status_code=401, detail="Incorrect password")
        access_token = await CommonService.create_access_token(
            {
                "id": user["_id"],
                "email": user["email"],
                "username": user["username"],
                "role": user["role"],
            }
        )
        refresh_token = await CommonService.create_refresh_token({"id": user["_id"]})
        user["id"] = str(user["_id"])
        return {
            "data": {
                "access_token": access_token,
                "refresh_token": refresh_token,
                "role": user["role"],
                "user": user,
            },
            "success": True,
            "message": "User logged in successfully",
        }

    async def get_users(self) -> UserListResponse:
        user_response = await self.repository.get_users()
        return {
            "success": True,
            "data": user_response,
            "message": "Users retrieved successfully",
        }

    async def get_user_by_id(self, user_id):
        data = await self.repository.get_user_by_id(user_id)
        return {"success": True, "data": data, "message": "User retrieved successfully"}

    async def get_user_by_email(self, email):
        return await self.repository.get_user_by_email(email)

    async def update_user(self, user_id: str, user: UpdateUserProfileSchema):
        return await self.repository.update_user(user_id, user)

    async def delete_user(self, user_id):
        return await self.repository.delete_user(user_id)

    async def update_user_password(
        self, user_data: UserTokenDecodedData, passwordData: UpdateUserPasswordSchema
    ):
        user = await self.repository.get_user_by_id(user_data.id)
        if not await CommonService.verify_password(
            passwordData.old_password, user["password"]
        ):
            return {"success": False, "message": "Incorrect password"}
        hashed_password = await CommonService.hash_password(passwordData.new_password)

        await self.repository.update_user_password(user_data.id, hashed_password)
        return {"success": True, "message": "Password updated successfully"}

    async def update_user_resume(self, user_id: str, resume: UploadFile):
        cloudinary_service = CloudinaryService()
        resume_url_info = await cloudinary_service.upload_document(resume)
        await self.repository.update_user_resume(user_id, resume_url_info["url"])
        return {
            "success": True,
            "message": "Resume updated successfully",
            "data": {"resume": resume_url_info["url"]},
        }

    async def update_user_profile_picture(
        self, user_id: str, profile_picture: UploadFile
    ):
        cloudinary_service = CloudinaryService()
        profile_picture_url_info = await cloudinary_service.upload_document(
            profile_picture
        )
        await self.repository.update_user_profile_picture(
            user_id, profile_picture_url_info["url"]
        )
        return {
            "success": True,
            "message": "Profile picture updated successfully",
            "data": {"profile_picture": profile_picture_url_info["url"]},
        }

    async def update_user_cover_picture(self, user_id: str, cover_picture: UploadFile):
        cloudinary_service = CloudinaryService()
        cover_picture_url_info = await cloudinary_service.upload_image(cover_picture)
        await self.repository.update_user_cover_picture(
            user_id, cover_picture_url_info["url"]
        )
        return {
            "success": True,
            "message": "Cover picture updated successfully",
            "data": {"cover_picture": cover_picture_url_info["url"]},
        }
