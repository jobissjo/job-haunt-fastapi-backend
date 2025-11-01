from typing import Optional

from pydantic import BaseModel, ConfigDict, EmailStr, Field

from app.schemas.common import BaseResponseSchema


class EmailSettings(BaseModel):
    from_email: EmailStr = Field(..., description="Email address to send from")
    username: str = Field(..., description="Email username")
    password: str = Field(..., description="Email password")
    use_tls: bool = Field(default=True, description="Enable TLS encryption")
    use_ssl: bool = Field(default=False, description="Enable SSL encryption")
    host: str = Field(..., description="Email server host")
    port: int = Field(ge=1, le=65535, description="Valid email server port (1–65535)")
    is_active: bool = Field(
        default=False, description="Whether this email setting is active"
    )

    model_config = ConfigDict(populate_by_name=True)


class EmailSettingsUpdate(BaseModel):
    from_email: Optional[EmailStr] = Field(
        None, description="Email address to send from"
    )
    username: Optional[str] = Field(None, description="Email username")
    password: Optional[str] = Field(None, description="Email password")
    use_tls: Optional[bool] = Field(None, description="Enable TLS encryption")
    use_ssl: Optional[bool] = Field(None, description="Enable SSL encryption")
    host: Optional[str] = Field(None, description="Email server host")
    port: Optional[int] = Field(
        None, ge=1, le=65535, description="Valid email server port (1–65535)"
    )
    is_active: Optional[bool] = Field(
        None, description="Whether this email setting is active"
    )

    model_config = ConfigDict(populate_by_name=True)


class EmailSettingsResponse(BaseModel):
    id: str = Field(default_factory=str, alias="_id")
    user_id: str
    from_email: EmailStr
    username: str
    password: str
    use_tls: bool
    use_ssl: bool
    host: str
    port: int
    is_active: bool

    model_config = ConfigDict(populate_by_name=True, from_attributes=True)


class EmailSettingsListResponse(BaseResponseSchema):
    data: list[EmailSettingsResponse]

    model_config = ConfigDict(populate_by_name=True)


class EmailSettingsDetailResponse(BaseResponseSchema):
    data: EmailSettingsResponse

    model_config = ConfigDict(populate_by_name=True)
