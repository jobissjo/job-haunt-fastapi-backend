from app.repositories.learning_plan_repository import LearningPlanRepository
from app.schemas.common import BaseResponseSchema
from app.schemas.learning_plan import (
    LearningPlanDetailResponse,
    LearningPlanListResponse,
    LearningPlanSchema,
)
from app.services.common import CommonService


class LearningPlanService:
    def __init__(self):
        self.repository = LearningPlanRepository()

    async def create_learning_plan(
        self, learning_plan: LearningPlanSchema, user_id: str
    ) -> BaseResponseSchema:
        learning_plan.expected_started_date = await CommonService.to_datetime(
            learning_plan.expected_started_date
        )
        learning_plan.expected_completed_date = await CommonService.to_datetime(
            learning_plan.expected_completed_date
        )
        learning_plan.actual_started_date = await CommonService.to_datetime(
            learning_plan.actual_started_date
        )
        learning_plan.actual_completed_date = await CommonService.to_datetime(
            learning_plan.actual_completed_date
        )
        await self.repository.create_learning_plan(learning_plan, user_id)
        return {"message": "Learning plan created successfully", "success": True}

    async def get_learning_plans(self, user_id: str) -> LearningPlanListResponse:
        data = await self.repository.get_learning_plans(user_id)
        return {
            "data": data,
            "message": "Learning plans fetched successfully",
            "success": True,
        }

    async def get_learning_plan_by_id(
        self, learning_plan_id: str
    ) -> LearningPlanDetailResponse:
        data = await self.repository.get_learning_plan_by_id(learning_plan_id)
        return {
            "data": data,
            "message": "Learning plan fetched successfully",
            "success": True,
        }

    async def update_learning_plan(
        self, learning_plan_id: str, learning_plan: LearningPlanSchema
    ) -> BaseResponseSchema:
        learning_plan.expected_started_date = await CommonService.to_datetime(
            learning_plan.expected_started_date
        )
        learning_plan.expected_completed_date = await CommonService.to_datetime(
            learning_plan.expected_completed_date
        )
        learning_plan.actual_started_date = await CommonService.to_datetime(
            learning_plan.actual_started_date
        )
        learning_plan.actual_completed_date = await CommonService.to_datetime(
            learning_plan.actual_completed_date
        )
        await self.repository.update_learning_plan(learning_plan_id, learning_plan)
        return {"message": "Learning plan updated successfully", "success": True}

    async def delete_learning_plan(self, learning_plan_id: str) -> BaseResponseSchema:
        await self.repository.delete_learning_plan(learning_plan_id)
        return {"message": "Learning plan deleted successfully", "success": True}
