from app.repositories.job_application_repository import JobApplicationRepository
from app.repositories.job_application_automation import JobApplicationAutomationRepository
from app.schemas.common import BaseResponseSchema
from app.schemas.job_application import (
    JobApplicationDetailResponse,
    JobApplicationListResponse,
    JobApplicationSchema,
)
from app.services.common import CommonService
from app.schemas.job_application_automation import JobApplicationAutomationSchema


class JobApplicationService:
    def __init__(self):
        self.repository = JobApplicationRepository()
        self.job_application_automation_repository = JobApplicationAutomationRepository()

    async def create_job_application(
        self, job_application: JobApplicationSchema, user_id: str
    ) -> None:
        job_application.applied_date = await CommonService.to_datetime(
            job_application.applied_date
        )
        job_application.job_posted_date = await CommonService.to_datetime(
            job_application.job_posted_date
        )
        job_application.job_closed_date = await CommonService.to_datetime(
            job_application.job_closed_date
        )
        job_application_id = await self.repository.create_job_application(job_application, user_id)
        return {"success": True, "message": "Job application created successfully", 'data': {'_id': str(job_application_id)}}

    async def get_job_applications(self, user_id: str) -> JobApplicationListResponse:
        data = await self.repository.get_job_applications(user_id)
        return {
            "success": True,
            "data": data,
            "message": "Job applications retrieved successfully",
        }

    async def get_job_application_by_id(
        self, job_application_id: str
    ) -> JobApplicationDetailResponse:
        data = await self.repository.get_job_application_by_id(job_application_id)
        return {
            "success": True,
            "data": data,
            "message": "Job application retrieved successfully",
        }

    async def update_job_application(
        self, job_application_id: str, job_application: JobApplicationSchema
    ) -> BaseResponseSchema:
        await self.repository.update_job_application(
            job_application_id, job_application
        )
        return {"success": True, "message": "Job application updated successfully"}

    async def delete_job_application(self, job_application_id) -> BaseResponseSchema:
        await self.repository.delete_job_application(job_application_id)
        return {"success": True, "message": "Job application deleted successfully"}
    
    async def create_job_application_automation(
        self, job_application_automation: JobApplicationAutomationSchema, user_id: str
    ) :
        job_application_automation_id = await self.job_application_automation_repository.create_job_application_automation(
            job_application_automation, user_id
        )
        return {"success": True, "message": "Job application automation created successfully", 'data': {'_id': str(job_application_automation_id)}}
