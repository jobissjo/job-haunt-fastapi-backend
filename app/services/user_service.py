from app.repositories.user_repository import UserRepository
from app.schemas.user import (LoginUserSchema, RegisterUserSchema,
                              UserDetailResponse, UserListResponse)
from app.services.common import CommonService


class UserService:
    def __init__(self):
        self.repository = UserRepository()

    async def register_user(self, user: RegisterUserSchema):
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
            return {"success": False, "message": "User not found"}
        if not await CommonService.verify_password(
            user_data.password, user["password"]
        ):
            return {"success": False, "message": "Incorrect password"}
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
        return await self.repository.get_user_by_id(user_id)

    async def get_user_by_email(self, email):
        return await self.repository.get_user_by_email(email)

    async def update_user(self, user_id, user):
        return await self.repository.update_user(user_id, user)

    async def delete_user(self, user_id):
        return await self.repository.delete_user(user_id)

    async def update_user_password(self, user_id, password):
        return await self.repository.update_user_password(user_id, password)
