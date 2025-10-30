from app.repositories.learning_status_repository import \
    LearningStatusRepository
from app.schemas.learning_status import (BaseResponseSchema,
                                         LearningStatusDetailResponse,
                                         LearningStatusListResponse,
                                         LearningStatusSchema)


class LearningStatusService:
    def __init__(self):
        self.repository = LearningStatusRepository()
    
    async def create_learning_status(self, learning_status: LearningStatusSchema)->BaseResponseSchema:
        await self.repository.create_learning_status(learning_status)
        return {'message': 'Learning status created successfully', 'success': True}
    
    async def get_learning_statuses(self, user_id: str)->LearningStatusListResponse:
        data = await self.repository.get_learning_status(user_id)
        return {'data': data, 'message': 'Learning statuses fetched successfully', 'success': True}
    
    async def get_learning_status_by_id(self, learning_status_id: str)->LearningStatusDetailResponse:
        data = await self.repository.get_learning_status_by_id(learning_status_id)
        return {'data': data, 'message': 'Learning status fetched successfully', 'success': True}
    
    async def update_learning_status(self, learning_status_id: str, learning_status: LearningStatusSchema)->BaseResponseSchema:
        await self.repository.update_learning_status(learning_status_id, learning_status)
        return {'message': 'Learning status updated successfully', 'success': True}
    
    async def delete_learning_status(self, learning_status_id: str)->BaseResponseSchema:
        await self.repository.delete_learning_status(learning_status_id)
        return {'message': 'Learning status deleted successfully', 'success': True}