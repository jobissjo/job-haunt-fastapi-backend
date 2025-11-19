from app.repositories.learning_resource_repository import LearningResourceRepository
from app.repositories.learning_plan_repository import LearningPlanRepository
from app.repositories.activity_log_repository import ActivityLogRepository
from app.schemas.learning_resource import (
    BaseResponseSchema,
    LearningResource,
    LearningResourceResponse,
)
from app.services.common import CommonService
from app.schemas.activity_log_schema import ActivityLogSchema
from fastapi import HTTPException


class LearningResourceService:
    def __init__(self):
        self.repository = LearningResourceRepository()
        self.activity_log_repository = ActivityLogRepository()
        self.learning_plan_repository = LearningPlanRepository()

    async def create_learning_resource(
        self, learning_resource: LearningResource, user_id: str
    ) -> BaseResponseSchema:
        learning_plan = await self.learning_plan_repository.get_learning_plan_by_id(
            learning_resource.learning_management, user_id
        )
        if not learning_plan:
            raise HTTPException(status_code=404, detail="Learning plan not found")
        learning_resource.expected_started_date = await CommonService.to_datetime(
            learning_resource.expected_started_date
        )
        learning_resource.expected_completed_date = await CommonService.to_datetime(
            learning_resource.expected_completed_date
        )
        learning_resource.actual_started_date = await CommonService.to_datetime(
            learning_resource.actual_started_date
        )
        learning_resource.actual_completed_date = await CommonService.to_datetime(
            learning_resource.actual_completed_date
        )
        await self.repository.create_learning_resource(
            learning_resource,
            user_id,
        )
        # ACTIVITY LOG
        await self.activity_log_repository.create_activity_log(
            user_id,
            ActivityLogSchema(
                type="learning resource",
                message=f" {learning_resource.name} (learning Resource) created under {learning_plan.get('name')}"
            ),
        )
        return {"message": "Learning resource created successfully", "success": True}

    async def get_learning_resources(
        self, user_id: str, learning_management: str
    ) -> list[LearningResourceResponse]:
        data = await self.repository.get_learning_resources(
            user_id, learning_management
        )
        return {
            "data": data,
            "message": "Learning resources fetched successfully",
            "success": True,
        }

    async def get_learning_resource_by_id(
        self, learning_resource_id: str
    ) -> LearningResourceResponse:
        data = await self.repository.get_learning_resource_by_id(learning_resource_id)
        return {
            "data": data,
            "message": "Learning resource fetched successfully",
            "success": True,
        }

    async def update_learning_resource(
        self, learning_resource_id: str, learning_resource: LearningResource,
        user_id: str
    ) -> BaseResponseSchema:
        learning_resource.expected_started_date = await CommonService.to_datetime(
            learning_resource.expected_started_date
        )
        learning_resource.expected_completed_date = await CommonService.to_datetime(
            learning_resource.expected_completed_date
        )
        learning_resource.actual_started_date = await CommonService.to_datetime(
            learning_resource.actual_started_date
        )
        learning_resource.actual_completed_date = await CommonService.to_datetime(
            learning_resource.actual_completed_date
        )
        await self.repository.update_learning_resource(
            learning_resource_id, learning_resource
        )
        # ACTIVITY LOG
        await self.activity_log_repository.create_activity_log(
            user_id,
            ActivityLogSchema(
                type="learning resource",
                message=f" {learning_resource.name} (learning Resource) updated"
            ),
        )
        return {"message": "Learning resource updated successfully", "success": True}

    async def delete_learning_resource(
        self, learning_resource_id: str, user_id: str
    ) -> BaseResponseSchema:
        learning_resource = await self.get_learning_resource_by_id(learning_resource_id)
        if not learning_resource:
            raise HTTPException(status_code=404, detail="Learning resource not found")
        learning_resource_name = learning_resource.get("name")
        await self.repository.delete_learning_resource(learning_resource_id)
        # ACTIVITY LOG
        await self.activity_log_repository.create_activity_log(
            user_id,
            ActivityLogSchema(
                type="learning resource",
                message=f" {learning_resource_name} (learning Resource) deleted"
            ),
        )
        return {"message": "Learning resource deleted successfully", "success": True}
