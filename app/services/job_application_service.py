from app.repositories.job_application_automation import (
    JobApplicationAutomationRepository,
)
from app.repositories.job_application_repository import JobApplicationRepository
from app.schemas.common import BaseResponseSchema
from app.schemas.job_application import (
    JobApplicationDetailResponse,
    JobApplicationListResponse,
    JobApplicationSchema,
)
from app.schemas.job_application_automation import JobApplicationAutomationSchema
from app.services.common import CommonService
from app.utils.email_utils import EmailUtils
from app.repositories.user_email_settings_repository import UserEmailSettingsRepository
from fastapi import HTTPException
from app.schemas.user import UserTokenDecodedData

class JobApplicationService:
    def __init__(self):
        self.repository = JobApplicationRepository()
        self.job_application_automation_repository = (
            JobApplicationAutomationRepository()
        )
        self.user_email_settings_repository = UserEmailSettingsRepository()

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
        job_application_id = await self.repository.create_job_application(
            job_application, user_id
        )
        return {
            "success": True,
            "message": "Job application created successfully",
            "data": {"_id": str(job_application_id)},
        }

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
        job_application.applied_date = await CommonService.to_datetime(
            job_application.applied_date
        )
        job_application.job_posted_date = await CommonService.to_datetime(
            job_application.job_posted_date
        )
        job_application.job_closed_date = await CommonService.to_datetime(
            job_application.job_closed_date
        )
        await self.repository.update_job_application(
            job_application_id, job_application
        )
        return {"success": True, "message": "Job application updated successfully"}

    async def delete_job_application(self, job_application_id) -> BaseResponseSchema:
        await self.repository.delete_job_application(job_application_id)
        return {"success": True, "message": "Job application deleted successfully"}

    async def create_job_application_automation(
        self, job_application_automation: JobApplicationAutomationSchema, user_id: str
    ):
        job_application_automation_id = await self.job_application_automation_repository.create_job_application_automation(
            job_application_automation, user_id
        )
        return {
            "success": True,
            "message": "Job application automation created successfully",
            "data": {"_id": str(job_application_automation_id)},
        }

    async def manual_job_application_mail_trigger(self, job_application_id: str, user_data: UserTokenDecodedData)->None:
        job_application = await self.repository.get_job_application_by_id(job_application_id)
        if not job_application:
            raise HTTPException(status_code=404, detail="Job application not found")
        email_setting = await self.user_email_settings_repository.get_active_email_setting(user_data.id)
        if not email_setting:
            raise HTTPException(status_code=404, detail="Email setting not found")
        if not job_application.contact_mail:
            raise HTTPException(status_code=404, detail="Contact mail not found in job application")
        if job_application.application_through not in {'email'}:
            raise HTTPException(status_code=404, detail="Job application not through email, so not able to send mail") 
        await EmailUtils.send_mail(
            user_id=user_data.id,
            email_setting=email_setting,
            to_email=job_application.contact_mail,
            subject=job_application.position,
            template_name="job_application.html",
            template_data={
                **job_application.model_dump(),

            },
            job_application_id=job_application_id,
        )
        
    
