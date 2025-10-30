from bson.objectid import ObjectId

from app.database import db
from app.schemas.learning_status import LearningStatusResponse, LearningStatusSchema


class LearningStatusRepository:
    def __init__(self):
        self.collection = db.learning_status

    async def create_learning_status(
        self, learning_status: LearningStatusSchema, user_id: str
    ) -> LearningStatusResponse:
        return await self.collection.insert_one(
            {**learning_status.model_dump(), "user_id": ObjectId(user_id)}
        )

    async def get_learning_status(self, user_id: str) -> list[LearningStatusResponse]:
        documents = []
        async for document in self.collection.find({"user_id": ObjectId(user_id)}):
            document["_id"] = str(document["_id"])
            documents.append(document)
        return documents

    async def get_learning_status_by_id(
        self, learning_status_id: str
    ) -> LearningStatusResponse:
        learning_status_response = await self.collection.find_one(
            {"_id": ObjectId(learning_status_id)}
        )
        learning_status_response["_id"] = str(learning_status_response["_id"])
        return learning_status_response

    async def update_learning_status(
        self, learning_status_id: str, learning_status: LearningStatusSchema
    ) -> None:
        await self.collection.update_one(
            {"_id": ObjectId(learning_status_id)},
            {"$set": learning_status.model_dump()},
        )

    async def delete_learning_status(self, learning_status_id: str):
        await self.collection.delete_one({"_id": ObjectId(learning_status_id)})
