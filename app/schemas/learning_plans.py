from datetime import date
from typing import Optional

from pydantic import BaseModel, ConfigDict, Field

from app.schemas.common import BaseResponseSchema


class LearningPlan(BaseModel):
    name: str
    description: Optional[str] = None
    expected_started_date: Optional[date] = Field(
        default=None, alias="expectedStartedDate"
    )
    expected_completed_date: Optional[date] = Field(
        default=None, alias="expectedCompletedDate"
    )
    actual_started_date: Optional[date] = Field(default=None, alias="actualStartedDate")
    actual_completed_date: Optional[date] = Field(
        default=None,
        alias="actualCompletedDate",
    )
    status: str = Field(..., description="Status of the learning plan")
    completed_percentage: Optional[float] = Field(
        default=0.0,
        ge=0,
        le=100,
        description="Completion percentage between 0 and 100",
        alias="completedPercentage",
    )
    model_config = ConfigDict(populate_by_name=True)


class LearningPlanResponse(LearningPlan):
    id: str = Field(default_factory=str, alias="_id")
    model_config = ConfigDict(populate_by_name=True)


class LearningPlanListResponse(BaseResponseSchema):
    data: list[LearningPlanResponse]

    model_config = ConfigDict(populate_by_name=True)


class LearningPlanDetailResponse(BaseResponseSchema):
    data: LearningPlanResponse

    model_config = ConfigDict(populate_by_name=True)
