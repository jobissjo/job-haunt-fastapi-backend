from pydantic import BaseModel, ConfigDict, Field

from app.schemas.common import BaseResponseSchema


class JobSkillSchema(BaseModel):
    name: str

    model_config = ConfigDict(populate_by_name=True)


class JobSkillResponse(JobSkillSchema):
    id: str = Field(default_factory=str, alias="_id")

    model_config = ConfigDict(populate_by_name=True)


class JobSkillListResponse(BaseResponseSchema):
    data: list[JobSkillResponse]

    model_config = ConfigDict(populate_by_name=True)


class JobSkillDetailResponse(BaseResponseSchema):
    data: JobSkillResponse

    model_config = ConfigDict(populate_by_name=True)
