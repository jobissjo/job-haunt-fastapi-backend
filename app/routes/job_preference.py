from fastapi import APIRouter, Depends

from app.schemas.common import BaseResponseSchema
from app.schemas.job_preference import JobPreferenceBase, JobPreferenceDetailResponse
from app.schemas.user import UserTokenDecodedData
from app.services.common import CommonService
from app.services.job_preference import JobPreferenceService

router = APIRouter(prefix="/job-preferences", tags=["Job Preferences"])


@router.get("/")
async def get_job_preference_by_user_id(
    user_data: UserTokenDecodedData = Depends(CommonService.verify_token_get_user),
    service: JobPreferenceService = Depends(JobPreferenceService),
) -> JobPreferenceDetailResponse:
    return await service.get_job_preference_by_user_id(user_data.id)


@router.post("/")
async def create_job_preference(
    job_preference: JobPreferenceBase,
    user_data: UserTokenDecodedData = Depends(CommonService.verify_token_get_user),
    service: JobPreferenceService = Depends(JobPreferenceService),
) -> BaseResponseSchema:
    return await service.create_job_preference(job_preference, user_data.id)


@router.put("/{job_preference_id}")
async def update_job_preference(
    job_preference_id: str,
    job_preference: JobPreferenceBase,
    user_data: UserTokenDecodedData = Depends(CommonService.verify_token_get_user),
    service: JobPreferenceService = Depends(JobPreferenceService),
) -> BaseResponseSchema:
    return await service.update_job_preference(job_preference, user_data.id)
