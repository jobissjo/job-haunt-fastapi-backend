from bson import ObjectId
from datetime import datetime
from app.database import db
from app.schemas.resource_todo import BaseResourceTodo, ResourceTodoResponse, ResourceTodoUpdate
from typing import Optional

class ResourceTodoRepository:
    def __init__(self):
        self.collection = db.resource_todos

    async def create_todo(self, todo: BaseResourceTodo, user_id: str):
        await self.collection.insert_one(
            {
                **todo.model_dump(),
                "user_id": ObjectId(user_id),
                "resource_id": ObjectId(todo.resource_id),
                "created_at": datetime.now(),
            }
        )

    async def get_todos(self, user_id: str, resource_id:Optional[str] = None) -> list[ResourceTodoResponse]:
        documents = []
        filter = {"user_id": ObjectId(user_id)}
        if resource_id:
            filter["resource_id"] = ObjectId(resource_id)
        async for document in self.collection.find(filter):
            document["_id"] = str(document["_id"])
            document["user_id"] = str(document["user_id"])
            document["resource_id"] = str(document["resource_id"])
            documents.append(document)
        return documents

    async def get_todo_by_id(self, todo_id: str, user_id: str) -> ResourceTodoResponse:
        todo_response = await self.collection.find_one(
            {"_id": ObjectId(todo_id), "user_id": ObjectId(user_id)}
        )
        if todo_response is None:
            return None
        todo_response["_id"] = str(todo_response["_id"])
        todo_response["user_id"] = str(todo_response["user_id"])
        todo_response["resource_id"] = str(todo_response["resource_id"])
        return todo_response

    async def update_todo(self, todo_id: str, todo: ResourceTodoUpdate, user_id: str):
        await self.collection.update_one(
            {"_id": ObjectId(todo_id), "user_id": ObjectId(user_id)},
            {
                "$set": todo.model_dump(),
                
            },
        )

    async def delete_todo(self, todo_id: str, user_id: str):
        return await self.collection.delete_one(
            {"_id": ObjectId(todo_id), "user_id": ObjectId(user_id)}
        )
