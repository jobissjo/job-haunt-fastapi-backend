from pydantic import BaseModel, ConfigDict, Field

from app.schemas.common import BaseResponseSchema


class AdminStats(BaseModel):
    total_users: int = Field(alias="totalUsers")
    total_skills: int = Field(alias="totalSkills")
    total_statuses: int = Field(alias="totalStatuses")
    recent_activity: int = Field(alias="recentActivity")

    model_config = ConfigDict(populate_by_name=True)


class AdminStatsResponse(BaseResponseSchema):
    data: AdminStats
