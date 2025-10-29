from fastapi import APIRouter, Depends

from app.schemas.job_skill import JobSkillSchema
from app.services.job_skills_service import JobSkillService

router = APIRouter(prefix="/job-skills", tags=["Job Skills"])


@router.get("/")
async def get_job_skills(service: JobSkillService = Depends(JobSkillService)):
    return await service.get_job_skills()


@router.get("/{job_skill_id}")
async def get_job_skill_by_id(
    job_skill_id: str, service: JobSkillService = Depends(JobSkillService)
):
    return await service.get_job_skill_by_id(job_skill_id)


@router.post("/")
async def create_job_skill(
    job_skill: JobSkillSchema, service: JobSkillService = Depends(JobSkillService)
):
    return await service.create_job_skill(job_skill)


@router.put("/{job_skill_id}")
async def update_job_skill(
    job_skill_id: str,
    job_skill: JobSkillSchema,
    service: JobSkillService = Depends(JobSkillService),
):
    return await service.update_job_skill(job_skill_id, job_skill)


@router.delete("/{job_skill_id}")
async def delete_job_skill(
    job_skill_id: str, service: JobSkillService = Depends(JobSkillService)
):
    return await service.delete_job_skill(job_skill_id)
