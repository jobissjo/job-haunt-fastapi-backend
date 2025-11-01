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


class SocialLinksSchema(BaseModel):
    linkedin: Optional[str] = None
    twitter: Optional[str] = None
    facebook: Optional[str] = None
    instagram: Optional[str] = None


class Profile(BaseModel):
    bio: Optional[str] = None
    profile_picture: Optional[str] = None
    cover_picture: Optional[str] = None
    resume: Optional[str] = None


class NotificationPreference(BaseModel):
    email: bool = True
    sms: bool = True
    push: bool = True


class UserSchemaResponse(BaseUserSchema):
    id: str = Field(default_factory=str, alias="_id")
    # password = Field(exclude=True)
    # profile: Profile = Field(..., alias="profile")
    # social_links: Optional[str] = None
    model_config = ConfigDict(populate_by_name=True, exclude={"password"})


class UpdateUserProfileSchema(BaseUserSchema):
    social_links: SocialLinksSchema
    profile: Profile


class UserResponseSchema(BaseUserSchema):
    id: str = Field(default_factory=str, alias="_id")
    profile: Profile = Field(..., alias="profile")
    social_links: Optional[str] = None
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


class UpdateUserPasswordSchema(BaseModel):
    old_password: str
    new_password: str
    new_password_confirm: str


class TokenResponseSchema(BaseModel):
    access_token: str
    refresh_token: str
    user: UserSchemaResponse

class TokenDetailResponseSchema(BaseResponseSchema):
    data: TokenResponseSchema
