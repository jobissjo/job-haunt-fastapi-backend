from datetime import date
from typing import List, Literal, Optional

from pydantic import BaseModel, ConfigDict, EmailStr, Field, HttpUrl

from app.schemas.common import BaseResponseSchema
from app.schemas.job_skill import JobSkillResponse
from app.schemas.job_status import JobStatusResponse


class JobApplicationSchema(BaseModel):
    position: str
    company_name: str
    location: Optional[str] = None
    applied_date: Optional[date] = None
    status: str = Field(description="Application status reference id")
    skills: List[str] = Field(default_factory=list, description="List of skill IDs")
    preferred_skills: List[str] = Field(
        default_factory=list, description="List of preferred skill IDs"
    )
    description: Optional[str] = None
    required_experience: Optional[int] = Field(
        default=0, ge=0, le=100, description="Years of experience required"
    )
    contact_mail: Optional[EmailStr] = None
    job_posted_date: Optional[date] = None
    job_closed_date: Optional[date] = None
    application_through: Literal[
        "email", "website", "referral", "other", "linkedin"
    ] = Field(default="email", description="Medium of application")
    application_url: Optional[HttpUrl] = Field(
        None, description="URL to apply or reference link"
    )

    model_config = ConfigDict(populate_by_name=True)


class JobApplicationResponse(JobApplicationSchema):
    id: str = Field(default_factory=str, alias="_id")
    status_detail: Optional[JobStatusResponse] = None
    skills_detail: Optional[List[JobSkillResponse]] = None
    preferred_skills_detail: Optional[List[JobSkillResponse]] = None
    model_config = ConfigDict(populate_by_name=True)


class JobApplicationListResponse(BaseResponseSchema):
    data: list[JobApplicationResponse]

    model_config = ConfigDict(populate_by_name=True)


class JobApplicationDetailResponse(BaseResponseSchema):
    data: JobApplicationResponse

    model_config = ConfigDict(populate_by_name=True)
