from app.repositories.job_skills import JobSkillRepository
from app.schemas.job_skill import (JobSkillDetailResponse,
                                   JobSkillListResponse, JobSkillResponse,
                                   JobSkillSchema)


class JobSkillService:
    def __init__(self):
        self.repository = JobSkillRepository()

    async def get_job_skills(self) -> JobSkillListResponse:
        documents = await self.repository.get_job_skills()
        return {
            "success": True,
            "data": documents,
            "message": "Job skills retrieved successfully",
        }

    async def get_job_skill_by_id(self, job_skill_id) -> JobSkillDetailResponse:
        document = await self.repository.get_job_skill_by_id(job_skill_id)
        return {
            "success": True,
            "data": document,
            "message": "Job skill retrieved successfully",
        }

    async def create_job_skill(self, job_skill: JobSkillSchema):
        await self.repository.create_job_skill(job_skill)
        return {"success": True, "message": "Job skill created successfully"}

    async def update_job_skill(self, job_skill_id, job_skill: JobSkillSchema):
        await self.repository.update_job_skill(job_skill_id, job_skill)
        return {"success": True, "message": "Job skill updated successfully"}

    async def delete_job_skill(self, job_skill_id: JobSkillSchema):
        await self.repository.delete_job_skill(job_skill_id)
        return {"success": True, "message": "Job skill deleted successfully"}
