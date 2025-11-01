from fastapi import APIRouter, Depends

from app.schemas.learning_resource import (
    BaseResponseSchema,
    LearningResource,
    LearningResourceDetailResponse,
    LearningResourceListResponse,
)
from app.schemas.user import UserTokenDecodedData
from app.services.common import CommonService
from app.services.learning_resource import LearningResourceService

router = APIRouter(prefix="/learning-resources", tags=["Learning Resources"])


@router.get("/")
async def get_learning_resources(
    service: LearningResourceService = Depends(LearningResourceService),
    user_data: UserTokenDecodedData = Depends(CommonService.verify_token_get_user),
    learning_management: str = "",
) -> LearningResourceListResponse:
    return await service.get_learning_resources(user_data.id, learning_management)


@router.get("/{learning_resource_id}")
async def get_learning_resource_by_id(
    learning_resource_id: str,
    service: LearningResourceService = Depends(LearningResourceService),
) -> LearningResourceDetailResponse:
    return await service.get_learning_resource_by_id(learning_resource_id)


@router.post("/")
async def create_learning_resource(
    learning_resource: LearningResource,
    service: LearningResourceService = Depends(LearningResourceService),
    user_data: UserTokenDecodedData = Depends(CommonService.verify_token_get_user),
) -> BaseResponseSchema:
    return await service.create_learning_resource(learning_resource, user_data.id)


@router.put("/{learning_resource_id}")
async def update_learning_resource(
    learning_resource_id: str,
    learning_resource: LearningResource,
    service: LearningResourceService = Depends(LearningResourceService),
) -> BaseResponseSchema:
    return await service.update_learning_resource(
        learning_resource_id, learning_resource
    )


@router.delete("/{learning_resource_id}")
async def delete_learning_resource(
    learning_resource_id: str,
    service: LearningResourceService = Depends(LearningResourceService),
) -> BaseResponseSchema:
    return await service.delete_learning_resource(learning_resource_id)
