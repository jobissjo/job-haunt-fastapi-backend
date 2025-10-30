from typing import Literal

from pydantic import BaseModel, ConfigDict, Field

from app.schemas.common import BaseResponseSchema
from app.schemas.job_skill import JobSkillResponse


class UserSkillSchema(BaseModel):
    skill: str
    level: Literal["beginner", "intermediate", "advanced", "expert"]
    confidence: int


class UserSkillResponse(UserSkillSchema):
    id: str = Field(default_factory=str, alias="_id")
    skill_detail: JobSkillResponse
    model_config = ConfigDict(populate_by_name=True)


class UserSkillListResponse(BaseResponseSchema):
    data: list[UserSkillResponse]

    model_config = ConfigDict(populate_by_name=True)


class UserSkillDetailResponse(BaseResponseSchema):
    data: UserSkillResponse

    model_config = ConfigDict(populate_by_name=True)
