from app.repositories.learning_plan_repository import LearningPlanRepository
from app.schemas.common import BaseResponseSchema
from app.schemas.learning_plan import (
    LearningPlanDetailResponse,
    LearningPlanListResponse,
    LearningPlanSchema,
)
from app.services.common import CommonService
from app.repositories.activity_log_repository import ActivityLogRepository
from app.schemas.activity_log_schema import ActivityLogSchema

class LearningPlanService:
    def __init__(self):
        self.repository = LearningPlanRepository()
        self.activity_log_repository = ActivityLogRepository()

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
        # Create activity log
        await self.activity_log_repository.create_activity_log(
            user_id,
            ActivityLogSchema(
                type="Learning Plan",
                message=f"Learning Plan created successfully for {learning_plan.name}"
            ),
        )
        return {"message": "Learning plan created successfully", "success": True}

    async def get_learning_plans(self, user_id: str) -> LearningPlanListResponse:
        data = await self.repository.get_learning_plans(user_id)
        return {
            "data": data,
            "message": "Learning plans fetched successfully",
            "success": True,
        }

    async def get_learning_plan_by_id(
        self, learning_plan_id: str, user_id: str
    ) -> LearningPlanDetailResponse:
        data = await self.repository.get_learning_plan_by_id(learning_plan_id, user_id)
        return {
            "data": data,
            "message": "Learning plan fetched successfully",
            "success": True,
        }

    async def update_learning_plan(
        self, learning_plan_id: str, learning_plan: LearningPlanSchema, user_id: str
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
        await self.repository.update_learning_plan(learning_plan_id, learning_plan, user_id)
        # Create activity log
        await self.activity_log_repository.create_activity_log(
            user_id,
            ActivityLogSchema(
                type="Learning Plan",
                message=f"Learning Plan updated successfully for {learning_plan.name}"
            ),
        )
        return {"message": "Learning plan updated successfully", "success": True}

    async def delete_learning_plan(self, learning_plan_id: str, user_id: str) -> BaseResponseSchema:
        data = await self.repository.get_learning_plan_by_id(learning_plan_id, user_id)
        learning_plan = None
        if data:
            learning_plan = data.get("name")
        await self.repository.delete_learning_plan(learning_plan_id, user_id)
        # Create activity log
        if learning_plan:
            await self.activity_log_repository.create_activity_log(
                user_id,
                ActivityLogSchema(
                    type="Learning Plan",
                    message=f"{learning_plan} Learning Plan deleted successfully"
                ),
            )
        return {"message": "Learning plan deleted successfully", "success": True}
