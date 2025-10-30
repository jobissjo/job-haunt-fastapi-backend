from pydantic import BaseModel, ConfigDict, Field
from app.schemas.common import BaseResponseSchema
from typing import Optional

class NotificationPreference(BaseModel):
    email: bool = True
    push: bool = True
    in_app: bool = True

    model_config = ConfigDict(populate_by_name=True)

class NotificationPreferenceUpdate(NotificationPreference):
    email: Optional[bool] = None
    push: Optional[bool] = None
    in_app: Optional[bool] = None


class NotificationPreferenceResponse(NotificationPreference):
    id: str = Field(default_factory=str, alias="_id")
    model_config = ConfigDict(populate_by_name=True)




class NotificationPreferenceDetailResponse(BaseResponseSchema):
    data: NotificationPreferenceResponse

    model_config = ConfigDict(populate_by_name=True)
