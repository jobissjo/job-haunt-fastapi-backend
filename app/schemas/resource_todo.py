from datetime import datetime
from typing import Optional
from pydantic import BaseModel, ConfigDict, Field

from app.schemas.common import BaseResponseSchema


class BaseResourceTodo(BaseModel):
    resource_id: str
    title: str
    is_completed: bool = False
    created_at: Optional[datetime] = Field(default_factory=datetime.now)


class ResourceTodoUpdate(BaseModel):
    # title: Optional[str] = None
    is_completed: Optional[bool] = None


class ResourceTodoResponse(BaseResourceTodo):
    id: str = Field(default_factory=str, alias="_id")
    user_id: str
    model_config = ConfigDict(populate_by_name=True)


class ResourceTodoListResponse(BaseResponseSchema):
    data: list[ResourceTodoResponse]


class ResourceTodoDetailResponse(BaseResponseSchema):
    data: ResourceTodoResponse
