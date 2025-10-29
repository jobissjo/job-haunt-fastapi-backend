from datetime import datetime
from typing import Optional

from pydantic import BaseModel, ConfigDict, Field

from app.schemas.common import BaseResponseSchema


class BaseUserSchema(BaseModel):
    first_name: str = Field(..., alias="firstName")
    last_name: str = Field(..., alias="lastName")
    email: str = Field(..., alias="email")
    phone_number: str = Field(..., alias="phoneNumber")
    username: str = Field(..., alias="username")
    password: str = Field(..., alias="password")
    role: str = Field(..., alias="role")

    model_config = ConfigDict(populate_by_name=True)


class RegisterUserSchema(BaseUserSchema):
    password: str = Field(..., alias="password")


class UserResponseSchema(BaseUserSchema):
    id: str = Field(default_factory=str, alias="_id")
    model_config = ConfigDict(populate_by_name=True)


class UserListResponse(BaseResponseSchema):
    data: list[UserResponseSchema]


class UserDetailResponse(BaseResponseSchema):
    data: UserResponseSchema


class LoginUserSchema(BaseModel):
    username: str
    password: str


class UserTokenDecodedData(BaseModel):
    id: str
    email: str
    username: str
    role: str
