from app.repositories.learning_resource_repository import LearningResourceRepository
from app.services.common import CommonService
from app.schemas.learning_resource import (
    BaseResponseSchema,
    LearningResource,
    LearningResourceResponse,
)


class LearningResourceService:
    def __init__(self):
        self.repository = LearningResourceRepository()

    async def create_learning_resource(
        self, learning_resource: LearningResource, user_id: str
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
        await self.repository.create_learning_resource(learning_resource, user_id, )
        return {"message": "Learning resource created successfully", "success": True}

    async def get_learning_resources(
        self, user_id: str, learning_management: str
    ) -> list[LearningResourceResponse]:
        data = await self.repository.get_learning_resources(user_id, learning_management)
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
        self, learning_resource_id: str, learning_resource: LearningResource
    ) -> BaseResponseSchema:
        await self.repository.update_learning_resource(
            learning_resource_id, learning_resource
        )
        return {"message": "Learning resource updated successfully", "success": True}

    async def delete_learning_resource(
        self, learning_resource_id: str
    ) -> BaseResponseSchema:
        await self.repository.delete_learning_resource(learning_resource_id)
        return {"message": "Learning resource deleted successfully", "success": True}
