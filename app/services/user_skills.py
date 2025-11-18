from app.repositories.job_skills import JobSkillRepository
from app.repositories.user_skills import UserSkillRepository
from app.schemas.user_skills import (
    BaseResponseSchema,
    UserSkillDetailResponse,
    UserSkillListResponse,
    UserSkillSchema,
)
from app.services.activity_log_service import ActivityLogService
from app.schemas.activity_log_schema import ActivityLogSchema


class UserSkillService:
    def __init__(self):
        self.repository = UserSkillRepository()
        self.activity_log_service = ActivityLogService()
        self.skill_repository = JobSkillRepository()

    async def create_user_skill(
        self, user_skill: UserSkillSchema, user_id: str
    ) -> BaseResponseSchema:
        await self.repository.create_user_skill(user_skill, user_id)
        skill = await self.skill_repository.get_job_skill_by_id(user_skill.skill)
        if skill:
            skill_name = skill.get('name')
            await self.activity_log_service.create_activity_log(user_id, ActivityLogSchema(**{
                "type": "skill",
                "message": f"Added new skill {skill_name}"
            }))
        return {"message": "User skill created successfully", "success": True}

    async def get_user_skills(self, user_id: str) -> UserSkillListResponse:
        data = await self.repository.get_user_skills(user_id)
        return {
            "data": data,
            "message": "User skills fetched successfully",
            "success": True,
        }

    async def get_user_skill_by_id(self, user_skill_id: str) -> UserSkillDetailResponse:
        data = await self.repository.get_user_skill_by_id(user_skill_id)
        return {
            "data": data,
            "message": "User skill fetched successfully",
            "success": True,
        }

    async def update_user_skill(
        self, user_skill_id: str, user_skill: UserSkillSchema
    ) -> BaseResponseSchema:
        await self.repository.update_user_skill(user_skill_id, user_skill)
        return {"message": "User skill updated successfully", "success": True}

    async def delete_user_skill(self, user_skill_id: str) -> BaseResponseSchema:
        await self.repository.delete_user_skill(user_skill_id)
        return {"message": "User skill deleted successfully", "success": True}
