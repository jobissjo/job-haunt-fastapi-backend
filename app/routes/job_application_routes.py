from fastapi import APIRouter, Depends

from app.schemas.job_application import JobApplicationSchema
from app.schemas.user import UserTokenDecodedData
from app.services.common import CommonService
from app.services.job_application_service import JobApplicationService
from app.schemas.job_application_automation import JobApplicationAutomationSchema

router = APIRouter(prefix="/job-applications", tags=["Job Applications"])


@router.post("/")
async def create_job_application(
    job_application: JobApplicationSchema,
    user_data: UserTokenDecodedData = Depends(CommonService.verify_token_get_user),
):
    return await JobApplicationService().create_job_application(
        job_application, user_data.id
    )


@router.get("/")
async def get_job_applications(
    user_data: UserTokenDecodedData = Depends(CommonService.verify_token_get_user),
):
    return await JobApplicationService().get_job_applications(user_data.id)


@router.get("/{job_application_id}")
async def get_job_application_by_id(job_application_id: str):
    return await JobApplicationService().get_job_application_by_id(job_application_id)

@router.post("/automation")
async def create_job_application_automation(
    job_application_automation: JobApplicationAutomationSchema,
    user_data: UserTokenDecodedData = Depends(CommonService.verify_token_get_user),
    service: JobApplicationService = Depends(JobApplicationService),
):
    return await service.create_job_application_automation(
        job_application_automation, user_data.id
    )


@router.put("/{job_application_id}")
async def update_job_application(
    job_application_id: str, job_application: JobApplicationSchema
):
    return await JobApplicationService().update_job_application(
        job_application_id, job_application
    )
