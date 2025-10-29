from typing import Literal

from pydantic import BaseModel, ConfigDict, Field

from app.schemas.common import BaseResponseSchema


class BaseJobStatus(BaseModel):
    name: str
    category: Literal["open", "applied", "interview", "offer", "rejected"]
    color: str

    model_config = ConfigDict(populate_by_name=True)


class JobStatusResponse(BaseJobStatus):
    id: str = Field(default_factory=str, alias="_id")
    model_config = ConfigDict(populate_by_name=True)


class JobStatusListResponse(BaseResponseSchema):
    data: list[JobStatusResponse]

    model_config = ConfigDict(populate_by_name=True)


class JobStatusDetailResponse(BaseResponseSchema):
    data: JobStatusResponse

    model_config = ConfigDict(populate_by_name=True)
