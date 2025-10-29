from typing import Optional

from pydantic import BaseModel, EmailStr, Field


class EmailSettings(BaseModel):
    from_email: EmailStr = Field(..., description="Email address to send from")
    username: str = Field(..., description="Email username")
    password: str = Field(..., description="Email password")
    use_tls: bool = Field(default=False, description="Enable TLS encryption")
    use_ssl: bool = Field(default=False, description="Enable SSL encryption")
    host: str = Field(..., description="Email server host")
    port: int = Field(ge=1, le=65535, description="Valid email server port (1–65535)")
    is_active: bool = True

    model_config = ConfigDict(populate_by_name=True)


class EmailSettingsResponse(EmailSettings):
    id: str = Field(default_factory=str, alias="_id")
    model_config = ConfigDict(populate_by_name=True)


class EmailSettingsListResponse(BaseResponseSchema):
    data: list[EmailSettingsResponse]

    model_config = ConfigDict(populate_by_name=True)


class EmailSettingsDetailResponse(BaseResponseSchema):
    data: EmailSettingsResponse

    model_config = ConfigDict(populate_by_name=True)
