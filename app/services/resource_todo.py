from fastapi import Depends, HTTPException

from app.repositories.resource_todo import ResourceTodoRepository
from app.schemas.common import BaseResponseSchema
from app.schemas.resource_todo import (
    BaseResourceTodo,
    ResourceTodoDetailResponse,
    ResourceTodoListResponse,
    ResourceTodoUpdate,
)
from app.schemas.user import UserTokenDecodedData
from app.services.common import CommonService


class ResourceTodoService:
    def __init__(self):
        self.repository = ResourceTodoRepository()

    async def create_todo(
        self,
        todo: BaseResourceTodo,
        user_data: UserTokenDecodedData = Depends(CommonService.verify_token_get_user),
    ) -> BaseResponseSchema:
        await self.repository.create_todo(todo, user_data.id)
        return BaseResponseSchema(success=True, message="Todo created successfully")

    async def get_todos(
        self,
        user_data: UserTokenDecodedData = Depends(CommonService.verify_token_get_user),
        resource_id: str | None = None,
    ) -> ResourceTodoListResponse:
        data = await self.repository.get_todos(user_data.id, resource_id)
        return ResourceTodoListResponse(
            data=data, success=True, message="Todos fetched successfully"
        )

    async def get_todo_by_id(
        self,
        todo_id: str,
        user_data: UserTokenDecodedData = Depends(CommonService.verify_token_get_user),
    ) -> ResourceTodoDetailResponse:
        data = await self.repository.get_todo_by_id(todo_id, user_data.id)
        return ResourceTodoDetailResponse(
            data=data, success=True, message="Todo fetched successfully"
        )

    async def update_todo(
        self,
        todo_id: str,
        todo: ResourceTodoUpdate,
        user_data: UserTokenDecodedData = Depends(CommonService.verify_token_get_user),
    ):
        is_todo_exists = await self.repository.get_todo_by_id(todo_id, user_data.id)
        if is_todo_exists is None:
            raise HTTPException(status_code=404, detail="Todo not found")
        await self.repository.update_todo(todo_id, todo, user_data.id)
        return BaseResponseSchema(success=True, message="Todo updated successfully")

    async def delete_todo(
        self,
        todo_id: str,
        user_data: UserTokenDecodedData = Depends(CommonService.verify_token_get_user),
    ):
        is_todo_exists = await self.repository.get_todo_by_id(todo_id, user_data.id)
        if is_todo_exists is None:
            raise HTTPException(status_code=404, detail="Todo not found")
        await self.repository.delete_todo(todo_id, user_data.id)
        return BaseResponseSchema(success=True, message="Todo deleted successfully")
