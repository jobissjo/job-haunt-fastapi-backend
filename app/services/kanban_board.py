from app.repositories.learning_status_repository import LearningStatusRepository
from app.schemas.kanban_board import (
    KanbanBoardLearningResourceResponse,
    KanbanBoardLearningPlanResponse,
)


class KanbanBoardService:
    def __init__(self):
        self.learning_status_repository = LearningStatusRepository()

    async def get_kanban_board_learning_resources(
        self, user_id: str
    ) -> KanbanBoardLearningResourceResponse:
        data = await self.learning_status_repository.get_learning_status_with_resources(
            user_id
        )
        print(data, 'data')
        return KanbanBoardLearningResourceResponse(
            data=data,
            message="Learning Resources fetched successfully",
            success=True,
        )

    async def get_kanban_board_learning_plans(
        self, user_id: str
    ) -> KanbanBoardLearningPlanResponse:
        data = await self.learning_status_repository.get_learning_status_with_plans(
            user_id
        )
        print(data, 'data')
        return KanbanBoardLearningPlanResponse(
            data=data, message="Learning Plans fetched successfully", success=True,
        )
