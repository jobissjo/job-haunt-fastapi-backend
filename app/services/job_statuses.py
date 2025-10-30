from app.repositories.job_status_repository import JobStatusRepository
from app.schemas.common import BaseResponseSchema
from app.schemas.job_status import (BaseJobStatus, JobStatusDetailResponse,
                                    JobStatusListResponse, JobStatusResponse)


class JobStatusService:
    def __init__(self):
        self.repository = JobStatusRepository()

    async def get_job_statuses(self) -> JobStatusListResponse:
        documents = await self.repository.get_job_status()
        return {
            "success": True,
            "data": documents,
            "message": "Job statuses retrieved successfully",
        }

    async def get_job_status_by_id(self, job_status_id) -> JobStatusDetailResponse:
        document = await self.repository.get_job_status_by_id(job_status_id)
        return {
            "success": True,
            "data": document,
            "message": "Job status retrieved successfully",
        }

    async def create_job_status(self, job_status: BaseJobStatus) -> BaseResponseSchema:
        await self.repository.create_job_status(job_status)
        return {
            "success": True,
            "message": "Job status created successfully",
        }

    async def update_job_status(self, job_status_id, job_status: BaseJobStatus) -> BaseResponseSchema:
        await self.repository.update_job_status(job_status_id, job_status)
        return {
            "success": True,
            "message": "Job status updated successfully",
        }

    async def delete_job_status(self, job_status_id: str) -> BaseResponseSchema:
        await self.repository.delete_job_status(job_status_id)
        return {"success": True, "message": "Job status deleted successfully"}
