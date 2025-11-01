from fastapi import APIRouter, Depends

from app.schemas.kanban_board import (
    KanbanBoardLearningPlanResponse,
    KanbanBoardLearningResourceResponse,
)
from app.schemas.user import UserTokenDecodedData
from app.services.common import CommonService
from app.services.kanban_board import KanbanBoardService

router = APIRouter(prefix="/kanban-board", tags=["Kanban Boards"])


@router.get("/learning-plans/")
async def get_kanban_board_learning_plans(
    user_data: UserTokenDecodedData = Depends(CommonService.verify_token_get_user),
    service: KanbanBoardService = Depends(KanbanBoardService),
) -> KanbanBoardLearningPlanResponse:
    return await service.get_kanban_board_learning_plans(user_data.id)


@router.get("/learning-resources/")
async def get_kanban_board_learning_resources(
    user_data: UserTokenDecodedData = Depends(CommonService.verify_token_get_user),
    service: KanbanBoardService = Depends(KanbanBoardService),
) -> KanbanBoardLearningResourceResponse:
    return await service.get_kanban_board_learning_resources(user_data.id)
