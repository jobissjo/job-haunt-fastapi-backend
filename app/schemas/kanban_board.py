from pydantic import BaseModel

from app.schemas.common import BaseResponseSchema
from app.schemas.learning_plan import LearningPlanResponse
from app.schemas.learning_resource import LearningResourceResponse
from app.schemas.learning_status import LearningStatusResponse


class KanbanBoardLearningResource(LearningStatusResponse):
    learning_resources: list[LearningResourceResponse]


class KanbanBoardLearningPlan(LearningStatusResponse):
    learning_plans: list[LearningPlanResponse]


class KanbanBoardLearningResourceResponse(BaseResponseSchema):
    data: list[KanbanBoardLearningResource]


class KanbanBoardLearningPlanResponse(BaseResponseSchema):
    data: list[KanbanBoardLearningPlan]
