from fastapi import APIRouter, Depends

from app.schemas.job_status import JobStatusSchema
from app.services.job_statuses_service import JobStatusService

router = APIRouter(prefix="/job-statuses", tags=["Job Statuses"])


@router.get("/")
async def get_job_statuses(service: JobStatusService = Depends(JobStatusService)):
    return await service.get_job_statuses()


@router.get("/{job_status_id}")
async def get_job_status_by_id(
    job_status_id: str, service: JobStatusService = Depends(JobStatusService)
):
    return await service.get_job_status_by_id(job_status_id)


@router.post("/")
async def create_job_status(
    job_status: JobStatusSchema, service: JobStatusService = Depends(JobStatusService)
):
    return await service.create_job_status(job_status)


@router.put("/{job_status_id}")
async def update_job_status(
    job_status_id: str,
    job_status: JobStatusSchema,
    service: JobStatusService = Depends(JobStatusService),
):
    return await service.update_job_status(job_status_id, job_status)


@router.delete("/{job_status_id}")
async def delete_job_status(
    job_status_id: str, service: JobStatusService = Depends(JobStatusService)
):
    return await service.delete_job_status(job_status_id)
