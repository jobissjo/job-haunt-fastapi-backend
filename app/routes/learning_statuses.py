from fastapi import APIRouter, Depends

from app.schemas.learning_status import (BaseResponseSchema,
                                         LearningStatusDetailResponse,
                                         LearningStatusListResponse,
                                         LearningStatusSchema)
from app.schemas.user import UserTokenDecodedData
from app.services.common import CommonService
from app.services.learning_statues import LearningStatusService

router = APIRouter(prefix="/learning-statuses", tags=["Learning Statuses"])

@router.get("/")
async def get_learning_statuses(service: LearningStatusService = Depends(LearningStatusService),
user_data:UserTokenDecodedData=Depends(CommonService.verify_token_get_user)) -> LearningStatusListResponse:
    return await service.get_learning_statuses(user_data.id)

@router.get("/{learning_status_id}")
async def get_learning_status_by_id(
    learning_status_id: str, service: LearningStatusService = Depends(LearningStatusService)
) -> LearningStatusDetailResponse:
    return await service.get_learning_status_by_id(learning_status_id)

@router.post("/")
async def create_learning_status(
    learning_status: LearningStatusSchema, service: LearningStatusService = Depends(LearningStatusService)
) -> BaseResponseSchema:
    return await service.create_learning_status(learning_status)

@router.put("/{learning_status_id}")
async def update_learning_status(
    learning_status_id: str,
    learning_status: LearningStatusSchema,
    service: LearningStatusService = Depends(LearningStatusService),
) -> BaseResponseSchema:
    return await service.update_learning_status(learning_status_id, learning_status)

@router.delete("/{learning_status_id}")
async def delete_learning_status(
    learning_status_id: str, service: LearningStatusService = Depends(LearningStatusService)
) -> BaseResponseSchema:
    return await service.delete_learning_status(learning_status_id)
