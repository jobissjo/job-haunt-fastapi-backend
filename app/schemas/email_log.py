from typing import Optional
from pydantic import BaseModel, ConfigDict, EmailStr, Field
from app.schemas.user_mail_settings import EmailSettings
from datetime import datetime
from app.schemas.common import BaseResponseSchema


class EmailLog(BaseModel):
    id: str = Field(default_factory=str, alias="_id")
    user_id: str
    email_setting: EmailSettings
    to_email: EmailStr
    subject: str
    body: str
    is_sent: bool
    status: Optional[str] = None
    sent_at: Optional[datetime] = None

    model_config = ConfigDict(populate_by_name=True, from_attributes=True)


class EmailLogListResponse(BaseResponseSchema):
    data: list[EmailLog]

    model_config = ConfigDict(populate_by_name=True)


class EmailLogDetailResponse(BaseResponseSchema):
    data: EmailLog

    model_config = ConfigDict(populate_by_name=True)

class TestEmailSchema(BaseModel):

    to_mail: EmailStr