from datetime import date
from typing import Literal, Optional

from pydantic import BaseModel, ConfigDict, Field

from app.schemas.common import BaseResponseSchema


class LearningStatus(BaseModel):
    name: str
    category: Literal["started", "in_progress", "completed"]
    color: str

    model_config = ConfigDict(populate_by_name=True)


class LearningStatusResponse(LearningStatus):
    id: str = Field(default_factory=str, alias="_id")
    model_config = ConfigDict(populate_by_name=True)


class LearningStatusListResponse(BaseResponseSchema):
    data: list[LearningStatusResponse]

    model_config = ConfigDict(populate_by_name=True)


class LearningStatusDetailResponse(BaseResponseSchema):
    data: LearningStatusResponse

    model_config = ConfigDict(populate_by_name=True)
