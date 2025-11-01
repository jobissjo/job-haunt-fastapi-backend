from datetime import datetime
from typing import List, Optional

from pydantic import BaseModel, ConfigDict, Field

from app.schemas.common import BaseResponseSchema


class JobPreferenceBase(BaseModel):
    job_title: Optional[str] = Field(None, example="Software Engineer")
    preferred_locations: Optional[List[str]] = Field(
        default_factory=list, example=["Chennai", "Bangalore"]
    )
    employment_type: Optional[str] = Field(
        None, example="Full-time"
    )  # Full-time / Part-time / Remote
    salary_expectation: Optional[str] = Field(None, example="6-8 LPA")
    experience_level: Optional[str] = Field(None, example="Mid-level")


class JobPreferenceSchemaCreate(JobPreferenceBase):
    pass


class JobPreferenceSchemaUpdate(JobPreferenceBase):
    pass


class JobPreferenceResponse(JobPreferenceBase):
    id: str = Field(..., alias="_id")
    user_id: str
    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(populate_by_name=True)


class JobPreferenceDetailResponse(BaseResponseSchema):
    data: JobPreferenceResponse
