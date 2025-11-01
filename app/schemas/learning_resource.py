from datetime import date
from typing import Literal, Optional

from pydantic import BaseModel, ConfigDict, Field

from app.schemas.common import BaseResponseSchema


class LearningResource(BaseModel):
    name: str
    resource_type: Literal[
        "video", "document", "quiz", "link", "article", "course", "other"
    ] = Field(..., description="Type of learning resource")
    resource_url: Optional[str] = Field(
        None, description="URL or file path for the resource"
    )
    learning_management: str = Field(
        ..., description="Related learning management ID or reference"
    )
    status: str = Field(..., description="Learning Status reference id")
    expected_started_date: Optional[date] = None
    expected_completed_date: Optional[date] = None
    actual_started_date: Optional[date] = None
    actual_completed_date: Optional[date] = None
    description: Optional[str] = None
    completed_percentage: Optional[int] = Field(
        default=0, ge=0, le=100, description="Completion percentage between 0 and 100"
    )

    model_config = ConfigDict(populate_by_name=True)


class LearningResourceResponse(LearningResource):
    id: str = Field(default_factory=str, alias="_id")
    model_config = ConfigDict(populate_by_name=True)


class LearningResourceListResponse(BaseResponseSchema):
    data: list[LearningResourceResponse]

    model_config = ConfigDict(populate_by_name=True)


class LearningResourceDetailResponse(BaseResponseSchema):
    data: LearningResourceResponse

    model_config = ConfigDict(populate_by_name=True)
