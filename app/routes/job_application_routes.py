from fastapi import APIRouter, Depends, BackgroundTasks

from app.schemas.job_application import JobApplicationSchema
from app.schemas.job_application_automation import JobApplicationAutomationSchema
from app.schemas.user import UserTokenDecodedData
from app.services.common import CommonService
from app.services.job_application_service import JobApplicationService
from app.schemas.common import BaseResponseSchema


router = APIRouter(prefix="/job-applications", tags=["Job Applications"])


@router.post("/")
async def create_job_application(
    job_application: JobApplicationSchema,
    user_data: UserTokenDecodedData = Depends(CommonService.verify_token_get_user),
    service: JobApplicationService = Depends(JobApplicationService),
):
    return await service.create_job_application(
        job_application, user_data.id
    )


@router.get("/")
async def get_job_applications(
    user_data: UserTokenDecodedData = Depends(CommonService.verify_token_get_user),
    service: JobApplicationService = Depends(JobApplicationService),
):
    return await service.get_job_applications(user_data.id)


@router.get("/{job_application_id}")
async def get_job_application_by_id(job_application_id: str,
    service: JobApplicationService = Depends(JobApplicationService),
    user_data: UserTokenDecodedData = Depends(CommonService.verify_token_get_user),
):
    return await service.get_job_application_by_id(job_application_id, user_data.id)


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
    job_application_id: str, job_application: JobApplicationSchema,
    user_data: UserTokenDecodedData = Depends(CommonService.verify_token_get_user),
    service: JobApplicationService = Depends(JobApplicationService),
    
):
    return await service.update_job_application(
        job_application_id, job_application, user_data.id
    )

@router.post("/{job_application_id}/manual-mail-trigger")
async def manual_job_application_mail_trigger(
    job_application_id: str,
    background_tasks: BackgroundTasks,
    user_data: UserTokenDecodedData = Depends(CommonService.verify_token_get_user),
    service: JobApplicationService = Depends(JobApplicationService),
)->BaseResponseSchema:
    background_tasks.add_task(service.manual_job_application_mail_trigger, job_application_id, user_data)
    return {"success": True, "message": "Job application mail triggered successfully"}


@router.delete("/{job_application_id}")
async def delete_job_application(
    job_application_id: str,
    user_data: UserTokenDecodedData = Depends(CommonService.verify_token_get_user),
    service: JobApplicationService = Depends(JobApplicationService),
)->BaseResponseSchema:
    return await service.delete_job_application(job_application_id, user_data.id)
