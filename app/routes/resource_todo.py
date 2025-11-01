from fastapi import APIRouter, Depends, Query

from app.services.resource_todo import ResourceTodoService
from app.schemas.common import BaseResponseSchema
from app.schemas.resource_todo import ResourceTodoListResponse, ResourceTodoDetailResponse, ResourceTodoUpdate, BaseResourceTodo
from app.schemas.user import UserTokenDecodedData
from app.services.common import CommonService
router = APIRouter()


@router.post("/todos", response_model=BaseResponseSchema, tags=["Resource Todos"])
async def create_todo(
    todo: BaseResourceTodo,
    user_data: UserTokenDecodedData = Depends(CommonService.verify_token_get_user),
    service: ResourceTodoService = Depends(ResourceTodoService),
) -> BaseResponseSchema:
    return await service.create_todo(todo, user_data)


@router.get("/todos", response_model=ResourceTodoListResponse, tags=["Resource Todos"])
async def get_todos(
    resource_id: str | None = Query(None, description="Filter todos by resource ID"),
    user_data: UserTokenDecodedData = Depends(CommonService.verify_token_get_user),
    service: ResourceTodoService = Depends(ResourceTodoService),
) -> ResourceTodoListResponse:
    return await service.get_todos(user_data, resource_id)


@router.get("/todos/{todo_id}", response_model= ResourceTodoDetailResponse, tags=["Resource Todos"])
async def get_todo_by_id(
    todo_id: str,
    user_data: UserTokenDecodedData = Depends(CommonService.verify_token_get_user),
    service: ResourceTodoService = Depends(ResourceTodoService),
) -> ResourceTodoDetailResponse:
    return await service.get_todo_by_id(todo_id, user_data)


@router.put("/todos/{todo_id}", response_model=BaseResponseSchema, tags=["Resource Todos"])
async def update_todo(
    todo_id: str,
    todo: ResourceTodoUpdate,
    user_data: UserTokenDecodedData = Depends(CommonService.verify_token_get_user),
    service: ResourceTodoService = Depends(ResourceTodoService),
) -> BaseResponseSchema:
    return await service.update_todo(todo_id, todo, user_data)


@router.delete("/todos/{todo_id}", response_model=BaseResponseSchema, tags=["Resource Todos"])
async def delete_todo(
    todo_id: str,
    user_data: UserTokenDecodedData = Depends(CommonService.verify_token_get_user),
    service: ResourceTodoService = Depends(ResourceTodoService),
) -> BaseResponseSchema:
    return await service.delete_todo(todo_id, user_data)
