from fastapi import APIRouter, Depends

from app.schemas.learning_plan import (
    BaseResponseSchema,
    LearningPlanDetailResponse,
    LearningPlanListResponse,
    LearningPlanSchema,
)
from app.schemas.user import UserTokenDecodedData
from app.services.common import CommonService
from app.services.learning_plan import LearningPlanService

router = APIRouter(prefix="/learning-plans", tags=["Learning Plans"])


@router.get("/")
async def get_learning_plans(
    service: LearningPlanService = Depends(LearningPlanService),
    user_data: UserTokenDecodedData = Depends(CommonService.verify_token_get_user),
) -> LearningPlanListResponse:
    return await service.get_learning_plans(user_data.id)


@router.get("/{learning_plan_id}")
async def get_learning_plan_by_id(
    learning_plan_id: str, service: LearningPlanService = Depends(LearningPlanService)
) -> LearningPlanDetailResponse:
    return await service.get_learning_plan_by_id(learning_plan_id)


@router.post("/")
async def create_learning_plan(
    learning_plan: LearningPlanSchema,
    service: LearningPlanService = Depends(LearningPlanService),
    user_data: UserTokenDecodedData = Depends(CommonService.verify_token_get_user),
) -> BaseResponseSchema:
    return await service.create_learning_plan(learning_plan, user_data.id)


@router.put("/{learning_plan_id}")
async def update_learning_plan(
    learning_plan_id: str,
    learning_plan: LearningPlanSchema,
    service: LearningPlanService = Depends(LearningPlanService),
) -> BaseResponseSchema:
    return await service.update_learning_plan(learning_plan_id, learning_plan)


@router.delete("/{learning_plan_id}")
async def delete_learning_plan(
    learning_plan_id: str, service: LearningPlanService = Depends(LearningPlanService)
) -> BaseResponseSchema:
    return await service.delete_learning_plan(learning_plan_id)
